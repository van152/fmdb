import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def langf(raw,nf,tr):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        for _f in range(nf):
            if raw[pos]==0xFF: pos+=1
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L].decode('utf-8')); pos+=4+L
        pos+=tr; recs.append((uid,f))
    return recs

# comp: 8_25 gives uid -> 3 names. Do those names appear ANYWHERE in archives?
recs=langf(lib.load_member('lang_update','8_25.dat'),3,1)
found={}
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'; ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    for e in ents:
        mn=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,mn)
        except Exception: continue
        for uid,f in recs:
            for s in f:
                if s and s.encode('utf-8') in raw:
                    found.setdefault(uid,set()).add(f'{a}/{mn}')
print('comp 8_25 names located:')
for uid in [r[0] for r in recs[:10]]:
    print(f'  {uid}: {sorted(found.get(uid,[]))}')
