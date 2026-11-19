#!/usr/bin/env python3
"""Incrementally consolidate accepted t57 club table_3 main-row fields into schema v8."""
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
V7_JSON = OUT / "club_nation_subtable_schema.v7.json"
V7_MD = OUT / "club_nation_subtable_schema.v7.md"
V8_JSON = OUT / "club_nation_subtable_schema.v8.json"
V8_MD = OUT / "club_nation_subtable_schema.v8.md"
V7_JSON_SHA256 = "d93a5070489c737e5d70fa2b8ffb135f9d4135d70df7ae4b6e2d27a4379ded10"
V7_MD_SHA256 = "f84d265c2ca067794bd98f8ddb15cda026dc2b63bd185bd3db0eab43bd6b83bc"
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
E96_SHA256 = "8fa14c406df939da7d1024eccdb2ed26e876071f9efef64270a998b9eb74cc92"
E97_SHA256 = "ba5a1079403dd970b30c9304a90c37d5a66f3d28163ee2cf2588fd355129ff32"
OLD_GUARDS = ("E87", "E89", "E90", "E91", "E92", "E93", "E94", "E95")
NEW_GUARDS = ("E96", "E97")
PROTECTED_ROOT_KEYS = (
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_data_side_status", "nation_static_side", "nation_t9_wire",
    "nation_main_row_fields",
)
EXPECTED_L3 = [
    "duni", "Cext", "Cedp", "Cnti", "Cbni", "Cccn", "Cncl",
    "Ccty", "CIns", "CASt", "Csot", "Ctsi", "CnCV",
]
EXPECTED_NEW_L3 = ["Cext", "Cedp", "Cncl", "CIns", "Ctsi"]
EXPECTED_GRADES = {
    "L3": 13,
    "held": 11,
    "skipped_separate_member": 10,
    "unmapped": 399,
}
T57_ARTIFACTS = {
    "scratch/t57/out/field_slots.json": "da3d3abd76e3d96a4db989c2dec3fcc1d352d1ccaac5267b00ab12731bbd6489",
    "scratch/t57/out/field_map.json": "0b04de7b15c455ccb85212d43221d5cbecb8fd5ccbf830ba71d5f4f3011f3664",
    "scratch/t57/out/instructions.part001.json": "c64bff5a17030f28ee0421ae0b3985b1eefd128deb881e8c0f123a3341d78050",
    "scratch/t57/out/instructions.part002.json": "4337bb0938b35a58cb153337126696819489ca4a36e16c5abc92cc2cf0d50468",
    "scratch/t57/out/instructions.part003.json": "f411ce54f3efa13bd2c5e42ec6d36a2572a6b5142807b94731a03ba311c8b6cd",
    "scratch/t57/out/instructions.part004.json": "462a0be204e0773ef66187d6f48c7d84c052525c5f53b6caca89a96ff6e56e13",
    "scratch/t57/out/instructions.part005.json": "0c31d8463915377c5047bd939a70c5a6c16bd769003ae5e325a37decb8f45430",
    "scratch/t57/out/instructions.part006.json": "b1a0181c75624ed0f718e6b57df419fcb0056341804a2a5210dc3526201f93ef",
    "scratch/t57/out/instructions.part007.json": "92af197f476d2a24ec3da7194d0ce4965b5698440fa322f814c7ca50aa58bc14",
    "scratch/t57/out/instructions.part008.json": "abca0e9f801141ff790b615c65644e961cf9298d5093ee492506499b39dc5697",
    "scratch/t57/out/instructions.part009.json": "a929a281336715b5c2607614fe609bbfbbf0d363102e24d58382251efff5d6b3",
    "scratch/t57/out/branches.part001.json": "078d39d16dedf15bb40f7a71f2eef622e08976fc70b00702a91985feeab931f5",
    "scratch/t57/out/branches.part002.json": "f568689b41f98df396c31ead1af542a243a9e813b006b5a49e2337bb5a830a63",
    "scratch/t57/out/branches.part003.json": "a5f49fb76eb87588e21c70d628c8f80cfcc574dcadfd5467626c26ecbdc8a444",
    "scratch/t57/out/verify.py": "396064544983619d568127432c97e91a685179330e5dec65afcd7e3c4789ed3f",
    "scratch/t57/out/REPORT.md": "8149962abe4a221e48a7880aea0bb81037f89cbc2a14fb9ad8259e04fcddcfb1",
    "scratch/t57/out/DONE.md": "f87808aafb5d40858ac0c0c81030af0738537abc7fd0de9c3f6adf6bd683ca7d",
    "scripts/t57_clubmain_fields.py": "c189ce419f2fedcba172e2d78f5d024dcd5f70c48de424e41c83f4cf6c7be32b",
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


def artifact_records() -> list[dict[str, Any]]:
    records = []
    for rel, expected in T57_ARTIFACTS.items():
        path = ROOT / rel
        records.append({"path": rel, "sha256": expected, "bytes": path.stat().st_size})
    return records


def ledger_record(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": item["kind"], "level": item["level"], "date": item["date"],
        "claim_sha256": canonical_sha256(item["claim"]),
    }


def load_inputs() -> dict[str, Any]:
    v7_json_raw = verify_file(V7_JSON, V7_JSON_SHA256)
    v7_md_raw = verify_file(V7_MD, V7_MD_SHA256)
    v7 = json.loads(v7_json_raw)
    require(v7.get("schema_version") == 7 and v7.get("generated_by") == "t56", "v7 snapshot identity")

    for rel, expected in T57_ARTIFACTS.items():
        verify_file(ROOT / rel, expected)
    field_slots = read_json(ROOT / "scratch/t57/out/field_slots.json")
    field_map = read_json(ROOT / "scratch/t57/out/field_map.json")
    require(field_slots["L4"] == field_map["L4"] == 0, "t57 L4 boundary")
    require(field_slots["status"] == "observed_dual_archive_outer_census_complete_unobserved_dispatch_not_replayed",
            "t57 field slot status")
    require(field_map["status"] == "partial" and field_map["scope"] == "club.xml#club top-level occurrences only",
            "t57 field map scope")
    require(field_map["fields_total"] == 433 and field_map["fields_with_unique_XML_alignment"] == 18 and
            field_map["domain_pass_L3"] == 13 and field_map["new_L3"] == EXPECTED_NEW_L3 and
            field_map["grade_counts"] == EXPECTED_GRADES and sum(EXPECTED_GRADES.values()) == 433,
            "t57 field census")
    require(field_map["order"]["inversions"] == 72 and field_map["order"]["first_counterexample"] ==
            [[3, 13, "Cext"], [10, 6, "Cnam"]], "t57 XML/wire inversion")

    source = field_slots["source"]
    main_extent = source["runtime_function_extents"]["15050656"]
    require(main_extent["begin"] == 15050656 and main_extent["end_exclusive"] == 15056842 and
            main_extent["reachable"] == 1412 and main_extent["conditional"] == 167 and
            main_extent["external_edges"] == [], "t57 CLUB reader extent")
    require(source["CLUB"]["slots"]["19"]["bytes"] == "a0b1e54001000000", "t57 CLUB slot19")

    expected_envelopes = {
        "client": (13, 6932060, 6932073, 6932082, [54, 156], "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f"),
        "server": (13, 16595290, 16595303, 16595312, [81, 2618], "77ebce41936acd17ac798def913c456aa78db77a9acf01f6f440d4b9867716bc"),
    }
    for side, (header, row_bytes, footer_at, payload, width_range, payload_sha) in expected_envelopes.items():
        env = field_slots["envelopes"][side]
        require((env["header"], env["row_bytes"], env["footer_at"], env["payload"], env["rows"], env["row_width"]) ==
                (header, row_bytes, footer_at, payload, 84259, width_range), f"t57 {side} envelope")
        require(env["footer"] == "0000000001e3c03a77" and
                field_slots["archives"][side]["members"]["3"]["payload_sha256"] == payload_sha,
                f"t57 {side} footer/payload")
        require(env["selector_counts"] == {"0": 84256, "12": 3} and
                env["identity_census"]["strictly_increasing"] and env["identity_census"]["nonzero"] and
                env["identity_census"]["unique"] and env["identity_census"]["repeats_equal"],
                f"t57 {side} identity census")

    framing = field_slots["framing_sensitivity"]
    for side, absolute in (("client", 5705237), ("server", 14067615)):
        negative = framing[side]["marker_0_footer_9"]
        require(negative["paths"] == 0 and negative["first_dead_ordinal"] == 69705 and
                negative["first_rejected_candidate"][0] == absolute and
                negative["first_rejected_raw"] == "491001003145d8053145d8050c", f"t57 {side} 13-byte negative")
        require(framing[side]["triple_footer_9"]["paths"] == 1, f"t57 {side} 12-byte path")
    require([framing[s][f"triple_footer_{n}"]["paths"] for n in (7, 8, 9, 10, 12) for s in ("client", "server")] ==
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], "t57 footer sensitivity")

    ledger_doc = read_json(LEDGER_PATH)
    entries: dict[str, dict[str, Any]] = {}
    for item in ledger_doc["entries"]:
        entry_id = item.get("id")
        if entry_id in (*OLD_GUARDS, *NEW_GUARDS):
            require(entry_id not in entries, f"duplicate ledger entry {entry_id}")
            entries[entry_id] = item
    require(set(entries) == {*OLD_GUARDS, *NEW_GUARDS}, "required ledger entries missing")
    old_recorded = v7["incremental_provenance"]["acceptance_ledger_entries"]
    for entry_id in OLD_GUARDS:
        actual = entries[entry_id]
        expected = old_recorded[entry_id]
        require(actual.get("kind") == expected.get("kind") and actual.get("level") == expected.get("level") and
                canonical_sha256(actual.get("claim")) == expected.get("claim_sha256"),
                f"baseline ledger entry mismatch: {entry_id}")
    for entry_id, expected_sha in (("E96", E96_SHA256), ("E97", E97_SHA256)):
        actual = entries[entry_id]
        require(actual.get("kind") == "acceptance" and actual.get("level") == "L3" and
                canonical_sha256(actual.get("claim")) == expected_sha, f"new ledger entry mismatch: {entry_id}")
    return {
        "v7": v7, "v7_json_raw": v7_json_raw, "v7_md_raw": v7_md_raw,
        "field_slots": field_slots, "field_map": field_map, "ledger_entries": entries,
    }


