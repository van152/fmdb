"""Commander's independent spot-check of t01g (luna) nation claims.

Static side: editor.exe raw bytes. Data side: client_db.dat table_10 payload via old reader.
Run from fm24-db root: py -V:3.12 -I scripts/t01g_spotcheck.py
"""
from __future__ import annotations
import importlib.util
import json
import struct
import sys

ED = r"D:\tmp2b\fm24\input\editor.exe"
VA_DELTA = 0xA00
fails = 0

with open(ED, "rb") as f:
    data = f.read()

def expect(label, off, hexstr):
    global fails
    e = bytes.fromhex(hexstr.replace(" ", ""))
    got = data[off:off + len(e)]
    good = got == e
    fails += not good
    print(f"{'PASS' if good else 'FAIL':4} {label:44} @{off:#x}: {got.hex()}" + ("" if good else f" exp={e.hex()}"))

def rel_target(off):
    b = data[off:off + 5]
    rel = struct.unpack_from("<i", b, 1)[0]
    return 0x140000000 + off + VA_DELTA + 5 + rel

# --- class & factory ---
expect("RTTI '.?AVNATION@db@@' @0x1aacac0", 0x1aacac0, "2e 3f 41 56 4e 41 54 49 4f 4e 40 64 62 40 40 00")
expect("ctor vptr write lea @0x103ec17", 0x103ec17, "48 8d 05 9a 9d 84 00")
expect("ctor vptr store @0x103ec1e", 0x103ec1e, "48 89 01")
tgt = rel_target(0xf48f37)
good = tgt == 0x14103EBF0
fails += not good
print(f"{'PASS' if good else 'FAIL':4} factory ctor call -> 0x14103ebf0 @0xf48f37: {hex(tgt)}")
expect("factory alloc 0x1d8 @0xf48f27", 0xf48f27, "b9 d8 01 00 00")
expect("type-10 item rel @0xf49d60", 0xf49d60, "ef f1 ff ff")
expect("slot7 query returns 10 @0x104e4b0", 0x104e4b0, "b8 0a 00 00 00 c3")
lea_va = 0x140000000 + 0x103ec17 + VA_DELTA + 7
tgt2 = lea_va + struct.unpack_from("<i", data, 0x103ec17 + 3)[0]
good = tgt2 == 0x1418889B8
fails += not good
print(f"{'PASS' if good else 'FAIL':4} ctor lea -> vptr 0x1418889b8: {hex(tgt2)}")

# --- vtable slot19/slot21 entries ---
def qword(off):
    return struct.unpack_from("<Q", data, off)[0]
for off, want, lbl in ((0x1888a50, 0x140103FAC0, "slot19 -> reader 0x140103fac0"),
                       (0x1888a60, 0x1401041460, "slot21 -> writer 0x1401041460")):
    got = qword(off)
    good = got == want
    fails += not good
    print(f"{'PASS' if good else 'FAIL':4} {lbl} @{off:#x}: {hex(got)}")

# --- reader structure ---
expect("param branch @0x103fae6", 0x103fae6, "0f 84 c4 0a 00 00")
# width instructions of the 7 mapped fields: mov r8d,N
for off, w in ((0x10405be, 1), (0x10405e2, 4), (0x1040606, 4), (0x104064e, 4),
               (0x1040672, 1), (0x1040696, 1), (0x10406de, 1)):
    expect(f"width mov r8d,{w}", off, f"41 b8 {w:02x} 00 00 00")

# --- count-driven loop pattern (negative-result evidence) ---
seq = data[0x1040773:0x104077d]
print(f"INFO loop insn @0x1040773: {seq.hex()}  (expect inc/cmp/jl pattern)")

# --- nation switch window: independent count of cmp esi,<nation imm32> hits ---
master = json.load(open(r"evidence/fm24/reports/editor_schema/master.json", encoding="utf-8"))
def nation_codes(obj):
    # find nation entity codes list
    if isinstance(obj, dict):
        if "nation" in obj and isinstance(obj["nation"], list):
            return obj["nation"]
        for v in obj.values():
            r = nation_codes(v)
            if r:
                return r
    return None
codes = nation_codes(master)
print(f"INFO master.json nation codes: {len(codes) if codes else 'NOT FOUND'}")
if codes:
    win = data[0x1041930:0x1045300]
    hits = {}
    for c in codes:
        cc = c.encode() if isinstance(c, str) else c
        if len(cc) != 4:
            continue
        imm = cc[::-1]  # big-endian 4CC -> little-endian imm32 bytes
        pat81 = b"\x81\xfe" + imm
        pat3d = b"\x3d" + imm
        n = win.count(pat81) + win.count(pat3d)
        if n:
            hits[cc.decode()] = n
    print(f"INFO independent cmp-esi scan in 0x1041930..0x1045300: {len(hits)} distinct nation codes")
    need = ["Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"]
    miss = [c for c in need if c not in hits]
    good = not miss
    fails += not good
    print(f"{'PASS' if good else 'FAIL':4} 7 mapped codes present in window (missing: {miss})")

# --- .dat side: table_10 payload ---
spec = importlib.util.spec_from_file_location("oldread", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
raw = None
for arch in ("client_db.dat", "server_db.dat"):
    path, d, meta = old._entries(DB, arch)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == 10:
            raw = old._decompress_entry(d, meta["data_base"], e)
            print(f"INFO table_10 in {arch}, payload {len(raw):#x}")
            break
    if raw is not None:
        break
assert raw is not None, "table_10 not found in either archive"

def dat_expect(label, off, hexstr):
    global fails
    e = bytes.fromhex(hexstr.replace(" ", ""))
    got = raw[off:off + len(e)]
    good = got == e
    fails += not good
    print(f"{'PASS' if good else 'FAIL':4} {label:44} @payload {off:#x}: {got.hex()}" + ("" if good else f" exp={e.hex()}"))

dat_expect("duni anchor 6e,6e (472446402670) @0x104", 0x104, "6e 00 00 00 6e 00 00 00")
dat_expect("candidate body prefix 25B @0x0e", 0x0e,
           "01 00 00 00 00 07 00 00 00 a3 04 00 00 01 00 00 00 02 0d 00 00 00 00 07 03")
du = struct.unpack_from("<II", raw, 0x104)
good = (du[0] | (du[1] << 32)) == 472446402670
fails += not good
print(f"{'PASS' if good else 'FAIL':4} duni assembled value = 472446402670: {du[0]|(du[1]<<32)}")

print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
