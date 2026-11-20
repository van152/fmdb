import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return out

P={n:pool(n) for n in (0,1,2)}
# person-name cross-check: do pool strings appear as people names in basic_people_db?
bp=lib.DB/'basic_people_db.dat'
raw=bp.read_bytes()
print('basic_people_db size', len(raw))
import re
# sample 4000 pool0 strings, check substring presence in people db
smp=[P[0][i] for i in range(0,len(P[0]),max(1,len(P[0])//4000))][:4000]
inb=sum(1 for s in smp if s and len(s)>=4 and s in raw)
print(f'pool0 sample {len(smp)}: substring-present in basic_people_db: {inb} ({100*inb/len(smp):.1f}%)')
smp2=[P[2][i] for i in range(0,len(P[2]),max(1,len(P[2])//2000))][:2000]
inb2=sum(1 for s in smp2 if s and len(s)>=4 and s in raw)
print(f'pool2 sample {len(smp2)}: substring-present: {inb2} ({100*inb2/len(smp2):.1f}%)')

# club/comp/nation names as control
ctrl=[b'Atletico',b'Pyunik',b'Liverpool F.C.',b'Arsenal',b'Premier Division',b'Serie A']
print('control (club/comp names) present in people_db:',{c.decode(): (c in raw) for c in ctrl})
