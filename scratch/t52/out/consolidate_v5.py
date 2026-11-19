#!/usr/bin/env python3
"""Incrementally merge t47/t49/t50/t51 nation evidence into schema v5."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V4_JSON = OUT_DIR / "club_nation_subtable_schema.v4.json"
V4_MD = OUT_DIR / "club_nation_subtable_schema.v4.md"
V4_JSON_SHA256 = "7567606c8082f53296caf9c07088489614c364d214e25ba3d4f6390e17d25932"
V4_MD_SHA256 = "ee47e88a4f7d82ecb996022dc7465975eff51bb153869f99adb987dc46ee3c0c"
EDITOR_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
LEDGER_SHA256 = "99e0161366c76e5ff1d924d6dd581b0aa1b37787b8021e02a5d29dafa089198d"
LEDGER_BYTES = 197568
PRIOR_V5_SHA256 = {
    "reports/club_nation_subtable_schema.json": "f30e1fcd4f18968a3c3ddef3bbab639a33ea295673716ea2d110416164f4fcc1",
    "reports/club_nation_subtable_schema.md": "1beaa653e08e00d8aa11a054aaf7907959710a856a7e41c413ba91e119f48747",
    "scratch/t52/out/REPORT.md": "d83475e992672cd782428caa734065a3dd7a616f2e898799c00299b8d78aa5b0",
    "scratch/t52/out/DONE.md": "357d8ff01cdaab31d6e560a67269358fb6519d7ceb66d2d173212e2e0b2fa952",
}

T47_DISCOVERY = "scratch/t47/out/discovery_nation_unknown.json"
T47_FIELDS = "scratch/t47/out/fields_nation_tax.json"
T47_CURSOR = "scratch/t47/out/cursor_nation_tax.json"
T47_REPORT = "scratch/t47/out/REPORT.md"
T49_DISCOVERY = "scratch/t49/out/discovery_t9_wire.json"
T49_REPORT = "scratch/t49/out/REPORT.md"
T49_FIELDS = [f"scratch/t49/out/fields_{name}.json" for name in
              ("Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Nfmp", "NCro")]
T49_CURSORS = ["scratch/t49/out/cursor_t9_client.json", "scratch/t49/out/cursor_t9_server.json"]
T50_REPORT = "scratch/t50/out/REPORT.md"
T50_PROFILE = "scratch/t50/out/profile_t9.json"
T50_DIFF = "scratch/t50/out/grammar_diff_t9.json"
T50_VERIFY = "scratch/t50/out/verify.py"
T50_DONE = "scratch/t50/out/DONE.md"
T50_BUILDER = "scripts/t50_nation_t9_profile.py"
T50_ACCEPTANCE_SPOT = "scratch/cmd/t50_spot.py"
T50_ROWS = [f"scratch/t50/out/profiles/table_{side}_{name}.rows.jsonl"
            for side in ("client", "server") for name in ("9", "extra_9")]
T51_DISCOVERY = "scratch/t51/out/discovery_unknown2.json"
T51_REPORT = "scratch/t51/out/REPORT.md"
T51_FIELDS = [f"scratch/t51/out/fields_{name}.json" for name in ("Nrvn", "Nftb", "Calt")]
T51_CURSORS = [
    "scratch/t51/out/cursor_table_9_client.json",
    "scratch/t51/out/cursor_table_9_server.json",
    "scratch/t51/out/cursor_table_10_server.json",
]
LEDGER = "scratch/t01/LEDGER.json"

EXPECTED_SOURCE_SHA256 = {
    T47_DISCOVERY: "2c0a5b535fd280c1c1c46825b5e1b8ea7206ff5d5be40d13c7ed8d241b05b5d3",
    T47_FIELDS: "b7b57595a3b8e4d60458f14f1e923b660e751304fdab1feff7c85b035a4af9b7",
    T47_CURSOR: "42b3e88db86c725221a23cd7b2bdd6e3d4c1b089d758ed844a56f84e103f2ea9",
    T47_REPORT: "c0742c66ad5ed0819b222983c046c1b7ec83db02fdcbe67bd7063ea0eab563f8",
    T49_DISCOVERY: "f3b9f06535bbdca2876f86caaf3f0c592969028281600b0e678c3912f6f50b9a",
    T49_REPORT: "0c0b1129c1edb5758d49403351950238383b5369d089097c9bfb8b0fe6d23974",
    "scratch/t49/out/cursor_t9_client.json": "82a733f8157b1518d38dadafcc33249a34fa3d563ec2a37c4d60740bf1f6b004",
    "scratch/t49/out/cursor_t9_server.json": "ccf78eba3d1d845b530550987b093b120ca20dd9e4a079da3970ca590259e69b",
    "scratch/t49/out/fields_NCro.json": "d3f1f0479587071389718005b12ce5820d0991ec7230db136f71d3efb1ada144",
    "scratch/t49/out/fields_NSps.json": "c4c420461c3de270d9168af06719d54b5885cffed540680629ff0ec588febbae",
    "scratch/t49/out/fields_NTRv.json": "c4afdc411be456f418dd854e407a491738d235d73777c78055fdff53c4c6c15a",
    "scratch/t49/out/fields_NWGv.json": "681db4ba1d42c480b86fa587cab1c8b459e8ea5e15890828e189061b6f5896ae",
    "scratch/t49/out/fields_Nctp.json": "75f983bfa703bdde1cab4b642404ea07f2251d806d6e67aa230d78331f682562",
    "scratch/t49/out/fields_Nfmp.json": "d1b8e84be431991682bb6a347b085a4c2d41241be757251a7234b656a42ecd14",
    "scratch/t49/out/fields_Nntp.json": "21a342822440328f3c9515d2208556306455262a486d3708d0d56771237de22a",
    "scratch/t49/out/fields_Nrtp.json": "d93a94262d035fe5e5f4938125b7879b9d5f80b8fad232fa1302dc6e5b9e5e22",
    T50_REPORT: "8994cc39ce7b67227f9f372c18ef997a173ade3e88ca583f6e4bb4870770b0ba",
    T50_PROFILE: "95a413310116af0b123128f7e819a47e94aa01556000fef0ab60bfc6d8c1fa06",
    T50_DIFF: "31f1fb7628d0f5d81acfea89e82b77f610942af188b20bc31bb9225148f81477",
    T50_VERIFY: "179b9c8fdacbff94c2ae6150ec7c08fdf48781c9c462d28b51c2e1617242486c",
    T50_DONE: "fae026b837e96e59645fbb3effdf3e59c1b1fd1532bb4a3e69545c40ab82f3f2",
    T50_BUILDER: "659de87f7799ee81242ac75f036068fd910c8fdcbf78ff231cdf438261de7b80",
    T50_ACCEPTANCE_SPOT: "aa5ee28b5421cdee0afc36079738cbd400288b1c8305a043ca75549da6efff16",
    "scratch/t50/out/profiles/table_client_9.rows.jsonl": "5c5d18c112813371e2b9fcee42046a481b7467337db3d21d0143ac539d6b0d1a",
    "scratch/t50/out/profiles/table_client_extra_9.rows.jsonl": "98817ff54bdfc6e4695ca415299a63f0e5985a0ddd039bbcee4e8dca4a583249",
    "scratch/t50/out/profiles/table_server_9.rows.jsonl": "2d8b7b92c350b287e1cc1525e1cb1f98899fda2881cd7c33e22d655902b031db",
    "scratch/t50/out/profiles/table_server_extra_9.rows.jsonl": "188c68e607b034caa0ce1283edd185780bbb0511b574e88810cd3d1caab09fd4",
    T51_DISCOVERY: "3b384f82cab9417a1bc41b0dfded0f15b96f79e354928c87235993045fe538f6",
    T51_REPORT: "3821c9a3e9da24a8e2c1fbd49929a4a425d5be39e9bcaa28dc594fb1bacc517b",
    "scratch/t51/out/cursor_table_9_client.json": "4f70c334ab30763e5ece062f493dfb9378d40ecd42d41aecdea3ce302b75a3e7",
    "scratch/t51/out/cursor_table_9_server.json": "6bff39851db865fec2fb18808ccfc3220bbbb367acc642a7328d459e26b0e670",
    "scratch/t51/out/cursor_table_10_server.json": "8236f250af16a120a23fb241755df9d66e7f741fcc6baf2c3cc8e1a61f61bf40",
    "scratch/t51/out/fields_Nrvn.json": "c663f14aed3a1cceccff3adfad55b7f0a23a15b63e3f58c0a8db0273e1191537",
    "scratch/t51/out/fields_Nftb.json": "69f83b15f3143e2305846967d36d6afc340b6626222527a04232fc90da1fa7b0",
    "scratch/t51/out/fields_Calt.json": "91a3ad1da9f738038660288071732c4e90f6590485c6e3def2ce40e5789e89d2",
    LEDGER: LEDGER_SHA256,
}

T9_PARENTS = ("Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Nfmp", "NCro")
T47_CONNECTED = ("Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Ntxr", "Nfmp", "NCro")
T47_UNKNOWN = ("Nftb", "EDfx", "EDsc", "Nrvn", "Calt", "TCrs")
T51_PARENT_ORDER = ("Nrvn", "Calt", "TCrs", "Nftb", "EDfx", "EDsc")


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def rel(path: str) -> Path:
    return ROOT / Path(path)


def read_json(path: str | Path) -> Any:
    target = path if isinstance(path, Path) else rel(path)
    return json.loads(target.read_text(encoding="utf-8"))


def read_jsonl(path: str) -> list[dict[str, Any]]:
    target = rel(path)
    return [json.loads(line) for line in target.read_text(encoding="ascii").splitlines() if line]


def artifact_record(path: str) -> dict[str, Any]:
    target = rel(path)
    require(target.is_file(), f"missing source artifact: {path}")
    raw = target.read_bytes()
    digest = sha256_bytes(raw)
    expected = EXPECTED_SOURCE_SHA256.get(path)
    if expected:
        require(digest == expected, f"source artifact SHA-256 changed: {path}")
    return {"path": path, "sha256": digest, "bytes": len(raw)}


def load_v4() -> tuple[dict[str, Any], bytes, str, bytes, bytes]:
    if V4_JSON.exists() or V4_MD.exists():
        require(V4_JSON.is_file() and V4_MD.is_file(), "both frozen v4 snapshots must exist together")
        json_raw, md_raw = V4_JSON.read_bytes(), V4_MD.read_bytes()
    else:
        require(PUBLIC_JSON.is_file() and PUBLIC_MD.is_file(), "public v4 baseline is missing")
        json_raw, md_raw = PUBLIC_JSON.read_bytes(), PUBLIC_MD.read_bytes()
    require(sha256_bytes(json_raw) == V4_JSON_SHA256, "v4 JSON baseline SHA-256 mismatch")
    require(sha256_bytes(md_raw) == V4_MD_SHA256, "v4 Markdown baseline SHA-256 mismatch")
    baseline = json.loads(json_raw.decode("utf-8"))
    require((baseline.get("schema_version"), baseline.get("generated_by")) == (4, "t48"),
            "expected the accepted t48 schema v4")
    require(len(baseline.get("tables", [])) == 8, "v4 baseline must contain eight tables")
    return baseline, json_raw, md_raw.decode("utf-8"), json_raw, md_raw


def compare_rows(left: list[dict[str, Any]], right: list[dict[str, Any]], left_name: str, right_name: str) -> dict[str, Any]:
    keys = ("row", "wire13", "legacy14", "end", "identity_at", "length", "identity", "wire_sha256")
    mismatch_rows = []
    for index, (a, b) in enumerate(zip(left, right)):
        if any(a.get(key) != b.get(key) for key in keys):
            mismatch_rows.append(index)
    if len(left) != len(right):
        mismatch_rows.extend(range(min(len(left), len(right)), max(len(left), len(right))))
    return {
        "sources": [left_name, right_name],
        "rows_left": len(left),
        "rows_right": len(right),
        "full_row_record_matches": len(left) == len(right) and not mismatch_rows,
        "mismatch_row_indices": mismatch_rows[:20],
        "compared_keys": list(keys),
    }


def compare_t50_to_t49(t49_rows: list[dict[str, Any]], t50_rows: list[dict[str, Any]], side: str) -> dict[str, Any]:
    require(len(t49_rows) == len(t50_rows) == 251, f"t50 {side} row profile count mismatch")
    offset_delta = [b["offset"] - a["wire13"] for a, b in zip(t49_rows, t50_rows)]
    length_delta = [b["len"] - a["length"] for a, b in zip(t49_rows, t50_rows)]
    identity_match = [b["identity"]["ordinal"] == a["identity"][0] and
                      b["identity"]["row_id"] == a["identity"][1] and
                      b["identity"]["repeated_id"] == a["identity"][2]
                      for a, b in zip(t49_rows, t50_rows)]
    identity_tail_start_match = [b["offset"] + b["identity"]["tail_offset_in_row"] == a["identity_at"]
                                 for a, b in zip(t49_rows, t50_rows)]
    raw_sha_match = [sha256_bytes(bytes.fromhex(b["raw_hex"])) == a["wire_sha256"]
                     for a, b in zip(t49_rows, t50_rows)]
    require(offset_delta == [0] + [1] * 250, f"t50 {side} boundary offset conflict pattern changed")
    require(length_delta == [1] + [0] * 250, f"t50 {side} row-length conflict pattern changed")
    require(all(identity_match), f"t50 {side} row identity ladder mismatch")
    require(all(identity_tail_start_match), f"t50 {side} absolute identity-tail starts differ from t49")
    require(not any(raw_sha_match), f"t50 {side} row spans unexpectedly match t49 wire hashes")
    return {
        "side": side,
        "rows_compared": 251,
        "start_offset_delta_t50_minus_t49": {"row_0": 0, "rows_1_to_250": 1},
        "row_length_delta_t50_minus_t49": {"row_0": 1, "rows_1_to_250": 0},
        "identity_ladder_matches": 251,
        "identity_tail_absolute_start_matches": sum(identity_tail_start_match),
        "t50_raw_row_sha_matches_t49_wire_sha": sum(raw_sha_match),
        "full_row_spans_match": 0,
        "conflict": True,
    }


def source_data() -> dict[str, Any]:
    source_groups = {
        "t47": [T47_DISCOVERY, T47_FIELDS, T47_CURSOR, T47_REPORT],
        "t49": [T49_DISCOVERY, T49_REPORT, *T49_CURSORS, *T49_FIELDS],
        "t50": [T50_REPORT, T50_PROFILE, T50_DIFF, T50_VERIFY, T50_DONE, *T50_ROWS],
        "t51": [T51_DISCOVERY, T51_REPORT, *T51_CURSORS, *T51_FIELDS],
    }
    artifacts = {task: [artifact_record(path) for path in paths] for task, paths in source_groups.items()}
    acceptance_artifacts = [artifact_record(path) for path in (T50_BUILDER, T50_ACCEPTANCE_SPOT)]

    t47_discovery, t47_fields, t47_cursor = read_json(T47_DISCOVERY), read_json(T47_FIELDS), read_json(T47_CURSOR)
    t49_discovery = read_json(T49_DISCOVERY)
    t49_fields = {Path(path).stem.removeprefix("fields_"): read_json(path) for path in T49_FIELDS}
    t49_cursors = {side: read_json(f"scratch/t49/out/cursor_t9_{side}.json") for side in ("client", "server")}
    t50_profile, t50_diff = read_json(T50_PROFILE), read_json(T50_DIFF)
    t50_report_raw = rel(T50_REPORT).read_text(encoding="utf-8")
    t50_rows = {f"{side}_{member}": read_jsonl(f"scratch/t50/out/profiles/table_{side}_{member}.rows.jsonl")
                for side in ("client", "server") for member in ("9", "extra_9")}
    t51_discovery = read_json(T51_DISCOVERY)
    t51_fields = {Path(path).stem.removeprefix("fields_"): read_json(path) for path in T51_FIELDS}
    t51_cursors = {
        "t9_client": read_json("scratch/t51/out/cursor_table_9_client.json"),
        "t9_server": read_json("scratch/t51/out/cursor_table_9_server.json"),
        "t10_server": read_json("scratch/t51/out/cursor_table_10_server.json"),
    }
    ledger = read_json(LEDGER)
    ledger_entries = {entry.get("id"): entry for entry in ledger.get("entries", [])}
    for entry_id in ("E87", "E89", "E90"):
        entry = ledger_entries.get(entry_id)
        require(entry is not None, f"acceptance ledger entry missing: {entry_id}")
        require((entry.get("kind"), entry.get("level")) == ("acceptance", "L3"),
                f"acceptance ledger grade mismatch: {entry_id}")
    e91 = ledger_entries.get("E91")
    require(e91 is not None and (e91.get("kind"), e91.get("level")) == ("acceptance", "L2"),
            "t50 L2 acceptance ledger entry E91 missing or incorrectly graded")
    require((sha256_file(rel(LEDGER)), rel(LEDGER).stat().st_size) == (LEDGER_SHA256, LEDGER_BYTES),
            "LEDGER snapshot changed from the verified E91 source")

    require(t47_discovery.get("status") == "partial_static_discovery" and
            (len(t47_discovery.get("parents", {})), t47_discovery.get("new_L3"),
             t47_discovery.get("unknown_links"), t47_discovery.get("closed_parents"),
             t47_discovery.get("L4")) == (15, 7, 6, 1, 0), "t47 static-discovery totals changed")
    require(t47_fields.get("L3") == 7 and t47_fields.get("L4") == 0 and
            set(t47_fields["fields"]) == {"lowa", "uppa", "capa", "year", "ppty", "txty", "perc", "fram", "leve"},
            "t47 Ntxr field ledger changed")
    require(t47_discovery.get("t9_owner_fixup") is not None, "t47 owner-fixup evidence missing")
    t47_server, t47_client = t47_cursor["server"], t47_cursor["client"]
    require((t47_server.get("mode"), t47_client.get("mode"), t47_server.get("row_count"),
             t47_client.get("row_count"), t47_server.get("tax_count"), t47_client.get("tax_count")) ==
            (1, 0, 251, 251, 1899, 0), "t47 Ntxr archive/mode closure changed")
    require(t47_server.get("item_tag_hist") == {"2": 1899} and t47_server.get("item_len_hist") == {"25": 1899},
            "t47 Ntxr item histograms changed")

    require(t49_discovery.get("status") == "partial_sidecar_positive_reader_open" and
            (t49_discovery.get("L3"), t49_discovery.get("held"), t49_discovery.get("L4")) == (17, 13, 0),
            "t49 field/status totals changed")
    require(t49_discovery.get("editor_sha256") == EDITOR_SHA256, "t49 editor SHA mismatch")
    require(t49_discovery["binding"]["table_9.dat"].get("client_mode") == 0 and
            t49_discovery["binding"]["table_9.dat"].get("server_mode") == 1 and
            t49_discovery["binding"]["table_extra_9.dat"].get("reader") is None and
            t49_discovery["binding"]["table_extra_9.dat"].get("mode") is None,
            "t49 table_9 binding or sidecar status changed")
    for side, mode, size, row_sum, payload_sha in (
        ("client", 0, 31956, 31934, "784810f0946a25d2cbb015917934c692c82059e6ba4ad21a0f88c0b7c95fabec"),
        ("server", 1, 307564, 307542, "6c2d8a0606de2665ecdda657e0d667bca78bd0e0f0860917d2b95d49a927875f"),
    ):
        cursor = t49_cursors[side]
        require((cursor.get("mode"), cursor.get("row_count"), cursor.get("row_sum"), cursor.get("payload_len"),
                 cursor.get("payload_sha256"), cursor.get("wire_footer")) ==
                (mode, 251, row_sum, size, payload_sha, 9), f"t49 {side} cursor closure mismatch")
        require(13 + row_sum + 9 == size and len(cursor.get("rows", [])) == 251,
                f"t49 {side} closure arithmetic mismatch")
    for parent in T9_PARENTS:
        fields = t49_fields[parent]
        require(fields.get("parent") == parent and fields.get("L4") == 0, f"t49 {parent} scope/L4 mismatch")
        l3 = sum(record.get("grade") == "L3" for record in fields.get("fields", {}).values())
        held = sum(record.get("grade") == "held" for record in fields.get("fields", {}).values())
        require(fields.get("L3") == l3, f"t49 {parent} L3 summary mismatch")
    t49_l3 = sum(source.get("L3", 0) for source in t49_fields.values())
    t49_held = sum(record.get("grade") == "held" for source in t49_fields.values()
                   for record in source.get("fields", {}).values())
    require((t49_l3, t49_held) == (17, 13), "t49 field totals mismatch")
    rejected_trials = []
    for side, members in t49_discovery.get("trials", {}).items():
        for member, modes in members.items():
            for mode, trial in modes.items():
                if not trial.get("closed"):
                    rejected_trials.append({"archive": side, "member": member, "mode": int(mode),
                                            "first_failure": copy.deepcopy(trial.get("first_failure"))})
    require(len(rejected_trials) == 6 and
            sum(item["member"] == "table_extra_9.dat" for item in rejected_trials) == 4,
            "t49 rejected member/mode trial count changed")

    require(t50_profile.get("status") == "partial_data_profile_t9" and
            t50_profile.get("evidence_level", {}).get("L3") == 0 and
            t50_profile.get("evidence_level", {}).get("L4") == 0 and
            t50_profile.get("framing_rules_are_candidates") is True,
            "t50 evidence status or grade changed")
    require(t50_diff.get("status") == "client_server_row_grammar_not_isomorphic" and
            t50_diff.get("evidence_level", {}).get("L3") == 0 and
            t50_diff.get("evidence_level", {}).get("L4") == 0,
            "t50 grammar diff status/grade changed")
    require(t50_profile.get("scope", {}).get("names_semantic_fields") is False and
            t50_profile.get("scope", {}).get("joins_target_ordinals") is False,
            "t50 scope must remain data-side and field-unassigned")
    for side in ("client", "server"):
        for member in ("table_9.dat", "table_extra_9.dat"):
            anchor = t50_profile["archives"][side]["members"][member]
            require(anchor["present"] is True and anchor["payload_sha256"] ==
                    t49_discovery["archives"][side]["members"][member]["payload_sha256"],
                    f"t50 {side}/{member} payload anchor disagrees with t49")
    t50_conflict = {side: compare_t50_to_t49(t49_cursors[side]["rows"], t50_rows[f"{side}_9"], side)
                    for side in ("client", "server")}
    t50_identity_tail_crosswalk = {}
    for side in ("client", "server"):
        conflict = t50_conflict[side]
        t50_identity_tail_crosswalk[side] = {
            "rows_compared": conflict["rows_compared"],
            "absolute_identity_tail_starts_match": conflict.pop("identity_tail_absolute_start_matches"),
            "t49_anchor": "cursor.identity_at",
            "t50_anchor": "row.offset + row.identity.tail_offset_in_row",
        }
    for side in ("client", "server"):
        c = t50_profile["members"][f"{side}/table_9.dat"]["closure"]
        require((c["row_start"], c["footer_bytes"], c["sum_row_lens"], c["count"]) ==
                (13, 8, 31935 if side == "client" else 307543, 251), f"t50 {side} candidate closure changed")
        require(c["framing_sensitivity"]["variants"]["footer=8"] == 1 and
                c["framing_sensitivity"]["variants"]["footer=9"] == 0 and
                all(c["framing_sensitivity"]["variants"][f"header={n}"] == 1 for n in range(11, 16)),
                f"t50 {side} framing sensitivity changed")
    extra_client = t50_profile["members"]["client/table_extra_9.dat"]["closure"]
    extra_server = t50_profile["members"]["server/table_extra_9.dat"]["closure"]
    require((extra_client["block_walks"], extra_server["block_walks"],
             extra_client["identity_structure_present"], extra_server["identity_structure_present"],
             extra_client["footer_separable"], extra_server["footer_separable"]) == (1, 4, False, False, False, False),
            "t50 table_extra_9 candidate summaries changed")
    require(extra_server["ambiguity"]["ambiguous_block_count"] == 2 and
            [item["row"] for item in extra_server["ambiguity"]["ambiguous"]] == [2, 82],
            "t50 table_extra_9 ambiguity records changed")
    require(all(result["complete_walks"] == 0 for side in (extra_client, extra_server)
                for result in side["identity_predicate_trial"]["results"]),
            "t50 table_extra_9 identity negative trials changed")
    require(t50_diff["table_9"]["identity_agrees_row_by_row"] is True and
            t50_diff["table_9"]["identical_row_count"] == 0 and
            all(t50_diff["cross_table"]["t9_ids_equal_t10_ids"][side] is True for side in ("client", "server")),
            "t50 cross-archive/cross-table L2 comparison changed")

    require(t51_discovery.get("status") == "partial" and t51_discovery.get("L3") == 6 and
            t51_discovery.get("L4") == 0 and tuple(t51_discovery.get("parents", {})) == T51_PARENT_ORDER,
            "t51 follow-up parent set/status changed")
    require(t51_discovery["parents"]["Nrvn"].get("member") == "table_9.dat" and
            t51_discovery["parents"]["Nftb"].get("member") == "table_10.dat" and
            t51_discovery["parents"]["Calt"].get("member") == "table_9.dat",
            "t51 archive bindings changed")
    require((t51_fields["Nrvn"].get("L3"), t51_fields["Nftb"].get("L3"), t51_fields["Calt"].get("L3")) == (2, 4, 0),
            "t51 field grade counts changed")
    require(sum(r.get("status") == "held" for r in t51_fields["Nftb"]["fields"].values()) == 3 and
            sum(r.get("status") == "held" for r in t51_fields["Calt"]["fields"].values()) == 2,
            "t51 held field counts changed")
    crosswalk = {
        "t9_client_t49_to_t51": compare_rows(t49_cursors["client"]["rows"], t51_cursors["t9_client"]["rows"], "t49-client", "t51-client"),
        "t9_server_t49_to_t51": compare_rows(t49_cursors["server"]["rows"], t51_cursors["t9_server"]["rows"], "t49-server", "t51-server"),
        "t10_server_t47_to_t51": compare_rows(t47_server["rows"], t51_cursors["t10_server"]["rows"], "t47-server", "t51-server"),
    }
    require(all(item["full_row_record_matches"] for item in crosswalk.values()), "t47/t49/t51 cross-walk changed")

    return {
        "t47_discovery": t47_discovery, "t47_fields": t47_fields, "t47_cursor": t47_cursor,
        "t49_discovery": t49_discovery, "t49_fields": t49_fields, "t49_cursors": t49_cursors,
        "t50_profile": t50_profile, "t50_diff": t50_diff, "t50_report_raw": t50_report_raw,
        "t50_rows": t50_rows, "t50_framing_conflict": t50_conflict,
        "t50_identity_tail_crosswalk": t50_identity_tail_crosswalk,
        "t51_discovery": t51_discovery, "t51_fields": t51_fields, "t51_cursors": t51_cursors,
        "ledger_entries": {key: ledger_entries[key] for key in ("E87", "E89", "E90", "E91")},
        "ledger_sha256": sha256_file(rel(LEDGER)), "ledger_bytes": rel(LEDGER).stat().st_size,
        "artifacts": artifacts, "acceptance_artifacts": acceptance_artifacts,
        "crosswalk": crosswalk, "rejected_trials": rejected_trials,
    }


def summarize_tax_field(code: str, record: dict[str, Any]) -> dict[str, Any]:
    result = {"code": code, "grade": record["status"], "schema": copy.deepcopy(record.get("schema")),
              "width_bytes": record.get("width"), "reason": record.get("reason"),
              "source_record": copy.deepcopy(record)}
    if record["status"] == "L3":
        result["item_relative_offset"] = record["accepted_item_offset"]
    else:
        result["candidate_item_relative_offset"] = record.get("static_item_offset")
    return result


def summarize_t9_field(code: str, record: dict[str, Any]) -> dict[str, Any]:
    return {"code": code, "grade": record["grade"], "schema": copy.deepcopy(record.get("schema")),
            "accepted_item_offset": record.get("accepted_item_offset"),
            "static_item_offset": record.get("static_item_offset"), "width_bytes": record.get("width"),
            "encoding": record.get("encoding"), "mask": record.get("mask"), "reason": record.get("reason"),
            "source_record": copy.deepcopy(record)}


def summarize_t9_cursor(cursor: dict[str, Any], side: str) -> dict[str, Any]:
    row_sum = cursor["row_sum"]
    footer_bytes = cursor["wire_footer"]
    payload_bytes = cursor["payload_len"]
    lengths = [row["length"] for row in cursor["rows"]]
    return {
        "archive": side, "member": "table_9.dat", "mode": cursor["mode"], "row_count": cursor["row_count"],
        "row_lengths_min_max": [min(lengths), max(lengths)], "row_stream_bytes": row_sum,
        "header_bytes": cursor["wire_header"], "wire_footer_bytes": footer_bytes,
        "payload_bytes": payload_bytes,
        "closure_formula": f"{cursor['wire_header']} + {row_sum} + {footer_bytes} = {payload_bytes}",
        "closure_ok": cursor["wire_header"] + row_sum + footer_bytes == payload_bytes,
        "payload_sha256": cursor["payload_sha256"], "footer_hex": cursor["footer"]["raw"],
        "selector_histogram": copy.deepcopy(cursor.get("selector_hist")),
    }


def build_nation_static_side(data: dict[str, Any]) -> dict[str, Any]:
    discovery, fields, cursor = data["t47_discovery"], data["t47_fields"], data["t47_cursor"]
    server, client = cursor["server"], cursor["client"]
    tax_fields = [summarize_tax_field(code, record) for code, record in fields["fields"].items()]
    linked_after_t51 = ["Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Ntxr", "Nfmp", "NCro", "Nrvn", "Calt", "Nftb"]
    t51_parents = data["t51_discovery"]["parents"]
    return {
        "source_task": "t47", "acceptance_ledger_entry": "E87",
        "status": "accepted_partial_static_discovery_with_Ntxr_cursor_closed",
        "evidence_grade": "L3 static; archive closure separately cited; L4=0",
        "Ntxr": {
            "scope": fields["scope"],
            "item_coordinate_basis": "Offsets are relative to the start of each Ntxr item, not the nation row. Parent-row coordinates vary with dynamic count and current cursor; wire13 and legacy14 origins differ by one byte.",
            "item_count_server": server["tax_count"], "item_tag_histogram_server": copy.deepcopy(server["item_tag_hist"]),
            "item_length_histogram_server": copy.deepcopy(server["item_len_hist"]),
            "archive_modes": {
                "client": {"mode": client["mode"], "row_count": client["row_count"], "item_count": client["tax_count"],
                           "payload_bytes": client["payload_len"], "payload_sha256": client["payload_sha256"],
                           "closure_formula": f"13 + {sum(r['length'] for r in client['rows'])} + 9 = {client['payload_len']}",
                           "closure_ok": 13 + sum(r["length"] for r in client["rows"]) + 9 == client["payload_len"],
                           "footer_hex": client["footer_hex"]},
                "server": {"mode": server["mode"], "row_count": server["row_count"], "item_count": server["tax_count"],
                           "payload_bytes": server["payload_len"], "payload_sha256": server["payload_sha256"],
                           "closure_formula": f"13 + {sum(r['length'] for r in server['rows'])} + 9 = {server['payload_len']}",
                           "closure_ok": 13 + sum(r["length"] for r in server["rows"]) + 9 == server["payload_len"],
                           "footer_hex": server["footer_hex"]},
            },
            "fields": tax_fields, "source_field_ledger": copy.deepcopy(fields),
        },
        "t47_static_discovery_map": {
            "as_of_task": "t47", "total_unknown_item_bearing_parents": len(discovery["parents"]),
            "reader_linked_count": len(T47_CONNECTED), "reader_linked_parents": list(T47_CONNECTED),
            "unknown_or_partial_count": len(T47_UNKNOWN), "unknown_or_partial_parents": list(T47_UNKNOWN),
            "parent_records": copy.deepcopy(discovery["parents"]),
            "owner_fixup": copy.deepcopy(discovery["t9_owner_fixup"]),
        },
        "t51_followup": {
            "source_task": "t51", "acceptance_ledger_entry": "E90", "status": data["t51_discovery"]["status"],
            "L3": data["t51_discovery"]["L3"], "L4": data["t51_discovery"]["L4"],
            "archive_or_owner_link_evidence_count": len(linked_after_t51),
            "archive_or_owner_link_evidence_parents": linked_after_t51,
            "remaining_unbound_or_unresolved_count": 3,
            "remaining_unbound_or_unresolved_parents": ["TCrs", "EDfx", "EDsc"],
            "parent_records": copy.deepcopy(t51_parents), "field_ledgers": copy.deepcopy(data["t51_fields"]),
            "Nrvn_server_item_summary": {
                "nonempty_rows": sum(bool(row.get("Nrvn", {}).get("items")) for row in data["t51_cursors"]["t9_server"]["rows"]),
                "items": sum(len(row.get("Nrvn", {}).get("items", [])) for row in data["t51_cursors"]["t9_server"]["rows"]),
                "grades": {code: rec["status"] for code, rec in data["t51_fields"]["Nrvn"]["fields"].items()},
            },
            "Nftb_server_item_summary": {
                "nonempty_rows": [r["row"] for r in data["t51_cursors"]["t10_server"]["rows"] if r.get("Nftb", {}).get("count", 0)],
                "item_count": sum(r.get("Nftb", {}).get("count", 0) for r in data["t51_cursors"]["t10_server"]["rows"]),
                "grades": {code: rec["status"] for code, rec in data["t51_fields"]["Nftb"]["fields"].items()},
                "held_references": [code for code, rec in data["t51_fields"]["Nftb"]["fields"].items() if rec["status"] == "held"],
            },
            "Calt_server_item_summary": {
                "row_count": len(data["t51_cursors"]["t9_server"]["rows"]),
                "nonzero_count_rows": sum(r.get("Calt", {}).get("count", 0) > 0 for r in data["t51_cursors"]["t9_server"]["rows"]),
                "grades": {code: rec["status"] for code, rec in data["t51_fields"]["Calt"]["fields"].items()},
            },
        },
        "L4": 0,
    }


def build_nation_t9_wire(data: dict[str, Any]) -> dict[str, Any]:
    discovery = data["t49_discovery"]
    parents = {}
    for parent in T9_PARENTS:
        source = data["t49_fields"][parent]
        field_records = [summarize_t9_field(code, record) for code, record in source["fields"].items()]
        parents[parent] = {"L3": sum(r["grade"] == "L3" for r in field_records),
                           "held": sum(r["grade"] == "held" for r in field_records),
                           "fields": field_records, "source_field_ledger": copy.deepcopy(source)}
    t50_sidecars = {}
    for side in ("client", "server"):
        closure = data["t50_profile"]["members"][f"{side}/table_extra_9.dat"]["closure"]
        t50_sidecars[side] = {
            "candidate_block_walks": closure["block_walks"], "block_count": closure["count"],
            "sum_block_spans": closure["sum_block_spans"], "equation": closure["equation"],
            "nameless_blocks": closure["nameless_blocks"], "footer_separable": closure["footer_separable"],
            "identity_structure_present": closure["identity_structure_present"],
            "identity_predicate_trial": copy.deepcopy(closure["identity_predicate_trial"]),
            "ambiguity": copy.deepcopy(closure["ambiguity"]),
            "block_internal_grammar": closure.get("block_internal_grammar", "unknown"),
        }
    t50_sources_verbatim = {
        "REPORT.md": data["t50_report_raw"],
        "DONE.md": rel(T50_DONE).read_text(encoding="utf-8"),
        "profile_t9.json": copy.deepcopy(data["t50_profile"]),
        "grammar_diff_t9.json": copy.deepcopy(data["t50_diff"]),
    }
    return {
        "source_task": "t49", "acceptance_ledger_entry": "E89",
        "status": discovery["status"], "editor_exe_sha256": discovery["editor_sha256"],
        "table_9": {
            "member": "table_9.dat", "owner": "NATIONAL_TEAM_CONTAINER", "table_type": 9,
            "row_count_each_archive": 251,
            "archive_modes": {side: summarize_t9_cursor(cursor, side) for side, cursor in data["t49_cursors"].items()},
            "parents": parents, "grade_totals": {"L3": 17, "held": 13},
            "source_discovery_binding": copy.deepcopy(discovery["binding"]["table_9.dat"]),
            "framing_status": "accepted_t49_cursor_with_t50_candidate_conflict_unresolved",
            "field_locator_preservation": "All 17 t49 accepted L3 field locators and 13 held records are retained unchanged. t50 is data-side L1/L2 only and does not replace, upgrade, or adjudicate these locators.",
        },
        "table_extra_9": {
            "status": "unbound_open_negative", "reader": None, "mode": None,
            "client_present": discovery["archives"]["client"]["members"]["table_extra_9.dat"]["present"],
            "server_present": discovery["archives"]["server"]["members"]["table_extra_9.dat"]["present"],
            "target_parent_assignment": [], "rejected_member_mode_attempts_total": len(data["rejected_trials"]),
            "rejected_member_mode_attempts_for_extra_9": sum(r["member"] == "table_extra_9.dat" for r in data["rejected_trials"]),
            "rejection_records": copy.deepcopy(data["rejected_trials"]),
            "source_discovery_binding": copy.deepcopy(discovery["binding"]["table_extra_9.dat"]),
            "t50_data_side_candidate_profile": t50_sidecars,
            "t50_L2_shape_assessment": {
                "acceptance_ledger_entry": "E91",
                "recorded_shape": "nation name-table block shape: ordinal|name_len|name",
                "scope": "L2 data-side structural assessment only; internal block grammar remains unresolved",
                "negative_evidence_for": "TCrs table_extra_9 sidecar hypothesis",
                "target_parent_assignment": [],
            },
            "t50_not_a_parent_assignment": True,
        },
        "t50_L2_cross_validation": {
            "source_task": "t50", "status": "accepted_L2_data_side_profile_fields_unassigned_framing_conflict_open",
            "acceptance_ledger_entry": "E91", "acceptance_ledger_level": "L2",
            "acceptance_ledger_claim_sha256": canonical_sha256(data["ledger_entries"]["E91"]["claim"]),
            "evidence_level": copy.deepcopy(data["t50_profile"]["evidence_level"]),
            "ledger_acceptance_scope": "E91 accepts only the L2 data-side profile and framing observations; it does not assert L3 field, reader, mode, or target-parent bindings.",
            "fields_named": False, "target_ordinals_joined": False,
            "table_9_candidate_framing": {
                "candidate_only": True, "header_bytes": 13,
                "footer_bytes_each_archive": 8, "footer_hex_each_archive": "00000001ec7ae404",
                "closure_formulas": {side: data["t50_profile"]["members"][f"{side}/table_9.dat"]["closure"]["equation"]
                                      for side in ("client", "server")},
                "header_11_through_15_each_close_once": True,
                "footer_8_closes_once_footer_9_closes_zero": True,
                "header_split_data_underdetermined": True,
                "report_caveat_preserved_verbatim": True,
            },
            "t49_t51_alternative": {
                "wire_header_bytes": 13, "wire_footer_bytes": 9,
                "footer_hex": {side: data["t49_cursors"][side]["footer"]["raw"] for side in ("client", "server")},
                "closure_formulas": {side: summarize_t9_cursor(data["t49_cursors"][side], side)["closure_formula"]
                                      for side in ("client", "server")},
                "t51_reproduces_t49_row_records": True,
            },
            "row_boundary_conflict": copy.deepcopy(data["t50_framing_conflict"]),
            "adjudication": "NO WINNER. Preserve both framings as source-specific alternatives. The t49 E89 accepted field ledger remains unchanged; t50 is an L1/L2 candidate profile, not the winning cursor and not a field-grade promotion.",
            "table_9_data_side_comparison": copy.deepcopy(data["t50_diff"]["table_9"]),
            "t9_t10_identity_ladder_comparison": copy.deepcopy(data["t50_diff"]["cross_table"]),
            "source_records_verbatim": t50_sources_verbatim,
            "source_report_sha256": next(a["sha256"] for a in data["artifacts"]["t50"] if a["path"] == T50_REPORT),
        },
        "t51_t47_t49_cross_walk": copy.deepcopy(data["crosswalk"]),
        "t50_identity_tail_crosswalk": copy.deepcopy(data["t50_identity_tail_crosswalk"]),
        "cross_walk_scope_note": "t51 reproduces t49's table_9 cursor records and t47's table_10 server records. t50 independently matches t49's absolute identity-tail starts on all 251 rows per archive, but its full row spans differ at the marker/selector boundary. These cross-walks do not select a whole-row framing; see row_boundary_conflict.",
        "L4": 0,
    }


def nation_unique_field_ids(static_side: dict[str, Any], t9_wire: dict[str, Any]) -> list[str]:
    ids = [f"t10/Ntxr/{f['code']}" for f in static_side["Ntxr"]["fields"] if f["grade"] == "L3"]
    for parent, item in t9_wire["table_9"]["parents"].items():
        ids.extend(f"t9/{parent}/{f['code']}" for f in item["fields"] if f["grade"] == "L3")
    followup = static_side["t51_followup"]["field_ledgers"]
    for parent, member in (("Nrvn", "t9"), ("Nftb", "t10")):
        ids.extend(f"{member}/{parent}/{code}" for code, record in followup[parent]["fields"].items()
                   if record["status"] == "L3")
    return ids


def build_schema(baseline: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    schema = copy.deepcopy(baseline)
    schema["schema_version"], schema["generated_by"] = 5, "t52"
    static_side = build_nation_static_side(data)
    data["nation_t9_wire"] = build_nation_t9_wire(data)
    t9_wire = data["nation_t9_wire"]
    unique_ids = nation_unique_field_ids(static_side, t9_wire)
    nation_l3 = 7 + 17 + 2 + 4
    nation_held = 2 + 13 + 2 + 3
    require((nation_l3, len(unique_ids), nation_held) == (30, 30, 20), "nation field coverage arithmetic mismatch")
    schema["nation_static_side"] = static_side
    schema["nation_t9_wire"] = t9_wire
    schema["coverage"].update({
        "nation_L3_occurrences": nation_l3,
        "nation_L3_unique_wire_fields": len(unique_ids),
        "nation_held_occurrences": nation_held,
        "nation_negative_records": 7,
        "nation_L2_cross_validation_members": 4,
        "nation_t50_candidate_framing_conflicts": 1,
        "nation_t50_negative_report_items": 7,
        "nation_L3_unique_wire_field_ids": unique_ids,
        "nation_negative_record_breakdown": {
            "t49_rejected_member_mode_attempts": 6,
            "t49_table_extra_9_rejections_within_total": 4,
            "t51_EDfx_UI_path_with_archive_backing_unbound": 1,
            "t50_report_section_6_negative_or_unresolved_items": 7,
            "t50_items_counted_separately_not_folded_into_nation_negative_records": True,
            "held_fields_are_not_negative_records": True,
            "unresolved_EDsc_and_partial_TCRS_are_not_absence_claims": True,
        },
        "nation_coverage_policy": (
            "Nation L3 occurrences are accepted scoped claims from t47 Ntxr, t49 table_9 parents, "
            "and t51 Nrvn/Nftb. Unique identity is archive member + parent + field code. Held items "
            "remain separate. nation_negative_records is the bounded t49 rejected-trial set plus "
            "the t51 EDfx UI-path/backing-unbound observation; t50's seven numbered report items "
            "are separately counted and preserved verbatim, not folded into that record total."
        ),
    })

    provenance = schema["incremental_provenance"]
    entries = provenance.setdefault("acceptance_ledger_entries", {})
    for entry_id, entry in data["ledger_entries"].items():
        entries[entry_id] = {"kind": entry["kind"], "level": entry["level"], "date": entry.get("date"),
                             "claim_sha256": canonical_sha256(entry["claim"])}
    tasks = provenance.setdefault("tasks", {})
    payloads47 = {"client_table_10": data["t47_cursor"]["client"]["payload_sha256"],
                  "server_table_10": data["t47_cursor"]["server"]["payload_sha256"]}
    payloads49 = {"client_table_9": data["t49_cursors"]["client"]["payload_sha256"],
                  "server_table_9": data["t49_cursors"]["server"]["payload_sha256"],
                  "client_table_extra_9": data["t49_discovery"]["archives"]["client"]["members"]["table_extra_9.dat"]["payload_sha256"],
                  "server_table_extra_9": data["t49_discovery"]["archives"]["server"]["members"]["table_extra_9.dat"]["payload_sha256"]}
    payloads50 = {f"{side}_{member}": data["t50_profile"]["archives"][side]["members"][filename]["payload_sha256"]
                  for side in ("client", "server") for member, filename in (("table_9", "table_9.dat"), ("table_extra_9", "table_extra_9.dat"))}
    payloads51 = {"client_table_9": data["t51_cursors"]["t9_client"]["payload_sha256"],
                  "server_table_9": data["t51_cursors"]["t9_server"]["payload_sha256"],
                  "server_table_10": data["t51_cursors"]["t10_server"]["payload_sha256"]}
    tasks["t47"] = {"status": "accepted_partial_static_discovery_with_Ntxr_cursor_closed",
                     "acceptance_ledger_entry": "E87", "editor_exe_sha256": EDITOR_SHA256,
                     "payload_sha256": payloads47, "source_artifacts": data["artifacts"]["t47"],
                     "ledger_claim_sha256": canonical_sha256(data["ledger_entries"]["E87"]["claim"])}
    tasks["t49"] = {"status": "accepted_partial_main_table_wire_sidecar_open",
                     "acceptance_ledger_entry": "E89", "editor_exe_sha256": EDITOR_SHA256,
                     "payload_sha256": payloads49, "source_artifacts": data["artifacts"]["t49"],
                     "ledger_claim_sha256": canonical_sha256(data["ledger_entries"]["E89"]["claim"])}
    tasks["t50"] = {"status": "accepted_L2_data_side_profile_fields_unassigned_framing_conflict_open",
                     "acceptance_ledger_entry": "E91", "ledger_status": "E91 accepts L2 data-side profile only; no L3 field, reader, mode, or parent mapping",
                     "ledger_claim_sha256": canonical_sha256(data["ledger_entries"]["E91"]["claim"]),
                     "evidence_level": copy.deepcopy(data["t50_profile"]["evidence_level"]),
                     "payload_sha256": payloads50, "source_artifacts": data["artifacts"]["t50"],
                     "acceptance_evidence": data["acceptance_artifacts"],
                     "framing_adjudication": "identity-tail absolute starts and identity ladder match t49; full row spans differ at marker/selector boundary; no winner"}
    tasks["t51"] = {"status": "accepted_partial_unknown_parent_followup_and_independent_cross_walk",
                     "acceptance_ledger_entry": "E90", "editor_exe_sha256": EDITOR_SHA256,
                     "payload_sha256": payloads51, "source_artifacts": data["artifacts"]["t51"],
                     "ledger_claim_sha256": canonical_sha256(data["ledger_entries"]["E90"]["claim"])}
    provenance["t52_ledger_snapshot"] = {"path": LEDGER, "sha256": data["ledger_sha256"],
                                         "bytes": data["ledger_bytes"], "entries_used": ["E87", "E89", "E90", "E91"],
                                         "t50_acceptance_entry": "E91", "t50_acceptance_level": "L2"}
    return schema


def render_markdown(v4_markdown: str, schema: dict[str, Any]) -> str:
    coverage = schema["coverage"]
    static = schema["nation_static_side"]
    nation = schema["nation_t9_wire"]
    tax = static["Ntxr"]
    t50 = nation["t50_L2_cross_validation"]
    lines = [
        "## t52 Incremental Addendum", "",
        "This addendum appends accepted nation evidence to the t48 v4 report. Earlier v4 sections are retained verbatim as historical baseline text; this section supersedes only the earlier t48 statement that t47 static discovery remained open. The t46 `nation_data_side_status` and all v4 club records remain unchanged.", "",
        "### Coverage", "",
        f"- Club counters remain unchanged: {coverage['club_L3_occurrences']} scoped L3 occurrences, {coverage['club_L3_unique_wire_fields']} unique wire fields, {coverage['held_fields']} held occurrences, and {coverage['negative_regressions']} original negative regressions.",
        f"- Nation accepted L3 occurrences / unique scoped wire fields / held occurrences: {coverage['nation_L3_occurrences']} / {coverage['nation_L3_unique_wire_fields']} / {coverage['nation_held_occurrences']}.",
        f"- Bounded nation negative records: {coverage['nation_negative_records']} (six t49 rejected member/mode trials, four of them against table_extra_9, plus one t51 EDfx UI-path/backing-unbound observation). t50's seven numbered report findings are separately counted, not added to this total.",
        "- L4: 0.", "",
        "### Nation Static Side", "",
        "t47 E87 maps 15 item-bearing parent targets: 9 reader-linked (Nntp, Nctp, Nrtp, NTRv, NWGv, NSps, Ntxr, Nfmp, NCro) and 6 unknown/partial (Nftb, EDfx, EDsc, Nrvn, Calt, TCrs). Its owner-fixup equation is `NATION+0x108+8*container[0xb9] = container`; slot 2 uses index 0 only on resolver success and non-null target, not for every archive nation row.", "",
        f"Ntxr closes {tax['item_count_server']} server items, all tag 2 and 25 B. Server mode is 1; client mode is 0 and bypasses the item list. Server payload: {tax['archive_modes']['server']['payload_bytes']} B, `{tax['archive_modes']['server']['closure_formula']}`, SHA-256 `{tax['archive_modes']['server']['payload_sha256']}`. Client payload: {tax['archive_modes']['client']['payload_bytes']} B, `{tax['archive_modes']['client']['closure_formula']}`, SHA-256 `{tax['archive_modes']['client']['payload_sha256']}`.", "",
        "Ntxr offsets are item-relative, not nation-row offsets; the parent-row coordinate varies with the dynamic count/current cursor. Full source field records are retained in JSON.", "",
        "| Field | Grade | Item-relative offset | Width | Source disposition |", "|---|---|---:|---:|---|",
    ]
    for field in tax["fields"]:
        offset = f"+{field['item_relative_offset']}" if field["grade"] == "L3" else f"candidate +{field['candidate_item_relative_offset']}"
        lines.append(f"| `{field['code']}` | `{field['grade']}` | {offset} | {field['width_bytes']} B | {field['reason']} |")
    lines += ["", "t51 E90 follows three prior unknowns to archive/owner evidence: Nrvn to table_9 (720 items, `nati` and `leve` L3); Nftb to table_10 row 162 (7 items, `NpFn`, `NpSn`, `NbCn`, `NbPd` L3; `NbPi`, `NbPn`, `NbFt` held); Calt to table_9 (251 zero counts, `cmid` and `stid` held). TCrs remains a partial table_extra_9 candidate without binding; EDfx proves a UI path but no archive backing; EDsc remains unresolved. None of these statuses proves absent persistence.", "",
        "### Nation t9 Wire", "",
        f"t49 E89 accepts `table_9.dat` under client mode 0 and server mode 1, 251 rows each, with 17 L3 and 13 held field claims. Client closure: `{nation['table_9']['archive_modes']['client']['closure_formula']}`; payload SHA-256 `{nation['table_9']['archive_modes']['client']['payload_sha256']}`. Server closure: `{nation['table_9']['archive_modes']['server']['closure_formula']}`; payload SHA-256 `{nation['table_9']['archive_modes']['server']['payload_sha256']}`.", "",
        "| Parent | L3 / held | Field grades and accepted item-relative coordinates |", "|---|---:|---|",
    ]
    for parent, details in nation["table_9"]["parents"].items():
        rendered = []
        for field in details["fields"]:
            if field["grade"] == "L3":
                coord = f"+{field['accepted_item_offset']}/{field['width_bytes']}B"
                if field.get("mask") is not None:
                    coord += f" mask 0x{field['mask']:02x}"
                rendered.append(f"`{field['code']}` L3 {coord}")
            else:
                candidate = field.get("static_item_offset")
                coord = f"candidate +{candidate}/{field['width_bytes']}B; " if candidate is not None and field.get("width_bytes") is not None else ""
                rendered.append(f"`{field['code']}` held {coord}{field['reason']}")
        lines.append(f"| `{parent}` | {details['L3']} / {details['held']} | {'; '.join(rendered)} |")
    lines += ["", "`table_extra_9.dat` remains unbound: no reader, mode, or target-parent assignment. t49 records six rejected member/mode trials overall, four against table_extra_9 across both archives and modes. E91 accepts the t50 L2 data-side shape as nation name-table blocks (`ordinal|name_len|name`), negative evidence against the TCrs sidecar hypothesis; the block-internal grammar remains unresolved and no target parent is assigned.", "",
        "### t50 Data-Side Comparison", "",
        "t50 supplied an L1/L2 data-side profile accepted by E91 (L3=0, L4=0; no semantic fields named and no target ordinals joined). It confirms 251 t9 identity tails and row-ID ladders agree between client/server, and absolute identity-tail starts match t49 on all 251 rows per archive; the t9/t10 identity ladders also agree. This is not a t9 schema-field, reader, mode, or parent-binding claim.", "",
        "**Framing conflict, unresolved; no winner.** t49 and its t51 replay use a 13-byte header plus a 9-byte wire footer (`0000000001ec7ae404`): client `13 + 31934 + 9 = 31956`, server `13 + 307542 + 9 = 307564`. t50 independently supplies an L2 candidate 13-byte header plus an 8-byte footer (`00000001ec7ae404`): client `13 + 31935 + 8 = 31956`, server `13 + 307543 + 8 = 307564`. The full row spans match on 0/251 rows: row 0 starts at the same offset but is one byte longer in t50; rows 1-250 start one byte later in t50, retain the same lengths, and carry the same identity tuples. Despite that, the absolute identity-tail start agrees on all 251 rows per archive. The remaining one-byte boundary is the marker/next-selector ownership question; no t50 raw row hash equals the t49 wire-row hash. t50 also reports headers 11-15 all close once, so the 13-byte header split is not data-determined. The t50 report's 8-vs-9 caveat is preserved verbatim in the v5 JSON source record.", "",
        "The t49 accepted field locators and held records are preserved exactly. E91 accepts t50 as L2 data-side evidence only, not as the winning cursor; it neither overwrites t49 nor promotes any field to L3. t51 confirms its own t9 row records match t49, while t50 confirms the shared identity-tail starts but does not resolve the full row framing.", "",
        "t50 `table_extra_9.dat`: 251 client blocks have one candidate walk; server has four walks with two internal ambiguities (rows 2 and 82). E91 records an L2 nation-name-table block shape (`ordinal|name_len|name`) and negative evidence against the TCrs sidecar hypothesis. Internal grammar is still unknown, no independent footer is separable, all four unchanged t9 identity-predicate variants die at row 1 on each archive, and the sidecar remains unassigned.", "",
        "t50's seven numbered negative/unresolved findings, DONE sentinel, full profile, and grammar diff are retained in `nation_t9_wire.t50_L2_cross_validation.source_records_verbatim`; `scratch/t50/out/DONE.md` and all source outputs are SHA-256 recorded. `table_extra_10.dat` is absent in both archives per that report.", "",
        "### t51 Cross-Walk", "",
        "t51 independently reproduces t49's table_9 client/server row records and t47's table_10 server row records (251/251 in each pair, including identities and per-row wire SHA-256). This establishes those source-pair matches only; it does not adjudicate the t50 candidate framing.", "",
        "### Provenance", "",
        f"Editor binary SHA-256 for t47/t49/t51: `{EDITOR_SHA256}`. Ledger entries: E87 (t47 L3), E89 (t49 L3), E90 (t51 L3), and E91 (t50 L2 only). E89/E90/E91 are dated `2026-11-20`, one day after the run date `2026-11-19`; the dates are recorded as present in the ledger, without independent timestamp validation.", "",
        "| Task | Source artifact | SHA-256 |", "|---|---|---|",
    ]
    for task in ("t47", "t49", "t50", "t51"):
        for artifact in schema["incremental_provenance"]["tasks"][task]["source_artifacts"]:
            lines.append(f"| {task} | `{artifact['path']}` | `{artifact['sha256']}` |")
    for artifact in schema["incremental_provenance"]["tasks"]["t50"]["acceptance_evidence"]:
        lines.append(f"| t50 acceptance | `{artifact['path']}` | `{artifact['sha256']}` |")
    lines += ["", f"Acceptance ledger snapshot SHA-256: `{schema['incremental_provenance']['t52_ledger_snapshot']['sha256']}`. L4 remains 0.", ""]
    return v4_markdown.rstrip() + "\n\n" + "\n".join(lines)


def render_report(schema: dict[str, Any]) -> str:
    c = schema["coverage"]
    conflict = schema["nation_t9_wire"]["t50_L2_cross_validation"]["row_boundary_conflict"]
    return "\n".join([
        "# t52 v5 Merge Report", "",
        "Status: complete, with t50/t49 framing conflict recorded and left unresolved.", "",
        "## Result", "",
        "- Public schema advanced from v4 to v5 by additive nation sections.",
        "- Protected v4 sections (`tables`, `negative_regressions`, `v3_baseline`, `club_auxiliary_sources`, `nation_data_side_status`) remain structurally identical to the frozen v4 snapshot.",
        f"- Nation totals: L3 occurrences={c['nation_L3_occurrences']}, unique wire fields={c['nation_L3_unique_wire_fields']}, held={c['nation_held_occurrences']}, bounded negative records={c['nation_negative_records']}.",
        "- t47 Ntxr: 7 L3, 2 held; 1,899 server items, tag 2, 25 bytes each; client mode 0 has no items.",
        "- t49 table_9: 17 L3, 13 held. table_extra_9 remains unbound; 6 rejected trials total, 4 against the sidecar.",
        "- t50 E91 acceptance: L2 data-side profile only; no semantic fields, target joins, L3, reader, mode, or parent assignment. Report, DONE, profile, and diff are retained in v5.",
        f"- Framing conflict: t49/t51 match their row records; t50 identity-tail starts match t49 on {schema['nation_t9_wire']['t50_identity_tail_crosswalk']['client']['absolute_identity_tail_starts_match']}/251 client and {schema['nation_t9_wire']['t50_identity_tail_crosswalk']['server']['absolute_identity_tail_starts_match']}/251 server rows, while full row spans match on {conflict['client']['full_row_spans_match']}/251 and {conflict['server']['full_row_spans_match']}/251. No framing winner; t49 field grades unchanged.",
        "- t51 follow-up: Nrvn, Nftb, and Calt records merged with held grades preserved; TCrs/EDfx/EDsc remain open or unresolved.",
        "- L4=0.", "",
        "## Deliverables", "",
        "- `reports/club_nation_subtable_schema.json` and `.md`: v5 pair.",
        "- `scratch/t52/out/club_nation_subtable_schema.v4.json` and `.md`: byte-exact v4 baseline snapshots.",
        "- `scratch/t52/out/consolidate_v5.py`: deterministic builder with `--help` and `--selftest`.",
        "- `scratch/t52/out/verify.py`: independent verifier; it does not import the builder or fm24_dump.",
        "- `scripts/t52_spot_v5.py`: independent 20+ item spot check with `--help` and `--selftest`.",
        "- `scratch/t52/out/spot_*.log`: execution logs.", "",
        "## Audit Note", "",
        "The frozen v4 JSON/Markdown hashes are pinned in the builder and verifier. New source-artifact hashes are recorded per task in `incremental_provenance.tasks`. Source tasks, the ledger, and pre-existing worktree changes were read-only.", "",
        "## fix1", "",
        "Root cause: build-side provenance was updated to E91 before the validator was updated, leaving a stale `acceptance_ledger_entry is None` guard.",
        "Fix: the validator now requires live E91 to be `acceptance`/`L2` and the t50 scope note to be present, while rejecting t50 attribution in field-grade structures. The L3=0 and `NO WINNER` records are unchanged.",
        "Verification commands were rerun; outputs are appended to `spot_*.log` with the `t52-fix1` marker.", "",
    ])


def verification_logs_passed() -> bool:
    required = {
        "spot_builder_help.log": ("usage:", "t52-fix1"),
        "spot_verify_help.log": ("usage:", "t52-fix1"),
        "spot_spotcheck_help.log": ("usage:", "t52-fix1"),
        "spot_builder_selftest.log": ("SELFTEST PASS", "t52-fix1"),
        "spot_verify_selftest.log": ("selftest PASS", "t52-fix1"),
        "spot_spotcheck_selftest.log": ("selftest PASS", "t52-fix1"),
        "spot_build.log": ("t52 schema v5 build complete", "t52-fix1"),
        "spot_verify.log": ("t52 independent verification PASS", "t52-fix1"),
        "spot_schema.log": ("t52 spot checks PASS", "t52-fix1"),
        "spot_t01_anchors.log": ("7/7 checks passed", "t52-fix1"),
    }
    for name, markers in required.items():
        path = OUT_DIR / name
        if not path.is_file():
            return False
        text = path.read_text(encoding="utf-8")
        if any(marker not in text for marker in markers):
            return False
    return True


def render_done(schema: dict[str, Any], verified: bool | None = None) -> str:
    if verified is None:
        verified = verification_logs_passed()
    runtime_line = ("- [x] Help, selftests, build, independent verification, spot checks, and t01 anchors passed; see `spot_*.log`."
                    if verified else
                    "- [ ] Runtime verification is pending; record passing commands in `spot_*.log`.")
    return "\n".join([
        "# t52 DONE", "",
        "- [x] v4 baseline frozen and SHA-256 verified.",
        "- [x] t47/t49/t50/t51 source artifacts SHA-256 recorded.",
        "- [x] v4 protected content retained; nation increments appended.",
        "- [x] t50 L1/L2 profile merged without semantic-field promotion.",
        "- [x] t49/t50 framing conflict represented as two alternatives; no winner selected.",
        "- [x] t50 sidecar candidate retained as unassigned; negative findings preserved.",
        "- [x] t51 cross-walk and follow-up field grades merged.",
        f"- [x] Coverage totals generated: {schema['coverage']['nation_L3_occurrences']} L3 / {schema['coverage']['nation_L3_unique_wire_fields']} unique / {schema['coverage']['nation_held_occurrences']} held / {schema['coverage']['nation_negative_records']} bounded negative records.",
        runtime_line,
        "",
        "L4=0. No game/editor/IDA process was launched; no network access was used.", "",
        "## fix1", "",
        "Root cause: the builder began emitting E91 provenance before the schema validator was updated, so build and validation disagreed about the t50 acceptance entry.",
        "Fix: validation now requires live E91 to be an `acceptance`/`L2` entry with the t50 ledger scope note, while separately rejecting any t50 attribution in field-grade structures. t50 remains L3=0.",
        "Runtime results are recorded in the appended `spot_*.log` entries marked `t52-fix1`.", "",
    ])


def validate_schema(schema: dict[str, Any], baseline: dict[str, Any], markdown: str) -> None:
    require((schema.get("schema_version"), schema.get("generated_by")) == (5, "t52"), "output is not schema v5")
    for key in ("tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "nation_data_side_status"):
        require(schema.get(key) == baseline.get(key), f"v4 protected block changed: {key}")
    for key, value in baseline["coverage"].items():
        require(schema["coverage"].get(key) == value, f"v4 coverage baseline changed: {key}")
    require(len(schema["tables"]) == 8 and len(schema["negative_regressions"]) == 4, "v4 base counts changed")
    require((schema["coverage"]["nation_L3_occurrences"], schema["coverage"]["nation_L3_unique_wire_fields"],
             schema["coverage"]["nation_held_occurrences"], schema["coverage"]["nation_negative_records"]) == (30, 30, 20, 7),
            "nation coverage totals mismatch")
    t50 = schema["nation_t9_wire"]["t50_L2_cross_validation"]
    require(t50["adjudication"] == "NO WINNER. Preserve both framings as source-specific alternatives. The t49 E89 accepted field ledger remains unchanged; t50 is an L1/L2 candidate profile, not the winning cursor and not a field-grade promotion." and
            t50["row_boundary_conflict"]["client"]["full_row_spans_match"] == 0 and
            t50["row_boundary_conflict"]["server"]["full_row_spans_match"] == 0 and
            schema["nation_t9_wire"]["t50_identity_tail_crosswalk"]["client"]["absolute_identity_tail_starts_match"] == 251 and
            schema["nation_t9_wire"]["t50_identity_tail_crosswalk"]["server"]["absolute_identity_tail_starts_match"] == 251,
            "t50 NO WINNER record or separate identity-tail cross-walk changed")
    require(schema["nation_t9_wire"]["table_9"]["grade_totals"] == {"L3": 17, "held": 13}, "t49 grades changed")
    require(schema["nation_t9_wire"]["table_extra_9"]["target_parent_assignment"] == [], "sidecar was assigned to a parent")
    require(schema["nation_static_side"]["Ntxr"]["item_count_server"] == 1899, "Ntxr item count changed")
    require(all(item["identical"] if "identical" in item else item["full_row_record_matches"]
                for item in schema["nation_t9_wire"]["t51_t47_t49_cross_walk"].values()), "t51 cross-walk mismatch")
    require(markdown.startswith((V4_MD.read_text(encoding="utf-8") if V4_MD.exists() else rel(PUBLIC_MD).read_text(encoding="utf-8")).rstrip() +
                                "\n\n## t52 Incremental Addendum"), "v4 Markdown prefix was not preserved")
    t50_task = schema["incremental_provenance"]["tasks"]["t50"]
    live_ledger = read_json(LEDGER)
    e91_matches = [entry for entry in live_ledger.get("entries", []) if entry.get("id") == "E91"]
    require(len(e91_matches) == 1 and
            (e91_matches[0].get("kind"), e91_matches[0].get("level")) == ("acceptance", "L2") and
            t50_task.get("acceptance_ledger_entry") == "E91" and
            isinstance(t50_task.get("ledger_status"), str) and
            "E91 accepts L2 data-side profile only" in t50_task["ledger_status"] and
            schema["nation_t9_wire"]["t50_L2_cross_validation"].get("acceptance_ledger_entry") == "E91",
            "t50 provenance may cite E91 only when the live ledger accepts it as L2 with scope note")

    def forbid_t50_field_attribution(node: Any, location: str) -> None:
        if isinstance(node, dict):
            require(node.get("source_task") != "t50" and node.get("field_source_task") != "t50" and
                    node.get("grade_source_task") != "t50" and node.get("acceptance_ledger_entry") != "E91",
                    f"t50 field-grade attribution found in {location}")
            for key, value in node.items():
                forbid_t50_field_attribution(value, f"{location}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                forbid_t50_field_attribution(value, f"{location}[{index}]")

    for label, mapping in (("nation_static_side", schema["nation_static_side"]),
                           ("nation_t9_wire.table_9", schema["nation_t9_wire"]["table_9"]),
                           ("tables", schema["tables"])):
        forbid_t50_field_attribution(mapping, label)
    require(schema["nation_t9_wire"]["t50_L2_cross_validation"]["evidence_level"]["L3"] == 0,
            "t50 L3 must remain zero")


def build_all() -> tuple[dict[str, Any], str, str, str, bytes, bytes, dict[str, Any]]:
    baseline, baseline_json, baseline_md, _, _ = load_v4()
    data = source_data()
    schema = build_schema(baseline, data)
    markdown = render_markdown(baseline_md, schema)
    validate_schema(schema, baseline, markdown)
    return schema, markdown, render_report(schema), render_done(schema), baseline_json, baseline_md.encode("utf-8"), data


def write_outputs(schema: dict[str, Any], markdown: str, report: str, done: str,
                  baseline_json: bytes, baseline_md: bytes) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if V4_JSON.exists():
        require(sha256_file(V4_JSON) == V4_JSON_SHA256, "existing v4 JSON snapshot hash mismatch")
    else:
        require(sha256_file(PUBLIC_JSON) == V4_JSON_SHA256, "public JSON is not the frozen v4 baseline")
        V4_JSON.write_bytes(baseline_json)
    if V4_MD.exists():
        require(sha256_file(V4_MD) == V4_MD_SHA256, "existing v4 Markdown snapshot hash mismatch")
    else:
        require(sha256_file(PUBLIC_MD) == V4_MD_SHA256, "public Markdown is not the frozen v4 baseline")
        V4_MD.write_bytes(baseline_md)
    expected = {
        PUBLIC_JSON: (json.dumps(schema, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        PUBLIC_MD: markdown.encode("utf-8"),
        OUT_DIR / "REPORT.md": report.encode("utf-8"),
        OUT_DIR / "DONE.md": done.encode("utf-8"),
    }
    for path, content in expected.items():
        if path.exists():
            current = path.read_bytes()
            allowed = {content}
            if path == PUBLIC_JSON:
                allowed.add(baseline_json)
            elif path == PUBLIC_MD:
                allowed.add(baseline_md)
            elif path == OUT_DIR / "DONE.md":
                allowed.add(render_done(schema, verified=False).encode("utf-8"))
            previous_hash = PRIOR_V5_SHA256.get(path.relative_to(ROOT).as_posix())
            recognized_previous = previous_hash is not None and sha256_bytes(current) == previous_hash
            require(current in allowed or recognized_previous, f"refusing to overwrite unexpected file: {path}")
        path.write_bytes(content)
        print(f"WROTE {path.relative_to(ROOT)}")
    if not V4_JSON.exists():
        raise CheckFailure("v4 JSON snapshot write did not persist")
    if not V4_MD.exists():
        raise CheckFailure("v4 Markdown snapshot write did not persist")
    print(f"FROZEN {V4_JSON.relative_to(ROOT)}")
    print(f"FROZEN {V4_MD.relative_to(ROOT)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge accepted t47/t49/t51 findings and E91-accepted t50 L2 data into schema v5 without choosing between conflicting t9 framings.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--selftest", action="store_true", help="validate all sources and preservation rules without writing")
    modes.add_argument("--build", action="store_true", help="write the v5 schema pair and t52 reports")
    args = parser.parse_args(argv)
    try:
        schema, markdown, report, done, baseline_json, baseline_md, _ = build_all()
        if args.selftest:
            print("SELFTEST PASS: protected v4 blocks unchanged; Ntxr 7 L3/2 held; t9 17 L3/13 held; t51 6 L3/5 held; E91 accepts t50 at L2 only with zero L3/L4 field attribution; identity-tail starts cross-walk 251/251 while full spans conflict, no winner; nation totals 30/30/20/7; L4=0")
            return 0
        write_outputs(schema, markdown, report, done, baseline_json, baseline_md)
        print("t52 schema v5 build complete")
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
