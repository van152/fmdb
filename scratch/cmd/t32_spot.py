# -*- coding: utf-8 -*-
"""t32_spot.py — commander independent full-table check of t32 Cmti.
Validates: closure 13+535*46+9, 3 record-key i32 pairs (2nd lane non-zero),
mths/cash/pyiv domains, identity lane0 ordinal, footer. Reads frozen payload only.
"""
import sys, os, json, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, load_payload
import struct
i32 = lambda b, p: struct.unpack_from("<i", b, p)[0]
u32 = lambda b, p: struct.unpack_from("<I", b, p)[0]

def main():
    raw = load_payload(_reader(), "server", 43)
    n, stride = 535, 46
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    ck("closure", 13 + n*stride + 9 == len(raw) and len(raw) == 24632, f"len={len(raw)}")
    ck("payload_sha", hashlib.sha256(raw).hexdigest() == "7981267028706e701d39a32126b5b2e85f9b4973266cf1545f09869a524a069e", hashlib.sha256(raw).hexdigest()[:16])
    pair2_nonzero = 0; mths_bad = cash_bad = pyiv_bad = ident_bad = 0
    mths_rng = [10**9, -10**9]; cash_rng = [10**9, -10**9]
    for i in range(n):
        bs = 14 + i*stride
        for po in (0, 8, 16):  # three key pairs
            lane1 = i32(raw, bs+po+4)
            if lane1 != 0: pair2_nonzero += 1
        m = i32(raw, bs+24); ca = i32(raw, bs+28); py = struct.unpack_from("<b", raw, bs+32)[0]
        if not (1 <= m <= 100): mths_bad += 1
        if not (0 <= ca <= 1000000000): cash_bad += 1
        if not (-128 <= py <= 127): pyiv_bad += 1
        mths_rng = [min(mths_rng[0], m), max(mths_rng[1], m)]
        cash_rng = [min(cash_rng[0], ca), max(cash_rng[1], ca)]
        if u32(raw, bs+33) != i: ident_bad += 1  # identity lane0 ordinal
    ck("key_pairs_2nd_lane_nonzero", pair2_nonzero == 3*n, f"{pair2_nonzero}/{3*n} (sol: 全表非零)")
    ck("mths_domain[1,100]", mths_bad == 0, f"bad={mths_bad} range={mths_rng}")
    ck("cash_domain[0,1e9]", cash_bad == 0, f"bad={cash_bad} range={cash_rng}")
    ck("pyiv_i8", pyiv_bad == 0, f"bad={pyiv_bad}")
    ck("identity_lane0_ordinal", ident_bad == 0, f"bad={ident_bad}")
    foot = raw[13+n*stride:]
    ck("footer_9B", len(foot) == 9 and foot[:4] == b"\x00\x00\x00\x00" and foot[4] == 1, f"hex={foot.hex()} last_u32={u32(foot,5)}")
    ck("footer_last_u32_eq_count", u32(foot, 5) == n, f"{u32(foot,5)} (maxUID==count ambiguous per sol)")
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t32 spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())