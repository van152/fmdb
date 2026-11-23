"""t88 rt_x: pre+4 候选 rec_type 与 presence/date 签名的交叉表。

用法: py -V:3.12 -I -B scripts/t88_rt_x.py [--help] [--selftest]
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
    ap.add_argument("--off", type=int, default=4)
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0

    pr, dt, rt = [], [], []
    for s, u, e in rows:
        pr.append("".join("1" if struct.unpack_from("<I", p, s + o)[0] != 0xFFFFFFFF else "0" for o in SLOTS))
        dt.append("".join("S" if struct.unpack_from("<I", p, u + 4 * k)[0] == 0x076C0001 else "x" for k in range(3)))
        rt.append(p[s + a.off])

    print("pre+%d domain=%d" % (a.off, len(set(rt))))
    print("%-5s %-7s %s" % ("val", "count", "presence(6) x dates(3) top combos"))
    for v, n in collections.Counter(rt).most_common(40):
        combos = collections.Counter(pr[i] + "/" + dt[i] for i in range(len(rt)) if rt[i] == v)
        print("%-5d %-7d %s" % (v, n, combos.most_common(3)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
