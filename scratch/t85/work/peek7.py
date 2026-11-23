import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
d=L('reports/club_nation_subtable_schema.json')
print('root keys:')
for k in d: print('  ',k, type(d[k]).__name__, len(d[k]) if hasattr(d[k],'__len__') else '')
