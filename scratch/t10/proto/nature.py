import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
# find prologue: scan backwards for push rbp/push rbx + sub rsp
def prologue_before(va, back=0x2000):
    start=max(0, pe.va2f(va)-back)
    end=pe.va2f(va)
    seg=raw[start:end]
    best=None
    for p in (b"\x40\x53\x55\x56\x57", b"\x53\x55\x56\x57", b"\x48\x83\xec", b"\x48\x81\xec"):
        i=seg.rfind(p)
        if i>=0:
            cand=start+i
            if best is None or cand>best: best=cand
    return best
for filelo,hi,label in ((0xe82b04,0xe846ac,'A'),(0xe89a34,0xe8cded,'B'),(0xe57de0,0xe59000,'S')):
    lo=filelo
    p=prologue_before(pe.f2va(lo))
    print(f'cluster {label} {lo:#x}..{hi:#x} prologue候选 {p:#x}' if p else f'cluster {label} no prologue')
    if p:
        v=pe.f2va(p)
        for i in list(md.disasm(raw[p:p+0x50],v))[:16]:
            print(f'    {i.address:#x} {i.mnemonic} {i.op_str}')
