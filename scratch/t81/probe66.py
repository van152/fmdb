"""t81-fix1 probe66 — per-row client/server prefix equality + declared-range feasibility."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p66")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))

raw_c = core["load_payload"]("client", 6)
raw_s = core["load_payload"]("server", 6)
n = 115
p3 = sum(1 for j in range(n) if raw_c[14 + j * 16: 14 + j * 16 + 3] ==
         raw_s[14 + j * 40: 14 + j * 40 + 3])
print("t6 client 3B business == server 3B business, per row:", p3, "/", n)

print("\n--- declared min/max feasibility (server 27B)")
for f in M["entities"]["injury.xml"][0]["fields"]:
    if f["type"] not in ("integer",):
        continue
    lo = int(f.get("min_value", 0))
    hi = int(f.get("max_value", 1 << 31))
    feas = []
    for w, fmt in ((1, "<B"), (2, "<H")):
        for off in range(0, 27 - w + 1):
            v = [struct.unpack_from(fmt, raw_s, 14 + j * 40 + off)[0] for j in range(n)]
            live = [x for x in v if x != 0xFF if w == 1] if w == 1 else v
            if all(lo <= x <= hi for x in live):
                feas.append(f"u{w*8}@{off}")
    print(f"  {f['field']:5s} {lo}..{hi:4d} : {' '.join(feas) if feas else '-'}")

print("\n--- boolean set per offset (server)")
for off in range(27):
    col = {raw_s[14 + j * 40 + off] for j in range(n)}
    if col <= {0, 1}:
        print(f"  off{off:2d} bool {sorted(col)}")
