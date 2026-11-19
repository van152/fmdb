#!/usr/bin/env python3
"""Commander independent spot-check of t24 claims (E61 acceptance).

Walks client table_3 with the t19 frame formula ONLY (no t24 builder code),
then checks t24's selector/footer/field claims against raw bytes.
"""
import hashlib
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from fm24_dump import _reader, load_payload  # noqa: E402

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def main():
    raw = load_payload(_reader(), "client", 3)
    check("member_len", len(raw) == 6932082, f"len={len(raw)}")
    sha = hashlib.sha256(raw).hexdigest()
    check("member_sha_vs_t21", sha == "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f", sha[:16])

    # t24 claim: row0 selector at member 0x0d; body starts 0x0e.
    pos = 13
    rows = []
    sel_counts = {}
    compact_ordinals = []
    bad = None
    for i in range(84259):
        sel = raw[pos]
        sel_counts[sel] = sel_counts.get(sel, 0) + 1
        body = pos + 1
        if sel == 0x0C:
            compact_ordinals.append(i)
            total = 55
            n = m = None
        elif sel == 0x00:
            n = U32(raw, body + 26)
            m = U32(raw, body + 30 + n)
            if n > 512 or m > 512:
                bad = (i, "name_len", n, m)
                break
            total = 50 + n + m
        else:
            bad = (i, "selector", sel)
            break
        rows.append((i, pos, body, sel, n, m, total))
        pos += total
    check("walk_84259_rows", bad is None and len(rows) == 84259, f"bad={bad} walked={len(rows)}")
    check("selector_counts", sel_counts == {0: 84256, 12: 3}, str(sel_counts))
    check("compact_ordinals", compact_ordinals == [69706, 69707, 69708], str(compact_ordinals))
    check("wire_footer_pos", pos == 0x69C669, hex(pos))
    tail = raw[pos:]
    check("footer_9B", tail == bytes.fromhex("0000000001e3c03a77"), tail.hex(" "))
    check("t21_footer_suffix", raw[0x69C66A:0x69C672] == bytes.fromhex("00000001e3c03a77"))

    # column stats over ALL rows (t21 counted compact too); compact body+0/8/12/20
    allb = [r[2] for r in rows]
    eq_0_8 = sum(U32(raw, b) == U32(raw, b + 8) for b in allb)
    eq_8_12 = sum(U32(raw, b + 8) == U32(raw, b + 12) for b in allb)
    check("u32@0==u32@8_count", eq_0_8 == 55868, str(eq_0_8))
    check("u32@8==u32@12_count", eq_8_12 == 84157, str(eq_8_12))

    std = [r for r in rows if r[3] == 0]
    # Cnti@0 nation wire index range; Ccty@16 city wire index range
    cnti = [U32(raw, b) for _, _, b, _, _, _, _ in std]
    ccty = [U32(raw, b + 16) for _, _, b, _, _, _, _ in std]
    cccn = [U32(raw, b + 12) for _, _, b, _, _, _, _ in std]
    SENT = 0xFFFFFFFF
    ok_cnti = all(v < 251 or v == SENT for v in cnti)
    ok_ccty = all(v < 56293 or v == SENT for v in ccty)
    ok_cccn = all(v < 251 or v == SENT for v in cccn)
    check("Cnti@0_in_nation_space", ok_cnti, f"max_nonSent={max(v for v in cnti if v != SENT)}")
    check("Ccty@16_in_city_space", ok_ccty, f"max_nonSent={max(v for v in ccty if v != SENT)}")
    check("Cccn@12_in_nation_space", ok_cccn, f"nonSent={sum(v != SENT for v in cccn)}")

    # identity: 12B at body+37+N+M, first u32 == ordinal (t24 post-check claim)
    ident_ok = 0
    uid_pair_ok = 0
    for i, _, b, _, n, m, _ in std:
        io = b + 37 + n + m
        if U32(raw, io) == i:
            ident_ok += 1
        if U32(raw, io + 4) == U32(raw, io + 8):
            uid_pair_ok += 1
    check("identity_first_u32==ordinal", ident_ok == 84256, f"{ident_ok}/84256")
    check("identity_uid_pair_equal", uid_pair_ok == 84256, f"{uid_pair_ok}/84256")

    # duni@41+N+M uniqueness
    dunis = [U32(raw, b + 41 + n + m) for _, _, b, _, n, m, _ in std]
    check("duni_unique", len(set(dunis)) == 84256, f"unique={len(set(dunis))}")

    # byte@20 (Csot mask 0x02) distribution vs t21 (all rows; compact byte20=255)
    b20 = {}
    for b in allb:
        v = raw[b + 20]
        b20[v] = b20.get(v, 0) + 1
    check("byte20_counts_vs_t21", b20 == {0: 79471, 2: 4785, 255: 3}, str(b20))

    # row0: t19/t23 "95" is row_length (50+33+12), full name is 33B
    r0 = std[0]
    check("row0_row_length_95", r0[6] == 95, str(r0[6]))
    check("row0_full_len_33", r0[4] == 33, str(r0[4]))
    name0 = raw[r0[2] + 30: r0[2] + 30 + r0[4]].decode("utf-8", "replace")
    check("row0_name", name0 == "Klubi i Futbollit Albpetrol Patos", name0)

    # compact body model: 4B(ffffffff)+1B(00)+5xu32(ffffffff)@5..24 + 6B zero@25
    for i, p, b, sel, _, _, _ in rows:
        if sel == 0x0C:
            head = U32(raw, b) == SENT and raw[b + 4] == 0
            shared = all(U32(raw, b + k) == SENT for k in range(5, 25, 4))
            zeros = raw[b + 25: b + 31] == bytes(6)
            ident = U32(raw, b + 42) == i and U32(raw, b + 46) == U32(raw, b + 50)
            check(f"compact_{i}_model", head and shared and zeros and ident,
                  f"head={head} shared={shared} zeros={zeros} ident={ident} uid={U32(raw, b + 46)}")

    print()
    if fails:
        print(f"SPOT FAIL: {len(fails)} -> {fails}")
        return 1
    print("SPOT PASS: all commander checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())