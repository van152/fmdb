import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lang1(raw):
    """uid u32; fields: [FF] (u32len utf8)*; trailer = single 0x00 byte."""
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        if pos+4>len(raw): return recs,pos,'eof uid'
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        f=[]
        while True:
            if pos>=len(raw): return recs,pos,'eof'
            if raw[pos]==0xFF: pos+=1; continue
            if raw[pos]==0x00: pos+=1; break
            if pos+4>len(raw): return recs,pos,'eof len'
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return recs,pos,f'bad {L}@{pos}'
            f.append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,f))
    return recs,pos,'ok'

for nm in ('8_3.dat','8_25.dat','8_0.dat','8_2.dat','8_21.dat','8_18.dat','8_6.dat','8_7.dat','8_9.dat'):
    raw=lib.load_member('lang_update',nm)
    r,p,st=lang1(raw)
    print(f'{nm:10s} cnt={struct.unpack_from("<I",raw,8)[0]:5d} recs={len(r):5d} end={p:6d} target={len(raw)-8:6d} {st}')
    if nm in ('8_25.dat','8_0.dat') and r:
        for x in r[:3]: print('    ',x[0],[s.decode('utf-8','replace')[:34] for s in x[1]])
