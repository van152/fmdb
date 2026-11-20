import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct

def test_fixed_mid(arch,tid,n,mid,htrue=14):
    raw=load(arch,tid); end=len(raw)-8
    pos=htrue; rows=[]
    for i in range(n):
        nl=struct.unpack_from('<I',raw,pos)[0]
        s=pos; e=s+4+nl+mid+13
        rows.append((s,e,nl,raw[s+4:s+4+nl]))
        pos=e
    return pos==end, rows, len(raw)

ok,rows,pl = test_fixed_mid('client',27,334,95)
print('t27 client fixed-mid 95 →', ok, 'payload',pl)
ok2,rows2,pl2 = test_fixed_mid('server',27,334,95)
print('t27 server fixed-mid 95 →', ok2, 'payload',pl2)
if ok:
    print(' first 3:',[(e-s,nm) for s,e,nl,nm in rows[:3]])
    print(' last:',[(e-s,nm) for s,e,nl,nm in rows[-2:]])
    print(' rowlens hist:')
    import collections
    print('  ', sorted(collections.Counter(e-s for s,e,nl,nm in rows).items()))
    print(' namelen min/max', min(nl for _,_,nl,_ in rows), max(nl for _,_,nl,_ in rows))
    # ordinal lane
    ords=[struct.unpack_from('<I',raw,e-13)[0] for s,e,nl,nm in rows]
    uids=[struct.unpack_from('<I',raw,e-9)[0] for s,e,nl,nm in rows]
    uids2=[struct.unpack_from('<I',raw,e-5)[0] for s,e,nl,nm in rows]
    print(' ordinals 0..n-1?', ords==list(range(334)))
    print(' uid==uid2 all?', all(a==b for a,b in zip(uids,uids2)))
    print(' uid strictly increasing?', all(uids[i]<uids[i+1] for i in range(len(uids)-1)))
    print(' markers all 0?', all(raw[e-1]==0 for s,e,nl,nm in rows))
    print(' first 6 ords/uids', list(zip(ords,uids))[:6])
ok3,rows3,_=test_fixed_mid('client',8,126,17)
print('t8 client fixed-mid 17 →', ok3)
