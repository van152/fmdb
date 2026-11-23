import sys, struct, importlib.util, io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='backslashreplace')
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    b=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
    N=len(b); n=struct.unpack_from('<I',b,8)[0]
    cands={k:[i for i in range(12,N-3) if struct.unpack_from('<I',b,i)[0]==k] for k in range(n)}
    reach=[set() for _ in range(n)]; parent=[{} for _ in range(n)]
    reach[0]={12}
    for k in range(n-1):
        for s in reach[k]:
            for t in cands[k+1]:
                if t>s:
                    reach[k+1].add(t); parent[k+1].setdefault(t,s)
    print(arch,'N',N,'n',n,'reach@last',len(reach[n-1]),'footer',[N-e for e in reach[n-1]])
    e=min(reach[n-1])
    chain=[0]*n; cur=e
    for k in range(n-1,0,-1):
        chain[k]=cur; cur=parent[k][cur]
    chain[0]=12
    lens=[chain[i+1]-chain[i] for i in range(n-1)]
    print('  starts',chain[:6],'len min/max',min(lens),max(lens))
    for i in range(5):
        r=b[chain[i]:chain[i+1]]
        o,nl=struct.unpack_from('<II',r,0)
        nm=r[8:8+nl].decode('utf-8','replace') if nl<200 else '<bad>'
        print('   rec%d @%d len%d ord%d nl%d %r'%(i,chain[i],len(r),o,nl,nm))
