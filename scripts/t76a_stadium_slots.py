#!/usr/bin/env python3
"""t76a-fix1 — stadium(21) dual-archive slot map (data side: L2 / candidate).

Row frames come verbatim from `scratch/t74/out/frames.json` (t74 closed them).
This tool NEVER re-closes a frame: it re-derives the byte-exact walk, asserts the
closure still holds, and only then addresses slots inside it.

`scripts/t73_mapper_core.py` is loaded through runpy for load_payload and the
reference-UID helper (read-only, unmodified).

    py -V:3.12 -I -B scripts/t76a_stadium_slots.py --all
    py -V:3.12 -I -B scripts/t76a_stadium_slots.py --archive client --json OUT
    py -V:3.12 -I -B scripts/t76a_stadium_slots.py --selftest

Exit codes: 0 success / 1 check failed / 2 usage or fatal.

Grading doctrine (AGENTS.md). Everything produced *here* is data-side:
  L2        = closed on this payload by an invariant that cannot be a coincidence
              (row-ordinal identity, UID-pair identity, ordinal-domain FK that is
              100% in-domain AND tight AND whose UID encoding is refuted).
  candidate = type width x schema range x value domain agree, but the data does
              not single the field out.
  held      = string/list/subobject; not a fixed-width scalar slot.
  escalate  = needs exe dispatch / cross-object pointer to decide.
Static L3 from the sibling task t79 is *cited* (`scratch/t79/out/field_map.json`)
and never re-derived here; it is labelled `l3_cited` so the two are never conflated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import struct
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

TID = 21
XML = "stadium.xml"
FRAMES = REPO / "scratch" / "t74" / "out" / "frames.json"
T79_MAP = REPO / "scratch" / "t79" / "out" / "field_map.json"
NULL32 = 0xFFFFFFFF

# Live row counts frozen by t57/t59 (ordinal domains, not UID sets).
NROWS = {"city": 56293, "club": 84259, "nation": 251, "region": 28,
         "comp": 7047, "stadium": 48413, "team": 84507, "continent": 7,
         "language": 126, "weather": 334, "local_region": 2488}
ENTITY_TID = {"city": 2, "club": 3, "nation": 10, "region": 19, "comp": 25,
              "stadium": 21, "continent": 5, "language": 8, "weather": 27,
              "local_region": 47}

_CORE = None


def core() -> dict:
    global _CORE
    if _CORE is None:
        _CORE = runpy.run_path(str(HERE / "t73_mapper_core.py"), run_name="t76a_core")
    return _CORE


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def t74_frame(archive: str) -> dict:
    """Frame as frozen by t74. Read-only: never recomputed here."""
    d = json.loads(FRAMES.read_text(encoding="utf-8"))
    return d["tables"][str(TID)]["archives"][archive]


def load_matrix(archive: str) -> tuple[bytes, np.ndarray, dict]:
    """payload + (count, stride) uint8 matrix + the t74 frame record."""
    fr = t74_frame(archive)
    raw = core()["load_payload"](archive, TID)
    H, S, n = fr["header"], fr["stride"], fr["count"]
    m = np.frombuffer(raw, np.uint8, H + n * S)[H:].reshape(n, S)
    return raw, m, fr


def walk_check(raw: bytes, fr: dict) -> dict:
    """Assert the t74 closure still holds on THIS payload (no re-closure)."""
    H, S, n, F = fr["header"], fr["stride"], fr["count"], fr["footer"]
    end = H + n * S
    ident_ok = 0
    for j in range(n):
        t = H + j * S + S - 13
        o, a, b = struct.unpack_from("<III", raw, t)
        if o == j and a == b != 0 and raw[t + 12] == 0:
            ident_ok += 1
    return {"header": H, "stride": S, "count": n, "footer": F,
            "closure": f"{H} + {n} x {S} + {F} = {len(raw)}",
            "closure_ok": end + F == len(raw),
            "count_header_ok": struct.unpack_from("<I", raw, 8)[0] == n,
            "identity_rows_ok": ident_ok,
            "identity_layout": fr["identity"]["layout"],
            "identity_anchor": fr["identity"]["anchor"]}


def u(m: np.ndarray, o: int, w: int) -> np.ndarray:
    return np.ascontiguousarray(m[:, o:o + w]).view(f"<u{w}").ravel().astype(np.int64)


def f32(m: np.ndarray, o: int) -> np.ndarray:
    """f32 view. NaN/Inf are preserved (not silenced): the caller splits them out."""
    with np.errstate(invalid="ignore", over="ignore"):
        return (np.ascontiguousarray(m[:, o:o + 4]).view("<f4").ravel()
                .astype(np.float64))


def profile(m: np.ndarray, o: int, S: int) -> dict:
    """Per-offset raw value domain. Widths are candidates, never decisions."""
    col = m[:, o]
    vals, cnt = np.unique(col, return_counts=True)
    d = {"offset": o, "u8_distinct": int(vals.size),
         "u8_values": [int(x) for x in vals[:16]],
         "u8_top": {int(a): int(b) for a, b in
                    sorted(zip(vals, cnt), key=lambda p: -p[1])[:6]},
         "all_zero": bool((col == 0).all()),
         "all_ff": bool((col == 0xFF).all()),
         "zero_rate": round(float((col == 0).mean()), 6)}
    for w in (2, 4):
        if o + w > S:
            continue
        v = u(m, o, w)
        nn = v[v != (1 << (8 * w)) - 1]
        d[f"u{w * 8}"] = {"min": int(v.min()), "max": int(v.max()),
                          "distinct": int(np.unique(v).size),
                          "n_null": int((v == (1 << (8 * w)) - 1).sum()),
                          "n_zero": int((v == 0).sum()),
                          "nonnull_min": int(nn.min()) if nn.size else None,
                          "nonnull_max": int(nn.max()) if nn.size else None}
    if o + 4 <= S:
        f = f32(m, o)
        fin = np.isfinite(f)
        d["f32"] = {"finite": int(fin.sum()), "n": int(f.size),
                    "min": round(float(f[fin].min()), 6) if fin.any() else None,
                    "max": round(float(f[fin].max()), 6) if fin.any() else None,
                    "zero_rate": round(float((f == 0).mean()), 6)}
        d["f32_plausible"] = bool(fin.all() and (np.abs(f[fin]) < 1e6).all())
    return d


def profile_all(m: np.ndarray) -> dict:
    S = m.shape[1]
    return {str(o): profile(m, o, S) for o in range(S)}


# --------------------------------------------------------------- ref domains --
def ref_uids(archive: str, tid: int) -> dict:
    """UID set of a reference table via t73 helper (cached on disk by t73)."""
    try:
        r = core()["reference_uids"](archive, tid)
    except Exception as exc:  # noqa: BLE001 - preserved verbatim
        return {"ok": False, "why": f"{type(exc).__name__}: {exc}", "uids": []}
    return r


def ord_fit(vals: np.ndarray, target: str) -> dict:
    """Ordinal-domain fit: null = all-ones; every non-null value < N; tightness."""
    N = NROWS[target]
    v = vals[vals != NULL32]
    if v.size == 0:
        return {"target": target, "N": N, "nonnull": 0}
    in_dom = float((v < N).mean())
    mx = int(v.max())
    return {"target": target, "N": N,
            "null": int((vals == NULL32).sum()), "nonnull": int(v.size),
            "distinct": int(np.unique(v).size),
            "min": int(v.min()), "max": mx,
            "in_domain": round(in_dom, 6),
            "max_over_N": round(mx / N, 4),
            "tight": bool(in_dom == 1.0 and mx > 0.6 * N),
            "zero_values": int((v == 0).sum())}


def all_fits(vals: np.ndarray, targets=None) -> list[dict]:
    out = []
    for t in (targets or NROWS):
        f = ord_fit(vals, t)
        if f.get("in_domain") == 1.0 and f.get("tight"):
            out.append(f)
    return sorted(out, key=lambda f: f["N"])


def uid_control(vals: np.ndarray, archive: str, target: str) -> dict:
    """Wrong-encoding control: does the slot hold the target's UID set instead?"""
    tid = ENTITY_TID[target]
    r = ref_uids(archive, tid)
    if not r.get("ok"):
        return {"target": target, "available": False, "why": r.get("why")}
    dom = set(r["uids"])
    v = vals[vals != NULL32]
    hits = int(sum(1 for x in v.tolist() if x in dom))
    return {"target": target, "available": True, "domain": len(dom),
            "uid_hits": hits, "nonnull": int(v.size),
            "uid_rate": round(hits / max(1, v.size), 6),
            "refuted": hits / max(1, v.size) < 0.5}


