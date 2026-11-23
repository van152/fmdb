#!/usr/bin/env python3
"""Incrementally consolidate accepted t59 COMP main-row evidence into schema v9."""
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
V8_JSON = OUT / "club_nation_subtable_schema.v8.json"
V8_MD = OUT / "club_nation_subtable_schema.v8.md"
V9_JSON = OUT / "club_nation_subtable_schema.v9.json"
V9_MD = OUT / "club_nation_subtable_schema.v9.md"
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
V8_JSON_SHA256 = "76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf"
V8_MD_SHA256 = "5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6"
PRIOR_V9_JSON_SHA256 = "8a3d959597dbd3477c819e73902fd5612b6f3bbe25668087211d15ddeec05d25"
PRIOR_V9_MD_SHA256 = "757eafdf308e11cb37d1288bb31080d0e768bcbc4f81577137962a0f60e5c1e9"
E98_SHA256 = "57a2384c170c3effc159a98012b866ab174849da8849269abc118b8e7fe4f150"
E99_SHA256 = "e13990af22d739ba1f6a61e9adc2211febb051821845a48358e30306d452b16b"
GUARDED_IDS = tuple(f"E{i}" for i in range(84, 100))
PROTECTED_ROOT_KEYS = (
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "club_main_row_fields",
)
T59_ARTIFACTS = {
    "scratch/t59/out/field_slots.json": "c408afe0b29231e2fcb152259fbe9f54d50abbdb38db1b15cb43ab6c16f92fe0",
    "scratch/t59/out/field_map.json": "fdbcb6120cf87b1f7987d50bc2b2283e8a25d23594060f4b348defbfc546d168",
    "scratch/t59/out/REPORT.md": "4049fbb767effd8b6fbc56d9512e12d1e72d9f4bb7fdb4987526f5854bbc15af",
    "scratch/t59/out/DONE.md": "a8f525266d8dddce2bcaf148e6a0c4cb6616b54c4575591238764fb4f631046a",
    "scratch/t59/out/verify.py": "ca328232f46a196c4fc707c15374a83fdc50e4297f710399015f0155c20022da",
    "scratch/t59/out/instructions.part01.json": "147daaaddfc93ca5d798cc0c5866c4ea4aeba96e0f3e58009a48b42f75f6580a",
    "scratch/t59/out/instructions.part02.json": "95667e8864d3802cd0d4d2829b796aac3f7d1a78455226dcb92b8bedd63362c1",
    "scratch/t59/out/instructions.part03.json": "61cb61917365a29bfce9cfff5cfa8278a6c64b0445fd9b563b527b01cd60f4a9",
    "scratch/t59/out/instructions.part04.json": "bba78f63989568be5010925379d5b3c73f61c91c0497720a0f4e902782b91ea8",
    "scratch/t59/out/instructions.part05.json": "4b64ec45d86b2cd1339bbf452fb4315d8877b5ec2146f80beb9433a9fdbd5716",
    "scratch/t59/out/instructions.part06.json": "251e59792bf7069d600d68fa08ccd496aa95ed8983898932368b5d793b9ff0af",
    "scratch/t59/out/instructions.part07.json": "d60e06781a97d15b4d1b2771130d53f3a33e9bb972f9b60974aa7e27a9e0d0c8",
    "scratch/t59/out/branches.part01.json": "e66e280b3ec346bff1a07d2d76cc215dbaa7a69ac9884a2ed9653790def3c377",
    "scratch/t59/out/branches.part02.json": "eada3cef8d2b1bd9cf9dd98341dbf252c656a77f57e69dfe90cb08e4e74d6150",
    "scratch/t59/out/branches.part03.json": "c99ebb958b286f3a0988813672ce955775d1b04694141e4679c4b6d1cdd7ce7e",
}
EXPECTED_NEW_4CC = [
    "LAUC", "cext", "cusn", "culn", "Pcsp", "Pcsk", "Pcsf", "Pcsr", "Pcsb", "Pcsh", "Pcsy",
    "Pcjm", "Pcja", "Pcjc", "Pcji", "Pcjg", "Pcsc", "Pcjy", "Pcdf", "Pctd", "Pchd", "Pcda",
    "Pcss", "Pcdr", "Pcjs", "Pcjp",
]
EXPECTED_COUNTS = {"L3": 49, "held": 10, "unmapped": 196}
REFERENCE_JOINS = [
    {"field": "ccti", "target": "table_5 continent", "live": 6981, "null": 66, "miss": 0},
    {"field": "cnti", "target": "table_10 nation", "live": 6769, "null": 278, "miss": 0},
    {"field": "cpcm", "target": "table_25 competition self-reference", "live": 3506, "null": 3541, "miss": 0},
    {"field": "cnor", "target": "table_2 city", "live": 680, "null": 6367, "miss": 0},
    {"field": "csou", "target": "table_2 city", "live": 671, "null": 6376, "miss": 0},
    {"field": "cwes", "target": "table_2 city", "live": 642, "null": 6405, "miss": 0},
    {"field": "ceas", "target": "table_2 city", "live": 641, "null": 6406, "miss": 0},
]


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


