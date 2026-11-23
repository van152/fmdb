import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def try_k(raw,k):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
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
        recs.append((uid,strs))
    return recs,pos

raw=lib.load_member('lang_update','8_3.dat')
r=try_k(raw,6)
print('k=6 end',r[1],'len-8',len(raw)-8,'diff',len(raw)-8-r[1])
print('tail after',raw[r[1]:r[1]+16].hex(' '))
print('last8',raw[-8:].hex(' '))
