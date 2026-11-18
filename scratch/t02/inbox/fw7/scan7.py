"""Explore table_7 body layout: candidate row starts via u32-length-prefixed strings."""
from __future__ import annotations
import importlib.util, struct, sys, re

OLD = r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py"
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID = 7
spec = importlib.util.spec_from_file_location("oldread", OLD)
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def payload(archive, tid):
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    raise SystemExit("absent")

raw = payload("client_db.dat", TID)
n = len(raw); count = struct.unpack_from("<I", raw, 8)[0]
body = raw[14:n-8]
print("count", count, "body", len(body))
print("tail 64:", raw[n-72:].hex(" "))
print()
# positions where u32 L in 2..80 and next L bytes are printable ascii
cands = []
for p in range(0, len(body)-4):
    L = struct.unpack_from("<I", body, p)[0]
    if 2 <= L <= 80 and p + 4 + L <= len(body):
        s = body[p+4:p+4+L]
        if all(32 <= c < 127 for c in s):
            cands.append((p, L, s.decode()))
print("n cands", len(cands))
for c in cands[:60]:
    print(c)