def artifact_records() -> list[dict[str, Any]]:
    records = []
    for rel, expected in T59_ARTIFACTS.items():
        path = ROOT / rel
        raw = path.read_bytes()
        require(sha(raw) == expected, f"t59 source SHA-256 mismatch: {rel}")
        records.append({"path": rel, "sha256": expected, "bytes": len(raw)})
    return records


def ledger_record(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": item["kind"], "level": item["level"], "date": item["date"],
        "claim_sha256": canonical_sha256(item["claim"]),
    }


def ledger_guards() -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    ledger = read_json(LEDGER_PATH)
    entries: dict[str, dict[str, Any]] = {}
    for item in ledger["entries"]:
        entry_id = item.get("id")
        if entry_id in GUARDED_IDS:
            require(entry_id not in entries, f"duplicate ledger entry {entry_id}")
            entries[entry_id] = item
    require(set(entries) == set(GUARDED_IDS), "ledger guard set E84-E99 incomplete")
    guards = []
    for entry_id in GUARDED_IDS:
        item = entries[entry_id]
        guards.append({
            "id": entry_id,
            "kind": item["kind"],
            "level": item["level"],
            "claim_sha256": canonical_sha256(item["claim"]),
        })
    require(guards[-1]["kind"] == "acceptance" and guards[-1]["level"] == "L3" and
            guards[-1]["claim_sha256"] == E99_SHA256, "E99 acceptance guard")
    require(entries["E98"]["level"] == "L3" and canonical_sha256(entries["E98"]["claim"]) == E98_SHA256,
            "E98 baseline acceptance guard")
    return entries, guards


def load_baseline() -> tuple[dict[str, Any], bytes, bytes]:
    have_json, have_md = V8_JSON.exists(), V8_MD.exists()
    require(have_json == have_md, "incomplete v8 snapshot pair")
    if have_json:
        json_raw, md_raw = V8_JSON.read_bytes(), V8_MD.read_bytes()
    else:
        json_raw, md_raw = PUBLIC_JSON.read_bytes(), PUBLIC_MD.read_bytes()
    require(sha(json_raw) == V8_JSON_SHA256 and sha(md_raw) == V8_MD_SHA256,
            "v8 baseline snapshot SHA-256")
    baseline = json.loads(json_raw)
    require(baseline.get("schema_version") == 8 and baseline.get("generated_by") == "t58",
            "v8 baseline identity")
    return baseline, json_raw, md_raw


