"""t81-fix1 probe67 — full per-offset value lists (server 6) + client/server byte correlation."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p67")

raw_c = core["load_payload"]("client", 6)
raw_s = core["load_payload"]("server", 6)
n = 115
cs = [raw_c[14 + j * 16: 14 + j * 16 + 3] for j in range(n)]
ss = [raw_s[14 + j * 40: 14 + j * 40 + 27] for j in range(n)]

print("--- client byte 2 vs every server byte (identical column test)")
for off in range(27):
    if all(cs[j][2] == ss[j][off] for j in range(n)):
        print(f"   client[2] == server[{off}] on all 115 rows")

print("\n--- u16 columns at 3 and 5")
for off in (3, 5):
    v = [struct.unpack_from("<H", raw_s, 14 + j * 40 + off)[0] for j in range(n)]
    print(f"  u16@{off}: min={min(v)} max={max(v)} distinct={len(set(v))} vals={sorted(set(v))}")
print("  u16@3 <= u16@5 on", sum(1 for j in range(n)
      if struct.unpack_from("<H", raw_s, 14 + j * 40 + 3)[0]
      <= struct.unpack_from("<H", raw_s, 14 + j * 40 + 5)[0]), "/115")

print("\n--- f32 at 13 (Iocr candidate)")
v = [struct.unpack_from("<f", raw_s, 14 + j * 40 + 13)[0] for j in range(n)]
print("   min", min(v), "max", max(v), "distinct", len(set(v)))
print("   sample", [round(x, 4) for x in v[:12]])

print("\n--- full value lists per offset")
for off in range(27):
    col = [ss[j][off] for j in range(n)]
    print(f"  off{off:2d} d={len(set(col)):3d} {sorted(set(col))[:16]}")
