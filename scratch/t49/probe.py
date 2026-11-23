import sys,runpy,struct,re,collections
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
import t49_nation_t9 as a
from t47_nation_unknown import read_archives
from t05_pe import PE
p=PE(a.EXE); b=p.raw
for k in ('repu','valu'):
 for x in [k.encode(),k.encode()[::-1]]:
  o=[m.start() for m in re.finditer(x,b) if (0x3db0000<m.start()<0x3dd0000) or (0x4460000<m.start()<0x44d0000) or (0x105e000<m.start()<0x1080000)]; print(k,x,len(o),[hex(v) for v in o])
_,raw=read_archives(); b=raw['server','table_9.dat']; r=a.walk(b,1)
for k,fmt in {'Nntp':'<ibbbbb','Nctp':'<ibbbb','Nrtp':'<ibbbb','NTRv':'<i','NWGv':'<i','NSps':'<i','Nfmp':'<ihbBb','NCro':'<Bii'}.items():
 vals=[]
 for x in r['rows']:
  col=x['collections'][k]; n=col['count'];
  if n: vals.extend(struct.iter_unpack(fmt,b[col['start']:col['end']]))
 print(k,len(vals),vals[:20]); print([(min(v),max(v),collections.Counter(v).most_common(12)) for v in zip(*vals)])
sys.path.append(str(a.ROOT.parent/'fm24/tools/python')); import zstandard as z
codec=runpy.run_path(str(a.ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))
for side in ('client','server'):
 _,blob,d=codec['_entries'](a.ROOT/f'scratch/data/{side}_db.dat')
 print(side,[(e['path'],e['size']) for e in d['entries'] if e['size']<1500 or any(s in e['path'] for s in ['table_9.','extra_9.'])])
