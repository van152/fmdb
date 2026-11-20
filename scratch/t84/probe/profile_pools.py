import sys, struct, collections, statistics
sys.path.insert(0,'scratch/t84/probe')
import lib

def pool(n):
    raw=lib.load_member('client',f'name_table_extra_{n}.dat')
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    while pos+8<=len(raw):
        i,l=struct.unpack_from('<II',raw,pos); out.append(raw[pos+8:pos+8+l]); pos+=8+l
    return out

P={n:pool(n) for n in (0,1,2)}
probes=[b'Liverpool',b'Arsenal',b'Chelsea',b'Everton',b'Barcelona',b'Milan',b'England',b'Brazil',b'France',
        b'Sabri',b'Smith',b'Jones',b'Patos',b'Albpetrol',b'Premier',b'Division',b'League',b'Cup']
for n,s in P.items():
    print(f'== pool {n} n={len(s)}')
    lens=[len(x) for x in s]
    print('   len mean %.1f max %d' % (statistics.mean(lens), max(lens)))
    print('   with space %.1f%%' % (100*sum(1 for x in s if b" " in x)/len(s)))
    print('   empty', sum(1 for x in s if not x))
    for p in probes:
        hits=[i for i,x in enumerate(s) if x==p]
        hitsub=[i for i,x in enumerate(s) if p in x]
        if hits or hitsub:
            print(f'   {p!r} exact={hits[:4]} substr={len(hitsub)} first={hitsub[:4]}')
    print('   sample idx 100-107', s[100:108])
    print('   sample idx 5000-5004', s[5000:5005])
