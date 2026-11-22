"""t88 rec_type hunt: 用 presence-pattern 交叉验证小域字节是否为 rec_type。

判据: rec_type 必须 (1) 全档小域, (2) 每个值 -> presence 模式确定 (family 决定槽位集),
      (3) 每个值 -> 日期槽 sentinel 分布确定。
用法: py -V:3.12 -I -B scripts/t88_rectype.py [--help] [--selftest]
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
CAND = [("pre", 3), ("pre", 8), ("pre", 12), ("pre", 16), ("pre", 20),
        ("suf", 15), ("suf", 17), ("suf", 19), ("suf", 21), ("suf", 24), ("suf", 25)]


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

    base = []
    for s, u, e in rows:
        pat = "".join("1" if struct.unpack_from("<I", p, s + o)[0] != 0xFFFFFFFF else "0" for o in SLOTS)
        sent = "".join("S" if struct.unpack_from("<I", p, u + 4 * k)[0] == 0x076C0001 else "x" for k in range(3))
        base.append((pat, sent))

    print("cand            d   deterministic(pat)  distinct(pat)  entropy-ok")
    for part, off in CAND:
        m = collections.defaultdict(collections.Counter)
        for i, (s, u, e) in enumerate(rows):
            b0 = s if part == "pre" else u
            m[p[b0 + off]][base[i][0]] += 1
        det = sum(1 for v, c in m.items() if len(c) == 1)
        print("%-6s+%-3d %4d  %3d/%-3d           %s" % (part, off, len(m), det, len(m),
                                                       sorted(len(c) for c in m.values())))
    # 交叉表: 最佳候选的分布
    print("--- distribution for pre+12 / suf+15 / suf+17 ---")
    for part, off in (("pre", 12), ("suf", 15), ("suf", 17)):
        m = collections.defaultdict(collections.Counter)
        for i, (s, u, e) in enumerate(rows):
            b0 = s if part == "pre" else u
            m[p[b0 + off]][base[i][0]] += 1
        print("%s+%d:" % (part, off))
        for v in sorted(m):
            tot = sum(m[v].values())
            print("   %-4d n=%-6d %s" % (v, tot, dict(m[v].most_common(4))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
