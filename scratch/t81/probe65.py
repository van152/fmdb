"""t81-fix1 probe65 — payload identity vs fk_index uid_set sha256 (re-derivation test)."""
import hashlib
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p65")
IDX = json.loads((REPO / "scratch/t81/out/fk_index.json").read_text("utf-8"))
SPEC = {6: {"client": (14, 16, 115, 3), "server": (14, 40, 115, 27)},
        23: {"client": (14, 14, 278, 1), "server": (14, 14, 278, 1)},
        35: {"client": (14, 15, 890, 2), "server": (14, 15, 890, 2)}}
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]

for tid, arcs in SPEC.items():
    for arc, (H, S, n, p) in arcs.items():
        raw = core["load_payload"](arc, tid)
        uids = [u32(raw, H + j * S + p + 4) for j in range(n)]
        ordn = [u32(raw, H + j * S + p) for j in range(n)]
        rec = IDX["targets"][f"{tid}/{arc}"]["uid_set"]
        cands = {
            "json_compact": hashlib.sha256(json.dumps(uids, separators=(",", ":")).encode()).hexdigest(),
            "json_spaces": hashlib.sha256(json.dumps(uids).encode()).hexdigest(),
            "csv": hashlib.sha256(",".join(map(str, uids)).encode()).hexdigest(),
            "concat_u32le": hashlib.sha256(b"".join(struct.pack("<I", u) for u in uids)).hexdigest(),
            "newline": hashlib.sha256("\n".join(map(str, uids)).encode()).hexdigest(),
        }
        hit = [k for k, v in cands.items() if v == rec["sha256"]]
        print(f"{tid}/{arc}: sha_match={hit} | len={len(raw)} "
              f"sha256={hashlib.sha256(raw).hexdigest()[:16]} | "
              f"ord_eq={sum(1 for j, o in enumerate(ordn) if o == j)}/{n} | "
              f"uid_min={min(uids)} max={max(uids)} distinct={len(set(uids))}")
        print(f"   idx: count={rec['count']} min={rec['min']} max={rec['max']} "
              f"distinct={rec['distinct']} first5={rec['values'][:5]}")
