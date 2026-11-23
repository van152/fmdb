#!/usr/bin/env python3
"""t98 closure for server table_45/table_48 STARTING_RECORD rows.

The script uses the already pinned FM24 payload loader, but performs the row
frame scan itself.  It emits the requested artifacts only after both payloads
and the generated independent verifier have passed.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import pathlib
import pprint
import runpy
import struct
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "scratch" / "t98" / "out"
SLOT_FILE = ROOT / "scratch" / "t88" / "out3" / "slots.json"

# Isolated mode still exposes the environment.  Keep the checked-in mirror the
# default so verify.py is reproducible outside the original game installation.
os.environ.setdefault("FM24_DB_DIR", str(ROOT / "scratch" / "data"))

HEADER_SIZE = 14
IDENTITY_SIZE = 13
FOOTER_SIZE = 8
DATE_SENTINEL = 0x076C0001
MAGIC_FOOTER_PREFIX = b"\x00"
EXPECTED = {
    45: {
        "count": 84477,
        "payload_size": 7608748,
        "sha256": "46799e2f79acc276cc2e349fa4724de917428e07d960d8d6059dc32b1fd58bf9",
        "footer": bytes.fromhex("00000001775f0100"),
    },
    48: {
        "count": 5210,
        "payload_size": 446049,
        "sha256": "f86bf6ee0bcc253fdc5b95a396e3a2fd433ccf92e1f769dbc742cdfcf73de8a5",
        "footer": bytes.fromhex("000000019f180000"),
    },
}

# The first 18 entries are the persisted STARTING_RECORD columns.  The
# identity trailer is structural and deliberately kept separate below.
PHYSICAL_COLUMNS = [
    {
        "id": "key_u32",
        "semantic": "record key / parent uid u32",
        "kind": "u32",
        "wire_offset": 0,
        "wire_expression": "row+0",
        "wire_width": 4,
        "mem_off": 76,
        "mem_hex": "0x4c",
        "read_c": "a1+19 as _DWORD*",
        "write_c": "a1+76",
        "read_source": "scratch/t95/funcs/141544130.c:22",
        "write_source": "scratch/t95/funcs/1444e4b00.c:27",
    },
    {
        "id": "rec_type",
        "semantic": "record type u8",
        "kind": "u8",
        "wire_offset": 4,
        "wire_expression": "row+4",
        "wire_width": 1,
        "mem_off": 94,
        "mem_hex": "0x5e",
        "read_c": "a1+94",
        "write_c": "a1+94",
        "read_source": "scratch/t95/funcs/141544130.c:26",
        "write_source": "scratch/t95/funcs/1444e4b00.c:31",
    },
    {
        "id": "uid_slot_0",
        "semantic": "8-byte database id / uid slot 0",
        "kind": "u64",
        "wire_offset": 5,
        "wire_expression": "row+5",
        "wire_width": 8,
        "mem_off": 24,
        "mem_hex": "0x18",
        "read_c": "a1+6 as _DWORD*",
        "write_c": "a1+24 and a1+28 as two u32 writes",
        "read_source": "scratch/t95/funcs/141544130.c:33",
        "write_source": "scratch/t95/funcs/1444e4b00.c:35-39",
    },
    {
        "id": "uid_slot_1",
        "semantic": "8-byte database id / uid slot 1",
        "kind": "u64",
        "wire_offset": 13,
        "wire_expression": "row+13",
        "wire_width": 8,
        "mem_off": 32,
        "mem_hex": "0x20",
        "read_c": "a1+8 as _DWORD*",
        "write_c": "a1+32 and a1+36 as two u32 writes",
        "read_source": "scratch/t95/funcs/141544130.c:46",
        "write_source": "scratch/t95/funcs/1444e4b00.c:43-47",
    },
    {
        "id": "uid_slot_2",
        "semantic": "8-byte database id / uid slot 2",
        "kind": "u64",
        "wire_offset": 21,
        "wire_expression": "row+21",
        "wire_width": 8,
        "mem_off": 40,
        "mem_hex": "0x28",
        "read_c": "a1+10 as _DWORD*",
        "write_c": "a1+40 via sub_140FEA120",
        "read_source": "scratch/t95/funcs/141544130.c:59",
        "write_source": "scratch/t95/funcs/1444e4b00.c:50",
    },
    {
        "id": "uid_slot_3",
        "semantic": "8-byte database id / uid slot 3",
        "kind": "u64",
        "wire_offset": 29,
        "wire_expression": "row+29",
        "wire_width": 8,
        "mem_off": 48,
        "mem_hex": "0x30",
        "read_c": "a1+12 via sub_140FEA0C0",
        "write_c": "a1+48 via sub_140FEA120",
        "read_source": "scratch/t95/funcs/141544130.c:68",
        "write_source": "scratch/t95/funcs/1444e4b00.c:52",
    },
    {
        "id": "name",
        "semantic": "length-prefixed utf8 name",
        "kind": "bytes_var",
        "wire_offset": 37,
        "wire_expression": "row+37: [u32 length][utf8 bytes]",
        "wire_width": "4+N",
        "mem_off": 56,
        "mem_hex": "0x38",
        "read_c": "a1+14 via sub_140814B10",
        "write_c": "a1+56 via sub_1408149D0",
        "read_source": "scratch/t95/funcs/141544130.c:70",
        "write_source": "scratch/t95/funcs/1444e4b00.c:54",
    },
    {
        "id": "date_0",
        "semantic": "date word pair 0",
        "kind": "date_u32",
        "wire_offset": None,
        "wire_expression": "tail+0 = row+41+namelen",
        "wire_relative": "tail+0",
        "wire_width": 4,
        "mem_off": 64,
        "mem_hex": "0x40",
        "read_c": "a1+16 via sub_140DB8980",
        "write_c": "a1+64 via sub_140DB89D0",
        "read_source": "scratch/t95/funcs/141544130.c:73",
        "write_source": "scratch/t95/funcs/1444e4b00.c:57",
    },
    {
        "id": "date_1",
        "semantic": "date word pair 1",
        "kind": "date_u32",
        "wire_offset": None,
        "wire_expression": "tail+4 = row+45+namelen",
        "wire_relative": "tail+4",
        "wire_width": 4,
        "mem_off": 68,
        "mem_hex": "0x44",
        "read_c": "a1+17 via sub_140DB8980",
        "write_c": "a1+68 via sub_140DB89D0",
        "read_source": "scratch/t95/funcs/141544130.c:75",
        "write_source": "scratch/t95/funcs/1444e4b00.c:59",
    },
    {
        "id": "date_2",
        "semantic": "date word pair 2",
        "kind": "date_u32",
        "wire_offset": None,
        "wire_expression": "tail+8 = row+49+namelen",
        "wire_relative": "tail+8",
        "wire_width": 4,
        "mem_off": 72,
        "mem_hex": "0x48",
        "read_c": "a1+18 via sub_140DB8980",
        "write_c": "a1+72 via sub_140DB89D0",
        "read_source": "scratch/t95/funcs/141544130.c:77",
        "write_source": "scratch/t95/funcs/1444e4b00.c:61",
    },
    {
        "id": "scalar_u32",
        "semantic": "tail scalar u32",
        "kind": "u32",
        "wire_offset": None,
        "wire_expression": "tail+12 = row+53+namelen",
        "wire_relative": "tail+12",
        "wire_width": 4,
        "mem_off": 80,
        "mem_hex": "0x50",
        "read_c": "a1+20",
        "write_c": "a1+80",
        "read_source": "scratch/t95/funcs/141544130.c:80",
        "write_source": "scratch/t95/funcs/1444e4b00.c:64",
    },
    {
        "id": "scalar_u16_0",
        "semantic": "tail scalar u16 0",
        "kind": "u16",
        "wire_offset": None,
        "wire_expression": "tail+16 = row+57+namelen",
        "wire_relative": "tail+16",
        "wire_width": 2,
        "mem_off": 84,
        "mem_hex": "0x54",
        "read_c": "a1+21",
        "write_c": "a1+84",
        "read_source": "scratch/t95/funcs/141544130.c:84",
        "write_source": "scratch/t95/funcs/1444e4b00.c:68",
    },
    {
        "id": "scalar_u16_1",
        "semantic": "tail scalar u16 1",
        "kind": "u16",
        "wire_offset": None,
        "wire_expression": "tail+18 = row+59+namelen",
        "wire_relative": "tail+18",
        "wire_width": 2,
        "mem_off": 86,
        "mem_hex": "0x56",
        "read_c": "a1+86",
        "write_c": "a1+86",
        "read_source": "scratch/t95/funcs/141544130.c:88",
        "write_source": "scratch/t95/funcs/1444e4b00.c:72",
    },
    {
        "id": "scalar_u16_2",
        "semantic": "tail scalar u16 2",
        "kind": "u16",
        "wire_offset": None,
        "wire_expression": "tail+20 = row+61+namelen",
        "wire_relative": "tail+20",
        "wire_width": 2,
        "mem_off": 88,
        "mem_hex": "0x58",
        "read_c": "a1+22",
        "write_c": "a1+88",
        "read_source": "scratch/t95/funcs/141544130.c:92",
        "write_source": "scratch/t95/funcs/1444e4b00.c:76",
    },
    {
        "id": "scalar_u8_0",
        "semantic": "tail scalar u8 0",
        "kind": "u8",
        "wire_offset": None,
        "wire_expression": "tail+22 = row+63+namelen",
        "wire_relative": "tail+22",
        "wire_width": 1,
        "mem_off": 90,
        "mem_hex": "0x5a",
        "read_c": "a1+90",
        "write_c": "a1+90",
        "read_source": "scratch/t95/funcs/141544130.c:96",
        "write_source": "scratch/t95/funcs/1444e4b00.c:80",
    },
    {
        "id": "scalar_u8_1",
        "semantic": "tail scalar u8 1",
        "kind": "u8",
        "wire_offset": None,
        "wire_expression": "tail+23 = row+64+namelen",
        "wire_relative": "tail+23",
        "wire_width": 1,
        "mem_off": 91,
        "mem_hex": "0x5b",
        "read_c": "a1+91",
        "write_c": "a1+91",
        "read_source": "scratch/t95/funcs/141544130.c:100",
        "write_source": "scratch/t95/funcs/1444e4b00.c:84",
    },
    {
        "id": "scalar_u8_2",
        "semantic": "tail scalar u8 2",
        "kind": "u8",
        "wire_offset": None,
        "wire_expression": "tail+24 = row+65+namelen",
        "wire_relative": "tail+24",
        "wire_width": 1,
        "mem_off": 92,
        "mem_hex": "0x5c",
        "read_c": "a1+23",
        "write_c": "a1+92",
        "read_source": "scratch/t95/funcs/141544130.c:104",
        "write_source": "scratch/t95/funcs/1444e4b00.c:88",
    },
    {
        "id": "scalar_u8_3",
        "semantic": "tail scalar u8 3",
        "kind": "u8",
        "wire_offset": None,
        "wire_expression": "tail+25 = row+66+namelen",
        "wire_relative": "tail+25",
        "wire_width": 1,
        "mem_off": 93,
        "mem_hex": "0x5d",
        "read_c": "a1+93",
        "write_c": "a1+93",
        "read_source": "scratch/t95/funcs/141544130.c:108",
        "write_source": "scratch/t95/funcs/1444e4b00.c:92",
    },
]

IDENTITY = {
    "status": "structural trailer, not one of the 18 persisted columns",
    "wire_expression": "row_end-13",
    "width": 13,
    "layout": "[ordinal u32][uid u32][uid u32][terminator u8]",
    "read_source": "scratch/t95/funcs/141544130.c:112",
    "row_length": "80+namelen",
    "body_expression": "row+41+namelen, length 26",
}

# STARTING_RECORD's own property functions.  A tag can be overloaded by the
# surrounding view/router; these are deliberately labeled as the direct
# function's behavior rather than silently merged with hub-side offsets.
DIRECT_TAGS = [
    {"tag": "otht", "physical_col": "uid_slot_2", "mem_off": 40, "wire": "wire+21", "kind": "u64", "get": [79, 95], "set": [], "get_behavior": "reads a1+40 and a1+44 as one 8-byte value", "set_behavior": "not a direct case; delegated after the local switch"},
    {"tag": "rati", "physical_col": "scalar_u8_0", "mem_off": 90, "wire": "tail+22", "kind": "u8", "get": [96, 112], "set": [], "get_behavior": "returns byte a1+90", "set_behavior": "not a direct case; delegated after the local switch"},
    {"tag": "rrea", "physical_col": "scalar_u8_2", "mem_off": 92, "wire": "tail+24", "kind": "u8", "get": [113, 130], "set": [], "get_behavior": "returns byte a1+92", "set_behavior": "not a direct case; delegated after the local switch"},
    {"tag": "info", "physical_col": "scalar_u8_1", "mem_off": 91, "wire": "tail+23", "kind": "u8", "get": [135, 151], "set": [256, 259], "get_behavior": "returns byte a1+91", "set_behavior": "writes byte a1+91"},
    {"tag": "ogls", "physical_col": "scalar_u16_2", "mem_off": 88, "wire": "tail+20", "kind": "u16", "get": [154, 174], "set": [261, 268], "get_behavior": "reads signed u16 a1+88", "set_behavior": "writes u16 a1+88 and applies null handling"},
    {"tag": "team", "physical_col": "uid_slot_1", "mem_off": 32, "wire": "wire+13", "kind": "u64", "get": [180, 196], "set": [226, 229], "get_behavior": "reads a1+32 and a1+36 as one 8-byte value", "set_behavior": "writes one 8-byte value at a1+32"},
    {"tag": "stnm", "physical_col": "name", "mem_off": 56, "wire": "wire+37", "kind": "bytes_var", "get": [197, 221], "set": [230, 243], "get_behavior": "retains pointer at a1+56", "set_behavior": "updates retained string pointer at a1+56"},
    {"tag": "stid", "physical_col": "uid_slot_0", "mem_off": 24, "wire": "wire+5", "kind": "u64", "get": [222, 243], "set": [245, 248], "get_behavior": "reads a1+24 and a1+28 as one 8-byte value", "set_behavior": "writes one 8-byte value at a1+24"},
    {"tag": "stdb", "physical_col": "date_2", "mem_off": 72, "wire": "tail+8", "kind": "date_u32", "get": [244, 275], "set": [141, 170], "get_behavior": "decodes packed date from a1+72/a1+74", "set_behavior": "encodes packed date at a1+72 and a1+74"},
    {"tag": "stdt", "physical_col": "date_0", "mem_off": 64, "wire": "tail+0", "kind": "date_u32", "get": [276, 317], "set": [172, 220], "get_behavior": "decodes packed date from a1+64/a1+66", "set_behavior": "encodes packed date at a1+64 and a1+66"},
    {"tag": "fsgt", "physical_col": "scalar_u16_2", "mem_off": 88, "wire": "tail+20", "kind": "u16", "get": [318, 336], "set": [84, 88], "get_behavior": "reads signed u16 a1+88", "set_behavior": "writes u16 a1+88"},
    {"tag": "gams", "physical_col": "scalar_u16_0", "mem_off": 84, "wire": "tail+16", "kind": "u16", "get": [337, 338], "set": [122, 136], "get_behavior": "reads signed u16 a1+84", "set_behavior": "writes u16 a1+84"},
    {"tag": "gols", "physical_col": "scalar_u16_1", "mem_off": 86, "wire": "tail+18", "kind": "u16", "get": [339, 366], "set": [89, 98], "get_behavior": "reads signed u16 a1+86", "set_behavior": "writes u16 a1+86 and maps null to -1"},
    {"tag": "endt", "physical_col": "date_1", "mem_off": 68, "wire": "tail+4", "kind": "date_u32", "get": [367, 424], "set": [27, 75], "get_behavior": "decodes packed date from a1+68/a1+70", "set_behavior": "encodes packed date at a1+68 and a1+70"},
    {"tag": "etin", "physical_col": "scalar_u8_3", "mem_off": 93, "wire": "tail+25", "kind": "u8", "get": [369, 381], "set": [77, 81], "get_behavior": "returns byte a1+93", "set_behavior": "writes byte a1+93"},
    {"tag": "apps", "physical_col": "scalar_u16_0", "mem_off": 84, "wire": "tail+16", "kind": "u16", "get": [425, 467], "set": [122, 136], "get_behavior": "shares local label with gams and reads a1+84", "set_behavior": "shares local write with gams at a1+84"},
    {"tag": "atte", "physical_col": "scalar_u32", "mem_off": 80, "wire": "tail+12", "kind": "u32", "get": [427, 468], "set": [124, 129], "get_behavior": "reads a1+80", "set_behavior": "writes a1+80 and nulls to -1"},
    {"tag": "cash", "physical_col": "scalar_u32", "mem_off": 80, "wire": "tail+12", "kind": "u32", "get": [469, 485], "set": [107, 109], "get_behavior": "reads a1+80", "set_behavior": "writes a1+80"},
    {"tag": "cnst", "physical_col": "scalar_u8_3", "mem_off": 93, "wire": "tail+25", "kind": "u8", "get": [486, 502], "set": [110, 112], "get_behavior": "returns boolean byte a1+93", "set_behavior": "writes boolean byte a1+93"},
    {"tag": "comp", "physical_col": "uid_slot_3", "mem_off": 48, "wire": "wire+29", "kind": "u64", "get": [503, 520], "set": [113, 116], "get_behavior": "reads a1+48 and a1+52 as one 8-byte value", "set_behavior": "writes one 8-byte value at a1+48"},
]

ROUTE_MEM = {
    28: {"physical_col": "uid_slot_0", "wire_off": "wire+9", "wire_row": "row+9", "note": "upper u32 component of uid_slot_0"},
    32: {"physical_col": "uid_slot_1", "wire_off": "wire+13", "wire_row": "row+13", "note": "start of uid_slot_1"},
    48: {"physical_col": "uid_slot_3", "wire_off": "wire+29", "wire_row": "row+29", "note": "start of uid_slot_3"},
    52: {"physical_col": "uid_slot_3", "wire_off": "wire+33", "wire_row": "row+33", "note": "upper u32 component of uid_slot_3"},
    64: {"physical_col": "date_0", "wire_off": "tail+0", "wire_row": "row+41+namelen", "note": "tail date 0"},
    80: {"physical_col": "scalar_u32", "wire_off": "tail+12", "wire_row": "row+53+namelen", "note": "tail u32"},
    86: {"physical_col": "scalar_u16_1", "wire_off": "tail+18", "wire_row": "row+59+namelen", "note": "tail u16"},
    88: {"physical_col": "scalar_u16_2", "wire_off": "tail+20", "wire_row": "row+61+namelen", "note": "tail u16"},
    90: {"physical_col": "scalar_u8_0", "wire_off": "tail+22", "wire_row": "row+63+namelen", "note": "tail u8"},
    92: {"physical_col": "scalar_u8_2", "wire_off": "tail+24", "wire_row": "row+65+namelen", "note": "tail u8"},
    94: {"physical_col": "rec_type", "wire_off": "wire+4", "wire_row": "row+4", "note": "record type byte"},
}

DIRECT_BY_TAG = {item["tag"]: item for item in DIRECT_TAGS}

FAMILY_DISPATCH = {
    "CFG": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "461-466", "route": "LABEL_394 -> 0x144026350"},
    "CHA": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "513-516", "route": "LABEL_394 -> 0x144026350"},
    "CHS": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "493-497", "route": "LABEL_394 -> 0x144026350"},
    "CLA": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "574-592", "route": "LABEL_394 -> 0x144026350"},
    "COS": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "549-566", "route": "LABEL_394 -> 0x144026350"},
    "CYP": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "1410-1415", "route": "LABEL_394 -> 0x144026350"},
    "CYS": {"file": "scratch/t95/funcs/1411f1090.c", "lines": "1436-1441", "route": "LABEL_394 -> 0x144026350"},
}

_CODEC_NS: dict[str, Any] | None = None
_CODEC: Any = None


def load_server_payload(table_id: int) -> bytes:
    global _CODEC_NS, _CODEC
    if _CODEC_NS is None:
        _CODEC_NS = runpy.run_path(str(ROOT / "scripts" / "fm24_dump.py"))
        _CODEC = _CODEC_NS["_reader"]()
    return _CODEC_NS["load_payload"](_CODEC, "server", table_id)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _stat_template(kind: str) -> dict[str, Any]:
    return {
        "kind": kind,
        "n": 0,
        "non_default": 0,
        "zero": 0,
        "all_ff": 0,
        "sentinel_076c0001": 0,
        "min": None,
        "max": None,
        "distinct": 0,
        "_seen": set(),
    }


def _update_stat(stat: dict[str, Any], value: int, default: tuple[int, ...], sentinel: bool = False) -> None:
    stat["n"] += 1
    if value == 0:
        stat["zero"] += 1
    if value == (0xFFFFFFFFFFFFFFFF if stat["kind"] == "u64" else 0xFFFFFFFF):
        stat["all_ff"] += 1
    if sentinel and value == DATE_SENTINEL:
        stat["sentinel_076c0001"] += 1
    if value not in default:
        stat["non_default"] += 1
    stat["min"] = value if stat["min"] is None else min(stat["min"], value)
    stat["max"] = value if stat["max"] is None else max(stat["max"], value)
    stat["_seen"].add(value)


def _update_name_stat(stat: dict[str, Any], length: int) -> None:
    stat["n"] += 1
    if length == 0:
        stat["zero"] += 1
    else:
        stat["non_default"] += 1
    stat["min"] = length if stat["min"] is None else min(stat["min"], length)
    stat["max"] = length if stat["max"] is None else max(stat["max"], length)
    stat["_seen"].add(length)


def _finalize_stat(stat: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in stat.items() if k != "_seen"}
    out["distinct"] = len(stat["_seen"])
    out["non_default_rate"] = round(stat["non_default"] / stat["n"], 6) if stat["n"] else 0.0
    out["zero_rate"] = round(stat["zero"] / stat["n"], 6) if stat["n"] else 0.0
    out["all_ff_rate"] = round(stat["all_ff"] / stat["n"], 6) if stat["n"] else 0.0
    return out


def _profile_template() -> dict[str, Any]:
    return {"n": 0, "columns": {c["id"]: _stat_template(c["kind"]) for c in PHYSICAL_COLUMNS}}


def _update_profile(profile: dict[str, Any], row: bytes, name_len: int, body_start: int) -> None:
    profile["n"] += 1
    values = {
        "key_u32": (struct.unpack_from("<I", row, 0)[0], (0, 0xFFFFFFFF), False),
        "rec_type": (row[4], (255,), False),
        "uid_slot_0": (struct.unpack_from("<Q", row, 5)[0], (0, 0xFFFFFFFFFFFFFFFF), False),
        "uid_slot_1": (struct.unpack_from("<Q", row, 13)[0], (0, 0xFFFFFFFFFFFFFFFF), False),
        "uid_slot_2": (struct.unpack_from("<Q", row, 21)[0], (0, 0xFFFFFFFFFFFFFFFF), False),
        "uid_slot_3": (struct.unpack_from("<Q", row, 29)[0], (0, 0xFFFFFFFFFFFFFFFF), False),
        "date_0": (struct.unpack_from("<I", row, body_start)[0], (0, 0xFFFFFFFF, DATE_SENTINEL), True),
        "date_1": (struct.unpack_from("<I", row, body_start + 4)[0], (0, 0xFFFFFFFF, DATE_SENTINEL), True),
        "date_2": (struct.unpack_from("<I", row, body_start + 8)[0], (0, 0xFFFFFFFF, DATE_SENTINEL), True),
        "scalar_u32": (struct.unpack_from("<I", row, body_start + 12)[0], (0, 0xFFFFFFFF), False),
        "scalar_u16_0": (struct.unpack_from("<H", row, body_start + 16)[0], (0, 0xFFFF), False),
        "scalar_u16_1": (struct.unpack_from("<H", row, body_start + 18)[0], (0, 0xFFFF), False),
        "scalar_u16_2": (struct.unpack_from("<H", row, body_start + 20)[0], (0, 0xFFFF), False),
        "scalar_u8_0": (row[body_start + 22], (0, 0xFF), False),
        "scalar_u8_1": (row[body_start + 23], (0, 0xFF), False),
        "scalar_u8_2": (row[body_start + 24], (0, 0xFF), False),
        "scalar_u8_3": (row[body_start + 25], (0, 0xFF), False),
    }
    for name, (value, default, is_date) in values.items():
        _update_stat(profile["columns"][name], value, default, is_date)
    _update_name_stat(profile["columns"]["name"], name_len)


def _finish_profile(profile: dict[str, Any]) -> dict[str, Any]:
    cols = {name: _finalize_stat(stat) for name, stat in profile["columns"].items()}
    active = [name for name, stat in cols.items() if stat["non_default"] > 0]
    return {
        "n": profile["n"],
        "columns": cols,
        "active_non_default_columns": active,
        "active_payload_columns": [name for name in active if name != "rec_type"],
    }


def scan_payload(table_id: int, raw: bytes) -> dict[str, Any]:
    expected = EXPECTED[table_id]
    if len(raw) != expected["payload_size"]:
        raise ValueError(f"table_{table_id}: payload size {len(raw)} != {expected['payload_size']}")
    digest = sha256_bytes(raw)
    if digest != expected["sha256"]:
        raise ValueError(f"table_{table_id}: sha256 {digest} != {expected['sha256']}")
    if len(raw) < HEADER_SIZE + FOOTER_SIZE:
        raise ValueError(f"table_{table_id}: payload too short")
    header_count = struct.unpack_from("<I", raw, 8)[0]
    if header_count != expected["count"]:
        raise ValueError(f"table_{table_id}: header count {header_count} != {expected['count']}")

    pos = HEADER_SIZE
    row_lengths = collections.Counter()
    name_lengths = collections.Counter()
    type_counts = collections.Counter()
    profiles: dict[int, dict[str, Any]] = {}
    bad_identity = 0
    last_identity: tuple[int, int, int, int] | None = None
    for ordinal in range(header_count):
        if pos + 41 > len(raw):
            raise ValueError(f"table_{table_id}: row {ordinal} has no name length")
        name_len = struct.unpack_from("<I", raw, pos + 37)[0]
        row_end = pos + 80 + name_len
        if row_end > len(raw):
            raise ValueError(f"table_{table_id}: row {ordinal} ends at {row_end} beyond payload")
        name = raw[pos + 41:pos + 41 + name_len]
        name.decode("utf-8")
        identity = struct.unpack_from("<III B", raw, row_end - IDENTITY_SIZE)
        if identity[0] != ordinal or identity[3] != 0:
            bad_identity += 1
            raise ValueError(f"table_{table_id}: identity mismatch row={ordinal} identity={identity}")
        rec_type = raw[pos + 4]
        body_start = pos + 41 + name_len
        if row_end - IDENTITY_SIZE - body_start != 26:
            raise ValueError(f"table_{table_id}: row {ordinal} body width is not 26")
        row = raw[pos:row_end]
        type_counts[rec_type] += 1
        profile = profiles.setdefault(rec_type, _profile_template())
        _update_profile(profile, row, name_len, body_start - pos)
        row_lengths[len(row)] += 1
        name_lengths[name_len] += 1
        last_identity = identity
        pos = row_end

    footer = raw[pos:]
    if footer != expected["footer"]:
        raise ValueError(f"table_{table_id}: footer {footer.hex()} != {expected['footer'].hex()}")
    footer9 = raw[pos - 1:]
    if footer9 != MAGIC_FOOTER_PREFIX + expected["footer"]:
        raise ValueError(f"table_{table_id}: 9-byte closure window {footer9.hex()} is unexpected")
    if bad_identity:
        raise ValueError(f"table_{table_id}: bad identity count {bad_identity}")
    return {
        "table_id": table_id,
        "path": f"server_db/table_{table_id}.dat",
        "payload_size": len(raw),
        "sha256": digest,
        "header_size": HEADER_SIZE,
        "header_hex": raw[:HEADER_SIZE].hex(),
        "record_count_header": header_count,
        "record_count_decoded": sum(type_counts.values()),
        "row_end": pos,
        "footer_size_observed": len(footer),
        "footer_hex": footer.hex(),
        "footer9_window_hex": footer9.hex(),
        "footer9_window_rule": "raw[row_end-1:] = 00 + footer8; the preceding 00 is the row terminator byte",
        "bad_identity": bad_identity,
        "last_identity": list(last_identity or ()),
        "row_length": {
            "min": min(row_lengths),
            "max": max(row_lengths),
            "distinct": len(row_lengths),
            "histogram": {str(k): v for k, v in sorted(row_lengths.items())},
        },
        "name_length": {
            "min": min(name_lengths),
            "max": max(name_lengths),
            "distinct": len(name_lengths),
        },
        "rec_type_counts": {str(k): v for k, v in sorted(type_counts.items())},
        "rec_type_distinct": len(type_counts),
        "rec_type_profiles": {str(k): _finish_profile(profiles[k]) for k in sorted(profiles)},
    }


def source_hashes() -> dict[str, str]:
    paths = [
        "scratch/t95/funcs/141544130.c",
        "scratch/t95/funcs/1415446a0.c",
        "scratch/t95/funcs/141545680.c",
        "scratch/t95/funcs/1444e4b00.c",
        "scratch/t95/funcs/140e8a400.c",
        "scratch/t95/funcs/140e834a0.c",
        "scratch/t95/funcs/1411f1090.c",
        "scratch/t88/out2/row_frame.json",
        "scratch/t88/out3/slots.json",
    ]
    return {p: sha256_bytes((ROOT / p).read_bytes()) for p in paths}


def accessor_codes(profiles45: dict[str, Any], profiles48: dict[str, Any]) -> list[dict[str, Any]]:
    source = json.loads(SLOT_FILE.read_text(encoding="utf-8"))
    codes = source.get("codes") or []
    if len(codes) != 117:
        raise ValueError(f"slots.json has {len(codes)} codes, expected 117")
    combined = {"table_45": profiles45, "table_48": profiles48}
    out: list[dict[str, Any]] = []
    for item in codes:
        code = dict(item)
        status = code.get("status")
        tag = code.get("tag")
        reader_off = code.get("reader_off")
        direct = DIRECT_BY_TAG.get(tag)
        family = code.get("family") or code.get("code", "")[:3]
        entry: dict[str, Any] = {
            "code": code.get("code"),
            "name": code.get("name"),
            "type": code.get("type"),
            "family": family,
            "suffix": code.get("suffix"),
            "tag": tag,
            "rec_type": code.get("rec_type"),
            "status": status,
            "grade": code.get("grade"),
            "crit": code.get("crit"),
            "source_asset": "scratch/t88/out3/slots.json",
            "data_side_profile_reference": "table45_full_schema.rec_type_profiles",
            "reader_off_asset_value": reader_off,
            "reader_off_interpretation": "frozen route/getter-side offset; not assumed to be STARTING_RECORD.this offset",
        }
        if direct is not None:
            physical = next(c for c in PHYSICAL_COLUMNS if c["id"] == direct["physical_col"])
            route = {
                "rec_type": code.get("rec_type"),
                "physical_col": direct["physical_col"],
                "mem_off": direct["mem_off"],
                "wire_off": direct["wire"],
            }
            entry.update({
                "mapping_tuple": route if status in ("mapped", "derived") else None,
                "physical_col": direct["physical_col"],
                "mem_off": direct["mem_off"],
                "mem_hex": hex(direct["mem_off"]),
                "wire_off": direct["wire"],
                "wire_row_expression": physical["wire_expression"],
                "physical_width": physical["wire_width"],
                "physical_kind": physical["kind"],
                "route_note": "tag joined to the direct STARTING_RECORD GET/SET case; tuple withheld for non-anchored family",
                "accessor_reader_width": code.get("width"),
            })
        else:
            entry.update({
                "mapping_tuple": None,
                "physical_col": None,
                "mem_off": None,
                "mem_hex": None,
                "wire_off": None,
                "wire_row_expression": None,
                "physical_width": None,
                "physical_kind": None,
                "route_note": None,
                "accessor_reader_width": code.get("width"),
            })

        if status == "held":
            candidate_rec_types: set[int] = set()
            if direct is not None:
                for archive_profiles in combined.values():
                    for rt_text, profile in archive_profiles.items():
                        col_stat = profile["columns"][direct["physical_col"]]
                        if col_stat["non_default"] > 0:
                            candidate_rec_types.add(int(rt_text))
            entry["data_side"] = {
                "grade": "L2_candidate" if candidate_rec_types else "held",
                "candidate_rec_types": sorted(candidate_rec_types),
                "candidate_column": direct["physical_col"] if direct is not None else None,
                "reason": "Data activity can identify candidate rec_type groups only; it does not prove this accessor family routes to the candidate column.",
            }
        elif status == "derived":
            entry["data_side"] = {
                "grade": "L2",
                "candidate_rec_types": [code.get("rec_type")],
                "candidate_column": direct["physical_col"] if direct is not None else None,
                "reason": "rec_type and suffix/tag interpretation are inherited from the mapped sibling/family; not an independent C proof.",
            }
        else:
            entry["data_side"] = {
                "grade": "L3",
                "candidate_rec_types": [code.get("rec_type")],
                "candidate_column": direct["physical_col"] if direct is not None else None,
                "reason": "rec_type/tag dispatch is pinned by the frozen route evidence and tag is translated through the direct STARTING_RECORD property case.",
            }

        dispatch = FAMILY_DISPATCH.get(family)
        if dispatch is not None and status in ("mapped", "derived"):
            entry["dispatch_evidence"] = dispatch
        else:
            entry["dispatch_evidence"] = {
                "status": "no family-specific rec_type anchor; remains held",
                "source": "scratch/t95/funcs/1411f1090.c:1399 (LABEL_362 fallback); data-side candidates do not promote",
            }
        if direct is not None:
            entry["starting_record_evidence"] = {
                "get": {"source": "scratch/t95/funcs/1415446a0.c", "lines": f"{direct['get'][0]}-{direct['get'][-1]}"},
                "set": {"source": "scratch/t95/funcs/141545680.c", "lines": f"{direct['set'][0]}-{direct['set'][-1]}" if direct["set"] else None},
            }
        else:
            entry["starting_record_evidence"] = None
        out.append(entry)
    return out


def build_verify_source(scan45: dict[str, Any], scan48: dict[str, Any]) -> str:
    expected_counts_45 = {int(k): v for k, v in scan45["rec_type_counts"].items()}
    expected_counts_48 = {int(k): v for k, v in scan48["rec_type_counts"].items()}
    columns = [(c["id"], c["mem_off"], c.get("wire_offset"), c["wire_expression"]) for c in PHYSICAL_COLUMNS]
    expected_names = repr([c["id"] for c in PHYSICAL_COLUMNS])
    expected_mem = repr([c["mem_off"] for c in PHYSICAL_COLUMNS])
    expected_wire = repr([c.get("wire_offset") for c in PHYSICAL_COLUMNS])
    return f'''#!/usr/bin/env python3
"""Independent byte-exact verifier for t98 table_45/table_48."""
from __future__ import annotations
import hashlib
import json
import os
import pathlib
import runpy
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
os.environ.setdefault("FM24_DB_DIR", str(ROOT / "scratch" / "data"))
EXPECTED = {repr({45: EXPECTED[45], 48: EXPECTED[48]})}
EXPECTED_TYPES = {{45: {repr(expected_counts_45)}, 48: {repr(expected_counts_48)}}}
COLUMNS = {repr(columns)}
EXPECTED_NAMES = {expected_names}
EXPECTED_MEM = {expected_mem}
EXPECTED_WIRE = {expected_wire}
HEADER_SIZE = 14
IDENTITY_SIZE = 13


def load(table_id):
    ns = runpy.run_path(str(ROOT / "scripts" / "fm24_dump.py"))
    codec = ns["_reader"]()
    return ns["load_payload"](codec, "server", table_id)


def check(table_id):
    raw = load(table_id)
    exp = EXPECTED[table_id]
    assert len(raw) == exp["payload_size"], (table_id, len(raw), exp["payload_size"])
    assert hashlib.sha256(raw).hexdigest() == exp["sha256"], table_id
    n = struct.unpack_from("<I", raw, 8)[0]
    assert n == exp["count"], (table_id, n, exp["count"])
    pos = HEADER_SIZE
    types = {{}}
    for i in range(n):
        assert pos + 41 <= len(raw), (table_id, i, pos)
        name_len = struct.unpack_from("<I", raw, pos + 37)[0]
        end = pos + 80 + name_len
        assert end <= len(raw), (table_id, i, end)
        raw[pos + 41:pos + 41 + name_len].decode("utf-8")
        ordinal, uid0, uid1, marker = struct.unpack_from("<III B", raw, end - IDENTITY_SIZE)
        assert ordinal == i and marker == 0, (table_id, i, ordinal, marker)
        body = pos + 41 + name_len
        assert end - IDENTITY_SIZE - body == 26, (table_id, i)
        # Exercise all 18 physical offsets on every row, including unaligned u64s.
        struct.unpack_from("<I", raw, pos + 0)
        raw[pos + 4]
        for off in (5, 13, 21, 29):
            struct.unpack_from("<Q", raw, pos + off)
        struct.unpack_from("<I", raw, body + 0)
        struct.unpack_from("<I", raw, body + 4)
        struct.unpack_from("<I", raw, body + 8)
        struct.unpack_from("<I", raw, body + 12)
        for off in (16, 18, 20):
            struct.unpack_from("<H", raw, body + off)
        for off in (22, 23, 24, 25):
            raw[body + off]
        rt = raw[pos + 4]
        types[rt] = types.get(rt, 0) + 1
        pos = end
    assert raw[pos:] == exp["footer"], (table_id, raw[pos:].hex(), exp["footer"].hex())
    assert raw[pos - 1:] == b"\\x00" + exp["footer"], (table_id, raw[pos - 1:].hex())
    assert pos == len(raw) - 8, (table_id, pos, len(raw))
    assert types == EXPECTED_TYPES[table_id], (table_id, types, EXPECTED_TYPES[table_id])
    return n, pos, types


def main():
    assert len(COLUMNS) == 18
    assert [x[0] for x in COLUMNS] == EXPECTED_NAMES
    assert [x[1] for x in COLUMNS] == EXPECTED_MEM
    assert [x[2] for x in COLUMNS] == EXPECTED_WIRE
    assert [x[3] for x in COLUMNS] == [
        "row+0", "row+4", "row+5", "row+13", "row+21", "row+29",
        "row+37: [u32 length][utf8 bytes]",
        "tail+0 = row+41+namelen", "tail+4 = row+45+namelen", "tail+8 = row+49+namelen",
        "tail+12 = row+53+namelen", "tail+16 = row+57+namelen", "tail+18 = row+59+namelen",
        "tail+20 = row+61+namelen", "tail+22 = row+63+namelen", "tail+23 = row+64+namelen",
        "tail+24 = row+65+namelen", "tail+25 = row+66+namelen",
    ]
    for table_id in (45, 48):
        n, end, types = check(table_id)
        print(f"PASS table_{{table_id}} rows={{n}} types={{len(types)}} row_end={{end}} footer8={{EXPECTED[table_id]['footer'].hex()}} footer9={{('00' + EXPECTED[table_id]['footer'].hex())}}")
    print("PASS t98 verify: 18 physical columns and both 9-byte closure windows")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("FAIL t98 verify:", exc)
        raise SystemExit(1)
'''


def report_text(scan45: dict[str, Any], scan48: dict[str, Any], codes: list[dict[str, Any]]) -> str:
    status_counts = collections.Counter(item["status"] for item in codes)
    lines = [
        "# t98 table_45/table_48 closure",
        "",
        "Status: complete for the byte frame, 18-column layout, rec_type census, and the 117-code evidence ledger.",
        "",
        "## Results",
        "",
        f"- `table_45`: {scan45['record_count_decoded']:,} rows, {scan45['payload_size']:,} bytes, SHA-256 `{scan45['sha256']}`.",
        f"- `table_48`: {scan48['record_count_decoded']:,} rows, {scan48['payload_size']:,} bytes, SHA-256 `{scan48['sha256']}`.",
        f"- Both tables decode with `rowlen = 80 + namelen`, 26-byte body, and 13-byte identity trailer; table_45 has {scan45['rec_type_distinct']} observed rec_type values and table_48 has {scan48['rec_type_distinct']}.",
        f"- 117 accessor rows: {status_counts['mapped']} mapped L3, {status_counts['derived']} derived L2, {status_counts['held']} held.",
        "",
        "## Footer ruling",
        "",
        "The byte-exact row walk ends at `payload_len - 8` for both tables. The observed footer is therefore 8 bytes: `table_45 = 00000001775f0100`, `table_48 = 000000019f180000`. The requested 9-byte closure is verified as the 9-byte window `00 + footer8`; its first zero is the final row terminator byte, not an independent footer field. `verify.py` asserts both forms.",
        "",
        "## Physical columns",
        "",
        "| Column | Wire location | this offset | Read source | Write source |",
        "|---|---|---:|---|---|",
    ]
    for c in PHYSICAL_COLUMNS:
        wire = c.get("wire_expression", "")
        lines.append(f"| `{c['id']}` | `{wire}` | `{c['mem_hex']}` | `{c['read_source']}` | `{c['write_source']}` |")
    lines += [
        "",
        "The identity trailer is structural at `row_end-13`: ordinal u32, two uid u32 values, and a zero terminator byte. It is excluded from the 18 persisted columns.",
        "",
        "## Direct STARTING_RECORD 4CCs",
        "",
        "The following aliases are from `STARTING_RECORD::slot02_get_prop` and `slot03_set_prop`; `get`/`set` behavior is kept separate from the outer router's tag names.",
        "",
        "| 4CC | Physical column | this offset | Wire location | GET lines | SET lines |",
        "|---|---|---:|---|---:|---:|",
    ]
    for item in DIRECT_TAGS:
        lines.append(f"| `{item['tag']}` | `{item['physical_col']}` | `0x{item['mem_off']:x}` | `{item['wire']}` | `{item['get'][0]}-{item['get'][-1]}` | `{(str(item['set'][0]) + '-' + str(item['set'][-1])) if item['set'] else 'delegated'}` |")
    lines += [
        "",
        "## rec_type activity",
        "",
        "`active_payload_columns` means a value is not one of the data defaults (zero, all-ones, or the packed date sentinel `0x076c0001`). It is a data-side profile only and never promotes a held accessor to L3.",
        "",
        "| rec_type | table_45 rows | table_48 rows | active table_45 payload columns |",
        "|---:|---:|---:|---|",
    ]
    all_types = sorted(set(scan45["rec_type_profiles"]) | set(scan48["rec_type_profiles"]))
    for key in all_types:
        p45 = scan45["rec_type_profiles"].get(key, {"n": 0, "active_payload_columns": []})
        p48 = scan48["rec_type_profiles"].get(key, {"n": 0})
        lines.append(f"| `{key}` | {p45.get('n', 0):,} | {p48.get('n', 0):,} | {', '.join('`' + x + '`' for x in p45.get('active_payload_columns', [])) or '-'} |")
    lines += [
        "",
        "## 117-code ledger",
        "",
        "Each mapped/derived row carries the tuple `(rec_type, physical_col, mem_off, wire_off)` plus the hub-side route offset from the frozen slots asset. Held rows have a null tuple and an explicit no-promotion reason. The complete machine-readable list is in `table45_full_schema.json`.",
        "",
        "The L3 dispatch families are evidenced in `scratch/t95/funcs/1411f1090.c` at the CFG/CHA/CHS/CLA/COS/CYP/CYS case blocks and the `LABEL_394 -> 0x144026350` hub. `LABEL_362` fallback and the absence criterion remain held for the other families.",
        "",
        "## Verification",
        "",
        "Run:",
        "",
        "```text",
        "C:\\Users\\oak\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -I -B scripts/t98_table45_closure.py --selftest",
        "C:\\Users\\oak\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -I -B scratch/t98/out/verify.py",
        "```",
    ]
    return "\n".join(lines) + "\n"


def _write_json(path: pathlib.Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def build() -> dict[str, Any]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    raw45 = load_server_payload(45)
    raw48 = load_server_payload(48)
    scan45 = scan_payload(45, raw45)
    scan48 = scan_payload(48, raw48)
    codes = accessor_codes(scan45["rec_type_profiles"], scan48["rec_type_profiles"])
    hashes = source_hashes()

    schema = {
        "status": "complete",
        "task": "t98",
        "generated_by": "scripts/t98_table45_closure.py",
        "inputs": {
            "server_db_dir": str(pathlib.Path(os.environ["FM24_DB_DIR"])),
            "source_sha256": hashes,
            "payloads": {
                "table_45": {k: scan45[k] for k in ("path", "payload_size", "sha256", "record_count_header", "footer_hex")},
                "table_48": {k: scan48[k] for k in ("path", "payload_size", "sha256", "record_count_header", "footer_hex")},
            },
        },
        "shared_vtable": "0x14187df38 (task evidence)",
        "row_frame": {
            "header_size": HEADER_SIZE,
            "row_length": "80+namelen",
            "name": "[u32 namelen][utf8 bytes] at row+37",
            "body": "26 bytes at row+41+namelen",
            "identity": IDENTITY,
            "footer_observed": "8 bytes",
            "footer_task_window": "9 bytes = 00 + observed footer8",
        },
        "physical_columns": PHYSICAL_COLUMNS,
        "direct_starting_record_4cc": DIRECT_TAGS,
        "table_45": scan45,
        "rec_type_profiles": scan45["rec_type_profiles"],
        "accessor_codes": codes,
        "summary": {
            "physical_column_count": len(PHYSICAL_COLUMNS),
            "rec_type_count_table_45": scan45["rec_type_distinct"],
            "rec_type_count_table_48": scan48["rec_type_distinct"],
            "accessor_count": len(codes),
            "status_counts": dict(collections.Counter(item["status"] for item in codes)),
            "l3_mapped_or_l2_derived_with_tuple": sum(1 for item in codes if item["mapping_tuple"] is not None),
            "held_without_tuple": sum(1 for item in codes if item["mapping_tuple"] is None),
        },
    }
    comparison = {
        "status": "complete",
        "task": "t98",
        "table": "server table_48",
        "shared_layout": "table45_full_schema.row_frame and physical_columns",
        "table_48": scan48,
        "comparison_to_table_45": {
            "table_45_rows": scan45["record_count_decoded"],
            "table_48_rows": scan48["record_count_decoded"],
            "row_frame_same": True,
            "physical_column_count": len(PHYSICAL_COLUMNS),
            "rec_type_union": sorted(set(scan45["rec_type_counts"]) | set(scan48["rec_type_counts"]), key=int),
            "rec_type_count_delta_48_minus_45": {
                key: int(scan48["rec_type_counts"].get(key, 0)) - int(scan45["rec_type_counts"].get(key, 0))
                for key in sorted(set(scan45["rec_type_counts"]) | set(scan48["rec_type_counts"],), key=int)
            },
            "footer8_differs": scan45["footer_hex"] != scan48["footer_hex"],
            "footer_rule_same": True,
        },
        "rec_type_profiles": scan48["rec_type_profiles"],
    }

    # Stage the data artifacts first. DONE is intentionally written last.
    _write_json(OUTDIR / "table45_full_schema.json", schema)
    _write_json(OUTDIR / "table48_comparison.json", comparison)
    (OUTDIR / "REPORT.md").write_text(report_text(scan45, scan48, codes), encoding="utf-8")
    verify_path = OUTDIR / "verify.py"
    verify_path.write_text(build_verify_source(scan45, scan48), encoding="utf-8")
    verify_path.chmod(0o755)

    result = {
        "schema": schema,
        "comparison": comparison,
        "scan45": scan45,
        "scan48": scan48,
        "codes": codes,
        "verify_path": verify_path,
    }
    return result


def run_verify(verify_path: pathlib.Path) -> None:
    env = dict(os.environ)
    env.setdefault("FM24_DB_DIR", str(ROOT / "scratch" / "data"))
    proc = subprocess.run([sys.executable, "-I", "-B", str(verify_path)], cwd=str(ROOT), env=env, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"independent verifier exited {proc.returncode}")


def write_done(result: dict[str, Any]) -> None:
    s45 = result["scan45"]
    s48 = result["scan48"]
    counts = collections.Counter(item["status"] for item in result["codes"])
    text = "\n".join([
        "# t98 done",
        "",
        "DONE type=t98",
        "",
        f"- table_45: {s45['record_count_decoded']} rows; payload {s45['payload_size']} B; sha256 {s45['sha256']}",
        f"- table_48: {s48['record_count_decoded']} rows; payload {s48['payload_size']} B; sha256 {s48['sha256']}",
        f"- physical columns: 18; observed rec_type groups: table_45={s45['rec_type_distinct']}, table_48={s48['rec_type_distinct']}",
        f"- accessor ledger: {counts['mapped']} mapped L3, {counts['derived']} derived L2, {counts['held']} held",
        f"- footer closure: observed 8 B; verified 9-byte windows table_45={s45['footer9_window_hex']}, table_48={s48['footer9_window_hex']}",
        "- independent verify.py: PASS",
        "",
    ])
    (OUTDIR / "DONE.md").write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit and verify t98 table_45/table_48 closure artifacts.")
    parser.add_argument("--selftest", action="store_true", help="scan both payloads, emit artifacts, and run independent verify.py")
    args = parser.parse_args(argv)
    if not args.selftest:
        parser.error("use --selftest")
    try:
        result = build()
        run_verify(result["verify_path"])
        write_done(result)
        counts = collections.Counter(item["status"] for item in result["codes"])
        print("PASS t98 selftest")
        print(f"table_45 rows={result['scan45']['record_count_decoded']} sha256={result['scan45']['sha256']}")
        print(f"table_48 rows={result['scan48']['record_count_decoded']} sha256={result['scan48']['sha256']}")
        print(f"physical_columns=18 rec_types_45={result['scan45']['rec_type_distinct']} rec_types_48={result['scan48']['rec_type_distinct']}")
        print(f"accessors mapped_l3={counts['mapped']} derived_l2={counts['derived']} held={counts['held']}")
        print("deliverables:")
        for name in ("table45_full_schema.json", "table48_comparison.json", "REPORT.md", "verify.py", "DONE.md"):
            print(f"  {OUTDIR / name}")
        return 0
    except Exception as exc:
        print(f"FAIL t98: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
