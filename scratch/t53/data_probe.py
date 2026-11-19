from probe import *
t=runpy.run_path('scripts/t49_nation_t9.py'); raw,_=t['archives'](); print(raw.keys()); b=raw['server','table_9.dat']; T=json.load(open('scratch/t49/out/cursor_t9_server.json')); print(T.keys());
pers=(t['dbroot']()/'basic_people_db.dat').read_bytes();import zstandard as zs
pers=zs.ZstdDecompressor().decompress(pers[8:],max_output_size=60000000); keys={};uids={}; a=5
for k in range(658011):
 tag,cls=pers[a:a+2]; a+=(83,83,83,34,22)[cls-1]; x,y,z=struct.unpack_from('<III',pers,a-12); assert x==k and y==z and y; keys[k]=(y,cls);uids[y]=k
from collections import Counter
series=[Counter() for x in range(7)]; jt=Counter(); ex={}; features=[]
P=[x for x in T['rows'] for s,a,w,n in x['trace'] if s==0x105dd07 and b[a]]
for x in P:
 ev=x['trace']; g=next(a for s,a,w,n in ev if s==0x105dd07); end=next(a for s,a,w,n in ev if s==0x105dd87); ver,n=struct.unpack_from('<II',b,g+1); a=g+9; features.append((ver,n,end-a))
 for j in range(n):
  data=struct.unpack_from('<hiBBHBB',b,a); tag,k,i,tt,job,ob8,ob9=data
  for h,v in zip(series,data):h[v]+=1
  if k!=-1:
   jt['live']+=1
   for typ,domain in [('ordinal',keys),('uid',uids)]:
    got=domain.get(k); jt[typ+str(got is not None)]+=1; ex.setdefault((typ,got is not None),(x['row'],j,a,data,got))
  else: jt['-1']+=1
  ex.setdefault(('ob9',ob9),(x['row'],j,a,data,keys.get(k)))
  a+=12
 assert a==end
print('features',Counter(k[0] for k in features),sum(k[1] for k in features))
print('hist',[(len(x),x if i!=1 else x.most_common(20)) for i,x in enumerate(series)]);print(jt,ex)
for side in ['client','server']:
 q=raw[side,'table_extra_9.dat']; a=12; d,n=struct.unpack_from('<II',q,a); a+=8+n
 print(side, hex(a),q[12:100].hex(), int.from_bytes(q[a:a+2],'little'),int.from_bytes(q[a+2:a+6],'little'))
PY=0
