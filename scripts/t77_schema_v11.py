#!/usr/bin/env python3
"""t77 — schema v10 -> v11 modular fold + repository hygiene.

  py -V:3.12 -I -B scripts/t77_schema_v11.py --selftest
  py -V:3.12 -I -B scripts/t77_schema_v11.py --build
  py -V:3.12 -I -B scripts/t77_schema_v11.py --verify

Exit codes: 0 pass / 1 check failed / 2 usage or fatal.

--build is additive only: it writes
  reports/club_nation_subtable_schema.json      (v11, existing sections byte-preserved)
  reports/club_nation_subtable_schema.md        (v10 bytes + one appended appendix)
  reports/other_tables_schema.json              (13 non-main-table slot verdicts)
  reports/xml_denominator_coverage.json         (1,034-occurrence denominator ledger)
and scratch/t77/out/v11_diff_summary.json.

--verify is a HISTORICAL verifier for the frozen v11 artifacts (commit 213657a).
It materialises those four files into scratch/t77/frozen/ if absent, re-reads every
accepted input from disk, re-derives the section counts and checks them against the
pinned v11 ledger claims. It never writes reports/ and never validates the current
v11.3 published schema (that is covered by t92_schema_v113.py --selftest).
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import t77_assemble as AS
import t77_build as BL
import t77_common as C
import t77_denominator as DN
import t77_md as MD
import t77_other_tables as OT
import t77_sections_a as A
import t77_sections_b as B


class Reporter:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def check(self, name: str, ok: bool, detail: Any = "") -> bool:
        self.rows.append({"check": name, "ok": bool(ok), "detail": detail})
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        return bool(ok)

    def failures(self) -> list[dict[str, Any]]:
        return [r for r in self.rows if not r["ok"]]


# --------------------------------------------------------------- selftest ----
def selftest(rep: Reporter) -> int:
    rep.check("sha256 empty vector",
              C.sha(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
              "known digest")
    rep.check("canonical_sha256 is key-order stable",
              C.canonical_sha256({"b": 1, "a": 2}) == C.canonical_sha256({"a": 2, "b": 1}),
              "sorted keys")
    rep.check("canonical_sha256 is separator sensitive",
              C.canonical_sha256({"a": 1}) != C.canonical_sha256({"a": "1"}),
              "type sensitivity")
    rep.check("json_bytes round-trips",
              json.loads(C.json_bytes({"x": [1, 2]})) == {"x": [1, 2]}, "utf-8 + newline")
    rep.check("guarded id range is E111-E120",
              C.GUARDED_IDS[0] == "E111" and C.GUARDED_IDS[-1] == "E120"
              and len(C.GUARDED_IDS) == 10, list(C.GUARDED_IDS))
    rep.check("pinned ledger table covers the guard set",
              set(BL.PINNED_LEDGER) == set(C.GUARDED_IDS), len(BL.PINNED_LEDGER))
    rep.check("source pin table is non-trivial", len(C.SOURCE_SHA256) >= 50,
              f"{len(C.SOURCE_SHA256)} artifacts pinned")
    fails = rep.failures()
    print(f"\nselftest: {len(rep.rows) - len(fails)}/{len(rep.rows)} checks passed")
    return 0 if not fails else 1


# ------------------------------------------------------------------ build ----
def build(rep: Reporter) -> int:
    r = AS.assemble()
    doc, base = r["doc"], r["base"]
    other, denom = r["other"], r["denom"]

    raw = C.json_bytes(doc)
    md_raw = BL.BASE_SNAPSHOT_MD.read_bytes()
    md_new = md_raw + MD.appendix(doc, r["sections"]).encode("utf-8")
    C.PUBLIC_JSON.write_bytes(raw)
    C.PUBLIC_MD.write_bytes(md_new)

    rep.check("v11 written", True, f"{len(raw):,} B json / {len(md_new):,} B md")
    rep.check("other_tables_schema.json written", True,
              f"{other['bytes']:,} B / {other['table_count']} tables")
    rep.check("xml_denominator_coverage.json written", True,
              f"{denom['bytes']:,} B / {denom['count']} occurrences")

    diff = diff_summary(base, doc, r["sections"], other, denom, len(raw), len(md_new))
    C.OUT.mkdir(parents=True, exist_ok=True)
    (C.OUT / "v11_diff_summary.json").write_bytes(C.json_bytes(diff))
    rep.check("v11_diff_summary.json written", True, str(C.OUT / "v11_diff_summary.json"))
    fails = rep.failures()
    print(f"\nbuild: {len(rep.rows) - len(fails)}/{len(rep.rows)} checks passed")
    return 0 if not fails else 1


def diff_summary(base: dict[str, Any], doc: dict[str, Any], sec: dict[str, Any],
                 other: dict[str, Any], denom: dict[str, Any],
                 json_bytes: int, md_bytes: int) -> dict[str, Any]:
    def size(o: Any) -> int:
        return len(json.dumps(o, ensure_ascii=False).encode("utf-8"))

    new_sections = {k: {"bytes": size(doc[k])} for k in BL.NEW_ROOT if k in doc}
    new_sections["club_extra_object_row"]["promoted_records"] = \
        sec["e111"]["promoted"]["count"]
    new_sections["slot_fingerprints"]["tables"] = {k: v["slot_count"]
                                                  for k, v in sec["e112"]["tables"].items()}
    new_sections["simple_tables"]["frames_closed"] = sec["e113"]["frames_closed"]
    new_sections["nation_segment_grammars"]["grammars"] = sec["e114g"]["grammar_count"]
    new_sections["xref_reverse_adjudication"]["adjudicated"] = \
        sec["e114x"]["totals"]["adjudicated"]
    new_sections["row_frames9"]["frames"] = len(sec["e115"]["frames"])
    new_sections["stadium_team_l3"]["counts"] = sec["e117"]["counts"]
    new_sections["scan_tables"]["stadium_slots"] = sec["scan"]["stadium"]["slot_counts"]
    new_sections["scan_tables"]["t76c_tables"] = sorted(sec["scan"]["t76c"])
    new_sections["xml_denominator_coverage"]["denominator"] = denom["count"]

    return {
        "generated_by": "t77",
        "base": {"schema_version": base["schema_version"], "generated_by": base["generated_by"],
                 "json_bytes": BL.BASE_SNAPSHOT.stat().st_size,
                 "md_bytes": BL.BASE_SNAPSHOT_MD.stat().st_size,
                 "sha256": C.BASE_JSON_SHA256, "md_sha256": C.BASE_MD_SHA256},
        "v11": {"schema_version": doc["schema_version"], "generated_by": doc["generated_by"],
                "json_bytes": json_bytes, "md_bytes": md_bytes,
                "root_keys": len(doc)},
        "root_key_delta": {"added": [k for k in doc if k not in base],
                           "removed": [k for k in base if k not in doc]},
        "section_entry_counts": new_sections,
        "preserved_sections": {k: {"bytes": size(base[k]),
                                  "unchanged": doc[k] == base[k]}
                               for k in base if k not in BL.MUTABLE_ROOT
                               and k not in BL.NEW_ROOT},
        "coverage_changes": {k: {"from": base["coverage"].get(k), "to": doc["coverage"].get(k)}
                             for k in set(base["coverage"]) | set(doc["coverage"])
                             if base["coverage"].get(k) != doc["coverage"].get(k)},
        "split_files": {
            "other_tables_schema.json": {"path": other["path"], "bytes": other["bytes"],
                                        "sha256": other["sha256"],
                                        "tables": other["table_count"]},
            "xml_denominator_coverage.json": {"path": denom["path"], "bytes": denom["bytes"],
                                              "sha256": denom["sha256"],
                                              "occurrences": denom["count"]},
        },
        "ledger_entries_added": list(C.GUARDED_IDS),
        "out_of_scope": {"E121": "t82 landed after this lane departed -> t87"},
        "L4": 0,
    }


# ----------------------------------------------------------------- verify ----
def verify_stage(rep: Reporter) -> int:
    import t77_verify as V
    return V.verify(rep)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="t77_schema_v11.py",
        description="Fold accepted E111-E120 into schema v11 (additive) and check the result.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build", action="store_true",
                   help="write reports/*.json, reports/*.md and scratch/t77/out/v11_diff_summary.json")
    g.add_argument("--verify", action="store_true",
                   help="re-read every accepted input and re-check all counts (writes nothing)")
    g.add_argument("--selftest", action="store_true", help="check the helper primitives only")
    args = ap.parse_args(argv)
    rep = Reporter()
    try:
        if args.selftest:
            return selftest(rep)
        if args.build:
            return build(rep)
        return verify_stage(rep)
    except C.CheckFailure as exc:
        print(f"FATAL: {exc}")
        return 1
    except FileNotFoundError as exc:
        print(f"FATAL: missing input: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
