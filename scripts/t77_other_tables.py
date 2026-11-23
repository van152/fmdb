"""t77 builder: reports/other_tables_schema.json — the 13 non-main-table slot verdicts.

Extracted from the main schema on purpose (size governance): t73 (4 tables) +
t76a (1) + t76c (4) + t74 (4 row frames only; t76b dropped so award/language/
media/team carry frames but no slot map).
"""
from __future__ import annotations

from typing import Any

from t77_common import ROOT, artifacts, json_bytes, read_json, sha

T73 = ROOT / "scratch" / "t73" / "out"
T74 = ROOT / "scratch" / "t74" / "out"
T76A = ROOT / "scratch" / "t76a" / "out"
T76C = ROOT / "scratch" / "t76c" / "out"

TABLE_ENTITY = {0: "award", 2: "city", 5: "continent", 7: "media", 8: "language",
                18: "derby", 19: "region", 21: "stadium", 24: "team", 27: "weather",
                41: "currency", 47: "local_region", 56: "agreement"}


def _t73_tables() -> dict[str, Any]:
    frames = read_json(T73 / "frames.json")
    out = {}
    for tid in (2, 5, 19, 41):
        entry: dict[str, Any] = {"table": tid, "entity": TABLE_ENTITY[tid],
                                 "source_task": "t73", "acceptance_ledger_entry": "E113",
                                 "acceptance_ledger_level": "L2", "archives": {}}
        for arch in ("client", "server"):
            key = f"{arch}_{tid}"
            fr = frames["out"].get(key)
            p = T73 / f"slots_{arch}_{tid}.json"
            rec = {"frame": fr, "slots": [], "status": "pending",
                   "reason": f"missing {p.name}"}
            if p.exists():
                d = read_json(p)
                rec = {
                    "status": d["status"],
                    "frame": d["frame"],
                    "closure": d.get("closure"),
                    "payload_len": d["payload_len"],
                    "payload_sha256": d["payload_sha256"],
                    "alias_group": d.get("alias_group"),
                    "header_origin_data_unique": d.get("header_origin_data_unique"),
                    "slots": d["slots"],
                    "offset_map": d.get("offset_map"),
                    "frozen_check": {k: d["frozen_check"][k]
                                     for k in ("checked", "ok")} if d.get("frozen_check") else None,
                    "held": d.get("held"),
                }
            entry["archives"][arch] = rec
        entry["slot_count"] = {a: len(v["slots"]) for a, v in entry["archives"].items()}
        out[str(tid)] = entry
    return out


def _t76a_tables() -> dict[str, Any]:
    out = {}
    for arch in ("client", "server"):
        p = T76A / f"slots_{arch}_21.json"
        d = read_json(p)
        out[arch] = {
            "status": d["status"], "frame": d["frame"], "walk": d["walk"],
            "slots": d["slots"], "offset_map": d.get("offset_map"),
            "grade_summary": d["grade_summary"], "coverage": d["coverage"],
            "anchors": d.get("anchors"), "held": d.get("held"),
            "not_in_schema": d.get("not_in_schema"),
            "payload_sha256": d["payload_sha256"],
        }
    return {"table": 21, "entity": "stadium", "source_task": "t76a",
            "acceptance_ledger_entry": "E120", "acceptance_ledger_level": "L2",
            "archives": out,
            "slot_count": {a: len(v["slots"]) for a, v in out.items()}}


def _t76c_tables() -> dict[str, Any]:
    out = {}
    for tid in (18, 27, 47, 56):
        entry = {"table": tid, "entity": TABLE_ENTITY[tid], "source_task": "t76c",
                 "acceptance_ledger_entry": "E118", "acceptance_ledger_level": "L2",
                 "archives": {}}
        for arch in ("client", "server"):
            p = T76C / f"slots_{arch}_{tid}.json"
            d = read_json(p)
            entry["archives"][arch] = {
                "status": d["status"], "t74_frame": d["t74_frame"], "walk": d["walk"],
                "identity": d["identity"], "slots": d["slots"],
                "unresolved": d.get("unresolved", []),
                "payload_sha256": d.get("payload_sha256"),
            }
        entry["slot_count"] = {a: len(v["slots"]) for a, v in entry["archives"].items()}
        out[str(tid)] = entry
    return out


