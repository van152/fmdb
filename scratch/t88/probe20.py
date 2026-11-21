import sys,struct,json,runpy,os,pathlib
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
b=open('scratch/t88/t3.bin','rb').read(); L=len(b); n=struct.unpack_from('<I',b,8)[0]
print('t3 len',L,'n',n,'mean',(L-22)/n)
cnt,starts,_=P._dp(b,'t3',14,L-8,n,13,strict_uid=True,pair=True)
print('paths',cnt)
rows=list(zip(starts,starts[1:]+[L-8]))
lens=[e-s for s,e in rows]; print('lens',min(lens),max(lens),len(set(lens)))
bad=0
for i,(s,e) in enumerate(rows):
    o,u1,u2=struct.unpack_from('<III',b,e-13)
    if o!=i or u1!=u2 or u1==0: bad+=1
print('bad',bad,'lastbyte',{b[e-1] for s,e in rows})
uids=np.array([struct.unpack_from('<I',b,e-9)[0] for s,e in rows])
print('uid uniq',len(np.unique(uids)),'first5',uids[:5].tolist())
json.dump({'uids':uids.tolist(),'starts':starts},open('scratch/t88/club.json','w'))
