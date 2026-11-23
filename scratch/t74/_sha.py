import sys; sys.path.insert(0,'scripts')
import json, hashlib
from t74_row_frames9 import payload, codec
p='scratch/t74/out/frames.json'
d=json.load(open(p,encoding='utf-8'))
c=codec()
for tid in ('56','0','21','8','27','18','7','47','24'):
    for arch in ('client','server'):
        arc=d['tables'][tid]['archives'].get(arch)
        if not arc or arc.get('status')=='absent': continue
        if 'payload_sha256' not in arc:
            b=payload(c,arch,int(tid))
            arc['payload_sha256']=hashlib.sha256(b).hexdigest()
            print('filled',tid,arch,arc['payload_sha256'][:16])
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
missing=[(t,a) for t in d['tables'] for a,ar in d['tables'][t]['archives'].items() if 'payload_sha256' not in ar and ar.get('status')!='absent']
print('still missing:',missing)
