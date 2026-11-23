#!/usr/bin/env python3
"""Read-only negative-result verifier for t01-i.

Run from the fm24-db workspace with: py -V:3.12 -I -B .../verify.py --selftest
No game/editor/IDA is launched and no files are written.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OLD_READER = Path("D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
DB_DIR = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
EDITOR = Path("D:/tmp2b/fm24/input/editor.exe")
CLIENT_SHA = "5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1"
SERVER_SHA = "99eed00bd26582648c0d3ff51b5c8e37a35b68c296a074e8fb476d1b3ca4a662"
EDITOR_SHA = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
BASIC_PEOPLE_SHA = "2ac7da37e7b1df755b76c16cf39c569cb0a1e96509a7557c2ab9acf5d67f48bc"
DIRECTORY_SNAPSHOT = "evidence/fm24/reports/dbdat_decode/client_db_directory.json"
DIRECTORY_SNAPSHOT_SHA = "90182a76d76674b52d06b79f15df0d6949ac1d4cd6a482170369fc3995a5e48b"


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_old_reader():
    if not OLD_READER.is_file():
        raise FileNotFoundError(f"read-only old decoder unavailable: {OLD_READER}")
    spec = importlib.util.spec_from_file_location("t01i_old_dbdat_reader", OLD_READER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load old decoder: {OLD_READER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def table_entries(reader, entries, table_id: int):
    return [e for e in entries if reader._table_id(e.get("path", "")) == table_id]


def run_selftest() -> None:
    reader = load_old_reader()

    editor_bytes = EDITOR.read_bytes()
    require(sha256(editor_bytes) == EDITOR_SHA, "editor.exe SHA-256 mismatch")
    static_checks = {
        "type-1 factory rel32 entry": (0xF49D3C, "da ef ff ff"),
        "factory allocation wrapper (112 B)": (0x3BCD6FC, "ba 70 00 00 00"),
        "BASIC_PERSON RTTI": (0x1AAC700, "2e 3f 41 56 42 41 53 49 43 5f 50 45 52 53 4f 4e 40 64 62 40 40 00"),
        "reader prologue": (0xE4F370, "41 57 41 56 56 57 55 53"),
        "first reader width instruction": (0xE4F393, "41 b8 01 00 00 00"),
    }
    for label, (offset, hex_bytes) in static_checks.items():
        expected = bytes.fromhex(hex_bytes)
        require(editor_bytes[offset:offset + len(expected)] == expected,
                f"{label} byte check failed at editor.exe+0x{offset:x}")

    h_path = ROOT / "scratch/t01/inbox/t01h/output.json"
    h = json.loads(h_path.read_text(encoding="utf-8"))
    item = next((x for x in h["census"] if x.get("type_id") == 1), None)
    require(item is not None, "t01h census lacks type-id 1")
    require(item["constructor_classes"][0]["rtti"]["name"] == ".?AVBASIC_PERSON@db@@",
            "t01h type-id 1 RTTI differs")
    slot_readers = item["reader"]["slot19_readers"]
    require(slot_readers and slot_readers[0]["entry_file_offset"] == "0xe4f370",
            "t01h reader entry differs")
    require(slot_readers[0]["width_count"] == 27, "t01h width count differs")

    archive_facts = {}
    expected_layouts = {
        "client_db.dat": {"data_base": 0x22, "toc_offset": 0xC81799, "directory_size": 1954, "table25_archive_offset": 0x4BC277},
        "server_db.dat": {"data_base": 0x22, "toc_offset": 0x36D7C94, "directory_size": 4784, "table25_archive_offset": 0x7F27B9},
    }
    for archive, expected_sha, expected_entries, expected_tables in (
        ("client_db.dat", CLIENT_SHA, 31, 20),
        ("server_db.dat", SERVER_SHA, 77, 59),
    ):
        archive_path, blob, layout = reader._entries(DB_DIR, archive)
        ids = [reader._table_id(e.get("path", "")) for e in layout["entries"]]
        ids = [table_id for table_id in ids if table_id is not None]
        require(sha256(blob) == expected_sha, f"{archive} SHA-256 mismatch")
        require(len(layout["entries"]) == expected_entries, f"{archive} directory entry count mismatch")
        require(len(ids) == expected_tables, f"{archive} table entry count mismatch")
        facts = expected_layouts[archive]
        require(layout["data_base"] == facts["data_base"] and
                layout["toc_offset"] == facts["toc_offset"] and
                layout["directory_size"] == facts["directory_size"],
                f"{archive} TOC/data-base framing mismatch")
        toc_header = bytes.fromhex("02 01 66 6d 66 2e 08 00 00 28 b5 2f fd")
        require(blob[layout["toc_offset"]:layout["toc_offset"] + len(toc_header)] == toc_header,
                f"{archive} TOC file-offset byte evidence mismatch")
        require(table_entries(reader, layout["entries"], 1) == [],
                f"unexpected exact table_1 entry in {archive}")
        archive_facts[archive] = {
            "sha256": sha256(blob),
            "directory_entries": len(layout["entries"]),
            "table_entries": len(ids),
            "table_1_entry_count": 0,
        }
        if archive == "client_db.dat":
            controls = table_entries(reader, layout["entries"], 25)
            require(len(controls) == 1, "client table_25 positive control missing")
            member_start = layout["data_base"] + controls[0]["offset"]
            require(member_start == facts["table25_archive_offset"] and
                    blob[member_start:member_start + 4] == bytes.fromhex("28 b5 2f fd"),
                    "client table_25 compressed-member offset/signature mismatch")
            raw = reader._decompress_entry(blob, layout["data_base"], controls[0])
            require(len(raw) == 894991 and raw[:8] == bytes.fromhex("03 01 74 61 64 2e f1 0d"),
                    "client table_25 payload framing differs")
            require(struct.unpack_from("<I", raw, 8)[0] == 7047,
                    "client table_25 count differs")

    # Exact-name negatives: a name-table entry is not a table, and table_25 is not table_1.
    require(reader._table_id("client_db/name_table_1.dat") is None,
            "name_table_1 was incorrectly classified as numeric table 1")
    require(reader._table_id("client_db/table_25.dat") == 25,
            "table_25 exact-name positive control failed")
    require(reader._table_id("client_db/table_25.dat") != 1,
            "table_25 was incorrectly classified as table 1")
    require(reader._table_id("client_db/table_01.dat") == 1,
            "synthetic exact table_1 positive control failed")

    manifest_path = ROOT / "evidence/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    record = next((x for x in manifest["files"] if x.get("path") == DIRECTORY_SNAPSHOT), None)
    require(record is not None and record["sha256"] == DIRECTORY_SNAPSHOT_SHA,
            "directory snapshot is not pinned by evidence/MANIFEST.json")
    frozen_path = ROOT / DIRECTORY_SNAPSHOT
    frozen_bytes = frozen_path.read_bytes()
    require(sha256(frozen_bytes) == DIRECTORY_SNAPSHOT_SHA,
            "frozen client directory snapshot hash mismatch")
    frozen = json.loads(frozen_bytes.decode("utf-8"))
    require(not any(reader._table_id(x.get("path", "")) == 1 for x in frozen),
            "frozen client directory snapshot contains table_1")

    # BASIC_PERSON-named archive is a separate file, not an FMF table_1 entry.
    basic_path = DB_DIR / "basic_people_db.dat"
    basic_bytes = basic_path.read_bytes()
    require(sha256(basic_bytes) == BASIC_PEOPLE_SHA, "basic_people_db.dat SHA-256 mismatch")
    require(basic_bytes[:10] == bytes.fromhex("03 01 74 61 64 2e f1 0d 28 b5"),
            "basic_people_db.dat direct-Zstd header differs")

    print("PASS: type-1 BASIC_PERSON static anchors and t01h width count verified")
    print("PASS: exact table_1 entry absent from client_db.dat and server_db.dat")
    print("PASS: frozen client directory snapshot hash and absence verified")
    print("PASS: table_25 payload is a working positive control; false table-name controls rejected")
    print("PASS: basic_people_db.dat is a separate direct-Zstd file (not classified as table_1)")
    for name, facts in archive_facts.items():
        print(f"INFO: {name}: {facts['directory_entries']} entries, {facts['table_entries']} numeric tables, table_1=0")
    print("RESULT: requested client_db/table_1 row mapping is blocked by absent input; no substitute mapping claimed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify t01-i's read-only table_1 negative result")
    parser.add_argument("--selftest", action="store_true", help="run byte, archive-directory, and negative-control checks")
    args = parser.parse_args()
    if not args.selftest:
        parser.print_help()
        return 2
    try:
        run_selftest()
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError, ImportError, KeyError, IndexError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
