"""t76c scratch: ORDINAL-domain FK tests (calibrated by stadium Scti@3 -> city)."""
import runpy, struct, random, json
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

# live row counts (frozen by t57/t59/t66/t73/t74)
N = {'club': 84259, 'team': 84507, 'comp': 7047, 'stadium': 48413, 'city': 56293,
     'nation': 251, 'region': 28, 'continent': 7, 'language': 126, 'weather': 334,
     'local_region': 2488, 'agreement': 6}


def ordtest(label, vals, width_bytes=4):
    """Ordinal encoding: value must be < N and reach near N-1. Null model uniform."""
    vals = [x for x in vals if x not in (0xFFFFFFFF, 0xFFFF, 0xFFFFFF, 0xFF)]
    if len(vals) < 5:
        print(f'  {label}: too few ({len(vals)})')
        return
    mx, mn = max(vals), min(vals)
    print(f'  {label}: n={len(vals)} range=[{mn},{mx}] distinct={len(set(vals))}')
    rng = random.Random(7)
    scored = []
    for nm, lim in N.items():
        hit = sum(1 for x in vals if x < lim)
        frac = hit / len(vals)
        if frac < 0.999:
            continue
        # null model: uniform in [mn, mx]
        out = []
        for _ in range(300):
            d = [rng.randint(mn, mx) for _ in range(min(400, len(vals)))]
            out.append(sum(1 for x in d if x < lim) / len(d))
        ch = sum(out) / len(out)
        # fit quality: how much of [0,lim) is used
        cover = (mx + 1) / lim if lim > mx else 1.0
        scored.append((nm, lim, round(frac, 4), round(ch, 4), round(cover, 3)))
    if not scored:
        print('    no table satisfies rate>=0.999')
        return
    # The tightest bounding table is the best ordinal candidate
    best = min(scored, key=lambda s: s[1])
    for nm, lim, frac, ch, cover in scored:
        mark = ' <== TIGHTEST' if nm == best[0] else ''
        print(f'    {nm:13} N={lim:<6} rate={frac:.4f} chance={ch:.4f} '
              f'max/N={cover:.3f}{mark}')


# ---------------- DERBY ----------------
def derby_num(arch):
    num = 36 if arch == 'client' else 42
    raw = load(arch, 18)
    pos, out = 14, []
    for j in range(1567):
        p, nb = pos, 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        out.append(raw[pos + 16 + nb:end - 13])
        pos = end
    return out


for arch in ('client', 'server'):
    D = derby_num(arch)
    print('=' * 22, 'DERBY', arch)
    for off in (4, 8, 12, 16, 20):
        ordtest(f'u32@{off}', [int.from_bytes(d[off:off + 4], 'little') for d in D])
    print('  --- u8/u16 tail')
    for off in range(24, len(D[0])):
        v = [d[off] for d in D]
        print(f'    b{off}: d={len(set(v)):4} min={min(v):3} max={max(v):3} '
              f'null_ff={v.count(255):4} zero={v.count(0):4}')
    for off in (28, 30, 32):
        if off + 2 <= len(D[0]):
            ordtest(f'u16@{off}', [int.from_bytes(d[off:off + 2], 'little') for d in D])
