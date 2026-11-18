"""verify the recorded framework for TID 5 (read-only)."""
from __future__ import annotations
import importlib.util, struct, sys

DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
TID = 5
HEAD = bytes.fromhex("03017461642ef10d")

spec = importlib.util.spec_from_file_location("oldread", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def grab(archive):
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", e.get("name", ""))) == TID:
            return old._decompress_entry(data, meta["data_base"], e)
    return None

fails = 0
def chk(label, cond, extra=""):
    global fails
    fails += not cond
    print(f"{'PASS' if cond else 'FAIL':4} {label} {extra}")

res = {}
for archive, stride in (("client_db.dat", 34), ("server_db.dat", 48)):
    raw = grab(archive)
    assert raw is not None, archive
    n = struct.unpack_from("<I", raw, 8)[0]
    chk(f"{archive} header 03017461642ef10d", raw[:8] == HEAD, raw[:8].hex())
    chk(f"{archive} count@8 == 7", n == 7, f"n={n}")
    chk(f"{archive} closure 14+{n}*{stride}+8 == {len(raw)}", 14 + n * stride + 8 == len(raw),
        f"14+{n*stride}+8={14+n*stride+8} len={len(raw)}")
    tail = raw[len(raw) - 8:]
    res[archive] = (raw, n, stride)
    print(f"     tail8 = {tail.hex()}   pad@12..13 = {raw[12:14].hex()}")
    for i in range(n):
        b = 14 + i * stride
        print(f"     row{i} @0x{b:03x}: {raw[b:b+stride].hex()}")
    # split detection: does row start align with a repeated 2-byte lead pattern?
    print(f"     row leads: {[raw[14+i*stride:16+i*stride].hex() for i in range(n)]}")

c, cn, cs = res["client_db.dat"]
s, sn, ss = res["server_db.dat"]
chk("count equal", cn == sn, f"{cn} vs {sn}")
chk("tail8 identical", c[-8:] == s[-8:], f"{c[-8:].hex()} / {s[-8:].hex()}")
# relation probe: server row prefix vs client row
same34 = sum(1 for i in range(cn) if s[14+i*ss:14+i*ss+cs] == c[14+i*cs:14+i*cs+cs])
chk("server row[:34] == client row (all rows)", same34 == cn, f"{same34}/{cn} rows match")
print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
