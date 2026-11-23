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

def walk_pn(raw):
    """payload: 6B magic+2B version, then records at 8:
       [u32 lenA][A][u32 fA][u32 lenB][B][u32 fB][u32 alias][u16][u8]; EOF = 4 zero bytes"""
    pos = 8; end = len(raw); recs = []
    while pos < end - 4:
        g1 = rd(raw, pos, end)
        if g1 is None: return None, ("A", pos, len(recs))
        a = g1[1]; pos += g1[0]
        if pos + 4 > end: return None, ("fA", pos, len(recs))
        fa = struct.unpack_from("<I", raw, pos)[0]; pos += 4
        g2 = rd(raw, pos, end)
        if g2 is None: return None, ("B", pos, len(recs))
        b = g2[1]; pos += g2[0]
        if pos + 4 > end: return None, ("fB", pos, len(recs))
        fb = struct.unpack_from("<I", raw, pos)[0]; pos += 4
        if pos + 7 > end: return None, ("tr", pos, len(recs))
        alias = struct.unpack_from("<I", raw, pos)[0]
        u16 = struct.unpack_from("<H", raw, pos+4)[0]
        u8 = raw[pos+6]; pos += 7
        recs.append((a, fa, b, fb, alias, u16, u8))
    if raw[pos:] != b"\x00" * (end - pos):
        return None, ("eof", pos, len(recs), raw[pos:].hex())
    return recs, None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0; ch = collections.Counter(); f = collections.Counter(); tr = collections.Counter()
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        r, err = walk_pn(raw)
        if r is None: bad.append((e["path"], err))
        else:
            ok += 1; tot += len(r)
            for rec in r:
                for s in (rec[0], rec[2]):
                    if s: ch["cjk" if any(0x4e00<=ord(c)<=0x9fff for c in s) else ("ascii" if s.isascii() else "other")] += 1
                f[(rec[1], rec[3])] += 1
                tr[(rec[4], rec[5], rec[6])] += 1
    print(label, "pn ok", ok, "bad", bad, "records", tot, dict(ch))
    print("   flag pairs", f.most_common(4))
    print("   trailers", tr.most_common(5))
