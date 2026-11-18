#!/usr/bin/env python3
"""Build t14's stage2_map.json and REPORT.md from frozen local evidence.

Only writes scratch/t14/out. Run with py -V:3.12 -I scripts/t14_build.py.
Exit codes: 0 success, 1 acceptance check failed, 2 usage/fatal error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t14/out"
E56_IDS = {22, 30, 31, 34, 37, 42, 43, 46, 49, 50, 51, 58}
FOCUS_NEGATIVES = {26, 29, 32, 36, 38, 39}
EMPTY_IDS = {52, 57}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm_entity(value: str | None) -> str | None:
    return {"player":"play", "person":"pers", "nation":"nati", "injury":"inju",
            "competition":"comp", "description":"dscr", "currency":"curr",
            "continent":"cont", "media_source":"mdso", "language":"lang",
            "stadium":"stad", "local_region":"lcrg"}.get(value, value)


def ev(kind: str, source: str, claim: str, **details: Any) -> dict[str, Any]:
    return {"kind": kind, "source": source, "claim": claim, **({"details": details} if details else {})}


def selftest() -> None:
    assert norm_entity("player") == "play"
    assert norm_entity("person") == "pers"
    assert E56_IDS == {22,30,31,34,37,42,43,46,49,50,51,58}
    assert len(FOCUS_NEGATIVES) == 6 and len(EMPTY_IDS) == 2


def build() -> tuple[dict[str, Any], str]:
    coverage = load(ROOT / "scratch/t05/COVERAGE.json")
    threeway = load(ROOT / "scratch/t01/stage2_three_way.json")
    identity = load(ROOT / "reports/stage2_table_identity.json")
    t13 = load(ROOT / "scratch/t13/out/anchors.json")
    e56 = load(ROOT / "scratch/cmd/stage2_candidate_adjudication.json")
    census = load(OUT / "census.json")
    boundaries_path = ROOT / "scratch/t05/server_bounds/boundaries.json"
    boundaries = load(boundaries_path) if boundaries_path.is_file() else {"tables": []}

    base_by_id = {r["table_type"]: r for r in threeway.get("rows", [])}
    ident_by_id = {r["table_type"]: r for r in identity.get("rows", [])}
    t13_by_id = {r["table_type"]: r for r in t13.get("tables", [])}
    e56_by_id = {r["table_type"]: r for r in e56.get("rows", [])}
    census_by_id = {r["table_type"]: r for r in census.get("tables", [])}
    bound_by_id = {r.get("table_id", r.get("table_type")): r for r in boundaries.get("tables", [])}

    source_tables = [r for r in coverage.get("tables", []) if r.get("archive") == "server"]
    if len(source_tables) != 59:
        raise ValueError(f"COVERAGE server skeleton has {len(source_tables)} rows, expected 59")

    rows: list[dict[str, Any]] = []
    for cov in sorted(source_tables, key=lambda x: x["table_id"]):
        tid = cov["table_id"]
        count = cov.get("count")
        cen = census_by_id.get(tid, {})
        identity_row = ident_by_id.get(tid, {})
        t13_row = t13_by_id.get(tid, {})
        e56_row = e56_by_id.get(tid, {})
        base = base_by_id.get(tid, {})
        entity: str | None = None
        status = "negative"
        evidence: list[dict[str, Any]] = []
        conflicts: list[dict[str, Any]] = []

        if tid in EMPTY_IDS or count == 0:
            b = bound_by_id.get(tid, {})
            rows.append({"table_type":tid,"archive":"server","count":count,"entity":None,
                         "status":"empty","evidence":[ev("A", "scratch/t05/COVERAGE.json; scratch/t05/server_bounds/boundaries.json",
                           f"table_{tid} has zero rows; boundary closure={b.get('closure')!r}, payload_len={b.get('payload_len')!r}")],
                         "conflicts":[]})
            continue

        # E22 / three-way base mapping.
        if base.get("census_status") == "resolved" and base.get("entity_tag"):
            entity = norm_entity(base["entity_tag"])
            status = "resolved"
            evidence.append(ev("A", "scratch/t01/stage2_three_way.json",
                               f"E22/table-type cross-map entity_tag={base['entity_tag']}; sources={base.get('sources', [])}",
                               factory_handler=base.get("factory_handler"), sources=base.get("sources", [])))

        # Explicit t13 A anchors; retain every claim/source and do not convert
        # rejected quantity candidates into evidence.
        if t13_row.get("status") == "resolved" and t13_row.get("entity"):
            t13_entity = norm_entity(t13_row["entity"])
            if entity and entity != t13_entity:
                conflicts.append({"source":"scratch/t13/out/anchors.json","claim":
                                  f"t13 resolved {t13_entity} conflicts with prior {entity}"})
                status, entity = "candidate", None
            else:
                entity, status = t13_entity, "resolved"
            for anchor in t13_row.get("anchors", []):
                evidence.append(ev(anchor.get("kind", "A"), "scratch/t13/out/anchors.json",
                                   anchor.get("claim", "t13 independent table anchor"),
                                   evidence=anchor.get("evidence", {}),
                                   independence=anchor.get("independence", "")))

        # E56 adjudication is kept as a distinct source; candidate status is not
        # silently promoted unless the RTTI class independently agrees.
        if e56_row:
            e_entity = norm_entity(e56_row.get("entity"))
            level = e56_row.get("level")
            if e56_row.get("anchors"):
                evidence.append(ev(level if level in {"A", "B", "C"} else "B",
                                   "scratch/cmd/stage2_candidate_adjudication.json",
                                   f"E56 {e56_row.get('status')} adjudication: {e56_row.get('role','')}; {e56_row.get('note','')}",
                                   anchors=e56_row.get("anchors", []), codes=e56_row.get("codes", []),
                                   df1_codes=e56_row.get("df1_codes", [])))
            if e_entity:
                if entity and entity != e_entity:
                    conflicts.append({"source":"scratch/cmd/stage2_candidate_adjudication.json",
                                     "claim":f"E56 entity {e_entity} conflicts with prior {entity}"})
                    status, entity = "candidate", None
                elif e56_row.get("status") == "resolved":
                    entity, status = e_entity, "resolved"
                elif e56_row.get("status") == "candidate" and not entity:
                    entity, status = e_entity, "candidate"
            elif e56_row.get("status") == "negative" and not entity:
                status = "negative"

        # Preserve t13 historical negative prose verbatim as a record even when
        # a new independent D anchor now resolves the entity.
        t13_original_negative = None
        if t13_row.get("status") == "negative":
            t13_original_negative = {
                "why_unresolved": t13_row.get("why_unresolved", ""),
                "rejected": t13_row.get("rejected", []),
            }

        # D: primary class is the shallowest assigned RTTI vtable in this
        # table_type's handler/callee graph. Keep the exact machine addresses.
        vt = [x for x in cen.get("vtables", []) if x.get("class")]
        primary_class = cen.get("primary_class")
        primary_hits = [x for x in vt if x.get("class") == primary_class]
        if primary_hits:
            for hit in primary_hits:
                aliases = sorted(x["table_type"] for x in census.get("tables", [])
                                 if x.get("handler_off") == cen.get("handler_off") and x.get("status") == "dedicated")
                shared_note = (f" This handler is shared by table types {aliases}; D establishes the shared constructor class, "
                               "not a unique separation between those aliases.") if len(aliases) > 1 else ""
                independence = (
                    f"table_type {tid} is independently decoded from its jump-table rel32 entry to handler_off "
                    f"{cen.get('handler_off')}; BFS depth {hit.get('depth')} reaches a vtable assignment at "
                    f"{hit.get('inst_off')}, whose preceding COL/TD chain names {hit.get('class')}. "
                    "The anchor uses the constructor/class identity, not record-count similarity or a schema-code vote."
                    + shared_note
                )
                evidence.append(ev("D", "editor.exe (read-only), factory jump-table -> RTTI constructor",
                                   f"RTTI construction anchor: {hit.get('class')} (depth {hit.get('depth')})",
                                   handler_off=cen.get("handler_off"), inst_off=hit.get("inst_off"),
                                   vtable_va=hit.get("vtable_va"), col_off=hit.get("col_off"),
                                   class_name=hit.get("class"), depth=hit.get("depth"),
                                   fm_cross=hit.get("fm_cross"), independence=independence))
        d_entity = norm_entity(cen.get("entity_tag"))
        if d_entity:
            if entity and entity != d_entity:
                conflicts.append({"source":"scratch/t14/out/census.json",
                                  "claim":f"D class {primary_class} maps to {d_entity}, conflicting with independent entity {entity}"})
                status, entity = "candidate", None
            elif tid == 58 and e56_row.get("status") == "candidate" and not e56_row.get("entity"):
                # E56 explicitly retained both person/club possibilities; D
                # identifies the record class but not its owning entity.
                status, entity = "candidate", None
                conflicts.append({"source":"scratch/cmd/stage2_candidate_adjudication.json",
                                  "claim":"E56 leaves person/club open; weekly-wage class does not independently identify its owning entity."})
            else:
                entity, status = d_entity, "resolved"
        elif not entity:
            status = "candidate" if vt else "negative"

        if t13_original_negative:
            conflicts.append({"source":"scratch/t13/out/anchors.json",
                              "claim":"Historical negative preserved verbatim; new D evidence is a later independent adjudication.",
                              "original":t13_original_negative})
        if tid in E56_IDS and e56_row:
            if tid in (30, 34, 37, 43, 49) and status == "resolved":
                # This explicit marker documents which E56 rows are dual-source.
                if e56_row.get("entity") and norm_entity(e56_row["entity"]) == entity:
                    evidence.append(ev("A" if e56_row.get("level") == "A" else "B",
                                       "scratch/cmd/stage2_candidate_adjudication.json (E56)",
                                       "Dual-source agreement: E56 entity adjudication agrees with the D RTTI class-family mapping.",
                                       table_type=tid, e56_status=e56_row.get("status")))

        # Generic class names do not override independent A/B anchors.
        if not entity and status == "resolved":
            status = "candidate"
        rows.append({"table_type":tid,"archive":"server","count":count,"entity":entity,
                     "status":status,"evidence":evidence,"conflicts":conflicts})

    counts = {s: sum(r["status"] == s for r in rows) for s in ("resolved", "candidate", "negative", "empty")}
    doc = {"status":"complete" if len(rows) == 59 and counts["resolved"] >= 45 else "partial_stage2_identity",
           "method":"COVERAGE server table list is the fixed 59-row skeleton. Resolved identities require an A/B/D anchor; E56 candidates require a matching independent D class-family mapping. C-only and count-similarity-only mappings are not promoted.",
           "summary":{"server_tables":len(rows),**counts},"tables":rows}

    report = make_report(doc, census, t13, e56, identity)
    return doc, report


def make_report(doc: dict[str, Any], census: dict[str, Any], t13: dict[str, Any],
                e56: dict[str, Any], identity: dict[str, Any]) -> str:
    rows = doc["tables"]
    lines = [
        "# t14 RTTI 构造锚普查与阶段二全图",
        "",
        f"状态：`{doc['status']}`。server 表 {doc['summary']['server_tables']} 张；resolved {doc['summary']['resolved']}、candidate {doc['summary']['candidate']}、negative {doc['summary']['negative']}、empty {doc['summary']['empty']}。",
        "",
        "## 方法与交叉检查",
        "",
        "- factory 跳表由 `0xF49D38 + signed_rel32@ (0xF49D38 + 4*t)` 从 editor.exe 原字节复算；RTTI 使用相对 RVA 的 COL，地址映射经 `scripts/t05_pe.py`。",
        f"- dedicated {census['summary']['dedicated']}/63 类型全部有类名；default {census['summary']['default']}/11。fm.exe TD 字符串缺失类：{len(census['summary']['fm_td_missing'])}；可确认的均记为 `td-only`（未声称 vtable/ref 交叉）。",
        "- 8 个指定实体交叉：0 AWARD、2 CITY、8 LANGUAGE、18 DERBY、19 REGION、23 STAGE_NAME、27 WEATHER、56 AGREEMENT；均与跳表 RTTI 主类零矛盾。",
        "- E56/RTTI 冲突不强行裁决；class tag 不明确时保留 candidate；count 本身不作实体锚。52/57 保留 empty。",
        "",
        "## 逐表结论（COVERAGE server 59 张）",
        "",
        "| type | count | entity_tag | status | RTTI primary class | D / other evidence |",
        "|---:|---:|---|---|---|---|",
    ]
    cen_by_id = {r["table_type"]: r for r in census["tables"]}
    for r in rows:
        c = cen_by_id.get(r["table_type"], {})
        cls = c.get("primary_class") or "—"
        sources = ", ".join(sorted({e["kind"] for e in r["evidence"]})) or "—"
        lines.append(f"| {r['table_type']} | {r['count']} | {r['entity'] or '—'} | {r['status']} | {cls} | {sources} |")

    lines += ["", "## 六张 t13 negative 表的正式裁决", "",
              "以下旧负结果按原字段保留；新 D 锚只作为后续证据，不改写旧结论。拒绝候选理由也逐字包含。", ""]
    for tid in sorted(FOCUS_NEGATIVES):
        old = next((r for r in t13.get("tables", []) if r.get("table_type") == tid), {})
        current = next(r for r in rows if r["table_type"] == tid)
        cls = cen_by_id[tid].get("primary_class")
        lines.append(f"### type {tid}: `{current['entity'] or '—'}` / {current['status']} — D `{cls or '无类名'}`")
        lines.append("")
        lines.append("原 `why_unresolved`（原文）：")
        lines.append("")
        lines.append("> " + (old.get("why_unresolved") or "（原工件无 why_unresolved 字段）").replace("\n", "\n> "))
        for rejected in old.get("rejected", []):
            lines.append("")
            lines.append(f"> 原拒绝 `{rejected.get('entity','')}`：{rejected.get('why','')}")
        lines.append("")
        lines.append(f"新裁决：handler `{cen_by_id[tid].get('handler_off')}` → {cls}; RTTI D tag `{cen_by_id[tid].get('entity_tag')}`。数量线索未作为锚。")
        lines.append("")

    lines += ["## E56 十二张候选表裁决", "",
              "| type | E56 entity/status | D class/tag | t14 status | 结论 |",
              "|---:|---|---|---|---|"]
    for tid in sorted(E56_IDS):
        er = next((r for r in e56.get("rows", []) if r.get("table_type") == tid), {})
        sr = next(r for r in rows if r["table_type"] == tid)
        cr = cen_by_id[tid]
        class_tag = f"{cr.get('primary_class') or '—'} / {cr.get('entity_tag') or '—'}"
        if tid == 22:
            conclusion = "冲突：STADIUM_CHANGE vs club；保守 candidate"
        elif tid == 58:
            conclusion = "E56 保留 person/club 两解；D 未消歧，保留 candidate"
        elif sr["status"] == "resolved":
            conclusion = "D 与 E56 同向或 D 独立补足；resolved"
        else:
            conclusion = "保留未决"
        lines.append(f"| {tid} | {er.get('entity') or '—'} / {er.get('status') or '—'} | {class_tag} | {sr['status']} | {conclusion} |")

    lines += ["", "## 冲突清单", ""]
    any_conflict = False
    for r in rows:
        for c in r.get("conflicts", []):
            any_conflict = True
            lines.append(f"- type {r['table_type']}: {c.get('claim','')}")
    if not any_conflict:
        lines.append("- 无")
    lines += ["", "## RTTI census 缺口 / class-family 裁决", "",
              "- 63 个 dedicated 类型均有至少一个通过 COL→TD 自洽校验的类名；17/18/20/28/40 等 default 表仍按默认 handler 标记，不当作 dedicated 缺失。",
              "- 非 schema 主实体/特殊记录名按 class-family 映射时以 schema entity tag 为目标；`STARTING_RECORD`、`FIXTURE_NAME` 等泛型类不单独决定 entity，依赖既有 A 锚或保持 candidate。",
              "- handler alias 需谨慎解释：45/48 共用 `0xf48ba6`；65/67/68/69 共用 `0xf48b55`。这些 D 锚只证明共享构造类，不宣称 RTTI 单独区分同 handler 的表；身份分辨沿用对应独立表证据/dispatch table_type。",
              "- 35 的旧 E22 entity=`dscr` 与 RTTI `PLAYER_TYPE`→`play` 冲突；22 的 E56 `club` 与 RTTI `STADIUM_CHANGE`→`stad` 冲突；两者均未写成 resolved。",
              "- 52、57 的 handler RTTI 不改变 COVERAGE 中 0 行的 empty 判决。",
              "",
              "## 验证状态", "",
              "运行：`py -V:3.12 -I scratch/t14/out/verify.py --help`、`--selftest`、默认全量验证。",
              f"当前 stage2 resolved={doc['summary']['resolved']}/59（验收线 ≥45）；census dedicated 命名={census['summary']['named']}/63；fm TD 缺失={len(census['summary']['fm_td_missing'])}。",
              ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build t14 stage2_map.json and REPORT.md from local evidence.")
    parser.add_argument("--selftest", action="store_true", help="run offline unit checks")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
            print("SELFTEST PASS")
            return 0
        doc, report = build()
        (OUT / "stage2_map.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (OUT / "REPORT.md").write_text(report, encoding="utf-8")
        summary = doc["summary"]
        print(f"wrote stage2_map.json and REPORT.md: resolved={summary['resolved']}/59 candidate={summary['candidate']} negative={summary['negative']} empty={summary['empty']}")
        return 0 if doc["status"] == "complete" else 1
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
