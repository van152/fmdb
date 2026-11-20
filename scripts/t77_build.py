"""t77 build: v10 -> v11 additive merge. Existing sections are copied by object
identity (no re-serialisation drift) and asserted equal at --verify time.

Shape of v11:
  v10 keys                        -> unchanged, verbatim
  schema_version                  -> 11
  generated_by                    -> t77
  coverage                        -> numbers updated (club L3 43, pointers, counts)
  incremental_provenance          -> E111-E120 appended, t70 snapshot preserved
  + club_extra_object_row  (E111 / t71)
  + slot_fingerprints      (E112 / t72)
  + simple_tables          (E113 / t73)
  + nation_segment_grammars, xref_reverse_adjudication (E114 / t75)
  + row_frames9            (E115 / t74)
  + xml_denominator_coverage (E116 / t78) -> pointer to reports/xml_denominator_coverage.json
  + stadium_team_l3        (E117 / t79)
  + scan_tables            (E118 t76c + E120 t76a; t76b pending)
  + pointer_artifacts      -> other_tables_schema.json path + SHA-256
"""
from __future__ import annotations

import copy
import json
from typing import Any

import t77_common as C
import t77_denominator as DN
import t77_other_tables as OT
import t77_sections_a as A
import t77_sections_b as B

BASE_SNAPSHOT = C.ROOT / "scratch" / "t70" / "out" / "club_nation_subtable_schema.v10.json"
BASE_SNAPSHOT_MD = C.ROOT / "scratch" / "t70" / "out" / "club_nation_subtable_schema.v10.md"

# Entry id -> (canonical claim sha256, kind, level); pinned so a rewritten claim
# cannot slip into the fold unnoticed.
PINNED_LEDGER = {
    "E111": ("d09b73bb6f6ccef14819eeba5a3379d0feab512deb83813439ced0410224810d", "acceptance", "L3"),
    "E112": ("4495b1874a9db05a03996d0e790125803c77b72844cbd45897453a3da72cc376", "acceptance", "L2"),
    "E113": ("c4e762f19d90ca70395a494038ffed1ddea29c05f7358fe132e7c8ff66a699fa", "acceptance", "L2"),
    "E114": ("45b004e792371c5858a622f481329f79cfc716186e03445b09b2deca0e8c7bc6", "acceptance", "L3"),
    "E115": ("b66ef5dbad3fe120394ddb7d80cc1937d01156cd4f83dd55ecf72189fe24d802", "acceptance", "L2"),
    "E116": ("e4a6045bf87df98d561014078dac066160a8afd6f654378a6348ea232b159b09", "acceptance", "L1"),
    "E117": ("4ebfb8b49091a59d2a76a5e82b45f36d966716b9352d08f190a5c7c3e6eec4a5", "acceptance", "L3"),
    "E118": ("c046421bb1b4587c341d183becd71e33074b35a478afb0ebdc90f3604fbd27c7", "acceptance", "L2"),
    "E119": ("0147b18e15cb25fff7ada97dc04ec94f64c139ba033bcd9acedf0fe435d188fa", "probe_negative", "L2"),
    "E120": ("266eecf0d2b641b226b5b0f76567f6db6ebfb804dfd91c302674bbaef1007d13", "acceptance", "L2"),
}

TASK_SPEC = {
    "t71": ("E111", "L3", "club_extra_object_row"),
    "t72": ("E112", "L2", "slot_fingerprints"),
    "t73": ("E113", "L2", "simple_tables"),
    "t74": ("E115", "L2", "row_frames9"),
    "t75": ("E114", "L3", "nation_segment_grammars + xref_reverse_adjudication"),
    "t76a": ("E120", "L2", "scan_tables/stadium"),
    "t76c": ("E118", "L2", "scan_tables/t76c"),
    "t78": ("E116", "L1", "xml_denominator_coverage (pointer)"),
    "t79": ("E117", "L3", "stadium_team_l3"),
}

# Sections whose values are allowed to change; every other v10 root key is
# asserted byte-identical after the fold.
MUTABLE_ROOT = {"schema_version", "generated_by", "coverage", "incremental_provenance"}
NEW_ROOT = ("club_extra_object_row", "slot_fingerprints", "simple_tables",
            "nation_segment_grammars", "xref_reverse_adjudication", "row_frames9",
            "xml_denominator_coverage", "stadium_team_l3", "scan_tables",
            "pointer_artifacts")


def load_baseline() -> tuple[dict[str, Any], bytes]:
    raw = BASE_SNAPSHOT.read_bytes()
    C.require(C.sha(raw) == C.BASE_JSON_SHA256, "pinned v10 baseline JSON SHA-256")
    C.require(C.sha(BASE_SNAPSHOT_MD.read_bytes()) == C.BASE_MD_SHA256,
              "pinned v10 baseline Markdown SHA-256")
    base = json.loads(raw)
    C.require(base["schema_version"] == 10 and base["generated_by"] == "t70",
              "v10 baseline identity")
    return base, raw


def check_sources() -> list[dict[str, Any]]:
    rows = []
    for rel, (want_sha, want_bytes) in C.SOURCE_SHA256.items():
        p = C.ROOT / rel
        C.require(p.exists(), f"missing accepted artifact: {rel}")
        raw = p.read_bytes()
        C.require(C.sha(raw) == want_sha, f"accepted artifact SHA-256 mismatch: {rel}")
        C.require(len(raw) == want_bytes, f"accepted artifact byte count changed: {rel}")
        rows.append({"path": rel, "sha256": want_sha, "bytes": want_bytes})
    return rows


