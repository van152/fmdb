import sys, struct, collections
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
        if found is None:
            return out, (i == n - 1)
        pos = found
    return out, True

res = collections.Counter()
per_file = {}
for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"),"base"), (Path(r"scratch/data/lang_update_db.dat"),"upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        tid = int(nm.split("_")[1])
        if tid != 18: continue
        raw = m._decompress_entry(data, base, e)
        a, ok = anchors_greedy(raw)
        c = collections.Counter()
        for i, s in enumerate(a):
            stop = a[i+1] if i+1 < len(a) else len(raw)
            p = s + 4; k = 0
            while p < stop:
                g = L._try_string(raw, p, stop)
                if g is None: break
                p += g[0]; k += 1
            c[(k, stop - p, raw[p:stop].hex() if stop - p <= 8 else "LONG%d" % (stop-p))] += 1
        per_file[label + ":" + nm] = (ok, len(a), c.most_common(4))
for k, v in per_file.items(): print(k, v)
