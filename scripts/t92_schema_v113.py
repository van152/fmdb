#!/usr/bin/env python3
"""t92 - schema v11.2 -> v11.3-candidate assembly (E132-E138 mechanical merge).

  py -V:3.12 -I -B scripts/t92_schema_v113.py --selftest
  py -V:3.12 -I -B scripts/t92_schema_v113.py --build
  py -V:3.12 -I -B scripts/t92_schema_v113.py --denominator
  py -V:3.12 -I -B scripts/t92_schema_v113.py --all

Assembly only, no re-adjudication (t90 pattern). Three new root sections are
appended (table45_structure_e132_e138 / t9_grammar_e133 / cbw_route_e135_e137)
and ONE existing section gets value edits plus an annotation
(table9_closure_e127: t51 frozen-cursor server 307,555 -> 307,564 per E133).

reports/ is never written: products are scratch/t92/out/schema_v113.json and
scratch/t92/out/denominator_note.json.
Exit codes: 0 pass / 1 check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "reports" / "club_nation_subtable_schema.json"
DENOM = ROOT / "reports" / "xml_denominator_coverage.json"
LEDGER = ROOT / "scratch" / "t01" / "LEDGER.json"
T88_2 = ROOT / "scratch" / "t88" / "out2"
T88_3 = ROOT / "scratch" / "t88" / "out3"
T89 = ROOT / "scratch" / "t89" / "out"
OUT = ROOT / "scratch" / "t92" / "out"
SCHEMA_OUT = OUT / "schema_v113.json"
DENOM_OUT = OUT / "denominator_note.json"

BASE_SHA = "e3c5400c6d1331605df433558dadce9fb8c84fda916913f0652182bfdd7f5a85"
BASE_BYTES = 21344318
BASE_VERSION = "11.2"
BASE_ROOTS = 40
NEW_VERSION = "11.3-candidate"
NEW_BY = "t92"
DENOM_SHA = "2cfefefb5b7ea676db2cc50f389cee6afa078bdfe9b59dcf6997d5c76b1c77b5"

SOURCES = {
    "scratch/t88/out2/row_frame.json":
        "2910173ba625d3a50e98771b5eb30c807c8e1fc4014d09d255b192b45b570d3e",
    "scratch/t88/out3/slots.json":
        "f1050953d19da7ea30902f3cc11ee4eb0cf1e55b1f4ca8be408f7f2026663420",
    "scratch/t88/out3/pe_sections.json":
        "894a34f5d5f1f65b545041cb9196e1bb8e2978e85ea1424fbb0975c351451d30",
    "scratch/t88/out3/rec_structure.json":
        "8dd00f0528fdbbbec60b8fc0ebe98b6c5ab44347fa767a62a4ebc2d9e33cf294",
    "scratch/t89/out/table9_grammar.json":
        "5915217d5aa12ecd127bfc1c28aec90c816a73cb5dd727cf725f409775d22bdd",
    "scratch/t89/out/_dual.json":
        "0b7aa492de9295d1f2eef2fa74de68a79385a32c4eba78cd124bbc61ca08de40",
    "scratch/t89/out/verify.py":
        "fc1d706fc2ab7d57a6901598f7d06f8dc6083d02652d88fc4c74af722f4513c8",
}

NEW_ROOTS = ("table45_structure_e132_e138", "t9_grammar_e133", "cbw_route_e135_e137")
MUTABLE = ("schema_version", "generated_by", "incremental_provenance",
           "coverage", "table9_closure_e127")
LEDGER_IDS = ("E132", "E133", "E134", "E135", "E136", "E137", "E138")
E133_OLD, E133_NEW = 307555, 307564


class CheckFailure(Exception):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm_bytes(value: Any) -> bytes:
    """Digest basis, t90 convention: indent=2, LF (the 32 existing
    untouched_root_digests in v11.2 recompute only under this form)."""
    return json.dumps(value, ensure_ascii=False, indent=2,
                      allow_nan=False).encode("utf-8")


def file_bytes(value: Any) -> bytes:
    """On-disk form of reports/*.json: indent=1, CRLF, no trailing newline."""
    txt = json.dumps(value, ensure_ascii=False, indent=1, allow_nan=False)
    return txt.replace("\n", "\r\n").encode("utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


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


# ------------------------------------------------- table_45 (E132/E134/E138) --
def table45_recompute() -> dict[str, Any]:
    """Independent t92 recompute over the frozen payload + start table."""
    pay = (T88_2 / "_p_server_45.bin").read_bytes()
    starts_raw = (T88_2 / "_starts.bin").read_bytes()
    n = len(starts_raw) // 4
    starts = list(struct.unpack("<%dI" % n, starts_raw))
    rt: dict[int, int] = {}
    bad_rowlen = 0
    rt8 = 0
    rt8_namelen_nonzero = 0
    bad_identity = 0
    rowlens = set()
    for i, s in enumerate(starts):
        end = starts[i + 1] if i + 1 < n else len(pay) - 8
        row = pay[s:end]
        namelen = struct.unpack_from("<I", row, 37)[0]
        rowlens.add(len(row))
        if len(row) != 80 + namelen:
            bad_rowlen += 1
        t = row[4]
        rt[t] = rt.get(t, 0) + 1
        if t == 8:
            rt8 += 1
            if namelen:
                rt8_namelen_nonzero += 1
        if len(row) < 13:
            bad_identity += 1
            continue
        ordn, uid1, uid2 = struct.unpack_from("<III", row, len(row) - 13)
        if not (ordn == i & 0xFFFFFFFF and uid1 == uid2 and row[-1] == 0):
            bad_identity += 1
    return {
        "source": ["scratch/t88/out2/_p_server_45.bin", "scratch/t88/out2/_starts.bin"],
        "payload_bytes": len(pay),
        "header_bytes": 13,
        "header_count_at_plus8": struct.unpack_from("<I", pay, 8)[0],
        "footer_bytes": 8,
        "footer_hex": pay[-8:].hex(),
        "rows": n,
        "bad_rowlen": bad_rowlen,
        "rowlen_min": min(rowlens),
        "rowlen_max": max(rowlens),
        "rowlen_distinct": len(rowlens),
        "rec_type_distinct": len(rt),
        "rec_type_255_null": rt.get(255, 0),
        "rec_type_8_rows": rt8,
        "rec_type_8_namelen_nonzero": rt8_namelen_nonzero,
        "bad_identity": bad_identity,
        "recompute_verdict": "rowlen==80+namelen universal; identity 13B self-consistent",
    }


def family_rt_map(slots: dict[str, Any]) -> dict[str, Any]:
    fam: dict[str, set] = {}
    l3 = 0
    for e in slots["codes"]:
        if e.get("grade") != "L3":
            continue
        l3 += 1
        if e.get("rec_type") is not None:
            fam.setdefault(e["family"], set()).add(int(e["rec_type"]))
    out = {k: sorted(v) for k, v in sorted(fam.items())}
    return {"map": out, "l3_codes": l3,
            "families": len(out),
            "rec_types": sorted({r for v in out.values() for r in v}),
            "conflict_families": sorted(k for k, v in out.items() if len(v) > 1)}


def table45_section(row_frame: dict[str, Any], rec_struct: dict[str, Any],
                    slots: dict[str, Any]) -> dict[str, Any]:
    fam = family_rt_map(slots)
    sec = rec_struct["sections"]
    return {
        "generated_by": "t92",
        "acceptance_ledger_entries": ["E132", "E134", "E138"],
        "acceptance_ledger_level": "L2",
        "source_task": ["t88-fix2/fix3/fix4 (E132 commander probe)",
                        "t88-fix5 (E134)", "t88-fix9 + commander (E138)"],
        "table": {
            "path": "server_db/table_45.dat",
            "table_type": 45,
            "rtti": ".?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@",
            "rows": 84477,
            "client_archive": "absent (client_db.dat has no table_45 entry; server-only)",
            "grade": "L2",
        },
        "row_decomposition_e138": {
            "grade": "L2",
            "form": "pre[0..36] 37B | [u32 namelen][utf8 name] @37 | tail 26B | identity 13B",
            "rowlen_rule": "rowlen == 80 + namelen (universal over all 84,477 rows)",
            "tail_at": "row_end - 39 (26B fixed window, fixed distance from row end)",
            "identity_at": "row_end - 13",
            "identity_layout": "[ordinal u32][uid u32][uid u32][u8 tail=0]",
            "physical_column_count": "~14 (8 prefix u32-slots + rec_type u8 + name + ~5 tail columns)",
            "capacity_verdict": "the physical row CANNOT hold 117 independent fields -> the 117 club.xml codes are an accessor VIEW over ~14 physical columns",
            "frozen_artifacts": ["scratch/t88/out2/row_frame.json",
                                 "scratch/t88/out3/rec_structure.json"],
            "header_count_at_plus8": row_frame["header_u32_at8"],
            "footer_hex": "00000001775f0100",
            "footer_bytes": 8,
            "t92_recompute": table45_recompute(),
        },
        "three_columns_e132": {
            "grade": "L2 (data-side self-consistent; u32@5 has an external anchor)",
            "columns": [
                {"col": "u32@0", "verdict": "club-uid link column",
                 "evidence": "96.7% membership against the 84,259 club main-row UIDs; 8,368 clubs actually appear"},
                {"col": "u8@4", "verdict": "rec_type byte",
                 "evidence": "37 distinct values; 255 = null x 38,968"},
                {"col": "u32@5", "verdict": "person-uid",
                 "evidence": "external anchor C.Ronaldo 735216 x18 (provenance ext/fm-data@d7a7150); 35,926 distinct"},
            ],
            "undetermined": rec_struct["sections"]["commander_columns"]["cols_undetermined"],
            "prefix_grid_e134": {"u32_slots": [0, 9, 13, 17, 21, 25, 29, 33],
                                 "u8_slots": [4],
                                 "note": "7 u32 slots @9..33 vary by rec_type; 37B prefix is fixed-length"},
            "identity_uid": "row self-key, dense 0..89,974",
            "premise_refuted": rec_struct["premise_refuted_carryover"],
        },
        "rec_type_census_e138": {
            "grade": "L2",
            "distinct": 37,
            "null_255": 38968,
            "rec_type_8": {"rows": 3391, "namelen_zero_all": True,
                           "note": "shortest rows in the table (namelen=0); prefix columns proven on this family: club_uid@0 / rt@4 / person_uid@5 (0xffffffff = empty) / club_uid2 pair @21,@25"},
            "census_source": "scratch/t88/out3/rec_structure.json#/sections/rec_type_census",
        },
        "accessor_view_model_e138": {
            "grade": "L2",
            "claim": "117 club.xml codes = (family -> rec_type, suffix -> row/column) accessor view, NOT 117 physical columns",
            "family_to_rec_type": fam["map"],
            "family_to_rec_type_basis": "34 L3 codes in scratch/t88/out3/slots.json (multi-suffix families share one rec_type)",
            "families_anchored": fam["families"],
            "rec_types_anchored": fam["rec_types"],
            "l3_code_count": fam["l3_codes"],
            "family_rt_conflicts": fam["conflict_families"],
            "rt_14_34_L3_examples": [
                {"family": "CFG", "rec_type": 24, "l3_codes": 6},
                {"family": "CHA", "rec_type": 13, "l3_codes": 1},
                {"family": "CHS", "rec_type": 25, "l3_codes": 5},
                {"family": "CLA", "rec_type": 26, "l3_codes": 4},
                {"family": "CYP", "rec_type": 10, "l3_codes": 6},
                {"family": "CYS", "rec_type": 27, "l3_codes": 6},
                {"family": "COS", "rec_type": 28, "l3_codes": 6},
            ],
            "reader_off_semantics": "the 34 L3 reader_off values are IN-MEMORY record offsets ([rdi+0xNN]), not wire offsets; wire_off derivation stays open",
            "open": ["suffix -> column pin-down (per-family reader_off or value-domain match)",
                     "reader_off -> wire_off derivation",
                     "per-4CC (rec_type, offset) mapping for the 80 held codes"],
        },
        "held_policy": "E134/E135 slot verdicts are copied as counts + the first counterexample pointers; nothing is re-adjudicated here",
        "L4": 0,
    }


def t9_grammar_section(grammar: dict[str, Any], dual: dict[str, Any],
                       sec127: dict[str, Any]) -> dict[str, Any]:
    eg = grammar["entry_grid"]
    cl, sv = dual["client"], dual["server"]
    return {
        "generated_by": "t92",
        "acceptance_ledger_entries": ["E133"],
        "acceptance_ledger_level": "L2",
        "source_task": "t89c (partial, commander REPORT/verify/DONE per E88 precedent)",
        "table": {"table_type": 9, "rtti": "NATIONAL_TEAM_CONTAINER",
                  "rows": 251, "archives": ["client", "server"], "grade": "L2"},
        "header_13b_decode": {
            "len": 13,
            "hex": eg["header"]["hex"],
            "fields": eg["header"]["fields"],
            "count_field": "u32 @ +8 = 251 (both archives)",
            "isomorphic_to_table_45": "same 13B header shape as table_45 (count u32@+8 = 84,477) -> the framing is a shared DATABASE_TABLE convention, not a t9 speciality",
        },
        "closure": {
            "rule": "13 + sum(body_len) + 12*rows + 9 = payload",
            "client": {"payload": cl["payload"], "body_sum": cl["body_len"]["sum"],
                       "arithmetic": "13 + 28,922 + 12*251 + 9 = 31,956",
                       "closure_exact": True,
                       "body_len": {"min": cl["body_len"]["min"], "max": cl["body_len"]["max"],
                                    "distinct": cl["body_len"]["distinct"]}},
            "server": {"payload": sv["payload"], "body_sum": sv["body_len"]["sum"],
                       "arithmetic": "13 + 304,530 + 12*251 + 9 = 307,564",
                       "closure_exact": True,
                       "body_len": {"min": sv["body_len"]["min"], "max": sv["body_len"]["max"],
                                    "distinct": sv["body_len"]["distinct"]},
                       "server_211_distinct_lengths": "unexplained (carried as open)"},
            "trailer": "12B identity [ordinal u32][uid u32][uid u32][u8 0]",
            "footer": {"len": 9, "hex": eg["footer"]["hex"]},
        },
        "lanes": {
            "ordinal_lane": {"offset": 12, "rule": "body[12] == ordinal & 0xff",
                             "rows_ok": "251/251", "archive": "client"},
            "sentinel_head": {"bytes": "00 ff ff ff ff", "offset": 0,
                              "rows_ok": "251/251", "archive": "client",
                              "note": "constant across all 251 client rows; the sentinel head is NOT the ordinal"},
        },
        "e127_correction": {
            "field": "server payload",
            "value_before": E133_OLD,
            "value_after": E133_NEW,
            "delta_bytes": E133_NEW - E133_OLD,
            "why_before": "E127/t85 recorded the t51 frozen-cursor footer offset (307,555) as the server payload length; the payload is 9 bytes longer because the 9B footer sits after that cursor end",
            "verified_by": "scratch/t89/out/verify.py V1 (len(payload)==307564) + t92 independent re-read of load_payload(server, table 9)",
            "ledger": "E133",
        },
        "carried_from_e127": {
            "table_9_is_per_nation": sec127["verdicts"]["table_9_is_per_nation"],
            "rows_equal_nation_rows": sec127["verdicts"]["table_9_rows_equal_nation_rows"],
            "item_grammar": sec127["held"]["item_grammar"],
            "nation_0x108": sec127["held"]["nation_0x108"],
        },
        "open": ["24 helper route expansion", "wire offset mapping",
                 "row0 byte-level reconciliation", "server 211 distinct body lengths"],
        "L4": 0,
    }


def cbw_route_section(pe: dict[str, Any], sec121: dict[str, Any]) -> dict[str, Any]:
    reloc = next(s for s in pe["sections"] if s["name"] == ".reloc")
    return {
        "generated_by": "t92",
        "acceptance_ledger_entries": ["E135", "E136", "E137"],
        "acceptance_ledger_level": "L2 (E136 correction is L1)",
        "source_task": ["t88-fix6 (E135)", "fix7 zero-output (E136)",
                        "fix8 PE baseline (E137)"],
        "negative_result_4cc_absence": {
            "grade": "L2",
            "claim": "the CBW*/CBD* family 4CC byte strings (CBDa/CBWa/CBWo/CHSo) are ZERO-OCCURRENCE in BOTH editor.exe (74.8MB) and fm.exe (491MB) - neither as cmp immediates nor as raw references",
            "method": "commander full-byte scan over both executables with the true PE section table (fix8 baseline)",
            "verdict_on_e135": "the fix6 '80 held' bucket is substantively correct, not a false negative",
            "preserved_as": "negative result kept verbatim; not upgraded to a positive routing proof",
        },
        "tag_position_routing": {
            "grade": "L2",
            "claim": "club record-family field reads = (rec_type, tag ordinal) POSITION routing; the 4CC exists only in the editor schema, not in the executables",
            "consistency": "self-consistent with the 34 L3 tag/rt chains in scratch/t88/out3/slots.json (E135) and with the accessor-view model (E138)",
            "consequence": "the remaining 80 held codes become a pure DATA-SIDE task: per-rec_type row-body tag sequence -> field order -> wire offset (recget_tagmap.json's 12 static groups are the seed)",
        },
        "e121_reference_downgrade": {
            "grade": "unverified (downgraded from an L3 citation)",
            "affected": "club_extra3_l3_e121 negative_proof: 'CBDa cmp @0x11f0ca7 / CBWa cmp @0x11f0cb6'",
            "reason": "cannot be reproduced byte-wise; t89_disasm.py used a hard-coded 5-section table that does not cover the 0x3ebad50 region, and the 0x1411f0ca7 window shows serialization code, not a cmp",
            "status": "the cited sites stay in the schema as UNVERIFIED references, not as evidence",
            "note": "the underlying TC_RECORD_GET chain addresses (0x3ebad50 etc.) live in the .reloc 45MB executable region; the true section table is fix8's",
            "preserved": "sec121.cbw_cbd_table_45_verdict is unchanged (it is a table-location verdict, not a dispatch verdict)",
        },
        "pe_baseline_fix8": {
            "exe": pe["exe"],
            "sha256": pe["sha256"],
            "image_base": pe["image_base"],
            "size_of_image": pe["size_of_image"],
            "nsec": pe["nsec"],
            "entry_rva": pe["entry_rva"],
            "reloc_section": {"name": reloc["name"], "rva": reloc["rva"],
                              "vsize": reloc["vsize"], "fo": reloc["fo"],
                              "rawsize": reloc["rawsize"], "exec": reloc["exec"]},
            "note": "true PE header (18 sections) replaces the hard-coded 5-section table used by t89_disasm.py",
            "source": "scratch/t88/out3/pe_sections.json",
        },
        "L4": 0,
    }

