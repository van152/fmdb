#!/usr/bin/env python3
"""t160_lang_roundtrip — lang_db_2400.dat + lang_update_db.dat lossless re-pack + varlen string patch.

Reuses scripts/t143_lang_db.py for FMF/Zstd container parsing and row grammar.
Supports:
  --selftest : lossless re-encode of all members (diff == 0, byte-exact)
  --patch    : apply (language_id, entity_table, dbid) -> new_translation patches
               then verify via t143 decode readback

Usage:
  py -V:3.12 -B scripts/t160_lang_roundtrip.py --selftest
  py -V:3.12 -B scripts/t160_lang_roundtrip.py --patch LID,TID,DBID,"new text" --out DIR
"""
from __future__ import annotations

import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import hashlib
import io
import json
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(_cfg.VENDOR_DIR))
sys.path.insert(0, str(_cfg.ROOT / "scripts"))
import zstandard as zstd  # noqa: E402

import t143_lang_db as t143  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch/t160/out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

U32 = struct.Struct('<I')
U16 = struct.Struct('<H')
U64 = struct.Struct('<Q')

DAT_MAGIC = b"\x03\x01tad."
FMF_MAGIC = bytes.fromhex("0201666d662e080000")
ZSTD_MAGIC = bytes.fromhex("28b52ffd")

# (language_id, table_type, dbid, new_text) patch specs for selftest demonstration.
# Simplified Chinese (1000002), table 21 (stadium names), real dbid 600 = "迪恩考特球场".
DEFAULT_PATCHES = [
    (1000002, 21, 600, "测试球场"),   # Simplified Chinese stadium rename
]

LANG_DB_DAT = _cfg.INPUT_DIR / "lang_db_2400.dat"
LANG_UPDATE_DAT = ROOT / "scratch/data/lang_update_db.dat"

SOURCES = (
    ("lang_db_2400", LANG_DB_DAT, "lang_db", 0x0DEF),
    ("lang_update_db", LANG_UPDATE_DAT, "lang_update_db", 0x0DF1),
)


# ---------------------------------------------------------------------------
# FMF directory writer (inverse of t112._DirectoryReader)
# ---------------------------------------------------------------------------
def _emit_string(buf: bytearray, s: str) -> None:
    b = s.encode("utf-8")
    buf.extend(U32.pack(len(b)))
    buf.extend(b)


def build_fmf_directory(folder: str, members: list[dict]) -> bytes:
    """Build the FMF directory blob (uncompressed) for one archive.

    members: list of dicts with keys path, offset, packed_size, size.
    Path format: "{folder}/{lid}_{tid}.dat" or "{folder}/{lid}_person_names.dat".
    Directory tree: root(folder) -> N files directly (flat, no subdirs).
    Each file record: name, ext, offset(u64), packed(u64), size(u64), 0, 0.
    """
    buf = bytearray()
    # Root folder: name = folder, file count = N, subdirectory count = 0.
    _emit_string(buf, folder)
    buf.extend(U32.pack(len(members)))
    for m in members:
        name, ext = m["path"].rsplit("/", 1)[1].rsplit(".", 1)
        _emit_string(buf, name)
        _emit_string(buf, "." + ext)
        buf.extend(U64.pack(m["offset"]))
        buf.extend(U64.pack(m["packed_size"]))
        buf.extend(U64.pack(m["size"]))
        buf.extend(U64.pack(0))  # reserved t1
        buf.extend(U64.pack(0))  # reserved t2
    buf.extend(U32.pack(0))  # no subdirectories
    return bytes(buf)


def compress_member(data: bytes, level: int = 3) -> bytes:
    """Zstd-compress a single member payload (one frame)."""
    cctx = zstd.ZstdCompressor(level=level, write_checksum=True, write_content_size=False)
    return cctx.compress(data)


# ---------------------------------------------------------------------------
# Member re-encode with string patching
# ---------------------------------------------------------------------------
def _string_slots(layout: str) -> list[int]:
    """Indices of 'S' (string) tokens in the layout, in order."""
    return [i for i, t in enumerate(layout) if t == "S"]


