"""t88 slot scan: 前缀 0..36 / 后缀 39B 的槽位统计(全档 84476 行)。

用法: py -V:3.12 -I -B scripts/t88_slot_scan.py [--help] [--selftest] [--part pre|suf|all]
输出 <=30 行/次。
"""
import argparse
import collections
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")


def load():
    p = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    sb = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    st = list(struct.unpack("<%dI" % (len(sb) // 4), sb))
    return p, st


def parts(p, st):
    """yield (idx, pre_start, suf_start, rowlen)"""
    n = len(st)
    for i in range(n - 1):  # 末行是 footer 残片, 排除
        a = st[i]
        b = st[i + 1]
        nl = struct.unpack_from("<I", p, a + 37)[0]
        yield i, a, a + 41 + nl, b - a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--part", default="all")
    ap.add_argument("--sufmax", type=int, default=36)
    a = ap.parse_args()
    p, st = load()
    club = set(json.load(open(os.path.join(ROOT, "scratch", "t88", "club.json")))["uids"])
    if a.selftest:
        it = list(parts(p, st))
        assert len(it) == 84476, len(it)
        assert all(suf + 39 == rowlen + st[i] for i, _, suf, rowlen in it), "suffix!=39"
        print("selftest ok rows=%d club=%d" % (len(it), len(club)))
        return 0

    rows = list(parts(p, st))
    print("rows=%d club_uids=%d" % (len(rows), len(club)))
    print("%-4s %-4s %-6s %-7s %-6s %-8s %s" % ("part", "off", "width", "distinct", "club", "top", "flags"))
    if a.part in ("pre", "all"):
        for off in range(0, 33):
            vals = [struct.unpack_from("<I", p, s + off)[0] for _, s, _, L in rows]
            d = len(set(vals))
            ch = sum(1 for v in vals if v in club)
            top = collections.Counter(vals).most_common(2)
            flag = ""
            if top[0][1] > 0.98 * len(vals):
                flag += "CONST "
            if d <= 4:
                flag += "SMALL "
            print("%-4s %-4d %-6s %-7d %-6d %-8s %s" % ("pre", off, "u32", d, ch, top, flag))
    if a.part in ("suf", "all"):
        for off in range(0, a.sufmax):
            vals = [struct.unpack_from("<I", p, u + off)[0] for _, _, u, L in rows]
            d = len(set(vals))
            ch = sum(1 for v in vals if v in club)
            top = collections.Counter(vals).most_common(2)
            flag = ""
            if top[0][1] > 0.98 * len(vals):
                flag += "CONST "
            if d <= 4:
                flag += "SMALL "
            print("%-4s %-4d %-6s %-7d %-6d %-8s %s" % ("suf", off, "u32", d, ch, top, flag))
    return 0


if __name__ == "__main__":
    sys.exit(main())
