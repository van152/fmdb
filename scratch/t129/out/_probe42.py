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

def walk_pn(raw, start=8):
    pos = start; end = len(raw); recs = []
    while pos < end:
        g1 = read_str(raw, pos, end)
        if g1 is None: return None, ("s1", pos, len(recs))
        p = pos + g1[0]
        if p + 4 > end: return None, ("p1", pos, len(recs))
        pad1 = struct.unpack_from("<I", raw, p)[0]; p += 4
        g2 = read_str(raw, p, end)
        if g2 is None: return None, ("s2", pos, len(recs))
        p += g2[0]
        if p + 4 > end: return None, ("p2", pos, len(recs))
        pad2 = struct.unpack_from("<I", raw, p)[0]; p += 4
        if p + 4 > end: return None, ("al", pos, len(recs))
        alias = struct.unpack_from("<I", raw, p)[0]; p += 4
        if alias != 0xFFFFFFFF:
            g3 = read_str(raw, p, end)
            if g3 is None: return None, ("s3", pos, len(recs))
            p += g3[0]
        if p + 3 > end: return None, ("tail", pos, len(recs))
        recs.append((g1[1], g2[1], pad1, pad2, alias, raw[p:p+3].hex()))
        p += 3
        pos = p
    return recs, None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0; samples = {}
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        r, err = walk_pn(raw)
        if r is None: bad.append((e["path"], err))
        else:
            ok += 1; tot += len(r)
            if len(r) > 1000: samples[e["path"]] = (len(r), r[:2])
    print(label, "pn ok", ok, "bad", bad, "records", tot)
    for k, v in samples.items(): print("   ", k, v)
