import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import re, collections

raw=load('server',24)
n=len(raw)
runs=[]
for m in re.finditer(rb'[ -~]{3,}', raw):
    runs.append((m.start(), m.end()-m.start(), m.group()[:40]))
print('printable runs >=3:', len(runs))
print('first 12:')
for a,b,c in runs[:12]: print(f'  @{a} len={b} {c!r}')
print('last 6:')
for a,b,c in runs[-6:]: print(f'  @{a} len={b} {c!r}')
# where do long runs cluster
import bisect
pos=[a for a,_,_ in runs]
buckets=collections.Counter(a//500000 for a in pos)
print('run starts per 500KB bucket:', sorted(buckets.items()))
print('total printable bytes', sum(b for _,b,_ in runs), 'of', n)
print('after header printable bytes', sum(b for a,b,_ in runs if a>=14))
