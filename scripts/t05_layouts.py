"""t05_layouts — 把 reader 宽度序列转成标准行内布局表(row_offsets)。

输入: scratch/t05/reader_widths.json (t05_reader_widths.py 产出)
输出: scratch/t05/layouts.json

每个实体的每个精确命中窗口, 展开成
    [{idx, row_off, width, evidence: "reader width instr @<va>"}]

字段名为 null(尚未 4CC 对齐), 但 offset/width 已由 exe 指令流确定,
且 sum == 业务区宽度(closure 成立) 作为硬约束。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scratch/t05/reader_widths.json"
OUT = ROOT / "scratch/t05/layouts.json"


def pick_best(hits: list[dict]) -> dict[str, dict]:
    """每个 archive 只保留字段数最多的那个精确命中(字段越多信息量越大)。"""
    best: dict[str, dict] = {}
    for h in hits:
        if h["sum"] != h["want"] or h["unknown"]:
            continue
        a = h["archive"]
        if a not in best or h["fields"] > best[a]["fields"]:
            best[a] = h
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(SRC))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    data = json.loads(Path(args.src).read_text(encoding="utf-8"))
    layouts = []
    total_fields = 0
    for r in data["results"]:
        best = pick_best(r.get("hits") or [])
        if not best:
            continue
        per_arch = {}
        for arch, h in best.items():
            off = 0
            fields = []
            for i, w in enumerate(h["widths"]):
                fields.append({"idx": i, "row_off": off, "width": w,
                               "field": None, "confidence": "layout_only"})
                off += w
            assert off == h["want"], (r["type_id"], arch, off, h["want"])
            per_arch[arch] = {
                "business_width": h["want"],
                "field_count": h["fields"],
                "closure": f"sum(widths) == {h['want']} == stride-13",
                "window": [h["start"], h["end"]],
                "fields": fields,
            }
            total_fields += h["fields"]
        layouts.append({
            "type_id": r["type_id"],
            "entity": r["entity"],
            "mode": r.get("mode"),
            "reader_entry": r.get("reader"),
            "reader_body": r.get("body"),
            "thunk_chain": r.get("thunk_chain"),
            "archives": per_arch,
        })

    Path(args.out).write_text(json.dumps({
        "note": "字段 offset/width 由 editor.exe reader 指令流的 mov r8d,N + call [rax+0x28] 累加确定;"
                "field 名为 null 表示尚未做 4CC getter 对齐。closure 硬约束: sum(width)==业务区宽度==stride-13。",
        "exe_sha256": data.get("exe_sha256"),
        "summary": {"entities": len(layouts), "fields": total_fields},
        "layouts": layouts,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"实体 {len(layouts)} 个, 字段布局 {total_fields} 条 -> {args.out}")
    print()
    print("type entity        client(宽/字段)   server(宽/字段)")
    for L in layouts:
        c = L["archives"].get("client")
        s = L["archives"].get("server")
        cs = f"{c['business_width']}B/{c['field_count']}f" if c else "-"
        ss = f"{s['business_width']}B/{s['field_count']}f" if s else "-"
        print(f"{L['type_id']:>4} {str(L['entity']):<13} {cs:<15} {ss}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
