#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成阶段二表身份总报告: 合并 E22 三向表 + E56 12表裁决 + E52/t13 10表锚点。

数据源(全部只读):
  scratch/t01/stage2_three_way.json      E22: 21 已定 table_type
  scratch/cmd/stage2_candidate_adjudication.json  E56: 12 已有候选表裁决
  scratch/t13/out/anchors.json           t13: 10 空白表 + 2 空表锚点
  scratch/cmd/stage2_t13_recheck.json    指挥官对 t13 的独立复核
输出:
  reports/stage2_table_identity.json
  reports/stage2_table_identity.md
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    with open(ROOT / rel, encoding="utf-8") as f:
        return json.load(f)

def build():
    three = load("scratch/t01/stage2_three_way.json")
    adj = load("scratch/cmd/stage2_candidate_adjudication.json")
    t13 = load("scratch/t13/out/anchors.json")
    recheck = load("scratch/cmd/stage2_t13_recheck.json")

    rows = {}
    for r in three["rows"]:
        rows[int(r["table_type"])] = dict(
            table_type=int(r["table_type"]), entity=r.get("entity_tag"),
            status="resolved", level="A", source="E22三向表",
            role=r.get("entity_xml", ""), anchors=r.get("sources", []),
        )
    for r in adj["rows"]:
        tt = int(r["table_type"])
        rows[tt] = dict(
            table_type=tt, entity=r.get("entity"), status=r["status"],
            level=r.get("level"), source="E56裁决", role=r.get("role", ""),
            anchors=r.get("anchors", []), note=r.get("note", ""),
        )
    for r in t13["tables"]:
        tt = int(r["table_type"])
        a = r.get("anchors") or []
        rows[tt] = dict(
            table_type=tt, entity=r.get("entity"), status=r["status"],
            level=(a[0]["kind"] if a else "-"), source="t13锚点",
            role="", anchors=[x.get("claim", "") for x in a],
            note=r.get("why_unresolved", ""),
        )

    # 不在 archive 的 14 张(三向表 unknown 减去 archive 内 24 张)
    in_archive = {r["table_type"] for r in adj["rows"]} | {r["table_type"] for r in t13["tables"]}
    unknown = set(three["table_types_without_row"])
    absent = sorted(unknown - in_archive)

    return dict(
        status="stage2-consolidated",
        n_total=len(rows),
        counts={
            "resolved": sum(1 for r in rows.values() if r["status"] == "resolved"),
            "candidate": sum(1 for r in rows.values() if r["status"] == "candidate"),
            "negative": sum(1 for r in rows.values() if r["status"] == "negative"),
            "empty": sum(1 for r in rows.values() if r["status"] == "empty"),
        },
        not_in_archive=absent,
        rows=[rows[k] for k in sorted(rows)],
        commander_recheck=recheck["commander_recheck"],
        devseek_t13d=recheck.get("devseek_t13d_crosscheck", {}),
        devseek_t13e=recheck.get("devseek_t13e_baselines", {}),
    )

def render_md(cat):
    o = []
    a = o.append
    a("# 阶段二：表身份总清单")
    a("")
    a(f"合并 E22 三向表、E56 十二表裁决、t13 空白表锚点。共 **{cat['n_total']}** 张已归纳表，"
      f"resolved {cat['counts']['resolved']} / candidate {cat['counts']['candidate']} / "
      f"negative {cat['counts']['negative']} / empty {cat['counts']['empty']}。")
    a("")
    a("## 已定表")
    a("")
    a("| type | 实体 | 状态 | 等级 | 来源 | 角色/证据摘要 |")
    a("|---:|---|---|---|---|---|")
    for r in cat["rows"]:
        ev = " / ".join(x for x in (
            r.get("role", ""),
            (r["anchors"][0] if r["anchors"] else ""),
            r.get("note", ""),
        ) if x)
        ev = str(ev).replace("|", "/").replace("\n", " ")[:88]
        a(f"| {r['table_type']} | `{r['entity']}` | {r['status']} | {r['level']} | {r['source']} | {ev} |")
    a("")
    a("## 不在 .dat archive 的表")
    a("")
    a(f"以下 **{len(cat['not_in_archive'])}** 张 table_type 属于工厂专属 / null-return（E24 负结果），"
      "存档里无对应表，保留原始负结果，不改写为“未解”：")
    a("")
    a("`" + "`, `".join(str(x) for x in cat["not_in_archive"]) + "`")
    a("")
    a("## 指挥官独立复核")
    a("")
    c = cat["commander_recheck"]
    a(f"- 静态锚反汇编：{c['detail']}")
    a(f"- schema df：{c['df']}")
    a("- 簇级证据补强：" + "; ".join(
        f"t{u['table']} {u.get('reason') or u.get('note', '')}" for u in c.get("upgrades", [])))
    a("")
    a("### 保留的边界")
    a("")
    for x in c.get("caveats", []):
        a(f"- {x}")
    a("")

    td = cat.get("devseek_t13d", {})
    if td:
        a("## 数据侧交叉（devseek t13d，终版）")
        a("")
        a(f"- t22：{td.get('t22', '')}")
        a(f"- t34：{td.get('t34', '')}")
        dn = td.get("t30_t49_DOWNGRADED", {})
        if dn:
            a(f"- **撤回的交叉项**：{dn.get('issue', '')}")
            a(f"  处理：{dn.get('action', '')}")
            a(f"  仓内可复核的独立基线只有：{dn.get('independent_baselines', '')}")
        a(f"- 易误读处：{td.get('method_note', '')}")
        a("")

    te = cat.get("devseek_t13e", {})
    if te:
        a("## 实体基数清单（devseek t13e）")
        a("")
        a(f"26 条基数，可靠度 {te.get('reliability', '')}，数字冲突 0；{te.get('key_values', '')}。")
        nf = te.get("new_finding", {})
        if nf:
            a(f"- **张力**：{nf.get('issue', '')}")
            a(f"  处理：{nf.get('action', '')}")
        for nc in te.get("name_conflicts", []):
            a(f"- 名字冲突：{nc}")
        a("")
    return "\n".join(o)

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        cat = build()
        assert cat["n_total"] >= 40, cat["n_total"]
        assert cat["counts"]["resolved"] >= 25, cat["counts"]
        assert any(r["table_type"] == 33 and r["entity"] == "club" for r in cat["rows"])
        assert any(r["table_type"] == 12 and r["entity"] == "awar" for r in cat["rows"])
        print("SELFTEST PASS")
        return 0
    cat = build()
    d = ROOT / "reports"
    d.mkdir(exist_ok=True)
    with open(d / "stage2_table_identity.json", "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=1)
    with open(d / "stage2_table_identity.md", "w", encoding="utf-8") as f:
        f.write(render_md(cat))
    print(f"wrote reports/stage2_table_identity.{{json,md}} rows={cat['n_total']} counts={cat['counts']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
