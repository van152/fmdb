#!/usr/bin/env python3
"""t88-fix2 probe2: 找 rec_type 列 / UID 列(小整数列 + 分组一致性)。

用法: py -V:3.12 -I -B scripts/t88_probe2.py [--small] [--group]
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

    if "--small" in argv:
        print("byte columns with 3..48 distinct values (off: values)")
        for off in range(0, 80):
            c = collections.Counter(p[a[i]+off] for i in range(n))
            if 3 <= len(c) <= 48:
                print(f"{off}: n={len(c)} {sorted(c.items())}")

    if "--group" in argv:
        # 每行 26B body 的 ff-mask 类
        def bb(i):
            return a[i] + 41 + struct.unpack_from("<I", p, a[i]+37)[0]
        cls = [tuple(p[bb(i)+k] == 0xff for k in range(26)) for i in range(n)]
        # 找哪些列在 mask 类内近乎常量
        print("col  const-within-mask  distinct")
        best = []
        for off in range(0, 80):
            for w in (1, 2, 4):
                if off + w > 80: continue
                tab = collections.defaultdict(set)
                for i in range(n):
                    tab[cls[i]].add(int.from_bytes(p[a[i]+off:a[i]+off+w], "little"))
                rate = sum(1 for k, v in tab.items() if len(v) == 1) / len(tab)
                if rate > 0.9:
                    best.append((rate, off, w, len(tab)))
        for r in sorted(best, reverse=True)[:25]:
            print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
