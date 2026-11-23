import sys, struct, collections
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def rd(raw, p, end):
    if p + 4 > end: return None
    ln = struct.unpack_from("<I", raw, p)[0]
    if ln == 0xFFFFFFFF: return (4, None)
    if ln > 65536 or p + 4 + ln > end: return None
    try: t = raw[p+4:p+4+ln].decode("utf-8")
    except UnicodeDecodeError: return None
    for ch in t:
        o = ord(ch)
        if (o < 32 and o != 9) or o == 0x7F: return None
    return (4+ln, t)

def walk_pn(raw, slots=4):
    pos = 8; end = len(raw); recs = []
    while pos < end:
        strs = []
        for k in range(slots):
            g = rd(raw, pos, end)
            if g is None: return None, ("s%d" % k, pos, len(recs))
            strs.append(g[1]); pos += g[0]
        if pos + 7 > end: return None, ("tail", pos, len(recs))
        alias = struct.unpack_from("<I", raw, pos)[0]; z = struct.unpack_from("<H", raw, pos+4)[0]
        w = raw[pos+6]; pos += 7
        recs.append((strs, alias, z, w))
    return recs, None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0; chars = collections.Counter()
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        r, err = walk_pn(raw)
        if r is None: bad.append((e["path"], err))
        else:
            ok += 1; tot += len(r)
            for rec in r:
                for s in rec[0]:
                    if s:
                        chars["cjk" if any(0x4e00<=ord(c)<=0x9fff for c in s) else ("ascii" if s.isascii() else "other")] += 1
    print(label, "pn ok", ok, "bad", bad, "records", tot, dict(chars))
