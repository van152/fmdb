"""t77 section builders, part 2: E114 (t75), E115 (t74), E116 (t78) denominator,
E117 (t79) and E118/E120 (t76c/t76a) scan tables.
"""
from __future__ import annotations

from typing import Any

from t77_common import ROOT, artifacts, read_json

T74 = ROOT / "scratch" / "t74" / "out"
T75 = ROOT / "scratch" / "t75" / "out"
T76A = ROOT / "scratch" / "t76a" / "out"
T76C = ROOT / "scratch" / "t76c" / "out"
T78 = ROOT / "scratch" / "t78" / "out"
T79 = ROOT / "scratch" / "t79" / "out"


def nation_segment_grammars() -> dict[str, Any]:
    fm = read_json(T75 / "field_map_r3.json")
    xr = read_json(T75 / "xref_reverse.json")
    grams = []
    for g in fm["nation_physical_grammar"]:
        esc = next((e for e in xr["nation_escalations"]
                    if e["escalation"]["slot"] == g["slot"]), None)
        row = {"slot": g["slot"], "grade": g["grade"], "prior_ids": g["prior_ids"]}
        if esc:
            row.update({
                "collection": esc["escalation"]["collection"],
                "grammar": esc["grammar"],
                "count_format": esc["count_format"],
                "reader_site": esc["reader_site"],
                "object_displacement": esc["object_displacement"],
                "server_rows": esc["archives"]["server"]["rows"],
                "server_bytes": esc["archives"]["server"]["bytes"],
                "server_items": esc["archives"]["server"].get("items"),
                "server_nonempty": esc["archives"]["server"].get("nonempty"),
                "client_rows": esc["archives"]["client"]["rows"],
                "width_histogram_distinct": len(esc["archives"]["server"]["width_histogram"]),
            })
        grams.append(row)
    return {
        "source_task": "t75",
        "acceptance_ledger_entry": "E114",
        "acceptance_ledger_level": "L3",
        "status": "nation_segment_grammar_layer_closed",
        "scope": ("wire-first reverse lookup: 10 t72 escalations (nation inner-item grammars) "
                  "first, then 99 club/comp/nation unnamed/held outer slots adjudicated"),
        "grammars": grams,
        "grammar_count": len(grams),
        "closed_grammars": sum(1 for g in grams if g["grade"] == "L3_physical_only"),
        "held_no_items": [g["slot"] for g in grams if g["grade"] == "held_no_items"],
        "ledger_claims": {
            "slot_4": "Nftb i16 count, u8 tag + 4x len-prefixed strings + date + 4 lanes, "
                      "1 row / 7 items 46-54B",
            "slot_11": "Ntxr 221 rows / 1,899 items tag2 25B — matches E87 frozen 1,899",
            "slot_12": "u32 count 164 rows / 27,178 items ordered-map key i32 + 2 packed dates; "
                       "container key NOT business ID",
            "slot_13": "19/58 loop 1+4+4+1+1+1+1+1",
            "slot_23": "Nlns i8 4+1, 237/492",
            "slot_24": "Nefr 5x4+date+date, 43/214",
            "slot_25": "Nnfr shares Nefr reader, 20/63 all-null kept static",
            "slot_26": "Nagr 4+date+date, 126/162",
            "slot_2/slot_3": "0 real items -> held",
        },
        "dual_archive_identity": "A/B/C/D four segments 251/251 dual-archive count+payload match",
        "prior_lanes_reverified": {
            "count": len(fm["nation_existing_named_server_domain_reverified"]),
            "note": ("19 existing named sub-slots of A/B/C/D re-verified against live target "
                     "identity (t5/8/10/19/56); lang 492/492 ordinal hits but 488 UID lookups "
                     "all wrong-pointing; Nnfr/nfrc 63 all-null; Nlns/perc 17/91 "
                     "raw!=reader-rewritten-100 preserved"),
        },
        "boundary": "new named L3 = 0 — remaining slots lack resolver+getter pairing",
        "L4": fm["L4"],
        "source_artifacts": artifacts("scratch/t75/out/xref_reverse.json",
                                      "scratch/t75/out/field_map_r3.json",
                                      "scratch/t75/out/verify.py",
                                      "scratch/t75/out/REPORT.md",
                                      "scratch/t75/out/DONE.md"),
        "pointer": "scratch/t75/out/xref_reverse.json (1.3 MB reader fragments + item replays)",
    }


