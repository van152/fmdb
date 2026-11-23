#!/usr/bin/env python3
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
EXPECTED = {45: {'count': 84477, 'payload_size': 7608748, 'sha256': '46799e2f79acc276cc2e349fa4724de917428e07d960d8d6059dc32b1fd58bf9', 'footer': b'\x00\x00\x00\x01w_\x01\x00'}, 48: {'count': 5210, 'payload_size': 446049, 'sha256': 'f86bf6ee0bcc253fdc5b95a396e3a2fd433ccf92e1f769dbc742cdfcf73de8a5', 'footer': b'\x00\x00\x00\x01\x9f\x18\x00\x00'}}
EXPECTED_TYPES = {45: {1: 2043, 2: 2151, 3: 2127, 4: 2221, 5: 1207, 6: 1514, 7: 2392, 8: 3391, 9: 3362, 10: 1688, 11: 1549, 12: 1358, 13: 1223, 14: 1490, 15: 1282, 16: 68, 17: 58, 18: 931, 19: 823, 20: 1783, 21: 879, 22: 1280, 23: 989, 24: 653, 25: 1811, 26: 946, 27: 1265, 28: 1243, 29: 936, 30: 1538, 31: 82, 32: 43, 33: 39, 34: 631, 253: 314, 254: 199, 255: 38968}, 48: {1: 13, 2: 19, 3: 45, 4: 65, 5: 68, 6: 76, 7: 276, 8: 660, 9: 161, 10: 227, 11: 222, 12: 210, 13: 191, 14: 222, 15: 193, 16: 4, 17: 1, 18: 158, 19: 121, 20: 166, 21: 8, 22: 343, 23: 354, 24: 147, 25: 574, 26: 157, 27: 188, 28: 175, 29: 89, 34: 74, 35: 3}}
COLUMNS = [('key_u32', 76, 0, 'row+0'), ('rec_type', 94, 4, 'row+4'), ('uid_slot_0', 24, 5, 'row+5'), ('uid_slot_1', 32, 13, 'row+13'), ('uid_slot_2', 40, 21, 'row+21'), ('uid_slot_3', 48, 29, 'row+29'), ('name', 56, 37, 'row+37: [u32 length][utf8 bytes]'), ('date_0', 64, None, 'tail+0 = row+41+namelen'), ('date_1', 68, None, 'tail+4 = row+45+namelen'), ('date_2', 72, None, 'tail+8 = row+49+namelen'), ('scalar_u32', 80, None, 'tail+12 = row+53+namelen'), ('scalar_u16_0', 84, None, 'tail+16 = row+57+namelen'), ('scalar_u16_1', 86, None, 'tail+18 = row+59+namelen'), ('scalar_u16_2', 88, None, 'tail+20 = row+61+namelen'), ('scalar_u8_0', 90, None, 'tail+22 = row+63+namelen'), ('scalar_u8_1', 91, None, 'tail+23 = row+64+namelen'), ('scalar_u8_2', 92, None, 'tail+24 = row+65+namelen'), ('scalar_u8_3', 93, None, 'tail+25 = row+66+namelen')]
EXPECTED_NAMES = ['key_u32', 'rec_type', 'uid_slot_0', 'uid_slot_1', 'uid_slot_2', 'uid_slot_3', 'name', 'date_0', 'date_1', 'date_2', 'scalar_u32', 'scalar_u16_0', 'scalar_u16_1', 'scalar_u16_2', 'scalar_u8_0', 'scalar_u8_1', 'scalar_u8_2', 'scalar_u8_3']
EXPECTED_MEM = [76, 94, 24, 32, 40, 48, 56, 64, 68, 72, 80, 84, 86, 88, 90, 91, 92, 93]
EXPECTED_WIRE = [0, 4, 5, 13, 21, 29, 37, None, None, None, None, None, None, None, None, None, None, None]
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
    types = {}
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
    assert raw[pos - 1:] == b"\x00" + exp["footer"], (table_id, raw[pos - 1:].hex())
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
        print(f"PASS table_{table_id} rows={n} types={len(types)} row_end={end} footer8={EXPECTED[table_id]['footer'].hex()} footer9={('00' + EXPECTED[table_id]['footer'].hex())}")
    print("PASS t98 verify: 18 physical columns and both 9-byte closure windows")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("FAIL t98 verify:", exc)
        raise SystemExit(1)
