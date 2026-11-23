import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]
    while len(recs)<cnt:
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        fields=[]; groups=[[]]
        while True:
            if pos>=len(raw): return cnt,recs,pos,'eof'
            # trailer detect: 00 xx 00 then plausible next uid
            if raw[pos]==0 and pos+7<=len(raw) and raw[pos+2]==0:
                nxt=struct.unpack_from('<I',raw,pos+3)[0]
                if pos+7<=len(raw) and nxt<len(raw):
                    pos+=3; break
            if raw[pos]==0xFF:
                groups.append([]); pos+=1; continue
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return cnt,recs,pos,f'badlen@{pos}={L}'
            groups[-1].append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,groups))
    return cnt,recs,pos,'ok'

raw=lib.load_member('lang_update','8_3.dat')
cnt,recs,pos,st=parse(raw)
print('cnt',cnt,'parsed',len(recs),'end',pos,'len',len(raw),'footer8',len(raw)-8,'status',st)
print('last', recs[-1][0] if recs else None)