def reencode_entity_member(raw: bytes, tid: int, header: bytes,
                           patch: dict | None) -> bytes:
    """Re-encode an entity-table member (tid is not None).

    patch: {dbid: new_text} applied to the first 'S' slot of the matching row.
    Returns the rebuilt decompressed member bytes.
    """
    layout = t143.LAYOUTS[tid]
    out = bytearray(header)
    out.extend(U32.pack(0))  # declared count, patched below
    p = t143.Cursor(raw, 8)
    (declared,) = p.unpack(U32)
    rows = []
    for _ in range(declared):
        (key,) = p.unpack(U32)
        fields = []
        for token in layout:
            if token == "S":
                fields.append(p.string())
            elif token == "B":
                fields.append(p.byte())
            elif token == "H":
                fields.append(p.unpack(U16)[0])
            elif token == "V":
                fields.append(p.variants())
        rows.append((key, fields))
    check = p.p
    # Apply patch: first row matching dbid, first string slot.
    if patch is not None:
        for key, fields in rows:
            if key in patch:
                sidx = _string_slots(layout)
                if sidx:
                    fields[sidx[0]] = patch[key]
                break
    # Re-emit.
    out = bytearray(header)
    out.extend(U32.pack(declared))
    for key, fields in rows:
        t143.emit_row(key, fields, layout, out)
    return bytes(out)


def reencode_person_names_member(raw: bytes, tid: None, header: bytes,
                                 patch: dict | None) -> bytes:
    """Re-encode a person_names member (tid is None).

    patch: {dbid: new_text} — person_names rows are text-keyed (first string is the key);
           we match the key string against patch keys (interpreted as text keys, not u32).
    """
    out = bytearray(header)
    p = t143.Cursor(raw, 8)
    end = len(raw) - 4
    rows = []
    while raw[p.p:p.p + 4] != t143.ZERO:
        slots = (p.string(), p.string(), p.string(), p.string())
        tail = p.unpack(t143.PERSON_TAIL)
        rows.append((slots, tail))
    # Apply patch: match first slot (key) against patch keys (as text).
    if patch is not None:
        for slots, _ in rows:
            if slots[0] in patch:
                slots = (patch[slots[0]], slots[1], slots[2], slots[3])
                break
    # Re-emit.
    for slots, tail in rows:
        for s in slots:
            t143.emit_string(s, out)
        out.extend(t143.PERSON_TAIL.pack(*tail))
    out.extend(t143.ZERO)
    return bytes(out)


def reencode_member(raw: bytes, tid, header: bytes, patch: dict | None) -> bytes:
    """Re-encode a single decompressed member, optionally applying a string patch."""
    if tid is None:
        return reencode_person_names_member(raw, tid, header, patch)
    return reencode_entity_member(raw, tid, header, patch)


def build_dat_blob(version: int, members: list[dict], folder: str) -> bytes:
    """Build a complete .dat file from member payloads (decompressed bytes).

    members: list of dicts {path, data} where data is the full decompressed member
    (including the 8-byte member header MAGIC + u16 version).
    Returns the .dat file bytes.
    """
    cctx = zstd.ZstdCompressor(level=3, write_checksum=True, write_content_size=False)

    # Compress each member, compute packed_size.
    comp = []
    for m in members:
        frame = cctx.compress(m["data"])
        comp.append({
            "path": m["path"],
            "data": m["data"],
            "packed": frame,
            "packed_size": len(frame),
            "size": len(m["data"]),
        })

    # Lay out data region contiguously starting at data_base.
    # FMF layout: 8-byte DAT shell + FMF header(9B) + dir_size(u64) + data_base(u64)
    #           + data region + TOC(FMF magic + compressed directory).
    #   archive_layout reads: base = 8 + 9 + u64_at(25); toc = 8 + 9 + u64_at(17).
    #   So u64_at(25) = data_base - 17, u64_at(17) = toc_offset - 17.
    dat_shell = DAT_MAGIC + U16.pack(version)
    data_base_abs = 8 + 26  # absolute file offset of data region (8 shell + 9 FMF + 8 + 8)
    offset = 0
    for c in comp:
        c["offset"] = offset
        offset += c["packed_size"]

    toc_offset = data_base_abs + offset  # end of data region = start of TOC

    # Build uncompressed directory.
    dir_entries = []
    for c in comp:
        dir_entries.append({
            "path": c["path"],
            "offset": c["offset"],
            "packed_size": c["packed_size"],
            "size": c["size"],
        })
    dir_blob = build_fmf_directory(folder, dir_entries)

    # Compress directory.
    dir_comp = cctx.compress(dir_blob)
    dir_size = toc_offset - (8 + 9)  # u64 at [17:25]

    # Assemble.  FMF header is 8+9+8+8 = 33 bytes, but data_base (orig file)
    # points at offset 34 — there is 1 pad byte at offset 33 before the first
    # zstd frame.  Replicate that layout.
    out = bytearray()
    out.extend(dat_shell)                                  # 8 bytes [0:8]
    out.extend(FMF_MAGIC)                                  # 9 bytes [8:17]
    out.extend(U64.pack(dir_size))                         # u64 [17:25]
    out.extend(U64.pack(data_base_abs - 17))               # u64 [25:33]
    out.append(0)                                          # pad byte [33:34]
    for c in comp:                                         # data region [34:...]
        out.extend(c["packed"])
    out.extend(FMF_MAGIC)                                  # secondary FMF magic at TOC
    out.extend(dir_comp)                                   # compressed directory
    return bytes(out)


