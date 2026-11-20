#!/usr/bin/env python3
"""Build t72: unnamed/held physical slot inventory + data-side value fingerprints.

Scope: pure data side. Three main tables (club table_3, comp table_25, nation table_10),
both archive modes. No exe static claim is made here; every statement is either
L1 (self-check) or L2 (independent fact cross-check against frozen digests) or a
candidate shape description.

Inputs are read-only:
  scratch/t57/out/field_slots.json + field_map.json      (club 34 slots)
  scratch/t59/out/field_slots.json + field_map.json      (comp 82 slots)
  scratch/t55/out/field_slots.json + field_map.json      (nation 40 slots)
  scratch/t63|t64|t65/out/field_map_r2.json              (per-occurrence grade)
  scratch/t66/out/collections.json                        (closed collection grammars)
  reports/club_nation_subtable_schema.json                (schema v10 L3 claims)

Replay is driven by the frozen field_slots metadata (envelope geometry, slot
types/widths, item widths, per-side execution order) and never by blind raw
scanning. Identity triples are re-derived per row and compared with the frozen
digests before any fingerprint is emitted.

Usage:
  py -V:3.12 -I -B scripts/t72_slot_fingerprint.py --selftest
  FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scripts/t72_slot_fingerprint.py
Exit codes: 0 success, 1 check failed, 2 usage/fatal.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
from hashlib import sha256
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t72/out"
WORK = ROOT / "scratch/t72/work"
sys.path.append(str(ROOT.parent / "fm24/tools/python"))

HEAD = bytes.fromhex("03017461642ef10d")
ALLOWED_SIDES = ("client", "server")
TABLES = {"club": 3, "comp": 25, "nation": 10}
IDENT = {"club": bytes.fromhex("0000000001e3c03a77"),
         "comp": bytes.fromhex("00000000014ec43a77"),
         "nation": bytes.fromhex("0000000001ec7ae404")}


class Check(Exception):
    """An evidence check failed (exit code 1)."""


def require(ok, detail):
    if not ok:
        raise Check(detail)


def H(x):
    return sha256(x if isinstance(x, (bytes, bytearray)) else bytes(x)).hexdigest()


def jload(rel):
    return json.loads((ROOT / rel).read_bytes())


def u(b, p=0):
    return struct.unpack_from("<I", b, p)[0]


# --------------------------------------------------------------------------- payloads
def load_payloads():
    """Reuse scripts/fm24_dump.py load_payload (runpy, unmodified)."""
    import runpy
    env = os.environ.get("FM24_DB_DIR")
    require(bool(env), "FM24_DB_DIR must be set (no Z: fallback in this task)")
    dump = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"), run_name="t72_dump")
    codec = dump["_reader"]()
    out = {}
    for side in ALLOWED_SIDES:
        for name, tid in TABLES.items():
            if tid == 24 and side == "client":
                continue
            out[side, name] = dump["load_payload"](codec, side, tid)
        out[side, "t2"] = dump["load_payload"](codec, side, 2)
        out[side, "t5"] = dump["load_payload"](codec, side, 5)
        out[side, "t21"] = dump["load_payload"](codec, side, 21)
        out[side, "t23"] = dump["load_payload"](codec, side, 23)
    out["server", "t24"] = dump["load_payload"](codec, "server", 24)
    return out


# --------------------------------------------------------------------------- replays
def replay_club(b, side):
    """CLUB main-row cursor. Grammar driven by field_slots positions/types/widths."""
    cols = {}

    def add(k, i, p, w):
        cols.setdefault(k, []).append((i, p, w))

    n = u(b, 8)
    foot = len(b) - 9
    q = 13
    ids = []
    spans = []
    for o in range(n):
        start = q
        add("selector", o, q, 1)
        sel = b[q]
        q += 1
        require(sel in (0, 12), (side, o, "selector", sel))
        if sel:
            add("derived_170", o, q, 4)
            q += 4
            add("derived_178", o, q, 1)
            q += 1
        for k in ("ref_d8", "ref_e0", "ref_e8", "ref_f0", "ref_f8"):
            add(k, o, q, 4)
            q += 4
        add("flags160", o, q, 6)
        q += 6
        for lk, bk in (("name_len", "name_bytes"), ("short_len", "short_bytes")):
            at = q
            add(lk, o, at, 4)
            q += 4
            L = u(b, at)
            require(q + L <= foot, (side, o, lk, L))
            if L:
                add(bk, o, q, L)
                q += L
        if side == "server":
            for k, w in (("raw16a", 1), ("raw166", 2), ("person148", 4), ("raw16c", 1)):
                add(k, o, q, w)
                q += w
            for k, cw, iw in (("vec110", 1, 4),):
                at = q
                cnt = struct.unpack_from("<b", b, at)[0]
                require(cnt >= 0 and q + cw + cnt * iw <= foot, (side, o, k, cnt))
                q += cw + cnt * iw
                add(k, o, at, q - at)
            add("obj150_tag", o, q, 1)
            tag = b[q]
            q += 1
            if tag == 0:
                add("obj150", o, q, 45)
                q += 45
            elif tag != 2:
                raise Check((side, o, "obj150 tag", tag))
            for k, cw, iw in (("vec130", 1, 24), ("vec138", 1, 12)):
                at = q
                cnt = struct.unpack_from("<b", b, at)[0]
                require(cnt >= 0 and q + cw + cnt * iw <= foot, (side, o, k, cnt))
                q += cw + cnt * iw
                add(k, o, at, q - at)
            for k, w in (("raw168", 2), ("stad140", 4)):
                add(k, o, q, w)
                q += w
        for k, w in (("base_ba", 1), ("base_b8", 2)):
            add(k, o, q, w)
            q += w
        if side == "server":
            for k, cw, iw, signed in (("base18", 1, 4, False), ("base30", 1, 4, False),
                                      ("base60", 1, 4, True), ("base78", 1, 4, True),
                                      ("base90", 1, 4, False), ("base48", 1, 16, False),
                                      ("basea8", 2, 28, True)):
                at = q
                cnt = int.from_bytes(b[at:at + cw], "little", signed=signed)
                require(0 <= cnt and q + cw + cnt * iw <= foot, (side, o, k, cnt))
                q += cw + cnt * iw
                add(k, o, at, q - at)
        at = q
        add("identity", o, at, 12)
        q += 12
        got, a, c = struct.unpack_from("<III", b, at)
        require(got == o and a == c and a > (ids[-1] if ids else 0), (side, o, "identity"))
        ids.append(a)
        spans.append((start, q, a))
    require(q == foot and b[q:] == IDENT["club"], (side, "club footer", q, len(b)))
    return cols, spans, ids


COMP_FIXED = ["selector", "m15c", "m15d", "colour_tag", "m120", "m124", "m128", "m12c",
              "m130", "m134", "m1a0", "m1a2", "m1a3", "m1a4", "m1a5", "stat_a_tag",
              "m198", "m199", "m19a", "m19b", "m19c", "m19d", "m19e", "stat_b_tag",
              "m189_197", "mf6", "m138", "m13c", "m58", "m60", "m70", "m68", "m150"]
COMP_FIXED_W = [1] * 4 + [2] * 5 + [1] * 15 + [15, 1] + [4] * 6 + [2]
COMP_EXT = ["m180", "mb8", "m188", "m184", "m186", "m182", "m160", "m168", "m170", "m178"]
COMP_EXT_W = [2, 4, 1, 2, 2, 2, 8, 8, 8, 8]
COMP_SUF = ["m148", "m152", "m154", "m156", "m158", "m15a", "m80", "m88", "m90", "m98",
            "wbcl_present"]
COMP_SUF_W = [4, 2, 2, 2, 2, 2, 4, 4, 4, 4, 1]


def replay_comp(b, side):
    server = side == "server"
    cols = {}

    def add(k, i, p, w):
        cols.setdefault(k, []).append((i, p, w))

    n = u(b, 8)
    q = 13
    spans = []
    ids = []
    for i in range(n):
        start = q

        def tr(k, w):
            nonlocal q
            p = q
            require(p + w <= len(b) - 9, (side, i, k, p, w))
            q += w
            add(k, i, p, w)
            return int.from_bytes(b[p:q], "little")

        vals = [tr(k, w) for k, w in zip(COMP_FIXED, COMP_FIXED_W, strict=True)]
        require(vals[0] == 0 and vals[3] == 1 and vals[10] != 4 and vals[15] == 2 and vals[23] == 3,
                (side, i, "fixed revision tags"))
        if server:
            for k, w in zip(COMP_EXT, COMP_EXT_W, strict=True):
                tr(k, w)
            p = q
            m = u(b, p)
            require(4 + 2 * m <= len(b) - 9 - q, (side, i, "vec30", m))
            q += 4 + 2 * m
            add("vec30", i, p, q - p)
            if tr("a8_present", 1):
                ver = b[q]
                tr("obj_a8", 1 + 32 + 4 * (ver >= 2) + 9 + (2 if ver >= 3 else 1) + 8)
            for k, w in (("mf0", 4), ("m1a1", 1), ("m1a8", 1), ("mf4", 1), ("mf5", 1)):
                tr(k, w)
            if tr("e0_present", 1):
                require(tr("obj_e0", 4) == 0, (side, i, "e0 payload"))
            p = q
            m = struct.unpack_from("<i", b, p)[0]
            require(0 <= m < (len(b) - p) // 7, (side, i, "vec18", m))
            q += 4
            for _ in range(m):
                q += 8 + (struct.unpack_from("<b", b, q)[0] >= 2)
            add("vec18", i, p, q - p)
            if tr("e8_present", 1):
                p = q
                m = u(b, p + 4)
                require(m < (len(b) - p) // 8, (side, i, "e8", m))
                q += 8
                for _ in range(m):
                    ver = struct.unpack_from("<h", b, q)[0]
                    q += 10 + (ver >= 2) + (ver >= 3)
                add("obj_e8", i, p, q - p)
            if tr("c0_present", 1):
                p = q
                m = u(b, p + 1)
                require(m < (len(b) - p) // 6, (side, i, "e0 outer", m))
                q += 5
                for _ in range(m):
                    q += 6 + 12 * u(b, q + 2)
                add("obj_c0", i, p, q - p)
            if tr("c8_present", 1):
                tr("obj_c8", 25)
            tr("m1a7", 1)
            if tr("d0_present", 1):
                tr("obj_d0", 15)
            if tr("d8_present", 1):
                tr("obj_d8", 15)
            m = struct.unpack_from("<h", b, q)[0]
            require(m >= 0, (side, i, "vec100"))
            tr("vec100", 2 + 5 * m)
        tail = []
        for k, w in zip(COMP_SUF, COMP_SUF_W, strict=True):
            tail.append(tr(k, w))
        if tail[-1]:
            tr("m14c", 2)
        for k, w in (("m140", 4), ("m144", 4), ("mf7", 1), ("mf8", 1), ("mf9", 1)):
            tr(k, w)
        at = q
        j, uid, rep = struct.unpack_from("<III", b, at)
        tr("identity", 12)
        require(j == i and uid == rep and uid > (ids[-1] if ids else 0), (side, i, "identity"))
        ids.append(uid)
        spans.append((start, q, uid))
    require(b[q:] == IDENT["comp"], (side, "comp footer", q, len(b)))
    return cols, spans, ids


NAT_W = [1, 4, 2, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4, 1, 1, 4, 1, 1,
         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 1, 12]
NAT_COLL = {2: ("h", 4), 3: ("i", 4), 4: ("h", None), 11: ("i", None), 12: ("I", 12),
            13: ("I", 14), 23: ("b", 5), 24: ("i", 28), 25: ("i", 28), 26: ("i", 12)}


def replay_nation(b, side):
    server = side == "server"
    order = list(range(40)) if server else [0, *range(14, 27), 39]
    n = u(b, 8)
    pos = 13
    rows = []
    ids = []
    for r in range(n):
        start = pos
        row = {}
        for k in order:
            a = pos
            w = NAT_W[k]
            require(a + w <= len(b) - 9, (side, r, k, "short fixed"))
            pos += w
            if k in NAT_COLL:
                code, iw = NAT_COLL[k]
                cnt = struct.unpack_from("<" + code, b, a)[0]
                if k == 4:  # u8 tag + 4 x (u32 len + bytes) + 4B packed date + 4 x 4B
                    require(0 <= cnt <= (len(b) - 9 - pos) // 37, (side, r, "Nftb", cnt))
                    for _ in range(cnt):
                        pos += 1
                        for _f in range(4):
                            require(pos + 4 <= len(b) - 9, (side, r, "Nftb len"))
                            L = u(b, pos)
                            pos += 4 + L
                            require(pos <= len(b) - 9, (side, r, "Nftb str"))
                        pos += 20
                elif k == 11:  # tag < 2 -> 23B else 25B
                    require(0 <= cnt <= (len(b) - 9 - pos) // 23, (side, r, "Ntxr", cnt))
                    for _ in range(cnt):
                        require(pos < len(b) - 9, (side, r, "Ntxr tag"))
                        tag = b[pos]
                        pos += 25 if tag >= 2 else 23
                else:
                    require(0 <= cnt <= (len(b) - 9 - pos) // iw, (side, r, k, cnt))
                    pos += cnt * iw
            require(pos <= len(b) - 9, (side, r, k, pos))
            row[k] = (a, pos - a, cnt if k in NAT_COLL else None)
        ia = row[39][0]
        i, uid, rep = struct.unpack_from("<III", b, ia)
        require(b[start] == 0 and i == r and uid == rep and uid != 0, (side, r, "identity"))
        ids.append(uid)
        rows.append((start, pos, row))
    require(b[pos:] == IDENT["nation"], (side, "nation footer", pos, len(b)))
    cols = {}
    for r, (_, _, row) in enumerate(rows):
        for k, (a, w, _cnt) in row.items():
            cols.setdefault(k, []).append((r, a, w))
    spans = [(s, e, ids[i]) for i, (s, e, _r) in enumerate(rows)]
    return cols, spans, ids


# --------------------------------------------------------------------------- targets
def identity_tails(b, stride, n, lead=13):
    """Fixed-stride target rows: identity triple is the last 12 bytes of each row."""
    require(lead + stride * n + 9 == len(b), ("fixed target geometry", len(b), stride, n))
    pts = [lead + stride * (i + 1) - 12 for i in range(n)]
    return pts


def target_domains(raw, club_ids, nation_ids, comp_ids_client, comp_ids_server):
    """live ordinal set + UID set for every FK target, each cross-checked by digest."""
    domains = {}

    def put(tid, side, uids, method):
        arr = np.asarray(uids, dtype=np.uint64)
        require(len(arr) == len(set(int(x) for x in arr)), (tid, side, "uid uniqueness"))
        domains.setdefault(str(tid), {})[side] = {
            "count": len(uids), "method": method,
            "identity_sha256": H(b"".join(struct.pack("<III", i, v, v) for i, v in enumerate(uids))),
            "ordinals": np.arange(len(uids), dtype=np.uint64),
            "uids": arr,
        }

    put(3, "client", club_ids, "t72 club replay identity triples")
    put(3, "server", club_ids, "t72 club replay identity triples")
    put(10, "client", nation_ids, "t72 nation replay identity triples")
    put(10, "server", nation_ids, "t72 nation replay identity triples")
    put(25, "client", comp_ids_client, "t72 comp replay identity triples")
    put(25, "server", comp_ids_server, "t72 comp replay identity triples")

    for side in ALLOWED_SIDES:
        b = raw[side, "t2"]
        uids = []
        for at in identity_tails(b, 43, 56293):
            i, v, r = struct.unpack_from("<III", b, at)
            require(v == r and v != 0xFFFFFFFF, (side, "t2 identity"))
            uids.append(v)
        put(2, side, uids, "fixed 43 B row identity tails")

        b = raw[side, "t5"]
        uids = []
        for at in identity_tails(b, 34 if side == "client" else 48, 7):
            i, v, r = struct.unpack_from("<III", b, at)
            require(v == r, (side, "t5 identity"))
            uids.append(v)
        put(5, side, uids, "fixed row identity tails (34 B client / 48 B server)")

        b = raw[side, "t21"]
        uids = []
        for at in identity_tails(b, 38 if side == "client" else 181, 48413):
            i, v, r = struct.unpack_from("<III", b, at)
            require(v == r, (side, "t21 identity"))
            uids.append(v)
        put(21, side, uids, "fixed 38/181 B row identity tails")

        b = raw[side, "t23"]
        require(len(b) == 13 + 14 * 278 + 9, (side, "t23 geometry"))
        uids = []
        for i in range(278):
            at = 13 + 14 * i + 2
            x, v, r = struct.unpack_from("<III", b, at)
            require(x == i and v == r, (side, "t23 identity"))
            uids.append(v)
        put(23, side, uids, "fixed 14 B rows, identity at row+2 (t66 witness form)")

    # t24 team: server only; ordered identity path over repeated triples.
    b = raw["server", "t24"]
    n = u(b, 8)
    g = [[] for _ in range(n)]
    end = len(b) - 9
    for shift in range(4):
        a = np.frombuffer(b, dtype="<u4", offset=shift, count=(len(b) - shift) // 4)
        for x in np.flatnonzero((a[:-2] < n) & (a[1:-1] == a[2:])).tolist():
            at = 4 * x + shift
            i, uid = int(a[x]), int(a[x + 1])
            if at >= 14 and at + 12 <= end and uid:
                if uid > u(b, len(b) - 4) or (i < n - 1 and b[at + 12] not in (10, 11)):
                    continue
                if i != n - 1 or at + 12 == end:
                    g[i].append((at, uid))
    links, nxt = [], []
    for i in range(n - 1, -1, -1):
        d, here = {}, []
        for at, uid in g[i]:
            if i == n - 1:
                d[at] = None
                here.append((at, uid, 1))
                continue
            tot = 0
            for z, v, c in nxt:
                if z >= at + 12 + 1 and uid < v:
                    tot = min(2, tot + c)
                    d[at] = z
                    if tot >= 2:
                        break
            if tot:
                here.append((at, uid, tot))
        links.append(d)
        nxt = here
        require(bool(nxt), ("t24 identity path dead", i))
    require(sum(c for _, _, c in nxt) == 1, "t24 identity path not unique")
    at = nxt[0][0]
    pts = []
    for m in reversed(links):
        pts.append(at)
        at = m[at]
    uids = []
    for i, at in enumerate(pts):
        x, v, r = struct.unpack_from("<III", b, at)
        require(x == i and v == r, ("t24 triple", i))
        uids.append(v)
    put(24, "server", uids, "unique forward/backward ordered identity path (t66 form)")
    return domains


TARGET_META = {
    2: ("city", 56293), 3: ("club", 84259), 5: ("continent", 7), 10: ("nation", 251),
    21: ("stadium", 48413), 23: ("stgn", 278), 24: ("team", 84507), 25: ("comp", 7047),
}


# --------------------------------------------------------------------------- fingerprints
def extract(b, cells, w):
    arr = np.frombuffer(b, dtype=np.uint8)
    abs_ = np.fromiter((c[1] for c in cells), dtype=np.int64, count=len(cells))
    val = arr[abs_].astype(np.uint64)
    for k in range(1, w):
        val |= arr[abs_ + k].astype(np.uint64) << np.uint64(8 * k)
    return abs_, val


def sample(b, cells, idx):
    i, p, w = cells[idx]
    return {"row": i, "absolute": p, "width": w, "raw": b[p:p + min(w, 40)].hex()}


def hist_of(vals, cap=24):
    uniq, cnt = np.unique(vals, return_counts=True)
    order = np.argsort(-cnt, kind="stable")
    keep = order[:cap]
    out = {str(int(uniq[k])): int(cnt[k]) for k in keep}
    return out, int(len(uniq) - len(keep))


def interp(vals, w):
    """All width-compatible interpretations; signedness is never adjudicated."""
    out = {}
    low8 = (vals & np.uint64(0xFF)).astype(np.int64)
    out["u8"] = {"min": int(low8.min()), "max": int(low8.max())}
    out["i8"] = {"min": int(((low8 + 128) % 256 - 128).min()),
                 "max": int(((low8 + 128) % 256 - 128).max())}
    if w >= 2:
        low16 = (vals & np.uint64(0xFFFF)).astype(np.int64)
        out["u16"] = {"min": int(low16.min()), "max": int(low16.max())}
        out["i16"] = {"min": int(((low16 + 32768) % 65536 - 32768).min()),
                      "max": int(((low16 + 32768) % 65536 - 32768).max())}
    if w >= 4:
        low32 = (vals & np.uint64(0xFFFFFFFF)).astype(np.uint32)
        s32 = low32.astype(np.int32)
        f32 = low32.view(np.float32)
        finite = f32[np.isfinite(f32)]
        out["u32"] = {"min": int(low32.min()), "max": int(low32.max())}
        out["i32"] = {"min": int(s32.min()), "max": int(s32.max())}
        out["f32"] = {"min": (float(finite.min()) if finite.size else None),
                      "max": (float(finite.max()) if finite.size else None),
                      "non_finite": int(f32.size - finite.size)}
    if w >= 8:
        out["u64"] = {"min": int(vals.min()), "max": int(vals.max())}
    return out


def fk_applies(vals, w):
    """Trivial-containment guard.

    A slot whose whole value range is much smaller than a target table's ordinal
    space is contained in *every* target by construction, so a 1.000 ordinal hit
    carries no information. Probes only run when the observed maximum is large
    enough (>=1000) and the width can express a real index (>=2 B).
    """
    if w < 2:
        return {"ok": False,
                "why": "1 B slot: value range < 256 cannot discriminate any target table"}
    if int(np.unique(vals).size) < 2:
        return {"ok": False,
                "why": f"constant slot (one distinct value): zero discriminating power, "
                       f"any hit would be an artefact of the constant"}
    live = vals[vals != np.uint64(0xFFFFFFFF)] if w >= 4 else vals
    if not live.size:
        return {"ok": False, "why": "every value is the 0xffffffff sentinel: no live index to probe"}
    mx = int(live.max())
    if mx < 1000:
        return {"ok": False,
                "why": f"observed max {mx} < 1000: every target ordinal set contains it "
                       f"trivially, so an ordinal hit would be vacuous"}
    return {"ok": True}


def range_only(vals, w, allow_team):
    """Range-only compatibility: an ordinal into a table with n rows must satisfy v < n.

    Reports which targets are *not excluded* by the observed upper bound alone.
    This is a necessary condition, never a hit and never a claim.
    """
    live = vals[vals != np.uint64(0xFFFFFFFF)] if w >= 4 else vals
    if not live.size:
        return {"live_max": None, "compatible": []}
    mx = int(live.max())
    compat = []
    for tid in (2, 3, 5, 10, 21, 23, 24, 25):
        if tid == 24 and not allow_team:
            continue
        if TARGET_META[tid][1] > mx:
            compat.append({"target_table": tid, "name": TARGET_META[tid][0],
                           "count": TARGET_META[tid][1]})
    return {"live_max": mx, "compatible": compat,
            "note": "ordinal(v) needs v < n; a target with n <= observed max is excluded, "
                    "a target with n > observed max is only not-excluded"}


def fk_block(vals, w, domains, allow_team):
    """Ordinal-set and UID-set hit counts per target; sentinels excluded and reported."""
    sentinel = np.uint64(0xFFFFFFFF)
    low32 = vals & np.uint64(0xFFFFFFFF)
    probe = low32 if w >= 4 else vals
    live = probe[probe != sentinel] if w >= 4 else probe
    res = {}
    for tid in (2, 3, 5, 10, 21, 23, 24, 25):
        entry = {}
        for side in ALLOWED_SIDES:
            dom = domains[str(tid)].get(side)
            if dom is None:
                entry[side] = None
                continue
            if tid == 24 and not allow_team:
                entry[side] = {"note": "t24 has no client member; only server live set exists"}
                continue
            ords, uids = dom["ordinals"], dom["uids"]
            o_hit = int(np.isin(live, ords).sum()) if live.size else 0
            u_hit = int(np.isin(live, uids).sum()) if live.size else 0
            # Vacuity: if the target's ordinal space is wider than what w bytes can
            # express, every possible value lands inside it by construction.
            vacuous = dom["count"] > (1 << (8 * min(w, 8))) - 1
            entry[side] = {
                "live": int(live.size),
                "ordinal_hits": o_hit,
                "ordinal_ratio": (round(o_hit / live.size, 6) if live.size else None),
                "uid_hits": u_hit,
                "uid_ratio": (round(u_hit / live.size, 6) if live.size else None),
                "ordinal_hit_vacuous": bool(vacuous),
            }
            if vacuous:
                entry[side]["ordinal_note"] = (f"target n={dom['count']} exceeds the "
                                               f"{8 * w}-bit value space: ordinal hit is "
                                               f"containment, not evidence")
            # first ordinal miss / first uid miss witnesses
            if live.size and o_hit < live.size:
                miss = np.flatnonzero(~np.isin(live, ords))
                k = int(miss[0])
                entry[side]["first_ordinal_miss"] = {"value": int(live[k]),
                                                     "uid_of_that_ordinal": (int(uids[int(live[k])])
                                                                             if int(live[k]) < len(uids) else None)}
            if live.size and u_hit < live.size:
                miss = np.flatnonzero(~np.isin(live, uids))
                entry[side]["first_uid_miss"] = {"value": int(live[int(miss[0])])}
        res[str(tid)] = entry
    return res


def best_fk(fk, side):
    """Highest ordinal-ratio target for one side (shape hint only, not a claim)."""
    cand = [(v["ordinal_ratio"], int(t)) for t, e in fk.items()
            if (v := e.get(side)) and v.get("ordinal_ratio") is not None
            and not v.get("ordinal_hit_vacuous")]
    if not cand:
        return None
    r, t = max(cand)
    if r <= 0:
        return None
    return {"target_table": t, "ordinal_ratio": r,
            "uid_ratio": fk[str(t)][side].get("uid_ratio"),
            "name": TARGET_META[t][0], "count": TARGET_META[t][1]}


def hint(stats, fk, w, named, side):
    """One sentence on value shape only. No semantic naming."""
    if stats.get("rows", 0) == 0:
        return "本档不序列化:该槽位在冻结轨迹里 0 次事件"
    if "fixed_width" in stats and stats["fixed_width"] is None:
        ranges = stats.get("width_histogram") or {}
        return ("变长槽位(宽度直方图 " + str(ranges) +
                "):父跨度已闭合,内层项文法不在 field_slots 内,不做位宽解释")
    if stats.get("all_zero"):
        return "全零常量:该档全部行恒为 0,不携带索引或枚举信息"
    if stats.get("all_ones_ratio") and stats["all_ones_ratio"] > 0.99:
        return "全一哨兵主导:全部行等于本宽度全 1,与合法 0 分列统计"
    bits = []
    d = stats.get("distinct", 0)
    if d <= 12:
        bits.append(f"小枚举子集(distinct={d})")
    elif d <= 64:
        bits.append(f"窄值域(distinct={d})")
    else:
        bits.append(f"宽值域(distinct={d})")
    if w >= 4 and (stats.get("u32_max_live") or 0) > 100_000_000:
        bits.append("u32 高位活跃(哨兵之外值跨度 >1e8,形态上像指针/大整数,不裁决)")
    best = best_fk(fk, side) if fk else None
    ro = stats.get("range_only") or {}
    if stats.get("fk_skipped"):
        bits.append("外键命中率无判别力(" + stats["fk_skipped"].split(":")[0] + ")")
        if ro.get("compatible"):
            bits.append("值域上界 %s 只排除 n<=上界 的目标,未被排除: %s" %
                        (ro["live_max"], ",".join("t%d(%s,n=%d)" % (c["target_table"], c["name"], c["count"])
                                                  for c in ro["compatible"][:4])))
    if best and best["ordinal_ratio"] >= 0.9:
        uid = best["uid_ratio"] or 0.0
        bits.append(f"{side} 档值域落在 t{best['target_table']}({best['name']},n={best['count']}) "
                    f"ordinal 内 {best['ordinal_ratio']:.3f},同值当 UID 查命中 {uid:.3f}")
    if stats.get("all_ones_ratio") and 0.001 <= stats["all_ones_ratio"] < 0.99:
        bits.append(f"含全一哨兵 {stats['all_ones_ratio']:.3f}")
    return ";".join(bits)


def slot_fingerprint(b, cells, side, domains, kind, claim):
    if not cells:
        return {"rows": 0, "status": "not_serialized_in_mode"}
    widths = np.fromiter((c[2] for c in cells), dtype=np.int64, count=len(cells))
    fixed = int(widths[0]) if len(np.unique(widths)) == 1 else None
    w = fixed if fixed else int(widths.max())
    out = {"rows": len(cells), "bytes": int(widths.sum())}
    wh, wdrop = hist_of(widths)
    out["width_histogram"] = wh
    if wdrop:
        out["width_histogram_omitted_kinds"] = wdrop
    out["fixed_width"] = fixed
    abs_, vals = extract(b, cells, fixed or 1)
    if fixed:
        out["first"] = sample(b, cells, 0)
        out["last"] = sample(b, cells, -1)
        out["distinct"] = int(np.unique(vals).size)
        out["all_zero"] = bool(not vals.any())
        zeros = int((vals == 0).sum())
        out["zero_count"] = zeros
        out["zero_ratio"] = round(zeros / len(cells), 6)
        mask = (np.uint64(1) << np.uint64(8 * fixed)) - np.uint64(1) if fixed < 8 else np.uint64(0xFFFFFFFFFFFFFFFF)
        ones = int((vals == mask).sum())
        out["all_ones_count"] = ones
        out["all_ones_ratio"] = round(ones / len(cells), 6)
        if fixed >= 4:
            f32ones = int(((vals & np.uint64(0xFFFFFFFF)) == np.uint64(0xFFFFFFFF)).sum())
            out["count_0xffffffff"] = f32ones
            out["ratio_0xffffffff"] = round(f32ones / len(cells), 6)
        interp_out = interp(vals, fixed)
        out["interpretations"] = interp_out
        out["u32_max"] = interp_out.get("u32", {}).get("max")
        if fixed >= 4:
            live = vals[vals != np.uint64(0xFFFFFFFF)]
            out["u32_max_live"] = int(live.max()) if live.size else None
        h, dropped = hist_of(vals)
        out["value_histogram"] = h
        if dropped:
            out["value_histogram_omitted_kinds"] = dropped
        if fixed >= 8:
            lanes = []
            arr = np.frombuffer(b, dtype=np.uint8)
            for lane in range(fixed):
                lv = arr[abs_ + lane].astype(np.int64)
                lanes.append({"lane": lane,
                              "min": int(lv.min()), "max": int(lv.max()),
                              "distinct": int(np.unique(lv).size),
                              "all_zero": bool(not lv.any())})
            out["byte_lanes"] = lanes
        if fixed >= 2:
            out["range_only"] = range_only(vals, fixed, side == "server")
        if kind != "l3_claimed":
            gate = fk_applies(vals, fixed)
            out["fk_probe_applies"] = gate
            if gate["ok"]:
                out["fk"] = fk_block(vals, fixed, domains, side == "server")
                out["fk_best"] = {side: best_fk(out["fk"], side)}
            else:
                out["fk_skipped"] = gate["why"]
    else:
        out["first"] = sample(b, cells, 0)
        out["last"] = sample(b, cells, -1)
        out["distinct_widths"] = int(np.unique(widths).size)
        out["escalate_to_sol"] = {
            "item": f"{side} slot with non-constant width",
            "what_tried": "width histogram + first/last raw samples only",
            "blocker": "variable-length slot: numeric interpretations and FK probes need an item grammar, which field_slots does not provide for this key",
        }
    out["xref_hint"] = hint(out, out.get("fk") or {}, fixed or 0, bool(claim), side)
    return out


# --------------------------------------------------------------------------- classification
def club_claims():
    """slot key -> [(code, grade)] from t57 field_map + t63 r2 wires + schema v10."""
    claims = {}
    fm = jload("scratch/t57/out/field_map.json")
    pos_key = {s["position"]: s["key"] for s in jload("scratch/t57/out/field_slots.json")["slots"]}
    for f in fm["fields"]:
        if f["grade"] not in ("L3", "held"):
            continue
        p = f.get("accepted_position") if f.get("accepted_position") is not None else f.get("candidate_position")
        if p is None or p not in pos_key:
            continue
        claims.setdefault(pos_key[p], []).append((f["code"], f["grade"]))
    r2 = jload("scratch/t63/out/field_map_r2.json")
    for f in r2["fields"]:
        w = f.get("wire") or {}
        slot = w.get("r1_slot")
        if slot and f["grade"] == "L3":
            claims.setdefault(slot, []).append((f["code"], "L3"))
    return claims


def comp_claims():
    claims = {}
    fm = jload("scratch/t59/out/field_map.json")
    for f in fm["fields"]:
        g = f.get("grade") or f.get("status")
        if g not in ("L3", "held"):
            continue
        slot = f.get("slot")
        if slot:
            claims.setdefault(slot, []).append((f["code"], g))
    return claims


def nation_claims():
    """position -> [(code, grade)]. prior_collection / linked_parent_held stay named."""
    claims = {}
    fm = jload("scratch/t55/out/field_map.json")
    for f in fm["fields"]:
        slot = f.get("slot")
        if slot is None:
            continue
        g = f.get("grade") or f.get("status")
        claims.setdefault(int(slot), []).append((f["code"], g))
    return claims


# field_slots key <-> t66 collection name / presence slot (t66 verify NAMES table)
T66_KEYS = {
    "vec30": "vec30", "vec18": "vec18",
    "obj_a8": "+0xa8", "a8_present": "+0xa8",
    "obj_e0": "+0xe0", "e0_present": "+0xe0",
    "obj_e8": "+0xe8", "e8_present": "+0xe8",
    "obj_c0": "+0xc0", "c0_present": "+0xc0",
    "obj_c8": "+0xc8", "c8_present": "+0xc8",
    "obj_d0": "+0xd0", "d0_present": "+0xd0",
    "obj_d8": "+0xd8", "d8_present": "+0xd8",
    "vec100": "+0x100",
}


def closed_collections():
    """t66 grade per collection name (L3 = closed, held = still open)."""
    col = jload("scratch/t66/out/collections.json")["collections"]
    return {name: rec.get("grade") for name, rec in col.items()}


def schema_attribution(name):
    """How the XML field side splits, so nobody conflates it with the physical slot side."""
    r2key = {"club": "club_main_row_fields_r2", "comp": "comp_main_row_fields_r2",
             "nation": "nation_main_row_fields_r2"}[name]
    r1key = {"club": "club_main_row_fields", "comp": "comp_main_row_fields",
             "nation": "nation_main_row_fields"}[name]
    schema = jload("reports/club_nation_subtable_schema.json")
    r2 = schema[r2key]
    r1 = schema[r1key]
    out = {"r2_source_task": r2.get("source_task"), "r2_status": r2.get("status"),
           "r2_round2_reviewed": r2.get("round2_reviewed")}
    for k in ("round2_grade_counts", "round2_classification_counts", "prior_round_preserved"):
        if isinstance(r2.get(k), dict):
            out[k] = r2[k]
    for k in ("L3", "held", "unmapped", "fields_total", "fields"):
        if isinstance(r1.get(k), (int, str)):
            out[f"r1_{k}"] = r1[k]
    for k in ("L3", "held", "unmapped", "skipped"):
        for kk in (k, f"{k}_count", f"{k}_fields"):
            if isinstance(r1.get(kk), int):
                out[f"r1_{kk}"] = r1[kk]
    out["note"] = ("unmapped XML field count is not the unnamed physical slot count: an XML "
                   "field without a main-row wire slot has no physical slot to point at, and "
                   "several XML fields can share one packed slot")
    return out


# --------------------------------------------------------------------------- build
def build_selftest():
    """Executable self-check of the arithmetic and the classification helpers."""
    cells = [(0, 0, 4), (1, 4, 4), (2, 8, 4)]
    b = struct.pack("<III", 7, 0xFFFFFFFF, 0)
    abs_, vals = extract(b, cells, 4)
    require(vals.tolist() == [7, 0xFFFFFFFF, 0], "extract")
    it = interp(vals, 4)
    require(it["u32"]["max"] == 0xFFFFFFFF and it["i32"]["min"] == -1, "interp signedness")
    require(it["f32"]["non_finite"] == 1, "f32 nan count")
    require(hist_of(np.array([1, 1, 2]))[0] == {"1": 2, "2": 1}, "histogram")
    require(identity_tails(b"\0" * 13 + b"\1" * 43 + b"\0" * 9, 43, 1) == [44], "identity tail")
    h = hint({"rows": 5, "all_zero": True, "all_ones_ratio": 0.0, "distinct": 1,
              "u32_max": 0}, {}, 4, False, "client")
    require("全零" in h, "hint all zero")
    h = hint({"rows": 5, "all_zero": False, "all_ones_ratio": 0.5, "distinct": 9,
              "u32_max": 12}, {}, 4, False, "client")
    require("小枚举" in h, "hint enum")
    print("t72 builder selftest PASS")


def build():
    IN = {
        "scratch/t57/out/field_slots.json": None, "scratch/t57/out/field_map.json": None,
        "scratch/t59/out/field_slots.json": None, "scratch/t59/out/field_map.json": None,
        "scratch/t55/out/field_slots.json": None, "scratch/t55/out/field_map.json": None,
        "scratch/t63/out/field_map_r2.json": None, "scratch/t64/out/field_map_r2.json": None,
        "scratch/t65/out/field_map_r2.json": None, "scratch/t66/out/collections.json": None,
        "reports/club_nation_subtable_schema.json": None,
    }
    for k in IN:
        IN[k] = H((ROOT / k).read_bytes())

    fsc = jload("scratch/t57/out/field_slots.json")
    fsp = jload("scratch/t59/out/field_slots.json")
    fsn = jload("scratch/t55/out/field_slots.json")
    schema = jload("reports/club_nation_subtable_schema.json")
    raw = load_payloads()

    # --- replay both modes, cross-check identity + every frozen coordinate digest
    replay_meta = {}
    cols = {}
    ids = {}
    for side in ALLOWED_SIDES:
        b = raw[side, "club"]
        c, spans, club_ids = replay_club(b, side)
        env = fsc["envelopes"][side]
        require((env["rows"], env["header"], env["payload"], env["footer_at"]) ==
                (len(spans), 13, len(b), spans[-1][1]), (side, "club envelope"))
        require(env["footer"] == IDENT["club"].hex(), (side, "club footer bytes"))
        require(env["identity_census"]["identity_sha256"] ==
                H(b"".join(struct.pack("<III", i, v, v) for i, v in enumerate(club_ids))),
                (side, "club identity census digest"))
        rr = H(b"".join(struct.pack("<IIIB", s, e, a, b[s]) for s, e, a in spans))
        require(rr == env["row_trace_sha256"], (side, "club row trace digest"))
        for s in fsc["slots"]:
            cells = c.get(s["key"], [])
            prof = s["profiles"][side]
            if not cells:
                require(prof.get("rows") == 0 or prof.get("status") == "bypassed",
                        (side, s["key"], "unexpected empty slot"))
                continue
            require(H(b"".join(struct.pack("<III", i, p, w) for i, p, w in cells)) ==
                    prof["coordinate_sha256"], (side, s["key"], "frozen coordinate digest"))
        cols["club", side] = c
        ids["club", side] = club_ids
        replay_meta["club", side] = {"rows": len(spans), "payload": len(b), "start": spans[0][0],
                                     "end": spans[-1][1], "header": 13, "footer": 9,
                                     "identity_sha256": env["identity_census"]["identity_sha256"],
                                     "row_trace_sha256": rr, "coordinate_digests_matched":
                                     sum(1 for s in fsc["slots"] if s["profiles"][side].get("rows") or s["profiles"][side].get("coordinate_sha256"))}

        b = raw[side, "comp"]
        c, spans, comp_ids = replay_comp(b, side)
        env = fsp["envelopes"][side]
        require((env["count"], env["header"], env["payload"], env["footer"]) ==
                (len(spans), 13, len(b), 9), (side, "comp envelope"))
        rr = H(b"".join(struct.pack("<III", s, e, a) for s, e, a in spans))
        require(rr == env["row_trace_sha256"], (side, "comp row trace digest"))
        for s in fsp["slots"]:
            cells = c.get(s["key"], [])
            prof = s["profiles"][side]
            if not cells:
                require(prof.get("events") == 0, (side, s["key"], "unexpected empty slot"))
                continue
            require(H(b"".join(struct.pack("<III", i, p, w) for i, p, w in cells)) ==
                    prof["coordinate_sha256"], (side, s["key"], "frozen coordinate digest"))
        cols["comp", side] = c
        ids["comp", side] = comp_ids
        replay_meta["comp", side] = {"rows": len(spans), "payload": len(b), "header": 13,
                                     "footer": 9, "row_trace_sha256": rr,
                                     "uid_min": min(comp_ids), "uid_max": max(comp_ids)}

        b = raw[side, "nation"]
        c, spans, nat_ids = replay_nation(b, side)
        tgt = fsn["targets"][side]["10"]
        require(H(b"".join(struct.pack("<III", i, v, v) for i, v in enumerate(nat_ids))) ==
                tgt["identity_sha256"], (side, "nation identity digest"))
        require(len(nat_ids) == tgt["count"] == 251, (side, "nation count"))
        for s in fsn["slots"]:
            exp = s["coordinates"][side]
            got = [[p, w] for _r, p, w in c.get(s["position"], [])]
            require(got == exp, (side, "nation slot coordinate", s["position"]))
        cols["nation", side] = c
        ids["nation", side] = nat_ids
        replay_meta["nation", side] = {"rows": len(spans), "payload": len(b), "header": 13,
                                       "footer": 9, "body": spans[-1][1] - 13,
                                       "identity_sha256": tgt["identity_sha256"]}

    # to make the "identity triple" claim explicit, record the frozen-vs-replayed compare
    for side in ALLOWED_SIDES:
        require(ids["club", side] == ids["club", "client"], (side, "club uid parity"))
        require(ids["nation", side] == ids["nation", "client"], (side, "nation uid parity"))
    require(fsc["target_identity_domains"][side]["3"]["identity_sha256"] ==
            replay_meta["club", side]["identity_sha256"], "t57 club target digest")
    require(fssp_target_ok(fsc, replay_meta, ids), "t57/t59/t55 target digest agreement")

    domains = target_domains(raw, ids["club", "client"], ids["nation", "client"],
                             ids["comp", "client"], ids["comp", "server"])

    # --- authoritative target digests (frozen references)
    frozen_targets = {
        "t57": fsc["target_identity_domains"], "t55": fsn["targets"],
    }
    for tid in (2, 3, 10, 21, 23, 25):
        for side in ALLOWED_SIDES:
            dom = domains[str(tid)][side]
            ref = (frozen_targets["t57"][side].get(str(tid))
                   or frozen_targets["t55"][side].get(str(tid)))
            if ref:
                require(ref["identity_sha256"] == dom["identity_sha256"],
                        (tid, side, "frozen identity digest", ref["identity_sha256"][:12],
                         dom["identity_sha256"][:12]))
                require(ref["count"] == dom["count"], (tid, side, "frozen count"))
    t66 = jload("scratch/t66/out/collections.json")["extra_identity_domains"]
    require(t66["24"]["server_count"] == domains["24"]["server"]["count"], "t66 t24 count")
    require(t66["23"]["client_count"] == domains["23"]["client"]["count"], "t66 t23 count")

    # --- inventory + fingerprints
    inventory = {"generated_by": "scripts/t72_slot_fingerprint.py", "inputs_sha256": IN,
                 "grading": {"ceiling": "L2/candidate (data side only; no exe static claim)",
                             "L4": 0},
                 "targets": {str(t): {"entity": TARGET_META[t][0], "count": TARGET_META[t][1],
                                      "sides": sorted(domains[str(t)]),
                                      "identity_sha256": {s: domains[str(t)][s]["identity_sha256"]
                                                          for s in domains[str(t)]}}
                             for t in (2, 3, 5, 10, 21, 23, 24, 25)},
                 "replay": {f"{t}/{s}": v for (t, s), v in replay_meta.items()},
                 "tables": {}}
    fingerprints = {"generated_by": "scripts/t72_slot_fingerprint.py", "inputs_sha256": IN,
                    "grading_ceiling": "L2/candidate", "L4": 0, "targets": inventory["targets"],
                    "tables": {}}
    escalations = []

    cclaims = club_claims()
    pclaims = comp_claims()
    nclaims = nation_claims()
    t66_grade = closed_collections()
    IDENT_SLOT = {"club": "identity", "comp": "identity", "nation": "39"}
    NAMED_NOT_L3 = ("held", "prior_collection", "linked_parent_held", "prior_identity")

    for name, fs, claims in (("club", fsc, cclaims), ("comp", fsp, pclaims),
                             ("nation", fsn, nclaims)):
        slots_out = []
        fp_out = []
        counts = {"l3_claimed": 0, "held": 0, "unnamed": 0, "collection_closed": 0,
                  "identity_envelope": 0}
        for idx, s in enumerate(fs["slots"]):
            pos = s.get("position", idx)
            key = s.get("key") if name != "nation" else f"slot_{pos}"
            colkey = pos if name == "nation" else key
            cl = claims.get(pos if name == "nation" else key, [])
            l3 = [c for c, g in cl if g == "L3"]
            rest = [(c, g) for c, g in cl if g != "L3"]
            t66 = t66_grade.get(T66_KEYS.get(key, ""), None) if name == "comp" else None
            if name == "comp" and (t66 == "L3" or key in ("vec18", "vec100")):
                kind = "collection_closed"
            elif (key == IDENT_SLOT[name] or s.get("type") == "identity") and not l3:
                kind = "identity_envelope"
            elif l3:
                kind = "l3_claimed"
            elif rest:
                kind = "held"
            else:
                kind = "unnamed"
            rec = {
                "position": pos, "key": key, "kind": kind,
                "slot_type": s.get("type"),
                "nominal_width": s.get("width") or s.get("nominal_width"),
                "object_displacement": s.get("object_displacement") or s.get("object_offset"),
                "execution_index": s.get("execution_index"),
                "coverage": {side: len(cols[name, side].get(colkey, [])) for side in ALLOWED_SIDES},
                "claims": [{"code": c, "grade": g} for c, g in cl],
                "grade_raw": sorted({g for _c, g in cl}),
                "site": s.get("site"),
            }
            if name == "comp" and t66:
                rec["t66_collection_grade"] = t66
            if kind == "collection_closed":
                rec["already_closed_by"] = "t66"
            if name == "club" and key == "obj150":
                r2 = jload("scratch/t63/out/field_map_r2.json")
                lanes = [{"code": f["code"], "lane": (f.get("wire") or {}).get("lane"),
                          "codec": (f.get("wire") or {}).get("codec")}
                         for f in r2["fields"] if (f.get("wire") or {}).get("r1_slot") == "obj150"]
                rec["claimed_members"] = sorted(lanes, key=lambda x: (x["lane"] is None, x["lane"]))
                rec["partial"] = True
                rec["note"] = ("opaque 45 B subobject; t63 gives 8 tag-0 member lanes L3; "
                               "the other 37 byte lanes stay unnamed (see fingerprints obj150)")
            if name == "nation" and s.get("collection"):
                rec["collection"] = s["collection"]
                rec["scope"] = s.get("scope")
                rec["item_grammar"] = "not in field_slots (count span only)"
            if s.get("item_width") and s.get("type") in ("count_i8", "count_u8", "count_i16"):
                rec["item_width"] = s["item_width"]
            if key in ("selector",):
                rec["role"] = "loader envelope selector, not a schema field"
            if kind == "identity_envelope":
                rec["role"] = "12 B ordinal+UID+repeat identity tail (closed; not a business slot)"
            slots_out.append(rec)
            counts[kind] += 1

            if kind in ("unnamed", "held"):
                entry = {"position": pos, "key": key, "kind": kind,
                         "named_fields": [c for c, _g in cl],
                         "grade_raw": sorted({g for _c, g in cl}),
                         "slot_type": s.get("type")}
                for side in ALLOWED_SIDES:
                    entry[side] = slot_fingerprint(raw[side, name], cols[name, side].get(colkey, []),
                                                   side, domains, kind, bool(cl))
                if s.get("collection"):
                    entry["collection"] = s["collection"]
                    entry["escalate_to_sol"] = {
                        "item": f"nation slot {pos} ({s['collection']['name']}) inner item grammar",
                        "what_tried": "parent count span replayed and matched t55 coordinates exactly; "
                                      "only the parent span is fingerprintable",
                        "blocker": "variable-length inner record (A/B/C/D segment); fingerprinting "
                                   "items would need an item grammar the frozen artifacts do not carry",
                    }
                    escalations.append({"table": name, "slot": key,
                                        "collection": s["collection"]["name"],
                                        "kind": "inner_item_grammar",
                                        "why": entry["escalate_to_sol"]["blocker"]})
                fp_out.append(entry)
        inventory["tables"][name] = {"table_id": TABLES[name], "slots": slots_out,
                                     "kind_counts": counts,
                                     "schema_attribution": schema_attribution(name)}
        fingerprints["tables"][name] = {"table_id": TABLES[name], "slots": fp_out}

    # club obj150 partial: fingerprint the unnamed lanes as a derived entry
    obj = next(s for s in fsc["slots"] if s["key"] == "obj150")
    for side in ALLOWED_SIDES:
        cells = cols["club", side].get("obj150", [])
        if not cells:
            continue
        r2 = jload("scratch/t63/out/field_map_r2.json")
        claimed = {(f.get("wire") or {}).get("lane") for f in r2["fields"]
                   if (f.get("wire") or {}).get("r1_slot") == "obj150"}
        arr = np.frombuffer(raw[side, "club"], dtype=np.uint8)
        abs_ = np.fromiter((c[1] for c in cells), dtype=np.int64, count=len(cells))
        lanes = []
        for lane in range(45):
            lv = arr[abs_ + lane].astype(np.int64)
            lanes.append({"lane": lane, "claimed_by_l3": lane in claimed,
                          "min": int(lv.min()), "max": int(lv.max()),
                          "distinct": int(np.unique(lv).size), "all_zero": bool(not lv.any())})
        fp = fingerprints["tables"]["club"]["slots"]
        tgt = next((e for e in fp if e["key"] == "obj150"), None)
        if tgt is None:
            tgt = {"position": 19, "key": "obj150", "kind": "l3_claimed", "partial": True,
                   "named_fields": ["Ccba", "Cadm", "Cesd", "Ceed", "Cead", "CteA", "Chaf", "Cmtp"]}
            fp.append(tgt)
        tgt[side] = {"rows": len(cells), "bytes": int(45 * len(cells)),
                     "fixed_width": 45, "byte_lanes": lanes,
                     "unclaimed_lanes": [l["lane"] for l in lanes if not l["claimed_by_l3"]]}

    inventory["escalations"] = escalations
    inventory["negative_notes"] = [
        "joined/destructured collections (comp t66, nation A/B/C/D) are skipped by design, not by failure",
        "no exe static site is asserted here; every ratio below is a data-shape statistic",
        "ordinal hit != UID hit: both are reported for every target and neither is a semantic claim",
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "inventory.json").write_text(json.dumps(inventory, indent=1, sort_keys=False) + "\n",
                                        encoding="utf-8")
    (OUT / "fingerprints.json").write_text(json.dumps(fingerprints, indent=1, sort_keys=False) + "\n",
                                          encoding="utf-8")
    print("wrote", OUT / "inventory.json")
    print("wrote", OUT / "fingerprints.json")
    for name in ("club", "comp", "nation"):
        c = inventory["tables"][name]["kind_counts"]
        print(f"  {name}: l3={c['l3_claimed']} held={c['held']} unnamed={c['unnamed']} "
              f"collection_closed={c['collection_closed']}")


def fssp_target_ok(fsc, replay_meta, ids):
    return (fsc["target_identity_domains"]["client"]["3"]["identity_sha256"] ==
            replay_meta["club", "server"]["identity_sha256"])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="run the arithmetic self-check only")
    args = ap.parse_args()
    try:
        if args.selftest:
            build_selftest()
            return 0
        build()
        return 0
    except Check as e:
        print("CHECK:", e, file=sys.stderr)
        return 1
    except Exception as e:  # fatal
        print("FATAL:", type(e).__name__, e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
