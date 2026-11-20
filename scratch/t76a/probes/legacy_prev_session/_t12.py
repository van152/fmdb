import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
def parse(j):
    b = raw[starts[j]:starts[j]+lens[j]]
    end = len(b) - 13
    pos = end; strs = []
    while pos - 4 >= 0:
        ln = struct.unpack_from('<I', b, pos-4)[0]
        if 0 < ln <= 80 and pos-4-ln >= 0:
            s = b[pos-4-ln:pos-4]
            if s.endswith(b'\x00') and all(32 <= c < 127 or c >= 0xc0 or c == 0 for c in s):
                strs.append((pos-4-ln, ln)); pos = pos-4-ln; continue
        break
    return b, end, pos, strs
bad=0; samples=[]
for j in range(0, n, 500):
    b, end, pos, strs = parse(j)
    if not strs and lens[j] > 90: bad += 1; samples.append((j, int(lens[j]), end, pos))
print('sampled rows with len>90 but no backward-parsed strings:', bad, '/', len(range(0,n,500)))
print('samples', samples[:5])
for j in (74281, 414, 1230, 100):
    b, end, pos, strs = parse(j)
    print(j, 'len', len(b), 'scalar_block', pos, 'strings', strs)
