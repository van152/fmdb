import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p='evidence/fm24/reports/dbdat_decode/db_tables_small.json'
d=json.loads(open(p,encoding='utf-8').read())
print('keys',list(d.keys()))
t=d['tables']
print(type(t),len(t))
k=list(t)[0]
print(json.dumps(t[k],ensure_ascii=False)[:800])
print()
rows=[]
for kk,it in t.items():
    rows.append((it.get('table_id'),it.get('record_count'),it.get('payload_size'),(it.get('row_boundary') or {}).get('stride'),(it.get('row_boundary') or {}).get('status')))
for r in sorted([r for r in rows if r[0] is not None]): print(r)
