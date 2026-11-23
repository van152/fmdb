import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

def anchors_greedy(raw):
    n = struct.unpack_from("<I", raw, 8)[0]
    end = len(raw); out = []; pos = 12
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        out.append(pos)
        p = pos + 4
        while True:
            g = L._try_string(raw, p, end)
            if g is None: break
            p += g[0]
        found = None
        for q in range(p, min(p + 64, end - 8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and L._try_string(raw, q + 4, end) is not None:
                found = q; break
        if found is None: return out
        pos = found
    return out

data, lay = m._read_archive(Path(r"scratch/data/lang_update_db.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["24_18.dat"])
a = anchors_greedy(raw)
for i, s in enumerate(a):
    stop = a[i+1] if i+1 < len(a) else len(raw)
    body = raw[s+4:stop]
    # parse leading strings
    p = 0; strs = []
    while True:
        g = L._try_string(body, p, len(body))
        if g is None: break
        strs.append(g[1]); p += g[0]
    print(f"{i:3d} dbid={struct.unpack_from('<I',raw,s)[0]:<10} strs={[x for x in strs]} rest={body[p:].hex(' ')}")