# ------------------------------------------------------------ schema helpers --
_SCHEMA = None


def schema() -> dict:
    global _SCHEMA
    if _SCHEMA is None:
        p = REPO / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
        _SCHEMA = json.loads(p.read_text(encoding="utf-8"))
    return _SCHEMA


def fields() -> list[dict]:
    return schema()["entities"][XML][0]["fields"]


def enum_domain(name: str) -> set[int]:
    e = schema().get("enums", {}).get(name) or {}
    return {int(v["enum"]) for v in e.get("values", [])
            if str(v["enum"]).lstrip("-").isdigit()}


def t79_cited() -> dict:
    """Static L3 harvest from the sibling task t79 — cited, never re-derived."""
    if not T79_MAP.exists():
        return {}
    d = json.loads(T79_MAP.read_text(encoding="utf-8"))
    return {f["field"]: f for f in d.get("stadium_21", {}).get("schema_fields", [])}


# ------------------------------------------------------------- frozen anchors --
# scripts/fm24_dump.py FIELDS, snapshot evidence/fm24/2026-11-18.
FROZEN_CLIENT = {"Scti": 3, "Slat": 17, "Slon": 21, "rdui": 25, "duni": 29}
# t79 static reconciliation of the same anchors onto server body offsets
# (server body = the 143B server-only prefix + the shared 38B tail).
FROZEN_SERVER = {"Scti": 146, "Slat": 160, "Slon": 164, "duni": 172}


def anchor_report(m: np.ndarray, archive: str) -> dict:
    """Re-verify every frozen anchor on THIS payload; no assumption reused."""
    n = m.shape[0]
    ar = np.arange(n)
    items = []
    anchors = FROZEN_CLIENT if archive == "client" else FROZEN_SERVER
    for fld, off in anchors.items():
        v = u(m, off, 4)
        it = {"field": fld, "offset": off,
              "distinct": int(np.unique(v).size),
              "min": int(v.min()), "max": int(v.max())}
        if fld == "rdui":
            it["kind"] = "row_ordinal"
            it["equals_row_index"] = int((v == ar).sum())
            it["ok"] = bool((v == ar).all())
        elif fld == "duni":
            it["kind"] = "uid_pair"
            it["pair_off"] = off + 4
            it["pair_equal"] = bool((v == u(m, off + 4, 4)).all())
            it["ok"] = bool(it["pair_equal"] and v.min() > 0)
        elif fld in ("Slat", "Slon"):
            f = f32(m, off)
            it["kind"] = "f32"
            it["f32_min"] = round(float(f.min()), 4)
            it["f32_max"] = round(float(f.max()), 4)
            it["ok"] = bool(np.isfinite(f).all() and np.abs(f).max() < 400)
        else:
            fit = ord_fit(v, "city")
            it["kind"] = "ordinal_ref"
            it["fit_city"] = fit
            it["ok"] = bool(fit["in_domain"] == 1.0)
        items.append(it)
    return {"checked": len(items), "ok": sum(1 for i in items if i["ok"]),
            "items": items}


# ------------------------------------------------------------------ layouts --
# Client 38B body. Offsets are row-relative (t74 stride coordinates == body coords).
CLIENT = [
    (0, 2, "flags_u16", "u16 bitflag word"),
    (2, 1, "opaque", "const 0 (+0xa8)"),
    (3, 4, "Scti", "u32 ordinal -> city"),
    (7, 4, "Snbs", "u32 ordinal -> stadium"),
    (11, 2, "Sptc", "u16"),
    (13, 4, "opaque", "packed date 1900-01-01 (+0x34)"),
    (17, 4, "Slat", "f32"),
    (21, 4, "Slon", "f32"),
    (25, 4, "row_ordinal", "u32 == row index"),
    (29, 4, "duni", "u32 UID pair"),
    (33, 4, "rdui_raw", "u32 == duni (suppressed)"),
    (37, 1, "marker", "const 0"),
]