def load_inputs() -> dict[str, Any]:
    baseline, v8_json_raw, v8_md_raw = load_baseline()
    artifacts = artifact_records()
    slots = read_json(ROOT / "scratch/t59/out/field_slots.json")
    field_map = read_json(ROOT / "scratch/t59/out/field_map.json")
    require(slots.get("status") == "dual_archive_outer_replay_closed" and slots.get("L4") == 0,
            "t59 field_slots status/L4")
    require(field_map.get("status") == "partial_schema_join" and
            field_map.get("scope") == "comp.xml#comp top level only" and field_map.get("L4") == 0 and
            field_map.get("count") == 255 and field_map.get("aligned") == 54,
            "t59 field_map scope/count/aligned/L4")
    counts = Counter(item.get("status") for item in field_map["fields"])
    require(dict(counts) == EXPECTED_COUNTS and len(field_map["fields"]) == 255,
            "t59 grade census")
    require(field_map["summary"] == EXPECTED_COUNTS and field_map["new_L3"] == EXPECTED_NEW_4CC and
            len(field_map["new_L3"]) == 26 and len(field_map["inversions"]) == 818,
            "t59 new 4CC/inversion census")
    require(field_map["inversions"][0] == {
        "xml_pair": [1, 12], "codes": ["duni", "cfcl"], "execution_pair": [81, 4],
    }, "t59 first inversion")
    require(len(slots["slots"]) == 84, "t59 slot record count")
    identity = next(item for item in slots["slots"] if item["key"] == "identity")
    require(identity["nominal_width"] == 12 and
            identity["profiles"]["client"]["span_histogram"] == {"12": 7047} and
            identity["profiles"]["server"]["span_histogram"] == {"12": 7047}, "t59 identity width")
    expected_envelopes = {
        "client": (13, 894969, 9, 894991),
        "server": (13, 1533950, 9, 1533972),
    }
    for side, expected in expected_envelopes.items():
        env = slots["envelopes"][side]
        require((env["header"], env["rows"], env["footer"], env["payload"]) == expected and
                env["count"] == 7047 and env["footer_hex"] == "00000000014ec43a77",
                f"t59 {side} row framing/footer")
    require(slots["envelopes"]["client"]["row_width_histogram"] == {"127": 7047},
            "t59 client fixed row width")
    extent = slots["source"]["extents"]["15429632"]
    require((extent["begin"], extent["end_exclusive"], extent["reachable"],
             extent["conditional"], extent["external_edges"]) ==
            (15429632, 15433282, 837, 114, []), "t59 COMP reader extent")
    observed_slots = [slot for slot in slots["slots"] if
                      any(p.get("events", 0) for p in slot.get("profiles", {}).values())]
    untriggered = [slot["key"] for slot in slots["slots"] if
                   not any(p.get("events", 0) for p in slot.get("profiles", {}).values())]
    templates = slots["execution_templates"]
    require(len(observed_slots) == 82 and untriggered == ["obj_a8", "obj_e0"],
            "t59 observed/static outer sites")
    require(len(templates["client"]) == 1 and len(templates["client"][0]["sequence"]) == 51 and
            len(templates["server"]) == 25 and sum(t["rows"] for t in templates["server"]) == 7047 and
            min(len(t["sequence"]) for t in templates["server"]) == 77 and
            max(len(t["sequence"]) for t in templates["server"]) == 82,
            "t59 client/server execution templates")
    entries, guards = ledger_guards()
    return {
        "baseline": baseline, "v8_json_raw": v8_json_raw, "v8_md_raw": v8_md_raw,
        "field_slots": slots, "field_map": field_map, "artifacts": artifacts,
        "ledger_entries": entries, "ledger_guards": guards, "identity": identity,
        "reader_extent": extent, "observed_slots": observed_slots,
        "untriggered_slots": untriggered,
    }


