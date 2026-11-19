#!/usr/bin/env python3
"""t15b probe3 — people_db.dat 头部 (count + class 子表) 与 basic_people_db 的关系验证。

只读;输出 probe3.json。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DB_DIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or r"scratch/data")
if not DB_DIR.is_absolute():
    DB_DIR = ROOT / DB_DIR
sys.path.insert(0, str(pathlib.Path(r"D:\tmp2b\fm24\tools\python")))


def dec(name: str, skip: int = 8) -> bytes:
    import zstandard as zstd
    data = (DB_DIR / name).read_bytes()
    with zstd.ZstdDecompressor().stream_reader(io.BytesIO(data[skip:]), read_across_frames=True) as r:
        return r.read(600 * 1024 * 1024)


def walk_compact(raw: bytes, pos: int, n: int):
    """people_db 紧凑段文法(逐行复现):
    u32 key | u32 type(=5) | u8 unk | u32 name_len | name | 8×00 | u32 key2(==key)
    | u32 duni | u32 duni(==前一列) ;行跨度 = 33 + name_len"""
    rows, bad = [], None
    start = pos
    for i in range(n):
        if pos + 33 > len(raw):
            bad = {"i": i, "off": pos, "why": "eof"}
            break
        key, typ = struct.unpack_from("<II", raw, pos)
        unk = raw[pos + 8]
        ln = struct.unpack_from("<I", raw, pos + 9)[0]
        end = pos + 13 + ln
        if typ != 5 or not (0 <= ln <= 64) or end + 20 > len(raw):
            bad = {"i": i, "off": pos, "type": typ, "len": ln,
                   "hex": raw[pos:pos + 12].hex()}
            break
        try:
            nm = raw[pos + 13:end].decode("utf-8") if ln else ""
        except UnicodeDecodeError:
            bad = {"i": i, "off": pos, "why": "utf8"}
            break
        pad = raw[end:end + 8]
        key2, d1, d2 = struct.unpack_from("<III", raw, end + 8)
        if any(pad) or key2 != key or d1 != d2:
            bad = {"i": i, "off": pos, "why": "trailer", "pad": pad.hex(),
                   "key2": key2, "key": key, "d1": d1, "d2": d2}
            break
        rows.append({"i": i, "off": pos, "key": key, "unk": unk, "name": nm, "duni": d1})
        pos = end + 20
    return rows, pos, bad, start


def main() -> int:
    ap = argparse.ArgumentParser(description="t15b probe3: people_db 头部子表结构")
    ap.add_argument("--out", default=str(ROOT / "scratch/t15b/out/probe3.json"))
    ap.add_argument("--n", type=int, default=1193)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        assert struct.unpack_from("<I", bytes.fromhex("5b0a0a00"), 0)[0] == 658011
        print("selftest OK")
        return 0

    raw = dec("people_db.dat")
    out = {"len": len(raw), "head_hex": raw[:32].hex()}
    out["u32_at_0"] = struct.unpack_from("<I", raw, 0)[0]
    out["u32_at_2"] = struct.unpack_from("<I", raw, 2)[0]
    out["head_after_count_hex"] = raw[2:26].hex()
    rows, endpos, bad, start = walk_compact(raw, 6, a.n)
    ok = rows
    out["compact"] = {
        "target_rows": a.n, "walked": len(ok), "stop_reason": bad,
        "end_pos": endpos, "start_pos": start, "byte_span": endpos - start,
        "row_span_formula": "33 + name_len",
        "all_type_5": all(True for _ in ok),
        "keys_unique": len({r["key"] for r in ok}) == len(ok),
        "keys_are_full_range": sorted(r["key"] for r in ok) == list(range(min(r["key"] for r in ok),
                                                                        max(r["key"] for r in ok) + 1)) if ok else None,
        "key_range": [min(r["key"] for r in ok), max(r["key"] for r in ok)] if ok else None,
        "duni_range": [min(r["duni"] for r in ok), max(r["duni"] for r in ok)] if ok else None,
        "empty_names": sum(1 for r in ok if not r["name"]),
        "names_head": [r["name"] for r in ok[:6]],
        "names_tail": [r["name"] for r in ok[-4:]],
    }
    # 段的后续字节(b22 报的 19,120B 未解区)
    out["gap_after_compact_hex_64"] = raw[endpos:endpos + 64].hex()
    # 段后第一个姓名/DOB 锚点位置
    p = raw.find(b"\xff\xff\xff\xff\x00", endpos)
    out["first_marker_after_compact"] = p
    out["first_marker_gap_bytes"] = p - endpos if p != -1 else None

    # basic_people_db 对照:解压头 + class 计数定义
    bp = dec("basic_people_db.dat")
    out["basic_people"] = {
        "len": len(bp),
        "head_hex_24": bp[:24].hex(),
        "u32_at_0": struct.unpack_from("<I", bp, 0)[0],
        "u32_at_1": struct.unpack_from("<I", bp, 1)[0],
        "u32_at_2": struct.unpack_from("<I", bp, 2)[0],
    }

    # 跨档案 Drun 锚点:compact 段的 (key, duni) 与 basic_people class-5 行走同一 ordinal 集
    CL = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
    cnt = struct.unpack_from("<I", bp, 0)[0]
    lo = min(r["key"] for r in ok)
    pos, bp_rows = 5, {}
    for i in range(cnt):
        cls = bp[pos + 1]
        ln = CL[cls]
        if i >= lo:
            o, dv1, dv2 = struct.unpack_from("<III", bp, pos + ln - 12)
            bp_rows[i] = {"ordinal": o, "duni": dv1, "duni2": dv2, "class": cls}
        pos += ln
    miss = [r["key"] for r in ok if r["key"] not in bp_rows]
    duni_ok = sum(1 for r in ok if r["key"] in bp_rows and bp_rows[r["key"]]["duni"] == r["duni"])
    out["cross_join"] = {
        "claim": "people_db compact 段 (key, duni) 与 basic_people_db 同 ordinal 行逐一相等",
        "rows_compared": len(ok), "key_missing_in_basic": miss[:4],
        "key_missing_count": len(miss),
        "duni_equal": duni_ok, "duni_equal_all": duni_ok == len(ok),
        "basic_class_all_5": all(bp_rows[r["key"]]["class"] == 5 for r in ok if r["key"] in bp_rows),
        "grade": "L1(两份档案逐字节对齐) + L2(跨文件同值锚点)",
    }
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "head_hex"}, ensure_ascii=False, indent=1)[:3000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
