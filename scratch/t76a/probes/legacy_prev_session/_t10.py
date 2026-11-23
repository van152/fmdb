import runpy, sys, struct, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
j = 74281
b = raw[starts[j]:starts[j]+lens[j]]
print('len', len(b))
for m in re.finditer(rb'[\x20-\x7e]{3,}', b):
    print('  off', m.start(), m.group()[:60])
print()
print('first 130:', b[:130].hex(' '))
print('tail 40:', b[-40:].hex(' '))
