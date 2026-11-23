import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
import lang_update_layer as L
from pathlib import Path

G18 = ["str","str","x4","x4","str","s"]
G56 = ["str","s","str","s","s"]

def walk(raw, g, start=12):
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = start; end = len(raw); rows=[]; prev=0
    for i in range(n):
        if pos+4 > end: return None, i, pos
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos+4
        fields=[]
        for slot in g:
            if slot=="str":
                got = L._try_string(raw, p, end)
                if got is None: return None, i, p
                fields.append(got[1]); p += got[0]
            elif slot=="s":
                if p>=end: return None,i,p
                fields.append(raw[p]); p+=1
            else:
                w=int(slot[1])
                if p+w>end: return None,i,p
                fields.append(raw[p:p+w].hex()); p+=w
        if i+1<n:
            if p+4>end: return None,i,p
            v=struct.unpack_from("<I", raw, p)[0]
            if v<=dbid: return None,i,p
        elif p!=end:
            return None,i,p
        rows.append((dbid,fields)); pos=p
    return rows, n, pos

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"),"base"), (Path(r"scratch/data/lang_update_db.dat"),"upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        tid = int(nm.split("_")[1])
        if tid not in (18,56): continue
        raw = m._decompress_entry(data, base, e)
        g = G18 if tid==18 else G56
        r = walk(raw, g)
        if r[0] is None:
            print(label, nm, "FAIL at row", r[1], "pos", r[2], "len", len(raw), "ctx", raw[max(0,r[2]-8):r[2]+40].hex(" "))
    print(label, "done 18/56 pass")
