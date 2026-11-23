"""Trace name-check walk rows 70..90 for table_7 client to see why it derails."""
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


def name_ok(p):
    if p + 4 > len(body):
        return False
    L = struct.unpack_from("<I", body, p)[0]
    if not 1 <= L <= 120 or p + 4 + L > len(body):
        return False
    return all(32 <= c < 127 for c in body[p + 4:p + 4 + L])


def is_tr(p, i):
    if p + 14 > len(body):
        return False
    if body[p] not in (0, 1) or body[p + 13] != 0:
        return False
    if struct.unpack_from("<I", body, p + 1)[0] != i:
        return False
    a, b = struct.unpack_from("<II", body, p + 5)
    return a == b


pos = 0
for i in range(90):
    p, hit = pos, None
    while p + 14 <= len(body):
        if is_tr(p, i):
            nxt = p + 14
            if i == 207 and nxt == len(body):
                hit = p; break
            if name_ok(nxt):
                hit = p; break
        p += 1
    if hit is None:
        print(f"FAIL row {i} pos {pos}")
        for o in range(max(0, pos - 16), min(pos + 320, len(body)), 16):
            ch = body[o:o + 16]
            print(f"{o:6d} {ch.hex(' '):<48} " + "".join(chr(c) if 32 <= c < 127 else '.' for c in ch))
        break
    nm = body[pos + 4:pos + 4 + struct.unpack_from('<I', body, pos)[0]]
    print(f"row {i:3d} {pos:6d}..{hit:6d} len={hit-pos:4d} tr={body[hit:hit+14].hex(' ')} "
          f"name={nm.decode('latin1')!r}")
    pos = hit + 14
