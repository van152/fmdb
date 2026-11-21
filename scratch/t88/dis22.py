import capstone,struct
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
BO=0x140000a00
lo=0x1544c80
ins=list(md.disasm(b[lo-BO:lo-BO+0x1400],lo))
print('insns',len(ins))
lines=[f'{i.address:x} {i.bytes.hex()} {i.mnemonic} {i.op_str}' for i in ins]
open('scratch/t88/record_set.asm','w').write('\n'.join(lines))
def cc(v): return struct.pack('<I',v)[::-1].decode('latin1')
tags=[(i.address,int(i.op_str.split(', ')[1],16)) for i in ins
      if i.mnemonic=='cmp' and i.op_str.startswith('edx, 0x')]
print('cmp edx',len(tags))
print(' '.join(cc(v) for a,v in tags if 0x20202020<=v<=0x7a7a7a7a))
