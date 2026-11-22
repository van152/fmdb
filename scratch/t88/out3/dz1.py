import capstone,sys
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
base=0x140000000
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
md.detail=False
start=0x1543ca0
end=start+0x2400
lines=[]
for ins in md.disasm(d[start:end], base+start):
    lines.append("%x %s %s"%(ins.address-base,ins.mnemonic,ins.op_str))
open('scratch/t88/out3/_rg.asm','w').write("\n".join(lines))
print(len(lines))
print("\n".join(lines[:60]))
