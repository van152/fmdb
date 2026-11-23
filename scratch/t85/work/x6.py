import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t50/out/profile_t9.json',encoding='utf-8').read())
for k in ('client/table_extra_9.dat','server/table_extra_9.dat'):
    m=d['members'][k]
    print('==',k,list(m.keys()))
    cl=m['closure']
    print(' starts first 6',[x for x in cl.items() if 'block_start' in x][:6])
    print(' keys',list(cl.keys()))
