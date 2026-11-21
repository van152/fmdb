"""t76b scratch: decisive probes — award date roles, language enum domains, i16 sentinels."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
SCH = json.loads(Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
EN = SCH["enums"]


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


# ---------------- award ----------------
raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]


def dmy(off):
    day = int.from_bytes(rows[0][off:off + 2], "little")  # placeholder
    return None


dates = {}
for off in (19, 60):
    dates[off] = [(int.from_bytes(r[off:off + 2], "little"),
                   int.from_bytes(r[off + 2:off + 4], "little")) for r in rows]
a19 = [(d, y) for off in (19,) for d, y in dates[off]]
a60 = dates[60]
print("date@19: null(=1,1900) count", sum(1 for d, y in a19 if y == 1900))
print("date@60: null count", sum(1 for d, y in a60 if y == 1900))
both = [(j, a19[j], a60[j]) for j in range(n) if a19[j][1] != 1900 and a60[j][1] != 1900]
print("both set:", len(both))
lt = sum(1 for j, x, y in both if (y[1], y[0]) < (x[1], x[0]))
print("  off60 earlier than off19:", lt, "later:", len(both) - lt)
print("  sample:", both[:6])

print("\n== i16 triple @4/@6/@8: value-set overlap with AWpo/AWfo bitmask domains ==")


def enum_dom(f):
    key = f.get("enum_ref") or f
    return {int(v["enum"]) for v in EN.get(key, {}).get("values", [])
            if str(v["enum"]).lstrip("-").isdigit()}


for f in ("AWpo", "AWfo", "AWsr", "AWnp", "AWvf", "AWrb", "AWbr", "AWss", "AWap", "AWrt", "AWty", "AWdr", "AWsc"):
    print(f"  {f}: {sorted(enum_dom(f))}")
for off in (4, 6, 8):
    v = {int.from_bytes(r[off:off + 2], "little") for r in rows}
    print(f"  col u16@{off}: d={len(v)} {sorted(v)[:20]}")

print("\n== AWpo domain vs col u16@4/6/8 subset? ==")
dpo = enum_dom("AWpo")
for off in (4, 6, 8):
    v = {int.from_bytes(r[off:off + 2], "little") for r in rows}
    print(f"  @{off}: subset={v <= dpo} extra={sorted(v - dpo)[:6]}")

print("\n== byte2 domain vs AWbr/AWss vs 'modulo-256 of something' ==")
v2 = [r[2] for r in rows]
print("  byte2 top:", Counter(v2).most_common())
for f in ("AWbr", "AWss"):
    print(f"  {f}: {sorted(enum_dom(f))} subset={set(v2) <= enum_dom(f)}")

# ---------------- language ----------------
raw8 = load(8)
pos, L8 = 14, []
for j in range(126):
    k = struct.unpack_from("<I", raw8, pos)[0]
    L8.append({"j": j, "k": k, "name": raw8[pos + 4:pos + 4 + k],
               "pre": raw8[pos + 4 + k:pos + 4 + k + 17]})
    pos += 4 + k + 30
print("\n== language prefix columns vs Lfam/Lgro/Lsub domains ==")
for f in ("Lfam", "Lgro", "Lsub"):
    d = sorted(enum_dom(f))
    print(f"  {f}: n={len(d)} min={d[0]} max={d[-1]} {d[:12]}...")
for off in (1, 2, 3, 5, 7):
    print(f"  pre{off}: d={len({r['pre'][off] for r in L8})} "
          f"{sorted({r['pre'][off] for r in L8})}")
print("\n== language: u16 columns in prefix ==")
for off in range(0, 15):
    v = [int.from_bytes(r["pre"][off:off + 2], "little") for r in L8]
    print(f"  pre{off:2d} u16 d={len(set(v)):3d} min={min(v)} max={max(v)} {sorted(set(v))[:12]}")
