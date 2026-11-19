import json, collections, importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
def analyze(S, label):
    S=sorted(S, key=lambda t:(t[1],t[0]))
    n=len(S)
    ov=0
    for i in range(len(S)-1):
        if S[i][1]+S[i][2] <= S[i+1][1]: ov+=1
    noor = ov/max(1,len(S)-1)
    lo,hi=S[0][1],max(o+s for c,o,s in S)
    cov=sum(s for c,o,s in S)/max(1,hi-lo)
    al=sum(1 for c,o,s in S if (s==4 and o%4==0) or (s==2 and o%2==0) or s==1)
    gaps=[]
    cur=lo
    for c,o,s in S:
        if o>cur: gaps.append((cur,o))
        cur=max(cur,o+s)
    print(f'[{label}] n={n} span={hex(lo)}..{hex(hi)} overlap_ok={ov}/{n-1}={noor:.1%} coverage={cov:.1%} align={al}/{n}={al/n:.1%} gaps={len(gaps)} gapbytes={sum(b-a for a,b in gaps)}')
    return dict(n=n,lo=lo,hi=hi,overlap_ok=ov,no_overlap_rate=noor,coverage=cov,align_ok=al,align_rate=al/n,gaps=gaps)
A=[h for h in hits if 0xe82afc<=h[0]<0xe846ac]
B=[h for h in hits if 0xe89a34<=h[0]<0xe8cded]
S=[h for h in hits if 0xe57de0<=h[0]<0xe59000]
res={}
for name,sub in (('A',A),('B',B),('S',S)):
    recs=b.find_candidates(pe, sub, md)
    res[name]=recs
tot=[]
for name in ('A','B'):
    for r in res[name]:
        tot.append((r['code'],r['object_off'],r['size']))
print('codes resolved A+B:',len({c for c,_,_ in tot}))
analyze(tot,'A+B all')
analyze([t for t in tot if t[0] in clubs],'A+B club-only')
# union with 4cc_table exact hits (that's the "global table" path, covers codes outside A/B)
glob=[]
for c in clubs:
    for r in t4.get(c,[]):
        glob.append((c,r['object_off'],r['size']))
print('global table club records:',len(glob),'codes',len({c for c,_,_ in glob}))
analyze(glob,'global-table club-only')
analyze(tot+glob,'union')
