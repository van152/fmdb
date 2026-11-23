import capstone,struct,re
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
fo=0x1543ca0; base=0x1415446a0; end=0x1544c80
ins=list(md.disasm(b[fo:end],base))
def txt(v):
    s=struct.pack('<I',v)[::-1]; return s.decode('latin1')
tags={}
for i in ins:
    if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x'):
        v=int(i.op_str.split(', ')[1],16)
        if 0x20202020<=v<=0x7a7a7a7a: tags.setdefault(v,[]).append(i.address)
print('distinct tag immediates',len(tags))
print(' '.join(sorted(txt(v) for v in tags)))
