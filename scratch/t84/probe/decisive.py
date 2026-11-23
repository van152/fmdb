import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lang6(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        f=[]
        for _f in range(6):
            if raw[pos]==0xFF: pos+=1
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L]); pos+=4+L
        pos+=3
        out.append((uid,f))
    return out,pos

raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))

def row_strings(body):
    """yield (rel_off, u32len, bytes) for plausible length-prefixed utf8."""
    out=[]
    for p in range(0,len(body)-4):
        L=struct.unpack_from('<I',body,p)[0]
        if 2<=L<=120 and p+4+L<=len(body):
            seg=body[p+4:p+4+L]
            try: s=seg.decode('utf-8')
            except Exception: continue
            if s and all(31<ord(c)<0x2100 for c in s) and any(c.isalpha() for c in s):
                out.append((p,L,seg))
    return out

recs,end=lang6(lib.load_member('lang_update','8_3.dat'))
print('lang 8_3 recs',len(recs),'closure end',end,'of',282975)

# index clubs by exact full-name string
idx={}
for i,off,body in rows:
    for p,L,seg in row_strings(body):
        idx.setdefault(seg,[]).append((i,off,p,body))
        break  # first string = full name

hit=0; miss=0; ex=[]
for uid,f in recs:
    nm=f[0]
    if nm not in idx: miss+=1; continue
    i,off,p,body=idx[nm][0]
    u32s={struct.unpack_from('<I',body,k)[0] for k in range(0,len(body)-3,4)}
    ok = uid in u32s
    if ok: hit+=1
    else: miss+=1
    if len(ex)<8: ex.append((uid,nm.decode('utf-8','replace'),i,ok))
print(f'lang uid in club row u32 set: hit={hit} miss={miss}')
for e in ex: print('  ',e)
