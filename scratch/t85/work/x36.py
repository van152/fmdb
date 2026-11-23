import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t72/out/fingerprints.json',encoding='utf-8').read())
s=d['tables']['nation']['slots']
print('n',len(s))
print('positions in list order:',[x['position'] for x in s])
