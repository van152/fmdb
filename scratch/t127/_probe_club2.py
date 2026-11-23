import importlib.util,sys,json
class W:
    def write(self,s): pass
    def flush(self): pass
    def reconfigure(self,**k): pass
sys.stdout=W()
spec=importlib.util.spec_from_file_location('t02','scripts/t02_club.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows=m.parse(m.load_table())[0]
sys.stdout=sys.__stdout__
byname={}
for r in rows:
    uid=r['identity'][1]
    byname.setdefault(uid, r['short_name'])
ks=(728,674,686,691,673,680,1736,1139,1708,868,1489,1668,55056835,4212171,1708)
out={str(k):byname.get(k) for k in ks}
open('scratch/t127/out/_clubnames2.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
print('unique uids',len(byname))
