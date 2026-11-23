import capstone,struct
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
fo=0x1543ca0; base=0x1415446a0; end=0x1544c80
ins=list(md.disasm(b[fo:end],base))
print('insns',len(ins),'range',hex(ins[0].address),hex(ins[-1].address))
def cc(v):
    s=struct.pack('<I',v); return ''.join(chr(c) if 32<=c<127 else '.' for c in s)
cmps=[(i.address,int(i.op_str.split(', ')[1],16)) for i in ins
      if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x')]
print('cmp edx count',len(cmps))
for a,v in cmps:
    if 0x20202020<=v<=0x7a7a7a7a: print(hex(a), cc(v))
# jump tables / indirect
for i in ins:
    if i.mnemonic in ('jmp','lea') and 'rip' in i.op_str and '*' in i.op_str:
        print('JT',hex(i.address),i.mnemonic,i.op_str)
    if i.mnemonic=='jmp' and i.op_str.startswith('qword ptr') :
        print('IND',hex(i.address),i.op_str)
