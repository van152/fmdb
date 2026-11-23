import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
n=struct.unpack_from('<I',raw,8)[0]
H=14; F=8; T=13
end=len(raw)-F
for allow in [(0,10,11),(10,11),(0,10,11,26)]:
    cands=collections.defaultdict(list)
    for p in range(H, end-(T-1)):
        if raw[p+12] not in allow: continue
        a,b,c=struct.unpack_from('<III',raw,p)
        if a<n and b==c and b: cands[a].append((p,b))
    for k in cands: cands[k].sort()
    states={(H,0)}
    ok=True
    for i in range(n):
        new={}
        for (cur,last) in states:
            for p,u in cands.get(i,()):
                if p<cur or u<=last: continue
                new.setdefault((p+T,u),None)
        pruned={}; m1=None
        for k in sorted(new):
            if m1 is not None and k[1]>=m1: continue
            pruned[k]=None; m1=k[1]
        if not pruned: ok=False; print(allow,'dead row',i); break
        states=set(pruned)
    if ok:
        fin=sorted(s for s in states if s[0]==end)
        print(allow,'alive final',fin[:3],'nstates',len(states))
