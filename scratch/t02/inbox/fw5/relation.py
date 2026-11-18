"""probe the client<->server relation for TID 5 rows (read-only)."""
from __future__ import annotations
import importlib.util, struct, sys

DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID = 5
spec = importlib.util.spec_from_file_location("oldread", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def grab(archive):
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == TID:
            return old._decompress_entry(data, meta["data_base"], e)

c = grab("client_db.dat"); s = grab("server_db.dat")
CS, SS, N = 34, 48, 7
crow = [c[14+i*CS:14+(i+1)*CS] for i in range(N)]
srow = [s[14+i*SS:14+(i+1)*SS] for i in range(N)]

for i in range(N):
    a, b = crow[i], srow[i]
    cp = 0
    while cp < min(len(a), len(b)) and a[cp] == b[cp]:
        cp += 1
    cs_ = 0
    while cs_ < min(len(a), len(b)) - cp and a[len(a)-1-cs_] == b[len(b)-1-cs_]:
        cs_ += 1
    diffs = [(j, a[j], b[j]) for j in range(len(a)) if a[j] != b[j]]
    print(f"row{i}: prefix={cp} suffix={cs_} diffs={len(diffs)}")
    print(f"   client {a.hex()}")
    print(f"   server {b.hex()}")
    print(f"   diffidx {[j for j, _, _ in diffs]}")
    # does client row appear as subsequence of server row?
    it = iter(b)
    sub = all(any(x == y for y in it) for x in a)
    print(f"   client-is-subsequence-of-server: {sub}")
