import capstone,struct
EXE='D:/tmp2b/fm24/input/editor.exe'
b=open(EXE,'rb').read()
print('exe len',len(b),'size',hex(len(b)))
def dis(fo,n,base=None):
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    code=b[fo:fo+n]
    for i in md.disasm(code, base if base is not None else 0):
        print(f'{fo+i.address-fo if base is None else i.address:08x} {i.bytes.hex():24s} {i.mnemonic} {i.op_str}')
import sys
fo=int(sys.argv[1],16); n=int(sys.argv[2]); base=int(sys.argv[3],16) if len(sys.argv)>3 else None
dis(fo,n,base)
