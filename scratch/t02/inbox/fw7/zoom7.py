"""Inspect region where greedy row walk derailed (table_7 client)."""
from __future__ import annotations
import importlib.util, struct

OLD = r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py"
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
spec = importlib.util.spec_from_file_location("oldread", OLD)
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def payload(archive, tid):
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    raise SystemExit("absent")

raw = payload("client_db.dat", 7)
body = raw[14:len(raw)-8]
a, b = 2000, 2560
for o in range(a, b, 16):
    chunk = body[o:o+16]
    print(f"{o:6d} {chunk.hex(' '):<48} " + "".join(chr(c) if 32 <= c < 127 else '.' for c in chunk))
