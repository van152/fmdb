import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse_v(raw, trailer_mode):
    """record: uid:u32 ; fields: [FF] (u32len bytes)* ; end when trailer_mode detects."""
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    for _ in range(cnt):
        if pos+4>len(raw): return out,pos,'eof'
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        f=[]
        while True:
            if pos>=len(raw): return out,pos,'eof_body'
            b=raw[pos]
            if b==0xFF: pos+=1; continue
            if b==0x00:
                if trailer_mode=='nz2' and pos+1<len(raw) and raw[pos+1]!=0: pos+=3; break
                if trailer_mode=='nz3' and pos+3<=len(raw) and raw[pos+2]!=0: pos+=3; break
                if trailer_mode=='nz1' and pos+1<len(raw) and raw[pos+1]>0x01: pos+=3; break
            if pos+4>len(raw): return out,pos,'eof_len'
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return out,pos,f'badlen {L}@{pos}'
            try: raw[pos+4:pos+4+L].decode('utf-8')
            except Exception: return out,pos,f'badutf8@{pos}'
            f.append(raw[pos+4:pos+4+L]); pos+=4+L
        out.append((uid,f))
    return out,pos,'ok'

for nm in ('8_25.dat','8_0.dat','8_3.dat','8_21.dat','8_18.dat','8_10.dat','8_2.dat'):
    try: raw=lib.load_member('lang_update',nm)
    except Exception: continue
    print(f'== {nm} len={len(raw)} cnt@8={struct.unpack_from("<I",raw,8)[0]}')
    for mode in ('nz2','nz3','nz1'):
        r,p,st=parse_v(raw,mode)
        print(f'   {mode}: recs={len(r)} end={p} target={len(raw)-8} {st}')
