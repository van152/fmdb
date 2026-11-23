"""t88 key probe: pre+0 与 identity 字段、refset、分段的关系。

用法: py -V:3.12 -I -B scripts/t88_keyprobe.py [--help] [--selftest]
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
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0
    refs = {k: set(v) for k, v in json.load(open(os.path.join(ROOT, "scratch", "t88", "refsets.json"))).items()}

    key = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    ordn = [struct.unpack_from("<I", p, e - 13)[0] for s, u, e in rows]
    iuid = [struct.unpack_from("<I", p, e - 9)[0] for s, u, e in rows]

    print("pre+0 == identity.ordinal : %d/%d" % (sum(1 for x, y in zip(key, ordn) if x == y), len(rows)))
    print("pre+0 == identity.uid     : %d/%d" % (sum(1 for x, y in zip(key, iuid) if x == y), len(rows)))

    # 分段: 以 pre+0 是否单调递增切段
    cuts = [0] + [i for i in range(1, len(key)) if key[i] < key[i - 1]] + [len(key)]
    segs = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]
    big = [s for s in segs if s[1] - s[0] >= 50]
    print("segments=%d  >=50rows=%d" % (len(segs), len(big)))
    for s, e in big[:8]:
        seg = key[s:e]
        print("  seg %6d..%-6d n=%-6d min=%-10d max=%-10d distinct=%-5d sorted=%s" % (
            s, e, e - s, min(seg), max(seg), len(set(seg)), seg == sorted(seg)))

    # 关键: 每个 pre+0 值的行数分布 (是否 = 记录族数)
    c = collections.Counter(key)
    print("distinct key=%d  rows/key top=%s" % (len(c), c.most_common(5)))
    print("key range buckets: <10000=%d  <1e6=%d  <1e8=%d  >=1e8=%d" % (
        sum(1 for x in key if x < 10000), sum(1 for x in key if x < 10 ** 6),
        sum(1 for x in key if x < 10 ** 8), sum(1 for x in key if x >= 10 ** 8)))

    # pre+0 落在哪个 refset
    for k, st_ in refs.items():
        h = sum(1 for x in key if x in st_)
        print("  pre+0 in %-4s : %6d (%.4f)" % (k, h, h / len(key)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
