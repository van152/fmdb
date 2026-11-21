"""t81-fix1 probe56 — frame self-proof for injury(6)/stage_name(23)/description(35)."""
import json
import runpy
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p56")


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def main():
    out = {}
    for tid in (6, 23, 35):
        for arc in ("client", "server"):
            raw = core["load_payload"](arc, tid)
            cf = core["canonical_frame"](raw)
            fc = core["frame_closure"](raw, min_rows=1)
            rec = {
                "len": len(raw),
                "canon": {k: cf.get(k) for k in
                          ("resolved", "why", "stride", "count", "header", "footer",
                           "identity_offset", "identity_abs", "alias_group",
                           "alias_size", "header_origin_data_unique", "footer",
                           "closure", "full_identity", "arith_candidates")},
                "closed_n": len(fc["closed"]),
                "closed": [{k: c[k] for k in ("header", "footer", "stride", "count",
                                              "identity_offset", "mode")}
                           for c in fc["closed"]],
            }
            out[f"{arc}/{tid}"] = rec
            print(f"== {arc}/{tid} len={len(raw)}")
            print("   canon:", json.dumps(rec["canon"], ensure_ascii=False))
            print("   closed:", json.dumps(rec["closed"], ensure_ascii=False))
    Path(REPO / "scratch/t81/out2").mkdir(parents=True, exist_ok=True)
    (REPO / "scratch/t81/out2/_probe_frames.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")


main()
