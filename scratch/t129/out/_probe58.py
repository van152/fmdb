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

# per-record shape: (pad1_after_A, has_B, pad2_after_B, alias_kind, tail)
SHAPES = []
for p1 in (0, 1, 2):
    for hasB in (True, False):
        for p2 in (0, 1, 2):
            for ak in ("u32", "str", "none"):
                for tail in (7, 11):
                    SHAPES.append((p1, hasB, p2, ak, tail))

def parse_at(raw, p, end, shape):
    p1, hasB, p2, ak, tail = shape
    g = rd(raw, p, end)
    if g is None: return None
    a = g[1]; q = p + g[0]
    q += 4 * p1
    b = None
    if hasB:
        g2 = rd(raw, q, end)
        if g2 is None: return None
        b = g2[1]; q += g2[0]
        q += 4 * p2
    if ak == "u32":
        if q + 4 > end: return None
        q += 4
    elif ak == "str":
        g3 = rd(raw, q, end)
        if g3 is None: return None
        q += g3[0]
    if q + tail > end: return None
    q += tail
    return q, (a, b)

def solve(raw, start=8):
    end = len(raw); memo = {}
    sys.setrecursionlimit(3000000)
    def dfs(p):
        if p == end: return []
        if end - p <= 8 and raw[p:] == b"\x00" * (end - p): return []
        if p in memo: return memo[p]
        memo[p] = None
        for shape in SHAPES:
            r = parse_at(raw, p, end, shape)
            if r is None: continue
            q, rec = r
            sub = dfs(q)
            if sub is not None:
                memo[p] = [(shape, rec)] + sub
                return memo[p]
        return None
    return dfs(start)

for path, label in [(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"), "base"), (Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    res = []
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        nm = e["path"].split("/")[1]
        if len(raw) <= 12:
            res.append((nm, 0, "empty")); continue
        r = solve(raw)
        if r is None: res.append((nm, None, "FAIL"))
        else:
            shapes = collections.Counter(s for s, _ in r)
            res.append((nm, len(r), shapes.most_common(2)))
    print(label)
    for x in res: print("  ", x)
