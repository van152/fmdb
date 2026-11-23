"""Relaxed trailer hunt for table_7 row 83 (client)."""
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

start = 15005
for i in (83,):
    print("candidates for row id", i)
    for p in range(start, min(start + 900, len(body) - 4)):
        if struct.unpack_from("<I", body, p + 1)[0] == i and body[p] in (0, 1):
            print(f"  p={p} ({p-start} into row) win={body[p:p+14].hex(' ')} "
                  f"next16={body[p+14:p+30].hex(' ')}")

print()
print("look for 53 00 00 00 anywhere 15005..16500")
for p in range(start, 16500):
    if body[p:p+4] == b"\x53\x00\x00\x00":
        print(f"  {p} ({p-start}): {body[p-1:p+20].hex(' ')}")
