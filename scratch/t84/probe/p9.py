import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def try_k(raw, k, trailer=3):
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]
    for _ in range(cnt):
        if pos+4>len(raw): return None
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        strs=[]
        for _f in range(k):
            if pos<len(raw) and raw[pos]==0xFF: pos+=1
            if pos+4>len(raw): return None
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return None
            try: raw[pos+4:pos+4+L].decode('utf-8')
            except Exception: return None
            strs.append(raw[pos+4:pos+4+L]); pos+=4+L
        pos+=trailer
        if pos>len(raw): return None
        recs.append((uid,strs))
    return recs,pos

for nm in ('8_3.dat','8_25.dat','8_0.dat','8_2.dat','8_6.dat','8_7.dat','8_9.dat','8_18.dat','8_21.dat','8person_names.dat','10_25.dat','15_0.dat'):
    raw=lib.load_member('lang_update',nm)
    cnt=struct.unpack_from('<I',raw,8)[0]
    good=[]
    for k in range(1,13):
        for tr in (0,1,2,3,4,8):
            r=try_k(raw,k,tr)
            if r and r[1]==len(raw)-8: good.append((k,tr,len(r[0])))
    print(f'{nm:22s} len={len(raw):7d} cnt={cnt:6d} closures={good}')
