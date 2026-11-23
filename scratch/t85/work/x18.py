import json,sys
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
for arch,size in (('client',83927),('server',105228)):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    t9=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_9.rows.jsonl',encoding='utf-8')]
    print('==',arch)
    for i in (0,55,139,250):
        r=rows[i]; b=bytes.fromhex(r['raw_hex'])
        print(f'  row{i} len={r["len"]} ord={r["marker"]["ordinal"]} name_len={r["marker"]["name_len"]} name={r["marker"]["name_ascii"]!r} t9_row_id={t9[i]["identity"]["row_id"]}')
    # count named
    named=sum(1 for r in rows if r['marker']['name_len']>0)
    print('  named blocks',named,'/251')
