import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
fc=m['field_codes']
for k in ('Nnam','Nsnm','N3ln','Nnty','dbnm','nhrl','ttcl','tbcl','TCnn','TCht','Nlns'):
    print(k,'->',json.dumps(fc.get(k),ensure_ascii=False)[:400])
