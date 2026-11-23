"""t88 layout dump: 按 presence-pattern 分组取代表行, 打印 pre/suf 逐字节。

用法: py -V:3.12 -I -B scripts/t88_layout.py [--help] [--selftest] [--per 2]
"""
import argparse
import collections
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")
FOOT = 8
SLOTS = [13, 17, 21, 25, 29, 33]


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
    ap.add_argument("--per", type=int, default=2)
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0

    groups = collections.defaultdict(list)
    for idx, (s, u, e) in enumerate(rows):
        pat = "".join("1" if struct.unpack_from("<I", p, s + o)[0] != 0xFFFFFFFF else "0" for o in SLOTS)
        groups[pat].append(idx)

    for pat, idxs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print("=== pattern %s  n=%d" % (pat, len(idxs)))
        for idx in idxs[:a.per]:
            s, u, e = rows[idx]
            nl = struct.unpack_from("<I", p, s + 37)[0]
            nm = p[s + 41:s + 41 + nl].decode("utf8", "replace")
            print("  idx=%-6d len=%-3d nl=%-2d uid=%-9d name=%r" % (
                idx, e - s, nl, struct.unpack_from("<I", p, s)[0], nm))
            print("    pre 0..36 : %s" % p[s:s + 37].hex(" "))
            print("    suf 0..25 : %s" % p[u:u + 26].hex(" "))
            print("    ident     : %s" % p[e - 13:e].hex(" "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
