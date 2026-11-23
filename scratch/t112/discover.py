"""t112b discovery: classify every (archive, table) payload into a row model.

fixed   : stride = (len-14-8)/count and every row ends with identity (i,dbid,uid,0)
variable: identity-scan row walk -> row-length rule inference
"""
import struct, json, pathlib, runpy, collections
ROOT = pathlib.Path(r"D:\tmp2b\fm24-db")
NY = runpy.run_path(str(ROOT/"scripts/fm24_dump.py"))
codec = NY["_reader"]()
HDR, FTR = 14, 8

def payload(a, t):
    return NY["load_payload"](codec, a, t)

def ident_ok(raw, t, i):
    return (struct.unpack_from("<I", raw, t)[0] == i
            and struct.unpack_from("<I", raw, t+4)[0] == struct.unpack_from("<I", raw, t+8)[0]
            and raw[t+12] == 0)

def try_fixed(raw):
    if len(raw) < HDR+FTR: return None
    n = struct.unpack_from("<I", raw, 8)[0]
    if not n: return None
    body = len(raw) - HDR - FTR
    if body % n: return None
    st = body // n
    if st < 13: return None
    bad = [i for i in range(n) if not ident_ok(raw, HDR+i*st+st-13, i)]
    return {"stride": st, "count": n, "bad_rows": len(bad), "first_bad": bad[:3]}

def scan_rows(raw, n, lo=13, hi=400):
    pos, lens = HDR, []
    for i in range(n):
        found = None
        for t in range(pos+lo-13, min(pos+hi-13, len(raw)-13)+1):
            if ident_ok(raw, t, i):
                found = t; break
        if found is None: return None, pos, i
        lens.append(found + 13 - pos)
        pos = found + 13
    return lens, pos, n

def rule_probe(raw, lens):
    """try rowlen = base + u32@k on each row; return all matching (base,k)."""
    hits = []
    for k in range(0, min(60, min(lens))):
        base = lens[0] - struct.unpack_from("<I", raw, HDR+k)[0]
        if base < 13: continue
        pos = HDR; ok = True
        for i, L in enumerate(lens):
            if base + struct.unpack_from("<I", raw, pos+k)[0] != L: ok=False; break
            pos += L
        if ok: hits.append({"base": base, "len_at": k})
    return hits

out = {}
for a in ("client", "server"):
    ents = codec["list_tables"](NY["DB_DIR"]/f"{a}_db.dat", f"{a}_db.dat")
    for e in sorted((x for x in ents if isinstance(x.get("table_id"), int)), key=lambda x: x["table_id"]):
        t = e["table_id"]
        try: raw = payload(a, t)
        except Exception as ex:
            out[f"{a}/{t}"] = {"error": str(ex)[:120]}; continue
        n = struct.unpack_from("<I", raw, 8)[0] if len(raw) >= 12 else 0
        rec = {"payload": len(raw), "count": n, "ver": hex(struct.unpack_from("<H", raw, 6)[0]) if len(raw)>=8 else None}
        f = try_fixed(raw)
        if f and f["bad_rows"] == 0:
            rec.update(model="fixed", stride=f["stride"])
        else:
            rec["fixed_attempt"] = f
            if n:
                lens, pos, done = scan_rows(raw, n)
                if lens:
                    rec.update(model="variable", rows=len(lens), walk_end=pos,
                               end_ok=(pos == len(raw)-FTR), len_min=min(lens), len_max=max(lens),
                               rules=rule_probe(raw, lens))
                else:
                    rec.update(model="variable_scan_fail", stopped_row=done, stopped_pos=pos)
        out[f"{a}/{t}"] = rec
pathlib.Path(ROOT/"scratch/t112/discover.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for k, v in out.items():
    if v.get("model") == "fixed":
        print(f"{k:12s} fixed stride={v['stride']:<4d} n={v['count']}")
    elif v.get("model") == "variable":
        print(f"{k:12s} VAR rows={v['rows']} len={v['len_min']}..{v['len_max']} end_ok={v['end_ok']} rules={v['rules'][:3]}")
    else:
        print(f"{k:12s} ?? {str(v)[:150]}")
