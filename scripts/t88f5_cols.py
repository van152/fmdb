#!/usr/bin/env python3
"""t88-fix5: per-rec_type column census (prefix 9..36 + suffix 0..25).

Usage: py -V:3.12 -I -B scripts/t88f5_cols.py [--selftest] [--out PATH] [--min 20]
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
REFS = os.path.join(ROOT, "scratch", "t88", "refsets.json")
FOOTER = 8


def load():
    payload = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    raw = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    n = len(raw) // 4
    starts = list(struct.unpack("<%dI" % n, raw))
    return payload, starts


def parse(payload, starts):
    rows = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(payload) - FOOTER
        r = payload[s:e]
        nl = struct.unpack("<I", r[37:41])[0]
        rows.append({
            "i": i,
            "pre": r[:37],
            "name": r[41:41 + nl],
            "suf": r[41 + nl:len(r) - 13],
            "id": r[len(r) - 13:],
            "len": len(r),
        })
    return rows


def u(b, o, w):
    return int.from_bytes(b[o:o + w], "little")


def is_date4(v):
    return 1 <= (v & 0x1FFFF) <= 366 and 1850 <= (v >> 17) <= 2120


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT3, "type_layout.json"))
    ap.add_argument("--min", type=int, default=20)
    a = ap.parse_args()
    payload, starts = load()
    rows = parse(payload, starts)
    if a.selftest:
        bad = [r["i"] for r in rows if len(r["suf"]) != 26]
        print("selftest rows=%d bad_suffix=%d" % (len(rows), len(bad)))
        return 0 if len(rows) == 84477 and not bad else 1
    refs = json.load(open(REFS, encoding="utf-8"))
    sets = {k: set(v) for k, v in refs.items()}
    by = defaultdict(list)
    for r in rows:
        by[r["pre"][4]].append(r)
    out = {}
    for t in sorted(by):
        grp = by[t]
        if len(grp) < a.min:
            out[str(t)] = {"n": len(grp), "skipped": True}
            continue
        cols = {}
        # prefix 4-byte slots 9..33 step 4, suffix 4-byte 0..22, plus u16/u8 spots
        slots = [("p", o, 4) for o in range(9, 34, 4)]
        slots += [("s", o, 4) for o in range(0, 24, 4)]
        slots += [("s", o, 2) for o in (16, 18, 20, 22, 24)]
        slots += [("s", o, 1) for o in (22, 23, 24, 25)]
        for tag, o, w in slots:
            key = "%s%d/%d" % (tag, o, w)
            if tag == "p":
                vals = [u(r["pre"], o, w) for r in grp]
            else:
                if o + w > 26:
                    continue
                vals = [u(r["suf"], o, w) for r in grp]
            mx = (1 << (8 * w)) - 1
            c = Counter(vals)
            top = c.most_common(3)
            mem = {k: round(sum(1 for v in vals if v in s) / len(vals), 3) for k, s in sets.items()}
            d4 = round(sum(1 for v in vals if is_date4(v)) / len(vals), 3) if w == 4 else None
            cols[key] = {
                "n": len(vals),
                "distinct": len(c),
                "sentinel": round(c.get(mx, 0) / len(vals), 3),
                "zero": round(c.get(0, 0) / len(vals), 3),
                "top": [[v, round(n / len(vals), 3)] for v, n in top],
                "max": max(vals),
                "ref": mem,
                "date4": d4,
            }
        out[str(t)] = {"n": len(grp), "cols": cols,
                       "names": round(sum(1 for r in grp if r["name"]) / len(grp), 3)}
    os.makedirs(OUT3, exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=0)
    print("types=%d written=%s" % (len(out), a.out))
    for t in sorted(out, key=int):
        if out[t].get("skipped"):
            continue
        print("t=%-4s n=%-6d names=%.2f" % (t, out[t]["n"], out[t]["names"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
