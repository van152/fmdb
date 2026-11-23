#!/usr/bin/env python3
"""t92 independent verifier for schema v11.3-candidate (E132-E138 merge).

Does NOT import the builder. Reads only:
  reports/club_nation_subtable_schema.json   (v11.2 baseline, read-only)
  reports/xml_denominator_coverage.json      (v2, read-only)
  scratch/t92/out/schema_v113.json           (product)
  scratch/t92/out/denominator_note.json      (product)
  scratch/t88/out3/slots.json, scratch/t89/out/_dual.json, scratch/t01/LEDGER.json

  py -V:3.12 -I -B scratch/t92/out/verify.py
  py -V:3.12 -I -B scratch/t92/out/verify.py --selftest

Writes scratch/t92/out/diff_inventory.json. Exit 0 all pass / 1 any fail / 2 fatal.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT / "reports" / "club_nation_subtable_schema.json"
DENOM = ROOT / "reports" / "xml_denominator_coverage.json"
PROD = HERE / "schema_v113.json"
NOTE = HERE / "denominator_note.json"
SLOTS = ROOT / "scratch" / "t88" / "out3" / "slots.json"
DUAL = ROOT / "scratch" / "t89" / "out" / "_dual.json"
LEDGER = ROOT / "scratch" / "t01" / "LEDGER.json"
INVENTORY = HERE / "diff_inventory.json"

NEW_ROOTS = ("table45_structure_e132_e138", "t9_grammar_e133", "cbw_route_e135_e137")
MUTABLE = ("schema_version", "generated_by", "coverage",
           "incremental_provenance", "table9_closure_e127")
LEDGER_IDS = [f"E{i}" for i in range(132, 139)]


def load(p: Path) -> Any:
    return json.loads(p.read_bytes())


def digest(v: Any) -> str:
    raw = json.dumps(v, ensure_ascii=False, indent=2, allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def leaves(o: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten to leaf paths; lists of scalars become one leaf (keeps diffs small)."""
    out: dict[str, Any] = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(leaves(v, f"{prefix}/{k}"))
    elif isinstance(o, list) and any(isinstance(x, (dict, list)) for x in o):
        for i, v in enumerate(o):
            out.update(leaves(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = o
    return out


def diff_paths(a: dict[str, Any], b: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for k in sorted(set(a) | set(b)):
        if k not in a:
            out.append({"path": k, "change": "added", "after": b[k]})
        elif k not in b:
            out.append({"path": k, "change": "removed", "before": a[k]})
        elif a[k] != b[k]:
            out.append({"path": k, "change": "value", "before": a[k], "after": b[k]})
    return out

def v1_traceability(pre: dict[str, Any], prod: dict[str, Any]) -> dict[str, Any]:
    """V1: every v11.2->v11.3 leaf diff traces to a declared source."""
    before = leaves({k: pre[k] for k in pre})
    after = leaves({k: prod[k] for k in prod})
    d = diff_paths(before, after)
    rules = {
        "/schema_version": "version bump t92",
        "/generated_by": "generator bump t92",
        "/coverage": "coverage counters appended by t92",
        "/incremental_provenance": "provenance snapshots appended by t92",
        "/table9_closure_e127": "E133 nine-byte correction + annotations",
    }
    untraced = []
    for item in d:
        p = item["path"]
        root = "/" + p.lstrip("/").split("/")[0].split("[")[0]
        new_root = root.lstrip("/") in NEW_ROOTS
        if new_root:
            item["trace"] = f"new root section {root} (E132-E138)"
        elif root in rules:
            item["trace"] = rules[root]
        else:
            item["trace"] = "UNTRACED"
            untraced.append(p)
    # every non-mutable, non-new root must be byte-identical
    silent = [k for k in pre if k in prod and k not in MUTABLE
              and k not in NEW_ROOTS and digest(pre[k]) != digest(prod[k])]
    return {"check": "V1_traceability", "diff_count": len(d), "untraced": untraced,
            "silently_changed_roots": silent,
            "pass": not untraced and not silent, "diff": d}


def v2_e127(prod: dict[str, Any]) -> dict[str, Any]:
    """V2: E133 correction applied exactly, before/after cross-checked."""
    cc = prod["table9_closure_e127"]["cross_check_t51_frozen_cursor"]
    srv, cli = cc["server|table_9.dat"], cc["client|table_9.dat"]
    checks = {
        "server_t51_footer_at_307564": srv["t51_footer_at"] == 307564,
        "server_t51_last_end_307564": srv["t51_last_end"] == 307564,
        "server_no_307555_left": 307555 not in (srv["t51_footer_at"], srv["t51_last_end"]),
        "why_before_present": bool(srv.get("t92_why_before")),
        "correction_block": srv.get("t92_correction", {}).get("value_before") == 307555
        and srv.get("t92_correction", {}).get("value_after") == 307564,
        "client_untouched_31947": cli["t51_footer_at"] == 31947
        and cli["t51_last_end"] == 31947,
        "client_plus_9_eq_payload": 31947 + 9 == 31956,
        "server_plus_9_eq_payload": 307555 + 9 == 307564,
        "closure_claim_already_right": prod["table9_closure_e127"]
        ["closure_claims"]["table_9_server"]["payload"] == 307564,
        "chain_already_right": prod["table9_closure_e127"]["chains"]
        ["server|table_9.dat"]["payload"] == 307564,
        "section_note": prod["table9_closure_e127"].get("t92_e127_note", {})
        .get("ledger") == "E133",
    }
    return {"check": "V2_e127_correction", "detail": checks,
            "pass": all(checks.values())}


def v3_section_counts(prod: dict[str, Any]) -> dict[str, Any]:
    """V3: the three new sections exist with their declared counters."""
    s45 = prod["table45_structure_e132_e138"]
    s9 = prod["t9_grammar_e133"]
    sc = prod["cbw_route_e135_e137"]
    rc = s45["row_decomposition_e138"]["t92_recompute"]
    checks = {
        "root_count_43": len(prod) == 43,
        "new_roots_present": all(k in prod for k in NEW_ROOTS),
        "s45_ledger_3": s45["acceptance_ledger_entries"] == ["E132", "E134", "E138"],
        "s45_rows_84477": s45["table"]["rows"] == 84477,
        "s45_recompute_rows": rc["rows"] == 84477,
        "s45_recompute_bad_rowlen_0": rc["bad_rowlen"] == 0,
        "s45_recompute_bad_identity_0": rc["bad_identity"] == 0,
        "s45_recompute_rt_distinct_37": rc["rec_type_distinct"] == 37,
        "s45_recompute_rt255": rc["rec_type_255_null"] == 38968,
        "s45_recompute_rt8": rc["rec_type_8_rows"] == 3391
        and rc["rec_type_8_namelen_nonzero"] == 0,
        "s45_physical_14": "~14" in s45["row_decomposition_e138"]
        ["physical_column_count"],
        "s45_view_117": s45["accessor_view_model_e138"]["claim"].startswith("117"),
        "s9_ledger_1": s9["acceptance_ledger_entries"] == ["E133"],
        "s9_header_13": s9["header_13b_decode"]["len"] == 13,
        "s9_count_251": s9["header_13b_decode"]["count_field"].startswith("u32 @ +8 = 251"),
        "s9_client_31956": s9["closure"]["client"]["payload"] == 31956,
        "s9_server_307564": s9["closure"]["server"]["payload"] == 307564,
        "s9_server_body_304530": s9["closure"]["server"]["body_sum"] == 304530,
        "s9_server_distinct_211": s9["closure"]["server"]["body_len"]["distinct"] == 211,
        "s9_client_distinct_92": s9["closure"]["client"]["body_len"]["distinct"] == 92,
        "s9_ordinal_251": s9["lanes"]["ordinal_lane"]["rows_ok"] == "251/251",
        "s9_sentinel_251": s9["lanes"]["sentinel_head"]["rows_ok"] == "251/251",
        "sc_ledger_3": sc["acceptance_ledger_entries"] == ["E135", "E136", "E137"],
        "sc_zero_occurrence": sc["negative_result_4cc_absence"]["grade"] == "L2",
        "sc_downgrade": "unverified" in sc["e121_reference_downgrade"]["grade"],
        "sc_pe_nsec_18": sc["pe_baseline_fix8"]["nsec"] == 18,
        "sc_reloc_45mb": sc["pe_baseline_fix8"]["reloc_section"]["vsize"] > 45_000_000,
        "L4_zero": prod["coverage"]["L4"] == 0
        and s45["L4"] == s9["L4"] == sc["L4"] == 0,
    }
    return {"check": "V3_new_section_counts", "detail": checks,
            "pass": all(checks.values())}


def v4_root_invariants(pre: dict[str, Any], prod: dict[str, Any]) -> dict[str, Any]:
    """V4: nothing removed, nothing silently rewritten, guard self-consistent."""
    guard = prod["incremental_provenance"]["t92_assembly_guard"]
    ud = guard["untouched_root_digests"]
    bad = [k for k, v in ud.items() if digest(prod[k]) != v["sha256"]]
    missing = [k for k in ud if k not in prod]
    checks = {
        "no_root_removed": set(pre) <= set(prod),
        "exactly_3_new": set(prod) - set(pre) == set(NEW_ROOTS),
        "untouched_digests_match": not bad,
        "untouched_roots_all_present": not missing,
        "untouched_count": len(ud) == len(pre) - len(MUTABLE),
        "mutable_listed": set(guard["mutable_roots"]) == set(MUTABLE)
        and len(guard["mutable_roots"]) == len(MUTABLE),
        "reports_touched_empty": guard["reports_touched"] == [],
        "baseline_pin": guard["baseline"]["sha256"]
        == hashlib.sha256(BASE.read_bytes()).hexdigest(),
        "baseline_version": pre["schema_version"] == "11.2",
        "product_version": prod["schema_version"] == "11.3-candidate"
        and prod["generated_by"] == "t92",
        "structural_edits_only_e127": len(guard["structural_edits"]) == 1
        and "table9_closure_e127" in guard["structural_edits"][0],
    }
    return {"check": "V4_root_invariants", "detail": checks,
            "bad_digests": bad, "pass": all(checks.values())}

def v5_family_rt(prod: dict[str, Any]) -> dict[str, Any]:
    """V5: family<->rec_type table agrees with slots.json (34 L3)."""
    slots = load(SLOTS)["codes"]
    l3 = [e for e in slots if e.get("grade") == "L3"]
    fam: dict[str, set] = {}
    for e in l3:
        if e.get("rec_type") is not None:
            fam.setdefault(e["family"], set()).add(int(e["rec_type"]))
    expect = {k: sorted(v) for k, v in sorted(fam.items())}
    got = prod["table45_structure_e132_e138"]["accessor_view_model_e138"]
    checks = {
        "l3_count_34": len(l3) == 34,
        "section_l3_count_34": got["l3_code_count"] == 34,
        "map_equals_slots": got["family_to_rec_type"] == expect,
        "families_7": got["families_anchored"] == len(expect) == 7,
        "rec_types_7": got["rec_types_anchored"] == [10, 13, 24, 25, 26, 27, 28],
        "no_family_conflict": got["family_rt_conflicts"] == [],
        "e138_examples_agree": all(
            got["family_to_rec_type"][x["family"]] == [x["rec_type"]]
            for x in got["rt_14_34_L3_examples"]),
        "example_l3_counts_agree": all(
            x["l3_codes"] == sum(1 for e in l3 if e["family"] == x["family"])
            for x in got["rt_14_34_L3_examples"]),
        "held_80": sum(1 for e in slots if e.get("status") == "held") == 80,
        "no_held_rec_type_claim": all(e.get("rec_type") is None for e in slots
                                      if e.get("status") == "held"),
    }
    return {"check": "V5_family_rt_vs_slots", "detail": checks,
            "expect": expect, "got": got["family_to_rec_type"],
            "pass": all(checks.values())}


def v6_denominator() -> dict[str, Any]:
    """V6: denominator note is annotation-only (no count/grade movement)."""
    den = load(DENOM)
    note = load(NOTE)
    base_rows = [r for r in den["rows"] if r["bucket_after"] == "re_routed_table_45"]
    checks = {
        "117_rows": len(note["rows"]) == len(base_rows) == 117,
        "ids_identical": [r["id"] for r in note["rows"]]
        == [r["id"] for r in base_rows],
        "codes_identical": [r["code"] for r in note["rows"]]
        == [r["code"] for r in base_rows],
        "grades_identical": [r["grade"] for r in note["rows"]]
        == [r["grade"] for r in base_rows],
        "grade_unchanged_flag": all(r["grade_unchanged"] for r in note["rows"]),
        "note_present": all(r["grade_note"] for r in note["rows"]),
        "note_ledger": all(r["note_ledger"] == ["E132", "E138"]
                           for r in note["rows"]),
        "totals_unchanged": note["totals_after_unchanged"] == den["totals_after"],
        "unresolved_unchanged": note["unresolved_wire_slot_unchanged"]
        == den["unresolved_wire_slot"],
        "base_pin": note["base"]["sha256"] == hashlib.sha256(DENOM.read_bytes()).hexdigest(),
        "report_not_written": den["generated_by"] == "t90"
        and den["schema_version"] == "2",
    }
    return {"check": "V6_denominator_note", "detail": checks,
            "pass": all(checks.values())}


def v7_ledger(prod: dict[str, Any]) -> dict[str, Any]:
    """V7: E132-E138 provenance rows match the ledger's canonical claim hashes."""
    led = {e["id"]: e for e in load(LEDGER)["entries"]}
    snap = prod["incremental_provenance"]["t92_ledger_snapshot"]
    rows = {r["id"]: r for r in snap["entries"]}
    checks = {"seven_entries": sorted(rows) == sorted(LEDGER_IDS)}
    for eid in LEDGER_IDS:
        e = led[eid]
        raw = json.dumps(e["claim"], ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
        h = hashlib.sha256(raw).hexdigest()
        checks[f"{eid}_hash"] = rows[eid]["claim_sha256"] == h
        checks[f"{eid}_kind"] = rows[eid]["kind"] == e["kind"]
        checks[f"{eid}_level"] = rows[eid]["level"] == e["level"]
        checks[f"{eid}_date"] = rows[eid]["date"] == e["date"]
        checks[f"{eid}_in_acceptance_map"] = (
            prod["incremental_provenance"]["acceptance_ledger_entries"]
            [eid]["claim_sha256"] == h)
    return {"check": "V7_ledger_provenance", "detail": checks,
            "pass": all(checks.values())}


def v8_dual(prod: dict[str, Any]) -> dict[str, Any]:
    """V8: t9 grammar numbers agree with the t89 dual profile."""
    dual = load(DUAL)
    s9 = prod["t9_grammar_e133"]["closure"]
    c, s = dual["client"], dual["server"]
    checks = {
        "client_payload": s9["client"]["payload"] == c["payload"] == 31956,
        "server_payload": s9["server"]["payload"] == s["payload"] == 307564,
        "client_sum": s9["client"]["body_sum"] == c["body_len"]["sum"] == 28922,
        "server_sum": s9["server"]["body_sum"] == s["body_len"]["sum"] == 304530,
        "client_distinct": s9["client"]["body_len"]["distinct"]
        == c["body_len"]["distinct"] == 92,
        "server_distinct": s9["server"]["body_len"]["distinct"]
        == s["body_len"]["distinct"] == 211,
        "closure_client": 13 + 28922 + 12 * 251 + 9 == 31956,
        "closure_server": 13 + 304530 + 12 * 251 + 9 == 307564,
        "ordinal_lane_dual": c["ordinal_lane_ok"] == 251,
        "sentinel_dual": c["const_head_offsets"] == {"0": 0, "1": 255, "2": 255,
                                                     "3": 255, "4": 255},
    }
    return {"check": "V8_t9_dual_agreement", "detail": checks,
            "pass": all(checks.values())}


def main() -> int:
    if not PROD.exists() or not NOTE.exists():
        print("FATAL: product files missing; run scripts/t92_schema_v113.py --all")
        return 2
    pre, prod = load(BASE), load(PROD)
    results = [v1_traceability(pre, prod), v2_e127(prod), v3_section_counts(prod),
               v4_root_invariants(pre, prod), v5_family_rt(prod), v6_denominator(),
               v7_ledger(prod), v8_dual(prod)]
    fails = [r for r in results if not r["pass"]]
    for r in results:
        bad = [k for k, v in r.get("detail", {}).items() if not v]
        if r["check"] == "V1_traceability":
            bad += r["untraced"] + r["silently_changed_roots"]
        print(("PASS " if r["pass"] else "FAIL ") + r["check"]
              + ("" if r["pass"] else "  failed=" + str(bad)))
    inv = {
        "generated_by": "t92",
        "product": {"path": "scratch/t92/out/schema_v113.json",
                    "sha256": hashlib.sha256(PROD.read_bytes()).hexdigest(),
                    "bytes": PROD.stat().st_size,
                    "schema_version": prod["schema_version"],
                    "root_keys": len(prod)},
        "baseline": {"path": "reports/club_nation_subtable_schema.json",
                     "sha256": hashlib.sha256(BASE.read_bytes()).hexdigest(),
                     "schema_version": pre["schema_version"],
                     "root_keys": len(pre)},
        "checks": [{k: r[k] for k in ("check", "pass")} for r in results],
        "diff_inventory": results[0]["diff"],
        "diff_count": results[0]["diff_count"],
        "new_roots": list(NEW_ROOTS),
        "mutable_roots": list(MUTABLE),
        "verdict": "pass" if not fails else "fail",
        "L4": 0,
    }
    INVENTORY.write_bytes(json.dumps(inv, ensure_ascii=False, indent=1).encode("utf-8"))
    print(f"\n{len(results) - len(fails)}/{len(results)} checks passed "
          f"| diff leaves {results[0]['diff_count']}")
    print(f"wrote {INVENTORY.relative_to(ROOT)}")
    return 0 if not fails else 1


def selftest() -> int:
    ok = True

    def ck(n: str, c: bool) -> None:
        nonlocal ok
        print(("OK   " if c else "FAIL ") + n)
        ok = ok and c

    ck("leaves flat", leaves({"a": {"b": 1}}) == {"/a/b": 1})
    ck("leaves scalar list one leaf", leaves({"a": [1, 2]}) == {"/a": [1, 2]})
    ck("diff detects value", diff_paths({"/a": 1}, {"/a": 2})[0]["change"] == "value")
    ck("diff detects added", diff_paths({}, {"/a": 1})[0]["change"] == "added")
    ck("diff detects removed", diff_paths({"/a": 1}, {})[0]["change"] == "removed")
    ck("e133 delta", 307564 - 307555 == 9)
    ck("closure", 13 + 304530 + 12 * 251 + 9 == 307564)
    print("SELFTEST PASSED" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
