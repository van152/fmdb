#!/usr/bin/env python3
"""t35 data-side Cafl/Cvfl discovery; no cursor inference or L3 promotion."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import runpy
import struct
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t35/out"
T14 = ROOT / "scratch/t14/out/census.json"
STAGE2 = ROOT / "reports/stage2_table_identity.json"
INVENTORY = ROOT / "scratch/t29/out/subtable_inventory.json"
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
T24_DIR = ROOT / "scratch/t24/out"
T27 = ROOT / "scratch/t27/out/replication.md"
T02_CLUB = ROOT / "scratch/t02/inbox/club_v2/output.json"
T29_INPUT_SHA = {
    "scratch/t14/out/census.json": "522138424a913a6ea899824443bf9277521162137decaa35c805763544b26a70",
    "reports/stage2_table_identity.json": "f2533a06de4e79c19b26d93c4f51471da7c0552d45a0c20b54ccc31c4f5b14c7",
    "scratch/t24/out/subtables.part001.json": "6ba93636161d924ebf2648cb4be254d864b773bc30b28bd9c4fdf3349a44b829",
    "scratch/t24/out/subtables.part002.json": "85291f96f14c9fee436ab66976c24813479374015657fef894680d21d07463a2",
    "scratch/t24/out/subtables.part003.json": "62f63febe1a022941610d9881b711799f1a86c615c25d7692458b61e90b09c84",
}
MASTER_SHA = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
MANIFEST_SHA = "28593fcb59f0c0d23d40cb7091b2c0f5ebb5725c7571fda44fe1eeef581d3fc0"
CLUB_CLIENT_PAYLOAD_SHA = "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f"
TAD_HEADER = bytes.fromhex("03 01 74 61 64 2e f1 0d")
ZSTD_MAGIC = bytes.fromhex("28 b5 2f fd")
SEMANTIC_TERMS = (
    "AFFILIAT", "CLUB_LINK", "LINKED_CLUB", "CLUB_RELATION", "RELATED_CLUB",
    "FEEDER_CLUB", "FARM_CLUB", "SATELLITE_CLUB", "SISTER_CLUB",
    "SUBSIDIARY_CLUB", "PARTNER_CLUB", "AFFILIATE_CLUB",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def ensure_input_hashes() -> dict:
    manifest_hash = file_sha(MANIFEST)
    if manifest_hash != MANIFEST_SHA:
        raise ValueError(f"evidence/MANIFEST.json hash mismatch: {manifest_hash}")
    manifest = read_json(MANIFEST)
    entry = next((f for f in manifest["files"] if f["path"] == "evidence/fm24/reports/editor_schema/master.json"), None)
    master_hash = file_sha(MASTER)
    if not entry or entry.get("sha256") != MASTER_SHA or master_hash != MASTER_SHA:
        raise ValueError("club schema snapshot does not match evidence/MANIFEST.json")
    actual = {"evidence/MANIFEST.json": manifest_hash, "evidence/fm24/reports/editor_schema/master.json": master_hash}
    for rel, expected in T29_INPUT_SHA.items():
        actual_hash = file_sha(ROOT / rel)
        if actual_hash != expected:
            raise ValueError(f"input hash mismatch for {rel}: {actual_hash}")
        actual[rel] = actual_hash
    inventory = read_json(INVENTORY)
    prov = inventory["provenance"]
    if prov.get("master_sha256") != MASTER_SHA or prov.get("manifest_sha256") != MANIFEST_SHA:
        raise ValueError("t29 inventory provenance does not match frozen schema/manifest")
    if prov.get("t14_census_sha256") != T29_INPUT_SHA["scratch/t14/out/census.json"]:
        raise ValueError("t29 census provenance mismatch")
    if prov.get("stage2_identity_sha256") != T29_INPUT_SHA["reports/stage2_table_identity.json"]:
        raise ValueError("t29 stage2 provenance mismatch")
    for rel in ("scratch/t24/out/subtables.part001.json", "scratch/t24/out/subtables.part002.json", "scratch/t24/out/subtables.part003.json"):
        if prov.get("t24_subtables_sha256", {}).get(rel) != T29_INPUT_SHA[rel]:
            raise ValueError(f"t29 t24 provenance mismatch for {rel}")
    actual["scratch/t27/out/replication.md"] = file_sha(T27)
    actual["scratch/t29/out/subtable_inventory.json"] = file_sha(INVENTORY)
    return {"sha256": actual, "manifest_snapshot_date": manifest.get("snapshot_date"), "master_manifest_entry": entry}


def schema_item_fields() -> dict[str, list[dict]]:
    master = read_json(MASTER)
    club = master["entities"]["club.xml"]
    if len(club) != 1 or club[0].get("id") != "club":
        raise ValueError("unexpected club.xml entity structure")
    master_lists = {f["field"]: f.get("list_item_fields", []) for f in club[0]["fields"] if f.get("field") in ("Cafl", "Cvfl")}
    out = {"Cafl": [], "Cvfl": []}
    for part in sorted(T24_DIR.glob("subtables.part00*.json")):
        doc = read_json(part)
        for field in doc.get("nested_fields", []):
            parent = field.get("parent")
            if parent in out and ((parent == "Cafl" and 370 <= field.get("idx", -1) <= 398) or (parent == "Cvfl" and 400 <= field.get("idx", -1) <= 418)):
                out[parent].append({
                    "schema_idx": field["idx"], "field": field["code"], "name": field.get("name"),
                    "type": field.get("type"), "optional": field.get("optional"),
                })
    for parent, expected in (("Cafl", 29), ("Cvfl", 19)):
        out[parent].sort(key=lambda f: f["schema_idx"])
        if len(out[parent]) != expected or len(master_lists.get(parent, [])) != expected:
            raise ValueError(f"schema item count mismatch for {parent}")
        t24_codes = [f["field"] for f in out[parent]]
        master_codes = [f.get("field") for f in master_lists[parent]]
        if t24_codes != master_codes:
            raise ValueError(f"t24 and frozen master field order mismatch for {parent}")
    return out


def class_semantic_text(row: dict) -> str:
    names = [row.get("primary_class") or ""]
    names.extend(v.get("class", "") for v in row.get("vtables", []))
    return " ".join(names).upper()


def discover_semantic_candidates(census: dict, stage2: dict) -> dict:
    stage_by_type = {r.get("table_type"): r for r in stage2.get("rows", [])}
    results = []
    for row in census.get("tables", []):
        cls = class_semantic_text(row)
        hit_terms = [term for term in SEMANTIC_TERMS if term in cls]
        if not hit_terms:
            continue
        t = row.get("table_type")
        s = stage_by_type.get(t, {})
        results.append({
            "table_type": t, "archive": "unknown", "rtti_class": row.get("primary_class") or "unknown",
            "primary_class": row.get("primary_class") or "unknown", "entity_tag": row.get("entity_tag") or "unknown",
            "vtables": sorted({v.get("class") for v in row.get("vtables", []) if v.get("class")}),
            "stage2_status": s.get("status", "unknown"), "stage2_entity": s.get("entity") or "unknown",
            "matched_terms": hit_terms, "match_status": "candidate_unresolved_archive",
        })
    return {
        "status": "complete_no_semantic_candidate" if not results else "partial_semantic_candidates_need_archive_join",
        "semantic_terms": list(SEMANTIC_TERMS), "candidate_count": len(results), "candidates": results,
        "scan_scope": {"t14_types": len(census.get("tables", [])), "stage2_rows": len(stage2.get("rows", []))},
    }


def load_data_module():
    os.environ["FM24_DB_DIR"] = str(ROOT / "scratch/data")
    return runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))


def archive_table_frames(codec: dict, archive: str, table_type: int) -> dict:
    path = ROOT / "scratch/data" / f"{archive}_db.dat"
    if not path.is_file():
        return {"status": "negative_archive_file_absent", "archive": archive, "table_type": table_type}
    entries = codec["list_tables"](path, path.name)
    try:
        entry = codec["_resolve_table"](table_type, entries, path.name)
    except Exception as exc:
        return {"status": "negative_table_member_absent", "archive": archive, "table_type": table_type, "error": str(exc)}
    packed = path.read_bytes()
    base = int(entry["offset"])
    hits = [i for i in range(base, min(base + 256, len(packed) - 3)) if packed[i:i + 4] == ZSTD_MAGIC]
    frames = []
    for offset in hits:
        try:
            payload = codec["_stream_decompress"](packed[offset:], 256 * 1024 * 1024)
            frames.append({
                "frame_offset": offset, "relative_frame_offset": offset - base,
                "payload_bytes": len(payload), "payload_sha256": sha(payload),
                "header_match": payload.startswith(TAD_HEADER),
                "row_count_header": struct.unpack_from("<I", payload, 8)[0] if len(payload) >= 12 and payload.startswith(TAD_HEADER) else None,
                "_payload": payload,
            })
        except Exception as exc:
            frames.append({"frame_offset": offset, "relative_frame_offset": offset - base, "decompress_error": f"{type(exc).__name__}: {exc}"})
    valid = [f for f in frames if f.get("header_match")]
    if archive == "client" and table_type == 3:
        picked = next((f for f in valid if f.get("payload_sha256") == CLUB_CLIENT_PAYLOAD_SHA), None)
    else:
        picked = valid[0] if len(valid) == 1 else None
    public_frames = [{k: v for k, v in f.items() if k != "_payload"} for f in frames]
    if picked is None:
        return {
            "status": "partial_frame_selection_unresolved", "archive": archive, "table_type": table_type,
            "member_offset": base, "frames": public_frames,
            "blocker": "No unique payload frame supported by the frozen hash/header evidence.",
        }
    payload = picked.pop("_payload")
    return {
        "status": "complete_payload_selected", "archive": archive, "table_type": table_type,
        "member_offset": base, "member_name": entry.get("name", f"table_{table_type}"),
        "frames": public_frames, "selected_frame": {k: v for k, v in picked.items() if k != "_payload"},
        "payload": payload,
    }


def parse_standard_row(raw: bytes, start: int, ordinal: int, width: int):
    p = start
    try:
        lanes = struct.unpack_from("<4I", raw, p)
        p += 16
        if p + width > len(raw):
            return None
        block = raw[p:p + width]
        p += width
        group = struct.unpack_from("<I", raw, p)[0]
        p += 4
        flag = raw[p]
        p += 1
        full_n = struct.unpack_from("<I", raw, p)[0]
        p += 4
        if full_n > 200 or p + full_n > len(raw):
            return None
        raw[p:p + full_n].decode("utf-8")
        p += full_n
        short_n = struct.unpack_from("<I", raw, p)[0]
        p += 4
        if short_n > 200 or p + short_n > len(raw):
            return None
        raw[p:p + short_n].decode("utf-8")
        p += short_n
        flags = raw[p:p + 3]
        if len(flags) != 3:
            return None
        p += 3
        stored, key_a, key_b = struct.unpack_from("<III", raw, p)
        p += 12
        marker = raw[p]
        p += 1
        if stored != ordinal or key_a != key_b or marker not in (0, 12):
            return None
        return {"ordinal": ordinal, "start": start, "end": p, "length": p - start,
                "block_width": width, "lanes": lanes, "block": block, "group": group,
                "flag": flag, "marker": marker, "identity_key": key_a}
    except (IndexError, struct.error, UnicodeDecodeError):
        return None


def walk_client_club(raw: bytes) -> dict:
    if len(raw) < 22 or raw[:8] != TAD_HEADER:
        raise ValueError("client table_3 payload header invalid")
    count = struct.unpack_from("<I", raw, 8)[0]
    if count != 84259:
        raise ValueError(f"client table_3 row count header changed: {count}")
    rows = []
    pos = 14
    widths = Counter()
    lengths = Counter()
    markers = Counter()
    prefix_lanes = [[], [], [], []]
    block_bytes = [[0] * 8 for _ in range(5)]
    for ordinal in range(count):
        matches = [r for width in (4, 5) if (r := parse_standard_row(raw, pos, ordinal, width)) is not None]
        if len(matches) > 1:
            raise ValueError(f"ambiguous standard row {ordinal} at {pos:#x}")
        if matches:
            row = matches[0]
            widths[str(row["block_width"])] += 1
            for n, value in enumerate(row["lanes"]):
                prefix_lanes[n].append(value)
            if row["block_width"] == 5:
                for b, value in enumerate(row["block"]):
                    for bit in range(8):
                        block_bytes[b][bit] += (value >> bit) & 1
        else:
            needle = struct.pack("<I", ordinal)
            stop = min(pos + 8192, len(raw) - 13)
            hits = []
            q = raw.find(needle, pos + 20, stop)
            while q >= 0:
                if q + 13 <= len(raw):
                    stored, key_a, key_b = struct.unpack_from("<III", raw, q)
                    marker = raw[q + 12]
                    if stored == ordinal and key_a == key_b and marker in (0, 12):
                        hits.append((q, key_a, marker))
                q = raw.find(needle, q + 1, stop)
            if len(hits) != 1:
                raise ValueError(f"identity frame for compact row {ordinal} is not unique: {len(hits)} hits")
            q, key, marker = hits[0]
            row = {"ordinal": ordinal, "start": pos, "end": q + 13, "length": q + 13 - pos,
                   "block_width": None, "marker": marker, "identity_key": key}
            widths["identity_only"] += 1
        rows.append(row)
        lengths[row["length"]] += 1
        markers[str(row["marker"])] += 1
        pos = row["end"]
    footer_start = len(raw) - 8
    if pos != footer_start:
        raise ValueError(f"row closure mismatch: parsed_end={pos}, footer_start={footer_start}")
    standard_count = sum(len(v) for v in prefix_lanes[:1])
    if standard_count != 84256 or widths.get("identity_only", 0) != 3:
        raise ValueError(f"unexpected row profile widths: {dict(widths)}")
    lane_profile = []
    for index, values in enumerate(prefix_lanes):
        lane_profile.append({
            "raw_u32_lane": index, "rows": len(values), "unique_values": len(set(values)),
            "minimum": min(values) if values else None, "maximum": max(values) if values else None,
            "values_in_club_ordinal_domain_0_84259": sum(0 <= v < 84259 for v in values),
            "sample_first_12": values[:12], "semantic_assignment": "none; parent-table structure only",
        })
    bit_profile = []
    n5 = widths.get("5", 0)
    for byte_offset, bits in enumerate(block_bytes, start=16):
        bit_profile.append({
            "row_relative_byte_offset": byte_offset, "rows": n5,
            "bits": [{"bit": b, "set_count": bits[b], "clear_count": n5 - bits[b]} for b in range(8)],
            "semantic_assignment": "none; 5-byte aggregate in parent-table framing, not Cafl/Cvfl item booleans",
        })
    return {
        "status": "complete_parent_client_row_profile", "table_type": 3, "archive": "client",
        "role": "club parent container context; not an affiliation child-table candidate",
        "count": count, "stride": None, "stride_status": "variable row spans",
        "payload_bytes": len(raw), "payload_sha256": sha(raw),
        "row_start": 14, "footer_bytes": 8, "footer_offset": footer_start,
        "row_width_counts": dict(widths), "row_length_distribution": {str(k): v for k, v in sorted(lengths.items())},
        "row_length_min": min(lengths), "row_length_max": max(lengths), "distinct_row_lengths": len(lengths),
        "row_body_bytes": pos - 14, "closure_equation": f"14 + {pos - 14} + 8 = {len(raw)}",
        "footer_hex": raw[footer_start:].hex(" "), "marker_counts": dict(markers),
        "compact_identity_only_rows": [r["ordinal"] for r in rows if r["block_width"] is None],
        "raw_prefix_u32_lanes": lane_profile, "aggregate5_byte_bit_counts": bit_profile,
        "item_field_columns": {"status": "not_extracted", "candidate_columns": [],
                               "reason": "No affiliation child member/row boundary was identified; do not assign Cafl/Cvfl schema codes to parent-row byte lanes."},
        "date_cash_enum_bool_profiles": {"status": "blocked_no_item_columns",
                                          "fields": ["stdt", "endt", "yfee", "type", "clfr", "boolean item fields"]},
        "row_samples": [{"ordinal": r["ordinal"], "row_offset": r["start"], "row_length": r["length"],
                         "block_width": r["block_width"], "identity_key": r["identity_key"], "marker": r["marker"]}
                        for r in (rows[0], rows[69705], rows[69706], rows[69707], rows[69708], rows[69709], rows[-1])],
    }


def build() -> dict:
    provenance = ensure_input_hashes()
    census = read_json(T14)
    stage2 = read_json(STAGE2)
    inventory = read_json(INVENTORY)
    fields = schema_item_fields()
    scan = discover_semantic_candidates(census, stage2)
    codec = load_data_module()["_reader"]()
    parent_archives = {}
    parent_profiles = {}
    for archive in ("client", "server"):
        info = archive_table_frames(codec, archive, 3)
        if info.get("status") == "complete_payload_selected":
            payload = info.pop("payload")
            parent_archives[archive] = info
            if archive == "client":
                if sha(payload) != CLUB_CLIENT_PAYLOAD_SHA:
                    raise ValueError("client table_3 payload does not match the existing closed-row evidence")
                parent_profiles[archive] = walk_client_club(payload)
            else:
                parent_profiles[archive] = {
                    "status": "partial_payload_only_no_row_walk", "table_type": 3, "archive": "server",
                    "role": "club parent container context; not an affiliation child-table candidate",
                    "payload_bytes": len(payload), "payload_sha256": sha(payload),
                    "row_count_header": struct.unpack_from("<I", payload, 8)[0] if len(payload) >= 12 else None,
                    "row_start": 14, "footer_bytes_expected_by_header_convention": 8,
                    "stride": None, "closure_equation": None,
                    "blocker": "No server table_3 row walker was applied; parent payload metadata cannot identify Cafl/Cvfl item columns.",
                }
        else:
            parent_archives[archive] = info
    t14_type3 = next((t for t in census["tables"] if t.get("table_type") == 3), {})
    stage_type3 = next((t for t in stage2.get("rows", []) if t.get("table_type") == 3), {})
    missing_parents = []
    for parent in ("Cafl", "Cvfl"):
        found = next((x for x in inventory.get("parents", []) if x.get("parent_4cc") == parent), None)
        if not found or found.get("table_type") != "unknown":
            raise ValueError(f"t29 inventory no longer marks {parent} unknown")
        missing_parents.append({
            "parent_4cc": parent, "candidate_table_type": "unknown", "archive": "unknown",
            "rtti_class": "unknown", "primary_class": "unknown", "entity_tag": "unknown",
            "count": None, "stride": None,
            "item_field_candidates": [],
            "schema_item_fields_not_mapped": fields[parent],
            "view_hypothesis_evidence": [
                "No t14 RTTI class or stage2 identity row matched the affiliation/link semantic search terms.",
                "t27 reports getter paths using club object offsets +0x118/+0x120 with different R8 flags; that is static lead context, not data proof.",
                "client table_type 3 is a club parent container and its rows close, but no Cafl/Cvfl child item columns were extracted from this payload.",
            ],
            "confidence": "unknown_no_child_table_match",
            "blockers": [
                "No independent RTTI/table_type/archive join for this parent.",
                "No affiliation item row boundary or column offset; schema order is not byte-layout evidence.",
                "No candidate item values to test packed dates, cash, enums, club references, or shared boolean masks.",
            ],
        })
    data = {
        "status": "partial_no_semantic_candidate",
        "task": "t35 Cafl/Cvfl club affiliation data-side discovery",
        "scope": "data-side only; no static cursor analysis and no L3 promotion",
        "provenance": provenance,
        "source_files": {
            "t27_replication_sha256": provenance["sha256"]["scratch/t27/out/replication.md"],
            "t29_inventory_sha256": provenance["sha256"]["scratch/t29/out/subtable_inventory.json"],
            "t14_summary": census.get("summary"), "stage2_summary": stage2.get("counts"),
        },
        "semantic_candidate_scan": scan,
        "near_miss_club_classes": [
            {"table_type": t.get("table_type"), "primary_class": t.get("primary_class"),
             "entity_tag": t.get("entity_tag") or "unknown", "disposition": "club-related but no affiliation/link name or independent Cafl/Cvfl join"}
            for t in census.get("tables", [])
            if "CLUB" in class_semantic_text(t) and not any(term in class_semantic_text(t) for term in SEMANTIC_TERMS)
        ],
        "parent_container_context": {
            "t14_table_type_3": {"primary_class": t14_type3.get("primary_class"), "entity_tag": t14_type3.get("entity_tag"),
                                 "vtables": sorted({v.get("class") for v in t14_type3.get("vtables", []) if v.get("class")})},
            "stage2_table_type_3": {"status": stage_type3.get("status"), "entity": stage_type3.get("entity"), "role": stage_type3.get("role")},
            "archives": parent_archives, "profiles": parent_profiles,
        },
        "view_hypothesis": {
            "status": "partial_not_testable_from_available_data_columns",
            "conclusion_tendency": "no_data_vote", "supports_one_collection_two_views": [],
            "supports_two_independent_tables": [],
            "negative_evidence": [
                "0 semantic RTTI candidates across the full 74-type t14 census.",
                "0 semantic entity/role candidates across the 45-row stage2 identity file.",
                "No two affiliation-like archive tables were found to compare.",
            ],
            "counterexamples_retained": [
                "This negative scan does not prove absence: an affiliation list may be embedded in a parent record or represented by an uninformative RTTI class.",
                "The client table_type 3 parent rows contain 84,256 standard rows and 3 identity-only compact bodies; the compact bodies are not semantically decoded and are not evidence for or against affiliation views.",
            ],
            "reason_not_decidable": "No Cafl/Cvfl item columns or rows were independently joined to a candidate table; no data comparison can test clfr/endt coverage, field subset compatibility, affl overlap, or shared bit masks.",
        },
        "copy_ready": missing_parents,
        "unknown_list": ["Cafl table_type/archive/RTTI/count/stride", "Cvfl table_type/archive/RTTI/count/stride",
                         "all item field offsets", "stdt/endt encodings", "yfee unit/storage", "affl reference encoding",
                         "type/clfr enum domains", "boolean bit packing", "one-view vs two-table data relation"],
        "data_boundary_note": "Parent table_type 3 is contextual only; it must not be copied to Cafl or Cvfl as their table_type.",
    }
    out_profiles = OUT / "profiles"
    out_profiles.mkdir(parents=True, exist_ok=True)
    (out_profiles / "semantic_candidate_scan.json").write_text(json.dumps(scan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_profiles / "parent_table3_context.json").write_text(json.dumps(data["parent_container_context"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "cafl_cvfl_discovery.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(data)
    (OUT / "DONE.md").write_text(
        "# t35 Done\n\n"
        "Status: `partial_no_semantic_candidate`. The requested semantic scan completed, but no Cafl/Cvfl child table was joined to an archive member. `client table_type 3` was profiled only as parent-container context. No field was assigned an offset or promoted to L3.\n\n"
        "Run verification with:\n\n"
        "```text\npy -V:3.12 -I -B scratch/t35/out/verify.py\npy -V:3.12 -I -B scripts/t01_anchors.py\n```\n",
        encoding="utf-8")
    return data


def write_report(data: dict) -> None:
    scan = data["semantic_candidate_scan"]
    ctx = data["parent_container_context"]
    client = ctx["profiles"].get("client", {})
    server = ctx["profiles"].get("server", {})
    near = data["near_miss_club_classes"]
    lines = [
        "# t35 Cafl/Cvfl 数据侧发现", "",
        "## 结果", "",
        "状态：`partial_no_semantic_candidate`。按 t14 的 74 个 RTTI/table type 和 stage2 的 45 条身份记录完成语义扫描；未找到 affiliation/link 类候选。Cafl、Cvfl 仍为 unknown。",
        "未对静态 cursor 做分析，也没有字段晋级 L3。", "",
        "## 候选扫描", "",
        f"- 正向语义候选：{scan['candidate_count']}。扫描词见 `profiles/semantic_candidate_scan.json`。",
        f"- t14 类型：{scan['scan_scope']['t14_types']}；stage2 记录：{scan['scan_scope']['stage2_rows']}。",
        f"- club-related RTTI near-miss：{len(near)} 项；它们没有 affiliation/link 类名或独立 Cafl/Cvfl join，不作为候选。",
        "- Cafl/Cvfl 的 29/19 个 schema item 字段按 master.json 与 t24 顺序交叉核对；它们仍是 schema 候选，不是数据列名。", "",
        "## 父表数据画像", "",
        "`table_type=3` 是 stage2 已解析的 club 父表，只作上下文，不能复制成 Cafl/Cvfl table_type。",
        f"- client：状态 `{client.get('status')}`；count={client.get('count')}；stride=variable；封口 `{client.get('closure_equation')}`；payload SHA-256 `{client.get('payload_sha256')}`。",
        f"- client 行跨度：{client.get('row_length_min')}..{client.get('row_length_max')} bytes，{client.get('distinct_row_lengths')} 种；标准 5B 聚合行 84,256，identity-only 紧凑行 3。",
        f"- server：状态 `{server.get('status')}`；payload bytes={server.get('payload_bytes')}；row_count_header={server.get('row_count_header')}；未做行 walker，不能给 count/stride/封口。",
        "- parent 原始 u32 lane 与 5B aggregate 的逐 bit 统计保存在 `profiles/parent_table3_context.json`；这些统计没有语义列名，不能视作 affiliation item 字段画像。", "",
        "## 视图假说", "",
        "结论倾向：`no_data_vote`，当前数据不能支持或反驳‘同一集合的两个视图’。没有找到两张 affiliation-like archive table，也没有提取到可检验的 Cafl/Cvfl item 列。",
        "保留反例/限制：RTTI 无命中不证明子表不存在；它可能嵌在 club 父记录或使用无语义 RTTI。client club 表中 3 条 compact body 仅由 identity 封口，未解 body 不作为视图证据。", "",
        "## Copy-ready", "",
        "`cafl_cvfl_discovery.json` 中 `copy_ready` 对 Cafl/Cvfl 分别保留 `candidate_table_type/archive/rtti_class/count/stride=unknown`、空 `item_field_candidates`、schema-only 字段和 blockers。",
        "与 sol 衔接：可复用‘无命中’和 table_type=3 仅为 parent context；下一步仍需沿已知 +0x118/+0x120 collection 找到独立 archive/row 证据，再做 item 列画像。", "",
        "## 验证与边界", "",
        "- 输入快照：master SHA-256 已与 evidence/MANIFEST.json 匹配；t14、stage2、t24 part 哈希与 t29 provenance 匹配。",
        "- `fm24_dump.py --archive client --table 3` 原命令因既有 `footer_offset` 十六进制字符串转 int 报错；本任务未改该脚本，使用了独立行 walker复算 client 闭合。",
        "- server table_type 3 只记录唯一 header-compatible frame 的 payload 元信息，没有推断行边界。", "",
        "验证命令：`py -V:3.12 -I -B scratch/t35/out/verify.py` 与 `py -V:3.12 -I -B scripts/t01_anchors.py`。", "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    try:
        provenance = ensure_input_hashes()
        fields = schema_item_fields()
        assert provenance["manifest_snapshot_date"] == "2026-11-18"
        assert len(fields["Cafl"]) == 29 and len(fields["Cvfl"]) == 19
        test = bytearray()
        test += struct.pack("<4I", 1, 2, 3, 4)
        test += bytes(5)
        test += struct.pack("<I", 7) + b"\0"
        test += struct.pack("<I", 1) + b"A"
        test += struct.pack("<I", 1) + b"B"
        test += bytes(3)
        test += struct.pack("<III", 0, 55, 55) + b"\0"
        parsed = parse_standard_row(bytes(test), 0, 0, 5)
        assert parsed and parsed["length"] == len(test)
        scan = discover_semantic_candidates(read_json(T14), read_json(STAGE2))
        assert scan["candidate_count"] == 0
    except Exception as exc:
        print(f"FAIL {type(exc).__name__}: {exc}")
        return 1
    print("PASS: frozen inputs, Cafl/Cvfl schema counts, row parser fixture, semantic scan (0 candidates)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--selftest", action="store_true", help="run offline source and parser checks")
    group.add_argument("--build", action="store_true", help="write t35 outputs under scratch/t35/out")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        result = build()
    except Exception as exc:
        print(f"fatal {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    parent = result["parent_container_context"]["profiles"].get("client", {})
    print(f"status={result['status']} candidates={result['semantic_candidate_scan']['candidate_count']} client_parent_rows={parent.get('count')} closure={parent.get('closure_equation')}")
    print("outputs: scratch/t35/out/cafl_cvfl_discovery.json, profiles/semantic_candidate_scan.json, profiles/parent_table3_context.json, REPORT.md, DONE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
