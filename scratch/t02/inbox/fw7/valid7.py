"""Validate table_7 row boundaries: each row should start with u32 name_len + ascii name."""
from __future__ import annotations
import importlib.util, struct, sys

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
count = struct.unpack_from("<I", raw, 8)[0]

def is_trailer(b, p, i, strict=True):
    if p + 14 > len(b): return False
    if b[p] not in (0,1) or b[p+13] != 0: return False
    if struct.unpack_from("<I", b, p+1)[0] != i: return False
    a, bb = struct.unpack_from("<II", b, p+5)
    if a != bb: return False
    if strict:
        # row trailer A is small-ish per earlier samples? keep loose
        pass
    return True

def walk(strict):
    pos, bounds = 0, []
    for i in range(count):
        p = pos
        while p + 14 <= len(body) and not is_trailer(body, p, i, strict):
            p += 1
        if p + 14 > len(body): return bounds, pos, i
        bounds.append((pos, p)); pos = p + 14
    return bounds, pos, None

for strict in (True,):
    bounds, end, failed = walk(strict)
    print("bounds", len(bounds), "end", end, "body", len(body), "failed", failed)
    names = []
    okname = 0
    for i, (a, b) in enumerate(bounds):
        L = struct.unpack_from("<I", body, a)[0]
        s = body[a+4:a+4+L]
        good = L < 200 and a+4+L <= b+14 and all(32 <= c < 127 for c in s)
        names.append((i, a, b-a, L, s.decode('latin1') if good else None))
        okname += good
    print("rows with valid name prefix:", okname, "/", len(bounds))
    for r in names[:6]: print(r)
    print()
    # interesting: check row lens
    lens = [x[2] for x in names]
    print("lens first 20:", lens[:20])
    print("distinct", len(set(lens)))
