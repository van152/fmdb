import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l].decode('utf-8','replace')); pos+=8+l
    return out
P={n:pool(n) for n in (0,1,2)}

print('=== A. Pool = person names (neighbour context of club-name collisions) ===')
for n in (0,1,2):
    for probe in ('England','Liverpool','Brazil','Denmark'):
        if probe in P[n]:
            i=P[n].index(probe)
            print(f'  pool{n}[{i}]={probe!r} neighbours={P[n][max(0,i-2):i+3]}')

print('\n=== B. Do pool strings look like person tokens? (single-token share) ===')
for n in (0,1,2):
    s=100*sum(1 for x in P[n] if ' ' not in x)/len(P[n])
    print(f'  pool{n}: single-token {s:.1f}%  n={len(P[n])}')

print('\n=== C. comp/nation names: present in table_25 / table_10 raw? ===')
for a,t in (('client','25'),('client','10')):
    raw=K['load_payload'](lib.CODEC,a,t)
    printable=sum(1 for b in raw if 32<=b<127)/len(raw)
    print(f'  {a} table_{t}: printable-byte share {100*printable:.1f}%  "Premier"={raw.find(b"Premier")} "England"={raw.find(b"England")}')
