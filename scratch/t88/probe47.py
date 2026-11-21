import json,re
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts)
TAGS=[b'stdt',b'comp',b'stid',b'stnm',b'gols',b'ogls',b'fsgt',b'gams',b'endt',b'atte',b'stdb',b'otht',b'cash',b'cnst',b'rati',b'info',b'ettt',b'stge',b'stda']
for t in TAGS:
    c=0; first=None
    for i in range(0,n,7):
        s,e=int(starts[i]),int(ends[i])
        if t in b[s:e]:
            c+=1
            if first is None: first=(i,b[s:e].find(t))
    print(t.decode(), c, '(sampled /12069 rows)', first)
