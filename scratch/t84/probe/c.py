import sys, struct, collections, zlib, hashlib
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
P=pool(0); R=idx(0)
# test col3 as crc/hash
tests={
 'crc32&0xffff': lambda s: zlib.crc32(s)&0xffff,
 'len': lambda s: len(s),
 'sum': lambda s: sum(s)&0xffff,
}
for nm,fn in tests.items():
    m=sum(1 for i in range(0,20000) if R[i][3]==fn(P[i]))
    print(f'col3 == {nm}: {m}/20000')
print('col3 values 0..10', [R[i][3] for i in range(10)])
print('col5 values 0..10', [R[i][5] for i in range(10)])
print('col0 values 0..10', [R[i][0] for i in range(10)])
print('col4 values 0..10', [R[i][4] for i in range(10)])
# distribution of col0
print('col0 top', collections.Counter(r[0] for r in R).most_common(5))
