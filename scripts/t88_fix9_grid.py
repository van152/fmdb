"""t88-fix9 grid: per-rec_type wire field census over the 26B body + 37B prefix.

Read-only. Writes scratch/t88/out3/_grid.json.

用法: py -V:3.12 -I -B scripts/t88_fix9_grid.py [--rt N] [--selftest]
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
O3 = os.path.join(S, "out3")


def load():
    p = open(os.path.join(O2, "_p_server_45.bin"), "rb").read()
    sb = open(os.path.join(O2, "_starts.bin"), "rb").read()
    st = list(struct.unpack("<%dI" % (len(sb) // 4), sb))
    n = len(st)
    rows = []
    for i in range(n):
        a = st[i]
        b = st[i + 1] if i + 1 < n else len(p) - 8
        nl = struct.unpack_from("<I", p, a + 37)[0]
        rows.append((a, b, a + 41 + nl))
    return p, rows


def refsets():
    d = json.load(open(os.path.join(S, "refsets.json"), encoding="utf-8"))
    return {k: set(v) for k, v in d.items()}


def date_ok(k):
    """FM packed date heuristic: (y-1900)<<9 | m<<5 | d."""
    d = k & 31
    m = (k >> 5) & 15
    y = (k >> 9) + 1900
    return 1 <= d <= 31 and 1 <= m <= 12 and 1900 <= y <= 2100


def stat(vals, n):
    c = collections.Counter(vals)
    return {
        "d": len(c),
        "min": min(c),
        "max": max(c),
        "ff": round(c.get(0xFFFFFFFF, 0) / n, 3),
        "z": round(c.get(0, 0) / n, 3),
        "top": [[k, round(v / n, 3)] for k, v in c.most_common(4)],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rt", type=int, default=-1)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    p, rows = load()
    if a.selftest:
        assert len(rows) == 84477
        assert all(b - bo == 26 + 13 for _, b, bo in rows)
        print("selftest ok rows=%d body=26 identity=13" % len(rows))
        return 0
    rs = refsets()
    by = collections.defaultdict(list)
    for r in rows:
        by[p[r[0] + 4]].append(r)
    out = {}
    for rt in sorted(by):
        if a.rt >= 0 and rt != a.rt:
            continue
        sel = by[rt]
        n = len(sel)
        rec = {"n": n, "body": {}, "prefix": {}}
        for o in range(26):
            for w, fmt in ((1, "B"), (2, "H"), (4, "I")):
                if o + w > 26:
                    continue
                vals = [struct.unpack_from("<" + fmt, p, bo + o)[0] for _, _, bo in sel]
                s = stat(vals, n)
                s["w"] = w
                if w == 2:
                    s["date"] = round(sum(1 for v in vals if date_ok(v)) / n, 3)
                if w == 4:
                    for k, ss in rs.items():
                        s["ref_" + k] = round(sum(1 for v in vals if v in ss) / n, 3)
                rec["body"]["%d_%d" % (o, w)] = s
        for o in (0, 5, 9, 13, 17, 21, 25, 29, 33):
            vals = [struct.unpack_from("<I", p, r[0] + o)[0] for r in sel]
            s = stat(vals, n)
            s["w"] = 4
            for k, ss in rs.items():
                s["ref_" + k] = round(sum(1 for v in vals if v in ss) / n, 3)
            rec["prefix"][o] = s
        out[str(rt)] = rec
    if a.rt < 0:
        json.dump(out, open(os.path.join(O3, "_grid.json"), "w"), indent=0)
    # compact print
    for rt in sorted(out, key=int):
        if a.rt >= 0 and int(rt) != a.rt:
            continue
        rec = out[rt]
        print("== rt %s n=%d" % (rt, rec["n"]))
        for o in range(26):
            b1 = rec["body"].get("%d_1" % o)
            b2 = rec["body"].get("%d_2" % o)
            b4 = rec["body"].get("%d_4" % o)
            line = "  o%02d" % o
            if b1:
                line += " u8 d=%-3d r%-4d" % (b1["d"], b1["max"])
            if b2:
                line += " | u16 d=%-3d r%-5d ff%.2f dt%.2f" % (
                    b2["d"], b2["max"], b2["ff"], b2.get("date", 0))
            if b4:
                line += " | u32 ff%.2f c3=%.2f c4=%.2f" % (
                    b4["ff"], b4.get("ref_t3", 0), b4.get("ref_t24", 0))
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