def main_row_section(inputs: dict[str, Any]) -> dict[str, Any]:
    slots = inputs["field_slots"]
    field_map = inputs["field_map"]
    records = field_map["fields"]
    by_pos = {slot["position"]: slot for slot in slots["slots"]}
    aligned = [item for item in records if item["grade"] == "L3"]
    l3_fields = []
    for item in aligned:
        pos = item["candidate_position"]
        slot = by_pos[pos]
        l3_fields.append({
            "code": item["code"],
            "xml_index": item["xml_index"],
            "wire_position": pos,
            "accepted_position": item["accepted_position"],
            "lane": item["lane"],
            "slot_key": slot["key"],
            "slot_type": slot["type"],
            "slot_width": slot["width"],
            "object_displacement": slot["object_displacement"],
            "reason": item["reason"],
            "static": copy.deepcopy(item["static"]),
            "domain_profiles": copy.deepcopy(item["domain_profiles"]),
            "source_record": copy.deepcopy(item),
            "slot_record": copy.deepcopy(slot),
        })
    grade_membership: dict[str, list[str]] = {}
    for item in records:
        grade_membership.setdefault(item["grade"], []).append(item["code"])
    main_extent = slots["source"]["runtime_function_extents"]["15050656"]
    identity = by_pos[33]
    framing = slots["framing_sensitivity"]
    return {
        "source_task": "t57",
        "acceptance_ledger_entry": "E97",
        "acceptance_ledger_level": "L3",
        "status": slots["status"],
        "scope": field_map["scope"],
        "evidence_level": {"L3_fields": field_map["domain_pass_L3"], "L4": field_map["L4"]},
        "outer_sequence_closure": {
            "positions": len(slots["slots"]),
            "reader": {
                "vtable_slot": 19,
                "file_offset": main_extent["begin"],
                "file_offset_hex": "0xe5a7a0",
                "VA": "0x140e5b1a0",
                "extent_end_exclusive": main_extent["end_exclusive"],
                "reachable_instructions": main_extent["reachable"],
                "conditional_branches": main_extent["conditional"],
                "external_edges": copy.deepcopy(main_extent["external_edges"]),
            },
            "archive_modes": copy.deepcopy(slots["envelopes"]),
            "execution_templates": copy.deepcopy(slots["execution_templates"]),
            "server_minus_client_row_bytes": copy.deepcopy(slots["server_minus_client_row_bytes"]),
            "external_modes": copy.deepcopy(slots["external_modes"]),
        },
        "identity_framing": {
            "native_tail_width": identity["width"],
            "layout": "ordinal | UID | UID",
            "object_displacement": identity["object_displacement"],
            "footer_hex": slots["envelopes"]["client"]["footer"],
            "selector_counts": copy.deepcopy(slots["envelopes"]["client"]["selector_counts"]),
            "identity_slot": copy.deepcopy(identity),
            "thirteen_byte_first_counterexample": {
                "ordinal": 69705,
                "client_absolute": framing["client"]["marker_0_footer_9"]["first_rejected_candidate"][0],
                "server_absolute": framing["server"]["marker_0_footer_9"]["first_rejected_candidate"][0],
                "raw": framing["client"]["marker_0_footer_9"]["first_rejected_raw"],
                "next_selector": "0c",
            },
            "footer_width_sensitivity": {
                "footer_7": 0, "footer_8": 0, "footer_9": 1,
                "footer_10": 0, "footer_12": 0,
            },
        },
        "field_census": {
            "fields_total": field_map["fields_total"],
            "fields_with_unique_XML_alignment": field_map["fields_with_unique_XML_alignment"],
            "alignment_ratio": field_map["alignment_ratio"],
            "grade_counts": copy.deepcopy(field_map["grade_counts"]),
            "new_L3": copy.deepcopy(field_map["new_L3"]),
        },
        "L3_fields": l3_fields,
        "grade_membership": grade_membership,
        "order": copy.deepcopy(field_map["order"]),
        "ordering_policy": "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐",
        "source_artifacts": artifact_records(),
        "negative_regressions_preserved": {
            "E60_original_Cccn_negative": field_map["regression"]["original_Cccn_negative"],
            "true_binding_note": "Cccn is bound at +0xf0, the fourth u32 transfer; +0xe8, the third u32 transfer, is Cbni.",
        },
        "source_records": {
            "field_slots": copy.deepcopy(slots),
            "field_map": copy.deepcopy(field_map),
        },
        "source_report_note": {
            "report_path": "scratch/t57/out/REPORT.md",
            "done_path": "scratch/t57/out/DONE.md",
            "held_and_unmapped_records": "The embedded field_map is the verbatim t57 occurrence ledger; no held or unmapped row is promoted here.",
        },
    }


