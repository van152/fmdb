"""t05_ref_match — 用"值域对齐目标表行数"批量识别 4 字节引用字段。

方法论(由 t06 在 city 上验证):
    若某 4B 槽的非哨兵值域 ⊆ [0, N) 且 N 恰为某张表的行数,
    则该字段几乎必然是那张表的记录引用。

city 三例已证:
    Cwea off14 max=333 -> type27 weather count=334
    Clgi off21 max=112 -> type8  language count=126 (81.7% 为 0xFFFFFFFF 哨兵)
    Clri off25 max=2476 -> type47 lcrg count=2488

判据(全部需同时满足):
    1. 槽宽 4B
    2. distinct >= 8 (排除常量/小枚举)
    3. 非哨兵 max < N 且 N == 某表 count
    4. 值域覆盖率: 非哨兵值 >= 50% 落在 [0,N)  (对无符号解释)
    5. 唯一性: 若多个表都满足, 按 (max/N 接近度, distinct) 排序并标注歧义

用法:
    py -V:3.12 -I -B scripts/t05_ref_match.py                 # 全部实体
    py -V:3.12 -I -B scripts/t05_ref_match.py --type 2        # 单实体
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "scratch/t05/layouts.json"
COVERAGE = ROOT / "scratch/t05/COVERAGE.json"
OUT = ROOT / "scratch/t05/ref_matches.json"

SENTINELS = {0xFFFFFFFF, 0xFFFFFFFE, 0x7FFFFFFF}
MIN_DISTINCT = 8
MIN_COVER = 0.50
MIN_FILL = 0.80   # 真引用通常接近满填(max/N 接近 1); 低于此值多为值域巧合


def load_tables() -> list[dict]:
    cov = json.loads(COVERAGE.read_text(encoding="utf-8"))
    out = []
    seen = set()
    for r in cov["tables"]:
        c = r.get("count")
        if not isinstance(c, int) or c < 8:
            continue
        key = (r["table_id"], c)
        if key in seen:
            continue
        seen.add(key)
        out.append({"table_id": r["table_id"], "entity": r.get("entity") or "?",
                    "archive": r["archive"], "count": c})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", type=int, default=None)
    ap.add_argument("--min-fill", type=float, default=MIN_FILL)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    import importlib.util
    spec = importlib.util.spec_from_file_location("_dmp", ROOT / "scripts/fm24_dump.py")
    dmp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dmp)
    codec = dmp._reader()
    specs = dmp.fixed_specs()
    tables = load_tables()
    lay = json.loads(LAYOUTS.read_text(encoding="utf-8"))

    results = []
    total_new = 0
    for L in lay["layouts"]:
        tid = L["type_id"]
        if args.type is not None and tid != args.type:
            continue
        per_arch = {}
        for arch, v in L["archives"].items():
            sp = specs.get((arch, tid))
            if not sp:
                continue
            try:
                raw = dmp.load_payload(codec, arch, tid)
            except Exception:
                continue
            H, ST, N = sp["header"], sp["stride"], sp["count"]
            slots = []
            for f in v["fields"]:
                if f["width"] != 4:
                    continue
                off = f["row_off"]
                vals = [int.from_bytes(raw[H + i * ST + off:H + i * ST + off + 4], "little")
                        for i in range(N)]
                sent = sum(1 for x in vals if x in SENTINELS)
                real = [x for x in vals if x not in SENTINELS]
                if not real:
                    continue
                dist = len(set(real))
                if dist < MIN_DISTINCT:
                    continue
                mx = max(real)
                cands = []
                for t in tables:
                    if t["count"] <= mx:
                        continue
                    inside = sum(1 for x in real if x < t["count"]) / len(real)
                    if inside < MIN_COVER:
                        continue
                    fill = mx / t["count"]
                    if fill < MIN_FILL:
                        continue
                    cands.append({"table_id": t["table_id"], "entity": t["entity"],
                                  "archive": t["archive"], "count": t["count"],
                                  "inside_ratio": round(inside, 4),
                                  "fill_ratio": round(fill, 3)})
                if not cands:
                    continue
                # 填满度越高越可能是该表全量引用; inside 高更可靠
                cands.sort(key=lambda c: (-c["inside_ratio"], -c["fill_ratio"], c["count"]))
                best = cands[0]
                ambiguous = len(cands) > 1 and abs(cands[0]["count"] - cands[1]["count"]) < max(8, 0.02 * cands[0]["count"])
                slots.append({
                    "row_off": off, "width": 4, "distinct": dist,
                    "sentinel_ratio": round(sent / N, 4),
                    "max": mx, "best": best,
                    "ambiguous": ambiguous,
                    "rivals": cands[1:4] if ambiguous else [],
                    "confidence": "ref_match_low" if ambiguous else "ref_match",
                })
                if not ambiguous:
                    total_new += 1
            if slots:
                per_arch[arch] = {"count": N, "slots": slots}
        if per_arch:
            results.append({"type_id": tid, "entity": L["entity"], "archives": per_arch})

    Path(args.out).write_text(json.dumps({
        "note": "4B 槽的值域对齐目标表行数 -> 引用字段候选。confidence=ref_match 表示唯一表匹配;"
                "ref_match_low 表示多表歧义(见 rivals)。哨兵按 0xFFFFFFFF/0xFFFFFFFE/0x7FFFFFFF 计。",
        "tables_considered": len(tables),
        "results": results,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"表候选 {len(tables)} 张; 无歧义引用字段匹配 {total_new} 个; 实体 {len(results)}")
    print()
    for r in results:
        if args.type is not None:
            print(f"type {r['type_id']} {r['entity']}")
            for arch, a in r["archives"].items():
                print(f"  [{arch}] n={a['count']}")
                for s in a["slots"]:
                    b = s["best"]
                    print(f"    row+{s['row_off']:<3} distinct={s['distinct']:<5} max={s['max']:<7} "
                          f"-> table_{b['table_id']}({b['entity']}) count={b['count']} "
                          f"inside={b['inside_ratio']} fill={b['fill_ratio']} "
                          f"{'AMBIG' if s['ambiguous'] else ''}")
        else:
            n = sum(len(a["slots"]) for a in r["archives"].values())
            na = sum(1 for a in r["archives"].values() for s in a["slots"] if not s["ambiguous"])
            print(f"{r['type_id']:>4} {str(r['entity']):<12} 4B槽命中={n:>3} 无歧义={na:>3}")
    print()
    print(f"写出 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
