import struct,json,collections
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); bb=np.frombuffer(b,np.uint8)
minlen=80
mask=np.zeros((n,67),dtype=np.uint8)
for o in range(67):
    mask[:,o]=(bb[starts+o]!=0xff)
keys=[mask[i].tobytes() for i in range(n)]
c=collections.Counter(keys)
print('distinct presence masks',len(c))
for k,v in c.most_common(12):
    m=np.frombuffer(k,np.uint8)
    runs=[]
    i=0
    while i<67:
        if m[i]:
            j=i
            while j<67 and m[j]: j+=1
            runs.append(f'{i}-{j-1}'); i=j
        else: i+=1
    print(f'{v:6d} runs={runs}')
