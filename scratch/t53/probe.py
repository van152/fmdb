import sys,struct,json,runpy,re
from pathlib import Path
sys.path.insert(0,'scripts')
from t05_pe import PE
from t21b_control_flow import ReaderCFG
from capstone import *
from capstone.x86 import *
p=PE(Path('../fm24/input/editor.exe')); p.pe.parse_data_directories(directories=[3]); m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
F=p.va2f; V=p.f2va; B=p.raw
def out(i):
 a=F(i.address); r=['%x'%F(i.operands[0].imm)] if i.mnemonic.startswith(('j','call')) and i.operands[0].type==X86_OP_IMM and F(i.operands[0].imm)!=None else []
 print('%08x %-7s %-55s %s'%(a,i.mnemonic,i.op_str,' '.join(r)))
def cfg(f): return ReaderCFG(p,m,f)
def dump(a,z):
 for i in m.disasm(B[a:z],V(a)):out(i)
def refs(a,jumps=False):
 va=V(a); s=p.section_of(a); result=[]
 for name,raw,size,rva in [(x.Name,x.PointerToRawData,x.SizeOfRawData,x.VirtualAddress) for x in p.pe.sections if x.Characteristics&0x20000000]:
  for ma in re.finditer(b'[\xe8\xe9]' if jumps else b'\xe8',B[raw:raw+size]):
   f=raw+ma.start()
   if p.base+rva+ma.start()+5+struct.unpack_from('<i',B,f+1)[0]==va:result.append(hex(f))
 return result
if __name__=='__main__':
 for x in sys.argv[1:]:
  if x.startswith('r'): a=int(x[1:],16); print(x,refs(a,True));continue
  if '-' in x: dump(*[int(s,16) for s in x.split('-')]);continue
  f=int(x,16); c=cfg(f);print('CFG',x,hex(c.function_end_off),len(c.instructions),c.external_edges)
  for i in sorted(c.instructions.values(),key=lambda i:i.address):out(i)
