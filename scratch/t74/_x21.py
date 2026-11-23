"""Brute-force t7 mid grammar: head + count + items + tail."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(x[0],x[1]) for x in b]

raw,rows = rows_of('client',7,208)

def mids(raw,rows):
    out=[]
    for s,e in rows:
        nl=struct.unpack_from('<I',raw,s)[0]
        p=s+4+nl+6
        ul=struct.unpack_from('<I',raw,p)[0]
        p+=4+ul
        out.append((p,e-13))    return out

M = mids(raw,rows)
print('mid lens', sorted(set(e-p for p,e in M))[:6], '...')
for i in range(3):
    p,e=M[i]
    print(f'row{i} mid[{p},{e}) len={e-p}')
    print('   ', raw[p:e].hex(' '))
print()
# search: head H (0..40), then u32 count, items each (u32,u32,lstr), tail T (0..20)
found=[]
for H in range(0,41):
    for T in range(0,21):
        ok=True
        for p,e in M:
            q=p+H
            if q+4>e: ok=False; break
            c=struct.unpack_from('<I',raw,q)[0]
            q+=4
            if c>64: ok=False; break
            good=True
            for _ in range(c):
                if q+12>e: good=False;break
                ln=struct.unpack_from('<I',raw,q+8)[0]
                if ln>400: good=False;break
                q+=12+ln
            if not good: ok=False;break
            if q!=e-T: ok=False;break
        if ok: found.append((H,T))
print('pattern A (head+count+items(u32,u32,lstr)+tail):',found)
