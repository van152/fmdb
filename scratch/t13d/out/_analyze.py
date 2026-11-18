#!/usr/bin/env python3
"""t13d 旁路:四张 server 表的列统计与候选实体量级比对(只读,输出到 scratch/t13d/out/)。

对每张表把行体按 u32 小端切列(前 20 列),统计 distinct/min/max/0 与 0xFFFFFFFF 比例,
再与候选实体已知基数比对,给出"量级吻合/不吻合/无法判断"。
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch/t13d/out"
FF = 0xFFFFFFFF
U32 = 0xFFFFFFFF + 1

TABLES = {
    22: {"files": ["t22.csv"], "count": 449, "stride": 79,
         "candidates": [("club", 3000, 6000), ("nation", 251, 251)]},
    30: {"files": ["t30.csv"], "count": 72473, "stride": 34,
         "candidates": [("player", 70000, 76000), ("club", 3000, 6000)]},
    34: {"files": ["t34.csv"], "count": 7115, "stride": 44,
         "candidates": [("club", 3000, 6000), ("nation", 251, 251)]},
    49: {"files": ["t49.csv"], "count": 792149, "stride": 36,
         "candidates": [("person", 760000, 820000), ("player", 70000, 76000)]},
}


def load_rows(path: pathlib.Path):
    import csv
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(bytes.fromhex(r["raw_hex"]))
    return out


def colstats(rows, ncols=20):
    cols = []
    w = min(len(r) for r in rows)
    for c in range(ncols):
        o = c * 4
        if o + 4 > w:
            break
        vals = [int.from_bytes(r[o:o + 4], "little") for r in rows]
        cnt = collections.Counter(vals)
        n = len(vals)
        top = cnt.most_common(3)
        cols.append({
            "col": c, "u32_offset": o,
            "distinct": len(cnt),
            "min": min(vals), "max": max(vals),
            "zero_ratio": round(cnt.get(0, 0) / n, 4),
            "ff_ratio": round(cnt.get(FF, 0) / n, 4),
            "top": [[v, c2] for v, c2 in top],
            "monotonic_unique": (max(vals) < n * 32 and len(cnt) == n),
        })
    return cols


def verdict(tid, rows, csv_path):
    spec = TABLES[tid]
    n = len(rows)
    cols = colstats(rows)
    # 行数列:找出"看似身份 ID"的列 —— distinct 接近行数且值域不超过行数数倍
    id_like = [c for c in cols if c["distinct"] >= 0.99 * n and c["max"] < n * 64]
    res = {
        "table_type": tid,
        "csv": str(csv_path.relative_to(ROOT)).replace("\\", "/"),
        "rows_dumped": n,
        "declared_count": spec["count"],
        "stride": spec["stride"],
        "cols": cols,
        "id_like_cols": [{"col": c["col"], "distinct": c["distinct"], "max": c["max"]} for c in id_like],
        "candidates": [],
    }
    for name, lo, hi in spec["candidates"]:
        if lo <= n <= hi:
            res["candidates"].append({"entity": name, "expected_rows": [lo, hi], "row_count_fit": True})
        else:
            res["candidates"].append({"entity": name, "expected_rows": [lo, hi], "row_count_fit": False})
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(OUT / "audit.json"))
    ap.add_argument("--md", default=str(OUT / "quick_audit.md"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--only", type=int, action="append")
    a = ap.parse_args()
    if a.selftest:
        rows = [bytes(8), int(1).to_bytes(4, "little") + bytes(4)]
        print(colstats(rows, 2))
        return 0

    out = {"status": "ok", "tool": "t13d quick audit", "tables": []}
    for tid, spec in sorted(TABLES.items()):
        if a.only and tid not in a.only:
            continue
        p = OUT / spec["files"][0]
        if not p.exists():
            out["tables"].append({"table_type": tid, "error": "csv missing"})
            out["status"] = "partial"
            continue
        rows = load_rows(p)
        out["tables"].append(verdict(tid, rows, p))

    pathlib.Path(a.json).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {a.json}")
    for t in out["tables"]:
        if "error" in t:
            print(t["table_type"], t["error"])
            continue
        print(f"\n== table_{t['table_type']} rows={t['rows_dumped']} stride={t['stride']}")
        for c in t["cols"]:
            print(f"  c{c['col']:<2d} d={c['distinct']:<8d} min={c['min']:<12d} max={c['max']:<12d} "
                  f"0={c['zero_ratio']:<6} FF={c['ff_ratio']:<6} top={c['top'][:2]}")
        print("  id_like:", t["id_like_cols"])
        print("  fit:", [(c["entity"], c["row_count_fit"]) for c in t["candidates"]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
