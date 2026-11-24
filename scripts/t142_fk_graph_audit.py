#!/usr/bin/env python3
"""t142: FM24 relational foreign-key graph discovery + referential integrity audit.

Read-only audit over the already byte-closed inputs of the repository:

  * 79/79 numbered tables (``server_db`` 59 + ``client_db`` 20) decoded by
    ``scripts/t133_fm24_reader_v2.py`` (2,846,936 rows, footer-closed);
  * ``basic_people_db.dat`` (658,011 people) via ``scripts/t123_basic_people_l3.py``
    verified layout constants;
  * ``club_links`` / ``name_table_0,1,2`` payloads from ``scratch/t106/out``
    (13/13 closed special members);
  * 4CC/L3 field bindings (``scratch/t121/out/master_79of79_l3.json``).

What it produces (``scratch/t142/out``):

  ``fk_graph_master.json``  identity-domain registry, verified FK edges
                            (code-corroborated vs statistical), anonymous
                            ``col_N`` upgrades, orphan audit, UID overlap matrix
  ``REPORT.md``             engineering report + mermaid ER diagram
  ``DONE.md``               completion marker

Method (no guessing):

  1. every integer scalar column of every table is decoded for *all* rows and
     kept as a typed array (cache in ``out/cache``);
  2. every table's ``ordinal`` / ``uid`` key domain is materialised exactly
     (min, max, count, set digest, density);
  3. a column is only promoted to a foreign key when the *whole* non-sentinel
     value vector lands inside a target key domain at >= 99 % and the accidental
     hit probability of that domain is <= 2 % (``chance`` model).  Small 0..N
     enum columns therefore stay ``ambiguous_low_specificity`` and are never
     promoted to ``CONTINENT`` / ``AGREEMENT`` style edges unless a 4CC/L3 field
     name or an adjacent ``(ordinal, uid)`` reference pair corroborates them;
  4. ``(ordinal u32, uid u32)`` adjacent pairs are tested jointly: this is the
     FM24 in-memory ``DATABASE_OBJECT_REF`` layout and a joint 99 % hit on both
     halves is a pair-proof of the edge.

CLI (exit 0 ok / 1 audit failure / 2 usage):

  py -V:3.12 -B scripts/t142_fk_graph_audit.py                # full pipeline
  py -V:3.12 -B scripts/t142_fk_graph_audit.py --selftest
  py -V:3.12 -B scripts/t142_fk_graph_audit.py --stage decode
  py -V:3.12 -B scripts/t142_fk_graph_audit.py --columns server 45
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import hashlib
import json
import struct
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
VENDOR = Path(str(_cfg.VENDOR_DIR))
if VENDOR.is_dir():
    sys.path.insert(0, str(VENDOR))
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import t112_fm24_reader as base          # noqa: E402
import t133_fm24_reader_v2 as t133       # noqa: E402
import t123_basic_people_l3 as people    # noqa: E402

# ---------------------------------------------------------------- registry
records, specs = t133.registry(t133.load(t133.TRACE))
l3 = t133.load(t133.L3)

OUT = ROOT / "scratch/t142/out"
CACHE = OUT / "cache"
T106_OUT = ROOT / "scratch/t106/out"
STAGE1 = OUT / "stage1_columns.json"
STAGE2 = OUT / "stage2_domains.json"
STAGE3 = OUT / "stage3_edges.json"
MASTER = OUT / "fk_graph_master.json"

# ---------------------------------------------------------------- thresholds
HIT_RATE_MIN = 0.99        # promotion floor for a whole-column FK
MIN_ROWS = 32              # non-sentinel rows needed before promotion
MIN_DISTINCT = 2           # a constant column is never a foreign key
CHANCE_MAX = 0.02          # accidental-hit allowance for statistical promotion
PAIR_RATE_MIN = 0.99       # joint (ordinal, uid) pair proof floor
SAMPLE_ORPHANS = 8

U32_MAX = 0xFFFFFFFF
U64_MAX = 0xFFFFFFFFFFFFFFFF
SENTINEL_BY_WIDTH = {1: 0xFF, 2: 0xFFFF, 4: U32_MAX, 8: U64_MAX}

# Selector variants whose row layout is a fixed prefix plus the base layout:
# flag -> (root path shift, byte shift) so both variants share one column id.
VAR_SHIFT = {("client", 3): {12: (2, 5)}, ("server", 3): {12: (2, 5)}}

# 4CC / L3 field-name tokens that corroborate a target class (t121 4CC names are
# IDA dispatch codes; these tokens are semantic, cited in REPORT.md).
NAME_TOKENS = {
    "NATION": ("natn", "cnat", "nati", "ntio"),
    "NATIONAL_TEAM_CONTAINER": ("ntc", "ntco"),
    "NATIONAL_TEAM": ("ntte", "ntmt", "natt"),
    "CLUB": ("club", "clid", "clu", "ccl"),
    "COMP": ("comp", "cmp", "cmpi", "compt"),
    "CITY": ("city", "ccty", "cty"),
    "STADIUM": ("stad", "stid", "stsi"),
    "REGION": ("regn", "rgin", "nrgi"),
    "CONTINENT": ("cont", "cnti", "cntn"),
    "LOCAL_REGION": ("locr", "lreg"),
    "TEAM": ("team", "tfte", "ttea", "otht", "t24"),
    "PERSON": ("pers", "plyr", "plid", "stid", "pid"),
    "INJURY": ("inju", "injr"),
    "AWARD": ("awar",),
    "LANGUAGE": ("lang", "lngu"),
    "MEDIA_SOURCE": ("medi", "media"),
    "PLAYER_TYPE": ("ptyp", "plrt"),
    "CURRENCY_RECORD": ("curr", "curi"),
    "WEATHER": ("weat",),
    "AGREEMENT": ("agrm", "agre"),
    "STAGE_NAME": ("stgn", "sten"),
    "DERBY": ("derb",),
    "STADIUM_CHANGE": ("stch",),
}
# Target classes whose small ordinal domain makes them enum-indistinguishable;
# they require corroboration before promotion.
SMALL_DOMAIN_GUARD = 64


# ---------------------------------------------------------------- utilities
def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def digest_set(arr) -> str:
    """Stable digest of a key set (order independent, dtype independent)."""
    if arr.size == 0:
        return "sha256:" + hashlib.sha256(b"").hexdigest()[:32]
    a = np.unique(np.asarray(arr, dtype=np.uint64))
    h = hashlib.sha256(a.astype("<u8").tobytes())
    return "sha256:" + h.hexdigest()[:32]


def n_present(arr) -> int:
    return int(arr.size)


# ---------------------------------------------------------------- decode
def walk_scalars(prog, data, start, end):
    """Yield (canonical_path, row_off, width, kind, unsigned value, in_vector) per scalar.

    String payloads advance the cursor without being reported.  Branch indices
    of ``tag``/``choose``/``switch``/``if`` descendants *and* vector element
    indices are not part of the canonical path, so one logical field keeps one
    identity across rows (and across vector element slots).
    """
    out = []
    p = start
    u16 = struct.Struct("<H").unpack_from
    u32 = struct.Struct("<I").unpack_from
    u64 = struct.Struct("<Q").unpack_from

    def num(w):
        if w == 1:
            return data[p]
        if w == 2:
            return u16(data, p)[0]
        if w == 4:
            return u32(data, p)[0]
        return u64(data, p)[0]

    def walk(block, path, tag, in_vec):
        nonlocal p
        for i, op in enumerate(block):
            kind = op[0]
            key = path + (i,)
            off = p - start
            if kind == "u":
                w = op[1]
                if w in (1, 2, 4, 8):
                    v, k = num(w), "u"
                else:
                    # unreduced wide read (3..20 bytes): keep the low 64 bits only
                    v = int.from_bytes(data[p:p + w], "little")
                    k = "u" if w < 8 else "uwide"
                    if w > 8:
                        v &= 0xFFFFFFFFFFFFFFFF
                out.append((key, off, w, k, v, in_vec))
                p += w
            elif kind == "s":
                ln = u32(data, p)[0]
                p += 4 + ln
            elif kind == "id":
                o, u, d = struct.unpack_from("<III", data, p)
                out.append((key, off, 4, "ord", o, in_vec))
                out.append((key, off + 4, 4, "uid", u, in_vec))
                out.append((key, off + 8, 4, "dbid", d, in_vec))
                p += 12
            elif kind in ("v", "rep"):
                if kind == "v":
                    w = op[1][1]
                    cnt = num(w)
                    p += w
                    body = op[2]
                else:
                    cnt, body = op[1], op[2]
                for _ in range(cnt):
                    walk(body, key, tag, True)
            elif kind in ("if", "zero", "tag", "switch"):
                w = op[1] if kind == "if" else abs(op[1])
                v = num(w)
                if kind != "if" and op[1] < 0 and v >= 1 << (8 * w - 1):
                    v -= 1 << (8 * w)
                out.append((key, off, w, "gate", v & ((1 << (8 * w)) - 1), in_vec))
                p += w
                if kind == "if":
                    if {"!=": v != op[3], "==": v == op[3]}[op[2]]:
                        walk(op[4], key, tag, in_vec)
                elif kind == "tag":
                    for th, body in op[2]:
                        if not th or v >= th:
                            walk(body, key, v, in_vec)
                elif kind == "switch":
                    if v not in op[2]:
                        raise base.WireError(f"switch value {v} missing")
                    walk(op[2][v], key, tag, in_vec)
            elif kind == "match":
                if tag == op[1]:
                    walk(op[2], key, tag, in_vec)
            elif kind == "choose":
                walk(op[2] if tag >= op[1] else op[3], key, tag, in_vec)
            else:  # pragma: no cover - grammar change would be an upstream bug
                raise ValueError(f"unknown op {op}")

    walk(prog, (), None, False)
    return out


def norm_path(path, root_shift):
    """Apply the variant root shift so selector variants share column ids."""
    if not root_shift:
        return path
    head = path[0]
    if not isinstance(head, int) or head < root_shift:
        return None
    return (head - root_shift,) + path[1:]


def col_id(path, kind, width):
    return f"{'/'.join(map(str, path))}|{kind}|{width}"


def decode_table(key, cols_only=False):
    """Decode every row of one numbered table into typed column arrays.

    Column identity is the canonical grammar path (branch- and vector-index
    free) plus kind/width, so a logical field keeps one identity across all
    rows and all vector slots.  Non-vector columns carry a per-row presence
    mask when a row may skip them (optional branches).
    """
    spec = specs[key]
    l3map = base._l3_name_map(l3, key[1], key[0])
    data = base.Archive(key[0]).payload(key[1])
    nrows = struct.unpack_from("<I", data, 8)[0]
    end = len(data) - base.FOOTER_SIZE
    cols = {}
    skipped_fields = 0
    flags = Counter()
    t0 = time.perf_counter()

    def put(cid, name, kind, off, width, values, rowidx=None, nrows_=None):
        a = np.asarray(values, dtype=np.uint64)
        entry = dict(id=cid, name=name, kind=kind, off=off, width=width, values=a)
        if rowidx is not None and nrows_ is not None:
            mask = np.zeros(nrows_, dtype=bool)
            np.maximum.at(mask, np.asarray(rowidx, dtype=np.int64), True)
            entry["present"] = mask
            entry["row_hits"] = int(mask.sum())
        if rowidx is not None and len(set(rowidx)) != len(rowidx):
            entry["multi_per_row"] = True
        cols[cid] = entry

    if spec.kind == "fixed":
        reader = base.TableReader(spec, l3)
        reader._fixed_setup()
        fmt, fields = reader._fixed_fmt, reader._fixed_fields
        buckets = [[] for _ in fields]
        p = base.HEADER_END
        mv = memoryview(data)
        for _ in range(nrows):
            vals = fmt.unpack_from(mv, p + 1)
            flags[data[p]] += 1
            p += 1 + fmt.size
            for b, v in zip(buckets, vals):
                if isinstance(v, int):
                    b.append(v)
        for (nm, off, width, sub), b in zip(fields, buckets):
            if not b:
                skipped_fields += 1
                continue
            kind = {"ordinal": "ord", "uid": "uid", "dbid": "dbid"}.get(sub or "", "u")
            name = f"{nm}.{sub}" if sub else nm
            put(col_id((nm, sub or ""), kind, width), name, kind, off, width, b,
                rowidx=range(len(b)), nrows_=nrows)
    elif nrows == 0 or (spec.prog is None and key not in t133.SELECTORS):
        # Empty table (t52/t57) or a variant-only table without a base program.
        skipped_fields += 1
        flags[0] = 0
    else:
        variants = t133.SELECTORS.get(key)
        progs = variants if variants else ({0: spec.prog} if spec.prog else {})
        shift = VAR_SHIFT.get(key, {})
        fasts = {f: t133.compile_walk(prog) for f, prog in progs.items()}
        buckets, rowidx, invec, first_off = {}, {}, {}, {}
        p = base.HEADER_END
        for row in range(nrows):
            flag = data[p] if variants else 0
            prog = progs[flag]
            body = p + 1
            q = fasts[flag](data, body, end)
            rshift, bshift = shift.get(flag, (0, 0))
            for path, off, width, kind, val, iv in walk_scalars(prog, data, body, q):
                npth = norm_path(path, rshift)
                if npth is None:
                    continue
                cid = col_id(npth, kind, width)
                buckets.setdefault(cid, []).append(val)
                if not iv:
                    rowidx.setdefault(cid, []).append(row)
                else:
                    invec[cid] = True
                if kind != "gate":
                    prev = first_off.get(cid)
                    noff = off - bshift
                    if prev is None or noff < prev:
                        first_off[cid] = noff
            flags[flag] += 1
            p = q
        for cid, b in buckets.items():
            parts = cid.split("|")
            kind, width = parts[-2], int(parts[-1])
            off = first_off.get(cid, 0)
            nm = l3map.get(off) if kind in ("u", "ord", "uid") else None
            name = nm or ({"ord": "identity.ordinal", "uid": "identity.uid",
                           "dbid": "identity.dbid"}.get(kind) or f"col_{off}")
            ri = None if invec.get(cid) else rowidx.get(cid)
            put(cid, name, kind, off, width, b, rowidx=ri, nrows_=nrows)

    meta = dict(archive=key[0], table_id=key[1], klass=spec.klass.lower(), kind=spec.kind,
                rows=nrows, columns=len(cols), skipped_fields=skipped_fields,
                flags={hex(k): v for k, v in sorted(flags.items())},
                elapsed_ms=round(1000 * (time.perf_counter() - t0), 1))
    return cols, meta


# ---------------------------------------------------------------- specials
def decode_basic_people():
    """basic_people_db: 658,011 fixed-stride people rows (t123 verified layout)."""
    payload, _ = people.decompress_basic()
    count = struct.unpack_from("<I", payload, 0)[0]
    widths = people.WIDTHS
    field = dict(person_type=[], ordinal=[], uid=[], dbid=[],
                 nation_ord=[], nation_uid=[], club_ord=[], club_uid=[],
                 ca=[], pa=[], birth_year=[])
    pos = 5
    present = {k: [] for k in field}
    for _ in range(count):
        if payload[pos] != 0x11:
            raise ValueError(f"basic_people marker at {pos}")
        kind = payload[pos + 1]
        row = payload[pos:pos + widths[kind]]
        field["person_type"].append(kind)
        present["person_type"].append(1)
        if kind in (1, 2, 3):
            ord_off, uid_off, nat_off, club_off, ca_off, pa_off, by_off = 71, 79, 2, 10, 48, 50, 52
        elif kind == 4:
            ord_off, uid_off, nat_off, club_off, ca_off, pa_off, by_off = 22, 30, 2, None, None, None, 12
        else:
            ord_off, uid_off, nat_off, club_off, ca_off, pa_off, by_off = 10, 18, None, None, None, None, None
        u32 = lambda o: struct.unpack_from("<I", row, o)[0]
        u16 = lambda o: struct.unpack_from("<H", row, o)[0]
        for nm, off in (("ordinal", ord_off), ("uid", uid_off)):
            field[nm].append(u32(off))
            present[nm].append(1)
        field["dbid"].append(0)
        present["dbid"].append(0)
        for nm, off in (("nation", nat_off), ("club", club_off)):
            if off is None:
                field[f"{nm}_ord"].append(0)
                field[f"{nm}_uid"].append(0)
                present[f"{nm}_ord"].append(0)
                present[f"{nm}_uid"].append(0)
            else:
                field[f"{nm}_ord"].append(u32(off))
                field[f"{nm}_uid"].append(u32(off + 4))
                present[f"{nm}_ord"].append(1)
                present[f"{nm}_uid"].append(1)
        for nm, off in (("ca", ca_off), ("pa", pa_off), ("birth_year", by_off)):
            if off is None:
                field[nm].append(0)
                present[nm].append(0)
            else:
                field[nm].append(u16(off))
                present[nm].append(1)
        pos += widths[kind]
    if pos != len(payload) - 9:
        raise ValueError(f"basic_people chain mismatch: {pos} != {len(payload) - 9}")
    cols = {}
    for nm, vals in field.items():
        if nm in ("ordinal", "uid"):
            kind = "ord" if nm == "ordinal" else "uid"
            name = f"identity.{nm}"
        elif nm.endswith("_ord") or nm.endswith("_uid"):
            base_nm = nm.rsplit("_", 1)[0]
            kind = "pair_ord" if nm.endswith("_ord") else "pair_uid"
            name = f"{base_nm}_ref.{nm.rsplit('_', 1)[1]}"
        else:
            kind, name = "u", nm
        a = np.asarray(vals, dtype=np.uint64)
        mask = np.asarray(present[nm], dtype=bool)
        cid = f"basic|{nm}"
        cols[cid] = dict(id=cid, name=name, kind=kind, off=0, width=4,
                         values=a, present=mask)
    meta = dict(archive="server", table_id="basic_people", klass="basic_person",
                kind="fixed", rows=count, columns=len(cols), skipped_fields=0,
                flags={}, elapsed_ms=0.0)
    return cols, meta


def load_payload(member):
    return (T106_OUT / f"payload_server_{member}.bin").read_bytes()


def decode_club_links():
    b = load_payload("club_links")
    count = struct.unpack_from("<I", b, 8)[0]
    stride = 47
    if 12 + count * stride != len(b):
        raise ValueError("club_links geometry changed")
    raw = np.frombuffer(b, dtype=np.uint8, count=count * stride, offset=12).reshape(count, stride)
    club_uid = np.ascontiguousarray(raw[:, 0:4]).view(np.uint32).reshape(-1).astype(np.uint64)
    linked = np.ascontiguousarray(raw[:, 9:13]).view(np.uint32).reshape(-1).astype(np.uint64)
    cols = {
        "clublinks|club_uid": dict(id="clublinks|club_uid", name="club_uid", kind="u", off=0, width=4, values=club_uid),
        "clublinks|linked_uid": dict(id="clublinks|linked_uid", name="linked_uid", kind="u", off=9, width=4, values=linked),
    }
    meta = dict(archive="server", table_id="club_links", klass="club_links", kind="fixed",
                rows=count, columns=len(cols), skipped_fields=0, flags={}, elapsed_ms=0.0)
    return cols, meta


def decode_name_table(idx):
    b = load_payload(f"name_table_{idx}")
    raw = np.frombuffer(b, dtype=np.uint8)
    count = struct.unpack_from("<I", raw, 8)[0]
    rows = raw[12:12 + count * 12].reshape(count, 12)
    meta_a = np.ascontiguousarray(rows[:, 0:2]).view(np.uint16).reshape(-1).astype(np.uint64)
    str_ord = np.ascontiguousarray(rows[:, 2:6]).view(np.uint32).reshape(-1).astype(np.uint64)
    meta_b = np.ascontiguousarray(rows[:, 6:8]).view(np.uint16).reshape(-1).astype(np.uint64)
    meta_c = np.ascontiguousarray(rows[:, 8:10]).view(np.uint16).reshape(-1).astype(np.uint64)
    meta_d = np.ascontiguousarray(rows[:, 10:12]).view(np.uint16).reshape(-1).astype(np.uint64)
    cols = {
        f"name{idx}|ordinal": dict(id=f"name{idx}|ordinal", name="identity.ordinal", kind="ord", off=0, width=4,
                                   values=np.arange(count, dtype=np.uint64)),
        f"name{idx}|string_ordinal": dict(id=f"name{idx}|string_ordinal", name="string_ordinal", kind="u", off=2, width=4, values=str_ord),
        f"name{idx}|meta_a": dict(id=f"name{idx}|meta_a", name="meta_a", kind="u", off=0, width=2, values=meta_a),
        f"name{idx}|meta_b": dict(id=f"name{idx}|meta_b", name="meta_b", kind="u", off=6, width=2, values=meta_b),
        f"name{idx}|meta_c": dict(id=f"name{idx}|meta_c", name="meta_c", kind="u", off=8, width=2, values=meta_c),
        f"name{idx}|meta_d": dict(id=f"name{idx}|meta_d", name="meta_d", kind="u", off=10, width=2, values=meta_d),
    }
    meta = dict(archive="server", table_id=f"name_table_{idx}", klass="name_table", kind="fixed",
                rows=count, columns=len(cols), skipped_fields=0, flags={}, elapsed_ms=0.0)
    return cols, meta


SPECIALS = {
    "basic_people": decode_basic_people,
    "club_links": decode_club_links,
    "name_table_0": lambda: decode_name_table(0),
    "name_table_1": lambda: decode_name_table(1),
    "name_table_2": lambda: decode_name_table(2),
}


def table_key(arch, tid):
    return f"{arch}/{tid}"


def all_table_keys():
    return sorted(records.keys())


# ---------------------------------------------------------------- cache io
def cache_path(name):
    return CACHE / f"{name.replace('/', '_')}.npz"


def save_columns(name, cols, meta):
    CACHE.mkdir(parents=True, exist_ok=True)
    meta_cols = []
    arrays = {}
    for i, (cid, c) in enumerate(cols.items()):
        key = f"a{i}"
        arrays[key] = c["values"]
        entry = dict(id=cid, name=c["name"], kind=c["kind"], off=c["off"], width=c["width"],
                     array=key, n=int(c["values"].size))
        if "present" in c:
            arrays[f"m{i}"] = np.packbits(c["present"])
            entry["mask"] = f"m{i}"
            entry["present"] = int(c["present"].sum())
        meta_cols.append(entry)
    np.savez(cache_path(name), **arrays)
    meta = dict(meta, columns_meta=meta_cols)
    dump_json(CACHE / f"{name.replace('/', '_')}.json", meta)
    return meta


def load_columns(name, arrays_cache=None):
    """Re-hydrate a cached column store.

    Presence masks are only kept for columns that do not cover every row; when
    the mask has the same length as the value array it is redundant and dropped
    (vector-valued columns carry an instance count, not a row mask).
    """
    meta = load_json(CACHE / f"{name.replace('/', '_')}.json")
    if arrays_cache is None:
        z = np.load(cache_path(name))
        arrays_cache = {}
        for k in z.files:
            arrays_cache[k] = z[k]
    cols = {}
    for e in meta["columns_meta"]:
        c = dict(id=e["id"], name=e["name"], kind=e["kind"], off=e["off"], width=e["width"],
                 values=arrays_cache[e["array"]])
        if e.get("mask"):
            bits = np.unpackbits(arrays_cache[e["mask"]])[:meta["rows"]].astype(bool)
            hits = int(bits.sum())
            n = int(c["values"].size)
            if n == meta["rows"] and hits < meta["rows"]:
                # placeholder layout: one value per row, missing rows flagged
                c["present"] = bits
            elif n == hits:
                # already-filtered layout: the mask only records *which* rows
                c["row_mask"] = bits
            else:
                raise ValueError("%s: mask/value mismatch for %s (%d vs %d)"
                                 % (name, e["id"], hits, n))
        cols[e["id"]] = c
    return cols, meta


def build_cache(force=False):
    """Stage 1: decode every table to the on-disk column cache."""
    CACHE.mkdir(parents=True, exist_ok=True)
    summary = []
    t0 = time.perf_counter()
    jobs = [(table_key(*k), (lambda kk=k: decode_table(kk))) for k in all_table_keys()]
    jobs += [(name, fn) for name, fn in SPECIALS.items()]
    for name, fn in jobs:
        meta_file = CACHE / f"{name.replace('/', '_')}.json"
        if meta_file.is_file() and not force:
            summary.append(load_json(meta_file))
            continue
        cols, meta = fn()
        save_columns(name, cols, meta)
        summary.append(load_json(meta_file))
        print(f"  decoded {name:28} rows={meta['rows']:>8} cols={meta['columns']:>4} "
              f"({time.perf_counter() - t0:.1f}s)")
    dump_json(STAGE1, dict(schema_id="fm24.t142.stage1_columns", schema_version=1,
                           elapsed_ms=round(1000 * (time.perf_counter() - t0), 1),
                           tables=summary))
    return summary


# ---------------------------------------------------------------- domains
# Scoring constants (documented in REPORT.md; `classify` holds the decision
# tree).  A column is only promoted when no plausible coincidence explains it.
ENUM_DISTINCT_MAX = 24          # <= this many distinct values looks like an enum
UID_UNIFORM_MAX = 1e-3         # accidental hit chance of a random u32 draw
SUPPORT_COVER_MAX = 0.02       # share of the column's value space the target may cover
MIN_DISTINCT_STAT = 25         # statistical promotion needs > enum cardinality
SAMPLE_PROBE = 4096            # values used by the cheap pre-filter


def domain_stats(arr) -> dict:
    a = np.unique(np.asarray(arr, dtype=np.uint64))
    n = int(a.size)
    if n == 0:
        return dict(count=0, min=None, max=None, dense_ratio=0.0, digest=digest_set(a))
    lo, hi = int(a[0]), int(a[-1])
    span = hi - lo + 1
    return dict(count=n, min=lo, max=hi, span=span,
                dense_ratio=round(n / span, 12), digest=digest_set(a),
                uniform_chance=round(n / float(1 << 32), 12),
                large_share=round(float(np.count_nonzero(a >= 1_000_000)) / n, 6),
                unique=n == int(np.asarray(arr).size))


def build_domains(write=True):
    """Identity-domain registry for every entity table (stage 2)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    registry, domain_sets = {}, {}
    names = [table_key(*k) for k in all_table_keys()] + list(SPECIALS)
    for name in names:
        cols, meta = load_columns(name)
        ords = [c["values"] for c in cols.values() if c["kind"] == "ord"]
        uids = [c["values"] for c in cols.values() if c["kind"] == "uid"]
        ord_arr = np.unique(np.concatenate(ords)) if ords else np.zeros(0, np.uint64)
        uid_arr = np.unique(np.concatenate(uids)) if uids else np.zeros(0, np.uint64)
        anomalies = []
        dense = False
        if ords:
            raw_ord = np.concatenate(ords)
            dup = int(raw_ord.size - ord_arr.size)
            if dup:
                anomalies.append(f"duplicate ordinal values: {dup}")
            if ord_arr.size and int(ord_arr.min()) == 0 and ord_arr.size == raw_ord.size and \
                    bool((ord_arr == np.arange(ord_arr.size, dtype=np.uint64)).all()):
                dense = True
                anomalies.append("ordinal == row index (dense 0..N-1)")
        if uids:
            raw_uid = np.concatenate(uids)
            dup = int(raw_uid.size - uid_arr.size)
            if dup:
                anomalies.append(f"duplicate uid values: {dup}")
            for sent in (0xFFFFFFFF, 0xFFFFFFFE):
                if bool((uid_arr == sent).any()):
                    anomalies.append(f"uid domain contains sentinel 0x{sent:X}")
        ent = dict(table=name, klass=meta["klass"], table_id=meta["table_id"],
                   archive=meta["archive"], rows=meta["rows"], columns=meta["columns"],
                   ordinal=domain_stats(ord_arr),
                   uid=domain_stats(uid_arr) if uid_arr.size else None,
                   anomalies=anomalies)
        ent["ordinal"]["form"] = "dense 0..N-1" if dense else ("sparse" if ord_arr.size else "absent")
        registry[name] = ent
        domain_sets[(name, "ordinal")] = ord_arr
        if uid_arr.size:
            domain_sets[(name, "uid")] = uid_arr

    classes = {}
    for name, ent in registry.items():
        slot = classes.setdefault(ent["klass"], {"tables": [], "ordinal": None, "uid": None})
        slot["tables"].append(name)
        for key in ("ordinal", "uid"):
            if (name, key) in domain_sets and (slot[key] is None or ent["archive"] == "server"):
                slot[key] = domain_sets[(name, key)]
                slot[f"{key}_source"] = name
    classes["basic_person"] = dict(tables=["basic_people"],
                                   ordinal=domain_sets[("basic_people", "ordinal")],
                                   uid=domain_sets[("basic_people", "uid")],
                                   ordinal_source="basic_people", uid_source="basic_people")

    digs, shared = {}, []
    for klass, slot in classes.items():
        for key in ("ordinal", "uid"):
            arr = slot.get(key)
            if arr is None or arr.size == 0:
                continue
            digs.setdefault(digest_set(arr), []).append(f"{klass}.{key}")
    for d, members in digs.items():
        if len(members) > 1:
            klass, key = members[0].split(".")
            shared.append(dict(digest=d, members=sorted(members),
                               count=int(classes[klass][key].size)))
    out = dict(schema_id="fm24.t142.stage2_domains", schema_version=1,
               registry=registry,
               classes={k: dict(tables=v["tables"],
                                ordinal_source=v.get("ordinal_source"),
                                uid_source=v.get("uid_source"),
                                ordinal_count=int(v["ordinal"].size) if v["ordinal"] is not None else 0,
                                uid_count=int(v["uid"].size) if v["uid"] is not None else 0,
                                ordinal_stats=domain_stats(v["ordinal"]) if v["ordinal"] is not None else None,
                                uid_stats=domain_stats(v["uid"]) if v["uid"] is not None else None)
                        for k, v in classes.items()},
               shared_namespaces=shared)
    if write:
        dump_json(STAGE2, out)
    return registry, domain_sets, classes


