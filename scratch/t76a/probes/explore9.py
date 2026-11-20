import runpy, sys, json
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core["load_payload"]("server", 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
S = ms[:, :143]
out = []


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


out.append("=== ALL byte columns 0..142 (distinct<=20 or const) ===")
for o in range(143):
    u = np.unique(S[:, o])
    out.append(f"  b{o:3d} d={u.size:4d} " + (str(u.tolist()) if u.size <= 20 else f"min={u.min()} max={u.max()}"))

out.append("\n=== 8-periodicity test: profile-equal classes ===")
sig = {o: (np.unique(S[:, o]).size, int(S[:, o].min()), int(S[:, o].max()), int((S[:, o] == 0).sum())) for o in range(143)}
for base in range(0, 120):
    same = [k for k in range(8) if base + k + 8 < 143 and sig[base + k] == sig[base + k + 8]]
    if len(same) >= 6:
        out.append(f"  base={base} period8 profile-equal bytes={same}")

out.append("\n=== u32 grid 0..142 step 4, with f32 plausibility ===")
for o in range(0, 140, 4):
    v = U(S, o, 4)
    f = np.ascontiguousarray(S[:, o:o + 4]).view("<f4").ravel()
    fin = np.isfinite(f)
    okf = bool(fin.all() and (np.abs(f[fin]) < 1e6).all())
    out.append(f"  @{o:3d} u32 d={np.unique(v).size:5d} z={int((v==0).sum()):6d} ff={int((v==0xffffffff).sum()):6d} "
               f"min={v.min():10d} max={v.max():10d} f32ok={okf}")

out.append("\n=== rows 0,1,2,7 byte-by-byte 0..142 ===")
for r in (0, 1, 2, 7):
    out.append(f"row{r}: " + " ".join(f"{i}:{S[r,i]:02x}" for i in range(143)))

out.append("\n=== client 38B full byte columns ===")
raw_c = core["load_payload"]("client", 21)
mc = np.frombuffer(raw_c, np.uint8, H + n * 38)[H:].reshape(n, 38)
for o in range(38):
    u = np.unique(mc[:, o])
    out.append(f"  c b{o:2d} d={u.size:4d} " + (str(u.tolist()) if u.size <= 20 else f"min={u.min()} max={u.max()}"))
print("\n".join(out))
