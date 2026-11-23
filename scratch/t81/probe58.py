"""t81-fix1 probe58 — dump rows for 6/23/35 (hex + interpretation)."""
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p58")
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]

SPEC = {6: {"client": (14, 16, 115, 3), "server": (14, 40, 115, 27)},
        23: {"client": (14, 14, 278, 1), "server": (14, 14, 278, 1)},
        35: {"client": (14, 15, 890, 2), "server": (14, 15, 890, 2)}}

for tid in (6, 23, 35):
    for arc in ("client", "server"):
        raw = core["load_payload"](arc, tid)
        H, S, n, p = SPEC[tid][arc]
        print(f"===== {arc}/{tid} H={H} S={S} n={n} p={p} len={len(raw)}")
        print("  header[0:14]:", raw[:14].hex())
        for j in (0, 1, 2):
            r = raw[H + j * S: H + j * S + S]
            print(f"   row{j}: {r.hex()}  biz={r[:p].hex()}")
        r = raw[H + (n - 1) * S: H + (n - 1) * S + S]
        print(f"   row{n-1}: {r.hex()}  biz={r[:p].hex()}")
        print("  footer[-8:]:", raw[-8:].hex())
        # is there a trailing region beyond the identity trailer? check marker byte
        print("  marker bytes set:", sorted({raw[H + j * S + S - 1] for j in range(n)}))
        print("  biz cols distinct:", [len({raw[H + j * S + k] for j in range(n)})
                                      for k in range(p)])
