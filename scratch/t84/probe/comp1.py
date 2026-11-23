import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lang_uid_fields(raw, nf):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        if pos+4>len(raw): break
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        okk=True
        for _f in range(nf):
            if pos<len(raw) and raw[pos]==0xFF: pos+=1
            if pos+4>len(raw): okk=False; break
            L=struct.unpack_from('<I',raw,pos)[0]
            if L>400 or pos+4+L>len(raw): okk=False; break
            try: f.append(raw[pos+4:pos+4+L].decode('utf-8'))
            except Exception: okk=False; break
            pos+=4+L
        if not okk: break
        pos+=3
        recs.append((uid,f))
    return recs,pos

raw=lib.load_member('lang_update','8_25.dat')
recs,end=lang_uid_fields(raw,3)
print(f'8_25: recs={len(recs)} cnt_hdr={struct.unpack_from("<I",raw,8)[0]} end={end} target={len(raw)-8}')
for r in recs[:6]: print('  ',r[0],r[1])

# comp table_25 client: header 13, row 127
c25=K['load_payload'](lib.CODEC,'client','25')
print('\ncomp table_25 client len',len(c25),'cnt',struct.unpack_from('<I',c25,9)[0])
for i in range(3):
    b=c25[13+i*127:13+(i+1)*127]
    print(' row',i,'head',b[:16].hex(' '))
