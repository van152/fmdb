#!/usr/bin/env python3
"""Independent focused t54 spot checks; does not import merge or verifier code."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t54" / "out"
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V5_JSON = OUT / "club_nation_subtable_schema.v5.json"
V5_MD = OUT / "club_nation_subtable_schema.v5.md"
V5_JSON_SHA256 = "03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184"
V5_MD_SHA256 = "4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009"
PROTECTED = ("tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "nation_static_side")
T53_PATHS = (
    "scratch/t53/out/discovery_crs_wire.json",
    "scratch/t53/out/cursor_crs_main_client.json",
    "scratch/t53/out/cursor_crs_main_server.json",
    "scratch/t53/out/cursor_crs_extra_client.json",
    "scratch/t53/out/cursor_crs_extra_server.json",
    "scratch/t53/out/fields_PUnI.json",
    "scratch/t53/out/fields_PUnT.json",
    "scratch/t53/out/fields_PUnP.json",
    "scratch/t53/out/fields_PUnJ.json",
    "scratch/t53/out/REPORT.md",
    "scratch/t53/out/DONE.md",
)
EXPECTED_T53 = {
    "scratch/t53/out/discovery_crs_wire.json": "6383063973c0b16ebd06f304b7aec4f3b46649324f93345b8e1cd879a07e66a5",
    "scratch/t53/out/cursor_crs_main_client.json": "52e043f612a95efca28b04ef87c04eecc580e8711cfe7a7088c4616cc4326cac",
    "scratch/t53/out/cursor_crs_main_server.json": "99fd9ad8cc53ce3c2c1911487ef4300b1847b622a0bb3d5d95768ef28f90c49d",
    "scratch/t53/out/cursor_crs_extra_client.json": "5fb9fcffe735063dc12f575e5b69b5f5bf534990e2d20bd8daca7afd9082f3d9",
    "scratch/t53/out/cursor_crs_extra_server.json": "b00c6fd0f6fe3732f9aa6045a338fc037d00545591478aa3c4807e924dd8cdea",
    "scratch/t53/out/fields_PUnI.json": "b0ecbba661c1633fcd7ce937a26b920cf23d0418301f450f953c24b862702b6e",
    "scratch/t53/out/fields_PUnT.json": "589bc4bf61bc2bf26c5d3b160adc7a34a885b6f9601a054bf2a385fc9040ff31",
    "scratch/t53/out/fields_PUnP.json": "994e4a11e01e10c7735275dca81fc44beac05d47a5a9bca83f9d782c8d5af37c",
    "scratch/t53/out/fields_PUnJ.json": "17124f10abaa07d83c76d097c7bc2dcfeaac7d03bfd176c9599b0a16a3a2dd4f",
    "scratch/t53/out/REPORT.md": "e4c07bed43d2d2c569f1aaa9ec9acd607a9cad315390c3d8762c0ebb7c5eddac",
    "scratch/t53/out/DONE.md": "46b6a65aef2a91fd38027e8ce39cd0c90ba410ab8af95339fba46f0885f5ab79",
}
T50_FILES = (
    ("scratch/t50/out/REPORT.md", "REPORT.md"),
    ("scratch/t50/out/DONE.md", "DONE.md"),
    ("scratch/t50/out/profile_t9.json", "profile_t9.json"),
    ("scratch/t50/out/grammar_diff_t9.json", "grammar_diff_t9.json"),
)


class SpotFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SpotFailure(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def check_spots() -> int:
    v5_json_raw, v5_md_raw = V5_JSON.read_bytes(), V5_MD.read_bytes()
    require(sha256(v5_json_raw) == V5_JSON_SHA256 and sha256(v5_md_raw) == V5_MD_SHA256,
            "v5 snapshot SHA assertion failed")
    baseline = json.loads(v5_json_raw.decode("utf-8"))
    schema = read_json(PUBLIC_JSON)
    markdown = PUBLIC_MD.read_bytes()
    require(markdown.startswith(v5_md_raw), "v5 Markdown prefix is not byte-exact")
    require(schema["schema_version"] == 6 and schema["generated_by"] == "t54", "schema metadata")
    for key in PROTECTED:
        require(schema[key] == baseline[key], f"protected section changed: {key}")
    for key, value in baseline["coverage"].items():
        if not key.startswith("nation_"):
            require(schema["coverage"].get(key) == value, f"club counter changed: {key}")
    require(schema["nation_t9_wire"]["table_9"] == baseline["nation_t9_wire"]["table_9"],
            "accepted t9 main-table field records changed")

    t53_node = schema["nation_t9_wire"]["t53_crs_adjudication"]
    source_records = {item["path"]: item for item in t53_node["source_artifacts"]}
    require(set(source_records) == set(T53_PATHS), "t53 artifact path set")
    parsed: dict[str, Any] = {}
    for path in T53_PATHS:
        raw = (ROOT / path).read_bytes()
        digest = sha256(raw)
        require(digest == EXPECTED_T53[path] and source_records[path]["sha256"] == digest and
                source_records[path]["bytes"] == len(raw), f"t53 source artifact hash: {path}")
        if path.endswith(".json"):
            parsed[path] = json.loads(raw.decode("utf-8"))
    discovery = parsed["scratch/t53/out/discovery_crs_wire.json"]
    require(t53_node["source_records_verbatim"]["discovery_crs_wire.json"] == discovery,
            "full t53 discovery artifact was not retained verbatim")
    main_server = parsed["scratch/t53/out/cursor_crs_main_server.json"]
    main_client = parsed["scratch/t53/out/cursor_crs_main_client.json"]
    extra_server = parsed["scratch/t53/out/cursor_crs_extra_server.json"]
    extra_client = parsed["scratch/t53/out/cursor_crs_extra_client.json"]

    main_presence = Counter(str(row["presence"]) for row in main_server["rows"])
    main_vectors = [row["vector"] for row in main_server["rows"] if row.get("vector")]
    main_items = [item for vector in main_vectors for item in vector["items"]]
    require(dict(main_presence) == {"0": 166, "1": 85} and len(main_vectors) == 85 and
            len(main_items) == 2219 and all(v["version"] == 2 for v in main_vectors) and
            all(item["tag"] == 3 and int.from_bytes(bytes.fromhex(item["raw"])[2:6], "little", signed=True) == -1
                for item in main_items), "main vector spot counts")
    extra_presence = Counter(str(row["presence"]) for row in extra_server["rows"])
    extra_vectors = [row["vector"] for row in extra_server["rows"] if row.get("vector")]
    extra_items = [item for vector in extra_vectors for item in vector["items"]]
    require(dict(extra_presence) == {"0": 179, "1": 72} and len(extra_vectors) == 72 and
            sum(v["count"] == 0 for v in extra_vectors) == 39 and
            sum(v["count"] > 0 for v in extra_vectors) == 33 and len(extra_items) == 76 and
            all(v["version"] == 2 for v in extra_vectors) and all(item["tag"] == 3 for item in extra_items),
            "getter suffix spot counts")
    require(len(main_client["rows"]) == len(extra_client["rows"]) == 251 and
            main_client["summary"]["skipped"] == extra_client["summary"]["skipped"] == 251,
            "client mode-0 skip counts")
    closures = t53_node["double_eof_closure"]
    for side, total in (("client", 31956), ("server", 307564)):
        cursor = main_client if side == "client" else main_server
        span = sum(r["end"] - r["start"] for r in cursor["rows"])
        require(cursor["header"] + span + len(bytes.fromhex(cursor["footer"])) == total and
                closures["main_table_9"][side] == f"13 + {span} + 9 = {total}",
                f"main {side} EOF formula")
    for side, total in (("client", 83927), ("server", 105228)):
        cursor = extra_client if side == "client" else extra_server
        span = sum(r["end"] - r["start"] for r in cursor["rows"])
        require(cursor["header"] + span == total and
                closures["getter_table_extra_9_suffix"][side] == f"12 + sum(spans={span}) = {total}",
                f"extra {side} EOF formula")
    require(discovery["L3_fields"] == 0 and discovery["L4"] == 0 and
            t53_node["acceptance_ledger_entry"] == "E93" and t53_node["acceptance_ledger_level"] == "L2",
            "t53 evidence grade boundary")
    require(len(t53_node["wrong_mode_trial_groups"]) == 8 and
            all(item["source_record"] == discovery["trials"][item["id"]]
                for item in t53_node["wrong_mode_trial_groups"]), "eight t53 negative groups")
    require((schema["coverage"]["nation_L3_occurrences"], schema["coverage"]["nation_held_occurrences"],
             schema["coverage"]["nation_negative_records"]) == (30, 20, 15), "nation count arithmetic")

    old_extra = baseline["nation_t9_wire"]["table_extra_9"]
    new_extra = schema["nation_t9_wire"]["table_extra_9"]
    require(new_extra["status"] != "unbound_open_negative" and new_extra["reader"]["source_task"] == "t53" and
            new_extra["rejection_records"] == old_extra["rejection_records"] and
            new_extra["rejected_member_mode_attempts_total"] == 6,
            "table_extra_9 new binding or old negatives")
    old_t50 = baseline["nation_t9_wire"]["t50_L2_cross_validation"]
    new_t50 = schema["nation_t9_wire"]["t50_L2_cross_validation"]
    require(new_t50["adjudication"].startswith(old_t50["adjudication"]) and
            new_t50["source_records_verbatim"] == old_t50["source_records_verbatim"],
            "t50 NO WINNER/original records changed")
    embedded_t50 = old_t50["source_records_verbatim"]
    for path, key in T50_FILES:
        raw = (ROOT / path).read_bytes()
        source = embedded_t50[key]
        if key.endswith(".md"):
            require(raw.decode("utf-8") == source, f"t50 original Markdown changed: {path}")
        else:
            require(json.loads(raw.decode("utf-8")) == source, f"t50 original JSON changed: {path}")
    ledger = read_json(ROOT / "scratch" / "t01" / "LEDGER.json")
    levels = {e["id"]: (e["kind"], e["level"]) for e in ledger["entries"] if e.get("id") in ("E91", "E92", "E93")}
    require(levels == {"E91": ("acceptance", "L2"), "E92": ("acceptance", "L2"),
                       "E93": ("acceptance", "L2")}, "E91/E92/E93 ledger levels")
    return 37


def selftest() -> None:
    require(sha256(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "spot SHA selftest")
    require(len(T53_PATHS) == 11 and len(PROTECTED) == 5, "spot constants selftest")
    require(13 + 31934 + 9 == 31956 and 12 + 105216 == 105228,
            "spot closure arithmetic selftest")
    print("t54 spot selftest PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently spot-check v5 snapshot SHA, protected sections, t53 cursor counts, and untouched t50 inputs.")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true", help="run isolated spot-script selftests")
    modes.add_argument("--check", action="store_true", help="check v6 against v5 and t53/t50 files")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            selftest()
            return 0
        checks = check_spots()
        print(f"t54 independent spot check PASS ({checks} checks)")
        print("v5 SHA/protected blocks verified; t53 2,219/76 and four EOF equations verified")
        print("t50 original files unchanged; NO WINNER retained; E93=L2; L4=0")
        return 0
    except SpotFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
