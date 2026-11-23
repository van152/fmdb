from probe import *
from collections import defaultdict
A=[(p.r2f(x.struct.BeginAddress),p.r2f(x.struct.EndAddress)) for x in p.pe.DIRECTORY_ENTRY_EXCEPTION]; A=sorted((a,z) for a,z in A if a is not None and z is not None); import bisect
starts=[a for a,z in A]
for h in [b'\x88\x01\0\0']:
 C=defaultdict(set)
 for x in re.finditer(re.escape(h),B):
  a=x.start(); f=bisect.bisect_right(starts,a)-1
  if f<0: continue
  s,z=A[f]
  if a<z and (0x1030000<s<0x1080000 or 0x11c0000<s<0x1200000 or 0x3d50000<s<0x3dd0000 or 0x3e90000<s<0x3ed0000): C[s].add(a)
 for s,poss in C.items():
  try:c=cfg(s)
  except ValueError:continue
  xs=[]; b0=[]
  for i in c.instructions.values():
   if i.disp_size==4 and F(i.address)+i.disp_offset in poss and any(o.type==X86_OP_MEM and o.mem.disp==392 and o.mem.base not in (X86_REG_RSP,X86_REG_RBP) for o in i.operands):xs.append(i)
   if any(o.type==X86_OP_MEM and o.mem.disp==176 and o.mem.base not in (X86_REG_RSP,X86_REG_RBP) for o in i.operands):b0.append(i)
  if xs:
   print('function',hex(s));[out(i) for i in xs+b0]
for a in [0xeb7783,0xe5d5a6,0x29c80]:
 i=bisect.bisect_right(starts,a)-1;s,z=A[i];c=cfg(s);print('owner',hex(a),hex(s),hex(z));[out(k) for k in sorted(c.instructions.values(),key=lambda j:j.address) if a-75<=F(k.address)<=a+45]
