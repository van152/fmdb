import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
def load(side,name):
    info=m['archive_info'](codec,side,cache)
    ent=next(e for e in info['tables'] if e['path'].endswith(name))
    return m['inspect_entry'](codec,ent,info)['data']
# extra_3: identity 12B tail [ord][uid][uid], header 12, footer 0
for side in ('server','client'):
    pl=load(side,'table_extra_3.dat'); n=struct.unpack_from('<I',pl,8)[0]
    H=12; T=12; end=len(pl)
    cands=collections.defaultdict(list)
    for p in range(H, end-(T-1)):
        a,b,c=struct.unpack_from('<III',pl,p)
        if a<n and b==c and b: cands[a].append((p,b))
    for k in cands: cands[k].sort()
    cur={(H,0):None}; hist=[]
    ok=True
    for i in range(n):
        new={}
        for (cp,last) in cur:
            for p,u in cands[i]:
                if p<cp or u<=last: continue
                new.setdefault((p+T,u),(p,(cp,last)))
        pruned={}; best=None
        for k in sorted(new):
            if best is not None and k[1]>=best: continue
            pruned[k]=new[k]; best=k[1]
        if not pruned: ok=False; print(side,'dead at',i); break
        hist.append(pruned); cur=set(pruned)
    if ok:
        fin=[k for k in cur if k[0]==end]
        print(side,'extra_3 states at end',[(k[0]-end) for k in list(cur)[:5]],'finals',len(fin))
        if fin:
            key=fin[0]; path=[]
            for i in range(n,0,-1):
                p,prev=hist[i-1][key]; path.append((p,key[1])); key=prev
            path.reverse(); lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
            print('  closure',H+sum(lens)+T*n==end,'lens',min(lens),max(lens), sum(lens)/n)
            for i in range(5):
                s=H if i==0 else path[i-1][0]+T
                print('  rec',i,'len',lens[i],pl[s:path[i][0]][:48].hex())
