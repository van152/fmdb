#!/usr/bin/env python3
"""t06 可复跑自检：布局闭合引用、校准集、high 命名的数据类型判据。"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def run_selftest() -> list[str]:
    errors: list[str] = []
    def check(ok: bool, message: str):
        if not ok:
            errors.append(message)
    layouts = load(ROOT / "scratch/t05/layouts.json")["layouts"]
    schema = load(ROOT / "scratch/t05/schema_inventory.json")["entities"]
    coverage = load(ROOT / "scratch/t05/COVERAGE.json")["tables"]
    coverage_counts = {(x.get("archive"), x.get("table_id")): x.get("count") for x in coverage}
    city_ref = load(ROOT / "scratch/t02/city_reference.json")
    regi_ref = load(ROOT / "scratch/t02/regi_reference.json")
    data = load(OUT / "assignments.json")
    check(data.get("status", "").startswith("complete_"), "assignments status is not complete")
    amap = {(a["type_id"], a["archive"]): a for a in data.get("assignments", [])}
    lmap = {(x["type_id"], ar): (x, x["archives"][ar]) for x in layouts for ar in x["archives"]}
    check(set(amap) == set(lmap), f"assignment archive/entity keys differ: assignment={len(amap)} layout={len(lmap)}")
    check(data.get("summary", {}).get("slots") == sum(len(x["archives"][a]["fields"]) for x in layouts for a in x["archives"]), "summary slot count mismatch")

    for key, (entity_layout, arch_layout) in lmap.items():
        a = amap.get(key)
        if a is None:
            continue
        check(a.get("business_width") == arch_layout["business_width"], f"{key}: business_width changed")
        slots = a.get("slots", [])
        source = arch_layout["fields"]
        check(len(slots) == len(source), f"{key}: slot count differs")
        for i, (got, src) in enumerate(zip(slots, source)):
            check((got.get("idx"), got.get("row_off"), got.get("width")) ==
                  (src.get("idx"), src.get("row_off"), src.get("width")),
                  f"{key} slot {i}: idx/row_off/width differs from layouts.json")
            if got.get("code") == "unresolved":
                check(bool(got.get("unresolved_reason")), f"{key} slot {i}: unresolved reason missing")

    # Schema type lookup: entity type_id -> schema_inventory key.
    schema_key = {2: "city", 6: "injury", 19: "region", 21: "stadium"}
    def field_type(type_id: int, code: str):
        entity = schema.get(schema_key.get(type_id, ""), {})
        return next((f.get("type") for f in entity.get("fields", []) if f.get("code") == code), None)

    def profile(name: str):
        return load(OUT / name)

    def validate_high(a, s):
        val = s.get("validation")
        if not val:
            check(False, f"{a['type_id']}/{a['archive']} slot {s['idx']}: high assignment lacks validation")
            return
        kind = val["kind"]
        if kind == "constant_byte":
            p = profile(val["profile"]); c = p["columns"][val["offset"]]
            check(p["rows"] == 28 and c.get("constant") == val["value"] and c["distinct_u8"] == 1,
                  "regi server boundary marker constant check failed")
            return
        p = profile(val["profile"])
        check(p.get("rows", 0) > 0, f"empty profile {val['profile']}")
        if kind == "f32_pair":
            for off, bounds in zip(val["offsets"], val["ranges"]):
                f = p["columns"][off].get("f32")
                check(f is not None and f.get("finite_ratio") == 1.0,
                      f"{val['profile']} @{off}: real is not all-finite f32")
                if f:
                    check(bounds[0] <= f["min"] <= f["max"] <= bounds[1],
                          f"{val['profile']} @{off}: f32 range outside {bounds}")
            return
        if kind == "reference":
            u = p["columns"][val["offset"]].get("u32", {})
            n = val["target_count"]
            target_tid = {"Cnti": 9, "Cwea": 27, "Clgi": 8, "Clri": 47}.get(s.get("code"))
            if target_tid is not None:
                check(coverage_counts.get(("client", target_tid)) == n,
                      f"reference target table {target_tid} count != {n}")
            check("ref_lt_N" in u and u.get("ref_lt_N") is not None, f"{val['profile']}: ref_lt_N absent")
            check(u.get("distinct", 0) > 1, f"{val['profile']} @{val['offset']}: reference has no variation")
            check(u.get("max", n) == 0xFFFFFFFF or u.get("max", 0) < 0xFFFFFFFF,
                  f"{val['profile']} @{val['offset']}: unexpected u32 max")
            if val.get("allow_ff"):
                check(abs(u.get("ref_lt_N", -9) - (1.0 - u.get("ff_ratio", 0.0))) <= 0.0002,
                      f"{val['profile']} @{val['offset']}: non-null reference values exceed target count")
            else:
                check(u.get("ff_ratio") == 0.0 and u.get("ref_lt_N") == 1.0,
                      f"{val['profile']} @{val['offset']}: values fail target-count/no-sentinel test")
            return
        if kind == "range":
            c = p["columns"][val["offset"]]
            keyname = "u8" if val["interpretation"] == "u8" else "u16"
            stats = c if keyname == "u8" else c.get("u16", {})
            minimum = stats.get("min_u8" if keyname == "u8" else "min")
            maximum = stats.get("max_u8" if keyname == "u8" else "max")
            distinct = stats.get("distinct_u8" if keyname == "u8" else "distinct")
            check((minimum, maximum, distinct) == (val["min"], val["max"], val["distinct"]),
                  f"{val['profile']} @{val['offset']}: numeric range/distinct mismatch")
            if "ff_ratio" in val:
                check(abs(c.get("ff_ratio_u8", -1) - val["ff_ratio"]) <= 0.0002,
                      f"{val['profile']} @{val['offset']}: 0xFF sentinel ratio mismatch")
            return
        check(False, f"unknown validation kind {kind}")

    # Every high schema assignment must have a schema type, and every high has data validation.
    for a in data.get("assignments", []):
        for s in a["slots"]:
            if s.get("confidence") != "high":
                continue
            codes = s.get("component_codes", [s.get("code")])
            for code in codes:
                if code == "boundary_marker":
                    check(s.get("schema_type", "").startswith("structural"), "boundary marker incorrectly claims schema type")
                    continue
                declared = field_type(a["type_id"], code)
                if declared is None and "exe-only" in s.get("schema_type", ""):
                    check(code in ("Imio", "Icdo"), f"unexpected exe-only high code {code}")
                else:
                    check(declared is not None, f"high code {code} absent from schema_inventory")
                    expected = s.get("schema_types", {}).get(code, s.get("schema_type"))
                    check(declared == expected, f"high code {code}: schema type {declared} != assignment {expected}")
            validate_high(a, s)

    # city exact anchors and merged float reader slot.
    city = amap.get((2, "client"), {})
    by_off = {s["row_off"]: s for s in city.get("slots", [])}
    check(by_off.get(10, {}).get("code") == "Cnti" and by_off.get(10, {}).get("width") == 4,
          "city Cnti@10 calibration not reproduced")
    check(by_off.get(1, {}).get("component_codes") == ["Clat", "Clon"] and by_off.get(1, {}).get("width") == 8,
          "city Clat/Clon merged-slot calibration not reproduced")
    refmap = city_ref.get("row_offset_map", [])
    check(any(x.get("row_off") == 10 and x.get("width") == 4 for x in refmap), "city reference lacks Cnti@10 anchor")
    check(any(x.get("row_off") == 1 and x.get("width") == 4 for x in refmap) and
          any(x.get("row_off") == 5 and x.get("width") == 4 for x in refmap), "city float reference offsets differ")
    expected_city_slots = [(0,1),(1,8),(9,1),(10,4),(14,4),(18,3),(21,4),(25,4),(29,1)]
    check([(s["row_off"],s["width"]) for s in city.get("slots",[])] == expected_city_slots,
          "city slot positions differ from calibrated layout")

    # regi: all eight manual 4B offsets reproduce; ninth server byte is kept structural.
    regi_client = amap.get((19, "client"), {}).get("slots", [])
    regi_server = amap.get((19, "server"), {}).get("slots", [])
    expected_regi = [(0,4),(4,4),(8,4),(12,4),(16,4),(20,4),(24,4),(28,4)]
    check([(s["row_off"],s["width"]) for s in regi_client] == expected_regi, "regi client eight-slot calibration differs")
    check([(s["row_off"],s["width"]) for s in regi_server[:8]] == expected_regi, "regi server eight-slot calibration differs")
    check(len(regi_server) == 9 and (regi_server[8].get("row_off"), regi_server[8].get("width"), regi_server[8].get("code")) ==
          (32, 1, "boundary_marker"), "regi server +32 marker calibration differs")
    rmap = regi_ref.get("row_offset_map", [])
    check([(x["row_off"],x["width"]) for x in rmap if x["width"] == 4] == expected_regi,
          "regi reference eight 4B anchors differ")

    # Injury: exact nine named calibrations, with user-provided spelling preserved.
    expected_injury = [(0,1,"icla"),(3,2,"Imnd"),(5,2,"Imio"),(8,1,"Irec"),
                       (17,1,"Imip"),(21,1,"Icms"),(23,1,"inSr"),(25,1,"Icdp"),(26,1,"Icdo")]
    injury = amap.get((6, "server"), {}).get("slots", [])
    got = [(s["row_off"],s["width"],s["code"]) for s in injury if s.get("code") != "unresolved"]
    check(got == expected_injury, f"injury calibration differs: {got!r}")
    check(load(OUT / "profile_server6_inju.json").get("rows") == 115, "injury semantic profile row count differs")

    # Every unresolved is explicitly explained in REPORT; report states zero calibration deltas.
    report = (OUT / "REPORT.md").read_text(encoding="utf-8")
    check("校准差异：0" in report and "unresolved" in report, "REPORT lacks calibration delta or unresolved summary")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser(description="t06 assignments 自检")
    ap.add_argument("--selftest", action="store_true", help="校验布局、校准集与所有 high 命名的类型证据")
    args = ap.parse_args()
    if not args.selftest:
        ap.error("请指定 --selftest")
    try:
        errors = run_selftest()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2
    if errors:
        for e in errors:
            print("FAIL:", e)
        print(f"{len(errors)} checks failed")
        return 1
    print("PASS: layout slots unchanged; city/regi/injury calibration exact; all high type/data checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
