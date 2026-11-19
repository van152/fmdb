import os,pathlib,runpy,struct,sys
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
def get(side,name='table_9.dat'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    e=es[name]; return z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(b,i):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,13)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
def solve(b,zero_ok,f_F_ok,mono):
    n=struct.unpack_from('<I',b,8)[0]; stop=len(b)-8
    C={i:cands(b,i) for i in range(n)}
    states={(13,-1):1}; layers=[]
    for i in range(n):
        nxt={}
        for (pos,last),cnt in states.items():
            for p,rid in C[i]:
                if p<pos or p+13>stop: continue
                if not zero_ok and rid==0: continue
                if not f_F_ok and rid==0xFFFFFFFF: continue
                if mono and not rid>last: continue
                nxt[(p+13,rid)]=nxt.get((p+13,rid),0)+cnt
        states=nxt; layers.append(dict(states))
        if not states: return None,None,i
    return sum(c for (p,l),c in states.items() if p==stop), states, n
for side in ('client','server'):
    b=get(side); print('='*60); print(side)
    for zo in (True,False):
        for ff in (True,False):
            r,st,n=solve(b,zo,ff,True)
            print(f'  zero_ok={zo} ff_ok={ff} -> walks={r} dead={n if r is None else "-"}')
    # where do zero/fF ids occur
    n=struct.unpack_from('<I',b,8)[0]
    z=[(i,[c for c in cands(b,i) if c[1]==0][:3]) for i in range(n)]
    print('  rows having a zero-id candidate:',sum(1 for i,x in z if x))
    print('  rows having 0xFFFFFFFF-id candidate:',[i for i in range(n) if any(c[1]==0xFFFFFFFF for c in cands(b,i))][:8])
