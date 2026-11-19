import importlib.util, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
def show(va,n=40):
    off=pe.va2f(va)
    print(f'--- va={va:#x} file={off:#x} {pe.section_of(off)}')
    for i in list(md.disasm(raw[off:off+n*4], va))[:n]:
        print(f'   {i.address:#x} {i.mnemonic} {i.op_str}')
for a in sys.argv[1:]:
    show(int(a,16), 40)
