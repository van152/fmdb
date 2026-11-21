import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
master=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
F=master['entities']['club.xml'][0]['fields'][211:328]
f4=json.load(open('scratch/t88/f4_to_rectype.json'))
# (rec_type, tag) -> list of field codes
tt={}
for f in F:
    c=f['field']
    for rt,tag in f4.get(c,[]):
        if rt is None or tag is None: continue
        tt.setdefault((rt,tag),[]).append(c)
b4=np.array([b[int(s)+4] for s in starts],dtype=np.int64)
keys=sorted(tt)
print('rectype/tag pairs from 117 set:',len(keys))
for k in keys: print(' ',k,tt[k])
json.dump({f'{a}|{c}':v for (a,c),v in tt.items()},open('scratch/t88/rt_tag_fields.json','w'),indent=1)
