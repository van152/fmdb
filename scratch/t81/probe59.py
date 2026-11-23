"""t81-fix1 probe59 — column profiling for 6/23/35 business regions."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p59")

SPEC = {6: {"client": (14, 16, 115, 3), "server": (14, 40, 115, 27)},
        23: {"client": (14, 14, 278, 1), "server": (14, 14, 278, 1)},
        35: {"client": (14, 15, 890, 2), "server": (14, 15, 890, 2)}}


def cols(raw, H, S, n, p):
    out = []
    for off in range(p):
        b = bytes(raw[H + j * S + off] for j in range(n))
        d = {"off": off, "u8_distinct": len(set(b)), "u8": sorted(set(b))[:10]}
        if off + 2 <= p:
            v = [struct.unpack_from("<H", raw, H + j * S + off)[0] for j in range(n)]
            d["u16"] = {"min": min(v), "max": max(v), "distinct": len(set(v))}
        if off + 4 <= p:
            v = [struct.unpack_from("<I", raw, H + j * S + off)[0] for j in range(n)]
            d["u32"] = {"min": min(v), "max": max(v), "distinct": len(set(v)),
                        "n_ff": v.count(0xFFFFFFFF), "n_zero": v.count(0)}
            f = [struct.unpack_from("<f", raw, H + j * S + off)[0] for j in range(n)]
            fin = [x for x in f if x == x and abs(x) != float("inf")]
            d["f32"] = {"n": len(f), "finite": len(fin),
                        "min": min(fin) if fin else None,
                        "max": max(fin) if fin else None}
        out.append(d)
    return out


res = {}
for tid in (6, 23, 35):
    for arc in ("client", "server"):
        raw = core["load_payload"](arc, tid)
        H, S, n, p = SPEC[tid][arc]
        res[f"{arc}/{tid}"] = {"len": len(raw), "biz": p, "cols": cols(raw, H, S, n, p)}
        print(f"== {arc}/{tid} biz={p}")
        for d in res[f"{arc}/{tid}"]["cols"]:
            print("  ", json.dumps(d, ensure_ascii=False)[:180])

# client prefix vs server prefix for t6
raw_c = core["load_payload"]("client", 6)
raw_s = core["load_payload"]("server", 6)
same = sum(1 for j in range(115)
           if raw_c[14 + j * 16: 14 + j * 16 + 3] == raw_s[14 + j * 40: 14 + j * 40 + 3])
print("t6 client biz3 == server biz[:3]:", same, "/115")

Path(REPO / "scratch/t81/out2/_probe_cols.json").write_text(
    json.dumps(res, indent=1), encoding="utf-8")
