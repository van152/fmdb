"""Commander's independent spot-check of t01m stadium claims.
Run from fm24-db root: py -V:3.12 -I scripts/t01m_spotcheck.py
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

data = open(str(_cfg.EDITOR_EXE), "rb").read()
def expect(label, off, hexstr):
    e = bytes.fromhex(hexstr.replace(" ", ""))
    got = data[off:off + len(e)]
    check(label, got == e, f"@{off:#x}: {got.hex()}" + ("" if got == e else f" exp={e.hex()}"))

# reader structure
expect("test bpl,bpl @0x1183f51", 0x1183f51, "40 84 ed")
expect("je common tail @0x1183f54", 0x1183f54, "0f 84 5c 04 00 00")
expect("ret @0x11844dd", 0x11844dd, "c3")
expect("row flag gate test byte [rsi],0x10 @0x11843dd", 0x11843dd, "f6 06 10")
# Scpy chain
expect("Scpy getter cmp edx @0x118688c", 0x118688c, "81 fb 79 70 63 53")
expect("Scpy getter obj+0x6c @0x1186898", 0x1186898, "8b 77 6c")
expect("Scpy reader dest @0x1183f5a", 0x1183f5a, "4c 8d 7b 6c")
expect("Scpy width 4 @0x1183f65", 0x1183f65, "41 b8 04 00 00 00")
expect("Scpy stream call @0x1183f6e", 0x1183f6e, "ff 50 28")
# Sscy / Secy
expect("Sscy getter @0x1186840", 0x1186840, "81 fb 79 63 73 53")
expect("Secy reader dest obj+0x7c @0x1183f88", 0x1183f88, "48 8d 53 7c")
# Scti (client+3 / server+146 / obj+0x50)
expect("Scti getter @0x1186b5d", 0x1186b5d, "81 fb 69 74 63 53")
expect("Scti reader dest obj+0x50 @0x1184427", 0x1184427, "48 8d 53 50")
expect("Scti width 4 @0x118442e", 0x118442e, "41 b8 04 00 00 00")
# Slat / Slon
expect("Slat getter @0x1186330", 0x1186330, "81 fb 74 61 6c 53")
expect("Slat reader dest obj+0x60 @0x1184495", 0x1184495, "48 8d 53 60")
expect("Slon getter @0x118633c", 0x118633c, "81 fb 6e 6f 6c 53")
expect("Slon reader dest obj+0x64 @0x11844b2", 0x11844b2, "48 8d 53 64")
# helper chain for obj+0x34
expect("helper dest obj+0x34 @0x1184481", 0x1184481, "48 8d 4b 34")
expect("helper call @0x1184488", 0x1184488, "e8 f3 3a c3 ff")

# --- data side ---
spec = importlib.util.spec_from_file_location("o", str(_cfg.OLD_DBDAT_READER))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
DB = str(_cfg.GAME_DB_DIR)

def get_table(arch, tid):
    path, d, meta = old._entries(DB, arch)
    for e in meta["entries"]:
        if old._table_id(e.get("path", "")) == tid:
            return old._decompress_entry(d, meta["data_base"], e)
    return None

c21 = get_table("client_db.dat", 21)
s21 = get_table("server_db.dat", 21)
check("client table_21 payload 1,839,716 B", c21 is not None and len(c21) == 1839716, f"{len(c21):,}" if c21 else "-")
check("server table_21 payload 8,762,775 B", s21 is not None and len(s21) == 8762775, f"{len(s21):,}" if s21 else "-")
check("client count=48413 @8", struct.unpack_from("<I", c21, 8)[0] == 48413)

def crow(i): return 14 + i * 38
def srow(i): return 14 + i * 181

# old-repo L1 anchors + t01m city anchors: Scti@client+3
CITIES = {67: ("Anfield", 1061), 71: ("Old Trafford", 1075), 430: ("Bernabéu", 316), 12048: ("Munich", 540)}
for row, (name, city) in CITIES.items():
    v = struct.unpack_from("<I", c21, crow(row) + 3)[0]
    check(f"row{row} ({name}) Scti@+3 == {city}", v == city, str(v))

# server[143:181] == client[0:38] sweep (sample 40 rows + row 0 and last)
bad = 0
for i in list(range(40)) + [48412]:
    if s21[srow(i) + 143:srow(i) + 181] != c21[crow(i):crow(i) + 38]:
        bad += 1
check("server[143:181]==client[0:38] (41-row sample)", bad == 0, f"bad={bad}")

# ordinal @client+25 & duni @client+29 (old repo L1; E20 erratum: ordinal not native rdui)
bad_ord = sum(1 for i in range(50) if struct.unpack_from("<I", c21, crow(i) + 25)[0] != i)
check("client +25 ordinal == row index (50 rows)", bad_ord == 0, f"bad={bad_ord}")
bad_duni = sum(1 for i in range(50) if struct.unpack_from("<II", c21, crow(i) + 29)[0] != struct.unpack_from("<II", c21, crow(i) + 33)[0])
check("client +29 dup-u32 duni (50 rows)", bad_duni == 0, f"bad={bad_duni}")

# Slat/Slon wire: client+17/+21 float32 finite lat/lon (old repo L1)
import math
ok = True
for i in range(0, 400, 40):
    lat, lon = struct.unpack_from("<ff", c21, crow(i) + 17)
    if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
        ok = False
        print(f"  INFO row {i}: lat={lat} lon={lon}")
check("Slat/Slon float32 plausible ranges (10-row sample)", ok)

print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
