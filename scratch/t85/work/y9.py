import sys,struct,json
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
# extra_9 row_id (u32 after name)
duni={}
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']
    rid=struct.unpack_from('<I',b,8+nl+len(b[8+nl:8+nl]))[0] if False else None
    # block: [ordinal][name_len][name][?] -> find row_id: it's block tail u32?
    duni[r['row']]=b.hex()
print('row0 len',len(bytes.fromhex(duni[0]))//2)
b=bytes.fromhex(duni[0]); print('row0 hex:',b[:40].hex(' '))
print('row0 last16:',b[-16:].hex(' '))
print('row139 last16:',bytes.fromhex(duni[139])[-16:].hex(' '))
