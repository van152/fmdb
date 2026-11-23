import json,collections
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
b4=np.array([b[int(s)+4] for s in starts])
def mask(i,lo,hi,anchor):
    base=int(starts[i]) if anchor=='s' else int(ne[i])
    return bytes(1 if b[base+k]!=0xff else 0 for k in range(lo,hi))
for anchor,rng,label in (('s',(0,37),'prefix'),('n',(0,26),'tail')):
    print(f'== {label} masks grouped by b4 ==')
    g=collections.defaultdict(collections.Counter)
    for i in range(0,n,37):
        g[int(b4[i])][mask(i,*rng,anchor)]+=1
    for k in sorted(g):
        tot=sum(g[k].values()); top=g[k].most_common(1)[0]
        print(f'  b4={k:3d} rows={tot:6d} patterns={len(g[k]):3d} top_share={top[1]/tot:.2f}')
