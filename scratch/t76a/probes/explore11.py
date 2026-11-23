import json, sys
s = json.load(open('evidence/fm24/reports/editor_schema/master.json'))
d = s['entities']['stadium.xml'][0]
fields = d['fields']
print('total fields', len(fields))
cli, srv, neither = [], [], []
for f in fields:
    cf = f.get('is_client_field') == 'true'
    (cli if cf else srv).append(f)
print('\n=== is_client_field=true (%d) ===' % len(cli))
for f in cli:
    print(' ', f['field'], '|', f['name'], '|', f['type'], '|', f.get('database_table_type', ''), '|',
          'lang' if f.get('is_language_field') else '')
print('\n=== NOT client (%d) ===' % len(srv))
for f in srv:
    print(' ', f['field'], '|', f['type'], '|', f.get('database_table_type', ''), '|',
          {k: v for k, v in f.items() if k in ('enum_ref', 'min_value', 'max_value')})
