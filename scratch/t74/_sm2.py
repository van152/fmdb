import json
d=json.load(open('evidence/fm24/reports/dbdat_decode/db_tables_small.json',encoding='utf-8'))
for k,v in d['tables'].items():
    print(k, v.get('entity'), v.get('model'), v.get('header'), v.get('footer'), v.get('count'),
          v.get('stride'), v.get('payload_client'), v.get('payload_server'))
