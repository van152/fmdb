import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
own = np.ascontiguousarray(ms[:,16:20]).view('<u4').ravel()
print('== FK test: server u32@16 (13,576 non-null) vs reference tables ==')
for tid in (3, 23, 24, 25, 2, 10, 47):
    try:
        raw = core['load_payload']('server', tid)
    except Exception as e:
        print(tid, 'load fail', e); continue
    # get row count from header
    import struct
    cnt = struct.unpack_from('<I', raw, 8)[0]
    print(f'  t{tid}: header count {cnt} payload {len(raw)}')
