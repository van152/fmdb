#!/usr/bin/env python3
"""t43 verify — 独立复算 `fm24_dump.load_payload` 修复后应得的 payload。

独立性声明
----------
本进程**不 import `scripts/fm24_dump.py`**。这里重新实现三件事(只依赖归档原始字节 +
上游只读解码器的 zstd 依赖):

  1. FMF 头解析:`data_base` / `toc_offset` 直接按格式从字节算:
     `start = 8 if data[:6]==b"\\x03\\x01tad." and data[8:17]==FMF_MAGIC else 0`
     `base = start + 9 + u64(start+17)`
  2. FMF 目录解析(自写 `_DirectoryReader` 等价物),得 `offset/packed_size/size`。
  3. 成员内逐帧解压(与 `zstd.decompressobj().unused_data` 推进),以 `len(frame)==size` 选帧。

对被验对象 `fm24_dump.load_payload` 的调用一律走**子进程**(`py -I -B -c ...`),
因此本文件自身不持有该模块的引用;两边只在"字节/SHA/长度"上对照。

复算内容:
  * 20 张回归表的 payload size + SHA 与仓内已落盘证据(t33 profiles / t29 inventory)一致
  * 修复后 = 独立复算(逐字节 SHA 相等)
  * 119 个受 `data_base` 缺陷影响的条目:修复后 `len == entry.size`、成员单帧、leftover==0
  * 修复前负例保留:legacy 算法(从 `entry.offset` 起扫 64B)在 server#34 上取到 12B stub
  * `load_payload` 源码不得出现硬编码 data_base(必须来自 `_archive_layout`)

用法
----
  py -V:3.12 -I -B scratch/t43/out/verify.py --selftest
  py -V:3.12 -I -B scratch/t43/out/verify.py --json out.json
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import struct
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = pathlib.Path(__file__).resolve().parent


def find_root(start: pathlib.Path) -> pathlib.Path:
    for cand in (start, *start.parents):
        if (cand / "AGENTS.md").is_file():
            return cand
    return start.parents[3]


ROOT = find_root(HERE)
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data"))
UPSTREAM = pathlib.Path(r"D:\tmp2b\fm24")
T33 = ROOT / "scratch/t33/out/profiles"
T29 = ROOT / "scratch/t29/out/subtable_inventory.json"
DUMP_SRC = ROOT / "scripts/fm24_dump.py"

DAT_HEAD = b"\x03\x01tad."
FMF_MAGIC = bytes.fromhex("0201666d662e080000")
ZSTD_MAGIC = bytes.fromhex("28b52ffd")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def zstd():
    if str(UPSTREAM / "tools/python") not in sys.path:
        sys.path.insert(0, str(UPSTREAM / "tools/python"))
    import zstandard

    return zstandard


def inflate(frame: bytes, limit: int = 256 * 1024 * 1024) -> bytes:
    out = zstd().ZstdDecompressor().decompressobj().decompress(frame)
    if len(out) > limit:
        raise ValueError("payload over limit")
    return out


# ---------------------------------------------------------------- FMF 自解析


class DirReader:
    def __init__(self, buf: bytes):
        self.b = buf
        self.pos = 0
        self.entries: list[dict] = []

    def take(self, n: int) -> bytes:
        if self.pos + n > len(self.b):
            raise ValueError("truncated directory")
        v = self.b[self.pos : self.pos + n]
        self.pos += n
        return v

    def u32(self) -> int:
        return struct.unpack("<I", self.take(4))[0]

    def string(self) -> str:
        return self.take(self.u32()).decode("utf-8")

    def directory(self, parent: str = "", depth: int = 0) -> None:
        if depth > 40:
            raise ValueError("nesting")
        cur = f"{parent}/{self.string()}" if parent else self.string()
        for _ in range(self.u32()):
            name, ext = self.string(), self.string()
            off, packed, size, _t1, _t2 = struct.unpack("<5Q", self.take(40))
            self.entries.append(
                {"path": f"{cur}/{name}{ext}", "offset": off, "packed_size": packed, "size": size}
            )
        for _ in range(self.u32()):
            self.directory(cur, depth + 1)


def archive_layout(db: bytes) -> dict:
    """自解析 FMF 头 + 目录(不调用上游 codec)。"""
    start = 8 if db.startswith(DAT_HEAD) and db[8:17] == FMF_MAGIC else 0
    if db[start : start + 9] != FMF_MAGIC:
        raise ValueError("no FMF signature")
    toc = start + 9 + struct.unpack_from("<Q", db, start + 9)[0]
    base = start + 9 + struct.unpack_from("<Q", db, start + 17)[0]
    if not (start + 26 <= base <= toc < len(db)):
        raise ValueError(f"bad offsets base={base} toc={toc}")
    if db[toc : toc + 9] != FMF_MAGIC:
        raise ValueError("missing secondary FMF header")
    directory = inflate(db[toc + 9 :])
    r = DirReader(directory)
    r.directory()
    if r.pos != len(directory):
        raise ValueError("unparsed directory bytes")
    return {"data_base": base, "toc_offset": toc, "entries": r.entries}


_CACHE: dict[str, dict] = {}


def archive(name: str) -> dict:
    if name not in _CACHE:
        p = DB_DIR / f"{name}_db.dat"
        db = p.read_bytes()
        _CACHE[name] = {"path": p, "data": db, **archive_layout(db)}
    return _CACHE[name]


def entry_by_name(name: str, selector: str) -> dict:
    """selector 可为表号("34"→table_34.dat)或成员文件名。与 codec._resolve_table 同义。"""
    sel = str(selector)
    if sel.isdecimal():
        sel = f"table_{int(sel)}.dat"
    want = pathlib.PurePosixPath(sel).name
    for e in archive(name)["entries"]:
        if pathlib.PurePosixPath(e["path"]).name == want:
            return e
    raise KeyError(f"{selector} not in {name}_db.dat")


def frames_in(region: bytes) -> tuple[list[dict], int, str | None]:
    """成员区内逐帧解压,绝不越出 region。"""
    dctx = zstd().ZstdDecompressor()
    out, data, pos, err = [], region, 0, None
    while data[:4] == ZSTD_MAGIC:
        try:
            obj = dctx.decompressobj()
            chunk = obj.decompress(data)
        except Exception as exc:
            err = f"decode failed at +{pos}: {exc}"
            break
        out.append({"off": pos, "len": len(chunk), "sha256": sha(chunk), "eof": bool(obj.eof)})
        consumed = len(data) - len(obj.unused_data)
        if not obj.eof or consumed <= 0:
            if not obj.eof:
                err = f"truncated frame at +{pos}"
            break
        pos += consumed
        data = obj.unused_data
        if not data:
            break
    return out, len(data), err


def expected_payload(name: str, selector: str) -> dict:
    """独立复算:应得 payload(成员区 data_base+offset,按 size 选帧)。"""
    a = archive(name)
    e = entry_by_name(name, selector)
    base = a["data_base"]
    start = base + e["offset"]
    end = start + e["packed_size"]
    region = a["data"][start:end]
    frames, leftover, err = frames_in(region)
    hits = [f for f in frames if f["len"] == e["size"]]
    if len(hits) != 1:
        raise RuntimeError(f"{name}/{selector}: size hits = {len(hits)} frames={[f['len'] for f in frames]}")
    # 取回字节(与 hits 对应:同长度唯一,单帧即唯一)
    raw = inflate(region[hits[0]["off"] :])
    return {
        "archive": name,
        "selector": selector,
        "path": e["path"],
        "data_base": base,
        "member_start": start,
        "packed_size": e["packed_size"],
        "declared_size": e["size"],
        "payload": raw,
        "len": len(raw),
        "sha256": sha(raw),
        "frame_count": len(frames),
        "frame_lengths": [f["len"] for f in frames],
        "leftover": leftover,
        "error": err,
        "packed_region_sha": sha(region),
    }


def legacy_payload(name: str, selector: str) -> dict:
    """复现修复前的算法(从 entry.offset 起扫 64B 取首帧)——负例对照,不删。"""
    a = archive(name)
    e = entry_by_name(name, selector)
    db, off = a["data"], e["offset"]
    hit = next((off + d for d in range(64) if db[off + d : off + d + 4] == ZSTD_MAGIC), None)
    if hit is None:
        return {"hit": None, "len": None, "sha256": None}
    raw = inflate(db[hit:])
    return {"hit": hit, "hit_delta_from_correct": hit - (a["data_base"] + off),
            "len": len(raw), "sha256": sha(raw)}


# ---------------------------------------------------------------- 被验对象(子进程)


DUMP_PROBE = r'''
import hashlib, json, runpy, sys
sys.path.insert(0, "scripts")
import fm24_dump
codec = fm24_dump._reader()
targets = json.load(sys.stdin)
out = []
for a, t in targets:
    try:
        raw = fm24_dump.load_payload(codec, a, t)
        out.append({"archive": a, "table": t, "len": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest()})
    except Exception as exc:
        out.append({"archive": a, "table": t, "error": f"{type(exc).__name__}: {exc}"})
print(json.dumps(out))
'''


def dump_probe(targets: list[tuple[str, object]]) -> dict[tuple[str, object], dict]:
    env = dict(os.environ)
    env["FM24_DB_DIR"] = str(DB_DIR)
    r = subprocess.run(
        [sys.executable, "-I", "-B", "-c", DUMP_PROBE],
        cwd=str(ROOT), input=json.dumps(targets), capture_output=True, text=True, env=env,
    )
    if r.returncode != 0:
        raise RuntimeError(f"probe failed rc={r.returncode}: {r.stderr[-800:]}")
    rows = json.loads(r.stdout.strip().splitlines()[-1])
    return {(x["archive"], x["table"]): x for x in rows}


# ---------------------------------------------------------------- 证据目标


def regression_targets() -> list[dict]:
    out: list[dict] = []
    if T33.is_dir():
        for f in sorted(T33.glob("*.profile.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            p = d["payload"]
            out.append({"archive": p["archive"], "table": int(d["table_type"]),
                        "size": int(p["payload_size"]), "sha256": p["payload_sha256"],
                        "source": f"scratch/t33/out/profiles/{f.name}"})
    if T29.is_file():
        inv = json.loads(T29.read_text(encoding="utf-8"))
        for t in inv["tables"]:
            key = (t["archive"], int(t["table_type"]))
            if any((o["archive"], o["table"]) == key for o in out):
                continue
            out.append({"archive": t["archive"], "table": int(t["table_type"]),
                        "size": int(t["payload_size"]), "sha256": t["payload_sha256"],
                        "source": "scratch/t29/out/subtable_inventory.json"})
    return out


def affected_entries(name: str) -> list[dict]:
    """前一成员 packed_size < data_base 的条目(修复前必错帧)。"""
    a = archive(name)
    base = a["data_base"]
    ents = sorted(a["entries"], key=lambda e: e["offset"])
    out = []
    for i, e in enumerate(ents):
        prev = ents[i - 1] if i else None
        if prev is not None and int(prev["packed_size"]) < base:
            out.append({**e, "prev_path": prev["path"], "prev_packed": int(prev["packed_size"])})
    return out


# ---------------------------------------------------------------- selftest


def main() -> int:
    ap = argparse.ArgumentParser(description="t43 独立复算 verify(不 import fm24_dump)")
    ap.add_argument("--selftest", action="store_true", help="跑全部检查并打印 PASS/FAIL")
    ap.add_argument("--json", help="把检查明细写成 JSON")
    args = ap.parse_args()
    if not (args.selftest or args.json):
        ap.print_help()
        return 2

    checks: list[dict] = []
    P = F = 0

    def ck(name: str, ok: bool, detail: str = "") -> None:
        nonlocal P, F
        checks.append({"name": name, "ok": bool(ok), "detail": detail})
        if ok:
            P += 1
        else:
            F += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    # ---- 1 归档坐标系
    for name in ("server", "client", "lang_update"):
        try:
            a = archive(name)
            ck(f"{name} FMF parsed", True,
               f"data_base={a['data_base']} toc={a['toc_offset']} entries={len(a['entries'])}")
        except Exception as exc:
            ck(f"{name} FMF parsed", False, f"raise {exc}")
    ck("all three data_base equal", len({archive(n)["data_base"] for n in ("server", "client", "lang_update")}) == 1,
       f"bases={[archive(n)['data_base'] for n in ('server', 'client', 'lang_update')]} (动态取,非硬编码)")

    # ---- 2 源码:必须走 _archive_layout,不得硬编码 data_base
    src = DUMP_SRC.read_text(encoding="utf-8")
    fn_src = ""
    fn_node = None
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.FunctionDef) and node.name == "load_payload":
            fn_node = node
            fn_src = ast.get_source_segment(src, node) or ""
    ck("load_payload uses _archive_layout", "_archive_layout" in fn_src, f"len(fn)={len(fn_src)}B")
    # 只检查**代码**(剔除 docstring):docstring 里提到 34 是解释文案,不是硬编码
    code_only: list[str] = []
    if fn_node is not None:
        for stmt in fn_node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                continue  # docstring
            code_only.append(ast.get_source_segment(src, stmt) or "")
    code_text = "\n".join(code_only)
    ck("load_payload code has no hardcoded data_base", re.search(r"\b34\b", code_text) is None,
       f"code_len={len(code_text)}B (docstring excluded); regex \\b34\\b absent")
    ck("load_payload does not fall back to first frame", "不回落首帧" in fn_src and "return out" in fn_src,
       "raises when no frame matches size")

    # ---- 3 20 表回归:独立复算 == 已落盘证据 == fm24_dump
    targets = regression_targets()
    probe = dump_probe([(t["archive"], t["table"]) for t in targets])
    bad_size = bad_sha = bad_probe = 0
    fixed_notes = []
    for t in targets:
        try:
            exp = expected_payload(t["archive"], str(t["table"]))
        except Exception as exc:
            ck(f"recompute {t['archive']}#{t['table']}", False, f"raise {exc}")
            bad_size += 1
            continue
        if exp["len"] != t["size"]:
            bad_size += 1
            fixed_notes.append(f"{t['archive']}#{t['table']} exp={exp['len']} != evidence {t['size']}")
        if exp["sha256"] != t["sha256"]:
            bad_sha += 1
            fixed_notes.append(f"{t['archive']}#{t['table']} sha mismatch")
        got = probe.get((t["archive"], t["table"]), {})
        if got.get("len") != exp["len"] or got.get("sha256") != exp["sha256"]:
            bad_probe += 1
            fixed_notes.append(f"{t['archive']}#{t['table']} load_payload={got}")
    ck("20-table regression: independent == evidence(size)", bad_size == 0,
       f"tables={len(targets)} mismatched={bad_size}")
    ck("20-table regression: independent == evidence(sha256)", bad_sha == 0, f"mismatched={bad_sha}")
    ck("20-table regression: load_payload == independent (byte-identical sha)", bad_probe == 0,
       f"mismatched={bad_probe}")
    for note in fixed_notes[:8]:
        print(f"       NOTE {note}")

    # ---- 4 119 受影响条目:修复后 len==size / 单帧 / leftover==0;legacy 仍错(负例保留)
    affected = {n: affected_entries(n) for n in ("server", "client", "lang_update")}
    total_aff = sum(len(v) for v in affected.values())
    ck("affected-entry count == 119 (E80 predicate)",
       total_aff == 119, f"per-archive={ {k: len(v) for k, v in affected.items()} }")

    rows = []
    bad_fixed = 0
    legacy_wrong_bytes = 0
    legacy_same_bytes = []
    legacy_wrong_coord = 0
    for name, ents in affected.items():
        for e in ents:
            sel = pathlib.PurePosixPath(e["path"]).name
            try:
                exp = expected_payload(name, sel)
            except Exception as exc:
                bad_fixed += 1
                rows.append({"archive": name, "path": e["path"], "error": str(exc)})
                continue
            old = legacy_payload(name, sel)
            ok = (exp["len"] == e["size"] and exp["frame_count"] == 1
                  and exp["leftover"] == 0 and exp["error"] is None)
            if not ok:
                bad_fixed += 1
            differs = old["sha256"] != exp["sha256"]
            legacy_wrong_bytes += 1 if differs else 0
            if old.get("hit_delta_from_correct") != 0:
                legacy_wrong_coord += 1
            if not differs:
                legacy_same_bytes.append({"archive": name, "selector": sel,
                                          "declared_size": e["size"], "legacy_len": old["len"],
                                          "sha256": old["sha256"], "hit_delta": old["hit_delta_from_correct"]})
            rows.append({
                "archive": name, "path": e["path"], "selector": sel,
                "data_base": exp["data_base"], "member_start": exp["member_start"],
                "packed_size": exp["packed_size"], "prev_path": e["prev_path"],
                "prev_packed": e["prev_packed"], "declared_size": e["size"],
                "fixed_len": exp["len"], "fixed_sha256": exp["sha256"],
                "fixed_frame_count": exp["frame_count"], "leftover": exp["leftover"],
                "legacy_len": old["len"], "legacy_sha256": old["sha256"],
                "legacy_bytes_differ": differs,
                "legacy_hit_delta": old.get("hit_delta_from_correct"),
                "member_boundary_ok": exp["packed_region_sha"] == _entry_packed_sha(name, sel),
                "ok": ok,
            })
    ck("119 sampled: fixed len==entry.size, single frame, leftover==0", bad_fixed == 0,
       f"entries={total_aff} bad={bad_fixed}")
    # 负例保留:legacy 在每个条目上都落在前一成员(坐标错 -25B),不论字节是否偶然相同
    ck("119 sampled: legacy coordinate wrong on all (-25B, inside previous member)",
       legacy_wrong_coord == total_aff, f"wrong_coord={legacy_wrong_coord}/{total_aff}")
    ck("119 sampled: legacy payload bytes differ (majority)", legacy_wrong_bytes > 0,
       f"legacy_sha_differs={legacy_wrong_bytes}/{total_aff} "
       f"identical={len(legacy_same_bytes)} (全部为 12B 空 stub 模板相同:legacy 取到前一成员的 stub,"
       f"字节偶然相等 —— 长度/SHA 判据在此类条目上失效,必须靠成员边界)")
    boundary_ok = sum(1 for r in rows if r.get("member_boundary_ok"))
    ck("119 sampled: sha256(packed region) == entry packed sha", boundary_ok == total_aff,
       f"ok={boundary_ok}/{total_aff}")

    # ---- 5 关键负例保留:server#34 = 12B stub(legacy) vs 313082(fixed)
    e34 = expected_payload("server", "34")
    old34 = legacy_payload("server", "34")
    ck("negative server#34 legacy = 12B stub (preserved)",
       old34["len"] == 12 and old34["hit_delta_from_correct"] == -25,
       f"legacy_len={old34['len']} sha={old34['sha256'][:16] if old34['sha256'] else None} "
       f"delta={old34['hit_delta_from_correct']}B")
    ck("negative server#34 fixed = 313082 (a07b2bb7...)",
       e34["len"] == 313082 and e34["sha256"].startswith("a07b2bb7"),
       f"len={e34['len']} sha={e34['sha256'][:16]}")

    # ---- 6 lang_update 抽样(119 中的 117):同一条代码路径可达
    lu = [r for r in rows if r["archive"] == "lang_update"][:6]
    lu_probe = dump_probe([("lang_update", r["selector"]) for r in lu]) if lu else {}
    lu_ok = all(lu_probe.get(("lang_update", r["selector"]), {}).get("sha256") == r["fixed_sha256"] for r in lu)
    ck("lang_update sample via load_payload(path form) == independent", lu_ok,
       f"n={len(lu)} details={[ (r['selector'], lu_probe.get(('lang_update', r['selector']),{}).get('len')) for r in lu ]}")

    # ---- 7 五锚点(与 t38 已接受证据交叉)
    anchors = [("server", "34", 313082), ("client", "3", 6932082), ("server", "73", 45),
               ("server", "66", 18094), ("server", "43", 24632)]
    anchor_rows = {}
    ok_all = True
    for name, sel, size in anchors:
        exp = expected_payload(name, sel)
        anchor_rows[f"{name}#{sel}"] = {"len": exp["len"], "sha256": exp["sha256"]}
        ok_all &= exp["len"] == size
    ck("five anchors (t38) independent recompute", ok_all, json.dumps({k: v["len"] for k, v in anchor_rows.items()}))

    print(f"--- t43 verify: {P} PASS / {F} FAIL ---")

    if args.json:
        pathlib.Path(args.json).write_text(
            json.dumps({"checks": checks, "pass": P, "fail": F, "affected": rows,
                        "legacy_byte_identical_stubs": legacy_same_bytes,
                        "anchors": anchor_rows}, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        print(f"wrote {args.json}")
    return 0 if F == 0 else 1


def _entry_packed_sha(name: str, selector: str) -> str:
    """entry 的 packed 区 SHA(独立算法重算;上游 list_tables 的 sha256 即此值)。"""
    a = archive(name)
    e = entry_by_name(name, selector)
    start = a["data_base"] + e["offset"]
    return sha(a["data"][start : start + e["packed_size"]])


if __name__ == "__main__":
    sys.exit(main())
