"""t88 wire offset probe: 找 club UID / rec_type 的 wire 偏移。

用法: py -V:3.12 -I -B scripts/t88_wire_probe.py [--help] [--selftest]
只读 out2 冻结产物; 输出 <=30 行。
"""
import argparse
import json
import os
import struct
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")


def load():
    p = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    sb = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    st = list(struct.unpack("<%dI" % (len(sb) // 4), sb))
    return p, st


def frames(p, st):
    n = len(st)
    out = []
    for i in range(n):
        a = st[i]
        b = st[i + 1] if i + 1 < n else len(p)
        out.append((a, b, b - a))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    p, st = load()
    fr = frames(p, st)
    n = len(fr)
    if a.selftest:
        assert n == 84477
        print("selftest ok rows=%d" % n)
        return 0

    club = set(json.load(open(os.path.join(ROOT, "scratch", "t88", "club.json")))["uids"])
    print("club uids=%d rows=%d" % (len(club), n))

    # 候选: 后缀区 (row_end-39 .. row_end-14) 的 u16 槽位
    print("--- suffix u16 slots: club-hit vs control(shift+1) ---")
    for rel in range(-39, -13, 2):
        vals = []
        for (s, e, L) in fr:
            o = e + rel
            vals.append(struct.unpack_from("<H", p, o)[0])
        hit = sum(1 for v in vals if v in club)
        ctl = sum(1 for v in vals if (v + 1) in club)
        d = len(set(vals))
        top = collections.Counter(vals).most_common(2)
        print("rel=%3d u16 distinct=%5d clubhit=%6d ctl=%6d top=%s" % (rel, d, hit, ctl, top))

    print("--- suffix u32 slots ---")
    for rel in range(-39, -16, 1):
        try:
            vals = [struct.unpack_from("<I", p, e + rel)[0] for (s, e, L) in fr]
        except Exception:
            continue
        hit = sum(1 for v in vals if v in club)
        if hit > 500:
            print("rel=%3d u32 distinct=%5d clubhit=%6d" % (rel, len(set(vals)), hit))

    print("--- prefix u16 slots 0..40 ---")
    for off in range(0, 40, 2):
        vals = [struct.unpack_from("<H", p, s + off)[0] for (s, e, L) in fr]
        hit = sum(1 for v in vals if v in club)
        if hit > 3000:
            print("off=%3d u16 distinct=%5d clubhit=%6d" % (off, len(set(vals)), hit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
