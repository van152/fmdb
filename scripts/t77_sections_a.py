"""t77 section builders, part 1: E111 (t71), E112 (t72), E113 (t73).

Every builder returns a compact, pointer-carrying section: counts, key tables and
verbatim negative/held statements only. Bulk stays in the accepted artifacts.
"""
from __future__ import annotations

from typing import Any

from t77_common import ROOT, artifacts, read_json

T71 = ROOT / "scratch" / "t71" / "out"
T72 = ROOT / "scratch" / "t72" / "out"
T73 = ROOT / "scratch" / "t73" / "out"

# Fields whose evidence class differs from the 22 cnst projections (E111 claim).
T71_SPECIAL = {"Cebd", "Cyfn"}


def club_extra_object_row() -> dict[str, Any]:
    fm = read_json(T71 / "field_map_r3.json")
    rows = read_json(T71 / "rows_extra3.json")
    fields = []
    for f in fm["fields"]:
        wire = f["wire"]
        server = f["profiles"]["server"]
        fields.append({
            "code": f["code"],
            "schema_id": f["id"],
            "grade": f["grade"],
            "prior_grade": f["prior"]["grade"],
            "prior_ledger": f["prior"]["ledger"],
            "type": f["schema"]["type"],
            "enum_ref": f["schema"].get("enum_ref"),
            "object_path": wire["object_path"],
            "width": wire["width"],
            "side": wire["side"],
            "body_anchor": wire.get("body_anchor"),
            "absolute_rule": wire["absolute_rule"],
            "client_default": wire.get("absent_client_default"),
            "wire_extra": {k: v for k, v in wire.items()
                           if k not in ("object_path", "width", "side", "body_anchor",
                                        "absolute_rule", "absent_client_default")},
            "getter_family": f["static_getter"].get("family", "non_cnst_chain"),
            "server_histogram": server["histogram"],
            "server_wire_rows": server["wire"],
            "server_violations": server["bad"],
            "uid_joined": f["uid_pair_control"]["uid_joined"],
            "uid_both_wire": f["uid_pair_control"]["both_wire"],
            "first_counterexample": f["first_counterexample"],
        })
    env = {a: {k: rows["envelopes"][a][k]
               for k in ("count", "header", "footer", "body", "payload", "width")}
           for a in ("client", "server")}
    env["client"].update(archive_sha256=rows["archives"]["client"]["archive_sha256"],
                         data_base=rows["archives"]["client"]["data_base"],
                         toc_offset=rows["archives"]["client"]["toc_offset"])
    env["server"].update(archive_sha256=rows["archives"]["server"]["archive_sha256"],
                         data_base=rows["archives"]["server"]["data_base"],
                         toc_offset=rows["archives"]["server"]["toc_offset"])
    return {
        "source_task": "t71",
        "acceptance_ledger_entry": "E111",
        "acceptance_ledger_level": "L3",
        "status": "accepted_cross_object_chain_closed",
        "scope": fm["scope"],
        "member_binding": ("table_extra_3.dat proven via name formatter (extra=1, old_save=0) "
                           "0xf5164c/58 -> 0xf54f00 -> 0x3bb8b70; 0x3cefca4/cb2 immediate "
                           "'table_extra_' + 0x3cefd4e decimal suffix + '.dat'; loaded by "
                           "4B-ordinal join loop into CLUB, object allocated 0x130B at "
                           "CLUB+0x100 (0xe5d250..29d); club_links / 8 numbered subtables / "
                           "name_table_* excluded with evidence"),
        "object": {"owner": "CLUB", "displacement": "CLUB+0x100",
                   "allocation_bytes": "0x130B", "member": "table_extra_3.dat"},
        "row_frame": {
            "identity": rows["identity"],
            "envelopes": env,
            "row_count": rows["envelopes"]["client"]["count"],
            "uid_join": "exact table_3 ordinal join 84,259/84,259 dual-archive",
            "coordinate_digest": rows["coordinate_digest"],
        },
        "wire_blocks": {
            "A": "tag 2 + 7 bytes -> extra+0xe0 (Ccsp Ccsk Ccsf Ccsr Ccsb Ccsh Ccsy)",
            "B": "tag 3 + 15 bytes -> extra+0xe7 (B-lane order per t63 object_path)",
            "E": "u8[r+83] election presence; A=r+132+19E, B=r+140+19E",
            "Cebd": "r+88 only if E=1 (11,963 present / 72,296 absent)",
            "Cyfn": "client r+4, server formula a28/f48/a68 (12-byte chain)",
        },
        "promoted": {
            "count": len(fields),
            "cnst_projections": [f["code"] for f in fields if f["code"] not in T71_SPECIAL],
            "special": sorted(T71_SPECIAL & {f["code"] for f in fields}),
            "fields": fields,
        },
        "scoped_enum": fm["scoped_enum"],
        "domain": {
            "cnst": "84,259 rows x 22 i8 columns = 1,853,698 bytes, 0 violations vs frozen "
                    "cnst={0,1,2,3,4,6}; enum 3 legal-unobserved",
            "server_only": "cnst/Cebd server-only wire (client 0 intersection vs default-6 "
                           "object baseline)",
            "Cyfn": "dual-archive (30,661 zero + 53,598 in 1857..2024)",
            "unnamed_adjacent": "extra+0xcc = 84,259 x ffffffff both archives, kept unnamed",
        },
        "regression_fixtures": rows["fixtures"],
        "negative_preserved": [
            "date_relationship_control, Casp and Csnm bounds untouched (t63/t65 originals kept)",
            "adjacent +0xcc stays unnamed (constant all-ones, not a business slot)",
        ],
        "L4": fm["L4"],
        "source_artifacts": artifacts(
            "scratch/t71/out/field_map_r3.json", "scratch/t71/out/rows_extra3.json",
            "scratch/t71/out/chain.json", "scratch/t71/out/verify.py",
            "scratch/t71/out/REPORT.md", "scratch/t71/out/DONE.md"),
        "pointer": "scratch/t71/out/field_map_r3.json (full getter/setter chains, 154 KB)",
    }


