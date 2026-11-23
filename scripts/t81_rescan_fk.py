#!/usr/bin/env python3
"""t81 — re-adjudicate FK lanes with the variable-length ordinal index.

t73's FK rule was "whole-u32 column, every value inside the target's live UID
domain, at rate 1.0". That rule is correct but its *domain provider* could only
read fixed-stride tables, so every lane pointing at a variable table came back
`unmapped` (t73 REPORT §3.4). `scripts/t81_fk_index.py` supplies the missing
domains; this module re-runs the lanes and reports, per lane:

  hit_ordinal   every non-sentinel value is a valid row index of the target
  wrong_uid     the column is a UID set of the target instead (encoding check)
  sentinel      values equal to the null sentinel, reported separately
  decision      mapped / unmapped / refuted, with the discriminator that decided

An ordinal hit is only accepted as a *mapping* when the domain test is
discriminating. A column of small integers is trivially "inside" the ordinal
domain of any large table, so the report also carries `tightness`
(max / row_count) and `coverage` (distinct targets touched / row_count). A lane
is `mapped` only when it is both in-domain and tight; otherwise `candidate`.

    FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data \
      py -V:3.12 -I -B scripts/t81_rescan_fk.py --json scratch/t81/out/rescan_fk_city.json

Exit codes: 0 all lanes adjudicated / 1 a check failed / 2 usage or fatal.
"""
from __future__ import annotations

import argparse
import json
import runpy
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
IDX = REPO / "scratch" / "t81" / "out" / "fk_index.json"
NULL32 = 0xFFFFFFFF
NULL16 = 0xFFFF
NULL8 = 0xFF

_CORE = None
_IDX = None


def core():
    global _CORE
    if _CORE is None:
        _CORE = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"),
                               run_name="t81_rescan_core")
    return _CORE


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def fk_index() -> dict:
    global _IDX
    if _IDX is None:
        _IDX = json.loads(IDX.read_text(encoding="utf-8"))
    return _IDX


def target(tid: int, archive: str = "client") -> dict | None:
    """Index record for a target table; prefers the requested archive."""
    t = fk_index()["targets"]
    return t.get(f"{tid}/{archive}") or t.get(f"{tid}/client") or t.get(f"{tid}/server")


def uid_domain(tid: int, archive: str = "client") -> set | None:
    rec = target(tid, archive)
    if not rec or rec["status"] != "closed":
        return None
    vals = rec["uid_set"].get("values")
    return set(vals) if vals else None


def ordinal_domain(tid: int, archive: str = "client") -> tuple[int, int] | None:
    rec = target(tid, archive)
    if not rec or rec["status"] != "closed":
        return None
    o = rec["ordinal_set"]
    return o["start"], o["stop"]


def adjudicate(values: list[int], tid: int, archive: str = "client",
               width: int = 4) -> dict:
    """Decide whether a column addresses table `tid` by ordinal or by UID."""
    rec = target(tid, archive)
    if rec is None or rec["status"] != "closed":
        return {"target": tid, "available": False,
                "why": "no closed index record for this target",
                "index_status": None if rec is None else rec["status"]}
    null = {4: NULL32, 2: NULL16, 1: NULL8}[width]
    n = len(values)
    sent = sum(1 for v in values if v == null)
    live = [v for v in values if v != null]
    N = rec["row_count"]
    if not live:
        return {"target": tid, "available": True, "rows": n, "sentinel": sent,
                "decision": "all-sentinel", "mapped": False}
    in_dom = sum(1 for v in live if 0 <= v < N)
    distinct = len({v for v in live})
    tight = max(live) / N if N else None
    cov = distinct / N if N else None
    uids = uid_domain(tid, archive)
    uid_hit = sum(1 for v in live if v in uids) if uids else 0
    out = {"target": tid, "target_rows": N, "available": True, "rows": n,
           "sentinel": sent, "live": len(live),
           "ordinal": {"in_domain": in_dom, "rate": in_dom / len(live),
                       "min": min(live), "max": max(live),
                       "distinct": distinct, "tightness": tight,
                       "coverage": cov},
           "uid": {"domain_size": len(uids) if uids else 0,
                   "hit": uid_hit, "rate": uid_hit / len(live)}}
    # Decision order: UID encoding is checked first because it is the t73 rule
    # and a UID hit at rate 1.0 would refute an ordinal reading outright.
    if uids and uid_hit == len(live):
        out.update({"decision": "uid-encoding", "mapped": False,
                    "why": "every live value is a UID of the target; the column "
                           "addresses the table by UID, not by row index"})
    elif in_dom == len(live) and tight is not None and tight >= 0.5:
        out.update({"decision": "mapped-ordinal", "mapped": True,
                    "why": "every live value is a valid row index and the "
                           "maximum reaches %.1f%% of the target's row count, "
                           "so the domain test discriminates" % (100 * tight)})
    elif in_dom == len(live):
        out.update({"decision": "candidate-ordinal", "mapped": False,
                    "why": "every live value is a valid row index but the "
                           "maximum is only %.1f%% of the target's row count: "
                           "any small-integer column would pass, so the domain "
                           "does not discriminate" % (100 * tight)})
    else:
        out.update({"decision": "refuted", "mapped": False,
                    "why": "%d of %d live values fall outside 0..%d"
                           % (len(live) - in_dom, len(live), N - 1)})
    return out


