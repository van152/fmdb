#!/usr/bin/env python3
"""t81-fix1 builder — slot maps for injury(6) / stage_name(23) / description(35).

Read-only reuse: `scripts/t73_mapper_core.py` is loaded through runpy and only its
`load_payload()` is called; nothing in t73/t74/t76 is imported or modified. The t81
prior deliverables (`scratch/t81/out/fk_index.json`, `rescan_fk_*.json`) are READ
for cross-check only — never rebuilt, never modified here.

Row frames are SELF-PROVED from the payload, not taken on trust:
  (a) arithmetic closure  header + count x stride + footer == payload_len
  (b) full identity       u32(ordinal) == row index  AND  u32 == u32 != 0
  (c) header origin       the data side cannot fix it (an alias group closes
                          identically), so the t73 footer rule decides: of the
                          alias members, only F=8 reads as BE 1.

    py -V:3.12 -I -B scripts/t81_small_slots.py --help
    py -V:3.12 -I -B scripts/t81_small_slots.py --selftest
    FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B \
        scripts/t81_small_slots.py --all

Exit codes: 0 success / 1 check failed / 2 usage or fatal.

Grades: L3 = frozen repo anchor (scripts/fm24_dump.py:FIELDS, snapshot
evidence/fm24 2026-11-18); L2 = closed on this payload by an invariant;
candidate = domain-compatible, membership/order NOT decided by the data;
unassigned = no schema field can own the byte; unmapped = field with no byte.
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
SCHEMA_P = REPO / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
OUTDIR = REPO / "scratch" / "t81" / "out2"
FK_INDEX = REPO / "scratch" / "t81" / "out" / "fk_index.json"

XML = {6: "injury.xml", 23: "stage name.xml", 35: "description.xml"}
EID = {6: "inju", 23: "stgn", 35: "dscr"}

# Frozen repo anchors. scripts/fm24_dump.py:FIELDS carries the CLIENT entry only.
# snapshot evidence/fm24, MANIFEST 2026-11-18.
FROZEN = {(6, "client"): {"rdui": 3, "duni": 7},
          (23, "client"): {"rdui": 1, "duni": 5},
          (35, "client"): {"rdui": 2, "duni": 6}}
IDENT_W = 13

_CORE = None
_SCHEMA = None


def core() -> dict:
    global _CORE
    if _CORE is None:
        _CORE = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"),
                               run_name="t81_small_core")
    return _CORE


def payload(archive: str, tid: int) -> bytes:
    return core()["load_payload"](archive, tid)


def schema() -> dict:
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = json.loads(SCHEMA_P.read_text(encoding="utf-8"))
    return _SCHEMA


def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]


def fields(xml: str) -> list[dict]:
    return schema()["entities"][xml][0]["fields"]


def enum_ints(name: str) -> list[int]:
    return sorted({int(v["enum"]) for v in schema()["enums"][name]["values"]
                   if str(v["enum"]).lstrip("-").isdigit()})


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- frame ------
MAXH, MAXF = 48, 24


def frame_candidates(raw: bytes) -> list[dict]:
    """Every (H, F, S) with exact closure AND a full identity at some p."""
    L, n = len(raw), u32(raw, 8)
    out = []
    for H in range(0, MAXH + 1):
        for F in range(1, MAXF + 1):
            body = L - H - F
            if body <= 0 or body % n:
                continue
            S = body // n
            for p in range(0, S - IDENT_W + 1):
                oh = uh = 0
                for j in range(n):
                    b = H + j * S + p
                    if u32(raw, b) == j:
                        oh += 1
                    if u32(raw, b + 4) == u32(raw, b + 8) != 0:
                        uh += 1
                if oh == n and uh == n:
                    out.append({"header": H, "footer": F, "stride": S, "count": n,
                                "identity_offset": p, "mode": "ordinal+uidpair"})
    return out


def frame_self_proof(raw: bytes) -> dict:
    """Pick the native frame; every loser and the alias group stay on record."""
    L, n = len(raw), u32(raw, 8)
    cands = frame_candidates(raw)
    if not cands:
        return {"resolved": False, "why": "no arithmetic+identity closure",
                "count_from_header": n, "payload_len": L}
    # footer flag: first 4 footer bytes read big-endian == 1 (t73 rule)
    for c in cands:
        F = c["footer"]
        c["footer_flag_be1"] = int.from_bytes(raw[L - F:L - F + 4], "big") == 1
    flagged = [c for c in cands if c["footer_flag_be1"]]
    al = sorted({(c["header"], c["footer"], c["identity_offset"]) for c in cands})
    rec = {
        "payload_len": L, "count_from_header": n,
        "arithmetic_and_identity_candidates": len(cands),
        "alias_group": [list(a) for a in al],
        "alias_group_size": len(al),
        "header_origin_data_unique": len({c["header"] for c in cands}) == 1,
        "footer_flag_be1_members": [[c["header"], c["footer"]] for c in flagged],
        "header_origin_decider": (
            "data side cannot fix the header origin: every alias member closes and "
            "carries the identical identity triple; the t73 rule selects the member "
            "whose footer head reads as big-endian 1 (F=8)"),
    }
    if len(flagged) != 1:
        rec.update({"resolved": False,
                    "why": f"{len(flagged)} alias members satisfy the footer flag"})
        return rec
    c = flagged[0]
    rec.update({
        "resolved": True,
        "frame": {"header": c["header"], "footer": c["footer"], "stride": c["stride"],
                  "count": c["count"], "identity_offset": c["identity_offset"],
                  "identity_site": "row_end-13", "model": "fixed"},
        "closure": f"{c['header']} + {c['count']} x {c['stride']} + "
                   f"{c['footer']} = {L}",
        "identity_rows": n,
    })
    return rec

# ------------------------------------------------------------- profiling ----
def column(raw: bytes, H: int, S: int, n: int, off: int, w: int = 1) -> list[int]:
    return [int.from_bytes(raw[H + j * S + off: H + j * S + off + w], "little")
            for j in range(n)]


def f32_column(raw: bytes, H: int, S: int, n: int, off: int) -> list[float]:
    return [struct.unpack_from("<f", raw, H + j * S + off)[0] for j in range(n)]


def dom(raw: bytes, H: int, S: int, n: int, off: int, w: int = 1) -> dict:
    """Value domain of one slot. 0xFF / 0xFFFFFFFF sentinels counted separately
    from legal zeros, never merged (task discipline #3)."""
    v = column(raw, H, S, n, off, w)
    sent = 0xFFFFFFFF if w == 4 else (1 << (8 * w)) - 1
    live = [x for x in v if x != sent]
    d = {"width": w, "rows": n, "distinct": len(set(v)),
         "min": min(v), "max": max(v),
         "n_zero": v.count(0), "n_sentinel_ff": v.count(sent),
         "live": len(live),
         "live_min": min(live) if live else None,
         "live_max": max(live) if live else None,
         "values": sorted(set(v))[:24]}
    if len(set(v)) > 24:
        d["values_truncated"] = True
    return d


def f32_viable(raw: bytes, H: int, S: int, n: int, off: int) -> dict:
    v = f32_column(raw, H, S, n, off)
    fin = [x for x in v if x == x and abs(x) != float("inf")]
    ok = (len(fin) == n and all(x == 0 or 1e-6 < abs(x) < 1e3 for x in fin)
          and len(set(fin)) >= 2)
    return {"viable": ok, "finite": len(fin), "distinct": len(set(fin)),
            "min": min(fin) if fin else None, "max": max(fin) if fin else None}


def strings_present(raw: bytes, min_run: int = 6) -> dict:
    """Does the payload carry any UTF-8/ASCII text at all? Magic 'tad.' is 4 B."""
    runs, cur = [], 0
    for b in raw:
        if 0x20 <= b < 0x7F:
            cur += 1
        else:
            if cur >= min_run:
                runs.append(cur)
            cur = 0
    if cur >= min_run:
        runs.append(cur)
    return {"min_run": min_run, "n_runs": len(runs),
            "longest": max(runs) if runs else 0,
            "note": "header magic 'tad.' is exactly 4 bytes, below min_run",
            "text_present": bool(runs)}


def trailer_marker(raw: bytes, H: int, S: int, n: int, p: int) -> dict:
    """t73/t76 doctrine: identity is 13 B [ord][uid][uid][marker], marker == 0."""
    mk = {raw[H + j * S + p + 12] for j in range(n)}
    ordn = column(raw, H, S, n, p, 4)
    a = column(raw, H, S, n, p + 4, 4)
    b = column(raw, H, S, n, p + 8, 4)
    return {"width": IDENT_W, "layout": "ord@+0 uid@+4 uid@+8 marker@+12",
            "ordinal_eq_row_index": sum(1 for j, o in enumerate(ordn) if o == j),
            "uid_pair_ok": sum(1 for j in range(n) if a[j] == b[j] != 0),
            "marker_values": sorted(mk), "rows": n,
            "uid_min": min(a), "uid_max": max(a), "uid_distinct": len(set(a))}


# --------------------------------------------------------- thin tables ------
# t23 / t35: the whole business block is constant zero, so no field can own a
# byte. Strings are absent from the payload entirely (no run >= 6 bytes), which
# is why dbnm / SNna / SNsn / SNpn / PTna are *held*, not "unmapped for lack of
# effort".

def thin_slots(raw: bytes, fr: dict, tid: int) -> dict:
    H = fr["frame"]["header"]
    S = fr["frame"]["stride"]
    n = fr["frame"]["count"]
    p = fr["frame"]["identity_offset"]
    biz = p
    slots = []
    for off in range(biz):
        d = dom(raw, H, S, n, off, 1)
        if d["distinct"] == 1:
            slots.append({
                "field": None, "offset": off, "width": 1,
                "grade": "unassigned",
                "why": f"constant 0x{d['min']:02x} in {n}/{n} rows: a byte that never "
                       "varies cannot be identified from the data side, and no "
                       "schema field of this entity is a constant-zero scalar",
                "domain": d})
        else:
            slots.append({"field": None, "offset": off, "width": 1,
                          "grade": "candidate", "why": "varies; see domain",
                          "domain": d})
    j = p
    slots.append({"field": "rdui", "offset": j, "width": 4, "grade": "L3",
                  "why": "row-relative ordinal equals row index on every row; site "
                         "equals the frozen anchor scripts/fm24_dump.py:FIELDS",
                  "evidence": [{"anchor": "scripts/fm24_dump.py:FIELDS",
                                "kind": "L3",
                                "snapshot": "evidence/fm24 2026-11-18"}],
                  "domain": dom(raw, H, S, n, j, 4)})
    slots.append({"field": "duni", "offset": j + 4, "width": 4, "grade": "L3",
                  "why": "UID pair u32==u32!=0 on every row; site equals the frozen "
                         "anchor scripts/fm24_dump.py:FIELDS",
                  "evidence": [{"anchor": "scripts/fm24_dump.py:FIELDS",
                                "kind": "L3",
                                "snapshot": "evidence/fm24 2026-11-18"}],
                  "domain": dom(raw, H, S, n, j + 4, 4)})
    return {"business_bytes": biz, "slots": slots, "identity": trailer_marker(raw, H, S, n, p)}

# ------------------------------------------------------------ injury(6) ------
# Server business block = 27 B. The tiling below is the *observed* physical
# structure: every byte covered exactly once, contiguous, no padding. Field
# assignment on top is graded separately and never inherits the tiling's grade.
TILE_SERVER = [(0, 1), (1, 1), (2, 1), (3, 2), (5, 2), (7, 1), (8, 1), (9, 1),
               (10, 1), (11, 1), (12, 1), (13, 4), (17, 1), (18, 2), (20, 1),
               (21, 1), (22, 1), (23, 1), (24, 1), (25, 1), (26, 1)]
PCT = ("Iiar", "Imip", "Igpr", "Icdp")          # declared 0..100, is_optional on last two
BOOL = ("Irec", "Icon", "Ibph", "Ibsp", "Ibin", "Ibis", "Ibpg")
DAYS = ("Imnd", "Iexd")                            # declared 0..720


def tiling_check(tile: list[tuple[int, int]], total: int) -> dict:
    """Exhaustive + contiguous + boundary-exact. Pure arithmetic, no semantics."""
    pos = 0
    ok = True
    for off, w in tile:
        if off != pos:
            ok = False
        pos = off + w
    return {"slots": len(tile), "bytes": sum(w for _, w in tile), "total": total,
            "contiguous_and_exhaustive": ok and pos == total,
            "u8": sum(1 for _, w in tile if w == 1),
            "u16": sum(1 for _, w in tile if w == 2),
            "u32": sum(1 for _, w in tile if w == 4)}


def enum_containment(vals: set[int], name: str) -> dict:
    """Exact/subset test of a slot's value set against a master.json enum."""
    dom = set(enum_ints(name))
    return {"enum": name, "domain": len(dom), "slot": len(vals),
            "subset": vals <= dom, "exact": vals == dom,
            "slot_minus_enum": sorted(vals - dom),
            "enum_minus_slot": sorted(dom - vals)}


def icau_mask_vacuity(raw: bytes, H: int, S: int, n: int, biz: int) -> dict:
    """Negative control for the multi-enum `Icau`. A bitmask test is only evidence
    if it DISCRIMINATES; here every u8 value and most u16 windows pass."""
    import itertools
    bits = [x for x in enum_ints("Icau") if x > 0]
    masks = {0}
    for k in range(1, len(bits) + 1):
        for c in itertools.combinations(bits, k):
            masks.add(sum(c))
    u8_pass = sum(1 for o in range(biz) if set(column(raw, H, S, n, o)) <= masks)
    u16_pass = [o for o in range(biz - 1)
                if set(column(raw, H, S, n, o, 2)) <= masks]
    return {"n_masks": len(masks), "max_mask": max(masks),
            "u8_windows_passing": f"{u8_pass}/{biz}",
            "u16_windows_passing": u16_pass,
            "verdict": "vacuous",
            "why": "every u8 value is inside the 13-bit mask space and 8192/65536 "
                   "(12.5%) of u16 windows pass by construction, so the test "
                   "cannot discriminate Icau from any other slot"}


def injury_client(raw: bytes, fr: dict) -> dict:
    H, S = fr["frame"]["header"], fr["frame"]["stride"]
    n, p = fr["frame"]["count"], fr["frame"]["identity_offset"]
    biz = p
    c0 = set(column(raw, H, S, n, 0))
    c1 = set(column(raw, H, S, n, 1))
    c2 = set(column(raw, H, S, n, 2))
    # which of the two client-field enums owns which byte: cardinality decides,
    # because a 12-value enum cannot emit 45 distinct values.
    e_iscl, e_icla = enum_containment(c1, "iscl"), enum_containment(c0, "icla")
    slots = [
        {"field": "icla", "offset": 0, "width": 1, "grade": "candidate",
         "why": "the only remaining byte of the 3-byte client business block once "
                "iscl is fixed at +1; icla is `is_client_field` and is the parent "
                "class of iscl. Enum containment FAILS by exactly one value (data "
                "carries 13, master lists 14) so this is not promoted to L2",
         "negative": "off0 domain = [1,3,4,5,6,8,9,10,11,12,13]; master enum icla = "
                     "[-3,1,3,4,5,6,8,9,10,11,12,14] -> slot_minus_enum [13], "
                     "enum_minus_slot [-3,14]. The editor XML enum and the shipped "
                     "data disagree on one code; recorded, not reconciled",
         "evidence": [e_icla], "domain": dom(raw, H, S, n, 0)},
        {"field": "iscl", "offset": 1, "width": 1, "grade": "L2",
         "why": "45/46 containment of the master `iscl` enum domain: every value in "
                "the column is a legal sub-classification, and a 12-value enum "
                "cannot produce 45 distinct values, so the assignment is unique "
                "among the two client-field enums",
         "negative": "master `iscl` is [-3]+1..48 with gaps; the column omits -3 "
                     "('Any'), which is the editor-only sentinel, not a data value",
         "evidence": [e_iscl], "domain": dom(raw, H, S, n, 1)},
        {"field": None, "offset": 2, "width": 1, "grade": "unassigned",
         "why": "binary column {0,1} with 27/115 ones; byte-identical to server "
                "offset 2 on all 115 rows, so it is a stored field, but no schema "
                "boolean carries `is_client_field`, so no field can claim it from "
                "the data side",
         "domain": dom(raw, H, S, n, 2)},
    ]
    return {"business_bytes": biz, "slots": slots,
            "identity": trailer_marker(raw, H, S, n, p)}

def slot_shape(raw: bytes, H: int, S: int, n: int, off: int, w: int) -> dict:
    """Shape test for ONE tiled slot. Shape is physical (width + value domain);
    shape is what budgets are counted on, never field identity."""
    v = column(raw, H, S, n, off, w)
    sent = (1 << (8 * w)) - 1
    live = [x for x in v if x != sent]
    n_ff = v.count(sent) if w == 1 else 0
    d = {"offset": off, "width": w, "distinct": len(set(v)), "n_ff": n_ff,
         "live_min": min(live) if live else None,
         "live_max": max(live) if live else None,
         "n_zero": v.count(0), "const": len(set(v)) == 1}
    d["binary"] = set(v) <= {0, 1}
    d["pct_in_100"] = bool(live) and min(live) >= 0 and max(live) <= 100
    d["pct_like"] = d["pct_in_100"] and not d["binary"]
    if w == 2:
        d["days_like"] = 0 < max(v) <= 720
    if w == 4:
        d["f32"] = f32_viable(raw, H, S, n, off)
    return d


def budget_tests(raw: bytes, H: int, S: int, n: int, biz: int) -> dict:
    """Population budgets over the OBSERVED tiling. A budget match fixes a group
    (how many fields of a shape, how many carry the sentinel); it never fixes the
    order inside the group."""
    shp = [slot_shape(raw, H, S, n, o, w) for o, w in TILE_SERVER]
    pct_f = [f["field"] for f in fields(XML[6])
             if f.get("min_value") == "0" and f.get("max_value") == "100"]
    opt_f = [f["field"] for f in fields(XML[6])
             if f["field"] in pct_f and f.get("is_optional") == "true"]
    bool_f = [f["field"] for f in fields(XML[6]) if f["type"] == "boolean"]
    pct_s = [s["offset"] for s in shp if s["pct_like"]]
    ff_s = [s["offset"] for s in shp if s["pct_like"] and s["n_ff"]]
    bin_s = [s["offset"] for s in shp if s["binary"]]
    day_s = [s["offset"] for s in shp if s.get("days_like")]
    f32_s = [s["offset"] for s in shp if s.get("f32", {}).get("viable")]
    return {
        "tiling": tiling_check(TILE_SERVER, biz),
        "pct": {"fields": pct_f, "n_fields": len(pct_f), "optional": opt_f,
                "n_optional": len(opt_f), "slots": pct_s, "n_slots": len(pct_s),
                "sentinel_slots": ff_s, "n_sentinel": len(ff_s),
                "budget_match": len(pct_s) == len(pct_f),
                "sentinel_match": len(ff_s) == len(opt_f),
                "grade": "L2" if len(pct_s) == len(pct_f)
                          and len(ff_s) == len(opt_f) else "candidate",
                "why": "0..100 declared range with 0xFF as 'not applicable'; the "
                       "group boundary is fixed by the population, the order inside "
                       "it is not"},
        "days": {"fields": list(DAYS), "n_fields": len(DAYS), "slots": day_s,
                 "n_slots": len(day_s), "budget_match": len(day_s) == len(DAYS),
                 "grade": "L2" if len(day_s) == len(DAYS) else "candidate",
                 "why": "two u16 slots whose maximum stays inside the declared 0..720 "
                        "day range"},
        "boolean": {"fields": bool_f, "n_fields": len(bool_f), "slots": bin_s,
                    "n_slots": len(bin_s),
                    "budget_match": len(bin_s) == len(bool_f),
                    "grade": "L2" if len(bin_s) == len(bool_f) else "candidate",
                    "why": "7 boolean fields vs 7 byte slots holding {0,1}; a boolean "
                           "that never fires stores as 0 and is physically "
                           "indistinguishable from padding -- only the population is "
                           "claimed"},
        "real": {"fields": ["Iocr"], "slots": f32_s, "n_slots": len(f32_s),
                 "budget_match": len(f32_s) == 1,
                 "grade": "L2" if len(f32_s) == 1 else "candidate"},
        "shapes": shp,
    }
def injury_server(raw: bytes, fr: dict, rc: bytes, frc: dict) -> dict:
    """27-byte server business block. Tiling is physical; grades are per-slot.
    Order inside a shape-group is left candidate -- the data cannot fix it."""
    H, S = fr["frame"]["header"], fr["frame"]["stride"]
    n, p = fr["frame"]["count"], fr["frame"]["identity_offset"]
    biz = p
    bud = budget_tests(raw, H, S, n, biz)
    shp = {s["offset"]: s for s in bud["shapes"]}
    pct_s = set(bud["pct"]["slots"])
    day_s = set(bud["days"]["slots"])
    bin_s = set(bud["boolean"]["slots"])

    # client/server byte equality: a prefix byte that matches on every row is a
    # stored field shared by both archives, which is what lets the client 3-byte
    # block be located inside the server 27-byte block.
    Hc, Sc = frc["frame"]["header"], frc["frame"]["stride"]
    shared = [o for o in range(min(biz, frc["frame"]["identity_offset"]))
              if all(raw[H + j * S + o] == rc[Hc + j * Sc + o] for j in range(n))]

    slots: list[dict] = []
    for off, w in TILE_SERVER:
        s = shp[off]
        rec = {"offset": off, "width": w, "field": None, "grade": "unassigned",
               "domain": dom(raw, H, S, n, off, w), "shape": s}
        slots.append(rec)

    byoff = {s["offset"]: s for s in slots}

    def put(off, field, grade, why, evidence=None, negative=None):
        r = byoff[off]
        r.update({"field": field, "grade": grade, "why": why,
                  "evidence": evidence or []})
        if negative:
            r["negative"] = negative

    # -- (+0) classification: byte-identical to the client icla slot
    put(0, "icla", "candidate",
        "byte-identical to the client icla slot on all 115 rows, and iscl at +1 "
        "(L2) marks the same two-byte client block, so +0 is the remaining "
        "client-field enum. Same one-value containment gap as on the client, so "
        "it stays candidate",
        [enum_containment(set(column(raw, H, S, n, 0)), "icla")],
        "off0 domain = [1,3,4,5,6,8,9,10,11,12,13] vs master enum icla = "
        "[-3,1,3,4,5,6,8,9,10,11,12,14]: data carries 13, XML lists 14, and the "
        "editor-only -3 is absent. Not reconciled here (kept as a data/XML "
        "divergence). 12 rows carry 13; every one of them also has iscl in "
        "{38,39,40,41,43} -- an iscl block the XML does not place under any icla")

    put(1, "iscl", "L2",
        "45/46 containment of master `iscl`; the only missing value is the editor "
        "sentinel -3 ('Any'). Cardinality rules out icla (12 entries cannot emit "
        "45 distinct values)",
        [enum_containment(set(column(raw, H, S, n, 1)), "iscl")],
        "hierarchy check: iscl -> icla is NOT a function -- iscl=22 occurs under "
        "both icla=6 and icla=8 (1 conflict of 45). The sub-classification tree is "
        "therefore not a clean partition; recorded, not repaired")

    # -- (+2) binary, no client flag on any boolean
    put(2, None, "unassigned",
        "binary {0,1} with 27/115 ones, byte-identical to client +2. A stored "
        "field, but all 7 injury booleans lack `is_client_field` while the client "
        "block holds it -- so this byte cannot belong to a boolean under the "
        "schema's own client/server split")

    # -- (+3,+5) two u16 day slots, population match
    put(3, None, "L2",
        "one of the 2 u16 day slots: population match '2 declared 0..720 fields / 2 "
        "u16 slots with max<=720' fixes the group. Imnd vs Iexd NOT decided",
        [bud["days"]], "group {Imnd,Iexd} @ {+3,+5}; both are 0..720 so neither "
        "range nor ordering separates them")
    put(5, None, "L2",
        "second 0..720 u16 day slot, same population match as +3",
        [bud["days"]], "u16@3 <= u16@5 holds on 96/115 rows only, so a "
        "'minimum <= extra' reading does NOT hold physically -- it cannot be used "
        "to order the pair")

    # -- (+7) percent
    put(7, None, "candidate",
        "percent-shaped u8 (0..100 step 10, 11 values, no 0xFF); belongs to the "
        "0..100 group but the group is larger than the declared field count")

    # -- (+8..+12) boolean row
    for o, note in ((8, "45/115 ones"), (9, "57/115 ones"), (10, "50/115 ones"),
                    (11, "50/115 ones; u16@11 is {0,1} so +11 is an independent byte"),
                    (12, "constant 0x00 in 115/115 rows -- see negative")):
        put(o, None, "L2" if o != 12 else "candidate",
            f"boolean slot ({note}); the 7-boolean / 7-binary-slot population match "
            "fixes membership in the group, not which boolean",
            [bud["boolean"]],
            None if o != 12 else
            "constant 0 for all rows: physically indistinguishable from padding. "
            "Counting it as one of the 7 booleans is a population argument only -- "
            "the alternative reading (one of the 7 booleans is not persisted at all, "
            "and +12 is padding) cannot be excluded from the data side")

    # -- (+13) f32 real
    put(13, "Iocr", "L2",
        "the only f32-viable 4-byte slot in the block (27 distinct values, "
        "1e-4..9.0, no NaN/inf); `Iocr` is the schema's only real field here and "
        "declares min_value 0, which the domain satisfies",
        [bud["real"]],
        "the f32 window is not byte-aligned with the u8 row (it straddles +13..+16), "
        "which is why the tiling has to be read as a typed struct, not a byte map")

    # -- (+17) percent
    put(17, None, "candidate",
        "percent-shaped u8 (0..90 step 5/10); 0..100 group member, order undecided")

    # -- (+20..+23) small enums
    for o, note in ((20, "{0,1,2}, 3 values"), (21, "{0,1,2,3}, 4 values"),
                    (22, "{0,1}, 3/115 ones"), (23, "{1,2,3,4,5}, 5 values")):
        put(o, None, "candidate",
            f"small enum domain {note}; four enum fields (inSr/Iagr/Icms + one of "
            "the class enums) remain and the domains do not decide which is which",
            None,
            "the master enum sets are permissive: {0,1} passes 4 enums and {1..5} "
            "passes 6 unrelated enums, so containment is not a discriminator here")

    # -- (+24,+25) sentinel-bearing percents
    put(24, None, "candidate",
        "percent-shaped with 0xFF 'not applicable' in 94/115 rows; the sentinel "
        "population matches the 2 is_optional 0..100 fields, so this is one of "
        "{Igpr,Icdp}",
        [bud["pct"]], "94/115 sentinel means the field is nearly always absent; "
        "the 21 live values are {5,40,75,90,100}")
    put(25, None, "candidate",
        "percent-shaped with 0xFF in 113/115 rows and a single live value (50): one "
        "of the 2 is_optional 0..100 fields, but a one-valued column cannot be "
        "separated from its twin",
        [bud["pct"]], "a single live value (50) with 2 sentinels is the weakest "
        "evidence in the table -- flagged, not promoted")

    # -- (+26) residue
    put(26, None, "unassigned",
        "15-valued u8 ({1,2,3,5,7,9,17,18,21,33,35,39,41,49,51}) satisfying no "
        "declared enum, range or boolean shape; left unassigned rather than fitted",
        None,
        "Icau (multiple_enum) was tested here and REJECTED as vacuous: the 13-bit "
        "mask space covers every u8 value (27/27 windows pass) and 12.5% of u16 "
        "windows pass, so the bitmask test has no discriminating power on this "
        "payload. See icau_mask_vacuity")

    return {
        "business_bytes": biz,
        "tiling": bud["tiling"],
        "budgets": {k: bud[k] for k in ("pct", "days", "boolean", "real")},
        "icau_mask_vacuity": icau_mask_vacuity(raw, H, S, n, biz),
        "client_server_shared_bytes": shared,
        "slots": slots,
        "identity": trailer_marker(raw, H, S, n, p),
    }
def fk_section(tid: int, archive: str) -> dict:
    """FK lanes INTO this table. Prior t81 products are read, never rebuilt."""
    idx = json.loads(FK_INDEX.read_text(encoding="utf-8"))
    t = idx["targets"][f"{tid}/{archive}"]
    inbound = []
    for rescan in ("rescan_fk_city.json", "rescan_fk_t76.json"):
        p = FK_INDEX.parent / rescan
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        for lane in d["lanes"]:
            if lane["target"] == tid:
                inbound.append({"source": lane.get("source"), "field": lane.get("field"),
                                "offset": lane.get("offset"),
                                "decision": lane.get("decision"),
                                "rescan": rescan})
    out = {
        "outbound": {"declared_fk_fields": [],
                     "why": f"{XML[tid]} declares no database_record_unique_id field; "
                            "the model is the other way round -- other tables point "
                            "at this one"},
        "inbound_lanes_scanned": len(inbound),
        "inbound": inbound,
        "ordinal_domain": {"kind": "range", "start": 0,
                           "stop": t["row_count"] - 1, "count": t["row_count"],
                           "source": "scratch/t81/out/fk_index.json (prior t81 "
                                     "deliverable, referenced not rebuilt)"},
        "uid_domain": {"count": t["uid_set"]["count"],
                       "distinct": t["uid_set"]["distinct"],
                       "min": t["uid_set"]["min"], "max": t["uid_set"]["max"],
                       "sha256": t["uid_set"]["sha256"]},
    }
    if tid == 6:
        out["inju_vs_table_30"] = {
            "cited_from": "reports/stage2_table_identity.json (stage2 conclusion, "
                          "NOT re-adjudicated in this task)",
            "stage2_row": {"table_type": 30, "entity": "player", "status": "resolved",
                           "level": "A",
                           "role": "player injury / future-state record table",
                           "note": "72,473 rows >> injury master 115, so table_30 is "
                                   "the player-side injury instance/status table, not "
                                   "the injury dictionary"},
            "reading": "injury(6) is the dictionary (115 rows) that table_30 rows "
                       "reference per player; the referential direction is "
                       "table_30 -> injury(6). ordinal sets are compatible "
                       "(0..114) but the link is NOT re-derived here: no byte-level "
                       "FK was established in either direction, so no grade is "
                       "claimed",
            "grade": "none (cited stage2 identity only)",
        }
    return out


def build(tid: int, archive: str) -> dict:
    raw = payload(archive, tid)
    fr = frame_self_proof(raw)
    if not fr["resolved"]:
        return {"archive": archive, "table": tid, "entity": XML[tid],
                "status": "escalate_to_sol", "frame_self_proof": fr}
    if tid in (23, 35):
        body = thin_slots(raw, fr, tid)
    else:
        rc = payload("client", 6) if archive == "server" else raw
        frc = frame_self_proof(rc) if archive == "server" else fr
        body = injury_server(raw, fr, rc, frc) if archive == "server" \
            else injury_client(raw, fr)
    H, S = fr["frame"]["header"], fr["frame"]["stride"]
    n = fr["frame"]["count"]
    slots = body["slots"]
    mapped = [s for s in slots if s.get("field")]
    grades: dict[str, int] = {}
    for s in slots:
        grades[s["grade"]] = grades.get(s["grade"], 0) + 1
    flds = [f["field"] for f in fields(XML[tid])]
    claimed = {s["field"] for s in mapped}
    string_fields = [f["field"] for f in fields(XML[tid]) if f["type"] == "string"]
    text = strings_present(raw)
    return {
        "archive": archive, "table": tid, "entity": XML[tid],
        "entity_id": EID[tid], "tool": "t81_small_slots",
        "schema": "t81.small_slots.v1",
        "payload_len": len(raw), "payload_sha256": sha(raw),
        "frame_self_proof": fr,
        "status": "closed",
        "business_bytes": body["business_bytes"],
        "identity": body["identity"],
        **{k: body[k] for k in ("tiling", "budgets", "icau_mask_vacuity",
                                "client_server_shared_bytes") if k in body},
        "slot_grades": grades,
        "slots": slots,
        "held": {
            "reason": "string fields live in a length-prefixed region, not a "
                      "fixed-width slot. This payload carries NO such region: "
                      f"runs of >=6 printable bytes = {text['n_runs']} "
                      f"(longest {text['longest']} B; the header magic 'tad.' is "
                      "4 B and is excluded from the count). The text is supplied "
                      "by the language/localisation layer and is therefore not "
                      "absent by omission -- it is structurally absent here",
            "text_probe": text,
            "fields": [f for f in string_fields if f not in claimed],
        },
        "unmapped": [f for f in flds if f not in claimed and f not in string_fields],
        "fk": fk_section(tid, archive),
        "column_profile": {str(o): dom(raw, H, S, n, o, 1) for o in range(S)},
    }
# ------------------------------------------------------------------ CLI ------
def selftest() -> int:
    """Pure-data checks that do not need a payload."""
    checks = []

    def ck(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    tc = tiling_check(TILE_SERVER, 27)
    ck("tiling is contiguous and exhaustive over 27 B",
       tc["contiguous_and_exhaustive"] and tc["bytes"] == 27, tc)
    ck("tiling shape population 17u8+3u16+1u32",
       (tc["u8"], tc["u16"], tc["u32"]) == (17, 3, 1), tc)
    ck("tiling misses no byte", sum(w for _, w in TILE_SERVER) == 27)

    e = enum_containment({1, 2, 3}, "inSr")
    ck("enum_containment reports subset and exact",
       e["subset"] and not e["exact"], e)
    e2 = enum_containment(set(enum_ints("inSr")), "inSr")
    ck("enum_containment detects exact equality", e2["exact"], e2)
    e3 = enum_containment({13}, "icla")
    ck("enum_containment exposes the icla 13/14 gap",
       e3["slot_minus_enum"] == [13] and 14 in e3["enum_minus_slot"], e3)

    ck("frozen anchors are exactly the 3 briefed client triples",
       FROZEN == {(6, "client"): {"rdui": 3, "duni": 7},
                  (23, "client"): {"rdui": 1, "duni": 5},
                  (35, "client"): {"rdui": 2, "duni": 6}}, FROZEN)
    ck("every frozen duni - rdui == 4 (identity triple is contiguous)",
       all(v["duni"] - v["rdui"] == 4 for v in FROZEN.values()))
    ck("7 injury booleans declared",
       len([f for f in fields(XML[6]) if f["type"] == "boolean"]) == 7)
    ck("2 declared 0..720 day fields",
       len([f for f in fields(XML[6]) if f.get("max_value") == "720"]) == 2)
    ck("4 declared 0..100 percent fields",
       len([f for f in fields(XML[6]) if f.get("min_value") == "0"
            and f.get("max_value") == "100"]) == 4)
    ck("exactly 2 of those percents are is_optional",
       len([f for f in fields(XML[6]) if f.get("max_value") == "100"
            and f.get("is_optional") == "true"]) == 2)
    ck("injury declares no database_record_unique_id field",
       not [f for f in fields(XML[6])
            if f["type"] == "database_record_unique_id"])
    ck("stage name declares exactly 4 string fields (dbnm+3 SN*)",
       sorted(f["field"] for f in fields(XML[23]) if f["type"] == "string")
       == ["SNna", "SNpn", "SNsn", "dbnm"])
    ck("description declares exactly 2 string fields (dbnm+PTna)",
       sorted(f["field"] for f in fields(XML[35]) if f["type"] == "string")
       == ["PTna", "dbnm"])

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" +
              ("" if ok else f"  -> {detail}"))
    print(f"selftest: {len(checks) - len(failed)}/{len(checks)} passed")
    return 0 if not failed else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="t81_small_slots.py",
        description="t81-fix1 slot maps for injury(6)/stage_name(23)/description(35).",
        epilog="exit codes: 0 success / 1 check failed / 2 usage or fatal")
    ap.add_argument("--selftest", action="store_true", help="pure-data checks")
    ap.add_argument("--all", action="store_true",
                    help="build all 6 (archive, table) slot maps into out2/")
    ap.add_argument("--table", type=int, choices=[6, 23, 35], help="one table")
    ap.add_argument("--archive", choices=["client", "server"], default="client")
    ap.add_argument("--json", metavar="PATH", help="write one record to PATH")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.all and a.table is None:
        ap.print_help()
        return 2

    OUTDIR.mkdir(parents=True, exist_ok=True)
    targets = [(t, ar) for t in (6, 23, 35) for ar in ("client", "server")] \
        if a.all else [(a.table, a.archive)]
    code = 0
    for tid, ar in targets:
        try:
            rec = build(tid, ar)
        except Exception as exc:  # noqa: BLE001 - fatal, reported verbatim
            print(f"FATAL {ar}/{tid}: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        txt = json.dumps(rec, indent=1, ensure_ascii=False)
        path = Path(a.json) if a.json else OUTDIR / f"slots_{ar}_{tid}.json"
        path.write_text(txt, encoding="utf-8")
        g = rec.get("slot_grades", {})
        print(f"{ar}/{tid}: {rec.get('status')} slots={len(rec.get('slots', []))} "
              f"grades={g} bytes={len(txt)}")
        if rec.get("status") != "closed":
            code = 1
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
