#!/usr/bin/env python3
"""t91 §2: 外源 fm-data 码表样例 vs 我们 master.json 全码表 diff。

外源 field_dict.csv(2103 条)不在克隆内(agentA §3 明示它在 work/agentA_re/),
因此可恢复的外源码只有报告正文引用的 **18 个 pers,* 样例** + 12 个表标签声明。
本脚本产出三清单:
  ① we_have_they_lack  — 我们有、外源样例没有(按码表规模给出,非逐条)
  ② they_have_we_lack  — 外源有、我们没有
  ③ both_but_conflict  — 双方都有但标签/表域冲突

外部代码一律不执行;只读 JSON 与 Markdown 正文。

用法:
  py -V:3.12 -I -B scripts/t91_codes.py [--help] [--selftest] [--out PATH]
退出码: 0 完成 / 1 检查未过 / 2 用法或致命错误
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
EXT_DOCS = ROOT / "scratch/ext/fm-data/docs/reports"
OUT = ROOT / "scratch/t91/out/code_coverage.json"
PROV = "ext/fm-data@d7a7150"

# agentA-native-re.md §3 表格逐行抄录(db_field, 外源 label)。只抄,不改写。
EXT_SAMPLES = [
    ("duni", "unique id"), ("PnRV", "name"), ("Pfna", "first name"),
    ("Psna", "second name"), ("Pcna", "common name"), ("Page", "age"),
    ("Pcbi", "city of birth"), ("Pnbi", "nation of birth"), ("Ncra", "current ability"),
    ("Npta", "potential ability"), ("Pnti", "nation"), ("Pcti", "club"),
    ("Ppsr", "position"), ("Pcwg", "wage"), ("Pcex", "contract expires"),
    ("PMsq", "squad status"), ("PCJO", "club primary job"), ("PSJO", "club secondary job"),
]
# briefing.md §Key files 声明的 12 个表标签
EXT_TAGS = ["pers", "club", "comp", "natc", "stad", "team", "weat", "awar",
            "inju", "nati", "city", "agrm"]
# 外源 §3 里 pers 码的 "table" 前缀(agentA 表格均为 pers,*)
EXT_PREFIX = "pers"

# 标签规范化:小写、去空格、去 "of/the"、去标点,用于判断"同义不同写法"
import re


def norm_label(s):
    if s is None:
        return None
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\b(the|of|a|an)\b", " ", s)
    return " ".join(s.split())


def _selftest() -> int:
    assert norm_label("City Of Birth") == "city birth"
    assert norm_label("city of birth") == "city birth"
    assert norm_label(None) is None
    assert norm_label("Club Primary Job") == "club primary job"
    print("selftest OK: label normalisation")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--help", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)
    if a.help:
        print(__doc__)
        return 0
    if a.selftest:
        return _selftest()

    m = json.loads(MASTER.read_text(encoding="utf-8"))
    fc = m["field_codes"]
    our_tags = {}
    for code, v in fc.items():
        for loc in v.get("locations", []):
            our_tags.setdefault(loc.split("#")[-1], set()).add(code)

    rows, they_lack, conflicts, exact = [], [], [], 0
    for code, ext_label in EXT_SAMPLES:
        v = fc.get(code)
        if v is None:
            they_lack.append({"code": code, "external_label": ext_label,
                              "note": "code absent from our 3009-code table"})
            rows.append({"code": code, "external_label": ext_label,
                         "status": "missing_in_ours"})
            continue
        ours = v.get("name")
        tags = sorted({loc.split("#")[-1] for loc in v.get("locations", [])})
        same_label = norm_label(ours) == norm_label(ext_label)
        in_pers = EXT_PREFIX in tags
        entry = {
            "code": code, "external_label": ext_label, "our_label": ours,
            "our_types": v.get("type"), "our_table_tags": tags,
            "external_table_tag": EXT_PREFIX,
            "label_match_normalised": same_label,
            "external_tag_present_in_our_locations": in_pers,
        }
        rows.append(entry)
        if same_label:
            exact += 1
        else:
            conflicts.append({**entry, "kind": "label_mismatch"})
        if not in_pers:
            conflicts.append({**entry, "kind": "table_domain_mismatch"})

    # 表标签对照
    tag_rows = []
    for t in EXT_TAGS:
        tag_rows.append({"external_tag": t,
                         "our_code_count": len(our_tags.get(t, ())),
                         "present": t in our_tags})
    ext_tags_missing = [r["external_tag"] for r in tag_rows if not r["present"]]
    our_tags_absent = sorted(set(our_tags) - set(EXT_TAGS))

    res = json.loads(pathlib.Path(a.out).read_text(encoding="utf-8")) \
        if pathlib.Path(a.out).exists() else {}
    res["provenance"] = {
        "external": PROV, "external_commit_date": "2026-11-11",
        "external_role": "hypothesis source only; never upgrades our L1/L2/L3",
        "our_schema": "evidence/fm24/reports/editor_schema/master.json",
        "our_game_version": m["meta"].get("game_version"),
        "external_game_version": "26.2.0 / 26.3.2",
        "field_dict_csv_present_in_clone": False,
        "field_dict_csv_note": ("agentA §3: field_dict.csv (2103 entries, 739 pers) "
                                "lives in their work/agentA_re/ which is NOT in the clone; "
                                "only the 18 pers samples quoted in report prose are recoverable"),
    }
    res["our_code_space"] = {
        "distinct_field_codes": len(fc),
        "distinct_table_tags": len(our_tags),
        "codes_without_name": sum(1 for v in fc.values() if not v.get("name")),
        "pers_codes": len(our_tags.get("pers", ())),
        "external_claimed_total_codes": 2103,
        "external_claimed_pers_codes": 739,
        "comparison_scope": "18 of 2103 external codes (0.86%)",
    }
    res["section_code_table_diff"] = {
        "state": "complete",
        "counts": {
            "external_codes_recoverable": len(EXT_SAMPLES),
            "both_present": len(EXT_SAMPLES) - len(they_lack),
            "both_label_exact_after_normalisation": exact,
            "they_have_we_lack": len(they_lack),
            "conflicts": len(conflicts),
            "conflicts_label_only": sum(1 for c in conflicts if c["kind"] == "label_mismatch"),
            "conflicts_table_domain": sum(1 for c in conflicts
                                          if c["kind"] == "table_domain_mismatch"),
        },
        "list_1_we_have_they_lack": {
            "note": ("cannot be enumerated: external field_dict.csv absent. Only a scale "
                     "statement is defensible — our table has 3009 codes vs their 2103, "
                     "and 271 codes are pers-scoped vs their 739."),
            "our_codes": len(fc), "external_codes": 2103,
            "our_pers_codes": len(our_tags.get("pers", ())), "external_pers_codes": 739,
            "scale_delta": len(fc) - 2103,
            "caveat": "FM26 vs FM24 code-table version drift; delta is NOT evidence of coverage gap",
        },
        "list_2_they_have_we_lack": they_lack,
        "list_3_both_but_conflict": conflicts,
        "per_code": rows,
        "table_tags": {
            "external_claimed": EXT_TAGS,
            "our_counts": {t: len(c) for t, c in sorted(our_tags.items())},
            "external_tags_missing_in_ours": ext_tags_missing,
            "our_tags_outside_external_claim_count": len(our_tags_absent),
            "note": ("`natc` is claimed by the external report but does not exist as a table "
                     "tag in our schema; we have `nati` (339 codes) + nation.xml. "
                     "Recorded as a domain-naming conflict, not as our gap."),
        },
    }
    res["status"] = "complete" if res.get("section_nulldate_probe", {}).get("state") == "complete" \
        else res.get("status", "in_progress")
    pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    c = res["section_code_table_diff"]["counts"]
    print(f"ext codes recoverable={c['external_codes_recoverable']} both={c['both_present']} "
          f"label_exact={c['both_label_exact_after_normalisation']} "
          f"they_have_we_lack={c['they_have_we_lack']} conflicts={c['conflicts']}")
    print(f"our codes={len(fc)} tags={len(our_tags)} pers={len(our_tags.get('pers', ()))}")
    print("ext tags missing in ours:", ext_tags_missing)
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
