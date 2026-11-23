import importlib.util,json,collections,struct
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
en=M['enums']
for k in ('icla','iscl','Icau','inSr','Iagr','Icms'):
    vals=[v['enum'] for v in en[k]['values']]
    print(k,'n=',len(vals),vals)
