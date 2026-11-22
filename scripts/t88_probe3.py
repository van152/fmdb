#!/usr/bin/env python3
"""t88-fix2 probe3: 找 rec_type —— 用 payload ff-mask 类 × prefix 列 交叉表。

行解剖(本脚本自证): [0..36]=37B prefix | [37..40]=u32 namelen | name | 26B payload | 13B identity
用法: py -V:3.12 -I -B scripts/t88_probe3.py [--masks] [--xtab]
"""
from __future__ import annotations
import array, collections, pathlib, struct, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
O2 = ROOT / "scratch/t88/out2"


def load():
    a = array.array("I"); a.frombytes((O2 / "_starts.bin").read_bytes())
    p = (O2 / "_p_server_45.bin").read_bytes()
    return a, p, list(a[1:]) + [len(p)]


def anatomy(a, p, ends):
    n = len(a)
    pl = collections.Counter()
    for i in range(n):
        nl = struct.unpack_from("<I", p, a[i] + 37)[0]
        pl[len(p[a[i]:ends[i]]) - 41 - nl - 13] += 1
    return pl


def payloads(a, p, ends):
    out = []
    for i in range(len(a)):
        nl = struct.unpack_from("<I", p, a[i] + 37)[0]
        out.append(p[a[i] + 41 + nl: a[i] + 41 + nl + 26])
    return out


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__); return 0
    a, p, ends = load()
    n = len(a)
    print("payload_len_hist:", dict(anatomy(a, p, ends)))
    P = payloads(a, p, ends)
    mask = [tuple(b != 0xff for b in pl) for pl in P]
    print("distinct masks:", len(set(mask)))

    if "--masks" in argv:
        # 每种 mask 的 12 个 slot(每 2 字节)是否"存在"
        sl = collections.Counter()
        for m in mask:
            key = tuple(sum(m[k:k+2]) for k in range(0, 26, 2))
            sl[key] += 1
        print("slot-fill pattern (13 x 2B slots, count of non-ff bytes):")
        for k, c in sl.most_common(20):
            print(" ", k, c)

    if "--xtab" in argv:
        cls = {m: j for j, m in enumerate(dict.fromkeys(mask))}
        lab = [cls[m] for m in mask]
        ncls = len(cls)
        best = []
        for off in range(0, 37):
            tab = collections.defaultdict(collections.Counter)
            for i in range(n):
                tab[p[a[i] + off]][lab[i]] += 1
            nv = len(tab)
            if nv > 40: continue
            # 每列值内 mask 类集中度
            conc = sum(max(c.values()) for c in tab.values()) / n
            best.append((round(conc, 4), off, nv))
        print(f"mask_classes={ncls}; prefix cols by concentration:")
        for r in sorted(best, reverse=True)[:14]:
            print(" ", r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