def _t74_frames_only() -> dict[str, Any]:
    d = read_json(T74 / "frames.json")
    out = {}
    for tid in (0, 7, 8, 24):
        t = d["tables"][str(tid)]
        rec = {"table": tid, "entity": TABLE_ENTITY[tid], "source_task": "t74",
               "acceptance_ledger_entry": "E115", "acceptance_ledger_level": "L2",
               "row_frame": {}, "slots": None,
               "slots_status": ("pending:t76b(由 t83 接收)" if tid in (0, 7, 8)
                                 else "see main schema #/stadium_team_l3/team_24 (E117)"),
               "slots_note": (("t76b (award/language/media) hit three walls with zero delivery "
                               "and was dropped; these tables carry t74 row frames only. "
                               "t83 owns their slot maps.")
                              if tid in (0, 7, 8) else
                              ("team/table_24 slot semantics were delivered by E117 (t79) and "
                               "live in the main schema's stadium_team_l3 section; this file "
                               "keeps only its t74 row frame."))}
        for arch in ("client", "server"):
            a = t["archives"].get(arch)
            if a is None:
                continue
            if a.get("status") == "absent":
                rec["row_frame"][arch] = {"status": "absent", "reason": a.get("reason")}
                continue
            rec["row_frame"][arch] = {
                "status": "closed", "header": a["header"], "footer": a["footer"],
                "count": a["count"], "model": a["model"], "stride": a.get("stride"),
                "row_len_range": a.get("row_len_range"), "row_rule": a["row_rule"],
                "identity": a.get("identity"), "closure": a["closure"],
                "payload_len": a["payload_len"], "payload_sha256": a["payload_sha256"],
            }
        out[str(tid)] = rec
    return out


def build() -> dict[str, Any]:
    t73 = _t73_tables()
    t76a = _t76a_tables()
    t76c = _t76c_tables()
    t74 = _t74_frames_only()
    tables = {}
    for group in (t73, t76c, t74):
        for k, v in group.items():
            tables[k] = v
    tables["21"] = t76a
    order = [2, 5, 19, 41, 21, 18, 27, 47, 56, 0, 7, 8, 24]
    tables = {str(t): tables[str(t)] for t in order}
    return {
        "schema_id": "fm24.other_tables_schema",
        "schema_version": 1,
        "generated_by": "t77",
        "parent_schema": {
            "path": "reports/club_nation_subtable_schema.json",
            "schema_version": 11,
            "note": ("The main schema keeps the three main tables, the eight numbered "
                     "club subtables, CLUB_LINK and the r2/r3 sections. This file carries "
                     "the 13 non-main-table verdicts to keep the main JSON tractable."),
        },
        "evidence_grade_policy": ("Only accepted source-ledger grades appear in `slots`. "
                                  "candidate/unmapped/unassigned rows are carried verbatim "
                                  "from the accepted artifacts and are not conclusions. L4=0."),
        "table_count": len(tables),
        "table_order": order,
        "table_ids": {str(t): TABLE_ENTITY[t] for t in order},
        "coverage_note": {
            "t73": "city/continent/region/currency — 8/8 archives closed, 10 distinct L2 slots",
            "t76a": "stadium — 12 client / 47 server slots, 0 uncovered bytes both archives",
            "t76c": "derby/weather/local_region/agreement — 8/8 archives closed",
            "t74": "award/media/language/team — row frames only (t76b dropped -> t83)",
        },
        "tables": tables,
        "source_artifacts": artifacts(
            "scratch/t73/out/frames.json", "scratch/t73/out/verify.py",
            "scratch/t76a/out/slots_client_21.json", "scratch/t76a/out/slots_server_21.json",
            "scratch/t76c/out/verify.py", "scratch/t74/out/frames.json"),
        "L4": 0,
    }


def write() -> dict[str, Any]:
    doc = build()
    raw = json_bytes(doc)
    (ROOT / "reports" / "other_tables_schema.json").write_bytes(raw)
    return {"path": "reports/other_tables_schema.json", "sha256": sha(raw), "bytes": len(raw),
            "table_count": doc["table_count"]}
