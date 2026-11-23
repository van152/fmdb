import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def read_str(raw, p, end):
    if p + 4 > end: return None
    ln = struct.unpack_from("<I", raw, p)[0]
    if ln == 0xFFFFFFFF: return (4, None)
    if ln > 8192 or p + 4 + ln > end: return None
    try: t = raw[p+4:p+4+ln].decode("utf-8")
    except UnicodeDecodeError: return None
    if any(ord(c) < 32 or ord(c) == 0x7F for c in t): return None
    return (4+ln, t)

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}

for nm in ["12_18.dat", "8_18.dat", "15_18.dat", "11_18.dat", "7_18.dat", "19_18.dat", "24_18.dat", "1000000_18.dat"]:
    raw = m._decompress_entry(data, base, ent[nm])
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw)
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4
        for k in range(4):
            g = read_str(raw, p, end)
            if g is None: break
            p += g[0]
        # tail: consume to next row anchor: look for next increasing dbid+str at p..p+16
        nxt = None
        for q in range(p, min(p+16, end-8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and read_str(raw, q+4, end) is not None:
                nxt = q; break
        if nxt is None:
            print(nm, "row", i, "no anchor, p", p, "ctx", raw[p:p+24].hex(" ")); break
        if i < 3: print(nm, "row", i, "tailbytes", nxt-p, raw[p:nxt].hex(" "))
        pos = nxt
