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
print('--- pool semantics: space share / token counts ---')
for n,v in P.items():
    sp=100*sum(1 for x in v if b' ' in x)/len(v)
    tk=collections.Counter(min(4,len(x.split())) for x in v)
    print(f'pool{n} n={len(v):7d} space={sp:5.1f}% tokens={dict(sorted(tk.items()))}')
print('  pool2 exact == pool0[i]+" "+pool1[j] pairs found:',
      sum(1 for x in P[2][:20000] if b' ' in x and x.split(b' ',1)[0] in set(P[0])))
print('--- nation/comp/club name exact membership in pools ---')
for nm in (b'England',b'Brazil',b'Wales',b'Denmark',b'Liverpool',b'Arsenal',b'Serie A',b'Premier Division'):
    print(f'  {nm.decode():18s}', {n:(nm in set(v)) for n,v in P.items()})
