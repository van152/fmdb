#!/usr/bin/env python3
"""Incrementally consolidate accepted t55 nation main-row fields into schema v7."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V5_JSON = OUT / "club_nation_subtable_schema.v5.json"
V5_MD = OUT / "club_nation_subtable_schema.v5.md"
V6_JSON = OUT / "club_nation_subtable_schema.v6.json"
V6_MD = OUT / "club_nation_subtable_schema.v6.md"
V5_JSON_SHA256 = "03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184"
V5_MD_SHA256 = "4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009"
V6_JSON_SHA256 = "02751ef7c79c60dfcf14bfbad5fe10e2077f15ed753d12e9ebfa1dfbbc010f44"
V6_MD_SHA256 = "a8d6509b090cd16ed7bf3d89c37638e23da120cbcfcc9e80424bd01a82234ac6"
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
T55_ARTIFACTS = {
    "scratch/t55/out/field_slots.json": "1625560fa99e635cdf60e10c108fedf799c359790adcfba429fc205edcfbcd17",
    "scratch/t55/out/field_map.json": "6828a434cff296af0a63471bff8deeb2edbcb0d2226cd3665955797c373137a4",
    "scratch/t55/out/abc_closure.json": "8fbce6d9ebc32d2d950d45c4c7fb35ca88d8095e26f8f045c564b06f45388153",
    "scratch/t55/out/instructions.part001.json": "32f4c3b017f47b736ddc5de425a7b9725ddd710f9bb008d73d545505d4206a0e",
    "scratch/t55/out/instructions.part002.json": "e50e8d1f2bb779bb13655a44be97296122740308854ec5e3da124880ec1e8de1",
    "scratch/t55/out/instructions.part003.json": "72158705e606f97321720a8ccb5a33037d7ff2277065c5ee4dcc262c4ac5f850",
    "scratch/t55/out/branches.part001.json": "bf7308fd411e23e43429be95090c4a093d862fd3731cbd64e86811346c741b48",
    "scratch/t55/out/verify.py": "fd8775d27dfb48bc71455c80fc33f5d5a32d4244760b69a70522c3d77488e7bf",
    "scratch/t55/out/REPORT.md": "9cbf22d1883cc200ef9f0da699828f71a1b23546381ef63dbb6a644cce058065",
    "scratch/t55/out/DONE.md": "05f3626869bd5daa5593277918f61129d4a91a7af28690f95dc66fcb51e80c50",
    "scripts/t55_natmain_fields.py": "350bf0cfe2fac90e90c4057cd313067e6e0cfaed878a2f5056a26a2ba83be27b",
}
INTERIM_V7_JSON_SHA256 = "b352fa7f39f5bbabea2be5a4a42ff4e4edc38a99200981a1dd95676151c6fa05"
INTERIM_V7_MD_SHA256 = "f4c47c4778eb64e302c592b33c651e7d378e55afc60dce61e24be71f9c87604c"
PREVIOUS_V7_JSON_SHA256 = "f9db4bcc18ff4853ec09182c8ef9e3aa9ba20e5f2511087975c348747b402241"
PREVIOUS_V7_MD_SHA256 = "f84d265c2ca067794bd98f8ddb15cda026dc2b63bd185bd3db0eab43bd6b83bc"
E94_SHA256 = "358243779bba359656ecae6804cea9cea26b1739ffce5bf96a2599d735263c89"
E95_SHA256 = "2632aaae869ee3a5c1020d82e409f1f26ad429d077f06f078d5f7f1058f43eb1"
PREVIOUS_GUARD_IDS = ("E87", "E89", "E90", "E91", "E92", "E93")
JSON_PROTECTED_KEYS = (
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_data_side_status", "nation_static_side", "nation_t9_wire",
)
COVERAGE_ALLOWED_KEYS = {
    "nation_side", "nation_L3_occurrences", "nation_L3_unique_wire_fields",
    "nation_L3_unique_wire_field_ids", "nation_held_occurrences", "nation_coverage_policy",
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


def verify_file(path: Path, expected: str) -> bytes:
    raw = path.read_bytes()
    require(sha(raw) == expected, f"SHA-256 mismatch: {path.relative_to(ROOT)}")
    return raw


def load_inputs() -> dict[str, Any]:
    verify_file(V5_JSON, V5_JSON_SHA256)
    verify_file(V5_MD, V5_MD_SHA256)
    v6_json_raw = verify_file(V6_JSON, V6_JSON_SHA256)
    v6_md_raw = verify_file(V6_MD, V6_MD_SHA256)
    v5 = read_json(V5_JSON)
    v6 = json.loads(v6_json_raw)
    require(v5.get("schema_version") == 5, "v5 snapshot version")
    require(v6.get("schema_version") == 6 and v6.get("generated_by") == "t54", "v6 snapshot identity")
    t55: dict[str, Any] = {}
    for rel, expected in T55_ARTIFACTS.items():
        path = ROOT / rel
        verify_file(path, expected)
        if rel.endswith(".json") and rel in (
            "scratch/t55/out/field_slots.json", "scratch/t55/out/field_map.json", "scratch/t55/out/abc_closure.json"
        ):
            t55[Path(rel).name] = read_json(path)
    field_slots = t55["field_slots.json"]
    field_map = t55["field_map.json"]
    abc = t55["abc_closure.json"]
    require(field_slots["source"]["entry"] == 17038016 and
            field_slots["source"]["end_exclusive"] == 17042404 and
            field_slots["source"]["reachable"] == 992 and
            field_slots["source"]["stream_slot_28_count"] == 40, "t55 CFG/source bounds")
    require(field_slots["status"] == "main_row_census_complete_for_two_archive_modes_names_partial" and
            field_slots["L4"] == field_map["L4"] == 0, "t55 partial/L4 boundary")
    require(field_map["fields_total"] == 346 and field_map["positions_with_unique_XML"] == 15 and
            field_map["grade_counts"] == {
                "L3": 5, "held": 5, "linked_parent_held": 1, "no_main_wire_slot": 1,
                "no_wire_slot": 1, "prior_collection": 5, "prior_identity": 1, "unmapped": 327,
            }, "t55 field census/grade counts")
    require(abc["status"] == "A_B_C_D_explained_for_both_modes" and
            set(abc["segments"]) == set("ABCD"), "t55 ABC closure")
    require(sha(LEDGER_PATH.read_bytes()) != "", "ledger readable")
    ledger_doc = read_json(LEDGER_PATH)
    entries: dict[str, dict[str, Any]] = {}
    for item in ledger_doc["entries"]:
        entry_id = item.get("id")
        if entry_id in (*PREVIOUS_GUARD_IDS, "E94", "E95"):
            require(entry_id not in entries, f"duplicate ledger entry {entry_id}")
            entries[entry_id] = item
    require(set(entries) == {*PREVIOUS_GUARD_IDS, "E94", "E95"}, "required ledger entries missing")
    for entry_id in PREVIOUS_GUARD_IDS:
        expected = v6["incremental_provenance"]["acceptance_ledger_entries"][entry_id]
        actual = entries[entry_id]
        require(actual.get("kind") == expected.get("kind") and actual.get("level") == expected.get("level") and
                canonical_sha256(actual.get("claim")) == expected.get("claim_sha256"),
                f"baseline ledger entry mismatch: {entry_id}")
    for entry_id, kind, level, expected_sha in (
        ("E94", "acceptance", "L3", E94_SHA256),
        ("E95", "acceptance", "L2", E95_SHA256),
    ):
        actual = entries[entry_id]
        require(actual.get("kind") == kind and actual.get("level") == level and
                canonical_sha256(actual.get("claim")) == expected_sha,
                f"new ledger entry mismatch: {entry_id}")
    return {
        "v5": v5, "v6": v6, "v6_json_raw": v6_json_raw, "v6_md_raw": v6_md_raw,
        "field_slots": field_slots, "field_map": field_map, "abc": abc,
        "ledger_entries": entries,
    }


def artifact_records() -> list[dict[str, Any]]:
    records = []
    for rel, expected in T55_ARTIFACTS.items():
        path = ROOT / rel
        records.append({"path": rel, "sha256": expected, "bytes": path.stat().st_size})
    return records


def ledger_record(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": item["kind"], "level": item["level"], "date": item["date"],
        "claim_sha256": canonical_sha256(item["claim"]),
    }


def main_row_section(inputs: dict[str, Any]) -> dict[str, Any]:
    slots = inputs["field_slots"]
    field_map = inputs["field_map"]
    abc = inputs["abc"]
    records = field_map["fields"]
    by_pos = {slot["position"]: slot for slot in slots["slots"]}
    aligned = sorted((r for r in records if r["grade"] == "L3"), key=lambda item: item["slot"])
    grade_membership: dict[str, list[str]] = {}
    for item in records:
        grade_membership.setdefault(item["grade"], []).append(item["code"])
    l3_fields = []
    for item in aligned:
        slot = by_pos[item["slot"]]
        profiles = slot["domain_profiles"]
        l3_fields.append({
            "code": item["code"], "xml_index": item["xml_index"], "wire_position": item["slot"],
            "type": slot["type"], "object_displacement": slot["object_displacement"],
            "modes": slot["modes"], "execution_index": slot["execution_index"],
            "target_table": slot.get("target_table"), "domain_profiles": profiles,
        })
    old_order = inputs["v6"]["coverage"]["nation_L3_unique_wire_field_ids"]
    new_ids = ["t10/main/Nnsi", "t10/main/Ncti", "t10/main/Nrgi", "t10/main/Ncur", "t10/main/Nndn"]
    require(all(record["code"] in {x["code"] for x in aligned} for record in aligned), "internal L3 record set")
    require(set(new_ids).isdisjoint(old_order), "t55 IDs overlap existing nation identities")
    return {
        "source_task": "t55",
        "acceptance_ledger_entry": "E94",
        "acceptance_ledger_level": "L3",
        "status": field_slots_status(slots),
        "scope": field_map["scope"],
        "evidence_level": {"L3_fields": field_map["domain_pass_L3"], "L4": field_map["L4"]},
        "outer_sequence_closure": {
            "entry_file_offset": slots["source"]["entry"],
            "end_exclusive_file_offset": slots["source"]["end_exclusive"],
            "reachable_instructions": slots["source"]["reachable"],
            "external_edges": slots["source"]["external_edges"],
            "stream_slot_28_count": slots["source"]["stream_slot_28_count"],
            "positions": {"server": 40, "client": 15},
            "archive_modes": {
                side: {k: env[k] for k in ("header", "body", "rows", "footer_at", "footer")}
                for side, env in slots["envelopes"].items()
            },
        },
        "field_census": {
            "fields_total": field_map["fields_total"],
            "positions_with_unique_XML": field_map["positions_with_unique_XML"],
            "alignment_ratio": field_map["alignment_ratio"],
            "grade_counts": copy.deepcopy(field_map["grade_counts"]),
        },
        "L3_fields": l3_fields,
        "grade_membership": grade_membership,
        "order": copy.deepcopy(field_map["order"]),
        "ordering_policy": "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐",
        "abc_closure_reference": {
            "source_task": "t55", "path": "scratch/t55/out/abc_closure.json",
            "sha256": T55_ARTIFACTS["scratch/t55/out/abc_closure.json"],
            "status": abc["status"], "formula": abc["formula"],
            "segments": copy.deepcopy(abc["segments"]),
            "source_record": copy.deepcopy(abc),
            "verification_note": (
                "The t55 independent verifier checks each of 251 rows per mode for count-width plus item-stride span, "
                "adjacent segment boundaries, and byte-for-byte equality of each A/B/C/D segment across modes."
            ),
        },
        "source_artifacts": artifact_records(),
        "source_records": {
            "field_slots": copy.deepcopy(slots),
            "field_map": copy.deepcopy(field_map),
        },
    }


def field_slots_status(slots: dict[str, Any]) -> str:
    return slots["status"]


def extend_schema(inputs: dict[str, Any]) -> dict[str, Any]:
    baseline = inputs["v6"]
    schema = copy.deepcopy(baseline)
    schema["schema_version"] = 7
    schema["generated_by"] = "t56"
    schema["nation_main_row_fields"] = main_row_section(inputs)

    coverage = schema["coverage"]
    old_ids = list(coverage["nation_L3_unique_wire_field_ids"])
    new_ids = ["t10/main/Nnsi", "t10/main/Ncti", "t10/main/Nrgi", "t10/main/Ncur", "t10/main/Nndn"]
    require(not (set(old_ids) & set(new_ids)), "duplicate nation L3 wire identity")
    coverage["nation_L3_unique_wire_field_ids"] = [*old_ids, *new_ids]
    coverage["nation_L3_occurrences"] += 5
    coverage["nation_L3_unique_wire_fields"] += 5
    coverage["nation_held_occurrences"] += inputs["field_map"]["grade_counts"]["held"]
    coverage["nation_coverage_policy"] += (
        " t55 adds five accepted table_10 main-row L3 occurrences; the five source-grade held fields are counted "
        "as held and remain distinct from linked_parent_held, no_main_wire_slot, no_wire_slot, and unmapped. "
        "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐。46 个倒置对的首例为 wire pos 1 Nnsi（XML 21）先于 pos 15 Ncti（XML 16）。"
    )
    coverage["nation_side"]["t55_main_row_census"] = {
        "source_task": "t55", "acceptance_ledger_entry": "E94", "acceptance_ledger_level": "L3",
        "fields_total": 346, "positions_with_unique_XML": 15, "L3_fields": 5, "L4": 0,
        "grade_counts": copy.deepcopy(inputs["field_map"]["grade_counts"]),
        "abc_closure_path": "scratch/t55/out/abc_closure.json",
        "abc_closure_sha256": T55_ARTIFACTS["scratch/t55/out/abc_closure.json"],
    }

    provenance = schema["incremental_provenance"]
    ledger_entries = provenance.setdefault("acceptance_ledger_entries", {})
    ledger_entries["E94"] = ledger_record(inputs["ledger_entries"]["E94"])
    ledger_entries["E95"] = ledger_record(inputs["ledger_entries"]["E95"])
    tasks = provenance.setdefault("tasks", {})
    tasks["t55"] = {
        "status": "accepted_L3_nation_main_row_census_names_partial",
        "acceptance_ledger_entry": "E94",
        "acceptance_ledger_level": "L3",
        "ledger_claim_sha256": E94_SHA256,
        "evidence_level": {"L3_fields": 5, "L4": 0},
        "source_artifacts": artifact_records(),
        "grade_counts": copy.deepcopy(inputs["field_map"]["grade_counts"]),
        "order_inversions": 46,
        "held_records_preserved": True,
        "unmapped_records_preserved": True,
    }
    provenance["t56_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level canonical claim SHA-256 plus id/kind/level; no live full-file hash or byte-count pin",
        "guarded_entries": [*PREVIOUS_GUARD_IDS, "E94", "E95"],
        "v6_baseline_acceptance_entry": "E95",
        "v6_baseline_acceptance_level": "L2",
        "t55_acceptance_entry": "E94",
        "t55_acceptance_level": "L3",
    }
    return schema


def markdown_appendix(inputs: dict[str, Any]) -> str:
    field_map = inputs["field_map"]
    slot_doc = inputs["field_slots"]
    abc = inputs["abc"]
    by_pos = {slot["position"]: slot for slot in slot_doc["slots"]}
    records = {item["code"]: item for item in field_map["fields"]}
    display = [
        ("Nnsi", 21, "Stadium", 21), ("Ncti", 16, "Continent", 5),
        ("Nrgi", 17, "Region", 19), ("Ncur", 20, "Currency", 41),
        ("Nndn", 29, "u16 bitfield", None),
    ]
    lines = [
        "", "", "## t56 — t55 Nation `table_10` 主行槽位增量（E94 / L3）", "",
        "本节为 v6 Markdown 的追加内容；此前 v6 全文保持为逐字节前缀。它记录顶层冻结 `nation.xml#nation` 的主行候选，不改写旧 t46 文本、负例、`nation_data_side_status` 或 `nation_t9_wire`。完整 346 项原台账、40 槽坐标和 A/B/C/D 证据以 SHA 固定在 v7 JSON 的 `nation_main_row_fields.source_records`。", "",
        f"- 外层 reader：server 40 / client 15 个位置；CFG `0x{slot_doc['source']['entry']:x}..0x{slot_doc['source']['end_exclusive']:x}` 可达 {slot_doc['source']['reachable']} 指令、无 extent 外边；两档各 251 行。",
        f"- 字段分母：{field_map['fields_total']}；唯一 XML 对齐 {field_map['positions_with_unique_XML']}（{field_map['alignment_ratio'] * 100:.2f}%）；L3 {field_map['domain_pass_L3']}，L4 {field_map['L4']}。",
        "- wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐。46 个倒置对的首例是 wire pos 1 `Nnsi` / XML 21，先于 wire pos 15 `Ncti` / XML 16。", "", 
        "| Wire pos | 字段 / XML index | 站点 / 对象位移 | L3 域证据 |",
        "|---:|---|---|---|",
    ]
    for code, xml_index, target_name, target_id in display:
        item = records[code]
        slot = by_pos[item["slot"]]
        if code == "Nndn":
            profile = slot["domain_profiles"]["server"]
            proof = f"server u16 mask `0x0200`: `{profile['decoded'].get('0', 0)}` false / `{profile['decoded'].get('1', 0)}` true; client bypass"
        else:
            profile = slot["domain_profiles"]["server"]
            proof = f"table_{target_id} {target_name} {profile['hit']}/{profile['miss']}/{profile['null']} hit/miss/null"
            if "client" in slot["domain_profiles"] and slot["domain_profiles"]["client"].get("rows", 0):
                client = slot["domain_profiles"]["client"]
                proof += f"; client {client['hit']}/{client['miss']}/{client['null']}"
            else:
                proof += "; client bypass"
        lines.append(
            f"| {item['slot']} | `{code}` / {xml_index} | `0x{slot['site']:x}` / `+0x{slot['object_displacement']:x}` | {proof} |"
        )
    grades = field_map["grade_counts"]
    membership: dict[str, list[str]] = {}
    for item in field_map["fields"]:
        membership.setdefault(item["grade"], []).append(item["code"])
    lines += [
        "", "### 等级与保留边界", "",
        f"`grade_counts` 原样：L3 {grades['L3']}、held {grades['held']}、linked_parent_held {grades['linked_parent_held']}、no_main_wire_slot {grades['no_main_wire_slot']}、no_wire_slot {grades['no_wire_slot']}、prior_collection {grades['prior_collection']}、prior_identity {grades['prior_identity']}、unmapped {grades['unmapped']}（合计 {sum(grades.values())}）。完整 held/unmapped occurrence 和首反例均保留于嵌入的 t55 `field_map.json`；Npop 是不在活动 schema 的 supplemental，不计入 346。",
        f"- held：`{', '.join(membership.get('held', []))}`；linked_parent_held：`{', '.join(membership.get('linked_parent_held', []))}`；prior_collection：`{', '.join(membership.get('prior_collection', []))}`；prior_identity：`{', '.join(membership.get('prior_identity', []))}`。",
        f"- no_main_wire_slot：`{', '.join(membership.get('no_main_wire_slot', []))}`；no_wire_slot：`{', '.join(membership.get('no_wire_slot', []))}`。台账原标签是 `EDsc=held`、`TCrs=no_main_wire_slot`、`EDfx=no_wire_slot`，不互换。",
        "- `Necf` / `Nygn` 因 schema 域冲突及首反例 held；`Ngct` / `Nsod` 缺 scoped `enum_ref`；不把候选晋级。", "",
        "### t46 A/B/C/D 收口", "",
        f"解释沿用 t55 的 `abc_closure.json`（SHA-256 `{T55_ARTIFACTS['scratch/t55/out/abc_closure.json']}`）；t46 原始负例和 v6 中的开放状态文字不改写。公式：{abc['formula']}。",
        "| 段 / 字段 | 位置 / 对象位移 | stride | 首行 count 绝对位置 client/server | 两档 items | 双档 count 分布相同 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for letter in "ABCD":
        segment = abc["segments"][letter]
        c, s = segment["profiles"]["client"], segment["profiles"]["server"]
        same = c["counts"] == s["counts"] and c["items"] == s["items"] and c["rows"] == s["rows"]
        require(same, f"ABC profile mismatch: {letter}")
        lines.append(
            f"| {letter} / `{segment['parent']}` | pos {segment['position']} / `+0x{segment['object_displacement']:x}` | "
            f"{segment['item_stride']} B | {c['first']['start']} / {s['first']['start']} | {c['items']} / {s['items']} | yes |"
        )
    lines += [
        "", "t55 的独立 verifier 对两档各 251 行逐行核验 count-width + item-stride 消费跨度、相邻段边界和 A/B/C/D 原始消费字节相同。表中的 count 分布也逐档一致。该闭合只解释四个已识别集合，不为其余未命名标量赋义。", "",
        "### 来源与 ledger", "",
        f"t55 acceptance `E94`：kind `acceptance` / level `L3` / canonical claim SHA-256 `{E94_SHA256}`。v6 基线 acceptance `E95`：kind `acceptance` / level `L2` / canonical claim SHA-256 `{E95_SHA256}`。守卫只钉条目 ID、claim SHA、kind、level，不钉 live ledger 全文件哈希。", "",
    ]
    return "\n".join(lines)


def check_protected(baseline: dict[str, Any], updated: dict[str, Any]) -> None:
    for key in JSON_PROTECTED_KEYS:
        require(updated.get(key) == baseline.get(key), f"protected JSON section changed: {key}")
    for key, value in baseline.items():
        if key not in {"schema_version", "generated_by", "coverage", "incremental_provenance", "nation_main_row_fields"}:
            require(updated.get(key) == value, f"unrequested root key changed: {key}")
    old_coverage = baseline["coverage"]
    new_coverage = updated["coverage"]
    for key, value in old_coverage.items():
        if key not in COVERAGE_ALLOWED_KEYS:
            require(new_coverage.get(key) == value, f"non-nation coverage changed: {key}")
    old_side = copy.deepcopy(old_coverage["nation_side"])
    new_side = copy.deepcopy(new_coverage["nation_side"])
    new_side.pop("t55_main_row_census", None)
    require(new_side == old_side, "existing nation-side coverage changed")
    old_prov = baseline["incremental_provenance"]
    new_prov = updated["incremental_provenance"]
    for key, value in old_prov.items():
        if key not in {"acceptance_ledger_entries", "tasks"}:
            require(new_prov.get(key) == value, f"existing provenance changed: {key}")
    for key, value in old_prov["acceptance_ledger_entries"].items():
        require(new_prov["acceptance_ledger_entries"].get(key) == value, f"existing ledger provenance changed: {key}")
    for key, value in old_prov["tasks"].items():
        require(new_prov["tasks"].get(key) == value, f"existing task provenance changed: {key}")


def report_text(schema: dict[str, Any], public_json: bytes, public_md: bytes) -> str:
    coverage = schema["coverage"]
    section = schema["nation_main_row_fields"]
    return (
        "# t56 — 公共 club/nation schema v7 增量\n\n"
        "## 变更\n\n"
        "- 基线：v6/t54 JSON 与 Markdown 快照 SHA 固定；Markdown 旧内容逐字节保留为新文件前缀。\n"
        "- 新增 `nation_main_row_fields`：嵌入 t55 全量 field_map、field_slots 与 ABC closure 结构记录，并固定来源 artifact SHA。\n"
        f"- Nation 汇总：L3 occurrences {coverage['nation_L3_occurrences']}、unique wire fields {coverage['nation_L3_unique_wire_fields']}、held occurrences {coverage['nation_held_occurrences']}、negative records {coverage['nation_negative_records']}；L4=0。\n"
        "- 新增 t55/E94 L3 与 v6 基线 E95/L2 的 entry-level ledger 记录；不比较 live ledger 全文件哈希。\n"
        "- 保持 `tables`、`negative_regressions`、`v3_baseline`、club 计数、`club_auxiliary_sources`、`nation_data_side_status`、`nation_static_side`、`nation_t9_wire` 原值。\n\n"
        "## 验收\n\n"
        f"- t55：{section['outer_sequence_closure']['reachable_instructions']} CFG instructions；40/15 positions；251+251 rows；15/346 XML alignments；L3=5、L4=0。\n"
        "- t55 source independent verifier passed before consolidation; t56 builder selftest, independent verify, spot checks, and anchors are recorded in `spot_*.log`.\n"
        f"- v7 JSON SHA-256 `{sha(public_json)}` ({len(public_json)} bytes); v7 Markdown SHA-256 `{sha(public_md)}` ({len(public_md)} bytes).\n"
    )


def done_text(schema: dict[str, Any], public_json: bytes, public_md: bytes) -> str:
    c = schema["coverage"]
    return (
        "# t56 完成记录\n\n"
        "- 公共 schema 已从 v6 增量升至 v7；旧 Markdown 全文保持为前缀，指定 JSON 保护节逐值不变。\n"
        "- 并入 t55/E94：5 L3、346 顶层字段、15 个唯一 XML 对齐、46 个 wire/XML 顺序倒置；held/unmapped 与 t55 原台账一致；L4=0。\n"
        "- Nation 汇总：L3 occurrences {l3}、unique {unique}、held {held}、negative records {neg}。\n"
        "- t46 A/B/C/D 解释作为 t55 新节引用；旧 t46 文本、负例、`nation_data_side_status` 不改写。\n"
        "- 交付：`consolidate_v7.py`、`verify.py`、`scripts/t56_spot_v7.py`、v5/v6/v7 快照、报告、完成记录及 `spot_*.log`。\n"
        "- JSON SHA-256 `{jsha}`；Markdown SHA-256 `{msha}`。\n"
    ).format(
        l3=c["nation_L3_occurrences"], unique=c["nation_L3_unique_wire_fields"],
        held=c["nation_held_occurrences"], neg=c["nation_negative_records"],
        jsha=sha(public_json), msha=sha(public_md),
    )


def selftest() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["v6"], schema)
    appendix = markdown_appendix(inputs).encode("utf-8")
    require(appendix.startswith(b"\n\n## t56"), "Markdown appendix heading")
    require(schema["coverage"]["nation_L3_occurrences"] == 35 and
            schema["coverage"]["nation_L3_unique_wire_fields"] == 35 and
            schema["coverage"]["nation_held_occurrences"] == 25, "selftest counters")
    require(schema["incremental_provenance"]["tasks"]["t55"]["ledger_claim_sha256"] == E94_SHA256,
            "selftest E94 pin")
    print("t56 builder selftest PASS: snapshots, entry guards, protected blocks, five L3, additive ABC and counters")


def build() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["v6"], schema)
    json_raw = json_bytes(schema)
    md_raw = inputs["v6_md_raw"] + markdown_appendix(inputs).encode("utf-8")
    current_json = PUBLIC_JSON.read_bytes()
    current_md = PUBLIC_MD.read_bytes()
    allowed_json = {V6_JSON_SHA256, INTERIM_V7_JSON_SHA256, PREVIOUS_V7_JSON_SHA256, sha(json_raw)}
    allowed_md = {V6_MD_SHA256, INTERIM_V7_MD_SHA256, PREVIOUS_V7_MD_SHA256, sha(md_raw)}
    require(sha(current_json) in allowed_json and sha(current_md) in allowed_md,
            "public schema is neither pinned v6 baseline nor this deterministic v7 build")
    PUBLIC_JSON.write_bytes(json_raw)
    PUBLIC_MD.write_bytes(md_raw)
    (OUT / "club_nation_subtable_schema.v7.json").write_bytes(json_raw)
    (OUT / "club_nation_subtable_schema.v7.md").write_bytes(md_raw)
    (OUT / "REPORT.md").write_text(report_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    (OUT / "DONE.md").write_text(done_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    print(f"t56 build PASS: schema v7; nation L3 {schema['coverage']['nation_L3_occurrences']}/unique {schema['coverage']['nation_L3_unique_wire_fields']}/held {schema['coverage']['nation_held_occurrences']}; L4=0")
    print(f"JSON {sha(json_raw)} ({len(json_raw)} bytes)")
    print(f"Markdown {sha(md_raw)} ({len(md_raw)} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--build", action="store_true", help="build public v7 pair (default)")
    group.add_argument("--selftest", action="store_true", help="run read-only builder checks")
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
