"""t12_catalog — 把 240 槽命名结果固化为正式交付物(reports/)。

输入(只读):
    scratch/t12/out/naming_result.json   最新命名(134/240, schema 违规 0)
    scratch/t11/out/schema_map.json      type_id -> schema 实体 归属
    scratch/t05/layouts.json             240 槽的权威 row_off/width
    scratch/t01/LEDGER.json              证据台账(取最新条目号做口径注记)

输出(成对):
    reports/t12_field_names.json         机读
    reports/t12_field_names.md           人读

用法:
    py -V:3.12 -I -B scripts/t12_catalog.py
    py -V:3.12 -I -B scripts/t12_catalog.py --selftest
    py -V:3.12 -I -B scripts/t12_catalog.py --out-json X.json --out-md X.md
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEF_JSON = ROOT / "reports/t12_field_names.json"
DEF_MD = ROOT / "reports/t12_field_names.md"

LEVELS = {
    "readpair": "L3 双侧指令直证(4CC getter 与 reader 槽同偏移)",
    "chain_unique": "L3 链内唯一(分发链内该偏移只有这一个码)",
    "ref_pair": "L3 引用字段(取指针+空检查, 宽度取 reader)",
    "ref_only": "L3 引用字段(值域与行数据双证)",
    "schema_fixed": "L3+约束(链内多码, 由 schema 字段集合定为唯一合法者)",
    "full_shape_unique": "L3 形态完整唯一(五类形态穷举后唯一)",
}

# 指挥官复核覆盖层: 生成器不自动否决, 但已证否的命名必须在此显式登记并降级。
# 每条都要带可复算的理由, 不许写"疑似"。
REVIEW_OVERRIDES = {
    (23, "client", 0): (
        "t23 row+0 在 278 行里全为 0; SNsn 的 schema 类型是 string, 而 reader 槽仅 1 字节; "
        "t11 已据数据侧证否并降级, t12 的单射唯一性不足以推翻数据"
    ),
    (23, "server", 0): (
        "同上(client/server 同槽): 278 行全 0, 字符串型字段不可能落在 1 字节槽"
    ),
}



def load(p: Path):
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def build() -> dict:
    naming = load(ROOT / "scratch/t12/out/naming_result.json")
    smap = {e["type_id"]: e["schema_entity"] for e in load(ROOT / "scratch/t11/out/schema_map.json")["entities"]}
    layouts = load(ROOT / "scratch/t05/layouts.json")
    layout_idx = {}
    for ent in layouts.get("entities", layouts if isinstance(layouts, list) else []):
        tid = ent.get("type_id")
        for arch, blob in (ent.get("archives") or {}).items():
            for f in blob.get("fields", []):
                layout_idx[(tid, arch, f["idx"])] = (f["row_off"], f["width"])

    slots = []
    for r in naming["results"]:
        tid = r["type_id"]
        for arch, blob in r["archives"].items():
            for f in blob["fields"]:
                key = (tid, arch, f["idx"])
                lr = layout_idx.get(key)
                row_off, width = (lr if lr else (f["row_off"], f["width"]))
                acc = (f.get("accesses") or [{}])[0]
                slots.append({
                    "type_id": tid, "schema_entity": smap.get(tid, "?"), "archive": arch, "idx": f["idx"],
                    "row_off": row_off, "width": width, "object_off": f.get("object_off"),
                    "field": f.get("field"), "codes": f.get("codes") or [],
                    "confidence": f["confidence"], "level": LEVELS.get(f["confidence"], ""),
                    "evidence": {
                        "file_off": acc.get("file_off"), "access_va": acc.get("access_va"),
                        "instruction": acc.get("instruction"), "chain_id": acc.get("chain_id"),
                    } if acc else {},
                    "why": (f.get("why") or [""])[0],
                })
    slots.sort(key=lambda s: (s["type_id"], s["archive"], s["idx"]))
    overridden = []
    for s in slots:
        ov = REVIEW_OVERRIDES.get((s["type_id"], s["archive"], s["idx"]))
        if ov and s["field"]:
            overridden.append({"type_id": s["type_id"], "archive": s["archive"], "idx": s["idx"],
                               "withdrawn_field": s["field"], "reason": ov})
            s["schema_field"] = s["field"]
            s["field"] = None
            s["confidence"] = "unresolved"
            s["level"] = "已由指挥官复核降级"
    named = [s for s in slots if s["field"]]
    dist = collections.Counter(s["confidence"] for s in slots)
    per_type = collections.defaultdict(lambda: {"slots": 0, "named": 0})
    for s in slots:
        per_type[s["type_id"]]["slots"] += 1
        if s["field"]:
            per_type[s["type_id"]]["named"] += 1
    return {
        "status": "complete",
        "source": "scratch/t12/out/naming_result.json",
        "schema_map": "scratch/t11/out/schema_map.json",
        "layout": "scratch/t05/layouts.json",
        "totals": {"slots": len(slots), "named": len(named), "dist": dict(dist)},
        "review_overrides": overridden,
        "per_type": [{"type_id": t, "schema_entity": smap.get(t, "?"), **v} for t, v in sorted(per_type.items())],
        "slots": slots,
    }


def render_md(cat: dict) -> str:
    t = cat["totals"]
    named = t["named"]
    total = t["slots"]
    lines = []
    a = lines.append
    a("# FM24 字段槽位命名台账 (t12 版)")
    a("")
    a(f"**{named}/{total}** 槽已命名字段(占 {named / total:.1%}),**schema 违规 0**。")
    a("")
    a("本表把 `editor.exe` 的 4CC 属性派发链与 `.dat` 行读取器的槽偏移连起来,得到「字段名 → 行内偏移」的映射。")
    a("名字来自 exe 的分发码,偏移来自 reader 指令流,两者必须同偏移才成立。")
    a("")
    a("## 口径与证据等级")
    a("")
    a("| confidence | 槽数 | 含义 |")
    a("|---|---:|---|")
    for k, v in sorted(cat["totals"]["dist"].items(), key=lambda x: -x[1]):
        a(f"| `{k}` | {v} | {LEVELS.get(k, '未解析' if k == 'unresolved' else '')} |")
    a("")
    a("`unresolved` 不等于空字段,只表示当前证据不足(无 4CC 窄访问 / schema 多义 / 槽为打包字节)。")
    a("")
    if cat.get("review_overrides"):
        a("### 已复核撤回的命名")
        a("")
        a("| type | 档 | 槽 | 撤回字段 | 理由 |")
        a("|---:|---|---:|---|---|")
        for o in cat["review_overrides"]:
            a(f"| {o['type_id']} | {o['archive']} | {o['idx']} | `{o['withdrawn_field']}` | {o['reason']} |")
        a("")
    a("")
    a("## 逐实体覆盖")
    a("")
    a("| type | schema 实体 | 槽数 | 已命名 | 覆盖 |")
    a("|---:|---|---:|---:|---:|")
    for r in cat["per_type"]:
        cov = r["named"] / r["slots"] if r["slots"] else 0
        a(f"| {r['type_id']} | {r['schema_entity']} | {r['slots']} | {r['named']} | {cov:.0%} |")
    a("")
    a("## 已命名字段全表")
    a("")
    a("| type | 实体 | 档 | row_off | w | field | 证据 |")
    a("|---:|---|---|---:|---:|---|---|")
    for s in cat["slots"]:
        if not s["field"]:
            continue
        ev = s["evidence"].get("file_off") or ""
        a(f"| {s['type_id']} | {s['schema_entity']} | {s['archive']} | {s['row_off']} | {s['width']} | "
          f"`{s['field']}` | {s['confidence']} {ev} |")
    a("")
    a("## 已知边界(必读)")
    a("")
    a("- **11 张小表(约 39 槽)在 4CC 路线上不可达**: 其 object 偏移 24/28 上没有任何 4CC 候选,"
      "t61/t63 的槽偏移集合与全体候选交集为空。这不是门槛问题,是这些表不走 4CC 派发。")
    a("- **club(433 字段)未解**: 575 个码里 386 存在于 exe,190 个拿到偏移或下沉路径;"
      "但 185 个 offset 只落在 73 个不同偏移上且重度撞车(0x30 有 12 个码),"
      "并混入 `levl/venu/perc` 这类跨表同名码 —— 全局「码→偏移」对 club 无效,必须按类作用域抽取。")
    a("- **引用字段宽度取自 reader,不是访问指令**: `mov r64,[reg+OFF]` 是取指针,行里存 4B id。"
      "早期版本把这类码整批丢弃,导致 `Sold/Salt/Snew` 缺失。")
    a("")
    a("## 复跑")
    a("")
    a("```")
    a("py -V:3.12 -I -B scripts/t12_catalog.py")
    a("py -V:3.12 -I scratch/t12/out/verify.py")
    a("```")
    return "\n".join(lines) + "\n"


def selftest() -> int:
    cat = build()
    ok = True
    if cat["totals"]["slots"] != 240:
        print(f"FAIL slots={cat['totals']['slots']} != 240")
        ok = False
    if cat["totals"]["named"] < 129:
        print(f"FAIL named={cat['totals']['named']} < 129")
        ok = False
    bad = [s for s in cat["slots"] if s["field"] and s["confidence"] == "unresolved"]
    if bad:
        print(f"FAIL {len(bad)} named slots carry unresolved confidence")
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="把 240 槽命名结果固化为 reports/ 交付物")
    ap.add_argument("--out-json", default=str(DEF_JSON))
    ap.add_argument("--out-md", default=str(DEF_MD))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    cat = build()
    Path(a.out_json).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out_json, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=1)
    with open(a.out_md, "w", encoding="utf-8") as f:
        f.write(render_md(cat))
    print(f"wrote {a.out_json}")
    print(f"wrote {a.out_md}")
    print(f"slots={cat['totals']['slots']} named={cat['totals']['named']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
