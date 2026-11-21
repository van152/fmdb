#!/usr/bin/env python3
"""t81 — FK index for variable-length tables (ordinal domain, not UID).

t73's `reference_uids()` self-certifies identity only on fixed-stride tables:
`canonical_frame()` needs a stride, so every variable-length target
(t10/t8/t27/t47/t24) returned `resolved=False`, its UID domain came back empty
and every FK lane pointing at those tables fell to `unmapped`
(t73 REPORT §3.4 — a tool gap, not a missing slot).

This module closes that gap **without touching t73/t74**. It walks the
`[ordinal u32][UID u32][UID u32][marker]` identity triple as a grammar-free
DP over absolute byte positions, so row count, ordinal domain and UID set are
available for fixed *and* variable tables alike.

Two independent outputs per (archive, table):

  ordinal_set  0..row_count-1. The chain is built so that the u32 at the
               identity site equals the row index on every row, so the
               ordinal domain *is* the index range by construction.
  uid_set      u32 at identity+4 on every row (equal to identity+8), for
               small tables; a SHA-256 digest + distinct/min/max for big ones.

Read-only reuse: `scripts/t73_mapper_core.py` is loaded through `runpy` and
only its `load_payload()` is called. Nothing in t73/t74 is modified.

    py -V:3.12 -I -B scripts/t81_fk_index.py --help
    py -V:3.12 -I -B scripts/t81_fk_index.py --selftest
    FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data \
      py -V:3.12 -I -B scripts/t81_fk_index.py --json scratch/t81/out/fk_index.json

Exit codes: 0 all closed / 1 a check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FRAMES = REPO / "scratch" / "t74" / "out" / "frames.json"
SCHEMA = REPO / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
H0 = 14          # canonical header origin (t73 §1: alias group, data-side H0)
FOOTER = 8       # footer length, invariant across every t74 table
IW = 13          # identity width (t74 self-certified per table, 17/17 archives)
# Generous default row-length window for tables t74 never framed. t10/server
# (nation, 422,345 B over 251 rows) averages 1,682 B/row and peaks near 31 KB,
# so 4 KB was too tight and lost the chain at row 176.
GEN_WINDOW = (8, 65536)

_CORE = None


def core():
    global _CORE
    if _CORE is None:
        _CORE = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"),
                               run_name="t81_fk_index_core")
    return _CORE


def load_payload(archive: str, tid: int) -> bytes:
    """Reuse fm24_dump.load_payload via t73's wrapper, unmodified."""
    return core()["load_payload"](archive, tid)


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


# ------------------------------------------------------------ candidate map ---
def candidate_map(raw: bytes, marker0: bool = False) -> dict:
    """ordinal value -> absolute identity positions whose UID pair is equal & non-zero.

    A position p is a candidate for row j when u32(p)==j and u32(p+4)==u32(p+8)!=0.
    With `marker0`, the 13th byte must also be 0 — true for every t74 table
    except team (24), whose tail byte is a selector ({0,10,11}) rather than a
    marker. That single predicate removes the prefix-byte coincidences that
    otherwise survive the DP on t10 (3673 -> 898 raw candidates).

    The scan is vectorised for large payloads (t24 is 8.8 MB) and falls back to
    a plain loop for small ones or when numpy is unavailable.
    """
    L = len(raw)
    out: dict[int, list[int]] = {}
    np = None
    if L >= (1 << 20):
        try:
            import numpy as np  # noqa: PLC0415 - optional, size-gated
        except Exception:  # noqa: BLE001 - absent numpy is not an error
            np = None
    if np is not None:
        buf = np.frombuffer(raw, dtype=np.uint8)
        for r in range(4):
            m = (L - r - 12) // 4 + 1
            if m <= 0:
                continue
            o = buf[r:r + 4 * m].view("<u4")
            a = buf[r + 4:r + 4 + 4 * m].view("<u4")
            b = buf[r + 8:r + 8 + 4 * m].view("<u4")
            ok = (a == b) & (a != 0)
            idx = np.nonzero(ok)[0]
            if idx.size == 0:
                continue
            pos_all = (r + 4 * idx)
            if marker0:
                # Drop indices, never just drop paired values: filtering `pos`
                # while keeping `o[idx]` misaligns the zip and silently binds
                # the wrong ordinal to a position (t81 bug on table 2).
                keep = np.array([p + 12 < L and raw[p + 12] == 0
                                 for p in pos_all.tolist()], dtype=bool)
                if keep.size and not keep.all():
                    idx = idx[keep]
                    pos_all = pos_all[keep]
                if idx.size == 0:
                    continue
            for p, v in zip(pos_all.tolist(), o[idx].tolist()):
                out.setdefault(v, []).append(p)
        return out
    for p in range(L - 12):
        a, b = u32(raw, p + 4), u32(raw, p + 8)
        if a == b and a != 0:
            if marker0 and raw[p + 12] != 0:
                continue
            out.setdefault(u32(raw, p), []).append(p)
    return out


