import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
refs=json.load(open('scratch/t88/refsets.json'))
S={'club':set(refs['t3']),'comp':set(refs['t25']),'team':set(refs['t24'])}
def getv(base,off,w):
    out=np.zeros(n,dtype=np.int64)
    for i in range(n):
        p=int(base[i])+off
        out[i]=int.from_bytes(b[p:p+w],'little') if p+w<=L else -1
    return out
rows=[]
for tag,base,lim in (('s',starts,67),('e',ne,26)):
    for o in range(lim):
        for w in (1,2,4):
            if o+w>lim: continue
            v=getv(base,o,w); mx=(1<<(8*w))-1
            f=v[v!=mx]
            d4=0.0
            if w==4 and len(f):
                d4=float((((f&0xffff)>=1)&((f&0xffff)<=366)&((f>>16)>=1850)&((f>>16)<=2120)).mean())
            rows.append(dict(col=f'{tag}+{o}',off=o,width=w,
                ff=round(float((v==mx).mean()),4),zero=round(float((v==0).mean()),4),
                nonzero_frac=round(float((v!=0).mean()),4),
                ref={k:round(float(np.mean([x in s for x in v.tolist()])),4) for k,s in S.items()},
                date4=round(d4,4),uniq=int(len(np.unique(v))),mx=int(v.max()),mn=int(v.min()),
                legit0=round(float(((v==0)&(v!=mx)).mean()),4)))
json.dump(rows,open('scratch/t88/colstat.json','w'),indent=0)
print('cols',len(rows))
for r in rows:
    if r['width']==4 and (max(r['ref'].values())>0.85 or r['date4']>0.9):
        print(f"{r['col']:6s} club={r['ref']['club']:.3f} comp={r['ref']['comp']:.3f} team={r['ref']['team']:.3f} date4={r['date4']:.2f} ff={r['ff']:.3f}")
