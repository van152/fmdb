"""t76b scratch: award(0) enum subset/coverage search at u8/u16/u32 widths."""
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

raw = D["load_payload"](C, "client", 0)
n = struct.unpack_from("<I", raw, 8)[0]
S = (len(raw) - 22) // n
rows = [raw[14 + j * S:14 + (j + 1) * S] for j in range(n)]


def col(o, w):
    return [int.from_bytes(r[o:o + w], "little") for r in rows]


print("== enum subset/coverage scan (u8/u16/u32), require >=60% domain coverage ==")
found = []
for w in (1, 2, 4):
    for o in range(0, 65 - w):
        v = col(o, w)
        null = {1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF}[w]
        nn = {x for x in v if x != null}
        if len(nn) < 2:
            continue
        for f, d in AW_ENUM.items():
            if not d or not (nn <= d):
                continue
            cov = len(nn) / len(d)
            if cov >= 0.6:
                found.append((cov, f, o, w, len(nn), len(d), sorted(nn)[:8],
                              sum(1 for x in v if x == null)))
for cov, f, o, w, k, dn, sample, nulls in sorted(found, reverse=True):
    print(f"  {f:5s} u{w*8}@{o:2d} cov={cov:.2f} obs={k}/{dn} null={nulls:4d} {sample}")

print("\n== three-FK assignment check ==")
for o, w, t in ((23, 4, "continent"), (27, 4, "nation"), (41, 4, "comp")):
    v = col(o, w)
    nn = [x for x in v if x != 0xFFFFFFFF]
    N = NROWS[t]
    print(f"  u32@{o}: {t}({N}) nonnull={len(nn)} max={max(nn)} "
          f"underN={sum(1 for x in nn if x < N)}/{len(nn)} "
          f"distinct={len(set(nn))} topfrac={max(nn)/N:.3f}")
