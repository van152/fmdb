import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
a0=np.array([int.from_bytes(b[int(s):int(s)+4],'little') for s in starts],dtype=np.int64)
# per-group first-row prefix signature: does group (a0) determine the prefix bytes 5..12?
import collections
g=collections.defaultdict(list)
for i in range(n): g[int(a0[i])].append(i)
sizes=[len(v) for v in g.values()]
print('groups',len(g),'size min/max',min(sizes),max(sizes))
# check monotone blocks: group members contiguous?
contig=sum(1 for v in g.values() if v[-1]-v[0]+1==len(v))
print('contiguous groups',contig,'/',len(g))
# tail shape per group
print('rows per group hist sample',sorted(sizes)[:5],sorted(sizes)[-5:])