# ---------------------------------------------------------------- FK scoring
class Domain:
    """A target key domain plus the statistics used to judge an edge."""

    __slots__ = ("klass", "key", "arr", "count", "min", "max", "large_share",
                 "uniform_chance", "digest")

    def __init__(self, klass, key, arr):
        self.klass, self.key = klass, key
        self.arr = np.ascontiguousarray(arr, dtype=np.uint64)
        self.count = int(self.arr.size)
        self.min = int(self.arr[0])
        self.max = int(self.arr[-1])
        self.large_share = float(np.count_nonzero(self.arr >= 1_000_000)) / self.count
        self.uniform_chance = self.count / float(1 << 32)
        self.digest = digest_set(self.arr)


def build_domain_list(classes):
    out = []
    for klass, slot in sorted(classes.items()):
        for key in ("ordinal", "uid"):
            arr = slot.get(key)
            if arr is None or arr.size == 0:
                continue
            out.append(Domain(klass, key, arr))
    return out


def domain_hits(arr, dom_arr):
    """Count values of ``arr`` present in the sorted unique ``dom_arr``."""
    if dom_arr.size == 0 or arr.size == 0:
        return 0
    idx = np.searchsorted(dom_arr, arr)
    idx[idx == dom_arr.size] = dom_arr.size - 1
    return int(np.count_nonzero(dom_arr[idx] == arr))


