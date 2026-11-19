import importlib.util
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
def show(va,n=60,label=''):
    off=pe.va2f(va)
    print(f'--- {label} va={va:#x} file={off:#x} section={pe.section_of(off)}')
    for i in list(md.disasm(raw[off:off+n*4], va))[:n]:
        print(f'   {i.address:#x} {i.mnemonic} {i.op_str}')
for va in (0x140e587e0,0x140e86191,0x140e85e57,0x140e65f60):
    show(va,25)
