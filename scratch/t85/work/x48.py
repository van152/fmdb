import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
pat=bytes.fromhex('ffffffffffffffff')
for rid in (0,3):
    r=rows[rid]; b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    print(f'== row{rid} name={r["marker"]["name_ascii"]!r} len={len(b)}')
    print('  tail head',t[:12].hex(' '),'tail len',len(t))
    # walk: u32 X, u8 count?, then items of 27
    print('  bytes 0..12:',[t[i] for i in range(12)])
    print('  at +5:',t[5],'at +6:',t[6],'at +7:',t[7])
    # right after: 8 bytes then items
    print('  first 3 items:')
    for k in range(3):
        s=8+k*27
        print(f'   item{k} @{s}: {t[s:s+27].hex(" ")}')
