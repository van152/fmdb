"""t88 census: 84,477 vs 84,259 club 的差额归属(程序化)。

用法: py -V:3.12 -I -B scripts/t88_census.py [--help] [--selftest]
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
        assert len(refs["t3"]) == 84259
        print("selftest ok rows=%d club=%d" % (len(rows), len(refs["t3"])))
        return 0

    key = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    in_c = [k in refs["t3"] for k in key]
    in_t = [k in refs["t24"] for k in key]
    print("rows=%d  club uids=%d  team uids=%d" % (len(rows), len(refs["t3"]), len(refs["t24"])))
    print("pre+0 in club: %d (%.4f)   in team: %d (%.4f)   in either: %d" % (
        sum(in_c), sum(in_c) / len(key), sum(in_t), sum(in_t) / len(key),
        sum(1 for i in range(len(key)) if in_c[i] or in_t[i])))
    print("pre+0 in club but not team: %d ; team but not club: %d ; neither: %d" % (
        sum(1 for i in range(len(key)) if in_c[i] and not in_t[i]),
        sum(1 for i in range(len(key)) if in_t[i] and not in_c[i]),
        sum(1 for i in range(len(key)) if not in_c[i] and not in_t[i])))

    miss = [i for i in range(len(key)) if not in_c[i]]
    mu = sorted(set(key[i] for i in miss))
    print("rows missing from club: %d  distinct uid: %d" % (len(miss), len(mu)))
    print("  of those uid in team: %d / %d" % (sum(1 for x in mu if x in refs["t24"]), len(mu)))
    print("  of those uid in comp: %d ; nation: %d" % (
        sum(1 for x in mu if x in refs["t25"]), sum(1 for x in mu if x in refs["t10"])))
    print("  uid < 10000: %d ; >= 2e9: %d" % (
        sum(1 for x in mu if x < 10000), sum(1 for x in mu if x >= 2000000000)))

    # 差额 218: 行数 vs club 行数的可能解释
    print("--- 218 delta ---")
    print("  84477 - 84259 = %d" % (len(rows) - len(refs["t3"])))
    print("  84507(team) - 84477 = %d" % (len(refs["t24"]) - len(rows)))
    print("  distinct pre+0 = %d ; rows with uid appearing >1 = %d" % (
        len(set(key)), sum(1 for k, c in collections.Counter(key).items() if c > 1)))
    print("  club uids with >=1 row: %d ; club uids with 0 row: %d" % (
        len(set(key) & refs["t3"]), len(refs["t3"] - set(key))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
