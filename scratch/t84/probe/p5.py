import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw, cnt):
    """uid u32; groups separated by 0xFF; each group = run of (u32 len, utf8);
       record trailer = u8 0x00 then u16 (flags); next record starts after."""
    pos=12; recs=[]
    while len(recs)<cnt:
        if pos+4>len(raw): return recs,pos,'eof_uid'
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        groups=[[]]
        while True:
            if pos>=len(raw): return recs,pos,'eof_body'
            b=raw[pos]
            if b==0xFF: groups.append([]); pos+=1; continue
            if b==0x00 and pos+3<=len(raw):
                # trailer candidate: 00 <u16> ; verify next u32 as uid-ish
                if pos+7<=len(raw):
                    pos+=3; break
            if pos+4>len(raw): return recs,pos,'eof_len'
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): return recs,pos,f'badlen {L} @{pos}'
            groups[-1].append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,groups))
    return recs,pos,'ok'

raw=lib.load_member('lang_update','8_3.dat')
cnt=struct.unpack_from('<I',raw,8)[0]
recs,pos,st=parse(raw,cnt)
print('cnt',cnt,'parsed',len(recs),'end',pos,'footer_start',len(raw)-8,'status',st)
ids=[r[0] for r in recs]
print('ids sorted?',ids==sorted(ids),'unique',len(set(ids)),'min',min(ids),'max',max(ids))
print('id sample',ids[:15])
print('groups per rec', sorted({len(r[1]) for r in recs}))
