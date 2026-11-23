#!/usr/bin/env python3
"""t88-fix5: per-rec_type x per-slot domain census with reference-set membership.

Wire frame (this lane): pre[0..36] + [u32 len][name] + tail[26] + identity[13]
tail grid: 3x date4 @0,4,8 + u32 @12 + u16 @16,18,20,22,24  (12+4+10 = 26)

Usage: py -V:3.12 -I -B scripts/t88f5_join.py [--selftest] [--out PATH] [--types 10,24]
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

PRE_U32 = [0, 5, 9, 13, 17, 21, 25, 29, 33]
TAIL_DATE = [0, 4, 8]
TAIL_U32 = [12]
TAIL_U16 = [16, 18, 20, 22, 24]
TAIL_U8 = [24, 25]


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
                     "tail": r[41 + nl:len(r) - 13], "len": len(r)})
    return rows


def d4(v):
    """decode wire date4.

    record_get 'endt' getter re-packs: year=[+0x46], doy=[+0x44]&0x1ff, extra=[+0x44]>>9.
    Wire u32 = w0 | (w1<<16) with w0=doy|extra<<9, w1=year.
    => year = v>>16, doy = v & 0x1ff, extra = (v>>9)&0x7f
    """
    return (v >> 16, v & 0x1FF, (v >> 9) & 0x7F)


def d4ok(v):
    y, doy, _ = d4(v)
    return 1850 <= y <= 2120 and 1 <= doy <= 366


def u(b, o, w):
    return int.from_bytes(b[o:o + w], "little")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT3, "slot_domains.json"))
    ap.add_argument("--types", default="")
    ap.add_argument("--min", type=int, default=30)
    a = ap.parse_args()
    payload, starts = load()
    rows = parse(payload, starts)
    if a.selftest:
        # sentinel 0x076c0001 must decode to year 1900, doy 1
        y, doy, lo = d4(0x076C0001)
        print("selftest rows=%d d4(0x076c0001)=y%d doy%d extra%d ok=%s"
              % (len(rows), y, doy, lo, (y, doy) == (1900, 1)))
        return 0 if len(rows) == 84477 and (y, doy) == (1900, 1) else 1
    refs = json.load(open(REFS, encoding="utf-8"))
    sets = {k: set(v) for k, v in refs.items()}
    by = defaultdict(list)
    for r in rows:
        by[r["pre"][4]].append(r)
    want = [int(x) for x in a.types.split(",")] if a.types else None
    out = {}
    for t in sorted(by):
        grp = by[t]
        if len(grp) < a.min or (want and t not in want):
            continue
        ent = {"n": len(grp), "name_frac": round(sum(1 for r in grp if r["name"]) / len(grp), 3),
               "prefix": {}, "tail": {}}
        for o in PRE_U32:
            vals = [u(r["pre"], o, 4) for r in grp]
            c = Counter(vals)
            ent["prefix"]["u32@%d" % o] = {
                "ff": round(c.get(0xFFFFFFFF, 0) / len(vals), 3),
                "zero": round(c.get(0, 0) / len(vals), 3),
                "distinct": len(c),
                "max": max(vals),
                "ref": {k: round(sum(1 for v in vals if v in s) / len(vals), 3)
                        for k, s in sets.items()},
            }
        for o in TAIL_DATE:
            vals = [u(r["tail"], o, 4) for r in grp]
            okv = [d4(v) for v in vals]
            sent = sum(1 for v in vals if v == 0x076C0001)
            ok = sum(1 for v in vals if d4ok(v))
            ys = sorted(set(y for y, _, _ in okv if 1850 <= y <= 2120))
            ent["tail"]["date@%d" % o] = {
                "sentinel_076c0001": round(sent / len(vals), 3),
                "ff": round(sum(1 for v in vals if v == 0xFFFFFFFF) / len(vals), 3),
                "date_ok": round(ok / len(vals), 3),
                "year_min": ys[0] if ys else None, "year_max": ys[-1] if ys else None,
                "ref": {k: round(sum(1 for v in vals if v in s) / len(vals), 3)
                        for k, s in sets.items()},
            }
        for o in TAIL_U32:
            vals = [u(r["tail"], o, 4) for r in grp]
            c = Counter(vals)
            ent["tail"]["u32@%d" % o] = {
                "ff": round(c.get(0xFFFFFFFF, 0) / len(vals), 3),
                "zero": round(c.get(0, 0) / len(vals), 3),
                "distinct": len(c), "max": max(vals),
                "ref": {k: round(sum(1 for v in vals if v in s) / len(vals), 3)
                        for k, s in sets.items()},
            }
        for o in TAIL_U16:
            vals = [u(r["tail"], o, 2) for r in grp]
            c = Counter(vals)
            ent["tail"]["u16@%d" % o] = {
                "ff": round(c.get(0xFFFF, 0) / len(vals), 3),
                "zero": round(c.get(0, 0) / len(vals), 3),
                "distinct": len(c), "max": max(vals),
                "top": [[v, n] for v, n in c.most_common(4)],
            }
        for o in TAIL_U8:
            vals = [u(r["tail"], o, 1) for r in grp]
            c = Counter(vals)
            ent["tail"]["u8@%d" % o] = {"ff": round(c.get(0xFF, 0) / len(vals), 3),
                                        "distinct": len(c),
                                        "top": [[v, n] for v, n in c.most_common(4)]}
        out[str(t)] = ent
    os.makedirs(OUT3, exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=0)
    print("types=%d -> %s" % (len(out), a.out))
    for t in sorted(out, key=int):
        e = out[t]
        p = e["prefix"]
        def fmt(sl):
            d = p[sl]["ref"]
            return "%s=%s" % (sl, ",".join("%s:%.2f" % (k, d[k]) for k in ("t3", "t24", "t25")))
        print("t=%-4s n=%-5d nm=%.2f  %s | %s | %s | %s | %s" % (
            t, e["n"], e["name_frac"],
            fmt("u32@9"), fmt("u32@13"), fmt("u32@21"), fmt("u32@29"), fmt("u32@33")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
