import capstone
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
start=0x11f2a40; end=0x11f2c40
for i in md.disasm(d[start:end],base+start):
    print("%x %s %s"%(i.address-base,i.mnemonic,i.op_str))
