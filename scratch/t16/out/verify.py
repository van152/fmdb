#!/usr/bin/env python3
"""Independent t16 artifact verifier; reads project evidence and t16 outputs only."""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch/t16/out"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify() -> dict:
    problems = []
    stage = read(ROOT / "scratch/t14/out/stage2_map.json")
    stage_status = stage.get("status")
    if not (stage_status == "complete" or (isinstance(stage_status, str) and stage_status.startswith("complete_"))):
        problems.append(f"t14 precondition status invalid: {stage_status!r}")

    results = read(OUT / "golden_results.json")
    golden = results.get("golden", {})
    expected_golden = {"city": "fail", "weather": "fail", "comp": "fail"}
    for key, status in expected_golden.items():
        if golden.get(key, {}).get("status") != status:
            problems.append(f"unexpected golden result {key}: {golden.get(key, {}).get('status')!r}")
    if golden.get("city", {}).get("baseline_status") != "pass" or golden.get("comp", {}).get("baseline_status") != "pass":
        problems.append("frozen city/comp baselines should be separately marked pass")
    if golden.get("city", {}).get("engine_fields_named", 0) >= 3 or golden.get("comp", {}).get("engine_reproduced_fields", 0) >= 18:
        problems.append("engine walk unexpectedly claims full golden reproduction")

    # City independently rechecks the t14 row-count anchor and at least three
    # named reference fields against t12's frozen client slot table.
    city = next((x for x in stage.get("tables", []) if x.get("table_type") == 2), {})
    t12 = read(ROOT / "reports/t12_field_names.json")
    refs = {code for slot in t12.get("slots", [])
            if slot.get("type_id") == 2 and slot.get("archive") == "client" and
            slot.get("confidence") == "ref_only" and slot.get("evidence", {}).get("file_off")
            for code in slot.get("codes", []) if code in {"Cnti", "Clgi", "Clri", "Cwea"}}
    if city.get("count") != 56293 or len(refs) < 3:
        problems.append(f"city golden anchor mismatch: count={city.get('count')}, refs={sorted(refs)}")

    # E20 independent binary-byte recalculation: each expected named field has
    # a matching frozen cursor row and an explicit mov r8d,width + stream call.
    e20 = read(ROOT / "reports/t01f_comp_row_offsets.json")
    schema = read(ROOT / "scratch/t05/schema_inventory.json")
    fields = {x.get("code"): x for x in schema.get("entities", {}).get("comp", {}).get("fields", [])}
    with open(r"<OLD_REPO>\input\editor.exe", "rb") as f:
        exe = f.read()
    layout = e20.get("row_codec", {}).get("cursor_layout", [])
    layout_by_step = {x.get("step"): x for x in layout}
    comp_map = e20.get("row_offset_map", {})
    comp_named = {k: v for k, v in comp_map.items() if v.get("counted_as_new_schema_business_field")}
    verified_comp = 0
    for code, item in comp_named.items():
        step = layout_by_step.get(code)
        if not step or (step.get("row_offset"), step.get("width"), step.get("object_offset")) != (
                item.get("row_offset"), item.get("width"), item.get("object_offset")):
            problems.append(f"E20 layout mismatch for {code}")
            continue
        ev = step.get("evidence", {})
        width_ev = ev.get("read_bytes") or ((ev.get("widths") or [{}])[0])
        try:
            off = int(width_ev.get("file_offset"), 16)
            width = int(item["width"])
        except (TypeError, ValueError, KeyError):
            problems.append(f"E20 missing instruction locator for {code}")
            continue
        chunk = exe[off:off + 24]
        imm = b"\x41\xb8" + struct.pack("<I", width)
        stream_call = any(chunk[i] == 0xff and i + 2 < len(chunk) and chunk[i + 2] == 0x28
                          for i in range(max(0, len(chunk) - 2)))
        if imm not in chunk or not stream_call:
            problems.append(f"E20 bytes mismatch for {code} at {width_ev.get('file_offset')}")
            continue
        if code not in fields:
            problems.append(f"E20 field absent from schema: {code}")
        verified_comp += 1
    if len(comp_named) != 18 or verified_comp != 18:
        problems.append(f"expected 18 verified E20 fields, got {verified_comp}")

    # Weather cannot pass without E27's independent 89-offset baseline. Check
    # that this limitation is represented honestly and no synthetic L3 rows
    # have been emitted.
    weather_schema = schema.get("entities", {}).get("weather", {}).get("fields", [])
    target_codes = [f.get("code") for f in weather_schema
                    if f.get("code") == "wnam" or re.fullmatch(r"w[0-3](?:sd|p[0-4]|w[0-4]|t[ev0-7]|dn)", f.get("code", ""))]
    artifact_paths = [ROOT / "scratch/t27/out", ROOT / "reports/t27_weather_offsets.json",
                      ROOT / "evidence/fm24/reports/t27_weather_offsets.json"]
    artifact_present = any(p.exists() for p in artifact_paths)
    if len(target_codes) != 89 or artifact_present:
        problems.append(f"weather baseline expectation changed: target_fields={len(target_codes)}, artifact_present={artifact_present}")
    weather_output = read(OUT / "fields_weather.json")
    if weather_output.get("fields_named") != 0 or any(f.get("grade") == "L3" for f in weather_output.get("fields", [])):
        problems.append("weather contains unsupported named/L3 fields")
    if results.get("batch_gate") == "blocked: all three goldens must pass before batch release":
        if any(x.get("status") != "pass" for x in results.get("golden", {}).values()):
            status_doc = read(OUT / "status.json")
            if status_doc.get("batch_released") is not False:
                problems.append("batch gate must remain closed after a golden failure")

    # Spot-check entity ledgers where debug runs were produced.
    samples = {}
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for tag in ("club", "nati"):
        p = OUT / f"fields_{tag}.json"
        if p.exists():
            d = read(p)
            if d.get("fields_total", 0) < 1 or len(d.get("fields", [])) != d.get("fields_total"):
                problems.append(f"{tag} field table shape mismatch")
            named = [f for f in d.get("fields", []) if f.get("grade") == "L3"]
            claimed = set()
            for field in named:
                evidence = field.get("evidence", {})
                try:
                    off = int(evidence.get("inst_off"), 16)
                    instructions = list(md.disasm(exe[off:off + 16], off))
                    actual = f"{instructions[0].mnemonic} {instructions[0].op_str}" if instructions else None
                except (TypeError, ValueError, IndexError):
                    actual = None
                if not actual or actual != evidence.get("instruction"):
                    problems.append(f"{tag} L3 instruction failed independent decode: {field.get('field')}")
                if tag == "club":
                    slot = (evidence.get("factory_type"), field.get("offset"), field.get("width"),
                            evidence.get("object_off"), evidence.get("inst_off"))
                    if slot in claimed:
                        problems.append(f"club injection conflict not cleared: {slot}")
                    claimed.add(slot)
            samples[tag] = {"fields_total": d.get("fields_total"), "fields_named": d.get("fields_named"),
                            "classes_walked": d.get("classes_walked"), "L3_instructions_rechecked": len(named)}

    for p in (OUT / "debug_fields_city.json", OUT / "debug_fields_comp.json"):
        if p.exists():
            d = read(p)
            for field in d.get("fields", []):
                if field.get("grade") != "L3":
                    continue
                ev = field.get("evidence", {})
                try:
                    off = int(ev.get("inst_off"), 16)
                    insns = list(md.disasm(exe[off:off + 16], off))
                    actual = f"{insns[0].mnemonic} {insns[0].op_str}" if insns else None
                except (TypeError, ValueError, IndexError):
                    actual = None
                if actual != ev.get("instruction"):
                    problems.append(f"debug {d.get('entity')} instruction decode failed: {field.get('field')}")

    return {"status": "pass" if not problems else "fail", "acceptance_ready": False,
            "t14_status": stage_status, "city_reference_fields": sorted(refs),
            "city_rows": city.get("count"), "comp_expected": len(comp_named),
            "comp_binary_rechecked": verified_comp, "weather_targets": len(target_codes),
            "weather_E27_baseline_present": artifact_present,
            "sample_entities": samples, "problems": problems}


def main() -> int:
    ap = argparse.ArgumentParser(description="Independently recalculate t16 output anchors.")
    ap.add_argument("--selftest", action="store_true", help="run checks and print summary")
    args = ap.parse_args()
    try:
        result = verify()
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
