from pathlib import Path
import sys,runpy,struct as s,collections
R=Path(__file__).resolve().parents[2];sys.path.extend([str(R/'scripts'),str(R.parent/'fm24/tools/python')]);import zstandard as z
from t47_nation_unknown import walk
get=runpy.run_path(str(R.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
for side in ['client','server']:
 _,b,d=get(R/f'scratch/data/{side}_db.dat');es={e['path'].split('/')[-1]:e for e in d['entries']};
 for t in [21,41,10]:
  e=es[f'table_{t}.dat'];lo=e['offset']+34;p=z.ZstdDecompressor().decompressobj().decompress(b[lo:lo+e['packed_size']]);
  n=s.unpack_from('<I',p,8)[0];w,mod=divmod(len(p)-22,n);print(side,t,len(p),n,w,mod,p[:55].hex())
  if t==41:
   p0=13; spans=[]; amb=[]; zer=[]
   for i in range(n):
    at=[];q=13
    while (q:=p.find(s.pack('<I',i),q))>=0:
     if q+13<=len(p) and p[q+4:q+8]==p[q+8:q+12] and p[q+4:q+8]!=bytes(4) and p[q+12]==0:at.append(q)
     q+=1
    if len(at)>1:amb.append((i,at))
    if not at:zer.append(i);continue
    tail=next((a for a in at if a>=p0),None)
    if tail is not None:spans.append((p0,tail+12-p0,p[p0:p0+16].hex(),s.unpack_from('<I',p,tail+4)[0]));p0=tail+12
   print('currency',amb[:5],zer[:5],p0,len(spans),'example',spans[:16]); print('hist',collections.Counter(x[1] for x in spans))
  if t==10:
   w=walk(p,int(side=='server'));site=[(0x103fb0e,4),(0x1040360,4),(0x1040384,4),(0x10403a8,4),(0x10403cc,4),(0x10403f0,4),(0x1040414,4),(0x10405c7,1),(0x10405eb,4),(0x104060f,4),(0x1040633,4),(0x1040657,4),(0x104067b,1),(0x104069f,1),(0x10406c3,4),(0x10406e7,1)]+[(0x10409f0+0x24*k,4 if k<10 else 2 if k==10 else 1) for k in range(12)];
   for st,width in site:
    if st not in w['visits']:continue
    pts=[]
    for row in w['rows']:
     y=walk(p[:13]+p[row['wire13']:row['end']],int(side=='server'),0) if False else None
     if side=='client': common=row['legacy14']
     else:common=None
    o=w['visits'][st]['absolute']; print(hex(st),o,p[o:o+width].hex(),int.from_bytes(p[o:o+width],'little',signed=True))
