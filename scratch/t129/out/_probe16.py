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

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm in ["12_18.dat", "18_18.dat", "15_18.dat"]:
    raw = m._decompress_entry(data, base, ent[nm])
    a = anchors_greedy(raw)
    print("==", nm, "rows", len(a))
    for i in range(min(8, len(a))):
        s = a[i]; stop = a[i+1] if i+1 < len(a) else len(raw)
        print(f" row{i} dbid={struct.unpack_from('<I',raw,s)[0]} body={raw[s+4:stop].hex(' ')}")
