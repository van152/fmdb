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

def walk(raw, nstr=4, nflag=5, check_order=True):
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw); ids = []
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4
        for k in range(nstr):
            g = read_str(raw, p, end)
            if g is None: return ("str%d" % k, i, pos, ids)
            p += g[0]
        p += nflag
        if p > end: return ("over", i, pos, ids)
        if check_order and i+1 < n and struct.unpack_from("<I", raw, p)[0] <= dbid:
            return ("order", i, pos, ids)
        if i+1 == n and p != end: return ("eof", i, p, ids)
        ids.append(dbid); pos = p
    return (None, n, pos, ids)

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["12_18.dat"])
r = walk(raw, check_order=False)
print("no-order walk:", r[0], r[1], r[2], "len", len(raw))
ids = r[3]
bad = [(i, ids[i], ids[i+1]) for i in range(len(ids)-1) if ids[i+1] <= ids[i]]
print("order violations:", len(bad), bad[:5])
print("first ids", ids[:8])