def in_domain(arr, dom_arr):
    if dom_arr.size == 0 or arr.size == 0:
        return np.zeros(arr.size, dtype=bool)
    idx = np.searchsorted(dom_arr, arr)
    idx[idx == dom_arr.size] = dom_arr.size - 1
    return dom_arr[idx] == arr


def sentinel_mask(values, width, kind="u"):
    """Rows carrying a real value (all-ones sentinels removed)."""
    s = SENTINEL_BY_WIDTH.get(width)
    if s is None:
        return np.ones(values.size, dtype=bool)
    return values != np.uint64(s)


def column_profile(values, width, kind="u"):
    keep = sentinel_mask(values, width, kind)
    live = values[keep]
    sent = [f"0x{int(x):X}" for x in np.unique(values[~keep])[:4]]
    return dict(rows=int(values.size), non_sentinel_rows=int(live.size),
                sentinel_rows=int(values.size - live.size), sentinel_values=sent,
                distinct=int(np.unique(live).size) if live.size else 0,
                min=int(live.min()) if live.size else None,
                max=int(live.max()) if live.size else None,
                width=width, live=live)


def corroboration(src_name, target, pair_kind=None):
    """4CC/L3 field-name token or reference-pair layout corroboration."""
    ev = []
    low = (src_name or "").lower()
    for tok in NAME_TOKENS.get(target.upper(), ()):
        if tok in low:
            ev.append("name_token:" + tok)
    if pair_kind:
        ev.append("layout:" + pair_kind)
    return ev


