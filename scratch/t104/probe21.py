import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
def load(side,name):
    info=m['archive_info'](codec,side,cache)
    ent=next(e for e in info['tables'] if e['path'].endswith(name))
    return m['inspect_entry'](codec,ent,info)['data']
for side in ('server','client'):
    pl=load(side,'table_extra_3.dat'); n=struct.unpack_from('<I',pl,8)[0]; end=len(pl); H=12; T=12
    cands=collections.defaultdict(list)
    for p in range(H, end-(T-1)):
        a,b,c=struct.unpack_from('<III',pl,p)
        if a<n and b==c and b and a not in cands or (a in cands and len(cands[a])<8):
            cands[a].append((p,b))
    for k in cands: cands[k].sort()
    # greedy forward without uid monotonic
    cur=H; path=[]; last=None; ok=True
    for i in range(n):
        p=None
        for pp,u in cands.get(i,()):
            if pp>=cur: p=(pp,u); break
        if p is None: print(side,'dead',i); ok=False; break
        path.append(p); cur=p[0]+T; last=p[1]
    if ok:
        print(side,'extra_3 greedy ok', cur==end, 'closure', cur, end)
        lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
        print('  lens',min(lens),max(lens),round(sum(lens)/n,2))
        for i in range(5):
            s=H if i==0 else path[i-1][0]+T
            print('  rec',i,'len',lens[i], pl[s:path[i][0]].hex())
