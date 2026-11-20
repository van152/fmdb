import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return out
P={n:pool(n) for n in (0,1,2)}
def ctx(n,i,k=8):
    print(f'pool{n}[{max(0,i-3)}..{i+k}]', P[n][max(0,i-3):i+k])
for i in (221925,228713,257767,190558,12315,466939,11606,11749,125048,66390):
    ctx(1,i)
