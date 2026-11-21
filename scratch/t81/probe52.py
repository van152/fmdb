import importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid,S in ((23,14),(35,15)):
    raw=m.load_payload('client',tid); n=m.u32(raw,8)
    u=[m.u32(raw,14+j*S+S-13+4) for j in range(n)]
    runs=[]; start=0
    for j in range(1,n+1):
        if j==n or u[j]-u[j-1]!=1:
            runs.append((start,j-1,u[start],u[j-1])); start=j
    print(f't{tid} n={n} runs={len(runs)}')
    for r in runs[:12]: print('   rows',r[0],'-',r[1],'uid',r[2],'-',r[3],'len',r[1]-r[0]+1)
    print('   big(>=1e9):',[(j,u[j]) for j in range(n) if u[j]>=10**9])