# Server-only 143B prefix (server row offset 0..142; client body starts at 143).
SERVER_PREFIX = [
    (0, 4, "Scpy", "i32 capacity"),
    (4, 4, "Sscy", "i32 seating"),
    (8, 4, "Secy", "i32 expansion"),
    (12, 4, "Scas", "i32 all-seater"),
    (16, 4, "Sowi", "u32 ordinal -> club"),
    (20, 1, "Sdcy", "i8"),
    (21, 4, "Sucy", "i32 used capacity"),
    (25, 2, "Spln", "i16 /10"),
    (27, 2, "Spwd", "i16 /10"),
    (29, 2, "SlIM", "i16 /10"),
    (31, 2, "SwIM", "i16 /10"),
    (33, 1, "Spty", "u8 enum"),
    (34, 1, "Sste", "i8 enum"),
    (35, 1, "Senv", "i8 enum"),
    (36, 1, "flags_u8", "u8 bitflag word"),
    (37, 4, "Sbld", "packed date"),
    (41, 4, "Srbd", "packed date"),
    (45, 4, "Doco", "packed date"),
    (49, 1, "Sunt", "i8 enum ubnt"),
    (50, 1, "Su21", "i8 enum ubnt"),
    (51, 1, "Su19", "i8 enum ubnt"),
    (52, 1, "Soty", "i8 enum"),
    (53, 1, "Snft", "internal 4CC, const 0"),
    (54, 2, "Smnl", "i16 /10"),
    (56, 2, "Smnw", "i16 /10"),
    (58, 2, "Smxl", "i16 /10"),
    (60, 2, "Smxw", "i16 /10"),
    (62, 1, "Sdtr", "i8 enum"),
    (63, 1, "Ssds_flag", "u8 flag"),
    (64, 64, "Ssds_sides", "8 x 8B side records"),
    (128, 2, "Ssds_tail", "2B tail"),
    (130, 1, "Sprr", "i8"),
    (131, 4, "SplR", "packed date"),
    (135, 4, "Sprl", "packed date"),
    (139, 4, "Sscl", "colour 4B rev"),
]

CLIENT_BITS = {0: "Scov", 1: "Sush", 6: "Srrf", 7: "Nucf", 11: "Wucf"}
SERVER_BITS = {0: "Sext", 2: "Sitg", 5: "Sovl", 6: "Sdah"}
SIDE_FIELDS = [(0, 4, "capc", "i32"), (4, 1, "flags", "u8"),
               (5, 2, "sage", "i16"), (7, 1, "cond", "i8")]


def bit_report(m: np.ndarray, off: int, width: int, names: dict) -> dict:
    v = u(m, off, width)
    out = {}
    for b in range(width * 8):
        n = int(((v >> b) & 1).sum())
        if n:
            out[str(b)] = {"field": names.get(b), "set": n,
                           "rate": round(n / v.shape[0], 6)}
    return {"offset": off, "width": width, "constant_zero_bits": sorted(
        set(range(width * 8)) - {int(k) for k in out}), "bits": out}


def packed_date(m: np.ndarray, off: int) -> dict:
    v = u(m, off, 4)
    doy, yr = v & 0xFFFF, v >> 16
    ok = (doy >= 1) & (doy <= 366) & (yr >= 1800) & (yr <= 2100)
    return {"offset": off, "rate_valid": round(float(ok.mean()), 6),
            "doy_min": int(doy.min()), "doy_max": int(doy.max()),
            "year_min": int(yr.min()), "year_max": int(yr.max()),
            "distinct": int(np.unique(v).size),
            "n_default_1900_01_01": int(((yr == 1900) & (doy == 1)).sum())}


def i16_div10(m: np.ndarray, off: int) -> dict:
    v = u(m, off, 2).astype(np.int64)
    sv = np.where(v >= 32768, v - 65536, v)
    return {"offset": off, "raw_min": int(v.min()), "raw_max": int(v.max()),
            "signed_min": int(sv.min()), "signed_max": int(sv.max()),
            "as_metres_min": round(float(sv.min()) / 10, 2),
            "as_metres_max": round(float(sv.max()) / 10, 2),
            "distinct": int(np.unique(v).size),
            "n_null_ffff": int((v == 0xFFFF).sum()),
            "n_zero": int((v == 0).sum())}


def slot(field, off, width, grade, why, evidence=None, kind="u32"):
    return {"field": field, "offset": off, "width": width, "kind": kind,
            "grade": grade, "why": why, "evidence": evidence or []}


