"""t76b scratch: media(7) mid — count-prefixed 12B-triple tail block test."""
import runpy, sys, struct
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def media_rows(arch):
    raw = load(7, arch)
    n = u32(raw, 8)
    hi = len(raw) - 8
    pos, rows = 14, []
    for j in range(n):
        k = u32(raw, pos)
        best = None
        for e in range(pos + 13 + 4 + k, hi + 1):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
            if o != j or u1 != u2 or u1 == 0 or m != 0:
                continue
            if e < hi:
                k2 = u32(raw, e)
                if k2 > 64:
                    continue
                try:
                    nm = raw[e + 4:e + 4 + k2].decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if not nm or any(ord(c) < 0x20 for c in nm):
                    continue
            best = e
        rows.append((pos, best))
        pos = best
    return raw, rows


for arch in ("client", "server"):
    raw, rows = media_rows(arch)
    print(f"=== {arch}")
    okc = Counter()
    detail = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        tail = body[a:len(body) - 18]        # drop 5B prefix + 13B identity
        # walk triples backwards from the end
        ntr = 0
        p = len(tail)
        while p - 12 >= 0:
            x, y, z = struct.unpack_from("<III", tail, p - 12)
            if x == y and z == 0:
                ntr += 1
                p -= 12
            else:
                break
        okc[("triples_tail", ntr)] += 1
        detail.append((j, len(tail), ntr, p, tail[:max(0, p)].hex()[:40]))
    print("  trailing 12B-triple counts:", okc.most_common(10))
    print("  rows where tail is EXACTLY 5 + 12n:", sum(1 for d in detail if d[3] == 5))
    print("  prefix-len hist (bytes before triple block):",
          Counter(d[3] for d in detail).most_common(10))
    for d in detail[:6]:
        print("   row%d tail=%d ntr=%d prefix=%d %s" % d)
