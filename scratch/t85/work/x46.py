import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
b=bytes.fromhex(rows[0]['raw_hex']); nl=rows[0]['marker']['name_len']
tail=b[8+nl:]
idx=[20,47,74,101,128,155,182,209]
print('item start (idx-19):',[i-19 for i in idx])
for i in range(len(idx)):
    s=idx[i]-19
    print(f'item{i} at tail+{s}: {tail[s:s+27].hex(" ")}')
print()
# column-wise stability across rows for a row with many items
for rid in (139,55,3):
    r=rows[rid]; bb=bytes.fromhex(r['raw_hex']); nn=r['marker']['name_len']; t=bb[8+nn:]
    ii=[]; p=t.find(bytes.fromhex('ffffffffffffffff'))
    while p>=0: ii.append(p); p=t.find(bytes.fromhex('ffffffffffffffff'),p+1)
    print(f'row{rid} ({r["marker"]["name_ascii"]!r}) n_items={len(ii)} first_item_at={ii[0]-19 if ii else None}')
    if ii: print('   item0',t[ii[0]-19:ii[0]+8].hex(' '))
