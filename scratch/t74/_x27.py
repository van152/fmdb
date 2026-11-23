import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n,W=13,mk=True):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n,W,mk)
    return raw, [(x[0],x[1]) for x in b]

raw,rows = rows_of('client',7,208)
def mids(raw,rows,pre=6):
    out=[]
    for s,e in rows:
        nl=struct.unpack_from('<I',raw,s)[0]
        p=s+4+nl+pre
        ul=struct.unpack_from('<I',raw,p)[0]
        p+=4+ul
        out.append((p,e-13))
    return out
M=mids(raw,rows)
# for every mid, find offsets o where u32 count parse lands exactly at e-13-T
for T in range(0,12):
  for H in range(0,40):
    hits=0
    for p,e in M:
        q=p+H
        if q+4>e: break
        c=struct.unpack_from('<I',raw,q)[0]
        q+=4
        good=0<c<600
        while good and q<e:
            if q+4>e: good=False;break
            ln=struct.unpack_from('<I',raw,q+8) if q+12<=e else 10**9
            if q+12>e: good=False;break
            if ln>600: good=False;break
            q+=12+ln
            c-=1
            if c==0: break
        if good and c==0 and q==e-T: hits+=1
    if hits>150: print('T',T,'H',H,'hits',hits)
print('---')
# also: maybe 2-byte shift at start
for T in range(0,12):
  for H in range(0,40):
    hits=0
    for p,e in M:
        q=p+H
        if q+2>e: break
        c=struct.unpack_from('<H',raw,q)[0]
        q+=2
        good=0<c<600
        while good and c>0:
            if q+4>e: good=False;break
            ln=struct.unpack_from('<I',raw,q+8) if q+12<=e else 10**9
            if q+12>e: good=False;break
            if ln>600: good=False;break
            q+=12+ln; c-=1
        if good and c==0 and q==e-T: hits+=1
    if hits>150: print('u16 count T',T,'H',H,'hits',hits)
