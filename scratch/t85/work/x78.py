import json,sys,collections,struct
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
items=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    for k in range(t[6]): items.append(t[8+27*k:8+27*(k+1)])
print('items',len(items))
# u16 lanes
for off in (1,3,5,7,9,11):
    v=[struct.unpack_from('<H',it,off)[0] for it in items]
    print(f' u16@{off}: distinct={len(set(v))} min={min(v)} max={max(v)} top={collections.Counter(v).most_common(4)}')
# candidate: repeating triples of u16 at 1..10
print()
for it in items[:6]:
    print(' ',it.hex(' '), [struct.unpack_from('<H',it,o)[0] for o in (1,3,5,7,9,11)])
