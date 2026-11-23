#!/usr/bin/env python3
"""t88-fix2 probe: 全档槽位扫描(只读 out2 冻结产物),找 club FK / rec_type。

用法: FM24_DB_DIR=... py -V:3.12 -I -B scripts/t88_probe.py --scan
"""
from __future__ import annotations
import array, collections, json, pathlib, struct, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
O2 = ROOT / "scratch/t88/out2"
O3 = ROOT / "scratch/t88/out3"


def load():
    b = (O2 / "_starts.bin").read_bytes()
    a = array.array("I"); a.frombytes(b)
    p = (O2 / "_p_server_45.bin").read_bytes()
    ends = list(a[1:]) + [len(p)]
    return a, p, ends


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__); return 0
    a, p, ends = load()
    n = len(a)
    ref = json.loads((ROOT / "scratch/t88/refsets.json").read_text())
    S = {k: set(v) for k, v in ref.items()}
    print(f"rows={n} payload={len(p)}")
    rows = []
    for off in range(0, 61):
        vals = [int.from_bytes(p[a[i]+off:a[i]+off+4], "little") for i in range(n)]
        u = len(set(vals))
        hit = {k: round(sum(1 for v in vals if v in S[k])/n, 4) for k in S}
        rows.append((off, u, hit, min(vals), max(vals)))
    print("off  uniq   t3     t24    t25    t10    min        max")
    for off, u, hit, mn, mx in rows:
        print(f"{off:<4} {u:<6} {hit['t3']:<6} {hit['t24']:<6} {hit['t25']:<6} {hit['t10']:<6} {mn:<10} {mx}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
