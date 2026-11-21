import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t78/out/buckets.json',encoding='utf-8').read())
nat={o['code']:o for o in d['occurrences'] if o['entity']=='nation'}
for c in ('TCnn','TCht','alnm','ntts','Nnam','Nsnm','N3ln','Nnty','dbnm','nhrl','ttcl','tbcl'):
    o=nat.get(c)
    print(f'{c:6s}', o['bucket'] if o else 'ABSENT', '|', (o or {}).get('note'))
print()
print('nation bucket counts:',collections.Counter(o['bucket'] for o in d['occurrences'] if o['entity']=='nation'))
