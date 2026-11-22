"""t88 idslots/tail: 验证 4 个 u64 id 槽归属 + 尾部 26B = 0x40..0x4b + 0x50..0x5d 拆分。

用法: py -V:3.12 -I -B scripts/t88_idslots.py [--help] [--selftest]
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
        assert all(u + 26 + 13 == e for _, u, e in rows)
        print("selftest ok rows=%d" % len(rows))
        return 0

    print("=== 4 x u64 id slots (pre+5/13/21/29), present = lo != 0xffffffff ===")
    for base in (5, 13, 21, 29):
        lo = [struct.unpack_from("<I", p, s + base)[0] for s, u, e in rows]
        hi = [struct.unpack_from("<I", p, s + base + 4)[0] for s, u, e in rows]
        pres = [i for i, v in enumerate(lo) if v != 0xFFFFFFFF]
        hi0 = sum(1 for i in pres if hi[i] == 0)
        hiFF = sum(1 for i in pres if hi[i] == 0xFFFFFFFF)
        line = " pre+%-2d present=%-6d hi==0:%-6d hi==FF:%-6d" % (base, len(pres), hi0, hiFF)
        sub = [lo[i] for i in pres]
        for k in ("t3", "t24", "t25", "t10"):
            h = sum(1 for v in sub if v in refs[k])
            line += " %s=%.3f" % (k, h / len(sub) if sub else 0)
        print(line)

    print("=== tail split 0x40..0x4b (12B dates) + 0x50..0x5d (14B) ===")
    checks = [("0x50 cash/atte w4", 12, 4), ("0x54 apps/gams w2", 16, 2),
              ("0x56 gols w2", 18, 2), ("0x58 fsgt/ogls w2", 20, 2),
              ("0x5a rati w1", 22, 1), ("0x5b info w1", 23, 1),
              ("0x5c rrea w1", 24, 1), ("0x5d cnst w1", 25, 1)]
    fmt = {1: "<B", 2: "<H", 4: "<I"}
    for name, off, w in checks:
        vals = [struct.unpack_from(fmt[w], p, u + off)[0] for s, u, e in rows]
        c = collections.Counter(vals)
        sent = c.get({1: 0xFF, 2: 0xFFFF, 4: 0xFFFFFFFF}[w], 0)
        print("  %-20s d=%-6d sentinel=%-6d (%.3f) top=%s" % (
            name, len(c), sent, sent / len(vals), c.most_common(4)))
    print("=== 0x4c check: wire+0 (pre+0) club-set rate vs tail 0x4c absent ===")
    key = [struct.unpack_from("<I", p, s)[0] for s, u, e in rows]
    print("  pre+0 in t3: %d (%.4f)" % (sum(1 for v in key if v in refs["t3"]),
                                       sum(1 for v in key if v in refs["t3"]) / len(key)))
    print("  pre+0 == 0xFFFFFFFF: %d" % sum(1 for v in key if v == 0xFFFFFFFF))
    return 0


if __name__ == "__main__":
    sys.exit(main())
