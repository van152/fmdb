"""t76b scratch: FK-domain extraction for award/language/media."""
import runpy, sys, struct
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def fixed_uids(tid, arch, H, S, ident_off):
    raw = load(tid, arch)
    n = (len(raw) - H - 8) // S
    return [u32(raw, H + j * S + ident_off + 4) for j in range(n)], n


def var_chain(raw, n, lo, hi):
    ways = [defaultdict(int) for _ in range(n + 1)]
    ways[0][lo] = 1
    for j in range(n):
        idx = [p for p in ways[j]]
        for p in idx:
            for e in range(p + 13, hi + 1):
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                if o == j and u1 == u2 != 0 and m == 0:
                    ways[j + 1][e] += ways[j][p]
    return ways


def nation_uids():
    raw = load(10)
    n = u32(raw, 8)
    ways = var_chain(raw, n, 14, len(raw) - 8)
    ends = [e for e, w in ways[n].items() if w]
    print("t10 ends", ends)
    # back-walk greedily
    rows = []
    e = ends[0]
    for j in range(n - 1, -1, -1):
        found = None
        for p in range(14, e - 12):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
            if o == j and u1 == u2 != 0 and m == 0:
                # need reachable prefix; accept if ways[j][p] > 0
                if ways[j].get(p, 0) > 0:
                    found = p
                    break
        rows.append((j, found, e, u32(raw, e - 9)))
        e = found
    rows.reverse()
    return [r[3] for r in rows]


if __name__ == "__main__":
    cu, cn = fixed_uids(5, "client", 14, 34, 21)
    print("continent", cn, cu)
    comp, cpn = fixed_uids(25, "client", 14, 127, 114)
    print("comp", cpn, len(set(comp)), comp[:6])
    stg, sn = fixed_uids(23, "client", 14, 14, 1)
    print("t23", sn, stg[:8])
    nat = nation_uids()
    print("nation", len(nat), len(set(nat)), nat[:8])