def ledger_guards() -> dict[str, Any]:
    found = C.ledger_entries()
    C.require(set(found) == set(C.GUARDED_IDS), "ledger guard set E111-E120 incomplete")
    rows, records = [], {}
    for eid in C.GUARDED_IDS:
        item = found[eid]
        want_sha, want_kind, want_level = PINNED_LEDGER[eid]
        got_sha = C.canonical_sha256(item["claim"])
        C.require(got_sha == want_sha, f"acceptance claim changed: {eid}")
        C.require(item["kind"] == want_kind, f"ledger kind changed: {eid}")
        C.require(item["level"] == want_level, f"ledger level changed: {eid}")
        rows.append({"id": eid, "kind": want_kind, "level": want_level,
                     "claim_sha256": want_sha, "date": item.get("date")})
        records[eid] = {"kind": want_kind, "level": want_level, "claim_sha256": want_sha,
                        "date": item.get("date")}
    return {"entries": rows, "records": records, "found": found}


def coverage_update(base: dict[str, Any], other: dict[str, Any],
                    denom: dict[str, Any], sec: dict[str, Any]) -> dict[str, Any]:
    cov = copy.deepcopy(base["coverage"])
    prior_l3 = cov["club_main_row_L3"]
    C.require(prior_l3 == 21, "v10 club_main_row_L3 baseline is 21")
    promoted = sec["e111"]["promoted"]["count"]
    delta = 22
    C.require(promoted == 24 and len(sec["e111"]["promoted"]["cnst_projections"]) == 22,
              "E111 promotion inventory is 24 records / 22 cnst")
    cov["club_main_row_L3"] = prior_l3 + delta
    cov["club_main_row_L3_prior_v10"] = prior_l3
    cov["club_main_row_L3_delta_E111"] = delta
    cov["club_main_row_L3_note"] = (
        "21 (v10) + 22 = 43 per E111. E111 promotes 24 held records in total "
        "(22 cnst projections at the table_extra_3 object + Cebd + Cyfn); the ledger states "
        "the main-row slot delta as 22. The full 24-record list is in "
        "#/club_extra_object_row/promoted/fields with each record's own object_path/lane.")
    cov["club_extra_object_promoted_records_E111"] = promoted
    cov["nation_side_L3_after_E114"] = cov.get("nation_L3_occurrences")
    cov["nation_side_L3_note_E114"] = (
        "E114 (t75) promoted zero new named L3; nation L3 occurrence count is unchanged.")
    cov["slot_fingerprint_unnamed_slots_E112"] = {
        "club": sec["e112"]["tables"]["club"]["slot_count"],
        "comp": sec["e112"]["tables"]["comp"]["slot_count"],
        "nation": sec["e112"]["tables"]["nation"]["slot_count"],
        "unnamed": {k: len(v["unnamed_keys"]) for k, v in sec["e112"]["tables"].items()},
        "escalations": sec["e112"]["escalations"]["count"],
    }
    cov["simple_tables_E113"] = {
        "frames_closed": sec["e113"]["frames_closed"],
        "frames_total": sec["e113"]["frames_total"],
        "L2_graded_records": sec["e113"]["slot_grades"]["L2"],
        "L2_distinct_slots": sec["e113"]["L2_slots"]["distinct_table_field_offset"],
        "frozen_anchors_reverified": sec["e113"]["frozen_anchors"]["count"],
        "frozen_anchor_conflicts": sec["e113"]["frozen_anchors"]["conflicts"],
    }
    cov["nation_segment_grammars_E114"] = {
        "closed": sec["e114g"]["closed_grammars"],
        "held_no_items": len(sec["e114g"]["held_no_items"]),
        "slots_adjudicated": sec["e114x"]["totals"]["adjudicated"],
        "new_named_L3": sec["e114x"]["totals"]["new_named_L3"],
    }
    cov["row_frames9_E115"] = {
        "tables": len(sec["e115"]["tables_verified"]),
        "archives_closed": sec["e115"]["archives_closed"],
        "escalations": len(sec["e115"]["escalations"]),
    }
    cov["scan_tables_E118_E120"] = {
        "stadium_client_slots": sec["scan"]["stadium"]["slot_counts"]["client"],
        "stadium_server_slots": sec["scan"]["stadium"]["slot_counts"]["server"],
        "t76c_archives_closed": sum(
            1 for t in sec["scan"]["t76c"].values()
            for a in t["archives"].values() if a.get("status") == "closed"),
        "t76b": "dropped (award/language/media -> t83); not in this version",
    }
    cov["stadium_team_L3_E117"] = sec["e117"]["counts"]
    cov["xml_denominator_pointer"] = {
        "path": denom["path"],
        "sha256": denom["sha256"],
        "bytes": denom["bytes"],
        "denominator": denom["count"],
        "carried": denom["carried"],
        "text": "110/1034 = 10.6% physical coverage",
        "note": "full bucket ledger lives in the split file; the main schema keeps this pointer",
    }
    cov["other_tables_pointer"] = {
        "path": other["path"],
        "sha256": other["sha256"],
        "bytes": other["bytes"],
        "table_count": other["table_count"],
        "note": "13 non-main-table slot verdicts (t73 4 + t76a 1 + t76c 4 + t74 frames 4)",
    }
    cov["L4"] = 0
    return cov
