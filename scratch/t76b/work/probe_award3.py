"""t76b scratch: award(0) constraint-based field/slot matching (no XML order)."""
import runpy, sys, struct, json
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]
BIZ = 64

sch = json.loads(Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
fields = sch["entities"]["award.xml"][0]["fields"]
enums = sch["enums"]

print("== packed day/year check ==")
for off in (19, 60):
    v = [int.from_bytes(r[off:off + 4], "little") for r in rows]
    yrs = [x >> 16 for x in v]
    days = [x & 0xFFFF for x in v]
    print(f" off{off}: years {min(yrs)}..{max(yrs)} distinct={len(set(yrs))}; "
          f"days {min(days)}..{max(days)} distinct={len(set(days))}; "
          f"days<=366 all={all(d <= 366 for d in days)}")
    from collections import Counter
    print("   year top:", Counter(yrs).most_common(6))
    print("   day top:", Counter(days).most_common(6))

print("\n== integer fields with min/max ==")
for f in fields:
    if f.get("type") in ("integer", "enum") and ("min_value" in f or "max_value" in f):
        print(" ", f["field"], f.get("type"), f.get("min_value"), f.get("max_value"), f.get("default_value"))

print("\n== candidate columns by strict domain containment ==")
ints = [f for f in fields if f.get("type") == "integer" and "min_value" in f and "max_value" in f]
for f in ints:
    lo, hi = int(f["min_value"]), int(f["max_value"])
    hits = []
    for w in (1, 2):
        for off in range(0, BIZ - w + 1):
            vals = [int.from_bytes(r[off:off + w], "little") for r in rows]
            s = set(vals)
            if min(s) >= lo and max(s) <= hi and len(s) >= 2:
                hits.append((off, w, len(s), min(s), max(s)))
    print(f" {f['field']:6} [{lo},{hi}] -> {hits}")


def enum_dom(f):
    key = f.get("enum_ref") or f["field"]
    return {int(v["enum"]) for v in enums.get(key, {}).get("values", [])
            if str(v["enum"]).lstrip("-").isdigit()}


print("\n== enum fields: literal and two's-complement (u8) domain fits ==")
for f in fields:
    if f.get("type") != "enum":
        continue
    d = enum_dom(f)
    dneg = {x & 0xFF for x in d}
    fits = []
    for off in range(BIZ):
        vals = {r[off] for r in rows}
        if len(vals) >= 2 and (vals <= d or vals <= dneg):
            fits.append((off, sorted(vals)))
    print(f" {f['field']:6} dom={sorted(d)} -> fits={fits}")
