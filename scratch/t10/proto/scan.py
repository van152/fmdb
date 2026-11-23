import importlib.util, json, sys, collections
from pathlib import Path
ROOT = Path(".")
spec = importlib.util.spec_from_file_location("_pe", ROOT/"scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe = pm.default()
raw = pe.raw
ranges=[(s["raw"], s["raw"]+s["rawsize"]) for s in pe._secs if s["exec"] and s["rawsize"]>0]
print("ranges", [(hex(a),hex(b)) for a,b in ranges], sum(b-a for a,b in ranges)/1e6)
PREF=(b"\x81\xfa",b"\x81\xfb",b"\x81\xf9",b"\x81\xf8",b"\x81\xfe",b"\x81\xff",b"\x81\xfd",b"\x81\xfc",b"\x3d")
hits=[]
for p in PREF:
    L=len(p)
    for a,b in ranges:
        i=a
        while True:
            i=raw.find(p,i,b)
            if i<0: break
            ia=i+L
            if ia+4<=b:
                imm=raw[ia:ia+4]
                if all(32<=c<127 for c in imm):
                    hits.append((i, imm[::-1].decode('latin1')))
            i+=1
print("hits",len(hits))
# validate with capstone: first instruction must be cmp with that imm
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64)
valid=[]
for off,code in hits:
    va=pe.f2va(off)
    ins=list(md.disasm(raw[off:off+12],va))
    if not ins: continue
    i0=ins[0]
    if i0.mnemonic!="cmp": continue
    if hex(int.from_bytes(raw[off+2:off+6],'little'))!=hex(int.from_bytes(code[::-1].encode('latin1'),'little')): pass
    valid.append((off,code,i0.op_str))
print("valid",len(valid),"distinct codes",len({c for _,c,_ in valid}))
Path("scratch/t10/proto/hits.json").write_text(json.dumps([[o,c] for o,c,_ in valid]),encoding='utf-8')