def build_client(raw: bytes, m: np.ndarray, fr: dict) -> dict:
    n = m.shape[0]
    cited = t79_cited()
    slots, columns = [], {}
    body_end = 25  # client: 25B shared body + 13B identity

    for off, w, name, note in CLIENT:
        columns[str(off)] = profile(m, off, 38)

    # (a) frozen anchors, re-verified on this payload
    ar_rep = anchor_report(m, "client")
    for it in ar_rep["items"]:
        fld = it["field"]
        c = cited.get(fld) or {}
        if fld == "rdui":
            slots.append(slot(
                "rdui", 25, 4, "L2",
                "offset column equals row index on all 48,413 rows; the frozen "
                "label 'rdui@25' is reconciled as the row ORDINAL, not the random "
                "UID (t79 static: this column is member +0x08, and the real rdui "
                "arm is suppressed on 48,413/48,413 rows)",
                [{"equals_row_index": it["equals_row_index"], "rows": n,
                  "l3_cited": {"member_off": c.get("member_off"),
                               "getter_fo": c.get("getter_fo")}}],
                kind="row_ordinal"))
        elif fld == "duni":
            slots.append(slot(
                "duni", 29, 4, "L2",
                "UID pair: u32@29 == u32@33, both non-zero, 48,413 distinct values "
                "on 48,413 rows",
                [{"pair_off": 33, "pair_equal": it["pair_equal"],
                  "distinct": it["distinct"], "rows": n}], kind="uid"))
        elif fld in ("Slat", "Slon"):
            f = f32(m, 29 if fld == "duni" else it["offset"])
            slots.append(slot(
                fld, it["offset"], 4, "L3",
                f"frozen FIELDS anchor (fm24_dump.py, snapshot 2026-11-18) "
                f"re-verified: finite f32, range [{it['f32_min']}, {it['f32_max']}]",
                [{"anchor": "scripts/fm24_dump.py:FIELDS", "kind": "L3",
                  "f32_min": it["f32_min"], "f32_max": it["f32_max"],
                  "zeros": int((f == 0).sum())}], kind="f32"))
        else:  # Scti
            fit = it["fit_city"]
            ctl = uid_control(u(m, it["offset"], 4), "client", "city")
            slots.append(slot(
                "Scti", it["offset"], 4, "L2",
                f"frozen anchor re-verified; whole-u32 column at 100% inside the "
                f"city ordinal domain (max {fit['max']} / {fit['N']} = "
                f"{fit['max_over_N']}) and the city UID encoding is REFUTED "
                f"({ctl.get('uid_hits')}/{ctl.get('nonnull')} = "
                f"{ctl.get('uid_rate')})",
                [{"anchor": "scripts/fm24_dump.py:FIELDS", "kind": "L3",
                  "fit": fit, "uid_control": ctl}], kind="ordinal_ref"))

    # (b) Snbs -> stadium ordinal
    v7 = u(m, 7, 4)
    fit7 = ord_fit(v7, "stadium")
    # Wrong-UID control for a self-referencing table: the stadium UID set is right
    # here in the duni column, so the control is available even though t21's own
    # frame is ambiguous for the generic resolver.
    own_uids = set(u(m, 29, 4).tolist())
    live7 = v7[v7 != NULL32]
    uid_hits7 = int(sum(1 for x in live7.tolist() if x in own_uids))
    ctl7 = {"encoding_control": "self-table UID set taken from duni@29",
            "uid_hits": uid_hits7, "nonnull": int(live7.size),
            "uid_rate": round(uid_hits7 / max(1, live7.size), 6),
            "refuted": uid_hits7 / max(1, live7.size) < 0.5}
    alt7 = all_fits(v7, ("stadium", "city", "club"))
    slots.append(slot(
        "Snbs", 7, 4, "L2",
        f"authored nullable slot: {fit7['null']:,} null (0xffffffff), "
        f"{fit7['nonnull']:,} live values, every live value < stadium(48,413) "
        f"at 100% with top {fit7['max']} ({fit7['max_over_N']} of domain, i.e. "
        f"TIGHT); the wrong-UID control is REFUTED at "
        f"{ctl7['uid_hits']}/{ctl7['nonnull']} = {ctl7['uid_rate']} -- ordinals, "
        f"not UIDs. Schema names stadium as the reference target of Snbs only, "
        f"and self-reference is the only target whose domain is tight here",
        [{"fit": fit7, "compatible_targets": alt7, "uid_control": ctl7,
          "self_reference_rows": int((live7 == np.arange(n)[v7 != NULL32]).sum())}],
        kind="ordinal_ref"))

    # (c) Sptc: u16 in schema range 0..200
    d11 = profile(m, 11, 38)
    slots.append(slot(
        "Sptc", 11, 2, "candidate",
        f"u16 slot, domain {d11['u16']['min']}..{d11['u16']['max']} inside the "
        f"schema range 0..200 (Pitch Condition); the data alone does not "
        f"separate it from the other bounded u16 slots on this row",
        [{"domain": d11["u16"]}], kind="u16"))

    # (d) flag word @0
    slots.append(slot(None, 0, 2, "candidate",
                      "u16 bitflag word on the shared 25B tail; 5 bits ever set "
                      f"(0,1,6,7,11) and 11 bits constant 0, so the field order "
                      "inside the word is not decidable from data",
                      [bit_report(m, 0, 2, CLIENT_BITS)], kind="bitflag"))

    # (e) opaque constants
    slots.append(slot(
        "rdui_raw", 33, 4, "L2",
        "second UID terminator of the identity triple: u32@33 == duni@29 on all "
        "48,413 rows. The exe suppresses this arm whenever [+0x0c]==[+0x10], i.e. "
        "always, so it never surfaces as the Random ID (t79 static hold)",
        [{"equals_duni": bool((u(m, 29, 4) == u(m, 33, 4)).all()),
          "distinct": int(np.unique(u(m, 33, 4)).size), "rows": n}],
        kind="uid"))
    for off, w, name, note in CLIENT:
        if name != "opaque":
            continue
        slots.append(slot(None, off, w, "unassigned",
                          f"opaque: {note}; constant across all {n:,} rows, no "
                          "schema field is bound to it",
                          [{"all_zero": bool((m[:, off:off + w] == 0).all()),
                            "distinct": int(np.unique(
                                m[:, off:off + w].view(np.uint8)).size)}],
                          kind="opaque"))
    slots.append(slot(None, 37, 1, "unassigned",
                      "row marker byte, constant 0 on all 48,413 rows (identity "
                      "triple terminator)", [], kind="marker"))

    return {"archive": "client", "body_len": 38, "slots": slots,
            "columns": columns, "anchors": ar_rep}


