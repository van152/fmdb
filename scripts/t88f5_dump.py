#!/usr/bin/env python3
"""t88-fix5: dump raw table_45 rows for layout inspection.

Usage: py -V:3.12 -I -B scripts/t88f5_dump.py [--help] [--selftest] [--n 8] [--type X]
"""
import argparse
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")
PAYLOAD = os.path.join(OUT2, "_p_server_45.bin")
STARTS = os.path.join(OUT2, "_starts.bin")


def load():
    payload = open(PAYLOAD, "rb").read()
    raw = open(STARTS, "rb").read()
    n = len(raw) // 4
    starts = list(struct.unpack("<%dI" % n, raw))
    return payload, starts


def rows(payload, starts):
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(payload)
        yield i, payload[s:e]


def selftest():
    payload, starts = load()
    assert len(starts) == 84477, len(starts)
    ok = 0
    for i, r in rows(payload, starts):
        if i >= 200:
            break
        nl = struct.unpack("<I", r[37:41])[0]
        if len(r) == 80 + nl:
            ok += 1
    print("selftest rowlen_ok=%d/200" % ok)
    return 0 if ok == 200 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--type", type=int, default=-1)
    ap.add_argument("--skip", type=int, default=0)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    payload, starts = load()
    shown = 0
    for i, r in rows(payload, starts):
        if i < a.skip:
            continue
        t = r[4]
        if a.type >= 0 and t != a.type:
            continue
        nl = struct.unpack("<I", r[37:41])[0]
        nm = r[41:41 + nl]
        print("#%d len=%d type=%d name=%r" % (i, len(r), t, nm.decode("utf-8", "replace")))
        pre = r[:37]
        print("  pre:", pre.hex(" "))
        suf = r[41 + nl:len(r) - 13]
        print("  suf(%d):" % len(suf), suf.hex(" "))
        print("  id :", r[len(r) - 13:].hex(" "))
        shown += 1
        if shown >= a.n:
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
