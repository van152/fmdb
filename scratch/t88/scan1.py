import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
refs=json.load(open('scratch/t88/refsets.json'))
S={'club':set(refs['t3']),'comp':set(refs['t25']),'team':set(refs['t24'])}
def get(base,off,w):
    idx=np.array([int(x)+off for x in base])
    lo=idx.min(); 
    out=np.zeros(n,dtype=np.int64)
    for i in range(n):
        p=int(idx[i])
        out[i]=int.from_bytes(b[p:p+w],'little') if p+w<=L else -1
    return out
def row(name,base,off,w):
    v=get(base,off,w); mx=(1<<(8*w))-1
    ff=float((v==mx).mean()); z=float((v==0).mean())
    refm={k:float(np.mean([x in s for x in v.tolist()])) for k,s in S.items()}
    dp=0.0
    if w==4:
        f=v[v!=mx]
        if len(f):
            dp=float((((f&0xffff)>=1)&((f&0xffff)<=366)&((f>>16)>=1850)&((f>>16)<=2120)).mean())
    return dict(name=name,off=off,width=w,ff=round(ff,4),zero=round(z,4),
                ref={k:round(x,4) for k,x in refm.items()},date4=round(dp,4),
                uniq=int(len(np.unique(v))),mx=int(v.max()),mn=int(v.min()))
out=[]
for o in range(0,67):
    for w in (1,2,4):
        if o+w>67: continue
        out.append(row(f's+{o}',starts,o,w))
for o in range(0,26):
    for w in (1,2,4):
        if o+w>26: continue
        out.append(row(f'e+{o}',ne,o,w))
json.dump(out,open('scratch/t88/colstat.json','w'))
print('cols',len(out))
for r in out:
    if r['date4']>0.9: print('DATE4',r['name'],r['width'],r['ff'],r['date4'])
for r in out:
    if r['width']==4 and max(r['ref'].values())>0.9: print('REF  ',r['name'],r['ref'])
