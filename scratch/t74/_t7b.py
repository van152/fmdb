import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    _,b,_,_=dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw,[(x[0],x[1]) for x in b]

def triple_ok(raw,q,me):
    if q+12>me: return False
    a,b,c=struct.unpack_from('<III',raw,q)
    return a==b and c==0 and a>0

def parse(raw,q,me):
    """DFS: at q consume [u32 c][c triples] or single triple or 0xffffffff or 0.
       returns list of token spans (unique or None)."""
    res=[]
    def rec(q,acc):
        if len(res)>1: return
        if q==me: res.append(list(acc)); return
        if q+4>me: return
        c=struct.unpack_from('<I',raw,q)[0]
        # A: count + c triples
        if 0<c<200:
            p=q+4; ok=True
            for _ in range(c):
                if not triple_ok(raw,p,me): ok=False; break
                p+=12
            if ok and p<=me:
                acc.append(('list',q,c)); rec(p,acc); acc.pop()
        # B: single triple
        if triple_ok(raw,q,me):
            acc.append(('tri',q)); rec(q+12,acc); acc.pop()
        # C: all ones
        if c==0xffffffff:
            acc.append(('ones',q)); rec(q+4,acc); acc.pop()
        # D: explicit zero
        if c==0:
            acc.append(('zero',q)); rec(q+4,acc); acc.pop()
    rec(q,[])
    return res

for arch in ('client','server'):
    raw,rows=rows_of(arch,7,208)
    stat=collections.Counter(); fails=[]; heads=collections.Counter()
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q0=s+4+nl+6          # 6B prefix
        L=struct.unpack_from('<I',raw,q0)[0]
        ms=q0+4+L; me=e-13
        sols=parse(raw,ms,me)
        stat[len(sols)]+=1
        if len(sols)!=1: fails.append((i,me-ms,len(sols)))
        else:
            toks=sols[0]
            heads[(raw[ms:ms+4].hex(), tuple(t[0] for t in toks[:3]))]+=1
    print(arch,'parse-solution dist',dict(stat))
    print('  fails',fails[:6])
    print('  distinct token-prefixes',len(heads))
