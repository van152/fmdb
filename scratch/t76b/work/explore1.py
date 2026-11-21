"""t76b scratch: payload probes (not a deliverable)."""
import runpy, sys, struct, json, itertools
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))


def dump():
    return runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")


D = dump()
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def fixed_uids(tid, arch, H, S, ident_off):
    raw = load(tid, arch)
    n = (len(raw) - H - 8) // S
    return [u32(raw, H + j * S + ident_off + 4) for j in range(n)]


def var_uids_chain(raw, n, lo, hi, ordinal_aware=True):
    """Find all identity-trailer chains; return list of (uids, ends)."""
    from collections import defaultdict
    ways = [defaultdict(int) for _ in range(n + 1)]
    prev = [dict() for _ in range(n + 1)]
    ways[0][lo] = 1
    for j in range(n):
        for pos in list(ways[j]):
            e = pos + 13
            while e <= hi:
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                ok = (o == j and u1 == u2 != 0 and m == 0) if ordinal_aware else (u1 == u2 != 0 and m == 0)
                if ok:
                    if e not in ways[j + 1]:
                        prev[j + 1][e] = pos
                    ways[j + 1][e] += ways[j][pos]
                e += 1
    return ways, prev


if __name__ == "__main__":
    raw9 = load(9)
    print("t9 len", len(raw9), "hdr", raw9[:14].hex())
    ways, prev = var_uids_chain(raw9, 251, 14, len(raw9) - 8)
    print("t9 chains ending at footer:", dict(ways[251]))
