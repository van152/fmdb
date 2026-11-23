import runpy, os, struct, sys
os.environ['FM24_DB_DIR']='D:/tmp2b/fm24-db/scratch/data'
k=runpy.run_path('scripts/fm24_dump.py')
codec=k['_reader']()
targets=[b'Liverpool', b'England', b'Premier Division', b'Arsenal', b'Manchester']
members=[]
for a in ('client','server'):
    for n in ('name_table_0','name_table_1','name_table_2','name_table_extra_0','name_table_extra_1','name_table_extra_2'):
        members.append((a,n))
for a,t in [('client','3'),('client','10'),('client','25'),('client','2'),('client','19')]:
    pass
for a,n in members:
    raw=k['load_payload'](codec,a,n)
    hits={t: raw.find(t) for t in targets if raw.find(t)>=0}
    cnt=struct.unpack_from('<I',raw,8)[0]
    print(a,n,'len',len(raw),'cnt',cnt,'hits',hits)
