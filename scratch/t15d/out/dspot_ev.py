#!/usr/bin/env python3
"""dspot_ev — t15d 单表证据摘要(只读):把 12 张表的"可引用列"压成一页。

对每张表输出三类列:
  ID   —— u32/u16 全行 < base-1 的列(comp 7047 / club 84259 / team 84507 / nation 251 …)
        并给 d/base(去重覆盖)与 max/base(贴界度)。E42:两者都报,不单独定案。
  MONEY——量级 1e4..1e11 且 1000/100 整除率高的列(整数金额样)。
  DATE —— u16 落在 1900..2100(年)或 1..366(年内日)比 >0.99 的列。
另外报 person_duni 真实命中(lift 已扣密度基线)。

用法
----
  py -V:3.12 -I -B scratch/t15d/out/dspot_ev.py --help
  py -V:3.12 -I -B scratch/t15d/out/dspot_ev.py --selftest
  py -V:3.12 -I -B scratch/t15d/out/dspot_ev.py --table 37
  py -V:3.12 -I -B scratch/t15d/out/dspot_ev.py --all --json scratch/t15d/out/ev.json

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
SPACES = {"comp": 7047, "nation": 251, "club": 84259, "team": 84507,
          "person": 658011, "city": 56293, "injury": 115, "award": 3545}
DUNI = None


def duni() -> np.ndarray:
    global DUNI
    if DUNI is None:
        DUNI = np.unique(np.load(ROOT / "scratch/t15/out/person_duni_all.npy").astype(np.int64))
    return DUNI


def ev(tid: int) -> dict:
    raw, n, stride = D.payload(tid), D.SPEC[tid][0], D.SPEC[tid][1]
    lead = stride - TAIL
    ds = duni()
    ids, money, dates = [], [], []
    for off in range(lead):
        for w in (4, 2):
            if off + w > lead:
                continue
            c = D.col(raw, stride, n, off, w).astype(np.int64)
            v = np.unique(c)
            d, mn, mx = int(v.size), int(c.min()), int(c.max())
            tag = f"u{w * 8}@{off}"
            # 纯 ID 列:值域上界压在某空间内,且不是行序
            for name, B in SPACES.items():
                if mx < B and d > 1 and not (d == n and mn <= 1 and mx <= n):
                    cov = d / B
                    ids.append({"col": tag, "space": name, "d": d, "min": mn, "max": mx,
                                "d_of_base": round(cov, 4),
                                "max_of_base": round(mx / B, 4)})
                    break
            if w == 4 and d > 3 and 10 ** 4 <= mx <= 10 ** 14:
                big = c[c > 0]
                if big.size:
                    k = float((big % 1000 == 0).mean())
                    if k > 0.9:
                        money.append({"col": tag, "d": d, "min": mn, "max": mx,
                                      "k1000": round(k, 3),
                                      "q50": int(np.percentile(big, 50))})
            if w == 2:
                yr = float(((c >= 1900) & (c <= 2100)).mean())
                dy = float(((c >= 1) & (c <= 366)).mean())
                if yr > 0.99:
                    dates.append({"col": tag, "kind": "year", "min": mn, "max": mx, "d": d})
                elif dy > 0.99 and d > 3:
                    dates.append({"col": tag, "kind": "doy", "min": mn, "max": mx, "d": d})
            # person 真实集合
            if w == 4 and d > 1:
                ok = np.isin(c, ds)
                rows = float(ok.mean())
                hi = max(1, mx)
                base = float((ds <= hi).sum()) / hi
                if rows > 0.98 and base > 0 and rows / base > 5:
                    ids.append({"col": tag, "space": "person_duni", "d": d, "min": mn, "max": mx,
                                "d_of_base": round(d / ds.size, 4),
                                "max_of_base": round(mx / int(ds.max()), 4),
                                "rows": round(rows, 4), "lift": round(rows / base, 1)})
    return {"table_type": tid, "rtti_class": D.RTTI[tid], "count": n, "stride": stride,
            "lead": lead, "ids": ids, "money": money, "dates": dates}


def selftest() -> int:
    ok = True
    # 正控:t42@0 必须被识别为 person_duni
    e = ev(42)
    hit = [x for x in e["ids"] if x["col"] == "u32@0" and x["space"] == "person_duni"]
    if not hit:
        print("FAIL: t42@0 not flagged as person_duni")
        ok = False
    # 负控:t37@0 (comp) 必须被识别为 comp
    e37 = ev(37)
    if not [x for x in e37["ids"] if x["col"] == "u32@0" and x["space"] == "comp"]:
        print("FAIL: t37@0 not flagged as comp")
        ok = False
    print("selftest:", "ok" if ok else "MISMATCH")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t15d 单表证据摘要(只读)")
    ap.add_argument("--table", type=int, action="append")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    tids = sorted(D.SPEC) if a.all else (a.table or [])
    if not tids:
        ap.print_help()
        return 2
    out = [ev(t) for t in tids]
    for e in out:
        print(f"=== t{e['table_type']} {e['rtti_class']}  {e['count']} x {e['stride']} (lead {e['lead']})")
        for x in e["ids"]:
            extra = f" rows={x['rows']} lift={x['lift']}" if "rows" in x else ""
            print(f"  ID  {x['col']:<8} -> {x['space']:<12} d={x['d']:<7} "
                  f"[{x['min']}..{x['max']}] d/base={x['d_of_base']:<7} max/base={x['max_of_base']}{extra}")
        for x in e["money"]:
            print(f"  MONEY {x['col']:<8} d={x['d']:<6} [{x['min']}..{x['max']}] k1000={x['k1000']} q50={x['q50']}")
        for x in e["dates"]:
            print(f"  DATE  {x['col']:<8} {x['kind']:<5} [{x['min']}..{x['max']}] d={x['d']}")
    if a.json:
        a.json.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"json: {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
