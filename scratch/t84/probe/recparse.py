import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw):
    """u32 count@8; records: u32 uid, then groups (u32 len, utf8) separated by 0xFF,
       terminated by 0x00 0x01 0x00."""
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]; err=None
    while len(recs)<cnt:
        if pos+4>len(raw): err=('eof',pos); break
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        groups=[]; cur=[]
        while pos<len(raw):
            b=raw[pos]
            if b==0xFF: pos+=1; break
            if b==0x00 and raw[pos:pos+3]==b'\x00\x01\x00': pos+=3; break
            if pos+4>len(raw): break
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>300 or pos+4+L>len(raw): break
            cur.append(raw[pos+4:pos+4+L]); pos+=4+L
        groups.append(cur)
        # continuation groups: (u32 len,str) separated by FF until 00 01 00
        while not (raw[pos-3:pos]==b'\x00\x01\x00'):
            if pos>=len(raw): break
            if raw[pos]==0xFF: pos+=1
            if pos+4>len(raw): break
            if raw[pos:pos+3]==b'\x00\x01\x00': pos+=3; break
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>300 or pos+4+L>len(raw): break
            groups.append([raw[pos+4:pos+4+L]]); pos+=4+L
        recs.append((uid,groups))
    return cnt,recs,pos,err

raw=lib.load_member('lang_update','8_3.dat')
cnt,recs,pos,err=parse(raw)
print('hdr cnt',cnt,'parsed',len(recs),'end',pos,'len',len(raw),'err',err)
for r in recs[:4]:
    print(r[0], [ [s.decode('utf-8','replace') for s in g] for g in r[1] ])
