import sys, struct, importlib.util, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
buf={}
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    buf[arch]=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
for arch,b in buf.items():
    N=len(b); n=struct.unpack_from('<I',b,8)[0]
    pos={}
    for k in range(n):
        needle=struct.pack('<I',k)
        lst=[]; i=12
        while True:
            j=b.find(needle,i)
            if j<0 or j+4>N: break
            lst.append(j); i=j+1
        pos[k]=lst
    # DP: valid chain s_0=12, s_k increasing
    dp=[set() for _ in range(n+1)]
    dp[0]={12}
    for k in range(n):
        for s in dp[k]:
            for t in pos.get(k+1,()):
                if t>s: dp[k+1].add(t)
    print(arch,'N',N,'reachable at n:',sorted(dp[n])[:5],'count',len(dp[n]))
    best=sorted(dp[n])
    print('  tail bytes for last', [(N-s) for s in best[:5]])
    # greedy first-5 with forward DP guaranteeing completion
    def can(k,s):
        return any(s in dp[k] for _ in [0])
    chain=[12]
    s=12
    for k in range(1,6):
        for t in sorted(pos[k]):
            if t>s and t in dp[k]:
                chain.append(t); s=t; break
    print('  chain first6',chain)
    print('  samples:')
    for i in range(5):
        st=chain[i]; en=chain[i+1] if i+1<len(chain) else None
        print('   rec',i,'@',st,'len',(en-st) if en else None, b[st:st+16].hex())
