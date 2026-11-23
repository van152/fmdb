exec(open('scratch/t55/probe.py',encoding='utf8').read().split("if sys.argv[1]=='xml'")[0]);import struct as s
def show(o,n):
 for i in m.disasm(p.raw[o:o+n],p.f2va(o)): print(hex(p.va2f(i.address)),i.mnemonic,i.op_str,hex(p.va2f(i.operands[0].imm) or 0) if i.mnemonic.startswith(('j','call')) and i.operands[0].type==2 else '')
for t in [10,41]:
 a=0xf49d38; v=p.va2f(p.f2va(a)+s.unpack_from('<i',p.raw,a+4*t)[0]); print('factory',t,hex(v));show(v,24)
for n in [2,19,20,21]:
 v=p.va2f(s.unpack_from('<Q',p.raw,0x18889b8+8*n)[0]); print('slot',n,hex(v));show(v,20)
for a,n in [(0x1041f30,16),(0xfe6da0,30),(0x104e6b0,16),(0xf2ba0e,35),(0xfae340,10),(0x3c60119,50)]:print();show(a,n)
