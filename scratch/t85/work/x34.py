import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t72/out/fingerprints.json',encoding='utf-8').read())
s=d['tables']['nation']['slots']
for x in s:
    if x['slot_type']!='collection': continue
    for a in ('client','server'):
        dd=x[a]
        fw=dd.get('width_histogram') or {}
        tot=sum(fw.values()) if fw else 0
        print(f"pos{x['position']:3d} {a:6s} rows={dd.get('rows')} tot={tot} distinct_widths={len(fw)} sample={list(fw.items())[:5]}")
    print('   named',x['named_fields'],'keys',[k for k in x if k not in ('position','key','kind','named_fields','grade_raw','slot_type','client','server')])
