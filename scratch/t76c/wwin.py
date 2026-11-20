"""t76c scratch: exhaustive window search inside the 23B weather block."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
raw = core['load_payload']('client', 27)
M, pos = [], 14
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    pos = end
n = len(M)
print('rows', n)

for b in range(4):
    base = 3 + 23 * b
    print(f'\n=== block{b} base={base}')
    best = []
    for o in range(23):
        for L in range(1, 12):
            if o + L > 23:
                continue
            s = [sum(m[base + o:base + o + L]) for m in M]
            best.append((s.count(100), o, L))
    best.sort(reverse=True)
    for c, o, L in best[:6]:
        print(f'   sum100={c:3}/{n}  window rel{o}..rel{o+L-1} (L={L})')
    print('   per-rel value domains:')
    for rel in range(23):
        v = [m[base + rel] for m in M]
        s = sorted(set(v))
        tag = ''
        if len(s) == 1:
            tag = ' CONST=%d' % s[0]
        elif s == [0, 100]:
            tag = ' {0,100}'
        elif s == [0, 1]:
            tag = ' {0,1}'
        print(f'     rel{rel:2} d={len(s):3} [{min(v):3},{max(v):3}] z={v.count(0):3}{tag}')
