import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def read_str(raw, p, end, allow_tab=True):
    if p + 4 > end: return None
    ln = struct.unpack_from("<I", raw, p)[0]
    if ln == 0xFFFFFFFF: return (4, None)
    if ln > 8192 or p + 4 + ln > end: return None
    seg = raw[p+4:p+4+ln]
    try: t = seg.decode("utf-8")
    except UnicodeDecodeError: return None
    for ch in t:
        o = ord(ch)
        if o < 32 and not (allow_tab and o == 9): return None
        if o == 0x7F: return None
    return (4+ln, t)

def walk(raw, slots, tail=(), allow_tab=True):
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw)
    for i in range(n):
        if pos + 4 > end: return ("hdr", i)
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4
        cnt = None
        for si, slot in enumerate(slots):
            if slot == "CNT":
                if p >= end: return ("cnt", i)
                cnt = raw[p]; p += 1
            elif slot == "str":
                g = read_str(raw, p, end, allow_tab)
                if g is None: return ("str%d" % si, i)
                p += g[0]
            else:
                if p >= end: return ("s%d" % si, i)
                p += 1
        if cnt:
            for k in range(cnt):
                g = read_str(raw, p, end, allow_tab)
                if g is None: return ("var%d" % k, i)
                p += g[0] + 3
                if p > end: return ("vartail", i)
        for t in tail:
            if p >= end: return ("tail", i)
            p += 1
        if i + 1 < n:
            if p + 4 > end: return ("next", i)
            if struct.unpack_from("<I", raw, p)[0] <= dbid: return ("order", i)
        elif p != end:
            return ("eof %d!=%d" % (p, end), i)
        pos = p
    return None

G = {
 0:(["str","s","str","s","CNT"],()),
 2:(["str","s","CNT"],()),
 3:(["str","s","str","s","str","str","str","s","str","CNT"],("s","s")),
 5:(["str","s","str","str","str","s","str","s","CNT"],()),
 6:(["str","s","str","s","CNT"],()),
 7:(["str","s"],()),
 9:(["str","s","str","s","str","str","CNT"],()),
 18:(["str","str","str","str","s","s","s","s","s"],()),
 19:(["str","CNT"],()),
 21:(["str","str","s","s","CNT"],()),
 23:(["str","s","str","s","str","s","CNT"],()),
 25:(["str","s","str","s","str","CNT"],()),
 35:(["s","s","CNT"],()),
 47:(["str","s","str","s","CNT"],()),
 56:(["str","s","str","s","s"],()),
}
for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"),"base"), (Path(r"scratch/data/lang_update_db.dat"),"upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    okc = 0; bad = []
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        tid = int(nm.split("_")[1])
        raw = m._decompress_entry(data, base, e)
        r = walk(raw, G[tid][0], G[tid][1])
        if r is None: okc += 1
        else: bad.append((nm, r))
    print(label, "ok", okc, "bad", len(bad), bad[:6])
