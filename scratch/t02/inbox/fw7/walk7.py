"""t02-f: probe variable-length row framing for table_7."""
from __future__ import annotations
import importlib.util, struct, sys

OLD = r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py"
DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID = 7

spec = importlib.util.spec_from_file_location("oldread", OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def payload(archive, tid):
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    raise SystemExit("absent")


def uleb(buf, p):
    v = 0
    s = 0
    while True:
        b = buf[p]
        p += 1
        v |= (b & 0x7F) << s
        if not b & 0x80:
            return v, p
        s += 7


raw = payload("client_db.dat", TID)
n = len(raw)
count = struct.unpack_from("<I", raw, 8)[0]
body = raw[14:n - 8]
print("len", n, "count", count, "body", len(body))
print("rows head:", body[:160].hex(" "))
print()
# try uleb length-prefixed rows
for start in (0,):
    p = start
    lens = []
    ok = True
    for i in range(count):
        try:
            L, q = uleb(body, p)
        except IndexError:
            ok = False
            break
        lens.append((L, q - p))
        p += L
    print(f"uleb rows: consumed={p} body={len(body)} closure={p == len(body)} ok={ok}")
    if lens:
        print("first 12 (len,prefixbytes):", lens[:12])
        print("min/max len:", min(l[0] for l in lens), max(l[0] for l in lens))

# try u8 length
p = 0
lens8 = []
for i in range(count):
    L = body[p]
    lens8.append(L)
    p += L
print(f"u8 rows: consumed={p} closure={p == len(body)}")
print("u8 first 40:", lens8[:40])
