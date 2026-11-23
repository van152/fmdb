import capstone,struct,collections
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
fo=0x1543ca0; base=0x1415446a0
code=b[fo:fo+0x1200]
ins=list(md.disasm(code,base))
def cc(v):
    s=struct.pack('<I',v)
    return ''.join(chr(c) if 32<=c<127 else '.' for c in s)
cmps=[]
for i in ins:
    if i.mnemonic=='cmp' and i.op_str.startswith('edx, '):
        try: v=int(i.op_str.split(', ')[1],16)
        except: v=None
        if v and 0x20202020<=v<=0x7a7a7a7a: cmps.append((i.address,v,cc(v)))
print('4CC compares',len(cmps))
print('jump tables:')
for i in ins:
    if 'rip' in i.op_str and ('jmp' in i.mnemonic or 'lea' in i.mnemonic) and ('rax*4' in i.op_str or 'rdx*4' in i.op_str):
        print(' ',hex(i.address),i.mnemonic,i.op_str)
# print first 40 compares with target
for a,v,s in cmps[:40]:
    print(hex(a),s,hex(v))
