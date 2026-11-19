import sys,re,struct
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
from t05_pe import PE
p=PE(Path('../fm24/input/editor.exe')); b=p.raw
for k in [b'table_extra', 'table_extra'.encode('utf-16-le')]:
 for m in re.finditer(k,b):
  o=m.start(); v=p.f2va(o); print(hex(o),hex(v),b[o:o+50]);
  for x in re.finditer(rb'[\x48-\x4f]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]....', b[:0x1752000], re.S):
   a=x.start(); q=a+7+struct.unpack_from('<i',b,a+3)[0];
   if o-10<=q<=o+15:print('xref',hex(a),hex(q))
v=p.va2f(0x1418898d8)
print([(i,hex(p.va2f(struct.unpack_from('<Q',b,v+i*8)[0]) or 0)) for i in range(45)])
