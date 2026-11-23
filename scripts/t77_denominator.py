"""t77 builder: reports/xml_denominator_coverage.json — the 1,034-occurrence ledger.

Split out of the main schema on purpose. Numbers come from scratch/t78/out/
buckets.json (E116, L1: frozen artifacts only, no .dat read, no disassembly).
"""
from __future__ import annotations

from typing import Any

from t77_common import ROOT, artifacts, json_bytes, read_json, sha

T78 = ROOT / "scratch" / "t78" / "out"
BUCKETS = ("mapped_l3", "independent_member", "string_name_table", "ui_or_derived",
           "held", "unresolved_wire_slot", "no_wire_evidence")


def build() -> dict[str, Any]:
    b = read_json(T78 / "buckets.json")
    occ = b["occurrences"]
    per_entity: dict[str, dict[str, int]] = {}
    for o in occ:
        e = per_entity.setdefault(o["entity"], {k: 0 for k in BUCKETS})
        e[o["bucket"]] = e.get(o["bucket"], 0) + 1
    for e in per_entity:
        per_entity[e]["sum"] = sum(per_entity[e][k] for k in BUCKETS)
    totals = {k: sum(v[k] for v in per_entity.values()) for k in BUCKETS}
    carried = totals["mapped_l3"] + totals["independent_member"] + totals["string_name_table"]

    unresolved_by_entity: dict[str, list[dict[str, Any]]] = {}
    for o in occ:
        if o["bucket"] == "unresolved_wire_slot":
            unresolved_by_entity.setdefault(o["entity"], []).append(
                {"id": o["id"], "code": o["code"], "note": o["note"],
                 "evidence_ref": o["evidence_ref"]})

    samples = {}
    for e in ("club", "comp", "nation"):
        rows = [o for o in occ if o["entity"] == e]
        samples[e] = [{"id": r["id"], "code": r["code"], "bucket": r["bucket"],
                       "evidence_ref": r["evidence_ref"]} for r in rows[:3]]

    return {
        "schema_id": "fm24.xml_denominator_coverage",
        "schema_version": 1,
        "generated_by": "t77",
        "source_task": "t78",
        "acceptance_ledger_entry": "E116",
        "acceptance_ledger_level": "L1",
        "status": "complete",
        "method": ("real physical-coverage denominator over club/nation/comp top-level XML "
                   "occurrences; frozen artifacts only (schema v10 + t71 r3 + t72 inventory + "
                   "t57/t69 tail ledger), no .dat read, no disassembly"),
        "schema_basis": b["schema_basis"],
        "buckets_order": list(BUCKETS),
        "count": b["count"],
        "per_entity": {e: per_entity[e] for e in ("club", "nation", "comp")},
        "totals": totals,
        "physical_coverage": {
            "formula": "mapped_l3 + independent_member + string_name_table",
            "carried": carried,
            "denominator": b["count"],
            "ratio": round(carried / b["count"], 4),
            "text": "110/1034 = 10.6%",
            "held": totals["held"],
            "unresolved_wire_slot": totals["unresolved_wire_slot"],
            "no_wire_evidence": totals["no_wire_evidence"],
        },
        "unresolved_wire_slot_detail": {
            "club": {"occurrences": len(unresolved_by_entity.get("club", [])),
                     "distinct_slots": 20,
                     "slots": ["pos0/selector", "pos1/derived_170", "pos2/derived_178",
                               "pos4/ref_e0", "pos9/name_len", "pos11/short_len",
                               "pos14/raw166", "pos16/raw16c", "pos17/vec110",
                               "pos18/obj150_tag", "pos20/vec130", "pos21/vec138",
                               "pos22/raw168", "pos24/base_ba", "pos26/base18",
                               "pos27/base30", "pos28/base60", "pos29/base78",
                               "pos30/base90", "pos32/basea8"],
                     "note": "highest naming ROI per E116"},
            "comp": {"occurrences": len(unresolved_by_entity.get("comp", [])),
                     "distinct_slots": 36},
            "nation": {"occurrences": len(unresolved_by_entity.get("nation", [])),
                       "note": "0 unresolved wire slots; 318 no_wire_evidence (grammar closed "
                               "by t75, naming needs name-pool/t02)"},
        },
        "occurrences": [{"id": o["id"], "entity": o["entity"], "code": o["code"],
                         "bucket": o["bucket"], "note": o["note"],
                         "evidence_ref": o["evidence_ref"]} for o in occ],
        "samples": samples,
        "purpose": ("priority basis for Wave 10/11 ordering and the targeted t02 Top-N list "
                    "(user directive: get the real denominator first)"),
        "source_artifacts": artifacts("scratch/t78/out/buckets.json",
                                      "scratch/t78/out/coverage.md",
                                      "scratch/t78/out/DONE.md"),
        "L4": 0,
    }


def write() -> dict[str, Any]:
    doc = build()
    raw = json_bytes(doc)
    (ROOT / "reports" / "xml_denominator_coverage.json").write_bytes(raw)
    return {"path": "reports/xml_denominator_coverage.json", "sha256": sha(raw),
            "bytes": len(raw), "count": doc["count"],
            "carried": doc["physical_coverage"]["carried"]}
