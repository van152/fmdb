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
def rows(n):
    raw=lib.load_member('client',f'name_table_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]
    return [struct.unpack_from('<6H',raw,12+12*i) for i in range(cnt)]
for n in (0,1,2):
    P=pool(n); R=rows(n)
    ok=sum(1 for i,r in enumerate(R) if (r[1] | (r[2]<<16))==i)
    print(f'=== pool {n} n={len(R)} index=col1|col2<<16 matches {ok}/{len(R)}')
    print('   last row', R[-1], 'expect idx', len(R)-1)
    # col3 and col5 vs string
    print('   col3 vs strlen equal count', sum(1 for i,r in enumerate(R) if r[3]==len(P[i])))
    print('   col0 top', collections.Counter(r[0] for r in R).most_common(3))
    print('   col4 top', collections.Counter(r[4] for r in R).most_common(4))
    print('   col3 sample', [(len(P[i]),R[i][3],P[i]) for i in range(0,6)])
