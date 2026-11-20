import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def pool(a,n):
    raw=lib.load_member(a,f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    assert pos==len(raw) and len(out)==cnt
    return out

# client vs server pool identity
for n in (0,1,2):
    c=pool('client',n); s=pool('server',n)
    print(f'pool{n} client==server: {c==s} (n={len(c)})')

# pool0 + ' ' + pool1 composition over pool2 (full)
P0={x for x in pool('client',0)}; P1={x for x in pool('client',1)}; P2=pool('client',2)
g=s=both=other=0
for x in P2:
    parts=x.split(b' ')
    if len(parts)==2:
        if parts[0] in P0 and parts[1] in P1: both+=1
        elif parts[0] in P0: g+=1
        elif parts[1] in P1: s+=1
        else: other+=1
    else:
        other+=1
tot=len(P2)
print(f'pool2 n={tot}: given+surname both={both} ({100*both/tot:.1f}%) given-only={g} surname-only={s} neither/multi={other}')
