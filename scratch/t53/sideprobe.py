import runpy,json,os,struct
from collections import Counter
T=runpy.run_path('scripts/t49_nation_t9.py'); raw,_=T['archives']();
for side in ('client','server'):
 b=raw[side,'table_extra_9.dat']; lines=[json.loads(x) for x in open(f'scratch/t50/out/profiles/table_{side}_extra_9.rows.jsonl',encoding='utf8')];
 for mode in (0,1):
  events=[];fail=[]
  for r in lines:
   a=r['offset']; e=a+r['len']; j=r['row']; stage=[]
   if side=='server' and j==1: e+=8
   if side=='server' and j==2: a+=8
   if side=='server' and j==81: e+=94
   if side=='server' and j==82: a+=94
   p=a+8+(struct.unpack_from('<I',b,a+4)[0])
   def n(w,s='n',sgn=False):
    global p
    at=p;p+=w
    if p>e:raise ValueError('short',s,at,e)
    return int.from_bytes(b[at:p],'little',signed=sgn)
   def c(w,s,m,sgn=False):
    at=p;v=n(w,s,sgn)
    if v<0 or v*m>e-p:raise ValueError('invalid count',s,at,v,e)
    return v
   try:
    n(2); n(c(4,'string2',1),'string2 byte data'); sw=c(1,'vector1',27); n(27*sw);n(8); stage.append((p,'end base', b[p:min(p+24,e)].hex()));
    if mode:
     v=c(2,'vector2',20,True);n(20*v); v=c(1,'vector3',6,True);n(6*v);n(16);v=c(2,'typed vector',1);stage.append((p,v))
     for _ in range(v):
      at=p;sel=n(1,'typed tag'); stage.append((at,'typed',sel))
      if sel!=9:raise ValueError('typed unresolved',at,sel)
      n(20,'type9 fixed');
      for _ in range(4):n(c(4,'type9 string',1),'type9 data')
     at=p;g=n(1,'gate'); stage.append((at,g))
     if g:
      v=n(4,'version'); k=c(4,'TCrs count',10); tags=[]; base=p
      for _ in range(k):
       tag=n(2,'tag',True);tags.append(tag); n(10 if tag>=3 else 9 if tag>=2 else 8,'item')
      stage.append((base,v,k,Counter(tags)))
      if k and side=='server' and mode==1:
       for x in range(base,p,12): print('item',j,x,struct.unpack_from('<hiBBHBB',b,x))
    if p!=e:raise ValueError('not end',p,e,e-p)
    events.append((j,stage))
   except ValueError as x:fail.append((j,x.args,stage))
  print(side,mode,'pass',len(events),'gates',Counter(x[1][-1][1] for x in events if len(x[1])==3),'items examples',[x for x in events if len(x[1])==4][:10]);print('fail',len(fail),fail[:12]);print('pass ex',events[:2]); print('typed tags',Counter(y[2] for _,_,ss in fail for y in ss if len(y)==3 and y[1]=='typed')); print('live',[(j,s[-2:]) for j,s in events if len(s[-1])==4])
