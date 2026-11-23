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

G = {
 0:(["str","s","str","s","CNT"],()), 2:(["str","s","CNT"],()),
 3:(["str","s","str","s","str","str","str","s","str","CNT"],("s","s")),
 5:(["str","s","str","str","str","s","str","s","CNT"],()),
 6:(["str","s","str","s","CNT"],()), 7:(["str","s"],()),
 9:(["str","s","str","s","str","str","CNT"],()),
 18:(["str","str","str","str","s","s","u16","CNT"],()),
 19:(["str","CNT"],()), 21:(["str","str","s","s","CNT"],()),
 23:(["str","s","str","s","str","s","CNT"],()),
 25:(["str","s","str","s","str","CNT"],()), 35:(["s","s","CNT"],()),
 47:(["str","s","str","s","CNT"],()), 56:(["str","s","str","s","s"],()),
}
def walk(raw, tid):
    slots, tail = G[tid]
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw); nstr = 0; nvar = 0
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]; p = pos + 4; cnt = None
        for s in slots:
            if s == "CNT": cnt = raw[p]; p += 1
            elif s == "str":
                g = read_str(raw, p, end)
                if g is None: return None, ("str", i)
                if g[1] is not None: nstr += 1
                p += g[0]
            elif s == "u16": p += 2
            else: p += 1
        for k in range(cnt or 0):
            g = read_str(raw, p, end)
            if g is None: return None, ("var", i)
            nvar += 1; p += g[0] + 3
        for t in tail: p += 1
        if p > end: return None, ("over", i)
        if i + 1 < n:
            if struct.unpack_from("<I", raw, p)[0] <= dbid: return None, ("order", i)
        elif p != end: return None, ("eof %d/%d" % (p, end), i)
        pos = p
    return (nstr, nvar), None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; ns = 0; nv = 0; nrows = 0
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        tid = int(nm.split("_")[1])
        raw = m._decompress_entry(data, base, e)
        r, err = walk(raw, tid)
        if r is None: bad.append((nm, err))
        else:
            ok += 1; ns += r[0]; nv += r[1]
            nrows += struct.unpack_from("<I", raw, 8)[0]
    print(label, "ok", ok, "/", ok + len(bad), "rows", nrows, "strings", ns, "variants", nv, "bad", bad)
