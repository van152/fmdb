"""Validate table_7 rows: names decode, and client/server row-level relation."""
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


def name_ok(body, p):
    if p + 4 > len(body):
        return False
    L = struct.unpack_from("<I", body, p)[0]
    if not 1 <= L <= 120 or p + 4 + L > len(body):
        return False
    try:
        s = body[p + 4:p + 4 + L].decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(ord(c) >= 32 for c in s)


def is_tr(body, p, i):
    if p + 14 > len(body):
        return False
    if body[p] not in (0, 1) or body[p + 13] != 0:
        return False
    if struct.unpack_from("<I", body, p + 1)[0] != i:
        return False
    a, b = struct.unpack_from("<II", body, p + 5)
    return a == b


def rows(archive):
    raw = payload(archive, 7)
    body = raw[14:len(raw) - 8]
    count = struct.unpack_from("<I", raw, 8)[0]
    pos, out = 0, []
    for i in range(count):
        p = pos
        while p + 14 <= len(body):
            if is_tr(body, p, i):
                nxt = p + 14
                if (i == count - 1 and nxt == len(body)) or (i < count - 1 and name_ok(body, nxt)):
                    break
            p += 1
        out.append(body[pos:p + 14])
        pos = p + 14
    return out, body, count


c, bc, cc = rows("client_db.dat")
s, bs, sc = rows("server_db.dat")
print("client rows", len(c), "server rows", len(s), "count", cc, sc)

bad = 0
for i, r in enumerate(c):
    L = struct.unpack_from("<I", r, 0)[0]
    try:
        nm = r[4:4 + L].decode("utf-8")
        good = all(ord(x) >= 32 for x in nm)
    except Exception:
        good = False
    if not good:
        bad += 1
        print("bad name row", i, r[:40].hex(" "))
print("client rows with non-decodable name:", bad)

same_name = 0
same_len = 0
cs_prefix = []
for i, (a, b) in enumerate(zip(c, s)):
    La = struct.unpack_from("<I", a, 0)[0]
    Lb = struct.unpack_from("<I", b, 0)[0]
    if a[4:4 + La] == b[4:4 + Lb]:
        same_name += 1
    if len(a) == len(b):
        same_len += 1
    k = 0
    for x, y in zip(a, b):
        if x != y:
            break
        k += 1
    cs_prefix.append(k)
print("same name both sides:", same_name, "/", len(c))
print("same row length:", same_len, "/", len(c))
print("row common-prefix min/max:", min(cs_prefix), max(cs_prefix))
print("rows identical:", sum(1 for a, b in zip(c, s) if a == b))
print()
print("first 5 names client:", [struct.unpack_from('<I', r, 0)[0] for r in c[:5]])
d = [len(r) - len(q) for r, q in zip(c, s)]
print("server-client row len delta: min", min(d), "max", max(d), "distinct", sorted(set(d))[:12])
