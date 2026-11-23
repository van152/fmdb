import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n=len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
def strip(j):
    b = raw[starts[j]:starts[j]+lens[j]]
    pos = len(b) - 13
    got = []
    while pos - 4 >= 0:
        ln = struct.unpack_from('<I', b, pos-4)[0]
        if 1 <= ln <= 90 and pos-4-ln >= 0:
            s = b[pos-4-ln:pos-4]
            try:
                t = s.decode('utf-8')
            except UnicodeDecodeError:
                break
            if t.endswith('\x00') and all(32 <= ord(ch) < 0x3000 for ch in t[:-1]) and len(t) > 1:
                got.append((pos-4-ln, ln, t[:-1]))
                pos = pos-4-ln
                continue
        break
    return pos, got
from collections import Counter
base = Counter(); nstr = Counter(); ok=0
for j in range(n):
    p, got = strip(j)
    base[p] += 1; nstr[len(got)] += 1
print('string count hist', dict(sorted(nstr.items())))
print('top base sizes', base.most_common(12))
