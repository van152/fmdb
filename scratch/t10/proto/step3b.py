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

def representative(records):
    """one offset per code: highest score; keep size."""
    best={}
    for r in records:
        c=r['code']
        if c not in best or r['score']>best[c]['score']:
            best[c]=r
    return {c:(r['object_off'],r['size']) for c,r in best.items()}

def newrec(pe,sub):
    recs=b.find_candidates(pe, sub, md)
    # find_candidates returns no score for some? check
    return recs

A=[h for h in hits if 0xe82afc<=h[0]<0xe846ac]
B=[h for h in hits if 0xe89a34<=h[0]<0xe8cded]
recsA=b.find_candidates(pe,A,md); recsB=b.find_candidates(pe,B,md)
for r in recsA+recsB: r.setdefault('score',0.5)
repA=representative(recsA); repB=representative(recsB)
print('repA',len(repA),'repB',len(repB))
comb={}
for d in (repA,repB):
    for c,v in d.items(): comb.setdefault(c,v)
print('union codes',len(comb))
def checks(m, label):
    items=sorted(m.items(), key=lambda kv: kv[1][0])
    # group by offset
    byoff=collections.defaultdict(list)
    for c,(o,s) in items: byoff[o].append((c,s))
    # distinct offsets with chosen size = max
    slots=[]
    for o,v in byoff.items():
        sizes=sorted({s for c,s in v})
        slots.append((o,max(sizes),len(v),sizes))
    slots.sort()
    gaps=[];cur=None
    for o,s,k,sizes in slots:
        if cur is not None and o>cur: gaps.append((cur,o))
        cur=max(cur or 0, o+s)
    lo=slots[0][0]; hi=max(o+s for o,s,k,sz in slots)
    covered=sum(s for o,s,k,sz in slots)
    # overlap test only across distinct offsets
    ov_ok=sum(1 for i in range(len(slots)-1) if slots[i][0]+slots[i][1] <= slots[i+1][0])
    al=sum(1 for o,s,k,sz in slots if (s==4 and o%4==0) or (s==2 and o%2==0) or s==1)
    print(f'[{label}] codes={len(items)} distinct_offsets={len(slots)} span={hex(lo)}..{hex(hi)} '
          f'coverage={covered/max(1,hi-lo):.1%} overlap_ok={ov_ok}/{len(slots)-1}={ov_ok/max(1,len(slots)-1):.1%} '
          f'align={al}/{len(slots)}={al/len(slots):.1%} gaps={len(gaps)}')
    return slots,gaps,lo,hi
checks(comb,'A+B reps')
checks({c:v for c,v in comb.items() if c in clubs},'A+B club only')
glob={}
for c in clubs:
    for r in t4.get(c,[]):
        glob.setdefault(c,(r['object_off'],r['size']))
checks(glob,'global table club only')
u=dict(glob); u.update(comb)
checks({c:v for c,v in u.items() if c in clubs},'union club only')