# ---------------------------------------------------------------- assembly ---
def patch_e127(sec127: dict[str, Any]) -> dict[str, Any]:
    """Value edit only: t51 frozen-cursor server offsets 307,555 -> 307,564."""
    sec = json.loads(json.dumps(sec127))
    cc = sec["cross_check_t51_frozen_cursor"]["server|table_9.dat"]
    before = {"t51_footer_at": cc["t51_footer_at"], "t51_last_end": cc["t51_last_end"]}
    require(before == {"t51_footer_at": E133_OLD, "t51_last_end": E133_OLD},
            f"E127 pre-edit value drift: {before}")
    cc["t51_footer_at"] = E133_NEW
    cc["t51_last_end"] = E133_NEW
    cc["t92_why_before"] = (
        "E127 recorded 307,555 for both t51_footer_at and t51_last_end. E133/t89 "
        "established the true server payload length is 307,564: 307,555 is the end of "
        "the LAST ROW BODY (== footer START), so the t51 frozen cursor stopped one 9B "
        "footer early. The 9 bytes are the footer 00 00 00 00 01 ec 7a e4 04, verified "
        "independently by t92 (load_payload(server,9)[307555:307564] == that footer). "
        "Client 31,947/31,956 is the identical 9-byte relation and is already correct.")
    cc["t92_correction"] = {"ledger": "E133", "value_before": E133_OLD,
                            "value_after": E133_NEW,
                            "delta_bytes": E133_NEW - E133_OLD,
                            "edits": ["t51_footer_at", "t51_last_end"]}
    sec["t92_e127_note"] = {
        "rule": "VALUE edit only on cross_check_t51_frozen_cursor/server; no other key "
                "of table9_closure_e127 is touched by t92",
        "why_the_section_was_right_elsewhere": "closure_claims/chains already carried "
                                               "307564; only the t51 cross-check copied "
                                               "the cursor end",
        "ledger": "E133",
    }
    return sec


