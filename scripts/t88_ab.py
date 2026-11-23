"""t88 probe11: A/B 槽 (pre+5, pre+9) 的 refset 对照 + suf+12 与 pre+0 的分组一致性。

用法: py -V:3.12 -I -B scripts/t88_ab.py [--help] [--selftest]
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

    print("=== pre+5 (A) / pre+9 (B) 未对齐 u32 ===")
    for off in (5, 9):
        vals = [struct.unpack_from("<I", p, s + off)[0] for s, u, e in rows]
        nz = [v for v in vals if v != 0]
        print(" off=%d distinct=%d nonzero=%d zero=%d min=%d max=%d" % (
            off, len(set(vals)), len(nz), len(vals) - len(nz),
            min(nz) if nz else 0, max(nz) if nz else 0))
        for k, st_ in refs.items():
            print("   %-4s hit=%-6d (%.4f) ctl+1B=%-5d" % (
                k, sum(1 for v in nz if v in st_),
                sum(1 for v in nz if v in st_) / len(nz) if nz else 0,
                sum(1 for s, u, e in rows if struct.unpack_from("<I", p, s + off + 1)[0] in st_)))

    print("=== suf+12 与 pre+0 分组一致性 ===")
    key = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    v12 = [struct.unpack_from("<I", p, u + 12)[0] for s, u, e in rows]
    g = collections.defaultdict(set)
    for k, v in zip(key, v12):
        g[k].add(v)
    multi = [k for k, s in g.items() if len(s) > 1]
    print(" keys=%d  keys with >1 suf+12 value: %d" % (len(g), len(multi)))
    nz12 = [v for v in v12 if v != 0xFFFFFFFF]
    print(" suf+12 present=%d distinct=%d" % (len(nz12), len(set(nz12))))
    print(" suf+12 vs pre+0 equal rows: %d" % sum(1 for x, y in zip(v12, key) if x == y))
    # 8 字节对 suf+12..19
    lo = [struct.unpack_from("<I", p, u + 12)[0] for s, u, e in rows]
    hi = [struct.unpack_from("<I", p, u + 16)[0] for s, u, e in rows]
    print(" suf+16 (cash) 与 suf+12 同时 present 的行: %d" % sum(
        1 for i in range(len(rows)) if lo[i] != 0xFFFFFFFF and hi[i] != 0xFFFFFFFF))
    return 0


if __name__ == "__main__":
    sys.exit(main())
