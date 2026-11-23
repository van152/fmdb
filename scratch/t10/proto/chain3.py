import json
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
for off in (0xe82afc,0xe82b04,0xe82b10,0xe834a5, 0xe83450):
    va=pe.f2va(off)
    print(hex(off),hex(va))
    for i in md.disasm(raw[off:off+0x1c], va):
        print('   ',hex(i.address),i.mnemonic,i.op_str)
