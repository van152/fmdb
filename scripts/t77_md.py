"""t77 Markdown appendix: appended to the byte-pinned v10 Markdown, never rewriting it."""
from __future__ import annotations

from typing import Any


def _rows(pairs: list[tuple[str, Any]]) -> str:
    return "\n".join(f"| {k} | {v} |" for k, v in pairs)


def appendix(doc: dict[str, Any], sec: dict[str, Any]) -> str:
    cov = doc["coverage"]
    e111, e112, e113 = sec["e111"], sec["e112"], sec["e113"]
    e114g, e114x = sec["e114g"], sec["e114x"]
    e115, e117, scan = sec["e115"], sec["e117"], sec["scan"]
    den = doc["xml_denominator_coverage"]
    L: list[str] = []
    add = L.append

    add("")
    add("## t77 — schema v10 -> v11 (E111–E120)")
    add("")
    add("This is an additive appendix to the byte-pinned v10 Markdown. Every existing section, "
        "including held/unmapped records and all negative regressions, is unchanged; v11 only "
        "adds sections and updates `schema_version`, `generated_by`, `coverage` and "
        "`incremental_provenance`. L4=0 throughout.")
    add("")
    add("### Volume governance")
    add("")
    add("| Item | Value |")
    add("|---|---|")
    add(_rows([
        ("main schema", "three main tables + 8 numbered club subtables + CLUB_LINK + r2/r3 sections + v11 pointer sections"),
        ("`reports/other_tables_schema.json`", f"{doc['pointer_artifacts']['other_tables_schema']['table_count']} non-main tables, "
                                               f"{doc['pointer_artifacts']['other_tables_schema']['bytes']:,} B, "
                                               f"SHA-256 `{doc['pointer_artifacts']['other_tables_schema']['sha256'][:16]}…`"),
        ("`reports/xml_denominator_coverage.json`", f"1,034 occurrence records, {den['bytes']:,} B, "
                                                    f"SHA-256 `{den['sha256'][:16]}…`"),
    ]))
    add("")

    add("### club `table_extra_3` object (t71 / E111, L3)")
    add("")
    add(f"- `CLUB+0x100` chain closed: member `table_extra_3.dat`, object allocation "
        f"`{e111['object']['allocation_bytes']}`, dual-archive row frame "
        f"client {e111['row_frame']['envelopes']['client']['header']} + "
        f"{e111['row_frame']['envelopes']['client']['body']:,} + "
        f"{e111['row_frame']['envelopes']['client']['footer']} = "
        f"{e111['row_frame']['envelopes']['client']['payload']:,}; server "
        f"{e111['row_frame']['envelopes']['server']['header']} + "
        f"{e111['row_frame']['envelopes']['server']['body']:,} + "
        f"{e111['row_frame']['envelopes']['server']['footer']} = "
        f"{e111['row_frame']['envelopes']['server']['payload']:,}; "
        f"{e111['row_frame']['row_count']:,} rows both archives.")
    add(f"- Identity: {e111['row_frame']['identity']}. UID join: {e111['row_frame']['uid_join']}.")
    add(f"- {e111['promoted']['count']} held records promoted: "
        f"{len(e111['promoted']['cnst_projections'])} cnst projections at the extra object "
        f"(A block `+0xe0`, B block `+0xe7`) plus `Cebd` and `Cyfn`.")
    add(f"- club main-row L3 {cov['club_main_row_L3_prior_v10']} -> **{cov['club_main_row_L3']}** "
        f"(delta {cov['club_main_row_L3_delta_E111']}, per E111's slot accounting).")
    add(f"- Domain: {e111['domain']['cnst']}.")
    add(f"- Server-only wire: {e111['domain']['server_only']}; `Cyfn` {e111['domain']['Cyfn']}.")
    add(f"- Kept unnamed: {e111['domain']['unnamed_adjacent']}.")
    add("")

    add("### Unnamed slot fingerprints (t72 / E112, L2, partial)")
    add("")
    add("| Table | Slots | unnamed | held | l3_claimed |")
    add("|---|---:|---:|---:|---:|")
    for name in ("club", "comp", "nation"):
        t = e112["tables"][name]
        add(f"| {name} | {t['slot_count']} | {len(t['unnamed_keys'])} | "
            f"{t['kind_counts'].get('held', 0)} | {t['kind_counts'].get('l3_claimed', 0)} |")
    add("")
    add(f"- {e112['escalations']['count']} escalations, all nation inner-item grammars, "
        f"handed to t75: {', '.join(e112['escalations']['slots'])}.")
    add(f"- Grading ceiling: {e112['grading_ceiling']}. {e112['delivery_gap']}.")
    add("")

    add("### Simple tables (t73 / E113, L2)")
    add("")
    add(f"- {e113['frames_closed']}/{e113['frames_total']} (archive, table) frames closed: "
        f"city(2), continent(5), region(19), currency(41).")
    add(f"- L2 slots: {e113['L2_slots']['ledger_stated_count']} stated in the claim, "
        f"{e113['L2_slots']['distinct_table_field_offset']} distinct (table, field, offset) "
        f"triples in the artifacts, {e113['L2_slots']['archive_graded_records']} graded records "
        f"over 8 archives. {e113['L2_slots']['count_note']}")
    add(f"- Frozen anchors re-verified: {e113['frozen_anchors']['count']}, conflicts "
        f"{e113['frozen_anchors']['conflicts']}.")
    add(f"- Alias negative: {e113['alias_negative']['result']}. Resolution: "
        f"{e113['alias_negative']['resolution']}.")
    add(f"- Dual archive: city {e113['dual_archive_findings']['city']}; continent "
        f"{e113['dual_archive_findings']['continent']}; region "
        f"{e113['dual_archive_findings']['region']}.")
    add("- Tool boundaries: " + "; ".join(e113["tool_boundaries"]) + ".")
    add("")

    add("### Nation segment grammars (t75 / E114, L3)")
    add("")
    add(f"- {e114g['grammar_count']} inner-item grammars surveyed, "
        f"{e114g['closed_grammars']} closed byte-level, held (0 real items): "
        f"{', '.join(e114g['held_no_items'])}.")
    add(f"- Dual archive: {e114g['dual_archive_identity']}.")
    add(f"- Prior named sub-slots re-verified: {e114g['prior_lanes_reverified']['count']}.")
    add(f"- Boundary: {e114g['boundary']}.")
    add("")

    add("### Slot adjudication (t75 / E114, L3)")
    add("")
    add("| Entity | Adjudicated | held |")
    add("|---|---:|---:|")
    for name, v in e114x["by_table"].items():
        add(f"| {name} | {v['adjudicated']} | {v['held']} |")
    add("")
    add(f"- Totals: {e114x['totals']['adjudicated']} slots adjudicated, "
        f"{e114x['totals']['held']} held, **new named L3 = {e114x['totals']['new_named_L3']}**.")
    for k, v in e114x["club_comp_findings"].items():
        add(f"- `{k}`: {v}")
    add("")

    add("### Nine-table row frames (t74 / E115, L2)")
    add("")
    add("| Table | Entity | Archive | Model | Header | Footer | Count | Identity | Closure |")
    add("|---|---|---|---|---:|---:|---:|---|---|")
    for r in e115["frames"]:
        if r["status"] == "absent":
            add(f"| {r['table']} | {r['entity']} | {r['archive']} | absent | – | – | – | – | entry absent |")
            continue
        ident = f"{r['identity_width']}B @ {r['identity_anchor']}"
        add(f"| {r['table']} | {r['entity']} | {r['archive']} | {r['model']} | {r['header']} | "
            f"{r['footer']} | {r['count']:,} | {ident} | `{r['closure']}` |")
    add("")
    add(f"- {e115['archives_closed']}/{e115['archives_verified']} (archive, table) closures, "
        f"zero escalations.")
    add(f"- Identity doctrine: {e115['identity_doctrine']['sensitivity_result']}")
    add("")

    add("### Stadium / team / extra_24 (t79 / E117, L3)")
    add("")
    add(f"- stadium.xml: {e117['counts']['stadium_L3']} L3 of "
        f"{e117['summary']['stadium_xml_total']} occurrences; team.xml "
        f"{e117['counts']['team_L3']} of {e117['summary']['team_xml_total']}; "
        f"table_extra_24 {e117['counts']['extra_24_mapped']} mapped fields; "
        f"club `+0x18` forwarding upgraded {e117['counts']['club_forwarded_L3']} fields held->L3.")
    add(f"- Grades (stadium): {e117['summary']['stadium_xml_grades']}")
    add(f"- Grades (team): {e117['summary']['team_xml_grades']}")
    add("")

    add("### Scan tables: stadium + derby/weather/lcrg/agreement (t76a E120, t76c E118, L2)")
    add("")
    add(f"- stadium(21): {scan['stadium']['slot_counts']['client']} client / "
        f"{scan['stadium']['slot_counts']['server']} server slots, 0 uncovered bytes both "
        f"archives, verify {scan['stadium']['verify_checks']} checks / "
        f"{scan['stadium']['verify_failed']} failed.")
    for line in scan["stadium"]["structural"]:
        add(f"  - {line}")
    add("")
    add("| Table | Entity | client slots | server slots |")
    add("|---|---|---:|---:|")
    for tid, t in scan["t76c"].items():
        add(f"| {tid} | {t['entity']} | {t['archives']['client'].get('slot_count')} | "
            f"{t['archives']['server'].get('slot_count')} |")
    add("")
    for line in scan["structural_findings"]:
        add(f"- {line}")
    add(f"- **t76b (award/language/media) is dropped**: {scan['pending']['t76b']}.")
    add("")

    add("### XML denominator (t78 / E116, L1) — split file")
    add("")
    add("| Entity | mapped_l3 | independent_member | string_name_table | ui_or_derived | held | unresolved_wire_slot | no_wire_evidence | Sum |")
    add("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for e in ("club", "nation", "comp"):
        v = den["summary"][e]
        add(f"| {e} | {v['mapped_l3']} | {v['independent_member']} | {v['string_name_table']} | "
            f"{v['ui_or_derived']} | {v['held']} | {v['unresolved_wire_slot']} | "
            f"{v['no_wire_evidence']} | **{v['sum']}** |")
    add("")
    add(f"- Physical coverage: **{den['physical_coverage']['text']}** "
        f"({den['physical_coverage']['carried']}/{den['physical_coverage']['denominator']}).")
    add(f"- Full ledger: `{den['path']}` (SHA-256 `{den['sha256']}`).")
    add("")

    add("### Provenance and boundaries")
    add("")
    add("- Ledger guards cover E111–E120 by entry id, kind, level and canonical claim SHA-256; "
        "the v10 t70 snapshot is preserved verbatim inside `incremental_provenance`.")
    add("- E119 (t80 enum-supplement premise void) is recorded as a `probe_negative` entry, "
        "not as an acceptance; E116 is L1 (frozen-artifact accounting only).")
    add("- E121 (t82, table_extra_3 dual-object closure) landed after this lane departed and is "
        "**not** folded here; it belongs to t87.")
    add("- v10 sections are byte-preserved: three main tables, 8 numbered club subtables, "
        "CLUB_LINK, all r2 sections and every negative regression.")
    add("- No game/editor/IDA was started; no `.dat` payload was decoded for this fold. L4=0.")
    add("")
    return "\n".join(L)
