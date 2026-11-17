"""Baseline coverage aggregation over the frozen evidence snapshot.

Reads only evidence/fm24/ snapshots; no game/editor involvement. Reproduces the
numbers recorded in docs/BASELINE.md (2026-11-18).

Usage:
  py -V:3.12 -I scripts/baseline_coverage.py            # print aggregates
  py -V:3.12 -I scripts/baseline_coverage.py --check    # exit 1 if stable aggregates drift
  py -V:3.12 -I scripts/baseline_coverage.py --selftest # internal consistency checks
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence" / "fm24"

# Stable aggregates recorded in docs/BASELINE.md (2026-11-18 snapshot).
EXPECTED = {
    "schema_total_fields": 2144,
    "numeric_tables": 59,
    "tier_confirmed": 5,
    "tier_candidate": 4,
    "tier_unknown": 50,
    "row_fixed_stride": 37,
    "row_variable_unresolved": 18,
    "payload_total_bytes": 242111759,
    "payload_resolved_bytes": 122640318,
}

RESOLVED_ROW_MODELS = {
    "fixed_stride",
    "variable_length_rows_fully_consumed",
    "template_anchored_variable_rows",
    "ordinal_keyed_fixed_stride",
    "empty_table_payload",
    "12byte_metadata_rows",
    "length_prefixed_string_pool",
    "byte_identical_alias_of_table_23.dat",
    "ordinal_tagged_variable_payload",
}


def load(rel: str):
    return json.loads((EV / rel).read_text(encoding="utf-8"))


def aggregate() -> dict:
    master = load("reports/editor_schema/master.json")
    census = load("reports/dbdat_decode/server_tables_census.json")
    big = load("reports/dbdat_decode/db_tables_big.json")

    entity_summary = master["entity_summary"]
    out: dict = {}
    out["schema_entities"] = len(entity_summary)
    out["schema_total_fields"] = sum(v["field_count"] for v in entity_summary.values())

    numeric = [e for e in census["entries"] if e["entry_type"] == "table"]
    auxiliary = [e for e in census["entries"] if e["entry_type"] == "auxiliary"]
    out["numeric_tables"] = len(numeric)
    out["auxiliary_members"] = len(auxiliary)

    tiers = Counter(e["entity_mapping"]["tier"] for e in numeric)
    out["tier_confirmed"] = tiers.get("confirmed", 0)
    out["tier_candidate"] = tiers.get("candidate", 0)
    out["tier_unknown"] = tiers.get("unknown", 0)

    models = Counter(e["row_model"] for e in numeric)
    out["row_fixed_stride"] = models.get("fixed_stride", 0)
    out["row_variable_unresolved"] = models.get("variable_or_nonstandard", 0)

    out["payload_total_bytes"] = sum(e["payload_size"] for e in census["entries"])
    out["payload_resolved_bytes"] = sum(
        e["payload_size"] for e in census["entries"] if e["row_model"] in RESOLVED_ROW_MODELS
    )
    out["payload_resolved_pct"] = round(100 * out["payload_resolved_bytes"] / out["payload_total_bytes"], 1)

    # Named slot entries per big table (informational; BASELINE.md annotates by hand).
    named = {}
    for tid, t in big["tables"].items():
        sm = t.get("slot_map")
        if isinstance(sm, list):
            fields = [s.get("field") for s in sm if isinstance(s, dict) and s.get("field")]
        elif isinstance(sm, dict):
            fields = []
            for rows in sm.values():
                if isinstance(rows, list):
                    fields += [s.get("field") for s in rows if isinstance(s, dict) and s.get("field")]
                elif isinstance(rows, dict) and rows.get("field"):
                    fields.append(rows["field"])
        else:
            fields = []
        named[f"table_{tid}"] = sorted(f for f in fields if f)
    out["named_slots_per_big_table"] = named
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate DB-parsing coverage baseline from evidence snapshots.")
    ap.add_argument("--check", action="store_true", help="exit 1 if stable aggregates drift from BASELINE.md")
    ap.add_argument("--selftest", action="store_true", help="internal consistency checks, then exit")
    args = ap.parse_args()

    data = aggregate()

    if args.selftest:
        problems = []
        if data["numeric_tables"] + data["auxiliary_members"] != 77:
            problems.append("census entries != 77")
        if data["tier_confirmed"] + data["tier_candidate"] + data["tier_unknown"] != data["numeric_tables"]:
            problems.append("tiers do not sum to numeric tables")
        if data["payload_resolved_bytes"] > data["payload_total_bytes"]:
            problems.append("resolved bytes exceed total")
        if problems:
            print("SELFTEST FAIL:", "; ".join(problems))
            return 1
        print("SELFTEST OK")
        return 0

    print(json.dumps(data, indent=1, ensure_ascii=False))

    if args.check:
        drift = {k: (EXPECTED[k], data.get(k)) for k in EXPECTED if data.get(k) != EXPECTED[k]}
        if drift:
            print("CHECK FAILED — drift from BASELINE.md:", json.dumps(drift, ensure_ascii=False))
            return 1
        print("CHECK OK — stable aggregates match docs/BASELINE.md (2026-11-18)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
