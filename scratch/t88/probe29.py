import struct,json
import numpy as np
b=open('scratch/t88/t3.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/club.json')); starts=np.array(d['starts']); uids=np.array(d['uids'])
ends=np.append(starts[1:],L-8)
print('club rows',len(starts))
print('uid first10',uids[:10].tolist(),'last3',uids[-3:].tolist())
print('uid<84259 count',int((uids<84259).sum()))
for off in (0,4,8,12,16):
    v=np.array([struct.unpack_from('<I',b,s+off)[0] for s in starts[:12]])
    print('offset',off,v.tolist())
print('row0 head',b[starts[0]:starts[0]+40].hex(' '))
