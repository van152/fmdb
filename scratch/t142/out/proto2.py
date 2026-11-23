import sys, struct, json
sys.path.insert(0,r'D:\tmp2b\fm24-db\scripts'); sys.dont_write_bytecode=True
import t133_fm24_reader_v2 as t133, t112_fm24_reader as base, numpy as np
rec,specs = t133.registry(t133.load(t133.TRACE)); l3=t133.load(t133.L3)

def ids(key):
    s=specs[key]; data=base.Archive(key[0]).payload(key[1])
    n=struct.unpack_from('<I',data,8)[0]
    ords=[];uids=[]
    if s.kind=='fixed':
        r=base.TableReader(s,l3); r._fixed_setup()
        fmt=r._fixed_fmt; mv=memoryview(data); p=base.HEADER_END
        idx={f[3]:i for i,f in enumerate(r._fixed_fields) if f[3]}
        io,iu=idx['ordinal'],idx['uid']
        for i in range(n):
            v=fmt.unpack_from(mv,p+1); p+=1+fmt.size; ords.append(v[io]); uids.append(v[iu])
    else:
        progs = t133.SELECTORS.get(key, {0:s.prog})
        fasts={k:t133.compile_walk(v) for k,v in progs.items()}
        p=base.HEADER_END
        for i in range(n):
            f=data[p]; body=p+1; q=fasts[f](data,body,len(data)-9)
            o,u,_=struct.unpack_from('<III',data,q-12); ords.append(o);uids.append(u); p=q
    return np.array(ords),np.array(uids)

for tid in (10,3,24,25,5,19,21,2,9,35,41,47,27,6,7,8,18,22,23,56,0):
    o,u=ids(('server',tid))
    print(('server',tid),rec[('server',tid)]['class'],'ord',o.min(),o.max(),len(np.unique(o)),'uid',u.min(),u.max(),len(np.unique(u)),'dense_uid' , len(np.unique(u))/(u.max()-u.min()+1))
o,u=ids(('server',10))
print('NATION first 8 (ord,uid):',list(zip(o[:8],u[:8])))
o3,u3=ids(('server',3))
print('CLUB first 5 (ord,uid):',list(zip(o3[:5],u3[:5])))
