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

def solve(raw, start=8, maxdepth=6):
    """DFS: record = [strA][opt u32 pads][strB][alias slot][u16][u8]; find program
    (pad count before B, alias present or not) closing whole payload."""
    end = len(raw)
    # try global program: p1 pads before B in {1,2}, alias mode in {"u32","str"}
    for pads in (1, 2, 0):
        for alias_mode in ("u32", "null4", "str"):
            pos = start; recs = []; ok = True
            while pos < end:
                g = rd(raw, pos, end)
                if g is None: ok = False; break
                a = g[1]; pos += g[0]
                if pos + 4 * pads > end: ok = False; break
                pos += 4 * pads
                g2 = rd(raw, pos, end)
                if g2 is None: ok = False; break
                b = g2[1]; pos += g2[0]
                if alias_mode == "u32":
                    if pos + 4 > end: ok = False; break
                    pos += 4
                elif alias_mode == "null4":
                    if pos + 4 > end: ok = False; break
                    pos += 4
                else:
                    g3 = rd(raw, pos, end)
                    if g3 is None: ok = False; break
                    pos += g3[0]
                if pos + 3 > end: ok = False; break
                pos += 3
                recs.append((a, b))
            if ok and pos == end:
                return (pads, alias_mode, len(recs))
    return None

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    res = {}
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        res[e["path"].split("/")[1]] = (len(raw), solve(raw))
    good = {k: v for k, v in res.items() if v[1]}
    bad = {k: v for k, v in res.items() if not v[1]}
    print(label, "solved", len(good), "/", len(res))
    for k, v in list(good.items())[:6]: print("  ", k, v)
    print("  unsolved", {k: v for k, v in bad.items()})