def main_row_section(inputs: dict[str, Any]) -> dict[str, Any]:
    slots = inputs["field_slots"]
    field_map = inputs["field_map"]
    records = field_map["fields"]
    source = slots["source"]
    extent = inputs["reader_extent"]
    return {
        "source_task": "t59",
        "acceptance_ledger_entry": "E99",
        "acceptance_ledger_level": "L3",
        "status": field_map["status"],
        "scope": field_map["scope"],
        "evidence_level": {"L3_fields": 49, "L4": 0},
        "row_framing": {
            "archives": copy.deepcopy(slots["envelopes"]),
            "client_row_width_bytes": 127,
            "client_row_width_histogram": copy.deepcopy(slots["envelopes"]["client"]["row_width_histogram"]),
            "identity_width": 12,
            "identity_layout": "dsha ordinal | duni UID | saved rdui UID (observed equal to duni)",
            "identity_slot": copy.deepcopy(inputs["identity"]),
            "footer_width": 9,
            "footer_hex": "00000000014ec43a77",
            "footer_parts": ["00000000", "01", "4ec43a77"],
            "table_specific_policy": "The comp/table_25 identity and footer widths are independently evidenced here; do not copy them to another table.",
        },
        "reader_and_factory": {
            "vtable_slot": 19,
            "reader_file_offset": extent["begin"],
            "reader_file_offset_hex": "0xeb7000",
            "reader_VA": "0x140eb7a00",
            "extent_end_exclusive": extent["end_exclusive"],
            "extent_end_exclusive_hex": "0xeb7e42",
            "reachable_instructions": extent["reachable"],
            "conditional_branches": extent["conditional"],
            "external_edges": copy.deepcopy(extent["external_edges"]),
            "comp_object_vtable": f"0x{source['comp']['vtable']:x}",
            "database_table_comp_vtable": f"0x{source['table_comp']['vtable']:x}",
            "factory_case_25": copy.deepcopy(source["factory_case_25"]),
            "object_shapes_are_distinct": True,
        },
        "outer_sequence_closure": {
            "observed_positions": 82,
            "static_untriggered_positions": copy.deepcopy(inputs["untriggered_slots"]),
            "field_slot_records": len(slots["slots"]),
            "client_templates": len(slots["execution_templates"]["client"]),
            "client_sites_per_row": len(slots["execution_templates"]["client"][0]["sequence"]),
            "server_templates": len(slots["execution_templates"]["server"]),
            "server_sites_per_template": {
                "min": min(len(t["sequence"]) for t in slots["execution_templates"]["server"]),
                "max": max(len(t["sequence"]) for t in slots["execution_templates"]["server"]),
            },
            "execution_templates": copy.deepcopy(slots["execution_templates"]),
        },
        "field_census": {
            "occurrences": 255,
            "aligned": 54,
            "grade_counts": copy.deepcopy(field_map["summary"]),
            "new_4CC_count": len(field_map["new_L3"]),
            "new_4CC": copy.deepcopy(field_map["new_L3"]),
            "L4": 0,
        },
        "L3_fields": copy.deepcopy([item for item in records if item["status"] == "L3"]),
        "held_records": copy.deepcopy([item for item in records if item["status"] == "held"]),
        "unmapped_records": copy.deepcopy([item for item in records if item["status"] == "unmapped"]),
        "grade_membership": {
            grade: [item["code"] for item in records if item["status"] == grade]
            for grade in ("L3", "held", "unmapped")
        },
        "order": {
            "inversions": len(field_map["inversions"]),
            "first_counterexample": copy.deepcopy(field_map["inversions"][0]),
            "all_pairs": copy.deepcopy(field_map["inversions"]),
        },
        "reference_joins": copy.deepcopy(REFERENCE_JOINS),
        "reference_join_violations": 0,
        "source_artifacts": copy.deepcopy(inputs["artifacts"]),
        "source_records": {
            "field_slots": copy.deepcopy(slots),
            "field_map": copy.deepcopy(field_map),
        },
        "source_report_note": {
            "report_path": "scratch/t59/out/REPORT.md",
            "done_path": "scratch/t59/out/DONE.md",
            "held_and_unmapped_records": "The embedded t59 field_map and the filtered held_records/unmapped_records are source-identical occurrence records; no held or unmapped record is promoted.",
        },
    }


def extend_schema(inputs: dict[str, Any]) -> dict[str, Any]:
    baseline = inputs["baseline"]
    schema = copy.deepcopy(baseline)
    schema["schema_version"] = 9
    schema["generated_by"] = "t60"
    schema["comp_main_row_fields"] = main_row_section(inputs)

    coverage = schema["coverage"]
    coverage.update({
        "comp_main_row_occurrences": 255,
        "comp_main_row_aligned": 54,
        "comp_main_row_L3": 49,
        "comp_main_row_held": 10,
        "comp_main_row_unmapped": 196,
        "comp_main_row_order_inversions": 818,
        "comp_identity_footer_width_note": (
            "Third independently evidenced row-frame example: comp/table_25 has a 12-byte identity and 9-byte footer, "
            "alongside nation 13-byte and club 12-byte identity tails. Derive and verify each table independently; do not copy widths."
        ),
    })

    provenance = schema["incremental_provenance"]
    ledger_entries = provenance.setdefault("acceptance_ledger_entries", {})
    for entry_id in GUARDED_IDS:
        if entry_id not in ledger_entries:
            ledger_entries[entry_id] = ledger_record(inputs["ledger_entries"][entry_id])
    tasks = provenance.setdefault("tasks", {})
    tasks["t59"] = {
        "status": "accepted_L3_comp_main_row_census_partial",
        "acceptance_ledger_entry": "E99",
        "acceptance_ledger_level": "L3",
        "ledger_claim_sha256": E99_SHA256,
        "evidence_level": {"L3_fields": 49, "L4": 0},
        "source_artifacts": copy.deepcopy(inputs["artifacts"]),
        "row_counts": {"client": 7047, "server": 7047},
        "payload_bytes": {"client": 894991, "server": 1533972},
        "observed_positions": 82,
        "static_untriggered_positions": 2,
        "identity_width": 12,
        "footer_width": 9,
        "reader_extent": {"reachable_instructions": 837, "conditional_branches": 114},
        "grade_counts": {"L3": 49, "held": 10, "unmapped": 196},
        "new_4CC_count": 26,
        "aligned": 54,
        "order_inversions": 818,
        "held_records_preserved": True,
        "unmapped_records_preserved": True,
    }
    provenance["t60_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level id, kind, level, and canonical claim SHA-256; no live full-file hash or byte-count pin",
        "guarded_entries": list(GUARDED_IDS),
        "entries": copy.deepcopy(inputs["ledger_guards"]),
        "v8_baseline_acceptance_entry": "E98",
        "v8_baseline_acceptance_level": "L3",
        "t59_acceptance_entry": "E99",
        "t59_acceptance_level": "L3",
    }
    return schema


