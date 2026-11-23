"""t81-fix1 probe74 — inbound FK lane scan: comp(25) 4B columns vs t6/23/35 ordinal domains."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p74")
IDX = json.loads((REPO / "scratch/t81/out/fk_index.json").read_text("utf-8"))

# comp client frame from fk_index (do not re-derive): 127B stride, identity row_end-13
t = IDX["targets"]["25/client"]
H, S, n = 14, t["window"][1], t["row_count"]
biz = S - t["identity_width"]
raw = core["load_payload"]("client", 25)
print(f"comp client: H={H} S={S} n={n} biz={biz} len={len(raw)}")
print("  closure check:", H + S * n + 8 == len(raw))

DOM = {tid: IDX["rollup"][str(tid)]["row_count"] for tid in (6, 23, 35)}
print("  target domains:", DOM)

print("\n--- 4B columns whose live values all fall in a target's ordinal range")
for off in range(0, biz - 3):
    v = [struct.unpack_from("<I", raw, H + j * S + off)[0] for j in range(n)]
    live = [x for x in v if x != 0xFFFFFFFF]
    if not live:
        continue
    for tid, lim in DOM.items():
        if all(0 <= x < lim for x in live):
            print(f"  off{off:3d}: in 0..{lim-1} (t{tid}) live={len(live)}/{n} "
                  f"max={max(live)} distinct={len(set(live))} "
                  f"coverage={len(set(live))/lim:.3f}")

print("\n--- declared FK fields pointing at injury/stage_name/description")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
for xml, ents in M["entities"].items():
    for e in ents:
        for f in e["fields"]:
            if f.get("database_table_type") in ("injury", "stage_name", "description") \
                    and f.get("type") == "database_record_unique_id":
                print(f"  {xml}#{e['id']} {f['field']} -> {f['database_table_type']}")
