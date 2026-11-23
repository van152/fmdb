import importlib.util,json,collections,struct
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
raw=m.load_payload('server',6); n=115; S=40; nb=27
rows=[raw[14+j*S:14+j*S+nb] for j in range(n)]
# bitmask validity helper for Icau powers
pow2={1,2,4,8,16,32,64,128,256,512,1024,2048,4096}
def isbm(v):
    if v==0: return True
    if v & ~sum(pow2) : return False
    # must be sum of distinct powers: always true for any subset bits
    return (v & 0x1FFF)==v
print('--- u16@18 and u8@18/19 columns')
for label,off,w in (('u8@18',18,1),('u8@19',19,1),('u16@18',18,2),('u16@19',19,2)):
    v=[int.from_bytes(r[off:off+w],'little') for r in rows]
    print(f'  {label}: distinct={len(set(v))} min={min(v)} max={max(v)} vals={sorted(set(v))[:14]}')
print('--- Icau bitmask test per offset')
for off,w in [(2,1),(9,1),(10,1),(11,1),(20,1),(22,1),(19,2),(18,2),(18,1),(24,1),(7,1),(12,1)]:
    v=[int.from_bytes(r[off:off+w],'little') for r in rows]
    ok=sum(1 for x in v if isbm(x))
    print(f'  off{off} w{w}: bitmask_valid={ok}/{n} distinct={len(set(v))}')
print('--- off0==13 rows')
r13=[j for j,r in enumerate(rows) if r[0]==13]
print('  count',len(r13),'their iscl:',[rows[j][1] for j in r13])
print('--- off0/off1 pair count', len({(r[0],r[1]) for r in rows}))
