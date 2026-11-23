import json, collections, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
hits=json.loads(Path("scratch/t10/proto/hits.json").read_text()); hits.sort()
byoff={o:c for o,c in hits}
lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
sel=[(o,c) for o,c in hits if lo<=o<hi]
print('n',len(sel))
for o,c in sel[:40]:
    va=pe.f2va(o)
    ins=list(md.disasm(raw[o:o+0x14],va))
    br=next((x for x in ins[1:3] if x.mnemonic in ("je","jz","jne","jnz")),None)
    tgt=''
    if br:
        t=int(br.op_str,0); tf=pe.va2f(t)
        body=list(md.disasm(raw[tf:tf+0x30],t))[:5]
        tgt=f"{br.mnemonic}->{hex(tf)}: "+" | ".join(f"{y.mnemonic} {y.op_str}" for y in body)
    print(f'{o:#x} {c} {tgt}')
