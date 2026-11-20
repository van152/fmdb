import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw3=K['load_payload'](lib.CODEC,'client','3')

def idblock(raw, nameoff):
    """scan backwards for db_id,FFFFFFFF,db_id,db_id"""
    for back in range(4, 60, 1):
        p=nameoff-back
        if p<0: break
        a,b,c,d=struct.unpack_from('<IIII',raw,p)
        if b==0xFFFFFFFF and a==c==d and 0<a<10**7:
            return p,a
    return None,None

for nm in (b'Klubi i Futbollit Albpetrol Patos', b'Atl\xc3\xa9tico Petr\xc3\xb3leos de Luanda', b'Pyunik Yerevan', b'Liverpool'):
    i=raw3.find(nm)
    p,did=idblock(raw3,i)
    print(f'{nm.decode("utf-8","replace")[:34]:34s} name@{i} idblock@{p} db_id={did}')
print()
print('=== length-prefixed exact-name probe ===')
probe=[('nation',b'Norway'),('nation',b'Denmark'),('nation',b'Iceland'),
       ('comp',b'Serie A'),('comp',b'La Liga'),('club',b'Liverpool')]
for a in ('client','server','lang_update'):
    pth=lib.DB/f'{a}_db.dat'; ents=lib.CODEC['list_tables'](pth,f'{a}_db.dat')
    for e in ents:
        mn=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,mn)
        except Exception: continue
        for kind,s in probe:
            pat=struct.pack('<I',len(s))+s
            n=raw.count(pat)
            if n: print(f'  {a:11s} {mn:24s} {kind:6s} {s.decode():8s} LP-hits={n}')
