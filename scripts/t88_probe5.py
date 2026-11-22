#!/usr/bin/env python3
"""t88-fix2 probe5: payload 槽位 × 引用集命中(分 mask 类)。

用法: py -V:3.12 -I -B scripts/t88_probe5.py [--slots] [--byte4]
"""
from __future__ import annotations
import array, collections, json, pathlib, struct, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
O2 = ROOT / "scratch/t88/out2"


def load():
    a = array.array("I"); a.frombytes((O2 / "_starts.bin").read_bytes())
    p = (O2 / "_p_server_45.bin").read_bytes()
    return a, p, list(a[1:]) + [len(p)]


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__); return 0
    a, p, ends = load()
    n = len(a)
    ref = json.loads((ROOT / "scratch/t88/refsets.json").read_text())
    S = {k: set(v) for k, v in ref.items()}

    def bb(i):
        return a[i] + 41 + struct.unpack_from("<I", p, a[i] + 37)[0]

    def pl(i):
        return p[bb(i):bb(i) + 26]

    if "--byte4" in argv:
        c4 = [p[a[i] + 4] for i in range(n)]
        namelen = [struct.unpack_from("<I", p, a[i] + 37)[0] for i in range(n)]
        print("byte4  n     namelen0  clubhit   masks")
        tab = collections.defaultdict(list)
        for i in range(n):
            tab[c4[i]].append(i)
        for v in sorted(tab):
            idx = tab[v]
            nl0 = sum(1 for i in idx if namelen[i] == 0)
            ch = sum(1 for i in idx if struct.unpack_from("<I", p, a[i])[0] in S["t3"])
            m = len({tuple(x != 0xff for x in pl(i)) for i in idx})
            print(f"{v:<6} {len(idx):<5} {nl0:<9} {ch/len(idx):<9.3f} {m}")

    if "--slots" in argv:
        # 按 mask 类分组,报每 2 字节槽的引用命中
        cls = collections.defaultdict(list)
        for i in range(n):
            cls[tuple(x != 0xff for x in pl(i))].append(i)
        top = sorted(cls.items(), key=lambda kv: -len(kv[1]))[:6]
        for m, idx in top:
            print("mask", "".join("F" if x else "." for x in m), "n=", len(idx))
            for off in range(0, 25):
                for w in (2, 4):
                    if off + w > 26: continue
                    vals = [int.from_bytes(pl(i)[off:off + w], "little") for i in idx]
                    ff = sum(1 for v in vals if v == (1 << (8 * w)) - 1)
                    if ff > 0.9 * len(vals): continue
                    hit = {k: sum(1 for v in vals if v in S[k]) / len(vals) for k in S}
                    best = max(hit.items(), key=lambda kv: kv[1])
                    if best[1] > 0.2:
                        print(f"  +{off} w={w} ff={ff/len(vals):.2f} {best[0]}={best[1]:.3f} uniq={len(set(vals))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
