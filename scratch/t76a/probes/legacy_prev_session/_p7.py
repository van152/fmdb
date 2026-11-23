import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n, Ss = 14, 48413, 181
ms = np.frombuffer(raw_s, dtype=np.uint8, count=H+n*Ss)[H:].reshape(n, Ss)
for j in range(4):
    print(j, ms[j, 0:143].tobytes().hex(' '))
print('--- printable runs in row0..3 (first 143 B) ---')
import re
for j in range(3):
    r = ms[j,0:143].tobytes()
    for m in re.finditer(rb'[\x20-\x7e]{3,}', r):
        print(j, m.start(), m.group())
