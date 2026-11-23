#!/usr/bin/env python3
"""Read-only t01-k checks for BASIC_PERSON reader/row alignment.

Run from the fm24-db workspace with Python 3.12:
  py -V:3.12 -I -B scratch/t01/inbox/t01k/verify.py --help
  py -V:3.12 -I -B scratch/t01/inbox/t01k/verify.py --selftest

The game database, editor.exe, frozen schema snapshot, and old decoder are
read-only. This verifier writes no files.
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
BASIC_PATH = Path(r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\basic_people_db.dat")
EDITOR_PATH = Path(r"D:\tmp2b\fm24\input\editor.exe")
OLD_READER_PATH = Path(r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
MASTER_PATH = ROOT / "evidence/fm24/reports/editor_schema/master.json"
BASIC_SHA256 = "2ac7da37e7b1df755b76c16cf39c569cb0a1e96509a7557c2ab9acf5d67f48bc"
RAW_SHA256 = "16709b0b5dda358179313c19ef58d0f78bff259cde68a0dcd1bb01c9589d35a5"
EDITOR_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
MASTER_SHA256 = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
CLASS_LENGTHS = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
EXPECTED_WIDTHS = [
    (0xE4F393, 1), (0xE4F43C, 2), (0xE4F468, 2),
    (0xE4F4F6, 8), (0xE4F4FE, 4), (0xE4F542, 8), (0xE4F54A, 4),
    (0xE4F57F, 8), (0xE4F587, 4), (0xE4F5BA, 4), (0xE4F5DA, 4),
    (0xE4F5FA, 2), (0xE4F61A, 2), (0xE4F63A, 2), (0xE4F65A, 2),
    (0xE4F67A, 2), (0xE4F69A, 2), (0xE4F6BA, 2), (0xE4F6DA, 2),
    (0xE4F6FA, 2), (0xE4F71A, 1), (0xE4F73A, 1), (0xE4F75A, 1),
    (0x3DC0241, 8), (0x3DC027B, 12), (0x3C6E121, 8), (0x3C6E129, 4),
]
GETTER_EVIDENCE = {
    "PNJO": (0xE50337, "81 fa 4f 4a 4e 50", 0xE5033D, "0f 85 83 14 00 00", 0xE50343, "0f b7 7f 62"),
    "duni": (0xE50480, "81 fa 69 6e 75 64", 0xE50486, "0f 84 8e 09 00 00", 0xE50E1A, "8b 7f 0c"),
    "Pcti": (0xE50534, "81 fa 69 74 63 50", 0xE5053A, "0f 84 03 0a 00 00", 0xE50F43, "48 8b 47 20"),
    "Pdob": (0xE506A5, "81 fa 62 6f 64 50", 0xE506AB, "0f 84 a7 0a 00 00", 0xE51158, "0f b7 7f 5a"),
    "Piap": (0xE50792, "81 fa 70 61 69 50", 0xE50798, "0f 84 e0 0d 00 00", 0xE5157E, "0f b6 7f 64"),
    "Pnai": (0xE5079E, "81 fa 69 61 6e 50", 0xE507A4, "0f 85 1c 10 00 00", 0xE507AA, "48 8b 47 28"),
    "PCJO": (0xE507BC, "81 fa 4f 4a 43 50", 0xE507C2, "0f 84 15 0e 00 00", 0xE515DD, "0f b7 7f 5e"),
    "Pnti": (0xE5094D, "81 fa 69 74 6e 50", 0xE50953, "0f 84 20 0d 00 00", 0xE51679, "48 8b 47 30"),
    "Ptyp": (0xE50959, "81 fa 70 79 74 50", 0xE5095F, "0f 85 61 0e 00 00", 0xE50965, "0f be 7f 65"),
    "PSJO": (0xE509D0, "81 fa 4f 4a 53 50", 0xE509D6, "0f 85 ea 0d 00 00", 0xE509DC, "0f b7 7f 60"),
}


class CheckFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CheckFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hx(data: bytes) -> str:
    return data.hex(" ")


def parse_rows(raw: bytes) -> dict:
    if len(raw) < 5:
        raise ValueError("truncated payload header")
    count = struct.unpack_from("<I", raw, 0)[0]
    pos = 5
    class_counts = {c: 0 for c in CLASS_LENGTHS}
    samples = {}
    for ordinal in range(count):
        if pos + 2 > len(raw):
            raise ValueError(f"truncated row header at payload+0x{pos:x}")
        tag, class_id = raw[pos], raw[pos + 1]
        if tag != 0x11:
            raise ValueError(f"bad row tag at payload+0x{pos:x}: {tag:#x}")
        if class_id not in CLASS_LENGTHS:
            raise ValueError(f"unknown class at payload+0x{pos + 1:x}: {class_id}")
        row_len = CLASS_LENGTHS[class_id]
        end = pos + row_len
        if end > len(raw):
            raise ValueError(f"row {ordinal} overruns payload")
        stored_ordinal, id_a, id_b = struct.unpack_from("<III", raw, end - 12)
        if stored_ordinal != ordinal:
            raise ValueError(f"ordinal mismatch at row {ordinal}: {stored_ordinal}")
        if id_a != id_b:
            raise ValueError(f"repeated-ID dwords differ at row {ordinal}")
        class_counts[class_id] += 1
        if class_id not in samples:
            row = raw[pos:end]
            samples[class_id] = {
                "ordinal": ordinal,
                "payload_offset": pos,
                "row_length": row_len,
                "row_hex": hx(row),
                "identity_offset": end - 12,
                "identity_hex": hx(row[-12:]),
            }
        pos = end
    return {
        "count": count,
        "rows_end": pos,
        "class_counts": class_counts,
        "samples": samples,
        "trailing": raw[pos:],
    }


def expected_bytes(data: bytes, offset: int, hex_text: str, label: str) -> None:
    expected = bytes.fromhex(hex_text)
    actual = data[offset:offset + len(expected)]
    require(actual == expected, f"{label} changed at editor.exe+0x{offset:x}: {hx(actual)}")


def static_checks(editor: bytes) -> None:
    require(len(editor) == 74_807_296 and sha256(editor) == EDITOR_SHA256,
            "editor.exe size/SHA-256 mismatch")
    checks = [
        (0x1AAC700, "2e 3f 41 56 42 41 53 49 43 5f 50 45 52 53 4f 4e 40 64 62 40 40 00", "BASIC_PERSON RTTI"),
        (0x187B328, "80 3d e5 40 01 00 00 00", "BASIC_PERSON vtable slot 0"),
        (0x187B338, "d0 0c e5 40 01 00 00 00", "BASIC_PERSON vtable slot 2 getter"),
        (0x187B3C0, "70 fd e4 40 01 00 00 00", "BASIC_PERSON reader slot 19"),
        (0xE4F370, "41 57 41 56 56 57 55 53 48 83 ec 48", "reader entry"),
        (0xE4F393, "41 b8 01 00 00 00", "read class byte: width 1"),
        (0xE4F3C8, "ba 20 00 09 00", "first class mask 0x90020"),
        (0xE4F3CD, "0f a3 ca", "first class bit test"),
        (0xE4F3D0, "0f 83 ff 00 00 00", "class bit clear branches to pre-read"),
        (0xE4F3E7, "ba 70 01 0d 00", "second class mask 0xd0170"),
        (0xE4F432, "48 8d 53 52", "class-4 first destination object+0x52"),
        (0xE4F42E, "3c 04", "class-4 comparison"),
        (0xE4F430, "75 4c", "non-class-4 branch"),
        (0xE4F43C, "41 b8 02 00 00 00", "class-4-branch width 2"),
        (0xE4F445, "ff 50 28", "class-4 first stream call"),
        (0xE4F468, "41 b8 02 00 00 00", "class-4-branch width 2"),
        (0xE4F471, "ff 50 28", "class-4 second stream call"),
        (0xE4F4D5, "80 3d 77 04 d1 00 00", "first runtime-width selector"),
        (0xE4F4EB, "74 11", "first runtime-width branch"),
        (0xE4F4ED, "80 3d 38 fd d0 00 00", "second runtime-width selector"),
        (0xE4F4F4, "75 08", "second runtime-width branch"),
        (0xE4F4F6, "41 b8 08 00 00 00", "pre-class-4 alternative width 8"),
        (0xE4F4FE, "41 b8 04 00 00 00", "pre-class-4 alternative width 4"),
        (0xE4F507, "ff d0", "pre-class-4 stream call"),
        (0xE4F542, "41 b8 08 00 00 00", "common alternative width 8"),
        (0xE4F54A, "41 b8 04 00 00 00", "common alternative width 4"),
        (0xE4F57F, "41 b8 08 00 00 00", "common alternative width 8"),
        (0xE4F587, "41 b8 04 00 00 00", "common alternative width 4"),
        (0xE4F452, "48 8d 53 5a", "class-4 second destination object+0x5a"),
        (0xE4F4DC, "48 8d 53 30", "pre-class-4 destination object+0x30"),
        (0xE4F529, "48 8d 53 20", "common destination object+0x20"),
        (0xE4F566, "48 8d 53 28", "common destination object+0x28"),
        (0xE4F59C, "48 8d 53 38", "unclosed-helper destination object+0x38"),
        (0xE4F5A3, "e8 f8 2b 16 00", "unclosed helper call"),
        (0xFB21A0, "e9 5b 6b e2 02", "unclosed helper thunk"),
    ]
    for off, raw, label in checks:
        expected_bytes(editor, off, raw, label)

    try:
        import capstone
    except ImportError as exc:
        raise RuntimeError("capstone unavailable; do not install dependencies") from exc
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    windows = ((0xE4F370, "reader"), (0x3DC0220, "callee-window"), (0x3C6E100, "callee-window"))
    observed = []
    for start, role in windows:
        for ins in md.disasm(editor[start:start + 0x800], start):
            if (ins.mnemonic == "mov" and len(ins.operands) == 2
                    and ins.reg_name(ins.operands[0].reg) == "r8d"
                    and ins.operands[1].type == capstone.x86.X86_OP_IMM):
                observed.append((ins.address, ins.operands[1].imm & 0xffffffff, role))
    require([(off, width) for off, width, _ in observed] == EXPECTED_WIDTHS,
            "27-site reader/callee width census changed")
    # Exactly 23 width immediates belong to the reader's code window; four are
    # in callee windows and are not extra sequential BASIC_PERSON row fields.
    require(sum(role == "reader" for _, _, role in observed) == 23,
            "reader-local width instruction count changed")

    for code, (cmp_off, cmp_hex, branch_off, branch_hex, member_off, member_hex) in GETTER_EVIDENCE.items():
        expected_bytes(editor, cmp_off, cmp_hex, f"{code} getter compare")
        expected_bytes(editor, branch_off, branch_hex, f"{code} getter equality/default branch")
        expected_bytes(editor, member_off, member_hex, f"{code} getter member access")

    # BASIC_PERSON slot 2 points to file offset 0xe502d0; its field-code register
    # is EDX (unlike the ESI convention in the nation getter example).
    getter_va = struct.unpack_from("<Q", editor, 0x187B338)[0]
    require(getter_va == 0x140E50CD0 and getter_va - 0x140000000 - 0xA00 == 0xE502D0,
            "getter vtable pointer does not resolve to 0xe502d0")


def run_selftest() -> None:
    require(sys.version_info[:2] == (3, 12), "run with py -V:3.12 -I -B")
    require(sha256(MASTER_PATH.read_bytes()) == MASTER_SHA256,
            "master.json differs from the frozen t01f-verified snapshot")
    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    person = master["entities"]["person.xml"]
    require(len(person) == 1 and person[0]["id"] == "pers" and len(person[0]["fields"]) == 271,
            "person.xml#pers schema census mismatch")
    person_fields = {field["field"]: field.get("name") for field in person[0]["fields"]}
    expected_person_names = {
        "Ptyp": "Person Type", "Pdob": "Date Of Birth", "Pnti": "Nation",
        "Pnai": "Nation", "Pcti": "Club", "PCJO": "Job", "PNJO": "Job",
        "PSJO": "Secondary Job", "Piap": "International Apps", "duni": "Unique ID",
    }
    require(all(person_fields.get(code) == name for code, name in expected_person_names.items()),
            "person schema field labels changed")

    if not OLD_READER_PATH.is_file():
        raise FileNotFoundError(f"read-only decoder unavailable: {OLD_READER_PATH}")
    old = runpy.run_path(str(OLD_READER_PATH))
    basic = BASIC_PATH.read_bytes()
    require(len(basic) == 12_934_775 and sha256(basic) == BASIC_SHA256,
            "basic_people_db.dat size/SHA-256 mismatch")
    require(basic[:8] == bytes.fromhex("03 01 74 61 64 2e f1 0d") and basic[8:12] == bytes.fromhex("28 b5 2f fd"),
            "basic_people wrapper/magic mismatch")
    raw = old["_stream_decompress"](basic[8:], 256 * 1024 * 1024)
    require(len(raw) == 54_060_043 and sha256(raw) == RAW_SHA256,
            "decompressed payload size/SHA-256 mismatch")
    rows = parse_rows(raw)
    require(rows["count"] == 658_011, "row count mismatch")
    require(rows["class_counts"] == {1: 166_064, 2: 476_158, 3: 4_757, 4: 9_839, 5: 1_193},
            "class count mismatch")
    require(rows["rows_end"] == 54_060_034 and rows["trailing"] == bytes.fromhex("00 00 00 00 01 4c bd 54 77"),
            "row-chain/trailing-byte closure mismatch")
    require(set(rows["samples"]) == set(CLASS_LENGTHS), "one sample per class was not recovered")
    expected_samples = {
        1: (0, 5), 2: (89, 7392), 3: (1155, 94939), 4: (972, 80681), 5: (656818, 54033788),
    }
    for class_id, (ordinal, offset) in expected_samples.items():
        sample = rows["samples"][class_id]
        require((sample["ordinal"], sample["payload_offset"]) == (ordinal, offset),
                f"class {class_id} first-sample location changed")
    class4 = raw[80681:80681 + 34]
    require(class4[:6] == bytes.fromhex("11 04 af 00 00 00"), "class-4 sample bytes changed")
    require(class4[22:] == bytes.fromhex("cc 03 00 00 d2 14 00 00 d2 14 00 00"),
            "class-4 sample identity bytes changed")

    editor = EDITOR_PATH.read_bytes()
    static_checks(editor)

    # Negative control: the class-4 compare is reached only after the earlier
    # 0x90020 bit test. Class 4 has bit 4 clear there, so a 4/8-byte stream read
    # to object+0x30 happens first. The later 2-byte reads therefore cannot be
    # assigned to row+2 and row+4 merely by concatenating 1+2+2 widths.
    require((0x90020 & (1 << 4)) == 0 and (0xD0170 & (1 << 4)) != 0,
            "class-4 bit-mask branch negative control failed")
    expected_bytes(editor, 0xE4F51C, "0f 86 c5 fe ff ff", "return to second class-mask test after pre-read")
    require(0xE4F3D0 + 6 + 0xFF == 0xE4F4D5
            and 0xE4F51C + 6 - 0x13B == 0xE4F3E7,
            "class-4 control-flow edges around the pre-read changed")
    require(0xE4F43C < 0xE4F468 and 0xE4F468 < 0xE4F47E,
            "class-4 direct-read branch order changed")
    # If the first width is 4 or 8, class-4 field reads at object+0x52/+0x5a
    # begin at row+6/+8 or row+10/+12 respectively, never row+2/+4.
    candidates = {(2 + width, 4 + width) for width in (4, 8)}
    require(candidates == {(6, 8), (10, 12)} and all(a != 2 and b != 4 for a, b in candidates),
            "class-4 shifted-offset control failed")
    require(class4[2:6] == bytes.fromhex("af 00 00 00")
            and class4[10:14] == bytes.fromhex("64 00 6c 07"),
            "class-4 sample does not demonstrate competing plausible spans")

    # The two mov-r8d sites in each 4/8 pair are mutually exclusive branch arms;
    # do not sum them into a single row width sequence.
    expected_bytes(editor, 0xE4F4EB, "74 11", "first width alternative branch")
    expected_bytes(editor, 0xE4F4F4, "75 08", "first width alternative branch")
    expected_bytes(editor, 0xE4F542, "41 b8 08 00 00 00", "8-byte arm")
    expected_bytes(editor, 0xE4F54A, "41 b8 04 00 00 00", "4-byte arm")

    # Synthetic positive/negative row controls, independent of the installed DB.
    good = bytearray(83)
    good[:2] = b"\x11\x01"
    struct.pack_into("<III", good, 71, 0, 0x1234, 0x1234)
    synthetic = struct.pack("<I", 1) + b"\x00" + good + bytes(9)
    require(parse_rows(synthetic)["count"] == 1, "synthetic positive row control failed")
    bad_tag = bytearray(synthetic)
    bad_tag[5] = 0x12
    try:
        parse_rows(bytes(bad_tag))
    except ValueError:
        pass
    else:
        raise CheckFailure("wrong-tag negative control unexpectedly passed")
    bad_id = bytearray(synthetic)
    struct.pack_into("<I", bad_id, 5 + 83 - 4, 0x1235)
    try:
        parse_rows(bytes(bad_id))
    except ValueError:
        pass
    else:
        raise CheckFailure("repeated-ID negative control unexpectedly passed")

    output_path = HERE / "output.json"
    require(output_path.is_file(), "output.json missing")
    output = json.loads(output_path.read_text(encoding="utf-8"))
    require(output["acceptance"]["outcome"] == "negative_result_reader_row_dispatch_variant",
            "output does not record the proved negative outcome")
    require(output["row_frame"]["rows"] == rows["count"], "output row count differs from fresh scan")
    out_samples = {int(item["class_id"]): item for item in output["samples_by_class"]}
    require(set(out_samples) == set(CLASS_LENGTHS), "output lacks five class samples")
    for class_id, sample in rows["samples"].items():
        item = out_samples[class_id]
        require(item["ordinal"] == sample["ordinal"]
                and item["payload_offset"] == sample["payload_offset"]
                and item["row_hex"] == sample["row_hex"],
                f"output class-{class_id} sample differs from fresh payload")
    require(output["acceptance"]["named_l3_fixed_row_offsets"] == 1,
            "output must not promote conditional offsets to fixed L3 claims")
    getter_map = output["getter_to_object_member"]["fields"]
    require(set(getter_map) == set(expected_person_names), "output getter map lost/added a schema code")
    require(getter_map["Ptyp"]["object_offset"] == "0x65"
            and getter_map["Pdob"]["object_offset"] == "0x5a"
            and getter_map["duni"]["row_link_status"].startswith("identity-tail candidate"),
            "output getter/member or duni-boundary labels changed")
    fixed = output["row_offset_map"]["class_1_2_3"]["fixed_l3_fields"]
    require(set(fixed) == {"Ptyp"} and fixed["Ptyp"]["row_offset"] == 1,
            "output fixed row-offset map overstates/loses the closed field")

    print("PASS: direct-Zstd payload hash; full 658,011-row chain, classes, IDs, and 9-byte tail")
    print("PASS: five class samples and exact BASIC_PERSON RTTI/vtable/reader/getter static bytes")
    print("PASS: 27-site width census; 23 reader-local sites distinguished from four callee sites")
    print("PASS: class-4 pre-read bitmask and mutually exclusive 4/8 widths refute naive 1+2+2 row offsets")
    print("PASS: schema hash/271 pers codes, getter-to-member anchors, and synthetic positive/negative controls")
    print("PASS: output.json agrees with fresh read-only reconstruction")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only t01-k BASIC_PERSON row-offset verifier")
    parser.add_argument("--selftest", action="store_true", help="rebuild all checks; do not write files")
    args = parser.parse_args()
    if not args.selftest:
        parser.print_help()
        return 2
    try:
        run_selftest()
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError, KeyError, IndexError, ImportError, struct.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
