"""t88 probe12: pre+4 精确值域 / u64@4 唯一性 / neither-519 明细 / suf+12 控制。

用法: py -V:3.12 -I -B scripts/t88_probe12.py [--help] [--selftest]
"""
import argparse
import collections
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")
FOOT = 8


def load_rows():
    p = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    sb = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    st = list(struct.unpack("<%dI" % (len(sb) // 4), sb))
    n = len(st)
    rows = []
    for i in range(n):
        a = st[i]
        b = st[i + 1] if i + 1 < n else len(p) - FOOT
        nl = struct.unpack_from("<I", p, a + 37)[0]
        rows.append((a, a + 41 + nl, b))
    return p, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    p, rows = load_rows()
    refs = {k: set(v) for k, v in json.load(open(os.path.join(ROOT, "scratch", "t88", "refsets.json"))).items()}
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0

    print("=== pre+4 u8 exact domain ===")
    c = collections.Counter(p[s + 4] for s, u, e in rows)
    print("  distinct=%d  values=%s" % (len(c), sorted(c.items())))
    print("  in rectype set {10,13,24,25,26,27,28}: rows=%d" % sum(
        v for k, v in c.items() if k in (10, 13, 24, 25, 26, 27, 28)))

    print("=== u64@4 uniqueness (id-like?) ===")
    u64 = [struct.unpack_from("<Q", p, s + 4)[0] for s, u, e in rows]
    print("  distinct=%d of %d" % (len(set(u64)), len(u64)))
    lo = [struct.unpack_from("<I", p, s + 4)[0] for s, u, e in rows]
    hi = [struct.unpack_from("<I", p, s + 8)[0] for s, u, e in rows]
    print("  lo==hi rows=%d ; hi==0 rows=%d ; lo==0 rows=%d" % (
        sum(1 for x, y in zip(lo, hi) if x == y), sum(1 for x in hi if x == 0),
        sum(1 for x in lo if x == 0)))

    print("=== neither-set rows (pre+0 not in club nor team) ===")
    key = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    nei = [i for i in range(len(key)) if key[i] not in refs["t3"] and key[i] not in refs["t24"]]
    nu = sorted(set(key[i] for i in nei))
    print("  rows=%d distinct=%d" % (len(nei), len(nu)))
    print("  value ranges: <57 =%d ; 57..1e6 =%d ; >=2e9 =%d" % (
        sum(1 for x in nu if x < 57), sum(1 for x in nu if 57 <= x < 10 ** 6),
        sum(1 for x in nu if x >= 2 * 10 ** 9)))
    print("  sample=%s" % nu[:12])

    print("=== suf+12 (rec+0x4c candidate) vs refsets with +/-1 control ===")
    v12 = [struct.unpack_from("<I", p, u + 12)[0] for s, u, e in rows]
    pres = [i for i, v in enumerate(v12) if v != 0xFFFFFFFF]
    print("  present=%d (%.4f)" % (len(pres), len(pres) / len(rows)))
    for k, st_ in refs.items():
        h = sum(1 for i in pres if v12[i] in st_)
        print("    %-4s %6d (%.4f)" % (k, h, h / len(pres)))
    print("  value range: min=%d max=%d distinct=%d" % (
        min(v12[i] for i in pres), max(v12[i] for i in pres),
        len(set(v12[i] for i in pres))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