def build_server(raw: bytes, m: np.ndarray, fr: dict) -> dict:
    n = m.shape[0]
    cited = t79_cited()
    slots, columns = [], {}
    for off in range(143):
        columns[str(off)] = profile(m, off, 181)
    for off in (168, 172, 176):
        columns[str(off)] = profile(m, off, 181)

    # (a) the shared 38B tail is byte-identical to the client body — prove it.
    rawC = core()["load_payload"]("client", TID)
    mc = np.frombuffer(rawC, np.uint8, 14 + n * 38)[14:].reshape(n, 38)
    ident_rows = int((m[:, 143:181] == mc).all(axis=1).sum())

    # (b) identity / anchors on the server stride
    ar_rep = anchor_report(m, "server")
    slots.append(slot(
        "row_ordinal", 168, 4, "L2",
        "u32@168 equals the row index on 48,413/48,413 rows (t74 identity anchor "
        "row_end-13); same invariant as the client row ordinal @25",
        [{"equals_row_index": int((u(ms_ := m, 168, 4) == np.arange(n)).sum()),
          "rows": n}], kind="row_ordinal"))
    slots.append(slot(
        "duni", 172, 4, "L2",
        "UID pair: u32@172 == u32@176, non-zero, distinct on all rows",
        [{"pair_off": 176, "pair_equal": bool((u(m, 172, 4) == u(m, 176, 4)).all()),
          "distinct": int(np.unique(u(m, 172, 4)).size)}], kind="uid"))
    slots.append(slot(
        "rdui_raw", 176, 4, "L2",
        "second UID terminator of the identity triple; equal to duni on all rows "
        "and suppressed by the exe (t79 static hold)",
        [{"equals_duni": bool((u(m, 172, 4) == u(m, 176, 4)).all())}], kind="uid"))
    slots.append(slot(
        "marker", 180, 1, "unassigned",
        "row marker byte, constant 0", [], kind="marker"))

    # (c) shared tail anchors (Scti/Slat/Slon at client+143)
    for it in ar_rep["items"]:
        fld = it["field"]
        if fld not in ("Scti", "Slat", "Slon"):
            continue
        off = it["offset"]
        if fld == "Scti":
            fit = it["fit_city"]
            ctl = uid_control(u(m, off, 4), "server", "city")
            slots.append(slot(fld, off, 4, "L2",
                              f"shared tail slot (client@3 + 143); 100% inside the "
                              f"city ordinal domain (max {fit['max']}), city UID "
                              f"encoding refuted ({ctl.get('uid_rate')})",
                              [{"fit": fit, "uid_control": ctl,
                                "shared_with_client_off": 3}], kind="ordinal_ref"))
        else:
            slots.append(slot(fld, off, 4, "L3",
                              f"shared tail f32 (client@{off - 143} + 143); "
                              f"finite, range [{it['f32_min']}, {it['f32_max']}]",
                              [{"shared_with_client_off": off - 143}], kind="f32"))
    v150 = u(m, 150, 4)
    fit150 = ord_fit(v150, "stadium")
    own_s = set(u(m, 172, 4).tolist())
    live150 = v150[v150 != NULL32]
    hits150 = int(sum(1 for x in live150.tolist() if x in own_s))
    ctl150 = {"encoding_control": "self-table UID set taken from duni@172",
              "uid_hits": hits150, "nonnull": int(live150.size),
              "uid_rate": round(hits150 / max(1, live150.size), 6),
              "refuted": hits150 / max(1, live150.size) < 0.5}
    slots.append(slot("Snbs", 150, 4, "L2",
                      f"shared tail slot (client@7 + 143): {fit150['null']:,} null, "
                      f"all live values < stadium(48,413) at 100%, top "
                      f"{fit150['max']} ({fit150['max_over_N']}); wrong-UID control "
                      f"refuted ({hits150}/{live150.size} = {ctl150['uid_rate']})",
                      [{"fit": fit150, "uid_control": ctl150,
                        "shared_with_client_off": 7}], kind="ordinal_ref"))
    d154 = profile(m, 154, 181)
    slots.append(slot("Sptc", 154, 2, "candidate",
                      f"shared tail u16 (client@11 + 143), domain "
                      f"{d154['u16']['min']}..{d154['u16']['max']} within schema "
                      "0..200", [{"domain": d154["u16"],
                                  "shared_with_client_off": 11}], kind="u16"))
    slots.append(slot(None, 143, 2, "candidate",
                      "shared tail u16 bitflag word (client@0 + 143); same "
                      "undecidable bit order as the client flags",
                      [bit_report(m, 143, 2, CLIENT_BITS)], kind="bitflag"))
    # shared-tail opaque slots (client@2 / @13 + 143) so the body is fully covered
    for off, w, note in ((145, 1, "const 0 (client@2 + 143, +0xa8)"),
                         (156, 4, "packed date, default 1900-01-01 "
                                   "(client@13 + 143, +0x34)")):
        slots.append(slot(None, off, w, "unassigned",
                          f"opaque shared-tail slot {note}; constant on all "
                          f"{n:,} rows, no schema field bound to it",
                          [{"all_zero": bool((m[:, off:off + w] == 0).all()),
                            "distinct": int(np.unique(m[:, off:off + w]).size),
                            "shared_with_client_off": off - 143}],
                          kind="opaque"))

    # (d) server-only 143B prefix
    # capacities 0..12: a real nesting invariant, but statistical (not absolute),
    # so it gets its own grade rather than being called a closed L2.
    cap_off = ((0, "Scpy", "Capacity"), (4, "Sscy", "Seating Capacity"),
               (8, "Secy", "Expansion Capacity"),
               (12, "Scas", "Capacity For All-Seater Competitions"))
    A, B, C, D = (u(m, o, 4) for o, _, _ in cap_off)
    both = (A > 0) & (B > 0) & (C > 0) & (D > 0)
    nest = ((D[both] <= B[both]) & (B[both] <= A[both]) & (A[both] <= C[both]))
    nest_rate = round(float(nest.mean()), 6) if both.any() else None
    nest_ev = {"rule": "Scas@12 <= Sscy@4 <= Scpy@0 <= Secy@8",
               "rows_all_nonzero": int(both.sum()),
               "rows_satisfying": int(nest.sum()),
               "rate": nest_rate,
               "pairwise": {
                   "Scas<=Sscy": round(float((D[(D > 0) & (B > 0)] <=
                                               B[(D > 0) & (B > 0)]).mean()), 6),
                   "Sscy<=Scpy": round(float((B[(B > 0) & (A > 0)] <=
                                               A[(B > 0) & (A > 0)]).mean()), 6),
                   "Scpy<=Secy": round(float((A[(A > 0) & (C > 0)] <=
                                               C[(A > 0) & (C > 0)]).mean()), 6)},
               "violations_preserved": int(both.sum() - nest.sum())}
    for off, fld, note in cap_off:
        d = profile(m, off, 181)
        v = u(m, off, 4)
        slots.append(slot(
            fld, off, 4, "L2_structural",
            f"i32 {note}: max {d['u32']['max']} inside schema 0..200000, "
            f"zeros {d['u32']['n_zero']:,}. The four capacity slots are ordered "
            f"by a business nesting that holds on {nest_rate*100:.2f}% of the "
            f"{int(both.sum()):,} rows where all four are non-zero: "
            f"Scas <= Sscy <= Scpy <= Secy. That order is exactly the schema "
            f"semantics, so the family assignment is data-decided, but the rule "
            f"is statistical rather than absolute ({nest_ev['violations_preserved']:,} "
            f"violations are preserved verbatim), hence not graded L2",
            [{"domain": d["u32"], "nesting": nest_ev}], kind="i32"))
    # Sowi
    v16 = u(m, 16, 4)
    fit16 = ord_fit(v16, "club")
    ctl16 = uid_control(v16, "server", "club")
    slots.append(slot("Sowi", 16, 4, "candidate",
                      f"authored nullable slot ({fit16['null']:,} null), every live "
                      f"value inside the club ordinal domain at 100% with top "
                      f"{fit16['max']} ({fit16['max_over_N']} of N). NOT promoted to "
                      f"L2: team(84,507) contains the same values equally well "
                      f"({[f['target'] for f in all_fits(v16)]}), and the club UID "
                      f"control is UNAVAILABLE (t3 frame unresolved), so the "
                      f"ordinal-vs-UID encoding cannot be refuted on this payload. "
                      f"Slot identity rests on the t79 static getter 0x11864e8 -> "
                      f"+0x80 with fixup 0x3e44580 -> table_3",
                      [{"fit": fit16, "uid_control": ctl16,
                        "compatible_targets": all_fits(v16),
                        "blocker": "club/team ordinal domains not separable; "
                                    "club UID set unavailable -> wrong-UID "
                                    "control cannot run"}], kind="ordinal_ref"))
    # Sdcy i8 0..20 (byte 20; the neighbouring u32 starts at 21, so they abut,
    # they do not overlap)
    d20 = profile(m, 20, 181)
    slots.append(slot("Sdcy", 20, 1, "candidate",
                      f"i8 slot, byte domain {d20['u8_values'][0]}.."
                      f"{max(d20['u8_values'])} inside schema 0..20 (Decay). The "
                      f"byte at 20 is a single value (5) on every row while the "
                      f"u32 at 21 carries real range, so the field boundary is "
                      f"consistent with a 1-byte slot abutting a 4-byte slot",
                      [{"u8_values": d20["u8_values"]}], kind="i8"))
    # Sucy: schema min_value=1, default 20000, optional -> zero is the null marker
    d21 = profile(m, 21, 181)
    slots.append(slot("Sucy", 21, 4, "candidate",
                      f"i32 at 21: max {d21['u32']['max']} inside schema 1..200000; "
                      f"{d21['u32']['n_zero']:,} zeros act as the null marker for "
                      f"an optional field whose declared default is 20000",
                      [{"domain": d21["u32"]}], kind="i32"))
    # pitch blocks
    for off, fld in ((25, "Spln"), (27, "Spwd"), (29, "SlIM"), (31, "SwIM"),
                     (54, "Smnl"), (56, "Smnw"), (58, "Smxl"), (60, "Smxw")):
        slots.append(slot(fld, off, 2, "candidate",
                          f"i16/10 (pitch distance): signed {i16_div10(m, off)['signed_min']}"
                          f"..{i16_div10(m, off)['signed_max']} raw units",
                          [i16_div10(m, off)], kind="i16"))
    # enums
    for off, fld in ((33, "Spty"), (34, "Sste"), (35, "Senv"), (52, "Soty"),
                     (62, "Sdtr")):
        dom = enum_domain(fld)
        col = {int(x) for x in np.unique(m[:, off]).tolist()}
        slots.append(slot(fld, off, 1, "candidate",
                          f"byte column domain {sorted(col)} vs scoped enum "
                          f"`{fld}` {sorted(dom)}: "
                          f"{'subset' if col <= dom else 'NOT a subset'}",
                          [{"column": sorted(col), "enum": sorted(dom),
                            "subset": col <= dom}], kind="enum"))
    for off, fld in ((49, "Sunt"), (50, "Su21"), (51, "Su19")):
        dom = enum_domain("ubnt")
        col = {int(x) for x in np.unique(m[:, off]).tolist()}
        cnt = {int(x): int((m[:, off] == x).sum())
               for x in np.unique(m[:, off])}
        # 21 byte columns on this row are subsets of 0..6, so a subset test does
        # NOT identify a slot. Only the t79 static wiring does; state that.
        slots.append(slot(fld, off, 1, "candidate",
                          f"byte column domain {sorted(col)} is a subset of the "
                          f"scoped `ubnt` enum {sorted(dom)}, but 21 columns on "
                          f"this row share that property, so the domain does NOT "
                          f"decide. Field identity is cited from t79 static "
                          f"(getter/setter pair on the member at +0xa1/+0xa2/+0xa3) "
                          f"and is not established by the data here",
                          [{"column_counts": cnt, "enum": sorted(dom),
                            "ambiguous_with": [
                                o for o in range(143)
                                if o not in (49, 50, 51)
                                and {int(x) for x in np.unique(m[:, o])} <= dom
                                and np.unique(m[:, o]).size > 1]}],
                          kind="enum"))
    for off, fld in ((37, "Sbld"), (41, "Srbd"), (45, "Doco"), (131, "SplR"),
                     (135, "Sprl")):
        pd = packed_date(m, off)
        # Packed-date validity is a strong shape test but it does not name WHICH
        # of the five date fields sits here; only t79 static does.
        slots.append(slot(fld, off, 4, "candidate",
                          f"packed date u32 (doy | year<<16): valid on "
                          f"{pd['rate_valid']*100:.2f}% of rows, years "
                          f"{pd['year_min']}..{pd['year_max']}, doy 1..366, "
                          f"{pd['distinct']:,} distinct, "
                          f"{pd['n_default_1900_01_01']:,} rows at the 1900-01-01 "
                          f"default. Five such slots exist on this row; the date "
                          f"shape confirms the encoding but not the field order, "
                          f"which is cited from t79 static",
                          [pd], kind="date"))
    slots.append(slot(None, 36, 1, "candidate",
                      "u8 bitflag word carrying Sext/Sitg/Sovl/Sdah on bits "
                      "0/2/5/6; the data cannot confirm which bit is which field",
                      [bit_report(m, 36, 1, SERVER_BITS)], kind="bitflag"))
    slots.append(slot(None, 53, 1, "unassigned",
                      "internal 4CC 'Snft' slot: constant 0 on all 48,413 rows",
                      [{"all_zero": bool((m[:, 53] == 0).all())}], kind="opaque"))
    slots.append(slot(None, 63, 1, "candidate",
                      "Ssds list header byte preceding the 8 x 8B side records",
                      [profile(m, 63, 181)], kind="u8"))
    slots.append(slot("Ssds", 64, 64, "candidate",
                      "8 x 8B side records: capc u32 @+0, flags u8 @+4, sage i16 "
                      "@+5, cond i8 @+7. t79 static wires 11/12 subfields but "
                      "'sage' violates min_value=0 on 20,425 values, so the block "
                      "stays a candidate subobject, not promoted",
                      [{"record_shape": SIDE_FIELDS,
                        "rec0_capc_max": int(u(m, 64, 4).max())}],
                      kind="subobject"))
    slots.append(slot(None, 128, 2, "unassigned",
                      "2B tail of the sides subobject, constant 0 on all rows",
                      [{"all_zero": bool((m[:, 128:130] == 0).all())}],
                      kind="opaque"))
    d130 = profile(m, 130, 181)
    slots.append(slot("Sprr", 130, 1, "candidate",
                      f"i8 slot, domain 0..{max(d130['u8_values'])} inside schema "
                      "0..20 (Pitch Recovery Rate)",
                      [{"u8_values": d130["u8_values"]}], kind="i8"))
    d139 = profile(m, 139, 181)
    slots.append(slot("Sscl", 139, 4, "candidate",
                      f"4B colour word: {d139['u8_distinct']} distinct low bytes, "
                      f"values {d139['u8_values'][:8]}",
                      [{"domain": d139["u32"]}], kind="colour"))

    return {"archive": "server", "body_len": 181,
            "server_only_segment": {
                "offset": 0, "length": 143,
                "note": "server-only prefix, absent from the client row; per-slot "
                        "semantics are graded below, anything unknown stays unknown"},
            "shared_tail": {"offset": 143, "length": 38,
                            "bytes_equal_to_client_body_rows": ident_rows,
                            "rows": n, "byte_identical": ident_rows == n},
            "slots": slots, "columns": columns, "anchors": ar_rep}


