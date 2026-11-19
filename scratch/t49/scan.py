import sys
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
from t05_pe import PE
from t21b_control_flow import ReaderCFG
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
from capstone.x86 import X86_OP_IMM
p=PE(Path('../fm24/input/editor.exe')); p.pe.parse_data_directories(directories=[3]); m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
for s in sys.argv[1:]:
 a,*z=map(lambda x:int(x,16),s.split(':')); c=(m.disasm(p.raw[a:z[0]],p.f2va(a)) if z else (i for v,i in sorted(ReaderCFG(p,m,a).instructions.items())))
 for i in c:
  trg=p.va2f(i.operands[0].imm) if i.operands and i.operands[0].type==X86_OP_IMM and (i.mnemonic=='call' or i.mnemonic.startswith('j')) else None
  print(f'{p.va2f(i.address):08x} {i.mnemonic:8} {i.op_str}'+(f' => {trg:x}' if trg is not None else ''))
