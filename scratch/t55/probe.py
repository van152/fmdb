import sys,json
from pathlib import Path
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'scripts'))
from t05_pe import PE
from t21b_control_flow import ReaderCFG
from capstone import *
p=PE(r.parent/'fm24/input/editor.exe');p.pe.parse_data_directories(directories=[3]);m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
D=lambda off,n=15: next(m.disasm(p.raw[off:off+n],p.f2va(off)),None)
fields=json.loads((r/'evidence/fm24/reports/editor_schema/master.json').read_bytes())['entities']['nation.xml'][0]['fields']; keys={int.from_bytes(f['field'].encode(),'big'):f['field'] for f in fields if len(f.get('field',''))==4}
for x in sys.argv[1:]:
 if ':' in x:
  a,b=map(lambda y:int(y,16),x.split(':')); seq=m.disasm(p.raw[a:b],p.f2va(a))
 else:
  a=int(x,16); c=ReaderCFG(p,m,a);seq=[i for v,i in sorted(c.instructions.items())];print(f'CFG {a:x}, size {len(seq)}, end {c.function_end_off:x}, ext {len(c.external_edges)}')
 for i in seq:
  ann='';ops=i.operands
  if len(ops)==2 and ops[1].type==2 and ops[1].imm in keys:ann=keys[ops[1].imm]
  if ops and ops[0].type==2 and (i.mnemonic=='call' or i.mnemonic.startswith('j')):
   ann=f'-> {p.va2f(ops[0].imm):x}'
  print(f'{p.va2f(i.address):x} {i.mnemonic:7} {i.op_str:40} {ann}')
