import capstone
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
def dump(va,n,limit=45):
    fo=va-BO;c=0
    for i in md.disasm(b[fo:fo+n],va):
        print(f'{i.address:x} {i.bytes.hex():20s} {i.mnemonic} {i.op_str}');c+=1
        if c>=limit:break
for va in (0x143dc1790,0x143dc2050,0x140057ef0):
    print('====',hex(va)); dump(va,160,40)
