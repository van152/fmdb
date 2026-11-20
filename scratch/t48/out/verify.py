#!/usr/bin/env python3
"""Independent verifier for the t48 schema v4 consolidation; does not import its builder."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
SCHEMA_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
SCHEMA_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V3_JSON = OUT_DIR / "club_nation_subtable_schema.v3.json"
V3_MD = OUT_DIR / "club_nation_subtable_schema.v3.md"
V3_JSON_SHA256 = "81efb123da581540d1ccd8644523648244fcbe401ad1b0f661a1214222c03921"
V3_MD_SHA256 = "71ba6c79d6df317c266cd6013c5aa0f81ae729b19ccd337fea5922be712c1662"
MASTER_SHA256 = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
EDITOR_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
MANIFEST_SHA256 = "28593fcb59f0c0d23d40cb7091b2c0f5ebb5725c7571fda44fe1eeef581d3fc0"
T44_FIELDS = "scratch/t44/out/fields_cafl_cvfl.json"
T44_CURSOR = "scratch/t44/out/cursor_club_links.json"
T44_DISCOVERY = "scratch/t44/out/discovery_cafl_cvfl.json"
T44_REPORT = "scratch/t44/out/REPORT.md"
T46_GRAMMAR = "scratch/t46/out/grammar_diff_client_server.json"
T46_PROFILE = "scratch/t46/out/profiles/table_server_10.profile.json"
T46_REPORT = "scratch/t46/out/REPORT.md"
T37_INVENTORY = "scratch/t37/out/nation_subtable_inventory.json"
LEDGER = "scratch/t01/LEDGER.json"
SOURCE_PATHS = [
    T44_FIELDS, T44_CURSOR, T44_DISCOVERY, T44_REPORT,
    T46_GRAMMAR, T46_PROFILE, T46_REPORT, T37_INVENTORY,
]
FLAG_CODES = {
    "frly", "golo", "fotb", "plfr", "yutr", "perm", "smbo", "fnhl", "hlwf",
    "mrrl", "scks", "cpsd", "ualf", "lpfs", "ustf", "yout", "rsrv", "pfpr",
    "UsSK", "bttr",
}


class VerifyFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyFailure(message)


def path_for(path: str) -> Path:
    return ROOT / Path(path)


def load_json(path: Path | str) -> Any:
    target = path if isinstance(path, Path) else path_for(path)
    return json.loads(target.read_text(encoding="utf-8"))


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return digest(raw)


def artifact_record(path: str) -> dict[str, Any]:
    target = path_for(path)
    require(target.is_file(), f"source artifact missing: {path}")
    raw = target.read_bytes()
    return {"path": path, "sha256": digest(raw), "bytes": len(raw)}


def expected_wire_map(fields: dict[str, Any]) -> dict[tuple[int, int], set[str]]:
    result: dict[tuple[int, int], set[str]] = {}
    for view in ("Cafl", "Cvfl"):
        for record in fields["occurrences"][view]:
            if record["grade"] != "L3":
                continue
            if record["code"] in {"affl", "ismc"}:
                lanes = record["endpoint_slots"].values()
                coords = [(lane["row_offset"], lane["width"]) for lane in lanes]
            else:
                coords = [(record["row_offset"], record["width"])]
            for offset, width in coords:
                result.setdefault((offset, width), set()).add(record["code"])
    return result


def verify_occurrences(source: dict[str, Any], field_source: dict[str, Any]) -> tuple[int, int, int]:
    total_l3 = 0
    total_held = 0
    total_runtime = 0
    seen_flags: set[str] = set()
    for view_name in ("Cafl", "Cvfl"):
        view = next((item for item in source["views"] if item.get("view") == view_name), None)
        require(view is not None, f"missing {view_name} view")
        records = field_source["occurrences"][view_name]
        output_records = view["occurrences"]
        require(len(records) == len(output_records), f"{view_name} occurrence count changed")
        require(view.get("occurrence_grade_counts") == field_source["occurrence_grades"][view_name],
                f"{view_name} grade summary changed")
        for record, item in zip(records, output_records):
            require(item.get("view") == view_name and item.get("schema_idx") == record["schema_idx"],
                    f"{view_name}.{record['code']} schema occurrence mismatch")
            require(item.get("code") == record["code"] and item.get("schema") == record["schema"],
                    f"{view_name}.{record['code']} schema metadata changed")
            require(item.get("grade") == record["grade"] and item.get("encoding") == record["encoding"],
                    f"{view_name}.{record['code']} grade/encoding changed")
            require(item.get("source_task") == "t44" and item.get("source_record") == record,
                    f"{view_name}.{record['code']} source record changed")
            require(item.get("source_record_sha256") == canonical_digest(record),
                    f"{view_name}.{record['code']} source record digest mismatch")
            if record["grade"] == "L3":
                total_l3 += 1
                require(item.get("status") == "accepted_L3", f"{view_name}.{record['code']} L3 status mismatch")
                if record["code"] in {"affl", "ismc"}:
                    require("row_offset" not in item and "wire_offset" not in item,
                            f"{view_name}.{record['code']} must not claim a single row offset")
                    require(item.get("wire_coordinates") == [], f"{view_name}.{record['code']} derived field has a single wire coordinate")
                    lanes = item.get("endpoint_lanes", [])
                    require([(lane.get("endpoint"), lane.get("wire_offset"), lane.get("width_bytes")) for lane in lanes] == [
                        ("A", 0, 4), ("B", 9, 4)
                    ], f"{view_name}.{record['code']} endpoint coordinates changed")
                    note = item.get("coordinate_note", "")
                    if record["code"] == "affl":
                        require("current club == A select B, otherwise select A" in note,
                                "affl viewer-relative formula missing")
                    else:
                        require("true exactly when current club == A" in note and "not a stored bit" in note,
                                "ismc viewer-relative formula missing")
                elif record["encoding"] == "bit":
                    seen_flags.add(record["code"])
                    coord = item.get("wire_coordinates", [None])[0]
                    require(coord is not None and (coord.get("wire_offset"), coord.get("width_bytes")) == (5, 4),
                            f"{view_name}.{record['code']} shared u32 coordinate mismatch")
                    require(coord.get("storage") == "shared_u32_bitmask" and coord.get("bit_index") == record["bit_index"] and
                            coord.get("bit_mask_u32") == record["bit_mask_u32"],
                            f"{view_name}.{record['code']} bit index/mask changed")
                    require("not an independent byte slot" in item.get("coordinate_note", ""),
                            f"{view_name}.{record['code']} shared-word caveat missing")
                elif record["code"] == "pwgp":
                    require(item.get("raw_zero_count") == 8776, "pwgp raw-zero profile changed")
                else:
                    coord = item.get("wire_coordinates", [None])[0]
                    require(coord is not None and (coord.get("wire_offset"), coord.get("width_bytes")) ==
                            (record["row_offset"], record["width"]), f"{view_name}.{record['code']} wire coordinate mismatch")
            elif record["grade"] == "runtime_only_no_wire_slot":
                total_runtime += 1
                require(record["code"] == "clfr" and item.get("status") == "runtime_only_no_wire_slot",
                        "unexpected runtime-only occurrence")
                require(item.get("wire_coordinates") == [] and item.get("runtime_coordinate", {}).get("offset") == 8,
                        "clfr must remain wrapper-only with no wire coordinate")
                require(item.get("validator_written_values") == [1, 2, 3, 4, 5, 6] and
                        item.get("copy_append_requires_validation_success") is False,
                        "clfr runtime validation/copy behavior changed")
            else:
                total_held += 1
                require(item.get("status") == "held" and item.get("wire_coordinates") == [],
                        f"{view_name}.{record['code']} held field was promoted")
                require(item.get("candidate_coordinate", {}).get("wire_offset") == record["candidate_row_offset"],
                        f"{view_name}.{record['code']} held candidate coordinate changed")
                require(item.get("first_counterexample") == record.get("first_counterexample"),
                        f"{view_name}.{record['code']} first counterexample changed")
    require(seen_flags == FLAG_CODES, "shared CLUB_LINK bool code set changed")
    require((total_l3, total_held, total_runtime) == (42, 5, 1), "t44 scoped status totals mismatch")
    return total_l3, total_held, total_runtime


def verify_all() -> dict[str, Any]:
    require(V3_JSON.is_file() and digest(V3_JSON.read_bytes()) == V3_JSON_SHA256, "v3 JSON snapshot missing or hash mismatch")
    require(V3_MD.is_file() and digest(V3_MD.read_bytes()) == V3_MD_SHA256, "v3 Markdown snapshot missing or hash mismatch")
    baseline_raw = V3_JSON.read_bytes()
    baseline = json.loads(baseline_raw.decode("utf-8"))
    baseline_md = V3_MD.read_text(encoding="utf-8")
    schema = load_json(SCHEMA_JSON)
    report = SCHEMA_MD.read_text(encoding="utf-8")
    fields = load_json(T44_FIELDS)
    cursor = load_json(T44_CURSOR)
    discovery = load_json(T44_DISCOVERY)
    grammar = load_json(T46_GRAMMAR)
    profile = load_json(T46_PROFILE)
    inventory = load_json(T37_INVENTORY)
    ledger = load_json(LEDGER)

    require((baseline.get("schema_version"), baseline.get("generated_by")) == (3, "t45"), "snapshot is not t45 v3")
    require((schema.get("schema_version"), schema.get("generated_by")) == (4, "t48"), "public schema is not t48 v4")
    require(schema.get("tables") == baseline.get("tables") and len(schema.get("tables", [])) == 8,
            "v3 eight numeric table objects changed")
    require(schema.get("negative_regressions") == baseline.get("negative_regressions") and len(schema["negative_regressions"]) == 4,
            "v3 negative regressions changed")
    require(schema.get("binary_provenance") == baseline.get("binary_provenance"), "v3 binary provenance changed")
    require(sum(len(table.get("fields", [])) for table in baseline["tables"]) == 52, "v3 table L3 baseline mismatch")
    require(sum(len(table.get("held_fields", [])) for table in baseline["tables"]) == 16, "v3 table held baseline mismatch")

    coverage = schema["coverage"]
    require((coverage.get("club_tables"), coverage.get("club_L3_fields"), coverage.get("club_L3_occurrences"),
             coverage.get("club_L3_unique_wire_fields"), coverage.get("held_fields"),
             coverage.get("held_fields_v3_numeric_tables"), coverage.get("negative_regressions"), coverage.get("L4")) ==
            (8, 52, 94, 59, 21, 16, 4, 0), "coverage counters mismatch")
    require(coverage.get("dual_accounting_policy", {}).get("club_L3_fields", "").startswith("v3 numeric-table scoped count retained verbatim"),
            "dual-accounting preservation policy missing")
    require("one u32 wire word" in coverage.get("dual_accounting_policy", {}).get("club_L3_unique_wire_fields", ""),
            "unique-slot bitmask policy missing")
    require("clfr" in coverage["dual_accounting_policy"]["club_L3_unique_wire_fields"], "runtime-only exclusion policy missing")
    require(coverage.get("t44_occurrence_grade_counts") == fields.get("occurrence_grades"), "t44 grade totals changed")

    # Recompute every unique physical slot from accepted t44 source records, not from builder output.
    slot_map = expected_wire_map(fields)
    require(sorted(slot_map) == [(0, 4), (5, 4), (9, 4), (13, 4), (17, 4), (35, 1), (42, 1)],
            "independently computed t44 unique slot set differs")
    require(coverage.get("t44_unique_wire_slot_count") == len(slot_map) == 7, "t44 unique wire slot count mismatch")

    sources = schema.get("club_auxiliary_sources", [])
    require(len(sources) == 1, "expected one named CLUB_LINK auxiliary source")
    source = sources[0]
    require((source.get("source_id"), source.get("source_kind"), source.get("member"), source.get("table_type")) ==
            ("CLUB_LINK", "named_auxiliary_pod", "server_db/club_links.dat", None), "CLUB_LINK source identity mismatch")
    require(source.get("entry_rtti") is None and source.get("entry_vptr") is None and
            source.get("vtable_slot19") is None and source.get("factory_case") is None,
            "CLUB_LINK numeric/RTTI factory identity was invented")
    require("no numeric table_type" in source.get("source_identity_note", ""), "CLUB_LINK auxiliary identity note missing")

    archives = cursor["archives"]
    server = archives["server"]
    client = archives["client"]
    replay = cursor["replay"]
    payload = source["server_payload"]
    require((server["count"], server["stride"], replay["payload_bytes"], replay["row_block_bytes"], replay["footer_bytes"]) ==
            (9261, 47, 435279, 435267, 0), "t44 source cursor dimensions mismatch")
    require(payload.get("closure_formula") == "12 + 9261 * 47 + 0 = 435279" and payload.get("closure_ok") is True,
            "CLUB_LINK POD closure mismatch")
    require(12 + 9261 * 47 + 0 == 435279 and payload.get("row_block_sha256") == replay.get("row_block_sha256") ==
            "17a167f0bb5945c19eacaf3a7884ea3c14b29eb4185aaf533e57f9a7ce89e75c", "CLUB_LINK row-block checksum mismatch")
    require(payload.get("payload_sha256") == server.get("payload_sha256") ==
            "8933328064b13a9d8dc153dd5b455970a7c28ada1e24f4ecc9df35735f42f3d2", "CLUB_LINK payload SHA mismatch")
    require(payload.get("header_hex") == "03017461642ef10d" and payload.get("count_offset") == 8 and payload.get("count_width_bytes") == 4,
            "CLUB_LINK header/count framing mismatch")
    require(source.get("cursor_semantics", {}).get("per_row_selector") is False and
            source["cursor_semantics"].get("per_row_identity_tail") is False and
            source["cursor_semantics"].get("vector_footer") is False, "CLUB_LINK cursor contains forbidden row trailer/footer")
    require(client.get("present") is False and client.get("entry") is None and source["client_observation"].get("present") is False,
            "client CLUB_LINK absence changed")
    require(source.get("version_gate") == {
        "word_VA": "0x141b60330", "threshold_hex": "0x0dd6", "observed_payload_version": 3569,
        "observed_payload_version_hex": "0x0df1", "selected_layout": "modern 47-byte rows", "runtime_assignment_observed": False,
    }, "CLUB_LINK version gate mismatch")
    reader = cursor["reader_cfg"]["22188560"]
    require(source.get("reader", {}).get("reader_VA") == reader.get("entry_VA") == "0x141529c10" and
            source["reader"].get("end_VA_exclusive") == reader.get("end_VA"), "t44 reader VA provenance mismatch")
    l3_count, held_count, runtime_count = verify_occurrences(source, fields)
    require(source["view_counts"] == {"scoped_L3_occurrences": l3_count, "held_occurrences": held_count,
                                      "runtime_only_occurrences": runtime_count, "unique_L3_wire_slots": 7},
            "CLUB_LINK view count summary mismatch")
    slots = source["wire_slot_policy"]["slots"]
    require(len(slots) == 7 and {(item["wire_offset"], item["width_bytes"]) for item in slots} == set(slot_map),
            "CLUB_LINK wire slot inventory mismatch")
    for slot in slots:
        require(set(slot.get("codes", [])) == slot_map[(slot["wire_offset"], slot["width_bytes"])],
                "CLUB_LINK slot field membership mismatch")
    require(source["wire_slot_policy"]["unique_l3_wire_slot_count"] == 7, "CLUB_LINK unique slot count mismatch")
    require(source.get("bool_word_evidence") == {
        "wire_offset": 5,
        "width_bytes": 4,
        "row0_hex": "e2018004",
        "row0_flags": {"frly": True, "golo": False},
        "flag_counts_32": fields["flag_counts"],
    } and len(source["bool_word_evidence"]["flag_counts_32"]) == 32,
        "CLUB_LINK shared bitmap word/flag_counts evidence mismatch")
    require(source.get("L4") == 0, "CLUB_LINK L4 must remain zero")

    provenance = discovery["provenance"]
    t44_provenance = source["provenance"]
    require(t44_provenance.get("source_task") == "t44" and t44_provenance.get("acceptance_ledger_entry") == "E84",
            "t44 source provenance/acceptance mismatch")
    require(t44_provenance.get("master_json_sha256") == MASTER_SHA256 and
            t44_provenance.get("editor_exe_sha256") == EDITOR_SHA256 and
            t44_provenance.get("manifest_sha256") == MANIFEST_SHA256, "t44 frozen provenance hashes mismatch")
    require(provenance.get("editor_sha256") == EDITOR_SHA256 and
            provenance.get("frozen_snapshots", {}).get("evidence/fm24/reports/editor_schema/master.json") == MASTER_SHA256,
            "t44 source provenance hash mismatch")

    # Verify nation-side state without promoting any field from its data profile.
    nation = schema.get("nation_data_side_status", {})
    require(nation.get("source_task") == "t46" and nation.get("acceptance_ledger_entry") == "E85" and
            nation.get("status") == "accepted_data_side_L1_L2_internal_grammar_open", "t46 status/provenance mismatch")
    require(nation.get("evidence_levels") == {"L1": True, "L2": True, "L3": 0, "L4": 0}, "t46 evidence levels mismatch")
    require(nation.get("server_only_fields_promoted") == 0 and nation.get("unknown_segment_count_positions_or_widths_promoted") == 0,
            "t46 nation fields/grammar were promoted")
    require(nation.get("grammar_diff_client_server") == grammar, "accepted t46 grammar data or negative result was changed")
    require(nation.get("segment_grammar") == grammar["segments"], "t46 A/B/C/D open status changed")
    require(nation.get("whole_row_grammar") == grammar["overall_row_grammar"], "t46 whole-row grammar result changed")
    require(nation.get("preserved_negative_result") == grammar["server_independent_observations"]["negative_result"],
            "t46 negative result wording changed")
    require(nation.get("server_payload", {}).get("payload_sha256") == profile["payload"]["payload_sha256"] ==
            "19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f", "t46 server payload hash mismatch")
    require(nation.get("server_payload", {}).get("row_block_sha256") == profile["row_closure"]["rows_sha256"] ==
            "4162770e55007a453c8ac55381458d28b414a0b5ba3836d6365a0887558ea45b", "t46 row-block SHA mismatch")
    require(nation.get("server_payload", {}).get("closure_formula") == profile["row_closure"]["equation"] ==
            "14 + sum(row_lens=422323) + 8 = 422345", "t46 closure mismatch")
    require(nation.get("client_comparison_only", {}).get("payload_sha256") ==
            "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34", "t46 client comparison SHA mismatch")
    require(nation.get("t37_inventory", {}).get("summary") == inventory["summary"] and
            nation["t37_inventory"].get("nation_exclusive_L3") == 0 and
            inventory["summary"].get("unknown_or_partial_parent_count") == 25 and
            inventory["summary"].get("new_L3_claims") == 0, "t37 partial nation state changed")
    require(nation.get("provenance", {}).get("reader_VA") is None and
            nation["provenance"].get("master_json_sha256") == MASTER_SHA256 and
            nation["provenance"].get("editor_exe_sha256") == EDITOR_SHA256, "t46 provenance note mismatch")

    entries = {entry.get("id"): entry for entry in ledger.get("entries", []) if entry.get("id") in {"E84", "E85"}}
    require((entries.get("E84", {}).get("kind"), entries.get("E84", {}).get("level")) == ("acceptance", "L3"), "E84 ledger record missing")
    require((entries.get("E85", {}).get("kind"), entries.get("E85", {}).get("level")) == ("acceptance", "L2"), "E85 ledger record missing")
    saved_ledger = schema["incremental_provenance"].get("acceptance_ledger_source", {})
    require(saved_ledger.get("path") == LEDGER and saved_ledger.get("sha256") == digest(path_for(LEDGER).read_bytes()) and
            saved_ledger.get("bytes") == path_for(LEDGER).stat().st_size, "current acceptance ledger provenance mismatch")
    for entry_id, entry in entries.items():
        saved = schema["incremental_provenance"]["acceptance_ledger_entries"][entry_id]
        require(saved.get("kind") == entry["kind"] and saved.get("level") == entry["level"] and
                saved.get("claim_sha256") == canonical_digest(entry["claim"]), f"{entry_id} ledger fingerprint mismatch")

    expected_artifacts = [artifact_record(path) for path in SOURCE_PATHS]
    for artifact in expected_artifacts:
        saved = next((item for item in schema.get("source_artifacts", []) if item.get("path") == artifact["path"]), None)
        require(saved == artifact, f"schema source artifact provenance mismatch: {artifact['path']}")
    require(t44_provenance.get("source_artifacts") == [item for item in expected_artifacts if item["path"].startswith("scratch/t44/")],
            "t44 artifact provenance list mismatch")
    require(nation["provenance"].get("source_artifacts") == [item for item in expected_artifacts if item["path"].startswith("scratch/t46/")],
            "t46 artifact provenance list mismatch")
    require(schema.get("incremental_provenance", {}).get("source_tasks") == ["t44", "t46"] and
            schema["incremental_provenance"].get("master_json_sha256") == MASTER_SHA256 and
            schema["incremental_provenance"].get("editor_exe_sha256") == EDITOR_SHA256,
            "incremental global provenance mismatch")
    require(schema.get("v3_baseline", {}).get("json_sha256") == V3_JSON_SHA256 and
            schema["v3_baseline"].get("markdown_sha256") == V3_MD_SHA256 and
            schema["v3_baseline"].get("tables_verbatim") is True, "v3 snapshot provenance missing")

    old_intro = "Generated by t45: the seven accepted t42 tables are retained verbatim and accepted t41 Csme evidence is appended. This is a consolidation of existing evidence; cursor extraction and payload/EXE parsing were not rerun."
    new_intro = "Generated by t48: the accepted t45 v3 baseline is retained; accepted t44 and t46 evidence is appended incrementally. No cursor extraction or payload/EXE parsing was rerun."
    expected_prefix = baseline_md.replace(old_intro, new_intro, 1).rstrip() + "\n\n## t48 Incremental Addendum"
    require(old_intro in baseline_md and report.startswith(expected_prefix), "v3 Markdown body was not preserved before the v4 addendum")
    require("zero nation-exclusive L3" in report and "e2018004" in report and "flag_counts` vector" in report,
            "v4 addendum lacks bitmap/t37 exclusivity evidence")
    require("## Provenance" in report and "Cafl" in report and "Cvfl" in report and "t46 E85" in report,
            "v4 Markdown lacks scoped source/provenance sections")
    return {"l3_occurrences": l3_count, "held_occurrences": held_count, "runtime_occurrences": runtime_count,
            "unique_wire_slots": len(slot_map), "nation_L3": nation["evidence_levels"]["L3"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently verify the t48 schema v4 outputs and accepted source provenance.")
    parser.add_argument("--selftest", action="store_true", help="run all independent preservation, closure, and coverage assertions")
    args = parser.parse_args(argv)
    try:
        result = verify_all()
        print(
            "VERIFY PASS: v3 eight tables verbatim; "
            f"L3 occurrences={52 + result['l3_occurrences']} unique wire fields={52 + result['unique_wire_slots']} "
            f"held occurrences={16 + result['held_occurrences']} runtime-only={result['runtime_occurrences']} "
            f"nation L3={result['nation_L3']} L4=0"
        )
        return 0
    except VerifyFailure as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
