import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

def anchors_greedy(raw, limit=None):
    n = struct.unpack_from("<I", raw, 8)[0]
    end = len(raw)
    out = []
    pos = 12
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        out.append(pos)
        p = pos + 4
        # skip strings
        while True:
            g = L._try_string(raw, p, end)
            if g is None: break
            p += g[0]
        # find next anchor: first q>=p where u32 > dbid and string follows
        found = None
        for q in range(p, min(p + 64, end - 8)):
            v = struct.unpack_from("<I", raw, q)[0]
            if v > dbid and L._try_string(raw, q + 4, end) is not None:
                found = q; break
        if found is None:
            return out, i
        pos = found
    return out, n

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
raw = m._decompress_entry(data, base, ent["8_18.dat"])
a, k = anchors_greedy(raw)
print("anchors", len(a), "stopped at", k, "count", struct.unpack_from("<I", raw, 8)[0])
bodies = []
for i in range(len(a)):
    stop = a[i+1] if i+1 < len(a) else len(raw)
    bodies.append(raw[a[i]+4:stop])
print("body lens", collections.Counter(len(b) for b in bodies).most_common(10))
lay2 = L.infer_layout(bodies, max_rows=60)
print("inferred", lay2)
