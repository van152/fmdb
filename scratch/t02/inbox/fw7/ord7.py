"""Find row trailer ordinals in table_7 body and derive exact row boundaries."""
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
n = len(raw); count = struct.unpack_from("<I", raw, 8)[0]
body = raw[14:n-8]

# locate "01 <u32 i>" trailer candidates, in order
hits = {}
for o in range(0, len(body) - 5):
    if body[o] == 0x01:
        v = struct.unpack_from("<I", body, o+1)[0]
        if v < count:
            hits.setdefault(v, []).append(o)
print("ordinals found:", len(hits), "of", count)
missing = [i for i in range(count) if i not in hits]
print("missing:", missing[:20])
dups = {i: h for i, h in hits.items() if len(h) > 1}
print("ordinals with multiple hits:", len(dups))
seq = [hits[i][0] for i in range(count) if i in hits]
print("first 10 offsets:", seq[:10])
print("monotone:", all(a < b for a, b in zip(seq, seq[1:])))

# trailing bytes after each ordinal marker
for i in range(6):
    o = hits[i][0]
    print(f"row {i} marker at {o}: tail =", body[o:o+20].hex(" "))
print()
for i in range(count-3, count):
    o = hits[i][0]
    print(f"row {i} marker at {o}: tail =", body[o:o+20].hex(" "))
print()
print("body len", len(body), "last marker", seq[-1] if seq else None)
