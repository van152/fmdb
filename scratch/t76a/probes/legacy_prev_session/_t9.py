import runpy, sys, struct, re
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
for name in (b'Arsenal', b'Manchester United', b'Real Madrid', b'Barcelona', b'Bayern'):
    for m in re.finditer(re.escape(name), raw):
        j = int(np.searchsorted(starts, m.start()) - 1)
        if 0 <= j < n and starts[j] <= m.start() < starts[j]+lens[j]:
            print(name.decode(), 'row', j, 'rowoff', m.start()-starts[j], 'rowlen', int(lens[j]))
            print('   row hex:', raw[starts[j]:starts[j]+min(int(lens[j]),130)].hex(' '))
        break
