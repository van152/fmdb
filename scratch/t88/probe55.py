import struct,json,sys
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
def ids(path,n,H=14,F=8):
    b=open(path,'rb').read()
    cnt,st,_=P._dp(b,'x',H,len(b)-F,n,13,strict_uid=True,pair=True)
    if cnt!=1: return None
    ends=[p+13 for p in st]+[len(b)-F]
    out=[]; bad=0
    for i in range(n):
        e=ends[i]
        o,u1,u2=struct.unpack_from('<III',b,e-13)
        if o!=i or u1!=u2 or u1==0: bad+=1
        out.append(u1)
    return out,bad
res={}
for name,n in (('t25',7047),('t24',84507),('t10',251)):
    r=ids(f'scratch/t88/{name}.bin',n)
    if not r: print(name,'no unique path'); continue
    u,bad=r; res[name]=u
    print(name,'bad_identity',bad,'distinct uid',len(set(u)),'min',min(u),'max',max(u),'first5',u[:5])
res['t3']=json.load(open('scratch/t88/club.json'))['uids']
json.dump(res,open('scratch/t88/refsets.json','w'))
print({k:len(v) for k,v in res.items()})
