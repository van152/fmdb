"""t77 assemble: build the v11 document object and its Markdown appendix."""
from __future__ import annotations

import copy
import json
from typing import Any

import t77_build as BL
import t77_common as C
import t77_denominator as DN
import t77_other_tables as OT
import t77_sections_a as A
import t77_sections_b as B


def build_sections() -> dict[str, Any]:
    return {
        "e111": A.club_extra_object_row(),
        "e112": A.slot_fingerprints(),
        "e113": A.simple_tables(),
        "e114g": B.nation_segment_grammars(),
        "e114x": B.xref_reverse_adjudication(),
        "e115": B.row_frames9(),
        "e117": B.stadium_team_l3(),
        "scan": B.scan_tables(),
        "denom": B.denominator_summary(),
    }


def provenance(base: dict[str, Any], guards: dict[str, Any],
               sec: dict[str, Any], other: dict[str, Any],
               denom: dict[str, Any]) -> dict[str, Any]:
    prov = copy.deepcopy(base["incremental_provenance"])
    rows = prov.setdefault("acceptance_ledger_entries", {})
    for eid, rec in guards["records"].items():
        if eid in rows:
            C.require(rows[eid].get("claim_sha256") == rec["claim_sha256"],
                      f"live ledger differs from pinned row: {eid}")
        rows[eid] = {"kind": rec["kind"], "level": rec["level"],
                     "date": rec["date"], "claim_sha256": rec["claim_sha256"]}
    tasks = prov.setdefault("tasks", {})
    for task, (eid, level, section) in BL.TASK_SPEC.items():
        C.require(task not in tasks, f"task already present in v10 provenance: {task}")
        tasks[task] = {
            "acceptance_ledger_entry": eid,
            "acceptance_ledger_level": level,
            "section": section,
            "source_artifacts": [a for a in C.SOURCE_SHA256
                                 if a.startswith(f"scratch/{task}/out/")],
        }
    prov["t77_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": ("entry-level id, kind, level and canonical claim SHA-256; "
                        "no live full-file hash or byte-count pin"),
        "guarded_entries": list(C.GUARDED_IDS),
        "entries": guards["entries"],
        "v10_baseline_acceptance_entry": "E110",
        "v10_baseline_acceptance_level": "L3",
        "v10_baseline_files": {
            "json": {"path": "scratch/t70/out/club_nation_subtable_schema.v10.json",
                     "sha256": C.BASE_JSON_SHA256,
                     "bytes": BL.BASE_SNAPSHOT.stat().st_size},
            "markdown": {"path": "scratch/t70/out/club_nation_subtable_schema.v10.md",
                         "sha256": C.BASE_MD_SHA256,
                         "bytes": BL.BASE_SNAPSHOT_MD.stat().st_size},
        },
        "merged_tasks": {t: eid for t, (eid, _, _) in BL.TASK_SPEC.items()},
        "out_of_scope_note": ("E121 (t82, table_extra_3 dual-object closure) landed after this "
                              "lane departed; it is not folded here and belongs to t87."),
    }
    prov["t77_volume_policy"] = {
        "main_schema_keeps": ["three main tables", "8 numbered club subtables", "CLUB_LINK",
                             "all r2/r3 sections", "the new pointer-carrying sections"],
        "split_files": [
            {"path": other["path"], "sha256": other["sha256"], "bytes": other["bytes"],
             "content": "13 non-main-table slot verdicts (t73/t76a/t76c slots + t74 frames)"},
            {"path": denom["path"], "sha256": denom["sha256"], "bytes": denom["bytes"],
             "content": "1,034-occurrence XML denominator ledger with per-occurrence records"},
        ],
        "rationale": ("v10 was 29.5 MB because bulk records (nation_t9_wire 1.27 MB, "
                      "comp_collections 4.10 MB, r2 held/unmapped lists) are embedded inline. "
                      "v11 does not touch those sections (byte-preserved) and keeps its own "
                      "additions pointer-based so the fold adds ~0.2 MB instead of ~2 MB."),
    }
    return prov


def assemble() -> dict[str, Any]:
    base, base_raw = BL.load_baseline()
    sources = BL.check_sources()
    guards = BL.ledger_guards()
    other = OT.write()
    denom = DN.write()
    sec = build_sections()
    doc = copy.deepcopy(base)
    doc["schema_version"] = 11
    doc["generated_by"] = "t77"
    doc["coverage"] = BL.coverage_update(base, other, denom, sec)
    doc["incremental_provenance"] = provenance(base, guards, sec, other, denom)
    doc["club_extra_object_row"] = sec["e111"]
    doc["slot_fingerprints"] = sec["e112"]
    doc["simple_tables"] = sec["e113"]
    doc["nation_segment_grammars"] = sec["e114g"]
    doc["xref_reverse_adjudication"] = sec["e114x"]
    doc["row_frames9"] = sec["e115"]
    doc["stadium_team_l3"] = sec["e117"]
    doc["scan_tables"] = sec["scan"]
    doc["xml_denominator_coverage"] = {
        "source_task": "t78", "acceptance_ledger_entry": "E116",
        "acceptance_ledger_level": "L1", "status": "split_file",
        "path": denom["path"], "sha256": denom["sha256"], "bytes": denom["bytes"],
        "denominator": denom["count"], "carried": denom["carried"],
        "summary": sec["denom"]["per_entity"],
        "physical_coverage": sec["denom"]["physical_coverage"],
        "pointer_note": ("The full bucket ledger (1,034 per-occurrence records with evidence "
                         "refs) is a separate report file; this section carries only the "
                         "aggregates and the path+SHA-256."),
    }
    doc["pointer_artifacts"] = {
        "other_tables_schema": {"path": other["path"], "sha256": other["sha256"],
                                "bytes": other["bytes"], "table_count": other["table_count"]},
        "xml_denominator_coverage": {"path": denom["path"], "sha256": denom["sha256"],
                                     "bytes": denom["bytes"]},
        "generated_by": "t77",
        "rule": ("sections in this file never inline another report file's bulk; they carry "
                 "path + SHA-256 + aggregates only"),
    }
    return {"doc": doc, "base": base, "base_raw": base_raw, "sections": sec,
            "other": other, "denom": denom, "sources": sources, "guards": guards}
