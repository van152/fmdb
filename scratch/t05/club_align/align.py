#!/usr/bin/env python3
"""Ordered schema/reader width alignment and evidence-limited club mapping.

Only this task directory is written.  The public ``align_fields`` function is
usable with caller-provided schema fields, transfer widths, row width, anchors,
and optional value samples.  A zero-width transition represents a schema value
not serialized inline; collections are kept unresolved unless their frame is
explicitly supplied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

OUTDIR = Path(__file__).resolve().parent
ROOT = OUTDIR.parents[2]
OLD_ROOT = ROOT.parent / "fm24"
SCHEMA_MD = OLD_ROOT / "reports" / "EDITOR_SCHEMA_FIELDS.md"
SCHEMA_INVENTORY = ROOT / "scratch" / "t05" / "schema_inventory.json"
SCHEMA_SNAPSHOT = ROOT / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
MANIFEST = ROOT / "evidence" / "MANIFEST.json"
SUBSTRATE = ROOT / "scratch" / "t02" / "field_mapper" / "club_substrate.json"
CLUB_L3 = ROOT / "scratch" / "t02" / "inbox" / "club_fields" / "output.json"
CLUB_FRAME = ROOT / "scratch" / "t02" / "inbox" / "club_v2" / "output.json"

# Fallbacks mirror scratch/t05/schema_inventory.json.  The inventory is the
# task-local canonical field-order/type source and also supplies optional flags.
TYPE_WIDTHS: dict[str, tuple[int, ...]] = {
    "boolean": (1, 0), "enum": (1, 2, 4), "multiple_enum": (1, 2, 4),
    "day_of_week": (1,), "integer": (1, 2, 4), "date": (2, 4),
    "colour": (3, 4), "database_record_unique_id": (4,), "unique_id": (8,),
    "cash": (4,), "real": (4,), "short_distance": (1, 2),
    "string": (4, 0), "picture": (4, 0), "list": (0,),
    "database_record_list": (0,),
}
_INVENTORY_CACHE: dict[str, Any] | None = None


def load_inventory() -> dict[str, Any]:
    global _INVENTORY_CACHE
    if _INVENTORY_CACHE is None:
        _INVENTORY_CACHE = json.loads(SCHEMA_INVENTORY.read_text(encoding="utf-8"))
    return _INVENTORY_CACHE


def inventory_fields(entity: str) -> list[dict[str, Any]]:
    raw = load_inventory()["entities"][entity]["fields"]
    return [{"field": x["code"], "name": x["name"], "type": x["type"],
             "top_level": x["parent"] is None, "parent_list": x["parent"],
             "optional": bool(x["optional"]), "field_index": int(x["idx"])} for x in raw]


def _schema_section(text: str, entity: str) -> tuple[str, int]:
    heading = re.compile(
        rf"^### {re.escape(entity)}（记录标识 `[^`]+`，(\d+) 个字段）\s*$", re.M
    )
    match = heading.search(text)
    if not match:
        raise ValueError(f"schema section not found: {entity}")
    end = re.search(r"^### ", text[match.end():], re.M)
    body_end = match.end() + end.start() if end else len(text)
    return text[match.end():body_end], int(match.group(1))


def parse_markdown_schema(path: Path, entity: str) -> tuple[list[dict[str, Any]], int]:
    text = path.read_text(encoding="utf-8")
    body, declared_count = _schema_section(text, entity)
    fields: list[dict[str, Any]] = []
    active_list: str | None = None
    list_heading = re.compile(r"列表项字段（([^）]+)）")
    cell = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
    for line in body.splitlines():
        if "↳ 列表项字段（" in line:
            m = list_heading.search(line)
            active_list = m.group(1) if m else None
            continue
        m = cell.match(line)
        if not m:
            continue
        code, name, typ = (x.strip() for x in m.groups())
        nested = not line.startswith("| `")
        if nested:
            fields.append({"field": code, "name": name, "type": typ,
                           "top_level": False, "parent_list": active_list})
        else:
            fields.append({"field": code, "name": name, "type": typ,
                           "top_level": True, "parent_list": None})
            active_list = code if typ in ("list", "database_record_list") else None
    top = [f for f in fields if f["top_level"]]
    if len(top) != declared_count:
        raise ValueError(f"{entity}: markdown declares {declared_count} top-level fields, parsed {len(top)}")
    return fields, declared_count


def candidate_widths(field: dict[str, Any], anchor: dict[str, Any] | None = None) -> tuple[int, ...]:
    typ = field.get("type", "")
    inventory = load_inventory()
    widths = tuple(inventory.get("type_width_candidates", {}).get(typ, {}).get(
        "candidates", TYPE_WIDTHS.get(typ, ())))
    if field.get("optional") and 0 not in widths:
        widths += (0,)
    # Explicit byte evidence may correct the generic type prior; never inferred.
    if anchor and isinstance(anchor.get("width"), int) and anchor.get("type_width_override"):
        return (anchor["width"],)
    return widths


def _sample_score(samples: dict[str, Any] | None, field_code: str, width: int) -> tuple[int, int]:
    """Return (passed checks, total checks) for simple, caller-declared validators."""
    if not samples or field_code not in samples:
        return 0, 0
    spec = samples[field_code]
    values = spec.get("values", []) if isinstance(spec, dict) else []
    kind = spec.get("kind") if isinstance(spec, dict) else None
    passed = 0
    for value in values:
        ok = True
        if kind == "reference":
            target_rows = int(spec["target_rows"])
            ok = value in spec.get("sentinels", []) or (isinstance(value, int) and 0 <= value < target_rows)
        elif kind == "enum":
            cardinality = int(spec["cardinality"])
            ok = isinstance(value, int) and 0 <= value < cardinality
        elif kind == "date":
            ok = isinstance(value, int) and 1500 <= value <= 2200
        elif kind == "colour":
            ok = isinstance(value, (list, tuple)) and len(value) in (3, 4) and all(
                isinstance(c, int) and 0 <= c <= 255 for c in value
            )
        passed += int(ok)
    return passed, len(values)


def align_fields(
    schema_fields: list[dict[str, Any]],
    reader_widths: list[int],
    row_width: int,
    anchors: dict[str, dict[str, Any]] | None = None,
    samples: dict[str, Any] | None = None,
    max_solutions: int = 256,
    prefix_width: int = 0,
    suffix_width: int = 0,
) -> list[dict[str, Any]]:
    """Enumerate type-compatible, order-preserving exact-width alignments.

    Every reader event is consumed by exactly one schema field. A field may
    take a zero-width transition when optional or non-inline. Prefix/suffix
    reserve framing bytes (e.g. identity trailers) outside the scalar sequence.
    Repeated field codes should be disambiguated by using
    ``field_index`` on schema items and anchor keys ``#<index>``.
    """
    anchors = anchors or {}
    top = [f for f in schema_fields if f.get("top_level", True)]
    code_indices: dict[str, list[int]] = {}
    for i, field in enumerate(top):
        code_indices.setdefault(field["field"], []).append(i)
    constraints: dict[int, dict[str, Any]] = {}
    for key, value in anchors.items():
        if key.startswith("#"):
            idx = int(key[1:])
        else:
            hits = code_indices.get(key, [])
            if len(hits) != 1:
                raise ValueError(f"anchor {key!r} is ambiguous or absent; use #field_index")
            idx = hits[0]
        if idx < 0 or idx >= len(top):
            raise ValueError(f"anchor index out of range: {idx}")
        constraints[idx] = value

    # Memoized state traversal; path tuples hold (field index, offset, width).
    memo: dict[tuple[int, int, int], list[tuple[tuple[int, int, int], ...]]] = {}

    def visit(i: int, j: int, offset: int):
        state = (i, j, offset)
        if state in memo:
            return memo[state]
        if offset > row_width:
            return []
        if i == len(top):
            result = [()] if j == len(reader_widths) and offset == row_width - suffix_width else []
            memo[state] = result
            return result
        field = top[i]
        code = field["field"]
        anchor = constraints.get(i)
        options = candidate_widths(field, anchor)
        found: list[tuple[tuple[int, int, int], ...]] = []
        if anchor is None or anchor.get("offset") == offset:
            # Non-inline schema fields do not consume reader events.
            if 0 in options and (anchor is None or anchor.get("width", 0) == 0):
                for tail in visit(i + 1, j, offset):
                    found.append(((i, offset, 0),) + tail)
                    if len(found) >= max_solutions:
                        break
            # Inline events preserve both schema order and reader order.
            if j < len(reader_widths):
                width = reader_widths[j]
                if width in options and width > 0 and (anchor is None or anchor.get("width", width) == width):
                    for tail in visit(i + 1, j + 1, offset + width):
                        found.append(((i, offset, width),) + tail)
                        if len(found) >= max_solutions:
                            break
        memo[state] = found[:max_solutions]
        return memo[state]

    if prefix_width < 0 or suffix_width < 0 or prefix_width + suffix_width > row_width:
        raise ValueError("invalid framing prefix/suffix widths")
    raw = visit(0, 0, prefix_width)
    solutions = []
    for path in raw:
        mapped = []
        for i, offset, width in path:
            f = top[i]
            mapped.append({"field": f["field"], "field_index": i, "offset": offset,
                           "width": width, "type": f["type"]})
        by_code: dict[str, list[dict[str, Any]]] = {}
        for row in mapped:
            by_code.setdefault(row["field"], []).append(row)
        checks = total = 0
        for code, spec in (samples or {}).items():
            widths = by_code.get(code, [])
            if widths:
                passed, count = _sample_score(samples, code, widths[0]["width"])
                checks += passed
                total += count
        solutions.append({"fields": mapped, "data_checks_passed": checks,
                          "data_checks_total": total,
                          "score": checks / total if total else 0.0})
    solutions.sort(key=lambda s: (-s["score"], tuple((x["offset"], x["width"]) for x in s["fields"])))
    return solutions


FIXTURES: dict[str, dict[str, Any]] = {
    "award": {
        "row_width": 77, "field_count": 38, "count": 3545, "stride": 77,
        "member_length": 272987, "header": 14, "footer": 8, "frame_prefix": 0, "frame_suffix": 13,
        "anchors": [
            {"field": "rdui", "offset": 64, "width": 4, "kind": "u32"},
            {"field": "duni", "offset": 68, "width": 8, "kind": "duplicate-u32 pair"},
        ],
        "variable": False,
    },
    "city": {
        "row_width": 43, "field_count": 15, "count": 56293, "stride": 43,
        "member_length": 2420621, "header": 14, "footer": 8, "frame_prefix": 1, "frame_suffix": 13,
        "anchors": [
            {"field": "Clat", "offset": 1, "width": 4, "kind": "f32"},
            {"field": "Clon", "offset": 5, "width": 4, "kind": "f32"},
            {"field": "Cnti", "offset": 10, "width": 4, "kind": "u32", "task_prompt_width": 1,
             "evidence": "scratch/t02/city_reference.json: row sample has 83 00 00 00 at +10 and reader mov r8d,4"},
            {"field": "rdui", "offset": 30, "width": 4, "kind": "u32"},
            {"field": "duni", "offset": 34, "width": 8, "kind": "duplicate-u32 pair"},
        ],
        "variable": False,
    },
    "stadium": {
        "row_width": 38, "field_count": 60, "count": 48413, "stride": 38,
        "member_length": 1839716, "header": 14, "footer": 8, "frame_prefix": 3, "frame_suffix": 13,
        "anchors": [
            {"field": "Scti", "offset": 3, "width": 4, "kind": "u32"},
            {"field": "Slat", "offset": 17, "width": 4, "kind": "f32"},
            {"field": "Slon", "offset": 21, "width": 4, "kind": "f32"},
            {"field": "rdui", "offset": 25, "width": 4, "kind": "u32"},
            {"field": "duni", "offset": 29, "width": 8, "kind": "duplicate-u32 pair"},
        ],
        "variable": False,
    },
    "injury": {
        "row_width": 16, "field_count": 27, "count": 115, "stride": 16,
        "member_length": 1862, "header": 14, "footer": 8, "frame_prefix": 0, "frame_suffix": 13,
        "anchors": [
            {"field": "rdui", "offset": 3, "width": 4, "kind": "u32"},
            {"field": "duni", "offset": 7, "width": 8, "kind": "duplicate-u32 pair"},
        ],
        "variable": False,
    },
    "language": {
        "row_width": None, "field_count": 12, "count": 126, "stride": None,
        "member_length": 5248, "header": 14, "footer": 8,
        "body_bytes": 5226, "frame_suffix": 30,
        "anchors": [
            {"field": "rdui", "offset": 17, "width": 4, "kind": "u32 ordinal relative to 17B suffix"},
        ],
        "variable": True,
    },
}


def _field_index(fields: list[dict[str, Any]], code: str) -> int | None:
    hits = [i for i, f in enumerate(fields) if f.get("top_level", True) and f["field"] == code]
    return hits[0] if len(hits) == 1 else None


def _fixture_result(name: str, spec: dict[str, Any]) -> dict[str, Any]:
    md_fields, md_declared = parse_markdown_schema(SCHEMA_MD, name)
    all_fields = inventory_fields(name)
    top = [f for f in all_fields if f["top_level"]]
    md_top = [f for f in md_fields if f["top_level"]]
    declared = load_inventory()["entities"][name]["declared_fields"]
    if declared != spec["field_count"] or md_declared != declared:
        raise ValueError(f"{name}: schema/inventory/fixture field counts disagree")
    if [f["field"] for f in top] != [f["field"] for f in md_top]:
        raise ValueError(f"{name}: schema inventory order does not match authoritative markdown")
    closure = (
        spec["header"] + spec["count"] * spec["stride"] + spec["footer"] == spec["member_length"]
        if not spec["variable"] else
        spec["header"] + spec["body_bytes"] + spec["footer"] == spec["member_length"]
    )
    # duni/rdui are framing suffix anchors, not members of the business-width
    # DP.  Compare only business anchors for schema-order contradictions.
    business_anchors = [a for a in spec["anchors"] if a["field"] not in ("duni", "rdui")]
    ordered = sorted(((_field_index(top, a["field"]), a) for a in business_anchors),
                     key=lambda pair: pair[0] if pair[0] is not None else -1)
    conflicts = []
    previous = None
    for idx, anchor in ordered:
        if idx is None:
            conflicts.append({"field": anchor["field"], "reason": "schema code is not unique top-level field"})
            continue
        if previous and anchor["offset"] < previous[1]["offset"]:
            conflicts.append({
                "before": previous[1]["field"], "before_schema_index": previous[0],
                "before_offset": previous[1]["offset"], "after": anchor["field"],
                "after_schema_index": idx, "after_offset": anchor["offset"],
                "reason": "business anchor offsets reverse schema field order",
            })
        previous = (idx, anchor)
    type_mismatches = []
    prompt_width_conflicts = []
    for anchor in spec["anchors"]:
        idx = _field_index(top, anchor["field"])
        if idx is None:
            continue
        f = top[idx]
        generic = candidate_widths(f)
        if anchor["width"] not in generic:
            type_mismatches.append({"field": anchor["field"], "schema_type": f["type"],
                                    "anchor_width": anchor["width"],
                                    "generic_candidates": list(generic)})
        if anchor.get("task_prompt_width") is not None and anchor["task_prompt_width"] != anchor["width"]:
            prompt_width_conflicts.append({"field": anchor["field"],
                                           "prompt_width": anchor["task_prompt_width"],
                                           "supported_width": anchor["width"],
                                           "evidence": anchor.get("evidence")})
    frame_anchors = [a for a in spec["anchors"] if a["field"] in ("duni", "rdui")]
    frame_ok = None
    if spec["variable"]:
        ordinal = next((a for a in frame_anchors if a["field"] == "rdui"), None)
        frame_ok = bool(ordinal and ordinal["offset"] == 17 and ordinal["width"] == 4)
    elif spec.get("row_width") is not None:
        rdui = next((a for a in frame_anchors if a["field"] == "rdui"), None)
        duni = next((a for a in frame_anchors if a["field"] == "duni"), None)
        frame_ok = bool(rdui and duni and rdui["width"] == 4 and duni["width"] == 8 and
                        rdui["offset"] == spec["row_width"] - 13 and
                        duni["offset"] == rdui["offset"] + 4 and
                        duni["offset"] + 8 == spec["row_width"] - 1)
    prefix = spec.get("frame_prefix", 0)
    suffix = spec.get("frame_suffix", 0)
    business_bytes = (spec["row_width"] - prefix - suffix
                      if spec["row_width"] is not None else None)
    return {
        "fixture": name,
        "schema_field_count": len(top),
        "schema_scalar_count": load_inventory()["entities"][name]["scalars"],
        "anchors_recovered_by_ordered_dp": 0,
        "anchor_count": len(spec["anchors"]),
        "frame_anchor_count": len(frame_anchors),
        "frame_anchors_recovered": len(frame_anchors) if frame_ok else 0,
        "row_width": spec["row_width"],
        "row_closure": {"header": spec["header"], "rows": spec["count"],
                         "stride": spec["stride"], "body_bytes": spec.get("body_bytes"),
                         "footer": spec["footer"], "member_length": spec["member_length"],
                         "exact": closure},
        "business_region": {"prefix_width": prefix, "suffix_width": suffix,
                            "available_bytes": business_bytes,
                            "reader_width_sequence_available": False},
        "identity_frame_anchors_consistent": frame_ok,
        "ordered_schema_alignment_feasible_from_anchors": not conflicts and not type_mismatches,
        "schema_order_conflicts": conflicts,
        "type_width_conflicts": type_mismatches,
        "prompt_width_conflicts": prompt_width_conflicts,
        "reader_width_sequence_available": False,
        "status": "FAIL",
        "blocked_reason": "No complete per-field reader-width sequence is available in the fixture inputs.",
        "limitation": "The row closure and frame anchors are checked separately; the ordered DP needs the actual per-field reader widths and cannot claim recovery from copied expected offsets.",
    }


def _algorithm_unit_test() -> dict[str, Any]:
    fields = [
        {"field": "small", "type": "integer", "top_level": True},
        {"field": "maybe", "type": "database_record_unique_id", "optional": True, "top_level": True},
        {"field": "nation", "type": "database_record_unique_id", "top_level": True},
    ]
    solutions = align_fields(
        fields, [2, 4], 10, {"nation": {"offset": 3, "width": 4}},
        {"nation": {"kind": "reference", "target_rows": 100, "values": [0, 99]}},
        prefix_width=1, suffix_width=3,
    )
    ok = (len(solutions) == 1 and
          [(x["field"], x["offset"], x["width"]) for x in solutions[0]["fields"]] ==
          [("small", 1, 2), ("maybe", 3, 0), ("nation", 3, 4)] and
          solutions[0]["data_checks_passed"] == 2)
    return {"status": "PASS" if ok else "FAIL", "solution_count": len(solutions),
            "checks": ["ordered transfer consumption", "optional field omission", "frame prefix/suffix", "anchor offset", "row-width closure", "reference sample scoring"]}


def run_selftest() -> dict[str, Any]:
    fixtures = [_fixture_result(name, spec) for name, spec in FIXTURES.items()]
    unit = _algorithm_unit_test()
    all_fixture_pass = all(f["status"] == "PASS" for f in fixtures)
    return {"task": "t05b ordered schema-reader alignment fixtures",
            "status": "PASS" if all_fixture_pass and unit["status"] == "PASS" else "FAIL",
            "fixture_count": len(fixtures),
            "pass_count": sum(f["status"] == "PASS" for f in fixtures),
            "fail_count": sum(f["status"] == "FAIL" for f in fixtures),
            "blocked_count": sum(bool(f.get("blocked_reason")) for f in fixtures),
            "algorithm_unit_test": unit,
            "fixtures": fixtures}


def _manifest_hash(path: str) -> str | None:
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for item in manifest.get("files", []):
        if item.get("path") == path:
            return item.get("sha256")
    return None


def _build_club_result() -> dict[str, Any]:
    markdown_fields, markdown_declared = parse_markdown_schema(SCHEMA_MD, "club")
    parsed = inventory_fields("club")
    top = [f for f in parsed if f["top_level"]]
    children = [f for f in parsed if not f["top_level"]]
    declared = load_inventory()["entities"]["club"]["declared_fields"]
    if markdown_declared != declared or [f["field"] for f in top] != [f["field"] for f in markdown_fields if f["top_level"]]:
        raise ValueError("club schema inventory order/count disagrees with authoritative markdown")
    source_l3 = json.loads(CLUB_L3.read_text(encoding="utf-8"))
    substrate = json.loads(SUBSTRATE.read_text(encoding="utf-8"))
    frame = json.loads(CLUB_FRAME.read_text(encoding="utf-8"))
    closed = next((row for row in source_l3.get("row_offset_map", []) if row.get("field") == "Cccn"), None)
    if not closed:
        raise ValueError("expected prior Cccn L3 evidence is absent")
    ev = closed["evidence"]
    named = [{
        "field": "Cccn", "offset": 8, "width": 4,
        "evidence": {
            "reader_file_offset": ev["reader_destination"]["file_offset"],
            "bytes": ev["reader_destination"]["bytes"],
            "width_file_offset": ev["reader_width"]["file_offset"],
            "width_bytes": ev["reader_width"]["bytes"],
            "transfer_file_offset": ev["reader_transfer"]["file_offset"],
            "transfer_bytes": ev["reader_transfer"]["bytes"],
            "getter_cmp_file_offset": ev["getter"]["file_offset"],
            "getter_cmp_bytes": ev["getter"]["bytes"],
            "getter_member_file_offset": ev["getter_member_read"]["file_offset"],
            "getter_member_bytes": ev["getter_member_read"]["bytes"],
            "source_evidence_file": "scratch/t02/inbox/club_fields/output.json",
        },
        "reader_mode": "CLUB",
        "confidence": "low",
        "data_validation": {
            "status": "blocked",
            "reason": "The row framing closes globally, but its proposed ordinal split has no per-row class byte and the three compact bodies are only identity-framed. The task forbids merging CLUB and LEAGUE_BODY_CLUB; no mode-safe table-wide Cccn value distribution is available.",
            "prior_single_sample": {"row": 69709, "bytes": "85 00 00 00", "note": "At this framed row, +8 repeats row+0 identity bytes; because the CLUB reader and framing/class partition are not linked per row, this is not Cccn data validation."},
        },
        "mapping_basis": "Existing getter 4CC -> object member +0xf0, CLUB reader sink to the same member, fixed width 4, and a single row-cursor candidate +8 in that reader's local analysis. This is not transferred to the LEAGUE_BODY_CLUB stream.",
    }]
    children_by_parent: dict[str, list[dict[str, Any]]] = {}
    for child in children:
        children_by_parent.setdefault(child["parent_list"], []).append(child)

    def item_tree(parent: str, active: frozenset[str] = frozenset()) -> list[dict[str, Any]]:
        if parent in active:
            raise ValueError(f"cyclic list schema at {parent}")
        out = []
        for child in children_by_parent.get(parent, []):
            node = {"field": child["field"], "type": child["type"], "name": child["name"]}
            descendants = item_tree(child["field"], active | {parent})
            if descendants:
                node["item_fields"] = descendants
            out.append(node)
        return out

    collections = []
    for f in top:
        if f["type"] not in ("list", "database_record_list"):
            continue
        collections.append({
            "field": f["field"], "kind": f["type"], "count_offset": None,
            "item_width": None,
            "item_fields": item_tree(f["field"]),
            "status": "unresolved",
            "reason": "No uniquely closed count/segment reader and row offset evidence; nested item schema is recorded only.",
        })
    prior_candidates = {x["field"]: x for x in source_l3.get("unclosed", [])
                        if isinstance(x, dict) and x.get("field")}
    unresolved = []
    for i, f in enumerate(top):
        if f["field"] == "Cccn":
            continue
        item = {"field_index": i, "field": f["field"], "name": f["name"],
                "type": f["type"], "reason": "No mode-safe L3 getter→reader→row-offset closure with required data validation."}
        if f["field"] in prior_candidates:
            item["prior_unclosed_candidate"] = prior_candidates[f["field"]]
        unresolved.append(item)
    schema_digest = hashlib.sha256(SCHEMA_SNAPSHOT.read_bytes()).hexdigest()
    inventory_digest = hashlib.sha256(SCHEMA_INVENTORY.read_bytes()).hexdigest()
    manifest_digest = _manifest_hash("evidence/fm24/reports/editor_schema/master.json")
    if schema_digest != manifest_digest:
        raise ValueError("schema snapshot SHA-256 does not match evidence/MANIFEST.json")
    inventory_entity = load_inventory()["entities"]["club"]
    scalar_count = inventory_entity["scalars"]
    return {
        "status": "complete_partial", "entity": "club", "type_id": 3,
        "total_schema_fields": declared,
        "top_level_scalars": scalar_count,
        "named": named,
        "collections": collections,
        "unresolved": unresolved,
        "reader_models": {
            "CLUB_Cccn_evidence_track": {
                "body_file_offset": "0xe5a7a0", "row_offset_candidate": 8,
                "width": 4, "event_file_offset": ev["reader_transfer"]["file_offset"],
                "partition_link": "not established to substrate's event stream; do not merge"
            },
            "CLUB_substrate_track": {
                "body_file_offset": "0xe5a7a0", "transfer_events": len(substrate.get("transfer_events", [])),
                "stable_prefix": [{"widths": x.get("widths"), "row_offset_candidates": x.get("row_offset_candidates"),
                                   "call_file_offset": (x.get("call") or {}).get("file_offset")}
                                  for x in substrate.get("transfer_events", [])[:5]],
                "first_cursor_split": "0xe5a801", "first_unknown_cursor_helper": "0xe5a952",
                "note": "The prefix [0,4,8,12,16] is a separate substrate result; not used to justify Cccn."
            },
            "LEAGUE_BODY_CLUB": {"body_file_offset": "0x43beba0", "transfer_events": 33,
                                  "status": "count-loop not expanded; kept separate"},
        },
        "row_frame": {"status": "closed_with_compact_rows", "walked_rows": frame.get("walked_rows"),
                      "footer_exact": frame.get("footer_exact"), "standard_rows": 84256,
                      "compact_identity_only_rows": 3,
                      "class_partition_candidate": frame.get("class_partition"),
                      "note": "Global row framing/footer is closed; the contiguous class split has no per-row class byte and is not used to merge the two readers."},
        "schema_source": {"path": "evidence/fm24/reports/editor_schema/master.json",
                          "sha256": schema_digest, "manifest_sha256": manifest_digest,
                          "manifest_match": True,
                          "order_inventory": "scratch/t05/schema_inventory.json",
                          "inventory_sha256": inventory_digest,
                          "inventory_counts": {"top_level": declared, "scalars": scalar_count,
                                               "lists": inventory_entity["lists"],
                                               "list_item_fields": inventory_entity["sub_fields"]}},
        "counts": {"medium_or_high": sum(x["confidence"] in ("medium", "high") for x in named),
                   "low": sum(x["confidence"] == "low" for x in named),
                   "unresolved_top_level_fields": len(unresolved),
                   "prior_unclosed_candidates_preserved": len(prior_candidates),
                   "collection_segments_closed": 0},
        "scope_note": "schema_inventory.json confirms 433 top-level fields = 386 scalars + 47 lists; 239 list item fields are separate and excluded from the scalar main sequence.",
    }


def _report_text(fixtures: dict[str, Any], club: dict[str, Any]) -> str:
    lines = [
        "# t05b — schema↔reader 宽度序列对齐器 + club 字段级映射", "",
        "## 结论", "",
        "本次实现可调用的约束 DP，并保留 fixtures 的真实负结果：完整 reader 宽度序列尚未提供；已知物理行锚点中 city 的 Cnti/Clat 顺序与 schema order 相反。没有把预填锚点冒充 DP 复原。club 仅保留一项既有 L3 reader 候选，因缺少安全的 class→reader 分区数据验证而降为 low。", "",
        f"- Fixtures：{fixtures['pass_count']}/{fixtures['fixture_count']} PASS；{fixtures['fail_count']} FAIL；DP synthetic unit {fixtures['algorithm_unit_test']['status']}。", 
        f"- Club：{len(club['named'])} 命名（high {sum(x['confidence']=='high' for x in club['named'])}, medium {sum(x['confidence']=='medium' for x in club['named'])}, low {sum(x['confidence']=='low' for x in club['named'])}）；闭合列表段 {club['counts']['collection_segments_closed']}。",
        f"- Schema：{club['total_schema_fields']} 顶层字段 = {club['top_level_scalars']} 标量 + {len(club['collections'])} 列表；list item 子字段 {club['schema_source']['inventory_counts']['list_item_fields']}。采用 `scratch/t05/schema_inventory.json` 并与权威 Markdown 保序交叉核对。", "",
        "## 对齐器", "",
        "`align_fields(schema_fields, reader_widths, row_width, anchors, samples, prefix_width=0, suffix_width=0)` 使用 memoized DP `(schema_index, transfer_index, offset)`，按 schema inventory 的候选宽度、reader transfer 顺序、锚点和精确宽度求解；optional 字段可取 0，boolean 可打包为 0 宽，list/database_record_list 固定按 0 宽从 scalar 序列排除。`prefix_width/suffix_width` 保留边界/身份帧，不把 `rdui/duni` 身份尾当业务字段。引用域、enum、date、colour 样本作合法性评分。", "",
        "## Fixture 结果", "",
        "五份输入均可机械复算 row closure。现有 hand-decoded reference 只给部分偏移/宽度，不是完整 `mov r8d,N` 序列；故 fixture 不能据此宣称完整 DP 复原。身份尾作为独立 frame 检查；award/city/stadium/injury 的 `rdui@row_width-13`、`duni@+4`、marker 位置一致。city 的业务 anchors `Cnti` 与 `Clat/Clon` 仍直接逆序：",
        "", "| fixture | 字段数 | 行宽 | anchors | frame anchors verified | closure | 业务序列顺序 | 结果 |", "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for f in fixtures["fixtures"]:
        closure = "PASS" if f["row_closure"]["exact"] else "FAIL"
        lines.append(f"| {f['fixture']} | {f['schema_field_count']} | {f['row_width'] if f['row_width'] is not None else 'variable'} | {f['anchor_count']} | {f['frame_anchors_recovered']}/{f['frame_anchor_count']} | {closure} | {'可行' if f['ordered_schema_alignment_feasible_from_anchors'] else '矛盾'} | {f['status']} |")
    lines += ["", "纠错：任务描述把 `city.Cnti` 写作 u8；`scratch/t02/city_reference.json` 的 row0 sample 在 +10 为 `83 00 00 00`，并记录 reader `mov r8d,4`，故本次按 u32/4B 处理。城市业务 anchors 仍为 `Cnti` 在 schema index 6、`Clat/Clon` 在 index 11/12，但物理 offset 分别 +10 与 +1/+5；这是对“schema 与 reader 保序”前提的真实冲突，不通过跳字段消除。其他定长夹具的身份字段均在 row frame 尾部，已从业务 DP 序列排除。language 后缀 ordinal 是相对 17B suffix 的动态锚点。详见 `fixtures_result.json` 与 `CORRECTION.md`。", "",
        "## Club 映射", "",
        "### 仅保留的字段", "",
        "| 字段 | 偏移/宽度 | 置信度 | L3 字节证据 |", "|---|---:|---|---|",
    ]
    for x in club["named"]:
        e = x["evidence"]
        lines.append(f"| `{x['field']}` | +{x['offset']} / {x['width']}B | {x['confidence']} | reader `{e['reader_file_offset']}` `{e['bytes']}`; width `{e['width_file_offset']}` `{e['width_bytes']}`; getter cmp `{e['getter_cmp_file_offset']}` `{e['getter_cmp_bytes']}` |")
    lines += ["", "该项仅保留既有 Cccn getter→sink 局部 cursor 证据；没有将它与 substrate 的 `[0,4,8,12,16]` 前缀或 `LEAGUE_BODY_CLUB` 的循环传输合并。全表 framing/footer 已闭合，但连续 class split 没有每行 class byte；row 69709 的物理 `row+8` 还是与 `row+0` 重复的 identity，不可将该样本拿来验证 Cccn。故不做全体引用域分布结论，置信度降到 low。", "",
        f"### 未闭合", "", f"- 其余 {len(club['unresolved'])} 个 top-level schema 项均不作偏移猜测；既有 `Cdof`、`Cprs`、`Ctsi` 三个 reader/getter 候选原样保留在 JSON，未升格。", f"- {len(club['collections'])} 个 list/database_record_list 字段有 {club['schema_source']['inventory_counts']['list_item_fields']} 个 schema 子字段；count_offset/item_width 均为空，闭合段数 0。", "- CLUB reader 在 `0xe5a801` 出现分支游标分裂；首个动态 helper `0xe5a952` 后宽度/游标未闭合。LEAGUE_BODY_CLUB `0x43beba0` 的 33 个 transfer events/count-loop 保持单独建模。", "- 行框架为 84,259/84,259 且 footer 精确；其中 3 行仅 identity-framed，class split 未由行内标记独立确认。不要把 framing closure 误称字段语义 closure。", "",
        "## 对旧 field_mapper 结论的勘误", "",
        "旧 `field_mapper` 的 39.7% 是其旧 fixtures 的字段偏移吻合率，旧 CFG 游标在分支/循环处失效；不可据此断言所有类型或字段映射不可解。本轮确认需要先拆 system identity frame、optional/位打包字段、变长语言后缀和两套 club reader。Cccn getter/sink 证据、substrate `[0,4,8,12,16]` 和 LEAGUE_BODY_CLUB loop 是三条独立 track，不得互相补游标。city anchors 还与 inventory 声称的保序关系不一致，必须先定清楚该 anchor/reader 对应关系，再把剩余序列送入 DP。未修改任何 t02 输入/旧脚本。", "",
        "## 复跑", "", "```powershell", "py -V:3.12 -I -B scratch/t05/club_align/align.py --selftest --json", "py -V:3.12 -I -B scratch/t05/club_align/align.py --entity club --json", "```", "", "## 来源", "",
        f"- schema 快照 SHA-256 `{club['schema_source']['sha256']}`，与 `evidence/MANIFEST.json` 一致；inventory 文件由 t05 提供。", "- correction/设计：`scratch/t05/club_align/CORRECTION.md`、`scratch/t05/ALIGNMENT_NOTES.md`；上游证据只读引用。", "- 本次没有启动游戏/editor/IDA，也没有写入外部数据；本目录为本任务唯一写入位置。", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true", help="check the five supplied alignment fixtures")
    mode.add_argument("--entity", choices=("club",), help="produce evidence-limited club mapping")
    parser.add_argument("--json", action="store_true", help="print machine-readable result")
    args = parser.parse_args(argv)
    if args.selftest:
        result = run_selftest()
        club = _build_club_result()
        (OUTDIR / "fixtures_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (OUTDIR / "club_fields.json").write_text(json.dumps(club, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (OUTDIR / "REPORT.md").write_text(_report_text(result, club), encoding="utf-8")
    else:
        result = _build_club_result()
        (OUTDIR / "club_fields.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # Keep the five-fixture machine result in sync when running club mode alone.
        fixtures = run_selftest()
        (OUTDIR / "fixtures_result.json").write_text(json.dumps(fixtures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (OUTDIR / "REPORT.md").write_text(_report_text(fixtures, result), encoding="utf-8")
    if args.json:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status={result.get('status')}; output={OUTDIR}")
        if args.selftest:
            print(f"fixtures PASS={result['pass_count']}/{result['fixture_count']} FAIL={result['fail_count']}")
        else:
            counts = result["counts"]
            print(f"club named={len(result['named'])} (high/medium={counts['medium_or_high']}, low={counts['low']})")
    if args.selftest:
        return 0 if result["status"] == "PASS" else 1
    return 0 if result["counts"]["medium_or_high"] >= 30 and result["counts"]["collection_segments_closed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
