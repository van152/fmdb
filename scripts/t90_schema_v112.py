#!/usr/bin/env python3
"""t90 - schema v11.1 -> v11.2-candidate assembly (E125 / E126 / E127).

  py -V:3.12 -I -B scripts/t90_schema_v112.py --selftest
  py -V:3.12 -I -B scripts/t90_schema_v112.py --build
  py -V:3.12 -I -B scripts/t90_schema_v112.py --verify

Additive assembly only, t87 pattern. Three new root sections are appended:
  fk_index_e125 / five_tables_l3_e126 / table9_closure_e127
and ONE existing section gets value edits (not structural):
  scan_tables -> t76c -> 27 -> archives -> {client,server} -> slots[]
  (the E126 weather R1/R2 corrections; 25 slots stay 25 slots).

reports/ is never written: the product is scratch/t90/out/schema_v112.json.
Exit codes: 0 pass / 1 check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "reports" / "club_nation_subtable_schema.json"
T81 = ROOT / "scratch" / "t81" / "out"
T83 = ROOT / "scratch" / "t83" / "out"
T85 = ROOT / "scratch" / "t85" / "out2"
OUT = ROOT / "scratch" / "t90" / "out" / "schema_v112.json"

BASE_SHA = "f811a216a8d1f72ea98dd86995924a3f55e952bc52b2b23466005dd7a7d4efed"
BASE_BYTES = 29893769
BASE_VERSION = "11.1"
NEW_VERSION = "11.2-candidate"
NEW_BY = "t90"

SOURCES = {
    "scratch/t81/out/fk_index.json":
        "28f2ef6aabc7c804c36d581c8a89f10d2dfa5ccc135a7c6fa5d410989cc83d45",
    "scratch/t81/out/rescan_fk_city.json":
        "e49642a8085021c3c1f6d24fe3d3fab2c3904ede3f73693e9cd39e45ddaf9c45",
    "scratch/t81/out/rescan_fk_t76.json":
        "305eea02d176146507d128e3b3b46e40c07fc631fa79325e874d061746d18e5f",
    "scratch/t83/out/field_map.json":
        "3a2db1496cd2c5217a03ec9f4ab5abf805b8ca727080491acc98e0157908969d",
    "scratch/t83/out/domain_stats.json":
        "0591f0d7c6777892e5741b314d091b234bb0f59566b4eb613d60f2c0160c26a9",
    "scratch/t83/out/REPORT.md":
        "fee0fa5960f0887b11519db6029a5b36f91a545ed2ee39e18e19f02b4f21f295",
    "scratch/t83/out/xref_award.json":
        "8df44b9e1bb3ad6d4ac5e5fbb8d0dfdcda4d27765362222169f060f6d5451134",
    "scratch/t83/out/xref_language.json":
        "8bc82612d9b5592b9b056c42756175f7652af0cb84d3d857dcb48d007b2868a0",
    "scratch/t83/out/xref_media.json":
        "dcc3d4a40ca9588d03f4d1318862748a4cf8269ccfa15222d18475704fbe95f9",
    "scratch/t83/out/xref_weather.json":
        "f278729c0a202ba1193231ba6c116eebae91e518ba4aa2e87cda5b1de88c5209",
    "scratch/t83/out/xref_derby.json":
        "97f2106091dd7d11bc51bb8fb37732ff5195dc58a8e541b2ae92dc482def0a10",
    "scratch/t85/out2/collection_fields.json":
        "c6f1d80d664584a2352d52b9e27c4480799198b5e80c3fb81d7cdb14e755ee8f",
    "scratch/t85/out2/wire_candidates.json":
        "05de607f7477565bd723f9a40b9341230f8b8b84826da7745481bca71f63b265",
    "scratch/t85/out2/profile_nation.json":
        "4d7114ebb696e95510e2e072dc1edc12b8badb2703d3f8e62cc185c5e5d1e7be",
}

NEW_ROOTS = ("fk_index_e125", "five_tables_l3_e126", "table9_closure_e127")
MUTABLE = ("schema_version", "generated_by", "coverage", "incremental_provenance",
           "scan_tables")
FIVE = ("award_0", "language_8", "derby_18", "weather_27", "media_7")
FIVE_META = {"award_0": (0, "award.xml"), "language_8": (8, "language.xml"),
             "derby_18": (18, "derby.xml"), "weather_27": (27, "weather.xml"),
             "media_7": (7, "media source.xml")}


class CheckFailure(Exception):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2,
                      allow_nan=False).encode("utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def json_bytes(value: Any) -> bytes:
    return norm_bytes(value) + b"\n"


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


def ledger_row(entry: dict[str, Any]) -> dict[str, Any]:
    raw = json.dumps(entry["claim"], ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return {"kind": entry["kind"], "level": entry["level"],
            "date": entry["date"], "claim_sha256": sha(raw)}


def section_digests(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {k: {"sha256": sha(norm_bytes(v)), "bytes": len(norm_bytes(v))}
            for k, v in doc.items()
            if k not in MUTABLE and k not in NEW_ROOTS}


# --------------------------------------------------------------- E125 -------
def fk_index_section(fk: dict[str, Any], city: dict[str, Any],
                     t76: dict[str, Any]) -> dict[str, Any]:
    tg = fk["targets"]
    slim = {}
    for key, v in tg.items():
        slim[key] = {"archive": v["archive"], "table": v["table"],
                     "payload_len": v["payload_len"],
                     "row_count": v["row_count"],
                     "row_count_from_header": v["row_count_from_header"],
                     "identity_width": v["identity_width"],
                     "identity_site": v.get("identity_site"),
                     "status": v["status"],
                     "unique_frame": v.get("unique_frame"),
                     "ordinal_set": v.get("ordinal_set")}
    return {
        "generated_by": NEW_BY,
        "acceptance_ledger_entry": "E125",
        "acceptance_ledger_level": "L2",
        "source_task": "t81",
        "source_artifacts": [
            {"path": "scratch/t81/out/fk_index.json", "sha256": SOURCES[
                "scratch/t81/out/fk_index.json"], "bytes": 590570,
             "rule": "pointer only; per-target window/tie_break detail stays in the artifact"},
            {"path": "scratch/t81/out/rescan_fk_city.json", "sha256": SOURCES[
                "scratch/t81/out/rescan_fk_city.json"], "bytes": 3536},
            {"path": "scratch/t81/out/rescan_fk_t76.json", "sha256": SOURCES[
                "scratch/t81/out/rescan_fk_t76.json"], "bytes": 3353},
        ],
        "doctrine": fk["identity_doctrine"],
        "counts": {"targets": len(tg), "closed": sum(
            1 for v in tg.values() if v["status"] == "closed"),
            "rollup_tables": len(fk["rollup"]), "L4": 0},
        "targets_slim": slim,
        "city_lanes": {"source": "scratch/t81/out/rescan_fk_city.json",
                       "summary": city["summary"],
                       "lanes": [{k: l[k] for k in
                                  ("target", "target_rows", "field", "offset",
                                   "entity", "source", "decision", "mapped",
                                   "grade_before", "grade_after", "sentinel",
                                   "live", "why")} for l in city["lanes"]]},
        "t76_rescan": {"source": "scratch/t81/out/rescan_fk_t76.json",
                       "summary": t76["summary"],
                       "lanes": [{k: l[k] for k in
                                  ("field", "entity", "target", "source",
                                   "decision", "mapped", "grade_before",
                                   "grade_after")} for l in t76["lanes"]]},
        "grade_policy": "E125 is an L2 acceptance; every lane above keeps its own "
                        "grade_after verbatim (L2/candidate or unmapped). No L3 claim "
                        "is made by this section.",
        "L4": 0,
    }


# --------------------------------------------------------------- E126 -------
def five_tables_section(fm: dict[str, Any], ds: dict[str, Any]) -> dict[str, Any]:
    tables = {}
    for key in FIVE:
        tid, xml = FIVE_META[key]
        blk = fm[key]
        grades = fm["summary"][key]["grades"]
        fields = []
        for f in blk["schema_fields"]:
            row = {"index": f["index"], "code": f["field"],
                   "schema_name": f.get("name"),
                   "schema_type": f.get("schema_type"),
                   "grade": f["grade"], "scope": f.get("scope")}
            for k in ("wire_loc", "wire_seq", "width", "wire_type",
                      "member_off", "client_num_off", "server_num_off",
                      "getter_fo", "setter_fo", "reader_fo", "fixup_fo",
                      "hold_reason", "note", "prior_refs"):
                if k in f:
                    row[k] = f[k]
            fields.append(row)
        tables[key] = {"table_id": tid, "xml": xml, "rows": blk["rows"],
                       "client_eq_server": blk["client_eq_server"],
                       "frame": blk.get("frame"),
                       "post_read_normalizer": blk.get("post_read_normalizer"),
                       "internal_wire_slots": blk.get("internal_wire_slots"),
                       "xml_fields": len(fields),
                       "grade_counts": grades,
                       "internal_wire_slot_count": fm["summary"][key]
                       ["internal_wire_slots"],
                       "l2_columns": ds[key],
                       "fields": fields}
    total_l3 = sum(t["grade_counts"].get("L3", 0) for t in tables.values())
    return {
        "generated_by": NEW_BY,
        "acceptance_ledger_entry": "E126",
        "acceptance_ledger_level": "L3",
        "source_task": "t83",
        "source_artifacts": [
            {"path": p, "sha256": SOURCES[p],
             "bytes": (ROOT / p).stat().st_size} for p in SOURCES
            if p.startswith("scratch/t83/")],
        "denominator": {
            "xml_fields": sum(t["xml_fields"] for t in tables.values()),
            "source": "evidence/fm24/reports/editor_schema/master.json "
                      "(MANIFEST-verified)",
            "note": fm["summary"]["xml_denominator_note"],
            "L3": total_l3,
            "held": sum(t["grade_counts"].get("held", 0) for t in tables.values()),
            "byte_gap": 0,
        },
        "grade_counts_total": fm["summary"]["total_grades"],
        "tables": tables,
        "reconciliations": fm["reconciliations"],
        "preserved_negatives": fm["preserved_negatives"],
        "integrity": fm["integrity"],
        "evidence_level": fm["evidence_level"],
        "address_convention": fm["address_convention"],
        "L4": 0,
    }


# --------------------------------------------------------------- E127 -------
def table9_section(cf: dict[str, Any], wc: dict[str, Any],
                   pn: dict[str, Any]) -> dict[str, Any]:
    chains = {}
    for key, c in wc["chains"].items():
        chains[key] = {k: c[k] for k in
                       ("archive", "path", "payload", "framing", "rows",
                        "closure_exact", "header_record_count",
                        "header_count_matches", "strict_tiling_solutions",
                        "body_len", "pair_uid_equal_all", "ordinal_chain_all",
                        "header13_hex", "footer9_hex") if k in c}
        if "uid_ladder" in c:
            lad = c["uid_ladder"]
            chains[key]["uid_ladder_head"] = lad[:5]
            chains[key]["uid_ladder_tail"] = lad[-2:]
            chains[key]["uid_ladder_len"] = len(lad)
    members = {}
    for key, m in pn["members"].items():
        members[key] = {k: m[k] for k in
                        ("archive", "path", "payload", "framing", "rows",
                         "strict_tiling_solutions", "uid_ladder_head",
                         "uid_ladder_tail", "body_len", "ordinal_lane",
                         "item_grammar") if k in m}
        members[key]["lane_domain_first32"] = m.get("lane_domain_first32", [])[:8]
    return {
        "generated_by": NEW_BY,
        "acceptance_ledger_entry": "E127",
        "acceptance_ledger_level": "L2",
        "source_task": "t85",
        "source_artifacts": [
            {"path": p, "sha256": SOURCES[p],
             "bytes": (ROOT / p).stat().st_size} for p in SOURCES
            if p.startswith("scratch/t85/")],
        "verdicts": wc["verdicts"],
        "method": wc["method"],
        "closure_claims": {
            "table_9_client": {"payload": 31956,
                               "arithmetic": "13 + 28,922 + 12*251 + 9 = 31,956",
                               "closure_exact": chains["client|table_9.dat"]
                               ["closure_exact"],
                               "strict_tiling_solutions": 1},
            "table_9_server": {"payload": 307564,
                               "closure_exact": chains["server|table_9.dat"]
                               ["closure_exact"],
                               "strict_tiling_solutions": 1},
            "table_10_client": {"payload": 24732,
                                "closure_exact": chains["client|table_10.dat"]
                                ["closure_exact"]},
            "table_10_server": {"payload": 422345,
                                "closure_exact": chains["server|table_10.dat"]
                                ["closure_exact"]},
        },
        "framing": wc["method"]["framing"],
        "chains": chains,
        "joins": wc["joins"],
        "census_drift": wc["census_drift"],
        "cross_check_t51_frozen_cursor": wc["cross_check_t51_frozen_cursor"],
        "profile_members": members,
        "collection_fields": {
            "counts": cf["counts"],
            "rule": cf["rule"],
            "nation": cf["nation"],
            "comp": cf["comp"],
            "negative_preserved": cf["negative_preserved"],
        },
        "held": {
            "item_grammar": "held_no_item_grammar (both archives, both tables; two "
                            "probing rounds, first counterexample preserved)",
            "nation_0x108": "whether table_9 is the wire home of [NATION+0x108] "
                            "remains UNPROVEN -> escalated to a static lane (t89)",
        },
        "L4": 0,
    }


# ---------------------------------------------------- weather R1/R2 edit -----
R1 = {"id": "R1_weather_wind_precip_swap",
      "prior_refs": ["t01l/E27", "t76c/E118"],
      "effect": "blk+2..6 (+0x02..+0x06) = w{b}w0..w4 (WIND); blk+7..11 "
                "(+0x07..+0x0b) = w{b}p0..w4 (PRECIPITATION)",
      "evidence_pointer": "scratch/t83/out/field_map.json#/reconciliations/0",
      "static_sites": ["WEATHER::read 0x158ba47..0x158bb79",
                       "WEATHER::get 0x158e7d1..0x158ec90",
                       "WEATHER_SEASON::get 0x158f28e/30c/780..a19",
                       "WEATHER::set 0x15902c5..0x1590b77",
                       "normalizer 0x43e7e10"],
      "grade": "L3"}
R2 = {"id": "R2_weather_sd_i16_and_dn_blk22",
      "prior_refs": ["t76c/E118"],
      "effect": "blk+0..1 (+0x00) is a 2B i16 w{b}sd (0..359); blk+22 (+0x16) is "
                "w{b}dn ('tend') with 0x64 (100) as explicit NULL sentinel",
      "evidence_pointer": "scratch/t83/out/field_map.json#/reconciliations/1",
      "static_sites": ["WEATHER_SEASON::get 0x158f3e5",
                       "WEATHER::set 0x1590498/a2f/a5b/a87"],
      "grade": "L3"}
# per block b (0..3): (sd_off, dn_off, wind_off, precip_off)
BLOCKS = {0: (3, 25, 5, 10), 1: (26, 48, 28, 33),
          2: (49, 71, 51, 56), 3: (72, 94, 74, 79)}


def weather_slots_after_e126(slots: list[dict[str, Any]],
                             expect: int | None = 25,
                             blocks: dict[int, tuple[int, int, int, int]] | None = None
                             ) -> list[dict[str, Any]]:
    """Value edits only: same slot count in and out, offsets preserved."""
    out = json.loads(json.dumps(slots))
    if expect is not None:
        require(len(out) == expect, f"weather slot count drift: {len(out)}")
    by_off = {s["offset"]: i for i, s in enumerate(out)}
    for b, (sd, dn, wind, prec) in (BLOCKS if blocks is None else blocks).items():
        # --- R2: sd becomes 2B i16, absorbing the byte E118 gave to dn
        s = out[by_off[sd]]
        s["why_before_E118"] = s.pop("why")
        s.update(field=f"w{b}sd", offset=sd, width=2, kind="i16", grade="L3",
                 why=f"R2: 2B i16 start day at blk+0..1 ({sd}..{sd + 1}). E118's 1B u8 "
                     f"split (sd@rel0 + dn@rel1) is superseded by WEATHER_SEASON::get "
                     f"0x158f3e5 / WEATHER::set 0x1590498",
                 provenance=R2)
        t = out[by_off[sd + 1]]
        require(t["field"] == f"w{b}dn", f"unexpected slot at {sd + 1}: {t['field']}")
        t["why_before_E118"] = t.pop("why")
        t.update(field=None, offset=sd + 1, width=1, kind="merged_into_prev",
                 grade="merged",
                 why=f"R2: high byte of the 2B i16 w{b}sd; not a separate field. "
                     f"E118 placed w{b}dn here by elimination - superseded.",
                 provenance=R2)
        # --- R1: swap the wind and precipitation block assignments
        wsl, psl = out[by_off[wind]], out[by_off[prec]]
        wsl["why_before_E118"] = wsl.pop("why")
        psl["why_before_E118"] = psl.pop("why")
        wsl.update(field=f"w{b}w0..w{b}w4", offset=wind, width=5, kind="i8x5",
                   grade="L3",
                   why=f"R1: WIND group at blk+2..6 ({wind}..{wind + 4}). E118 labelled "
                       f"this window 'precipitation'; corrected by WEATHER::read "
                       f"0x158ba47 and normalizer 0x43e7e10 (76 non-100 blocks = wind)",
                   provenance=R1)
        psl.update(field=f"w{b}p0..w{b}p4", offset=prec, width=5, kind="i8x5",
                   grade="L3",
                   why=f"R1: PRECIPITATION group at blk+7..11 ({prec}..{prec + 4}). "
                       f"E118 labelled this window 'wind'; corrected by the same "
                       f"quadruple static chain (67 non-100 blocks = precip)",
                   provenance=R1)
        # --- R2: dn moves to blk+22 with the 0x64 NULL sentinel
        d = out[by_off[dn]]
        require(d["field"] is None, f"expected an unassigned slot at {dn}")
        d["why_before_E118"] = d.pop("why")
        d.update(field=f"w{b}dn", offset=dn, width=1,
                 kind="i8_optional_0x64_null", grade="L3",
                 why=f"R2: day/night 'tend' at blk+22 ({dn}); 0x64 (100) is an explicit "
                     f"NULL sentinel. E118 left this byte unassigned (it read it as a "
                     f"row-level {{0,100}} property repeated per block).",
                 provenance=R2)
    return out


# ---------------------------------------------------------------- assembly ---
def patch_doc(pre: dict[str, Any], sec125: dict[str, Any],
              sec126: dict[str, Any], sec127: dict[str, Any],
              ledger: dict[str, Any]) -> dict[str, Any]:
    doc = json.loads(json.dumps(pre))
    doc["schema_version"] = NEW_VERSION
    doc["generated_by"] = NEW_BY
    doc["fk_index_e125"] = sec125
    doc["five_tables_l3_e126"] = sec126
    doc["table9_closure_e127"] = sec127

    # --- the single structural-preserving value edit: weather slots
    arch = doc["scan_tables"]["t76c"]["27"]["archives"]
    for k in ("client", "server"):
        before = len(arch[k]["slots"])
        arch[k]["slots"] = weather_slots_after_e126(arch[k]["slots"])
        require(len(arch[k]["slots"]) == before == 25,
                f"weather {k} slot count changed")
    doc["scan_tables"]["acceptance_ledger_entries"] = [
        "E120", "E118", "E126"]
    doc["scan_tables"]["t90_weather_value_edit"] = {
        "rule": "E126 R1/R2 applied as VALUE edits on scan_tables/t76c/27 slots; "
                "slot count (25) and offset set unchanged, structure untouched",
        "R1": R1, "R2": R2,
        "supersedes": "t76c/E118 wind/precip assignment and the 1B sd + 1B dn split",
        "e118_evidence_preserved": "every edited slot keeps its original rationale "
                                  "under `why_before_E118`; nothing is deleted",
    }

    cov = doc["coverage"]
    cov["five_tables_E126"] = {
        "xml_fields": sec126["denominator"]["xml_fields"],
        "L3": sec126["denominator"]["L3"],
        "held": sec126["denominator"]["held"],
        "byte_gap": 0,
        "denominator_source": "evidence/fm24/reports/editor_schema/master.json "
                              "(NOT the 1,034-occurrence club/comp/nation file)",
        "note": "these five tables live outside reports/xml_denominator_coverage.json; "
                "their 188-field denominator is counted directly from master.json",
    }
    cov["fk_index_E125"] = {
        "targets": sec125["counts"]["targets"],
        "closed": sec125["counts"]["closed"],
        "city_lanes_mapped": sum(1 for l in sec125["city_lanes"]["lanes"]
                                 if l.get("mapped")),
        "grade": "L2",
        "note": "variable-table FK ordinal/UID domain index; per-lane grades kept "
                "verbatim (L2/candidate or unmapped)",
    }
    cov["table9_closure_E127"] = {
        "table_9_client_bytes": 31956,
        "table_9_server_bytes": 307564,
        "closure": "13 + 28,922 + 12*251 + 9 = 31,956 (client)",
        "strict_tiling_solutions": 1,
        "item_grammar": "held_no_item_grammar",
        "grade": "L2",
        "note": "variable-member framing (13B header + 12B trailer + 9B footer) "
                "proven for t9/t10; no L3 field claim",
    }
    cov["xml_denominator_pointer_v112"] = {
        "note": "E116 numbers stand unchanged in the split file; t90's re-bucket is "
                "a candidate in scratch/t90/out/denominator_v2.json, not a report edit",
        "denominator": 1034, "carried": 110,
        "re_routed_table_45": 117,
        "unresolved_wire_slot_before": 277,
        "unresolved_wire_slot_after": 160,
    }
    cov["L4"] = 0

    prov = doc["incremental_provenance"]
    for eid in ("E125", "E126", "E127"):
        prov["acceptance_ledger_entries"][eid] = ledger_row(ledger[eid])
    prov["t90_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level id, kind, level, date and canonical claim "
                       "SHA-256; no live full-file hash pin",
        "guarded_entries": ["E125", "E126", "E127"],
        "entries": [{"id": e, **ledger_row(ledger[e])} for e in
                    ("E125", "E126", "E127")],
        "out_of_scope_note": "E124 (t87) stays as pinned; E128+ belong to the next lane",
    }
    prov["t90_volume_policy"] = {
        "main_schema_keeps": ["per-field grade + wire_loc + provenance pointer",
                              "counters", "one source pointer per artifact"],
        "bulk_stays_out": "the t83 214KB field_map per-field domains, the t81 590KB "
                          "fk_index per-target windows and the t85 75KB lane domains "
                          "stay in their own artifacts",
        "split_files_untouched": ["reports/other_tables_schema.json",
                                  "reports/xml_denominator_coverage.json"],
    }
    prov["t90_additive_rule"] = (
        "v11.1 sections are value-identical after the patch except scan_tables "
        "(weather slots only, 25 slots in / 25 out, offsets preserved); only "
        "schema_version, generated_by, coverage and incremental_provenance change, "
        "plus the three new root sections")
    return doc


def build() -> int:
    base_raw = BASE.read_bytes()
    require(sha(base_raw) == BASE_SHA, f"v11.1 pin mismatch: {sha(base_raw)}")
    require(len(base_raw) == BASE_BYTES, "v11.1 byte count mismatch")
    for p, h in SOURCES.items():
        require(sha((ROOT / p).read_bytes()) == h, f"source pin mismatch: {p}")
    pre = json.loads(base_raw)
    require(pre["schema_version"] == BASE_VERSION, "baseline is not v11.1")
    require(len(pre) == 37, f"baseline root key count {len(pre)} != 37")

    ledger = {e["id"]: e for e in read_json(ROOT / "scratch/t01/LEDGER.json")["entries"]}
    for eid, lvl in (("E125", "L2"), ("E126", "L3"), ("E127", "L2")):
        require(ledger[eid]["level"] == lvl, f"{eid} ledger level drift")

    sec125 = fk_index_section(read_json(T81 / "fk_index.json"),
                              read_json(T81 / "rescan_fk_city.json"),
                              read_json(T81 / "rescan_fk_t76.json"))
    sec126 = five_tables_section(read_json(T83 / "field_map.json"),
                                 read_json(T83 / "domain_stats.json"))
    sec127 = table9_section(read_json(T85 / "collection_fields.json"),
                            read_json(T85 / "wire_candidates.json"),
                            read_json(T85 / "profile_nation.json"))
    doc = patch_doc(pre, sec125, sec126, sec127, ledger)

    # additive guard
    removed = [k for k in pre if k not in doc]
    changed = [k for k in pre if k in doc and doc[k] != pre[k]
               and k not in MUTABLE]
    require(not removed, f"root keys removed: {removed}")
    require(not changed, f"non-mutable roots changed: {changed}")
    require(len(doc) == 37 + len(NEW_ROOTS), f"root count {len(doc)}")
    doc["incremental_provenance"]["t90_assembly_guard"] = {
        "baseline": {"schema_version": BASE_VERSION, "sha256": BASE_SHA,
                     "bytes": BASE_BYTES, "root_keys": 37},
        "product": {"schema_version": NEW_VERSION, "root_keys": len(doc)},
        "untouched_root_digests": section_digests(pre),
        "mutable_roots": list(MUTABLE),
        "new_roots": list(NEW_ROOTS),
        "structural_edits": ["scan_tables/t76c/27/archives/{client,server}/slots "
                             "(values only, 25 slots preserved)"],
        "reports_touched": [],
        "L4": 0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(json_bytes(doc))
    print(f"wrote {OUT.relative_to(ROOT)}  {OUT.stat().st_size:,} B")
    print("root keys", len(doc), "| new", len(NEW_ROOTS))
    print("five tables L3", doc["five_tables_l3_e126"]["denominator"]["L3"])
    print("fk targets", doc["fk_index_e125"]["counts"]["targets"])
    return 0


def verify() -> int:
    doc = read_json(OUT)
    pre = json.loads(BASE.read_bytes())
    fails: list[str] = []

    def ck(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    ck("baseline pin", sha(BASE.read_bytes()) == BASE_SHA)
    ck("version", doc["schema_version"] == NEW_VERSION and doc["generated_by"] == NEW_BY)
    ck("root keys 37+3", len(doc) == 40, str(len(doc)))
    ck("no extra root invented", set(doc) - set(pre) == set(NEW_ROOTS),
       str(sorted(set(doc) - set(pre))))
    ck("no root removed", set(pre) <= set(doc))
    guard = doc["incremental_provenance"]["t90_assembly_guard"]["untouched_root_digests"]
    bad = [k for k, v in guard.items()
           if sha(norm_bytes(doc[k])) != v["sha256"]]
    ck("untouched roots byte-identical", not bad, str(bad))

    # ---- every diff traces to a source out file
    s125 = doc["fk_index_e125"]
    ck("E125 pointer+grade", s125["acceptance_ledger_entry"] == "E125"
       and s125["acceptance_ledger_level"] == "L2")
    fk = read_json(T81 / "fk_index.json")
    ck("E125 targets match source", set(s125["targets_slim"]) == set(fk["targets"]))
    ck("E125 target rows match source",
       all(s125["targets_slim"][k]["row_count"] == fk["targets"][k]["row_count"]
           for k in fk["targets"]))
    city = read_json(T81 / "rescan_fk_city.json")
    ck("E125 city lanes match source",
       [l["field"] for l in s125["city_lanes"]["lanes"]]
       == [l["field"] for l in city["lanes"]])

    s126 = doc["five_tables_l3_e126"]
    ck("E126 pointer+grade", s126["acceptance_ledger_entry"] == "E126"
       and s126["acceptance_ledger_level"] == "L3")
    fm = read_json(T83 / "field_map.json")
    ck("E126 five tables present", set(s126["tables"]) == set(FIVE))
    ck("E126 field counts match source",
       all(s126["tables"][k]["xml_fields"] == len(fm[k]["schema_fields"])
           for k in FIVE),
       str(sum(s126["tables"][k]["xml_fields"] for k in FIVE)))
    ck("E126 L3 total 152", s126["denominator"]["L3"] == 152,
       str(s126["denominator"]["L3"]))
    ck("E126 codes match source",
       all([f["code"] for f in s126["tables"][k]["fields"]]
           == [f["field"] for f in fm[k]["schema_fields"]] for k in FIVE))
    ck("E126 reconciliations R1..R5", [r["id"] for r in s126["reconciliations"]]
       == [r["id"] for r in fm["reconciliations"]], str(len(s126["reconciliations"])))

    s127 = doc["table9_closure_e127"]
    ck("E127 pointer+grade", s127["acceptance_ledger_entry"] == "E127"
       and s127["acceptance_ledger_level"] == "L2")
    wc = read_json(T85 / "wire_candidates.json")
    ck("E127 table_9 client payload", s127["closure_claims"]["table_9_client"]
       ["payload"] == wc["chains"]["client|table_9.dat"]["payload"] == 31956)
    ck("E127 arithmetic", 13 + 28922 + 12 * 251 + 9 == 31956)
    ck("E127 item grammar held",
       s127["profile_members"]["client|table_9"]["item_grammar"]["verdict"]
       == "held_no_item_grammar")

    # ---- weather R1/R2 value edit
    for k in ("client", "server"):
        slots = doc["scan_tables"]["t76c"]["27"]["archives"][k]["slots"]
        pre_slots = pre["scan_tables"]["t76c"]["27"]["archives"][k]["slots"]
        ck(f"weather {k} slot count 25", len(slots) == len(pre_slots) == 25)
        ck(f"weather {k} offsets preserved",
           [s["offset"] for s in slots] == [s["offset"] for s in pre_slots])
        w0 = next(s for s in slots if s["offset"] == 5)
        p0 = next(s for s in slots if s["offset"] == 10)
        sd = next(s for s in slots if s["offset"] == 3)
        dn = next(s for s in slots if s["offset"] == 25)
        ck(f"weather {k} R1 wind@5", w0["field"] == "w0w0..w0w4"
           and w0["provenance"]["id"].startswith("R1"))
        ck(f"weather {k} R1 precip@10", p0["field"] == "w0p0..w0p4")
        ck(f"weather {k} R2 sd 2B", sd["width"] == 2 and sd["field"] == "w0sd")
        ck(f"weather {k} R2 dn@25", dn["field"] == "w0dn"
           and "0x64" in dn["why"])
        ck(f"weather {k} E118 rationale preserved",
           all("why_before_E118" in s for s in slots if s.get("provenance")))

    ck("no report written by t90",
       doc["incremental_provenance"]["t90_assembly_guard"]["reports_touched"] == [])
    ck("L4 == 0", s125["L4"] == 0 and s126["L4"] == 0 and s127["L4"] == 0
       and doc["coverage"]["L4"] == 0)
    print(f"\n{len(fails)} failure(s)")
    return 0 if not fails else 1


def selftest() -> int:
    fails = 0

    def ck(name: str, ok: bool) -> None:
        nonlocal fails
        print(("PASS " if ok else "FAIL ") + name)
        fails += 0 if ok else 1

    ck("sha of empty", sha(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b93"
                              "4ca495991b7852b855")
    ck("norm_bytes stable", sha(norm_bytes({"a": 1})) == sha(norm_bytes({"a": 1})))
    ck("norm_bytes key-order sensitive", sha(norm_bytes({"a": 1, "b": 2}))
       != sha(norm_bytes({"b": 2, "a": 1})))
    toy = [{"field": "w0sd", "offset": 3, "width": 1, "kind": "u8",
            "grade": "L2", "why": "x"},
           {"field": "w0dn", "offset": 4, "width": 1, "kind": "u8",
            "grade": "candidate", "why": "y"},
           {"field": "w0p0..w0p4", "offset": 5, "width": 5, "kind": "u8x5",
            "grade": "L2", "why": "z"},
           {"field": "w0w0..w0w4", "offset": 10, "width": 5, "kind": "u8x5",
            "grade": "L2", "why": "q"},
           {"field": None, "offset": 25, "width": 1, "kind": "u8",
            "grade": "unassigned", "why": "u"}]
    got = weather_slots_after_e126(toy, expect=None,
                                   blocks={0: (3, 25, 5, 10)})
    ck("toy R1 swap", got[2]["field"] == "w0w0..w0w4"
       and got[3]["field"] == "w0p0..w0p4")
    ck("toy R2 sd 2B", got[0]["width"] == 2 and got[1]["grade"] == "merged")
    ck("toy R2 dn@25", got[4]["field"] == "w0dn")
    ck("toy length preserved", len(got) == len(toy))
    ck("toy originals kept", all("why_before_E118" in s for s in got))
    print(f"\n{8 - fails}/8 selftest checks")
    return 0 if not fails else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if not (a.build or a.verify or a.selftest):
        ap.print_help()
        return 2
    try:
        if a.selftest:
            return selftest()
        if a.build:
            return build()
        return verify()
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