def xref_reverse_adjudication() -> dict[str, Any]:
    fm = read_json(T75 / "field_map_r3.json")
    xr = read_json(T75 / "xref_reverse.json")
    by_table: dict[str, dict[str, Any]] = {}
    for name in ("nation", "club", "comp"):
        rows = fm[name]
        held = [r for r in rows if r["grade"] == "held"]
        by_table[name] = {
            "adjudicated": len(rows),
            "held": len(held),
            "held_slots": [r["slot"] for r in held],
            "held_with_counterexample": sum(1 for r in held if r.get("first_counterexample")),
        }
    return {
        "source_task": "t75",
        "acceptance_ledger_entry": "E114",
        "acceptance_ledger_level": "L3",
        "status": "all_99_slots_adjudicated_zero_new_named_L3",
        "totals": {"adjudicated": sum(v["adjudicated"] for v in by_table.values()),
                   "held": sum(v["held"] for v in by_table.values()),
                   "new_named_L3": fm["new_named_L3"]},
        "by_table": by_table,
        "held_counts_declared": fm["held_counts"],
        "club_comp_findings": {
            "club_ref_e0": "reproduces E106 nation resolver 26,587 live full-hit, no scoped 4CC -> held",
            "club_raw168_comp_m152": ("true t21 ordinal lanes (84,259 & 7,047 full hit, "
                                      "wrong-UID all wrong-pointing) but no resolver+4CC "
                                      "pairing -> cannot name Stadium, held"),
            "comp_Ccre_cosr": "exact gates found but not in frozen field_codes -> not promoted",
            "slot_12_slot_13": "new physical lanes profiled unnamed",
        },
        "excluded_t71_4cc": {"count": len(xr["excluded_t71_4cc"]),
                             "note": "24 E111 4CC excluded from this scan by design"},
        "negative_evidence": {
            "t72_negative_notes_verbatim": xr["t72_negative_notes_verbatim"],
            "edsc_control": xr["edsc_control"]["conclusion_verbatim"],
        },
        "boundary": ("remaining slots lack resolver+getter pairing; the un-named residue is "
                     "documented as that gap, the precise target for editor-runtime (t02) if authorized"),
        "L4": xr["L4"],
        "source_artifacts": artifacts("scratch/t75/out/field_map_r3.json",
                                      "scratch/t75/out/verify.py",
                                      "scratch/t75/out/REPORT.md"),
    }


def row_frames9() -> dict[str, Any]:
    d = read_json(T74 / "frames.json")
    sens = read_json(T74 / "sensitivity.json")
    rows = []
    for tid in sorted(d["tables"], key=int):
        t = d["tables"][tid]
        for arch in ("client", "server"):
            a = t["archives"].get(arch)
            if a is None:
                continue
            if a.get("status") == "absent":
                rows.append({"table": int(tid), "entity": t["entity"], "archive": arch,
                             "status": "absent", "reason": a.get("reason")})
                continue
            ident = a.get("identity") or {}
            rows.append({
                "table": int(tid), "entity": t["entity"], "archive": arch,
                "status": "closed",
                "header": a["header"], "footer": a["footer"], "count": a["count"],
                "model": a["model"], "stride": a.get("stride"),
                "row_len_range": a.get("row_len_range"),
                "identity_width": ident.get("width"),
                "identity_anchor": ident.get("anchor"),
                "identity_layout": ident.get("layout"),
                "closure": a["closure"],
                "payload_len": a["payload_len"],
                "payload_sha256": a["payload_sha256"],
                "verified": a.get("verified"),
            })
    return {
        "source_task": "t74",
        "acceptance_ledger_entry": "E115",
        "acceptance_ledger_level": "L2",
        "status": "closed_17_of_17_archives_zero_escalate",
        "scope": d["scope"],
        "identity_doctrine": d["identity_doctrine"],
        "tables_verified": d["summary"]["tables_verified"],
        "archives_verified": len(d["summary"]["archives_verified"]),
        "archives_closed": sum(1 for r in rows if r["status"] == "closed"),
        "escalations": d["summary"]["escalations"],
        "upstream_conflicts": d["summary"]["upstream_conflicts"],
        "double_archive_identical_payloads": d["summary"]["double_archive_identical_payloads"],
        "double_archive_different": d["summary"]["double_archive_different"],
        "frames": rows,
        "sensitivity": {"keys": sorted(sens.keys()),
                        "note": "per (table, archive) identity-width x footer matrix"},
        "grammars": {
            "agreement": "13B fixed x6",
            "award": "77B fixed x3545",
            "stadium": "client 38B / server 181B x48413 (server extra = per-row 143B block)",
            "language": "[len][UTF-8 name][17B][13B id] suffix 30B, rdui_suffix@17 126/126",
            "weather": "[len][name][95B numeric mid][13B id]",
            "derby": "k-lstr + (const-4k) numeric + 13B id, k in {2,4}, const 65 client / 71 server",
            "lcrg": "41+5k rows {41..76}",
            "media": "identity-DP, server +7B per row before identity",
            "team": "server-only 84,507 rows variable 86..666B; client entry absent",
        },
        "L4": 0,
        "source_artifacts": artifacts("scratch/t74/out/frames.json",
                                      "scratch/t74/out/sensitivity.json",
                                      "scratch/t74/out/verify.py",
                                      "scratch/t74/out/REPORT.md",
                                      "scratch/t74/out/DONE.md"),
        "pointer": "scratch/t74/out/row_widths_*.csv (per-table width histograms)",
    }


