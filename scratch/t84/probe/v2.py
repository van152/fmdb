import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def pool(a,n):
    raw=lib.load_member(a,f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return out

P0=pool('client',0); P1=pool('client',1); P2=pool('client',2)
print('pool0 sample', [ascii(x) for x in P0[:8]])
print('pool1 sample', [ascii(x) for x in P1[:8]])
print('pool2 sample', [ascii(x) for x in P2[:5]])
# Does pool2[i] == pool0[a]+' '+pool1[b] for any? check first 2000 pool2 strings as combos
set0=set(P0); set1=set(P1)
combo=sum(1 for x in P2[:3000] if b' ' in x and x.split(b' ',1)[0] in set0)
print(f'pool2 first-token found in pool0: {combo}/3000')
combo2=sum(1 for x in P2[:3000] if b' ' in x and x.rsplit(b' ',1)[-1] in set1)
print(f'pool2 last-token found in pool1: {combo2}/3000')
# cross: club names in pools?
for nm in (b'Liverpool',b'Arsenal',b'Celtic',b'Rangers'):
    print(nm, 'pool0',nm in set0,'pool1',nm in set1,'pool2',nm in set(P2))