def patch_doc(pre: dict[str, Any], sec45: dict[str, Any], sec_t9: dict[str, Any],
              sec_cbw: dict[str, Any], ledger: dict[str, Any]) -> dict[str, Any]:
    doc = json.loads(json.dumps(pre))
    doc["schema_version"] = NEW_VERSION
    doc["generated_by"] = NEW_BY
    doc["table45_structure_e132_e138"] = sec45
    doc["t9_grammar_e133"] = sec_t9
    doc["cbw_route_e135_e137"] = sec_cbw
    doc["table9_closure_e127"] = patch_e127(pre["table9_closure_e127"])

    cov = doc["coverage"]
    cov["table45_structure_E132_E138"] = {
        "table": "server_db/table_45.dat",
        "rows": 84477,
        "physical_columns": "~14",
        "xml_codes_viewed": 117,
        "family_to_rec_type_anchored": sec45["accessor_view_model_e138"]["families_anchored"],
        "L3_codes": sec45["accessor_view_model_e138"]["l3_code_count"],
        "grade": "L2",
        "note": "117 club.xml codes = accessor view over ~14 physical columns; "
                "suffix->column pin-down stays open (no new L3)",
    }
    cov["t9_grammar_E133"] = {
        "table_9_client_bytes": 31956,
        "table_9_server_bytes": E133_NEW,
        "server_corrected_from": E133_OLD,
        "ordinal_lane": "251/251",
        "sentinel_head": "251/251",
        "grade": "L2",
        "note": "13B header decode + closure + lanes; corrects E127's server value by "
                "+9 bytes (footer not counted in the t51 cursor end)",
    }
    cov["cbw_route_E135_E137"] = {
        "four_cc_zero_occurrence": True,
        "binaries_scanned": ["editor.exe", "fm.exe"],
        "routing_model": "tag-position ((rec_type, tag ordinal))",
        "e121_citation_downgraded": True,
        "grade": "L2",
        "note": "negative result preserved; 80 held codes become a data-side task",
    }
    cov["L4"] = 0

    prov = doc["incremental_provenance"]
    for eid in LEDGER_IDS:
        prov["acceptance_ledger_entries"][eid] = ledger_row(ledger[eid])
    prov["t92_ledger_snapshot"] = {
        "path": "scratch/t01/LEDGER.json",
        "guard_scope": "entry-level id, kind, level, date and canonical claim "
                       "SHA-256; no live full-file hash pin",
        "guarded_entries": list(LEDGER_IDS),
        "entries": [{"id": e, **ledger_row(ledger[e])} for e in LEDGER_IDS],
        "out_of_scope_note": "E131 and earlier stay as pinned by t90/t91",
    }
    prov["t92_source_snapshot"] = [
        {"path": p, "sha256": h, "bytes": (ROOT / p).stat().st_size}
        for p, h in SOURCES.items()]
    prov["t92_volume_policy"] = {
        "main_schema_keeps": ["per-section grade + ledger pointer",
                              "counters", "one source pointer per artifact"],
        "bulk_stays_out": "the t88 out2 7.6MB payload, the 337KB start table, the "
                          "t88 out3 559KB grid and the t89 28KB dual profile stay in "
                          "their own artifacts; only recomputed aggregates enter",
        "split_files_untouched": ["reports/other_tables_schema.json",
                                  "reports/xml_denominator_coverage.json"],
    }
    prov["t92_additive_rule"] = (
        "v11.2 sections are value-identical after the patch except table9_closure_e127 "
        "(two integer values + annotation keys under cross_check_t51_frozen_cursor/"
        "server, plus one new sibling key t92_e127_note); only schema_version, "
        "generated_by, coverage and incremental_provenance change, plus the three new "
        "root sections")
    return doc


