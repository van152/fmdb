import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; n=len(ident); lens=d['lens']
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
rows=[]
for i in range(n):
    b=body(i); pref=49 if sel[i]==11 else 0
    if len(b)<pref+53+12: continue
    c=struct.unpack_from('<H',b,pref+33)[0]
    base=pref+53+4*c
    if len(b)<base+12: continue
    blk=b[base:base+12]
    # tail names must be exact
    rest=b[base+12:]
    if len(rest)<8: continue
    l1=struct.unpack_from('<I',rest,0)[0]
    if l1>80 or 4+l1+4>len(rest): continue
    l2=struct.unpack_from('<I',rest,4+l1)[0]
    if l2>80 or 4+l1+4+l2!=len(rest): continue
    try:
        s1=rest[4:4+l1].decode('utf-8'); s2=rest[4+l1+4:].decode('utf-8')
    except: continue
    rows.append((i,sel[i],blk,s1,s2))
print('parsed rows', len(rows), 'of', n)
c0=collections.Counter(r[2][0] for r in rows); print('blk[0] (Ttyp)', sorted(c0.items())[:20])
print('blk[1] (Tisn)', collections.Counter(r[2][1] for r in rows))
print('blk[2..6]', collections.Counter(r[2][2:6].hex() for r in rows).most_common(5))
print('blk[6..10] range', min(int.from_bytes(r[2][6:10],'little') for r in rows), max(int.from_bytes(r[2][6:10],'little') for r in rows))
print('blk[10..12]', collections.Counter(r[2][10:12].hex() for r in rows).most_common(5))
print('sel vs Tisn', collections.Counter((r[1],r[2][1]) for r in rows))
names=[r for r in rows if r[3] or r[4]]
print('rows with names', len(names))
for r in names[:6]: print(r[0], r[1], r[2].hex(), repr(r[3]), repr(r[4]))
# owner ordinal check vs sel
own=[(r[1], int.from_bytes(r[2][6:10],'little')) for r in rows]
for s in (10,11):
    v=[o for ss,o in own if ss==s]
    if v: print('sel',s,'owner min/max',min(v),max(v),'count',len(v))
