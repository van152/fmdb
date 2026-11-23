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

def walk18(raw, nstr=4):
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw); rows = []
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4
        strs = []
        for k in range(nstr):
            g = read_str(raw, p, end)
            if g is None: return None, ("str%d" % k, i)
            strs.append(g[1]); p += g[0]
        if p + 5 > end: return None, ("hdr", i)
        a, b, c16, cnt = raw[p], raw[p+1], struct.unpack_from("<H", raw, p+2)[0], raw[p+4]
        p += 5
        vs = []
        for k in range(cnt):
            g = read_str(raw, p, end)
            if g is None: return None, ("var%d" % k, i)
            if p + g[0] + 3 > end: return None, ("varflag%d" % k, i)
            vs.append(g[1]); p += g[0] + 3
        if i + 1 < n:
            if p + 4 > end: return None, ("next", i)
            if struct.unpack_from("<I", raw, p)[0] <= dbid: return None, ("order", i)
        elif p != end: return None, ("eof", i)
        rows.append((dbid, strs, (a, b, c16, cnt), vs)); pos = p
    return rows, None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0; vs = 0
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        if int(nm.split("_")[1]) != 18: continue
        raw = m._decompress_entry(data, base, e)
        rows, err = walk18(raw)
        if rows is None: bad.append((nm, err))
        else:
            ok += 1; tot += len(rows); vs += sum(len(r[3]) for r in rows)
    print(label, "t18 ok", ok, "bad", bad, "rows", tot, "variants", vs)
