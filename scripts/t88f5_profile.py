#!/usr/bin/env python3
"""t88-fix5: compact per-rec_type byte profile of prefix u32 slots + tail bytes.

Usage: py -V:3.12 -I -B scripts/t88f5_profile.py [--selftest] [--types 24,25] [--full]
"""
import argparse
import json
import os
import struct
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")
FOOTER = 8
PRE_U32 = [0, 5, 9, 13, 17, 21, 25, 29, 33]


def load():
    payload = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    raw = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    n = len(raw) // 4
    return payload, list(struct.unpack("<%dI" % n, raw))


def parse(payload, starts):
    rows = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(payload) - FOOTER
        r = payload[s:e]
        nl = struct.unpack("<I", r[37:41])[0]
        rows.append({"i": i, "pre": r[:37], "name": r[41:41 + nl],
                     "tail": r[41 + nl:len(r) - 13]})
    return rows


def d4ok(v):
    y = v >> 16
    return 1850 <= y <= 2120 and 1 <= (v & 0x1FF) <= 366


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--types", default="")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT3, "byte_profile.json"))
    a = ap.parse_args()
    payload, starts = load()
    rows = parse(payload, starts)
    if a.selftest:
        print("selftest rows=%d tail26=%d" % (len(rows), sum(1 for r in rows if len(r["tail"]) == 26)))
        return 0 if len(rows) == 84477 else 1
    by = defaultdict(list)
    for r in rows:
        by[r["pre"][4]].append(r)
    want = [int(x) for x in a.types.split(",")] if a.types else sorted(by)
    out = {}
    for t in want:
        grp = by[t]
        ent = {"n": len(grp), "pre": {}, "tail": {}}
        for o in PRE_U32:
            vals = [int.from_bytes(r["pre"][o:o + 4], "little") for r in grp]
            c = Counter(vals)
            ent["pre"]["@%d" % o] = {
                "ff": round(c.get(0xFFFFFFFF, 0) / len(vals), 2),
                "z": round(c.get(0, 0) / len(vals), 2),
                "d": len(c), "mx": max(vals),
                "d4": round(sum(1 for v in vals if d4ok(v)) / len(vals), 2),
            }
        # tail: byte-level, plus sliding u16 and date4 windows
        for o in range(26):
            vals = [r["tail"][o] for r in grp]
            c = Counter(vals)
            ent["tail"]["b%d" % o] = {"ff": round(c.get(0xFF, 0) / len(vals), 2),
                                      "z": round(c.get(0, 0) / len(vals), 2),
                                      "d": len(c)}
        ent["u16"] = {}
        for o in range(0, 25):
            vals = [int.from_bytes(r["tail"][o:o + 2], "little") for r in grp]
            c = Counter(vals)
            ent["u16"]["@%d" % o] = {"ff": round(c.get(0xFFFF, 0) / len(vals), 2),
                                     "z": round(c.get(0, 0) / len(vals), 2),
                                     "d": len(c), "mx": max(vals)}
        ent["d4"] = {}
        for o in range(0, 23):
            vals = [int.from_bytes(r["tail"][o:o + 4], "little") for r in grp]
            ent["d4"]["@%d" % o] = round(sum(1 for v in vals if d4ok(v)) / len(vals), 2)
        out[str(t)] = ent
    os.makedirs(OUT3, exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=0)
    print("types=%d -> %s" % (len(out), a.out))
    for t in want:
        e = out[str(t)]
        d4 = e["d4"]
        best = sorted(d4.items(), key=lambda kv: -kv[1])[:4]
        print("t=%-4d n=%-5d d4windows=%s" % (t, e["n"],
              " ".join("%s:%.2f" % (k, v) for k, v in best)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
