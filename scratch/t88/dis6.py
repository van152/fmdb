import capstone
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
base_off=0x140000a00
def dump(va_start,n):
    fo=va_start-base_off
    for i in md.disasm(b[fo:fo+n],va_start):
        print(f'{i.address:x} {i.bytes.hex():20s} {i.mnemonic} {i.op_str}')
dump(0x1411f1680,0x90)
print('...')
dump(0x1411f1a40,0x60)
