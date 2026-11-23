import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}

def read_str(raw, p):
    if p+4 > len(raw): return None
    ln = struct.unpack_from("<I", raw, p)[0]
    if ln == 0xffffffff: return (4, None)
    if ln > 200 or p+4+ln > len(raw): return None
    try: t = raw[p+4:p+4+ln].decode("utf-8")
    except UnicodeDecodeError: return None
    if any(ord(c) < 32 for c in t): return None
    return (4+ln, t)

raw = m._decompress_entry(data, base, ent["8_18.dat"])
n = struct.unpack_from("<I", raw, 8)[0]
pos = 12
gaps = collections.Counter()
rows = []
for i in range(min(n, 200)):
    dbid = struct.unpack_from("<I", raw, pos)[0]
    p = pos + 4
    parts = []
    for k in range(3):
        g = read_str(raw, p)
        if g is None: break
        parts.append(g[1]); p += g[0]
    # now find next dbid: scan minimal gap
    found = None
    for q in range(p, min(p+40, len(raw)-8)):
        v = struct.unpack_from("<I", raw, q)[0]
        if v > dbid and read_str(raw, q+4) is not None:
            found = (q, v); break
    if not found:
        print("row", i, "dbid", dbid, "parts", parts, "no next; ctx", raw[p:p+40].hex(" ")); break
    gap = raw[p:found[0]]
    gaps[(len(gap), gap.hex())] += 1
    rows.append((dbid, parts, gap.hex(), found[1]))
    pos = found[0]
for k, v in gaps.most_common(12): print("gap", k[0], v, k[1][:80])
print("rows", len(rows))
for r in rows[:8]: print(r)
