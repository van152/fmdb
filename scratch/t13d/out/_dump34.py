#!/usr/bin/env python3
"""t13d 旁路:table 34 的 zstd 帧搜索修正(仅本任务用,输出到 scratch/t13d/out/)。

fm24_dump.load_payload 取 offset..offset+64 内第一个 zstd magic,但 table_34 命中了
伪帧(解出 12 B)。这里枚举所有候选帧,取能闭合 14 + 7115*44 + 8 == 313082 的那个。
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import runpy
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
DB_DIR = pathlib.Path(
    r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
)
MAGIC = bytes.fromhex("28b52ffd")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", type=int, default=34)
    ap.add_argument("--csv", default=str(ROOT / "scratch/t13d/out/t34.csv"))
    ap.add_argument("--scan", type=int, default=256, help="offset 后多少字节内搜帧头")
    ap.add_argument("--expect", type=int, default=313082)
    ap.add_argument("--stride", type=int, default=44)
    ap.add_argument("--count", type=int, default=7115)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        print("selftest: imports only")
        return 0

    k = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py"))
    codec = runpy.run_path(str(k["OLD_READER_PATH"]))
    fn = "server_db.dat"
    p = DB_DIR / fn
    db = p.read_bytes()
    ent = codec["_resolve_table"](a.table, codec["list_tables"](p, fn), fn)
    off = ent["offset"]
    print(f"table {a.table} offset {off} size {ent['size']}")

    cands = []
    i = off
    end = off + a.scan
    while i < end:
        j = db.find(MAGIC, i, end)
        if j < 0:
            break
        cands.append(j)
        i = j + 1
    print(f"zstd magic candidates: {[c - off for c in cands]}")

    for c in cands:
        try:
            raw = codec["_stream_decompress"](db[c:], 256 * 1024 * 1024)
        except Exception as ex:
            print(f"  +{c - off}: decompress fail {ex}")
            continue
        ok = len(raw) == a.expect and 14 + a.count * a.stride + 8 == len(raw)
        print(f"  +{c - off}: payload {len(raw)} {'CLOSED' if ok else 'no closure'}")
        if not ok:
            continue
        rows = []
        for n in range(a.count):
            b = 14 + n * a.stride
            rows.append({"row": n, "offset": b, "len": a.stride,
                         "raw_hex": raw[b:b + a.stride].hex()})
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["row", "offset", "len", "raw_hex"])
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {a.csv} ({len(rows)} rows)")
        return 0
    print("no closable frame found", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
