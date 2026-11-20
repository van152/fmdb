import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
rawS = core["load_payload"]("server", 21)
rawC = core["load_payload"]("client", 21)
H, n = 14, 48413
ms = np.frombuffer(rawS, np.uint8, H + n * 181)[H:].reshape(n, 181)
mc = np.frombuffer(rawC, np.uint8, H + n * 38)[H:].reshape(n, 38)
SV = ms[:, :143]


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


c0, c4, c8, c12 = U(SV, 0, 4), U(SV, 4, 4), U(SV, 8, 4), U(SV, 12, 4)
print("=== capacity ordering tests ===")
for nm, a, b in (("@0", c0, "@4"), ("@0", c0, "@8"), ("@0", c0, "@12"),
                 ("@4", c4, "@8"), ("@4", c4, "@12"), ("@8", c8, "@12")):
    pass
print("  @0==@4 :", float((c0 == c4).mean()), " @0==@12:", float((c0 == c12).mean()),
      " @4==@12:", float((c4 == c12).mean()))
print("  @8>=@0 :", float((c8 >= c0).mean()), " @0>=@4:", float((c0 >= c4).mean()),
      " @12>=@4:", float((c12 >= c4).mean()))
print("  zeros: @0", int((c0 == 0).sum()), "@4", int((c4 == 0).sum()),
      "@8", int((c8 == 0).sum()), "@12", int((c12 == 0).sum()))
print("  @0<1 rate:", float((c0 < 1).mean()), " (Sucy min_value=1)")

print("\n=== 5 dates: adjacency + sentinel ===")
for o in (37, 41, 45, 131, 135):
    v = U(SV, o, 4)
    doy, yr = v & 0xFFFF, v >> 16
    import collections
    print(f"  @{o}: yr top-byte const? b{o+3} uniq={np.unique(SV[:,o+3]).tolist()} "
          f"yr[{yr.min()},{yr.max()}] doy[{doy.min()},{doy.max()}] "
          f"is_1900_01_01={(int(((yr==1900)&(doy==1)).sum()))}")

print("\n=== 8x8B block 64..127: per-record field shapes ===")
for r in range(8):
    b = 64 + r * 8
    print(f"  rec{r} @{b}: u16a d={np.unique(U(SV,b,2)).size} max={U(SV,b,2).max():6d} | "
          f"u16b d={np.unique(U(SV,b+2,2)).size} max={U(SV,b+2,2).max():6d} | "
          f"b{b+4} {np.unique(SV[:,b+4]).tolist()[:6]} b{b+5} d={np.unique(SV[:,b+5]).size} "
          f"b{b+6} {np.unique(SV[:,b+6]).tolist()[:6]} b{b+7} {np.unique(SV[:,b+7]).tolist()[:6]}")

print("\n=== u16a >= u16b? (capacity vs seating within side) ===")
for r in range(8):
    b = 64 + r * 8
    a, bb = U(SV, b, 2), U(SV, b + 2, 2)
    print(f"  rec{r}: a>=b {float((a>=bb).mean()):.4f}  a0 {(a==0).mean():.4f} b0 {(bb==0).mean():.4f}")

print("\n=== pitch-ish: b33/b34/b35 and u16@33 ===")
for o in (32, 33, 34, 35, 36):
    print(f"  b{o}: {np.unique(SV[:,o]).tolist()[:20]}")
print("  u16@33 vals sample:", np.unique(U(SV,33,2))[:20].tolist())
print("  u16@34 vals sample:", np.unique(U(SV,34,2))[:20].tolist())
print("  u16@35 vals sample:", np.unique(U(SV,35,2))[:20].tolist())

print("\n=== client @0..2 and @11..16 vs server: any match? ===")
for co in range(3):
    for so in range(143):
        if np.array_equal(mc[:, co], SV[:, so]) and not (mc[:, co] == 0).all():
            print(f"  client b{co} == server b{so}")
for co in range(11, 17):
    for so in range(143):
        if np.array_equal(mc[:, co], SV[:, so]) and not (mc[:, co] == 0).all():
            print(f"  client b{co} == server b{so}")
