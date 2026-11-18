"""final check: server row == client row with 14 bytes inserted at offset 21 (TID 5)."""
from __future__ import annotations
import importlib.util, struct, sys

DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID, CS, SS, N = 5, 34, 48, 7
spec = importlib.util.spec_from_file_location("oldread", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def grab(archive):
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == TID:
            raw = old._decompress_entry(data, meta["data_base"], e)
            return raw, struct.unpack_from("<I", raw, 8)[0]

c, cn = grab("client_db.dat"); s, sn = grab("server_db.dat")
fails = 0
def chk(l, ok, x=""):
    global fails; fails += not ok; print(f"{'PASS' if ok else 'FAIL':4} {l} {x}")

chk("client closure 14+7*34+8 == 260", 14+cn*CS+8 == len(c) == 260)
chk("server closure 14+7*48+8 == 358", 14+sn*SS+8 == len(s) == 358)
chk("counts equal (7)", cn == sn == N)
K = 21
for i in range(N):
    a = c[14+i*CS:14+(i+1)*CS]
    b = s[14+i*SS:14+(i+1)*SS]
    pred = a[:K] + b"\x00"*14 + a[K:]
    chk(f"row{i}: server == client[:{K}] + 14*0x00 + client[{K}:]", pred == b)
    # second reading: gap is 14 bytes of per-row server-only fields
    if pred != b:
        print("   pred", pred.hex(), "\n   real", b.hex())
print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
