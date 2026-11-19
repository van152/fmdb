import sys,json,runpy,struct,os
from pathlib import Path
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'scripts'))
import t47_nation_unknown as t47
sys.path.append(str(r.parent/'fm24/tools/python')); import zstandard as z
codec=runpy.run_path(str(r.parent/'fm24/scripts/modding_read_dbdat.py')); N=lambda x:json.loads((r/x).read_bytes());P=N('scratch/t47/out/cursor_nation_tax.json');
for side in ('client','server'):
 _,b,x=codec['_entries'](r/f'scratch/data/{side}_db.dat');
 for e in x['entries']:
  if e['path'].split('/')[-1] not in [f'table_{i}.dat' for i in range(1,32) if i not in (3,9,25)]:continue
  p=z.ZstdDecompressor().decompress(b[e['offset']+34:e['offset']+34+e['packed_size']],max_output_size=e['size']);n=struct.unpack_from('<I',p,8)[0]; print(side,e['path'],len(p),n,divmod(len(p)-22,n) if n else '',p[-21:].hex());
  if e['path'].endswith('table_10.dat'):
   for i in [0,55,139,149,162]:
    a=P[side]['rows'][i]; q=a['identity_at']; print(i,a['identity'],p[a['legacy14']:a['legacy14']+36].hex(),p[q-43:q].hex());
for x in ['reports/t22_nation_capital.json','scratch/t46/out/grammar_diff_client_server.json','scratch/t28/out/fields_nation_client.json','scratch/t47/out/fields_nation_tax.json','scratch/t53/out/fields_PUnJ.json']:
 y=N(x);print(x,[(k,type(v).__name__,len(v) if hasattr(v,'__len__') else v) for k,v in y.items()]);
