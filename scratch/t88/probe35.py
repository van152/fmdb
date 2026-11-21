import struct,json,collections
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); bb=np.frombuffer(b,np.uint8)
ne=starts+41+sl
# presence mask over tail region rel name end (26 bytes) and prefix
def homog(col,keys):
    g=collections.defaultdict(set)
    for v,k in zip(col.tolist(),keys): g[v].add(k)
    pure=sum(1 for v,s in g.items() if len(s)==1)
    return len(g), pure, sum(len(s) for s in g.values())/max(1,len(g))
keys=[bb[s:s+45].tobytes() for s in starts]  # prefix fingerprint
print('== prefix cols grouped by tail-shape homogeneity ==')
tkeys=[bb[ne[i]+0:ne[i]+26].tobytes() for i in range(n)]
for o in range(0,41):
    col=bb[starts+o]
    ng,pure,avg=homog(col,tkeys)
    print(f'P{o:3d} uniq={ng:4d} pure={pure:4d} avg_tails_per_val={avg:6.1f}')
