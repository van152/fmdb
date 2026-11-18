"""Finalize t02 club framing audit; all writes stay in this output directory."""
from __future__ import annotations
import argparse
import importlib.util
import json
import struct
from pathlib import Path

OUT = Path(__file__).resolve().parent
SOLVER = OUT / "solve.py"


def load_solver():
    spec = importlib.util.spec_from_file_location("club_v2_solver", SOLVER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def audit_rows(mod, raw):
    count = struct.unpack_from("<I", raw, 8)[0]
    p = 14
    found = {}
    width4_ok = 0
    standard = 0
    for i in range(count):
        r4 = mod.try_row(raw, p, i, 4)
        r5 = mod.try_row(raw, p, i, 5)
        if r4 is not None:
            width4_ok += 1
        candidates = [r for r in (r4, r5) if r is not None]
        if len(candidates) == 1:
            row = candidates[0]
            standard += 1
            if i in set(range(69702, 69712)) or i in (0, 1, 2, 84258):
                found[i] = row
            p = row["end_off"]
            continue
        if len(candidates) > 1:
            raise RuntimeError(f"ambiguous widths at row {i} offset {p:#x}")
        needle = struct.pack("<I", i)
        end_search = min(p + 8192, len(raw) - 13)
        hits = []
        q = raw.find(needle, p + 20, end_search)
        while q >= 0:
            if q + 13 <= len(raw):
                o, x, y = struct.unpack_from("<III", raw, q)
                if o == i and x == y and raw[q + 12] in (0, 12):
                    hits.append(q)
            q = raw.find(needle, q + 1, end_search)
        if len(hits) != 1:
            raise RuntimeError(f"identity framing not unique at row {i}: {hits[:5]}")
        q = hits[0]
        row = {"idx": i, "payload_off": p, "end_off": q + 13, "row_len": q + 13 - p,
               "block_width": None, "identity_rel_off": q - p, "marker": raw[q + 12]}
        if i in set(range(69702, 69712)) or i in (0, 1, 2, 84258):
            found[i] = row
        p = q + 13
    return found, p, width4_ok, standard


def sample(raw, row):
    return {
        "row": row["idx"],
        "member_offset": f"0x{row['payload_off']:x}",
        "row_length": row["end_off"] - row["payload_off"],
        "parsed_block_width": row.get("block_width"),
        "identity_relative_offset": row.get("identity_rel_off"),
        "marker": row.get("marker"),
        "full_name": row.get("full_name"),
        "short_name": row.get("short_name"),
        "bytes_hex": raw[row["payload_off"]:row["end_off"]].hex(" "),
    }


def field_evidence(raw, row, label, offset, width):
    start = row["payload_off"]
    off = start + offset
    return {"member_offset": f"0x{off:x}", "row_relative_offset": offset,
            "width": width, "bytes_hex": raw[off:off + width].hex(" ")}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    mod = load_solver()
    raw = mod.load_raw()
    out = json.loads((OUT / "output.json").read_text(encoding="utf-8"))
    rows, final_pos, width4_ok, standard_count = audit_rows(mod, raw)
    r0 = mod.try_row(raw, 14, 0, 5)
    assert r0 is not None

    # Field boundaries are L1 byte-structure observations, not schema/4CC mappings.
    n1 = r0["full_len"]
    n2 = r0["short_len"]
    tail_identity = r0["end_off"] - 13
    first_short_len = r0["payload_off"] + 30 + n1
    short_text = first_short_len + 4
    flag3_off = short_text + n2
    fmap_specs = [
        (0, "db_id (u32)", 0, 4),
        (1, "parent_ref (u32; FFFFFFFF observed as none candidate)", 4, 4),
        (2, "duplicate u32 #1", 8, 4),
        (3, "duplicate u32 #2", 12, 4),
        (4, "five-byte block (semantic subdivision unresolved)", 16, 5),
        (5, "group/status u32 candidate", 21, 4),
        (6, "one-byte flag candidate", 25, 1),
        (7, "full-name byte length (u32)", 26, 4),
        (8, "short-name byte length (u32)", first_short_len - r0["payload_off"], 4),
        (9, "three-byte block (semantic unresolved)", flag3_off - r0["payload_off"], 3),
        (10, "ordinal|ID|repeated-ID (12B)", tail_identity - r0["payload_off"], 12),
        (11, "row trailer byte (value varies in three boundary rows)", r0["end_off"] - r0["payload_off"] - 1, 1),
    ]
    row_map = []
    for idx, name, offset, width in fmap_specs:
        width_value = width
        row_offset_value = offset
        variant_offsets = None
        if idx == 4:
            name = "class-dependent ID block (5B CLUB / 4B LEAGUE_BODY_CLUB)"
            width_value = {"CLUB": 5, "LEAGUE_BODY_CLUB": 4}
        elif idx == 5:
            row_offset_value = {"CLUB": 21, "LEAGUE_BODY_CLUB": 20}
            variant_offsets = row_offset_value
        elif idx == 6:
            row_offset_value = {"CLUB": 25, "LEAGUE_BODY_CLUB": 24}
            variant_offsets = row_offset_value
        row_map.append({
            "idx": idx, "field": name,
            "row_offset": row_offset_value,
            "width": width_value,
            "class_specific_following_byte": "LEAGUE_BODY_CLUB row+25 is retained as unassigned byte so the name length remains at +26" if idx == 6 else None,
            "offset_formula": (
                "row+16; width selected by class" if idx == 4 else
                "row+21 CLUB / row+20 LEAGUE_BODY_CLUB" if idx == 5 else
                "row+25 CLUB / row+24 LEAGUE_BODY_CLUB" if idx == 6 else
                "row+30+full_name_len" if idx == 8 else
                "row+34+full_name_len+short_name_len" if idx == 9 else
                "row_end-13" if idx == 10 else
                "row_end-1" if idx == 11 else "fixed row offset"),
            "mapping_level": "L1_structural_only",
            "schema_4cc": None, "object_offset": None,
            "evidence": field_evidence(raw, r0, name, offset, width),
        })
    lbc_row = rows[69709]
    lbc_extra_off = lbc_row["payload_off"] + 25
    row_map.append({
        "idx": 12, "field": "unassigned one-byte position after LEAGUE_BODY_CLUB flag candidate",
        "row_offset": 25, "width": 1, "offset_formula": "row+25 (LEAGUE_BODY_CLUB layout only)",
        "mapping_level": "L1_unassigned_byte", "schema_4cc": None, "object_offset": None,
        "evidence": {"member_offset": f"0x{lbc_extra_off:x}", "row_relative_offset": 25,
                     "width": 1, "bytes_hex": raw[lbc_extra_off:lbc_extra_off+1].hex(" "),
                     "sample_row": 69709}
    })

    before = [sample(raw, rows[i]) for i in (69702, 69703, 69704)]
    transition = sample(raw, rows[69705])
    compact = [sample(raw, rows[i]) for i in (69706, 69707, 69708)]
    after = [sample(raw, rows[i]) for i in (69709, 69710, 69711)]
    r_after = rows[69709]
    # Under the current candidate layout, a 4-byte block shifts the length word by one byte.
    wrong_len_off = r_after["payload_off"] + 25
    wrong_len = struct.unpack_from("<I", raw, wrong_len_off)[0]

    out.update({
        "status": "in_progress",
        "count": 84259,
        "class_partition": {
            "rule": "ordinal 0..69704 = CLUB (ID block 5B); ordinal 69705..84258 = LEAGUE_BODY_CLUB (ID block 4B)",
            "rows": {"CLUB": 69705, "LEAGUE_BODY_CLUB": 14554},
            "class_byte_or_flag_found": False,
            "basis": "the task's accepted contiguous class split plus type_id=3 dual-RTTI/slot19 evidence in scratch/t01/inbox/t01h/output.json; no per-row class byte is claimed",
            "CLUB_samples": [sample(raw, rows[i]) for i in (0, 1, 2)],
            "LEAGUE_BODY_CLUB_samples": [sample(raw, rows[i]) for i in (69705, 69709, 69710)],
            "compact_rows_inside_LEAGUE_BODY_CLUB_segment": [69706, 69707, 69708],
            "semantic_widths_vs_byte_walker": "class field widths are 5B/4B; the framing walker consumes the adjacent +20 byte as part of a 5-byte aggregate to keep subsequent boundaries. For LEAGUE_BODY_CLUB the schema split is 4B block plus separate row+20 byte; row+25 remains unassigned pending full schema decode.",
            "width4_candidate_successes_note": "zero refers only to retrying the entire main-class parser with the ID block changed to 4B and no class-specific adjacent-byte handling; it does not negate the accepted class-specific 4B field width"
        },
        "semantic_field_width_counts": {"CLUB_ID_block_5B": 69705, "LEAGUE_BODY_CLUB_ID_block_4B": 14554, "class-specific_body_unparsed": 3},
        "walked_rows": 84259,
        "member_length": len(raw),
        "member_sha256": out.get("member_sha256"),
        "row_body_end_member_offset": f"0x{final_pos:x}",
        "footer_offset": f"0x{len(raw)-8:x}",
        "footer_hex": raw[-8:].hex(" "),
        "footer_exact": final_pos == len(raw) - 8,
        "standard_layout_rows": standard_count,
        "width4_candidate_successes": width4_ok,
        "row_offset_map": row_map,
        "variants": [
            {
                "id": "byte-framing-parser",
                "rows": 84256,
                "interpretation": "the generic framing parser consumes row+16..20 as a 5-byte aggregate; semantic ID-block width is class-dependent and separately recorded in class_partition", 
                "ordinal_ranges_included": [[0, 69705], [69709, 84258]],
                "rule_status": "observed layout, not class discriminator",
                "sample_rows_before_transition": before,
                "transition_row": transition,
                "sample_rows_after_transition": after,
                "width4_negative_example": {
                    "row": 69709, "member_offset": f"0x{wrong_len_off:x}",
                    "row_relative_offset": 25, "bytes_hex": raw[wrong_len_off:wrong_len_off+4].hex(" "),
                    "u32_le": wrong_len, "result": "would be implausible full-name length under the same schema (the valid 5-byte parse has length 18 at row+26)"
                }
            },
            {
                "id": "compact-identity-framed-body",
                "rows": 3,
                "ordinal_range": [69706, 69708],
                "rule_status": "body not decoded; only identity suffix framing established",
                "identity_relative_offset": 42,
                "row_span_bytes": 55,
                "samples": compact,
            }
        ],
        "marker_counts": {"0": 84256, "12": 3},
        "row_length_distribution": out.get("row_length_distribution", {}),
        "class_reader_evidence": [
            {
                "class": ".?AVCLUB@db@@",
                "source": "editor.exe (SHA-256 b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4)",
                "slot19_entry_file_offset": "0xe5a7a0",
                "width_instruction_file_offset": "0xe5a811",
                "width_instruction_bytes": "41 b8 04 00 00 00",
                "nearby_destination_file_offset": "0xe5a807",
                "nearby_destination_bytes": "49 8d be e0 00 00 00",
                "note": "proves one 4-byte transfer to object+0xe0, not a row-level class selector"
            },
            {
                "class": ".?AVLEAGUE_BODY_CLUB@db@@",
                "source": "editor.exe (SHA-256 b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4)",
                "slot19_thunk_file_offset": "0x157cff0",
                "unwrapped_reader_file_offset": "0x43beba0",
                "transfer4_file_offset": "0x43bebe6",
                "transfer4_bytes": "41 b8 04 00 00 00",
                "destination4_file_offset": "0x43bebdc",
                "destination4_bytes": "48 8d 91 70 01 00 00",
                "transfer1_file_offset": "0x43bec05",
                "transfer1_bytes": "41 b8 01 00 00 00",
                "destination1_file_offset": "0x43bebfb",
                "destination1_bytes": "48 8d 93 78 01 00 00",
                "note": "reader has separate 4-byte and 1-byte transfers to object+0x170/+0x178; not yet aligned to table row fields"
            }
        ],
        "field_mapping_progress": {"structural_entries": 13, "schema_4cc_to_object_to_row_L3": 0, "target": 10},
        "unclosed": [
            {
                "issue": "class-to-row discriminator / 5B-vs-4B field identity",
                "evidence": "The parsed suffix rows 69709..84258 validate using the 5-byte aggregate layout; a width-4 retry at row 69709 shifts the length word to 0x1200 (4608). The class-specific readers show 4-byte transfers, but their destination offsets are not aligned to row fields yet.",
                "status": "unresolved; do not infer class from ordinal, marker, flag, or name order"
            },
            {
                "issue": "three compact records body semantics",
                "rows": [69706, 69707, 69708],
                "evidence": "55-byte spans, identity at row+42, marker bytes 0x0c/0x0c/0x00; standard field parser fails",
                "status": "identity framing only; body fields unparsed"
            },
            {
                "issue": "4CC getter-to-reader alignment",
                "evidence": "No getter 4CC has yet been aligned to the slot19 reader destination and payload offset in this run.",
                "status": "0 L3 field mappings; threshold 10 not met"
            }
        ]
    })
    (OUT / "output.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"walked={out['walked_rows']}; standard={standard_count}; compact=3; footer_exact={out['footer_exact']}; L3_fields=0; status={out['status']}")
    if args.selftest:
        assert final_pos == len(raw) - 8
        assert standard_count == 84256
        assert width4_ok == 0
        assert [rows[i]["marker"] for i in (69705, 69706, 69707, 69708)] == [12, 12, 12, 0]
        assert wrong_len == 0x1200
        print("selftest OK")


if __name__ == "__main__":
    main()
