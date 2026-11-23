import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
# For 8_25: after uid 0x1fbea (130026), first len 0x17 'Clearer Water Irish Cup'
# structure: uid, then FF-separated fields? Try: uid, then (FF? len str)*, then trailer 00 + u16
def parse(raw, mode):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        if pos+4>len(raw): return recs,pos,f'eof uid @{pos}'
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        f=[]
        while True:
            if pos>=len(raw): return recs,pos,'eof'
            if raw[pos]==0xFF: pos+=1; continue
            if raw[pos]==0x00:
                if mode=='a' and pos+3<=len(raw): pos+=3; break
                if mode=='b' and pos+1<len(raw) and raw[pos+1]!=0: pos+=3; break
            if pos+4>len(raw): return recs,pos,'eof len'
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return recs,pos,f'bad {L}@{pos}'
            f.append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,f))
    return recs,pos,'ok'
for nm in ('8_25.dat','8_0.dat','8_2.dat','8_21.dat'):
    raw=lib.load_member('lang_update',nm)
    for mode in ('a','b'):
        r,p,st=parse(raw,mode)
        print(f'{nm:10s} mode={mode} recs={len(r):4d} end={p:6d} target={len(raw)-8:6d} {st}')
    if nm=='8_25.dat':
        r,p,st=parse(raw,'b')
        for x in r[:4]: print('   ',x[0],[s.decode('utf-8','replace') for s in x[1]])
