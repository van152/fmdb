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

def solve(raw, start=8, footer_max=12):
    end = len(raw); memo = {}
    def dfs(p):
        if end - p <= footer_max and raw[p:] == b"\x00" * (end - p):
            return []
        if p in memo: return memo[p]
        memo[p] = None
        cands = []
        g = rd(raw, p, end)
        if g is not None: cands.append((g[0], "str"))
        for w in (4, 2, 1):
            if p + w <= end: cands.append((w, "u%d" % (w*8)))
        for w, name in cands:
            r = dfs(p + w)
            if r is not None:
                memo[p] = [(name, p, w)] + r
                return memo[p]
        return None
    sys.setrecursionlimit(2000000)
    return dfs(start)

for path, label in [(Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    for nm in ["24person_names.dat", "7person_names.dat", "12person_names.dat", "17person_names.dat"]:
        e = [x for x in lay["entries"] if x["path"].endswith("/" + nm)][0]
        raw = m._decompress_entry(data, base, e)
        r = solve(raw)
        print("==", nm, "len", len(raw), "parsed", r is not None)
        if r:
            print("   tokens", " ".join("%s@%d" % (n, o) for n, o, w in r[:40]))