def column(raw: bytes, H: int, S: int, n: int, off: int, w: int = 4,
           signed: bool = False) -> list[int]:
    return [int.from_bytes(raw[H + j * S + off: H + j * S + off + w], "little",
                           signed=signed) for j in range(n)]


def walk_rows(raw: bytes, tid: int) -> list[int] | None:
    """Identity positions for a variable table, via the t81 index builder."""
    sys.path.insert(0, str(REPO / "scripts"))
    import importlib.util  # noqa: PLC0415
    spec = importlib.util.spec_from_file_location(
        "t81_fk_index", str(REPO / "scripts" / "t81_fk_index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------ lane registry ---
# city(2) client: t73 §3.4 left exactly these four lanes unmapped. Offsets are
# the frozen FIELDS / t05 layout anchors, so the lane is not re-derived here —
# only its *target domain* is new.
CITY_LANES = [
    ("Cnti", 10, 10, "nation"),
    ("Clgi", 21, 8, "language"),
    ("Clri", 25, 47, "local_region"),
    ("Cwea", 14, 27, "weather"),
]

# t76c lanes whose target is a variable table (the index's reason to exist).
T76_LANES = [
    # (source table, archive, field, row-offset, target tid, target entity)
    (18, "client", "Dtm1", 4, 24, "team"),
    (18, "client", "Dtm2", 8, 24, "team"),
    (47, "client", "Lnat?", 24, 10, "nation"),
    (47, "client", "Lwea?", 24, 27, "weather"),
]


def rescan_city() -> dict:
    raw = core()["load_payload"]("client", 2)
    H, S, n = 14, 43, 56293
    lanes = []
    for field, off, tid, ent in CITY_LANES:
        vals = column(raw, H, S, n, off)
        adj = adjudicate(vals, tid, "client")
        adj.update({"field": field, "offset": off, "entity": ent,
                    "source": "city(2) client",
                    "grade_before": "unmapped (t73 §3.4)",
                    "grade_after": GRADE_AFTER.get(adj.get("decision"), "unmapped")})
        lanes.append(adj)
    return {"schema": "t81.rescan.v1", "task": "t81", "scope": "city(2) FK lanes",
            "index": "scratch/t81/out/fk_index.json",
            "method": "ordinal-domain test against the target's row-index range, "
                      "with a UID-encoding control and an explicit sentinel column",
            "lanes": lanes,
            "summary": {d: sum(1 for x in lanes if x.get("decision") == d)
                        for d in ("mapped-ordinal", "candidate-ordinal",
                                  "uid-encoding", "refuted")}}


GRADE_AFTER = {"mapped-ordinal": "L2/candidate",
               "candidate-ordinal": "L2/candidate (domain non-discriminating)",
               "uid-encoding": "refuted-as-ordinal",
               "refuted": "unmapped"}


def biz_base(raw: bytes, tid: int, row_starts: list[int]) -> list[int]:
    """Per-row base that the t76c slot offsets are measured against.

    t76c reports offsets relative to its own `biz` slice, which differs per
    table: lcrg's biz is the whole row body, derby's biz is the *numeric
    region* that follows the length-prefixed names. Using the row start for
    derby reads into the name bytes and every lane looks refuted (this is the
    exact false negative t81 hit before adding this helper).
    """
    if tid != 18:
        return list(row_starts)
    out = []
    for s in row_starts:
        p = s
        nb = 0
        for _ in range(4):  # derby always carries 4 name slots
            ln = u32(raw, p)
            nb += ln
            p += 4 + ln
        out.append(s + 16 + nb)
    return out


def rescan_t76() -> dict:
    """Re-run the t76 lanes whose target is a variable table."""
    import importlib.util  # noqa: PLC0415
    spec = importlib.util.spec_from_file_location(
        "t81_fk_index", str(REPO / "scripts" / "t81_fk_index.py"))
    fk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fk)
    lanes = []
    # derby(18): Dtm1@4 / Dtm2@8 -> team(24).  Rows are variable, so addresses
    # come from the index builder rather than a fixed stride.
    for tid, arch, field, off, ref, ent in T76_LANES:
        raw = core()["load_payload"](arch, tid)
        rec = fk.index_one(arch, tid, raw)
        if rec["status"] != "closed":
            lanes.append({"field": field, "target": ref, "entity": ent,
                          "decision": "unavailable",
                          "why": "source table did not close: %s" % rec.get("why")})
            continue
        win = tuple(rec["window"])
        cand = fk.candidate_map(raw, marker0=rec["marker0_applied"])
        n = rec["row_count"]
        res = fk.solve_chain(raw, cand, n, window=win, iw=rec["identity_width"])
        pos = fk.pick(res["reach"], raw, window=win)
        # `pos[j]` is the identity SITE, not the row start. Row-relative offsets
        # must be measured from the row base, which is the previous row's
        # identity end (or the header for row 0). Reading at `p - 13 + off`
        # would land inside the previous row's identity.
        iw = rec["identity_width"]
        starts = [14] + [pos[j - 1] + iw for j in range(1, n)]
        base = biz_base(raw, tid, starts)
        vals = [u32(raw, base[j] + off) for j in range(n)]
        adj = adjudicate(vals, ref, "server" if ref == 24 else arch)
        adj.update({"field": field, "offset": off, "entity": ent,
                    "source": "t%d %s" % (tid, arch),
                    "grade_before": "unmapped (t76c, variable target)",
                    "grade_after": GRADE_AFTER.get(adj.get("decision"), "unmapped")})
        lanes.append(adj)
    return {"schema": "t81.rescan.v1", "task": "t81",
            "scope": "t76 cross-table FK lanes (variable targets)",
            "note": "only lanes whose TARGET is a variable table are re-run; "
                    "fixed-target lanes are unchanged from t76c",
            "lanes": lanes,
            "summary": {d: sum(1 for x in lanes if x.get("decision") == d)
                        for d in ("mapped-ordinal", "candidate-ordinal",
                                  "uid-encoding", "refuted", "unavailable")}}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Re-adjudicate FK lanes using the t81 variable-table index.")
    ap.add_argument("--json", help="write the city rescan here")
    ap.add_argument("--json-t76", help="write the t76 rescan here")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    rc = 0
    if args.json:
        out = rescan_city()
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("city: " + json.dumps(out["summary"]), file=sys.stderr)
        for ln in out["lanes"]:
            print("  %-5s -> %-12s %-20s %s"
                  % (ln["field"], ln.get("entity"), ln.get("decision"),
                     ln.get("grade_after")), file=sys.stderr)
        rc = 0 if all(l.get("decision") for l in out["lanes"]) else 1
    if args.json_t76:
        out = rescan_t76()
        p = Path(args.json_t76)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("t76: " + json.dumps(out["summary"]), file=sys.stderr)
        for ln in out["lanes"]:
            print("  %-6s -> %-12s %-20s %s"
                  % (ln.get("field"), ln.get("entity"), ln.get("decision"),
                     ln.get("grade_after")), file=sys.stderr)
    return rc


# --------------------------------------------------------------- selftest ----
def selftest() -> int:
    """Domain-adjudication logic on synthetic columns; no game data needed."""
    fails: list[str] = []

    def chk(cond: bool, label: str, detail: str = "") -> None:
        print(("PASS " if cond else "FAIL ") + label + ("  " + detail if detail else ""))
        if not cond:
            fails.append(label)

    # stub target: 1000 rows, UID set {9000..9009}
    global _IDX
    _IDX = {"targets": {"999/client": {
        "table": 999, "archive": "client", "status": "closed", "row_count": 1000,
        "ordinal_set": {"start": 0, "stop": 999, "count": 1000},
        "uid_set": {"kind": "explicit", "count": 10, "distinct": 10,
                    "values": list(range(9000, 9010))}}}}

    a = adjudicate([0, 5, 999, 400], 999)
    chk(a["decision"] == "mapped-ordinal" and a["mapped"],
        "tight ordinal column is mapped", a["decision"])
    b = adjudicate([0, 1, 2, 3], 999)
    chk(b["decision"] == "candidate-ordinal" and not b["mapped"],
        "small-integer column is only a candidate (non-discriminating)", b["decision"])
    c = adjudicate([9000, 9001, 9005], 999)
    chk(c["decision"] == "uid-encoding", "UID column is refuted as ordinal",
        c["decision"])
    d = adjudicate([0, 5000, NULL32], 999)
    chk(d["decision"] == "refuted" and d["sentinel"] == 1,
        "out-of-domain column is refuted and the sentinel is counted separately",
        "sentinel=%d" % d["sentinel"])
    e = adjudicate([NULL32, NULL32], 999)
    chk(e["decision"] == "all-sentinel", "all-sentinel column is its own verdict",
        e["decision"])
    f = adjudicate([0, 5], 12345)
    chk(not f["available"], "absent target is reported unavailable", str(f.get("why")))
    # a column that is dense across the whole range must be tight AND wide
    g = adjudicate(list(range(0, 1000, 1)), 999)
    chk(g["decision"] == "mapped-ordinal" and g["ordinal"]["coverage"] == 1.0,
        "full-coverage column is mapped with coverage 1.0", str(g["ordinal"]["coverage"]))
    print("\n%d checks failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
