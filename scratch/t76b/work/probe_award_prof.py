"""t76b scratch: award(0) full column profile + ordinal-domain FK tests."""
import runpy, sys, struct
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()

NROWS = {"club": 84259, "comp": 7047, "stadium": 48413, "city": 56293,
         "nation": 251, "region": 28, "continent": 7, "language": 126,
         "media_source": 208, "award": 3545}


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


for arch in ("client", "server"):
    raw = load(0, arch)
    n = struct.unpack_from("<I", raw, 8)[0]
    print(f"=== award {arch} payload={len(raw)} n={n} stride={(len(raw)-22)//n}")
    S = (len(raw) - 22) // n
    rows = [raw[14 + j * S:14 + (j + 1) * S] for j in range(n)]
    print("  stride", S, "rows", len(rows), "row0len", len(rows[0]))
    print("  byte constants:", [o for o in range(S)
                                if len({r[o] for r in rows}) == 1])
    print("\n  -- u8 columns --")
    for o in range(S):
        v = [r[o] for r in rows]
        s = set(v)
        if len(s) == 1:
            continue
        print(f"   b{o:2d}: d={len(s):3d} min={min(s):3d} max={max(s):3d} "
              f"{sorted(s)[:10]}")
    print("\n  -- u16 columns --")
    for o in range(0, S - 1):
        v = [int.from_bytes(r[o:o + 2], "little") for r in rows]
        s = set(v)
        if len(s) <= 40 or o in (19, 21, 60, 62):
            print(f"   u16@{o:2d}: d={len(s):4d} min={min(s)} max={max(s)} "
                  f"{sorted(s)[:8]}")
    print("\n  -- u32 columns --")
    for o in range(0, S - 3):
        v = [int.from_bytes(r[o:o + 4], "little") for r in rows]
        nn = [x for x in v if x != 0xffffffff]
        s = set(nn)
        if not s:
            continue
        if len(s) <= 600:
            fit = {t: (sum(1 for x in nn if x < N) / len(nn), max(nn), N)
                   for t, N in NROWS.items() if max(nn) < N}
            tight = {t: round(f[0], 4) for t, f in fit.items() if f[0] == 1.0}
            print(f"   u32@{o:2d}: d={len(s):4d} null={v.count(0xffffffff):4d} "
                  f"min={min(nn)} max={max(nn)} ord_fits={list(tight)[:8]}")
    break
