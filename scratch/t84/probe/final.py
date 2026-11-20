import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return out
def idx(n):
    raw=lib.load_member('client',f'name_table_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]
    return [struct.unpack_from('<6H',raw,12+12*i) for i in range(cnt)]

for n in (0,1,2):
    P=pool(n); R=idx(n)
    tok=sum(1 for i in range(0,len(P),max(1,len(P)//5000)) if R[i][4]==len(P[i].split()))
    tot=len(range(0,len(P),max(1,len(P)//5000)))
    print(f'pool{n}: col4==token_count {tok}/{tot}; empty_col4 {sum(1 for r in R if r[4]==0)}')
    print('   col3 sample', [(R[i][3], ascii(P[i])[:18]) for i in range(0,4)])
    print('   col5 sample', [R[i][5] for i in range(0,6)])
    # single token vs multi
    single=sum(1 for x in P[:20000] if b' ' not in x)
    print(f'   single-token share(first 20k) {100*single/20000:.1f}%')
