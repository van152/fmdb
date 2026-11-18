"""Zoom on region after row 0 in table_7 client body."""
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
body = raw[14:len(raw) - 8]

for a, b in ((0, 200), (14900, 15120), (36500, 36802)):
    print(f"===== {a}..{b} =====")
    for o in range(a, min(b, len(body)), 16):
        ch = body[o:o + 16]
        print(f"{o:6d} {ch.hex(' '):<48} " + "".join(chr(c) if 32 <= c < 127 else '.' for c in ch))
    print()