def scan_tables() -> dict[str, Any]:
    c21 = read_json(T76A / "slots_client_21.json")
    s21 = read_json(T76A / "slots_server_21.json")
    ver = read_json(T76A / "verify.json")
    stadium = {
        "entity": "stadium", "table": 21,
        "acceptance_ledger_entry": "E120",
        "status": c21["status"],
        "frame_source": c21["frame_source"],
        "client": {"frame": c21["frame"], "slots": c21["slots"],
                   "grade_summary": c21["grade_summary"],
                   "coverage": c21["coverage"],
                   "anchors_checked": c21["anchors"]["checked"],
                   "anchors_ok": c21["anchors"]["ok"],
                   "not_in_schema": c21["not_in_schema"]},
        "server": {"frame": s21["frame"], "slots": s21["slots"],
                   "grade_summary": s21["grade_summary"],
                   "coverage": s21["coverage"],
                   "server_only_segment": s21["server_only_segment"],
                   "shared_tail": s21["shared_tail"],
                   "not_in_schema": s21["not_in_schema"]},
        "slot_counts": {"client": len(c21["slots"]), "server": len(s21["slots"])},
        "verify_checks": len(ver["checks"]),
        "verify_failed": sum(1 for c in ver["checks"] if not c["pass"]),
        "structural": [
            "server 143B differential = server-only prefix segment; server[143:181] == "
            "client[0:38] byte-identical on 48,413/48,413 rows",
            "rdui@25 label ambiguity resolved: @25 is row_ordinal (== arange 48,413), "
            "@33 is rdui_raw (== duni, exe-suppressed arm)",
            "new intermediate grade L2_structural for capacity family "
            "Scas<=Sscy<=Scpy<=Secy (98.70% on 5,065 non-zero rows; 66 counterexamples kept)",
        ],
        "honest_downgrades": ["Sowi candidate (club/team domain ambiguity)",
                              "5 date slots candidate (business order only 77.1%)",
                              "8 pitch slots data-undecidable",
                              "flags u16 bit-order data-undecidable"],
        "source_artifacts": artifacts("scratch/t76a/out/slots_client_21.json",
                                      "scratch/t76a/out/slots_server_21.json",
                                      "scratch/t76a/out/verify.json",
                                      "scratch/t76a/out/verify.py",
                                      "scratch/t76a/out/REPORT.md",
                                      "scratch/t76a/out/DONE.md"),
    }

    t76c = {}
    for tid, entity in ((18, "derby"), (27, "weather"), (47, "local_region"),
                        (56, "agreement")):
        per_arch = {}
        for arch in ("client", "server"):
            p = T76C / f"slots_{arch}_{tid}.json"
            if not p.exists():
                per_arch[arch] = {"status": "pending", "reason": f"missing {p.name}"}
                continue
            d = read_json(p)
            per_arch[arch] = {
                "status": d["status"], "entity": d.get("entity"),
                "t74_frame": d["t74_frame"], "walk": d["walk"],
                "identity": d["identity"], "slots": d["slots"],
                "unresolved": d.get("unresolved", []),
                "slot_count": len(d["slots"]),
                "payload_sha256": d.get("payload_sha256"),
            }
        t76c[str(tid)] = {"entity": entity, "table": tid,
                          "acceptance_ledger_entry": "E118", "archives": per_arch}
    return {
        "source_task": "t76a+t76c",
        "acceptance_ledger_entries": ["E120", "E118"],
        "acceptance_ledger_level": "L2",
        "status": "closed_10_of_10_archives",
        "scope": ("batch scan lane wave 2: stadium (t76a) + derby/weather/local_region/"
                  "agreement (t76c); award/language/media NOT included"),
        "pending": {"t76b": "award/language/media — three-wall zero-delivery, dropped; "
                            "absorbed by t83 (not in this version)"},
        "stadium": stadium,
        "t76c": t76c,
        "structural_findings": [
            "derby dual-archive 6-byte row difference = exactly the 3 non-client schema "
            "fields D1tw/D1td/D1tl (three u16, born/die together)",
            "weather 95B mid-block = 3 + 4x23 proven by discriminant: the only {0,100} "
            "column lands at 3+23b+22; rival 3+4x22+4 collapses 1519->583 of 4008",
        ],
        "slot_totals": {
            "derby": "11 slots",
            "weather": "4 groups per block (4x23B blocks)",
            "lcrg": "2 groups",
            "agreement": "identity-only (6 rows, 13B fixed)",
        },
        "L4": 0,
        "source_artifacts": artifacts(
            "scratch/t76c/out/slots_client_18.json", "scratch/t76c/out/slots_server_18.json",
            "scratch/t76c/out/slots_client_27.json", "scratch/t76c/out/slots_server_27.json",
            "scratch/t76c/out/slots_client_47.json", "scratch/t76c/out/slots_server_47.json",
            "scratch/t76c/out/slots_client_56.json", "scratch/t76c/out/slots_server_56.json",
            "scratch/t76c/out/verify.py", "scratch/t76c/out/REPORT.md",
            "scratch/t76c/out/DONE.md"),
        "pointer": "reports/other_tables_schema.json#/tables (per-table slot detail)",
    }


