import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_server_extra_9.rows.jsonl',encoding='utf-8')]
for i in (0,1,2,3,55,139):
    r=rows[i]; b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']
    print(f'row{i} len={len(b)} name_len={nl}')
    print('  prefix', b[:8].hex(' '))
    print('  name  ', b[8:8+nl])
    print('  after ', b[8+nl:8+nl+40].hex(' '))
    print('  tail20', b[-20:].hex(' '))
