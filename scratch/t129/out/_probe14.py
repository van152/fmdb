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
        if found is None: return out, False
        pos = found
    return out, True

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"),"base"), (Path(r"scratch/data/lang_update_db.dat"),"upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    for tid in (18, 56):
        tails = collections.Counter(); nstr = collections.Counter(); bad = 0
        for e in lay["entries"]:
            nm = e["path"].split("/")[1][:-4]
            if "person" in nm: continue
            if int(nm.split("_")[1]) != tid: continue
            raw = m._decompress_entry(data, base, e)
            a, ok = anchors_greedy(raw)
            if not ok: bad += 1; continue
            for i, s in enumerate(a):
                stop = a[i+1] if i+1 < len(a) else len(raw)
                p = s + 4; k = 0
                while p < stop:
                    g = L._try_string(raw, p, stop)
                    if g is None: break
                    p += g[0]; k += 1
                nstr[k] += 1
                tails[(stop - p, raw[p:stop].hex() if stop-p <= 6 else "LONG")] += 1
        print(label, "t%d" % tid, "files_bad", bad, "strings/row", dict(nstr))
        print("   trailers", tails.most_common(6))