# --------------------------------------------------------------- DP solver ---
def solve_chain(raw: bytes, cand: dict, n: int, hdr: int = H0,
                footer: int = FOOTER, window: tuple = GEN_WINDOW,
                iw: int = IW) -> dict:
    """Backward DP then forward window filter; reports reach per row.

    Backward pass pins the last identity so that `identity_end == len - footer`,
    then every row j needs a predecessor whose end sits within `window` of it.
    The forward pass prunes by the row-length window, which is what removes the
    prefix-byte coincidences (row 0 usually has several).
    """
    L = len(raw)
    lo, hi = window
    reach: list[set] = [set() for _ in range(n)]
    for p in cand.get(n - 1, ()):
        if p + iw == L - footer:
            reach[n - 1].add(p)
    if not reach[n - 1]:
        return {"ok": False, "why": "last row identity does not close at len-footer",
                "lost_at": n - 1, "reach": None}
    for j in range(n - 2, -1, -1):
        nxt = reach[j + 1]
        if not nxt:
            return {"ok": False, "why": "empty successor set", "lost_at": j,
                    "reach": None}
        floor = min(nxt)
        for p in cand.get(j, ()):
            if floor - p > hi:
                continue
            for s in nxt:
                if lo <= s - p <= hi:
                    reach[j].add(p)
                    break
        if not reach[j]:
            return {"ok": False, "why": "no admissible predecessor", "lost_at": j,
                    "reach": None}
    # Virtual predecessor identity site at hdr-iw: the first row's identity
    # ends exactly at hdr+rowlen, so its site is hdr+rowlen-iw and the gap to
    # the virtual site is exactly rowlen (identity always ends at the row end).
    prev = {hdr - iw}
    for j in range(n):
        keep = {p for p in reach[j] if any(lo <= p - s <= hi for s in prev)}
        if not keep:
            return {"ok": False, "why": "row-length window excludes every candidate",
                    "lost_at": j, "reach": None}
        reach[j] = keep
        prev = keep
    sizes = [len(s) for s in reach]
    return {"ok": True, "reach": reach, "rows": n,
            "multi_rows": [j for j, s in enumerate(sizes) if s > 1],
            "max_reach": max(sizes), "min_reach": min(sizes),
            "unique": max(sizes) == 1,
            "end": max(reach[-1]) + iw, "payload_len": L}


