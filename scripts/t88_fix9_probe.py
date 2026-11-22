"""t88-fix9 body grammar probe (read-only data side).

Dump per-rec_type body byte stats + ref-set membership scan to locate fields.

用法: py -V:3.12 -I -B scripts/t88_fix9_probe.py [--rt N] [--selftest]
输出 <=30 行。
"""
import argparse
import collections
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scratch", "t88")
O2 = os.path.join(S, "out2")


def load_rows():
    p = open(os.path.join(O2, "_p_server_45.bin"), "rb").read()
    sb = open(os.path.join(O2, "_starts.bin"), "rb").read()
    st = list(struct.unpack("<%dI" % (len(sb) // 4), sb))
    n = len(st)
    rows = []
    for i in range(n):
        a = st[i]
        b = st[i + 1] if i + 1 < n else len(p) - 8
        nl = struct.unpack_from("<I", p, a + 37)[0]
        body = a + 41 + nl
        rows.append((a, b, nl, body))
    return p, rows


def refsets():
    d = json.load(open(os.path.join(S, "refsets.json"), encoding="utf-8"))
    return {k: set(v) for k, v in d.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rt", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        assert all(b - (bo + 26 + 13) == 0 for _, b, _, bo in rows)
        print("selftest ok rows=%d body=26 tail_ok" % len(rows))
        return 0
    rs = refsets()
    sel = [r for r in rows if p[r[0] + 4] == a.rt]
    print("rt=%d rows=%d" % (a.rt, len(sel)))
    print("--- per-offset: distinct / const / ff-frac / top ---")
    for o in range(26):
        vals = [p[bo + o] for _, _, _, bo in sel]
        c = collections.Counter(vals)
        print("  o%02d d=%3d ff=%.2f z=%.2f top=%s"
              % (o, len(c), c[255] / len(vals), c[0] / len(vals), c.most_common(2)))
    print("--- ref membership scan (u16/u32 windows) ---")
    for name, s in rs.items():
        for w in (2, 4):
            for o in range(0, 27 - w):
                hit = 0
                for _, _, _, bo in sel:
                    v = struct.unpack_from("<H" if w == 2 else "<I", p, bo + o)[0]
                    if v in s:
                        hit += 1
                if hit > len(sel) * 0.3:
                    print("  %s w=%d o=%02d hit=%.2f" % (name, w, o, hit / len(sel)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
