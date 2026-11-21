"""t81-fix1 probe71 — Icau mask test @18, payload identity, string presence."""
import hashlib
import itertools
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p71")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
icau = sorted(int(v["enum"]) for v in M["enums"]["Icau"]["values"])
base = [x for x in icau if x > 0]
masks = {0}
for k in range(1, len(base) + 1):
    for c in itertools.combinations(base, k):
        masks.add(sum(c))
print("Icau base bits:", base, "| max mask", max(masks), "| n masks", len(masks))

raw_s = core["load_payload"]("server", 6)
n = 115
for off, w in ((18, 2), (19, 1), (20, 1), (26, 1)):
    v = [int.from_bytes(raw_s[14 + j * 40 + off: 14 + j * 40 + off + w], "little")
         for j in range(n)]
    st = set(v)
    print(f"  off{off} w{w}: distinct={len(st)} subset_of_Icau_masks={st <= masks}"
          f" values={sorted(st)[:14]}")

print("\n--- payload identity client vs server")
for tid in (6, 23, 35):
    c = core["load_payload"]("client", tid)
    s = core["load_payload"]("server", tid)
    print(f"  t{tid}: equal={c == s} len={len(c)}/{len(s)} sha_c={hashlib.sha256(c).hexdigest()[:16]}"
          f" sha_s={hashlib.sha256(s).hexdigest()[:16]}")

print("\n--- printable ascii runs >=4 in payloads")
for tid in (6, 23, 35):
    for arc in ("client", "server"):
        raw = core["load_payload"](arc, tid)
        runs, cur = [], 0
        for b in raw:
            if 0x20 <= b < 0x7F:
                cur += 1
            else:
                if cur >= 4:
                    runs.append(cur)
                cur = 0
        if cur >= 4:
            runs.append(cur)
        print(f"  {arc}/{tid}: ascii_runs>=4 {len(runs)} longest={max(runs) if runs else 0}")
