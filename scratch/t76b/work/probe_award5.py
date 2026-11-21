"""t76b scratch: award(0) hypothesis tests H1-H4 (FK / dates / enums / widths)."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
SCH = json.loads(Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
EN = SCH["enums"]


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def var_uids(tid, n_from_header=True):
    raw = load(tid)
    n = u32(raw, 8)
    hi = len(raw) - 8
    ways = [defaultdict(int) for _ in range(n + 1)]
    prev = defaultdict(list)
    ways[0][14] = 1
    for j in range(n):
        for p in sorted(ways[j]):
            for e in range(p + 13, hi + 1):
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                if o == j and u1 == u2 != 0 and m == 0:
                    if e not in ways[j + 1]:
                        prev[(j + 1, e)].append(p)
                    ways[j + 1][e] += ways[j][p]
    ends = [e for e in ways[n] if ways[n][e]]
    e = max(ends)
    out = []
    for j in range(n, 0, -1):
        ps = [p for p in prev[(j, e)] if ways[j - 1].get(p, 0)]
        p = min(ps)
        out.append((p, e, u32(raw, e - 9), u32(raw, e - 13)))
        e = p
    out.reverse()
    return raw, out


raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]

# reference domains
cont = {1, 2, 3, 4, 5, 6, 7}
raw9, r9 = var_uids(9)
nation = {r[2] for r in r9}
nation_ord = {r[3] for r in r9}
raw25 = load(25)
comp = {u32(raw25, 14 + j * 127 + 118) for j in range(7047)}
raw2 = load(2)
city = {u32(raw2, 14 + j * 43 + 34) for j in range(56293)}
print("domains: continent %d nation %d (ord set %d) comp %d city %d" %
      (len(cont), len(nation), len(nation_ord), len(comp), len(city)))

print("\nH1: FK membership per u32 column (null = 0 or 0xffffffff)")
for off in (23, 27, 31, 41):
    v = [u32(r, off) for r in rows]
    nn = [x for x in v if x not in (0, 0xFFFFFFFF)]
    print(f" off{off}: nulls 0={v.count(0)} ff={v.count(0xFFFFFFFF)} "
          f"real={len(nn)} distinct={len(set(nn))}")
    for nm, dom in (("continent", cont), ("nation", nation), ("comp", comp), ("city", city)):
        h = sum(1 for x in nn if x in dom)
        print(f"    {nm}: {h}/{len(nn)} = {h / max(1, len(nn)):.4f}")
    print("    sample:", nn[:8])

print("\nH2: date dependency. For each (byte offset, value) check correlation with date@19/@60 set")
d19 = [int.from_bytes(r[19:21], "little") != 0 and int.from_bytes(r[21:23], "little") != 1900 for r in rows]
d60 = [int.from_bytes(r[62:64], "little") != 1900 for r in rows]
print(" date@19 set %d ; date@60 set %d ; both %d ; neither %d" %
      (sum(d19), sum(d60), sum(1 for i in range(n) if d19[i] and d60[i]),
       sum(1 for i in range(n) if not d19[i] and not d60[i])))
for off in range(64):
    vals = [r[off] for r in rows]
    for k in sorted(set(vals)):
        mask = [v == k for v in vals]
        c = sum(mask)
        if c < 30:
            continue
        h19 = sum(1 for i in range(n) if mask[i] and d19[i])
        h60 = sum(1 for i in range(n) if mask[i] and d60[i])
        if h19 / c > 0.9 or h60 / c > 0.9 or h19 / c < 0.02 or h60 / c < 0.02:
            print(f"   byte{off}=={k} ({c}) -> date19 {h19 / c:.2f} date60 {h60 / c:.2f}")

print("\nH3: width detection — for each offset, how often are the next bytes zero")
for off in range(0, 60):
    z1 = sum(1 for r in rows if r[off + 1] == 0)
    z2 = sum(1 for r in rows if r[off + 1] == 0 and r[off + 2] == 0)
    z3 = sum(1 for r in rows if r[off + 1] == 0 and r[off + 2] == 0 and r[off + 3] == 0)
    if z3 == n or z2 == n or z1 == n:
        print(f" off{off:2d}: next1_zero={z1}/{n} next2={z2} next3={z3}")

print("\nH4: enum domain fits with full-domain-used flag")
for f in SCH["entities"]["award.xml"][0]["fields"]:
    if f.get("type") != "enum":
        continue
    key = f.get("enum_ref") or f["field"]
    dom = {int(v["enum"]) for v in EN.get(key, {}).get("values", []) if str(v["enum"]).lstrip("-").isdigit()}
    for off in range(64):
        vals = {r[off] for r in rows}
        if len(vals) >= 2 and vals <= dom:
            print(f" {f['field']:5} off{off:2d} used={len(vals)}/{len(dom)} "
                  f"full={vals == dom} vals={sorted(vals)}")
