import struct,json,sys
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
def ids(path,n,H=14,F=8):
    b=open(path,'rb').read(); L=len(b)
    cnt,st,_=P._dp(b,'x',H,L-F,n,13,strict_uid=True,pair=True)
    if cnt!=1: return None,None
    ends=list(st[1:])+[L-F]
    out=[];bad=0
    for i in range(n):
        e=ends[i]
        o,u1,u2=struct.unpack_from('<III',b,e-13)
        if o!=i or u1!=u2 or u1==0: bad+=1
        out.append(u1)
    return out,bad
res={}
for name,n in (('t25',7047),('t24',84507),('t10',251)):
    u,bad=ids(f'scratch/t88/{name}.bin',n)
    res[name]=u
    print(name,'bad',bad,'distinct',len(set(u)),'min',min(u),'max',max(u),'first6',u[:6])
res['t3']=json.load(open('scratch/t88/club.json'))['uids']
json.dump(res,open('scratch/t88/refsets.json','w'))
print({k:(len(v),len(set(v))) for k,v in res.items()})
