import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); bb=np.frombuffer(b,np.uint8)
RT={7,8,9,10,11,12,13,14,15,18,19,23,24,25,26,27,28}
minlen=(ends-starts).min()
print('min row len',minlen)
best=[]
for o in range(0,minlen-13):
    col=bb[starts+o]
    u,c=np.unique(col,return_counts=True)
    frac=np.isin(col,list(RT)).mean()
    if frac>0.5 and len(u)<=20:
        best.append((o,len(u),char:=frac,sorted(u.tolist())))
for o,k,f,u in best: print('cand byte',o,'uniq',k,'frac_rt',round(f,4),u)
