import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def tryk(raw, nf, tr):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        if pos+4>len(raw): return None
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        for _f in range(nf):
            if pos<len(raw) and raw[pos]==0xFF: pos+=1
            if pos+4>len(raw): return None
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return None
            try: f.append(raw[pos+4:pos+4+L].decode('utf-8'))
            except Exception: return None
            pos+=4+L
        pos+=tr
        if pos>len(raw): return None
        recs.append((uid,f))
    return recs,pos

for nm in ('8_3.dat','8_25.dat','8_0.dat','8_2.dat','8_21.dat','8_18.dat','8_7.dat','8_9.dat','8_6.dat','10_25.dat','10_0.dat','15_0.dat'):
    try: raw=lib.load_member('lang_update',nm)
    except Exception: continue
    tgt=len(raw)-8
    best=[]
    for nf in range(1,13):
        for tr in range(0,5):
            r=tryk(raw,nf,tr)
            if r: best.append((abs(r[1]-tgt), nf, tr, len(r[0]), r[1]))
    best.sort()
    print(f'{nm:10s} len={len(raw):7d} tgt={tgt:7d} best={best[:3]}')
