import sys, struct, random
sys.path.insert(0,'scratch/t84/probe'); sys.path.insert(0,'scripts')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
import t84_join as J
K=lib.K
G={"8_3":(6,3),"8_25":(3,1),"8_0":(2,2),"8_2":(1,2),"8_21":(2,3),"8_7":(1,1)}
for st,(nf,tr) in G.items():
    r,_,s=J.lang_records(lib.load_member('lang_update',st),nf,tr)
    print(f'== {st} n={len(r)} closure={s}')
    for x in r[:3]: print('   ',x['uid'],[f[:38] for f in x['fields']])

# comp wrong-uid control
raw25=K['load_payload'](lib.CODEC,'client','25')
recs,_,_=J.lang_records(lib.load_member('lang_update','8_25'),3,1)
random.seed(84); allu=[x['uid'] for x in recs]
t=w=0
for x in recs:
    if struct.pack('<I',x['uid']) in raw25: t+=1
    y=random.choice(allu)
    if y!=x['uid'] and struct.pack('<I',y) in raw25: w+=1
print(f'comp 8_25: uid in table_25 {t}/{len(recs)}  wrong-uid {w}/{len(recs)}')

# nation name hunt across encodings
print('\n== nation name hunt ==')
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'; ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    for e in ents:
        mn=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,mn)
        except Exception: continue
        for nm in (b'Norway',b'Iceland'):
            if nm in raw:
                i=raw.find(nm)
                ctx=raw[max(0,i-20):i+len(nm)+6]
                print(f'  {a}/{mn} {nm.decode()} @{i} ctx={ctx!r}')
