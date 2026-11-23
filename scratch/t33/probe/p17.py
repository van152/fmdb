import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
want={'Plhs','Pnph','Pacl','Pcbl','PcbV','Pdcn','PErt','Prls','Csme','Cwcl','csap','Cffp','CPsL','Cafl','Calt','pfvp'}
def walk(fields,path,out):
    for f in fields:
        out.append((path,f))
        if f.get('list_item_fields'): walk(f['list_item_fields'], path+'.'+str(f.get('field')), out)
for fn,ents in m.get('entities',{}).items():
    for e in ents:
        out=[]; walk(e.get('fields',[]), f"{fn}#{e.get('id')}", out)
        for p,f in out:
            if f.get('type')=='list' and f.get('field') in want:
                print(f"== {p}.{f.get('field')} | {f.get('name')}")
                for sf in (f.get('list_item_fields') or []):
                    print(f"    {sf.get('field'):6s} {str(sf.get('name'))[:34]:36s} {sf.get('type'):28s} {sf.get('database_table_type') or ''}")