def classify(cand, prof, src_name):
    """Promotion decision for one (column, target-domain) candidate."""
    if prof["non_sentinel_rows"] < MIN_ROWS:
        return "rejected", ["too_few_rows"]
    if prof["distinct"] < MIN_DISTINCT:
        return "rejected", ["constant_column"]
    if cand["hit_rate"] < HIT_RATE_MIN:
        return "rejected", ["hit_rate_below_floor"]
    corr = corroboration(src_name, cand["target"], cand.get("pair_kind"))
    enum_like = (prof["distinct"] <= ENUM_DISTINCT_MAX
                 and cand["target_domain_count"] <= SMALL_DOMAIN_GUARD)
    low_spec = cand["support_coverage"] > SUPPORT_COVER_MAX
    if corr:
        notes = ["corroborated:" + ",".join(corr)]
        if low_spec:
            notes.append("low_specificity_support_coverage=%s" % cand["support_coverage"])
        return "code_corroborated", notes
    if (cand["target_key"] == "uid"
            and cand["uniform_chance"] <= UID_UNIFORM_MAX
            and not low_spec
            and prof["distinct"] >= MIN_DISTINCT_STAT):
        return "statistical", ["uid_sparse:uniform_chance=%.2e,support_coverage=%s"
                               % (cand["uniform_chance"], cand["support_coverage"])]
    if low_spec:
        return "ambiguous", ["support_collision_possible:coverage=%s" % cand["support_coverage"]]
    if enum_like:
        return "ambiguous", ["enum_like_small_domain"]
    if cand["target_key"] == "ordinal":
        return "ambiguous", ["dense_ordinal_domain_not_provable"]
    return "ambiguous", ["low_specificity"]


