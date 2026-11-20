import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw, cnt):
    """uid u32 ; then repeated (0xFF sep)? (u32 len, utf8) ; trailer = 00 + 2 bytes."""
    pos=12; recs=[]
    while len(recs)<cnt:
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        groups=[[]]
        while True:
            if pos>=len(raw): return recs,pos,'eof'
            b=raw[pos]
            if b==0xFF: groups.append([]); pos+=1; continue
            if b==0x00:
                # trailer? next u32 after 3 bytes must be plausible uid
                if pos+7<=len(raw):
                    nxt=struct.unpack_from('<I',raw,pos+3)[0]
                    if nxt<cnt+100000: pos+=3; break
                # else it's a len-0 string
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return recs,pos,f'badlen {L}@{pos}'
            groups[-1].append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,groups))
    return recs,pos,'ok'

raw=lib.load_member('lang_update','8_3.dat')
cnt=struct.unpack_from('<I',raw,8)[0]
recs,pos,st=parse(raw,cnt)
print('cnt',cnt,'parsed',len(recs),'end',pos,'footer',len(raw)-8,'status',st)
print('ids',[r[0] for r in recs[:8]])
for r in recs[:3]: print(r[0],[[s.decode('utf-8','replace') for s in g] for g in r[1]])
