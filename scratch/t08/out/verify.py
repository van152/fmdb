from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
LAYOUTS = ROOT / "scratch/t05/layouts.json"
T07_NAMING = ROOT / "scratch/t07/out/naming_result.json"
NAMING = OUT / "naming_result.json"
CHAINS = OUT / "chains.json"
PAIRING = OUT / "pairing.json"

INJURY = {
    "icla": (0x4C, 1), "iscl": (0x4D, 1), "Imnd": (0x34, 2), "Iexd": (0x36, 2),
    "Iiar": (0x58, 1), "Irec": (0x59, 1), "Iocr": (0x30, 4), "Imip": (0x50, 1),
    "Iagr": (0x51, 1), "Icms": (0x52, 1), "Icon": (0x53, 1), "inSr": (0x54, 1),
    "Icdp": (0x56, 1),
}
CITY = {"Clat": (0x48, 4), "Clon": (0x4C, 4), "Cnti": (0x20, 4),
        "Cwea": (0x28, 4), "Clgi": (0x30, 4), "Clri": (0x38, 4)}
ALLOWED_CONFIDENCE = {"chain_unique", "chain_ambiguous", "readpair", "ref_only", "unresolved"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def named_count(entity):
    return sum(field.get("field") is not None
               for archive in entity.get("archives", {}).values()
               for field in archive.get("fields", []))


def map_entities(document, key):
    return {item["type_id"]: item for item in document.get(key, [])}


def calibration_evidence(named, code):
    hits = []
    for entity in named.get("results", []):
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                for access in field.get("accesses", []):
                    if access.get("code") == code:
                        hits.append((access.get("object_off"), access.get("size")))
                if code in field.get("codes", []):
                    if isinstance(field.get("object_off"), int):
                        hits.append((field.get("object_off"), field.get("width")))
    return hits


def selftest():
    assert len(INJURY) == 13 and len(CITY) == 6
    assert sum((0x4C, 1) == value for value in INJURY.values()) == 1
    assert "chain_unique" in ALLOWED_CONFIDENCE and "unresolved" in ALLOWED_CONFIDENCE
    print("verify.py selftest: OK")
    return 0


def check():
    failures = []
    layouts_doc = load(LAYOUTS)
    baseline = load(T07_NAMING)
    naming = load(NAMING)
    chain_doc = load(CHAINS)
    pairing = load(PAIRING)
    for label, doc in (("chains", chain_doc), ("pairing", pairing), ("naming", naming)):
        if not str(doc.get("status", "")).startswith("complete_"):
            failures.append(f"{label}.status not complete: {doc.get('status')!r}")

    base_by_type = map_entities(baseline, "results")
    out_by_type = map_entities(naming, "results")
    layouts_by_type = map_entities(layouts_doc, "layouts")
    if set(out_by_type) != set(layouts_by_type):
        failures.append(f"entity coverage mismatch: output={len(out_by_type)}, layouts={len(layouts_by_type)}")
    preserved = 0
    base_named = {}
    for tid, entity in base_by_type.items():
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                if field.get("field") is not None:
                    base_named[(tid, archive, field["idx"])] = field.get("field")
    for key, old_name in base_named.items():
        tid, archive, idx = key
        new_entity = out_by_type.get(tid)
        new_spec = new_entity.get("archives", {}).get(archive, {}) if new_entity else {}
        new_field = next((f for f in new_spec.get("fields", []) if f.get("idx") == idx), None)
        if not new_field:
            failures.append(f"t07 named slot missing: type {tid}/{archive}/idx {idx}")
        elif new_field.get("field") != old_name:
            failures.append(f"t07 name changed: type {tid}/{archive}/idx {idx}: {old_name!r} -> {new_field.get('field')!r}")
        else:
            preserved += 1
    if preserved != 45 or len(base_named) != 45:
        failures.append(f"t07 preservation count must be 45/45; source={len(base_named)}, preserved={preserved}")

    # Original row_off/width and closure are immutable across all archives.
    for tid, layout in layouts_by_type.items():
        out_entity = out_by_type.get(tid)
        if not out_entity:
            continue
        for archive, spec in layout.get("archives", {}).items():
            out_spec = out_entity.get("archives", {}).get(archive)
            if not out_spec:
                failures.append(f"type {tid} missing archive {archive}")
                continue
            source_fields = spec.get("fields", [])
            out_fields = out_spec.get("fields", [])
            if len(source_fields) != len(out_fields):
                failures.append(f"type {tid}/{archive} field count changed")
                continue
            for original, current in zip(source_fields, out_fields):
                if (original.get("idx"), original.get("row_off"), original.get("width")) != (
                        current.get("idx"), current.get("row_off"), current.get("width")):
                    failures.append(f"type {tid}/{archive}/idx {original.get('idx')} row_off/width changed")
                if current.get("confidence") not in ALLOWED_CONFIDENCE:
                    failures.append(f"type {tid}/{archive}/idx {current.get('idx')} invalid confidence {current.get('confidence')!r}")
            actual = sum(f.get("width", 0) for f in out_fields)
            if actual != spec.get("business_width") or actual != out_spec.get("business_width"):
                failures.append(f"type {tid}/{archive} sum(width)={actual}, business_width={spec.get('business_width')}")

    # Fixed t07 calibration: access-level checks preserve 13 injury and 6 city facts.
    injury_ok = 0
    for code, expected in INJURY.items():
        got = calibration_evidence(naming, code)
        if expected in got:
            injury_ok += 1
        else:
            failures.append(f"injury calibration missing {code} @+{expected[0]:#x}/{expected[1]}B; got={got}")
    city_ok = 0
    for code, expected in CITY.items():
        got = calibration_evidence(naming, code)
        if expected in got:
            city_ok += 1
        else:
            failures.append(f"city calibration missing {code} @+{expected[0]:#x}/{expected[1]}B; got={got}")

    # Reverse check: a chain_unique label must be the sole raw direct code for that pair
    # inside its selected primary chain (not merely the sole post-filter schema candidate).
    chains_by_id = {c["chain_id"]: c for c in chain_doc.get("chains", [])}
    primary_by_type = {x["type_id"]: x.get("primary_chain") for x in pairing.get("readers", [])}
    for chain in chain_doc.get("chains", []):
        if chain.get("n_codes", 0) < 5:
            failures.append(f"retained chain {chain.get('chain_id')} has n_codes<5")
    unique_checked = 0
    for entity in naming.get("results", []):
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                if field.get("confidence") != "chain_unique":
                    continue
                chain_id = field.get("chain_id")
                chain = chains_by_id.get(chain_id)
                code_list = set(field.get("codes", []))
                off, width = field.get("object_off"), field.get("width")
                raw_codes = {x.get("code") for x in (chain or {}).get("candidate_pairs", [])
                             if x.get("object_off") == off and x.get("width") == width}
                if chain_id != primary_by_type.get(entity["type_id"]):
                    failures.append(f"chain_unique slot is not on reader primary chain: type {entity['type_id']}, {chain_id}")
                if not chain or len(raw_codes) != 1 or raw_codes != code_list:
                    failures.append(f"chain_unique reverse-check failed type {entity['type_id']}/{archive}/idx {field.get('idx')}: "
                                    f"chain={chain_id}, pair=({off},{width}), raw_codes={sorted(raw_codes)}, labels={sorted(code_list)}")
                else:
                    unique_checked += 1

    type22 = out_by_type.get(22)
    type22_named = named_count(type22) if type22 else 0
    total_named = sum(named_count(x) for x in naming.get("results", []))
    if type22_named < 14:
        failures.append(f"type22 named slots {type22_named}/19 < 14")
    if total_named < 62:
        failures.append(f"total named slots {total_named}/240 < 62")
    if len(pairing.get("readers", [])) != 26:
        failures.append(f"pairing reader count={len(pairing.get('readers', []))}, expected 26")
    for reader in pairing.get("readers", []):
        primary = reader.get("primary_chain")
        if primary:
            top = next((x for x in reader.get("top3", []) if x.get("chain_id") == primary), None)
            if not top or top.get("score", 0) < 3:
                failures.append(f"reader {reader.get('type_id')} primary chain lacks score>=3")

    print(f"t07 preserved {preserved}/45; injury {injury_ok}/13; city {city_ok}/6; "
          f"type22 {type22_named}/19; total {total_named}/240; chain_unique reverse-check {unique_checked}")
    if failures:
        for item in failures:
            print("FAIL:", item)
        return 1
    print("PASS: zero regression, calibration, layout closure, pairing, and chain uniqueness verified")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Verify t08 outputs against t07 regression baseline and t08 acceptance gates.")
    ap.add_argument("--selftest", action="store_true", help="run pure verification helper tests")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        return check()
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
