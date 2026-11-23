import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse6(raw):
    """uid u32; 6 x (0xFF sep, u32 len, utf8); trailer u8 00 + u16 flags."""
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]
    while len(recs)<cnt:
        if pos+4>len(raw): return recs,pos,'eof_uid'
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        strs=[]
        for k in range(6):
            if pos<len(raw) and raw[pos]==0xFF: pos+=1
            if pos+4>len(raw): return recs,pos,'eof_len'
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return recs,pos,f'badlen {L} @{pos} rec{len(recs)} fld{k}'
            strs.append(raw[pos+4:pos+4+L]); pos+=4+L
        if pos+3>len(raw): return recs,pos,'eof_trailer'
        pos+=3
        recs.append((uid,strs))
    return recs,pos,'ok'

for lang,typ in (('8','3'),('8','25'),('8','0'),('15','3'),('12','0')):
    nm=f'{lang}_{typ}.dat'
    try: raw=lib.load_member('lang_update',nm)
    except Exception: continue
    cnt=struct.unpack_from('<I',raw,8)[0]
    recs,pos,st=parse6(raw)
    print(f'{nm:12s} len={len(raw):7d} cnt={cnt:6d} parsed={len(recs):6d} end={pos:7d} footer={len(raw)-8:7d} {st}')
    if recs:
        print('   ', recs[0][0], [s.decode('utf-8','replace') for s in recs[0][1]])
