"""t88 struct join: C++ struct offset -> wire offset 对照(指令证据 + 全档统计)。

C++ 端来自 record_get_handlers.json / record_get_tagmap.json 的 [rdi+0xNN] 读取。
用法: py -V:3.12 -I -B scripts/t88_structjoin.py [--help] [--selftest]
"""
import argparse
import collections
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")
FOOT = 8


def load_rows():
    p = open(os.path.join(OUT2, "_p_server_45.bin"), "rb").read()
    sb = open(os.path.join(OUT2, "_starts.bin"), "rb").read()
    st = list(struct.unpack("<%dI" % (len(sb) // 4), sb))
    n = len(st)
    rows = []
    for i in range(n):
        a = st[i]
        b = st[i + 1] if i + 1 < n else len(p) - FOOT
        nl = struct.unpack_from("<I", p, a + 37)[0]
        rows.append((a, a + 41 + nl, b))
    return p, rows


# C++ 端: handler -> (struct_off, width, signed, tag)
CPP = [
    ("stid", 0x18, 4), ("stid", 0x1c, 4), ("team", 0x20, 4), ("team", 0x24, 4),
    ("otht", 0x28, 4), ("otht", 0x2c, 4), ("comp", 0x30, 4), ("comp", 0x34, 4),
    ("stdt", 0x40, 2), ("stdt", 0x42, 2), ("endt", 0x44, 2), ("endt", 0x46, 2),
    ("stdb", 0x48, 2), ("stdb", 0x4a, 2), ("cash", 0x50, 4), ("atte", 0x50, 4),
    ("apps", 0x54, 2), ("gams", 0x54, 2), ("gols", 0x56, 2), ("fsgt", 0x58, 2),
    ("ogls", 0x58, 2), ("rati", 0x5a, 1), ("info", 0x5b, 1), ("rrea", 0x5c, 1),
    ("cnst", 0x5d, 1), ("etin", 0x5d, 1),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        assert all(u + 26 + 13 == e for _, u, e in rows), "suf=26, ident=13"
        print("selftest ok rows=%d suffix=26 ident=13" % len(rows))
        return 0

    print("== 假设: wire_suf_off = struct_off - 0x40 ; 校验每槽 domain ==")
    for tag, so, w in CPP:
        wo = so - 0x40
        fmt = {1: "<B", 2: "<H", 4: "<I"}[w]
        vals = [struct.unpack_from(fmt, p, u + wo)[0] for s, u, e in rows]
        c = collections.Counter(vals)
        ff = c.get(0xFFFFFFFF if w == 4 else (0xFFFF if w == 2 else 0xFF), 0)
        print("  %-4s cpp+0x%02x -> suf+%-2d w%d d=%-6d ff=%-6d top=%s" % (
            tag, so, wo, w, len(c), ff, c.most_common(2)))

    print("== 尾部闭合: struct 0x40..0x5d = %d B vs wire suffix 26 B ==" % (0x5E - 0x40))
    print("== rec_type cpp+0x5e -> suf+30 (超出 26B 后缀) ==")

    print("== pre 区: 每字节 domain ==")
    for o in range(37):
        c = collections.Counter(p[s + o] for s, u, e in rows)
        print("  pre+%-2d d=%-4d ff=%6d zero=%6d top=%s" % (
            o, len(c), c.get(0xFF, 0), c.get(0, 0), c.most_common(3)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
