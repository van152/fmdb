import json
s = json.load(open('evidence/fm24/reports/editor_schema/master.json'))
E = s['enums']
for k in ('ubnt', 'Soty', 'Spty', 'Sdtr', 'Sste', 'Senv', 'Sdcy', 'Sscl'):
    v = E.get(k)
    print('---', k, '->', json.dumps(v)[:500] if v is not None else 'MISSING')
print('\n=== all enum keys containing "stadium"/"pitch"/"owner" ===')
for k in E:
    j = json.dumps(E[k]).lower()
    if 'stadium' in j or 'pitch' in j or 'owner type' in j:
        print(' ', k, json.dumps(E[k])[:200])
