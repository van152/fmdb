"""t81-fix1 probe75 — comp FK lanes: UID-set membership (not just range) + discrimination control."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p75")
IDX = json.loads((REPO / "scratch/t81/out/fk_index.json").read_text("utf-8"))

H, S, n, biz = 14, 127, 7047, 114
raw = core["load_payload"]("client", 25)

UIDS = {}
for tid in (6, 23, 35, 10):
    u = IDX["targets"][f"{tid}/client"]["uid_set"]
    UIDS[tid] = set(u["values"])
print("uid domain sizes:", {k: len(v) for k, v in UIDS.items()})

print("\n--- 4B columns: live values subset of a target UID set (rate==1.0)")
for off in range(0, biz - 3):
    v = [struct.unpack_from("<I", raw, H + j * S + off)[0] for j in range(n)]
    live = [x for x in v if x != 0xFFFFFFFF]
    if len(live) < n // 2:
        continue
    for tid in (6, 23, 35, 10):
        d = UIDS[tid]
        hit = sum(1 for x in live if x in d)
        if hit == len(live):
            print(f"  off{off:3d}: 100% of {len(live)} live values in t{tid} UID set "
                  f"(distinct={len(set(live))}, max={max(live)})")

print("\n--- discrimination control: off56 vs nation(251) and stage_name(278)")
v = [struct.unpack_from("<I", raw, H + j * S + 56)[0] for j in range(n)]
live = [x for x in v if x != 0xFFFFFFFF]
print("  live=%d/%d max=%d distinct=%d ff=%d" % (len(live), n, max(live), len(set(live)),
                                                 n - len(live)))
for tid, lim in ((10, 251), (23, 278), (35, 890), (6, 115)):
    inr = sum(1 for x in live if x < lim)
    print(f"   vs t{tid} range 0..{lim-1}: {inr}/{len(live)} in range "
          f"({inr/len(live):.4f})")
print("  -> ordinal-range test alone cannot separate 251/278/890 domains "
      "(any value <251 is also <278 and <890): non-discriminating.")
