#!/usr/bin/env python3
"""Independently verify public schema v10 against pinned t62-t69 evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V9_JSON = OUT / "club_nation_subtable_schema.v9.json"
V9_MD = OUT / "club_nation_subtable_schema.v9.md"
V10_JSON = OUT / "club_nation_subtable_schema.v10.json"
V10_MD = OUT / "club_nation_subtable_schema.v10.md"
LEDGER = ROOT / "scratch" / "t01" / "LEDGER.json"
BASE_JSON_SHA256 = "703df30ea34fbee3b555ccf4233d4fe012bcb614435381efb68a3224e5ae64ee"
BASE_MD_SHA256 = "ded0da91af36098b2648af769ed258fd39d903e86f0494b5b2f8fab3a98c5757"
GUARDED_IDS = tuple(f"E{i}" for i in range(84, 110))
NEW_CLUB_L3 = ["Ccba", "Cadm", "Cesd", "Ceed", "Cead", "CteA", "Chaf", "Cmtp"]
SOURCE_SHA256 = {
    "scratch/t62/out/chain.json": "09344d8caf0f71bd84c5073de38b7f338b649b3fea653e9d56d29ab56d5fad70",
    "scratch/t62/out/xref.json": "649baa2f57b67ddba6dc3835e2fedd45acfc4e3095df4cb733e93689787d246e",
    "scratch/t62/out/exclusions.json": "1ca20195a487310ae273911c34d81125169b48b2a2b07f058a4e99019cec2d96",
    "scratch/t62/out/REPORT.md": "795cc016469cabfad7fc781d4b1595c8751218925dcf107673dd9c855c1af15c",
    "scratch/t62/out/DONE.md": "e7450053b9153bc5bfc3d14f433f19d54ed5c63eb424e40f031aead9af2b2a33",
    "scratch/t62/out/verify.py": "61562ed4019f1caf48341665b38705b7748426ec4a9a906216e18293a50bb493",
    "scratch/t63/out/field_map_r2.json": "5bdf1fc6e35c6c0cabe666a0e173228f6127a770392b73ca8d23b0a35c24dd46",
    "scratch/t63/out/projections.json": "2526ecc58871f7d994e58fcf2d42aab11d1ccf0e45afa79d525e16f86ed3a08b",
    "scratch/t63/out/REPORT.md": "860c2b8b747fb674c0ca24a341551a7e0a6c9f02458253f0d754a4b722b650cf",
    "scratch/t63/out/DONE.md": "9cf7ed3bbca5ea8d6d7dc56050a2bc9e4b53f0bbd3e0eec6e755a6c68d7ca38f",
    "scratch/t63/out/verify.py": "4b114464b8b40d0b143bd988f1aa8fc62509a06e98e30dab26c6fd224064cb26",
    "scratch/t64/out/field_map_r2.json": "77fbe4c4f913dc7ab5c3e067c09f1e9ca0f9be75d1ae1e336ce7b40a463317b1",
    "scratch/t64/out/helpers.json": "daa0c8f2f261e9bc9779339d4c02f028bfbea02da689034a4f90b22b1c485c2c",
    "scratch/t64/out/exclusions.json": "6393247ab76fd21e1fbd507a081a416c5e317e7fda8c5585c532bb70e1d704ee",
    "scratch/t64/out/REPORT.md": "fe9c92c540fa7344a76e25b9310543c181af91d59cbedc736c53b7e9dec7f5d8",
    "scratch/t64/out/DONE.md": "1ab6201ee52c69570a5d192f6ab469ce8760d7acfe7e9bba2afee15df43d5818",
    "scratch/t64/out/verify.py": "ebb3def43e0a43673378da997858a3b0d6acd9512d629b52160275cc76d0a812",
    "scratch/t65/out/field_map_r2.json": "637c583e5e0c08ad72e40c16496fed0f2dc800df23b65e1db3de28c4aee69a20",
    "scratch/t65/out/projections.json": "2b326d2a2e19fe861383a815907b551f91a5ffc98ea48f37767bc532c64c2c4e",
    "scratch/t65/out/REPORT.md": "4e63556814c4ddc7ac4d43eb9992af4eb800b6db07e2c2a16332968fa29ad658",
    "scratch/t65/out/DONE.md": "4e7b4c1cc00658c5d07890a0fb6b95e35d7d790bf9e9cc7d687ac97f14423813",
    "scratch/t65/out/verify.py": "b8f94b25c9a050d4e29e50336b6cd23f8ff85c0185a92cb046a4cdc3723b1188",
    "scratch/t66/out/collections.json": "e4e133a44b98488f9981bf17442165dcd172bbeaf0a6a8ef120b43b43697932d",
    "scratch/t66/out/census.json": "a433472c132a7263cc03cbb41a774656ec9f080c46b83994de4058ca3ef3ae56",
    "scratch/t66/out/REPORT.md": "75431d107b0209a65821c529c19e81266e0d1a607984163e9403fa161323db5a",
    "scratch/t66/out/DONE.md": "a8a000d3ae76217264ef163c37c78b403a3e0ff80b897845878a0828dc93d4e0",
    "scratch/t66/out/verify.py": "6d680dde9263290d1ee52613e4d9821c4aca4687dff96622953d8aaae197b28f",
    "scratch/t69/out/tail_ledger.json": "60940356817f2420148eea4ffa3fd7e6794dce4ecccb27bbb34f292bae265d05",
    "scratch/t69/out/SUMMARY.md": "b7eb17d6bbdeaf034b8747e82c7bcf6c8f28fd72fa10516b3c42dd465ddce83d",
    "scratch/t69/out/REPORT.md": "b7358e85fadc2ba11f014dca0736e07f03741865acf020d41a657980cd602c41",
    "scratch/t69/out/DONE.md": "12b4dece22ff124089fa114239c9a27d4d363ea1cf9531f58d67abcbbfb0aa33",
    "scratch/t69/out/verify.py": "659bb0bd1b16c5200995f0ed226cfb5864b52c58e180c3685bd3f2680eadac67",
}
JSON_INPUTS = {
    "t62": {"chain": "scratch/t62/out/chain.json", "xref": "scratch/t62/out/xref.json",
            "exclusions": "scratch/t62/out/exclusions.json"},
    "t63": {"field_map_r2": "scratch/t63/out/field_map_r2.json", "projections": "scratch/t63/out/projections.json"},
    "t64": {"field_map_r2": "scratch/t64/out/field_map_r2.json", "helpers": "scratch/t64/out/helpers.json",
            "exclusions": "scratch/t64/out/exclusions.json"},
    "t65": {"field_map_r2": "scratch/t65/out/field_map_r2.json", "projections": "scratch/t65/out/projections.json"},
    "t66": {"collections": "scratch/t66/out/collections.json", "census": "scratch/t66/out/census.json"},
    "t69": {"tail_ledger": "scratch/t69/out/tail_ledger.json"},
}
TEXT_INPUTS = {
    "t62": {"REPORT.md": "scratch/t62/out/REPORT.md", "DONE.md": "scratch/t62/out/DONE.md"},
    "t63": {"REPORT.md": "scratch/t63/out/REPORT.md", "DONE.md": "scratch/t63/out/DONE.md"},
    "t64": {"REPORT.md": "scratch/t64/out/REPORT.md", "DONE.md": "scratch/t64/out/DONE.md"},
    "t65": {"REPORT.md": "scratch/t65/out/REPORT.md", "DONE.md": "scratch/t65/out/DONE.md"},
    "t66": {"REPORT.md": "scratch/t66/out/REPORT.md", "DONE.md": "scratch/t66/out/DONE.md"},
    "t69": {"SUMMARY.md": "scratch/t69/out/SUMMARY.md", "REPORT.md": "scratch/t69/out/REPORT.md",
            "DONE.md": "scratch/t69/out/DONE.md"},
}
TASK_FILES = {
    "t62": ["scratch/t62/out/chain.json", "scratch/t62/out/xref.json", "scratch/t62/out/exclusions.json",
            "scratch/t62/out/REPORT.md", "scratch/t62/out/DONE.md", "scratch/t62/out/verify.py"],
    "t63": ["scratch/t63/out/field_map_r2.json", "scratch/t63/out/projections.json",
            "scratch/t63/out/REPORT.md", "scratch/t63/out/DONE.md", "scratch/t63/out/verify.py"],
    "t64": ["scratch/t64/out/field_map_r2.json", "scratch/t64/out/helpers.json", "scratch/t64/out/exclusions.json",
            "scratch/t64/out/REPORT.md", "scratch/t64/out/DONE.md", "scratch/t64/out/verify.py"],
    "t65": ["scratch/t65/out/field_map_r2.json", "scratch/t65/out/projections.json",
            "scratch/t65/out/REPORT.md", "scratch/t65/out/DONE.md", "scratch/t65/out/verify.py"],
    "t66": ["scratch/t66/out/collections.json", "scratch/t66/out/census.json",
            "scratch/t66/out/REPORT.md", "scratch/t66/out/DONE.md", "scratch/t66/out/verify.py"],
    "t69": ["scratch/t69/out/tail_ledger.json", "scratch/t69/out/SUMMARY.md",
            "scratch/t69/out/REPORT.md", "scratch/t69/out/DONE.md", "scratch/t69/out/verify.py"],
}
NEW_ROOT_KEYS = {"club_main_row_fields_r2", "comp_main_row_fields_r2", "nation_main_row_fields_r2",
                 "comp_collections", "edfx_edsc_dispatch", "tail_ledger"}
MUTABLE_COVERAGE = {"club_main_row_L3", "club_main_row_new_L3", "club_main_row_held", "club_main_row_unmapped"}


class CheckFailure(Exception):
    pass


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha(raw)


def load_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def verify_sources() -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]],
                              dict[str, dict[str, str]]]:
    source_records: dict[str, dict[str, Any]] = {}
    manifests: dict[str, list[dict[str, Any]]] = {}
    documents: dict[str, dict[str, str]] = {}
    for task, rels in TASK_FILES.items():
        manifests[task] = []
        for rel in rels:
            raw = (ROOT / rel).read_bytes()
            actual = sha(raw)
            require(actual == SOURCE_SHA256[rel], f"accepted source changed: {rel}")
            manifests[task].append({"path": rel, "sha256": actual, "bytes": len(raw)})
        source_records[task] = {key: load_json(ROOT / rel) for key, rel in JSON_INPUTS[task].items()}
        documents[task] = {name: (ROOT / rel).read_bytes().decode("utf-8")
                           for name, rel in TEXT_INPUTS[task].items()}
    return source_records, manifests, documents


def baseline_pair() -> tuple[dict[str, Any], bytes, bytes]:
    require(V9_JSON.is_file() and V9_MD.is_file(), "v9 snapshots missing")
    jraw, mraw = V9_JSON.read_bytes(), V9_MD.read_bytes()
    require(sha(jraw) == BASE_JSON_SHA256 and sha(mraw) == BASE_MD_SHA256, "v9 snapshot hash mismatch")
    schema = json.loads(jraw)
    require(schema.get("schema_version") == 9 and schema.get("generated_by") == "t60",
            "v9 snapshot identity")
    return schema, jraw, mraw


def verify_ledger(schema: dict[str, Any]) -> None:
    ledger = load_json(LEDGER)
    live = {item.get("id"): item for item in ledger["entries"] if item.get("id") in GUARDED_IDS}
    require(set(live) == set(GUARDED_IDS), "live ledger E84-E109 incomplete")
    snap = schema["incremental_provenance"]["t70_ledger_snapshot"]
    require(snap["guarded_entries"] == list(GUARDED_IDS), "ledger snapshot guard extent")
    expected_detail = []
    for entry_id in GUARDED_IDS:
        item = live[entry_id]
        digest = canonical_sha256(item["claim"])
        row = {"id": entry_id, "kind": item["kind"], "level": item["level"], "claim_sha256": digest}
        expected_detail.append(row)
        stored = schema["incremental_provenance"]["acceptance_ledger_entries"].get(entry_id)
        require(stored is not None and stored["kind"] == row["kind"] and stored["level"] == row["level"] and
                stored["claim_sha256"] == digest, f"acceptance ledger record mismatch: {entry_id}")
    require(snap["entries"] == expected_detail, "entry-level ledger guard mismatch")
    require(snap["guard_scope"] == "entry-level id, kind, level, and canonical claim SHA-256; no live full-file hash or byte-count pin",
            "ledger snapshot guard policy")
    require(live["E104"]["level"] == live["E105"]["level"] == live["E106"]["level"] ==
            live["E107"]["level"] == live["E108"]["level"] == "L3" and live["E109"]["level"] == "L2",
            "accepted t62-t69 evidence levels")


def verify_protected(baseline: dict[str, Any], updated: dict[str, Any]) -> None:
    protected = {"tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
                 "club_main_row_fields", "nation_main_row_fields", "comp_main_row_fields"}
    protected.update(key for key in baseline if key.startswith("nation_"))
    for key in protected:
        require(updated.get(key) == baseline.get(key), f"protected section changed: {key}")
    require(set(updated) == set(baseline) | NEW_ROOT_KEYS, "root-level schema additions changed")
    for key, old in baseline.items():
        if key in {"schema_version", "generated_by", "coverage", "incremental_provenance"}:
            continue
        require(updated.get(key) == old, f"unrequested v9 root key changed: {key}")
    for key, old in baseline["coverage"].items():
        if key not in MUTABLE_COVERAGE:
            require(updated["coverage"].get(key) == old, f"unapproved coverage delta: {key}")
    oldprov = baseline["incremental_provenance"]
    newprov = updated["incremental_provenance"]
    for key, old in oldprov.items():
        if key in {"tasks", "acceptance_ledger_entries"}:
            continue
        require(newprov.get(key) == old, f"unapproved provenance delta: {key}")
    for key, old in oldprov["tasks"].items():
        require(newprov["tasks"].get(key) == old, f"existing task provenance changed: {key}")
    for key, old in oldprov["acceptance_ledger_entries"].items():
        require(newprov["acceptance_ledger_entries"].get(key) == old,
                f"existing acceptance ledger guard changed: {key}")


def verify_embedded_records(schema: dict[str, Any], src: dict[str, dict[str, Any]],
                            manifests: dict[str, list[dict[str, Any]]],
                            documents: dict[str, dict[str, str]]) -> None:
    club = schema["club_main_row_fields_r2"]
    club_map = src["t63"]["field_map_r2"]
    club_all = club_map["fields"]
    require(club["source_records"] == {"field_map_r2": club_map, "projections": src["t63"]["projections"]},
            "embedded t63 records differ from accepted evidence")
    require(club["source_artifacts"] == manifests["t63"] and
            club["source_documents"] == documents["t63"], "t63 source document/artifact provenance mismatch")
    require(club["round2_reviewed"] == 399 and club["round2_grade_counts"] ==
            {"L3": 8, "held": 41, "unmapped": 350} and club["new_L3"] == NEW_CLUB_L3 and club["L4"] == 0,
            "t63 round-2 counters")
    require(club["new_L3_records"] == [row for row in club_all if row.get("code") in NEW_CLUB_L3],
            "t63 new-L3 rows mismatch")
    require(club["held_records"] == [row for row in club_all if row.get("grade") == "held"] and
            club["unmapped_records"] == [row for row in club_all if row.get("grade") == "unmapped"],
            "t63 held/unmapped records mismatch")
    casp = next(row for row in club_all if row.get("code") == "Casp")["first_counterexample"]
    require(club["casp_counterexample"] == casp and casp["value"] == 85746.4609375 and
            casp["absolute"] == 15571299, "Casp counterexample lost")
    require(club["cumulative_L3"] == 21 and club["prior_round_preserved"] ==
            {"L3": 13, "held": 11, "skipped_separate_member": 10, "unmapped": 399}, "club cumulative count")

    comp = schema["comp_main_row_fields_r2"]
    comp_map = src["t64"]["field_map_r2"]
    require(comp["source_records"] == {"field_map_r2": comp_map, "helpers": src["t64"]["helpers"],
                                        "exclusions": src["t64"]["exclusions"]},
            "embedded t64 records differ from accepted evidence")
    require(comp["source_artifacts"] == manifests["t64"] and comp["source_documents"] == documents["t64"] and
            comp["round2_reviewed"] == 196 and comp["new_L3"] == 0 and comp["baseline_frozen"] ==
            {"L3": 49, "held": 10, "unmapped": 196, "order_inversions": 818}, "t64 negative increment")
    expected_static = {name: src["t64"]["helpers"]["main_reader"]["payload_entry_conditions"][key]["data"]
                       for key, name in (("a8", "+0xa8"), ("e0", "+0xe0"))}
    require(comp["static_zero_samples"] == expected_static and
            all(row["client"]["presence_events"] == 0 and row["server"]["presence_events"] == 7047 and
                row["server"]["presence_nonzero"] == 0 and row["server"]["object_events"] == 0
                for row in expected_static.values()), "t64 static-zero sample evidence")
    require(comp["stream_call_accounting"]["direct"] == 55 and comp["stream_call_accounting"]["outer"] == 52 and
            comp["stream_call_accounting"]["tag4_alternates"] == 3 and comp["L4"] == 0,
            "t64 corrected stream call accounting")

    nation = schema["nation_main_row_fields_r2"]
    nation_map = src["t65"]["field_map_r2"]
    all_nation = nation_map["fields"]
    held = [row for row in all_nation if row.get("grade") == "held" and row.get("status") != "unchanged_e94"]
    unmapped = [row for row in all_nation if row.get("grade") == "unmapped"]
    require(nation["source_records"] == {"field_map_r2": nation_map, "projections": src["t65"]["projections"]},
            "embedded t65 records differ from accepted evidence")
    require(nation["source_artifacts"] == manifests["t65"] and nation["source_documents"] == documents["t65"] and
            nation["round2_reviewed"] == 327 and
            nation["new_L3"] == 0 and nation["round2_grade_counts"] == {"held": 9, "unmapped": 318} and
            nation["held_records"] == held and nation["unmapped_records"] == unmapped and
            len(held) == 9 and len(unmapped) == 318 and nation["L4"] == 0, "t65 held/unmapped records")
    require(nation["dual_archive_closure"] == {"client": "13+24710+9=24732", "server": "13+422323+9=422345",
                                               "identity_width": 12, "footer_hex": "00000000|01|ec7ae404"},
            "t65 closure")

    compc = schema["comp_collections"]
    coll = src["t66"]["collections"]
    census = src["t66"]["census"]
    require(compc["source_records"] == {"collections": coll, "census": census} and
            compc["source_artifacts"] == manifests["t66"] and compc["source_documents"] == documents["t66"],
            "embedded t66 records/documents differ from accepted evidence")
    require(compc["L3_physical_grammars"] == 7 and compc["L3_reference_lanes"] == 4 and
            compc["held_reference_lanes"] == 4 and compc["independent_member_bindings"] == 0 and
            compc["L4"] == 0, "t66 grade totals")
    expected_grammars = ["vec18", "+0xe8", "+0xc0", "+0xc8", "+0xd0", "+0xd8", "+0x100"]
    expected_bindings = [
        {"slot": "vec18", "lane": "item.+1", "target_table": 24},
        {"slot": "+0xd0", "lane": "item.+0", "target_table": 23},
        {"slot": "+0xd8", "lane": "item.+0", "target_table": 23},
        {"slot": "+0xd8", "lane": "item.+4", "target_table": 23},
    ]
    expected_held_lanes = [
        {"slot": "+0xe8", "lane": "item.+2", "reason": "6597/6597 all-ones; no live target"},
        {"slot": "+0xc0", "lane": "inner.+4", "reason": "t10 ordinal miss; multiple other domains match"},
        {"slot": "+0xc0", "lane": "inner.+8", "reason": "t10 ordinal miss; multiple other domains match"},
        {"slot": "+0xd0", "lane": "item.+4", "reason": "no live values; first @842 is ffffffff"},
    ]
    require(compc["L3_grammar_slots"] == expected_grammars and
            compc["L3_reference_lane_bindings"] == expected_bindings and
            compc["held_reference_lane_records"] == expected_held_lanes and
            compc["held_slots"] == ["vec30", "+0xa8", "+0xe0"], "t66 grade-level lane bindings")

    expected_nonempty = {"+0xc0": 315, "+0xc8": 366, "+0xd0": 121, "+0xd8": 51}
    for key, count in expected_nonempty.items():
        rows = coll["collections"][key]["sides"]["server"]["nonempty_ordinals"]
        require(len(rows) == count and compc["corrected_nonempty_rows"][key] == count,
                f"t66 nonempty row count {key}")
    require(census["identity_width"] == 12 and census["envelopes"]["client"]["payload"] == 894991 and
            census["envelopes"]["server"]["payload"] == 1533972, "t66 archive closure")

    ed = schema["edfx_edsc_dispatch"]
    chain, xref, exclusions = src["t62"]["chain"], src["t62"]["xref"], src["t62"]["exclusions"]
    require(ed["source_records"] == {"chain": chain, "xref": xref, "exclusions": exclusions} and
            ed["source_artifacts"] == manifests["t62"] and ed["source_documents"] == documents["t62"],
            "embedded t62 records/documents differ from accepted evidence")
    dispatch = ed["edsc_dispatch"]
    route = xref["key_routes"]["EDsc"]
    require(dispatch == {"key": "0x45447363", "normalized_index": "0x32", "table_base": "0x2a7f0",
                         "cell": "0x2a8b8", "cell_bytes": "99ebffff", "rel32": -5223,
                         "target": "0x29389", "unique_target_index": True,
                         "consumer_types": {"COMP": 25, "NATION": 10}, "persisted_field": False},
            "t62 EDsc bound dispatch")
    require(route["index"] == 0x32 and route["cell"] == 0x2a8b8 and route["entry"] == 0x29389 and
            route["same_target_indices"] == [0x32] and ed["L4"] == 0 and
            ed["original_t55_grade_preserved"] == "held", "t62 EDsc dispatch and grade")
    require(ed["edfx"]["upstream_persistence_bound"] is False and ed["edfx"]["reader"] is None and
            ed["edfx"]["writer"] is None and ed["edfx"]["member"] is None and
            ed["edfx"]["bounded_exclusions"] == len(exclusions["excludes"]) == 7, "t62 EDfx boundary")

    tail = schema["tail_ledger"]
    tail_src = src["t69"]["tail_ledger"]
    require(tail["source_records"] == {"tail_ledger": tail_src} and tail["source_artifacts"] == manifests["t69"] and
            tail["source_documents"] == documents["t69"], "embedded t69 record/documents differ from accepted evidence")
    require(tail["items"] == 18 and tail["items"] == tail_src["count"] and tail["unresolved_club"] == [] and
            tail["totals"] == tail_src["totals"] and tail["new_L3"] == 0 and tail["L4"] == 0,
            "t69 reconciliation")


def verify_coverage_and_provenance(schema: dict[str, Any], baseline: dict[str, Any],
                                   manifests: dict[str, list[dict[str, Any]]],
                                   v9_json: bytes, v9_md: bytes) -> None:
    expected_coverage = {
        "club_main_row_L3": 21, "club_main_row_new_L3": 8, "club_main_row_held": 41,
        "club_main_row_unmapped": 350, "club_main_row_occurrences": 433,
        "club_main_row_skipped_separate_member": 10, "club_main_row_r1_L3": 13, "club_main_row_r1_held": 11,
        "club_main_row_r1_skipped_separate_member": 10, "club_main_row_r1_unmapped": 399,
        "club_main_row_r1_new_L3": 5, "club_main_row_r2_reviewed": 399,
        "club_main_row_r2_new_L3": 8, "club_main_row_r2_held": 41, "club_main_row_r2_unmapped": 350,
        "comp_main_row_r2_reviewed": 196, "comp_main_row_r2_new_L3": 0,
        "nation_main_row_r2_reviewed": 327, "nation_main_row_r2_new_L3": 0,
        "nation_main_row_r2_held": 9, "nation_main_row_r2_unmapped": 318,
        "comp_collections_L3_physical_grammars": 7, "comp_collections_L3_reference_lanes": 4,
        "comp_collections_held_reference_lanes": 4, "comp_collections_independent_member_bindings": 0,
        "edsc_dispatch_closed": 1, "edfx_upstream_persistence_bound": 0,
        "tail_ledger_items": 18, "tail_ledger_unresolved_club": 0,
    }
    for key, value in expected_coverage.items():
        require(schema["coverage"].get(key) == value, f"coverage count mismatch: {key}")
    require(schema["schema_version"] == 10 and schema["generated_by"] == "t70", "v10 identity")
    prov = schema["incremental_provenance"]
    task_entries = {"t62": "E105", "t63": "E106", "t64": "E107", "t65": "E108", "t66": "E104", "t69": "E109"}
    live_ledger = {item["id"]: item for item in load_json(LEDGER)["entries"] if item.get("id") in task_entries.values()}
    for task, entry_id in task_entries.items():
        item = prov["tasks"].get(task)
        ledger_item = live_ledger[entry_id]
        claim_hash = canonical_sha256(ledger_item["claim"])
        require(item is not None and item["acceptance_ledger_entry"] == entry_id and
                item["acceptance_ledger_level"] == ledger_item["level"] and
                item["ledger_claim_sha256"] == claim_hash and item["accepted_claim"] == ledger_item["claim"] and
                item["source_artifacts"] == manifests[task], f"task provenance mismatch: {task}")
    require(prov["t70_ledger_snapshot"]["v9_baseline_acceptance_entry"] == "E100" and
            prov["t70_ledger_snapshot"]["v9_baseline_acceptance_level"] == "L3", "baseline ledger provenance")
    require(prov["t70_ledger_snapshot"]["v9_baseline_files"] == {
                "json": {"path": "scratch/t70/out/club_nation_subtable_schema.v9.json",
                         "sha256": sha(v9_json), "bytes": len(v9_json)},
                "markdown": {"path": "scratch/t70/out/club_nation_subtable_schema.v9.md",
                             "sha256": sha(v9_md), "bytes": len(v9_md)},
            }, "v9 baseline file provenance")
    require(set(prov["acceptance_ledger_entries"]) >= set(GUARDED_IDS), "ledger entry rows incomplete")
    verify_ledger(schema)
    require(baseline["schema_version"] == 9, "v9 comparison input")


def verify_all() -> tuple[dict[str, Any], bytes, bytes]:
    baseline, v9_json, v9_md = baseline_pair()
    src, manifests, documents = verify_sources()
    public_json = PUBLIC_JSON.read_bytes()
    public_md = PUBLIC_MD.read_bytes()
    require(sha(public_json) == sha(V10_JSON.read_bytes()) and sha(public_md) == sha(V10_MD.read_bytes()),
            "public and t70 v10 copies differ")
    schema = json.loads(public_json)
    require(schema["schema_version"] == 10 and schema["generated_by"] == "t70", "public identity")
    require(public_md.startswith(v9_md), "v9 Markdown prefix changed")
    require(sha(v9_json) == BASE_JSON_SHA256 and sha(v9_md) == BASE_MD_SHA256, "pinned baseline changed")
    verify_protected(baseline, schema)
    verify_embedded_records(schema, src, manifests, documents)
    verify_coverage_and_provenance(schema, baseline, manifests, v9_json, v9_md)
    return schema, public_json, public_md


def selftest() -> None:
    schema, _, _ = verify_all()
    bad = dict(schema)
    bad["club_main_row_fields"] = {**schema["club_main_row_fields"], "L3": -1}
    detected = False
    try:
        baseline, _, _ = baseline_pair()
        verify_protected(baseline, bad)
    except CheckFailure:
        detected = True
    require(detected, "selftest failed to detect protected-section mutation")
    bad_coverage = {**schema, "coverage": {**schema["coverage"], "nation_main_row_r2_held": 8}}
    detected = False
    try:
        baseline, v9_json, v9_md = baseline_pair()
        _, manifests, _ = verify_sources()
        verify_coverage_and_provenance(bad_coverage, baseline, manifests, v9_json, v9_md)
    except CheckFailure:
        detected = True
    require(detected, "selftest failed to detect coverage mutation")
    print("t70 independent verifier selftest PASS: current v10 plus protected-section and counter tamper probes")


def write_log(path: str | None, text: str) -> None:
    if path is None:
        return
    target = (OUT / path).resolve()
    require(target.parent == OUT.resolve() and target.name.startswith("spot_") and target.suffix == ".log",
            "--log must name spot_*.log directly under scratch/t70/out")
    target.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify public v10 pair (default)")
    group.add_argument("--selftest", action="store_true", help="run verification and tamper probes")
    group.add_argument("--anchors", action="store_true", help="run t01 anchor regression")
    parser.add_argument("--log", help="write successful check summary to spot_*.log under this directory")
    args = parser.parse_args()
    try:
        if args.anchors:
            proc = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "scripts" / "t01_anchors.py")],
                                  cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            message = proc.stdout + proc.stderr
            require(proc.returncode == 0 and "7/7 checks passed" in message, "t01 anchors did not pass 7/7")
            print(message, end="")
        elif args.selftest:
            selftest()
            message = "t70 independent verifier selftest PASS: v9 protection, source records, E84-E109 and tamper probes\n"
        else:
            schema, json_raw, md_raw = verify_all()
            message = ("t70 independent verification PASS\n"
                       f"schema_version={schema['schema_version']} generated_by={schema['generated_by']}\n"
                       f"club r2=8 L3 / 41 held / 350 unmapped; cumulative L3={schema['coverage']['club_main_row_L3']}\n"
                       "COMP r2=196 reviewed / 0 L3; nation r2=9 held / 318 unmapped / 0 L3\n"
                       "collections=7 physical grammars / 4 reference lanes; EDsc 0x32->0x29389; tail=18 unresolved=0\n"
                       f"v10 JSON sha256={sha(json_raw)} bytes={len(json_raw)}\n"
                       f"v10 Markdown sha256={sha(md_raw)} bytes={len(md_raw)}\n")
            print(message, end="")
        write_log(args.log, message)
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
