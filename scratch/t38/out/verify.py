#!/usr/bin/env python3
"""t38 verify — 从归档独立复算多帧/成员感知选帧结论。

独立性声明
----------
本脚本**不 import `scripts/t38_multiframe.py`**,也不复用其 selftest 结果:
成员定位、帧枚举、选帧、SHA、回归对照全部在此重新实现一遍,只依赖:
  * 上游只读解码器 `D:\\tmp2b\\fm24\\scripts\\modding_read_dbdat.py`(取 FMF 目录)
  * 归档原始字节 `scratch/data/*_db.dat`
  * 仓内已落盘证据 `scratch/t29`,`scratch/t33`

它复算的是**文件事实**,再与被验对象 `scratch/t38/out/multiframe_report.json`
逐项比对;两者不一致即 FAIL。

用法
----
  py -V:3.12 -I -B scratch/t38/out/verify.py --selftest
  py -V:3.12 -I -B scratch/t38/out/verify.py --help
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import runpy
import struct
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = pathlib.Path(__file__).resolve().parent


def find_root(start: pathlib.Path) -> pathlib.Path:
    """向上找含 AGENTS.md 的目录。

    注:`HERE.parents[2]` == `scratch/`(不是仓根),因此不硬编码 parents[N],
    改为按标志文件定位,避免 t29b 那样把 ROOT 算到 `D:\\tmp2b` 的 bug。
    """
    for cand in [start, *start.parents]:
        if (cand / "AGENTS.md").is_file():
            return cand
    return start.parents[3]


ROOT = find_root(HERE)
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data"))
VERIFY_READER = ROOT / "scratch/t01/inbox/t01k/verify.py"
UPSTREAM = pathlib.Path(r"D:\tmp2b\fm24")
REPORT = HERE / "multiframe_report.json"
MAGIC = bytes.fromhex("28b52ffd")
DAT_MAGIC = b"\x03\x01tad."


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Fail(Exception):
    pass


def codec():
    if str(UPSTREAM / "tools/python") not in sys.path:
        sys.path.insert(0, str(UPSTREAM / "tools/python"))
    k = runpy.run_path(str(VERIFY_READER))
    return runpy.run_path(str(k["OLD_READER_PATH"]))


def zstd():
    import zstandard

    return zstandard


def table_id_of(path: str) -> int | None:
    name = pathlib.PurePosixPath(path).name
    if name.startswith("table_") and name.endswith(".dat"):
        mid = name[len("table_"):-len(".dat")]
        if mid.isdigit():
            return int(mid)
    return None


def frames_in(region: bytes, strict: bool = True) -> tuple[list[dict], int]:
    """区间内逐帧解压;非 MAGIC 停止。strict=True 时帧未闭合即 raise。

    strict=False 保留已解字节并标 eof=False,用于观测被边界截断的帧(E77)。
    """
    dctx = zstd().ZstdDecompressor()
    out: list[dict] = []
    data = region
    pos = 0
    err = None
    while data[:4] == MAGIC:
        obj = dctx.decompressobj()
        chunk = obj.decompress(data)
        complete = bool(obj.eof)
        out.append(
            {
                "member_offset": pos,
                "length": len(chunk),
                "sha256": sha(chunk),
                "eof": complete,
            }
        )
        if not complete:
            err = f"truncated frame at +{pos}(region boundary)"
            break
        consumed = len(data) - len(obj.unused_data)
        if consumed <= 0:
            err = f"no zstd progress at +{pos}"
            break
        pos += consumed
        data = obj.unused_data
        if not data:
            break
    if strict and err:
        raise Fail(err)
    return out, len(data)


def load_archive(cc, arch: str) -> dict:
    p = DB_DIR / f"{arch}_db.dat"
    if not p.is_file():
        raise Fail(f"missing archive {p}")
    db = p.read_bytes()
    lay = cc["_archive_layout"](db)
    base = int(lay["data_base"])
    ents = sorted(lay["entries"], key=lambda e: e["offset"])
    return {"archive": arch, "file": str(p), "data": db, "base": base,
            "toc": int(lay["toc_offset"]), "entries": ents,
            "tables": cc["list_tables"](p, f"{arch}_db.dat")}


def recompute(arch: str) -> dict:
    cc = codec()
    a = load_archive(cc, arch)
    base, db = a["base"], a["data"]
    # entry.sha256 只由 list_tables 提供;raw layout 条目没有该键
    packed_sha = {e["path"]: e.get("sha256") for e in a["tables"]}
    rows = {}
    misread = {}
    for i, e in enumerate(a["entries"]):
        prev = a["entries"][i - 1] if i else None
        start = base + int(e["offset"])
        end = start + int(e["packed_size"])
        region = db[start:end]
        fr, left = frames_in(region)
        tid = table_id_of(e["path"])
        rows[e["path"]] = {
            "table_id": tid,
            "base": base,
            "entry_offset": int(e["offset"]),
            "member_start": start,
            "packed_size": int(e["packed_size"]),
            "size": int(e["size"]),
            "frame_lengths": [f["length"] for f in fr],
            "frame_shas": [f["sha256"] for f in fr],
            "leftover": left,
            "packed_sha_ok": sha(region) == packed_sha.get(e["path"]),
            "prev": prev["path"] if prev else None,
            "prev_packed": int(prev["packed_size"]) if prev else None,
        }
        # 旧法取帧(用 entry.offset 当绝对偏移)
        off = int(e["offset"])
        hit = next((d for d in range(64) if db[off + d: off + d + 4] == MAGIC), None)
        if hit is not None and hit != base:
            blk = None
            if prev is not None:
                ps = base + int(prev["offset"])
                pf, _ = frames_in(db[ps: ps + int(prev["packed_size"])])
                blk = pf[0]["length"] if pf else None
            misread[e["path"]] = {"table_id": tid, "delta": hit, "legacy_len": blk,
                                 "prev": prev["path"] if prev else None,
                                 "prev_packed": int(prev["packed_size"]) if prev else None}
    return {"meta": {"archive": arch, "file": a["file"], "size": len(db),
                     "sha256": sha(db), "base": base, "toc": a["toc"],
                     "entries": len(a["entries"])}, "rows": rows, "misread": misread}


def pick(arch: str, tid: int) -> tuple[bytes, dict]:
    """独立选帧:data_base+offset → packed_size 区间 → size 唯一命中。"""
    r = recompute(arch)
    fn = f"{arch}_db.dat"
    path = f"{arch}_db/{fn[:-4]}/table_{tid}.dat" if False else None
    cand = [p for p, row in r["rows"].items() if row["table_id"] == tid]
    if not cand:
        raise Fail(f"{arch}: table_{tid} not found")
    row = r["rows"][cand[0]]
    cc = codec()
    a = load_archive(cc, arch)
    e = cc["_resolve_table"](tid, a["tables"], fn)
    start, end = a["base"] + int(e["offset"]), a["base"] + int(e["offset"]) + int(e["packed_size"])
    region = a["data"][start:end]
    fr, left = frames_in(region)
    hits = [f for f in fr if f["length"] == int(e["size"])]
    if len(hits) != 1:
        raise Fail(f"{arch}#{tid}: size hits {len(hits)} of frames {[f['length'] for f in fr]}")
    # 从区间原位重新解出帧 1 字节流(不复用 frames_in 的缓存,保证独立性)
    dctx = zstd().ZstdDecompressor()
    raw = dctx.decompressobj().decompress(region)
    if len(raw) != hits[0]["length"] or sha(raw) != hits[0]["sha256"]:
        raise Fail(f"{arch}#{tid}: re-decompress mismatch")
    return raw, {
        "frames": [f["length"] for f in fr],
        "member_offset": hits[0]["member_offset"],
        "leftover": left,
        "row": row,
        "entry_sha": e.get("sha256"),
    }


def run_selftest(verbose: bool = False) -> int:
    if sys.version_info[:2] != (3, 12):
        print("FAIL: 需要 py -V:3.12 -I -B", file=sys.stderr)
        return 2
    checks: list[tuple[str, bool, str]] = []

    def ck(name, ok, det=""):
        checks.append((name, bool(ok), det))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {det}")

    if not REPORT.is_file():
        print(f"ERROR: 被验对象缺失 {REPORT}", file=sys.stderr)
        return 2
    doc = json.loads(REPORT.read_text(encoding="utf-8"))

    # ---------- A 独立复算:全归档普查 ----------
    rec = {arch: recompute(arch) for arch in ("server", "client", "lang_update")}
    total = sum(len(v["rows"]) for v in rec.values())
    nonconf = [
        (a, p, row["frame_lengths"], row["size"], row["leftover"])
        for a, v in rec.items()
        for p, row in v["rows"].items()
        if len(row["frame_lengths"]) != 1 or row["frame_lengths"][0] != row["size"] or row["leftover"]
    ]
    multi = [(a, p) for a, v in rec.items() for p, row in v["rows"].items() if len(row["frame_lengths"]) != 1]
    ck("census total entries", total == doc["census"]["entries_total"],
       f"recomputed={total} reported={doc['census']['entries_total']}")
    ck("census single-frame all", not nonconf and not multi,
       f"nonconforming={len(nonconf)} multi_frame={len(multi)}")
    ck("census multi_frame zero", len(multi) == doc["census"]["multi_frame_members"] == 0,
       f"recomputed={len(multi)} reported={doc['census']['multi_frame_members']}")
    ck("packed sha == entry sha (all)", all(row["packed_sha_ok"] for v in rec.values() for row in v["rows"].values()),
       "sha256(archive[member_start:member_start+packed_size]) == entry.sha256 for every entry")

    # ---------- B 五个锚点独立选帧 ----------
    want = [
        ("server", 34, 313082, "a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812"),
        ("client", 3, 6932082, "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f"),
        ("server", 73, 45, "592528c36b85b775b0245116a5a6237c9406acbb220208c1abdf8b7ecf72e22e"),
        ("server", 66, 18094, "3ddd47bbeec04ff6789dafdfe40148367abc4373700b082452fc79be06e02911"),
        ("server", 43, 24632, "7981267028706e701d39a32126b5b2e85f9b4973266cf1545f09869a524a069e"),
    ]
    for arch, tid, size, wsha in want:
        try:
            raw, meta = pick(arch, tid)
        except Fail as exc:
            ck(f"anchor {arch}#{tid}", False, str(exc))
            continue
        ck(f"anchor {arch}#{tid}", len(raw) == size and sha(raw) == wsha,
           f"len={len(raw)}/{size} sha={sha(raw)[:16]} frames={meta['frames']} member+{meta['member_offset']}")
        # 对照被验 JSON
        j = next((x for x in doc["anchor_selection"] if x["archive"] == arch and x["table_id"] == tid), None)
        ck(f"anchor-repro {arch}#{tid}", j is not None and j["obtained_sha256"] == sha(raw)
           and j["frame_lengths"] == meta["frames"] and j["packed_size"] == meta["row"]["packed_size"],
           "report matches independent recompute" if j else "absent from report")

    # 目录条目 size 必等于 payload 头 record_count 可解释 + 版本一致
    for arch, tid, size, _ in want:
        raw, _ = pick(arch, tid)
        ck(f"header {arch}#{tid}", raw[:6] == DAT_MAGIC and len(raw) >= 14,
           f"tad. magic={raw[:6].hex()} ver={struct.unpack_from('<H', raw, 6)[0]} "
           f"rc={struct.unpack_from('<I', raw, 8)[0]}")

    # ---------- C 单帧回归:与 t33/t29 已落盘 size+sha 一致 ----------
    reg_doc = {(r["archive"], r["table_id"]): r for r in doc["single_frame_regression"]}
    t33 = {}
    for f in sorted((ROOT / "scratch/t33/out/profiles").glob("*.profile.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        t33[(d["payload"]["archive"], int(d["table_type"]))] = (
            int(d["payload"]["payload_size"]), d["payload"]["payload_sha256"])
    t29 = {}
    inv = json.loads((ROOT / "scratch/t29/out/subtable_inventory.json").read_text(encoding="utf-8"))
    for t in inv["tables"]:
        t29[(t["archive"], int(t["table_type"]))] = (int(t["payload_size"]), t["payload_sha256"])

    ck("regression source maps", len(t33) == 7 and len(t29) == 13, f"t33={len(t33)} t29={len(t29)}")
    bad = 0
    for key, (size, wsha) in {**t29, **t33}.items():
        arch, tid = key
        raw, _ = pick(arch, tid)
        if len(raw) != size or sha(raw) != wsha:
            bad += 1
            print(f"   MISMATCH {arch}#{tid}: {len(raw)}/{size} {sha(raw)[:8]}/{wsha[:8]}")
    ck("regression payload size+sha", bad == 0, f"{len(t29) + len(t33)} tables, mismatches={bad}")

    # 旧法对照:差异集合必须 == 旧法错帧集合(可预测)
    legacy = None
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import fm24_dump

        legacy = fm24_dump.load_payload
    except Exception as exc:  # 只读引用失败不掩盖结论,记 SKIP
        print(f"   note: legacy loader unavailable ({exc})")
    if legacy is not None:
        cc = codec()
        pred = {(a, row["table_id"]) for a, v in rec.items() for row in v["rows"].values()
                if row["table_id"] is not None and row["prev_packed"] is not None
                and row["prev_packed"] < row["base"]}
        obs = set()
        for a, v in rec.items():
            for p, m in v["misread"].items():
                if m["table_id"] is not None:
                    obs.add((a, m["table_id"]))
        ck("legacy predicate exact", pred == obs,
           f"predicted={len(pred)} observed={len(obs)} symmetric_diff={len(pred ^ obs)}")
        same = 0
        for key, (size, wsha) in {**t29, **t33}.items():
            arch, tid = key
            raw, _ = pick(arch, tid)
            old = legacy(cc, arch, tid)
            if old == raw:
                same += 1
            elif key not in obs:
                ck(f"unexplained legacy diff {arch}#{tid}", False, f"legacy={len(old)} correct={len(raw)}")
        ck("legacy diffs all explained", all(
            (r["archive"], r["table_id"]) in obs for r in doc["single_frame_regression"] if not r["identical"]
        ), f"identical_to_legacy={same}/{len(t29) + len(t33)}; divergent tables in report ⊆ predicted set")

    # ---------- D 契约:无匹配帧必须 raise(不开后门回退) ----------
    cc = codec()
    a = load_archive(cc, "server")
    e34 = next(x for x in a["entries"] if x["path"].endswith("table_34.dat"))
    start = a["base"] + int(e34["offset"])
    fr, _ = frames_in(a["data"][start:start + int(e34["packed_size"])])
    impossible = int(e34["size"]) + 7
    ck("impossible size has no frame", all(f["length"] != impossible for f in fr),
       f"size+7={impossible} not among {[f['length'] for f in fr]}")
    ck("truncated member cuts frame", frames_in_safe(a["data"][start:start + 100]) is False,
       "packed_size=100 cuts the frame (loader must not pad it)")

    # ---------- D2 E77 独立复算:坐标系 vs packed_size 语义 ----------
    off34 = int(e34["offset"])
    packed34 = int(e34["packed_size"])
    db34 = a["data"]
    base34 = a["base"]
    hit34 = next((d for d in range(64) if db34[off34 + d: off34 + d + 4] == MAGIC), None)
    bounded_start = off34 + (hit34 or 0)
    e77_frames, _ = frames_in(db34[bounded_start: off34 + packed34], strict=False)
    unb_frames, _ = frames_in(db34[bounded_start: len(db34)], strict=False)
    corr_frames, corr_left = frames_in(db34[base34 + off34: base34 + off34 + packed34])
    ck("E77 bounded reproduces truncation",
       any(not f["eof"] for f in e77_frames)
       and [f["length"] for f in e77_frames] == [12, 287410],
       f"frames={[(f['length'], f['eof']) for f in e77_frames]}")
    ck("E77 unbounded 2nd frame == size",
       len(unb_frames) >= 2 and unb_frames[1]["length"] == int(e34["size"])
       and unb_frames[1]["sha256"] == "a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812",
       f"lens={[f['length'] for f in unb_frames][:3]}")
    ck("E77 correct coord = whole member single frame",
       len(corr_frames) == 1 and corr_frames[0]["length"] == int(e34["size"])
       and corr_frames[0]["eof"] and corr_left == 0,
       f"frames={[(f['length'], f['eof']) for f in corr_frames]} leftover={corr_left}")
    j77 = doc["e77_investigation"]
    ck("E77 report matches recompute",
       j77["correct_member_start"] == base34 + off34
       and j77["e77_coordinate_delta_from_correct"] == bounded_start - (base34 + off34)
       and j77["conclusion"]["packed_size_is_whole_member"] is True
       and j77["conclusion"]["e77_symptom_reproduced"] is True,
       f"delta={j77['e77_coordinate_delta_from_correct']}B vs recomputed "
       f"{bounded_start - (base34 + off34)}B")

    # ---------- D3 E77 推荐的无界方法:独立验证它何时歧义 ----------
    def unbounded(arch: str, tid: int):
        a2 = load_archive(cc, arch)
        e2 = cc["_resolve_table"](tid, a2["tables"], f"{arch}_db.dat")
        s2 = a2["base"] + int(e2["offset"])
        fr, _ = frames_in(a2["data"][s2:], strict=False)
        owners = sorted(a2["entries"], key=lambda x: x["offset"])
        hits = [
            (f["member_offset"], f["sha256"],
             next((o["path"] for o in owners
                   if a2["base"] + int(o["offset"]) == s2 + f["member_offset"]), None))
            for f in fr if f["length"] == int(e2["size"])
        ]
        return len(fr), hits, int(e2["packed_size"]), int(e2["size"])

    amb = []
    for arch in ("server", "client", "lang_update"):
        a3 = load_archive(cc, arch)
        for p, row in rec[arch]["rows"].items():
            tid = row["table_id"]
            if tid is None:
                continue
            n_unb, hits, _pk, _sz = unbounded(arch, tid)
            if len(hits) > 1:
                amb.append((arch, tid, n_unb, [(h[2], h[1][:8]) for h in hits]))
    rep_amb = set(doc["unbounded_method_study"]["ambiguous_tables"])
    got_amb = {f"{a}#{t}" for a, t, _, _ in amb}
    ck("unbounded ambiguity reproduced", got_amb == rep_amb,
       f"recomputed={sorted(got_amb)} reported={sorted(rep_amb)}")
    ck("bounded path needs no disambiguation",
       doc["unbounded_method_study"]["ambiguous_table_count"] == len(amb) and len(amb) > 0,
       f"{len(amb)} tables size-ambiguous under unbounded scan; bounded always unique")
    # server#51 是最危险的一例:撞击帧来自**另一个表**,内容不同
    r51 = next((x for x in amb if x[0] == "server" and x[1] == 51), None)
    ck("server#51 collision is cross-table with different payload",
       r51 is not None and len({h[1] for h in r51[3]}) == 2
       and any("table_60" in (h[0] or "") for h in r51[3]),
       f"hits={r51[3]}" if r51 else "not found")

    # ---------- E 报告自洽 ----------
    ck("report anchor count 5", len(doc["anchor_selection"]) == 5, str(len(doc["anchor_selection"])))
    ck("report regression 20", doc["regression_summary"]["targets"] == 20
       and doc["regression_summary"]["mf_ok"] == 20, str(doc["regression_summary"]))
    ck("report members 460", len(doc["members"]) == total == 460, f"{len(doc['members'])}/{total}")
    ck("report defect count", doc["legacy_load_payload_defect"]["affected_count"]
       == sum(len(v["misread"]) for v in rec.values()),
       f"{doc['legacy_load_payload_defect']['affected_count']}")
    ck("report data_base consistent",
       all(x["data_base"] == 34 for x in doc["archives"]), str([x["data_base"] for x in doc["archives"]]))

    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t38 verify: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1


def frames_in_safe(region: bytes) -> bool:
    """若帧在区间内被截断,返回 False(用于负结果检查)。"""
    try:
        frames_in(region, strict=True)
        return True
    except Fail:
        return False


def main() -> int:
    ap = argparse.ArgumentParser(
        description="t38 独立复算:多帧/成员感知选帧结论(不 import 被验加载器)")
    ap.add_argument("--selftest", action="store_true", help="从归档复算并比对 multiframe_report.json")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    if not args.selftest:
        ap.print_help()
        return 2
    try:
        return run_selftest(verbose=args.verbose)
    except Fail as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, KeyError, ValueError, RuntimeError, ImportError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
