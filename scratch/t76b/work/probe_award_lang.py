"""t76b scratch: award row hex samples + language 17B prefix/suffix profile."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()

# ---- award ----
raw = D["load_payload"](C, "client", 0)
n = struct.unpack_from("<I", raw, 8)[0]
S = (len(raw) - 22) // n
rows = [raw[14 + j * S:14 + (j + 1) * S] for j in range(n)]
print(f"award client n={n} stride={S}")
for j in (0, 1, 2, 3, 100):
    r = rows[j]
    print(f"--- row{j}")
    for i in range(0, 64, 16):
        print(f"  {i:2d}: {r[i:i+16].hex(' ')}")

print("\n== candidate colour region: 3B triples anywhere in 0..63 ==")
for o in range(0, 62):
    tri = [r[o:o + 3] for r in rows]
    d = [len({t[k] for t in tri}) for k in range(3)]
    if all(x > 100 for x in d):
        print(f"  triple@{o}: distinct per byte {d}")

print("\n== near-full-range u8 columns (colour-like) ==")
for o in range(64):
    v = {r[o] for r in rows}
    if len(v) > 180:
        print(f"  b{o:2d} d={len(v)} min={min(v)} max={max(v)}")

print("\n== 4B colour words ==")
for o in range(0, 61):
    v = {int.from_bytes(r[o:o + 4], "little") for r in rows}
    if len(v) > 400:
        print(f"  u32@{o:2d} d={len(v)} max={max(v):#x}")

# ---- language ----
raw8 = D["load_payload"](C, "client", 8)
nc = struct.unpack_from("<I", raw8, 8)[0]
pos, L = 14, []
for j in range(nc):
    k = struct.unpack_from("<I", raw8, pos)[0]
    L.append({"j": j, "k": k, "name": raw8[pos + 4:pos + 4 + k],
              "pre": raw8[pos + 4 + k:pos + 4 + k + 17],
              "trail": raw8[pos + 4 + k + 17:pos + 4 + k + 30]})
    pos += 4 + k + 30
print(f"\nlanguage client n={nc} end={pos} payload={len(raw8)}")
print("name lens:", sorted({r['k'] for r in L})[:20], "max", max(r['k'] for r in L))
print("\npre bytes: per-offset value sets")
for o in range(17):
    v = [r["pre"][o] for r in L]
    print(f"  pre{o:2d}: d={len(set(v)):3d} {sorted(set(v))[:14]}")
print("\ntrail (13B) sample:", L[0]["trail"].hex(), L[125]["trail"].hex())
bad = [r["j"] for r in L if struct.unpack_from("<I", r["trail"], 0)[0] != r["j"]
       or struct.unpack_from("<I", r["trail"], 4)[0] != struct.unpack_from("<I", r["trail"], 8)[0]
       or struct.unpack_from("<I", r["trail"], 4)[0] == 0 or r["trail"][12] != 0]
print("identity bad rows:", bad)
print("\npre as u32 words:")
for o in (0, 4, 8, 12, 13):
    v = [int.from_bytes(r["pre"][o:o + 4], "little") for r in L]
    print(f"  u32@pre{o}: d={len(set(v))} min={min(v)} max={max(v)}")
