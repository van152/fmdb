import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t78/out/buckets.json',encoding='utf-8').read())
occ=d['occurrences']
nat=[o for o in occ if o['entity']=='nation']
print(collections.Counter(o['bucket'] for o in nat))
for b in ('string_name_table','unresolved_wire_slot','held'):
    print('=====',b)
    for o in nat:
        if o['bucket']==b: print('  ',o['code'],o['id'],'|',o.get('note'))