def slot_fingerprints() -> dict[str, Any]:
    inv = read_json(T72 / "inventory.json")
    fp = read_json(T72 / "fingerprints.json")
    tables = {}
    for name, t in inv["tables"].items():
        keys = [s["key"] for s in t["slots"]]
        tables[name] = {
            "table_id": t["table_id"],
            "slot_count": len(t["slots"]),
            "kind_counts": t["kind_counts"],
            "slot_keys": keys,
            "unnamed_keys": [s["key"] for s in t["slots"] if s["kind"] == "unnamed"],
            "held_keys": [s["key"] for s in t["slots"] if s["kind"] == "held"],
        }
    return {
        "source_task": "t72",
        "acceptance_ledger_entry": "E112",
        "acceptance_ledger_level": "L2",
        "status": "partial_data_side_only",
        "grading_ceiling": inv["grading"]["ceiling"],
        "scope": ("unnamed/held physical slot inventory + dual-archive value fingerprints "
                  "for club/comp/nation; no exe static claim"),
        "tables": tables,
        "escalations": {
            "count": len(inv["escalations"]),
            "slots": [e["slot"] for e in inv["escalations"]],
            "tables": sorted({e["table"] for e in inv["escalations"]}),
            "kind": sorted({e["kind"] for e in inv["escalations"]}),
            "handed_to": "t75 (E114) nation segment grammars",
        },
        "replay": {"tables": sorted(inv["replay"].keys()),
                   "note": "frozen-trajectory replay; coordinate_digests_matched per table"},
        "fingerprint_shape": ["width histogram", "first/last (row,absolute,raw)",
                              "distinct", "zero/all-ones ratios", "u8..i32/f32 interpretations",
                              "value histograms", "FK probes", "xref_hint (shape only)"],
        "negative_notes_verbatim": inv["negative_notes"],
        "delivery_gap": ("verify.py/REPORT/DONE not delivered by the lane (wall-clock kill); "
                         "inventory.json + fingerprints.json + commander-written REPORT/DONE "
                         "are the accepted artifacts"),
        "L4": fp["L4"],
        "source_artifacts": artifacts("scratch/t72/out/inventory.json",
                                      "scratch/t72/out/fingerprints.json",
                                      "scratch/t72/out/REPORT.md",
                                      "scratch/t72/out/DONE.md"),
        "pointer": "scratch/t72/out/fingerprints.json (470 KB per-slot fingerprints)",
    }


