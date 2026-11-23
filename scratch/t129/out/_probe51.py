import sys, struct
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

data, lay = m._read_archive(Path(r"D:\tmp2b\fm24\input\lang_db_2400.dat"))
base = lay["data_base"]
ent = {e["path"]: e for e in lay["entries"]}
payloads = []
for nm in ["lang_db/30person_names.dat", "lang_db/1000004person_names.dat", "lang_db/21person_names.dat", "lang_db/19person_names.dat", "lang_db/24person_names.dat"]:
    raw = m._decompress_entry(data, base, ent[nm])
    payloads.append((nm, raw, 8))

sys.setrecursionlimit(100000)
memo = {}
def solve(state, prog):
    key = state
    if key in memo: return memo[key]
    ends = [len(p[1]) for p in payloads]
    if all(state[i] == ends[i] for i in range(len(payloads))):
        return list(prog)
    if any(state[i] > ends[i] for i in range(len(payloads))):
        return None
    if len(prog) > 14: return None
    # try str
    got = []
    ok = True
    for i, (nm, raw, st) in enumerate(payloads):
        g = rd(raw, state[i], ends[i])
        if g is None: ok = False; break
        got.append(g[0])
    if ok:
        ns = tuple(state[i] + got[i] for i in range(len(payloads)))
        r = solve(ns, prog + ["str"])
        if r is not None: memo[key] = r; return r
    for w in (4, 2, 1):
        if any(state[i] + w > ends[i] for i in range(len(payloads))): continue
        ns = tuple(state[i] + w for i in range(len(payloads)))
        r = solve(ns, prog + ["u%d" % (w * 8)])
        if r is not None: memo[key] = r; return r
    memo[key] = None
    return None

res = solve(tuple(p[2] for p in payloads), [])
print("joint program:", res)