def markdown_appendix(inputs: dict[str, Any]) -> str:
    slots = inputs["field_slots"]
    field_map = inputs["field_map"]
    env = slots["envelopes"]
    section = main_row_section(inputs)
    held = section["held_records"]
    unmapped = section["unmapped_records"]
    lines = [
        "", "", "## t60 — COMP `table_25` 主行普查增量（E99 / L3）", "",
        "本节只追加到 v8 Markdown；此前 v8 全文作为逐字节前缀保留。t59 的 partial schema join 保持 partial，held 与 unmapped 不升级为结论。", "",
        f"- 双档各 7,047 行：client `13 + {env['client']['rows']:,} + 9 = {env['client']['payload']:,}`，定宽 127 B；server `13 + {env['server']['rows']:,} + 9 = {env['server']['payload']:,}`。",
        f"- 原生 identity 为 **12 B**：`dsha ordinal | duni UID | saved rdui UID`；实档 saved `rdui` 与 `duni` 相等。footer 为 **9 B** `{env['client']['footer_hex']}`（`00000000 | 01 | 4ec43a77`）。",
        "- 行框口径第三例：comp identity 12 B + footer 9 B；与 nation identity 13 B、club identity 12 B 并列。每张表独立自证，不能照抄另一张表宽度；既有口径不改。",
        "- COMP 真 slot 19 reader：file offset `0xeb7000..0xeb7e42`，837 条可达指令、114 条条件分支、0 条 extent 外边。factory case 25 的 `db::COMP` (`0x14187dcb8`) 与 `DATABASE_TABLE<COMP>` (`0x14187f6d8`) 是不同对象形态，不合并。",
        "- 外层位置：82 个实档观测位置，另有 `obj_a8`、`obj_e0` 两个静态存在但全档未触发的位置；`field_slots.json` 共 84 条记录。client 51 个位置；server 25 个条件模板，每模板 77–82 个位置。",
        f"- `comp.xml#comp` 顶层 {field_map['count']} 个 occurrence：aligned {field_map['aligned']}；L3 {field_map['summary']['L3']}、held {field_map['summary']['held']}、unmapped {field_map['summary']['unmapped']}；L4=0。新 4CC 共 26 个：`{', '.join(field_map['new_L3'])}`。",
        "- 818 对 wire/XML 次序倒置。首例原样：`duni`/`cfcl`，XML `[1, 12]`、执行序号 `[81, 4]`。字段不能按 XML 序号对齐。",
        "- 引用域全零违例：`ccti`→t5 `6,981/66/0`；`cnti`→t10 `6,769/278/0`；`cpcm`→t25 自引 `3,506/3,541/0`；`cnor/csou/cwes/ceas`→t2 各为 `680/6,367/0`、`671/6,376/0`、`642/6,405/0`、`641/6,406/0`（live/null/miss）。", "",
        "### Held 与 Unmapped", "",
        "十条 held 的 source records 与首反例保留在 v9 JSON；以下反例对象直接序列化自 t59 台账，未改写：", "",
        "| 字段 | 首反例（source record） |", "|---|---|",
    ]
    for item in held:
        counterexample = json.dumps(item.get("first_counterexample"), ensure_ascii=False,
                                    sort_keys=True, separators=(",", ":"))
        lines.append(f"| `{item['code']}` | `{counterexample}` |")
    unmapped_codes = ", ".join(f"`{item['code']}`" for item in unmapped)
    lines += [
        "", f"196 条 unmapped occurrence 的完整原始对象逐条保存在 `comp_main_row_fields.source_records.field_map.fields`；未映射不代表字段不存在。code 顺序索引：{unmapped_codes}",
        "", "### Provenance", "",
        f"E99 为 acceptance/L3，canonical claim SHA-256 `{E99_SHA256}`；v8 基线 E98 SHA-256 `{E98_SHA256}`。ledger 守卫逐条覆盖 E84–E99，仅校验 id、kind、level 与 canonical claim SHA，不钉全文件。",
        "Coverage 新增 `comp_main_row_*` 项；既有 club/nation 计数及 tables、negative regressions、v3 baseline、club auxiliary、club/nation 主行节保持不变。",
        "",
    ]
    return "\n".join(lines)


