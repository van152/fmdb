import pickle, struct, numpy as np
from hashlib import sha256
raw=pickle.load(open('scratch/t72/work/raw.pkl','rb'))
b=raw['server',24]; n=struct.unpack_from('<I',b,8)[0]
print('n',n,'len',len(b), '13+9',13+9)
end=len(b)-9
# candidate triples (i,uid,uid) at any offset, uid increasing, selector 10/11
g=[[] for _ in range(n)]
for shift in range(4):
    a=np.frombuffer(b,dtype='<u4',offset=shift,count=(len(b)-shift)//4)
    m=(a[:-2]<n)&(a[1:-1]==a[2:])
    idx=np.flatnonzero(m)
    print('shift',shift,'cands',len(idx))
    for x in idx.tolist():
        at=4*x+shift; i=int(a[x]); uid=int(a[x+1])
        if at+12<=end and b[at+12] in (10,11): g[i].append((at,uid))
print('rows with cands', sum(1 for x in g if x))
