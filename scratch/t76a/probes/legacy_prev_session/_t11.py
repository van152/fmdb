import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
def show(j, lo=None):
    b = raw[starts[j]:starts[j]+lens[j]]
    print('row', j, 'len', len(b))
    lo = lo or max(0, len(b)-70)
    print('  tail from', lo, ':', b[lo:].hex(' '))
    return b
for j in (74281, 0, 1):
    b = show(j)
    # parse backward: identity 13 bytes
    end = len(b) - 13
    print('  identity', struct.unpack_from('<III', b, end), 'selector', b[-1])
    # strings: try to walk backwards: [u32 len][bytes(len)]
    pos = end
    out=[]
    while pos >= 4:
        ln = struct.unpack_from('<I', b, pos-4)[0]
        if 1 <= ln <= 60 and pos-4-ln >= 0:
            s = b[pos-4-ln:pos-4]
            if all(32 <= c < 127 or c == 0 for c in s) and s.endswith(b'\x00'):
                out.append((pos-4-ln, s))
                pos = pos-4-ln
                continue
        break
    print('  backward strings:', [(o, s) for o, s in out])
    print('  field region ends at', pos, 'of', end)
