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
    for ch in t:
        o = ord(ch)
        if (o < 32 and o != 9) or o == 0x7F: return None
    return (4+ln, t)

G = {
 0:["str","s","str","s"], 2:["str","s"], 3:["str","s","str","s","str","str","str","s","str"],
 5:["str","s","str","str","str","s","str","s"], 6:["str","s","str","s"], 7:["str","s"],
 9:["str","s","str","s","str","str"], 19:["str"], 21:["str","str","s","s"],
 23:["str","s","str","s","str","s"], 25:["str","s","str","s","str"], 35:["s","s"],
 47:["str","s","str","s"],
}

def rows(raw, tid):
    g = G[tid]; n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw); out = []
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]; p = pos + 4
        for s in g:
            if s == "str":
                got = read_str(raw, p, end)
                if got is None: return out
                p += got[0]
            else: p += 1
        # count + variants
        cnt = raw[p]; p += 1
        vs = []
        for k in range(cnt):
            got = read_str(raw, p, end)
            if got is None: break
            vs.append(got[1]); p += got[0] + 3
        out.append((dbid, raw[pos+4:p], vs))
        pos = p
    return out

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
for nm, tid in [("8_9.dat",9), ("8_3.dat",3), ("8_21.dat",21), ("8_25.dat",25), ("8_0.dat",0), ("8_2.dat",2), ("8_7.dat",7)]:
    raw = m._decompress_entry(data, base, ent[nm])
    rs = rows(raw, tid)
    print("==", nm, "rows", len(rs))
    for r in rs[:3]:
        # re-parse body to strings
        body = r[1]; p = 0; strs = []
        while True:
            got = read_str(body, p, len(body))
            if got is None: break
            strs.append(got[1]); p += got[0]
        print("   dbid", r[0], "strs", strs, "vars", r[2])