def pick(reach: list[set], raw: bytes, window: tuple = GEN_WINDOW,
         anchor_abs: int | None = None) -> list[int]:
    """Chain-consistent reconstruction with a UID-anchored tie-break.

    Two defects were found here by t81 on real payloads and both are fixed by
    construction below:

    1. Taking `min(reach[j])` independently per row is wrong — a candidate can
       be numerically smallest yet unreachable from the chosen predecessor.
       The reconstruction therefore stays on the chain (forward, using the
       window against the position actually chosen).

    2. A run of zero bytes followed by a small u32 yields several positions
       that all read ordinal==j with an equal UID pair: t10 row 0 has
       {63,64,65,66} giving UIDs {0x05000000, 0x00050000, 0x00000500, 5}.
       These are one byte-run read at successive offsets, so `min` picks the
       byte-rotated artefact. The honest discriminator is the UID itself: the
       true UID sits in the same numeric neighbourhood as the rows that were
       pinned unambiguously (rows 1..250 hold 6,7,8,...), while an artefact is
       orders of magnitude away. Among chain-admissible candidates we therefore
       choose the one whose UID is nearest any pinned UID.
    """
    lo, hi = window
    pinned = [next(iter(s)) for s in reach if len(s) == 1]
    ref = [u32(raw, p + 4) for p in pinned] or None

    out: list[int] = []
    prev = None
    for j, s in enumerate(reach):
        if prev is None:
            cands = set(s)
        else:
            cands = {p for p in s if lo <= p - prev <= hi} or set(s)
        if not cands:
            return out
        if j == 0 and anchor_abs is not None and anchor_abs in cands:
            # A frozen FIELDS anchor (fm24_dump.py, snapshot evidence/fm24)
            # names the identity site outright, e.g. (client,23) rdui@1 means
            # the identity triple starts at row_base+1 = 15. When the row-0
            # byte-run leaves several chain-admissible sites, the frozen
            # anchor is the only tie-break that is not a guess.
            p = anchor_abs
        elif len(cands) == 1 or ref is None:
            p = min(cands)
        else:
            # nearest pinned UID wins; ties fall back to the smallest position
            p = min(cands, key=lambda q: (min(abs(u32(raw, q + 4) - u) for u in ref), q))
        out.append(p)
        prev = p
    return out


def identity_summary(raw: bytes, pos: list[int]) -> dict:
    L = len(raw)
    ord_ok = sum(1 for j, p in enumerate(pos) if u32(raw, p) == j)
    uid_ok = sum(1 for p in pos if u32(raw, p + 4) == u32(raw, p + 8) != 0)
    tail = {raw[p + 12] for p in pos if p + 12 < L}
    uids = [u32(raw, p + 4) for p in pos]
    return {"rows": len(pos), "ordinal_eq_index": ord_ok, "uid_pair_ok": uid_ok,
            "tail_byte_values": sorted(tail)[:8],
            "uid_distinct": len(set(uids)), "uid_min": min(uids) if uids else None,
            "uid_max": max(uids) if uids else None,
            "uid_sha256": hashlib.sha256(
                b"".join(struct.pack("<I", v) for v in uids)).hexdigest()}


# --------------------------------------------------------------- table spec ---
# Row-length windows per (archive, table). For the 9 t74 tables the window is
# taken verbatim from t74 frames.json; the three t81 targets and nation are
# given a generous window because t74 never framed them (nation is fixed at
# 13+24,710+9 but the identity is only 12B, see below).
T74_WINDOW = {}
try:  # pragma: no cover - data-dependent, absent in a bare checkout
    _fr = json.loads(FRAMES.read_text(encoding="utf-8"))
    for _t, _v in _fr["tables"].items():
        for _a, _av in _v["archives"].items():
            if _av.get("count") is not None:
                T74_WINDOW[(int(_t), _a)] = tuple(_av["row_len_range"])
except Exception:  # noqa: BLE001 - frames.json optional for --selftest
    T74_WINDOW = {}

# Identity widths observed: every t74 table is 13B. t10 (nation) is the one
# exception — t28's frozen walk puts identity at [ord][uid][uid] with the
# selector consumed separately, giving 12B there. Both are tried and the
# winner is the width whose chain closes.
WIDTH_TRY = (13, 12)

# Tables whose identity tail byte is a selector, not a marker (t74 §2: team's
# 13th byte is {0,10,11}). For these the marker predicate must be OFF from the
# start; every other table is tried marker-0 first and falls back to no-marker.
SELECTOR_TAIL = {24}

TARGETS = [(10, "client"), (10, "server"), (8, "client"), (8, "server"),
           (27, "client"), (27, "server"), (47, "client"), (47, "server"),
           (24, "server"), (6, "client"), (6, "server"),
           (23, "client"), (23, "server"), (35, "client"), (35, "server"),
           (2, "client"), (2, "server"), (3, "client"), (3, "server"),
           (25, "client"), (25, "server"), (21, "client"), (21, "server"),
           (0, "client"), (0, "server"), (5, "client"), (5, "server"),
           (19, "client"), (19, "server"), (41, "client"), (41, "server"),
           (18, "client"), (18, "server"), (7, "client"), (7, "server"),
           (56, "client"), (56, "server")]

