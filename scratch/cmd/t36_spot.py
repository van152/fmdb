# -*- coding: utf-8 -*-
"""t36_spot.py — commander independent full-table check of sol t36 Cdbt.
sol hit usage limit after cursor+fields (5/5 L3) but before REPORT/verify/DONE.
Validates: closure 2560333, cash i32 domain, sour i8 enum, stdt/endt packed
day/year (low9 day, mid7 zero, high16 year), inrt float32 finite nonnegative
(specials raw -99/-1), identity ordinal. Reads frozen payload only.
"""
import sys, os, json, hashlib, struct, math
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, load_payload
i32 = lambda b, p: struct.unpack_from("<i", b, p)[0]
u32 = lambda b, p: struct.unpack_from("<I", b, p)[0]
f32 = lambda b, p: struct.unpack_from("<f", b, p)[0]

def packed_ok(v):
    day = v & 0x1FF; mid = (v >> 9) & 0x7F; year = v >> 16
    return (1 <= day <= 366) and mid == 0 and (1850 <= year <= 2100), (day, mid, year)

def main():
    raw = load_payload(_reader(), "server", 33)
    n, stride = 32409, 79
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    ck("closure", 13+n*stride+9 == len(raw) == 2560333, f"len={len(raw)}")
    ck("payload_sha", hashlib.sha256(raw).hexdigest() == "b2bf8e2f1db6d73bc0080e4fd9a2666fa6bbdd7d053cd386e19590d557e987c3", hashlib.sha256(raw).hexdigest()[:16])
    cash_bad = sour_bad = stdt_bad = endt_bad = inrt_bad = ident_bad = 0
    cash_rng = [10**9, -10**9]; sour_set = set(); inrt_special = 0; inrt_max = 0.0
    stdt_first = endt_first = None
    for i in range(n):
        bs = 14 + i*stride
        ca = i32(raw, bs+4); so = struct.unpack_from("<b", raw, bs+14)[0]
        sd = u32(raw, bs+19); ed = u32(raw, bs+23); ir_raw = i32(raw, bs+27)
        if not (-1000000000 <= ca <= 1000000000): cash_bad += 1
        cash_rng = [min(cash_rng[0], ca), max(cash_rng[1], ca)]
        sour_set.add(so)
        ok_s, ds = packed_ok(sd); ok_e, de = packed_ok(ed)
        if not ok_s: stdt_bad += 1
        if not ok_e: endt_bad += 1
        if i == 0: stdt_first = ds; endt_first = de
        if ir_raw in (-99, -1): inrt_special += 1
        else:
            fv = f32(raw, bs+27)
            if fv in (-99.0, -1.0): inrt_special += 1  # sol specials are FLOAT values -99.0/-1.0
            elif not (math.isfinite(fv) and fv >= 0): inrt_bad += 1
            else: inrt_max = max(inrt_max, fv)
        if u32(raw, bs+66) != i: ident_bad += 1
    ck("cash_domain[-1e9,1e9]", cash_bad == 0, f"bad={cash_bad} range={cash_rng}")
    ck("sour_i8_enum_finite", len(sour_set) <= 40, f"distinct={len(sour_set)} vals={sorted(sour_set)[:20]}")
    ck("stdt_packed_day_year", stdt_bad == 0, f"bad={stdt_bad}/{n} row0={stdt_first}")
    ck("endt_packed_day_year", endt_bad == 0, f"bad={endt_bad}/{n} row0={endt_first}")
    ck("inrt_float32_finite_nonneg", inrt_bad == 0, f"bad={inrt_bad} specials(-99/-1)={inrt_special} max={inrt_max:.4f}")
    ck("identity_lane0_ordinal", ident_bad == 0, f"bad={ident_bad}")
    foot = raw[13+n*stride:]
    ck("footer_9B", len(foot) == 9 and foot[:4] == b"\x00\x00\x00\x00" and foot[4] == 1, f"hex={foot.hex()} last_u32={u32(foot,5)}")
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t36 spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())