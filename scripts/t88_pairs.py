"""t88 probe9: 三个 id 对 (13,17)/(21,25)/(29,33) 的取值域与 refset 对照(带位移控制)。

用法: py -V:3.12 -I -B scripts/t88_pairs.py [--help] [--selftest]
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

    for name, lo in (("A", 13), ("B", 21), ("C", 29)):
        print("=== pair %s (pre+%d lo, pre+%d hi) ===" % (name, lo, lo + 4))
        lo_v = [struct.unpack_from("<I", p, s + lo)[0] for s, u, e in rows]
        hi_v = [struct.unpack_from("<I", p, s + lo + 4)[0] for s, u, e in rows]
        present = [i for i, v in enumerate(lo_v) if v != 0xFFFFFFFF]
        print("  present=%d  hi==0: %d  hi!=0: %d" % (
            len(present), sum(1 for i in present if hi_v[i] == 0),
            sum(1 for i in present if hi_v[i] != 0)))
        sub = [lo_v[i] for i in present]
        print("  lo distinct=%d min=%d max=%d top=%s" % (
            len(set(sub)), min(sub), max(sub), collections.Counter(sub).most_common(3)))
        for k, st_ in refs.items():
            h = sum(1 for v in sub if v in st_)
            # 控制: 同一位移 +1 字节
            ctl = [struct.unpack_from("<I", p, s + lo + 1)[0] for s, u, e in rows]
            hc = sum(1 for i in present if ctl[i] in st_)
            print("    %-4s hit=%-6d (%.4f)  ctl+1B=%-6d" % (k, h, h / len(sub) if sub else 0, hc))

    # 每个 pre+0 键的记录族构成
    key = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    pat = []
    for s, u, e in rows:
        b = "".join("1" if struct.unpack_from("<I", p, s + o)[0] != 0xFFFFFFFF else "0" for o in (13, 21, 29))
        pat.append(b)
    grp = collections.defaultdict(collections.Counter)
    for k, v in zip(key, pat):
        grp[k][v] += 1
    print("=== rows-per-key: %d distinct keys ===" % len(grp))
    rp = collections.Counter(sum(c.values()) for c in grp.values())
    print("  rows/key dist top=%s" % rp.most_common(8))
    print("  keys with pattern set == all 4 : %d" % sum(1 for c in grp.values() if len(c) == 4))
    print("  pattern combos per key top: %s" % collections.Counter(
        tuple(sorted(c)) for c in grp.values()).most_common(6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
