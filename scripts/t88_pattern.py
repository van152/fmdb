"""t88 pattern probe: 行内 slot 存在性模式 + 小域字节, 找 rec_type 与 family 判别。

用法: py -V:3.12 -I -B scripts/t88_pattern.py [--help] [--selftest] [--dump N]
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
SLOTS = [13, 17, 21, 25, 29, 33]   # pre 内 6 个 u32 槽 (24B)


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
    ap.add_argument("--dump", type=int, default=0)
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0

    pat = collections.Counter()
    for s, u, e in rows:
        bits = "".join("1" if struct.unpack_from("<I", p, s + o)[0] != 0xFFFFFFFF else "0" for o in SLOTS)
        pat[bits] += 1
    print("presence pattern (slot13,17,21,25,29,33 ; 1=present): %d distinct" % len(pat))
    for k, v in pat.most_common(12):
        print("  %s  %d" % (k, v))

    # 每个 slot 的 distinct 与 top
    print("--- slot value domains (u32) ---")
    for o in SLOTS:
        vals = [struct.unpack_from("<I", p, s + o)[0] for s, u, e in rows]
        c = collections.Counter(vals)
        print("  pre+%-2d d=%-6d ff=%-6d top=%s" % (o, len(c), c.get(0xFFFFFFFF, 0), c.most_common(3)))

    print("--- suffix 3 date slots: sentinel(1/1/1900=0x076c0001) vs other ---")
    for k in range(3):
        vals = [struct.unpack_from("<I", p, u + 4 * k)[0] for s, u, e in rows]
        sent = sum(1 for v in vals if v == 0x076C0001)
        ff = sum(1 for v in vals if v == 0xFFFFFFFF)
        zero = sum(1 for v in vals if v == 0)
        yrs = collections.Counter(v >> 16 for v in vals if v != 0xFFFFFFFF)
        print("  suf+%-2d sentinel=%-6d ff=%-6d zero=%-5d d=%-6d years=%s" % (
            4 * k, sent, ff, zero, len(set(vals)), sorted(yrs.items(), key=lambda x: -x[1])[:5]))

    if a.dump:
        print("--- dump first %d rows (uid, pre bytes, namelen, name) ---" % a.dump)
        for s, u, e in rows[:a.dump]:
            nl = struct.unpack_from("<I", p, s + 37)[0]
            nm = p[s + 41:s + 41 + nl].decode("utf8", "replace")
            print("  uid=%-9d pre=%s nl=%-2d name=%r" % (
                struct.unpack_from("<I", p, s)[0], p[s + 4:s + 13].hex(), nl, nm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