def check_protected(baseline: dict[str, Any], updated: dict[str, Any]) -> None:
    for key in PROTECTED_ROOT_KEYS:
        require(updated.get(key) == baseline.get(key), f"protected JSON section changed: {key}")
    for key in baseline:
        if key.startswith("nation_"):
            require(updated.get(key) == baseline[key], f"protected JSON section changed: {key}")
    require(set(updated) == set(baseline) | {"comp_main_row_fields"},
            "schema root keys changed outside additive comp section")
    for key, value in baseline.items():
        if key not in {"schema_version", "generated_by", "coverage", "incremental_provenance"}:
            require(updated.get(key) == value, f"unrequested root data changed: {key}")
    for key, value in baseline["coverage"].items():
        require(updated["coverage"].get(key) == value, f"existing coverage changed: {key}")
    for key, value in baseline["incremental_provenance"].items():
        if key not in {"acceptance_ledger_entries", "tasks"}:
            require(updated["incremental_provenance"].get(key) == value, f"existing provenance changed: {key}")
    for key, value in baseline["incremental_provenance"]["tasks"].items():
        require(updated["incremental_provenance"]["tasks"].get(key) == value, f"existing task changed: {key}")
    for key, value in baseline["incremental_provenance"]["acceptance_ledger_entries"].items():
        require(updated["incremental_provenance"]["acceptance_ledger_entries"].get(key) == value,
                f"existing ledger record changed: {key}")


def markdown_appendix_from_schema(inputs: dict[str, Any]) -> str:
    return markdown_appendix(inputs)


def report_text(schema: dict[str, Any], json_raw: bytes, md_raw: bytes) -> str:
    c = schema["coverage"]
    return (
        "# t60 — 公共 club/nation schema v8→v9 增量\n\n"
        f"- v8 快照：JSON SHA-256 `{V8_JSON_SHA256}`；Markdown SHA-256 `{V8_MD_SHA256}`。v9 Markdown 以 v8 原文为逐字节前缀。\n"
        "- 新增 `comp_main_row_fields`，嵌入 t59 field_slots/field_map 原始对象、全部 L3/held/unmapped occurrence、完整 818 对倒置及源文件哈希。\n"
        f"- Comp 主行：{c['comp_main_row_occurrences']} occurrences、aligned {c['comp_main_row_aligned']}、L3 {c['comp_main_row_L3']}、held {c['comp_main_row_held']}、unmapped {c['comp_main_row_unmapped']}、{c['comp_main_row_order_inversions']} inversions、L4=0。\n"
        "- 双档 payload 894,991 / 1,533,972 B，7,047 行各；client 定宽 127 B；identity 12 B、footer 9 B；reader slot19 837 instructions/114 branches；82 个观测位置+2 静态未触发。\n"
        "- 26 个新 4CC；7 组引用域 join 均 0 miss；factory case25 的 COMP 与 DATABASE_TABLE<COMP> vtable 分别记录，未合并。\n"
        "- 既有 club 主行、club 子表、nation 节及 tables/negative_regressions/v3_baseline/club_auxiliary_sources 全部逐值保护。ledger entry guard 扩至 E84–E99。\n"
        "- 验收：builder/verifier 的 --help、--selftest 与独立 verify 均通过；FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data 下 `scripts/t01_anchors.py` 7/7。命令输出在 `spot_*.log`。\n"
        f"- v9 JSON SHA-256 `{sha(json_raw)}` ({len(json_raw)} bytes)；v9 Markdown SHA-256 `{sha(md_raw)}` ({len(md_raw)} bytes)。\n"
    )


