"""t81-fix1 probe72 — mask negative control + inbound FK lanes into 6/23/35."""
import itertools
import json
import runpy
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p72")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
base = [int(v["enum"]) for v in M["enums"]["Icau"]["values"] if int(v["enum"]) > 0]
masks = {0}
for k in range(1, len(base) + 1):
    for c in itertools.combinations(base, k):
        masks.add(sum(c))

raw_s = core["load_payload"]("server", 6)
n = 115
print("--- negative control: every offset/window tested against Icau mask set")
for w in (1, 2):
    ok = []
    for off in range(0, 27 - w + 1):
        v = {int.from_bytes(raw_s[14 + j * 40 + off: 14 + j * 40 + off + w], "little")
             for j in range(n)}
        if v <= masks:
            ok.append((off, len(v)))
    print(f"  w{w}: {len(ok)} windows pass ->", ok)
print("  mask-space density:", len(masks), "/", 2 ** (13 * 1), "for u16 =",
      round(len(masks) / 65536, 4))

print("\n--- inbound FK lanes (fk_index targets that are 6/23/35)")
IDX = json.loads((REPO / "scratch/t81/out/fk_index.json").read_text("utf-8"))
for k, t in IDX["targets"].items():
    if t["table"] in (6, 23, 35):
        print(f"  {k}: rows={t['row_count']} status={t['status']} "
              f"identity_width={t['identity_width']}")
print("\n--- rollup for 6/23/35")
for tid in ("6", "23", "35"):
    r = IDX["rollup"].get(tid)
    print("  ", tid, json.dumps(r, ensure_ascii=False)[:200])
