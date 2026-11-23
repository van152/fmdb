#!/usr/bin/env python3
"""t88-fix5: per-type row layout census for table_45.

Usage: py -V:3.12 -I -B scripts/t88f5_types.py [--selftest] [--per 2]
"""
import argparse
import os
import struct
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")


def load():
    payload = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    raw = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    n = len(raw) // 4
    starts = list(struct.unpack("<%dI" % n, raw))
    return payload, starts


FOOTER = 8  # payload footer_hex 00000001775f0100 (row_frame.json)


def split(payload, starts):
    out = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(payload) - FOOTER
        r = payload[s:e]
        nl = struct.unpack("<I", r[37:41])[0]
        out.append((r[:37], r[41:41 + nl], r[41 + nl:-13], r[-13:]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--per", type=int, default=1)
    ap.add_argument("--type", type=int, default=-1)
    a = ap.parse_args()
    payload, starts = load()
    rows = split(payload, starts)
    if a.selftest:
        bad = sum(1 for p, nm, sf, idt in rows if len(sf) != 26)
        print("selftest rows=%d bad_suffix=%d" % (len(rows), bad))
        return 0 if len(rows) == 84477 and bad == 0 else 1
    cnt = Counter(p[4] for p, nm, sf, idt in rows)
    print("types:", len(cnt), "null255:", cnt.get(255))
    seen = defaultdict(int)
    for i, (p, nm, sf, idt) in enumerate(rows):
        t = p[4]
        if a.type >= 0 and t != a.type:
            continue
        if seen[t] >= a.per:
            continue
        seen[t] += 1
        print("t=%3d #%d n=%d name=%r" % (t, cnt[t], i, nm.decode("utf-8", "replace")[:22]))
        print("   pre9..36:", p[9:].hex(" "))
        print("   suf:", sf.hex(" "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