def extend_schema(inputs: dict[str, Any]) -> dict[str, Any]:
    baseline = inputs["v7"]
    schema = copy.deepcopy(baseline)
    schema["schema_version"] = 8
    schema["generated_by"] = "t58"
    schema["club_main_row_fields"] = main_row_section(inputs)

    coverage = schema["coverage"]
    framing_policy = (
        "Identity-tail and footer widths are table-specific evidence. Derive and verify each table independently; "
        "never copy another table's identity or footer width, including the nation 13-byte versus club 12-byte distinction."
    )
    coverage_items: dict[str, Any] = {}
    for key, value in coverage.items():
        coverage_items[key] = value
        if key == "nation_coverage_policy":
            coverage_items["row_identity_footer_width_policy"] = framing_policy
    if "row_identity_footer_width_policy" not in coverage_items:
        coverage_items["row_identity_footer_width_policy"] = framing_policy
    coverage.clear()
    coverage.update(coverage_items)
    counts = inputs["field_map"]["grade_counts"]
    coverage.update({
        "club_main_row_occurrences": inputs["field_map"]["fields_total"],
        "club_main_row_aligned": inputs["field_map"]["fields_with_unique_XML_alignment"],
        "club_main_row_L3": counts["L3"],
        "club_main_row_held": counts["held"],
        "club_main_row_skipped_separate_member": counts["skipped_separate_member"],
        "club_main_row_unmapped": counts["unmapped"],
        "club_main_row_new_L3": len(inputs["field_map"]["new_L3"]),
        "club_main_row_order_inversions": inputs["field_map"]["order"]["inversions"],
        "club_main_row_L4": inputs["field_map"]["L4"],
    })

    provenance = schema["incremental_provenance"]
    ledger_entries = provenance.setdefault("acceptance_ledger_entries", {})
    ledger_entries["E96"] = ledger_record(inputs["ledger_entries"]["E96"])
    ledger_entries["E97"] = ledger_record(inputs["ledger_entries"]["E97"])
    tasks = provenance.setdefault("tasks", {})
    tasks["t57"] = {
        "status": "accepted_L3_club_main_row_census_partial",
        "acceptance_ledger_entry": "E97",
        "acceptance_ledger_level": "L3",
        "ledger_claim_sha256": E97_SHA256,
        "evidence_level": {"L3_fields": 13, "L4": 0},
        "source_artifacts": artifact_records(),
        "row_counts": {"client": 84259, "server": 84259},
        "positions": 34,
        "identity_width": 12,
        "reader_extent": {"reachable_instructions": 1412, "conditional_branches": 167},
        "grade_counts": copy.deepcopy(counts),
        "order_inversions": 72,
        "held_records_preserved": True,
        "unmapped_records_preserved": True,
    }
    provenance["t57_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level canonical claim SHA-256 plus id/kind/level; no live full-file hash or byte-count pin",
        "guarded_entries": [*OLD_GUARDS, *NEW_GUARDS],
        "t56_acceptance_entry": "E96",
        "t56_acceptance_level": "L3",
        "t57_acceptance_entry": "E97",
        "t57_acceptance_level": "L3",
    }
    return schema


