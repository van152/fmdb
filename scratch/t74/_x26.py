"""Verify byte-exact grammars for t8/t7/t18/t27 with known DP row frames."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    assert b, (arch,tid)
    return raw, [(x[0],x[1]) for x in b], [x[2] for x in b]

def lstr(raw,p,e):
    if p+4>e: return None
    n=struct.unpack_from('<I',raw,p)[0]
    if n>4096 or p+4+n>e: return None
    return raw[p+4:p+4+n], p+4+n

def is_text(b):
    try: s=b.decode('utf-8')
    except Exception: return False
    return all(ch.isprintable() for ch in s) and len(s)>0

# ---------- t18 derby: k strings (k even) + numeric(52-4k) + 13 identity
for arch in ('client','server'):
    raw,rows,uids = rows_of(arch,18,1567)
    res=collections.Counter(); bad=[]
    for i,(s,e) in enumerate(rows):
        match=[]
        for k in (2,4,6,8):
            p=s; okk=True
            for _ in range(k):
                r=lstr(raw,p,e)
                if not r or not is_text(r[0]): okk=False;break
                p=r[1]
            if not okk: continue
            need=52-4*k
            if p+need+13==e and need>=0:
                match.append(k)
        if len(match)==1: res[match[0]]+=1
        else: bad.append((i,e-s,match))
    print(f't18 {arch}: k-string distribution {dict(res)} ambiguous/bad {len(bad)}', bad[:5])

# ---------- t27 weather: lstr + 95 numeric + 13 identity
for arch in ('client','server'):
    raw,rows,uids = rows_of(arch,27,334)
    ok=0; bad=[]
    for i,(s,e) in enumerate(rows):
        r=lstr(raw,s,e)
        if r and is_text(r[0]) and r[1]+95+13==e: ok+=1
        else: bad.append((i,e-s,r))
    print(f't27 {arch}: lstr+95+13 ok {ok}/334 bad {len(bad)}', [(b[0],b[1]) for b in bad[:5]])

# ---------- t8 language: lstr + 30 suffix (suffix = 17 pre + 13 identity)
for arch in ('client','server'):
    raw,rows,uids = rows_of(arch,8,126)
    ok=0; bad=[]
    for i,(s,e) in enumerate(rows):
        r=lstr(raw,s,e)
        if r and is_text(r[0]) and r[1]+30==e: ok+=1
        else: bad.append((i,e-s))
    print(f't8 {arch}: lstr+30 ok {ok}/126 bad {bad[:3]}')

# ---------- t7 media: lstr name + 6 + u32 urllen + url + 30 head + u32 cnt + cnt*(u32,u32,lstr) + [srv 7] + 5 + 13
for arch,extra in (('client',0),('server',7)):
    raw,rows,uids = rows_of(arch,7,208)
    ok=0; bad=[]
    counts=collections.Counter(); heads=set()
    for i,(s,e) in enumerate(rows):
        r=lstr(raw,s,e)
        if not r: bad.append((i,'name')); continue
        p=r[1]
        heads.add(raw[p:p+6])
        p+=6
        if p+4>e: bad.append((i,'urllen')); continue
        ul=struct.unpack_from('<I',raw,p)[0]
        p+=4
        if p+ul>e: bad.append((i,'url',ul)); continue
        p+=ul
        head=raw[p:p+30]; p+=30
        if p+4>e: bad.append((i,'cnt')); continue
        c=struct.unpack_from('<I',raw,p)[0]; p+=4
        good=True
        for _ in range(c):
            if p+12>e: good=False;break
            rr=lstr(raw,p+8,e)
            if not rr: good=False;break
            p=rr[1]
        if not good: bad.append((i,'items',c)); continue
        p+=extra
        if p+5+13==e: ok+=1; counts[c]+=1
        else: bad.append((i,'tail',e-p))
    print(f't7 {arch}: grammar ok {ok}/208 bad {len(bad)}', bad[:5], 'counts', dict(counts), '6Bprefix', set(x.hex() for x in heads))
