import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
n=struct.unpack_from('<I',raw,8)[0]
H=14; F=8; T=13
end=len(raw)-F
ALLOW=(0,10,11)
cands=collections.defaultdict(list)
for p in range(H, end-(T-1)):
    if raw[p+12] not in ALLOW: continue
    a,b,c=struct.unpack_from('<III',raw,p)
    if a<n and b==c and b: cands[a].append((p,b))
for k in cands: cands[k].sort()
back=[{}]; states={(H,0)}
for i in range(n):
    new={}
    for (cur,last) in states:
        for p,u in cands[i]:
            if p<cur or u<=last: continue
            new.setdefault((p+T,u),(cur,last))
    pruned={}; m1=None
    for k in sorted(new):
        if m1 is not None and k[1]>=m1: continue
        pruned[k]=new[k]; m1=k[1]
    back.append(pruned); states=set(pruned)
fin=[s for s in states if s[0]==end][0]
path=[]; key=fin
for i in range(n,0,-1):
    prev=back[i][key]; path.append((prev[0],key[1])); key=prev
path.reverse()
lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
sel=collections.Counter(raw[path[i][0]+12] for i in range(n))
print('n',n,'lens min/max/mean',min(lens),max(lens),round(sum(lens)/n,3))
print('selector',sel, 'closure', H+sum(lens)+T*n+F==len(raw))
def body(i):
    s=H if i==0 else path[i-1][0]+T
    return raw[s:path[i][0]]
for i in range(3):
    print('row',i,'len',lens[i],'sel',raw[path[i][0]+12], body(i).hex())
normal=[i for i in range(n) if raw[path[i][0]+12]==10]
nat=[i for i in range(n) if raw[path[i][0]+12]==11]
zero=[i for i in range(n) if raw[path[i][0]+12]==0]
print('normal',len(normal),'nat',len(nat),'zero',zero)
print('normal lens',collections.Counter(lens[i] for i in normal).most_common(5))
print('nat lens',collections.Counter(lens[i] for i in nat).most_common(8))
for i in nat[:2]+[nat[-1]]:
    print('NAT row',i,lens[i], body(i).hex())
for i in normal[:2]:
    print('NORM row',i,lens[i], body(i).hex())
if zero: print('ZERO',zero,[lens[i] for i in zero],[body(i).hex() for i in zero])
json.dump({'lens':lens,'ident':path}, open('scratch/t104/path.json','w'))
