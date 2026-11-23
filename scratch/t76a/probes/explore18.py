import runpy, sys, json
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
print("=== reference_uids availability (client archive) ===")
for tid, nm in ((2, "city"), (3, "club"), (10, "nation"), (19, "region"), (25, "comp"), (21, "stadium")):
    r = core["reference_uids"]("client", tid)
    print(f"  t{tid:<3} {nm:8} ok={r['ok']} n={len(r['uids']) if r['ok'] else '-'} "
          f"{(r.get('why') or '')[:60]}")

print("\n=== ANCHOR RECONCILIATION: client identity triple ===")
rawC = core["load_payload"]("client", 21)
H, n = 14, 48413
mc = np.frombuffer(rawC, np.uint8, H + n * 38)[H:].reshape(n, 38)


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


ar = np.arange(n)
for o in (25, 29, 33):
    v = U(mc, o, 4)
    print(f"  @{o}: ==row_index {int((v == ar).sum())}/{n}  distinct={np.unique(v).size} "
          f"min={v.min()} max={v.max()}")
print("  @29==@33:", bool((U(mc, 29, 4) == U(mc, 33, 4)).all()))
print("  @25==@29:", bool((U(mc, 25, 4) == U(mc, 29, 4)).all()))

rawS = core["load_payload"]("server", 21)
ms = np.frombuffer(rawS, np.uint8, H + n * 181)[H:].reshape(n, 181)
for o in (168, 172, 176):
    v = U(ms, o, 4)
    print(f"  server @{o}: ==row_index {int((v == ar).sum())}/{n} distinct={np.unique(v).size}")
print("  server @172==@176:", bool((U(ms, 172, 4) == U(ms, 176, 4)).all()))
