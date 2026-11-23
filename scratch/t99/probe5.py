import sys,struct,time
sys.path.insert(0,'scratch/t99')
from ld import load
MAGIC=bytes.fromhex('03017461642ef10d')
def u32(b,p): return struct.unpack_from('<I',b,p)[0]

def str_at(raw,r):
    if r+4>len(raw): return None
    ln=u32(raw,r)
    if ln>2048 or r+4+ln>len(raw): return None
    try: s=raw[r+4:r+4+ln].decode('utf-8')
    except UnicodeDecodeError: return None
    if ln and not all(c.isprintable() for c in s): return None
    return ln

def field_ends(raw,p,maxf,flagmax,window):
    L=len(raw); ends={p+4:0}; frontier={p+4:0}
    while frontier:
        nxt={}
        for q,nf in frontier.items():
            if nf>=maxf or q-p>window: continue
            for fo in range(flagmax+1):
                v=str_at(raw,q+fo)
                if v is None: continue
                e=q+fo+4+v
                if e>L: continue
                if ends.get(e,99)>nf+1:
                    ends[e]=nf+1; nxt[e]=nf+1
        frontier=nxt
    return ends

def parse(raw,maxf,flagmax,maxtr,window):
    L=len(raw); cnt=u32(raw,8)
    if cnt==0: return L==12
    layer={12:None}
    for i in range(cnt):
        nxt={}
        for p in layer:
            if p+4>L: continue
            uid=u32(raw,p)
            for e,nf in field_ends(raw,p,maxf,flagmax,window).items():
                for tr in range(maxtr+1):
                    q=e+tr
                    if q>L: break
                    if i+1<cnt:
                        if q+4>L or u32(raw,q)<=uid: continue
                    else:
                        if q!=L: continue
                    if q not in nxt: nxt[q]=1
        if not nxt: return None
        if len(nxt)>30000: return None
        layer=nxt
    return L in layer

FAILS=['1000000_18.dat','1000000_19.dat','1000000_5.dat','1000000_9.dat','1000001_19.dat','1000001_5.dat','1000001_9.dat','1000002person_names.dat','1000003person_names.dat','10_35.dat','10_5.dat','10_9.dat','11_18.dat','12_0.dat','12_18.dat','12_19.dat','12_2.dat','12_21.dat','12_3.dat','12_5.dat']
for m in FAILS:
    raw=load(m); res=[]
    for flagmax in (1,2,3):
        for maxf in (6,10,16):
            for maxtr in (2,4,6):
                if parse(raw,maxf,flagmax,maxtr,4000):
                    res.append((flagmax,maxf,maxtr)); break
            if res: break
        if res: break
    print(f"{m:26s} cnt={u32(raw,8):5d} -> {res}")
