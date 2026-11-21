"""t76b scratch: award(0) structural probes — dates, sentinels, repeats."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]

print("== rows 0..5, byte index ==")
for j in range(6):
    print(j, " ".join(f"{i}:{rows[j][i]:02x}" for i in range(0, 40)))
    print(j, " ".join(f"{i}:{rows[j][i]:02x}" for i in range(40, 77)))

print("\n== u16 columns: doy/year candidate check ==")
for off, w in ((19, 2), (21, 2), (60, 2), (62, 2)):
    v = [int.from_bytes(r[off:off + w], "little") for r in rows]
    c = Counter(v)
    print(f" off{off} w{w}: d={len(c)} min={min(v)} max={max(v)} top={c.most_common(6)}")

print("\n== u32 columns with 0xffffffff sentinel ==")
for off in range(0, 61):
    v = [int.from_bytes(r[off:off + 4], "little") for r in rows]
    nff = v.count(0xFFFFFFFF)
    if nff:
        nz = v.count(0)
        setv = [x for x in v if x not in (0, 0xFFFFFFFF)]
        print(f" off{off:2d} ff={nff:4d} zero={nz:4d} set={len(setv):4d} "
              f"set_range={(min(setv), max(setv)) if setv else None}")

print("\n== u8 columns containing 0xff (optional byte) ==")
for off in range(0, 64):
    v = [r[off] for r in rows]
    nff = v.count(0xFF)
    if 20 < nff < n:
        others = sorted({x for x in v if x != 0xFF})
        print(f" off{off:2d} ff={nff:4d} others({len(others)})={others[:14]}")

print("\n== internal repeat autocorrelation (stride equality within row) ==")
for w in (2, 4):
    for stride in range(4, 25, 2):
        eq = tot = 0
        for r in rows:
            for i in range(0, 64 - stride - w + 1):
                tot += 1
                if r[i:i + w] == r[i + stride:i + stride + w]:
                    eq += 1
        if tot and eq / tot > 0.35:
            print(f" w{w} stride{stride}: eq_rate={eq / tot:.3f}")
