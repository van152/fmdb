#!/usr/bin/env python3
"""t88-fix2 probe4: 逐列 date4 / 小整数 / uid 判据(prefix 0..36 + payload 0..25)。

用法: py -V:3.12 -I -B scripts/t88_probe4.py [--date] [--u16] [--uid]
"""
from __future__ import annotations
import array, collections, json, pathlib, struct, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
O2 = ROOT / "scratch/t88/out2"


def load():
    a = array.array("I"); a.frombytes((O2 / "_starts.bin").read_bytes())
    p = (O2 / "_p_server_45.bin").read_bytes()
    return a, p, list(a[1:]) + [len(p)]


def cols(a, p):
    """返回 (name, base_index_fn, maxlen)。base 为行首或 payload 首。"""
    n = len(a)

    def pre(i, off, w):
        return int.from_bytes(p[a[i] + off: a[i] + off + w], "little")

    def pay(i, off, w):
        nl = struct.unpack_from("<I", p, a[i] + 37)[0]
        s = a[i] + 41 + nl + off
        return int.from_bytes(p[s:s + w], "little")
    return pre, pay, n


def date4_ok(v):
    d = v & 0x1FF
    m = (v >> 9) & 0x7F
    y = (v >> 16) & 0xFFFF
    return 1 <= d <= 31 and 0 <= m <= 12 and 1900 <= y <= 2100


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__); return 0
    a, p, ends = load()
    pre, pay, n = cols(a, p)
    ref = json.loads((ROOT / "scratch/t88/refsets.json").read_text())
    S = {k: set(v) for k, v in ref.items()}

    if "--date" in argv:
        print("date4 validity rate (excluding all-ff):")
        for tag, fn, lim in (("pre", pre, 37), ("pay", pay, 26)):
            for off in range(0, lim - 3):
                vals = [fn(i, off, 4) for i in range(n)]
                ff = sum(1 for v in vals if v == 0xFFFFFFFF)
                live = [v for v in vals if v != 0xFFFFFFFF]
                if not live: continue
                ok = sum(date4_ok(v) for v in live) / len(live)
                if ok > 0.9:
                    print(f"  {tag}+{off:<3} ff={ff/n:.3f} live={len(live):<6} date_ok={ok:.4f}")

    if "--u16" in argv:
        print("u16 columns: uniq / ff / zero / club-hit")
        for tag, fn, lim in (("pre", pre, 37), ("pay", pay, 26)):
            for off in range(0, lim - 1):
                vals = [fn(i, off, 2) for i in range(n)]
                u = len(set(vals))
                if u > 3000: continue
                ff = sum(1 for v in vals if v == 0xFFFF) / n
                z = sum(1 for v in vals if v == 0) / n
                hit = sum(1 for v in vals if v in S["t3"]) / n
                print(f"  {tag}+{off:<3} uniq={u:<6} ff={ff:.3f} z={z:.3f} club={hit:.3f}")

    if "--uid" in argv:
        print("u32 columns: uniq / ff / zero / club-hit / team-hit / comp-hit")
        for tag, fn, lim in (("pre", pre, 37), ("pay", pay, 26)):
            for off in range(0, lim - 3):
                vals = [fn(i, off, 4) for i in range(n)]
                ff = sum(1 for v in vals if v == 0xFFFFFFFF) / n
                hit = {k: sum(1 for v in vals if v in S[k]) / n for k in ("t3", "t24", "t25", "t10")}
                if max(hit.values()) < 0.5: continue
                print(f"  {tag}+{off:<3} ff={ff:.3f} uniq={len(set(vals))} "
                      f"club={hit['t3']:.3f} team={hit['t24']:.3f} comp={hit['t25']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
