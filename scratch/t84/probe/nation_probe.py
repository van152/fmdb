import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K

def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return out

P={n:pool(n) for n in (0,1,2)}
names=[b'England',b'France',b'Brazil',b'Wales',b'Scotland',b'China PR',b'Germany',b'Spain',b'Italy']
for n,s in P.items():
    for nm in names:
        hit=[i for i,x in enumerate(s) if x==nm]
        if hit: print(f'pool{n} {nm!r} exact idx {hit[:6]}')
