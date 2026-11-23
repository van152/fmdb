import sys,json,struct
sys.path.insert(0,'scripts')
import importlib.util
spec=importlib.util.spec_from_file_location('t72','scripts/t72_slot_fingerprint.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import os
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
raw=m.load_payloads()
fsc=json.load(open('scratch/t57/out/field_slots.json'))
cols,spans,ids=m.replay_club(raw['server','club'],'server')
for key in ('raw16a','raw166','person148','raw16c','vec110','obj150_tag','obj150','vec130','vec138','raw168','stad140'):
    cells=cols.get(key,[])
    prof=next(s for s in fsc['slots'] if s['key']==key)['profiles']['server']
    dg=m.H(b''.join(struct.pack('<III',i,p,w) for i,p,w in cells))
    print(key, dg[:12], prof['coordinate_sha256'][:12], dg==prof['coordinate_sha256'], 'rows',len(cells), prof.get('rows'), 'first',cells[0] if cells else None, prof.get('first'))
