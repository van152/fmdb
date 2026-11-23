"""t76b scratch: award dependency gating tests (AWdr==6 -> AWda, AWrt gating)."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
SCH = json.loads(Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]


def date_set(off):
    return [int.from_bytes(r[off + 2:off + 4], "little") != 1900 for r in rows]


d19, d60 = date_set(19), date_set(60)
print("dates: off19 set=%d off60 set=%d" % (sum(d19), sum(d60)))

print("\n=== contingency: byte column value -> date-set rate ===")
for off in range(64):
    vals = [r[off] for r in rows]
    dom = sorted(set(vals))
    if len(dom) > 10 or len(dom) < 2:
        continue
    line = []
    for k in dom:
        m = [v == k for v in vals]
        c = sum(m)
        r19 = sum(1 for i in range(n) if m[i] and d19[i]) / c
        r60 = sum(1 for i in range(n) if m[i] and d60[i]) / c
        line.append(f"{k}:n{c}/d19={r19:.2f}/d60={r60:.2f}")
    print(f" byte{off:2d} ({len(dom)}) " + "  ".join(line))

print("\n=== i16 sentinel scan (0x7fff) & i32 sentinel (0x7fffffff) ===")
for off in range(0, 62):
    v16 = [int.from_bytes(r[off:off + 2], "little") for r in rows]
    v32 = [int.from_bytes(r[off:off + 4], "little") for r in rows]
    c16 = v16.count(0x7FFF)
    c32 = v32.count(0x7FFFFFFF)
    cff = v32.count(0xFFFFFFFF)
    if c16 > 100 or c32 > 100 or cff > 100:
        print(f" off{off:2d}: i16sent={c16} i32sent={c32} ff32={cff}")

print("\n=== bytes 4..9 as three i16 pairs (0x7fff unset) ===")
for off in (4, 6, 8, 10):
    v = [int.from_bytes(r[off:off + 2], "little") for r in rows]
    s = sorted(set(v))
    print(f" off{off}..{off + 1}: d={len(s)} min={min(s)} max={max(s)} "
          f"sent7fff={v.count(0x7FFF)} top={Counter(v).most_common(5)}")

print("\n=== colour triples: 3-byte groups whose 3rd byte high bits vary ===")
for off in range(0, 40):
    r_ = [r[off] for r in rows]
    g_ = [r[off + 1] for r in rows]
    b_ = [r[off + 2] for r in rows]
    if len(set(r_)) < 3:
        continue
    # colours in FM: 0..255 per channel, but stored with 0x00 prefix? check high-byte pattern
    if all(x <= 0xFF for x in g_) and len(set(g_)) > 2:
        pass
