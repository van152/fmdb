"""Search for exact count-loop grammar in t7 mid region."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(s,e) for s,e,u in b]

raw,rows = rows_of('client',7,208)

def split_media(raw,s,e):
    nl=struct.unpack_from('<I',raw,s)[0]
    name=raw[s+4:s+4+nl]
    p=s+4+nl
    pre=raw[p:p+6]
    p+=6
    ul=struct.unpack_from('<I',raw,p)[0]; p+=4
    url=raw[p:p+ul]; p+=ul
    return nl, pre, ul, url, p  # mid starts at p

# verify prefix constant
pres=set(); 
for s,e in rows:
    nl,pre,ul,url,p = split_media(raw,s,e)
    pres.add(pre)
print('distinct 6B prefixes:', [x.hex() for x in pres])

# candidate grammar: at mid start we have head H bytes then u32 count then count*(u32,u32,str)
mids=[]
for s,e in rows:
    nl,pre,ul,url,p=split_media(raw,s,e)
    mids.append((p,e))

for H in range(8,22):
  for tailT in range(0,20):
    ok=True
    for p,e in mids:
        q=p+H
        if q+4>e: ok=False; break
        c=struct.unpack_from('<I',raw,q)[0]
        q+=4
        if c>200: ok=False; break
        good=True
        for _ in range(c):
            if q+12>e: good=False; break
            ln=struct.unpack_from('<I',raw,q+8)[0]
            if ln>400: good=False; break
            q+=12+ln
        if not good: ok=False; break
        if q != e-13-tailT:
            ok=False; break
    if ok:
        print('MATCH H=',H,'tailT=',tailT)
