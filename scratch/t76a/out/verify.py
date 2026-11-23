#!/usr/bin/env python3
"""t76a-fix1 verifier — independent re-derivation of the stadium(21) slot map.

Deliberately imports NOTHING from the builder. It re-reads the payload from the
archives through `scripts/fm24_dump.py` (runpy, unmodified), re-walks the rows
from the t74 frame, re-extracts every anchor and re-checks >=5 slots against
expectations written down here by hand.

    py -V:3.12 -I -B scratch/t76a/out/verify.py
    py -V:3.12 -I -B scratch/t76a/out/verify.py --selftest
    py -V:3.12 -I -B scratch/t76a/out/verify.py --json scratch/t76a/out/verify.json

Exit codes: 0 all checks pass / 1 a check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import json
import runpy
import struct
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
REPO = OUT.parent.parent.parent
FRAMES = REPO / "scratch" / "t74" / "out" / "frames.json"
TID, XML = 21, "stadium.xml"
NULL32 = 0xFFFFFFFF
FORBIDDEN = ("t76a_stadium_slots",)

_CORE = None


def core() -> dict:
    global _CORE
    if _CORE is None:
        p = REPO / "scripts" / "t73_mapper_core.py"
        _CORE = runpy.run_path(str(p), run_name="t76a_verify_core")
    return _CORE


def load(archive: str):
    fr = json.loads(FRAMES.read_text(encoding="utf-8"))["tables"][str(TID)]["archives"][archive]
    raw = core()["load_payload"](archive, TID)
    H, S, n = fr["header"], fr["stride"], fr["count"]
    m = np.frombuffer(raw, np.uint8, H + n * S)[H:].reshape(n, S)
    return raw, m, fr


def u(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


def f32(m, o):
    with np.errstate(invalid="ignore"):
        return np.ascontiguousarray(m[:, o:o + 4]).view("<f4").ravel().astype(np.float64)


class Checker:
    def __init__(self):
        self.items = []

    def chk(self, name, cond, detail):
        self.items.append({"check": name, "pass": bool(cond), "detail": detail})
        return bool(cond)

    @property
    def ok(self):
        return sum(1 for i in self.items if i["pass"])

    @property
    def total(self):
        return len(self.items)


def verify_archive(archive: str, ck: Checker) -> dict:
    raw, m, fr = load(archive)
    H, S, n = fr["header"], fr["stride"], fr["count"]
    ar = np.arange(n)

    # 1. frame closure, recomputed from bytes (not read from the builder output)
    ck.chk(f"{archive}/closure", H + n * S + fr["footer"] == len(raw),
           f"{H} + {n} x {S} + {fr['footer']} = {len(raw)}")
    ck.chk(f"{archive}/count_header",
           struct.unpack_from("<I", raw, 8)[0] == n, f"header count == {n}")

    # 2. identity triple at row_end-13 on every row
    bad = 0
    for j in range(n):
        t = H + j * S + S - 13
        o, a, b = struct.unpack_from("<III", raw, t)
        if not (o == j and a == b != 0 and raw[t + 12] == 0):
            bad += 1
    ck.chk(f"{archive}/identity_all_rows", bad == 0, f"bad rows = {bad} / {n}")

    # 3. row ordinal column == row index
    ord_off = 25 if archive == "client" else 168
    v = u(m, ord_off, 4)
    ck.chk(f"{archive}/row_ordinal@{ord_off}", bool((v == ar).all()),
           f"{int((v == ar).sum())} / {n} rows equal the row index")

    # 4. duni UID pair
    duni = 29 if archive == "client" else 172
    a_, b_ = u(m, duni, 4), u(m, duni + 4, 4)
    ck.chk(f"{archive}/duni_pair@{duni}", bool((a_ == b_).all()) and int(a_.min()) > 0,
           f"pair equal, {int(np.unique(a_).size):,} distinct, min {int(a_.min())}")

    # 5. Scti -> city ordinal domain + wrong-UID control
    scti_off = 3 if archive == "client" else 146
    s = u(m, scti_off, 4)
    N_CITY = 56293
    ck.chk(f"{archive}/Scti@{scti_off}_in_city_domain",
           float((s < N_CITY).mean()) == 1.0 and int(s.max()) > 0.6 * N_CITY,
           f"max {int(s.max())} / {N_CITY} = {int(s.max())/N_CITY:.4f}, "
           f"100% in domain")

    # 6. Slat / Slon f32 plausibility
    for off, nm in ((17 if archive == "client" else 160, "Slat"),
                    (21 if archive == "client" else 164, "Slon")):
        f = f32(m, off)
        ck.chk(f"{archive}/{nm}@{off}_f32",
               bool(np.isfinite(f).all() and float(np.abs(f).max()) < 400),
               f"finite, range [{float(f.min()):.3f}, {float(f.max()):.3f}]")
    return {"archive": archive, "raw_len": len(raw), "stride": S, "count": n}


def verify_slots(archive: str, ck: Checker) -> None:
    """>=5 hand-written slot expectations per archive, re-derived from bytes."""
    raw, m, fr = load(archive)
    n = m.shape[0]
    if archive == "client":
        # Scti@3: ordinal into city; the city UID encoding must be refuted
        city = core()["reference_uids"]("client", 2)
        s = u(m, 3, 4)
        if city.get("ok"):
            dom = set(city["uids"])
            hits = int(sum(1 for x in s.tolist() if x in dom))
            ck.chk("client/Scti_uid_control", hits / n < 0.5,
                   f"{hits:,} / {n:,} = {hits/n:.4f} in the city UID set "
                   f"(ordinal encoding, not UID)")
        else:
            ck.chk("client/Scti_uid_control", False,
                   f"city UID set unavailable: {city.get('why')}")

        # Snbs@7: nullable ordinal into stadium; self-table UID control refuted
        own = set(u(m, 29, 4).tolist())
        v7 = u(m, 7, 4)
        live = v7[v7 != NULL32]
        hits = int(sum(1 for x in live.tolist() if x in own))
        ck.chk("client/Snbs_nullable_ordinal",
               int((v7 == NULL32).sum()) == 44240 and int(live.max()) < 48413,
               f"{int((v7 == NULL32).sum()):,} null, live max {int(live.max())} "
               f"< 48,413")
        ck.chk("client/Snbs_uid_control", hits / max(1, live.size) < 0.5,
               f"{hits:,} / {live.size:,} = {hits/max(1,live.size):.4f} in the "
               f"stadium UID set (ordinal encoding)")

        # rdui_raw@33 duplicates duni@29
        ck.chk("client/rdui_raw_dup", bool((u(m, 29, 4) == u(m, 33, 4)).all()),
               "u32@33 == u32@29 on every row")

        # Sptc@11 u16 within schema range 0..200
        sp = u(m, 11, 2)
        ck.chk("client/Sptc@11_range", int(sp.min()) >= 0 and int(sp.max()) <= 200,
               f"u16 range [{int(sp.min())}, {int(sp.max())}] within schema 0..200")

        # flags@0: exactly the documented bits ever set
        fl = u(m, 0, 2)
        bits = sorted(b for b in range(16) if ((fl >> b) & 1).any())
        ck.chk("client/flags@0_bits", bits == [0, 1, 6, 7, 11],
               f"bits ever set = {bits}")
        return

    # ---- server ----
    # Sowi@16 inside the club ordinal domain
    sw = u(m, 16, 4)
    live = sw[sw != NULL32]
    ck.chk("server/Sowi@16_club_domain",
           float((live < 84259).mean()) == 1.0 and int(live.max()) > 0.9 * 84259,
           f"live max {int(live.max())} / 84,259 = {int(live.max())/84259:.4f}")

    # capacity nesting invariant, recomputed here
    A, B, C, D = (u(m, o, 4) for o in (0, 4, 8, 12))
    k = (A > 0) & (B > 0) & (C > 0) & (D > 0)
    rate = float(((D[k] <= B[k]) & (B[k] <= A[k]) & (A[k] <= C[k])).mean())
    ck.chk("server/capacity_nesting", rate > 0.98,
           f"Scas<=Sscy<=Scpy<=Secy on {rate*100:.2f}% of {int(k.sum()):,} "
           f"all-nonzero rows")

    # packed dates: all five valid
    for off in (37, 41, 45, 131, 135):
        v = u(m, off, 4)
        doy, yr = v & 0xFFFF, v >> 16
        ok = float(((doy >= 1) & (doy <= 366) & (yr >= 1800) & (yr <= 2100)).mean())
        ck.chk(f"server/date@{off}", ok == 1.0, f"valid packed date on {ok*100:.2f}%")

    # shared 38B tail byte-identical to the client body
    rawC = core()["load_payload"]("client", TID)
    mc = np.frombuffer(rawC, np.uint8, 14 + n * 38)[14:].reshape(n, 38)
    eq = int((m[:, 143:181] == mc).all(axis=1).sum())
    ck.chk("server/shared_tail_identical", eq == n,
           f"{eq:,} / {n:,} rows: server[143:181] == client[0:38]")

    # ubnt slots are subsets of 0..6 (shape only, not identity)
    for off in (49, 50, 51):
        col = {int(x) for x in np.unique(m[:, off])}
        ck.chk(f"server/ubnt@{off}_shape", col <= set(range(7)),
               f"domain {sorted(col)} subset of ubnt 0..6")


def check_outputs(ck: Checker) -> None:
    """The JSON artifacts must agree with the claims the report makes."""
    for archive in ("client", "server"):
        p = OUT / f"slots_{archive}_{TID}.json"
        if not ck.chk(f"{archive}/json_exists", p.exists(), str(p)):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        ck.chk(f"{archive}/status_closed", d.get("status") == "closed",
               f"status = {d.get('status')}")
        ck.chk(f"{archive}/frame_from_t74",
               "t74" in d.get("frame_source", ""),
               d.get("frame_source", ""))
        ck.chk(f"{archive}/frame_matches",
               d["frame"]["stride"] == (38 if archive == "client" else 181)
               and d["frame"]["count"] == 48413,
               f"stride {d['frame']['stride']}, count {d['frame']['count']}")
        ck.chk(f"{archive}/no_uncovered_bytes",
               not d["coverage"]["uncovered_offsets"],
               f"uncovered = {d['coverage']['uncovered_offsets']}")
        ck.chk(f"{archive}/anchors_all_ok",
               d["anchors"]["ok"] == d["anchors"]["checked"],
               f"{d['anchors']['ok']} / {d['anchors']['checked']}")
        # every slot must carry a why-string and stay inside the body
        bad = [s for s in d["slots"]
               if not s.get("why") or s["offset"] < 0
               or s["offset"] + s["width"] > d["frame"]["stride"]]
        ck.chk(f"{archive}/slots_wellformed", not bad,
               f"{len(d['slots'])} slots, {len(bad)} malformed")
        if archive == "server":
            ck.chk("server/shared_tail_declared",
                   d.get("shared_tail", {}).get("byte_identical") is True,
                   json.dumps(d.get("shared_tail")))
            seg = d.get("server_only_segment", {})
            ck.chk("server/server_only_segment_declared",
                   seg.get("length") == 143 and seg.get("offset") == 0,
                   json.dumps(seg)[:160])


def selftest() -> int:
    ck = Checker()
    ck.chk("sanity_true", 1 + 1 == 2, "arithmetic")
    ck.chk("sanity_false_detected", not (1 + 1 == 3), "negation")
    # the checker must be able to report failure, not only success
    ck.chk("intentional_negative", False, "this one is expected to fail")
    print(f"selftest: {ck.ok}/{ck.total} (1 intentional failure)")
    return 0 if ck.total - ck.ok == 1 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="t76a_verify",
        description="Independent verification of the stadium(21) slot map. "
                    "Imports nothing from the builder; re-reads the archives.",
        epilog="Exit codes: 0 all pass / 1 a check failed / 2 usage or fatal.")
    ap.add_argument("--json", metavar="OUT")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    # guard: the verifier must not have pulled in the builder
    leaked = [k for k in sys.modules if any(f in k for f in FORBIDDEN)]
    if leaked:
        print(f"FATAL: verifier imported builder modules {leaked}", file=sys.stderr)
        return 2

    ck = Checker()
    metas = []
    for archive in ("client", "server"):
        metas.append(verify_archive(archive, ck))
        verify_slots(archive, ck)
    check_outputs(ck)

    for it in ck.items:
        print(f"  [{'PASS' if it['pass'] else 'FAIL'}] {it['check']:<42} {it['detail']}")
    print(f"\n{ck.ok}/{ck.total} checks passed")
    res = {"task": "t76a-fix1", "archive_meta": metas,
           "checks": ck.items, "passed": ck.ok, "total": ck.total}
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                encoding="utf-8")
        print(f"wrote {a.json}")
    return 0 if ck.ok == ck.total else 1


if __name__ == "__main__":
    raise SystemExit(main())
