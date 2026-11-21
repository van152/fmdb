"""t76b scratch: award(0) systematic constraint search."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
REPO = Path(r"D:/tmp2b/fm24-db")
SCH = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
EN, ENT = SCH["enums"], SCH["entities"]

NROWS = {"club": 84259, "comp": 7047, "stadium": 48413, "city": 56293,
         "nation": 251, "region": 28, "continent": 7, "language": 126,
         "media_source": 208, "award": 3545}


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


FIELDS = ENT["award.xml"][0]["fields"]
AW_ENUM = {f["field"]: enum_ids(f.get("enum_ref") or f["field"])
           for f in FIELDS if f["type"] == "enum"}
AW_INT = {f["field"]: (int(f.get("min_value", 0)), int(f.get("max_value", 0)))
          for f in FIELDS if f["type"] == "integer" and "min_value" in f}
AW_FK = {f["field"]: f.get("database_table_type")
         for f in FIELDS if f["type"] in ("database_record_unique_id", "database_record_list")
         and f.get("database_table_type")}
print("enum fields:", {k: len(v) for k, v in AW_ENUM.items()})
print("int fields:", AW_INT)
print("fk fields:", AW_FK)

raw = D["load_payload"](C, "client", 0)
n = struct.unpack_from("<I", raw, 8)[0]
S = (len(raw) - 22) // n
rows = [raw[14 + j * S:14 + (j + 1) * S] for j in range(n)]


def col(o, w):
    return [int.from_bytes(r[o:o + w], "little") for r in rows]


print("\n== year==1900 rows by day value (date null semantics) ==")
for doff, yoff in ((19, 21), (60, 62)):
    pairs = [(int.from_bytes(r[doff:doff + 2], "little"),
              int.from_bytes(r[yoff:yoff + 2], "little")) for r in rows]
    y1900 = [d for d, y in pairs if y == 1900]
    print(f"  date@{doff}: year1900 rows={len(y1900)} day dist={Counter(y1900).most_common(5)}")
    nonnull = [(d, y) for d, y in pairs if y != 1900]
    print(f"    nonnull={len(nonnull)} day_range={min(d for d, _ in nonnull)}..{max(d for d, _ in nonnull)}"
          f" year_range={min(y for _, y in nonnull)}..{max(y for _, y in nonnull)}")

print("\n== u8 columns: enum exact/subset + int-range match ==")
for o in range(64):
    v = col(o, 1)
    s = set(v)
    if len(s) < 2:
        continue
    lines = []
    for f, d in AW_ENUM.items():
        if d and s == d:
            lines.append(f"{f}=EXACT")
        elif d and s <= d:
            lines.append(f"{f}SUBSET")
    for f, (lo, hi) in AW_INT.items():
        nn = [x for x in v if x != 0xFF]
        if nn and min(nn) >= lo and max(nn) <= hi and len(set(nn)) > 3:
            lines.append(f"{f}[{lo},{hi}]")
    if lines:
        print(f"  b{o:2d} d={len(s):3d} {sorted(s)[:9]} -> {' '.join(lines)}")

print("\n== u32 columns: ordinal tight fit (max+1 close to N) ==")
for o in range(0, 61):
    v = col(o, 4)
    nn = [x for x in v if x != 0xFFFFFFFF]
    if len(set(nn)) < 3:
        continue
    fits = []
    for t, N in NROWS.items():
        if max(nn) < N:
            fits.append(f"{t}({N},top={max(nn)},cov={max(nn)/N:.2f})")
    if fits:
        print(f"  u32@{o:2d} null={v.count(0xFFFFFFFF):4d} d={len(set(nn)):4d} max={max(nn)} -> {fits}")

print("\n== nonnull-count cross match (find gating partners) ==")
cnt = {}
for o in range(64):
    for w in (1, 2, 4):
        if o + w > 64:
            continue
        v = col(o, w)
        null = {1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF}[w]
        cnt[(o, w)] = sum(1 for x in v if x != null)
targets = {"date@19_nonnull": 253, "date@60_nonnull": 374}
for name, t in targets.items():
    hits = [(k, c) for k, c in cnt.items() if c == t]
    print(f"  {name}={t}: columns with same nonnull count -> {hits[:12]}")
