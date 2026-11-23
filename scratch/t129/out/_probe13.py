import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

G18 = ["str"]*5 + ["s"]

def walk(raw, g):
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw)
    for i in range(n):
        if pos+4 > end: return ("hdr", i, pos)
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4
        for si, slot in enumerate(g):
            if slot == "str":
                got = L._try_string(raw, p, end)
                if got is None: return ("slot%d" % si, i, p)
                p += got[0]
            else:
                if p >= end: return ("slot%d" % si, i, p)
                p += 1
        if i+1 < n:
            if p+4 > end: return ("next", i, p)
            if struct.unpack_from("<I", raw, p)[0] <= dbid: return ("order", i, p)
        elif p != end:
            return ("tail", i, p)
        pos = p
    return None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"),"base"), (Path(r"scratch/data/lang_update_db.dat"),"upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    bad = []
    ok = 0
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        tid = int(nm.split("_")[1])
        if tid != 18: continue
        raw = m._decompress_entry(data, base, e)
        r = walk(raw, G18)
        if r is None: ok += 1
        else: bad.append((nm, r))
    print(label, "t18 ok", ok, "bad", bad)
