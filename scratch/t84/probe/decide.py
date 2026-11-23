import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

print('=== A. nation-name literal scan (unlikely person/club names) ===')
nn=[b'Cura\xc3\xa7ao',b'Liechtenstein',b'Suriname',b'Bhutan',b'Comoros',b'Vanuatu',b'Tahiti']
for a in ('client','server','lang_update'):
    p=lib.DB/f'{a}_db.dat'; ents=lib.CODEC['list_tables'](p,f'{a}_db.dat')
    for e in ents:
        nm=e['path'].split('/')[-1]
        try: raw=lib.load_member(a,nm)
        except Exception: continue
        h={n.decode('utf-8','replace'):raw.count(n) for n in nn if raw.count(n)}
        if h: print(' ',a,nm,h)

print('\n=== B. lang id -> main row join (club, 8_3) ===')
raw3=K['load_payload'](lib.CODEC,'client','3')
def lang_recs(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while len(out)<cnt:
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        while True:
            b=raw[pos]
            if b==0xFF: pos+=1; continue
            if b==0 and raw[pos+1]!=0: pos+=3; break
            L=struct.unpack_from('<I',raw,pos)[0]; f.append(raw[pos+4:pos+4+L]); pos+=4+L
        out.append((uid,f))
    return out
lr=lang_recs(lib.load_member('lang_update','8_3.dat'))
print('lang recs',len(lr),'id range',min(x[0] for x in lr),max(x[0] for x in lr))
hit=miss=0; samples=[]
for uid,f in lr[:400]:
    name=f[0]
    if len(name)<6: continue
    i=raw3.find(name)
    if i<0: miss+=1; continue
    # is uid present as u32 within 40 bytes before name?
    win=raw3[max(0,i-48):i]
    found=any(struct.unpack_from('<I',win,k)[0]==uid for k in range(0,len(win)-3))
    if found: hit+=1; samples.append((uid,name.decode('utf-8','replace')))
    else: miss+=1
print(f'uid within 48B before name: hit={hit} miss={miss} of first-400')
print('samples',samples[:5])