ENTITY_TID = {"continent": 5, "language": 8, "nation": 10, "region": 19,
              "currency": 41, "agreement": 56, "club": 3, "comp": 25,
              "stadium": 21, "city": 2, "local_region": 47, "weather": 27,
              "person": 1, "team": 24, "injury": 6, "stage_name": 23,
              "description": 35}


# Frozen FIELDS identity anchors (scripts/fm24_dump.py, snapshot evidence/fm24
# 2026-11-18). Only used as a row-0 tie-break when the byte-run leaves several
# chain-admissible identity sites — never to override a data-closed result.
FROZEN_IDENT = {(6, "client"): 3, (6, "server"): 3,
                (23, "client"): 1, (23, "server"): 1,
                (35, "client"): 2, (35, "server"): 2}


def index_one(archive: str, tid: int, raw: bytes | None = None) -> dict:
    """Build the FK index record for one (archive, table)."""
    if raw is None:
        raw = load_payload(archive, tid)
    L = len(raw)
    n = u32(raw, 8)
    win = T74_WINDOW.get((tid, archive), GEN_WINDOW)
    # The marker predicate is an *accelerator*, not doctrine. t74 certifies
    # marker==0 for its 16 archives (team excepted), but a table outside t74
    # (club, 3) carries non-zero tail bytes on some rows, so a hard assumption
    # would kill an otherwise closed chain. Try marker-0 first, then fall back
    # without it, and record which hypothesis actually closed.
    modes = [False] if tid in SELECTOR_TAIL else [True, False]
    tries = []
    best = None
    for mk in modes:
        cand = candidate_map(raw, marker0=mk)
        for w in WIDTH_TRY:
            r = solve_chain(raw, cand, n, window=win, iw=w)
            rec = {"marker0": mk, "identity_width": w, "ok": r["ok"],
                   "why": r.get("why"), "lost_at": r.get("lost_at"),
                   "unique": r.get("unique"),
                   "multi_rows": len(r["multi_rows"]) if r["ok"] else None,
                   "max_reach": r.get("max_reach"),
                   "end": r.get("end"),
                   "end_matches": (r.get("end") == L - FOOTER) if r["ok"] else None}
            tries.append(rec)
            if r["ok"] and rec["end_matches"]:
                if best is None or (w == IW and mk):
                    best = (w, mk, r)
                if w == IW and mk:
                    break
        if best is not None and best[0] == IW and best[1]:
            break
    if best is None:
        return {"archive": archive, "table": tid, "payload_len": L,
                "row_count_from_header": n, "window": list(win),
                "status": "escalate_to_sol",
                "why": "no identity width closed the ordinal chain",
                "width_tries": tries}
    w, mk, r = best
    # When t74 never framed this table the generic window is deliberately wide,
    # and a wide window admits byte-run prefix artefacts (t23 row 0 could read
    # ordinal==0 at three offsets). Re-derive the *observed* row-length window
    # from the chain itself and re-solve under it; the table then becomes
    # self-framing and the artefact window disappears.
    derived = None
    if (tid, archive) not in T74_WINDOW:
        probe = pick(r["reach"], raw, window=win)
        gaps = [probe[i + 1] - probe[i] for i in range(len(probe) - 1)]
        gaps.append(probe[0] + w - H0)
        if gaps and min(gaps) > 0:
            derived = (min(gaps), max(gaps))
            r2 = solve_chain(raw, cand, n, window=derived, iw=w)
            if r2["ok"] and r2["end"] == L - FOOTER:
                r = r2
                win = derived
    pos = pick(r["reach"], raw, window=win,
               anchor_abs=(H0 + FROZEN_IDENT[(tid, archive)]
                           if (tid, archive) in FROZEN_IDENT else None))
    idn = identity_summary(raw, pos)
    uids = [u32(raw, p + 4) for p in pos]
    rec = {
        "archive": archive, "table": tid, "payload_len": L,
        "row_count_from_header": n, "row_count": idn["rows"],
        "window": list(win), "identity_width": w,
        "marker0_applied": mk,
        "window_derived_from_chain": derived is not None,
        "identity_site": "row_end-%d" % w,
        "status": "closed",
        "closure": "identity_end == len - %d" % FOOTER,
        "unique_frame": r["unique"],
        "tie_break": None if r["unique"] else
                     "smallest identity position per row; %d row(s) had >1 candidate"
                     % len(r["multi_rows"]),
        "multi_rows": r["multi_rows"][:20],
        "max_reach": r["max_reach"],
        "identity": idn,
        "ordinal_set": {"kind": "range", "start": 0, "stop": idn["rows"] - 1,
                        "count": idn["rows"]},
        "uid_set": {"kind": "explicit" if idn["rows"] <= 20000 else "digest",
                    "count": idn["rows"],
                    "distinct": idn["uid_distinct"],
                    "min": idn["uid_min"], "max": idn["uid_max"],
                    "sha256": idn["uid_sha256"]},
        "width_tries": tries,
    }
    if idn["rows"] <= 20000:
        rec["uid_set"]["values"] = uids
    return rec


