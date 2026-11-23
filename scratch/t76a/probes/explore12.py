import json
s = json.load(open('evidence/fm24/reports/editor_schema/master.json'))
print('meta', json.dumps(s['meta'])[:800])
print('\nformat_sections type', type(s['format_sections']), len(s['format_sections']))
print(json.dumps(s['format_sections'], indent=1)[:1500])
print('\n=== entity keys stadium ===', json.dumps({k: (v if k != 'fields' else '...') for k, v in s['entities']['stadium.xml'][0].items()})[:1200])
