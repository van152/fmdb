import json, collections, importlib.util, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
ranges=[(s["raw"], s["raw"]+s["rawsize"]) for s in pe._secs if s["exec"] and s["rawsize"]>0]
REG=[0x140833eb0, 0x140835380]
sites=[]
for tgt in REG:
    for a,b in ranges:
        i=a
        while True:
            i=raw.find(b"\xe8", i, b)
            if i<0: break
            rel=int.from_bytes(raw[i+1:i+5],'little',signed=True)
            va=pe.f2va(i)
            if va is not None and va+5+rel==tgt: sites.append((i,tgt))
            i+=1
print('sites',len(sites))
def is4cc(v):
    if not (0x20202020<=v<=0x7e7e7e7e): return False
    bs=v.to_bytes(4,'big')
    return all(48<=c<=57 or 65<=c<=90 or 97<=c<=122 for c in bs)
recs=[]
for s,tgt in sites:
    va=pe.f2va(s)
    lo=max(0, s-0x60)
    body=list(md.disasm(raw[pe.va2f(lo) or lo:s], pe.f2va(lo) or 0))
    win=body[-14:]
    code=None; off=None; src=None
    for x in win:
        o=x.op_str.lower()
        if x.mnemonic=='mov' and o.startswith('edx,') and 'ptr' not in o:
            try: v=int(o.split(',')[1].strip(),0)
            except Exception: continue
            if is4cc(v): code=v.to_bytes(4,'big').decode('latin1')
        m=re.match(r'rax, (0x[0-9a-f]+)$', o)
        if x.mnemonic=='add' and m: off=int(m.group(1),16)
        m2=re.match(r'(esi|edi|ebx|ecx|eax|r8d|r9d|r10d|r11d|r12d|r13d|r14d|r15d), (0x[0-9a-f]+)$', o)
        if x.mnemonic=='mov' and m2: src=m2.group(1)
    if code: recs.append({"code":code,"off":off,"src":src,"site":hex(s),"callee":hex(tgt)})
print('records',len(recs),'with off',sum(1 for r in recs if r['off'] is not None),'distinct codes',len({r['code'] for r in recs}))
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
co=[r for r in recs if r['code'] in clubs and r['off'] is not None]
print('club recs with off',len(co),'distinct codes',len({r['code'] for r in co}),'distinct offs',len({r['off'] for r in co}))
cmap=collections.defaultdict(set)
for r in co: cmap[r['code']].add(r['off'])
amb={c:v for c,v in cmap.items() if len(v)>1}
print('club codes w/ >1 off:',len(amb),list(amb.items())[:5])
for c in ('Cccn','Cnam','Csnm','Csxn','Cl3n','Ca3n','Crep','Csta','duni','rdui','Cext','Cyfn','Cprs'):
    print(' ',c,[hex(x) for x in sorted(cmap.get(c,[]))])
Path('scratch/t10/proto/tunnel3.json').write_text(json.dumps(recs,ensure_ascii=False,indent=1),encoding='utf-8')
