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
names={}
for r in rows: names.setdefault(r['id5'],r['short_name'])
ks=(728,674,686,512,1708,1489,915,1865,460,1282,623,586,811,1489,680,1234)
out={k:names.get(k) for k in ks}
open('scratch/t127/out/_clubnames.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
print('ok',len(names))
