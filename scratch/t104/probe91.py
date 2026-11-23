import sys, struct, importlib.util
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
out={}
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    b=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
    N=len(b); n=struct.unpack_from('<I',b,8)[0]
    cands={k:[i for i in range(12,N-3) if struct.unpack_from('<I',b,i)[0]==k] for k in range(n)}
    reach=[set() for _ in range(n)]; reach[0]={12}
    for k in range(n-1):
        for s in reach[k]:
            for t in cands[k+1]:
                if t>s: reach[k+1].add(t)
    ends=sorted(reach[n-1])
    print(arch,'N',N,'n',n,'reach@last',len(ends),'footers',[N-e for e in ends][:6])
    e=ends[0]
    # recover chain
    chain=[None]*n; cur=e
    for k in range(n-1,0,-1):
        chain[k]=cur
        prev=[s for s in reach[k-1] if s<cur and cur in cands[k]]
        cur=max(s for s in reach[k-1] if s<cur)
    chain[0]=12
    lens=[chain[i+1]-chain[i] for i in range(n-1)]
    print('  chain ok', all(chain[i]<chain[i+1] for i in range(n-1)), 'len min/max', min(lens), max(lens))
    print('  first 6 starts', chain[:6])
    print('  footer', N-chain[-1])
    out[arch]=(b,chain,N)
import json
for arch,(b,chain,N) in out.items():
    print('==',arch)
    for i in range(5):
        st=chain[i]; en=chain[i+1]
        r=b[st:en]
        o,nl=struct.unpack_from('<II',r,0)
        nm=r[8:8+nl].decode('utf-8','replace')
        print('  rec',i,'@',st,'len',len(r),'ord',o,'namelen',nl,'name',repr(nm))
