import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib

def pool(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return cnt,out

def idxrows(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]
    return [struct.unpack_from('<6H',raw,12+12*i) for i in range(cnt)]

for n in (0,1,2):
    ir=idxrows(lib.load_member('client',f'name_table_{n}.dat'))
    cnt,st=pool(lib.load_member('client',f'name_table_extra_{n}.dat'))
    print(f'== pool {n} rows={len(ir)} strings={cnt}')
    for i in range(6):
        print('  ',ir[i], st[i][:20])
    cols=collections.Counter()
    for r in ir: cols[tuple(r[j] for j in (0,2,4))]+=1
    print('   (f0,f2,f4) top:', cols.most_common(6))
    c3=collections.Counter(r[3] for r in ir)
    print('   f3 top:', c3.most_common(5))
    c5=collections.Counter(r[5] for r in ir)
    print('   f5 top:', c5.most_common(5))
