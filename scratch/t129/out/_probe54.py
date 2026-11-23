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

# candidate record shapes: (pads_before_B, pads_before_alias)
SHAPES = [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(1,2),(0,2),(2,2)]

def parse_at(raw, p, end, shape):
    pb, pa = shape
    g1 = rd(raw, p, end)
    if g1 is None: return None
    a = g1[1]; q = p + g1[0]
    if q + 4*pb > end: return None
    q += 4 * pb
    g2 = rd(raw, q, end)
    if g2 is None: return None
    b = g2[1]; q += g2[0]
    if q + 4*pa + 7 > end: return None
    q += 4 * pa
    alias = struct.unpack_from("<I", raw, q)[0]
    u16 = struct.unpack_from("<H", raw, q+4)[0]
    u8 = raw[q+6]
    q += 7
    return q, (a, b, alias, u16, u8)

def solve(raw, start=8):
    end = len(raw)
    memo = {}
    order = []
    def dfs(p):
        if p == end: return True
        if p in memo: return memo[p]
        memo[p] = False
        for shape in SHAPES:
            r = parse_at(raw, p, end, shape)
            if r is None: continue
            q, rec = r
            if dfs(q):
                order.append((p, shape, rec))
                memo[p] = True
                return True
        return False
    sys.setrecursionlimit(2000000)
    ok = dfs(start)
    return ok, list(reversed(order))

for path, label in [(Path(r"scratch/data/lang_update_db.dat"), "upd")]:
    data, lay = m._read_archive(path); base = lay["data_base"]
    for e in lay["entries"]:
        if "person_names" not in e["path"]: continue
        raw = m._decompress_entry(data, base, e)
        if len(raw) <= 12: 
            print(label, e["path"].split("/")[1], "empty", len(raw)); continue
        ok, recs = solve(raw)
        print(label, e["path"].split("/")[1], "len", len(raw), "closed", ok, "recs", len(recs),
              "shapes", collections.Counter(s for _, s, _ in recs).most_common(3))
