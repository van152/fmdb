import json, collections, importlib.util, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
# find all `call 0x140835380` sites, then look back for mov edx,imm32 4CC and add rax,imm / value width
ranges=[(s["raw"], s["raw"]+s["rawsize"]) for s in pe._secs if s["exec"] and s["rawsize"]>0]
# call rel32 to 0x140835380: E8 rel32
target=0x140835380 - pe.base
sites=[]
for a,b in ranges:
    i=a
    while True:
        i=raw.find(b"\xe8", i, b)
        if i<0: break
        rel=int.from_bytes(raw[i+1:i+5],'little',signed=True)
        va=pe.f2va(i)
        if va is not None and (va+5+rel)==0x140835380:
            sites.append(i)
        i+=1
print('call sites', len(sites))
out=[]
for s in sites:
    va=pe.f2va(s)
    lo=max(0,s-0x60)
    body=list(md.disasm(raw[lo:s+6], pe.f2va(lo) or 0))
    # last instructions before call
    win=[x for x in body if x.address < va][-10:]
    code=None; off=None; width=None; val=None
    for x in win:
        if x.mnemonic=='mov' and x.op_str.lower().startswith('edx,'):
            try: v=int(x.op_str.split(',')[1].strip(),0)
            except Exception: continue
            bs=v.to_bytes(4,'little')
            if all(48<=c<=57 or 65<=c<=90 or 97<=c<=122 for c in bs):
                code=bs[::-1].decode('latin1')
        m=re.match(r'rax,\s*(0x[0-9a-f]+)', x.op_str.lower())
        if x.mnemonic=='add' and m:
            off=int(m.group(1),16)
        if x.mnemonic=='mov' and re.match(r'(byte|word|dword) ptr \[rbp', x.op_str.lower()):
            width={'byte':1,'word':2,'dword':4}[x.op_str.split()[0]]
        m2=re.match(r'(esi|edi|eax|ebx|ecx|edx|r8d|r9d|r10d|r11d|r12d|r13d|r14d|r15d), (0x[0-9a-f]+|0)$', x.op_str.lower())
        if x.mnemonic=='mov' and m2: val=m2.group(1)
    if code:
        out.append({"site":hex(s),"code":code,"add_off":off,"width":width,"src":val})
print('records with 4CC', len(out), 'distinct codes', len({r['code'] for r in out}))
Path('scratch/t10/proto/propmap.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
c=collections.Counter(r['code'] for r in out)
print(c.most_common(10))
for r in out[:15]: print(r)
