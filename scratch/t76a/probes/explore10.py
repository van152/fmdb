import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core["load_payload"]("server", 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
S = ms[:, :143]

print("=== exact indexed dump, rows 0-3, one byte per token ===")
for r in (0, 1, 2):
    print(f"--- row{r}")
    for base in range(0, 143, 16):
        print("  " + " ".join(f"{i:3d}:{S[r,i]:02x}" for i in range(base, min(base + 16, 143))))

print("\n=== exact column-equality period search (period P, k blocks) ===")
for P in range(4, 40):
    for phi in range(0, 143):
        k = (143 - phi) // P
        if k < 3:
            continue
        blocks = [(phi + i * P, phi + (i + 1) * P) for i in range(k)]
        eqcols = []
        for j in range(P):
            cols = [S[:, a + j] for a, b in blocks]
            eq = all(np.array_equal(cols[0], c) for c in cols[1:])
            eqcols.append(eq)
        score = sum(eqcols)
        if score >= P - 2 and score >= 5:
            print(f"  P={P:2d} phi={phi:3d} k={k} eq={score}/{P} -> {phi}..{phi+k*P}")

print("\n=== 16B-block equality: S[:,64:132] as 4x16 vs structure ===")
for a in range(64, 132):
    for b in range(a + 1, 132):
        L = 8
        if b + L <= 143 and np.array_equal(S[:, a:a + L], S[:, b:b + L]):
            print(f"  exact 8B equal: @{a} == @{b}")
