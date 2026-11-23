import runpy, sys, struct, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
own = np.ascontiguousarray(ms[:,16:20]).view('<u4').ravel().astype(np.int64)
# t24 rows and names
raw24 = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n24=len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
def rowname(j):
    b = raw24[starts[j]:starts[j]+lens[j]]
    ss = [m.group().decode('utf-8','replace') for m in re.finditer(rb'[\x20-\x7e]{4,}', b)]
    return ss
# find t24 rows containing club names
targets = ['Manchester United','Liverpool','Arsenal','Aston Villa','Chelsea','Manchester City',
           'Barcelona','Real Madrid','AC Milan','Inter','Bayern','Borussia Dortmund','Celtic',
           'Tottenham','West Ham','Newcastle']
for t in targets:
    pat = t.encode()
    idx = []
    for j in range(0, n24, 1):
        if pat in raw24[starts[j]:starts[j]+lens[j]]:
            idx.append(j)
            if len(idx)>=3: break
    print(f'{t:20s} t24 rows {idx[:3]}')
