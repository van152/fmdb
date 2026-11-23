"""t81-fix1 probe62 — enum/mask containment tests for injury(6)."""
import itertools
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p62")
S = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
E = {n: sorted(int(v["enum"]) for v in S["enums"][n]["values"]
               if str(v["enum"]).lstrip("-").isdigit())
     for n in ("icla", "iscl", "inSr", "Iagr", "Icms", "Icau")}


def masks(nmax=3):
    base = [x for x in E["Icau"] if x > 0]           # 1,2,4,...,4096
    out = {0}
    for k in range(1, nmax + 1):
        for c in itertools.combinations(base, k):
            out.add(sum(c))
    return out


SP = {("client", 6): (14, 16, 115, 3), ("server", 6): (14, 40, 115, 27)}
for (arc, tid), (H, Sx, n, biz) in SP.items():
    raw = core["load_payload"](arc, tid)
    print(f"===== {arc}/{tid} biz={biz}")
    for off in range(biz):
        res = []
        for w in (1, 2):
            if off + w > biz:
                continue
            v = [int.from_bytes(raw[H + j * Sx + off: H + j * Sx + off + w], "little")
                 for j in range(n)]
            st = set(v)
            for name, dom in E.items():
                if name == "Icau":
                    continue
                if w == 1 and st <= set(dom):
                    exact = st == set(dom)
                    res.append(f"{name}(w{w}{',exact' if exact else ''},"
                               f"{len(st)}/{len(dom)})")
            if st <= {0, 1}:
                res.append(f"bool(w{w})")
        # bitmask test on 2B and 4B
        for w in (2, 4):
            if off + w > biz:
                continue
            v = [int.from_bytes(raw[H + j * Sx + off: H + j * Sx + off + w], "little")
                 for j in range(n)]
            st = set(v)
            for k in (1, 2, 3):
                m = masks(k)
                if st <= m:
                    res.append(f"Icau<=k{k}(w{w},{len(st)}d)")
        if res:
            print(f"  off{off:2d}: {', '.join(res)}")