def stadium_team_l3() -> dict[str, Any]:
    fm = read_json(T79 / "field_map.json")
    return {
        "source_task": "t79",
        "acceptance_ledger_entry": "E117",
        "acceptance_ledger_level": "L3",
        "status": "static_harvest_closed",
        "scope": ("stadium/team/table_extra_24 static L3 harvest + CLUB+0x18 forwarding "
                  "chain closed (neon lane)"),
        "summary": fm["summary"],
        "stadium_21": {
            "schema_fields": fm["stadium_21"]["schema_fields"],
            "internal_wire_slots": fm["stadium_21"]["internal_and_opaque_wire_slots"],
        },
        "team_24": {
            "schema_fields": fm["team_24"]["schema_fields"],
            "internal_wire_slots": fm["team_24"]["internal_wire_slots"],
        },
        "table_extra_24": fm["table_extra_24"],
        "club_base18_forwarded_6": fm["club_base18_forwarded_6"],
        "counts": {"stadium_L3": fm["summary"]["stadium_xml_grades"]["L3"],
                   "team_L3": fm["summary"]["team_xml_grades"]["L3"],
                   "extra_24_mapped": fm["summary"]["extra_24_mapped_fields"],
                   "club_forwarded_L3": fm["summary"]["club_base18_forwarded_upgraded_L3"]},
        "evidence_level": fm["evidence_level"],
        "L4": 0,
        "source_artifacts": artifacts("scratch/t79/out/field_map.json",
                                      "scratch/t79/out/xref_stad_team.json",
                                      "scratch/t79/out/verify.py",
                                      "scratch/t79/out/REPORT.md",
                                      "scratch/t79/out/DONE.md"),
    }


def denominator_summary() -> dict[str, Any]:
    b = read_json(T78 / "buckets.json")
    occ = b["occurrences"]
    buckets = {}
    for o in occ:
        buckets.setdefault(o["entity"], {})
        buckets[o["entity"]][o["bucket"]] = buckets[o["entity"]].get(o["bucket"], 0) + 1
    per_bucket = {}
    for e, d in buckets.items():
        per_bucket[e] = {k: d.get(k, 0) for k in
                         ("mapped_l3", "independent_member", "string_name_table",
                          "ui_or_derived", "held", "unresolved_wire_slot", "no_wire_evidence")}
        per_bucket[e]["sum"] = sum(per_bucket[e].values())
    carried = sum(v.get("mapped_l3", 0) + v.get("independent_member", 0)
                  + v.get("string_name_table", 0) for v in per_bucket.values())
    return {
        "source_task": "t78",
        "acceptance_ledger_entry": "E116",
        "acceptance_ledger_level": "L1",
        "status": "complete",
        "count": b["count"],
        "per_entity": per_bucket,
        "physical_coverage": {"carried": carried, "denominator": b["count"],
                              "ratio": round(carried / b["count"], 4),
                              "text": "110/1034 = 10.6%"},
        "L4": 0,
        "source_artifacts": artifacts("scratch/t78/out/buckets.json",
                                      "scratch/t78/out/coverage.md",
                                      "scratch/t78/out/DONE.md"),
    }