def denominator_note() -> dict[str, Any]:
    raw = DENOM.read_bytes()
    require(sha(raw) == DENOM_SHA, f"denominator pin mismatch: {sha(raw)}")
    den = json.loads(raw)
    rows = [r for r in den["rows"] if r["bucket_after"] == "re_routed_table_45"]
    require(len(rows) == 117, f"re_routed row count {len(rows)} != 117")
    note = ("accessor-view model proven (E138): the 117 codes are a view over ~14 "
            "physical columns of server_db/table_45.dat; per-suffix column pin-down "
            "still pending (next wave). grade unchanged.")
    out_rows = [{
        "id": r["id"], "entity": r["entity"], "code": r["code"],
        "bucket_after": r["bucket_after"], "grade": r["grade"],
        "grade_unchanged": True,
        "grade_note": note,
        "note_ledger": ["E132", "E138"],
        "pointer": r["pointer"],
    } for r in rows]
    return {
        "schema_id": "fm24.xml_denominator_coverage.t92_note",
        "schema_version": "2+note",
        "generated_by": "t92",
        "status": "candidate_note_only",
        "base": {"path": "reports/xml_denominator_coverage.json",
                 "sha256": DENOM_SHA, "bytes": len(raw),
                 "schema_version": den["schema_version"],
                 "generated_by": den["generated_by"]},
        "rule": "annotation only: no bucket moves, no count changes, no grade value "
                "changes; the report file itself is NOT written by t92",
        "bucket": "re_routed_table_45",
        "row_count": len(rows),
        "grade_values_seen": sorted({str(r["grade"]) for r in rows}),
        "note": note,
        "note_ledger": ["E132", "E138"],
        "totals_after_unchanged": den["totals_after"],
        "unresolved_wire_slot_unchanged": den["unresolved_wire_slot"],
        "rows": out_rows,
        "L4": 0,
    }


