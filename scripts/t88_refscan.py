"""t88 refset scan: 在各 wire 偏移/宽度上找 refset 命中(refset 归约到 u32 子集)。

refsets: t3=club uids, t24=team, t25=comp, t10=? (全部来自 refsets.json)
用法: py -V:3.12 -I -B scripts/t88_refscan.py [--help] [--selftest]
输出 <=30 行/次, 只打印命中率高的行。
"""
import argparse
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
        rows.append((a, a + 41 + nl, b))  # pre_start, suf_start, end
    return p, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--minhit", type=float, default=0.30)
    a = ap.parse_args()
    p, rows = load_rows()
    refs = {k: set(v) for k, v in json.load(open(os.path.join(ROOT, "scratch", "t88", "refsets.json"))).items()}
    if a.selftest:
        assert len(rows) == 84477
        assert all(s + 26 + 13 == e for _, s, e in rows), "suffix split"
        print("selftest ok rows=%d refsets=%s" % (len(rows), {k: len(v) for k, v in refs.items()}))
        return 0

    # 只对 u32 (dword) 扫描; 参照 C++ 结构里 8 字节 id 对 = 两个 dword
    hits = {k: [] for k in refs}
    for part, offs in (("pre", range(0, 37)), ("suf", range(0, 26))):
        for off in offs:
            vals = []
            for s, u, e in rows:
                base = s if part == "pre" else u
                vals.append(struct.unpack_from("<I", p, base + off)[0])
            for k, st_ in refs.items():
                h = sum(1 for v in vals if v in st_)
                if h >= a.minhit * len(vals):
                    hits[k].append((part, off, h))
    for k in refs:
        top = sorted(hits[k], key=lambda x: -x[2])[:6]
        print("%-4s n=%-6d %s" % (k, len(refs[k]), top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
