"""t76b scratch: award(0) joint constraint solve — null patterns, dates, ordinals."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()

raw = D["load_payload"](C, "client", 0)
n = struct.unpack_from("<I", raw, 8)[0]
S = (len(raw) - 22) // n
rows = [raw[14 + j * S:14 + (j + 1) * S] for j in range(n)]
print(f"n={n} stride={S} field_region={S - 13} (t74 said 73 -> arithmetic slip)")

# identity re-verify
bad = [j for j, r in enumerate(rows)
       if struct.unpack_from("<I", r, 64)[0] != j
       or struct.unpack_from("<I", r, 68)[0] != struct.unpack_from("<I", r, 72)[0]
       or struct.unpack_from("<I", r, 68)[0] == 0 or r[76] != 0]
print("identity bad:", bad[:5], len(bad))

# packed dates. null sentinel = (day=1, year=1900)
def dates(doff, yoff):
    out = []
    for r in rows:
        d = int.from_bytes(r[doff:doff + 2], "little")
        y = int.from_bytes(r[yoff:yoff + 2], "little")
        out.append(None if (d == 1 and y == 1900) else (y, d))
    return out

D19, D60 = dates(19, 21), dates(60, 62)
print("date@19 nonnull:", sum(x is not None for x in D19),
      " date@60 nonnull:", sum(x is not None for x in D60))

print("\n== column null-pattern map (u8 / u16 / u32 windows) ==")
for o in range(0, 64):
    b = [r[o] for r in rows]
    nn8 = [x for x in b if x != 0xFF]
    print(f"  b{o:2d} nullFF={b.count(0xFF):4d} d_nonnull={len(set(nn8)):3d} "
          f"range={min(nn8) if nn8 else None}..{max(nn8) if nn8 else None}")

print("\n== u32 slots with 0xffffffff null semantics ==")
for o in range(0, 61):
    v = [int.from_bytes(r[o:o + 4], "little") for r in rows]
    nulls = v.count(0xFFFFFFFF)
    nn = [x for x in v if x != 0xFFFFFFFF]
    if nulls and len(set(nn)) > 1:
        print(f"  u32@{o:2d} null={nulls:4d} distinct_nn={len(set(nn)):4d} "
              f"min={min(nn)} max={max(nn)}")
