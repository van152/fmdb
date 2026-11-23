import json, collections
from pathlib import Path
hits = json.loads(Path("scratch/t10/proto/hits.json").read_text())
hits.sort()
region=[(o,c) for o,c in hits if 0xe54000<=o<0xe94000]
print('hits in 0xe54000..0xe94000',len(region))
# print gaps > 0x400
prev=None
for o,c in region:
    if prev is not None and o-prev>0x200:
        print(f'  gap {prev:#x} -> {o:#x} = {o-prev:#x}')
    prev=o
print('first',region[0], 'last', region[-1])
# bucket by 0x1000
b=collections.Counter(o//0x1000 for o,c in region)
for k in sorted(b): print(hex(k*0x1000), b[k])