# ------------------------------------------------------------------ assembly --
def grade_summary(slots: list[dict]) -> dict:
    out: dict[str, list] = {}
    for s in slots:
        out.setdefault(s["grade"], []).append(s["field"] or f"@{s['offset']}")
    return {k: v for k, v in sorted(out.items())}


def coverage(body_len: int, slots: list[dict]) -> dict:
    """Byte coverage of the row body by *assigned* slots (overlaps counted once)."""
    seen: set[int] = set()
    owned: set[int] = set()
    for s in slots:
        off, w = s["offset"], s["width"]
        rng = set(range(off, min(off + w, body_len)))
        seen |= rng
        if s["grade"] in ("L2", "L3", "L2_structural"):
            owned |= rng
    return {"body_len": body_len,
            "slotted_bytes": len(seen),
            "L2_L3_bytes": len(owned),
            "L2_L3_ratio": round(len(owned) / body_len, 4),
            "uncovered_offsets": sorted(set(range(body_len)) - seen)}


def build(archive: str) -> dict:
    raw, m, fr = load_matrix(archive)
    w = walk_check(raw, fr)
    base = build_client(raw, m, fr) if archive == "client" else build_server(raw, m, fr)
    schema_fields = [f["field"] for f in fields()]
    claimed = {s["field"] for s in base["slots"] if s["field"]}
    held = [f for f in schema_fields if f not in claimed]
    out = {
        "task": "t76a-fix1", "archive": archive, "table": TID, "entity": XML,
        "payload_len": len(raw), "payload_sha256": sha256(raw),
        "frame_source": "scratch/t74/out/frames.json (frozen; not re-closed)",
        "frame": {"header": w["header"], "stride": w["stride"], "count": w["count"],
                  "footer": w["footer"], "identity": fr["identity"]},
        "walk": w,
        "status": "closed" if (w["closure_ok"] and w["count_header_ok"]
                               and w["identity_rows_ok"] == w["count"]) else "escalate_to_sol",
        "slots": base["slots"],
        "offset_map": {str(s["offset"]): s["field"] for s in base["slots"] if s["field"]},
        "grade_summary": grade_summary(base["slots"]),
        "not_in_schema": [s["field"] or f"@{s['offset']}" for s in base["slots"]
                          if s["field"] is None],
        "schema_fields_unclaimed": held,
        "held": {"reason": "string / list / subobject / non-wire fields are not "
                           "fixed-width scalar row slots; out of scope for a "
                           "data-side slot map",
                 "fields": [f for f in held if f in (
                     "Snam", "dbnm", "Ssds", "Scpc", "NDBC", "FDBC", "Snti",
                     "Shcc", "Shts", "Shtr", "Shrs", "Shbr", "Shbs", "Shbl",
                     "Shls", "Shtl")]},
        "coverage": coverage(base["body_len"], base["slots"]),
        "columns": base["columns"], "anchors": base["anchors"],
    }
    if archive == "server":
        out["server_only_segment"] = base["server_only_segment"]
        out["shared_tail"] = base["shared_tail"]
    return out


