import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

# ---------- t7: post-name prefix + url + rest, per row
raw=load('client',7)
p,b,_,_=dp_walk(raw,'c7',14,len(raw)-8,208)
rows=[(x[0],x[1]) for x in b]
pats=collections.Counter(); rowsd=[]
for i,(s,e) in enumerate(rows):
    nl=struct.unpack_from('<I',raw,s)[0]
    q=s+4+nl
    pre=raw[q:q+12]
    rowsd.append((i,e-s,nl,q-s,pre.hex(),raw[s+4:s+4+nl].decode('utf-8','replace')))
    pats[pre[:11].hex()]+=1
print('distinct 11B post-name prefixes:', len(pats))
for k,v in pats.most_common(6): print(' ',v,k)
for r in rowsd[:10]: print(r[:5], r[5][:28])
print('...')
print('prelen variants (bytes before a plausible urllen):')
# heuristic: urllen = u32 at q+7 if plausible then url text starts with http or empty
alt=collections.Counter()
for i,(s,e) in enumerate(rows):
    nl=struct.unpack_from('<I',raw,s)[0]
    q=s+4+nl
    for off in (6,7,10,11):
        L=struct.unpack_from('<I',raw,q+off)[0]
        ok=False
        if L==0: ok=True
        elif 4<=L<200 and q+off+4+L<=e:
            try:
                t=raw[q+off+4:q+off+4+L].decode('ascii')
                ok=t.startswith('http')
            except Exception: pass
        if ok: alt[(off,L==0)]+=1
print(alt)

# ---------- t27 rows 0..2 geometry
raw27=load('client',27)
p,b,_,_=dp_walk(raw27,'c27',14,len(raw27)-8,334)
r27=[(x[0],x[1]) for x in b]
for i in (0,1,2,3):
    s,e=r27[i]
    nl=struct.unpack_from('<I',raw27,s)[0]
    print(f'--- t27 row{i} [{s},{e}) len={e-s} name_len={nl} name={raw27[s+4:s+4+nl][:24]!r}')
    body=raw27[s:e]
    for j in range(0,len(body),16):
        print(f'  {j:4d} {body[j:j+16].hex(" ")}  {body[j:j+16]!r}')
