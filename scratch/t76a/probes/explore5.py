import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
for r in (0, 1, 2, 3, 7):
    print(f'row{r} [0:143]:')
    for i in range(0, 143, 24):
        print(f'  {i:3d}: ' + ms[r, i:i+24].tobytes().hex(' '))
# look for repeated 17-byte or 23-byte blocks
S = ms[:, :143]
print('\n=== self-similarity: is S[:,a:a+L] == S[:,b:b+L]? ===')
for L in (4, 8, 17, 23, 28, 30):
    hits = []
    for a in range(0, 143 - L + 1):
        for b in range(a + 1, 143 - L + 1):
            if np.array_equal(S[:, a:a+L], S[:, b:b+L]) and not (S[:, a:a+L] == 0).all():
                hits.append((a, b))
    print(f'L={L}: {len(hits)} hits', hits[:10])
