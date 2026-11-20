import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def langf(raw, nf, tr):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        for _f in range(nf):
            if raw[pos]==0xFF: pos+=1
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L].decode('utf-8')); pos+=4+L
        pos+=tr; recs.append((uid,f))
    return recs,pos

recs,end=langf(lib.load_member('lang_update','8_25.dat'),3,1)
print('8_25 recs',len(recs),'end',end,'target',len(lib.load_member('lang_update','8_25.dat'))-8)
for a in ('client','server'):
    raw=K['load_payload'](lib.CODEC,a,'25')
    hit=0; ex=[]
    for uid,f in recs:
        pat=struct.pack('<I',uid)
        i=raw.find(pat)
        if i<0: continue
        hit+=1
        if len(ex)<6:
            ctx=raw[max(0,i-24):i+80]
            # find the name nearby
            nb=f[1].encode('utf-8')
            ex.append((uid,f[0][:28],f[1][:20],raw.find(nb,max(0,i-200))>=0))
    print(f'{a} table_25: uid hits {hit}/{len(recs)}')
    for e in ex: print('   ',e)
