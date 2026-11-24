"""Commander's independent verification of t01l: WEATHER table_27 claims.
Independent decompression + row walk + static byte checks.
Run from fm24-db root: py -V:3.12 -I scripts/t01l_spotcheck.py
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import importlib.util
import struct
import sys

fails = 0
def check(label, cond, detail=""):
    global fails
    fails += not cond
    print(f"{'PASS' if cond else 'FAIL':4} {label} {detail}")

ED = str(_cfg.EDITOR_EXE)
DB = str(_cfg.GAME_DB_DIR)

# --- static byte checks ---
data = open(ED, "rb").read()
def expect(label, off, hexstr):
    e = bytes.fromhex(hexstr.replace(" ", ""))
    got = data[off:off + len(e)]
    check(label, got == e, f"@{off:#x}: {got.hex()}" + ("" if got == e else f" exp={e.hex()}"))

check("RTTI '.?AVWEATHER@db@@' @0x1aae200", data[0x1aae200:0x1aae211] == b".?AVWEATHER@db@@\x00", data[0x1aae200:0x1aae211].decode(errors="replace"))
expect("alloc wrapper mov edx,0x88 @0x3bd750c", 0x3bd750c, "ba 88 00 00 00")
expect("type query returns 27 @0xfb37f0", 0xfb37f0, "b8 1b 00 00 00 c3")
expect("slot19 ptr -> reader VA 0x14158c370 @0x1882480", 0x1882480, "70 c3 58 41 01 00 00 00")
expect("season loop add r12,0x18 @0x158bcf9", 0x158bcf9, "49 83 c4 18")
expect("season loop cmp r12,0x60 @0x158bcfd", 0x158bcfd, "49 83 fc 60")
expect("season loop jne @0x158bd01", 0x158bd01, "0f 85 1d fd ff ff")
expect("season first width 2 @0x158ba2f", 0x158ba2f, "41 b8 02 00 00 00")
expect("w0sd getter cmp edx,'w0sd' @0x158e91c", 0x158e91c, "81 fa 64 73 30 77")
expect("wnam getter cmp edx,'wnam' @0x158e971", 0x158e971, "81 fa 6d 61 6e 77")
expect("w0p1 range lea @0x158e7d9", 0x158e7d9, "8d 82 d0 8f cf 88")
expect("w0p1 bound cmp eax,4 @0x158e7df", 0x158e7df, "83 f8 04")
expect("w0p1 table lea @0x158e7e8", 0x158e7e8, "48 8d 0d c9 04 00 00")
# w0p1 range arithmetic: imm 0x88cf8fd0 signed = -0x77307030; w0p1 = 0x77307031 -> index 1
val = (0x77307031 + struct.unpack("<i", bytes.fromhex("d08fcf88"))[0]) & 0xFFFFFFFF
check("w0p1 range arithmetic -> index 1", val == 1, f"{val:#x}")
# table entry index1 @0x158ecbc -> 0x158eb74
rel = struct.unpack("<i", data[0x158ecbc:0x158ecbc + 4])[0]
tbl_base = 0x158e7e8 + 7 + struct.unpack("<i", data[0x158e7e8 + 3:0x158e7e8 + 7])[0]
tgt = tbl_base + rel
check("w0p1 table[1] -> 0x158eb74", tgt == 0x158eb74, f"{tgt:#x}")
expect("w0p1 handler lea [rdi+0x20] @0x158eb74", 0x158eb74, "48 83 c7 20")
expect("w0p1 inner cmp edx,'pre1' @0x158ebab", 0x158ebab, "ba 31 65 72 70")
expect("reader sink lea [r11+r12+0x23] @0x158ba64", 0x158ba64, "4a 8d 54 23 23")
expect("reader width 1 @0x158ba6c", 0x158ba6c, "41 b8 01 00 00 00")
expect("wnam string dest object+0x18 @0x158b98c", 0x158b98c, "4c 8d 43 18")
expect("date compare @0x158bd0b", 0x158bd0b, "66 3b 43 38")

# --- data side: independent decompress + row walk ---
spec = importlib.util.spec_from_file_location("o", str(_cfg.OLD_DBDAT_READER))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
zmod = old._zstd_module()
zdecompress = old._stream_decompress

path, d, meta = old._entries(DB, "client_db.dat")
t27 = None
for e in meta["entries"]:
    if e.get("path", "").endswith("table_27.dat"):
        t27 = old._decompress_entry(d, meta["data_base"], e)
        break
check("table_27 present in client_db.dat", t27 is not None)
payload = t27
check("payload size 43,345", len(payload) == 43345, f"{len(payload):,}")
check("header count=334 @0", struct.unpack_from("<I", payload, 8)[0] == 334)
check("tad. head", payload[:8] == bytes.fromhex("03017461642ef10d"))

# row walk: start[0]=14; start[i+1]=start[i]+112+u32le(name_len)
starts = []
pos = 14
ok = True
names_ok = True
for i in range(334):
    starts.append(pos)
    nlen = struct.unpack_from("<I", payload, pos)[0]
    if not (5 <= nlen <= 44):
        ok = False
        break
    name = payload[pos + 4:pos + 4 + nlen]
    try:
        name.decode("utf-8")
    except UnicodeDecodeError:
        names_ok = False
    pos += 112 + nlen
    # boundary marker sits at next_start-1 (the 112 already includes it)
    if payload[pos - 1] != 0:
        ok = False
        break
check("334-row walk closure + boundary markers", ok and pos == 43345 - 8, f"end={pos:#x}")
check("all names valid UTF-8, len 5..44", names_ok)

def row_sample(idx):
    s = starts[idx]
    nlen = struct.unpack_from("<I", payload, s)[0]
    return payload[s + 4:s + 4 + nlen].decode("utf-8"), s, nlen

n0, s0, l0 = row_sample(0)
check("row0 name 'English Coastal'", n0 == "English Coastal", f"{n0!r} @payload {s0:#x}")
n1, s1, l1 = row_sample(1)
check("row1 name 'English Inland'", n1 == "English Inland", f"{n1!r} @payload {s1:#x}")
n333, s333, l333 = row_sample(333)
check("row333 name NGA Tropical", n333 == "NGA - Tropical Rainforest Climate Zone", f"{n333!r} @payload {s333:#x}")
n139, s139, l139 = row_sample(139)
check("row139 name BLR-Southern", n139 == "BLR-Southern", f"{n139!r} @payload {s139:#x}")

# w0sd wire offset: row+N+7 -> 2B at start+name+7
val = struct.unpack_from("<H", payload, s0 + l0 + 7)[0]
print(f"INFO row0 w0sd wire value: {val}")
# identity block: 12B tail = ordinal|ID|ID, sits at s_end-13 (marker occupies s_end-1)
s_end = s0 + 112 + l0
idblk = payload[s_end - 13:s_end - 1]
o, a, b = struct.unpack_from("<III", idblk, 0)
check("row0 identity ordinal=0, dup-ID", o == 0 and a == b, f"ord={o} id={a:#x},{b:#x}")
s_end333 = s333 + 112 + l333
o333, a3, b3 = struct.unpack_from("<III", payload[s_end333 - 13:s_end333 - 1], 0)
check("row333 identity ordinal=333, dup-ID", o333 == 333 and a3 == b3, f"ord={o333}")
# sweep ordinal+dup across all rows
bad = 0
for i in range(334):
    s = starts[i]
    nl = struct.unpack_from("<I", payload, s)[0]
    se = s + 112 + nl
    o2, a2, b2 = struct.unpack_from("<III", payload[se - 13:se - 1], 0)
    if o2 != i or a2 != b2:
        bad += 1
check("identity ordinal+dup-ID sweep 334/334", bad == 0, f"bad={bad}")
# footer
check("footer 8B @0xa949", payload[0xa949:0xa951].hex() == "000000011fee3777", payload[0xa949:0xa951].hex())

print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