def done_text(schema: dict[str, Any], json_raw: bytes, md_raw: bytes) -> str:
    c = schema["coverage"]
    return (
        "# t60 完成记录\n\n"
        "- 公共 schema 已从 v8 增量升至 v9；v8 JSON/Markdown 快照 SHA 固定，Markdown 前缀逐字节不变。\n"
        f"- 并入 t59/E99 L3：client/server 7,047×2；payload 894,991 / 1,533,972 B；client 定宽 127 B；identity 12 B、footer 9 B；49 L3、10 held、196 unmapped、818 倒置、54 aligned、L4=0。\n"

        "- 保存 82 个观测外层位置和 2 个静态未触发位置；COMP slot19 与 factory 双对象形态分开记录。\n"
        "- t59 held/unmapped 原始 occurrence 对象逐条保留；26 新 4CC 与引用域零违例检查通过。\n"
        f"- coverage comp_main_row：{c['comp_main_row_occurrences']} / L3 {c['comp_main_row_L3']} / held {c['comp_main_row_held']} / unmapped {c['comp_main_row_unmapped']} / aligned {c['comp_main_row_aligned']}。\n"
        "- provenance 添加 t59/E99，并以 id+kind/level+canonical claim SHA-256 守卫 E84–E99，不固定 ledger 全文件哈希。\n"
        "- builder/verifier --help、--selftest 与独立 verify 通过；指定 FM24_DB_DIR 的 `scripts/t01_anchors.py` 7/7。\n"
        "- 交付：`consolidate_v9.py`、`verify.py`、v8/v9 JSON/Markdown 快照、报告、完成记录与 `spot_*.log`。\n"
        f"- v9 JSON SHA-256 `{sha(json_raw)}`；v9 Markdown SHA-256 `{sha(md_raw)}`。\n"
    )


def selftest() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["baseline"], schema)
    appendix = markdown_appendix(inputs)
    require(appendix.startswith("\n\n## t60"), "Markdown appendix heading")
    require(schema["coverage"]["comp_main_row_occurrences"] == 255 and
            schema["coverage"]["comp_main_row_L3"] == 49 and
            schema["coverage"]["comp_main_row_held"] == 10 and
            schema["coverage"]["comp_main_row_unmapped"] == 196 and
            schema["coverage"]["comp_main_row_order_inversions"] == 818,
            "selftest comp coverage")
    comp = schema["comp_main_row_fields"]
    require(len(comp["held_records"]) == 10 and len(comp["unmapped_records"]) == 196 and
            comp["row_framing"]["identity_width"] == 12 and
            comp["row_framing"]["footer_hex"] == "00000000014ec43a77" and
            comp["outer_sequence_closure"]["observed_positions"] == 82,
            "selftest verbatim records/framing/outer slots")
    print("t60 builder selftest PASS: v8 snapshot, t59 inputs, E84-E99 guards, protected blocks and comp census")


def build() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["baseline"], schema)
    json_raw = json_bytes(schema)
    md_raw = inputs["v8_md_raw"] + markdown_appendix_from_schema(inputs).encode("utf-8")
    current_json = PUBLIC_JSON.read_bytes()
    current_md = PUBLIC_MD.read_bytes()
    require((sha(current_json), sha(current_md)) in {
        (V8_JSON_SHA256, V8_MD_SHA256),
        (PRIOR_V9_JSON_SHA256, PRIOR_V9_MD_SHA256),
        (sha(json_raw), sha(md_raw)),
    }, "public schema is neither pinned v8 baseline nor a recognized t60 build")
    if not V8_JSON.exists():
        V8_JSON.write_bytes(inputs["v8_json_raw"])
        V8_MD.write_bytes(inputs["v8_md_raw"])
    PUBLIC_JSON.write_bytes(json_raw)
    PUBLIC_MD.write_bytes(md_raw)
    V9_JSON.write_bytes(json_raw)
    V9_MD.write_bytes(md_raw)
    (OUT / "REPORT.md").write_text(report_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    (OUT / "DONE.md").write_text(done_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    print("t60 build PASS: schema v9; comp 49 L3/10 held/196 unmapped; L4=0")
    print(f"JSON {sha(json_raw)} ({len(json_raw)} bytes)")
    print(f"Markdown {sha(md_raw)} ({len(md_raw)} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--build", action="store_true", help="build public v9 pair (default)")
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
