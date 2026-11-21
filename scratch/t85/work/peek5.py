import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
f=L('scratch/t72/out/fingerprints.json')
n=f['tables']['nation']['slots']
for s in n:
    if s['position'] in (2,3,4,11,12,13,23,24,25,26):
        print('pos',s['position'],'type',s['slot_type'],'named',s['named_fields'])
        for a in ('client','server'):
            d=s[a]
            print('  ',a,'rows',d.get('rows'),'bytes',d.get('bytes'),'w',d.get('width_histogram'),'distinct',d.get('distinct'))
            print('    extra keys',[k for k in d if k not in ('rows','bytes','width_histogram','fixed_width','first','last','distinct','all_zero','zero_count','zero_ratio','all_ones_count','all_ones_ratio','interpretations','u32_max','value_histogram','fk_probe_applies','fk_skipped','xref_hint')])
        print('    other',[k for k in s if k not in ('position','key','kind','named_fields','grade_raw','slot_type','client','server')])
