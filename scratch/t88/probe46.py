import struct,json,sys
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
def uids(path,n,H=14,F=8):
    b=open(path,'rb').read()
    cnt,st,_=P._dp(b,'x',H,len(b)-F,n,13,strict_uid=True,pair=True)
    if cnt!=1: return None,cnt
    return set(struct.unpack_from('<I',b,p+4)[0] for p in st),1
out={}
for name,n in (('t25',7047),('t24',84507),('t10',251)):
    s,c=uids(f'scratch/t88/{name}.bin',n)
    print(name,'paths',c,'uids',len(s) if s else None)
    if s: out[name]=sorted(s)
out['t3']=json.load(open('scratch/t88/club.json'))['uids']
json.dump(out,open('scratch/t88/refsets.json','w'))
print('sizes',{k:len(v) for k,v in out.items()})
