import sys,runpy,struct,re
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
import t49_nation_t9 as a
from t05_pe import PE
p=PE(a.EXE)
for k in ('repu','valu'):
 q=k.encode()[::-1]; print(k,[hex(m.start()) for m in re.finditer(q,p.raw[:0x1752000]) if 0x1000000<m.start()<0x16a0000 or 0x4490000<m.start()<0x44a0000])
sys.path.append(str(a.ROOT.parent/'fm24/tools/python')); import zstandard as z
codec=runpy.run_path(str(a.ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))
for side in ('client','server'):
 _,blob,d=codec['_entries'](a.ROOT/f'scratch/data/{side}_db.dat')
 for e in d['entries']:
  if e['path'].split('/')[-1] not in [f'table_{n}.dat' for n in (3,4,8,9,10,11,19,25)]+['table_extra_9.dat']: continue
  off=34+e['offset']; raw=z.ZstdDecompressor().decompress(blob[off:off+e['packed_size']],max_output_size=e['size']); print(side,e['path'],len(raw),struct.unpack_from('<I',raw,8)[0],raw[:82].hex(' '),raw[-25:].hex(' '))
 if side=='client':
  for k in [b'table_extra_9.dat',b'table_9.dat']:
   for m in list(re.finditer(k,blob))[:5]: print(k,hex(m.start()))
