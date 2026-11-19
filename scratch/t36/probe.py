from pathlib import Path
import sys,struct
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from t05_pe import PE
from capstone import *
from t21b_control_flow import ReaderCFG
p=PE(Path('D:/tmp2b/fm24/input/editor.exe'));p.pe.parse_data_directories(directories=[3]);m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
v=0x1418835e8
slots={i:p.va2f(struct.unpack_from('<Q',p.raw,p.va2f(v)+8*i)[0]) for i in range(26)}
print({i:hex(o) for i,o in slots.items() if o is not None})
def ins(o):return next(m.disasm(p.raw[o:o+15],p.f2va(o),count=1))
def fmt(i):
 a=p.va2f(i.address); t=p.va2f(i.operands[0].imm) if i.mnemonic.startswith(('j','call')) and i.operands[0].type==2 else None
 print(f'{a:09x} {i.mnemonic:8} {i.op_str:48} '+(hex(t) if t is not None else ''))
def show(o,count):
 for i in m.disasm(p.raw[o:o+15*count],p.f2va(o),count=count):fmt(i)
for arg in sys.argv[1:]:
 if arg=='hits':
  key=b'tbdC';idx=0
  while (idx:=p.raw.find(key,idx))!=-1:
   if p.section_of(idx)=='.text': print(hex(idx))
   idx+=1
  continue
 a,_,b=arg.partition(':');o=slots[int(a[1:])] if a.startswith('s') else int(a,16)
 if b:show(o,int(b));continue
 for _ in range(5):
  i=ins(o)
  if i.mnemonic!='jmp':break
  fmt(i);o=p.va2f(i.operands[0].imm)
 cfg=ReaderCFG(p,m,o);print('extent',hex(o),hex(cfg.function_end_off),len(cfg.instructions),cfg.external_edges)
 for i in sorted(cfg.instructions.values(),key=lambda i:i.address):fmt(i)
