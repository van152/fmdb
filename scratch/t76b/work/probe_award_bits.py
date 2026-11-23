"""t76b scratch: award(0) i16 null-sentinel fields + bit-level field extraction."""
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
BIZ = 64

print("== i16 fields with 0x7fff null sentinel ==")
for o in range(0, BIZ - 1):
    v = [int.from_bytes(r[o:o + 2], "little") for r in rows]
    n7 = v.count(0x7FFF)
    if not n7:
        continue
    nn = [x for x in v if x != 0x7FFF]
    print(f"  i16@{o:2d} null7fff={n7:4d} nonnull={len(nn):4d} "
          f"range={min(nn)}..{max(nn)} distinct={len(set(nn))}")

print("\n== bit-level: constant bits over all 3545 rows ==")
bits = []
for bit in range(BIZ * 8):
    bo, bi = bit // 8, bit % 8
    vals = {(r[bo] >> bi) & 1 for r in rows}
    bits.append(len(vals) == 1)
runs, cur = [], None
for i, c in enumerate(bits):
    if c and cur is None:
        cur = i
    elif not c and cur is not None:
        runs.append((cur, i - 1))
        cur = None
if cur is not None:
    runs.append((cur, len(bits) - 1))
print("  constant bit runs (start_bit,end_bit,len):")
print("   ", runs)

print("\n== bit-run 0/1 field scan: contiguous non-constant bit fields whose")
print("   value-set exactly equals an award enum domain (search width 1..16 bits) ==")
SCH = json.loads((Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json")
                  ).read_text(encoding="utf-8"))
EN, ENT = SCH["enums"], SCH["entities"]


def enum_ids(name):
    e = EN.get(name)
    if not e:
        return None
    out = set()
    for v in e["values"]:
        try:
            out.add(int(v["enum"]))
        except (TypeError, ValueError):
            pass
    return out


AW_ENUM = {f["field"]: enum_ids(f.get("enum_ref") or f["field"])
           for f in ENT["award.xml"][0]["fields"] if f["type"] == "enum"}

ints = [int.from_bytes(r, "little") for r in rows]
hits = []
for w in range(1, 17):
    mask = (1 << w) - 1
    for bit in range(0, BIZ * 8 - w + 1):
        if bit % 8 == 0:
            continue  # byte-aligned already covered
        vals = {(x >> bit) & mask for x in ints}
        if len(vals) < 2 or len(vals) > 40:
            continue
        for f, d in AW_ENUM.items():
            if d and vals == d:
                hits.append((f, bit, w, sorted(vals)))
for f, bit, w, vals in sorted(hits):
    print(f"  {f:5s} bit={bit:3d} w={w:2d} vals={vals}")
print("  total exact-bit hits:", len(hits))