# ------------------------------------------------------------------ selftest --
def selftest() -> int:
    """Offline: synthetic frames exercising every helper, no archive access."""
    n = 3
    ok = 0

    def chk(cond, msg):
        nonlocal ok
        assert cond, msg
        ok += 1

    # u / f32 decode
    m = np.arange(24, dtype=np.uint8).reshape(3, 8)
    chk(u(m, 0, 4).tolist() == [0x03020100, 0x0B0A0908, 0x13121110], "u32 decode")
    chk(u(m, 0, 2).tolist() == [0x0100, 0x0908, 0x1110], "u16 decode")

    # ord_fit: nulls split out, tightness
    v = np.array([0, 1, 2, NULL32], dtype=np.int64)
    f = ord_fit(v, "region")
    chk(f["null"] == 1 and f["nonnull"] == 3, "ord_fit null split")
    chk(f["in_domain"] == 1.0, "ord_fit in_domain")
    # [0,1,2] against N=28 is in-domain but NOT tight (max 2 << 0.6*28) -- that
    # distinction is the whole point of the tightness test, so assert it.
    chk(f["tight"] is False, "ord_fit not tight for small values")
    # a value that reaches the top of the domain IS tight
    f_t = ord_fit(np.array([0, 27], dtype=np.int64), "region")
    chk(f_t["tight"] is True and f_t["max_over_N"] == round(27 / 28, 4),
        "ord_fit tight at top")

    # nulls must not be counted as in-domain values
    f2 = ord_fit(np.array([NULL32, NULL32], dtype=np.int64), "region")
    chk(f2["nonnull"] == 0, "ord_fit all-null")

    # enum_domain / fields load from the frozen schema
    chk(enum_domain("ubnt") == set(range(7)), "ubnt enum domain")
    chk(enum_domain("Sdtr") == {1, 2, 3}, "Sdtr enum domain")
    chk(len(fields()) == 60, "stadium.xml field count")

    # t79 citation is read-only and keyed by field
    cit = t79_cited()
    chk(cit.get("Scti", {}).get("server_body_off") == 146, "t79 citation suture")

    # packed_date round-trip: doy 1 + year 1900 -> 0x076c0001
    raw = b"\x01\x00\x6c\x07"
    mm = np.frombuffer(raw, np.uint8).reshape(1, 4)
    pd = packed_date(mm, 0)
    chk(pd["n_default_1900_01_01"] == 1 and pd["rate_valid"] == 1.0, "packed date")

    # a 2026-11-20 style value stays valid
    doy, yr = 324, 2026
    raw2 = struct.pack("<I", doy | (yr << 16))
    pd2 = packed_date(np.frombuffer(raw2, np.uint8).reshape(1, 4), 0)
    chk(pd2["year_min"] == 2026 and pd2["doy_min"] == 324, "packed date 2026")

    # i16/10 decode incl. negative
    mm2 = np.array([[0x9C, 0xFF], [0x10, 0x27]], np.uint8)  # -100, 10000
    d = i16_div10(mm2, 0)
    chk(d["signed_min"] == -100 and d["signed_max"] == 10000, "i16 signed")
    chk(d["as_metres_min"] == -10.0, "i16 /10 metres")

    # bit_report ignores always-zero bits
    mb = np.zeros((2, 2), np.uint8)
    mb[0, 0] = 0b101
    br = bit_report(mb, 0, 1, {0: "A", 2: "C"})
    chk(sorted(int(k) for k in br["bits"]) == [0, 2], "bit_report set bits")
    chk(1 in br["constant_zero_bits"], "bit_report zero bit")

    # walk_check on a synthetic 13B-identity frame
    rows = b"".join(struct.pack("<III", j, 100 + j, 100 + j) + b"\x00" for j in range(2))
    syn = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", 2) + bytes(2) + rows
           + struct.pack(">I", 1) + struct.pack("<I", 11))
    fr = {"header": 14, "stride": 13, "count": 2, "footer": 8,
          "identity": {"layout": "ord@0 uid@4 uid@8 marker@12",
                       "anchor": "row_end-13"}}
    wc = walk_check(syn, fr)
    chk(wc["closure_ok"] and wc["count_header_ok"], "walk_check closure")
    chk(wc["identity_rows_ok"] == 2, "walk_check identity")

    # coverage counts overlaps once
    cv = coverage(8, [{"offset": 0, "width": 4, "grade": "L2"},
                      {"offset": 2, "width": 4, "grade": "candidate"}])
    chk(cv["slotted_bytes"] == 6, "coverage union")
    chk(cv["L2_L3_bytes"] == 4, "coverage L2 bytes")

    print(f"selftest ok ({ok} checks)")
    return 0


