"""Commander's independent .dat-side spot-check of t01f claims (row 7 / 250 / 639 bytes).

Imports the OLD repo reader read-only (never writes game files). Run from fm24-db root:
py -V:3.12 -I scripts/t01f_dat_spotcheck.py
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import importlib.util
import struct
import sys

spec = importlib.util.spec_from_file_location("oldread", str(_cfg.OLD_DBDAT_READER))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)

DB = str(_cfg.GAME_DB_DIR)
path, data, meta = old._entries(DB, "client_db.dat")
raw = None
for e in meta["entries"]:
    tid = old._table_id(e.get("path", e.get("name", "")))
    if tid == 25:
        raw = old._decompress_entry(data, meta["data_base"], e)
        break
assert raw is not None, "table_25 not found"
print(f"payload size: {len(raw):#x}")

def rowbase(i: int) -> int:
    return 14 + i * 127

def show(label, off, n, expect=None):
    b = raw[off:off + n]
    ok = ""
    if expect is not None:
        ok = " PASS" if b == expect else f" FAIL (expected {expect.hex()})"
    print(f"{label:34} @payload {off:#07x}: {b.hex()}{ok}")

fails = 0
def expect(label, off, n, hexstr):
    global fails
    b = raw[off:off + n]
    e = bytes.fromhex(hexstr.replace(" ", ""))
    good = b == e
    fails += not good
    print(f"{'PASS' if good else 'FAIL':4} {label:30} @payload {off:#07x}: {b.hex()}" + ("" if good else f"  expected {e.hex()}"))

# row 7 (base payload 0x387)
b7 = rowbase(7)
expect("r7 lead marker @13+7*127", b7 - 1, 1, "00")
expect("r7 +0..1 (2B prefix)", b7, 2, None) if False else show("r7 +0..1 prefix", b7, 2)
expect("r7 levl@+15 = 00", b7 + 15, 1, "00")
expect("r7 ccti@+52 = 02 00 00 00", b7 + 52, 4, "02 00 00 00")
expect("r7 cnti@+56 = 8b 00 00 00", b7 + 56, 4, "8b 00 00 00")
show("r7 cpcm@+64", b7 + 64, 4)
expect("r7 cmnl@+76 = 1a 04 (1050)", b7 + 76, 2, "1a 04")
show("r7 wbcl@+101", b7 + 101, 2)
expect("r7 +114 row ordinal = 07", b7 + 114, 4, "07 00 00 00")
expect("r7 +118 dup-ID block = 0b,0b", b7 + 118, 8, "0b 00 00 00 0b 00 00 00")
show("r7 +122 native rdui?", b7 + 122, 4)
show("r7 +126 boundary", b7 + 126, 1)

# row 250 anchors (old repo b47)
b250 = rowbase(250)
expect("r250 ccti@+52 = 01 00 00 00", b250 + 52, 4, "01 00 00 00")
expect("r250 cnti@+56 = 37 00 00 00", b250 + 56, 4, "37 00 00 00")

# row 639
b639 = rowbase(639)
expect("r639 cnti@+56 = ff ff ff ff", b639 + 56, 4, "ff ff ff ff")

# claimed direct payload anchors (North/South parent rows)
expect("payload 0x15f0b = 60 01 00 00", 0x15f0b, 4, "60 01 00 00")
expect("payload 0x15f8a = 60 01 00 00", 0x15f8a, 4, "60 01 00 00")

# ordinal sweep: +114 == row_index for first 60 rows
bad = sum(1 for i in range(60) if struct.unpack_from("<I", raw, rowbase(i) + 114)[0] != i)
print(f"ordinal sweep rows 0..59: {60 - bad}/60 equal row_index ({bad} mismatch)")

# row 7 payload 0x3eb/0x3ee/0x3f2 claimed raw bytes
expect("r7 +100 marker+color", b7 + 100, 3, "01 c0 7f")
expect("r7 +103 wbst = 31 01 e1 07", b7 + 103, 4, "31 01 e1 07")
expect("r7 +107 wben = 3b 00 e2 07", b7 + 107, 4, "3b 00 e2 07")

print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