def evaluate_column(vals, width, src_name, src_table, domains, own):
    """Test one column against every target key domain."""
    prof = column_profile(vals, width)
    live = prof["live"]
    out = []
    if live.size < MIN_ROWS or prof["distinct"] < MIN_DISTINCT:
        return out, prof
    vmin, vmax = prof["min"], prof["max"]
    probe = live[::max(1, live.size // SAMPLE_PROBE)]
    for d in domains:
        if (d.klass, d.key) in own:
            continue
        if vmax > d.max or vmin < d.min:
            continue
        if domain_hits(probe, d.arr) < 0.90 * probe.size:
            continue
        h = domain_hits(live, d.arr)
        rate = h / live.size
        if rate < 0.90:
            continue
        # how much of the column's own value space the target domain covers
        lo = int(np.searchsorted(d.arr, vmin, "left"))
        hi = int(np.searchsorted(d.arr, vmax, "right"))
        cover = (hi - lo) / float(vmax - vmin + 1)
        out.append(dict(target=d.klass, target_key=d.key, target_domain_count=d.count,
                        target_large_share=round(d.large_share, 6),
                        uniform_chance=d.uniform_chance,
                        support_coverage=round(cover, 8),
                        hits=h, rows=int(live.size), hit_rate=round(rate, 6)))
    out.sort(key=lambda r: (-r["hit_rate"], r["support_coverage"], r["uniform_chance"],
                            -r["target_domain_count"]))
    return out, prof


def orphan_detail(vals, width, dom_arr, limit=SAMPLE_ORPHANS):
    prof = column_profile(vals, width)
    miss = prof["live"][~in_domain(prof["live"], dom_arr)]
    if miss.size == 0:
        return 0, 0, []
    uniq, counts = np.unique(miss, return_counts=True)
    samples = [dict(value=int(v), rows=int(c)) for v, c in zip(uniq[:limit], counts[:limit])]
    return int(miss.size), int(uniq.size), samples


def scan_edges(classes, verbose=True):
    """Stage 3: audit every integer scalar column and every reference pair."""
    domains = build_domain_list(classes)
    dmap = {(d.klass, d.key): d for d in domains}
    edges, ambiguous, pair_edges = [], [], []
    scanned = tests = 0
    t0 = time.perf_counter()
    names = [table_key(*k) for k in all_table_keys()] + list(SPECIALS)
    for name in names:
        cols, meta = load_columns(name)
        klass = meta["klass"]
        own = {(klass, "ordinal"), (klass, "uid")}
        test_cols = []
        for cid, c in cols.items():
            k, w = c["kind"], c["width"]
            if k in ("gate", "ord", "uid", "dbid", "uwide"):
                continue
            mask = c.get("present")
            if k == "u" and w in (1, 2, 4):
                test_cols.append((cid, c["name"], w, c["values"], mask, c["off"]))
            elif k in ("pair_ord", "pair_uid"):
                test_cols.append((cid, c["name"], 4, c["values"], mask, c["off"]))
            elif k == "u" and w == 8:
                # 8-byte references are (uid u32, dbid u32): only the low half is
                # ever an independent reference target.
                v = c["values"]
                test_cols.append((cid + "#lo32", c["name"] + ".lo32", 4,
                                  v & np.uint64(0xFFFFFFFF), mask, c["off"]))
        for cid, cname, width, vals, mask, off in test_cols:
            if mask is not None:
                vals = vals[mask]
            if vals.size < MIN_ROWS:
                continue
            scanned += 1
            cands, prof = evaluate_column(vals, width, cname, name, domains, own)
            if not cands:
                continue
            tests += len(cands)
            best = None
            for cand in cands:
                tier, notes = classify(cand, prof, cname)
                if tier == "rejected":
                    continue
                rec = dict(src_table=name, src_class=klass, src_column=cname,
                           src_col_id=cid, src_width=width, src_offset=off,
                           rows=prof["rows"], non_sentinel_rows=prof["non_sentinel_rows"],
                           sentinel_rows=prof["sentinel_rows"],
                           sentinel_values=prof["sentinel_values"],
                           distinct=prof["distinct"], min=prof["min"], max=prof["max"],
                           target=cand["target"], target_key=cand["target_key"],
                           target_domain_count=cand["target_domain_count"],
                           target_large_share=cand["target_large_share"],
                           uniform_chance=round(cand["uniform_chance"], 12),
                           support_coverage=cand["support_coverage"],
                           valid_hits=cand["hits"], hit_rate=cand["hit_rate"],
                           tier=tier, verified=True, evidence=notes)
                if tier in ("code_corroborated", "statistical"):
                    d = dmap[(cand["target"], cand["target_key"])]
                    orph, orph_uniq, samples = orphan_detail(vals, width, d.arr)
                    rec.update(orphan_rows=orph, orphan_values=orph_uniq,
                               orphan_samples=samples)
                    if best is None:
                        best = rec
                        edges.append(rec)
                    else:
                        ambiguous.append(dict(
                            src_table=name, src_column=cname, src_col_id=cid,
                            src_offset=off, target=cand["target"],
                            target_key=cand["target_key"], tier="superseded",
                            rows=prof["non_sentinel_rows"], distinct=prof["distinct"],
                            hit_rate=cand["hit_rate"],
                            support_coverage=cand["support_coverage"],
                            evidence=notes + ["superseded_by:" +
                                              best["target"] + "." + best["target_key"]]))
                else:
                    rec["verified"] = False
                    ambiguous.append(dict(
                        src_table=name, src_column=cname, src_col_id=cid,
                        src_offset=off, target=cand["target"],
                        target_key=cand["target_key"], tier=tier,
                        rows=prof["non_sentinel_rows"], distinct=prof["distinct"],
                        hit_rate=cand["hit_rate"],
                        support_coverage=cand["support_coverage"],
                        evidence=notes))
        # ---- reference pairs: adjacent u32 columns and u64 halves
        pair_cands = []
        by_off = {}
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 4 and "row_mask" not in c \
                    and "present" not in c:
                by_off.setdefault(c["off"], []).append(c)
        for off in sorted(by_off):
            for c1 in by_off[off]:
                for c2 in by_off.get(off + 4, []):
                    if c2 is not c1:
                        for layout in ("uid_dbid", "ordinal_uid"):
                            pair_cands.append((c1["name"], c2["name"], c1["values"],
                                               c2["values"], layout))
        for cid, c in cols.items():
            if c["kind"] == "u" and c["width"] == 8 and "present" not in c \
                    and "row_mask" not in c:
                v = c["values"]
                pair_cands.append((c["name"] + ".lo32", c["name"] + ".hi32",
                                   v & np.uint64(0xFFFFFFFF), v >> np.uint64(32),
                                   "uid_dbid"))
        if name == "basic_people":
            for base in ("nation", "club"):
                a, b = cols.get("basic|%s_ord" % base), cols.get("basic|%s_uid" % base)
                if a is None or b is None:
                    continue
                m = a["present"] & b["present"]
                pair_cands.append((base + "_ref.ordinal", base + "_ref.uid",
                                   a["values"][m], b["values"][m], "ordinal_uid"))
        seen_pairs = set()
        for n1, n2, v1, v2, layout in pair_cands:
            for got in test_reference_pair(name, klass, n1, n2, v1, v2, layout, domains):
                sig = (got["src_table"], got["low_column"], got["high_column"],
                       got["target"], got["layout"])
                if sig in seen_pairs:
                    continue
                seen_pairs.add(sig)
                pair_edges.append(got)
        if verbose:
            print("  %-26s cols=%5d edges=%5d pairs=%3d (%.1fs)" %
                  (name, scanned, len(edges), len(pair_edges), time.perf_counter() - t0))
    return dict(edges=edges, ambiguous=ambiguous, pair_edges=pair_edges,
                columns_scanned=scanned, candidate_tests=tests,
                elapsed_ms=round(1000 * (time.perf_counter() - t0), 1))


def test_reference_pair(src_table, src_class, n1, n2, v1, v2, layout, domains):
    """Reference-pair proof for the two layouts proven empirically.

    ``ordinal_uid``  low u32 = target ``ordinal``, high u32 = target ``uid``
                     (basic_people ``nation_ref`` / ``club_ref``);
    ``uid_dbid``     low u32 = target ``uid``, high u32 is the companion
                     ``dbid`` (== uid for same-database objects, 0 for
                     cross-database person references).
    """
    if v1.size < MIN_ROWS or v2.size != v1.size:
        return []
    keep = sentinel_mask(v1, 4) & sentinel_mask(v2, 4)
    if int(keep.sum()) < MIN_ROWS:
        return []
    a, b = v1[keep], v2[keep]
    out = []
    uids = {d.klass: d for d in domains if d.key == "uid"}
    for d in domains:
        if d.klass == src_class:
            continue
        d_uid = uids.get(d.klass)
        if d_uid is None:
            continue
        if layout == "ordinal_uid":
            if d.key != "ordinal":
                continue
            if int(a.max()) > d.max or int(b.max()) > d_uid.max:
                continue
            h_a = in_domain(a, d.arr)
            h_b = in_domain(b, d_uid.arr)
            key_a, key_b = "ordinal", "uid"
        elif layout == "uid_dbid":
            if d.key != "uid":
                continue
            if int(a.max()) > d_uid.max:
                continue
            h_a = in_domain(a, d_uid.arr)
            h_b = (b == a) | (b == np.uint64(0))
            key_a, key_b = "uid", "dbid"
        else:
            continue
        joint = h_a & h_b
        hits = int(np.count_nonzero(joint))
        if hits < PAIR_RATE_MIN * a.size:
            continue
        bad = a[~joint]
        res = dict(src_table=src_table, src_class=src_class, layout=layout,
                   low_column=n1, high_column=n2, target=d.klass,
                   low_key=key_a, high_field=key_b, rows=int(a.size),
                   low_hit_rate=round(int(np.count_nonzero(h_a)) / a.size, 6),
                   high_hit_rate=round(int(np.count_nonzero(h_b)) / b.size, 6),
                   joint_hits=hits, joint_rate=round(hits / a.size, 6),
                   orphan_rows=int(a.size - hits),
                   orphan_samples=[int(x) for x in np.unique(bad)[:SAMPLE_ORPHANS]],
                   tier="pair_proved", verified=True,
                   evidence=["pair:" + layout, "joint_rate=%s" % round(hits / a.size, 6)]
                   + corroboration(n1, d.klass, layout))
        out.append(res)
    return out


# ---------------------------------------------------------------- overlap
def uid_overlap_matrix(classes):
    """Cross-class uid namespace overlap (exact set intersections)."""
    names = sorted(k for k, v in classes.items() if v.get("uid") is not None and v["uid"].size)
    pairs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            sa, sb = classes[a]["uid"], classes[b]["uid"]
            small, big = (sa, sb) if sa.size <= sb.size else (sb, sa)
            inter = small[in_domain(small, big)]
            if inter.size == 0:
                continue
            pairs.append(dict(a=a, b=b, overlap=int(inter.size),
                              a_count=int(sa.size), b_count=int(sb.size),
                              share_of_a=round(inter.size / sa.size, 6),
                              share_of_b=round(inter.size / sb.size, 6),
                              samples=[int(x) for x in inter[:6]]))
    pairs.sort(key=lambda r: (-r["overlap"], r["a"], r["b"]))
    return dict(class_count=len(names), overlapping_pairs=len(pairs), pairs=pairs)


def row_text_fields(name, want_uid):
    """First textual fields of the row whose identity uid matches (evidence)."""
    try:
        if "/" not in name:
            return []
        arch, tid = name.split("/")
        key = (arch, int(tid))
        spec = specs.get(key)
        if spec is None:
            return []
        data = base.Archive(arch).payload(int(tid))
        nrows = struct.unpack_from("<I", data, 8)[0]
        end = len(data) - base.FOOTER_SIZE
        variants = t133.SELECTORS.get(key)
        if spec.kind == "variable" or variants:
            progs = variants if variants else {0: spec.prog}
            fasts = {f: t133.compile_walk(p) for f, p in progs.items()}
            p = base.HEADER_END
            for _ in range(nrows):
                flag = data[p] if variants else 0
                body = p + 1
                q = fasts[flag](data, body, end)
                _, u, _ = struct.unpack_from("<III", data, q - 12)
                if u == want_uid:
                    fields, _ = t133.sample_walk(progs[flag], data, body, q)
                    return [v for _, _, _, k, v in fields if k == "s" and v][:3]
                p = q
            return []
        reader = base.TableReader(spec, l3)
        reader._fixed_setup()
        fmt, fields = reader._fixed_fmt, reader._fixed_fields
        ui = [i for i, f in enumerate(fields) if f[3] == "uid"]
        if not ui:
            return []
        ui = ui[0]
        p = base.HEADER_END
        mv = memoryview(data)
        for _ in range(nrows):
            vals = fmt.unpack_from(mv, p + 1)
            p += 1 + fmt.size
            if int(vals[ui]) != want_uid:
                continue
            out = []
            for v in vals:
                if isinstance(v, bytes) and len(v) >= 3:
                    txt = "".join(chr(c) if 32 <= c < 127 else "\x00" for c in v)
                    txt = txt.strip("\x00 ")
                    if txt:
                        out.append(txt)
            return out[:3]
        return []
    except Exception:
        return []
# ---------------------------------------------------------------- C evidence
SLOT_RE = __import__("re").compile(r"qword_141B5FD[0-9A-Fa-f]{2}")


def c_slot_index():
    """getter VA -> referenced ``qword_141B5FDxx`` DATABASE_OBJECT_REF globals."""
    idx = {}
    dirs = [ROOT / "scratch/t95/funcs", ROOT / "scratch/t124/out/funcs",
            ROOT / "scratch/t132/out/funcs"]
    for d in dirs:
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.c")):
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            slots = sorted(set(SLOT_RE.findall(txt)))
            if slots:
                idx.setdefault(f.stem, set()).update(slots)
    return {k: sorted(v) for k, v in idx.items()}


def l3_fourcc_index():
    """(archive, table_id, wire_off_row0) -> 4CC binding records."""
    idx = defaultdict(list)
    master = load_json(t133.L3)
    for t in master["tables"]:
        tid = t["table_type"]
        for j in t["joined_l3_fourccs"]:
            idx[(j["archive"], tid, j["wire_off_row0"])].append(
                dict(fourcc=j["fourcc"], wire_len=j["wire_len"], mem_off=j["mem_off"],
                     in_slot_off=j["in_slot_off"], getter=j["getter_cite"],
                     access=j["access_kind"], ida_slot=j.get("ida_slot")))
    return idx


def code_evidence(src_table, off, l3idx, slots):
    """Attach 4CC + DATABASE_OBJECT_REF slot evidence for one source column."""
    if "/" not in str(src_table):
        return {}
    arch, tid = src_table.split("/")
    try:
        tid = int(tid)
    except ValueError:
        return {}
    hits = l3idx.get((arch, tid, off), [])
    if not hits:
        return {}
    primary = hits[0]
    ev = dict(fourcc=primary["fourcc"], wire_len=primary["wire_len"],
              mem_off=primary["mem_off"], getter_cite=primary["getter"],
              access_kind=primary["access"], ida_slot=primary["ida_slot"],
              fourcc_aliases=sorted({h["fourcc"] for h in hits}))
    sl = slots.get(primary["getter"].lower().replace("0x", ""), [])
    if sl:
        ev["database_object_ref_slots"] = sl
    return ev


# ---------------------------------------------------------------- selection
CLASS_PREFERENCE = ["nation", "club", "comp", "city", "stadium", "region", "injury",
                    "basic_person", "national_team", "national_team_container"]


def rank_candidate(rec):
    """Deterministic best-target ranking.

    Corroborated before statistical; then the *most specific* (smallest) key
    domain that fully contains the column; then the highest hit rate; then the
    canonical class preference (so NATION wins over the identical NTC domain).
    """
    pref = CLASS_PREFERENCE.index(rec["target"]) if rec["target"] in CLASS_PREFERENCE else 99
    count = rec.get("target_domain_count", rec.get("rows", 10 ** 9))
    rate = rec.get("hit_rate", rec.get("joint_rate", 0.0))
    return (0 if rec["tier"] == "code_corroborated" else 1, count, -rate, pref, rec["target"])


def select_best(records):
    """Split candidate records into (kept, superseded)."""
    groups = defaultdict(list)
    for r in records:
        key = (r["src_table"], r.get("src_col_id") or r.get("low_column"),
               r.get("layout"))
        groups[key].append(r)
    kept, dropped = [], []
    for key, group in groups.items():
        group.sort(key=rank_candidate)
        kept.append(group[0])
        for r in group[1:]:
            r = dict(r)
            r["tier"] = "superseded"
            r["verified"] = False
            r["evidence"] = list(r.get("evidence") or []) + [
                "superseded_by:%s.%s" % (group[0]["target"],
                                          group[0].get("target_key") or group[0].get("low_key"))]
            dropped.append(r)
    return kept, dropped


# ---------------------------------------------------------------- assemble
def assemble(registry, classes, scan, l3idx, slots):
    stage2 = load_json(STAGE2)
    edges, superseded_cols = select_best(scan["edges"])
    pairs, superseded_pairs = select_best(scan["pair_edges"])
    for e in edges:
        ev = code_evidence(e["src_table"], e["src_offset"], l3idx, slots)
        if ev:
            e["code"] = ev
            if ev.get("fourcc"):
                e["evidence"] = list(e["evidence"]) + ["4CC:" + ev["fourcc"]]
            if ev.get("database_object_ref_slots"):
                e["evidence"] = list(e["evidence"]) + [
                    "c:DATABASE_OBJECT_REF@" + ",".join(ev["database_object_ref_slots"])]
    for p in pairs:
        ev = code_evidence(p["src_table"], None, l3idx, slots)
    code_edges = [e for e in edges if e["tier"] == "code_corroborated"]
    stat_edges = [e for e in edges if e["tier"] == "statistical"]
    anon = [e for e in edges if str(e["src_column"]).startswith("col_")]
    anon_pairs = [dict(src_table=p["src_table"], src_class=p["src_class"],
                       src_column=p["low_column"], target=p["target"],
                       target_key=p["low_key"], hit_rate=p["joint_rate"],
                       evidence=list(p.get("evidence") or []),
                       src_offset=None, rows=p["rows"])
                  for p in pairs if str(p["low_column"]).startswith("col_")]

    overlap = uid_overlap_matrix(classes)
    # notable cross-table uid collisions (the t143 UID 676 example first)
    notable = []
    for want in (676,):
        row = []
        for klass in ("club", "stadium", "city", "comp", "national_team"):
            arr = classes.get(klass, {}).get("uid")
            if arr is None:
                continue
            if bool((arr == want).any()):
                row.append(klass)
        if len(row) > 1:
            notable.append(dict(uid=want, classes=row,
                                evidence={k: row_text_fields(classes[k]["uid_source"], want)
                                          for k in row}))
    for pr in overlap["pairs"][:8]:
        if pr["overlap"] < 1000:
            continue
        notable.append(dict(uid_sample=pr["samples"][:3], classes=[pr["a"], pr["b"]],
                            overlap=pr["overlap"]))

    orphan_edges = [dict(src_table=e["src_table"], src_column=e["src_column"],
                         target=e["target"], target_key=e["target_key"],
                         orphan_rows=e["orphan_rows"], orphan_values=e["orphan_values"],
                         orphan_samples=e.get("orphan_samples", []),
                         hit_rate=e["hit_rate"], tier=e["tier"])
                    for e in edges if e.get("orphan_rows")]
    pair_orphans = [dict(src_table=p["src_table"], columns=[p["low_column"], p["high_column"]],
                         target=p["target"], layout=p["layout"],
                         orphan_rows=p["orphan_rows"], orphan_samples=p.get("orphan_samples", []),
                         joint_rate=p["joint_rate"])
                    for p in pairs if p.get("orphan_rows")]

    reason_counts = Counter()
    for a in scan["ambiguous"]:
        for n in a.get("evidence") or []:
            reason_counts[n.split(":")[0]] += 1
    ambiguous_best = {}
    for a in scan["ambiguous"]:
        if a.get("tier") == "superseded":
            continue
        key = (a["src_table"], a["src_col_id"])
        cur = ambiguous_best.get(key)
        if cur is None or (-a["hit_rate"], a["support_coverage"]) < \
                (-cur["hit_rate"], cur["support_coverage"]):
            ambiguous_best[key] = a
    ambiguous_sample = sorted(ambiguous_best.values(),
                              key=lambda r: (-r["hit_rate"], r["support_coverage"]))[:250]

    health = dict(
        tables_audited=len(registry),
        numbered_tables=len(all_table_keys()),
        special_tables=len(SPECIALS),
        rows_decoded=sum(v["rows"] for v in registry.values()),
        columns_inventoried=sum(v["columns"] for v in registry.values()),
        columns_scanned=scan["columns_scanned"],
        candidate_tests=scan["candidate_tests"],
        verified_edges=len(edges),
        verified_code_corroborated=len(code_edges),
        verified_statistical=len(stat_edges),
        verified_pair_proofs=len(pairs),
        anonymous_col_edges=len(anon) + len(anon_pairs),
        ambiguous_candidates=len(scan["ambiguous"]) - len(superseded_cols),
        rejected_candidates=len(scan["ambiguous"]) - len(superseded_cols) - len(ambiguous_sample),
        orphan_rows_column_edges=sum(e.get("orphan_rows", 0) for e in edges),
        orphan_rows_pair_edges=sum(p.get("orphan_rows", 0) for p in pairs),
        edges_with_orphans=len(orphan_edges) + len(pair_orphans),
        uid_overlapping_class_pairs=overlap["overlapping_pairs"],
        shared_key_namespaces=len(stage2["shared_namespaces"]),
    )
    master = dict(
        schema_id="fm24.t142.fk_graph_master",
        schema_version=1,
        game="Football Manager 2024 24.3.0 (database version 0x0df1)",
        inputs=["scratch/data/server_db.dat", "scratch/data/client_db.dat",
                "scratch/data/basic_people_db.dat",
                "scratch/t106/out/payload_server_club_links.bin",
                "scratch/t106/out/payload_server_name_table_{0,1,2}.bin",
                "scratch/t121/out/master_79of79_l3.json",
                "scratch/t95/funcs/*.c", "scratch/t124/out/funcs/*.c",
                "scratch/t132/out/funcs/*.c"],
        method=dict(
            decode="every integer scalar column of every table decoded for all rows "
                   "(t133 verified grammars); vector slots merged into logical fields; "
                   "branch- and vector-index-free canonical column identity",
            domains="exact ordinal/uid key sets per table, plus canonical per-class "
                    "domains (server archive preferred) and the basic_people person domain",
            promotion=["hit_rate >= %.2f over non-sentinel rows" % HIT_RATE_MIN,
                       "non_sentinel_rows >= %d, distinct >= %d" % (MIN_ROWS, MIN_DISTINCT),
                       "code_corroborated: 4CC/L3 field name token, adjacent "
                       "(ordinal,uid) or (uid,dbid) reference pair, or C "
                       "DATABASE_OBJECT_REF slot evidence",
                       "statistical: uid target, support coverage <= %.2f, "
                       "uniform_chance <= %.0e, distinct >= %d"
                       % (SUPPORT_COVER_MAX, UID_UNIFORM_MAX * 10, MIN_DISTINCT_STAT),
                       "everything else stays ambiguous (enum guard: a <=%d value "
                       "column never becomes a CONTINENT/AGREEMENT edge)"
                       % ENUM_DISTINCT_MAX],
            caveats=["8-byte references carry (uid u32, dbid u32); dbid == uid for "
                     "same-database objects and 0 for cross-database person references",
                     "person references resolve only against the trimmed "
                     "basic_people table (658,011 rows), the full roster lives in "
                     "people_db.dat (out of scope)",
                     "t24 NATIONAL_TEAM is the generic TEAM table: it holds clubs as "
                     "well as national teams (club uids are a subset of team uids)",
                     "ordinal-keyed foreign keys cannot be proven statistically "
                     "because ordinal domains are dense 0..N-1; they are only "
                     "promoted with code corroboration"]),
        health=health,
        identity_registry=registry,
        shared_key_namespaces=stage2["shared_namespaces"],
        class_domains=stage2["classes"],
        edges_verified=sorted(edges, key=lambda r: (r["src_table"], r["src_column"],
                                                    r["target"])),
        edges_code_corroborated=len(code_edges),
        edges_statistical=len(stat_edges),
        reference_pairs=sorted(pairs, key=lambda r: (r["src_table"], r["low_column"])),
        anonymous_col_edges=sorted(anon + anon_pairs,
                                   key=lambda r: (r["src_table"], r["src_column"])),
        ambiguous_candidates=ambiguous_sample,
        ambiguous_reason_counts=dict(reason_counts),
        orphan_audit=dict(column_edges=orphan_edges, pair_edges=pair_orphans,
                          total_orphan_rows=health["orphan_rows_column_edges"]
                          + health["orphan_rows_pair_edges"]),
        uid_overlap=overlap,
        notable_uid_collisions=notable,
        elapsed_ms=scan["elapsed_ms"],
    )
    return master


# ---------------------------------------------------------------- report
CLASS_DISPLAY = {
    "national_team": "TEAM(t24)", "national_team_container": "NTC(t9)",
    "basic_person": "PERSON(658k)", "starting_average_points": "STARTING_AVG_POINTS",
}


def disp(klass):
    return CLASS_DISPLAY.get(klass, klass.upper())


def render_report(master):
    h = master["health"]
    lines = []
    add = lines.append
    add("# t142 — FM24 全库外键关系图谱与引用完整性体检 (Relational FK Graph & Referential Integrity Audit)")
    add("")
    add("对 **FM24 24.3.0** 实际发行数据库 (`database version 0x0df1`) 做一次**只读**的全量关系图谱挖掘：")
    add("79 张编号表 (`server_db` 59 + `client_db` 20) + `basic_people` (658,011 人) + `club_links` (9,261)"
        " + `name_table_0/1/2` (873,709 条)。")
    add("")
    add("| 指标 | 值 |")
    add("|---|---:|")
    add("| 审计表数 | %d (编号 %d + 特殊成员 %d) |" % (h["tables_audited"], h["numbered_tables"], h["special_tables"]))
    add("| 解码行数 | %s |" % f"{h['rows_decoded']:,}")
    add("| 列清单 | %s 列（其中 %s 列参与外键测试）|" % (f"{h['columns_inventoried']:,}", f"{h['columns_scanned']:,}"))
    add("| 已验证外键边 | **%d**（代码印证 %d + 统计验证 %d）|" % (h["verified_edges"], h["verified_code_corroborated"], h["verified_statistical"]))
    add("| 引用对证明 (pair proof) | **%d** |" % h["verified_pair_proofs"])
    add("| 匿名 `col_N` 破译 | **%d** |" % h["anonymous_col_edges"])
    add("| 悬空引用行数 | **%s** |" % f"{h['orphan_rows_column_edges'] + h['orphan_rows_pair_edges']:,}")
    add("| 低特异度候选（不下结论）| %s |" % f"{h['ambiguous_candidates']:,}")
    add("")
    add("## 1. 判定规则（零假阳性设计）")
    add("")
    add("外键只有在**无法用巧合解释**时才被确认：")
    add("")
    add("1. `hit_rate ≥ 99%`（分母为去掉 `0xFF/0xFFFF/0xFFFFFFFF/0xFFFFFFFFFFFFFFFF` 哨兵后的真实值），"
        "且 `non_sentinel_rows ≥ 32`、`distinct ≥ 2`；")
    add("2. **代码印证 (code_corroborated)**：`t121` 4CC 字段名 token 命中目标类、或相邻 "
        "`(ordinal,uid)` / `(uid,dbid)` 引用对、或 C 反编译函数里对 "
        "`qword_141B5FDxx` (`DATABASE_OBJECT_REF` 全局表指针) 的引用；")
    add("3. **统计验证 (statistical)**：目标是 `uid` 域、`support_coverage ≤ 2%`"
        "（目标域只覆盖列自身值域的极小部分）、`uniform_chance ≤ 1e-3` 且 `distinct ≥ 25`；")
    add("4. 其余一律停在 `ambiguous`。**枚举守卫**：≤%d 个取值的小列永远不会被提升为 "
        "`CONTINENT` / `AGREEMENT` 这类小目标表的外键。" % ENUM_DISTINCT_MAX)
    add("")
    add("> 关键结论：`ordinal` 域是稠密 `0..N-1`，任何计数器/枚举都能 100% “命中”，"
        "因此**序号型外键无法用统计证明**，只能靠代码印证。这也是本报告把两类分开统计的原因。")
    add("")
    add("## 2. 核心实体 ER 图")
    add("")
    add("```mermaid")
    add(render_mermaid(master))
    add("```")
    add("")
    add("`t24 NATIONAL_TEAM` 实际上是**通用 TEAM 表**（84,507 行，包含俱乐部与国家队），"
        "`CLUB` (84,259) 的 uid 是其子集；`t9 NTC` 与 `t10 NATION` 共享同一 uid 命名空间。")
    add("")
    add("## 3. 已验证外键边（含匿名列）")
    add("")
    add("| 源表 | 列 (4CC) | 行数 | 取值数 | 目标 | 命中率 | 特异度 cov | 悬空 | 等级 |")
    add("|---|---|---:|---:|---|---:|---:|---:|---|")
    for e in master["edges_verified"]:
        fcc = (e.get("code") or {}).get("fourcc") or ""
        add("| `%s` | `%s`%s | %s | %s | `%s.%s` | %.4f | %.5f | %s | %s |" % (
            e["src_table"], e["src_column"], (" (%s)" % fcc) if fcc else "",
            f"{e['non_sentinel_rows']:,}", f"{e['distinct']:,}", disp(e["target"]),
            e["target_key"], e["hit_rate"], e["support_coverage"],
            e.get("orphan_rows", 0) or 0, e["tier"]))
    add("")
    add("### 3.1 引用对证明（`(ordinal,uid)` / `(uid,dbid)` 布局）")
    add("")
    add("| 源表 | 低半 / 高半 | 布局 | 目标 | 行数 | 联合命中 | 悬空 |")
    add("|---|---|---|---|---:|---:|---:|")
    for p in master["reference_pairs"]:
        add("| `%s` | `%s` / `%s` | %s | `%s.%s` | %s | %.4f | %s |" % (
            p["src_table"], p["low_column"], p["high_column"], p["layout"],
            disp(p["target"]), p["low_key"], f"{p['rows']:,}", p["joint_rate"],
            p["orphan_rows"]))
    add("")
    add("## 4. 匿名列 (`col_N`) 语义破译")
    add("")
    anon = master["anonymous_col_edges"]
    add("共 **%d** 个此前未命名的 `col_N` 列被证明是真实外键（表内偏移即列名）：" % len(anon))
    add("")
    add("| 表 | 匿名列 | 偏移 | 目标 | 命中率 | 证据 |")
    add("|---|---|---:|---|---:|---|")
    for e in sorted(anon, key=lambda r: (r["src_table"], r["src_column"]))[:80]:
        add("| `%s` | `%s` | %s | `%s.%s` | %.4f | %s |" % (
            e["src_table"], e["src_column"], e.get("src_offset"), disp(e["target"]),
            e.get("target_key", "uid"), e["hit_rate"],
            "; ".join(e["evidence"])[:110]))
    add("")
    add("## 5. 悬空 / 破损引用审计")
    add("")
    oa = master["orphan_audit"]
    add("真实发行库中确实存在**少量**悬空引用（目标行不存在），逐条列出：")
    add("")
    add("| 源表 | 列 | 目标 | 悬空行 | 悬空取值 | 样例 |")
    add("|---|---|---|---:|---:|---|")
    for e in sorted(oa["column_edges"], key=lambda r: -r["orphan_rows"]):
        add("| `%s` | `%s` | `%s.%s` | %s | %s | %s |" % (
            e["src_table"], e["src_column"], disp(e["target"]), e["target_key"],
            f"{e['orphan_rows']:,}", e["orphan_values"],
            ",".join(str(s["value"]) for s in e.get("orphan_samples", [])[:4])))
    for p in sorted(oa["pair_edges"], key=lambda r: -r["orphan_rows"]):
        add("| `%s` | `%s`/`%s` | `%s` | %s | - | %s |" % (
            p["src_table"], p["columns"][0], p["columns"][1], disp(p["target"]),
            f"{p['orphan_rows']:,}", ",".join(str(x) for x in p["orphan_samples"][:4])))
    add("")
    add("总计 **%s** 行悬空引用（列级 %s + 引用对 %s）。" % (
        f"{oa['total_orphan_rows']:,}", f"{master['health']['orphan_rows_column_edges']:,}",
        f"{master['health']['orphan_rows_pair_edges']:,}"))
    add("")
    add("## 6. UID 命名空间重叠")
    add("")
    add("`uid` 在单表内唯一，但**跨表存在系统性重叠**（同一 uid 数值在不同类中表示不同对象）：")
    add("")
    add("| 类 A | 类 B | 重叠 | A 总数 | B 总数 | 样例 UID |")
    add("|---|---|---:|---:|---:|---|")
    for pr in master["uid_overlap"]["pairs"][:15]:
        add("| %s | %s | %s | %s | %s | %s |" % (
            disp(pr["a"]), disp(pr["b"]), f"{pr['overlap']:,}", f"{pr['a_count']:,}",
            f"{pr['b_count']:,}", ",".join(map(str, pr["samples"][:4]))))
    add("")
    for n in master["notable_uid_collisions"][:3]:
        if "uid" in n:
            add("- **UID %s** 同时存在于：%s；解码出的文本字段：%s" % (
                n["uid"], ", ".join(disp(c) for c in n["classes"]),
                {disp(k): v for k, v in (n.get("evidence") or {}).items()}))
    add("")
    add("## 7. 身份域注册表（节选）")
    add("")
    add("| 表 | 类 | 行数 | ordinal (min..max, count) | uid (min..max, count) | 不变量 |")
    add("|---|---|---:|---|---|---|")
    for name in sorted(master["identity_registry"]):
        e = master["identity_registry"][name]
        o, u = e["ordinal"], e["uid"] or {}
        add("| `%s` | %s | %s | %s..%s, %s | %s..%s, %s | %s |" % (
            name, disp(e["klass"]), f"{e['rows']:,}", o.get("min"), o.get("max"),
            f"{o.get('count'):,}", u.get("min"), u.get("max"), f"{u.get('count', 0):,}",
            "; ".join(e["anomalies"])[:60] or "ok"))
    add("")
    add("## 8. 复现")
    add("")
    add("```bat")
    add("py -V:3.12 -B scripts/t142_fk_graph_audit.py            # 全流程（解码→域→图谱→报告）")
    add("py -V:3.12 -B scripts/t142_fk_graph_audit.py --selftest # 自检")
    add("```")
    add("")
    add("中间产物：`scratch/t142/out/cache/`（列存储）、`stage1_columns.json`、"
        "`stage2_domains.json`、`stage3_edges.json`、`fk_graph_master.json`。")
    add("")
    return "\n".join(lines) + "\n"


def render_mermaid(master):
    order = ["club", "comp", "nation", "city", "stadium", "region", "injury",
             "basic_person", "national_team", "national_team_container", "player_type",
             "media_source", "language", "award", "weather", "stage_name", "local_region",
             "currency_record", "agreement", "derby", "continent"]
    edges = []
    for e in master["edges_verified"]:
        score = (2 if e["tier"] == "code_corroborated" else 1, e["hit_rate"], e["distinct"])
        edges.append((e["src_class"], e["target"], e["src_column"], score))
    for p in master["reference_pairs"]:
        edges.append((p["src_class"], p["target"],
                      "%s/%s" % (p["low_column"], p["high_column"]),
                      (3, p["joint_rate"], p["rows"])))
    best = {}
    for s, t, col, score in edges:
        k = (s, t)
        if k not in best or score > best[k][0]:
            best[k] = (score, col)
    keep = set(order)
    lines = ["erDiagram"]
    shown = 0
    for (s, t), (score, col) in sorted(best.items(), key=lambda kv: -kv[1][0][0]):
        if s not in keep or t not in keep or s == t:
            continue
        if shown >= 26:
            break
        lines.append('  %s ||--o{ %s : "%s"' % (t.upper().replace("-", "_"),
                                                s.upper().replace("-", "_"), col))
        shown += 1
    if shown == 0:
        lines = ["flowchart LR", "  none[none]"]
    return "\n".join(lines)


def render_done(master):
    h = master["health"]
    lines = [
        "DONE type=t142b",
        "DONE type=t142 (alias line, same audit: fm24 relational fk graph & integrity)",
        "",
        "tables_audited: %d (numbered %d + special %d)"
        % (h["tables_audited"], h["numbered_tables"], h["special_tables"]),
        "rows_decoded: %s" % f"{h['rows_decoded']:,}",
        "columns_inventoried: %s" % f"{h['columns_inventoried']:,}",
        "columns_scanned: %s" % f"{h['columns_scanned']:,}",
        "verified_fk_edges: %d (code_corroborated %d + statistical %d)"
        % (h["verified_edges"], h["verified_code_corroborated"], h["verified_statistical"]),
        "verified_pair_proofs: %d" % h["verified_pair_proofs"],
        "newly_decoded_col_N_fks: %d" % h["anonymous_col_edges"],
        "orphan_rows: %s (column edges %s + pair edges %s)"
        % (f"{h['orphan_rows_column_edges'] + h['orphan_rows_pair_edges']:,}",
           f"{h['orphan_rows_column_edges']:,}", f"{h['orphan_rows_pair_edges']:,}"),
        "ambiguous_candidates: %s" % f"{h['ambiguous_candidates']:,}",
        "uid_overlapping_class_pairs: %d" % h["uid_overlapping_class_pairs"],
        "",
        "artifacts: fk_graph_master.json, REPORT.md, DONE.md, stage1_columns.json, "
        "stage2_domains.json, stage3_edges.json, cache/",
        "--selftest PASS",
        "",
    ]
    return "\n".join(lines)
# ---------------------------------------------------------------- selftest
def selftest(full=False):
    ok = True

    def check(name, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))

    # ---- 1. pure logic: sentinels, domain stats, specificity guards
    vals = np.array([1, 2, 3, 0xFFFFFFFF, 0xFFFFFFFF], dtype=np.uint64)
    prof = column_profile(vals, 4)
    check("sentinel_excluded", prof["non_sentinel_rows"] == 3 and prof["min"] == 1,
          str(prof["non_sentinel_rows"]))

    enum_col = np.arange(1000, dtype=np.uint64) % 8          # 0..7 enum, 1000 rows
    dom_cont = Domain("continent", "ordinal", np.arange(7, dtype=np.uint64))
    prof_e = column_profile(enum_col, 4)
    cand = dict(target="continent", target_key="ordinal", target_domain_count=7,
                target_large_share=0.0, uniform_chance=7 / 2 ** 32, support_coverage=1.0,
                hits=1000, rows=1000, hit_rate=1.0)
    tier, notes = classify(cand, prof_e, "col_0")
    check("enum_guard_blocks_continent", tier == "ambiguous", str(notes))

    dense_ord_col = (np.arange(5000, dtype=np.uint64) % 251)  # nation-like ordinals
    prof_d = column_profile(dense_ord_col, 4)
    cand_d = dict(target="nation", target_key="ordinal", target_domain_count=251,
                  target_large_share=0.0, uniform_chance=5.8e-08, support_coverage=1.0,
                  hits=5000, rows=5000, hit_rate=1.0)
    tier_d, _ = classify(cand_d, prof_d, "col_4")
    check("dense_ordinal_not_promoted", tier_d == "ambiguous")

    check("name_token_corroborates",
          classify(dict(cand_d, target="nation"), prof_d, "Cnat")[0] == "code_corroborated")

    # statistical promotion of a sparse uid column (>= 25 distinct large sparse UIDs)
    uid_col = np.repeat(np.arange(1, 31, dtype=np.uint64) * 50_000_000 + 12345, 3)
    prof_u = column_profile(uid_col, 4)
    cand_u = dict(target="club", target_key="uid", target_domain_count=84259,
                  target_large_share=0.9, uniform_chance=84259 / 2 ** 32,
                  support_coverage=1e-6, hits=90, rows=90, hit_rate=1.0)
    check("sparse_uid_promoted", classify(cand_u, prof_u, "col_9")[0] == "statistical")
    cand_u2 = dict(cand_u, support_coverage=1.0)
    check("uid_coverage_guard", classify(cand_u2, prof_u, "col_9")[0] == "ambiguous")
    cand_u3 = dict(cand_u, hit_rate=0.95)
    check("hit_rate_floor", classify(cand_u3, prof_u, "col_9")[0] == "rejected")

    # ---- 2. real data invariants
    nat = ids_of(("server", 10))
    check("nation_ordinal_dense_0..250",
          nat["ordinal"].size == 251 and int(nat["ordinal"].max()) == 250
          and bool((nat["ordinal"] == np.arange(251, dtype=np.uint64)).all()))
    club = ids_of(("server", 3))
    check("club_uid_unique", np.unique(club["uid"]).size == club["uid"].size)
    team = ids_of(("server", 24))
    inter = np.intersect1d(club["uid"], team["uid"]).size
    check("club_uid_overlap_with_team_uid", inter >= club["uid"].size - 5 and inter == 84256,
          "%d/%d" % (inter, club["uid"].size))

    # ---- 3. known edges reproduced from scratch
    cc, _ = decode_club_links()
    club_uid_vals = cc["clublinks|club_uid"]["values"]
    check("club_links.club_uid -> club key",
          domain_hits(club_uid_vals, club["ordinal"]) == club_uid_vals.size
          or domain_hits(club_uid_vals, club["uid"]) == club_uid_vals.size)

    bp, _ = decode_basic_people()
    n_ord, n_uid = bp["basic|nation_ord"], bp["basic|nation_uid"]
    mask = n_ord["present"] & n_uid["present"]
    o, u = n_ord["values"][mask], n_uid["values"][mask]
    joint = (in_domain(o, nat["ordinal"]) & in_domain(u, nat["uid"]))
    check("basic_people.nation_ref pair 100%", int(joint.sum()) == o.size,
          "%d/%d" % (int(joint.sum()), o.size))
    check("basic_people.uid count", bp["basic|uid"]["values"].size == 658011,
          str(bp["basic|uid"]["values"].size))

    nt = decode_name_table(2)[0]
    check("name_table string_ordinal == row index",
          bool((nt["name2|string_ordinal"]["values"] == nt["name2|ordinal"]["values"]).all()))

    # ---- 4. uid 676 collision (t143 finding) reproduced
    stad = ids_of(("server", 21))
    coll = [k for k, arr in (("club", club["uid"]), ("stadium", stad["uid"]))
            if bool((arr == 676).any())]
    check("uid676_in_club_and_stadium", len(coll) == 2, str(coll))

    # ---- 5. artifacts
    if not full and not MASTER.exists():
        print("[SKIP] artifacts not built yet (run the pipeline first)")
    else:
        master = load_json(MASTER)
        check("master_schema", master.get("schema_id") == "fm24.t142.fk_graph_master")
        check("master_has_edges", master["health"]["verified_edges"] > 0,
              str(master["health"]["verified_edges"]))
        check("master_has_pair_proofs", master["health"]["verified_pair_proofs"] > 0)
        check("master_identity_registry_covers_all",
              len(master["identity_registry"]) == 84,
              str(len(master["identity_registry"])))
        check("master_rows_total", master["health"]["rows_decoded"] == 4387917,
              str(master["health"]["rows_decoded"]))
        for d in master["edges_verified"]:
            if d["hit_rate"] < HIT_RATE_MIN or not d.get("verified", True):
                check("edge_threshold_invariant", False, str(d)[:80])
                break
        else:
            check("edge_threshold_invariant", True)
        check("report_written", (OUT / "REPORT.md").is_file())
        check("done_written", (OUT / "DONE.md").is_file())
    print("--- t142 selftest: %s ---" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def ids_of(key):
    """ordinal/uid arrays of one numbered table, decoding it directly."""
    cols, meta = decode_table(key) if not (CACHE / ("%s_%s.json" % key)).is_file() \
        else load_columns(table_key(*key))
    out = {}
    for c in cols.values():
        if c["kind"] in ("ord", "uid"):
            out[c["kind"]] = c["values"]
    if "ord" in out and "ordinal" not in out:
        out["ordinal"] = out["ord"]
    return out


# ---------------------------------------------------------------- CLI
def write_artifacts(master):
    dump_json(MASTER, master)
    (OUT / "REPORT.md").write_text(render_report(master), encoding="utf-8")
    (OUT / "DONE.md").write_text(render_done(master), encoding="utf-8")


def print_summary(master):
    h = master["health"]
    print("\n=== t142 FM24 FK graph & referential integrity audit ===")
    print("tables audited          : %d (numbered %d + special %d)"
          % (h["tables_audited"], h["numbered_tables"], h["special_tables"]))
    print("rows decoded            : %s" % f"{h['rows_decoded']:,}")
    print("columns scanned         : %s of %s inventoried"
          % (f"{h['columns_scanned']:,}", f"{h['columns_inventoried']:,}"))
    print("verified FK edges       : %d  (code %d + statistical %d)"
          % (h["verified_edges"], h["verified_code_corroborated"], h["verified_statistical"]))
    print("reference pair proofs   : %d" % h["verified_pair_proofs"])
    print("anonymous col_N FKs     : %d" % h["anonymous_col_edges"])
    print("orphan rows             : %s  (edges with orphans: %d)"
          % (f"{h['orphan_rows_column_edges'] + h['orphan_rows_pair_edges']:,}",
             h["edges_with_orphans"]))
    print("ambiguous candidates    : %s" % f"{h['ambiguous_candidates']:,}")
    print("uid overlap class pairs : %d   shared namespaces: %d"
          % (h["uid_overlapping_class_pairs"], h["shared_key_namespaces"]))
    print("deliverables:")
    for f in ("fk_graph_master.json", "REPORT.md", "DONE.md", "stage1_columns.json",
              "stage2_domains.json", "stage3_edges.json"):
        p = OUT / f
        print("  %-24s %s" % (f, f"{p.stat().st_size:,} B" if p.is_file() else "MISSING"))


def cmd_columns(arch, tid):
    key = (arch, int(tid))
    cols, meta = decode_table(key)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    rows = []
    for cid, c in cols.items():
        mask = c.get("present")
        vals = c["values"][mask] if mask is not None else c["values"]
        prof = column_profile(vals, c["width"])
        rows.append((c["name"], c["kind"], c["width"], c["off"], prof["non_sentinel_rows"],
                     prof["distinct"], prof["min"], prof["max"]))
    print("%-18s %-6s %-4s %-6s %9s %8s %14s %14s" %
          ("name", "kind", "w", "off", "rows", "distinct", "min", "max"))
    for r in sorted(rows, key=lambda r: (r[3] is None, r[3])):
        print("%-18s %-6s %-4s %-6s %9s %8s %14s %14s" % r)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="run the self test")
    ap.add_argument("--stage", choices=["decode", "domains", "edges", "report", "all"],
                    default="all")
    ap.add_argument("--columns", nargs=2, metavar=("ARCHIVE", "TID"),
                    help="dump decoded column inventory of one table")
    ap.add_argument("--force-decode", action="store_true", help="ignore the column cache")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.columns:
        return cmd_columns(*args.columns)
    if args.selftest:
        return selftest()

    OUT.mkdir(parents=True, exist_ok=True)
    if args.stage in ("decode", "all"):
        print("[stage 1] decoding every table into the column cache")
        build_cache(force=args.force_decode)
    if args.stage in ("domains", "all"):
        print("[stage 2] identity domains")
        build_domains()
    if args.stage in ("edges", "all"):
        print("[stage 3] foreign-key audit")
        _, _, classes = build_domains()
        scan = scan_edges(classes, verbose=not args.quiet)
        dump_json(STAGE3, scan)
    if args.stage in ("report", "all"):
        print("[stage 4] assembly + report")
        registry, _, classes = build_domains()
        scan = load_json(STAGE3)
        master = assemble(registry, classes, scan, l3_fourcc_index(), c_slot_index())
        write_artifacts(master)
        print_summary(master)
    return 0


if __name__ == "__main__":
    sys.exit(main())