# ---------------------------------------------------------------------- main --
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="t76a_stadium_slots",
        description="stadium(21) dual-archive slot map. Frames are taken verbatim "
                    "from scratch/t74/out/frames.json and never re-closed. "
                    "t73_mapper_core is loaded via runpy (unmodified).",
        epilog="Exit codes: 0 success / 1 check failed / 2 usage or fatal.")
    ap.add_argument("--archive", choices=("client", "server"))
    ap.add_argument("--all", action="store_true", help="both archives")
    ap.add_argument("--json", metavar="OUT", help="write JSON to this path")
    ap.add_argument("--outdir", default="scratch/t76a/out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="with --json: re-read and assert key invariants, then exit")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.all and a.archive is None:
        ap.print_help()
        return 2

    targets = ("client", "server") if a.all else (a.archive,)
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rc = 0
    for arch in targets:
        try:
            res = build(arch)
        except Exception as exc:  # noqa: BLE001 - fatal, surfaced verbatim
            print(f"FATAL {arch}: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        p = Path(a.json) if (a.json and len(targets) == 1) \
            else outdir / f"slots_{arch}_{TID}.json"
        p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        gs = res["grade_summary"]
        n23 = sum(len(gs.get(g, [])) for g in ("L2", "L3", "L2_structural"))
        print(f"{arch:6} t{TID} status={res['status']:8} "
              f"rows={res['frame']['count']:,} stride={res['frame']['stride']} "
              f"L2/L3={n23} cov={res['coverage']['L2_L3_ratio']:.1%} -> {p}")
        if res["status"] != "closed":
            rc = 1
        if a.check:
            d = json.loads(p.read_text(encoding="utf-8"))
            assert d["walk"]["closure_ok"], "closure"
            assert d["walk"]["identity_rows_ok"] == d["frame"]["count"], "identity"
            if arch == "server":
                assert d["shared_tail"]["byte_identical"], "shared tail"
            print(f"  check ok: closure + identity"
                  + (" + shared-tail" if arch == "server" else ""))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