def simple_tables() -> dict[str, Any]:
    frames = read_json(T73 / "frames.json")
    out = frames["out"]
    frame_rows, slot_rows, graded = {}, [], {"L2": 0, "L3": 0, "candidate": 0, "unmapped": 0}
    for key, rec in out.items():
        frame_rows[key] = {
            "status": rec["status"],
            "frame": rec["frame"],
            "closure": rec["closure"],
            "payload_len": rec["payload_len"],
            "payload_sha256": rec["payload_sha256"],
            "alias_group": rec["alias_group"],
            "header_origin_data_unique": rec["header_origin_data_unique"],
            "footer_flag_be1": rec["footer"].get("flag_be1"),
            "footer_hex": rec["footer"].get("footer_hex"),
        }
    for tid in (2, 5, 19, 41):
        for arch in ("client", "server"):
            p = T73 / f"slots_{arch}_{tid}.json"
            if not p.exists():
                continue
            d = read_json(p)
            for s in d["slots"]:
                graded[s["grade"]] = graded.get(s["grade"], 0) + 1
                if s["grade"] != "unmapped":
                    slot_rows.append({"table": tid, "archive": arch,
                                      "field": s["field"], "offset": s["offset"],
                                      "width": s["width"], "grade": s["grade"]})
    l2 = [r for r in slot_rows if r["grade"] == "L2"]
    distinct_l2 = sorted({(r["table"], r["field"], r["offset"]) for r in l2})
    return {
        "source_task": "t73",
        "acceptance_ledger_entry": "E113",
        "acceptance_ledger_level": "L2",
        "status": "closed_8_of_8_archives",
        "tables": frames["tables"],
        "frames": frame_rows,
        "frames_closed": sum(1 for r in frame_rows.values() if r["status"] == "closed"),
        "frames_total": len(frame_rows),
        "slot_grades": graded,
        "slots": slot_rows,
        "L2_slots": {
            "ledger_stated_count": 17,
            "enumerated_in_claim": 10,
            "archive_graded_records": len(l2),
            "distinct_table_field_offset": len(distinct_l2),
            "distinct_rows": [{"table": t, "field": f, "offset": o} for t, f, o in distinct_l2],
            "count_note": ("The E113 claim text states 17 L2 slots but enumerates 10 "
                           "(city 2 + continent 2 + region 2 + currency 4). The artifacts "
                           "carry 14 L2-graded records over 8 archives = 10 distinct "
                           "(table, field, offset) triples. Both numbers are recorded; the "
                           "substance (offsets) is asserted in --verify, the count discrepancy "
                           "is kept as an open accounting note for the commander."),
        },
        "alias_negative": {
            "result": ("(13,9)/(14,8)/(15,7) same-alias-group — data side CANNOT determine "
                       "header origin for fixed-stride tables"),
            "resolution": "footer flag byte (F=8 flag_be1) + frozen anchor sanity",
            "header_origin_data_unique_all_false": True,
            "rejected_rule": "footer_last_eq_max_uid rejected as non-generic (fails on 7-row tables)",
        },
        "dual_archive_findings": {
            "city": "client and server payload byte-identical (sha 66f8cc27..)",
            "continent": "server = client business bytes + 14B all-zero slot block (7/7 rows)",
            "region": "server +1B per row (constant 04 at the extra site, 28/28)",
            "currency": "variable trailer walk, 173 rows, rdui@-13 / duni@-9",
        },
        "frozen_anchors": {"count": 14, "conflicts": 0,
                           "city_checked": 9,
                           "list": ["city Clat@1 Clon@5 Catt@9 Cnti@10 Cwea@14 Clgi@21 Clri@25 "
                                    "rdui@30 duni@34", "continent rdui@21 duni@25",
                                    "region rdui@32 duni@36", "currency rdui=-13 duni=-9"]},
        "unmapped_not_forced": {
            "city": ["NDBC", "FDBC", "Calt", "Cinh"],
            "continent": ["NDBC", "FDBC", "Crgs", "DBvw"],
            "region": ["NDBC", "FDBC"],
            "currency": ["NDBC", "FDBC"],
            "reason": "value domains do not decide; DBvw enum has 4 empty names in master.json",
        },
        "tool_boundaries": [
            "only fixed-stride tables self-prove identity; variable tables need walk_var or escalate",
            "enum judgement requires non-empty scoped enum names",
            "footer_last_eq_max_uid is not a general criterion",
            "FK judgement has no capability against variable-length target tables "
            "(Cnti/Clgi/Clri/Cwea offsets stand via frozen L3 anchors, not via FK hits)",
        ],
        "L4": 0,
        "source_artifacts": artifacts(
            "scratch/t73/out/frames.json",
            "scratch/t73/out/slots_client_2.json", "scratch/t73/out/slots_server_2.json",
            "scratch/t73/out/slots_client_5.json", "scratch/t73/out/slots_server_5.json",
            "scratch/t73/out/slots_client_19.json", "scratch/t73/out/slots_server_19.json",
            "scratch/t73/out/slots_client_41.json", "scratch/t73/out/slots_server_41.json",
            "scratch/t73/out/verify.py", "scratch/t73/out/REPORT.md",
            "scratch/t73/out/DONE.md"),
        "pointer": "reports/other_tables_schema.json#/tables (per-table slot detail)",
    }
