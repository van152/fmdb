#!/usr/bin/env python3
"""Build the t29b parent inventory from already-delivered evidence only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PROFILE_IDS = (33, 34, 37, 43, 50, 51, 60, 61, 62, 63, 64, 66, 70)
PROFILE_DIR = OUT / "profiles"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
SCOUT_REL = "scratch/t27/out/scout.json"
PARENT_FILES = sorted((ROOT / "scratch/t24/out").glob("subtables.part00*.json"))
LINKED_LEDGER = {37: "scratch/t30/out/fields_clhs.json", 62: "scratch/t31/out/fields_csrs.json"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def field_hints(field: dict, columns: list[dict]) -> dict:
    kind = field.get("type", "unknown")
    table = field.get("database_table_type", "")
    out = []
    for col in columns:
        width = col["width"]
        small = col.get("small_value_set")
        compatible = False
        score = 0.0
        reason = ""
        if kind == "database_record_unique_id" and width == 4:
            domains = col.get("reference_domains", {})
            domain = domains.get(table, {}) if table else {}
            if domain.get("ratio", 0) >= 0.80:
                compatible, score = True, domain["ratio"]
                reason = f"{table or 'reference'}-domain ratio {score:.3f}"
        elif kind == "boolean" and width == 1 and small is not None and len(small) == 2 and set(small) <= {0, 1}:
            compatible, score = True, 1.0
            reason = "observed byte domain is exactly {0,1}"
        elif kind == "day_of_week" and width == 1 and small is not None and 2 <= len(small) <= 8 and set(small) <= set(range(8)):
            compatible, score = True, 1.0
            reason = "observed byte domain is a subset of 0..7"
        elif kind in ("enum", "multiple_enum") and width == 1 and small is not None and 2 <= len(small) <= 32:
            compatible, score = True, 1.0 / len(small)
            reason = f"low-cardinality byte domain ({len(small)} values)"
        elif kind == "date" and width == 4:
            date = col.get("packed_day_year", {})
            if date.get("valid_ratio_nonblank", 0) >= 0.90 and date.get("nonblank_count", 0):
                compatible, score = date["valid_ratio_nonblank"], date["valid_ratio_nonblank"]
                reason = f"packed day/year valid ratio {score:.3f}"
        elif kind == "cash" and width == 4:
            signed = col.get("signed_i32", {})
            if signed.get("within_abs_1e9_rate_nonzero_nonnull", 0) >= 0.90:
                compatible, score = True, signed["within_abs_1e9_rate_nonzero_nonnull"]
                reason = f"signed cash-range rate {score:.3f}"
        elif kind == "real" and width == 4:
            finite = col.get("float32", {})
            if finite.get("finite_ratio", 0) >= 0.99:
                compatible, score = True, finite["finite_ratio"]
                reason = "finite float32 reinterpretation (weak diagnostic)"
        elif kind == "integer" and width in (1, 2, 4):
            lo, hi = field.get("min_value"), field.get("max_value")
            if lo is not None and hi is not None:
                try:
                    lo, hi = int(lo), int(hi)
                    if col.get("min_unsigned", lo - 1) >= max(0, lo) and col.get("max_unsigned", hi + 1) <= hi:
                        compatible, score = True, 1.0
                        reason = f"unsigned profile range within schema [{lo},{hi}]"
                except (TypeError, ValueError):
                    pass
    
        if compatible:
            out.append({"legacy_offset": col["offset"], "width": width, "score": round(float(score), 6), "basis": reason})
    out.sort(key=lambda x: (-x["score"], x["width"], x["legacy_offset"]))
    return {
        "profile_column_hint_count": len(out),
        "profile_column_hints": out[:12],
        "hints_truncated": len(out) > 12,
        "hint_policy": "type/statistics compatibility only; not a field-to-offset assignment",
    }


def main() -> None:
    manifest = read_json(ROOT / "evidence/MANIFEST.json")
    pins = {x["path"]: x["sha256"] for x in manifest["files"]}
    master_bytes = (ROOT / MASTER_REL).read_bytes()
    master_sha = sha(master_bytes)
    if pins.get(MASTER_REL) != master_sha or not master_sha.startswith("7d57477e"):
        raise SystemExit("frozen master.json SHA does not match evidence/MANIFEST.json")
    master = json.loads(master_bytes)
    club = master["entities"]["club.xml"][0]["fields"]
    schema_parents = {f["field"]: f.get("list_item_fields", []) for f in club if f.get("list_item_fields")}

    nested = []
    source_hashes = {}
    for path in PARENT_FILES:
        raw = path.read_bytes()
        source_hashes[path.relative_to(ROOT).as_posix()] = sha(raw)
        nested.extend(read_json(path)["nested_fields"])
    parents: dict[str, list[dict]] = {}
    for item in nested:
        parents.setdefault(item["parent"], []).append(item)
    for code, items in parents.items():
        items.sort(key=lambda x: x["idx"])
        schema_codes = [x.get("field") for x in schema_parents.get(code, [])]
        actual_codes = [x["code"] for x in items]
        schema_iter = iter(schema_codes)
        if schema_codes and not all(any(candidate == code for candidate in schema_iter) for code in actual_codes):
            raise SystemExit(f"t24 direct items are not an ordered subset of frozen schema for {code}: {actual_codes}")

    scout = read_json(ROOT / SCOUT_REL)
    scout_by_parent = {x["parent"]: x for x in scout["rows"] if x.get("parent")}
    scout_by_type = {x["table_id"]: x for x in scout["rows"] if isinstance(x.get("table_id"), int)}
    census = read_json(ROOT / "scratch/t14/out/census.json")
    census_by_type = {x["table_type"]: x for x in census["tables"]}
    stage2 = read_json(ROOT / "reports/stage2_table_identity.json")
    stage2_by_type = {x["table_type"]: x for x in stage2["rows"]}

    profiles = {}
    for tid in PROFILE_IDS:
        p = PROFILE_DIR / f"table_server_{tid}.profile.json"
        raw = p.read_bytes()
        profile = json.loads(raw)
        if profile.get("status") != "complete_data_profile" or profile.get("table_type") != tid:
            raise SystemExit(f"unexpected profile identity: {p}")
        profiles[tid] = (profile, sha(raw))

    ledger_docs = {tid: read_json(ROOT / rel) for tid, rel in LINKED_LEDGER.items()}
    ledger_fields = {
        tid: {f["code"]: f for f in doc["fields"]}
        for tid, doc in ledger_docs.items()
    }
    table_to_parent = {22: "Cstc", 33: "Cdbt", 34: "Tchl", 37: "Clhs", 43: "Cmti", 62: "CSrs", 66: "CNtp", 70: "CAmb"}
    parent_to_table = {parent: tid for tid, parent in table_to_parent.items()}
    parent_to_table.update({parent: row["table_id"] for parent, row in scout_by_parent.items()
                            if isinstance(row.get("table_id"), int)})

    def base_fields(parent: str) -> list[dict]:
        items = parents[parent]
        schema = schema_parents.get(parent, [])
        by_code: dict[str, list[dict]] = {}
        for sf in schema:
            by_code.setdefault(sf.get("field", ""), []).append(sf)
        result = []
        for item in items:
            candidates = by_code.get(item["code"], [])
            sf = candidates.pop(0) if candidates else {}
            result.append({
                "schema_idx": item["idx"], "field": item["code"], "name": item["name"],
                "type": item["type"], "optional": item.get("optional"),
                "database_table_type": sf.get("database_table_type"),
                "enum_ref": sf.get("enum_ref"), "min_value": sf.get("min_value"),
                "max_value": sf.get("max_value"),
            })
        return result

    parent_rows = []
    for parent in sorted(parents):
        tid = parent_to_table.get(parent)
        profile_entry = profiles.get(tid) if tid in profiles else None
        profile = profile_entry[0] if profile_entry else None
        scout_row = scout_by_parent.get(parent, {})
        table_scout = scout_by_type.get(tid, {}) if tid is not None else {}
        class_row = census_by_type.get(tid, {}) if tid is not None else {}
        s2 = stage2_by_type.get(tid, {}) if tid is not None else {}
        rtti = (profile or {}).get("rtti_class") or scout_row.get("RTTI") or class_row.get("primary_class") or "unknown"
        reader_va = scout_row.get("reader_VA") or table_scout.get("reader_VA") or (profile or {}).get("identity_basis", {}).get("reader_va")
        if parent == "CAmb":
            link_status, confidence = "candidate_semantic", "candidate"
            blockers = ["table 70 RTTI STARTING_VISION_OBJECTIVE is semantically compatible with CAmb, but no direct parent collection/reader join is present in t27 or t14."]
        elif tid == 37:
            link_status, confidence = "linked_field_ledger_L3", "high"
            blockers = ["The t30 ledger has 8 L3 fields and preserves 4 sink/profile conflicts as held; no further field promotion is inferred here."]
        elif tid == 62:
            link_status, confidence = "linked_field_ledger_L3", "high"
            blockers = ["The t31 ledger binds CSrs to table 62 and has 10 L3 fields; this inventory does not expand beyond that ledger."]
        elif scout_row.get("status") == "complete_E56_parent_link":
            link_status, confidence = "linked_by_t27", "high"
            blockers = ["Parent/table link is established by t27; t29b did not re-walk table 22 or revalidate its item offsets."]
        elif tid is not None:
            link_status, confidence = "candidate", "candidate"
            blockers = ["RTTI semantics and scout/table evidence support this parent candidate, but an end-to-end parent collection to reader sink join is not established."]
            if s2.get("status") == "candidate":
                blockers.append("stage2_table_identity.json keeps this table entity adjudication at candidate.")
        else:
            link_status, confidence = "unknown", "unknown"
            blockers = ["No supported table_type-to-parent join; table_type, archive count and stride remain unknown."]
        if parent in ("Cafl", "Cvfl"):
            blockers = ["t27 records a shared getter collection lead at club offsets +0x118/+0x120; standalone storage, writer/reader and independent archive member are unproven.",
                        "Preserve the Cafl/Cvfl dual-view ambiguity; do not count them as two independent tables."]
        if parent == "Csme":
            blockers = ["Table 59 / STARTING_MEDIA_EXPECTATIONS / reader 0x141583ba0 is a scout candidate only; stride and the parent-to-member link are unresolved."]

        fields = base_fields(parent)
        item_candidates = []
        for field in fields:
            code = field["field"]
            if tid in ledger_fields and code in ledger_fields[tid]:
                row = ledger_fields[tid][code]
                sink = row.get("candidate_sink", {})
                grade = row.get("grade", "candidate")
                field_offset = row.get("row_offset")
                item_candidates.append({
                    **field,
                    "status": "L3" if grade == "L3_named_row_coordinate" else "held",
                    "evidence_level": "L3" if grade == "L3_named_row_coordinate" else "held_pending_domain",
                    "confidence": "high" if grade == "L3_named_row_coordinate" else "held",
                    "legacy_offset": field_offset if field_offset is not None else sink.get("legacy_offset"),
                    "wire_offset": row.get("wire_offset") if row.get("wire_offset") is not None else sink.get("wire_offset"),
                    "width": sink.get("width"),
                    "grade": grade,
                    "blocker": None if grade == "L3_named_row_coordinate" else "t30 retains the reader sink as a candidate but full-table values conflict with the frozen schema domain; do not promote.",
                })
            elif profile is not None and link_status in ("candidate", "candidate_semantic"):
                hints = field_hints(field, profile["columns"])
                item_candidates.append({
                    **field, "status": "candidate", "evidence_level": "L2_candidate",
                    "confidence": "low_candidate", **hints,
                    "blocker": "Schema item semantics and profile column diagnostics are compatible only; no reader sink/unique row coordinate is proven.",
                })
        profile_summary = None
        if profile is not None:
            closure = profile["row_closure"]
            profile_summary = {
                "profile_file": f"profiles/table_server_{tid}.profile.json",
                "profile_sha256": profile_entry[1], "rows_file": profile["full_rows_file"],
                "rows_jsonl_sha256": profile["full_rows_sha256"],
                "rows_sha256": closure["rows_sha256"], "payload_sha256": profile["payload"]["payload_sha256"],
                "payload_size": closure["payload_bytes"], "packed_offset": profile["payload"].get("packed_offset"),
                "count": closure["count"], "stride": closure["stride"],
                "row_start": closure["row_start"], "footer_bytes": closure["footer_bytes"],
                "profile_status": profile["status"],
            }
        count = profile["row_closure"]["count"] if profile else scout_row.get("archive_index", {}).get("server", {}).get("count")
        stride = profile["row_closure"]["stride"] if profile else (scout_row.get("stride") or {}).get("server")
        if isinstance(stride, dict):
            stride = stride.get("server")
        archive = profile.get("archive") if profile else ("client+server" if parent == "Cstc" else ("server" if count is not None else "unknown"))
        if parent == "Cstc":
            count, stride = {"client": 449, "server": 449}, {"client": 13, "server": 79}
        table_value = tid if tid is not None else "unknown"
        entity = s2.get("entity")
        if entity is None and profile:
            entity = profile.get("entity_tag")
        attribution = "unresolved" if s2.get("status") == "negative" or entity is None else entity
        if s2.get("status") == "negative":
            blockers.append("Consolidated stage2 adjudication is negative for an entity assignment; retain unresolved attribution.")
        if table_value == 70:
            attribution = "club-like candidate (profile/T14 tag only; exact parent/entity path unresolved)"
        parent_rows.append({
            "parent_4cc": parent, "table_type": table_value, "archive": archive,
            "rtti_class": rtti, "reader_va": reader_va, "count": count, "stride": stride,
            "confidence": confidence, "link_status": link_status,
            "entity_attribution": attribution, "stage2_status": s2.get("status", (profile or {}).get("stage2_status")),
            "schema_item_fields": fields, "item_field_candidates": item_candidates,
            "profile": profile_summary, "blockers": blockers,
        })

    unjoined = []
    for tid in (50, 51, 60, 61, 63, 64):
        profile, profile_sha = profiles[tid]
        c = census_by_type[tid]
        s2 = stage2_by_type.get(tid, {})
        scout_row = scout_by_type.get(tid, {})
        closure = profile["row_closure"]
        blockers = ["No club.xml nested parent link is established; do not assign this table to a similarly named list without a reader/collection join."]
        if tid in (50, 51):
            blockers.append("stage2_table_identity.json explicitly records a negative entity adjudication for this fieldless table.")
        elif tid in (60, 61, 63):
            blockers.append("RTTI/class name mentions MLS or Italian non-EU slots, while current evidence does not resolve the owning entity; possible nation/competition/other ownership remains open.")
        else:
            blockers.append("t27 identifies STARTING_CLUB_STAFF_JOB_STATUS (reader 0x141584350) but leaves the exact schema parent unjoined.")
        if tid == 34:
            pass
        if s2.get("status") == "negative":
            entity = "unresolved"
        elif tid == 64:
            entity = "club-like RTTI label; parent unresolved"
        else:
            entity = "unresolved; profile/T14 class tag is not a nested-parent proof"
        unjoined.append({
            "parent_4cc": None, "table_type": tid, "archive": profile["archive"],
            "rtti_class": profile["rtti_class"], "reader_va": scout_row.get("reader_VA") or profile["identity_basis"].get("reader_va"),
            "count": closure["count"], "stride": closure["stride"], "confidence": "unresolved",
            "link_status": "profiled_unjoined", "entity_attribution": entity,
            "stage2_status": s2.get("status", profile.get("stage2_status")),
            "item_field_candidates": [], "blockers": blockers,
            "profile": {
                "profile_file": f"profiles/table_server_{tid}.profile.json", "profile_sha256": profile_sha,
                "rows_file": profile["full_rows_file"], "rows_jsonl_sha256": profile["full_rows_sha256"],
                "rows_sha256": closure["rows_sha256"], "payload_sha256": profile["payload"]["payload_sha256"],
                "payload_size": closure["payload_bytes"], "packed_offset": profile["payload"].get("packed_offset"),
                "count": closure["count"], "stride": closure["stride"], "row_start": closure["row_start"],
                "footer_bytes": closure["footer_bytes"], "profile_status": profile["status"],
            },
        })

    profile_rows = []
    for tid in PROFILE_IDS:
        profile, profile_sha = profiles[tid]
        cl = profile["row_closure"]
        profile_rows.append({
            "table_type": tid, "archive": profile["archive"], "parent_4cc": table_to_parent.get(tid),
            "rtti_class": profile["rtti_class"], "count": cl["count"], "stride": cl["stride"],
            "payload_size": cl["payload_bytes"], "payload_sha256": profile["payload"]["payload_sha256"],
            "packed_offset": profile["payload"].get("packed_offset"),
            "rows_file": profile["full_rows_file"], "rows_jsonl_sha256": profile["full_rows_sha256"],
            "rows_sha256": cl["rows_sha256"], "profile_file": f"profiles/table_server_{tid}.profile.json",
            "profile_sha256": profile_sha,
        })

    unknown = sorted(code for code in parents if parent_to_table.get(code) is None)
    candidate_fields = sum(1 for row in parent_rows for f in row["item_field_candidates"] if f["status"] == "candidate")
    l3_fields = sum(1 for row in parent_rows for f in row["item_field_candidates"] if f["status"] == "L3")
    held_fields = sum(1 for row in parent_rows for f in row["item_field_candidates"] if f["status"] == "held")
    hint_fields = sum(1 for row in parent_rows for f in row["item_field_candidates"] if f.get("profile_column_hint_count", 0))
    inv = {
        "status": "partial_parent_identity_coverage",
        "task": "t29b club nested-subtable inventory; synthesis only, no redump",
        "generated_on": "2026-11-19",
        "provenance": {
            "master_path": MASTER_REL, "master_sha256": master_sha,
            "manifest_snapshot_date": manifest.get("snapshot_date"),
            "manifest_sha256": sha((ROOT / "evidence/MANIFEST.json").read_bytes()),
            "t24_subtables_sha256": source_hashes,
            "t27_scout_sha256": sha((ROOT / SCOUT_REL).read_bytes()),
            "t14_census_sha256": sha((ROOT / "scratch/t14/out/census.json").read_bytes()),
            "stage2_identity_sha256": sha((ROOT / "reports/stage2_table_identity.json").read_bytes()),
            "field_ledgers": {str(tid): {"path": rel, "sha256": sha((ROOT / rel).read_bytes())} for tid, rel in LINKED_LEDGER.items()},
            "profile_basis": "existing complete_data_profile JSON and rows.jsonl only; no archive payload reread",
            "table34_sampling_note": "Use the existing table_server_34 profile/rows; its recorded packed_offset is the +34-byte zstd-frame origin, not the +9-byte empty stub.",
            "evidence_grade_policy": "L2 entries remain candidates; L3 only where t30/t31 field ledgers already provide it; L4=0",
        },
        "summary": {
            "nested_parent_count": len(parent_rows), "profile_count": len(profile_rows),
            "profiled_parent_links": sum(1 for row in parent_rows if row["profile"] is not None),
            "unknown_parent_count": len(unknown), "unknown_parent_codes": unknown,
            "l2_item_field_candidate_count": candidate_fields,
            "candidate_fields_with_profile_column_hints": hint_fields,
            "l3_item_field_count": l3_fields, "held_item_field_count": held_fields,
            "unjoined_profiled_table_count": len(unjoined), "L4": 0,
        },
        "tables": profile_rows,
        "parents": parent_rows,
        "unjoined_tables": unjoined,
        "next_scout": [
            {"parent_4cc": code, "table_type": "unknown", "priority": "high" if code in ("Cafl", "Cvfl", "CAmb", "CpTI", "Calt", "Cspb", "Coin", "Camc") else "normal",
             "blocker": next((b for r in parent_rows if r["parent_4cc"] == code for b in r["blockers"]), "No table identity or reader anchor in current scout.")}
            for code in unknown
        ],
    }
    (OUT / "subtable_inventory.json").write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(inv["summary"], ensure_ascii=False))
    print(f"wrote {OUT / 'subtable_inventory.json'}")


if __name__ == "__main__":
    main()
