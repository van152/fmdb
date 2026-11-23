import json, collections, importlib.util, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
ranges=[(s["raw"], s["raw"]+s["rawsize"]) for s in pe._secs if s["exec"] and s["rawsize"]>0]

def targets(imm_va):
    out=[]
    for a,b in ranges:
        i=a
        while True:
            i=raw.find(b"\xe8", i, b)
            if i<0: break
            rel=int.from_bytes(raw[i+1:i+5],'little',signed=True)
            va=pe.f2va(i)
            if va is not None and va+5+rel==imm_va:
                out.append(i)
            i+=1
    return out

ALLOC=[0x14083d4f0]
def build():
    pairs=[]
    for tgt in ALLOC:
        for s in targets(tgt):
            va=pe.f2va(s)
            for y in list(md.disasm(raw[s:s+0x18],va))[:4]:
                if y.mnemonic=='add' and re.match(r'rax, 0x[0-9a-f]+$', y.op_str):
                    off=int(y.op_str.split(',')[1],16)
                    if not (0x20<=off<=0x400): break
                    # look ahead for mov edx, 4CC
                    fo=pe.va2f(y.address)
                    for z in list(md.disasm(raw[fo:fo+0x60], y.address))[:14]:
                        if z.mnemonic=='mov' and z.op_str.lower().startswith('edx,'):
                            try: v=int(z.op_str.split(',')[1].strip(),0)
                            except Exception: break
                            try: bs=v.to_bytes(4,'big')
                            except OverflowError: break
                            if all(48<=c<=57 or 65<=c<=90 or 97<=c<=122 for c in bs):
                                pairs.append({"code":bs.decode('latin1'),"off":off,"add_site":hex(y.address),"mov_site":hex(z.address),"cmp_site":hex(pe.f2va(s))})
                            break
                        if z.mnemonic in ('ret','jmp','call') and z.mnemonic!='call': break
                    break
    return pairs
pairs=build()
print('pairs',len(pairs),'codes',len({p['code'] for p in pairs}))
CITY={"Clat":0x48,"Clon":0x4c,"Cnti":0x20,"Cwea":0x28,"Clgi":0x30,"Clri":0x38}
for c,want in CITY.items():
    got=sorted({p['off'] for p in pairs if p['code']==c})
    print(' ',c,'want',hex(want),'got',[hex(x) for x in got], 'OK' if got==[want] else '')
INJ={"icla":(0x4C,1),"iscl":(0x4D,1),"Imnd":(0x34,2),"Iexd":(0x36,2),"Iiar":(0x58,1),"Irec":(0x59,1),"Iocr":(0x30,4),"Imip":(0x50,1),"Iagr":(0x51,1),"Icms":(0x52,1),"Icon":(0x53,1),"inSr":(0x54,1),"Icdp":(0x56,1)}
print('injury:')
ok=0
for c,(off,w) in INJ.items():
    got=sorted({p['off'] for p in pairs if p['code']==c})
    m = got==[off]
    ok += m
    print(' ',c,'want',hex(off),'got',[hex(x) for x in got],'OK' if m else '')
print('injury ok',ok,'/13')
Path('scratch/t10/proto/tunnel.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=1),encoding='utf-8')
