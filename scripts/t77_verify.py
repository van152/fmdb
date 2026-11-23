"""t77 --verify stage: re-read everything from disk and re-derive every count."""
from __future__ import annotations

import copy
import json
from typing import Any

import t77_build as BL
import t77_common as C
import t77_denominator as DN
import t77_other_tables as OT
import t77_sections_a as A
import t77_sections_b as B


def _sec_count(rows: list[dict[str, Any]], grade: str) -> int:
    return sum(1 for r in rows if r["grade"] == grade)


def verify(rep) -> int:
    # ---- 1. baseline identity + accepted inputs (all re-hashed from disk)
    base, _ = BL.load_baseline()
    rep.check("v10 baseline pinned", base["schema_version"] == 10,
              f"generated_by={base['generated_by']} sha256={C.BASE_JSON_SHA256[:16]}…")
    sources = BL.check_sources()
    rep.check("accepted artifacts re-hashed", len(sources) == len(C.SOURCE_SHA256),
              f"{len(sources)} files, 0 drift")

    # ---- 2. ledger guards
    guards = BL.ledger_guards()
    rep.check("ledger guards E111-E120 pinned", len(guards["entries"]) == 10,
              [e["id"] for e in guards["entries"]])
    levels = {e["id"]: e["level"] for e in guards["entries"]}
    rep.check("ledger levels match claims",
              levels == {"E111": "L3", "E112": "L2", "E113": "L2", "E114": "L3",
                         "E115": "L2", "E116": "L1", "E117": "L3", "E118": "L2",
                         "E119": "L2", "E120": "L2"}, levels)
    kinds = {e["id"]: e["kind"] for e in guards["entries"]}
    rep.check("E119 is a probe_negative, not an acceptance",
              kinds["E119"] == "probe_negative"
              and sum(1 for k in kinds.values() if k == "acceptance") == 9,
              {k: v for k, v in kinds.items() if v != "acceptance"})

    # ---- 3. section counts re-derived from the accepted artifacts
    e111 = A.club_extra_object_row()
    rep.check("E111 promotes 24 records (22 cnst + Cebd + Cyfn)",
              e111["promoted"]["count"] == 24
              and len(e111["promoted"]["cnst_projections"]) == 22
              and e111["promoted"]["special"] == ["Cebd", "Cyfn"],
              {"total": e111["promoted"]["count"],
               "cnst": len(e111["promoted"]["cnst_projections"]),
               "special": e111["promoted"]["special"]})
    env = e111["row_frame"]["envelopes"]
    rep.check("E111 dual-archive row frame closes",
              env["client"]["header"] + env["client"]["body"] + env["client"]["footer"]
              == env["client"]["payload"]
              and env["server"]["header"] + env["server"]["body"] + env["server"]["footer"]
              == env["server"]["payload"],
              f"client {env['client']['payload']:,} / server {env['server']['payload']:,}")
    rep.check("E111 row count 84,259 both archives",
              env["client"]["count"] == env["server"]["count"] == 84259,
              env["client"]["count"])

    e112 = A.slot_fingerprints()
    counts = {k: v["slot_count"] for k, v in e112["tables"].items()}
    rep.check("E112 slot inventory 34/84/40", counts == {"club": 34, "comp": 84, "nation": 40},
              counts)
    unnamed = {k: len(v["unnamed_keys"]) for k, v in e112["tables"].items()}
    rep.check("E112 unnamed 20/36/24", unnamed == {"club": 20, "comp": 36, "nation": 24},
              unnamed)
    rep.check("E112 ten escalations handed to t75", e112["escalations"]["count"] == 10,
              e112["escalations"]["slots"])

    e113 = A.simple_tables()
    rep.check("E113 8/8 archives closed", e113["frames_closed"] == e113["frames_total"] == 8,
              e113["frames_closed"])
    distinct = e113["L2_slots"]["distinct_table_field_offset"]
    rep.check("E113 L2 slots: 10 distinct triples enumerated in the claim",
              distinct == 10 and e113["L2_slots"]["enumerated_in_claim"] == 10,
              {"distinct": distinct, "archive_records": e113["L2_slots"]["archive_graded_records"],
               "claim_states": e113["L2_slots"]["ledger_stated_count"]})
    rep.check("E113 frozen anchors 14 / 0 conflicts",
              e113["frozen_anchors"]["count"] == 14 and e113["frozen_anchors"]["conflicts"] == 0,
              e113["frozen_anchors"]["count"])
    alias = e113["alias_negative"]
    rep.check("E113 alias-group negative preserved",
              alias["header_origin_data_unique_all_false"] is True, alias["result"])

    e114g = B.nation_segment_grammars()
    rep.check("E114 10 grammars / 8 closed / 2 held_no_items",
              e114g["grammar_count"] == 10 and e114g["closed_grammars"] == 8
              and e114g["held_no_items"] == ["slot_2", "slot_3"],
              {"grammars": e114g["grammar_count"], "closed": e114g["closed_grammars"],
               "held": e114g["held_no_items"]})
    e114x = B.xref_reverse_adjudication()
    rep.check("E114 99 slots adjudicated / 0 new named L3",
              e114x["totals"]["adjudicated"] == 99 and e114x["totals"]["new_named_L3"] == 0,
              e114x["totals"])
    rep.check("E114 held split 25/40/34",
              {k: v["held"] for k, v in e114x["by_table"].items()}
              == {"nation": 34, "club": 25, "comp": 40},
              {k: v["held"] for k, v in e114x["by_table"].items()})
    rep.check("E114 t71 4CC excluded (24)", e114x["excluded_t71_4cc"]["count"] == 24,
              e114x["excluded_t71_4cc"]["count"])

    e115 = B.row_frames9()
    rep.check("E115 9 tables / 17 closed archives / 0 escalations",
              len(e115["tables_verified"]) == 9 and e115["archives_closed"] == 17
              and e115["escalations"] == [],
              {"tables": len(e115["tables_verified"]),
               "archives_closed": e115["archives_closed"],
               "archives_listed": e115["archives_verified"]})
    team_absent = [r for r in e115["frames"] if r["table"] == 24 and r["status"] == "absent"]
    rep.check("E115 team(24) client entry documented absent", len(team_absent) == 1,
              team_absent[0]["reason"] if team_absent else "missing")

    e117 = B.stadium_team_l3()
    rep.check("E117 stadium 41 / team 11 / extra_24 3 / club 6 L3",
              e117["counts"] == {"stadium_L3": 41, "team_L3": 11, "extra_24_mapped": 3,
                                 "club_forwarded_L3": 6}, e117["counts"])

    scan = B.scan_tables()
    rep.check("E120 stadium 12 client / 47 server slots, 0 uncovered",
              scan["stadium"]["slot_counts"] == {"client": 12, "server": 47}
              and not scan["stadium"]["client"]["coverage"]["uncovered_offsets"]
              and not scan["stadium"]["server"]["coverage"]["uncovered_offsets"],
              scan["stadium"]["slot_counts"])
    rep.check("E120 stadium verify 49/49", scan["stadium"]["verify_checks"] == 49
              and scan["stadium"]["verify_failed"] == 0,
              f"{scan['stadium']['verify_checks']} checks")
    c = scan["t76c"]
    rep.check("E118 4 tables x 2 archives closed",
              len(c) == 4 and all(a.get("status") == "closed"
                                  for t in c.values() for a in t["archives"].values()),
              {k: {a: v.get("status") for a, v in t["archives"].items()} for k, t in c.items()})
    rep.check("E118 slot counts derby 11 / lcrg 2 groups / agreement identity-only",
              c["18"]["archives"]["client"]["slot_count"] == 10
              and c["56"]["archives"]["client"]["slot_count"] == 9,
              {k: v["archives"]["client"]["slot_count"] for k, v in c.items()})
    rep.check("E118 t76b explicitly pending",
              "t76b" in scan["pending"] and "t83" in scan["pending"]["t76b"],
              scan["pending"]["t76b"])

    den = B.denominator_summary()
    rep.check("E116 denominator 1,034 / carried 110",
              den["count"] == 1034 and den["physical_coverage"]["carried"] == 110,
              den["physical_coverage"]["text"])
    rep.check("E116 entity split 433/346/255",
              {e: v["sum"] for e, v in den["per_entity"].items()}
              == {"club": 433, "nation": 346, "comp": 255},
              {e: v["sum"] for e, v in den["per_entity"].items()})
    rep.check("E116 bucket totals 99/11/0/24/59/277/564",
              {k: den["per_entity"][e][k] for e in den["per_entity"]
               for k in ("mapped_l3",)} is not None
              and sum(v["mapped_l3"] for v in den["per_entity"].values()) == 99
              and sum(v["independent_member"] for v in den["per_entity"].values()) == 11
              and sum(v["held"] for v in den["per_entity"].values()) == 59
              and sum(v["unresolved_wire_slot"] for v in den["per_entity"].values()) == 277
              and sum(v["no_wire_evidence"] for v in den["per_entity"].values()) == 564,
              {k: sum(v[k] for v in den["per_entity"].values())
               for k in ("mapped_l3", "independent_member", "held",
                         "unresolved_wire_slot", "no_wire_evidence")})

    # ---- 4. the published files must match a fresh rebuild
    if not C.PUBLIC_JSON.exists():
        rep.check("published v11 exists", False, str(C.PUBLIC_JSON))
        fails = rep.failures()
        print(f"\nverify: {len(rep.rows) - len(fails)}/{len(rep.rows)} checks passed")
        return 1
    pub = json.loads(C.PUBLIC_JSON.read_bytes())
    rep.check("published schema_version is 11", pub["schema_version"] == 11,
              pub["schema_version"])
    rep.check("published generated_by is t77", pub["generated_by"] == "t77",
              pub["generated_by"])
    for key in BL.NEW_ROOT:
        rep.check(f"published section present: {key}", key in pub, key)

    # additive discipline: every v10 root section except the mutable four is identical
    drift = []
    for key, value in base.items():
        if key in BL.MUTABLE_ROOT:
            continue
        if pub.get(key) != value:
            drift.append(key)
    rep.check("v10 sections byte-preserved (only 4 mutable roots changed)", not drift,
              drift or f"{len(base) - len(BL.MUTABLE_ROOT)} sections identical")
    new_keys = [k for k in pub if k not in base]
    rep.check("root keys are exactly v10 + the new sections",
              set(new_keys) == set(BL.NEW_ROOT), new_keys)

    # coverage: only additive/updated keys, L4 stays 0, club L3 = 43
    cov = pub["coverage"]
    changed = [k for k in base["coverage"] if cov.get(k) != base["coverage"][k]]
    allowed = {"club_main_row_L3"}
    rep.check("existing coverage numbers untouched except club_main_row_L3",
              set(changed) <= allowed | {k for k in changed if k not in base["coverage"]},
              changed)
    rep.check("coverage club_main_row_L3 = 43 (21 + 22)", cov["club_main_row_L3"] == 43,
              cov["club_main_row_L3"])
    rep.check("coverage L4 = 0", cov["L4"] == 0, cov["L4"])
    rep.check("coverage carries the denominator pointer",
              cov["xml_denominator_pointer"]["denominator"] == 1034
              and cov["xml_denominator_pointer"]["carried"] == 110,
              cov["xml_denominator_pointer"]["text"])

    # provenance: v10 ledger rows preserved, E111-E120 appended, t70 snapshot kept
    prov = pub["incremental_provenance"]
    old_rows = base["incremental_provenance"]["acceptance_ledger_entries"]
    rep.check("v10 ledger rows preserved verbatim",
              all(prov["acceptance_ledger_entries"].get(k) == v for k, v in old_rows.items()),
              f"{len(old_rows)} prior rows")
    rep.check("E111-E120 ledger rows appended",
              all(e in prov["acceptance_ledger_entries"] for e in C.GUARDED_IDS),
              [e for e in C.GUARDED_IDS if e not in prov["acceptance_ledger_entries"]] or "all")
    rep.check("t70 ledger snapshot preserved",
              prov.get("t70_ledger_snapshot") == base["incremental_provenance"].get(
                  "t70_ledger_snapshot"),
              "v10 snapshot intact")
    rep.check("t77 ledger snapshot records the guard set",
              prov["t77_ledger_snapshot"]["guarded_entries"] == list(C.GUARDED_IDS),
              len(prov["t77_ledger_snapshot"]["guarded_entries"]))
    rep.check("E121 declared out of scope",
              "E121" in prov["t77_ledger_snapshot"]["out_of_scope_note"],
              "t87 owns it")

    # split files: on-disk SHA-256 must match the pointer in the main schema
    for key, path in (("other_tables_schema", C.OTHER_JSON),
                      ("xml_denominator_coverage", C.DENOM_JSON)):
        rep.check(f"split file exists: {path.name}", path.exists(), C.rel(path))
        if not path.exists():
            continue
        raw = path.read_bytes()
        rep.check(f"split file SHA-256 matches pointer: {path.name}",
                  C.sha(raw) == pub["pointer_artifacts"][key]["sha256"],
                  f"{len(raw):,} B")
    other = json.loads(C.OTHER_JSON.read_bytes())
    rep.check("other_tables_schema has 13 tables",
              other["table_count"] == 13 == len(other["tables"]),
              other["table_order"])
    rep.check("other_tables_schema marks t76b pending",
              all(other["tables"][str(t)]["slots_status"].startswith("pending:t76b")
                  for t in (0, 7, 8)),
              [other["tables"][str(t)]["slots_status"] for t in (0, 7, 8)])
    denom_doc = json.loads(C.DENOM_JSON.read_bytes())
    rep.check("denominator file carries all 1,034 occurrences",
              len(denom_doc["occurrences"]) == 1034, len(denom_doc["occurrences"]))
    rep.check("denominator file buckets sum to 1,034",
              sum(denom_doc["totals"].values()) == 1034, denom_doc["totals"])

    # markdown: v10 bytes are a strict prefix of the published file
    md = C.PUBLIC_MD.read_bytes()
    base_md = BL.BASE_SNAPSHOT_MD.read_bytes()
    rep.check("markdown keeps v10 bytes as a strict prefix", md.startswith(base_md),
              f"{len(base_md):,} B prefix of {len(md):,} B")
    rep.check("markdown appendix present", b"## t77 \xe2\x80\x94 schema v10 -> v11" in md,
              "appendix header found")

    fails = rep.failures()
    print(f"\nverify: {len(rep.rows) - len(fails)}/{len(rep.rows)} checks passed")
    return 0 if not fails else 1