# ---------------------------------------------------------------------------
# Roundtrip test: lossless re-encode of all members (diff == 0)
# ---------------------------------------------------------------------------
def roundtrip_test() -> dict:
    """Verify every member of both archives re-encodes byte-exact (diff == 0)."""
    results: dict = {"archives": {}, "all_diff_zero": True, "all_byte_exact": True,
                     "member_count": 0, "diff_zero_count": 0}
    for label, path, folder, version in SOURCES:
        if not path.is_file():
            results["archives"][label] = {"error": f"missing {path}"}
            results["all_diff_zero"] = False
            continue
        ar = t143.LanguageArchive((label, path, folder, version))
        members = []
        for (lid, tid), e in sorted(ar.entries.items(), key=lambda kv: (kv[0][0], kv[0][1] is not None, kv[0][1] if kv[0][1] is not None else -1)):
            raw = ar.payload(e)
            m = t143.decode(raw, tid, ar.header, roundtrip=True)
            members.append({
                "language_id": lid, "table_type": tid,
                "path": e["path"], "offset": e["offset"],
                "records": m["records"], "diff": m["diff"],
                "byte_exact": m["byte_exact"],
                "decompressed_bytes": m["decoded_end"],
            })
            results["member_count"] += 1
            if m["diff"] != 0:
                results["all_diff_zero"] = False
            if m["byte_exact"] is not True:
                results["all_byte_exact"] = False
        results["archives"][label] = {
            "file": str(path), "file_bytes": len(ar.data),
            "sha256": hashlib.sha256(ar.data).hexdigest(),
            "version": hex(version),
            "member_count": len(ar.entries),
            "diff_zero_count": sum(1 for m_ in members if m_["diff"] == 0),
            "byte_exact_count": sum(1 for m_ in members if m_["byte_exact"] is True),
            "members": members,
        }
    results["all_diff_zero"] = results["all_diff_zero"] and results["member_count"] > 0
    results["all_byte_exact"] = results["all_byte_exact"] and results["member_count"] > 0
    return results


# ---------------------------------------------------------------------------
# Patch API
# ---------------------------------------------------------------------------
def parse_patch_spec(spec: str) -> tuple[int, int, int, str]:
    """Parse 'LID,TID,DBID,new_text' -> (lid, tid, dbid, new_text)."""
    parts = spec.split(",", 3)
    if len(parts) != 4:
        raise ValueError(f"invalid patch spec '{spec}': expected LID,TID,DBID,new_text")
    return int(parts[0]), int(parts[1]), int(parts[2]), parts[3]


