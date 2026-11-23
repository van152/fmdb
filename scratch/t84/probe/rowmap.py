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
    col1=[r[1] for r in R]
    print(f'=== pool {n}: strings={len(P)} rows={len(R)}')
    print('   col1 unique', len(set(col1))==len(col1), 'min', min(col1), 'max', max(col1))
    # find where col1 stops equalling i
    brk=next((i for i,r in enumerate(R) if r[1]!=i), None)
    print('   first break col1!=i at', brk)
    print('   rows 0..3', R[:4])
    print('   around break', R[max(0,(brk or 0)-2):(brk or 0)+4])
    # does col1 permute onto 0..count-1?
    s=sorted(col1)
    print('   col1 sorted==range?', s==list(range(len(R))))
    # check col2 distinct
    print('   col2 top', collections.Counter(r[2] for r in R).most_common(4))
    print('   col3 range', min(r[3] for r in R), max(r[3] for r in R))
