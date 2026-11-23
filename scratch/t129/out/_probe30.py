import sys, struct, json, collections
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
    for ch in t:
        o = ord(ch)
        if (o < 32 and o != 9) or o == 0x7F: return None
    return (4+ln, t)

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for tid in (0,2,3,5,6,7,9,18,19,21,23,25,35,47,56):
    nm = "8_%d.dat" % tid
    raw = m._decompress_entry(data, base, ent[nm])
    n = struct.unpack_from("<I", raw, 8)[0]
    print("=== t%d %s count=%d len=%d" % (tid, nm, n, len(raw)))
    pos = 12; end = len(raw)
    for i in range(min(2, n)):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4; strs = []
        while True:
            g = read_str(raw, p, end)
            if g is None: break
            strs.append(g[1]); p += g[0]
        # find next anchor
        found = end
        for q in range(p, min(p + 96, end - 8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and read_str(raw, q + 4, end) is not None:
                found = q; break
        print("  row%d dbid=%d strs=%r rest=%s" % (i, dbid, strs, raw[p:found].hex(" ")[:60]))
        pos = found
