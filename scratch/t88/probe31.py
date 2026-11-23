import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); minlen=int((ends-starts).min())
print('== date-pair scan: u16 day @o + u16 year @o+2 ==')
res=[]
for o in range(0,minlen-13-3):
    day=np.zeros(n,dtype=np.int64); yr=np.zeros(n,dtype=np.int64)
    for i,(s,e) in enumerate(zip(starts.tolist(),ends.tolist())):
        if s+o+4>e: day[i]=-1; continue
        day[i],yr[i]=struct.unpack_from('<HH',b,s+o)
    good=((day>=1)&(day<=366)&(yr>=1850)&(yr<=2120))
    f=good.mean()
    if f>0.30: res.append((o,round(float(f),4),int((day==0xffff).mean()*1000)/1000))
for o,f,ff in res: print(f'  +{o:3d} frac={f} ffday={ff}')
