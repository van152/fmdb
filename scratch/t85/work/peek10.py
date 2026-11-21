import json,sys,runpy
sys.stdout.reconfigure(encoding='utf-8')
k=runpy.run_path('scratch/t01/inbox/t01k/verify.py')
codec=runpy.run_path(k['OLD_READER_PATH'])
import pathlib
for a in ('client','server'):
    fn=f'{a}_db.dat'; p=pathlib.Path('scratch/data')/fn
    db=p.read_bytes()
    lay=codec['_archive_layout'](db)
    ents=codec['list_tables'](p,fn)
    print(a,'entries',len(ents),'layout',{kk:lay[kk] for kk in list(lay)[:8]})
    print(' sample',json.dumps(ents[0],ensure_ascii=False)[:300])
    types=[e.get('entry_type') for e in ents]
    import collections; print(' types',collections.Counter(types))
    tids=sorted(e.get('table_id') for e in ents if e.get('table_id') is not None)
    print(' tids',tids)
