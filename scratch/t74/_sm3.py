import json
d=json.load(open('evidence/fm24/reports/dbdat_decode/db_tables_small.json',encoding='utf-8'))
import pprint
pprint.pprint(d['tables']['7'])
print('---')
pprint.pprint(d['tables']['27'])
