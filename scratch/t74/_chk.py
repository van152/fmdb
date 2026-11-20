import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, hashlib, collections

def fixed(arch,tid,H,stride,F,n):
    raw=load(arch,tid)
    ok_closure = H+n*stride+F==len(raw)
    bad=0; uids=[]
    for i in range(n):
        p=H+i*stride+stride-13
        o,u1,u2=struct.unpack_from('<III',raw,p)
        if not(o==i and u1==u2 and raw[p+12]==0): bad+=1
        uids.append(u1)
    return dict(payload=len(raw),closure=ok_closure,bad=bad,count=n,stride=stride,
                sha=hashlib.sha256(raw).hexdigest(),uid_uniq=len(set(uids)))

for arch in ('client','server'):
    print('56',arch,fixed(arch,56,14,13,8,6))
    print('0 ',arch,fixed(arch,0,14,77,8,3545))
    print('21',arch,fixed(arch,21,14,38 if arch=='client' else 181,8,48413))
