# -*- coding: utf-8 -*-
"""t34_spot.py — commander independent full-table check of t34 CNtp.
Validates sol's quantitative claims: closure 18094, nati i32 nation identity
(row1@42=1651, ordinal-hypothesis miss), rati i8 enum, mina/maxa u8 zero counts
(436/395), both-zero 389 / both-nonzero 311 / min>max 6, identity ordinal.
"""
import sys, os, json, hashlib, struct
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, load_payload
i32 = lambda b, p: struct.unpack_from("<i", b, p)[0]
u32 = lambda b, p: struct.unpack_from("<I", b, p)[0]
u8 = lambda b, p: b[p]

def main():
    raw = load_payload(_reader(), "server", 66)
    n, stride = 753, 24
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    ck("closure", 13+n*stride+9 == len(raw) == 18094, f"len={len(raw)}")
    ck("payload_sha", hashlib.sha256(raw).hexdigest() == "3ddd47bbeec04ff6789dafdfe40148367abc4373700b082452fc79be06e02911", hashlib.sha256(raw).hexdigest()[:16])
    # row1 nati @ absolute 42 = 1651 (sol ordinal-miss counterexample)
    ck("row1_nati_1651", u32(raw, 42) == 1651, f"@42={u32(raw,42)} (sol: UID not ordinal 189)")
    mina_zero = maxa_zero = both_zero = both_nz = min_gt_max = ident_bad = 0
    mina_nz_rng = [255, 0]; maxa_nz_rng = [255, 0]; rati_set = set()
    nati_neg = 0
    for i in range(n):
        bs = 14 + i*stride
        na = i32(raw, bs+4); ra = struct.unpack_from("<b", raw, bs+8)[0]
        mi = u8(raw, bs+9); ma = u8(raw, bs+10)
        rati_set.add(ra)
        if na == -1: nati_neg += 1
        if mi == 0: mina_zero += 1
        else: mina_nz_rng = [min(mina_nz_rng[0], mi), max(mina_nz_rng[1], mi)]
        if ma == 0: maxa_zero += 1
        else: maxa_nz_rng = [min(maxa_nz_rng[0], ma), max(maxa_nz_rng[1], ma)]
        if mi == 0 and ma == 0: both_zero += 1
        if mi != 0 and ma != 0:
            both_nz += 1
        if mi > ma: min_gt_max += 1  # sol counts raw min>max over ALL rows (the 6 max-only-zero rows)
        if u32(raw, bs+11) != i: ident_bad += 1
    ck("mina_zero_436", mina_zero == 436, f"{mina_zero} nz_range={mina_nz_rng} (sol [14,32])")
    ck("maxa_zero_395", maxa_zero == 395, f"{maxa_zero} nz_range={maxa_nz_rng} (sol [17,45])")
    ck("mina_nz_in_xml[14,44]", 14 <= mina_nz_rng[0] and mina_nz_rng[1] <= 44, f"{mina_nz_rng}")
    ck("maxa_nz_in_xml[15,45]", 15 <= maxa_nz_rng[0] and maxa_nz_rng[1] <= 45, f"{maxa_nz_rng}")
    ck("both_zero_389", both_zero == 389, f"{both_zero}")
    ck("both_nonzero_311", both_nz == 311, f"{both_nz}")
    ck("min_gt_max_6", min_gt_max == 6, f"{min_gt_max} (sol row57 (18,0))")
    ck("identity_lane0_ordinal", ident_bad == 0, f"bad={ident_bad}")
    ck("rati_i8_enum_finite", len(rati_set) <= 30, f"distinct={len(rati_set)} vals={sorted(rati_set)[:15]}")
    foot = raw[13+n*stride:]
    ck("footer_9B", len(foot) == 9 and foot[:4] == b"\x00\x00\x00\x00" and foot[4] == 1, f"hex={foot.hex()} last_u32={u32(foot,5)}")
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t34 spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())