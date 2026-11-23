import capstone
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
for start,end in ((0x3ebad50,0x3ebad50+0x400),):
    lines=["%x %s %s"%(i.address-base,i.mnemonic,i.op_str) for i in md.disasm(d[start:end],base+start)]
    print("\n".join(lines))
