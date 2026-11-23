"""t112 probe — solve t10 NATION unknown vector element sizes by exhaustive walk.

Walks all 251 rows of server/client table_10 with byte-accounting only; the three
element parsers missing decompilations (sub_1415CFD70, sub_141072F60, sub_1415CFEA0)
plus the empirically-suspected 605B0 element get candidate sizes. A candidate closes
when the walk lands exactly on footer_off with every row's identity ordinal == row idx.
"""
import itertools
import pathlib
import struct
import sys
from collections import Counter

ROOT = pathlib.Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import t112_fm24_reader as R  # noqa: E402

# op = ("u", n) | ("rep", n, size) | ("v", count_bytes, elem_size)
# elem_size may be a callable-like sentinel via dict lookup of symbolic names.
S3, S7, S10, S605 = "s3", "s7", "s10", "s605"  # symbolic size slots


def server_ops():
    return [
        ("u", 4),
        ("v", 2, 4),         # v128  loop READ 4 elements
        ("v", 4, 4),         # v126  loop READ 4 elements
        ("v", 2, S3),        # v127  loop sub_1415CFD70  <-- unknown
        ("rep", 6, 4),
        ("v", 4, 25),        # v125  sub_14144C6A0 (25B)
        ("v", 4, 12),        # v135  [u32, DATE, DATE]
        ("v", 4, S7),        # 143EE0430 -> sub_141072F60 <-- unknown
        ("u", 1), ("u", 4), ("u", 4), ("u", 4), ("u", 4),
        ("u", 1), ("u", 1), ("u", 4), ("u", 1),
        ("v", 1, 5),         # u8 count, [u32,u8] via 143EF2D20
        ("v", 4, S10),       # v133 sub_1415CFEA0 <-- unknown
        ("v", 4, S10),       # v136 sub_1415CFEA0 <-- unknown
        ("v", 4, S605),      # v126-2 sub_1410605B0 (hand: 12B)
        ("rep", 10, 4), ("u", 2), ("u", 1),
        ("u", 12),           # identity
    ]


def client_ops():
    return [
        ("u", 1), ("u", 4), ("u", 4), ("u", 4), ("u", 4),
        ("u", 1), ("u", 1), ("u", 4), ("u", 1),
        ("v", 1, 5),
        ("v", 4, S10),
        ("v", 4, S10),
        ("v", 4, 12),
        ("u", 12),
    ]


def walk(mv, nrows, footer_off, ops, sizes, ident_check=True, diag=False):
    """Byte-accounting walk; returns (True, vec_stats) or (False, None).

    vec_stats: list of Counter per vector op with the counts seen.
    diag: returns (False, (row, pos, op, detail)) at first failure.
    """
    pos = 13
    stats = [Counter() for op in ops if op[0] == "v"]
    for i in range(nrows):
        row0 = pos
        pos += 1  # flag
        vi = 0
        for op in ops:
            k = op[0]
            if k == "u":
                n = op[1]
                if pos + n > footer_off:
                    return (False, (i, pos, op, "oob")) if diag else (False, None)
                if n == 12 and ident_check:
                    if int.from_bytes(mv[pos : pos + 4], "little") != i:
                        return (False, (i, pos, op, f"id={bytes(mv[pos:pos+12]).hex()}")) if diag else (False, None)
                pos += n
            elif k == "rep":
                n = op[2]
                pos += op[1] * n
                if pos > footer_off:
                    return (False, (i, pos, op, "oob-rep")) if diag else (False, None)
            else:  # v
                cn, es = op[1], op[2]
                if pos + cn > footer_off:
                    return (False, (i, pos, op, "oob-count")) if diag else (False, None)
                c = int.from_bytes(mv[pos : pos + cn], "little")
                stats[vi][c] += 1
                vi += 1
                pos += cn
                if c:
                    if isinstance(es, str):
                        es = sizes[es]
                    if es <= 0 or pos + c * es > footer_off:
                        return (False, (i, pos, op, f"c={c} es={es}")) if diag else (False, None)
                    pos += c * es
        if diag and pos > footer_off:
            return False, (i, pos, None, "row overshoot")
    if diag and pos != footer_off:
        return False, (nrows, pos, None, f"final pos {pos} != {footer_off}")
    return (pos == footer_off), stats


def main() -> int:
    arc = R.Archive("server")
    pay = arc.payload(10)
    mv = memoryview(pay)
    footer_off = len(pay) - 9
    nrows = int.from_bytes(pay[8:12], "little")
    print(f"server t10: rows={nrows} footer_off={footer_off} payload={len(pay)}")

    ops = server_ops()
    ranges = {S3: range(1, 49), S7: range(1, 49), S10: range(1, 49), S605: range(8, 17)}
    for check in (True, False):
        hits = []
        for combo in itertools.product(*(ranges[k] for k in (S3, S7, S10, S605))):
            sizes = dict(zip((S3, S7, S10, S605), combo))
            ok, stats = walk(mv, nrows, footer_off, ops, sizes, ident_check=check)
            if ok:
                hits.append((sizes, stats))
        print(f"server closing candidates (ident_check={check}): {len(hits)}")
        for sizes, stats in hits[:10]:
            nz = {k: (max(v), sum(1 for c in v.values() if c)) for k, v in
                  zip(["v128", "v126h", "v127", "v125", "v135", "ee0430", "u8vec", "v133", "v136", "v1262"],
                      stats)}
            print("  SIZES", sizes, "vec max/nonzero-rows:", nz)
        if hits:
            break
    if not hits:
        ok, d = walk(mv, nrows, footer_off, ops, {S3: 4, S7: 16, S10: 12, S605: 12}, ident_check=False, diag=True)
        print("server diag (4,16,12,12):", d)
        if d:
            i, pos, op, why = d
            print(f"  row {i} pos {pos} op {op} why {why}")
            print("  bytes:", pay[max(13, pos - 24):pos + 24].hex())

    arc_c = R.Archive("client")
    pay_c = arc_c.payload(10)
    mv_c = memoryview(pay_c)
    fo_c = len(pay_c) - 9
    nr_c = int.from_bytes(pay_c[8:12], "little")
    print(f"client t10: rows={nr_c} footer_off={fo_c} payload={len(pay_c)}")
    ops_c = client_ops()
    hits_c = []
    for s10 in range(0, 49):
        ok, stats = walk(mv_c, nr_c, fo_c, ops_c, {S10: s10}, ident_check=True)
        if ok:
            hits_c.append((s10, stats))
    print(f"client closing candidates (s10): {[h[0] for h in hits_c]}")
    for s10, stats in hits_c[:5]:
        print(f"  s10={s10} vec counts: {[dict(c) for c in stats]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
