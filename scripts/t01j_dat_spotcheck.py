"""Commander's independent verification of t01j: basic_people_db.dat structure.

Fully independent decompression + row-chain walk (does not reuse t01j's verify.py logic).
Run from fm24-db root: py -V:3.12 -I scripts/t01j_dat_spotcheck.py
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import struct
import sys

BP = _cfg.GAME_DB_DIR / "basic_people_db.dat"
ED = str(_cfg.EDITOR_EXE)
fails = 0

def check(label, cond, detail=""):
    global fails
    fails += not cond
    print(f"{'PASS' if cond else 'FAIL':4} {label} {detail}")

# --- decompress independently via old repo zstd helper ---
spec = None
import importlib.util
spec = importlib.util.spec_from_file_location("o", str(_cfg.OLD_DBDAT_READER))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
zmod = old._zstd_module()
raw_file = open(BP, "rb").read()
check("container head tad. @0", raw_file[:8] == bytes.fromhex("03017461642ef10d"), raw_file[:8].hex())
check("zstd magic @8", raw_file[8:12] == bytes.fromhex("28b52ffd"), raw_file[8:12].hex())
frame = raw_file[8:]
payload = old._stream_decompress(frame, 256 * 1024 * 1024)
print(f"INFO decompressed payload: {len(payload):,} B")

# --- header & row chain ---
count = struct.unpack_from("<I", payload, 0)[0]
check("count u32 @0 == 658011", count == 658011, str(count))
check("byte @4 == 0", payload[4] == 0, hex(payload[4]))

CLASS_LEN = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
pos = 5
cls_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
ord_ok = True
id_ok = True
bad = 0
for i in range(count):
    if payload[pos] != 0x11:
        bad += 1
        if bad <= 3:
            print(f"  INFO row {i} @payload {pos:#x}: header {payload[pos]:02x} != 0x11")
    cid = payload[pos + 1]
    ln = CLASS_LEN.get(cid)
    if ln is None:
        bad += 1
        break
    cls_counts[cid] += 1
    # identity block: last 12B of the row = ordinal | ID | ID
    o, a, b = struct.unpack_from("<III", payload, pos + ln - 12)
    if o != i or a != b:
        ord_ok = False
        if sum(cls_counts.values()) < 5:
            print(f"  INFO row {i}: ord={o} idA={a:#x} idB={b:#x}")
    pos += ln
check("all row headers == 0x11", bad == 0, f"bad={bad}")
check("ordinal continuous + dup-ID on ALL rows", ord_ok and id_ok)
check("class tally 1:166064/2:476158/3:4757/4:9839/5:1193",
      cls_counts == {1: 166064, 2: 476158, 3: 4757, 4: 9839, 5: 1193}, str(cls_counts))
check("closure 5+rows+9 == payload size", pos + 9 == len(payload), f"rows_end {pos:,} payload {len(payload):,}")
tail = payload[pos:pos + 9]
print(f"INFO tail 9B: {tail.hex()}")

# --- sample row spot-checks from t01j REPORT ---
def row_bytes(off, n):
    return payload[off:off + n].hex()
check("row0 header @5", row_bytes(5, 2) == "1101", row_bytes(5, 2))
check("row0 identity @5+83-12=76", row_bytes(76, 12) == "000000000300000003000000", row_bytes(76, 12))
check("class4 sample header @80681", row_bytes(80681, 6) == "1104af000000", row_bytes(80681, 6))
check("class4 identity @80681+34-12", row_bytes(80681 + 22, 12) == "cc030000d2140000d2140000", row_bytes(80681 + 22, 12))
check("class5 identity @54033788+10", row_bytes(54033798, 12) == "b2050a00a4b85477a4b85477", row_bytes(54033798, 12))

# --- static: class-4 branch instructions in reader ---
data = open(ED, "rb").read()
def expect(label, off, hexstr):
    e = bytes.fromhex(hexstr.replace(" ", ""))
    got = data[off:off + len(e)]
    check(label, got == e, f"@{off:#x}: {got.hex()}")
expect("reader cmp al,4 @0xe4f42e", 0xe4f42e, "3c 04")
expect("reader jne skip @0xe4f430", 0xe4f430, "75 4c")
expect("reader first width mov r8d,1 @0xe4f393", 0xe4f393, "41 b8 01 00 00 00")
expect("reader width-2 @0xe4f43c", 0xe4f43c, "41 b8 02 00 00 00")
expect("reader width-2 @0xe4f468", 0xe4f468, "41 b8 02 00 00 00")

print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
