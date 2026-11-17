#!/usr/bin/env python3
"""Read-only t01-j verifier for basic_people_db.dat.

Run from the fm24-db workspace with Python 3.12:
  py -V:3.12 -I -B scratch/t01/inbox/t01j/verify.py --help
  py -V:3.12 -I -B scratch/t01/inbox/t01j/verify.py --selftest
  py -V:3.12 -I -B scratch/t01/inbox/t01j/verify.py --write

Inputs (installed game files, editor.exe, frozen snapshots, old decoder) are
read-only. Only --write creates/replaces this directory's output.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DB_DIR = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
BASIC_PATH = DB_DIR / "basic_people_db.dat"
EDITOR_PATH = Path("D:/tmp2b/fm24/input/editor.exe")
OLD_READER_PATH = Path("D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
FMF_PREFIX = bytes.fromhex("02 01 66 6d 66 2e 08 00 00 28 b5 2f fd")
FMF_MAGIC = FMF_PREFIX[:9]
ZSTD_MAGIC = bytes.fromhex("28 b5 2f fd")
DAT_MAGIC = bytes.fromhex("03 01 74 61 64 2e")
BASIC_SHA256 = "2ac7da37e7b1df755b76c16cf39c569cb0a1e96509a7557c2ab9acf5d67f48bc"
RAW_SHA256 = "16709b0b5dda358179313c19ef58d0f78bff259cde68a0dcd1bb01c9589d35a5"
EDITOR_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
ARCHIVE_SHA256 = {
    "client_db.dat": "5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1",
    "server_db.dat": "99eed00bd26582648c0d3ff51b5c8e37a35b68c296a074e8fb476d1b3ca4a662",
}
SNAPSHOTS = {
    "evidence/fm24/reports/dbdat_decode/PEOPLE_DB.md": "246f2b46712c13fe6413a6b054a2821751bc673057a578cdec903f3125eb966c",
    "evidence/fm24/reports/dbdat_decode/PEOPLE_FIELDS.md": "671a1f69aacafb8621082f2b15a24f8352741f493364a18347c74765ba3a2e03",
}
CLASS_LENGTHS = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
WIDTH_WINDOWS = ((0xE4F370, "slot19-entry"), (0x3DC0220, "direct-callee"), (0x3C6E100, "direct-callee"))
EXPECTED_WIDTHS = [
    (0xE4F393, 1), (0xE4F43C, 2), (0xE4F468, 2),
    (0xE4F4F6, 8), (0xE4F4FE, 4), (0xE4F542, 8), (0xE4F54A, 4),
    (0xE4F57F, 8), (0xE4F587, 4), (0xE4F5BA, 4), (0xE4F5DA, 4),
    (0xE4F5FA, 2), (0xE4F61A, 2), (0xE4F63A, 2), (0xE4F65A, 2),
    (0xE4F67A, 2), (0xE4F69A, 2), (0xE4F6BA, 2), (0xE4F6DA, 2),
    (0xE4F6FA, 2), (0xE4F71A, 1), (0xE4F73A, 1), (0xE4F75A, 1),
    (0x3DC0241, 8), (0x3DC027B, 12), (0x3C6E121, 8), (0x3C6E129, 4),
]


class CheckFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CheckFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hx(data: bytes) -> str:
    return data.hex(" ")


def load_old_reader():
    if not OLD_READER_PATH.is_file():
        raise FileNotFoundError(f"read-only decoder unavailable: {OLD_READER_PATH}")
    return runpy.run_path(str(OLD_READER_PATH))


def manifest_snapshot_hashes() -> dict[str, str]:
    manifest_path = ROOT / "evidence/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pinned = {item["path"]: item["sha256"] for item in manifest["files"]}
    checked = {}
    for rel, expected in SNAPSHOTS.items():
        actual = sha256((ROOT / rel).read_bytes())
        require(pinned.get(rel) == expected and actual == expected,
                f"frozen snapshot is not manifest-pinned: {rel}")
        checked[rel] = actual
    return checked


def parse_rows(raw: bytes, lengths: dict[int, int] = CLASS_LENGTHS) -> dict:
    """Parse count + flag + class-sized records, checking ordinal and repeated ID."""
    if len(raw) < 5:
        raise ValueError("truncated basic_people header")
    count = struct.unpack_from("<I", raw, 0)[0]
    flag = raw[4]
    pos = 5
    classes: dict[int, int] = {}
    first_samples: dict[int, dict] = {}
    identity_mismatches = []
    ordinal_mismatches = []
    for ordinal in range(count):
        if pos + 2 > len(raw):
            raise ValueError(f"truncated record header at payload+0x{pos:x}")
        tag, class_id = raw[pos], raw[pos + 1]
        if tag != 0x11:
            raise ValueError(f"bad row tag at payload+0x{pos:x}: {tag:#x}")
        if class_id not in lengths:
            raise ValueError(f"unknown row class at payload+0x{pos + 1:x}: {class_id}")
        row_len = lengths[class_id]
        end = pos + row_len
        if end > len(raw):
            raise ValueError(f"row {ordinal} overruns payload at payload+0x{pos:x}")
        row_ordinal, id_a, id_b = struct.unpack_from("<III", raw, end - 12)
        if row_ordinal != ordinal:
            ordinal_mismatches.append((ordinal, row_ordinal, pos))
        if id_a != id_b:
            identity_mismatches.append((ordinal, id_a, id_b, pos))
        classes[class_id] = classes.get(class_id, 0) + 1
        if class_id not in first_samples:
            row = raw[pos:end]
            first_samples[class_id] = {
                "ordinal": ordinal,
                "payload_offset": pos,
                "row_length": row_len,
                "tag_class_bytes": hx(row[:2]),
                "row_hex": hx(row),
                "identity_block": {
                    "payload_offset": end - 12,
                    "bytes": hx(row[-12:]),
                    "ordinal_u32": row_ordinal,
                    "repeated_identifier_u32": id_a,
                    "repeated_identifier_hex": f"0x{id_a:08x}",
                },
            }
        pos = end
    return {
        "header_count": count,
        "flag": flag,
        "rows_end_offset": pos,
        "trailing_bytes": raw[pos:],
        "class_counts": classes,
        "sample_rows_by_class": first_samples,
        "row_count_parsed": count,
        "ordinal_mismatch_count": len(ordinal_mismatches),
        "repeated_identifier_mismatch_count": len(identity_mismatches),
        "first_ordinal_mismatches": ordinal_mismatches[:3],
        "first_identifier_mismatches": identity_mismatches[:3],
    }


def pe_file_offset_for_va(data: bytes, va: int) -> int:
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    require(data[pe:pe + 6] == b"PE\0\0\x64\x86", "editor.exe is not x64 PE")
    opt = pe + 24
    require(struct.unpack_from("<H", data, opt)[0] == 0x20B, "editor.exe is not PE32+")
    image_base = struct.unpack_from("<Q", data, opt + 24)[0]
    section_table = opt + struct.unpack_from("<H", data, pe + 20)[0]
    section_count = struct.unpack_from("<H", data, pe + 6)[0]
    for i in range(section_count):
        off = section_table + 40 * i
        _, _virtual_size, rva, raw_size, raw_off = struct.unpack_from("<8sIIII", data, off)
        delta = va - (image_base + rva)
        if 0 <= delta < raw_size:
            return raw_off + delta
    raise CheckFailure(f"VA has no file mapping: {va:#x}")


def static_evidence(editor: bytes) -> dict:
    require(len(editor) == 74_807_296 and sha256(editor) == EDITOR_SHA256,
            "editor.exe size/hash mismatch")
    byte_checks = [
        (0xF49D3C, "da ef ff ff", "factory type-1 rel32 entry"),
        (0x3BCD6FC, "ba 70 00 00 00", "112-byte allocation wrapper"),
        (0x1AAC700, "2e 3f 41 56 42 41 53 49 43 5f 50 45 52 53 4f 4e 40 64 62 40 40 00", "BASIC_PERSON RTTI"),
        (0x187B3C0, "70 fd e4 40 01 00 00 00", "slot-19 reader pointer"),
        (0xE4F370, "41 57 41 56 56 57 55 53 48 83 ec 48", "reader entry"),
        (0xE4F393, "41 b8 01 00 00 00", "first reader width"),
        (0xE4F42E, "3c 04", "reader class-4 compare"),
        (0xE4F430, "75 4c", "non-class-4 branch"),
        (0xE4F445, "ff 50 28", "class-4 first width-2 stream call"),
        (0xE4F471, "ff 50 28", "class-4 second width-2 stream call"),
    ]
    evidence = []
    for off, expected_hex, label in byte_checks:
        expected = bytes.fromhex(expected_hex)
        actual = editor[off:off + len(expected)]
        require(actual == expected, f"editor.exe+0x{off:x}: {label} bytes changed")
        evidence.append({"file": "editor.exe", "file_offset": hex(off), "bytes": hx(actual), "claim": label})

    base = 0xF49D38
    handler = base + struct.unpack_from("<i", editor, 0xF49D3C)[0]
    require(handler == 0xF48D12, "type-1 jump-table target mismatch")
    reader_va = struct.unpack_from("<Q", editor, 0x187B3C0)[0]
    reader_off = pe_file_offset_for_va(editor, reader_va)
    require(reader_off == 0xE4F370, "slot-19 pointer does not map to reader entry")

    try:
        import capstone
    except ImportError as exc:
        raise RuntimeError("capstone unavailable; do not install dependencies for this task") from exc
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    observed = []
    for start, role in WIDTH_WINDOWS:
        for ins in md.disasm(editor[start:start + 0x800], start):
            if (ins.mnemonic == "mov" and len(ins.operands) == 2
                    and ins.reg_name(ins.operands[0].reg) == "r8d"
                    and ins.operands[1].type == capstone.x86.X86_OP_IMM):
                observed.append((ins.address, ins.operands[1].imm & 0xFFFFFFFF, role, bytes(ins.bytes)))
    require([(off, width) for off, width, _, _ in observed] == EXPECTED_WIDTHS,
            "27-instruction BASIC_PERSON width census mismatch")
    widths = []
    for off, width, role, encoded in observed:
        expected = b"\x41\xb8" + struct.pack("<I", width)
        require(encoded == expected, f"width encoding mismatch at editor.exe+0x{off:x}")
        widths.append({"file": "editor.exe", "file_offset": hex(off), "bytes": hx(encoded),
                       "width": width, "instruction": f"mov r8d, {width}", "scan_role": role})
    return {
        "editor": {"file": EDITOR_PATH.as_posix(), "bytes": len(editor), "sha256": EDITOR_SHA256},
        "factory_type1": {"entry_file_offset": "0xf49d3c", "entry_bytes": "da ef ff ff",
                           "rel32_base_file_offset": "0xf49d38", "handler_file_offset": hex(handler)},
        "basic_person": {"rtti_file_offset": "0x1aac700", "rtti_bytes": hx(editor[0x1AAC700:0x1AAC700 + 22]),
                         "allocation_size": 112, "allocation_file_offset": "0x3bcd6fc",
                         "slot19_pointer_file_offset": "0x187b3c0", "slot19_pointer_bytes": hx(editor[0x187B3C0:0x187B3C8]),
                         "reader_va": hex(reader_va), "reader_file_offset": hex(reader_off),
                         "reader_entry_bytes": hx(editor[reader_off:reader_off + 12])},
        "width_instruction_count": len(widths),
        "width_instructions": widths,
        "class4_path": {
            "class_compare": {"file_offset": "0xe4f42e", "bytes": "3c 04", "instruction": "cmp al, 4"},
            "non_class4_branch": {"file_offset": "0xe4f430", "bytes": "75 4c", "instruction": "jne 0xe4f47e"},
            "stream_widths": [
                {"file_offset": "0xe4f43c", "bytes": hx(editor[0xE4F43C:0xE4F442]), "width": 2,
                 "call_file_offset": "0xe4f445", "destination_instruction_file_offset": "0xe4f432"},
                {"file_offset": "0xe4f468", "bytes": hx(editor[0xE4F468:0xE4F46E]), "width": 2,
                 "call_file_offset": "0xe4f471", "destination_instruction_file_offset": "0xe4f452"},
            ],
        },
        "byte_evidence": evidence,
    }


def archive_facts(reader, archive_name: str) -> dict:
    path, blob, layout = reader["_entries"](DB_DIR, archive_name)
    got_sha = sha256(blob)
    require(got_sha == ARCHIVE_SHA256[archive_name], f"{archive_name} SHA-256 mismatch")
    ids, entries = [], []
    for entry in layout["entries"]:
        table_id = reader["_table_id"](entry["path"])
        if table_id is not None:
            ids.append(table_id)
        entries.append({**entry, "table_id": table_id,
                        "entry_type": "numeric_table" if table_id is not None else "auxiliary"})
    toc = layout["toc_offset"]
    require(blob[toc:toc + len(FMF_PREFIX)] == FMF_PREFIX,
            f"{archive_name} TOC FMF/Zstd prefix mismatch")
    return {
        "file": path.as_posix(), "bytes": len(blob), "sha256": got_sha,
        "outer_header": {"file_offset": "0x0", "bytes": hx(blob[:8])},
        "fmf": {"present": True, "container_offset": layout["container_offset"],
                "primary_header_file_offset": layout["container_offset"],
                "primary_header_bytes": hx(blob[layout["container_offset"]:layout["container_offset"] + 9]),
                "data_base": layout["data_base"], "toc_offset": toc,
                "toc_header_bytes": hx(blob[toc:toc + len(FMF_PREFIX)]),
                "directory_size": layout["directory_size"], "directory_entry_count": len(entries),
                "numeric_table_count": len(ids), "numeric_table_ids_in_directory_order": ids,
                "entries": entries},
    }


def build_output() -> dict:
    require(sys.version_info[:2] == (3, 12), "run with py -V:3.12 -I -B")
    reader = load_old_reader()
    snapshot_hashes = manifest_snapshot_hashes()
    basic = BASIC_PATH.read_bytes()
    require(len(basic) == 12_934_775 and sha256(basic) == BASIC_SHA256,
            "basic_people_db.dat size/SHA-256 mismatch")
    require(basic[:8] == bytes.fromhex("03 01 74 61 64 2e f1 0d"),
            "basic_people_db.dat outer TAD header mismatch")
    require(basic[8:12] == ZSTD_MAGIC, "no direct Zstandard frame at file+0x8")
    marker_offsets = []
    search = 0
    while True:
        search = basic.find(FMF_PREFIX, search)
        if search < 0:
            break
        marker_offsets.append(search)
        search += 1
    fmf_header_offsets = []
    search = 0
    while True:
        search = basic.find(FMF_MAGIC, search)
        if search < 0:
            break
        fmf_header_offsets.append(search)
        search += 1
    require(not marker_offsets and not fmf_header_offsets,
            "FMF header/directory-frame signature unexpectedly occurs in basic_people_db.dat")

    zstd = reader["_zstd_module"]()
    frame = zstd.ZstdDecompressor().decompressobj()
    raw = frame.decompress(basic[8:])
    require(frame.eof and not frame.unused_data and not frame.unconsumed_tail,
            "basic_people_db.dat is not exactly one fully consumed Zstandard frame")
    require(len(raw) == 54_060_043 and sha256(raw) == RAW_SHA256,
            "decompressed basic_people payload size/SHA-256 mismatch")
    rows = parse_rows(raw)
    require(rows["header_count"] == 658_011 and rows["flag"] == 0,
            "basic_people row count/flag mismatch")
    require(rows["class_counts"] == {1: 166_064, 2: 476_158, 3: 4_757, 4: 9_839, 5: 1_193},
            "basic_people class counts mismatch")
    require(rows["rows_end_offset"] == 54_060_034 and len(rows["trailing_bytes"]) == 9,
            "basic_people payload end/remaining-byte closure mismatch")
    require(rows["trailing_bytes"] == bytes.fromhex("00 00 00 00 01 4c bd 54 77"),
            "basic_people trailing bytes changed")
    require(rows["ordinal_mismatch_count"] == 0 and rows["repeated_identifier_mismatch_count"] == 0,
            "basic_people ordinal/repeated-identifier invariant failed")

    editor = EDITOR_PATH.read_bytes()
    static = static_evidence(editor)
    # Verify the class-4 branch against the raw row bytes at their exact offsets.
    c4 = rows["sample_rows_by_class"][4]
    c4_start = c4["payload_offset"]
    c4_row = raw[c4_start:c4_start + c4["row_length"]]
    c4_spans = [
        {"reader_width": 1, "reader_instruction_file_offset": "0xe4f393",
         "payload_file_offset": c4_start + 1, "bytes": hx(c4_row[1:2])},
        {"reader_width": 2, "reader_instruction_file_offset": "0xe4f43c",
         "payload_file_offset": c4_start + 2, "bytes": hx(c4_row[2:4])},
        {"reader_width": 2, "reader_instruction_file_offset": "0xe4f468",
         "payload_file_offset": c4_start + 4, "bytes": hx(c4_row[4:6])},
    ]
    require(c4_row[:6] == bytes.fromhex("11 04 af 00 00 00"),
            "class-4 row prefix changed")
    require([len(bytes.fromhex(x["bytes"])) for x in c4_spans] == [1, 2, 2],
            "class-4 static width spans do not match row bytes")

    archives = {name.removesuffix(".dat"): archive_facts(reader, name)
                for name in ("client_db.dat", "server_db.dat")}
    basic_source = {
        "file": BASIC_PATH.as_posix(), "bytes": len(basic), "sha256": BASIC_SHA256,
        "outer_header": {"file_offset": "0x0", "bytes": hx(basic[:8]), "version_u16_le": 3569},
        "direct_zstd": {"file_offset": "0x8", "frame_magic": hx(basic[8:12]),
                         "compressed_bytes_after_header": len(basic) - 8,
                         "single_frame_consumed_all_input": True},
        "fmf_directory_frame": {"present": False, "fmf_header_bytes": hx(FMF_MAGIC),
                                 "matching_fmf_header_offsets": fmf_header_offsets,
                                 "search_prefix_bytes": hx(FMF_PREFIX),
                                 "matching_file_offsets": marker_offsets,
                                 "directory_entries": [], "numeric_table_ids": [],
                                 "note": "No FMF directory exists here; [] is not an enumeration of logical tables."},
    }
    row_summary = {
        "payload_offset_domain": "decompressed basic_people_db.dat Zstandard frame",
        "payload_bytes": len(raw), "payload_sha256": RAW_SHA256,
        "header": {"count_file_offset": "0x0", "count_bytes": hx(raw[:4]),
                   "count_u32_le": rows["header_count"], "flag_file_offset": "0x4",
                   "flag_bytes": hx(raw[4:5]), "first_row_file_offset": 5},
        "row_format": {
            "prefix": "u8 tag=0x11 | u8 class_id",
            "class_lengths_bytes": {str(k): v for k, v in CLASS_LENGTHS.items()},
            "row_start_formula": "start[0]=5; start[n+1]=start[n]+class_length(class_id[n])",
            "stride": "variable by class (83 B for classes 1/2/3; 34 B for class 4; 22 B for class 5)",
            "class_counts": {str(k): v for k, v in sorted(rows["class_counts"].items())},
            "rows": rows["row_count_parsed"],
            "row_bytes_consumed": rows["rows_end_offset"] - 5,
            "end_offset_exclusive": rows["rows_end_offset"],
            "trailing_bytes": {"offset": rows["rows_end_offset"], "length": len(rows["trailing_bytes"]),
                               "bytes": hx(rows["trailing_bytes"])},
            "closure": "5-byte header + sum(per-class row lengths) = 54,060,034; 9 trailing bytes close to payload size 54,060,043",
        },
        "identity_block": {
            "relative_location": "row_end-12",
            "shape": "u32 ordinal | u32 repeated_identifier_candidate | u32 same_identifier_candidate",
            "rows_checked": rows["row_count_parsed"],
            "ordinal_is_0_based_contiguous": rows["ordinal_mismatch_count"] == 0,
            "duplicate_u32_pair_matches": rows["repeated_identifier_mismatch_count"] == 0,
            "semantic_label": "do not promote to duni/rdui without an independent join",
        },
        "samples_by_class": [rows["sample_rows_by_class"][key] for key in sorted(rows["sample_rows_by_class"])],
    }
    return {
        "task": "t01-j basic_people_db.dat reconnaissance",
        "acceptance": {
            "met": True,
            "outcome": "direct_tad_zstd_not_fmf; variable_class_rows_recovered",
            "directory_enumeration": {"applicable": False, "reason": "input is a direct Zstandard resource, not an FMF archive"},
            "row_frame_recovered": True,
            "rows": rows["row_count_parsed"],
            "full_27_width_to_all_row_fields_linked": False,
            "five_sample_rows_checked": len(rows["sample_rows_by_class"]),
            "person_storehouse_hypothesis": "strong candidate; partial L3 serializer-prefix correspondence only",
            "L4": 0,
        },
        "python": "py -V:3.12 -I -B",
        "read_only_inputs": True,
        "sources": {
            "basic_people_db": basic_source,
            "main_archive_comparison": archives,
            "frozen_snapshot_hashes_checked_against_MANIFEST": snapshot_hashes,
        },
        "row_frame": row_summary,
        "BASIC_PERSON_reader": {
            **static,
            "row_byte_comparison": {
                "status": "partial L3 alignment; no field names assigned",
                "class4_sample": {"ordinal": c4["ordinal"], "row_payload_offset": c4_start,
                                   "row_length": c4["row_length"], "row_prefix_file_offset": c4_start,
                                   "row_prefix_bytes": hx(c4_row[:6]),
                                   "static_width_segments": c4_spans,
                                   "explanation": "reader first reads class byte (1 B); cmp al,4 selects two following 2-B reads; raw class-4 row matches 04 | af 00 | 00 00 at these exact payload offsets."},
                "caveat": "The 27 static mov-r8d instructions include mutually exclusive width alternatives and helper paths; do not concatenate their widths as one linear record layout. Only the class-4 prefix path is byte-aligned here; remainder of all variants is not claimed recovered.",
            },
        },
        "negative_controls": {
            "basic_file_contains_fmf_directory_signature": False,
            "exact_single_zstd_frame": True,
            "row_tag_class_and_identity_checks": "658,011/658,011 passed",
            "factory_type_id_1_equals_archive_table_id_1": False,
            "duni_or_rdui_semantics_assigned_to_repeated_identifier": False,
        },
    }


def strict_parse_rows(raw: bytes) -> dict:
    result = parse_rows(raw)
    require(result["ordinal_mismatch_count"] == 0, "row ordinals are not contiguous")
    require(result["repeated_identifier_mismatch_count"] == 0, "repeated identifier pair mismatch")
    return result


def expect_failure(fn, label: str) -> None:
    try:
        fn()
    except (ValueError, CheckFailure):
        return
    raise CheckFailure(f"negative control unexpectedly passed: {label}")


def run_selftest() -> dict:
    output = build_output()
    # Synthetic positive: one 83-byte record with 0x11/class-1 prefix and trailer.
    row = bytearray(83)
    row[:2] = b"\x11\x01"
    struct.pack_into("<III", row, 71, 0, 17, 17)
    synthetic = struct.pack("<I", 1) + b"\x00" + row + bytes(9)
    parsed = parse_rows(synthetic)
    require(parsed["row_count_parsed"] == 1 and parsed["rows_end_offset"] == 88,
            "synthetic row positive control failed")
    wrong_tag = bytearray(synthetic)
    wrong_tag[5] = 0x12
    expect_failure(lambda: parse_rows(bytes(wrong_tag)), "wrong row tag")
    wrong_identity = bytearray(synthetic)
    struct.pack_into("<I", wrong_identity, 5 + 83 - 4, 18)
    expect_failure(lambda: strict_parse_rows(bytes(wrong_identity)), "non-repeated identity")
    wrong_ordinal = bytearray(synthetic)
    struct.pack_into("<I", wrong_ordinal, 5 + 83 - 12, 1)
    expect_failure(lambda: strict_parse_rows(bytes(wrong_ordinal)), "wrong ordinal")

    # The two wrapper shapes must not be conflated.
    require(not (DAT_MAGIC + bytes.fromhex("f1 0d") + ZSTD_MAGIC).startswith(DAT_MAGIC + FMF_MAGIC),
            "direct-Zstd negative wrapper control failed")
    require((DAT_MAGIC + FMF_MAGIC + bytes(16)).startswith(DAT_MAGIC + FMF_MAGIC),
            "FMF positive wrapper control failed")
    stored = HERE / "output.json"
    require(stored.is_file(), "output.json missing; run --write before --selftest")
    disk = json.loads(stored.read_text(encoding="utf-8"))
    require(disk == output, "output.json differs from a fresh read-only reconstruction")
    print("PASS: basic_people direct-Zstd wrapper, absence of FMF directory, and main-archive contrast")
    print("PASS: full decompression hash, 658,011 class-sized rows, 9-byte tail closure, and identity invariants")
    print("PASS: editor.exe BASIC_PERSON anchors and all 27 static width instructions")
    print("PASS: class-4 reader width path matches payload bytes; full field layout remains explicitly partial")
    print("PASS: synthetic positive/negative row controls and output.json reconstruction")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only basic_people_db.dat directory/row-frame verifier")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--selftest", action="store_true", help="rebuild and verify all evidence; no files written")
    group.add_argument("--write", action="store_true", help="write reconstructed output.json in this directory")
    args = parser.parse_args()
    if not args.selftest and not args.write:
        parser.print_help()
        return 2
    try:
        output = run_selftest() if args.selftest else build_output()
        if args.write:
            target = HERE / "output.json"
            target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"WROTE: {target.as_posix()}")
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError, KeyError, IndexError, ImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
