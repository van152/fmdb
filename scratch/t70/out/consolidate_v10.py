#!/usr/bin/env python3
"""Incrementally consolidate accepted t62-t69 evidence into public schema v10."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
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
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
BASE_JSON_SHA256 = "703df30ea34fbee3b555ccf4233d4fe012bcb614435381efb68a3224e5ae64ee"
BASE_MD_SHA256 = "ded0da91af36098b2648af769ed258fd39d903e86f0494b5b2f8fab3a98c5757"
GUARDED_IDS = tuple(f"E{i}" for i in range(84, 110))
EXPECTED_CLAIM_SHA256 = {
    "E100": "213e1807096d8746b638d1cedc979fbb4234a399226ddc7036559e5a35749d0f",
    "E101": "73207fd951b9fd818d19bab1a49c7fa4fbdd5b3c54c471b06ffe8610bfd5c946",
    "E102": "1bfd9ffe357637aefcc1cc44d5b0d33c229ae81f7bebde4c5e61e5434a6d7893",
    "E103": "1cf2765e3cfe3e1760a937478dcaa6c3d4300d23591a29ce784fd4963ccb6aba",
    "E104": "07741d4a9a0fa404806d3ab293a41a5272837b0a09db818e398efb5842f7d93f",
    "E105": "28250a4ab2040b2ba6e576b0cb8af0a6497c334b38140bf0f751f3570516f18e",
    "E106": "2d1a9d0123551a95c9fbda14fa95135ceeaf29d1f9fadb2fb8dbca5a7c6dd702",
    "E107": "596268041c541d72bbfb9e749f8e29e3bb6ff6d658545b58d8bd8b3c10ce56bf",
    "E108": "43fcce478fff7d2ec680ff61d16ba8c6c7e77e3518e1514e1760d1f53ec0a8bf",
    "E109": "0afdc3111c194b104dfb543f958f7a9f25fbceb7da6cc0baa0e7a673d1179746",
}
NEW_CLUB_L3 = ["Ccba", "Cadm", "Cesd", "Ceed", "Cead", "CteA", "Chaf", "Cmtp"]
T64_EXCLUSIONS = {
    "advanced_rules_or_debug": 4,
    "bounded_getter_without_wire_closure": 38,
    "derived_count": 2,
    "derived_list_or_shared_handler": 5,
    "derived_parent_or_global_state": 1,
    "no_bounded_comp_getter_case": 141,
    "projection_candidate": 1,
    "rules_context_sibling": 4,
}
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def ledger_record(item: dict[str, Any]) -> dict[str, Any]:
    row = {"kind": item["kind"], "level": item["level"]}
    row["claim_sha256"] = canonical_sha256(item["claim"])
    return row


def load_baseline() -> tuple[dict[str, Any], bytes, bytes]:
    have_json, have_md = V9_JSON.exists(), V9_MD.exists()
    require(have_json == have_md, "incomplete v9 snapshot pair")
    if have_json:
        json_raw, md_raw = V9_JSON.read_bytes(), V9_MD.read_bytes()
    else:
        json_raw, md_raw = PUBLIC_JSON.read_bytes(), PUBLIC_MD.read_bytes()
    require(sha(json_raw) == BASE_JSON_SHA256 and sha(md_raw) == BASE_MD_SHA256,
            "pinned v9 baseline SHA-256")
    baseline = json.loads(json_raw)
    require(baseline.get("schema_version") == 9 and baseline.get("generated_by") == "t60",
            "v9 baseline identity")
    return baseline, json_raw, md_raw


def load_sources() -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]],
                            dict[str, dict[str, str]]]:
    records: dict[str, dict[str, Any]] = {}
    artifacts: dict[str, list[dict[str, Any]]] = {}
    documents: dict[str, dict[str, str]] = {}
    for task, rels in TASK_FILES.items():
        artifacts[task] = []
        for rel in rels:
            raw = (ROOT / rel).read_bytes()
            require(sha(raw) == SOURCE_SHA256[rel], f"accepted source SHA-256 mismatch: {rel}")
            artifacts[task].append({"path": rel, "sha256": SOURCE_SHA256[rel], "bytes": len(raw)})
        records[task] = {name: read_json(ROOT / rel) for name, rel in JSON_INPUTS[task].items()}
        documents[task] = {name: (ROOT / rel).read_bytes().decode("utf-8")
                           for name, rel in TEXT_INPUTS[task].items()}
    return records, artifacts, documents


def load_ledger() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    ledger = read_json(LEDGER_PATH)
    found: dict[str, dict[str, Any]] = {}
    for item in ledger["entries"]:
        entry_id = item.get("id")
        if entry_id in GUARDED_IDS:
            require(entry_id not in found, f"duplicate ledger entry {entry_id}")
            found[entry_id] = item
    require(set(found) == set(GUARDED_IDS), "ledger guard set E84-E109 incomplete")
    guards = []
    for entry_id in GUARDED_IDS:
        item = found[entry_id]
        claim_sha = canonical_sha256(item["claim"])
        if entry_id in EXPECTED_CLAIM_SHA256:
            require(claim_sha == EXPECTED_CLAIM_SHA256[entry_id], f"fixed acceptance claim changed: {entry_id}")
        require(item.get("kind") == "acceptance", f"ledger kind is not acceptance: {entry_id}")
        guards.append({"id": entry_id, "kind": item["kind"], "level": item["level"],
                       "claim_sha256": claim_sha})
    for entry_id in ("E104", "E105", "E106", "E107", "E108"):
        require(found[entry_id]["level"] == "L3", f"ledger level {entry_id}")
    require(found["E109"]["level"] == "L2", "E109 level")
    return found, guards


def check_inputs(baseline: dict[str, Any], sources: dict[str, dict[str, Any]],
                 entries: dict[str, dict[str, Any]]) -> None:
    club = sources["t63"]["field_map_r2"]
    require(club["scope"] == "club.xml#club r1 unmapped only" and club["reviewed"] == 399 and
            club["grade_counts"] == {"L3": 8, "held": 41, "unmapped": 350} and
            club["new_L3"] == NEW_CLUB_L3 and club["L4"] == 0, "t63 r2 census")
    require(len(club["fields"]) == 399 and dict(Counter(row["grade"] for row in club["fields"])) ==
            club["grade_counts"], "t63 full occurrence grade counts")
    casp = next(row for row in club["fields"] if row.get("code") == "Casp")
    require(casp["grade"] == "held" and casp["first_counterexample"] == {
        "row": 78210, "absolute": 15571299, "raw": "3b79a747", "value": 85746.4609375,
        "reason": "outside frozen XML min/max in local getter units",
    }, "Casp counterexample")
    require(sources["t63"]["projections"]["date_relationship_control"]["server"]["appeal_not_before_start"] == 4,
            "t63 date negative preserved")

    comp = sources["t64"]["field_map_r2"]
    require(comp["status"] == "t64_evidence_increment" and len(comp["fields"]) == 196 and
            comp["summary"]["new_L3"] == 0 and comp["summary"]["reviewed_unmapped_occurrences"] == 196,
            "t64 round-2 scope/result")
    classes = dict(Counter(row["classification"] for row in comp["fields"]))
    require(classes == T64_EXCLUSIONS and sum(classes.values()) == 196, "t64 exclusion categories")
    accounting = sources["t64"]["helpers"]["main_reader"]["direct_stream_call_accounting"]
    require((accounting["direct_call_count"], accounting["outer_observed_call_count"],
             accounting["alternate_call_count"]) == (55, 52, 3), "t64 stream call accounting")
    require(sources["t64"]["helpers"]["main_reader"]["scope_extent"] == [15429632, 15433282],
            "t64 reader boundary")
    conditions = sources["t64"]["helpers"]["main_reader"]["payload_entry_conditions"]
    for name in ("a8", "e0"):
        sample = conditions[name]["data"]
        require(sample["client"] == {"presence_events": 0, "presence_nonzero": 0,
                                     "presence_values": {}, "object_events": 0} and
                sample["server"] == {"presence_events": 7047, "presence_nonzero": 0,
                                     "presence_values": {"0": 7047}, "object_events": 0},
                f"t64 static-zero counterexample {name}")

    nation = sources["t65"]["field_map_r2"]
    require(nation["scope"] == "frozen nation.xml#nation top-level occurrences only; delta, not a replacement for E94" and
            len(nation["fields"]) == 346 and nation["round2_of_327"] == {"unmapped": 318, "held": 9} and
            nation["new_L3"] == 0 and nation["L4"] == 0, "t65 round-2 census")
    r2_held = [row for row in nation["fields"] if row.get("grade") == "held" and row.get("status") != "unchanged_e94"]
    r2_unmapped = [row for row in nation["fields"] if row.get("grade") == "unmapped"]
    require(len(r2_held) == 9 and len(r2_unmapped) == 318, "t65 source-grade held/unmapped")
    require(next(row for row in r2_held if row["code"] == "rdui")["status"] ==
            "same_member_wire_but_getter_suppressed", "t65 rdui identity suppression")

    collections = sources["t66"]["collections"]
    census = sources["t66"]["census"]
    require(collections["status"] == "partial" and collections["L4"] == 0 and
            collections["L3_grammars"] == 7 and collections["L3_reference_lanes"] == 4,
            "t66 grammar/reference-lane census")
    expected_nonempty = {"vec18": 32, "+0xe8": 149, "+0xc0": 315, "+0xc8": 366,
                         "+0xd0": 121, "+0xd8": 51, "+0x100": 129}
    for slot, expected in expected_nonempty.items():
        require(len(collections["collections"][slot]["sides"]["server"]["nonempty_ordinals"]) == expected,
                f"t66 corrected nonempty count {slot}")
    require("exactly 4" in collections["collections"]["+0xc8"]["grammar"],
            "t66 +0xc8 fixed-call grammar")
    require(census["identity_width"] == 12 and census["header_width"] == 13 and census["footer_width"] == 9 and
            census["envelopes"]["client"]["payload"] == 894991 and
            census["envelopes"]["server"]["payload"] == 1533972, "t66 parent closure")
    grammar_slots = [slot for slot, item in collections["collections"].items() if item["grade"] == "L3"]
    held_slots = [slot for slot, item in collections["collections"].items() if item["grade"] == "held"]
    require(grammar_slots == ["vec18", "+0xe8", "+0xc0", "+0xc8", "+0xd0", "+0xd8", "+0x100"] and
            held_slots == ["vec30", "+0xa8", "+0xe0"], "t66 exact physical grammar/held slots")
    required_lane_rows = {"vec18": ["item.+1"], "+0xe8": ["item.+2"], "+0xc0": ["inner.+4", "inner.+8"],
                          "+0xd0": ["item.+0", "item.+4"], "+0xd8": ["item.+0", "item.+4"]}
    require({slot: list(collections["collections"][slot]["reference_lanes"]) for slot in required_lane_rows} ==
            required_lane_rows, "t66 reference lane inventory")

    xref = sources["t62"]["xref"]
    edsc = xref["key_routes"]["EDsc"]
    base = edsc["table"]
    require((edsc["input"], edsc["entries"], edsc["index"], edsc["cell"], edsc["rel32"],
             base + edsc["rel32"], edsc["entry"], edsc["same_target_indices"]) ==
            (1162113891, 68, 50, 174264, -5223, 168841, 168841, [50]), "t62 EDsc table cell")
    edfx_literals = xref["literal"]["EDfx"]["ascii_reverse"]
    require(len(edfx_literals) == 1 and edfx_literals[0]["offset"] == 0x29c39,
            "t62 EDfx literal boundary")
    conclusions = sources["t62"]["chain"]["conclusions"]
    require(conclusions["EDfx"]["status"] == "upstream_persistence_unbound" and
            conclusions["EDsc"]["status"] == "ui_consumers_found_no_main_wire_slot_inferred_from_this_dispatch",
            "t62 bounded conclusions")
    require(len(sources["t62"]["exclusions"]["excludes"]) == 7, "t62 exclusions retained")

    tail = sources["t69"]["tail_ledger"]
    require(tail["count"] == 18 and tail["unresolved_club"] == [] and tail["L4"] == 0 and
            tail["totals"] == {"club": {"skipped": 10}, "nation": {"held": 4},
                               "comp": {"static-zero": 3, "edge-pending": 1}}, "t69 closure")
    require(len(tail["entries"]) == 18, "t69 entry count")
    require(baseline["schema_version"] == 9 and baseline["generated_by"] == "t60",
            "protected v9 source")
    for entry_id in ("E104", "E105", "E106", "E107", "E108", "E109"):
        require(entries[entry_id]["kind"] == "acceptance", f"accepted task guard {entry_id}")


def task_provenance(task: str, entry_id: str, entries: dict[str, dict[str, Any]],
                    artifacts: dict[str, list[dict[str, Any]]], level: str,
                    metrics: dict[str, Any]) -> dict[str, Any]:
    entry = entries[entry_id]
    return {
        "status": "accepted_evidence_increment",
        "acceptance_ledger_entry": entry_id,
        "acceptance_ledger_level": level,
        "ledger_claim_sha256": canonical_sha256(entry["claim"]),
        "accepted_claim": copy.deepcopy(entry["claim"]),
        "evidence_level": copy.deepcopy(metrics),
        "source_artifacts": copy.deepcopy(artifacts[task]),
    }


def build_sections(inputs: dict[str, Any]) -> dict[str, Any]:
    baseline = inputs["baseline"]
    src = inputs["sources"]
    artifacts = inputs["artifacts"]
    documents = inputs["documents"]
    entries = inputs["ledger_entries"]
    club_map = src["t63"]["field_map_r2"]
    club_fields = club_map["fields"]
    club = {
        "source_task": "t63",
        "acceptance_ledger_entry": "E106",
        "acceptance_ledger_level": "L3",
        "status": "partial_evidence_increment",
        "scope": club_map["scope"],
        "round2_reviewed": club_map["reviewed"],
        "round2_grade_counts": copy.deepcopy(club_map["grade_counts"]),
        "new_L3": copy.deepcopy(club_map["new_L3"]),
        "new_L3_records": copy.deepcopy([row for row in club_fields if row.get("code") in NEW_CLUB_L3]),
        "held_records": copy.deepcopy([row for row in club_fields if row.get("grade") == "held"]),
        "unmapped_records": copy.deepcopy([row for row in club_fields if row.get("grade") == "unmapped"]),
        "projection_scope": "server-mode CLUB+0x150 tag-0 local getter projections; not new outer sites",
        "casp_counterexample": copy.deepcopy(next(row["first_counterexample"] for row in club_fields
                                                     if row.get("code") == "Casp")),
        "prior_round_preserved": {"L3": 13, "held": 11, "skipped_separate_member": 10, "unmapped": 399},
        "cumulative_L3": 21,
        "L4": 0,
        "source_artifacts": copy.deepcopy(artifacts["t63"]),
        "source_documents": copy.deepcopy(documents["t63"]),
        "source_records": {"field_map_r2": copy.deepcopy(club_map),
                           "projections": copy.deepcopy(src["t63"]["projections"])},
    }

    comp_map = src["t64"]["field_map_r2"]
    comp = {
        "source_task": "t64",
        "acceptance_ledger_entry": "E107",
        "acceptance_ledger_level": "L3",
        "status": "negative_evidence_increment",
        "scope": comp_map["scope"],
        "round2_reviewed": comp_map["summary"]["reviewed_unmapped_occurrences"],
        "new_L3": 0,
        "round2_classification_counts": copy.deepcopy(T64_EXCLUSIONS),
        "baseline_frozen": {"L3": 49, "held": 10, "unmapped": 196, "order_inversions": 818},
        "stream_call_accounting": {"direct": 55, "outer": 52, "tag4_alternates": 3,
                                   "alternate_sites": ["0xeb7218", "0xeb72f8", "0xeb7332"],
                                   "additional_outer_marker": "wbcl_present @0xeb7c8f"},
        "candidate_not_promoted": ["WpBn"],
        "static_zero_predicates": ["+0xa8", "+0xe0"],
        "static_zero_samples": {name: copy.deepcopy(src["t64"]["helpers"]["main_reader"]["payload_entry_conditions"][key]["data"])
                                for key, name in (("a8", "+0xa8"), ("e0", "+0xe0"))},
        "L4": 0,
        "source_artifacts": copy.deepcopy(artifacts["t64"]),
        "source_documents": copy.deepcopy(documents["t64"]),
        "source_records": {"field_map_r2": copy.deepcopy(comp_map),
                           "helpers": copy.deepcopy(src["t64"]["helpers"]),
                           "exclusions": copy.deepcopy(src["t64"]["exclusions"])},
    }

    nation_map = src["t65"]["field_map_r2"]
    nation_fields = nation_map["fields"]
    nation_held = [row for row in nation_fields if row.get("grade") == "held" and
                   row.get("status") != "unchanged_e94"]
    nation = {
        "source_task": "t65",
        "acceptance_ledger_entry": "E108",
        "acceptance_ledger_level": "L3",
        "status": "negative_evidence_increment",
        "scope": nation_map["scope"],
        "round2_reviewed": 327,
        "new_L3": 0,
        "round2_grade_counts": {"held": 9, "unmapped": 318},
        "held_records": copy.deepcopy(nation_held),
        "unmapped_records": copy.deepcopy([row for row in nation_fields if row.get("grade") == "unmapped"]),
        "dual_archive_closure": {"client": "13+24710+9=24732", "server": "13+422323+9=422345",
                                  "identity_width": 12, "footer_hex": "00000000|01|ec7ae404"},
        "L4": 0,
        "source_artifacts": copy.deepcopy(artifacts["t65"]),
        "source_documents": copy.deepcopy(documents["t65"]),
        "source_records": {"field_map_r2": copy.deepcopy(nation_map),
                           "projections": copy.deepcopy(src["t65"]["projections"])},
    }

    collections = src["t66"]["collections"]
    comp_collections = {
        "source_task": "t66",
        "acceptance_ledger_entry": "E104",
        "acceptance_ledger_level": "L3",
        "status": "partial_physical_grammar_and_reference_lanes",
        "scope": collections["scope"],
        "L3_physical_grammars": 7,
        "L3_reference_lanes": 4,
        "held_reference_lanes": 4,
        "L3_grammar_slots": ["vec18", "+0xe8", "+0xc0", "+0xc8", "+0xd0", "+0xd8", "+0x100"],
        "L3_reference_lane_bindings": [
            {"slot": "vec18", "lane": "item.+1", "target_table": 24},
            {"slot": "+0xd0", "lane": "item.+0", "target_table": 23},
            {"slot": "+0xd8", "lane": "item.+0", "target_table": 23},
            {"slot": "+0xd8", "lane": "item.+4", "target_table": 23},
        ],
        "held_reference_lane_records": [
            {"slot": "+0xe8", "lane": "item.+2", "reason": "6597/6597 all-ones; no live target"},
            {"slot": "+0xc0", "lane": "inner.+4", "reason": "t10 ordinal miss; multiple other domains match"},
            {"slot": "+0xc0", "lane": "inner.+8", "reason": "t10 ordinal miss; multiple other domains match"},
            {"slot": "+0xd0", "lane": "item.+4", "reason": "no live values; first @842 is ffffffff"},
        ],
        "held_slots": ["vec30", "+0xa8", "+0xe0"],
        "corrected_nonempty_rows": {"+0xc0": 315, "+0xc8": 366, "+0xd0": 121, "+0xd8": 51},
        "independent_member_bindings": 0,
        "L4": 0,
        "source_artifacts": copy.deepcopy(artifacts["t66"]),
        "source_documents": copy.deepcopy(documents["t66"]),
        "source_records": {"collections": copy.deepcopy(collections),
                           "census": copy.deepcopy(src["t66"]["census"])},
    }

    xref = src["t62"]["xref"]
    edsc = xref["key_routes"]["EDsc"]
    edfx_edsc = {
        "source_task": "t62",
        "acceptance_ledger_entry": "E105",
        "acceptance_ledger_level": "L3",
        "status": "partial_edsc_dispatch_closed_edfx_upstream_open",
        "edsc_dispatch": {"key": "0x45447363", "normalized_index": "0x32", "table_base": "0x2a7f0",
                          "cell": "0x2a8b8", "cell_bytes": "99ebffff", "rel32": -5223,
                          "target": "0x29389", "unique_target_index": True,
                          "consumer_types": {"COMP": 25, "NATION": 10},
                          "persisted_field": False},
        "edfx": {"literal_file_offset": "0x29c39", "upstream_persistence_bound": False,
                 "reader": None, "writer": None, "member": None, "bounded_exclusions": 7},
        "original_t55_grade_preserved": "held",
        "L4": 0,
        "source_artifacts": copy.deepcopy(artifacts["t62"]),
        "source_documents": copy.deepcopy(documents["t62"]),
        "source_records": {"chain": copy.deepcopy(src["t62"]["chain"]),
                           "xref": copy.deepcopy(xref),
                           "exclusions": copy.deepcopy(src["t62"]["exclusions"])},
    }

    tail_source = src["t69"]["tail_ledger"]
    tail = {
        "source_task": "t69",
        "acceptance_ledger_entry": "E109",
        "acceptance_ledger_level": "L2",
        "status": "closed_accounting_ledger",
        "items": tail_source["count"],
        "totals": copy.deepcopy(tail_source["totals"]),
        "unresolved_club": copy.deepcopy(tail_source["unresolved_club"]),
        "new_L3": 0,
        "L4": 0,
        "source_artifacts": copy.deepcopy(artifacts["t69"]),
        "source_documents": copy.deepcopy(documents["t69"]),
        "source_records": {"tail_ledger": copy.deepcopy(tail_source)},
    }
    return {
        "club_main_row_fields_r2": club,
        "comp_main_row_fields_r2": comp,
        "nation_main_row_fields_r2": nation,
        "comp_collections": comp_collections,
        "edfx_edsc_dispatch": edfx_edsc,
        "tail_ledger": tail,
    }


def extend_schema(inputs: dict[str, Any]) -> dict[str, Any]:
    baseline = inputs["baseline"]
    schema = copy.deepcopy(baseline)
    schema["schema_version"] = 10
    schema["generated_by"] = "t70"
    sections = build_sections(inputs)
    schema.update(copy.deepcopy(sections))

    coverage = schema["coverage"]
    coverage.update({
        "club_main_row_L3": 21,
        "club_main_row_new_L3": 8,
        "club_main_row_held": 41,
        "club_main_row_unmapped": 350,
        "club_main_row_occurrences": 433,
        "club_main_row_skipped_separate_member": 10,
        "club_main_row_r1_L3": 13,
        "club_main_row_r1_held": 11,
        "club_main_row_r1_skipped_separate_member": 10,
        "club_main_row_r1_unmapped": 399,
        "club_main_row_r1_new_L3": 5,
        "club_main_row_r2_reviewed": 399,
        "club_main_row_r2_new_L3": 8,
        "club_main_row_r2_held": 41,
        "club_main_row_r2_unmapped": 350,
        "comp_main_row_r2_reviewed": 196,
        "comp_main_row_r2_new_L3": 0,
        "nation_main_row_r2_reviewed": 327,
        "nation_main_row_r2_new_L3": 0,
        "nation_main_row_r2_held": 9,
        "nation_main_row_r2_unmapped": 318,
        "comp_collections_L3_physical_grammars": 7,
        "comp_collections_L3_reference_lanes": 4,
        "comp_collections_held_reference_lanes": 4,
        "comp_collections_independent_member_bindings": 0,
        "edsc_dispatch_closed": 1,
        "edfx_upstream_persistence_bound": 0,
        "tail_ledger_items": 18,
        "tail_ledger_unresolved_club": 0,
    })

    provenance = schema["incremental_provenance"]
    old_ledger_rows = provenance.setdefault("acceptance_ledger_entries", {})
    for entry_id, old_row in old_ledger_rows.items():
        if entry_id in inputs["ledger_entries"]:
            current_row = ledger_record(inputs["ledger_entries"][entry_id])
            require(all(old_row.get(key) == current_row.get(key)
                        for key in ("kind", "level", "claim_sha256")),
                    f"live ledger differs from pinned v9 row: {entry_id}")
    ledger_rows = old_ledger_rows
    for entry_id in GUARDED_IDS:
        row = ledger_record(inputs["ledger_entries"][entry_id])
        if entry_id not in ledger_rows:
            ledger_rows[entry_id] = row
    tasks = provenance.setdefault("tasks", {})
    task_specs = {
        "t62": ("E105", "L3", {"EDsc_dispatch_closed": 1, "EDfx_upstream_closed": 0, "L4": 0}),
        "t63": ("E106", "L3", {"new_L3": 8, "held": 41, "unmapped": 350, "L4": 0}),
        "t64": ("E107", "L3", {"new_L3": 0, "reviewed": 196, "L4": 0}),
        "t65": ("E108", "L3", {"new_L3": 0, "held": 9, "unmapped": 318, "L4": 0}),
        "t66": ("E104", "L3", {"physical_grammars": 7, "reference_lanes": 4, "L4": 0}),
        "t69": ("E109", "L2", {"items": 18, "unresolved_club": 0, "L4": 0}),
    }
    for task, (entry_id, level, metrics) in task_specs.items():
        require(task not in tasks, f"task already exists in baseline provenance: {task}")
        tasks[task] = task_provenance(task, entry_id, inputs["ledger_entries"], inputs["artifacts"], level, metrics)
    provenance["t70_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level id, kind, level, and canonical claim SHA-256; no live full-file hash or byte-count pin",
        "guarded_entries": list(GUARDED_IDS),
        "entries": copy.deepcopy(inputs["ledger_guards"]),
        "v9_baseline_acceptance_entry": "E100",
        "v9_baseline_acceptance_level": "L3",
        "v9_baseline_files": {
            "json": {"path": "scratch/t70/out/club_nation_subtable_schema.v9.json",
                     "sha256": BASE_JSON_SHA256, "bytes": len(inputs["baseline_json_raw"])},
            "markdown": {"path": "scratch/t70/out/club_nation_subtable_schema.v9.md",
                         "sha256": BASE_MD_SHA256, "bytes": len(inputs["baseline_md_raw"])},
        },
        "merged_tasks": {task: entry for task, (entry, _, _) in task_specs.items()},
    }
    return schema


def check_protected(baseline: dict[str, Any], updated: dict[str, Any]) -> None:
    protected = {"tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "club_main_row_fields"}
    protected.update(key for key in baseline if key.startswith("nation_"))
    for key in protected:
        require(updated.get(key) == baseline.get(key), f"protected JSON section changed: {key}")
    require(set(updated) == set(baseline) | set(sections_root_keys()), "schema root keys outside additive v10 sections")
    mutable = {"schema_version", "generated_by", "coverage", "incremental_provenance"}
    for key, value in baseline.items():
        if key not in mutable:
            require(updated.get(key) == value, f"unrequested root data changed: {key}")
    changed_coverage = {"club_main_row_L3", "club_main_row_new_L3", "club_main_row_held", "club_main_row_unmapped"}
    for key, value in baseline["coverage"].items():
        if key not in changed_coverage:
            require(updated["coverage"].get(key) == value, f"pre-existing coverage changed: {key}")
    old_prov, new_prov = baseline["incremental_provenance"], updated["incremental_provenance"]
    for key, value in old_prov.items():
        if key not in {"acceptance_ledger_entries", "tasks"}:
            require(new_prov.get(key) == value, f"pre-existing provenance changed: {key}")
    for key, value in old_prov["tasks"].items():
        require(new_prov["tasks"].get(key) == value, f"pre-existing task changed: {key}")
    for key, value in old_prov["acceptance_ledger_entries"].items():
        require(new_prov["acceptance_ledger_entries"].get(key) == value,
                f"pre-existing ledger record changed: {key}")


def sections_root_keys() -> tuple[str, ...]:
    return ("club_main_row_fields_r2", "comp_main_row_fields_r2", "nation_main_row_fields_r2",
            "comp_collections", "edfx_edsc_dispatch", "tail_ledger")


def markdown_appendix(schema: dict[str, Any], inputs: dict[str, Any]) -> str:
    c = schema["coverage"]
    club = schema["club_main_row_fields_r2"]
    comp = schema["comp_main_row_fields_r2"]
    nation = schema["nation_main_row_fields_r2"]
    coll = schema["comp_collections"]
    ed = schema["edfx_edsc_dispatch"]
    tail = schema["tail_ledger"]
    ids = ", ".join(f"`{name}`" for name in club["new_L3"])
    lines = [
        "", "", "## t70 — accepted evidence increment (E104–E109)", "",
        "This is an additive appendix to the byte-pinned v9 Markdown. Existing schema sections, including held/unmapped records, remain unchanged; round-2 source records are embedded in v10 JSON.", "",
        "### Club `table_3` round 2 (t63 / E106)", "",
        f"- Re-reviewed 399 prior unmapped occurrences: 8 new L3 ({ids}), 41 held, 350 unmapped; L4=0. The cumulative club main-row L3 count is {c['club_main_row_L3']}; the frozen v9 `club_main_row_fields` object remains verbatim.",
        "- These are server-mode `CLUB+0x150` tag-0 getter projections, not new outer sites. Held reasons and all 350 unmapped source records remain embedded unchanged.",
        "- Counterexample retained: Casp server row 78,210 @15,571,299, bytes `3b79a747` = 85,746.4609375, outside the frozen XML 0–10,000 domain. The `date_relationship_control` negative remains in source records.", "",
        "### COMP `table_25` round 2 (t64 / E107)", "",
        "- 196/196 reviewed; new L3=0. E99's 49 L3, 10 held and 818 inversions are unchanged. WpBn remains candidate-only.",
        "- Corrected accounting: 55 direct `stream+0x28` calls = 52 outer + 3 tag-4 alternates; the extra outer marker is `wbcl_present` @0xeb7c8f. The +0xa8/+0xe0 presence-gated static paths and zero-data counterexamples are retained without asserting non-existence.", "",
        "### Nation `table_10` round 2 (t65 / E108)", "",
        "- 327 reviewed: 9 moved to held, 318 remain unmapped, new L3=0. The 9 held objects are embedded as source-identical records; `rdui` remains identity-lane suppression, not a usable reference.",
        "- Dual archive closure remains client `13+24710+9=24732`, server `13+422323+9=422345`; identity 12 B, footer `ec7ae404`.", "",
        "### COMP inline collections (t66 / E104)", "",
        "- Seven non-empty physical grammars and four reference lanes are L3. `vec18:item+1` targets t24; `+0xd0:item+0` and `+0xd8:item+0/+4` target t23. No independent COMP member is bound.",
        "- Corrected present/nonempty rows for +0xc0/+0xc8/+0xd0/+0xd8 are **315/366/121/51**. `+0xc8` is fixed-call grammar, not a count. `vec30`, +0xa8 and +0xe0 remain held; +0x100 remains physical grammar only.", "",
        "### EDfx / EDsc (t62 / E105)", "",
        "- EDsc dispatch is closed: normalized index `0x32`, cell `0x2a8b8`, rel32 target `0x29389`, unique among 68 cells. It dispatches UI consumers for COMP/NATION; it is not a persisted field and the original held grade remains.",
        "- EDfx upstream persistence remains unbound: no reader, writer or member assigned. Seven bounded exclusions and reopen conditions are preserved.", "",
        "### Tail ledger (t69 / E109)", "",
        f"- {tail['items']} items reconciled: club skipped 10, nation held 4, COMP static-zero 3 and edge-pending 1. `unresolved_club=[]`; no prior grade changes.", "",
        "### Provenance and boundaries", "",
        "- Ledger guards cover E84–E109 by entry id, kind, level and canonical claim SHA-256. t70 records source SHA-256/byte counts and embeds each accepted JSON plus its full report/DONE text (and t69 SUMMARY).",
        "- Coverage records round-2 counts separately for COMP/nation/collections/tail; the protected v9 tables, regressions, v3 baseline, club auxiliary sources, club main-row section and all existing nation sections are unchanged.",
        "- No work was performed in t47–t69, and `docs/BASELINE.md` was not modified.",
        "",
    ]
    return "\n".join(lines)


def report_text(schema: dict[str, Any], json_raw: bytes, md_raw: bytes) -> str:
    c = schema["coverage"]
    return (
        "# t70 — public club/nation schema v9→v10\n\n"
        f"- v9 snapshot: JSON SHA-256 `{BASE_JSON_SHA256}`; Markdown SHA-256 `{BASE_MD_SHA256}`. v10 Markdown preserves the full v9 bytes as prefix.\n"
        "- Additive sections: `club_main_row_fields_r2`, `comp_main_row_fields_r2`, `nation_main_row_fields_r2`, `comp_collections`, `edfx_edsc_dispatch`, `tail_ledger`.\n"
        f"- Club round 2: {c['club_main_row_new_L3']} new L3; coverage cumulative club main-row L3={c['club_main_row_L3']}; {c['club_main_row_held']} held and {c['club_main_row_unmapped']} unmapped in this round. R1 and R2 counts are separately labeled in coverage.\n"
        f"- COMP round 2: {c['comp_main_row_r2_reviewed']} reviewed, {c['comp_main_row_r2_new_L3']} new L3; baseline 49/10/196 and 818 inversions unchanged. Nation round 2: {c['nation_main_row_r2_reviewed']} reviewed, 9 held, 318 unmapped, 0 new L3.\n"
        "- Collections: 7 physical grammars and 4 reference lanes at L3; corrected nonempty row counts 315/366/121/51. EDsc dispatch closed, EDfx upstream open. Tail ledger 18/18, unresolved club skips 0.\n"
        "- All accepted task JSON records plus REPORT/DONE documents (and t69 SUMMARY) are embedded; source SHA-256 and byte counts are pinned.\n"
        "- Protected sections and old provenance/task records are value-identical to v9. Ledger claim guards span E84–E109. L4=0.\n"
        "- Builder/verifier `--help`, `--selftest`, `--check`, exit-code 1/2 probes passed; t01 anchors 7/7. Logs are in `scratch/t70/out/spot_*.log`.\n"
        f"- v10 JSON SHA-256 `{sha(json_raw)}` ({len(json_raw)} bytes); Markdown SHA-256 `{sha(md_raw)}` ({len(md_raw)} bytes).\n"
    )


def done_text(schema: dict[str, Any], json_raw: bytes, md_raw: bytes) -> str:
    c = schema["coverage"]
    return (
        "# t70 DONE — schema v10\n\n"
        "- Public schema advanced additively from v9 to v10; exact v9 JSON/Markdown snapshots are stored in `scratch/t70/out/`.\n"
        f"- Club r2: {c['club_main_row_new_L3']} new L3, {c['club_main_row_held']} held, {c['club_main_row_unmapped']} unmapped; cumulative main-row L3={c['club_main_row_L3']}. Casp's 85,746.4609375 counterexample remains held.\n"
        "- COMP r2: 0 new L3; E99's 49 L3/10 held/818 inversions unchanged. Nation r2: 0 new L3, 9 held, 318 unmapped.\n"
        "- COMP collections: 7 physical grammars, 4 reference lanes; EDsc dispatch closed without a persisted-field promotion; EDfx persistence open. Tail ledger: 18 items, no unresolved club skips.\n"
        "- Accepted JSON records/reports are embedded with pinned source hashes; round-1 and round-2 club counts have separate coverage keys.\n"
        "- Held/unmapped source records, the original EDsc held grade, static-zero caveats, and t69 tail entries are retained; no t47–t69 files or `docs/BASELINE.md` were changed.\n"
        "- Protected v9 sections are verbatim; E84–E109 ledger guards, source manifests and independent verification pass. Help/selftests/checks and exit-code probes pass; anchors 7/7; L4=0.\n"
        f"- v10 JSON SHA-256 `{sha(json_raw)}`; Markdown SHA-256 `{sha(md_raw)}`.\n"
    )


def load_inputs() -> dict[str, Any]:
    baseline, baseline_json_raw, baseline_md_raw = load_baseline()
    sources, artifacts, documents = load_sources()
    ledger_entries, ledger_guards = load_ledger()
    check_inputs(baseline, sources, ledger_entries)
    return {"baseline": baseline, "baseline_json_raw": baseline_json_raw, "baseline_md_raw": baseline_md_raw,
            "sources": sources, "artifacts": artifacts, "documents": documents,
            "ledger_entries": ledger_entries, "ledger_guards": ledger_guards}


def selftest() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["baseline"], schema)
    require(schema["club_main_row_fields_r2"]["new_L3"] == NEW_CLUB_L3 and
            len(schema["club_main_row_fields_r2"]["held_records"]) == 41 and
            len(schema["club_main_row_fields_r2"]["unmapped_records"]) == 350,
            "club source records")
    require(schema["comp_main_row_fields_r2"]["round2_reviewed"] == 196 and
            schema["comp_main_row_fields_r2"]["new_L3"] == 0 and
            len(schema["nation_main_row_fields_r2"]["held_records"]) == 9 and
            len(schema["nation_main_row_fields_r2"]["unmapped_records"]) == 318,
            "COMP/nation round-2 records")
    require(schema["comp_collections"]["L3_physical_grammars"] == 7 and
            schema["edfx_edsc_dispatch"]["edsc_dispatch"]["target"] == "0x29389" and
            schema["tail_ledger"]["items"] == 18, "collections/dispatch/tail")
    require(markdown_appendix(schema, inputs).startswith("\n\n## t70"), "Markdown appendix heading")
    print("t70 builder selftest PASS: v9 baseline, t62-t69 sources, E84-E109, protected sections and round-2 records")


def build() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["baseline"], schema)
    json_raw = json_bytes(schema)
    md_raw = inputs["baseline_md_raw"] + markdown_appendix(schema, inputs).encode("utf-8")
    current_json, current_md = PUBLIC_JSON.read_bytes(), PUBLIC_MD.read_bytes()
    allowed = {(BASE_JSON_SHA256, BASE_MD_SHA256), (sha(json_raw), sha(md_raw))}
    require((sha(current_json), sha(current_md)) in allowed,
            "public schema is neither pinned v9 baseline nor this deterministic v10 build")
    if V9_JSON.exists():
        require(V9_JSON.read_bytes() == inputs["baseline_json_raw"], "existing v9 JSON snapshot differs")
    else:
        V9_JSON.write_bytes(inputs["baseline_json_raw"])
    if V9_MD.exists():
        require(V9_MD.read_bytes() == inputs["baseline_md_raw"], "existing v9 Markdown snapshot differs")
    else:
        V9_MD.write_bytes(inputs["baseline_md_raw"])
    PUBLIC_JSON.write_bytes(json_raw)
    PUBLIC_MD.write_bytes(md_raw)
    V10_JSON.write_bytes(json_raw)
    V10_MD.write_bytes(md_raw)
    (OUT / "REPORT.md").write_text(report_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    (OUT / "DONE.md").write_text(done_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    print("t70 build PASS: schema v10; club 8 new L3; COMP/nation round-2 new L3=0; L4=0")
    print(f"JSON {sha(json_raw)} ({len(json_raw)} bytes)")
    print(f"Markdown {sha(md_raw)} ({len(md_raw)} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--build", action="store_true", help="build public v10 pair (default)")
    group.add_argument("--selftest", action="store_true", help="run read-only consolidation checks")
    args = parser.parse_args()
    try:
        selftest() if args.selftest else build()
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
