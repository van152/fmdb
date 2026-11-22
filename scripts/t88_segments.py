"""t88 probe13: 段结构判定 -- pre+4(B)/pre+0(A) 是否在连续段内恒定; 218 差额算式。

用法: py -V:3.12 -I -B scripts/t88_segments.py [--help] [--selftest]
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


def runs(vals):
    out = []
    s = 0
    for i in range(1, len(vals) + 1):
        if i == len(vals) or vals[i] != vals[s]:
            out.append((s, i - s, vals[s]))
            s = i
    return out


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

    A = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    B = [p[s + 4] for s, u, e in rows]

    for name, vals in (("A=pre+0", A), ("B=pre+4", B)):
        r = runs(vals)
        print("%s: runs=%d  len1=%d  median=%d  max=%d" % (
            name, len(r), sum(1 for x in r if x[1] == 1),
            sorted(x[1] for x in r)[len(r) // 2], max(x[1] for x in r)))

    print("--- A runs >=100: 是否 A 单调段 ---")
    rA = [x for x in runs(A) if x[1] >= 100]
    print("  count=%d total_rows=%d" % (len(rA), sum(x[1] for x in rA)))

    print("--- B 值 -> 是否单一块 (block count) ---")
    blk = collections.defaultdict(list)
    for s, ln, v in runs(B):
        blk[v].append((s, ln))
    for v in sorted(blk)[:40]:
        print("  B=%-3d blocks=%-4d rows=%d" % (v, len(blk[v]), sum(x[1] for x in blk[v])))

    print("--- 218 算式候选 ---")
    print("  rows=%d club=%d team=%d comp=%d" % (len(rows), len(refs["t3"]), len(refs["t24"]), len(refs["t25"])))
    print("  84477-84259=%d ; 84477-84507=%d ; 84259 distinct A=%d" % (
        len(rows) - len(refs["t3"]), len(rows) - len(refs["t24"]), len(set(A))))
    ac = collections.Counter(A)
    print("  A values with exactly 1 row: %d ; with >1: %d" % (
        sum(1 for c in ac.values() if c == 1), sum(1 for c in ac.values() if c > 1)))
    print("  distinct A in club=%d ; A<1000 rows=%d" % (
        len(set(A) & refs["t3"]), sum(1 for x in A if x < 1000)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
