import sys, struct
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, r"D:\tmp2b\fm24\scripts")
import modding_read_dbdat as m
from pathlib import Path

def u32(raw, p): return struct.unpack_from("<I", raw, p)[0]

def walk_pn(raw):
    """header 8 bytes; then records: [u32 lenA][A][u32 x][u32 lenB][B][u32 y][u32 alias][u16 z][u8 w]"""
    pos = 8; end = len(raw); recs = []
    while pos < end:
        if pos + 4 > end: return None, ("lenA", pos, len(recs))
        la = u32(raw, pos); pos += 4
        if la > 4096 or pos + la > end: return None, ("A", pos, len(recs))
        try: a = raw[pos:pos+la].decode("utf-8")
        except UnicodeDecodeError: return None, ("Adec", pos, len(recs))
        pos += la
        if pos + 8 > end: return None, ("x", pos, len(recs))
        x = u32(raw, pos); pos += 4
        lb = u32(raw, pos); pos += 4
        if lb > 4096 or pos + lb > end: return None, ("B", pos, len(recs))
        try: b = raw[pos:pos+lb].decode("utf-8")
        except UnicodeDecodeError: return None, ("Bdec", pos, len(recs))
        pos += lb
        if pos + 4 > end: return None, ("y", pos, len(recs))
        y = u32(raw, pos); pos += 4
        if pos + 4 > end: return None, ("al", pos, len(recs))
        alias = u32(raw, pos); pos += 4
        al = None
        if alias != 0xFFFFFFFF:
            la2 = u32(raw, pos) if pos + 4 <= end else 0
            # try reading as len-prefixed string
            if 0 < la2 <= 4096 and pos + 4 + la2 <= end:
                try:
                    al = raw[pos+4:pos+4+la2].decode("utf-8"); pos += 4 + la2
                except UnicodeDecodeError: al = None
        if pos + 3 > end: return None, ("z", pos, len(recs))
        z = struct.unpack_from("<H", raw, pos)[0]; w = raw[pos+2]; pos += 3
        recs.append((a, x, b, y, alias, al, z, w))
    return recs, None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    ok = 0; bad = []; tot = 0
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        r, err = walk_pn(raw)
        if r is None: bad.append((e["path"], err))
        else: ok += 1; tot += len(r)
    print(label, "pn ok", ok, "bad", bad, "records", tot)
