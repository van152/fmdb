"""t88 rectype hunt v2: 找值域 ⊆ {10,13,24,25,26,27,28} 的槽 (f4_to_rectype 的 rectype 集)。

并做 layout-signature 纯度检验: 用 presence+日期 sentinel+id 槽 组成的签名, 看哪个字节
能最好地预测签名 (rec_type 应决定字段集)。
用法: py -V:3.12 -I -B scripts/t88_rectype2.py [--help] [--selftest]
"""
import argparse
import collections
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT2 = os.path.join(ROOT, "scratch", "t88", "out2")
FOOT = 8
SLOTS = [13, 17, 21, 25, 29, 33]
RT = {10, 13, 24, 25, 26, 27, 28}
FMT = {1: "<B", 2: "<H", 4: "<I"}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    p, rows = load_rows()
    if a.selftest:
        assert len(rows) == 84477
        print("selftest ok rows=%d" % len(rows))
        return 0

    sig = []
    for s, u, e in rows:
        pr = "".join("1" if struct.unpack_from("<I", p, s + o)[0] != 0xFFFFFFFF else "0" for o in SLOTS)
        dt = "".join("S" if struct.unpack_from("<I", p, u + 4 * k)[0] == 0x076C0001 else "x" for k in range(3))
        sig.append(pr + dt)
    print("layout signatures: %d distinct" % len(set(sig)))
    for k, v in collections.Counter(sig).most_common(10):
        print("  %s  %d" % (k, v))

    print("--- slots with domain subset of rectype set (u8/u16/u32) ---")
    for part, lim in (("pre", 37), ("suf", 26)):
        for w in (1, 2, 4):
            for off in range(0, lim - w + 1):
                if off % w:
                    continue
                vals = [struct.unpack_from(FMT[w], p, (s if part == "pre" else u) + off)[0] for s, u, e in rows]
                vs = set(vals)
                if vs <= RT and len(vs) >= 2:
                    print("  HIT %s+%-2d w%d values=%s" % (part, off, w, sorted(vs)))

    print("--- layout-signature purity (top 8) ---")
    scored = []
    for part, lim in (("pre", 37), ("suf", 26)):
        for w in (1, 2, 4):
            for off in range(0, lim - w + 1):
                if off % w:
                    continue
                vals = [struct.unpack_from(FMT[w], p, (s if part == "pre" else u) + off)[0] for s, u, e in rows]
                if len(set(vals)) > 64:
                    continue
                m = collections.defaultdict(collections.Counter)
                for v, sg in zip(vals, sig):
                    m[v][sg] += 1
                # 加权纯度: 每个值组里主签名占比
                pure = sum(c.most_common(1)[0][1] for c in m.values()) / len(vals)
                scored.append((pure, part, off, w, len(m)))
    for pure, part, off, w, d in sorted(scored, reverse=True)[:8]:
        print("  %-4s+%-2d w%d d=%-3d purity=%.4f" % (part, off, w, d, pure))
    return 0


if __name__ == "__main__":
    sys.exit(main())