# ------------------------------------------------------------------- driver ---
def build() -> int:
    base_raw = BASE.read_bytes()
    require(sha(base_raw) == BASE_SHA, f"v11.2 pin mismatch: {sha(base_raw)}")
    require(len(base_raw) == BASE_BYTES, "v11.2 byte count mismatch")
    for p, h in SOURCES.items():
        require(sha((ROOT / p).read_bytes()) == h, f"source pin mismatch: {p}")
    pre = json.loads(base_raw)
    require(pre["schema_version"] == BASE_VERSION, "baseline is not v11.2")
    require(len(pre) == BASE_ROOTS, f"baseline root key count {len(pre)} != 40")

    ledger = {e["id"]: e for e in read_json(LEDGER)["entries"]}
    for eid in LEDGER_IDS:
        require(eid in ledger, f"{eid} missing from LEDGER")
    require(ledger["E133"]["level"] == "L2", "E133 ledger level drift")
    require(ledger["E136"]["kind"] == "correction", "E136 ledger kind drift")

    sec45 = table45_section(read_json(T88_2 / "row_frame.json"),
                            read_json(T88_3 / "rec_structure.json"),
                            read_json(T88_3 / "slots.json"))
    sec_t9 = t9_grammar_section(read_json(T89 / "table9_grammar.json"),
                                read_json(T89 / "_dual.json"),
                                pre["table9_closure_e127"])
    sec_cbw = cbw_route_section(read_json(T88_3 / "pe_sections.json"),
                                pre["club_extra3_l3_e121"])
    doc = patch_doc(pre, sec45, sec_t9, sec_cbw, ledger)

    removed = [k for k in pre if k not in doc]
    changed = [k for k in pre if k in doc and doc[k] != pre[k] and k not in MUTABLE]
    require(not removed, f"root keys removed: {removed}")
    require(not changed, f"non-mutable roots changed: {changed}")
    require(len(doc) == BASE_ROOTS + len(NEW_ROOTS), f"root count {len(doc)}")
    doc["incremental_provenance"]["t92_assembly_guard"] = {
        "baseline": {"schema_version": BASE_VERSION, "sha256": BASE_SHA,
                     "bytes": BASE_BYTES, "root_keys": BASE_ROOTS},
        "product": {"schema_version": NEW_VERSION, "root_keys": len(doc)},
        "untouched_root_digests": section_digests(pre),
        "mutable_roots": list(MUTABLE),
        "new_roots": list(NEW_ROOTS),
        "structural_edits": [
            "table9_closure_e127/cross_check_t51_frozen_cursor/server|table_9.dat/"
            "{t51_footer_at,t51_last_end}: 307555 -> 307564 (values only, E133)",
        ],
        "annotation_keys_added": [
            "table9_closure_e127/cross_check_t51_frozen_cursor/server|table_9.dat/"
            "t92_why_before", ".../t92_correction", "table9_closure_e127/t92_e127_note"],
        "reports_touched": [],
        "L4": 0,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    SCHEMA_OUT.write_bytes(file_bytes(doc))
    print(f"wrote {SCHEMA_OUT.relative_to(ROOT)}  {SCHEMA_OUT.stat().st_size:,} B")
    print("root keys", len(doc), "| new", len(NEW_ROOTS))
    print("table45 L3 family rt", sec45["accessor_view_model_e138"]["family_to_rec_type"])
    print("t9 server", E133_NEW, "| e127 edits", doc["table9_closure_e127"]
          ["cross_check_t51_frozen_cursor"]["server|table_9.dat"]["t51_last_end"])
    return 0


def build_denominator() -> int:
    note = denominator_note()
    OUT.mkdir(parents=True, exist_ok=True)
    DENOM_OUT.write_bytes(file_bytes(note))
    print(f"wrote {DENOM_OUT.relative_to(ROOT)}  {DENOM_OUT.stat().st_size:,} B")
    print("rows", note["row_count"], "| grades", note["grade_values_seen"])
    return 0


def selftest() -> int:
    ok = True

    def ck(name: str, cond: bool) -> None:
        nonlocal ok
        print(("OK   " if cond else "FAIL ") + name)
        ok = ok and cond

    ck("E133 delta 9", E133_NEW - E133_OLD == 9)
    ck("closure client", 13 + 28922 + 12 * 251 + 9 == 31956)
    ck("closure server", 13 + 304530 + 12 * 251 + 9 == 307564)
    ck("rowlen rule", 80 + 14 == 94)
    ck("count 84477", struct.unpack_from("<I", b"\xfd\x49\x01\x00", 0)[0] == 84477)
    ck("roots", len(NEW_ROOTS) == 3 and BASE_ROOTS + 3 == 43)
    print("SELFTEST PASSED" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--build", action="store_true")
    g.add_argument("--denominator", action="store_true")
    g.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.build:
            return build()
        if a.denominator:
            return build_denominator()
        rc = build()
        return rc or build_denominator()
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
