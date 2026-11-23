import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core["load_payload"]("server", 21)
raw_c = core["load_payload"]("client", 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
mc = np.frombuffer(raw_c, np.uint8, H + n * 38)[H:].reshape(n, 38)
S = ms[:, :143]


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


print("=== period search in server-only 143B (byte-profile signature match) ===")
sig = {}
for o in range(143):
    u = np.unique(S[:, o])
    sig[o] = (u.size, tuple(u[:6].tolist()))
for P in range(8, 25):
    best = None
    for phi in range(0, 143 - 3 * P):
        score = sum(1 for i in range(P) if sig[phi + i] == sig[phi + P + i] == sig[phi + 2 * P + i])
        if best is None or score > best[0]:
            best = (score, phi)
    if best[0] > P * 0.7:
        print(f"  P={P} phi={best[1]} score={best[0]}/{P}")

print("\n=== candidate capacities (u32 @0,4,8,12) vs schema max 200000 ===")
for o in (0, 4, 8, 12):
    v = U(S, o, 4)
    print(f"  @{o}: max={v.max()} le200000={(v<=200000).mean():.4f} zeros={int((v==0).sum())} d={np.unique(v).size}")

print("\n=== ordinal-domain checks (client) ===")
NROWS = {"city": 56293, "club": 84259, "nation": 251, "region": 28, "comp": 7047, "stadium": 48413}
NULL = 0xFFFFFFFF
for o, w in ((3, 4), (7, 4), (25, 4)):
    v = U(mc, o, w)
    keep = v != NULL
    print(f"  client @{o} u{w//8}: null={int((~keep).sum())} nonnull={int(keep.sum())}")
    for t, N in NROWS.items():
        vv = v[keep]
        print(f"     {t:8} N={N:6d} in_domain={(vv<N).mean():.4f} max={vv.max()}")

print("\n=== ordinal-domain checks (server-only) ===")
for o in (16,):
    v = U(S, o, 4)
    keep = v != NULL
    vv = v[keep]
    print(f"  @{o}: null={int((~keep).sum())} nonnull={int(keep.sum())}")
    for t, N in NROWS.items():
        print(f"     {t:8} N={N:6d} in_domain={(vv<N).mean():.4f} max={vv.max()}")

print("\n=== client b11 correlation ===")
b11 = mc[:, 11]
for o, w in ((3, 4), (7, 4)):
    v = U(mc, o, w)
    print(f"  b11 x @{o}: groups={np.unique(b11).size}")
    for g in np.unique(b11):
        sel = b11 == g
        print(f"    b11={g:3d} n={int(sel.sum()):6d} nonnull_ff={int((v[sel]!=NULL).sum())}")
