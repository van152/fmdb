"""Hexdump helper for table_7 rows with candidate row boundaries."""
from __future__ import annotations
import importlib.util, struct, sys

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
n = len(raw); body = raw[14:n-8]
starts = [0, 190, 381, 618, 826, 1173, 1392, 1539, 1743, 2050]
for i, s in enumerate(starts):
    e = starts[i+1] if i+1 < len(starts) else s + 220
    seg = body[s:min(e, len(body))]
    print(f"--- row at {s} len {e-s} ---")
    for o in range(0, len(seg), 16):
        chunk = seg[o:o+16]
        print(f"{s+o:6d} {chunk.hex(' '):<48} " +
              "".join(chr(c) if 32 <= c < 127 else '.' for c in chunk))
    print()
