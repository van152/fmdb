import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
def walk(fields,path,out):
    for f in fields:
        out.append((path,f))
        if f.get('list_item_fields'):
            walk(f['list_item_fields'], path+'.'+str(f.get('field'))+'.item', out)
for fn,ents in m.get('entities',{}).items():
    for e in ents:
        out=[]; walk(e.get('fields',[]), f"{fn}#{e.get('id')}", out)
        for p,f in out:
            if f.get('field') in ('csap','NWGv','Cffp','Csme','Cwcl','CPsL'):
                print("==",f"{fn}#{e.get('id')}",f.get('field'),f.get('name'),p)
                for sf in (f.get('list_item_fields') or []):
                    print("   ",sf.get('field'),'|',sf.get('name'),'|',sf.get('type'),'|',sf.get('database_table_type',''),'|',sf.get('min_value'),sf.get('max_value'))
                print()
