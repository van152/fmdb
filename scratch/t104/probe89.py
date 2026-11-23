import sys, struct, importlib.util
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    b=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
    N=len(b); n=struct.unpack_from('<I',b,8)[0]
    cands={k:[i for i in range(12,N-3) if struct.unpack_from('<I',b,i)[0]==k] for k in range(n+1)}
    reach=[set() for _ in range(n+1)]; reach[0]={12}
    for k in range(n):
        for s in reach[k]:
            for t in cands[k+1]:
                if t>s: reach[k+1].add(t)
        if not reach[k+1]:
            print(arch,'DP dies at k=',k+1,'from',len(reach[k]),'states; max state',max(reach[k]))
            print('   candidates for',k+1,cands[k+1][:5])
            break
    print(arch,'final reach count',len(reach[n]))
