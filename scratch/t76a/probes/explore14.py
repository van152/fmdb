import runpy, sys, json
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
rawC = core["load_payload"]("client", 21)
rawS = core["load_payload"]("server", 21)
H, n = 14, 48413
mc = np.frombuffer(rawC, np.uint8, H + n * 38)[H:].reshape(n, 38)
ms = np.frombuffer(rawS, np.uint8, H + n * 181)[H:].reshape(n, 181)
SV = ms[:, :143]


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


print("=== client 16-bit flag word @0 (bit rates) ===")
v = U(mc, 0, 2)
for b in range(16):
    r = float(((v >> b) & 1).mean())
    if r > 0:
        print(f"  bit{b:2d}: {r:.5f}  n={int(((v>>b)&1).sum())}")

print("\n=== server: 1-byte boolean candidates (d==2, values {0,1}) ===")
for o in range(143):
    u = np.unique(SV[:, o])
    if u.tolist() == [0, 1]:
        print(f"  b{o:3d}: n1={int((SV[:,o]==1).sum())}")

print("\n=== server: 3-value bytes {0,1,255} or {0,1,2} ===")
for o in range(143):
    u = np.unique(SV[:, o]).tolist()
    if u in ([0, 1, 255], [0, 1, 2], [0, 1, 2, 3]):
        print(f"  b{o:3d}: {u} counts={[int((SV[:,o]==x).sum()) for x in u]}")

print("\n=== server u16 pitch-range columns (values 300..1500) ===")
for o in range(0, 142):
    v2 = U(SV, o, 2)
    u = np.unique(v2)
    if u.size <= 400 and u.min() >= 200 and u.max() <= 2000 and u.size > 3:
        print(f"  u16@{o:3d} d={u.size} min={u.min()} max={u.max()} zeros={int((v2==0).sum())}")

print("\n=== server 64..127: block variance (which bytes vary within 16B block) ===")
for base in (64, 80, 96, 112):
    desc = []
    for k in range(16):
        u = np.unique(SV[:, base + k])
        desc.append(f"{base+k}:d{u.size}")
    print("  " + " ".join(desc))

print("\n=== packed date candidates: verify all 5 (server 37,41,45,131,135; client 13) ===")
import datetime
for tag, m, o in (("s@37", SV, 37), ("s@41", SV, 41), ("s@45", SV, 45),
                  ("s@131", SV, 131), ("s@135", SV, 135), ("c@13", mc, 13)):
    v4 = U(m, o, 4)
    doy, yr = v4 & 0xFFFF, v4 >> 16
    ok = (doy >= 1) & (doy <= 366) & (yr >= 1850) & (yr <= 2035)
    print(f"  {tag}: ok={ok.mean():.4f} doy[{doy[ok].min()},{doy[ok].max()}] "
          f"yr[{yr[ok].min()},{yr[ok].max()}] distinct_vals={np.unique(v4).size}")
