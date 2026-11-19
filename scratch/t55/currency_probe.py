exec(open('scratch/t55/probe.py',encoding='utf8').read().split('for x in sys.argv[1:]:')[0]);import struct as s
for k in sys.argv[1:]:
 o=int(k,16)
 for i in m.disasm(p.raw[o:o+160],p.f2va(o)):
  op=i.operands; t=p.va2f(op[0].imm) if op and op[0].type==2 and i.mnemonic.startswith(('j','call')) else None
  v=next((i.address+i.size+x.mem.disp for x in op if x.type==3 and m.reg_name(x.mem.base)=='rip'),None)
  print(hex(p.va2f(i.address)),i.mnemonic,i.op_str,hex(t) if t else '',hex(v) if v else '')
  if i.mnemonic in ('jmp','ret'):break
