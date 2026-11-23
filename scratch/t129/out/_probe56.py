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

def walk_pn(raw, min_rec_tail=11):
    """[8B hdr][rec...][zero footer <= 8B]
       rec = [strA][u32 fA][strB][u32 fB][u32 alias][u16][u8]"""
    end = len(raw); pos = 8; recs = []
    while pos < end:
        if end - pos <= 8 and raw[pos:] == b"\x00" * (end - pos):
            break  # footer
        g1 = rd(raw, pos, end)
        if g1 is None: return None, ("A", pos, len(recs))
        a = g1[1]; pos += g1[0]
        if pos + 4 > end: return None, ("fA", pos, len(recs))
        fa = struct.unpack_from("<I", raw, pos)[0]; pos += 4
        g2 = rd(raw, pos, end)
        if g2 is None: return None, ("B", pos, len(recs))
        b = g2[1]; pos += g2[0]
        if pos + 11 > end: return None, ("tr", pos, len(recs))
        fb = struct.unpack_from("<I", raw, pos)[0]
        alias = struct.unpack_from("<I", raw, pos+4)[0]
        u16 = struct.unpack_from("<H", raw, pos+8)[0]
        u8 = raw[pos+10]; pos += 11
        recs.append((a, fa, b, fb, alias, u16, u8))
    return recs, None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0; ch = collections.Counter()
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        r, err = walk_pn(raw)
        if r is None: bad.append((e["path"].split("/")[1], err))
        else:
            ok += 1; tot += len(r)
            for rec in r:
                for s in (rec[0], rec[2]):
                    if s: ch["cjk" if any(0x4e00<=ord(c)<=0x9fff for c in s) else ("ascii" if s.isascii() else "other")] += 1
    print(label, "pn ok", ok, "bad", bad, "records", tot, dict(ch))