def build_fk_index(tables=None, archive_filter=None, verbose: bool = False) -> dict:
    """Build `{table_id: {ordinal_set, uid_set, row_count}}` for every target."""
    targets = TARGETS if tables is None else [
        t for t in TARGETS if t[0] in tables and
        (archive_filter is None or t[1] == archive_filter)]
    out: dict[str, dict] = {}
    for tid, arch in targets:
        try:
            rec = index_one(arch, tid)
        except Exception as exc:  # noqa: BLE001 - absence is data, not a crash
            rec = {"archive": arch, "table": tid,
                   "status": "absent" if "not found" in str(exc) else "error",
                   "why": "%s: %s" % (type(exc).__name__, exc)}
        key = "%d/%s" % (tid, arch)
        out[key] = rec
        if verbose:
            print("  %-10s %-6s %-8s rows=%s width=%s unique=%s"
                  % (tid, arch, rec["status"], rec.get("row_count"),
                     rec.get("identity_width"), rec.get("unique_frame")),
                  file=sys.stderr)
    # per-table roll-up (a table is usable when either archive closes)
    roll: dict[str, dict] = {}
    for key, rec in out.items():
        tid = rec["table"]
        e = roll.setdefault(str(tid), {"table": tid, "archives": {},
                                       "row_count": None, "ordinal_set": None})
        e["archives"][rec["archive"]] = rec["status"]
        if rec["status"] == "closed":
            e["row_count"] = rec["row_count"]
            e["ordinal_set"] = {"kind": "range", "start": 0,
                                "stop": rec["row_count"] - 1,
                                "count": rec["row_count"]}
            e["identity_width"] = rec["identity_width"]
    return {"schema": "t81.fk_index.v1", "task": "t81",
            "purpose": "FK ordinal/UID domain index for fixed AND variable tables",
            "identity_doctrine": {
                "triple": "[ordinal u32][UID u32][UID u32][marker/selector 1B]",
                "widths_tried": list(WIDTH_TRY),
                "ordinal_semantics": "u32 at the identity site equals the row "
                                     "index on every row, so ordinal_set is the "
                                     "index range 0..count-1 by construction",
                "uid_semantics": "u32(identity+4) == u32(identity+8) != 0",
                "frame_rule": "last identity ends exactly at payload_len - 8; "
                              "row length window per t74 frames.json",
                "t73_gap_closed": "t73 reference_uids() needs canonical_frame(), "
                                  "which needs a fixed stride; this DP is "
                                  "grammar-free and closes variable tables"},
            "targets": out, "rollup": roll}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build the t81 FK ordinal/UID index (variable-length capable).")
    ap.add_argument("--json", help="write the index to this path")
    ap.add_argument("--table", type=int, action="append",
                    help="restrict to these table ids (repeatable)")
    ap.add_argument("--archive", choices=["client", "server"])
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    idx = build_fk_index(tables=args.table, archive_filter=args.archive,
                         verbose=args.verbose)
    closed = sum(1 for r in idx["targets"].values() if r["status"] == "closed")
    total = len(idx["targets"])
    print(json.dumps({"targets": total, "closed": closed,
                      "escalate": total - closed,
                      "tables": {k: v["status"] for k, v in idx["targets"].items()}},
                     ensure_ascii=False, indent=1))
    if args.json:
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote %s" % p, file=sys.stderr)
    return 0 if closed == total else 1


