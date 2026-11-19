#!/usr/bin/env python3
"""dspot_final — t15d 交付用的一次性测量(只读),产出 dspot.json 的全部引用数字。

每条测量都写成可复算的 `claim`:
  {"table":42, "field":"u32@0", "kind":"person_duni", "rows":1.0, "d":16756, "lift":3092}

用法
----
  py -V:3.12 -I -B scratch/t15d/out/dspot_final.py --help
  py -V:3.12 -I -B scratch/t15d/out/dspot_final.py --selftest
  py -V:3.12 -I -B scratch/t15d/out/dspot_final.py --out scratch/t15d/out/measure.json

退出码:0 成功 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUTDIR = ROOT / "scratch/t15d/out"
sys.path.insert(0, str(OUTDIR))
import dspot as D  # noqa: E402

TAIL = 13


def load_sets() -> dict:
    return {
        "duni": np.unique(np.load(ROOT / "scratch/t15/out/person_duni_all.npy").astype(np.int64)),
        "uid": np.unique(np.load(ROOT / "scratch/t15/out/person_uid_all.npy").astype(np.int64)),
    }


S = {}


def colv(tid: int, off: int, w: int) -> np.ndarray:
    raw, n, st = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    return D.col(raw, st, n, off, w).astype(np.int64)


def duni_m(tid: int, off: int, w: int = 4) -> dict:
    c = colv(tid, off, w)
    ds = S["duni"]
    ok = np.isin(c, ds)
    hi = max(1, int(c.max()))
    base = float((ds <= hi).sum()) / hi
    return {"field": f"u{w * 8}@{off}", "kind": "person_duni",
            "rows": round(float(ok.mean()), 4), "d": int(np.unique(c).size),
            "dist_hit": int(np.unique(c[ok]).size),
            "min": int(c.min()), "max": int(c.max()),
            "lift": round(float(ok.mean()) / base, 1) if base else None}


def mask_m(tid: int, off: int, base: int, w: int = 4) -> dict:
    """去掉高位标记位后落进 base 的比例(用于 FM 的 xx<<8 | tag 编码)。"""
    c = colv(tid, off, w)
    lo = c & 0xFFFF
    lo2 = c & 0xFFFFFF
    return {"field": f"u{w * 8}@{off}", "kind": f"low16<{base}",
            "frac": round(float((lo < base).mean()), 4),
            "frac24": round(float((lo2 < base).mean()), 4),
            "d_lo": int(np.unique(lo[lo < base]).size),
            "min": int(c.min()), "max": int(c.max())}


def plain(tid: int, off: int, w: int, note: str = "") -> dict:
    c = colv(tid, off, w)
    v = np.unique(c)
    return {"field": f"u{w * 8}@{off}", "kind": "range", "note": note,
            "d": int(v.size), "min": int(v.min()), "max": int(v.max()),
            "zero": round(float((c == 0).mean()), 3),
            "top": [int(x) for x in v[:6]]}


def ordinal(tid: int) -> dict:
    raw, n, st = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    c = D.col(raw, st, n, st - TAIL, 4).astype(np.int64)
    return {"field": f"u32@{st - TAIL}", "kind": "row_ordinal",
            "all_match": bool((c == np.arange(n)).all()), "n": n}


def measure() -> dict:
    M: dict[int, list] = {}
    # t42 RETIREMENT: 人 + 退役日期
    M[42] = [duni_m(42, 0), ordinal(42), plain(42, 8, 2, "day-of-year"),
             plain(42, 10, 2, "year")]
    # t43 MONTHLY_INSTALLMENT: 人 + 月数 + 金额
    M[43] = [duni_m(43, 0), ordinal(43), plain(43, 24, 4, "months"),
             plain(43, 28, 4, "amount")]
    # t46 DRAFT_TRANSFER: 仅 7 行,只有链式引用
    M[46] = [plain(46, 0, 4, "id_a"), plain(46, 4, 4, "id_b"),
             ordinal(46), plain(46, 10, 2, "year")]
    # t50 MLS_TRADED_SLOT: 左值/右值 + 日期
    M[50] = [plain(50, 0, 4, "slot_a"), plain(50, 4, 4, "slot_b"),
             ordinal(50), plain(50, 9, 2, "day-of-year"),
             plain(50, 11, 2, "year")]
    # t51 MLS_GAM
    M[51] = [plain(51, 0, 4, "club_or_amount"), plain(51, 4, 4, "amount_b"),
             ordinal(51), plain(51, 8, 2, "year")]
    # t58 WEEKLY_WAGE_CONTRIBUTION: 8 行
    M[58] = [duni_m(58, 0), plain(58, 8, 4, "amount_a"), plain(58, 16, 4, "amount_b"),
             plain(58, 28, 4, "amount_c"), ordinal(58)]
    # t62 RESERVE_TEAM: club 引用
    M[62] = [mask_m(62, 1, 84259), plain(62, 0, 1, "flag_u8"), ordinal(62)]
    # t64 CLUB_STAFF_JOB_STATUS: 纯 club ID + 枚举
    M[64] = [plain(64, 0, 4, "club_id"), plain(64, 4, 1, "job_type"),
             plain(64, 6, 1, "enum"), ordinal(64)]
    # t66 TRANSFER_PREFERENCE
    M[66] = [duni_m(66, 0), mask_m(66, 4, 84259), plain(66, 8, 3, "enum_bytes"),
             ordinal(66)]
    # t70 VISION_OBJECTIVE
    M[70] = [duni_m(70, 0), duni_m(70, 4), plain(70, 20, 2, "comp?"),
             ordinal(70)]
    # t34 CUP_HISTORY: comp + 起止年
    M[34] = [mask_m(34, 0, 7047), plain(34, 8, 2, "year_start"),
             plain(34, 10, 2, "year_end"), ordinal(34)]
    # t37 LEAGUE_HISTORY: comp + team + 年份 + 小计数
    M[37] = [plain(37, 0, 2, "comp_id"), plain(37, 4, 4, "team_id"),
             plain(37, 12, 2, "year"), plain(37, 5, 2, "points?"),
             ordinal(37)]
    return {str(k): v for k, v in M.items()}


def selftest() -> int:
    global S
    S = load_sets()
    ok = True
    m = measure()
    # 正控:t42@0 必须 rows≈1 且 lift 巨大
    r = m["42"][0]
    print(f"  t42@0 duni rows={r['rows']} lift={r['lift']}")
    if r["rows"] < 0.99 or r["lift"] < 100:
        ok = False
    # 负控:行序号列不应通过 duni 判据
    neg = duni_m(42, 22, 4)
    print(f"  neg t42@22 (row ordinal zone) rows={neg['rows']} lift={neg['lift']}")
    if neg["rows"] > 0.9 and neg["lift"] and neg["lift"] > 3:
        ok = False
    print("selftest:", "ok" if ok else "MISMATCH")
    return 0 if ok else 1


def main() -> int:
    global S
    ap = argparse.ArgumentParser(description="t15d 交付测量(只读)")
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    S = load_sets()
    if a.selftest:
        return selftest()
    m = measure()
    text = json.dumps(m, ensure_ascii=False, indent=1)
    if a.out:
        a.out.write_text(text, encoding="utf-8")
        print(f"json: {a.out} ({len(text)} B)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
