import json, collections, importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe)
codes={h[1] for h in hits}
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club=[f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None]
clubs=set(club)
print('Cccn in cmp hits?', 'Cccn' in codes)
for c in ('Cccn','Cnam','Csta','Crep','Csnm','duni','rdui'):
    print(' ',c, c in codes, len([h for h in hits if h[1]==c]))
# prefix-3 analysis
exact=[c for c in clubs if c in codes]
p3=[c for c in clubs if c not in codes and any(x[:3]==c[:3] for x in codes)]
none=[c for c in clubs if c not in codes and not any(x[:3]==c[:3] for x in codes)]
print(f'club top-level {len(clubs)}: exact cmp dispatch {len(exact)} ({len(exact)/len(clubs):.1%}); prefix3-only {len(p3)}; none {len(none)}')
# also: how many club codes appear in 4cc_table
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
print('in 4cc_table:',len([c for c in clubs if c in t4]))
# fuzzy: edit distance <=1 against cmp code set restricted to same first char
def ed1(a,b):
    if a==b: return True
    if abs(len(a)-len(b))>1: return False
    if len(a)==len(b):
        return sum(x!=y for x,y in zip(a,b))==1
    s,l=(a,b) if len(a)<len(b) else (b,a)
    for i in range(len(l)):
        if l[:i]+l[i+1:]==s: return True
    return False
cand=sorted(x for x in codes if x[:1]=='C')
fz=[c for c in clubs if c not in codes and any(ed1(c,x) for x in cand)]
print('fuzzy ed<=1 (C-prefixed):',len(fz), fz[:12])
