import sys,struct,runpy,os,pathlib,json
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
b=open('scratch/t88/t45.bin','rb').read(); L=len(b); n=84477
cnt,starts,_=P._dp(b,'t45',14,L-8,n,13,strict_uid=True,pair=True)
print('paths',cnt)
bounds=[14]+[p+13 for p in starts]
rows=[(bounds[i],bounds[i+1]) for i in range(n)]
print('closure',bounds[-1]==L-8,'lens',min(e-s for s,e in rows),max(e-s for s,e in rows),len(set(e-s for s,e in rows)))
bad=0; last={}
for i,(s,e) in enumerate(rows):
    o,u1,u2=struct.unpack_from('<III',b,e-13)
    if o!=i or u1!=u2 or u1==0: bad+=1
    last[b[e-1]]=last.get(b[e-1],0)+1
print('bad_identity',bad,'lastbyte',last)
uids=[struct.unpack_from('<I',b,e-9)[0] for s,e in rows]
u=np.array(uids); print('uid unique',len(np.unique(u)),'monotone',bool((np.diff(u)>0).all()))
# first dword of each row payload
d0=np.array([struct.unpack_from('<I',b,s)[0] for s,e in rows])
print('d0 range',d0.min(),d0.max(),'uniq',len(np.unique(d0)),'top',np.unique(d0,return_counts=True)[0][:10])
# save
json.dump({'starts':starts},open('scratch/t88/rows.json','w'))
