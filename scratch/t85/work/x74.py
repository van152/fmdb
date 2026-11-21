import json,sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
# server t10 row walk (A/B/C/D) + server extra_9 n_items
raw=C.payload('server','server_db/table_10.dat',422345)
offs=C.identity_offsets(raw); starts=[14]+[o+13 for o in offs[:-1]]; lens=[o+13-s for o,s in zip(offs,starts)]
print('server t10 rows',len(offs))
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_server_extra_9.rows.jsonl',encoding='utf-8')]
nitem=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    nitem.append(t[6] if len(t)>6 else None)
print('server extra9 n_items sum',sum(x for x in nitem if x))
print('first 10 n_items',nitem[:10])
# compare with the i16/i32 counts at the documented t10 object displacements
disp={2:0x128,3:0x158,4:0x170,11:0x60,12:0xd8,13:0x78,23:0x48,24:0xa8,25:0x90,26:0xc0}
for slot,d in sorted(disp.items()):
    vals=[]
    for s,l in zip(starts,lens):
        b=raw[s:s+l]
        off=min(d,len(b)-1)
        vals.append(b[off])
    same=sum(1 for i in range(251) if vals[i]==nitem[i])
    print(f'  slot_{slot} disp={d:#x} byte-at-disp vs n_items: {same}/251')
