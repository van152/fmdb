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
for n in (1,2):
    P=pool(n); R=rows(n)
    print(f'=== pool {n} n={len(P)}')
    for i in (0,1,2,3,12315,221925,466939,100,500):
        print(ascii(P[i]), len(P[i]), R[i])
    print('  col1==i sampled', sum(1 for i in range(0,len(P),997) if R[i][1]==i), len(range(0,len(P),997)))
    print('  col3==len sampled', sum(1 for i in range(0,len(P),997) if R[i][3]==len(P[i])), len(range(0,len(P),997)))
    print('  col0 top', collections.Counter(R[i][0] for i in range(0,len(P),97)).most_common(3))
    print('  col4 top', collections.Counter(R[i][4] for i in range(0,len(P),97)).most_common(4))
