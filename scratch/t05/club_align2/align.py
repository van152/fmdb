#!/usr/bin/env python3
"""Schema-ordered byte-width search for the t05 fixed-row fixtures.

Anchors are loaded from fixtures_truth.json and contribute search score only;
validation is a separate pass.  Non-anchor fields retain schema order.  Verified
anchor placements are allowed to override that order (notably city's physical
Clat/Clon slots precede Cnti); this exception is reported, never hidden.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import runpy
import struct
import sys
from itertools import product

ROOT = pathlib.Path(__file__).resolve().parents[3]
INPUT = ROOT / "scratch" / "t05"
OUT = pathlib.Path(__file__).resolve().parent
IDENTITY_CODES = {"duni", "rdui"}


def load_inputs():
    schema = json.loads((INPUT / "schema_inventory.json").read_text(encoding="utf-8"))
    truth = json.loads((INPUT / "fixtures_truth.json").read_text(encoding="utf-8"))
    widths = schema["type_width_candidates"]
    fixtures = {x["name"]: x for x in truth["fixtures"]}
    profiles = {
        name: json.loads((INPUT / f"profile_{name}.json").read_text(encoding="utf-8"))
        for name in ("award", "city", "stadium", "injury")
    }
    return schema, widths, fixtures, profiles


def scalar_fields(schema, name):
    fields = schema["entities"][name]["fields"]
    return [f for f in fields if not f.get("list") and f.get("parent") is None
            and f["type"] not in ("list", "database_record_list", "button", "label")]


def width_options(field, width_types):
    vals = list(width_types.get(field["type"], {}).get("candidates", [0]))
    # Zero represents unresolved/shared storage in this heuristic, not evidence
    # that a non-optional schema property is absent.
    if 0 not in vals:
        vals.append(0)
    return sorted(set(int(x) for x in vals))


def type_stat_score(field, width, offset, columns):
    if width == 0 or offset is None or offset >= len(columns):
        return -0.08 if width == 0 else -4.0
    c = columns[offset]
    typ = field["type"]
    if typ == "boolean":
        return 3.0 if width == 1 and c.get("distinct_u8", 256) <= 2 and c.get("max_u8", 255) <= 1 else -5.0
    if typ in ("enum", "day_of_week", "multiple_enum"):
        if width == 1:
            lo, hi, distinct = c.get("min_u8", 0), c.get("max_u8", 255), c.get("distinct_u8", 256)
            return 2.0 if hi <= 31 and distinct >= 2 and (hi - lo + 1 <= distinct + 2) else -1.0
        return 0.2 if width in (2, 4) else -1.0
    if typ == "database_record_unique_id" and width == 4:
        ref = c.get("u32", {}).get("ref_lt_N")
        return 3.0 if ref is not None and ref >= 0.8 else (0.0 if ref is None else -2.0)
    if typ == "real" and width == 4:
        f = c.get("f32", {})
        if f.get("finite_ratio") == 1.0:
            lo, hi = f.get("min", math.inf), f.get("max", -math.inf)
            return 2.0 if max(abs(lo), abs(hi)) <= 1_000_000 and (hi != 0 or lo != 0) else -2.0
        return -4.0
    if typ == "date" and width == 2:
        u = c.get("u16", {})
        return 0.5 if u.get("max", 65536) < 65536 else -0.5
    if typ in ("integer", "cash", "short_distance", "player_attribute"):
        if width == 1 and c.get("max_u8", 255) <= 255:
            return 1.0
        if width == 2 and c.get("u16", {}).get("max", 65536) <= 65535:
            return 0.7
        return 0.2
    if typ in ("string", "picture"):
        return 0.15 if width == 4 else -0.25
    if typ == "colour":
        return 0.1 if width in (3, 4) else -0.5
    return 0.0


def anchor_field_code(anchor_name, fields):
    codes = {f["code"] for f in fields}
    if anchor_name in codes:
        return anchor_name
    # duni is represented by a pair of adjacent 32-bit anchor assertions.
    for suffix in ("_lo", "_hi"):
        if anchor_name.endswith(suffix) and anchor_name[:-len(suffix)] in codes:
            return anchor_name[:-len(suffix)]
    return None


def anchor_suboffset(anchor_name):
    return 4 if anchor_name.endswith("_hi") else 0


def find_anchor_layout(fields, anchors, business_len, columns):
    """Search placements for anchored business fields; truth targets score +10.

    Candidate placements are explored rather than read as fixed assignments.
    Maximum hit count is the primary objective, then the documented score.
    """
    by_code = {f["code"]: f for f in fields}
    grouped = {}
    for name, spec in anchors.items():
        code = anchor_field_code(name, fields)
        if code is None or code in IDENTITY_CODES:
            continue
        grouped.setdefault(code, []).append((name, spec))
    # One physical field may be described by multiple sub-anchors. Resolve its
    # total allocation from its schema candidate, except where truth explicitly
    # constrains a one-byte field such as city Cnti.
    groups = []
    for code, items in grouped.items():
        f = by_code[code]
        target_start = min(int(a["offset"]) - anchor_suboffset(n) for n, a in items)
        target_width = max(anchor_suboffset(n) + int(a["width"]) for n, a in items)
        groups.append((f, items, target_start, target_width))

    # Enumerate all starts for anchor fields. Truth only adds the +10 hit score;
    # type/statistical evidence scores every candidate location.
    choices = []
    for f, items, target, aw in groups:
        schema_ws = width_options(f, {})
        # Anchored wire width is independently documented in truth, and may be
        # narrower than a schema reader's scalar candidate (e.g. Cnti u8/u32).
        candidate_ws = sorted(set(schema_ws + [aw]))
        field_choices = []
        for w in candidate_ws:
            if w <= 0 or w > business_len:
                continue
            for pos in range(0, business_len - w + 1):
                hit = all(pos + anchor_suboffset(n) == int(a["offset"])
                          and int(a["width"]) == (4 if n.endswith(("_lo", "_hi")) else w)
                          for n, a in items)
                # The pair anchors describe halves of an 8-byte unique ID.
                if f["code"] == "duni":
                    hit = all(pos + anchor_suboffset(n) == int(a["offset"])
                              for n, a in items) and w == 8
                stat = type_stat_score(f, min(w, 4), pos, columns)
                field_choices.append((pos, w, (10.0 if hit else 0.0) + stat, int(hit)))
        choices.append(field_choices)

    if not groups:
        return [], 0, 0.0
    best = None
    for layout in product(*choices):
        occupied = set()
        good = True
        for pos, w, _, _ in layout:
            span = set(range(pos, pos + w))
            if occupied & span:
                good = False
                break
            occupied |= span
        if not good:
            continue
        hits = sum(x[3] for x in layout)
        score = sum(x[2] for x in layout)
        key = (hits, score)
        if best is None or key > best[0]:
            best = (key, layout)
    if best is None:
        return [], 0, 0.0
    layout = best[1]
    result = []
    for (f, items, target, aw), (pos, w, score, hit) in zip(groups, layout):
        result.append({"field": f["code"], "offset": pos, "width": w,
                       "confidence": "high" if hit else "unresolved",
                       "anchor_names": [n for n, _ in items], "anchor_hit": bool(hit),
                       "score": round(score, 3)})
    return result, best[0][0], best[0][1]


def dp_remaining(fields, available, columns, width_types, capacity, topn=3):
    """DP over schema field order and consumed byte count; retain top paths."""
    # At a transition of width W, physical bytes must be contiguous. This lets
    # DP respect fixed anchor windows without allowing a field to straddle one.
    states = {0: [(0.0, [])]}
    for f in fields:
        opts = width_options(f, width_types)
        nxt = {}
        for used, paths in states.items():
            for score, path in paths:
                for w in opts:
                    new_used = used + w
                    if new_used > capacity:
                        continue
                    pos = None
                    if w:
                        if new_used > len(available):
                            continue
                        start = used
                        physical = available[start:new_used]
                        if len(physical) != w or physical[-1] - physical[0] + 1 != w:
                            continue
                        pos = physical[0]
                    extra = type_stat_score(f, w, pos, columns)
                    entry = (score + extra, path + [{"field": f["code"], "offset": pos,
                                                     "width": w, "confidence": "low" if w else "unresolved",
                                                     "anchor_hit": False, "score": round(extra, 3)}])
                    bucket = nxt.setdefault(new_used, [])
                    bucket.append(entry)
        states = {}
        for used, paths in nxt.items():
            # Stable deterministic ordering, avoid retaining equivalent layouts.
            paths.sort(key=lambda x: (x[0], tuple((a["offset"] if a["offset"] is not None else -1,
                                                   a["width"], a["field"]) for a in x[1])), reverse=True)
            seen, kept = set(), []
            for p in paths:
                signature = tuple((a["offset"], a["width"]) for a in p[1])
                if signature in seen:
                    continue
                seen.add(signature)
                kept.append(p)
                if len(kept) == topn:
                    break
            states[used] = kept
    return states.get(capacity, [])


def identity_assignment(fields, anchors):
    out = []
    by_code = {f["code"]: f for f in fields}
    if "rdui" in by_code and "rdui" in anchors:
        a = anchors["rdui"]
        out.append({"field": "rdui", "offset": int(a["offset"]), "width": int(a["width"]),
                    "region": "identity_tail", "confidence": "high", "anchor_hit": True,
                    "score": 10.0})
    duni = by_code.get("duni")
    if duni and "duni_lo" in anchors:
        a = anchors["duni_lo"]
        hi = anchors.get("duni_hi", {})
        out.append({"field": "duni", "offset": int(a["offset"]),
                    "width": int(a["width"]) + int(hi.get("width", 0)),
                    "region": "identity_tail", "confidence": "high", "anchor_hit": True,
                    "score": 20.0})
    return out


def validate_truth_samples(fixture, assignment):
    by_name = {a["field"]: a for a in assignment}
    anchors = fixture["anchors"]
    checks = []
    for sample in fixture.get("samples", []):
        row = bytes.fromhex(sample["hex"])
        ok = len(row) == fixture["stride"]
        for name, a in anchors.items():
            off, width = int(a["offset"]), int(a["width"])
            if off + width > len(row):
                ok = False
                continue
            # Only compare values explicitly included in the truth sample.
            value_key = name
            if name == "duni_lo":
                value_key = "duni_lo"
            elif name == "duni_hi":
                value_key = "duni_hi"
            if value_key in sample and width <= 4:
                observed = int.from_bytes(row[off:off + width], "little")
                if observed != int(sample[value_key]):
                    ok = False
        checks.append({"row": sample["row"], "ok": ok})
    return checks


def validate_fixture(fixture, profile, assignment, business_width, verify_raw=False):
    stride = int(fixture["stride"])
    business = stride - 13
    closure = int(fixture["header"]) + int(fixture["count"]) * stride + 8 == int(fixture["payload_len"])
    profile_ok = int(profile["rows"]) == int(fixture["count"]) and int(profile["width"]) == stride
    by_code = {a["field"]: a for a in assignment}
    anchors_ok = []
    for name, a in fixture["anchors"].items():
        code = anchor_field_code(name, [{"code": x["field"]} for x in assignment])
        found = by_code.get(code) if code else None
        sub = anchor_suboffset(name)
        expected_width = int(a["width"])
        hit = bool(found and found["offset"] is not None
                    and int(found["offset"]) + sub == int(a["offset"]))
        if name not in ("duni_lo", "duni_hi"):
            hit = hit and int(found["width"]) >= expected_width
        else:
            hit = hit and int(found["width"]) >= sub + expected_width
        anchors_ok.append({"name": name, "expected_offset": int(a["offset"]),
                           "expected_width": expected_width, "hit": bool(hit)})
    sample_checks = validate_truth_samples(fixture, assignment)
    raw_result = {"attempted": False, "verified_rows": 0, "ok": None}
    if verify_raw:
        raw_result["attempted"] = True
        try:
            dump = runpy.run_path(str(ROOT / "scripts" / "fm24_dump.py"))
            codec = dump["_reader"]()
            raw = dump["load_payload"](codec, fixture["archive"], int(fixture["table_id"]))
            spec = {"header": int(fixture["header"]), "stride": stride,
                    "footer": 8, "count": int(fixture["count"])}
            rows_checked = 0
            all_ok = len(raw) == int(fixture["payload_len"])
            rdui_off = fixture["anchors"].get("rdui", {}).get("offset")
            dlo = fixture["anchors"].get("duni_lo", {}).get("offset")
            dhi = fixture["anchors"].get("duni_hi", {}).get("offset")
            marker = fixture.get("extra", {}).get("marker_offset")
            named = {}
            for label, specrow in fixture.get("extra", {}).get("named_rows", {}).items():
                row_index, expected = specrow
                named[int(row_index)] = (label, expected)
            cnti_off = fixture["anchors"].get("Cnti", {}).get("offset")
            for i, _, row in dump["walk_fixed"](raw, spec):
                rows_checked += 1
                all_ok &= len(row) == stride and len(row[:business]) + len(row[business:]) == stride
                if rdui_off is not None:
                    all_ok &= struct.unpack_from("<I", row, int(rdui_off))[0] == i
                if dlo is not None and dhi is not None:
                    all_ok &= struct.unpack_from("<I", row, int(dlo))[0] == struct.unpack_from("<I", row, int(dhi))[0]
                if cnti_off is not None:
                    # Verify the documented u8/u32 equivalence across every city row.
                    all_ok &= row[int(cnti_off) + 1:int(cnti_off) + 4] == b"\x00\x00\x00"
                if i in named:
                    expected = named[i][1]
                    for key, off in (("rdui", rdui_off), ("Cnti", cnti_off), ("duni_lo", dlo)):
                        if key in expected and off is not None:
                            size = 1 if key == "Cnti" else 4
                            all_ok &= int.from_bytes(row[int(off):int(off) + size], "little") == int(expected[key])
                if marker is not None:
                    all_ok &= row[int(marker)] == int(fixture.get("extra", {}).get("marker_expect", 0))
            raw_result = {"attempted": True, "verified_rows": rows_checked,
                          "ok": bool(all_ok and rows_checked == int(fixture["count"]))}
        except Exception as exc:  # external read-only source may not be mounted
            raw_result = {"attempted": True, "verified_rows": 0, "ok": False,
                          "error": f"{type(exc).__name__}: {exc}"}
    named_rows_ok = all(x.get("match") is True for x in fixture.get("named_rows_check", []))
    return {
        "anchors": anchors_ok,
        "anchors_hit": sum(x["hit"] for x in anchors_ok),
        "anchors_total": len(anchors_ok),
        "closure_ok": bool(closure and profile_ok and business_width == business),
        "sample_checks": sample_checks,
        "named_rows_ok": named_rows_ok,
        "raw_rows": raw_result,
    }


def solve_fixture(name, schema, width_types, fixture, profile, verify_raw=False):
    fields = scalar_fields(schema, name)
    business_len = int(fixture["stride"]) - 13
    columns = profile["columns"]
    identity = identity_assignment(fields, fixture["anchors"])
    id_codes = IDENTITY_CODES
    business_fields = [f for f in fields if f["code"] not in id_codes]
    anchor_layout, anchor_hits, anchor_score = find_anchor_layout(
        business_fields, fixture["anchors"], business_len, columns)
    # Identity-tail anchors participate in the same +10 objective even though
    # their placement is structural and excluded from business-byte DP.
    anchor_score += 10.0 * sum(name in fixture["anchors"]
                               for name in ("rdui", "duni_lo", "duni_hi"))
    anchored_codes = {x["field"] for x in anchor_layout}
    used = set()
    for a in anchor_layout:
        used.update(range(int(a["offset"]), int(a["offset"]) + int(a["width"])))
    available = [i for i in range(business_len) if i not in used]
    rest = [f for f in business_fields if f["code"] not in anchored_codes]
    paths = dp_remaining(rest, available, columns, width_types, len(available), topn=3)
    top_solutions = []
    for score, path in paths:
        assign = [dict(x) for x in anchor_layout + path + identity]
        # Lists have no inline width in this model; include them transparently.
        for f in schema["entities"][name]["fields"]:
            if f.get("parent") is None and f.get("type") in ("list", "database_record_list"):
                assign.append({"field": f["code"], "offset": None, "width": 0,
                               "region": "list_not_inline", "confidence": "unresolved",
                               "anchor_hit": False, "score": 0.0})
        # Mark the searched body and identity partitions explicitly.
        for a in assign:
            if "region" not in a:
                a["region"] = "business"
        total_business = sum(int(a["width"]) for a in assign if a["region"] == "business")
        # Include +1 for the exact end-of-business/identity-tail closure.
        total_score = score + anchor_score + (1.0 if total_business == business_len else 0.0)
        order = {f["code"]: i for i, f in enumerate(fields)}
        assign.sort(key=lambda a: (order.get(a["field"], 10_000), a.get("offset") or -1))
        validation = validate_fixture(fixture, profile, assign, total_business, verify_raw)
        top_solutions.append({"total_score": round(total_score, 3),
                              "total_width": total_business,
                              "assignment": assign,
                              "anchor_validation": validation["anchors"],
                              "anchors_hit": validation["anchors_hit"],
                              "anchors_total": validation["anchors_total"],
                              "closure_ok": validation["closure_ok"],
                              "sample_checks": validation["sample_checks"],
                              "named_rows_ok": validation["named_rows_ok"],
                              "raw_rows": validation["raw_rows"]})
    if not top_solutions:
        return {"name": name, "anchors_hit": 0, "anchors_total": len(fixture["anchors"]),
                "total_width": 0, "closure_ok": False, "assignment": [],
                "top_solutions": [], "status": "FAIL", "error": "no exact-width DP solution"}
    best = top_solutions[0]
    # DP paths are useful hypotheses, but profile-only matches are not enough to
    # publish a field name as resolved. Keep them in top_solutions; the primary
    # assignment names only truth-anchored fields and represents all other bytes
    # as anonymous unresolved wire ranges.
    candidate_assignment = best["assignment"]
    for candidate in top_solutions:
        candidate["candidate_only"] = True
        candidate["interpretation"] = "statistical DP hypothesis; non-anchor names are unverified"
    schema_rank = {f["code"]: i for i, f in enumerate(business_fields)}
    physical_codes = [x["field"] for x in sorted(
        [x for x in candidate_assignment if x["region"] == "business" and x["width"]],
        key=lambda x: x["offset"]) if x["field"] in schema_rank]
    order_violations = sum(schema_rank[a] > schema_rank[b]
                           for a, b in zip(physical_codes, physical_codes[1:]))
    anchor_by_code = {x["field"]: x for x in anchor_layout}
    primary = []
    for f in fields:
        code = f["code"]
        if code in IDENTITY_CODES:
            continue
        if code in anchor_by_code:
            entry = dict(anchor_by_code[code])
            entry["region"] = "business"
            primary.append(entry)
        else:
            primary.append({"field": code, "offset": None, "width": 0,
                            "region": "business", "confidence": "unresolved",
                            "anchor_hit": False, "score": 0.0})
    primary.extend(identity)
    for f in schema["entities"][name]["fields"]:
        if f.get("parent") is None and f.get("type") in ("list", "database_record_list"):
            primary.append({"field": f["code"], "offset": None, "width": 0,
                            "region": "list_not_inline", "confidence": "unresolved",
                            "anchor_hit": False, "score": 0.0})
    occupied = set()
    for a in anchor_layout:
        occupied.update(range(int(a["offset"]), int(a["offset"]) + int(a["width"])))
    free = [i for i in range(business_len) if i not in occupied]
    start = last = None
    for pos in free + [None]:
        if pos is not None and (last is None or pos == last + 1):
            start = pos if start is None else start
            last = pos
            continue
        if start is not None:
            primary.append({"field": "unresolved_wire", "offset": start,
                            "width": last - start + 1, "region": "business",
                            "confidence": "unresolved", "anchor_hit": False,
                            "score": 0.0})
        start = pos
        last = pos
    primary.sort(key=lambda a: (schema_rank.get(a["field"], 10_000),
                                a.get("offset") if a.get("offset") is not None else 1_000_000))
    total_business = sum(int(a["width"]) for a in primary if a["region"] == "business")
    validation = validate_fixture(fixture, profile, primary, total_business, verify_raw)
    ok = (validation["anchors_hit"] == validation["anchors_total"]
          and validation["closure_ok"] and validation["named_rows_ok"]
          and all(x["ok"] for x in validation["sample_checks"])
          and (not verify_raw or validation["raw_rows"].get("ok") is True))
    return {
        "name": name, "anchors_hit": validation["anchors_hit"],
        "anchors_total": validation["anchors_total"], "total_width": total_business,
        "closure_ok": validation["closure_ok"], "assignment": primary,
        "total_score": best["total_score"], "anchor_validation": validation["anchors"],
        "sample_checks": validation["sample_checks"],
        "named_rows_ok": validation["named_rows_ok"], "raw_rows": validation["raw_rows"],
        "top_solutions": top_solutions, "order_violations": order_violations,
        "order_note": ("Anchor-supported slots are independent of the remaining schema-order DP; "
                       "non-anchor field names remain unresolved in the primary assignment."),
        "status": "PASS" if ok else "FAIL",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true", help="solve and validate all four fixtures")
    ap.add_argument("--entity", choices=("award", "city", "stadium", "injury"))
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    ap.add_argument("--verify-raw", action="store_true", help="re-read all fixed rows via fm24_dump")
    args = ap.parse_args(argv)
    if not args.selftest and not args.entity:
        ap.error("use --selftest or --entity NAME")
    schema, width_types, fixtures, profiles = load_inputs()
    names = ["award", "city", "stadium", "injury"] if args.selftest else [args.entity]
    results = [solve_fixture(n, schema, width_types, fixtures[n], profiles[n],
                             verify_raw=(args.verify_raw or args.selftest)) for n in names]
    output = {"status": "PASS" if all(x["status"] == "PASS" for x in results) else "FAIL",
              "fixtures": results}
    if args.selftest:
        # This is the sole automatic output and remains within the requested OUTDIR.
        (OUT / "fixtures_result.json").write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        for x in results:
            print(f"{x['name']}: {x['anchors_hit']}/{x['anchors_total']} anchors; "
                  f"business_width={x['total_width']}; closure={x['closure_ok']}; "
                  f"status={x['status']}; raw_rows={x.get('raw_rows', {}).get('verified_rows', 0)}")
        print(f"overall: {output['status']}")
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
