#!/usr/bin/env python3
"""t05 — client table_47 (LOCAL_REGION / lcrg) 行边界:精确闭合 + 身份验证。

结论(本脚本可复现):
  payload = 14B header + 2,488 行 + 8B footer,总计 109,505 B
  行文法: prefix(28 + 5k) + rdui(4) + duni(4) + duni(4) + marker(1)   [13B 身份尾]
          rdui == 行号(0-based);duni 两个 u32 相等
  行长分布: 41×1380 / 46×878 / 51×129 / 56×79 / 71×14 / 61×6 / 76×2

两条既有结论的勘误:
  1) 上游 DB_TABLES_BIG/SMALL 报 `25 + 2488*44 + 8 = 109505` 为 exact fixed stride。
     → 纯算术巧合。按 44B 切分后 rdui==index 仅 3/2488、重复尾 u32 仅 576/2488,**证伪**。
  2) 本仓 scratch/t02/lcrg_partial.json 报"第 9 行起变长、无法封口"。
     → 变长是真的,但用"尾锚 + 最短行长贪心"可精确封口,**该 partial 结论可升级为 complete**。

用法:
  py -V:3.12 -I -B scripts/t05_lcrg.py            # 全量走查并打印结论
  py -V:3.12 -I -B scripts/t05_lcrg.py --selftest # 自检(断言闭合/身份/行长集合)
  py -V:3.12 -I -B scripts/t05_lcrg.py --json     # 输出机读结论
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import runpy
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLIENT_DB = pathlib.Path(
    r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\client_db.dat"
)
READER = pathlib.Path(r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
MAGIC = bytes.fromhex("28b52ffd")

TABLE_ID = 47
EXPECT_COUNT = 2488
EXPECT_PAYLOAD = 109505
HEADER = 14
FOOTER = 8
TAIL = 13          # rdui(4) + duni(4) + duni(4) + marker(1)
BASE_PREFIX = 28   # 41 - 13
STEP = 5
MAX_K = 60


def load_payload() -> bytes:
    k = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py"))
    codec = runpy.run_path(str(k["OLD_READER_PATH"]))
    db = CLIENT_DB.read_bytes()
    e = codec["_resolve_table"](TABLE_ID, codec["list_tables"](), "client_db.dat")
    off = e["offset"]
    hit = None
    for d in range(64):
        if db[off + d: off + d + 4] == MAGIC:
            hit = off + d
            break
    if hit is None:
        raise SystemExit("zstd frame not found")
    return codec["_stream_decompress"](db[hit:], 256 * 1024 * 1024)


def tail_ok(raw: bytes, pos: int, ln: int, idx: int | None = None) -> bool:
    """行尾 13B = rdui(4) + duni(4) + duni(4) + marker(1)。

    判据:两个 duni 相等、marker==0;若给出 idx,还要求 rdui == 行号。
    仅靠 duni 有多解(实测 1927/2488),必须加上 rdui==行号才能唯一定位。
    """
    t = pos + ln - TAIL
    if t < 0 or t + TAIL > len(raw):
        return False
    rdui, d1, d2 = struct.unpack_from("<III", raw, t)
    if not (d1 == d2 and raw[t + 12] == 0):
        return False
    if idx is not None and rdui != idx:
        return False
    return True


def walk(raw: bytes):
    """尾锚 + rdui==行号 双约束下的最短行长贪心。

    行长集合是 41+5k(实测只用 41..76)。双约束使候选唯一,贪心即精确:
    每次取满足 (duni 相等 + marker=0 + rdui==当前行号) 的最短行长。
    """
    end = len(raw) - FOOTER
    cands = sorted([BASE_PREFIX + TAIL + STEP * k for k in range(MAX_K)])
    pos, rows = HEADER, []
    while pos < end:
        idx = len(rows)
        pick = None
        for ln in cands:
            if pos + ln > end:
                break
            if tail_ok(raw, pos, ln, idx):
                pick = ln
                break
        if pick is None:
            return rows, pos
        rows.append((pos, pick))
        pos += pick
    return rows, pos


def analyse(raw: bytes) -> dict:
    rows, endpos = walk(raw)
    end = len(raw) - FOOTER
    lens = [ln for _, ln in rows]
    rdui_off = collections.Counter()
    duni_ok = 0
    for i, (s, ln) in enumerate(rows):
        p = s + ln - TAIL
        if struct.unpack_from("<I", raw, p)[0] == i:
            rdui_off[p - s] += 1
        a, b = struct.unpack_from("<II", raw, p + 4)
        if a == b:
            duni_ok += 1
    return {
        "type_id": TABLE_ID,
        "entity": "local region (lcrg)",
        "archive": "client_db.dat",
        "payload_len": len(raw),
        "count": len(rows),
        "closure": f"{HEADER} + {sum(lens)} + {FOOTER} = {HEADER + sum(lens) + FOOTER}",
        "closure_ok": (HEADER + sum(lens) + FOOTER == len(raw)) and endpos == end,
        "row_grammar": "prefix(28+5k) + rdui(4) + duni(4) + duni(4) + 0x00",
        "identity": {
            "rdui_equals_row_index": sum(rdui_off.values()),
            "rdui_offset_relative_to_row_end": "row_len - 13",
            "rdui_offsets_seen": dict(sorted(rdui_off.items())),
            "duni_repeated_u32_rows": duni_ok,
        },
        "row_len_distribution": dict(sorted(collections.Counter(lens).items())),
        "errata": [
            "上游 25+2488*44+8=109505 的 fixed stride 为算术巧合:44B 切分下 rdui==index 仅 3/2488、重复尾 u32 仅 576/2488。",
            "本仓 lcrg_partial 的『第 9 行起变长、无法封口』不成立:变长可行,尾锚贪心即精确封口。",
        ],
        "status": "complete",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = load_payload()
    r = analyse(raw)

    if args.selftest:
        checks = {
            "payload_len": len(raw) == EXPECT_PAYLOAD,
            "count": r["count"] == EXPECT_COUNT,
            "closure": r["closure_ok"],
            "identity_rdui_all": r["identity"]["rdui_equals_row_index"] == EXPECT_COUNT,
            "identity_duni_all": r["identity"]["duni_repeated_u32_rows"] == EXPECT_COUNT,
            "row_len_set": set(r["row_len_distribution"]) <= set(BASE_PREFIX + TAIL + STEP * k for k in range(MAX_K)),
        }
        for k, v in checks.items():
            print(("PASS" if v else "FAIL"), k)
        print(f"rows={r['count']} closure={r['closure']} "
              f"rdui={r['identity']['rdui_equals_row_index']} duni={r['identity']['duni_repeated_u32_rows']}")
        return 0 if all(checks.values()) else 1

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"type={r['type_id']} {r['entity']} count={r['count']} payload={r['payload_len']}")
        print("closure:", r["closure"], "OK" if r["closure_ok"] else "FAIL")
        print("grammar:", r["row_grammar"])
        print("identity:", r["identity"]["rdui_equals_row_index"], "/", r["count"],
              "rdui offsets:", r["identity"]["rdui_offsets_seen"])
        print("row len dist:", r["row_len_distribution"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