# --------------------------------------------------------------- selftest ----
def selftest() -> int:
    """Synthetic payloads with known chains; no game data needed."""
    fails: list[str] = []

    def chk(cond: bool, label: str, detail: str = "") -> None:
        print(("PASS " if cond else "FAIL ") + label + ("  " + detail if detail else ""))
        if not cond:
            fails.append(label)

    def synth(n: int, var: bool, seed: int = 1) -> bytes:
        body = b""
        rows = []
        for j in range(n):
            pad = bytes(((j * 7 + seed) % 5) + 3) if var else b"\x00" * 4
            body += pad + struct.pack("<III", j, 900 + j, 900 + j) + b"\x00"
            rows.append(len(pad) + 13)
        hdr = b"\x03\x01tad.\xf1\x0d" + struct.pack("<I", n) + b"\x00\x00"
        return hdr + body + b"\x00\x00\x00\x01" + struct.pack("<I", 0x77)

    # 1. fixed-length synthetic (4-byte pad -> stride 17)
    p = synth(40, var=False)
    n = u32(p, 8)
    r = solve_chain(p, candidate_map(p), n, window=(17, 17))
    chk(r["ok"] and r["unique"], "synth fixed: chain closes and is unique",
        "multi=%d" % (len(r["multi_rows"]) if r["ok"] else -1))
    # 2. variable-length synthetic. Row 0 legitimately stays 2-way (the
    #    all-zero/garbage pad admits a one-byte prefix coincidence) — that is
    #    the ambiguity the DP exists to REPORT, not a defect. The load-bearing
    #    assertion is that every later row is pinned and the chain closes.
    p2 = synth(60, var=True)
    n2 = u32(p2, 8)
    r2 = solve_chain(p2, candidate_map(p2), n2, window=(16, 20))
    chk(r2["ok"] and r2["end"] == len(p2) - FOOTER,
        "synth variable: chain closes at len-footer",
        "end=%s len-8=%d" % (r2.get("end"), len(p2) - FOOTER))
    chk(r2["ok"] and all(len(r2["reach"][j]) == 1 for j in range(1, n2)),
        "synth variable: every row after 0 is pinned",
        "multi_rows=%s" % (r2["multi_rows"] if r2["ok"] else None))
    # 3. identity summary invariants
    if r2["ok"]:
        pos = pick(r2["reach"], p2)
        s = identity_summary(p2, pos)
        chk(s["ordinal_eq_index"] == n2 and s["uid_pair_ok"] == n2,
            "synth: ordinal==index and UID pair on 100% of rows", str(s["rows"]))
        chk(s["uid_sha256"] and s["uid_distinct"] == n2,
            "synth: UID digest and distinct count", str(s["uid_distinct"]))
    # 4. window that cannot fit must fail, not silently accept
    r3 = solve_chain(p2, candidate_map(p2), n2, window=(500, 600))
    chk(not r3["ok"], "synth: impossible window is rejected (no silent accept)",
        str(r3.get("why")))
    # 5. footer mismatch must fail: pair a 40-row body with a 20-row header
    r4 = solve_chain(p, candidate_map(p), 20, window=(17, 17))
    chk(not r4["ok"], "synth: header/body mismatch is rejected",
        str(r4.get("why")))
    print("\n%d passed, %d failed" % (11 - len(fails) - 6 + 6 - len(fails), len(fails))
          if False else "\n%d checks failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
