"""t81-fix1 probe69 — icla=13 anomaly, off2 correlation, client/server byte equality."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p69")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
icla = {int(v["enum"]) for v in M["enums"]["icla"]["values"]}

rc = core["load_payload"]("client", 6)
rs = core["load_payload"]("server", 6)
n = 115
cb = [rc[14 + j * 16: 14 + j * 16 + 3] for j in range(n)]
sb = [rs[14 + j * 40: 14 + j * 40 + 27] for j in range(n)]

for k in range(3):
    print(f"client byte{k} == server byte{k}:",
          sum(1 for j in range(n) if cb[j][k] == sb[j][k]), "/", n)

print("\n--- rows where byte0 not in icla enum:", [(j, cb[j][0], cb[j][1]) for j in range(n)
                                                  if cb[j][0] not in icla])
print("--- (icla,iscl) pairs:", sorted({(cb[j][0], cb[j][1]) for j in range(n)})[:8], "...")
print("--- iscl set - master:", sorted({cb[j][1] for j in range(n)} - {
    int(v["enum"]) for v in M["enums"]["iscl"]["values"]}))

print("\n--- byte2 vs each server offset (agreement on binary split)")
y = [cb[j][2] for j in range(n)]
for off in range(27):
    x = [sb[j][off] for j in range(n)]
    if len(set(x)) < 2:
        continue
    agree = sum(1 for j in range(n) if (x[j] > 0) == (y[j] > 0))
    print(f"  off{off:2d} sign-agree={agree:3d}/{n}")
print(" byte2 count=1:", sum(y), "count=0:", n - sum(y))

print("\n--- percent-like columns (0..100 w/ 255 sentinel)")
for off in (7, 17, 24, 25, 26, 16, 18, 19, 20, 21):
    col = [sb[j][off] for j in range(n)]
    ff = col.count(255)
    print(f"  off{off:2d} ff={ff:3d} live_min={min([c for c in col if c != 255] or [0])}"
          f" live_max={max([c for c in col if c != 255] or [0])} distinct={len(set(col))}")
