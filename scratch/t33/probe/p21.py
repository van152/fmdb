import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
def walk(fields,path,out):
    for f in fields:
        out.append((path,f))
        if f.get('list_item_fields'): walk(f['list_item_fields'], path+'.'+str(f.get('field')), out)
allnodes=[]
for fn,ents in m['entities'].items():
    for e in ents:
        out=[]; walk(e.get('fields',[]), f"{fn}#{e.get('id')}", out)
        for p,f in out: allnodes.append((fn,e,p,f))
print("--- nodes mentioning restricted/non-eu/slot")
for fn,e,p,f in allnodes:
    s=(str(f.get('name'))+' '+str(f.get('field'))).lower()
    if 'restrict' in s or ('non eu' in s) or 'non-eu' in s:
        print(f"  {p}.{f.get('field')} | {f.get('name')} | {f.get('type')}")
print("--- Plhs/Pnph/Pacl items")
for fn,e,p,f in allnodes:
    if f.get('field') in ('Plhs','Pnph','Pacl') and f.get('type')=='list' and p.startswith('person.xml'):
        print(f"== {p}.{f.get('field')} {f.get('name')}")
        for sf in f['list_item_fields']:
            print(f"    {sf.get('field'):6s} {str(sf.get('name'))[:34]:36s} {sf.get('type'):28s} {sf.get('database_table_type') or ''} {sf.get('min_value')} {sf.get('max_value')}")
