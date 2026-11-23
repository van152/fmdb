import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]
    while len(recs)<cnt and pos+4<=len(raw):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        strs=[]
        while pos<len(raw):
            b=raw[pos]
            if b==0xFF: pos+=1; continue
            if b==0x00 and pos+3<=len(raw):
                # trailer: 00 + u16
                tail=struct.unpack_from('<H',raw,pos+1)[0] if pos+3<=len(raw) else None
                pos+=3; break
            if pos+4>len(raw): break
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>300 or pos+4+L>len(raw): break
            strs.append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,strs))
    return cnt,recs,pos

raw=lib.load_member('lang_update','8_3.dat')
cnt,recs,pos=parse(raw)
print('cnt',cnt,'parsed',len(recs),'end',pos,'len',len(raw))
ids=[r[0] for r in recs]
print('ids sorted?',ids==sorted(ids),'unique',len(set(ids)))
print('first 10',ids[:10])
for r in recs[:3]: print(r[0],[s.decode('utf-8','replace') for s in r[1]])
