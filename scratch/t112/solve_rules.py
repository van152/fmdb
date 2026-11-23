"""t112b: solve a clean row-length rule rowlen = base + u32@k for every variable table."""
import struct, json, pathlib, runpy
ROOT = pathlib.Path(r"D:\tmp2b\fm24-db")
NY = runpy.run_path(str(ROOT/"scripts/fm24_dump.py")); codec = NY["_reader"]()
HDR, FTR = 14, 8
VARS = [("client",8),("client",18),("client",27),("client",47),
        ("server",8),("server",12),("server",18),("server",27),("server",32),
        ("server",45),("server",47),("server",48),("server",59),("server",72)]

def ident_ok(raw, t, i):
    return (struct.unpack_from("<I", raw, t)[0] == i
            and struct.unpack_from("<I", raw, t+4)[0] == struct.unpack_from("<I", raw, t+8)[0]
            and raw[t+12] == 0)

def cand_ends(raw, pos, i, hi=400):
    return [t for t in range(pos+13, min(pos+hi, len(raw)-13)+1) if ident_ok(raw, t, i)]

def verify(raw, n, base, k, width=4):
    pos = HDR
    for i in range(n):
        if pos + k + width > len(raw): return None
        v = struct.unpack_from("<I" if width==4 else "<H", raw, pos+k)[0]
        L = base + v
        if L < 13 or pos + L > len(raw): return None
        if not ident_ok(raw, pos+L-13, i): return None
        pos += L
    return pos

def solve(a, t):
    raw = NY["load_payload"](codec, a, t)
    n = struct.unpack_from("<I", raw, 8)[0]
    ends0 = cand_ends(raw, HDR, 0)
    good = []
    for width, tag in ((4, "u32"), (2, "u16")):
        for k in range(0, 90):
            if HDR + k + width > len(raw): break
            v = struct.unpack_from("<I" if width==4 else "<H", raw, HDR+k)[0]
            for t0 in ends0:
                L0 = t0 + 13 - HDR
                base = L0 - v
                if base < 13: continue
                end = verify(raw, n, base, k, width)
                if end == len(raw) - FTR:
                    good.append({"base": base, "len_at": k, "width": tag, "rows": n,
                                 "rowlen_min": base, "end": end})
        if good: break
    return {"archive": a, "table_id": t, "payload": len(raw), "count": n, "rules": good,
            "row0_candidate_ends": [x-HDR+13 for x in ends0]}

res = []
for a, t in VARS:
    r = solve(a, t); res.append(r)
    print(f"{a}/{t}: n={r['count']} rules={[(x['base'],x['len_at'],x['width']) for x in r['rules']][:4]} cand0={r['row0_candidate_ends']}")
pathlib.Path(ROOT/"scratch/t112/rules.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
