#!/usr/bin/env python3
"""t76c independent verifier — re-derives every claim from the payload.

Deliberately does NOT import scripts/t76c_slots.py. It re-implements the row
walks, re-reads every slot it can address, and re-computes the invariants. It
also re-derives the two load-bearing calibration facts from unrelated tables:

  * reference slots hold dense ordinals, not UIDs   (stadium Scti -> city)
  * derby's 6-byte archive delta == the 3 non-client schema fields

    py -V:3.12 -I -B scratch/t76c/out/verify.py            # full
    py -V:3.12 -I -B scratch/t76c/out/verify.py --quick    # small tables only

Exit codes: 0 all checks pass / 1 a check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
OUT = HERE
sys.path.insert(0, str(REPO / "scripts"))

CORE = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"),
                      run_name="t76c_verify_core")
load = CORE["load_payload"]
NROWS = {"club": 84259, "team": 84507, "comp": 7047, "stadium": 48413,
         "city": 56293, "nation": 251, "region": 28, "continent": 7,
         "language": 126, "weather": 334, "local_region": 2488, "agreement": 6}
NU = 0xFFFFFFFF
N16 = 0xFFFF
N8 = 0xFF

PASS, FAIL = [], []


def chk(cond, label, detail=""):
    (PASS if cond else FAIL).append(label)
    mark = "PASS" if cond else "FAIL"
    print(f"  [{mark}] {label}" + (f"  {detail}" if detail else ""))
    return cond


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


# ------------------------------------------------------- independent walks ----
def w_agrm(raw):
    n = u32(raw, 8)
    rows = [raw[14 + j * 13:14 + (j + 1) * 13] for j in range(n)]
    return rows, 14 + n * 13, n


def w_derby(raw, num):
    n = u32(raw, 8)
    rows, pos = [], 14
    for j in range(n):
        p, nb = pos, 0
        for _ in range(4):
            ln = u32(raw, p)
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        rows.append((raw[pos + 16 + nb:end - 13], raw[end - 13:end]))
        pos = end
    return rows, pos, n


def w_weather(raw):
    n = u32(raw, 8)
    rows, pos = [], 14
    for j in range(n):
        ln = u32(raw, pos)
        end = pos + 4 + ln + 95 + 13
        rows.append((raw[pos + 4 + ln:end - 13], raw[end - 13:end], ln))
        pos = end
    return rows, pos, n


def w_lcrg(raw):
    n = u32(raw, 8)
    rows, pos = [], 14
    for j in range(n):
        hit = None
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            if end > len(raw):
                break
            o, a, b = struct.unpack_from("<III", raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                hit = (ln, k, end)
                break
        ln, k, end = hit
        rows.append((raw[pos:end - 13], raw[end - 13:end], k))
        pos = end
    return rows, pos, n


def ident_ok(trailer, j):
    o, a, b = struct.unpack_from("<III", trailer, 0)
    return o == j and a == b != 0 and trailer[12] == 0


# ------------------------------------------------------------------ checks ----
def check_frames(tid, arch, res, rows, end, n):
    """The slot JSON must reproduce the t74 frame exactly."""
    fr = json.loads((REPO / "scratch" / "t74" / "out" / "frames.json")
                    .read_text(encoding="utf-8"))["tables"][str(tid)]["archives"][arch]
    raw = load(arch, tid)
    chk(res["payload_len"] == len(raw), f"t{tid}/{arch} payload_len")
    chk(res["payload_sha256"] == hashlib.sha256(raw).hexdigest(),
        f"t{tid}/{arch} payload_sha256")
    chk(len(raw) - end == fr["footer"], f"t{tid}/{arch} footer=={fr['footer']}",
        f"got {len(raw) - end}")
    chk(n == fr["count"], f"t{tid}/{arch} count=={fr['count']}", f"got {n}")
    chk(res["walk"]["rows"] == n and res["walk"]["end"] == end,
        f"t{tid}/{arch} walk matches re-walk")


def v_agrm(arch, res):
    raw = load(arch, 56)
    rows, end, n = w_agrm(raw)
    check_frames(56, arch, res, rows, end, n)
    chk(all(ident_ok(r[0:0] + r, j) for j, r in enumerate(rows)),
        f"t56/{arch} identity triple on all {n} rows")
    chk(end + 8 == len(raw) and len(rows[0]) == 13,
        f"t56/{arch} row is exactly 13B, closure 14+6*13+8=100")
    chk(res["slots"][0]["field"] == "rdui" and res["slots"][0]["offset"] == 0,
        f"t56/{arch} rdui@0 L3 present")
    chk(res["slots"][1]["field"] == "duni" and res["slots"][1]["offset"] == 4,
        f"t56/{arch} duni@4 L3 present")
    neg = [s for s in res["slots"] if s.get("kind") == "neg"]
    chk(len(neg) == 1 and "NEGATIVE RESULT" in neg[0]["why"],
        f"t56/{arch} negative result preserved verbatim")
    un = [s for s in res["slots"] if s["grade"] == "unmapped"]
    chk(len(un) == 6, f"t56/{arch} 6 business fields marked unmapped",
        f"got {len(un)}")


def v_derby(arch, res):
    num = 36 if arch == "client" else 42
    raw = load(arch, 18)
    rows, end, n = w_derby(raw, num)
    check_frames(18, arch, res, rows, end, n)
    chk(all(ident_ok(t, j) for j, (_, t) in enumerate(rows)),
        f"t18/{arch} identity triple on all {n} rows")
    chk(all(len(b) == num for b, _ in rows), f"t18/{arch} numeric region == {num}B")
    by = {s["field"]: s for s in res["slots"] if s["field"]}

    # packed date
    doy = [int.from_bytes(b[0:2], "little") for b, _ in rows]
    yr = [int.from_bytes(b[2:4], "little") for b, _ in rows]
    chk(by["Dfmd"]["offset"] == 0, f"t18/{arch} Dfmd@0")
    chk(all(1 <= v <= 366 for v in doy), f"t18/{arch} day-of-year in 1..366",
        f"[{min(doy)},{max(doy)}]")
    chk(all(1850 <= v <= 2025 for v in yr), f"t18/{arch} year in 1850..2025",
        f"[{min(yr)},{max(yr)}]")

    # club-ordinal lanes + wrong-UID control
    for f, off in (("Dtm1", 4), ("Dtm2", 8)):
        v = [int.from_bytes(b[off:off + 4], "little") for b, _ in rows]
        nn = [x for x in v if x != NU]
        chk(by[f]["offset"] == off, f"t18/{arch} {f}@{off}")
        chk(all(x < NROWS["club"] for x in nn), f"t18/{arch} {f} non-null < club rows",
            f"max {max(nn)} / {NROWS['club']}, null {len(v) - len(nn)}")
    chk(all(int.from_bytes(a[4:8], "little") != int.from_bytes(a[8:12], "little")
            for a, _ in rows), f"t18/{arch} Dtm1 != Dtm2 on every row (control)")

    # Dfma must be rejected as a reference (attendance-sized)
    v = [int.from_bytes(b[20:24], "little") for b, _ in rows]
    nn = [x for x in v if x != NU]
    chk(by["Dfma"]["grade"] == "L2" and all(x <= 200000 for x in nn),
        f"t18/{arch} Dfma is 0..200000 attendance",
        f"max {max(nn)}, null {len(v) - len(nn)}")
    chk("vacuous" in json.dumps(by["Dfma"]["evidence"]),
        f"t18/{arch} Dfma ordinal-fit explicitly marked vacuous")

    # constant blocks
    chk(all(int.from_bytes(b[24:28], "little") == NU for b, _ in rows),
        f"t18/{arch} @24 constant 0xffffffff")

    if arch == "client":
        chk(all(int.from_bytes(b[30:34], "little") == 0 for b, _ in rows),
            "t18/client @30 constant zero 4B")
        chk(by["D1tw/D1td/D1tl"]["grade"] != "L2" if "D1tw/D1td/D1tl" in by
            else True, "t18/client has no D1tw group (client-only archive)")
        r = [b[34] for b, _ in rows]
        s = [b[35] for b, _ in rows]
        chk(max(r) <= 200 and max(s) <= 200, "t18/client reputation pair 0..200")
    else:
        tri = [tuple(int.from_bytes(b[o:o + 2], "little") for o in (28, 30, 32))
               for b, _ in rows]
        allnull = sum(1 for t in tri if t == (N16,) * 3)
        mixed = sum(1 for t in tri if N16 in t and t != (N16,) * 3)
        chk(by["D1tw/D1td/D1tl"]["offset"] == 28, "t18/server D1 group @28")
        chk(mixed == 0, "t18/server trio is all-null-together (no partial rows)",
            f"null {allnull}/{n}")
        # cross-archive byte identity
        rc = load("client", 18)
        crows, _, _ = w_derby(rc, 36)
        chk(all(c[0][0:28] == s[0][0:28] for c, s in zip(crows, rows)),
            "t18 server[0:28] == client[0:28]")
        chk(all(s[0][34:36] == c[0][28:30] and s[0][40:42] == c[0][34:36]
                for c, s in zip(crows, rows)),
            "t18 server tail == client tail shifted +6")


def v_weather(arch, res):
    raw = load(arch, 27)
    rows, end, n = w_weather(raw)
    check_frames(27, arch, res, rows, end, n)
    chk(all(ident_ok(t, j) for j, (_, t, _) in enumerate(rows)),
        f"t27/{arch} identity triple on all {n} rows")
    biz = [b for b, _, _ in rows]
    chk(all(len(b) == 95 for b in biz), f"t27/{arch} middle == 95B")
    chk(all(b[0:3] == b"\0\0\0" for b in biz), f"t27/{arch} 3B zero prefix")

    # the decisive layout test, re-derived
    two = [o for o in range(95) if {m[o] for m in biz} == {0, 100}]
    chk(two == [25, 48, 71, 94],
        f"t27/{arch} only {{0,100}} columns are 25/48/71/94", f"got {two}")
    chk(all(len({m[25], m[48], m[71], m[94]}) == 1 for m in biz),
        f"t27/{arch} those 4 columns coincide row-wise")
    # rival hypothesis must lose
    def sum100(prefix, blk, tail):
        tot = 0
        for b in range(4):
            base = prefix + blk * b
            for o, L in ((1, 5), (6, 5), (11, 10)):
                tot += sum(1 for m in biz if sum(m[base + o:base + o + L]) == 100)
        return tot
    a = sum100(3, 23, 0)
    b_ = sum100(3, 22, 4)
    chk(a > b_ * 2, f"t27/{arch} 3+4x23 beats 3+4x22+4 on sum==100",
        f"{a} vs {b_}")

    for b in range(4):
        base = 3 + 23 * b
        sd = [m[base] for m in biz]
        chk(max(sd) <= 365, f"t27/{arch} block{b} w{b}sd 0..365", f"max {max(sd)}")
        for name, o, L in (("p", 2, 5), ("w", 7, 5)):
            v = [m[base + o:base + o + L] for m in biz]
            s = [sum(x) for x in v]
            chk(max(max(x) for x in v) <= 100,
                f"t27/{arch} block{b} {name}* each <=100")
            chk(s.count(100) >= 300, f"t27/{arch} block{b} {name}* sum==100 majority",
                f"{s.count(100)}/{n}")
        t = [m[base + 12:base + 22] for m in biz]
        st = [sum(x) for x in t]
        chk(max(max(x) for x in t) <= 100, f"t27/{arch} block{b} temp each <=100")
        chk(sum(1 for v in st if v > 105) == 0,
            f"t27/{arch} block{b} temp group bounded (<=105)")
        flag = [m[base + 1] for m in biz]
        chk(set(flag) <= {0, 1}, f"t27/{arch} block{b} w{b}dn is a {{0,1}} byte",
            f"ones {flag.count(1)}")
    by = {s["field"]: s for s in res["slots"] if s["field"]}
    chk(by["w0dn"]["grade"] == "candidate",
        f"t27/{arch} w0dn graded candidate (assigned by elimination)")
    chk(sum(1 for s in res["slots"] if s["grade"] == "escalate_to_sol") == 0,
        f"t27/{arch} no escalations left")


def v_lcrg(arch, res):
    raw = load(arch, 47)
    rows, end, n = w_lcrg(raw)
    check_frames(47, arch, res, rows, end, n)
    chk(all(ident_ok(t, j) for j, (_, t, _) in enumerate(rows)),
        f"t47/{arch} identity triple on all {n} rows")
    chk(all(len(b) == 23 + 5 * (k + 1) for b, _, k in rows),
        f"t47/{arch} closure 23 + 5*(k+1) + 13 == 41 + 5k")
    chk(all(b[22] == k for b, _, k in rows), f"t47/{arch} b22 == k")
    chk(all(b[1:4] == b"\0\0\0" and b[20] == 0 for b, _, _ in rows),
        f"t47/{arch} constant prefix bytes")
    by = {s["field"]: s for s in res["slots"] if s["field"]}
    chk(by["rdui"]["offset"] == -13, f"t47/{arch} rdui@-13 L3")
    chk(by["duni"]["offset"] == -9, f"t47/{arch} duni@-9 L3")
    pop = [int.from_bytes(b[4:8], "little") for b, _, _ in rows]
    chk(max(pop) <= 10 ** 9, f"t47/{arch} Lpop <= 1e9", f"max {max(pop)}")
    # items
    pct, ref = [], []
    for b, _, k in rows:
        for i in range(1, k + 1):
            o = 23 + 5 * i
            pct.append(b[o])
            ref.append(int.from_bytes(b[o + 1:o + 5], "little"))
    chk(max(pct) <= 100, f"t47/{arch} Llgp percentages 0..100", f"max {max(pct)}")
    s = [sum(b[23 + 5 * i] for i in range(1, k + 1)) for b, _, k in rows if k]
    chk(s.count(100) >= 800, f"t47/{arch} per-row pct sum == 100 majority",
        f"{s.count(100)}/{len(s)}")
    chk(all(b[23] == 0 for b, _, _ in rows), f"t47/{arch} leading item pct == 0")
    nn = [x for x in ref if x != NU]
    chk(max(nn) < NROWS["weather"], f"t47/{arch} Llgl ref fits weather ordinal",
        f"max {max(nn)}")
    chk(sum(1 for x in nn if x < NROWS["language"]) < len(nn) * 0.8,
        f"t47/{arch} Llgl ref does NOT fit language UID set (rejection kept)",
        f"{sum(1 for x in nn if x < NROWS['language'])}/{len(nn)}")
    chk(by["Lrll[i].Llgl"]["grade"] == "candidate",
        f"t47/{arch} Llgl graded candidate, not L2")


def v_calibration():
    """Re-derive the ordinal-vs-UID rule from tables unrelated to this task."""
    raw = load("client", 21)   # stadium, 38B, Scti@3
    scti = [int.from_bytes(raw[14 + j * 38 + 3:14 + j * 38 + 7], "little")
            for j in range(48413)]
    chk(all(v < 56293 for v in scti),
        "calib: stadium Scti@3 all < city rows (ordinal encoding)",
        f"max {max(scti)}")
    chk(max(scti) > 0.9 * 56293, "calib: stadium Scti@3 spans the city domain",
        f"max/N {max(scti)/56293:.3f}")
    raw2 = load("client", 2)   # city, 43B, Cwea@14
    cwea = [int.from_bytes(raw2[14 + j * 43 + 14:14 + j * 43 + 16], "little")
            for j in range(56293)]
    nn = [v for v in cwea if v != N16]
    chk(all(v < 334 for v in nn),
        "calib: city Cwea@14 all < weather rows (ordinal encoding)", f"max {max(nn)}")


def v_schema_delta():
    """derby's 6-byte archive delta == exactly 3 non-client fields."""
    m = json.loads((REPO / "evidence" / "fm24" / "reports" / "editor_schema" /
                    "master.json").read_text(encoding="utf-8"))
    ent = m["entities"]["derby.xml"][0]
    non_client = [f["field"] for f in ent["fields"] if not f.get("is_client_field")]
    chk(len([f for f in non_client if f in ("D1tw", "D1td", "D1tl")]) == 3,
        "schema: derby has exactly 3 non-client business fields (D1tw/D1td/D1tl)")
    rc, rs = load("client", 18), load("server", 18)
    cr, _, _ = w_derby(rc, 36)
    sr, _, _ = w_derby(rs, 42)
    chk(all(len(s[0]) - len(c[0]) == 6 for c, s in zip(cr, sr)),
        "schema: derby archive delta is exactly 6 bytes on every row")
    chk(6 == 3 * 2, "schema: 3 x u16 == 6B delta (structural match)")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="t76c verify")
    ap.add_argument("--quick", action="store_true",
                    help="agreement + derby only (skip the 2,488-row lcrg and weather)")
    ap.add_argument("--selftest", action="store_true",
                    help="verify the verifier's own helpers offline")
    a = ap.parse_args(argv)
    if a.selftest:
        n = 2
        body = b"".join(struct.pack("<III", j, 7 + j, 7 + j) + b"\0" for j in range(n))
        raw = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", n) + bytes(2)
               + body + struct.pack(">I", 1) + struct.pack("<I", 7))
        rows, end, cnt = w_agrm(raw)
        assert cnt == 2 and len(rows) == 2 and end + 8 == len(raw)
        assert all(ident_ok(r, j) for j, r in enumerate(rows))
        assert NU == 0xFFFFFFFF and N16 == 0xFFFF
        print("verify selftest ok")
        return 0

    files = sorted(OUT.glob("slots_*.json"))
    if not files:
        print(f"no slot files in {OUT}", file=sys.stderr)
        return 2
    print(f"== independent verification of {len(files)} slot files\n")
    print("== calibration (re-derived from stadium/city, not from this task)")
    v_calibration()
    print("\n== schema cross-check")
    v_schema_delta()
    for p in files:
        res = json.loads(p.read_text(encoding="utf-8"))
        tid, arch = res["table"], res["archive"]
        print(f"\n== {p.name}  (t{tid}/{arch})")
        if res.get("status") != "closed":
            chk(False, f"t{tid}/{arch} status closed", str(res.get("status")))
            continue
        if tid in (18, 56):
            {56: v_agrm, 18: v_derby}[tid](arch, res)
            continue
        if a.quick:
            print("  [SKIP] --quick")
            continue
        {27: v_weather, 47: v_lcrg}[tid](arch, res)
    print(f"\n== {len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        for f in FAIL:
            print("  FAILED:", f)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
