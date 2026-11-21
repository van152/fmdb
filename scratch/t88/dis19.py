import capstone
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
def dump(fo,n,l=60):
    va=fo+BO;c=0
    for i in md.disasm(b[fo:fo+n],va):
        print(f'{i.address:x} {i.bytes.hex():18s} {i.mnemonic} {i.op_str}');c+=1
        if c>=l:break
dump(0xc5d250,0x120,60)
