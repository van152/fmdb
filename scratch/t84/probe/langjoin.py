import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]
    while len(recs)<cnt and pos+4<=len(raw):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        groups=[]; cur=[]
        while pos<len(raw):
            b=raw[pos]
            if b==0xFF: pos+=1; break
            if b==0 and raw[pos:pos+3]==b'\x00\x01\x00': pos+=3; break
            if pos+4>len(raw): break
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>300 or pos+4+L>len(raw): break
            cur.append(raw[pos+4:pos+4+L]); pos+=4+L
        groups.append(cur)
        while pos+3<=len(raw) and raw[pos:pos+3]!=b'\x00\x01\x00':
            if raw[pos]==0xFF: pos+=1; continue
            if pos+4>len(raw): break
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>300 or pos+4+L>len(raw): break
            groups.append([raw[pos+4:pos+4+L]]); pos+=4+L
        if raw[pos:pos+3]==b'\x00\x01\x00': pos+=3
        recs.append((uid,groups))
    return cnt,recs,pos

raw=lib.load_member('lang_update','8_3.dat')
cnt,recs,pos=parse(raw)
print('cnt',cnt,'parsed',len(recs),'end',pos,'of',len(raw))
ids=[r[0] for r in recs]
print('ids min/max',min(ids),max(ids),'unique',len(set(ids)),'monotone',ids==sorted(ids))
print('first 12 ids',ids[:12])
print('first rec groups',[[s.decode('utf-8','replace') for s in g] for g in recs[0][1]])
