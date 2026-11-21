import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
# find 3-letter uppercase ASCII runs in blocks
for i in (139,55,0,189,61):
    b=bytes.fromhex(rows[i]['raw_hex'])
    runs=[(m.start(),m.group().decode()) for m in re.finditer(rb'[A-Z]{3}(?![A-Z])',b)]
    print(f'row{i} len={len(b)} name={rows[i]["marker"]["name_ascii"]!r} 3upper={runs[:8]}')
