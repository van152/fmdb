"""t76b scratch: consolidated discriminators — award dependency test, language FK/enums, media prefix."""
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


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


# ---------- award ----------
raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]
da_set = [int.from_bytes(r[19:21], "little") for r in rows]
yrs = [int.from_bytes(r[21:23], "little") for r in rows]
ann_yrs = [int.from_bytes(r[62:64], "little") for r in rows]
sel = [j for j in range(n) if yrs[j] != 1900]
print("A. rows with off19 date set:", len(sel))
print("   off60 also set:", sum(1 for j in sel if ann_yrs[j] != 1900))
print("   AWdr==6 test: which byte is constant 6 over the 253 rows?")
for off in range(64):
    vals = {rows[j][off] for j in sel}
    if vals == {6}:
        print(f"     byte{off}: ALL 6 over selected rows; overall dist={sorted({r[off] for r in rows})}")
# check the reverse: AWdr!=6 -> date null
print("   colour triples: 3 consecutive bytes, all rows, low-ish range")
for off in range(0, 62):
    tri = [r[off:off + 3] for r in rows]
    if all(max(t) <= 0xFF for t in tri) and len({t for t in tri}) > 1:
        pair = sum(1 for t in tri if t[1] == t[2])
        if pair > n * 0.7:
            print(f"     off{off}..{off + 2}: g==b in {pair}/{n}; distinct={len(set(tri))} "
                  f"sample={[t.hex() for t in tri[:4]]}")

# ---------- language ----------
raw8 = load(8)
pos, L8 = 14, []
for j in range(126):
    k = u32(raw8, pos)
    L8.append({"j": j, "k": k, "name": raw8[pos + 4:pos + 4 + k],
               "pre": raw8[pos + 4 + k:pos + 4 + k + 17],
               "tr": raw8[pos + 4 + k + 17:pos + 4 + k + 30]})
    pos += 4 + k + 30
raw9 = load(9)
# nation UID domain
nat = set()
from collections import defaultdict
ways = [defaultdict(int) for _ in range(252)]
ways[0][14] = 1
hi = len(raw9) - 8
for j in range(251):
    for p in sorted(ways[j]):
        for e in range(p + 13, hi + 1):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw9, e - 13)
            if o == j and u1 == u2 != 0 and m == 0:
                ways[j + 1][e] += 1
    if j == 250:
        break
e = max([x for x in ways[251] if ways[251][x]])
for j in range(251, 0, -1):
    nat.add(u32(raw9, e - 9))
    # step back: find predecessor (first with ways>0) just scan
    ps = [p for p in range(14, e - 12)
          if ways[j - 1].get(p, 0) and struct.unpack_from("<IIIB", raw9, e - 13)[0] == j - 1]
    e = ps[0] if ps else 14
nat = {x for x in nat if x}
print("\nB. language: nation domain size", len(nat), "sample", sorted(nat)[:6])
for off in range(0, 14):
    vals = [u32(r["pre"], off) for r in L8]
    h = sum(1 for v in vals if v in nat)
    if h:
        print(f"   pre u32@{off}: nation hits {h}/{126}")
for f in ("Lfam", "Lgro", "Lsub"):
    dom = {int(v["enum"]) for v in EN.get(f, {}).get("values", []) if str(v["enum"]).lstrip("-").isdigit()}
    fits = []
    for off in range(17):
        vals = {r["pre"][off] for r in L8}
        if len(vals) >= 2 and vals <= dom:
            fits.append((off, len(vals), sorted(vals)[:6]))
    print(f"   {f}: dom={len(dom)} {sorted(dom)[:8]}.. fits={fits}")
for off in range(17):
    vals = [r["pre"][off] for r in L8]
    print(f"   pre{off:2d}: d={len(set(vals)):3d} min={min(vals)} max={max(vals)}")

# ---------- media ----------
raw7 = load(7)
pos, M7 = 14, []
for j in range(208):
    k = u32(raw7, pos)
    # walk forward to identity trailer with next-row anchor
    for e in range(pos + 13 + 4 + k, len(raw7) - 8 + 1):
        o, u1, u2, m = struct.unpack_from("<IIIB", raw7, e - 13)
        if o == j and u1 == u2 != 0 and m == 0 and (e == len(raw7) - 8 or u32(raw7, e) <= 64):
            break
    M7.append({"j": j, "start": pos, "end": e, "k": k,
               "name": raw7[pos + 4:pos + 4 + k],
               "six": raw7[pos + 4 + k:pos + 10 + k],
               "ul": u32(raw7, pos + 10 + k),
               "url": raw7[pos + 14 + k:pos + 14 + k + u32(raw7, pos + 10 + k)]})
    pos = e
print("\nC. media rows", len(M7), "end", pos, "footer", len(raw7) - pos)
six = Counter(m["six"] for m in M7)
print("   6B prefixes:", [(h.hex(), c) for h, c in six.most_common(12)])
for i in range(6):
    vals = sorted({m["six"][i] for m in M7})
    print(f"   six[{i}]: d={len(vals)} {vals[:14]}")
print("   url_len: zero rows", sum(1 for m in M7 if m["ul"] == 0),
      "range", min(m["ul"] for m in M7), max(m["ul"] for m in M7))
print("   hashtag search: does any row have a second length-prefixed string after url?")
cnt = 0
for m in M7[:20]:
    body = raw7[m["start"]:m["end"]]
    a = 14 + m["k"] + m["ul"]
    cand = u32(body, a)
    print(f"     row{m['j']}: after-url u32={cand} midlen={len(body) - 18 - a}")
