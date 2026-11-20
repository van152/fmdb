import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
print('len', len(raw), 'count hdr', struct.unpack_from('<I', raw, 8)[0])
# walk rows: identity at row_end-13 (ord, uid, uid, selector)
n = struct.unpack_from('<I', raw, 8)[0]
pos = 14
starts = np.empty(n, dtype=np.int64); ends = np.empty(n, dtype=np.int64)
# fast approach: find all candidate identity positions via ordinal match? Use given DP result: need row boundaries.
# Instead: use the fact that selector at -1 and ord at -13; do a greedy scan is O(n*L). Try quick: search for ordinals sequentially with small window.
rows = []
p = 14
ok = 0
for j in range(n):
    # try to find end such that u32@(end-13)==j
    found = None
    for ln in range(86, 667):
        e = p + ln
        if e > len(raw) - 8: break
        if struct.unpack_from('<I', raw, e-13)[0] == j:
            a, b = struct.unpack_from('<II', raw, e-9)
            if a == b != 0:
                found = ln; break
    if found is None:
        print('stuck at row', j, 'pos', p); break
    rows.append((p, found)); p += found; ok += 1
print('rows walked', ok, 'end', p, 'payload', len(raw), 'footer', len(raw)-p)
lens = np.array([l for _, l in rows])
print('len stats', lens.min(), lens.max(), lens.mean(), len(np.unique(lens)))
