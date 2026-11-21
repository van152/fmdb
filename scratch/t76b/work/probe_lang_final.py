"""t76b scratch: language(8) 17B pre-region vs Lfam/Lgro/Lsub enum domains."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
SCH = json.loads((Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json")
                  ).read_text(encoding="utf-8"))
EN = SCH["enums"]


def ids(name):
    out = set()
    for v in EN[name]["values"]:
        try:
            out.add(int(v["enum"]))
        except (TypeError, ValueError):
            pass
    return out


L = {k: ids(k) for k in ("Lfam", "Lgro", "Lsub")}
for k, v in L.items():
    print(f"{k}: n={len(v)} min={min(v)} max={max(v)}")

for arch in ("client", "server"):
    raw = D["load_payload"](C, arch, 8)
    nc = struct.unpack_from("<I", raw, 8)[0]
    pos, rows = 14, []
    for j in range(nc):
        k = struct.unpack_from("<I", raw, pos)[0]
        rows.append({"j": j, "k": k,
                     "name": raw[pos + 4:pos + 4 + k],
                     "pre": raw[pos + 4 + k:pos + 4 + k + 17],
                     "trail": raw[pos + 4 + k + 17:pos + 4 + k + 30]})
        pos += 4 + k + 30
    print(f"\n=== language {arch} n={nc} close={pos + 8 == len(raw)}")
    for o in range(17):
        v = [r["pre"][o] for r in rows]
        s = set(v)
        if len(s) < 2:
            continue
        m = []
        for f, d in L.items():
            if s <= d:
                m.append(f"{f}({len(s)}/{len(d)}={len(s)/len(d):.2f})")
        print(f"  pre{o:2d} d={len(s):3d} min={min(s):3d} max={max(s):3d} "
              f"{'ENUMFIT ' + ' '.join(m) if m else ''}")
    # hierarchy test: family->group->subgroup should be nested
    p1 = [r["pre"][1] for r in rows]
    p2 = [r["pre"][2] for r in rows]
    p3 = [r["pre"][3] for r in rows]
    for a, b, na, nb in ((1, 2, "pre1", "pre2"), (2, 3, "pre2", "pre3"), (1, 3, "pre1", "pre3")):
        va = [r["pre"][a] for r in rows]
        vb = [r["pre"][b] for r in rows]
        mp = {}
        ok = True
        for x, y in zip(va, vb):
            if mp.setdefault(x, y) != y:
                ok = False
        print(f"  functional dep {na}->{nb}: {ok}")
    # infin/diff ints 0..20
    print("  pre9 range", min(r['pre'][9] for r in rows), max(r['pre'][9] for r in rows))
    print("  pre13 range", min(r['pre'][13] for r in rows), max(r['pre'][13] for r in rows))
    print("  pre5 max", max(r['pre'][5] for r in rows),
          "pre7 max", max(r['pre'][7] for r in rows))
    # nation ordinal? 0..250
    for o in (1, 2, 3, 5, 7):
        v = [r["pre"][o] for r in rows]
        print(f"   pre{o} <=250 all: {all(x <= 250 for x in v)}")
