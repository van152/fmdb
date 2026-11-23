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

def walk(raw, slots):
    n = struct.unpack_from("<I", raw, 8)[0]
    pos = 12; end = len(raw)
    for i in range(n):
        dbid = struct.unpack_from("<I", raw, pos)[0]
        p = pos + 4
        for si, s in enumerate(slots):
            if s == "str":
                g = read_str(raw, p, end)
                if g is None: return ("str%d" % si, i, pos)
                p += g[0]
            else:
                w = int(s[1:])
                if p + w > end: return ("x%d@%d" % (w, si), i, pos)
                p += w
        if i + 1 < n:
            if p + 4 > end: return ("next", i, pos)
            if struct.unpack_from("<I", raw, p)[0] <= dbid: return ("order", i, pos)
        elif p != end: return ("eof", i, p)
        pos = p
    return None

G18 = ["str", "str", "str", "str", "x4", "x1"]
for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []
    for e in lay["entries"]:
        nm = e["path"].split("/")[1][:-4]
        if "person" in nm: continue
        if int(nm.split("_")[1]) != 18: continue
        raw = m._decompress_entry(data, base, e)
        r = walk(raw, G18)
        if r is None: ok += 1
        else: bad.append((nm, r))
    print(label, "t18(4str+u32+u8) ok", ok, "bad", bad)
