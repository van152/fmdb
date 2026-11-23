#!/usr/bin/env python3
"""Commander independent spot for t41 Csme variable-stride cursor (no builder/verifier import)."""
import hashlib, pathlib, runpy, struct, sys
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")
import zstandard as zstd
ROOT = pathlib.Path(r"D:/tmp2b/fm24-db"); DB = ROOT / "scratch/data"
MAGIC = bytes.fromhex("28b52ffd")
c = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py")); c = runpy.run_path(str(c["OLD_READER_PATH"]))
def pick(arch, tid):
    fn = f"{arch}_db.dat"; p = DB / fn
    e = c["_resolve_table"](tid, c["list_tables"](p, fn), fn); db = p.read_bytes(); off = e["offset"]
    hit = next((off+d for d in range(64) if db[off+d:off+d+4] == MAGIC), None)
    if hit is None: return None
    pos = hit; want = e.get("size")
    for _ in range(64):
        if db[pos:pos+4] != MAGIC: break
        o = zstd.ZstdDecompressor().decompressobj()
        try: out = o.decompress(db[pos:])
        except Exception: break
        if want and len(out) == want: return out
        if not o.eof: break
        nxt = db.find(MAGIC, pos+4)
        if nxt < 0: break
        pos = nxt
    return None
P = F = 0
def ck(n, cond, x=""):
    global P, F
    if cond: P += 1; print(f"PASS {n} {x}")
    else: F += 1; print(f"FAIL {n} {x}")
raw = pick("server", 59)
ck("server59 resolved", raw is not None)
if raw is None: print(f"--- {P}/{F} ---"); sys.exit(1)
ck("payload 224880", len(raw) == 224880, str(len(raw)))
ck("SHA 7eee0ecc", hashlib.sha256(raw).hexdigest().startswith("7eee0ecc"))
try:
    _cl = pick("client", 59)
except KeyError:
    _cl = None
ck("client no table59", _cl is None)
# variable walk
N = 9079; pos = 13; rows = []; n0 = n1 = 0; sumlen = 0; ids = []; uniq = set(); idok = True
melf = []; msid_bad = 0; tags = []; outer = []; owners = []; sel_ok = True
for i in range(N):
    s = pos
    sel = raw[s]; n = struct.unpack_from("<I", raw, s+6)[0]
    rl = 22 + 10*n
    if sel != 0: sel_ok = False
    owners.append(struct.unpack_from("<i", raw, s+1)[0])
    outer.append(raw[s+5])
    a, b, cc = struct.unpack_from("<III", raw, s+10+10*n)
    if a != i or b != cc or b == 0: idok = False
    ids.append(b); uniq.add(b)
    if n == 0: n0 += 1
    elif n == 1:
        n1 += 1
        tags.append(raw[s+10])
        melf.append(raw[s+19])
        p0, p1 = struct.unpack_from("<ii", raw, s+11)
        if (p0, p1) != (-1, -1): msid_bad += 1
    rows.append((s, n, rl)); sumlen += rl; pos += rl
ck("walk 9079 rows", len(rows) == N and pos == 224871, f"end={pos}")
ck("count0=6567 count1=2512", n0 == 6567 and n1 == 2512, f"{n0}/{n1}")
ck("sum row_lens 224858", sumlen == 224858, str(sumlen))
ck("closure 13+224858+9", 13 + sumlen + 9 == len(raw))
ck("selector all 0", sel_ok)
ck("identity lane0=ord,lane1==lane2!=0", idok)
ck("identity unique 9079", len(uniq) == N, str(len(uniq)))
ck("Melf 2512 vals 1..33", len(melf) == 2512 and all(1 <= v <= 33 for v in melf), f"range={min(melf)}..{max(melf)}")
ck("Melf no raw 0/ff", 0 not in melf and 255 not in melf)
ck("Msid all (-1,-1)", msid_bad == 0, f"bad={msid_bad}")
ck("tag all 0x01", all(t == 1 for t in tags), f"set={set(tags)}")
ck("outer byte 0..4", all(0 <= v <= 4 for v in outer), f"set={sorted(set(outer))}")
ck("outer 114 zeros", sum(1 for v in outer if v == 0) == 114)
ck("owner 9079 distinct", len(set(owners)) == N, str(len(set(owners))))
# footer
ck("footer vector count 0", struct.unpack_from("<I", raw, 224871)[0] == 0)
ck("footer flag 1", raw[224875] == 1)
ck("footer last u32 9079", struct.unpack_from("<I", raw, 224876)[0] == 9079)
# specific反例
ck("row0 count0 identity@23=(0,1,1)", struct.unpack_from("<III", raw, 23) == (0, 1, 1))
ck("row0 owner@14=0", struct.unpack_from("<i", raw, 14)[0] == 0)
s2 = rows[2][0]
ck("row2 count1", rows[2][1] == 1, f"s2={s2}")
ck("row2 Msid@68=(-1,-1)", struct.unpack_from("<ii", raw, s2+11) == (-1, -1))
ck("row2 Melf@76=4", raw[s2+19] == 4, str(raw[s2+19]))
print(f"--- {P} PASS / {F} FAIL ---")
sys.exit(0 if F == 0 else 1)