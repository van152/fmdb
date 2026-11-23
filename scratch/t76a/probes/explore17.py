import runpy, sys, json
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
rawS = core["load_payload"]("server", 21)
H, n = 14, 48413
ms = np.frombuffer(rawS, np.uint8, H + n * 181)[H:].reshape(n, 181)
SV = ms[:, :143]
S = json.load(open('evidence/fm24/reports/editor_schema/master.json'))
E = S['enums']


def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


print("=== enum domain match (byte col subset of scoped enum) ===")
for fname in ('Soty', 'Spty', 'Sdtr', 'Sste', 'Senv', 'Sunt', 'Su21', 'Su19', 'indx'):
    dom = {int(v['enum']) for v in E.get(fname, {}).get('values', [])
           if str(v['enum']).lstrip('-').isdigit()}
    if not dom:
        continue
    hits = []
    for o in range(143):
        col = set(np.unique(SV[:, o]).tolist())
        if len(col) >= 2 and col <= dom:
            hits.append((o, sorted(col)))
    print(f"  {fname:5} dom={sorted(dom)} -> {len(hits)} byte cols: {hits[:6]}")

print("\n=== u16 columns in plausible pitch range (short_distance) ===")
for o in range(0, 142):
    v = U(SV, o, 2)
    u = np.unique(v)
    if u.size < 4:
        continue
    if u.min() >= 40 and u.max() <= 130:
        print(f"  u16@{o:3d} d={u.size} min={u.min()} max={u.max()}")
    elif u.min() >= 4000 and u.max() <= 13000:
        print(f"  u16@{o:3d} (x100) d={u.size} min={u.min()} max={u.max()}")

print("\n=== 0..20 and 0..200 single-byte ints ===")
for o in range(143):
    u = np.unique(SV[:, o])
    if u.size > 3 and u.max() <= 20 and u.min() == 0:
        print(f"  b{o:3d} 0..{u.max()} d={u.size}")
    if u.size > 3 and u.max() <= 200 and u.min() == 0 and u.max() > 20:
        print(f"  b{o:3d} 0..{u.max()} d={u.size} (0..200 Sptc?)")

print("\n=== b49/50/51 cross-tab (Sunt/Su21/Su19) ===")
for o in (49, 50, 51):
    u, c = np.unique(SV[:, o], return_counts=True)
    print(f"  b{o}: {dict(zip(u.tolist(), c.tolist()))}")

print("\n=== sides block: is b68..b71 a 4-bool byte? ===")
for o in (68, 76, 84, 92, 100, 108, 116, 124):
    print(f"  b{o}: {np.unique(SV[:,o]).tolist()}  b{o+1}: {np.unique(SV[:,o+1]).tolist()[:10]}"
          f"  b{o+2}: {np.unique(SV[:,o+2]).tolist()[:10]}  b{o+3}: d={np.unique(SV[:,o+3]).size}")
