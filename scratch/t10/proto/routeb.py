import json, collections, importlib.util, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
# scan for mov r32, imm32 (BA/BB/B9/B8 + REX 41/44/45 prefix) with ASCII imm
PREF=[(b"\xba",0),(b"\xbb",0),(b"\xb9",0),(b"\xb8",0),
      (b"\x41\xba",0),(b"\x41\xbb",0),(b"\x41\xb9",0),(b"\x41\xb8",0)]
ranges=[(s["raw"], s["raw"]+s["rawsize"]) for s in pe._secs if s["exec"] and s["rawsize"]>0]
hits=[]
for p,_ in PREF:
    L=len(p)
    for a,b in ranges:
        i=a
        while True:
            i=raw.find(p,i,b)
            if i<0: break
            ia=i+L
            if ia+4<=b:
                imm=raw[ia:ia+4]
                if all(48<=c<=57 or 65<=c<=90 or 97<=c<=122 or c in (0x5f,) for c in imm):
                    code=imm[::-1].decode('latin1')
                    hits.append((i,code,imm))
            i+=1
print('mov-imm ascii hits',len(hits),'distinct codes',len({c for _,c,_ in hits}))
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club={f['code'] for f in si['entities']['club']['fields']}
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
print('club codes with mov-imm hit', len({c for _,c,_ in hits if c in club}))
print('Cnam hits',len([1 for _,c,_ in hits if c=='Cnam']))
print('Cccn hits',len([1 for _,c,_ in hits if c=='Cccn']))
# validate with capstone that instruction is mov reg,imm
ok=[]
for off,code,imm in hits:
    va=pe.f2va(off)
    ins=list(md.disasm(raw[off:off+8],va))
    if ins and ins[0].mnemonic=='mov' and '0x' in ins[0].op_str:
        ok.append((off,code,va,ins[0].op_str))
print('validated',len(ok),'distinct',len({c for _,c,_,_ in ok}))
print('club validated',len({c for _,c,_,_ in ok if c in club}))
Path('scratch/t10/proto/movimm.json').write_text(json.dumps([[o,c] for o,c,_,_ in ok]),encoding='utf-8')
for c in ('Cnam','Cccn','Csnm','Csxn','Cl3n','Ca3n','duni','rdui','Cext'):
    o=[x for x in ok if x[1]==c]
    print(c,len(o),[hex(x[0]) for x in o[:4]])
