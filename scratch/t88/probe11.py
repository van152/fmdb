import sys,struct,json
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
b=open('scratch/t88/t45.bin','rb').read(); L=len(b); n=84477
cnt,starts,_=P._dp(b,'t45',14,L-8,n,13,strict_uid=True,pair=True)
print('paths',cnt,'starts0..3',starts[:3])
rows=list(zip(starts,starts[1:]+[L-8]))
print('closure',rows[-1][1]==L-8, 'n',len(rows))
lens=[e-s for s,e in rows]
print('lens min/max/distinct',min(lens),max(lens),len(set(lens)),'sum',sum(lens),'expect',L-8-14)
bad=0;last={}
for i,(s,e) in enumerate(rows):
    o,u1,u2,mk=struct.unpack_from('<IIIB',b,s)
    if o!=i or u1!=u2 or u1==0: bad+=1
    last[mk]=last.get(mk,0)+1
print('identity at row_start bad',bad,'marker',last)
uids=np.array([struct.unpack_from('<I',b,s+4)[0] for s,e in rows])
print('uid uniq',len(np.unique(uids)),'monotone',bool((np.diff(uids)>0).all()))
print('len hist sample',sorted(set(lens))[:10],sorted(set(lens))[-6:])
# where is identity within row? try row_start and row_end-13
d=[e-s for s,e in rows]
print('first rows',rows[:4])
print('row0 hex',b[14:rows[0][1]].hex(' '))
json.dump({'starts':starts},open('scratch/t88/rows.json','w'))
