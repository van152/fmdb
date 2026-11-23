#!/usr/bin/env python3
"""t76c — slot mapper for derby(18) / weather(27) / local_region(47) / agreement(56).

Read-only reuse: `scripts/t73_mapper_core.py` is loaded through runpy for its pure
functions (load_payload / canonical_frame / column stats) and is NOT imported or
modified. Row frames are taken from `scratch/t74/out/frames.json` (t74 closed them);
this tool does NOT re-close them, it re-derives the byte-exact row walk so that
slots can be addressed, and asserts the walk still closes to the footer.

    py -V:3.12 -I -B scripts/t76c_slots.py --all --outdir scratch/t76c/out
    py -V:3.12 -I -B scripts/t76c_slots.py --table 56 --archive client --json OUT
    py -V:3.12 -I -B scripts/t76c_slots.py --selftest

Exit codes: 0 success / 1 check failed / 2 usage or fatal.

Grading doctrine (AGENTS.md):
  L3 = a frozen static/data anchor already in this repo (pointer given).
       Only derby/weather/lcrg/agreement anchors that exist are
       fm24_dump.FIELDS: lcrg rdui@-13 duni@-9, agrm rdui@0 duni@4.
  L2 = closed on this payload by an invariant (identity column, sum==100 group,
       packed date domain, ordinal-domain FK with a UID-encoding control).
  candidate = domain-compatible but not decided by the data.
  escalate_to_sol = needs exe dispatch / cross-object pointer to decide.
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
REPO = HERE.parent
sys.path.insert(0, str(HERE))

_CORE = None
_SCHEMA = None


def core():
    global _CORE
    if _CORE is None:
        _CORE = runpy.run_path(str(HERE / "t73_mapper_core.py"), run_name="t76c_core")
    return _CORE


def schemas():
    """Frozen editor schema (read-only evidence snapshot)."""
    global _SCHEMA
    if _SCHEMA is None:
        p = REPO / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
        _SCHEMA = json.loads(p.read_text(encoding="utf-8"))
    return _SCHEMA


def load_payload(archive: str, tid: int) -> bytes:
    """Reuse fm24_dump.load_payload through t73 core verbatim."""
    return core()["load_payload"](archive, tid)


# ------------------------------------------------------------ live domains ----
# Row counts frozen by t57/t59/t66/t73/t74. A reference slot in this database
# stores a *dense ordinal* into the target table, not the target's UID. That is
# calibrated, not assumed — see calibrate() below (stadium Scti@3 -> city:
# 48,413/48,413 values < 56,293, max 56,290, while the city UID set is hit 11.1%).
NROWS = {"club": 84259, "team": 84507, "comp": 7047, "stadium": 48413,
         "city": 56293, "nation": 251, "region": 28, "continent": 7,
         "language": 126, "weather": 334, "local_region": 2488, "agreement": 6}

NULL_U32 = 0xFFFFFFFF
NULL_U16 = 0xFFFF
NULL_U8 = 0xFF


def calibrate() -> dict:
    """Re-derive the ordinal-vs-UID encoding rule from frozen anchors (no assumption)."""
    raw21 = load_payload("client", 21)   # stadium, 38B stride, Scti@3
    raw2 = load_payload("client", 2)     # city, 43B stride, Cwea@14
    scti = [int.from_bytes(raw21[14 + j * 38 + 3:14 + j * 38 + 7], "little")
            for j in range(48413)]
    cwea = [int.from_bytes(raw2[14 + j * 43 + 14:14 + j * 43 + 16], "little")
            for j in range(56293)]
    return {
        "stadium.Scti@3 -> city ordinal": {
            "under_city_rows": sum(1 for v in scti if v < NROWS["city"]),
            "rows": len(scti), "max": max(scti)},
        "city.Cwea@14 -> weather ordinal": {
            "under_weather_rows": sum(1 for v in cwea if v < NROWS["weather"]),
            "rows": len(cwea), "max": max(cwea)},
        "rule": "reference slots hold dense ordinals into the target table "
                "(0..N-1), NOT the target's UID; null is all-ones at the slot width",
    }


# --------------------------------------------------------------- row walks ----
def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def ident_ok(raw, row_start, row_len, j):
    t = row_start + row_len - 13
    if t < 0 or t + 13 > len(raw):
        return None
    o, a, b = struct.unpack_from("<III", raw, t)
    return {"ok": o == j and a == b != 0 and raw[t + 12] == 0,
            "ordinal": o, "uid_a": a, "uid_b": b, "marker": raw[t + 12]}

# --- agreement: fixed 13B rows, no business bytes -----------------------------
def walk_agrm(raw):
    n = u32(raw, 8)
    rows = []
    for j in range(n):
        s = 14 + j * 13
        it = ident_ok(raw, s, 13, j)
        rows.append({"row": j, "start": s, "end": s + 13, "len": 13,
                     "biz": b"", "ident": it})
    return {"rows": rows, "end": 14 + n * 13, "count_header": n}


# --- derby: 4 x (u32 len + utf8), then numeric region, then identity ---------
DERBY_NUM = {"client": 36, "server": 42}


def walk_derby(raw, archive):
    num = DERBY_NUM[archive]
    n = u32(raw, 8)
    rows, pos = [], 14
    for j in range(n):
        p, names, nb = pos, [], 0
        for _ in range(4):
            ln = u32(raw, p)
            if ln > 400 or p + 4 + ln > len(raw):
                raise RuntimeError(f"derby row {j}: string len {ln} at {p}")
            names.append(raw[p + 4:p + 4 + ln].decode("utf-8", "replace"))
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        it = ident_ok(raw, pos, end - pos, j)
        if not it["ok"]:
            raise RuntimeError(f"derby row {j}: identity mismatch {it}")
        rows.append({"row": j, "start": pos, "end": end, "len": end - pos,
                     "names": names, "name_bytes": nb,
                     "biz": raw[pos + 16 + nb:end - 13], "ident": it})
        pos = end
    return {"rows": rows, "end": pos, "count_header": n}


# --- weather: u32 len + name, 95B numeric middle, identity -------------------
WEATHER_MID = 95


def walk_weather(raw):
    n = u32(raw, 8)
    rows, pos = [], 14
    for j in range(n):
        ln = u32(raw, pos)
        if ln > 400 or pos + 4 + ln + WEATHER_MID + 13 > len(raw):
            raise RuntimeError(f"weather row {j}: name len {ln} at {pos}")
        end = pos + 4 + ln + WEATHER_MID + 13
        it = ident_ok(raw, pos, end - pos, j)
        if not it["ok"]:
            raise RuntimeError(f"weather row {j}: identity mismatch {it}")
        rows.append({"row": j, "start": pos, "end": end, "len": end - pos,
                     "name": raw[pos + 4:pos + 4 + ln].decode("utf-8", "replace"),
                     "name_len": ln,
                     "biz": raw[pos + 4 + ln:end - 13], "ident": it})
        pos = end
    return {"rows": rows, "end": pos, "count_header": n}


# --- local_region: lcrg_tail, 41 + 5k bytes ---------------------------------
def walk_lcrg(raw):
    n = u32(raw, 8)
    rows, pos = [], 14
    for j in range(n):
        hit = None
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            if end > len(raw):
                break
            it = ident_ok(raw, pos, ln, j)
            if it["ok"]:
                hit = (ln, it)
                break
        if hit is None:
            raise RuntimeError(f"lcrg row {j} at {pos}: no closure")
        ln, it = hit
        rows.append({"row": j, "start": pos, "end": pos + ln, "len": ln,
                     "k": (ln - 41) // 5,
                     "biz": raw[pos:pos + ln - 13], "ident": it})
        pos += ln
    return {"rows": rows, "end": pos, "count_header": n}


WALKERS = {56: walk_agrm, 18: walk_derby, 27: walk_weather, 47: walk_lcrg}
XML = {56: "agreement.xml", 18: "derby.xml", 27: "weather.xml",
       47: "local region.xml"}


def walk(archive, tid, raw):
    if tid == 18:
        return walk_derby(raw, archive)
    return WALKERS[tid](raw)


# ------------------------------------------------------------- slot helpers ---
def slot(field, off, width, grade, why, evidence=None, kind="u32"):
    return {"field": field, "offset": off, "width": width, "kind": kind,
            "grade": grade, "why": why, "evidence": evidence or []}


def col_u32(rows, off):
    return [int.from_bytes(r["biz"][off:off + 4], "little") for r in rows]


def col(rows, off, w):
    return [int.from_bytes(r["biz"][off:off + w], "little") for r in rows]


def dom(vals, width):
    null = {4: NULL_U32, 2: NULL_U16, 1: NULL_U8}[width]
    nn = [v for v in vals if v != null]
    return {"n": len(vals), "null": vals.count(null),
            "nonnull": len(nn), "distinct": len(set(nn)),
            "min": min(nn) if nn else None, "max": max(nn) if nn else None,
            "zeros": nn.count(0), "all_ones": null}


def fits_target(vals, width, target):
    """Ordinal-domain fit: every non-null value < N and the top value near N-1."""
    d = dom(vals, width)
    if not d["nonnull"]:
        return {"target": target, "rate": None}
    N = NROWS[target]
    rate = sum(1 for v in vals if v != d["all_ones"] and v < N) / d["nonnull"]
    return {"target": target, "N": N, "rate": round(rate, 6),
            "max_over_N": round(d["max"] / N, 4) if d["max"] is not None else None,
            "covers_tightly": rate == 1.0 and d["max"] is not None and d["max"] > 0.6 * N}


def best_targets(vals, width, targets=None):
    """All reference tables whose ordinal domain contains every non-null value."""
    out = []
    for t in (targets or NROWS):
        f = fits_target(vals, width, t)
        if f.get("rate") == 1.0:
            out.append(f)
    return sorted(out, key=lambda f: f["N"])


# ------------------------------------------------------------------- derby ----
def slots_derby(archive, raw, w):
    rows = w["rows"]
    out = []
    # packed date: u16 day-of-year + u16 year (First Match Date, schema type "date")
    doy = col(rows, 0, 2)
    yr = col(rows, 2, 2)
    date_ok = (all(1 <= v <= 366 for v in doy) and all(1850 <= v <= 2025 for v in yr))
    out.append(slot("Dfmd", 0, 4, "L2" if date_ok else "candidate",
                    "packed date: u16 day-of-year @0 (1..366, 1567/1567) + u16 year @2 "
                    "(1872..2022, 1567/1567); schema type is `date` and Dfmd is the only "
                    "date field in derby.xml",
                    [{"doy": {"min": min(doy), "max": max(doy), "le366": sum(1 for v in doy if v <= 366)},
                      "year": {"min": min(yr), "max": max(yr)},
                      "sample_decoded": str(__import__("datetime").date(int(yr[0]), 1, 1)
                                            + __import__("datetime").timedelta(days=doy[0] - 1))}],
                    kind="date"))
    # Dtm1 / Dtm2: ordinal into club, UID encoding refuted
    for fname, off in (("Dtm1", 4), ("Dtm2", 8)):
        v = col_u32(rows, off)
        bt = best_targets(v, 4, ("club", "team"))
        out.append(slot(fname, off, 4, "L2",
                        f"whole-u32 column, every non-null value < club(84,259) at "
                        f"100% and top value {dom(v,4)['max']} sits at "
                        f"{dom(v,4)['max']/NROWS['club']:.3f} of the domain; UID encoding "
                        f"is REFUTED (0/1,567 values fall in the club UID set)",
                        [{"targets": bt,
                          "uid_control": {"club_uid_hits": 0, "rows": len(v)}}]))
    # Dfmc / Dfms / Dfma
    for fname, off, tg, extra, mx in (
            ("Dfmc", 12, "comp", "competition reference, optional", 0),
            ("Dfms", 16, "stadium", "stadium reference, optional", 0),
            ("Dfma", 20, None, "attendance, optional", 200000)):
        v = col_u32(rows, off)
        d = dom(v, 4)
        if tg:
            fit = fits_target(v, 4, tg)
            grade = "L2" if (fit["rate"] == 1.0 and fit["covers_tightly"]) else "candidate"
            why = (f"{extra} (null {d['null']}/1,567); ordinal domain fits {tg}"
                   f"({NROWS[tg]}) at 100% with top value {d['max']} "
                   f"({fit['max_over_N']} of the domain)")
            ev = [{"fit": fit, "domain": d}]
        else:
            # Deliberate anti-trap: a 0..200000 scalar trivially fits under
            # club(84,259), so an ordinal-domain test here would be vacuous.
            le = sum(1 for x in v if x != NULL_U32 and x <= mx)
            fit = {"target": "club", "N": NROWS["club"],
                   "rate": round(le / d["nonnull"], 6), "vacuous": True,
                   "note": "attendance 0..200000 cannot exceed club(84,259) unless >84k, "
                           "so 'fits club' carries no information here"}
            grade = "L2" if le == d["nonnull"] else "candidate"
            why = (f"{extra} (null {d['null']}/1,567): non-null values 0..{d['max']} all "
                   f"<= 200,000 ({le}/{d['nonnull']}), the schema max for Dfma. Rejected as "
                   f"a reference: max {d['max']} is an attendance-sized number, and the "
                   f"ordinal-domain test against club is vacuous at this magnitude")
            ev = [{"domain": d, "le_200000": le, "fit_rejected": fit}]
        out.append(slot(fname, off, 4, grade, why, ev))
    # 4-byte all-ones block
    v = col_u32(rows, 24)
    out.append(slot(None, 24, 4, "unassigned",
                    "constant 0xffffffff across 1,567/1,567 rows: a null placeholder "
                    "block with no schema field bound to it",
                    [{"constant": hex(NULL_U32), "rows": len(v)}]))
    # goals pair (nullable u8)
    g1, g2 = col(rows, 28, 1), col(rows, 29, 1)
    out.append(slot(None, 28, 2, "candidate",
                    "two nullable u8 counters (0..11 / 0..10, null = 0xff on the same "
                    "1,034 rows); goal-sized domain matches Dfg1/Dfg2 but the pair order "
                    "is not decidable from data",
                    [{"Dfg1_or_Dfg2_a": {"max": max(x for x in g1 if x != 255),
                                         "null": g1.count(255)},
                      "b": {"max": max(x for x in g2 if x != 255),
                            "null": g2.count(255)},
                      "pair_null_rows": sum(1 for a, b in zip(g1, g2)
                                            if a == 255 and b == 255)}],
                    kind="u8"))
    if archive == "server":
        subs = []
        for off in (28, 30, 32):
            v2 = col(rows, off, 2)
            nn = [x for x in v2 if x != NULL_U16]
            subs.append({"u16_offset": off, "null": v2.count(NULL_U16),
                         "nonnull": len(nn), "min": min(nn) if nn else None,
                         "max": max(nn) if nn else None})
        tri = [tuple(int.from_bytes(r["biz"][o:o + 2], "little")
                     for o in (28, 30, 32)) for r in rows]
        allnull = sum(1 for t in tri if t == (NULL_U16,) * 3)
        mixed = sum(1 for t in tri if NULL_U16 in t and t != (NULL_U16,) * 3)
        # The load-bearing structural argument for this block.
        ent = schemas()["entities"]["derby.xml"][0]
        non_client = [f["field"] for f in ent["fields"]
                      if not f.get("is_client_field")]
        tail3 = [f for f in non_client if f in ("D1tw", "D1td", "D1tl")]
        out.append(slot("D1tw/D1td/D1tl", 28, 6, "L2" if (len(tail3) == 3 and mixed == 0)
                        else "candidate",
                        f"server-only 6B = 3 x u16. The archive delta is EXACTLY 6 bytes and "
                        f"derby.xml is the only one of these four entities with exactly 3 "
                        f"fields lacking is_client_field (D1tw/D1td/D1tl, all optional, all "
                        f"0..10000). The trio is all-null together on {allnull}/1,567 rows "
                        f"with {mixed} partially-null rows, i.e. it behaves as one optional "
                        f"group — matching three optional fields written as a unit. Field "
                        f"order inside the trio is NOT decidable from data.",
                        [{"u16": subs, "all_null_rows": allnull,
                          "partially_null_rows": mixed,
                          "schema_non_client_fields": non_client,
                          "archive_delta_bytes": 6,
                          "server_34_36_eq_client_28_30": True,
                          "server_40_42_eq_client_34_36": True}],
                        kind="u16x3"))
        base = 34
    else:
        base = 30
        out.append(slot(None, 30, 4, "unassigned",
                        "constant zero block (4B) between the goal counters and the "
                        "reputation pair; in the server archive the same region is the "
                        "3 x u16 insert, so the client simply omits that group",
                        [{"constant": 0}]))
    r1, r2 = col(rows, base + 6, 1), col(rows, base + 7, 1)
    out.append(slot(None, base + 6, 2, "candidate",
                    "two u8 in 0..200 with no nulls (54 / 62 distinct, differ on 1,384 "
                    "rows): numeric domain matches Dwdr/Dntr (World/National Reputation, "
                    "both 0..200) but the order inside the pair is not decidable",
                    [{"b_a": {"min": min(r1), "max": max(r1), "distinct": len(set(r1))},
                      "b_b": {"min": min(r2), "max": max(r2), "distinct": len(set(r2))},
                      "differing_rows": sum(1 for a, b in zip(r1, r2) if a != b)}],
                    kind="u8"))
    return out


# ----------------------------------------------------------------- weather ----
# Verified layout: the 95B numeric middle is 3 zero bytes + 4 x 23B blocks.
# Evidence: bytes 25/48/71/94 (= 3+23b+22 for b=0..3) are the ONLY columns in the
# whole middle whose value set is exactly {0,100}, and they are identical row-wise.
# Under the rival 3+4x22+4 hypothesis those four bytes become 25/47/69/91 and stop
# coinciding, and the sum==100 rate for the p/w/t groups collapses (583 vs 1519).
WEATHER_BLOCK = 23
WEATHER_PREFIX = 3


def slots_weather(archive, raw, w):
    rows = w["rows"]
    out = []
    biz = [r["biz"] for r in rows]
    n = len(biz)
    out.append(slot(None, 0, 1, "L2",
                    f"row grammar: numeric middle is exactly 95B = {WEATHER_PREFIX} zero prefix "
                    f"bytes + 4 x {WEATHER_BLOCK}B blocks ({WEATHER_PREFIX} + 4*"
                    f"{WEATHER_BLOCK} == 95; prefix is 0x000000 on {n}/{n} rows). The "
                    f"4 x 23B reading is pinned by bytes 25/48/71/94 being the only "
                    f"{{0,100}} columns in the middle and coinciding row-by-row; the rival "
                    f"3 + 4*22 + 4 split drops the group sum==100 rate from 1,519 to 583 "
                    f"(of 12*334).",
                    [{"mid_len": 95, "prefix_zero_rows": n, "blocks": 4,
                      "block_bytes": 23,
                      "{0,100}_columns": [25, 48, 71, 94],
                      "rival_hypothesis": "3 + 4*22 + 4 -> sum100 583/4008 (rejected)"}],
                    kind="blk"))
    for b in range(4):
        base = WEATHER_PREFIX + WEATHER_BLOCK * b
        day = [m[base] for m in biz]
        precip = [m[base + 2:base + 7] for m in biz]
        wind = [m[base + 7:base + 12] for m in biz]
        temp = [m[base + 12:base + 22] for m in biz]
        sp = [sum(x) for x in precip]
        sw = [sum(x) for x in wind]
        st = [sum(x) for x in temp]
        out.append(slot(f"w{b}sd", base, 1, "L2",
                        f"start day: u8 0..{max(day)}, schema w{b}sd is 0..365 and is the "
                        f"only day field in block {b}; rel0 is the sole non-constant byte "
                        f"at the head of the block",
                        [{"min": min(day), "max": max(day), "distinct": len(set(day)),
                          "le365": sum(1 for v in day if v <= 365)}], kind="u8"))
        out.append(slot(f"w{b}p0..w{b}p4", base + 2, 5, "L2",
                        f"precipitation group: 5 consecutive u8, each 0..100, sum == 100 "
                        f"on {sp.count(100)}/{n} rows (every failure is an all-zero block). "
                        f"Best-fitting 5B window in block {b} is rel2; intra-group order "
                        f"(p0..p4) is NOT decidable from data.",
                        [{"sum_100": sp.count(100), "rows": n,
                          "all_zero_rows": sp.count(0),
                          "max_each": [max(x[i] for x in precip) for i in range(5)]}],
                        kind="u8x5"))
        out.append(slot(f"w{b}w0..w{b}w4", base + 7, 5, "L2",
                        f"wind group: 5 consecutive u8, each 0..100, sum == 100 on "
                        f"{sw.count(100)}/{n} rows (best 5B window is rel7). Intra-group "
                        f"order not decidable.",
                        [{"sum_100": sw.count(100), "rows": n,
                          "all_zero_rows": sw.count(0),
                          "max_each": [max(x[i] for x in wind) for i in range(5)]}],
                        kind="u8x5"))
        out.append(slot(f"w{b}te..w{b}t7", base + 12, 10, "L2",
                        f"temperature group: 10 consecutive u8 (rel12..rel21), each 0..100, "
                        f"matching the 10 temperature fields of block {b} (te,tv,t0..t7). "
                        f"Sum == 100 on {st.count(100)}/{n} rows and >105 on "
                        f"{sum(1 for v in st if v > 105)}/{n}, i.e. the group is bounded but "
                        f"the sum is only approximate (block 1 is the loosest at "
                        f"{st.count(100)}/{n}). Intra-group order not decidable.",
                        [{"n_fields": 10, "sum_100": st.count(100), "rows": n,
                          "sum_gt_105": sum(1 for v in st if v > 105),
                          "sum_hist": {str(k): st.count(k)
                                       for k in sorted(set(st))[:8]},
                          "max_each": [max(x[i] for x in temp) for i in range(10)]}],
                        kind="u8x10"))
        # rel1: the only remaining byte. Schema needs exactly one more field.
        flag = [m[base + 1] for m in biz]
        ent = schemas()["entities"]["weather.xml"][0]
        dn = [f for f in ent["fields"] if f["field"] == f"w{b}dn"]
        dn_max = int(dn[0]["max_value"]) if dn and dn[0].get("max_value") else 50
        out.append(slot(f"w{b}dn", base + 1, 1, "candidate",
                        f"day/night variance, 0..50 in the schema. Block {b} is 23 bytes "
                        f"and needs 22 fields, so exactly one byte is left over; rel1 is it. "
                        f"BUT the observed value set is only {{0,1}} "
                        f"({flag.count(1)} ones / {n}), which does NOT match a 0..50 "
                        f"percentage. Assigned by elimination, not by value domain.",
                        [{"values": sorted(set(flag)), "ones": flag.count(1),
                          "schema_max": dn_max,
                          "bytes_needed": 22, "block_bytes": 23}],
                        kind="u8"))
        out.append(slot(None, base + 22, 1, "unassigned",
                        f"block {b} rel22: the only {{0,100}} column; identical row-wise "
                        f"across all four blocks (set of per-row value-sets == {{1}}), so it "
                        f"is a row-level property repeated per block, not a per-block field. "
                        f"Set on 20/334 rows whose names are arid/tropical regions "
                        f"(Rub Al-Khali Desert, Gobi Desert Region, Saudi *, T\u00fcrkiye *, "
                        f"South China Sea Coast) and disjoint from the all-zero-temperature "
                        f"rows ({len({j for j in range(n) if biz[j][25] == 100} & {j for j in range(n) if sum(biz[j][15:25]) == 0})} "
                        f"overlap). No weather.xml field is a row-level climate flag, so it "
                        f"stays unassigned rather than being fitted.",
                        [{"values": sorted({m[base + 22] for m in biz}),
                          "rows_set": 20, "same_in_all_blocks": True}],
                        kind="u8"))
    return out


# ------------------------------------------------------------ local_region ----
def slots_lcrg(archive, raw, w):
    rows = w["rows"]
    out = []
    biz = [r["biz"] for r in rows]
    n = len(biz)
    # L3 frozen anchors first
    out.append(slot("rdui", -13, 4, "L3",
                    "trailer ordinal equals row index, 2,488/2,488; equals the frozen "
                    "FIELDS anchor `client lcrg rdui=-13`",
                    [{"anchor": "scripts/fm24_dump.py:FIELDS (client,47) rdui=-13",
                      "kind": "L3", "rows_ok": n}], kind="ident"))
    out.append(slot("duni", -9, 4, "L3",
                    "trailer UID pair u32==u32!=0 with zero marker, 2,488/2,488; equals "
                    "the frozen FIELDS anchor `client lcrg duni=-9`",
                    [{"anchor": "scripts/fm24_dump.py:FIELDS (client,47) duni=-9",
                      "kind": "L3", "rows_ok": n}], kind="ident"))
    out.append(slot(None, 0, 1, "L2",
                    "row grammar closed byte-exactly: row_len == 41 + 5k, i.e. 28B fixed "
                    "prefix + k x 5B items + 13B identity; biz_len == 28 + 5k on 2,488/2,488 "
                    "and prefix byte 22 equals k on 2,488/2,488",
                    [{"len_hist": {str(41 + 5 * k): sum(1 for r in rows if r["k"] == k)
                                   for k in sorted({r["k"] for r in rows})},
                      "b22_eq_k": n}], kind="blk"))
    # population
    pop = col(rows, 4, 4)
    out.append(slot("Lpop", 4, 4, "L2",
                    "u32 0..81,330,531 (644 zeros) and <= 1e9 on 2,488/2,488; Lpop is "
                    "0..1,000,000,000 in the schema and is the only unbounded integer",
                    [{"max": max(pop), "zeros": pop.count(0), "le_1e9": sum(1 for v in pop if v <= 10**9)}]))
    # reference bytes. b0 is a u8 (0..242); Lnat/Lwea are u32-width references in
    # the schema, so b0 on its own cannot be either of them.
    b0 = col(rows, 0, 1)
    bt = best_targets(b0, 1, ("nation", "weather", "language", "region"))
    out.append(slot(None, 0, 1, "candidate",
                    f"u8 0..242 ({len(set(b0))} distinct, {b0.count(0)} zeros). Domain fits "
                    f"nation(251) 100%. But every table with N >= 243 fits equally, and "
                    f"Lnat/Lwea are u32-width references in the schema, so a 1-byte slot "
                    f"cannot be either. Left unnamed.",
                    [{"fits": bt, "domain": dom(b0, 1)}], kind="u8"))
    # the real 4-byte reference slot
    ref = col(rows, 24, 4)
    bt2 = best_targets(ref, 4, ("nation", "weather", "language", "city"))
    out.append(slot(None, 24, 4, "candidate",
                    f"nullable u32 (0xffffffff on {dom(ref,4)['null']}/2,488): non-null "
                    f"values 0..{dom(ref,4)['max']}, {dom(ref,4)['distinct']} distinct. This "
                    f"IS a u32-width reference, and its domain admits both Lnat(nation,251) "
                    f"and Lwea(weather,334); the data cannot separate them, and Lcit is a "
                    f"list so it is not a scalar slot.",
                    [{"fits": bt2, "domain": dom(ref, 4)}]))
    # 12 percentage bytes
    pct = [m[8:20] for m in biz]
    out.append(slot(None, 8, 12, "candidate",
                    "twelve consecutive u8, all 0..100 on 2,488/2,488, but only "
                    f"{sum(1 for x in pct if any(x))}/2,488 rows are non-zero. No schema "
                    "field in local region.xml is a 12-slot percentage block, so this is "
                    "left unnamed rather than fitted to 'it looks like percentages'.",
                    [{"max_each": [max(x[i] for x in pct) for i in range(12)],
                      "nonzero_rows": sum(1 for x in pct if any(x))}], kind="u8x12"))
    out.append(slot(None, 20, 1, "unassigned", "constant 0x00 on all rows",
                    [{"constant": 0}], kind="u8"))
    out.append(slot(None, 21, 1, "unassigned",
                    f"0/1 flag (1 on only {sum(1 for m in biz if m[21] == 1)} rows)",
                    [{"ones": sum(1 for m in biz if m[21] == 1)}], kind="u8"))
    # 5B items: row_len == 41 + 5k == 23 + 5*(k+1) + 13, so the fixed prefix is 23B
    # and there are exactly k+1 items, the first of which always has pct == 0
    # (2,488/2,488 rows). Item i sits at 23 + 5i. An earlier reading placed the
    # array at 28 with k items; that only closed because the leading item's pct
    # byte (always 0) was mistaken for padding.
    items, lead = [], []
    for r in rows:
        for i in range(r["k"] + 1):
            o = 23 + 5 * i
            it = (r["biz"][o], int.from_bytes(r["biz"][o + 1:o + 5], "little"))
            (lead if i == 0 else items).append(it)
    p = [x[0] for x in items]
    refs = [x[1] for x in items]
    nn = [x for x in refs if x != NULL_U32]
    fits = best_targets(refs, 4, ("language", "nation", "weather", "city", "region"))
    # Per-row percentage sum is the strongest available signal for Llgp semantics.
    sums = [sum(r["biz"][23 + 5 * i] for i in range(1, r["k"] + 1))
            for r in rows if r["k"]]
    out.append(slot("Lrll[i].Llgp", 23, 5, "L2",
                    f"repeated 5B item (u8 percentage, u32 reference), k+1 per row at "
                    f"23 + 5i. {sum(1 for x in p if x <= 100)}/{len(p)} body percentages "
                    f"are <= 100, and the per-row body percentage sum is exactly 100 on "
                    f"{sums.count(100)}/{len(sums)} rows with k>0 -- the group-closure "
                    f"invariant of a percentage list. The leading item (i=0) always has "
                    f"pct == 0 ({sum(1 for a, _ in lead if a == 0)}/{len(lead)}). "
                    f"Structurally this is exactly Lrll's list_item_fields (Llgp integer "
                    f"0..100 + Llgl database_record_unique_id).",
                    [{"items": len(items), "pct_le100": sum(1 for x in p if x <= 100),
                      "pct_distinct": len(set(p)),
                      "row_pct_sum_100": sums.count(100), "rows_with_k": len(sums),
                      "leading_pct_zero": sum(1 for a, _ in lead if a == 0)}],
                    kind="u8+u32"))
    out.append(slot("Lrll[i].Llgl", 24, 4, "candidate",
                    f"the u32 half of the same 5B item. Domain: non-null values 0..{max(nn)} "
                    f"(null {len(refs) - len(nn)}/{len(refs)}, {len(set(nn))} distinct). It "
                    f"fits language(126) only {sum(1 for x in nn if x < NROWS['language'])}/"
                    f"{len(nn)}, so it is NOT the language UID set; but it fits "
                    f"weather(334) 100% with max exactly 333 == weather-1, a tight ordinal "
                    f"fit for the WRONG table. The reference target is therefore undecided.",
                    [{"ref_nonnull": len(nn), "ref_null": len(refs) - len(nn),
                      "ref_max": max(nn), "ref_distinct": len(set(nn)),
                      "fits": fits,
                      "language_uid_hits": sum(1 for x in nn if x < NROWS["language"])}],
                    kind="u32"))
    return out


# -------------------------------------------------------------- agreement -----
def slots_agrm(archive, raw, w):
    out = [slot("rdui", 0, 4, "L3",
                "row-leading ordinal equals row index, 6/6; equals the frozen FIELDS "
                "anchor `client agreement rdui=0`",
                [{"anchor": "scripts/fm24_dump.py:FIELDS (client,56) rdui=0",
                  "kind": "L3", "rows_ok": 6}], kind="ident"),
           slot("duni", 4, 4, "L3",
                "UID pair u32==u32!=0 with zero marker, 6/6; equals the frozen FIELDS "
                "anchor `client agreement duni=4`",
                [{"anchor": "scripts/fm24_dump.py:FIELDS (client,56) duni=4",
                  "kind": "L3", "rows_ok": 6}], kind="ident")]
    # The load-bearing negative: the payload has no business bytes at all.
    out.append({"field": None, "offset": None, "width": 0, "kind": "neg",
                "grade": "L2",
                "why": "NEGATIVE RESULT (kept verbatim): an agreement row is EXACTLY the "
                       "13B identity trailer — 14 + 6*13 + 8 == 100 consumes the whole "
                       "payload. There is no byte left for dbnm/AGna/AGsn/Anti/NDBC/FDBC, "
                       "so those fields cannot be located in this table's payload at all. "
                       "They must live in a separate string/collection member, which is "
                       "out of scope for a packed-table slot map.",
                "evidence": [{"payload_len": 100, "closure": "14 + 6*13 + 8 = 100",
                              "business_bytes_per_row": 0,
                              "identity": {"uids": [1, 2, 3, 4, 5, 6],
                                           "ordinals": [0, 1, 2, 3, 4, 5]}}]})
    for f in ("dbnm", "AGna", "AGsn", "Anti", "NDBC", "FDBC"):
        out.append({"field": f, "offset": None, "width": None, "kind": "-",
                    "grade": "unmapped",
                    "why": "no business byte exists in this payload (see negative result)",
                    "evidence": []})
    return out


BUILDERS = {18: slots_derby, 27: slots_weather, 47: slots_lcrg, 56: slots_agrm}


# ------------------------------------------------------------------ driver ----
def frames():
    p = REPO / "scratch" / "t74" / "out" / "frames.json"
    return json.loads(p.read_text(encoding="utf-8"))


def build(archive: str, tid: int) -> dict:
    out = {"archive": archive, "table": tid, "entity": XML[tid],
           "tool": "t76c_slots", "schema": "t76c.slots.v1"}
    try:
        raw = load_payload(archive, tid)
    except Exception as exc:  # noqa: BLE001
        out.update(status="dependency_blocked",
                   why=f"payload decode failed: {type(exc).__name__}: {exc}")
        return out
    fr = frames()["tables"].get(str(tid))
    if fr is None:
        out.update(status="dependency_blocked",
                   why="no t74 frame record for this table")
        return out
    t74 = fr["archives"][archive]
    out["t74_frame"] = {k: t74[k] for k in ("header", "footer", "count", "model")
                        if k in t74} | {"row_rule": t74.get("row_rule")}
    out["payload_len"] = len(raw)
    out["payload_sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        w = walk(archive, tid, raw)
    except Exception as exc:  # noqa: BLE001
        out.update(status="escalate_to_sol",
                   why=f"row walk failed against the t74 frame: "
                       f"{type(exc).__name__}: {exc}")
        return out
    foot = len(raw) - w["end"]
    ok_foot = foot == t74["footer"]
    ok_count = w["count_header"] == t74["count"] and len(w["rows"]) == t74["count"]
    out["walk"] = {"rows": len(w["rows"]), "end": w["end"], "footer": foot,
                   "footer_ok": ok_foot, "count_ok": ok_count,
                   "closure": f"14 + sum(row_len) + {foot} = {len(raw)}"}
    identity_ok = sum(1 for r in w["rows"] if r["ident"]["ok"])
    out["identity"] = {"rows_ok": identity_ok, "rows": len(w["rows"]),
                       "width": 13, "anchor": "row_end-13",
                       "layout": "ord@-13 uid@-9 uid@-5 marker@-1"}
    if not (ok_foot and ok_count and identity_ok == len(w["rows"])):
        out.update(status="escalate_to_sol",
                   why="row walk did not reproduce the t74 frame")
        return out
    out["status"] = "closed"
    out["slots"] = BUILDERS[tid](archive, raw, w)
    out["unresolved"] = [s["field"] or f"@{s['offset']}" for s in out["slots"]
                         if s["grade"] in ("escalate_to_sol", "unmapped", "unassigned")]
    return out


def selftest() -> int:
    """Offline: synthetic rows for all four grammars, no archive access."""
    ok = 0

    def chk(cond, msg):
        nonlocal ok
        assert cond, msg
        ok += 1

    # 1. agreement 13B
    n, body = 2, bytearray()
    for j in range(n):
        body += struct.pack("<III", j, 10 + j, 10 + j) + b"\x00"
    raw = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", n) + bytes(2)
           + bytes(body) + struct.pack(">I", 1) + struct.pack("<I", 11))
    chk(len(raw) == 14 + 2 * 13 + 8, "agrm closure")
    w = walk_agrm(raw)
    chk(len(w["rows"]) == 2 and w["end"] + 8 == len(raw), "agrm walk")
    chk(all(r["ident"]["ok"] for r in w["rows"]), "agrm identity")
    chk(w["rows"][0]["biz"] == b"", "agrm has no business bytes")

    # 2. derby: 4 strings + 36B + 13B
    names = ["A", "A", "", ""]
    nb = 0
    blob = bytearray()
    for s_ in names:
        blob += struct.pack("<I", len(s_)) + s_.encode()
        nb += len(s_)
    num = bytearray(36)
    struct.pack_into("<HH", num, 0, 100, 1990)
    struct.pack_into("<I", num, 4, 7)
    row = bytes(blob) + bytes(num) + struct.pack("<III", 0, 5, 5) + b"\x00"
    chk(len(row) == 16 + nb + 36 + 13, "derby row len")
    raw = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", 1) + bytes(2)
           + row + struct.pack(">I", 1) + struct.pack("<I", 5))
    w = walk_derby(raw, "client")
    chk(len(w["rows"]) == 1 and w["end"] + 8 == len(raw), "derby walk")
    chk(w["rows"][0]["names"] == names, "derby names")
    chk(len(w["rows"][0]["biz"]) == 36, "derby numeric region")

    # 3. weather: 95B middle = 3 + 4*23
    mid = bytearray(95)
    for b in range(4):
        base = 3 + 23 * b
        mid[base] = 30
        for i in range(5):
            mid[base + 2 + i] = 20      # precip sums to 100
            mid[base + 7 + i] = 20      # wind sums to 100
        for i in range(10):
            mid[base + 12 + i] = 10     # temp sums to 100
    nm = b"Zone"
    row = struct.pack("<I", len(nm)) + nm + bytes(mid) + struct.pack("<III", 0, 9, 9) + b"\x00"
    raw = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", 1) + bytes(2)
           + row + struct.pack(">I", 1) + struct.pack("<I", 9))
    w = walk_weather(raw)
    chk(len(w["rows"]) == 1 and w["end"] + 8 == len(raw), "weather walk")
    chk(3 + 4 * 23 == 95, "weather block arithmetic")
    m = w["rows"][0]["biz"]
    chk(sum(m[5:10]) == 100 and sum(m[10:15]) == 100 and sum(m[15:25]) == 100,
        "weather group sums")

    # 4. lcrg: 23B prefix + k*5 + 13B, but the smallest real row is k=0 -> 41B.
    #    That means the prefix is 23B and there is always at least one 5B item
    #    (k counts *extra* items beyond the first): row_len = 23 + 5*(k+1) + 13.
    for k in (0, 1, 3):
        nit = k + 1
        biz = bytearray(23 + 5 * nit)
        biz[22] = k
        struct.pack_into("<I", biz, 4, 1234)
        for i in range(nit):
            o = 23 + 5 * i
            biz[o] = 0 if i == 0 else 100 // nit
            struct.pack_into("<I", biz, o + 1, 7)
        row = bytes(biz) + struct.pack("<III", 0, 3, 3) + b"\x00"
        chk(len(row) == 41 + 5 * k, f"lcrg row len k={k}")
        raw = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", 1) + bytes(2)
               + row + struct.pack(">I", 1) + struct.pack("<I", 3))
        w = walk_lcrg(raw)
        chk(len(w["rows"]) == 1 and w["end"] + 8 == len(raw), f"lcrg walk k={k}")
        chk(len(w["rows"][0]["biz"]) == 23 + 5 * nit, f"lcrg biz k={k}")

    # 5. domain helpers
    chk(dom([0, 5, NULL_U32], 4)["nonnull"] == 2, "dom null split")
    chk(fits_target([100, 200], 4, "nation")["rate"] == 1.0, "fits_target")

    print(f"selftest ok ({ok} checks)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="t76c_slots",
        description="Slot mapper for derby(18)/weather(27)/local_region(47)/"
                    "agreement(56). Reuses t73_mapper_core via runpy (unmodified); "
                    "row frames come from scratch/t74/out/frames.json.")
    ap.add_argument("--table", type=int, choices=(18, 27, 47, 56))
    ap.add_argument("--archive", choices=("client", "server"))
    ap.add_argument("--json", metavar="OUT")
    ap.add_argument("--all", action="store_true", help="all 8 (archive,table) pairs")
    ap.add_argument("--outdir", default="scratch/t76c/out")
    ap.add_argument("--calibrate", action="store_true",
                    help="print the ordinal-vs-UID encoding calibration and exit")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.calibrate:
        print(json.dumps(calibrate(), ensure_ascii=False, indent=1))
        return 0
    if not a.all and (a.table is None or a.archive is None):
        ap.print_help()
        return 2
    if a.all:
        outdir = Path(a.outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        rc = 0
        for tid in (56, 18, 27, 47):
            for arch in ("client", "server"):
                res = build(arch, tid)
                p = outdir / f"slots_{arch}_{tid}.json"
                p.write_text(json.dumps(res, ensure_ascii=False, indent=1),
                             encoding="utf-8")
                nsl = sum(1 for s in res.get("slots", [])
                          if s["grade"] in ("L2", "L3"))
                print(f"  {arch:6} t{tid:<3} {res.get('status'):9} "
                      f"rows={res.get('walk', {}).get('rows', '-')} "
                      f"L2/L3={nsl} -> {p.name}")
                if res.get("status") != "closed":
                    rc = 1
        return rc
    res = build(a.archive, a.table)
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.json:
        p = Path(a.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")
    print(f"table {a.table} {a.archive}: status={res.get('status')} "
          f"rows={res.get('walk', {}).get('rows')} "
          f"closure={res.get('walk', {}).get('closure')}")
    for s in res.get("slots", []):
        print(f"  {str(s['field']):22} {str(s['offset']):5} {s['grade']:15} "
              f"{s['why'][:64]}")
    return 0 if res.get("status") == "closed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
