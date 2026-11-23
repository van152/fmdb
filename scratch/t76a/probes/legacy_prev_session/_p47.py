import runpy, sys, struct, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
dump = runpy.run_path('scripts/fm24_dump.py', run_name='d5')
codec = dump['_reader']()
t3 = dump['load_payload'](codec, 'client', 3)
r3 = list(dump['walk_club_block'](t3))
# find t3 rows containing club names
def find3(name):
    pat = name.encode()
    for j,(i,off,b) in enumerate(r3):
        if pat in b: return j
    return None
raw24 = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); starts=rows[:,0].astype(np.int64); lens=rows[:,1].astype(np.int64)
def find24(name):
    pat = name.encode()
    for j in range(len(rows)):
        if pat in raw24[starts[j]:starts[j]+lens[j]]: return j
    return None
raw_s = core['load_payload']('server', 21)
H,n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
own = np.ascontiguousarray(ms[:,16:20]).view('<u4').ravel().astype(np.int64)
def rowname24(j):
    b = raw24[starts[j]:starts[j]+lens[j]]
    return [m.group().decode('utf-8','replace') for m in re.finditer(rb'[\x20-\x7e]{4,}', b)][:3]
print('t3 ordinal of "Manchester United":', find3('Manchester United'))
print('t24 row of "Manchester United":', find24('Manchester United'))
print()
for nm, strow in (('Manchester United',71),('Liverpool',67),('Arsenal',7718),('Chelsea',27),
                  ('Barcelona',414),('Real Madrid',430),('Bayern',12048),('Celtic',1191)):
    i3 = find3(nm); i24 = find24(nm)
    print(f'{nm:20s} t3={i3} t24={i24} stadium @16={int(own[strow])}  t24[@{int(own[strow])}]={rowname24(int(own[strow])) if own[strow]<len(rows) else "OOR"}')
