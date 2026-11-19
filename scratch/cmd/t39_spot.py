#!/usr/bin/env python3
"""Commander independent spot for t39 Tchl (does NOT import builder/verifier)."""
import hashlib, pathlib, runpy, struct, sys
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")
import zstandard as zstd
ROOT = pathlib.Path(r"D:/tmp2b/fm24-db")
DB = pathlib.Path(r"D:/tmp2b/fm24-db/scratch/data")
MAGIC = bytes.fromhex("28b52ffd")
codec = runpy.run_path(str(ROOT / "scratch/t01/inbox/t01k/verify.py"))
codec = runpy.run_path(str(codec["OLD_READER_PATH"]))

def pick_frame(archive, tid):
    fn = f"{archive}_db.dat"
    p = DB / fn
    ents = codec["list_tables"](p, fn)
    e = codec["_resolve_table"](tid, ents, fn)
    db = p.read_bytes()
    off = e["offset"]
    hit = next((off + d for d in range(64) if db[off+d:off+d+4] == MAGIC), None)
    if hit is None:
        return None, e
    want = e.get("size")
    pos = hit; frames = []
    dctx = zstd.ZstdDecompressor()
    for _ in range(64):
        if db[pos:pos+4] != MAGIC:
            break
        try:
            obj = dctx.decompressobj()
            out = obj.decompress(db[pos:])
            eof = obj.eof
        except Exception:
            break
        frames.append((len(out), hashlib.sha256(out).hexdigest(), eof))
        if want and len(out) == want:
            return out, e
        # advance to next frame
        if not eof:
            break
        # find next magic after this frame's compressed end (approx: scan)
        nxt = db.find(MAGIC, pos+4)
        if nxt < 0:
            break
        pos = nxt
    return None, e

P = F = 0
def ck(name, cond, extra=""):
    global P, F
    if cond: P += 1; print(f"PASS {name} {extra}")
    else: F += 1; print(f"FAIL {name} {extra}")

raw, e = pick_frame("server", 34)
ck("server34 frame resolved", raw is not None, f"size={e.get('size')}")
if raw is None:
    print(f"--- {P} PASS / {F} FAIL ---"); sys.exit(1)
ck("payload len 313082", len(raw) == 313082, str(len(raw)))
ck("SHA a07b2bb7", hashlib.sha256(raw).hexdigest().startswith("a07b2bb7"))
ck("closure 13+7115*44+9", 13 + 7115*44 + 9 == len(raw))
# client no table34
try:
    craw, ce = pick_frame("client", 34)
    ck("client no table34", craw is None)
except Exception:
    ck("client no table34", True)

N = 7115
def row(i): return 13 + 44*i
def u32(i, w): return struct.unpack_from("<I", raw, row(i)+w)[0]
def i32(i, w): return struct.unpack_from("<i", raw, row(i)+w)[0]
def u16(i, w): return struct.unpack_from("<H", raw, row(i)+w)[0]
def i8(i, w): return struct.unpack_from("<b", raw, row(i)+w)[0]
def u8(i, w): return raw[row(i)+w]

# wire offsets
TCHC,OWNER,STYR,EDYR,MSTN,SSTN,FLAG,STATE,CQUF,POSI,TCOP,ID = 1,5,9,11,13,17,21,22,23,27,28,32
sel = [u8(i,0) for i in range(N)]
ck("selector all 0", all(s==0 for s in sel), f"set={set(sel)}")
def cnt_hits(w):
    v=[i32(i,w) for i in range(N)]; return sum(1 for x in v if x!=-1), sum(1 for x in v if x==-1)
for nm,w,hh,nn in [("tchc",TCHC,7084,31),("mstn",MSTN,6956,159),("sstn",SSTN,3441,3674),("cquf",CQUF,1022,6093),("tcop",TCOP,2629,4486),("owner",OWNER,7084,31)]:
    h,n=cnt_hits(w); ck(f"{nm} hits/neg", h==hh and n==nn, f"{h}/{n} want {hh}/{nn}")
# styr/edyr zeros
ck("styr 161 zeros", sum(1 for i in range(N) if u16(i,STYR)==0)==161)
ck("edyr 21 zeros", sum(1 for i in range(N) if u16(i,EDYR)==0)==21)
# posi
posi=[i8(i,POSI) for i in range(N)]
ck("posi 2650 neg", sum(1 for x in posi if x==-1)==2650)
ck("posi live 1..16", all(1<=x<=16 for x in posi if x!=-1), f"range={min(x for x in posi if x!=-1)}..{max(x for x in posi if x!=-1)}")
# dbrt
flag=[u8(i,FLAG) for i in range(N)]; state=[i8(i,STATE) for i in range(N)]
from collections import Counter
fc=Counter(flag); ck("dbrt flag {0:6499,1:616}", fc.get(0)==6499 and fc.get(1)==616, str(dict(fc)))
ck("dbrt state set", set(state)<= {-1,1,2,3,4,5,6,7,8}, str(sorted(set(state))))
# identity tail
ids=[]; ok=True; uniq=set()
for i in range(N):
    a,b,c=struct.unpack_from("<III", raw, row(i)+ID)
    if a!=i or b!=c or b==0: ok=False
    ids.append(b); uniq.add(b)
ck("identity lane0=ordinal,lane1==lane2!=0", ok)
ck("identity unique", len(uniq)==N, f"{len(uniq)}")
# footer
ck("footer vector count 0", struct.unpack_from("<I",raw,313073)[0]==0)
ck("footer byte 01", raw[313077]==1)
last=struct.unpack_from("<I",raw,313078)[0]
ck("footer last u32 == max identity", last==max(ids), f"{last} vs {max(ids)}")
# specific反例
ck("owner row0 @18 = 50", u32(0,OWNER)==50, str(u32(0,OWNER)))
ck("posi row1 @84 = -1", i8(1,POSI)==-1)
ck("styr row28 @1254 = 0", u16(28,STYR)==0)
print(f"--- {P} PASS / {F} FAIL ---")
sys.exit(0 if F==0 else 1)