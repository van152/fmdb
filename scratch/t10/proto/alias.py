import json, collections, importlib.util, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
def is4cc(v):
    if not (0x20202020<=v<=0x7e7e7e7e): return False
    return True
rows=[]
for off,code,va,_ in hits:
    ins=list(md.disasm(raw[off:off+0x18],va))
    br=next((x for x in ins[1:4] if x.mnemonic in ('je','jz')),None)
    if not br: continue
    t=int(br.op_str,0); tf=pe.va2f(t)
    body=list(md.disasm(raw[tf:tf+0x40],t))[:12]
    alias=None
    for y in body:
        o=y.op_str.lower()
        if y.mnemonic=='mov' and o.startswith('edx,') and 'ptr' not in o:
            try: v=int(o.split(',')[1].strip(),0)
            except Exception: continue
            if is4cc(v):
                alias=v.to_bytes(4,'big').decode('latin1')
            break
        if y.mnemonic in ('ret',): break
    if alias:
        rows.append((code,alias,hex(off)))
print('alias rows',len(rows),'distinct query codes',len({r[0] for r in rows}))
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs=[f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None]
cr=[r for r in rows if r[0] in set(clubs)]
print('club alias rows',len(cr),'distinct club codes',len({r[0] for r in cr}))
al=collections.Counter(r[1] for r in cr)
print('top alias targets:', al.most_common(10))
print('distinct alias targets', len(al))
for c in ('Cnam','Cccn','Csnm','Csxn','Cl3n','Ca3n','Crep','Csta','duni','Cext','Cprs'):
    print('  ',c,sorted({r[1] for r in cr if r[0]==c}))
Path('scratch/t10/proto/alias.json').write_text(json.dumps(rows,ensure_ascii=False,indent=1),encoding='utf-8')