def _profile_summary(item: dict[str, Any]) -> str:
    parts = []
    for side in ("client", "server"):
        profile = item["domain_profiles"].get(side)
        if not profile:
            continue
        if profile.get("status") == "bypassed":
            parts.append(f"{side}=bypassed")
        elif "hit" in profile:
            parts.append(f"{side}:hit={profile['hit']},miss={profile['miss']},null={profile['null']}")
        elif "decoded" in profile:
            parts.append(f"{side}:decoded={profile['decoded']}")
        else:
            parts.append(f"{side}:domain={profile.get('domain')}")
    return "; ".join(parts)


def markdown_appendix(inputs: dict[str, Any]) -> str:
    slots = inputs["field_slots"]
    field_map = inputs["field_map"]
    records = field_map["fields"]
    by_pos = {slot["position"]: slot for slot in slots["slots"]}
    l3 = [item for item in records if item["grade"] == "L3"]
    held = [item for item in records if item["grade"] == "held"]
    env = slots["envelopes"]
    main = slots["source"]["runtime_function_extents"]["15050656"]
    lines = [
        "", "", "## t58 — t57 Club `table_3` 主行槽位增量（E97 / L3）", "",
        "本节为 v7 Markdown 的追加内容；此前 v7 全文保持为逐字节前缀。新增内容只建立 Club 主行层，" \
        "不改写 8 张既有表、负回归、`v3_baseline`、`club_auxiliary_sources` 或任何 `nation_*` 节。", "",
        f"- 双档各 {env['client']['rows']:,} 行、34 个逻辑位置；client `13 + {env['client']['row_bytes']:,} + 9 = {env['client']['payload']:,}`，" \
        f"server `13 + {env['server']['row_bytes']:,} + 9 = {env['server']['payload']:,}`。行宽 client {env['client']['row_width'][0]}–{env['client']['row_width'][1]} B、" \
        f"server {env['server']['row_width'][0]}–{env['server']['row_width'][1]} B。", 
        f"- payload SHA：client `{slots['archives']['client']['members']['3']['payload_sha256']}`；server `{slots['archives']['server']['members']['3']['payload_sha256']}`。", 
        f"- CLUB 主 reader 为 vtable slot 19，file offset `0xe5a7a0` / VA `0x140e5b1a0`；PE extent 可达 {main['reachable']:,} 指令、{main['conditional']} 条条件、0 条 extent 外边。", 
        "- 原生 identity tail 是 **12 B** `ordinal | UID | UID`，两档 footer 均 `0000000001e3c03a77`；selector 为 0 的 84,256 行、selector 12 的 3 行。identity 宽度按表自证，不从 nation 的 13 B 口径复制。任何表的 identity-tail/footer 宽度均须逐表自证，不照抄其他表。", 
        "- 强制 13 B / 末 byte==0 的旧假设在 ordinal **69705** 断开：client `@5705237`、server `@14067615`，raw `491001003145d8053145d8050c`；末 `0c` 是下一条 selector。12 B / footer 9 的唯一闭合保留。", "",
        "### 主行字段台账", "",
        f"433 个 `club.xml#club` 顶层 occurrence 中，唯一 XML 对齐 {field_map['fields_with_unique_XML_alignment']} 项；grade_counts 原样：L3 {field_map['grade_counts']['L3']}、held {field_map['grade_counts']['held']}、skipped_separate_member {field_map['grade_counts']['skipped_separate_member']}、unmapped {field_map['grade_counts']['unmapped']}。L4=0。", 
        "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐。共 72 对倒置，首例是 wire pos 3 `Cext` / XML 13 先于 wire pos 10 `Cnam` / XML 6；完整倒置和 433 项原始记录在 v8 JSON 的 `club_main_row_fields.source_records` 中逐条保留。", "",
        "| Wire pos | 字段 / XML index | 槽位 | 全档域证据 |", 
        "|---:|---|---|---|",
    ]
    for item in l3:
        pos = item["candidate_position"]
        slot = by_pos[pos]
        lines.append(f"| {pos} | `{item['code']}` / {item['xml_index']} | `{slot['key']}` / `+0x{(slot['object_displacement'] or 0):x}` | {_profile_summary(item)} |")
    lines += [
        "", f"新增 L3：`{', '.join(field_map['new_L3'])}`。13 个主行 L3 的完整静态链、getter、slot profile 与 raw first/last 记录均从 t57 原台账嵌入，未把共享物理槽拆成额外字段。", 
        "- `Cext` 与 `Cnti` 共用 position 3；`CIns`、`CASt`、`Csot`、`CnCV` 共用 flags position 8；`Cncl`、`Cedp` 共用 base48 position 31。", 
        "- `Cccn` 的 E60 `old row+8` negative 原文逐字保留如下；真绑定是 `+0xf0` 第四次 u32 transfer，`+0xe8` 第三次为 `Cbni`。", 
        "> " + field_map["regression"]["original_Cccn_negative"], 
        "- `Ctsi` 是 Training Ground 的 position 23 / `+0x140`，不是 `Csti`；server 9,403 live、74,856 null。`Ccty` 两档均为 74,079 live / 10,180 null、0 miss。","",
        "### Held 与未映射边界", "",
        "候选不写成结论。以下 11 个 held occurrence 的 reason 与首反例来自 t57 `field_map.json`，未改写；399 个 unmapped occurrence 也完整嵌入 JSON，不能解释为 absence。", 
        "| 字段 | reason | 首反例 |", "|---|---|---|",
    ]
    for item in held:
        counterexample = json.dumps(item["first_counterexample"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        lines.append(f"| `{item['code']}` | {item['reason']} | `{counterexample}` |")
    lines += [
        "", "首反例重点包括 `Csnm` XML max 25 下每档 537 条越界、`CLat/CLon` getter 装箱 0 不能贴成 Club 坐标、`Csti` 证据不足，以及 `Cyfn` getter 指向 `extra + 0xd8` 而非主行。`Cnam` backing text 与本地化 getter 不等同；`PLgn`、`Cprs`、`Cdof` 不因 raw/control byte 取得语义。", "",
        "### Coverage 与 provenance", "",
        "主行层单列：occurrences 433、aligned 18、L3 13、held 11、skipped_separate_member 10、unmapped 399、new L3 5、wire/XML inversions 72、L4=0。既有 `club_L3_occurrences=94`、`club_L3_unique_wire_fields=59`、`held_fields=21` 等子表层计数不动。", 
        f"E97 acceptance：kind `acceptance` / level `L3` / canonical claim SHA-256 `{E97_SHA256}`；t56/E96：canonical claim SHA-256 `{E96_SHA256}`。条目级守卫扩至 E87/E89/E90/E91/E92/E93/E94/E95/E96/E97；不钉 live ledger 全文件哈希。", 
        "t57 的独立 verifier、builder selftest、本文档前缀、v7 快照 SHA、保护节和 t01 anchors 均在 t58 输出日志中记录。", "",
    ]
    return "\n".join(lines)


def check_protected(baseline: dict[str, Any], updated: dict[str, Any]) -> None:
    for key in PROTECTED_ROOT_KEYS:
        require(updated.get(key) == baseline.get(key), f"protected JSON section changed: {key}")
    expected_root = set(baseline) | {"club_main_row_fields"}
    require(set(updated) == expected_root, "schema root keys changed outside additive section")
    for key, value in baseline.items():
        if key not in {"schema_version", "generated_by", "coverage", "incremental_provenance"}:
            require(updated.get(key) == value, f"unrequested root data changed: {key}")
    old_coverage = baseline["coverage"]
    new_coverage = updated["coverage"]
    for key, value in old_coverage.items():
        require(new_coverage.get(key) == value, f"existing coverage changed: {key}")
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
    c = schema["coverage"]
    return (
        "# t58 — 公共 club/nation schema v7→v8 增量\n\n"
        "## 变更\n\n"
        f"- 基线：v7 JSON SHA-256 `{V7_JSON_SHA256}`；v7 Markdown SHA-256 `{V7_MD_SHA256}`；Markdown 旧内容逐字节保留为新文件前缀。\n"
        "- 新增 `club_main_row_fields`：嵌入 t57 双档 34 槽、field_map 全量 occurrence、field_slots、静态 reader extent 与 framing sensitivity。\n"
        f"- Club 主行汇总：433 occurrences、aligned {c['club_main_row_aligned']}、L3 {c['club_main_row_L3']}、held {c['club_main_row_held']}、skipped {c['club_main_row_skipped_separate_member']}、unmapped {c['club_main_row_unmapped']}、72 inversions、L4=0。\n"
        "- 既有 club 子表口径保持：`club_L3_occurrences=94`、`club_L3_unique_wire_fields=59`、`held_fields=21`；8 张表和所有 nation 节逐值保护。\n"
        f"- 条目级 ledger 守卫：E87/E89/E90/E91/E92/E93/E94/E95/E96/E97；E97 为 L3，canonical claim SHA `{E97_SHA256}`。\n\n"
        "## 验收\n\n"
        "- t57 数字断言：client/server 6,932,082 / 16,595,312 B；84,259 + 84,259 rows；identity 12 B；reader 1,412 instructions / 167 branches；13 L3；72 inversions；69705 13-byte negative 保留。\n"
        "- held/unmapped 原样保留：`Csnm` 537 越界、`CLat/CLon` 非 Club 坐标、`Csti` 证据不足、`Cyfn` 为 extra+0xd8 非主行；E60 `Cccn` negative 与真绑定 `+0xf0` 注记保留。\n"
        "- builder selftest、independent verify、`--help` / `--selftest` 与 t01 anchors 结果写入 `spot_*.log`。\n"
        f"- v8 JSON SHA-256 `{sha(public_json)}` ({len(public_json)} bytes)；v8 Markdown SHA-256 `{sha(public_md)}` ({len(public_md)} bytes)。\n"
    )


def done_text(schema: dict[str, Any], public_json: bytes, public_md: bytes) -> str:
    c = schema["coverage"]
    return (
        "# t58 完成记录\n\n"
        "- 公共 schema 已从 v7 增量升至 v8；v7 Markdown 前缀、指定保护节和既有 club 子表计数逐值保持。\n"
        "- 并入 t57/E97：双档各 84,259 行、34 位置、native identity 12 B、reader 1,412/167、13 L3、11 held、10 skipped、399 unmapped、72 倒置；held/unmapped 原台账嵌入。\n"
        f"- 主行 coverage：{c['club_main_row_occurrences']} occurrences / {c['club_main_row_L3']} L3 / {c['club_main_row_held']} held / {c['club_main_row_unmapped']} unmapped / L4=0；子表 `club_L3_occurrences=94` 不变。\n"
        "- provenance 增加 t57/E97，并以条目级 canonical claim SHA 守卫 E87/E89/E90/E91/E92/E93/E94/E95/E96/E97。\n"
        "- 交付：`consolidate_v8.py`、`verify.py`、v7/v8 快照、报告、完成记录及 `spot_*.log`。\n"
        f"- JSON SHA-256 `{sha(public_json)}`；Markdown SHA-256 `{sha(public_md)}`。\n"
    )


def selftest() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["v7"], schema)
    appendix = markdown_appendix(inputs).encode("utf-8")
    require(appendix.startswith(b"\n\n## t58"), "Markdown appendix heading")
    require(schema["coverage"]["club_main_row_L3"] == 13 and
            schema["coverage"]["club_main_row_held"] == 11 and
            schema["coverage"]["club_main_row_unmapped"] == 399 and
            schema["coverage"]["club_L3_occurrences"] == 94, "selftest coverage")
    require(schema["incremental_provenance"]["tasks"]["t57"]["ledger_claim_sha256"] == E97_SHA256,
            "selftest E97 pin")
    print("t58 builder selftest PASS: v7 snapshot, t57 artifacts, entry guards, protected blocks, 13 L3 and 433-grade census")


def build() -> None:
    inputs = load_inputs()
    schema = extend_schema(inputs)
    check_protected(inputs["v7"], schema)
    json_raw = json_bytes(schema)
    md_raw = inputs["v7_md_raw"] + markdown_appendix(inputs).encode("utf-8")
    current_json = PUBLIC_JSON.read_bytes()
    current_md = PUBLIC_MD.read_bytes()
    prior_v8_json_sha256 = "ecea83900ee770cb3dabad714745d4219d785675c46d9d63b77b589b7def2db3"
    prior_v8_md_sha256 = "f04f0d5ef1f1182aad43d16f99f4318e3a976c6062b7c4e949af00243e23aaa6"
    require(sha(current_json) in {V7_JSON_SHA256, prior_v8_json_sha256, sha(json_raw)} and
            sha(current_md) in {V7_MD_SHA256, prior_v8_md_sha256, sha(md_raw)},
            "public schema is neither pinned v7 baseline nor a pinned t58 build")
    PUBLIC_JSON.write_bytes(json_raw)
    PUBLIC_MD.write_bytes(md_raw)
    V8_JSON.write_bytes(json_raw)
    V8_MD.write_bytes(md_raw)
    (OUT / "REPORT.md").write_text(report_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    (OUT / "DONE.md").write_text(done_text(schema, json_raw, md_raw), encoding="utf-8", newline="\n")
    print(f"t58 build PASS: schema v8; club main L3 {schema['coverage']['club_main_row_L3']}/held {schema['coverage']['club_main_row_held']}/unmapped {schema['coverage']['club_main_row_unmapped']}; L4=0")
    print(f"JSON {sha(json_raw)} ({len(json_raw)} bytes)")
    print(f"Markdown {sha(md_raw)} ({len(md_raw)} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--build", action="store_true", help="build public v8 pair (default)")
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
