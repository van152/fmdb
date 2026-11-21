import sys,struct; sys.path.insert(0,'scripts')
import importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import json,io
d=json.load(io.open('scratch/t81/out/fk_index.json',encoding='utf-8'))
raw=m.load_payload('client',10); L=len(raw)
r=d['targets']['10/client']
c=m.candidate_map(raw,marker0=True)
res=m.solve_chain(raw,c,251,window=(8,65536))
pos=m.pick(res['reach'],raw,window=(8,65536))
print('rows',len(pos))
for j in range(4):
    p=pos[j]; print(j,'pos',p,'ord',m.u32(raw,p),'uid',m.u32(raw,p+4),'tail',raw[p+12], 'alt', sorted(res['reach'][j]))