def apply_patches_and_repack(patch_specs: list[str], out_path: Path) -> dict:
    """Apply patches, rebuild .dat, then read back via t143 to verify.

    Returns a dict with before/after comparison for each patched term.
    """
    patches: dict[tuple[int, int], dict[int, str]] = {}
    for spec in patch_specs:
        lid, tid, dbid, new_text = parse_patch_spec(spec)
        patches.setdefault((lid, tid), {})[dbid] = new_text

    before_texts: list[dict] = []
    rebuilt_members: dict[str, list[dict]] = {}

    for label, path, folder, version in SOURCES:
        if not path.is_file():
            raise FileNotFoundError(f"missing source {path}")
        ar = t143.LanguageArchive((label, path, folder, version))
        members_out = []
        for (lid, tid), e in sorted(ar.entries.items(), key=lambda kv: (kv[0][0], kv[0][1] is not None, kv[0][1] if kv[0][1] is not None else -1)):
            raw = ar.payload(e)
            patch = None
            key_patch = None
            for _pk, _pv in patches.items():
                if _pk[0] == lid and _pk[1] == tid:
                    key_patch = _pv
                    break
            if key_patch is not None:

                def _capture(key, offset, fields, _kp=key_patch, _lid=lid, _tid=tid):
                    if key in _kp:
                        sidx = _string_slots(t143.LAYOUTS[_tid])
                        if sidx:
                            before_texts.append({
                                "language_id": _lid, "table_type": _tid, "dbid": key,
                                "slot_index": sidx[0],
                                "before": fields[sidx[0]],
                                "after": _kp[key],
                            })

                t143.decode(raw, tid, ar.header, visit=_capture)
                patch = key_patch
            new_raw = reencode_member(raw, tid, ar.header, patch)
            check_ok = t143.decode(new_raw, tid, ar.header, roundtrip=True)
            if check_ok["diff"] != 0:
                raise ValueError(f"{e['path']}: patched re-encode diff={check_ok['diff']}")
            members_out.append({"path": e["path"], "data": new_raw})
        rebuilt_members[label] = members_out

    # Write repacked .dat files.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for label, path, folder, version in SOURCES:
        members = [{"path": m["path"], "data": m["data"]} for m in rebuilt_members[label]]
        blob = build_dat_blob(version, members, folder)
        out_file = out_path / f"{label}_patched.dat"
        out_file.write_bytes(blob)
        written.append({
            "label": label, "out_file": str(out_file),
            "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest(),
        })

    # Read back patched files via t143 and verify after values.
    # Collect ALL after_texts across all written archives before comparing.
    all_after_texts: dict[tuple[int, int, int], str] = {}
    for entry in written:
        label = entry["label"]
        src = next(s for s in SOURCES if s[0] == label)
        ar = t143.LanguageArchive((label, Path(entry["out_file"]), src[2], src[3]))
        for (lid, tid), e in sorted(ar.entries.items(), key=lambda kv: (kv[0][0], kv[0][1] is not None, kv[0][1] if kv[0][1] is not None else -1)):
            key_patch = None
            for _pk, _pv in patches.items():
                if _pk[0] == lid and _pk[1] == tid:
                    key_patch = _pv
                    break

            def _readback(key, offset, fields, _kp=key_patch, _lid=lid, _tid=tid):
                if key in _kp:
                    sidx = _string_slots(t143.LAYOUTS[_tid])
                    if sidx:
                        all_after_texts[(_lid, _tid, key)] = fields[sidx[0]]

            if key_patch is None:
                continue

            t143.decode(ar.payload(e), tid, ar.header, visit=_readback)

    readback = []
    for bt in before_texts:
        key = (bt["language_id"], bt["table_type"], bt["dbid"])
        after_val = all_after_texts.get(key)
        readback.append({
            "language_id": bt["language_id"], "table_type": bt["table_type"],
            "dbid": bt["dbid"], "slot_index": bt["slot_index"],
            "before": bt["before"], "after": after_val,
            "match": after_val == bt["after"],
        })

    all_match = len(readback) > 0 and all(r["match"] for r in readback)
    return {
        "patches": [{"language_id": p[0], "table_type": p[1], "dbid": p[2], "new_text": p[3]}
                    for p in [parse_patch_spec(s) for s in patch_specs]],
        "written": written,
        "readback": readback,
        "all_match": all_match,
    }


