import json
d=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
ents=d['entities']
for key in ('media source.xml','derby.xml','weather.xml','language.xml','agreement.xml','award.xml'):
    e=ents[key]
    fl = e.get('fields') if isinstance(e,dict) else None
    print('==',key, list(e)[:8] if isinstance(e,dict) else type(e))
    if isinstance(fl,list):
        print('  fields n=',len(fl))
        for f in fl[:40]:
            print('   ',f if not isinstance(f,dict) else (f.get('name'),f.get('type')))
