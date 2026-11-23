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
 0:(["str","s","str","s","CNT"],()), 2:(["str","s","CNT"],()),
 3:(["str","s","str","s","str","str","str","s","str","CNT"],("s","s")),
 5:(["str","s","str","str","str","s","str","s","CNT"],()),
 6:(["str","s","str","s","CNT"],()), 7:(["str","s"],()),
 9:(["str","s","str","s","str","str","CNT"],()),
 18:(["str","str","str","str","s","s","s","s","CNT"],()),
 19:(["str","CNT"],()), 21:(["str","str","s","s","CNT"],()),
 23:(["str","s","str","s","str","s","CNT"],()),
 25:(["str","s","str","s","str","CNT"],()), 35:(["s","s","CNT"],()),
 47:(["str","s","str","s","CNT"],()), 56:(["str","s","str","s","s"],()),
}

def parse(raw, tid):
    slots, tail = G[tid]
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw); rows = []
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]; p = pos + 4
        strs = []; cnt = None
        for s in slots:
            if s == "CNT":
                cnt = raw[p]; p += 1
            elif s == "str":
                g = read_str(raw, p, end)
                if g is None: return None
                strs.append(g[1]); p += g[0]
            else: p += 1
        vs = []
        for k in range(cnt or 0):
            g = read_str(raw, p, end)
            if g is None: return None
            vs.append(g[1]); p += g[0] + 3
        for t in tail: p += 1
        rows.append((dbid, strs, vs)); pos = p
    return rows

def names(path, lang, tid):
    data, lay = m._read_archive(Path(path)); base = lay["data_base"]
    ent = {e["path"].split("/")[1]: e for e in lay["entries"]}
    key = "%d_%d.dat" % (lang, tid)
    raw = m._decompress_entry(data, base, ent[key])
    rows = parse(raw, tid)
    return {r[0]: r[1][0] for r in rows}, raw

BASE = r"D:\tmp2b\fm24\input\lang_db_2400.dat"
UPD = r"scratch/data/lang_update_db.dat"
# nations: find China
n8, _ = names(BASE, 8, 9)
zh, _ = names(BASE, 1000002, 9)
for k in n8:
    if n8[k] in ("China", "China PR", "England", "Brazil"):
        print("nation", k, n8[k], "zh:", zh.get(k))
c8, _ = names(BASE, 8, 3)
czh, _ = names(BASE, 1000002, 3)
print("club676", c8.get(676), czh.get(676))
comp8, _ = names(BASE, 8, 25)
compzh, _ = names(BASE, 1000002, 25)
print("comp130932", comp8.get(130932), compzh.get(130932))
st8, _ = names(BASE, 8, 21)
stzh, _ = names(BASE, 1000002, 21)
print("stadium600", st8.get(600), stzh.get(600))
aw8, _ = names(BASE, 8, 0)
awzh, _ = names(BASE, 1000002, 0)
print("award102406", aw8.get(102406), awzh.get(102406))
# update layer zh
u_zh, _ = names(UPD, 1000002, 9)
print("upd zh t9 count", len(u_zh), list(u_zh.items())[:3])
