"""t88 small-cardinality slot scan: 找 rec_type 之类的小域字段。

扫描前缀 0..36 与后缀 0..25 的所有 u8/u16/u32 对齐槽, 打印 distinct<=16 的槽。
用法: py -V:3.12 -I -B scripts/t88_typescan.py [--help] [--selftest] [--maxd N]
"""
import argparse
import collections
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


FMT = {1: "<B", 2: "<H", 4: "<I"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--maxd", type=int, default=16)
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0

    print("rows=%d  (scan u8/u16/u32, distinct<=%d)" % (len(rows), a.maxd))
    for part in ("pre", "suf"):
        lim = 37 if part == "pre" else 26
        for w in (1, 2, 4):
            for off in range(0, lim - w + 1):
                if off % w:
                    continue
                vals = []
                for s, u, e in rows:
                    base = s if part == "pre" else u
                    vals.append(struct.unpack_from(FMT[w], p, base + off)[0])
                c = collections.Counter(vals)
                if len(c) <= a.maxd:
                    print("%s+%-2d w%d d=%-2d %s" % (part, off, w, len(c), sorted(c.items(), key=lambda x: -x[1])[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
