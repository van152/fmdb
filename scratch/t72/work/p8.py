import sys,json,struct,os
import importlib.util
spec=importlib.util.spec_from_file_location('t72','scripts/t72_slot_fingerprint.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
raw=m.load_payloads()
fsc=json.load(open('scratch/t57/out/field_slots.json'))
cols,spans,ids=m.replay_club(raw['server','club'],'server')
for key in ('vec110','vec130','vec138'):
    cells=cols[key]; prof=next(s for s in fsc['slots'] if s['key']==key)['profiles']['server']
    print(key,'mybytes',sum(w for _,_,w in cells),'frozen',prof['bytes'],'myrows',len(cells))
    print('  widths mine',sorted(set(w for _,_,w in cells))[:10], 'last cell',cells[-1],'frozen last',prof['last'])