# ---------------------------------------------------------------------------
# Selftest + report
# ---------------------------------------------------------------------------
def selftest() -> dict:
    t0 = time.time()
    rt = roundtrip_test()
    # Use a real-world patch: Simplified Chinese, table 21 (club short-name-like),
    # well-known dbid 23397138 (seen in t143 SHOWCASE for tid=25). Use table 21.
    patch_specs = [f"{lid},{tid},{dbid},{text}" for (lid, tid, dbid, text) in DEFAULT_PATCHES]
    pt = apply_patches_and_repack(patch_specs, OUT_DIR)
    ok = rt["all_diff_zero"] and rt["all_byte_exact"] and pt["all_match"]
    return {
        "pass": ok,
        "status": "complete" if ok else "failed",
        "elapsed_sec": round(time.time() - t0, 2),
        "roundtrip": rt,
        "patch": pt,
    }


def write_report(doc: dict) -> None:
    rt = doc["roundtrip"]
    pt = doc["patch"]
    lines = [
        "# t160: lang_db_2400.dat + lang_update_db.dat 双向修改重打包引擎",
        "",
        f"- status: **{doc.get('status')}**",
        f"- 成员总数: {rt['member_count']} (2 个归档 × 22 语种 × 16 成员)",
        f"- 无损重编码 diff=0: {'是' if rt['all_diff_zero'] else '否'}",
        f"- 字节精确闭合: {'是' if rt['all_byte_exact'] else '否'}",
        f"- 变长译名修补: {'全部生效' if pt['all_match'] else '失败'}",
        f"- 耗时: {doc['elapsed_sec']}s",
        "",
        "## 归档无损校验",
        "",
        "| 归档 | 文件 | 成员 | diff=0 | byte-exact | SHA-256 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for label, ar in rt["archives"].items():
        if "error" in ar:
            lines.append(f"| `{label}` | {ar['error']} | - | - | - | - |")
        else:
            lines.append(f"| `{label}` | `{ar['file']}` | {ar['member_count']} | "
                         f"{ar['diff_zero_count']} | {ar['byte_exact_count']} | `{ar['sha256'][:16]}...` |")
    lines += [
        "",
        "## 变长译名修补前后回读对比",
        "",
        "| 语言ID | 表类型 | DBID | 槽位 | 修改前 | 修改后 | 匹配 |",
        "|---:|---:|---:|---:|---|---|---:|",
    ]
    for r in pt["readback"]:
        lines.append(f"| {r['language_id']} | {r['table_type']} | {r['dbid']} | {r['slot_index']} | "
                     f"{r['before']} | {r['after']} | {int(r['match'])} |")
    lines += [
        "",
        f"- 重打包文件: {[w['out_file'] for w in pt['written']]}",
        f"- 所有补丁精确生效: {pt['all_match']}",
        "",
        f"- 总耗时: {doc['elapsed_sec']}s  pass={doc['pass']}",
    ]
    (OUT_DIR / "lang_roundtrip_report.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "DONE.md").write_text(
        "DONE type=lang_roundtrip\n"
        f"status={doc.get('status')}\n"
        f"roundtrip_all_diff_zero={rt['all_diff_zero']}\n"
        f"roundtrip_all_byte_exact={rt['all_byte_exact']}\n"
        f"member_count={rt['member_count']}\n"
        f"patch_all_match={pt['all_match']}\n"
        f"elapsed_sec={doc['elapsed_sec']}\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description="lang_db_2400.dat + lang_update_db.dat lossless re-pack + varlen string patch")
    ap.add_argument("--selftest", action="store_true",
                    help="lossless re-encode of all members (diff == 0, byte-exact)")
    ap.add_argument("--patch", metavar="SPEC", action="append",
                    help='patch spec "LID,TID,DBID,new_text" (repeatable)')
    ap.add_argument("--out", metavar="DIR", default=str(OUT_DIR),
                    help=f"output directory (default: {OUT_DIR})")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.selftest:
        doc = selftest()
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        print("SELFTEST:", "PASS" if doc["pass"] else "FAIL", flush=True)
        write_report(doc)
        return 0 if doc["pass"] else 1
    if args.patch:
        pt = apply_patches_and_repack(args.patch, out_dir)
        print(json.dumps(pt, ensure_ascii=False, indent=2))
        print("PATCH:", "OK" if pt["all_match"] else "FAIL", flush=True)
        return 0 if pt["all_match"] else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())


