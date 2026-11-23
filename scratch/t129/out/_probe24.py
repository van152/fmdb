import sys, struct, collections
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
raw = m._decompress_entry(data, base, ent["12_18.dat"])
n = struct.unpack_from("<I", raw, 8)[0]
end = len(raw); pos = 12; rows = []
for i in range(n):
    dbid = struct.unpack_from("<I", raw, pos)[0]
    p = pos + 4; strs = []
    while True:
        g = read_str(raw, p, end)
        if g is None: break
        strs.append(g[1]); p += g[0]
    # next anchor: search forward for increasing dbid + string, minimal
    found = None
    for q in range(p, min(p + 80, end - 8)):
        v = struct.unpack_from("<I", raw, q)[0]
        if v > dbid and read_str(raw, q + 4, end) is not None:
            found = q; break
    if found is None:
        found = end
    rows.append((pos, dbid, strs, raw[p:found].hex(" ")))
    pos = found
    if pos >= end: break
print("rows walked", len(rows), "of", n, "end pos", pos, "len", end)
print("remainder shapes:", collections.Counter(r[3] for r in rows).most_common(8))
print("nstr distribution:", collections.Counter(len(r[2]) for r in rows).most_common(6))
