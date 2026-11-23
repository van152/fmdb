#!/usr/bin/env python3
"""t90 deliverable verifier - independent of the two builders.

  py -V:3.12 -I -B scratch/t90/out/verify.py --selftest
  py -V:3.12 -I -B scratch/t90/out/verify.py --verify

Checks, from the products only (no builder imports):
  A. v11.2 vs v11.1 diff list is exactly {3 new roots} + {5 mutable roots},
     and every entry is traceable to a named source out file.
  B. denominator_v2 conserves the 1,034 occurrences and the pre-image totals.
  C. weather R1/R2 edits are value-only (25 slots, offsets identical).
  D. reports/ untouched by this task (byte pins).
Exit codes: 0 pass / 1 check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PRE = ROOT / "reports" / "club_nation_subtable_schema.json"
POST = OUT / "schema_v112.json"
DEN = OUT / "denominator_v2.json"
DEN_BASE = ROOT / "reports" / "xml_denominator_coverage.json"

PRE_SHA = "f811a216a8d1f72ea98dd86995924a3f55e952bc52b2b23466005dd7a7d4efed"
PRE_BYTES = 29893769
DEN_SHA = "e3a6d56e639fb3d9cd507500d81b3e5d4a9f591eafdfc75f0d1f1227d23df9c4"
DEN_BYTES = 297905

NEW_ROOTS = {"fk_index_e125", "five_tables_l3_e126", "table9_closure_e127"}
MUTABLE = {"schema_version", "generated_by", "coverage",
           "incremental_provenance", "scan_tables"}

# Every diff entry -> the source out file(s) it must trace to.
TRACE = {
    "fk_index_e125": ["scratch/t81/out/fk_index.json",
                      "scratch/t81/out/rescan_fk_city.json",
                      "scratch/t81/out/rescan_fk_t76.json"],
    "five_tables_l3_e126": ["scratch/t83/out/field_map.json",
                            "scratch/t83/out/domain_stats.json",
                            "scratch/t83/out/REPORT.md"],
    "table9_closure_e127": ["scratch/t85/out2/collection_fields.json",
                            "scratch/t85/out2/wire_candidates.json",
                            "scratch/t85/out2/profile_nation.json"],
    "scan_tables": ["scratch/t83/out/field_map.json"],
    "coverage": ["scratch/t81/out/rescan_fk_city.json",
                 "scratch/t83/out/domain_stats.json",
                 "scratch/t85/out2/wire_candidates.json",
                 "scratch/t90/out/denominator_v2.json"],
    "incremental_provenance": ["scratch/t01/LEDGER.json"],
    "schema_version": [], "generated_by": [],
}

fails: list[str] = []


def ck(name: str, ok: bool, detail: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm(v) -> bytes:
    return json.dumps(v, ensure_ascii=False, indent=2,
                      allow_nan=False).encode("utf-8")


def load(p: Path):
    return json.loads(p.read_bytes())


def verify() -> int:
    fails.clear()
    pre_raw = PRE.read_bytes()
    ck("A0 v11.1 baseline pin", sha(pre_raw) == PRE_SHA
       and len(pre_raw) == PRE_BYTES, f"{len(pre_raw):,} B")
    ck("A0b denominator baseline pin",
       sha(DEN_BASE.read_bytes()) == DEN_SHA
       and DEN_BASE.stat().st_size == DEN_BYTES)

    pre, post = json.loads(pre_raw), load(POST)
    added = sorted(set(post) - set(pre))
    removed = sorted(set(pre) - set(post))
    changed = sorted(k for k in pre if k in post and post[k] != pre[k])
    ck("A1 exactly 3 new roots", added == sorted(NEW_ROOTS), str(added))
    ck("A2 no root removed", removed == [], str(removed))
    ck("A3 changed roots subset of mutable", set(changed) <= MUTABLE, str(changed))
    ck("A4 all mutable roots present in diff",
       MUTABLE == set(changed), str(sorted(MUTABLE - set(changed))))
    ck("A5 root count 37 -> 40", len(pre) == 37 and len(post) == 40, str(len(post)))

    # every diff entry traces to a declared source
    missing = [p for k in added + changed for p in TRACE.get(k, [])
               if not (ROOT / p).is_file()]
    ck("A6 every diff entry has an existing source pointer", not missing,
       str(missing))
    untraced = [k for k in added + changed if k not in TRACE]
    ck("A7 no diff entry without a trace rule", not untraced, str(untraced))

    # untouched roots byte-identical
    guard = post["incremental_provenance"]["t90_assembly_guard"]
    bad = [k for k, v in guard["untouched_root_digests"].items()
           if sha(norm(post[k])) != v["sha256"]]
    ck("A8 untouched roots byte-identical", not bad, str(bad))
    ck("A9 guard covers all non-mutable v11.1 roots",
       set(guard["untouched_root_digests"]) == set(pre) - MUTABLE,
       str(len(guard["untouched_root_digests"])))

    # --- B. denominator conservation
    den, base = load(DEN), load(DEN_BASE)
    rows = den["rows"]
    ck("B1 occurrence count conserved", len(rows) == base["count"] == 1034,
       str(len(rows)))
    ck("B2 ids unique", len({r["id"] for r in rows}) == len(rows))
    pre_tot = {}
    for r in rows:
        pre_tot[r["bucket_before"]] = pre_tot.get(r["bucket_before"], 0) + 1
    ck("B3 before-image equals E116 totals",
       pre_tot == {k: v for k, v in base["totals"].items() if v}, str(pre_tot))
    post_tot = {}
    for r in rows:
        post_tot[r["bucket_after"]] = post_tot.get(r["bucket_after"], 0) + 1
    ck("B4 after totals recompute", post_tot == den["totals_after"], str(post_tot))
    ck("B5 sum before == sum after",
       sum(pre_tot.values()) == sum(post_tot.values()) == 1034)
    moved = [r for r in rows if r["bucket_before"] != r["bucket_after"]]
    ck("B6 moved rows == 117 (table_45 only)", len(moved) == 117, str(len(moved)))
    ck("B7 every moved row has reason+pointer",
       all(r["reason"] and r["pointer"] for r in moved))
    ck("B8 unresolved 277 -> 160",
       den["unresolved_wire_slot"]["before"] == 277
       and den["unresolved_wire_slot"]["after"] == 160,
       f"{den['unresolved_wire_slot']['after']}")
    ck("B9 carried 110 unchanged",
       den["physical_coverage_after"]["carried"] == 110)
    ck("B10 no invented bucket",
       set(post_tot) <= set(den["buckets_order"]))
    ck("B11 held/no_wire/ui never moved",
       all(r["bucket_after"] == r["bucket_before"] for r in rows
           if r["bucket_before"] in ("held", "no_wire_evidence", "ui_or_derived")))
    ck("B12 conflicts recorded, not adjudicated",
       len(den["conflicts"]) >= 2
       and all("escalate" in c for c in den["conflicts"]),
       str(len(den["conflicts"])))

    # --- C. weather value-only edit
    for arch in ("client", "server"):
        a = post["scan_tables"]["t76c"]["27"]["archives"][arch]["slots"]
        b = pre["scan_tables"]["t76c"]["27"]["archives"][arch]["slots"]
        ck(f"C1 weather {arch} 25 slots", len(a) == len(b) == 25, str(len(a)))
        ck(f"C2 weather {arch} offsets identical",
           [s["offset"] for s in a] == [s["offset"] for s in b])
        ck(f"C3 weather {arch} R1 wind@5 / precip@10",
           next(s for s in a if s["offset"] == 5)["field"] == "w0w0..w0w4"
           and next(s for s in a if s["offset"] == 10)["field"] == "w0p0..w0p4")
        ck(f"C4 weather {arch} R2 sd 2B i16",
           next(s for s in a if s["offset"] == 3)["width"] == 2)
        ck(f"C5 weather {arch} R2 dn@25 with 0x64",
           next(s for s in a if s["offset"] == 25)["field"] == "w0dn")

    # --- D. no report touched
    ck("D1 reports untouched by t90",
       guard["reports_touched"] == [] and guard["structural_edits"]
       == ["scan_tables/t76c/27/archives/{client,server}/slots "
           "(values only, 25 slots preserved)"])

    # --- E. diff inventory, machine readable
    inv = {"added": added, "removed": removed, "changed": changed,
           "trace": {k: TRACE.get(k, []) for k in added + changed},
           "untouched_root_count": len(guard["untouched_root_digests"]),
           "pre_bytes": len(pre_raw), "post_bytes": POST.stat().st_size}
    (OUT / "diff_inventory.json").write_bytes(
        json.dumps(inv, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    ck("E1 diff inventory written", (OUT / "diff_inventory.json").is_file())

    print(f"\n{len(fails)} failure(s)")
    return 0 if not fails else 1


def selftest() -> int:
    global fails
    fails = []
    ck("sha of empty", sha(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b93"
                              "4ca495991b7852b855")
    ck("norm stable", sha(norm({"a": 1})) == sha(norm({"a": 1})))
    ck("norm order-sensitive", sha(norm({"a": 1, "b": 2}))
       != sha(norm({"b": 2, "a": 1})))
    ck("TRACE covers all diff keys", set(TRACE) == NEW_ROOTS | MUTABLE,
       str(sorted(set(TRACE) ^ (NEW_ROOTS | MUTABLE))))
    ck("mutable and new roots disjoint", not (NEW_ROOTS & MUTABLE))
    print(f"\n{len(fails)} failure(s)")
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if not (a.verify or a.selftest):
        ap.print_help()
        return 2
    try:
        return selftest() if a.selftest else verify()
    except FileNotFoundError as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
