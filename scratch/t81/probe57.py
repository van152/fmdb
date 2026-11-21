"""t81-fix1 probe57 — structural frame for 6/23/35: count@8 + closure + identity."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p57")


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


rows_out = {}
for tid in (6, 23, 35):
    for arc in ("client", "server"):
        raw = core["load_payload"](arc, tid)
        L = len(raw)
        n_hdr = u32(raw, 8)
        magic = raw[:6]
        # candidate strides: those with (L - 14 - 8) % n == 0
        body = L - 14 - 8
        cands = [body // n_hdr] if n_hdr and body % n_hdr == 0 else []
        # also allow any S with closure and count==n_hdr
        info = {"len": L, "count_hdr": n_hdr, "magic": magic.hex(),
                "body": body, "stride": cands[0] if cands else None}
        if cands:
            S = cands[0]
            H = 14
            # identity scan over every offset
            hits = []
            for p in range(0, S - 12 + 1):
                ord_ok = uid_ok = 0
                for j in range(n_hdr):
                    b = H + j * S + p
                    if u32(raw, b) == j:
                        ord_ok += 1
                    if u32(raw, b + 4) == u32(raw, b + 8) != 0:
                        uid_ok += 1
                if ord_ok == n_hdr or uid_ok == n_hdr:
                    hits.append({"p": p, "ord": ord_ok, "uid": uid_ok})
            info["identity_hits"] = hits
            # alias group: (H,F) pairs with same S and same absolute identity site
            if hits:
                p = hits[0]["p"]
                q = H + p
                alias = [{"H": h, "F": L - h - S * n_hdr, "p": q - h}
                         for h in range(0, 30)
                         if L - h - S * n_hdr >= 0]
                info["alias_group"] = alias
                info["footer_flag_be1"] = {a["F"]: int.from_bytes(
                    raw[L - a["F"]:L - a["F"] + 4], "big") == 1
                    for a in alias if a["F"] >= 4}
        rows_out[f"{arc}/{tid}"] = info
        print(f"== {arc}/{tid} len={L} count_hdr={n_hdr} stride={info.get('stride')}"
              f" magic={info['magic']}")
        print("   hits:", json.dumps(info.get("identity_hits"), ensure_ascii=False)[:400])
        print("   alias:", json.dumps(info.get("alias_group"), ensure_ascii=False)[:500])
        print("   footBE1:", json.dumps(info.get("footer_flag_be1"), ensure_ascii=False))
        print("   tail8:", raw[-8:].hex())

Path(REPO / "scratch/t81/out2/_probe_struct.json").write_text(
    json.dumps(rows_out, indent=1), encoding="utf-8")
