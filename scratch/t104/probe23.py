import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
def load(side,name):
    info=m['archive_info'](codec,side,cache)
    ent=next(e for e in info['tables'] if e['path'].endswith(name))
    return m['inspect_entry'](codec,ent,info)['data']

def ident_dp(pl, n, H, T, footer):
    end=len(pl)-footer
    # candidate identity positions indexed by ordinal
    cand=collections.defaultdict(list)
    for p in range(H, end-(T-1)):
        a,b,c=struct.unpack_from('<III',pl,p)
        if a<n and b==c and b!=0:
            cand[a].append((p,b))
    for k in cand: cand[k].sort()
    # DP: dict cursor -> count(capped 2), with parent map per row
    cur={H:1}
    parents=[]
    for i in range(n):
        nxt={}
        par={}
        for cp,cnt in cur.items():
            for p,u in cand.get(i,()):
                if p<cp: continue
                nc=p+T
                nxt[nc]=min(2, nxt.get(nc,0)+cnt)
                if nc not in par: par[nc]=(cp,p,u)
        parents.append(par); cur=nxt
        if not cur: return None, i
    tot=sum(cur.get(end,0) for _ in [0])
    # paths ending exactly at end
    if end not in cur: return None, n
    # reconstruct (unique if count==1)
    path=[]; cp=end
    for i in range(n,0,-1):
        pc,pp,pu=parents[i-1][cp]; path.append((pp,pu)); cp=pc
    path.reverse()
    return (path, cur[end]), n

for side in ('server','client'):
    pl=load(side,'table_extra_3.dat'); n=struct.unpack_from('<I',pl,8)[0]
    r,info=ident_dp(pl,n,12,12,0)
    print(side,'extra_3',('path' if r else 'none'), 'unique' if r and r[1]==1 else (r[1] if r else None), 'info',info)
    if r:
        path=r[0]; lens=[path[i][0]-(12 if i==0 else path[i-1][0]+12) for i in range(n)]
        print('   closure',12+sum(lens)+12*n==len(pl),'lens',min(lens),max(lens),round(sum(lens)/n,2))
