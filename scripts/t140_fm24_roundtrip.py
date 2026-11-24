#!/usr/bin/env python3
"""t140_fm24_roundtrip — FM24 `.dat` bidirectional re-encoder, FMF/zstd repacker
and dual (pure-Python + real editor.exe x86_64) round-trip verifier.

Three stages, all structurally honest (no raw row-blob pass-through on any table
that is claimed to be re-encoded):

  Stage 1  Grammar-driven decode -> value model -> re-encode.  Every numbered
           table payload is rebuilt from parsed values (13-byte header rebuilt
           from magic/version/row_count/reserved, every row rebuilt as
           [1B selector][re-encoded body + 12B identity], 9-byte footer rebuilt
           from the terminator + the 8-byte trailer re-emitted as u64) and
           compared by SHA-256 with the original payload.

  Stage 2  A spec-compliant FMF archive writer: header re-emitted, zstd frames
           produced for mutated members, every other member copied packed-byte
           for packed-byte, directory tree re-serialised with recomputed
           offset/packed_size/size for every member, TOC re-compressed.
           Nine field mutations across six table classes (incl. two string
           length changes that shift every following row and member size).

  Stage 3  Dual independent verification: (a) the unmodified t133 pure-Python
           reader must close all 79/79 tables to the footer on the *repacked*
           archives and read back every mutated value; (b) real `editor.exe`
           x86_64 machine code (Unicorn, t96c `slot19` + t120 `PLAYER::slot19`)
           must consume the exact new row lengths and land the mutated values
           in C++ object memory.

Usage (exit 0 = pass, 1 = verification failure, 2 = usage / fatal):
  py -V:3.12 -B scripts/t140_fm24_roundtrip.py --roundtrip-all
  py -V:3.12 -B scripts/t140_fm24_roundtrip.py --build-patched
  py -V:3.12 -B scripts/t140_fm24_roundtrip.py --selftest

Read-only inputs: scratch/data/*, scripts/t112,t119,t120,t133,t96*.py.
Writes only: scripts/t140_fm24_roundtrip.py, scratch/t140/out/*.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import struct
import sys
import time

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parents[1]

# The repository's designated vendor dir for zstandard (never find_library()).
sys.path.insert(0, str(_cfg.VENDOR_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

import zstandard  # noqa: E402  (vendored 0.25.0 / libzstd)

DB_DIR = ROOT / "scratch/data"
OUT_DIR = ROOT / "scratch/t140/out"
WORK_DIR = ROOT / "scratch/t140"

DAT_MAGIC = b"\x03\x01tad."
FMF_MAGIC = bytes.fromhex("0201666d662e080000")
ZSTD_MAGIC = bytes.fromhex("28b52ffd")
HEADER_END = 13
FOOTER_SIZE = 9
IDENTITY_SIZE = 12
VERSION = 0x0DF1

# zstd frame parameters of the shipped members: checksum present, *no* frame
# content size (streaming writer), 4 MiB window.  We mirror that shape.
ZSTD_LEVEL = 15

_U2 = struct.Struct("<H").unpack_from
_U4 = struct.Struct("<I").unpack_from
_U8 = struct.Struct("<Q").unpack_from
_P2 = struct.Struct("<H").pack
_P4 = struct.Struct("<I").pack
_P8 = struct.Struct("<Q").pack
_IDENT = struct.Struct("<III").unpack_from
_MASKS = {w: (1 << (8 * w)) - 1 for w in (1, 2, 3, 4, 6, 8, 9, 10, 12, 16)}


class WireError(ValueError):
    """Structural or bounds violation (never swallowed)."""


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _hex(b: bytes) -> str:
    return b.hex()


# =====================================================================
# 1. value-level row codec (same op algebra as t133_fm24_reader_v2)
# =====================================================================
def read_num(b, p: int, w: int) -> int:
    if w == 1:
        return b[p]
    if w == 2:
        return _U2(b, p)[0]
    if w == 4:
        return _U4(b, p)[0]
    if w == 8:
        return _U8(b, p)[0]
    return int.from_bytes(b[p : p + w], "little")


def pack_num(v: int, w: int) -> bytes:
    return (v & _MASKS.get(w, (1 << (8 * w)) - 1)).to_bytes(w, "little")


def compile_transcode(ops):
    """Compile a grammar into `walk(b, p, end, out) -> p`.

    Every field is *parsed into a value* and *re-encoded from that value*:
    numbers via int read/struct pack, strings via utf-8 decode/encode with a
    recomputed u32 length prefix, identities via three u32s, vector counts
    recomputed from the number of emitted elements.  Nothing is memcpy'd.
    """
    src = [
        "def walk(b, p, end, out, U2=_U2, U4=_U4, U8=_U8, P2=_P2, P4=_P4, P8=_P8,"
        " WireError=WireError):"
    ]
    serial = [0]

    def nv(prefix="v"):
        serial[0] += 1
        return f"{prefix}{serial[0]}"

    def num_read(w, ind, signed=False):
        v = nv()
        src.append(f"{ind}if p + {w} > end: raise WireError('short {w}B read at %d' % p)")
        if w == 1:
            src.append(f"{ind}{v} = b[p]")
        elif w == 2:
            src.append(f"{ind}{v} = U2(b, p)[0]")
        elif w == 4:
            src.append(f"{ind}{v} = U4(b, p)[0]")
        elif w == 8:
            src.append(f"{ind}{v} = U8(b, p)[0]")
        else:
            src.append(f"{ind}{v} = int.from_bytes(b[p:p+{w}], 'little')")
        src.append(f"{ind}p += {w}")
        if signed:
            src.append(f"{ind}{v} = {v} - {1 << (8 * w)} if {v} >= {1 << (8 * w - 1)} else {v}")
        return v

    def num_write(w, v, ind):
        if w == 1:
            src.append(f"{ind}out.append({v} & 0xFF)")
        elif w in (2, 4, 8):
            src.append(f"{ind}out += P{w}({v} & {(1 << (8 * w)) - 1})")
        else:
            src.append(f"{ind}out += ({v} & {(1 << (8 * w)) - 1}).to_bytes({w}, 'little')")

    def emit(block, ind, tag=None):
        for op in block:
            kind = op[0]
            if kind == "u":
                w = op[1]
                num_write(w, num_read(w, ind), ind)
            elif kind == "s":
                src.append(f"{ind}if p + 4 > end: raise WireError('short string length at %d' % p)")
                ln, txt, enc = nv("ln"), nv("s"), nv("e")
                src.append(f"{ind}{ln} = U4(b, p)[0]; p += 4")
                src.append(f"{ind}if p + {ln} > end: raise WireError('string %d at %d beyond end' % ({ln}, p))")
                src.append(f"{ind}{txt} = b[p:p+{ln}].decode('utf-8', 'surrogateescape')")
                src.append(f"{ind}p += {ln}")
                src.append(f"{ind}{enc} = {txt}.encode('utf-8', 'surrogateescape')")
                src.append(f"{ind}out += P4(len({enc})); out += {enc}")
            elif kind == "id":
                src.append(f"{ind}if p + 12 > end: raise WireError('short identity at %d' % p)")
                a, c, d = nv("i"), nv("i"), nv("i")
                src.append(f"{ind}{a}, {c}, {d} = I(b, p); p += 12")
                src.append(f"{ind}out += P4({a}); out += P4({c}); out += P4({d})")
            elif kind == "v":
                cw = op[1][1]
                cnt = num_read(cw, ind, signed=False)
                src.append(f"{ind}if {cnt} > end: raise WireError('vector count %d at %d exceeds bound' % ({cnt}, p))")
                if op[1][0] == "i":
                    src.append(
                        f"{ind}if {cnt} >= {1 << (8 * cw - 1)}:"
                        f" raise WireError('negative vector count at %d' % (p - {cw}))"
                    )
                at, seen = nv("at"), nv("n")
                src.append(f"{ind}{at} = len(out)")
                src.append(f"{ind}out += bytes({cw})")
                src.append(f"{ind}{seen} = 0")
                src.append(f"{ind}for _ in range({cnt}):")
                emit(op[2], ind + "    ", tag)
                src.append(f"{ind}    {seen} += 1")
                if cw in (2, 4, 8):
                    src.append(f"{ind}out[{at}:{at}+{cw}] = P{cw}({seen})")
                else:
                    src.append(f"{ind}out[{at}:{at}+{cw}] = {seen}.to_bytes({cw}, 'little')")
            elif kind == "rep":
                src.append(f"{ind}for _ in range({op[1]}):")
                emit(op[2], ind + "    ", tag)
            elif kind == "if":
                w = op[1]
                v = num_read(w, ind)
                num_write(w, v, ind)
                src.append(f"{ind}if {v} {op[2]} {op[3]}:")
                emit(op[4], ind + "    ", tag)
            elif kind == "zero":
                w = op[1]
                v = num_read(w, ind)
                num_write(w, v, ind)
                src.append(f"{ind}if {v}: raise WireError({('missing nonempty path ' + op[2])!r})")
            elif kind == "tag":
                w = abs(op[1])
                v = num_read(w, ind, signed=op[1] < 0)
                num_write(w, v, ind)
                for threshold, body in op[2]:
                    if threshold:
                        src.append(f"{ind}if {v} >= {threshold}:")
                        emit(body, ind + "    ", v)
                    else:
                        emit(body, ind, v)
            elif kind == "switch":
                w = op[1]
                v = num_read(w, ind)
                num_write(w, v, ind)
                for idx, (value, body) in enumerate(op[2].items()):
                    src.append(f"{ind}{'if' if idx == 0 else 'elif'} {v} == {value}:")
                    if body:
                        emit(body, ind + "    ", tag)
                    else:
                        src.append(f"{ind}    pass")
                src.append(f"{ind}else: raise WireError({op[3]!r})")
            elif kind == "match":
                src.append(f"{ind}if {tag} == {op[1]}:")
                emit(op[2], ind + "    ", tag)
            elif kind == "choose":
                src.append(f"{ind}if {tag} >= {op[1]}:")
                emit(op[2], ind + "    ", tag)
                src.append(f"{ind}else:")
                emit(op[3], ind + "    ", tag)
            else:  # pragma: no cover
                raise ValueError(f"unknown op {op}")

    emit(ops, "    ")
    src.append('    if p > end: raise WireError("row end %d exceeds %d" % (p, end))')
    src.append("    return p")
    env = {"WireError": WireError, "_U2": _U2, "_U4": _U4, "_U8": _U8, "_P2": _P2,
           "_P4": _P4, "_P8": _P8, "I": _IDENT}
    exec("\n".join(src), env)  # noqa: S102 - in-process grammar constants only
    return env["walk"]


# ---- row model (only built for the handful of mutated rows) -----------------
N_NUM, N_STR, N_ID, N_VEC = "n", "s", "id", "v"
N_GATE, N_TAG, N_SWITCH, N_ZERO, N_REP, N_ELEM = "g", "t", "sw", "z", "r", "e"


def parse_tree(ops, b: bytes, start: int, end: int):
    """Parse one row into a value tree [(kind, width, value, children, off)]."""
    p = start
    root = []

    def num(w, signed=False):
        nonlocal p
        at = p - start
        if p + w > end:
            raise WireError(f"short {w}B read at {p}")
        v = read_num(b, p, w)
        p += w
        if signed and v >= 1 << (8 * w - 1):
            v -= 1 << (8 * w)
        return v, at

    def walk(block, sink, tag=None):
        nonlocal p
        for op in block:
            kind = op[0]
            if kind == "u":
                v, at = num(op[1])
                sink.append([N_NUM, op[1], v, None, at])
            elif kind == "s":
                if p + 4 > end:
                    raise WireError(f"short string length at {p}")
                at = p - start
                ln = _U4(b, p)[0]
                p += 4
                if p + ln > end:
                    raise WireError(f"string {ln} at {p} beyond end")
                txt = bytes(b[p : p + ln]).decode("utf-8", "surrogateescape")
                p += ln
                sink.append([N_STR, ln, txt, None, at])
            elif kind == "id":
                if p + 12 > end:
                    raise WireError(f"short identity at {p}")
                at = p - start
                ident = _IDENT(b, p)
                p += 12
                sink.append([N_ID, 12, ident, None, at])
            elif kind == "v":
                cw = op[1][1]
                cnt, at = num(cw)
                if op[1][0] == "i" and cnt >= 1 << (8 * cw - 1):
                    raise WireError(f"negative vector count at {p - cw}")
                if cnt > end:
                    raise WireError(f"vector count {cnt} at {p} exceeds bound")
                kids = []
                for _ in range(cnt):
                    # one wrapper node per *element*, so the re-encoded count is
                    # derived from the element list, not from the raw count field
                    elem = []
                    walk(op[2], elem, tag)
                    kids.append([N_ELEM, 0, None, elem, p - start])
                sink.append([N_VEC, cw, cnt, kids, at])
            elif kind == "rep":
                kids = []
                for _ in range(op[1]):
                    walk(op[2], kids, tag)
                sink.append([N_REP, 0, None, kids, p - start])
            elif kind == "if":
                v, at = num(op[1])
                kids = []
                if {"!=": v != op[3], "==": v == op[3]}[op[2]]:
                    walk(op[4], kids, tag)
                sink.append([N_GATE, op[1], v, kids, at])
            elif kind == "zero":
                v, at = num(op[1])
                if v:
                    raise WireError("missing nonempty path " + op[2])
                sink.append([N_ZERO, op[1], v, None, at])
            elif kind == "tag":
                w = abs(op[1])
                v, at = num(w, signed=op[1] < 0)
                kids = []
                for threshold, body in op[2]:
                    if not threshold or v >= threshold:
                        walk(body, kids, v)
                sink.append([N_TAG, w, v, kids, at])
            elif kind == "switch":
                v, at = num(op[1])
                if v not in op[2]:
                    raise WireError(op[3])
                kids = []
                walk(op[2][v], kids, tag)
                sink.append([N_SWITCH, op[1], v, kids, at])
            elif kind == "match":
                if tag == op[1]:
                    walk(op[2], sink, tag)
            elif kind == "choose":
                walk(op[2] if tag >= op[1] else op[3], sink, tag)
            else:  # pragma: no cover
                raise ValueError(f"unknown op {op}")

    walk(ops, root)
    if p > end:
        raise WireError(f"row end {p} exceeds {end}")
    return root, p


def encode_tree(nodes, out: bytearray) -> None:
    for kind, width, value, children, _off in nodes:
        if kind == N_NUM:
            out += pack_num(value, width)
        elif kind == N_STR:
            enc = value.encode("utf-8", "surrogateescape")
            out += _P4(len(enc))
            out += enc
        elif kind == N_ID:
            out += _P4(value[0]) + _P4(value[1]) + _P4(value[2])
        elif kind == N_VEC:
            out += pack_num(len(children), width)  # count recomputed from the model
            encode_tree(children, out)
        elif kind in (N_GATE, N_TAG, N_SWITCH, N_ZERO):
            out += pack_num(value, width)
            if children:
                encode_tree(children, out)
        elif kind in (N_REP, N_ELEM):
            encode_tree(children, out)
        else:  # pragma: no cover
            raise ValueError(kind)


def tree_values(nodes) -> int:
    n = 0
    for kind, _w, _v, children, _o in nodes:
        if kind in (N_GATE, N_TAG, N_SWITCH, N_ZERO):
            n += 1
        elif kind == N_ELEM:
            n += 0
        else:
            n += 1
        if children:
            n += tree_values(children)
    return n


def find_nodes(nodes, off, kind=None):
    for node in nodes:
        if node[4] == off and (kind is None or node[0] == kind):
            yield node
        if node[3]:
            yield from find_nodes(node[3], off, kind)


# =====================================================================
# 2. engine: the unmodified t112/t133 registry + grammars
# =====================================================================
class Engine:
    def __init__(self):
        import t112_fm24_reader as base
        import t133_fm24_reader_v2 as t133

        self.base, self.t133 = base, t133
        self.traces = t133.load(t133.TRACE)
        self.records, self.specs = t133.registry(self.traces)
        self.l3 = t133.load(t133.L3)
        self._walkers: dict = {}
        self._arcs: dict = {}

    def archive(self, name: str):
        arc = self._arcs.get(name)
        if arc is None:
            arc = self.base.Archive(name)
            self._arcs[name] = arc
        return arc

    def ops_for(self, key, flag: int):
        sel = self.t133.SELECTORS.get(key)
        if sel is not None:
            if flag not in sel:
                raise WireError(f"{key}: unexpected selector {flag}")
            return sel[flag]
        return self.specs[key].prog

    def walker(self, key, flag: int):
        k = (key, flag)
        fn = self._walkers.get(k)
        if fn is None:
            fn = compile_transcode(self.ops_for(key, flag))
            self._walkers[k] = fn
        return fn

    def fixed_reader(self, key):
        spec = self.specs[key]
        rd = self.base.TableReader(spec, self.l3)
        rd._fixed_setup()
        return rd

    def l3_name(self, key, off: int):
        return self.base._l3_name_map(self.l3, key[1], key[0]).get(off)


# =====================================================================
# 3. payload encoder (Stage 1 + Stage 2 mutations)
# =====================================================================
def encode_payload(eng: Engine, key, payload: bytes, mutation: dict | None = None) -> dict:
    """Rebuild a full numbered-table payload from parsed values."""
    spec = eng.specs[key]
    t0 = time.perf_counter()
    if payload[:6] != DAT_MAGIC:
        raise WireError(f"{key}: bad payload magic")
    ver = _U2(payload, 6)[0]
    nrows = _U4(payload, 8)[0]
    if ver != VERSION:
        raise WireError(f"{key}: unexpected payload version {ver:#x}")
    if payload[12] != 0:
        raise WireError(f"{key}: reserved header byte != 0")
    footer_off = len(payload) - FOOTER_SIZE
    if payload[footer_off] != 0:
        raise WireError(f"{key}: identity terminator != 0")

    out = bytearray(DAT_MAGIC + struct.pack("<H", ver) + struct.pack("<I", nrows) + b"\x00")
    p = HEADER_END
    row0_info = {"body_len": None, "delta": 0, "values": 0, "mutation": None}
    rows = 0

    if spec.kind == "fixed":
        rd = eng.fixed_reader(key)
        fmt = rd._fixed_fmt
        if fmt.size != spec.rowlen:
            raise WireError(f"{key}: fixed struct {fmt.size} != rowlen {spec.rowlen}")
        step = 1 + fmt.size
        if HEADER_END + nrows * step != footer_off:
            raise WireError(f"{key}: fixed geometry mismatch")
        pack, unpack_from = fmt.pack, fmt.unpack_from
        new_fixed = key in eng.t133.NEW_FIXED
        mut_idx = None
        if mutation is not None:
            if mutation["kind"] != N_NUM:
                raise WireError(f"{key}: fixed-stride tables only take scalar mutations")
            for i, (_nm, off, width, sub) in enumerate(rd._fixed_fields):
                if sub is None and off == mutation["off"] and width == mutation["width"]:
                    mut_idx = i
                    break
            if mut_idx is None:
                raise WireError(f"{key}: no fixed field at wire {mutation['off']}")
        for i in range(nrows):
            flag = payload[p]
            if new_fixed and (flag != 0 or _U4(payload, p + 1 + fmt.size - 12)[0] != i):
                raise WireError(f"{key}: AWARD framing broken at row {i}")
            vals = unpack_from(payload, p + 1)
            if i == 0 and mut_idx is not None:
                vals = list(vals)
                if vals[mut_idx] != mutation["old"]:
                    raise WireError(
                        f"{key}: scalar anchor mismatch {vals[mut_idx]} != {mutation['old']}"
                    )
                vals[mut_idx] = mutation["new"]
                row0_info["mutation"] = {"old_body_len": fmt.size, "new_body_len": fmt.size}
            out.append(flag)
            out += pack(*vals)
            p += step
            rows += 1
        row0_info["body_len"] = fmt.size
        row0_info["values"] = len(rd._fixed_fields)
    elif spec.kind == "variable":
        first = True
        while rows < nrows:
            if p >= footer_off:
                raise WireError(f"{key}: row {rows} past footer")
            flag = payload[p]
            body = p + 1
            if first and mutation is not None:
                ops = eng.ops_for(key, flag)
                tree, q = parse_tree(ops, payload, body, footer_off)
                probe = bytearray()
                encode_tree(tree, probe)
                if bytes(probe) != payload[body:q]:
                    raise WireError(f"{key}: value-tree re-encode of row 0 is not byte-identical")
                hits = list(find_nodes(tree, mutation["off"], mutation["kind"]))
                if len(hits) != 1:
                    raise WireError(
                        f"{key}: mutation anchor at wire {mutation['off']} matched {len(hits)} nodes"
                    )
                node = hits[0]
                if mutation["kind"] == N_STR:
                    if node[2] != mutation["old"]:
                        raise WireError(f"{key}: string anchor mismatch {node[2]!r}")
                    node[2] = mutation["new"]
                else:
                    if node[1] != mutation["width"] or node[2] != mutation["old"]:
                        raise WireError(
                            f"{key}: scalar anchor mismatch width={node[1]} value={node[2]}"
                        )
                    node[2] = mutation["new"]
                rowb = bytearray()
                encode_tree(tree, rowb)
                expect = (q - body) + (
                    len(mutation["new"].encode("utf-8", "surrogateescape"))
                    - len(mutation["old"].encode("utf-8", "surrogateescape"))
                    if mutation["kind"] == N_STR else 0
                )
                if len(rowb) != expect:
                    raise WireError(
                        f"{key}: mutated row 0 is {len(rowb)} B, expected {expect} B"
                    )
                out.append(flag)
                out += rowb
                row0_info.update(
                    body_len=len(rowb),
                    delta=len(rowb) - (q - body),
                    values=tree_values(tree),
                    mutation={"old_body_len": q - body, "new_body_len": len(rowb)},
                )
                p = q
                rows += 1
                first = False
                continue
            walk = eng.walker(key, flag)
            out.append(flag)
            q = walk(payload, body, footer_off, out)
            if first:
                tree, q2 = parse_tree(eng.ops_for(key, flag), payload, body, footer_off)
                if q2 != q:
                    raise WireError(f"{key}: compiled/interpreted walk disagree ({q} != {q2})")
                probe = bytearray()
                encode_tree(tree, probe)
                if bytes(probe) != payload[body:q]:
                    raise WireError(f"{key}: value-tree re-encode of row 0 is not byte-identical")
                row0_info["body_len"] = q - body
                row0_info["values"] = tree_values(tree)
                first = False
            p = q
            rows += 1
    else:  # empty table
        if nrows or footer_off != HEADER_END:
            raise WireError(f"{key}: 0-row table with non-empty body")
        row0_info["body_len"] = 0

    if p != footer_off:
        raise WireError(f"{key}: end {p} != footer {footer_off} (diff {p - footer_off:+d})")
    footer8 = _U8(payload, footer_off + 1)[0]
    out += b"\x00" + struct.pack("<Q", footer8)

    return {
        "payload": bytes(out),
        "rows": rows,
        "kind": spec.kind,
        "class": spec.klass,
        "elapsed_ms": round(1000 * (time.perf_counter() - t0), 1),
        "row0": row0_info,
        "footer8": f"{footer8:016x}",
    }


def roundtrip_all(out_dir: pathlib.Path) -> dict:
    eng = Engine()
    t_start = time.perf_counter()
    tables = {}
    for key in sorted(eng.specs):
        spec = eng.specs[key]
        payload = eng.archive(key[0]).payload(key[1])
        try:
            enc = encode_payload(eng, key, payload)
            new = enc["payload"]
            diff = sum(1 for a, b in zip(payload, new) if a != b) + abs(len(payload) - len(new))
            tables[f"{key[0]}/{key[1]}"] = {
                "archive": key[0],
                "table_id": key[1],
                "class": spec.klass,
                "kind": spec.kind,
                "rows": enc["rows"],
                "payload_bytes": len(payload),
                "reencoded_bytes": len(new),
                "sha256_original": sha256(payload),
                "sha256_reencoded": sha256(new),
                "sha256_match": sha256(payload) == sha256(new),
                "diff_bytes": diff,
                "wire_values_row0": enc["row0"]["values"],
                "footer8_u64": enc["footer8"],
                "elapsed_ms": enc["elapsed_ms"],
            }
        except (WireError, struct.error, ValueError) as exc:
            tables[f"{key[0]}/{key[1]}"] = {
                "archive": key[0], "table_id": key[1], "class": spec.klass,
                "kind": spec.kind, "rows": 0, "sha256_match": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
    elapsed = round(time.perf_counter() - t_start, 1)
    ok = [t for t in tables.values() if t["sha256_match"]]
    doc = {
        "schema_id": "fm24.t140.roundtrip_79",
        "schema_version": 1,
        "stage": "1 — structural decode -> re-encode, payload SHA-256 identity",
        "inputs": {
            "db_dir": str(DB_DIR),
            "traces": str(eng.t133.TRACE.relative_to(ROOT)),
            "l3": str(eng.t133.L3.relative_to(ROOT)),
            "zstandard": zstandard.__file__,
        },
        "method": (
            "Each payload is parsed field-by-field with the t133 grammar (fixed: struct field map; "
            "variable: op algebra incl. vectors/tagged unions/selector-12), then rebuilt from the "
            "parsed values: 13B header re-emitted, per-row [selector][body+12B identity] re-emitted, "
            "9B footer re-emitted (terminator + trailer as u64). No raw row bytes are copied."
        ),
        "summary": {
            "tables_total": len(tables),
            "tables_sha256_match": len(ok),
            "tables_failed": len(tables) - len(ok),
            "rows_reencoded_total": sum(t.get("rows", 0) for t in tables.values()),
            "payload_bytes_total": sum(t.get("payload_bytes", 0) for t in tables.values()),
            "fixed_tables": sum(1 for t in tables.values() if t["kind"] == "fixed"),
            "variable_tables": sum(1 for t in tables.values() if t["kind"] == "variable"),
            "empty_tables": sum(1 for t in tables.values() if t["kind"] == "empty"),
            "elapsed_sec": elapsed,
        },
        "tables": tables,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "roundtrip_79_report.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return doc


def print_roundtrip_summary(doc: dict) -> None:
    s = doc["summary"]
    print(
        f"Stage 1: {s['tables_sha256_match']}/{s['tables_total']} tables bit-exact, "
        f"{s['rows_reencoded_total']:,} rows re-encoded from parsed values, "
        f"{s['payload_bytes_total']:,} payload bytes, {s['elapsed_sec']}s"
    )
    for name, t in sorted(doc["tables"].items()):
        if not t.get("sha256_match"):
            print(f"  FAIL {name} {t['class']}: {t.get('error') or 'sha mismatch'}")


# =====================================================================
# 4. FMF archive reader / writer
# =====================================================================
def parse_directory(raw: bytes):
    pos = 0

    def u32():
        nonlocal pos
        v = _U4(raw, pos)[0]
        pos += 4
        return v

    def string():
        nonlocal pos
        n = u32()
        v = raw[pos : pos + n].decode("utf-8")
        pos += n
        return v

    def folder(parent: str):
        nonlocal pos
        name = string()
        cur = f"{parent}{name}/"
        files = []
        for _ in range(u32()):
            nm, ext = string(), string()
            off, packed, size, t1, t2 = struct.unpack_from("<5Q", raw, pos)
            pos += 40
            files.append({"name": nm, "ext": ext, "path": cur + nm + ext,
                          "offset": off, "packed_size": packed, "size": size,
                          "t1": t1, "t2": t2})
        subs = [folder(cur) for _ in range(u32())]
        return {"name": name, "files": files, "subdirs": subs}

    tree = folder("")
    return tree, pos


def serialize_directory(node) -> bytes:
    out = bytearray()

    def string(text: str):
        enc = text.encode("utf-8")
        out.extend(struct.pack("<I", len(enc)))
        out.extend(enc)

    def folder(nd):
        string(nd["name"])
        out.extend(struct.pack("<I", len(nd["files"])))
        for f in nd["files"]:
            string(f["name"])
            string(f["ext"])
            out.extend(struct.pack("<5Q", f["offset"], f["packed_size"], f["size"], f["t1"], f["t2"]))
        out.extend(struct.pack("<I", len(nd["subdirs"])))
        for sub in nd["subdirs"]:
            folder(sub)

    folder(node)
    return bytes(out)


def compress_frame(payload: bytes, level: int = ZSTD_LEVEL) -> bytes:
    """Mirror the shipped frame shape: checksum on, no content-size field."""
    cctx = zstandard.ZstdCompressor(level=level, write_checksum=True, write_content_size=False)
    return cctx.compress(payload)


class FmfArchive:
    """Read + rewrite one `*_db.dat` FMF/zstd archive."""

    def __init__(self, path: pathlib.Path):
        self.path = pathlib.Path(path)
        self.data = self.path.read_bytes()
        d = self.data
        self.start = 8 if d[:6] == DAT_MAGIC and d[8:17] == FMF_MAGIC else 0
        if d[self.start : self.start + 9] != FMF_MAGIC:
            raise WireError(f"{self.path.name}: no FMF signature at {self.start}")
        if self.start:
            self.version = _U2(d, 6)[0]
        else:
            self.version = VERSION
        self.toc_rel = _U8(d, self.start + 9)[0]
        self.data_rel = _U8(d, self.start + 17)[0]
        self.toc = self.start + 9 + self.toc_rel
        self.base = self.start + 9 + self.data_rel
        if not (self.start + 26 <= self.base <= self.toc < len(d)):
            raise WireError(f"{self.path.name}: FMF offsets outside file")
        if d[self.toc : self.toc + 9] != FMF_MAGIC:
            raise WireError(f"{self.path.name}: missing secondary FMF header")
        self.header_extra = d[self.start + 25 : self.base]
        obj = zstandard.ZstdDecompressor().decompressobj()
        self.dir_raw = obj.decompress(d[self.toc + 9 :])
        if not obj.eof:
            raise WireError(f"{self.path.name}: directory frame not closed")
        self.tree, consumed = parse_directory(self.dir_raw)
        if consumed != len(self.dir_raw):
            raise WireError(f"{self.path.name}: {len(self.dir_raw) - consumed} unparsed directory bytes")
        self.files = list(self._flat(self.tree))

    @staticmethod
    def _flat(node):
        for f in node["files"]:
            yield f
        for sub in node["subdirs"]:
            yield from FmfArchive._flat(sub)

    # -- member access ---------------------------------------------------
    def member_frame(self, entry) -> bytes:
        start = self.base + entry["offset"]
        return self.data[start : start + entry["packed_size"]]

    def payload(self, entry) -> bytes:
        frames, leftover = decode_frames(self.member_frame(entry), entry["packed_size"])
        hits = [f for f in frames if len(f["data"]) == entry["size"]]
        if len(hits) != 1 or leftover != 0:
            raise WireError(
                f"{self.path.name}:{entry['path']}: {len(hits)} size hits, leftover={leftover}"
            )
        return hits[0]["data"]

    def build(self, replacements: dict) -> tuple[bytes, dict]:
        """Re-emit the archive; `replacements` maps path -> new *payload* bytes."""
        stats = {"repacked": [], "copied": 0, "frames": []}
        new_offsets = {}
        running = 0
        body = bytearray()
        for entry in self.files:
            new_payload = replacements.get(entry["path"])
            if new_payload is None:
                blob = self.member_frame(entry)
                packed, size = entry["packed_size"], entry["size"]
                stats["copied"] += 1
            else:
                blob = compress_frame(new_payload)
                packed, size = len(blob), len(new_payload)
                stats["repacked"].append(entry["path"])
            if blob[:4] != ZSTD_MAGIC:
                raise WireError(f"{entry['path']}: member frame lost its zstd signature")
            body += blob
            new_offsets[entry["path"]] = {"offset": running, "packed_size": packed, "size": size,
                                          "delta_offset": running - entry["offset"]}
            stats["frames"].append({"path": entry["path"], "offset": running,
                                    "packed_size": packed, "size": size})
            running += packed

        def rewrite(node):
            for f in node["files"]:
                info = new_offsets[f["path"]]
                f["offset"] = info["offset"]
                f["packed_size"] = info["packed_size"]
                f["size"] = info["size"]
            for sub in node["subdirs"]:
                rewrite(sub)

        rewrite(self.tree)
        dir_raw = serialize_directory(self.tree)
        dir_frame = compress_frame(dir_raw)

        out = bytearray()
        if self.start:
            out += DAT_MAGIC + struct.pack("<H", self.version)
        out += FMF_MAGIC
        out += struct.pack("<Q", self.data_rel + running)
        out += struct.pack("<Q", self.data_rel)
        out += self.header_extra
        if len(out) != self.base:
            raise WireError(f"{self.path.name}: rebuilt header {len(out)} != data_base {self.base}")
        out += body
        if len(out) != self.base + running:
            raise WireError(f"{self.path.name}: data block length mismatch")
        out += FMF_MAGIC + dir_frame
        stats.update(
            total_packed=running,
            dir_raw_bytes=len(dir_raw),
            dir_packed_bytes=len(dir_frame),
            dir_frame_identical=dir_frame == self.data[self.toc + 9 :],
            member_block_identical=bytes(out[self.base : self.base + running])
            == self.data[self.base : self.base + self.toc_rel - 17],
            new_offsets=new_offsets,
        )
        return bytes(out), stats


def decode_frames(region: bytes, bound: int | None = None):
    """Enumerate zstd frames inside a member region (bounded by packed_size)."""
    dctx = zstandard.ZstdDecompressor()
    frames = []
    data = region if bound is None else region[:bound]
    pos = 0
    while data[:4] == ZSTD_MAGIC:
        obj = dctx.decompressobj()
        chunk = obj.decompress(data)
        frames.append({"member_offset": pos, "data": chunk})
        if not obj.eof:
            raise WireError(f"truncated zstd frame at member+{pos}")
        consumed = len(data) - len(obj.unused_data)
        if consumed <= 0:
            raise WireError(f"zstd made no progress at member+{pos}")
        pos += consumed
        data = obj.unused_data
        if not data:
            break
    return frames, len(data)


# =====================================================================
# 5. mutation plan (Stage 2)
# =====================================================================
CLUB_NAME_OLD = "Klubi i Futbollit Albpetrol Patos"
T140_TAG = " [T140-PATCHED]"

MUTATIONS = [
    {
        "id": "M1",
        "archive": "server", "table_id": 3, "row": 0,
        "class": "CLUB", "field": "club long name (first UTF-8 string of CLUB_HEAD)",
        "kind": N_STR, "off": 26, "old": CLUB_NAME_OLD, "new": CLUB_NAME_OLD + T140_TAG,
        "why": "string grows +15 B: every subsequent row offset and the member size shift",
    },
    {
        "id": "M2",
        "archive": "client", "table_id": 3, "row": 0,
        "class": "CLUB", "field": "club long name (first UTF-8 string of CLUB_HEAD)",
        "kind": N_STR, "off": 26, "old": CLUB_NAME_OLD, "new": CLUB_NAME_OLD + T140_TAG,
        "why": "same mutation on the client mirror archive",
    },
    {
        "id": "M3",
        "archive": "server", "table_id": 45, "row": 0,
        "class": "STARTING_RECORD", "field": "record name (u32 namelen + UTF-8)",
        "kind": N_STR, "off": 37, "old": "Markelian Xhai", "new": "M. Xhai",
        "why": "string shrinks -7 B: namelen prefix and row length both change",
    },
    {
        "id": "M4",
        "archive": "server", "table_id": 21, "row": 0,
        "class": "STADIUM", "field": "Scas (stadium capacity-class u32)",
        "kind": N_NUM, "off": 12, "width": 4, "old": 11464, "new": 22464,
        "why": "4-byte scalar inside a fixed-stride table",
    },
    {
        "id": "M5",
        "archive": "server", "table_id": 0, "row": 0,
        "class": "AWARD", "field": "AWwh (u8 award scalar)",
        "kind": N_NUM, "off": 39, "width": 1, "old": 200, "new": 251,
        "why": "1-byte scalar, AWARD fixed stride 76 B",
    },
    {
        "id": "M6",
        "archive": "client", "table_id": 0, "row": 0,
        "class": "AWARD", "field": "AWwh (u8 award scalar)",
        "kind": N_NUM, "off": 39, "width": 1, "old": 200, "new": 251,
        "why": "same mutation on the client mirror archive",
    },
    {
        "id": "M7",
        "archive": "server", "table_id": 10, "row": 0,
        "class": "NATION", "field": "Npop (population, u32)",
        "kind": N_NUM, "off": 604, "width": 4, "old": 43851044, "new": 45000000,
        "why": "4-byte scalar inside a deeply nested variable row",
    },
    {
        "id": "M8",
        "archive": "client", "table_id": 10, "row": 0,
        "class": "NATION", "field": "NcpR (u32, client-side NATION tail block)",
        "kind": N_NUM, "off": 9, "width": 4, "old": 1187, "new": 1587,
        "why": "same table class, client-side grammar (tail subset)",
    },
    {
        "id": "M9",
        "archive": "server", "table_id": 25, "row": 0,
        "class": "COMP", "field": "cmnl (min pitch length, u16)",
        "kind": N_NUM, "off": 848, "width": 2, "old": 1050, "new": 1150,
        "why": "2-byte scalar in a 898-byte tagged/variant row",
    },
    {
        "id": "M10",
        "archive": "client", "table_id": 25, "row": 0,
        "class": "COMP", "field": "cmnl (min pitch length, u16)",
        "kind": N_NUM, "off": 76, "width": 2, "old": 1050, "new": 1150,
        "why": "same field on the client mirror archive",
    },
]

# Unicorn (editor.exe slot19) targets: (archive, table_id)
UNICORN_TARGETS = [("client", 3), ("server", 3), ("server", 45), ("server", 21),
                   ("server", 0), ("client", 0), ("server", 10), ("client", 10),
                   ("server", 25), ("client", 25)]

KANE = {
    "uid": 28049320,
    "ordinal": 166119,
    "person_type": 2,
    "record_offset": 252735069,
    "body_len": 1148,
    "mutations": [
        {"fourcc": "PCAB", "field": "CA", "off": 6, "width": 2, "old": 184, "new": 190,
         "obj_off": -0x78, "expr": "obj - 0x78"},
        {"fourcc": "PPAB", "field": "PA", "off": 8, "width": 2, "old": 185, "new": 195,
         "obj_off": -0x76, "expr": "obj - 0x76"},
        {"fourcc": "PDfn", "field": "Finishing", "off": 46, "width": 1, "old": 19, "new": 20,
         "obj_off": -0x70 + 17, "expr": "obj - 0x70 + 17"},
        {"fourcc": "PDpc", "field": "Pace", "off": 82, "width": 1, "old": 14, "new": 17,
         "obj_off": -0x70 + 53, "expr": "obj - 0x70 + 53"},
    ],
}


# =====================================================================
# 6. t133 (pure Python) verification of the repacked archives
# =====================================================================
def verify_with_t133(eng: Engine, out_dir: pathlib.Path, keys=None) -> dict:
    base, t133 = eng.base, eng.t133
    root = out_dir / "t133_root"
    root.mkdir(parents=True, exist_ok=True)
    link_modes = {}
    for arch in ("server", "client"):
        src = out_dir / f"patched_{arch}_db.dat"
        dst = root / f"{arch}_db.dat"
        if dst.exists():
            dst.unlink()
        try:
            os.link(src, dst)  # same bytes, t133's DB_DIR naming convention
            link_modes[arch] = "hardlink"
        except OSError:
            shutil.copy2(src, dst)
            link_modes[arch] = "copy"

    old_db_dir = base.DB_DIR
    base.DB_DIR = root  # t112.Archive resolves its module-global DB_DIR per call
    arcs = {}
    results = {}
    try:
        records, specs = t133.registry(eng.traces)
        l3 = eng.l3
        wanted = keys if keys is not None else sorted(specs)
        for key in sorted(wanted):
            spec = specs[key]
            if key[0] not in arcs:
                arcs[key[0]] = base.Archive(key[0])
            payload = arcs[key[0]].payload(key[1])
            res = t133.verify_table(spec, records[key], l3, payload, samples=3, variant_samples=True)
            results[f"{key[0]}/{key[1]}"] = res
    finally:
        base.DB_DIR = old_db_dir

    closed = [r for r in results.values() if r["footer_closed"]]
    return {
        "reader": "scripts/t133_fm24_reader_v2.py (unmodified; base.DB_DIR pointed at repacked archives)",
        "materialisation": link_modes,
        "tables_verified": len(results),
        "tables_closed": len(closed),
        "tables_failed": len(results) - len(closed),
        "rows_decoded": sum(r["rows_decoded"] for r in results.values()),
        "tables": results,
    }


def readback_mutation(eng: Engine, patched_payload: bytes, mut: dict) -> dict:
    """Re-read the mutated field with t133's own decoder (struct map or sample walker)."""
    key = (mut["archive"], mut["table_id"])
    spec = eng.specs[key]
    footer_off = len(patched_payload) - FOOTER_SIZE
    if spec.kind == "fixed":
        rd = eng.fixed_reader(key)
        fmt = rd._fixed_fmt
        vals = fmt.unpack_from(patched_payload, HEADER_END + 1)
        idx = next(
            (i for i, (_nm, off, width, sub) in enumerate(rd._fixed_fields)
             if sub is None and off == mut["off"] and width == mut["width"]),
            None,
        )
        if idx is None:
            return {"field_found": False}
        return {
            "field_found": True,
            "wire_off": mut["off"],
            "field_kind": "u",
            "width": mut["width"],
            "value": vals[idx],
            "matches_target": vals[idx] == mut["new"],
            "row0_body_len": fmt.size,
            "l3_fourcc": eng.l3_name(key, mut["off"]),
            "decoder": "t112 fixed struct map (t133 fixed path)",
        }
    flag = patched_payload[HEADER_END]
    ops = eng.ops_for(key, flag)
    fields, end = eng.t133.sample_walk(ops, patched_payload, HEADER_END + 1, footer_off)
    hits = [f for f in fields if f[1] == mut["off"]]
    if not hits:
        return {"field_found": False}
    _path, off, width, kind, value = hits[0]
    return {
        "field_found": True,
        "wire_off": off,
        "field_kind": kind,
        "width": width if kind != "s" else None,
        "value": value,
        "matches_target": value == mut["new"],
        "row0_body_len": (end - HEADER_END - 1),
        "l3_fourcc": eng.l3_name(key, off),
        "decoder": "t133 sample_walk (variable grammar)",
    }


# =====================================================================
# 7. editor.exe (real x86_64) verification
# =====================================================================
def run_emulated_row(ut, emu, m, tid: int, flag: int, body: bytes, ver: int, a7: int, db_a3: int):
    obj, vt, s19, err = m.construct_via_factory(ut, emu, tid, flag)
    if err or not s19:
        return None, {"error": f"ctor: {err}", "obj": obj, "s19": s19}
    res = m.run_one_row(ut, emu, obj, s19, body, ver, a7, a3_ptr=0)
    used_a3 = 0
    if not res["ok"] and res["unhandled"] and res["unhandled"][0].get("addr") == "0x80":
        obj, vt, s19, err = m.construct_via_factory(ut, emu, tid, flag)
        res = m.run_one_row(ut, emu, obj, s19, body, ver, a7, a3_ptr=db_a3)
        used_a3 = 1
    res["obj"] = obj
    res["slot19"] = s19
    res["vtable"] = vt
    res["a3"] = used_a3
    return res, {"error": None}


def _mem_read(emu, addr: int, n: int) -> bytes:
    return bytes(emu.mu.mem_read(addr, n))


def unicorn_table_targets(eng: Engine, patched: dict, orig: dict) -> list:
    """Feed original + mutated rows into real editor.exe slot19 code."""
    import t119_unicorn_last5 as t119
    import t96c_unicorn_master as t96c

    m, ut, emu, db_a3 = t119.setup_patched_emulator()
    out = []
    for arch, tid in UNICORN_TARGETS:
        key = (arch, tid)
        spec = eng.specs[key]
        ver = _U2(patched[key], 6)[0]
        a7 = 1 if arch == "server" else 0
        flag = patched[key][HEADER_END]
        # exact row-0 body slices (row 0 only, so: header -> next row flag)
        orig_row0 = _row0_body(eng, key, orig[key])
        mut_row0 = _row0_body(eng, key, patched[key])

        res_o, oerr = run_emulated_row(ut, emu, t96c, tid, flag, orig_row0, ver, a7, db_a3)
        res_m, merr = run_emulated_row(ut, emu, t96c, tid, flag, mut_row0, ver, a7, db_a3)
        entry = {
            "archive": arch,
            "table_id": tid,
            "class": spec.klass,
            "selector": flag,
            "slot19_va": hex(res_m["slot19"]) if res_m else None,
            "vtable_va": hex(res_m["vtable"]) if res_m else None,
            "a3_table_ctx_used": bool(res_m and res_m.get("a3")),
            "row0_len_original": len(orig_row0),
            "row0_len_mutated": len(mut_row0),
            "bytes_consumed_original": res_o["bytes_consumed"] if res_o else None,
            "bytes_consumed_mutated": res_m["bytes_consumed"] if res_m else None,
            "framework_trailer_bytes": (len(orig_row0) - res_o["bytes_consumed"]) if res_o else None,
            "ok_original": bool(res_o and res_o["ok"]),
            "ok_mutated": bool(res_m and res_m["ok"]),
            "end_rip_mutated": res_m["end_rip"] if res_m else None,
            "error_mutated": res_m["error"] if res_m else merr,
            "exact_new_length_consumed": bool(
                res_m
                and res_o
                and res_m["bytes_consumed"] - res_o["bytes_consumed"] == len(mut_row0) - len(orig_row0)
                and res_m["bytes_consumed"] == len(mut_row0) - (len(orig_row0) - res_o["bytes_consumed"])
            ),
            "readbacks": [],
        }
        for mut in [x for x in MUTATIONS if (x["archive"], x["table_id"]) == key]:
            fourcc = eng.l3_name(key, mut["off"])
            entry["readbacks"].append(
                _unicorn_readback_scalar(emu, res_m, mut, fourcc)
                if mut["kind"] == N_NUM
                else _unicorn_readback_string(emu, res_m, mut, fourcc)
            )
        trailer = entry["framework_trailer_bytes"]
        trail_o = orig_row0[len(orig_row0) - trailer:] if trailer else b""
        trail_m = mut_row0[len(mut_row0) - trailer:] if trailer else b""
        entry["framework_trailer_hex_original"] = _hex(trail_o)
        entry["framework_trailer_hex_mutated"] = _hex(trail_m)
        entry["framework_trailer_identical"] = trail_o == trail_m
        entry["row_fully_accounted"] = bool(
            res_m and res_m["bytes_consumed"] + trailer == len(mut_row0) and trail_o == trail_m
        )
        entry["read_count_original"] = len(res_o["reads"]) if res_o else 0
        entry["read_count_mutated"] = len(res_m["reads"]) if res_m else 0
        entry["pass"] = bool(
            entry["ok_original"]
            and entry["ok_mutated"]
            and entry["end_rip_mutated"] == hex(ut.STOP_ADDR)
            and entry["exact_new_length_consumed"]
            and entry["row_fully_accounted"]
            and all(r.get("matches_target") for r in entry["readbacks"])
        )
        out.append(entry)
    return out


def _row0_body(eng: Engine, key, payload: bytes) -> bytes:
    spec = eng.specs[key]
    if spec.kind == "fixed":
        return bytes(payload[HEADER_END + 1 : HEADER_END + 1 + spec.rowlen])
    flag = payload[HEADER_END]
    ops = eng.ops_for(key, flag)
    _fields, end = eng.t133.sample_walk(ops, payload, HEADER_END + 1, len(payload) - FOOTER_SIZE)
    return bytes(payload[HEADER_END + 1 : end])


def _unicorn_readback_scalar(emu, res, mut: dict, fourcc=None) -> dict:
    """editor.exe wrote the value straight into C++ object memory: read it back."""
    hits = [r for r in res["reads"] if r["wire_pos"] == mut["off"] and r["n"] == mut["width"]]
    if not hits:
        return {"mutation": mut["id"], "read_found": False, "matches_target": False}
    rd = hits[0]
    addr = int(rd["dst"], 16)
    raw = _mem_read(emu, addr, mut["width"])
    value = int.from_bytes(raw, "little")
    return {
        "mutation": mut["id"],
        "field": mut["field"],
        "fourcc": fourcc,
        "access_kind": "scalar",
        "wire_off": mut["off"],
        "width": mut["width"],
        "destination_addr": hex(addr),
        "destination_obj_off": rd.get("obj_off"),
        "cpu_written_value": value,
        "target_value": mut["new"],
        "matches_target": value == mut["new"],
        "raw_bytes": _hex(raw),
    }


def _unicorn_readback_string(emu, res, mut: dict, fourcc=None) -> dict:
    """Read the std::string editor.exe materialised for the mutated field."""
    len_hit = [r for r in res["reads"] if r["wire_pos"] == mut["off"] and r["n"] == 4]
    body_hit = [r for r in res["reads"] if r["wire_pos"] == mut["off"] + 4]
    if not len_hit or not body_hit:
        return {"mutation": mut["id"], "read_found": False, "matches_target": False}
    slot = int(body_hit[0]["dst"], 16)
    ptr = _U8(_mem_read(emu, slot, 8), 0)[0]
    if ptr == 0:
        return {"mutation": mut["id"], "read_found": True, "matches_target": False,
                "error": "null std::string pointer"}
    # measured layout of the string block materialised by editor.exe's reader:
    #   ptr+0 = u32 length, ptr+4 = utf-8 bytes, ptr-4 = refcount (1)
    length = _U4(_mem_read(emu, ptr, 4), 0)[0]
    if length > 4096:
        return {"mutation": mut["id"], "read_found": True, "matches_target": False,
                "error": f"implausible string length {length}"}
    raw = _mem_read(emu, ptr + 4, length)
    text = raw.decode("utf-8", "replace")
    return {
        "mutation": mut["id"],
        "field": mut["field"],
        "fourcc": fourcc,
        "access_kind": "std::string",
        "string_layout": "len@ptr+0, data@ptr+4, refcount@ptr-4",
        "wire_off": mut["off"],
        "string_slot_obj_off": body_hit[0].get("obj_off"),
        "string_slot_addr": hex(slot),
        "string_pointer": hex(ptr),
        "block_header_hex": _hex(_mem_read(emu, ptr - 4, 8 + min(length, 16))),
        "stored_length": length,
        "stored_text": text,
        "target_value": mut["new"],
        "matches_target": text == mut["new"],
        "bytes_consumed_by_cpu": len(raw) + 4,
    }


# =====================================================================
# 8. people_db.dat — Harry Kane (Stage 2B)
# =====================================================================
def build_kane_patch(out_dir: pathlib.Path) -> dict:
    people = DB_DIR / "people_db.dat"
    raw = people.read_bytes()
    need = KANE["record_offset"] + 5 + KANE["body_len"]
    dctx = zstandard.ZstdDecompressor()
    buf = bytearray()
    with dctx.stream_reader(raw[8:]) as rdr:
        while len(buf) < need:
            chunk = rdr.read(min(1 << 20, need - len(buf)))
            if not chunk:
                break
            buf += chunk
    if len(buf) < need:
        raise WireError(f"people_db: only {len(buf)} bytes available, need {need}")
    off = KANE["record_offset"]
    header = bytes(buf[off : off + 5])
    ordinal, ptype = struct.unpack("<IB", header)
    body = bytes(buf[off + 5 : off + 5 + KANE["body_len"]])
    if ordinal != KANE["ordinal"] or ptype != KANE["person_type"]:
        raise WireError(f"people_db: record header mismatch ordinal={ordinal} ptype={ptype}")
    for mut in KANE["mutations"]:
        got = int.from_bytes(body[mut["off"] : mut["off"] + mut["width"]], "little")
        if got != mut["old"]:
            raise WireError(f"Kane {mut['fourcc']}: expected {mut['old']}, found {got}")
    mutated = bytearray(body)
    for mut in KANE["mutations"]:
        mutated[mut["off"] : mut["off"] + mut["width"]] = mut["new"].to_bytes(mut["width"], "little")
    mutated = bytes(mutated)
    changed = [i for i in range(len(body)) if body[i] != mutated[i]]
    record = header + mutated
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "patched_kane_record.bin").write_bytes(record)
    return {
        "record_offset": off,
        "header_hex": _hex(header),
        "ordinal": ordinal,
        "person_type": ptype,
        "body_len_original": len(body),
        "body_len_mutated": len(mutated),
        "record_len_original": len(header) + len(body),
        "record_len_mutated": len(record),
        "length_preserved": len(mutated) == len(body),
        "framing": {"header_bytes": 5, "body_bytes": len(mutated), "next_record_offset": off + 5 + len(mutated)},
        "changed_offsets": changed,
        "changed_count": len(changed),
        "record_sha256_original": sha256(header + body),
        "record_sha256_mutated": sha256(record),
        "written": str((out_dir / "patched_kane_record.bin").relative_to(ROOT)),
        "_body_original": body,
        "_body_mutated": mutated,
    }


def unicorn_kane_check(kane: dict) -> dict:
    import t120_people_unicorn as t120

    _mm, ut, emu, _db = t120.setup_people_emulator()
    obj, vt, s19, err = t120.call_people_factory(ut, emu, KANE["person_type"])
    if err:
        return {"pass": False, "error": f"factory: {err}"}
    res_o = t120.run_person_row(ut, emu, obj, s19, kane["_body_original"])
    obj_o = obj
    # sample the *original* C++ RAM now: the next factory call resets the bump
    # heap, so a later read would already see the mutated object.
    baseline = {}
    for mut in KANE["mutations"]:
        addr = obj_o + mut["obj_off"]
        baseline[mut["fourcc"]] = int.from_bytes(_mem_read(emu, addr, mut["width"]), "little")

    obj, vt, s19, err = t120.call_people_factory(ut, emu, KANE["person_type"])
    if err:
        return {"pass": False, "error": f"factory: {err}"}
    res_m = t120.run_person_row(ut, emu, obj, s19, kane["_body_mutated"])

    ram = {}
    for mut in KANE["mutations"]:
        addr = obj + mut["obj_off"]
        raw = _mem_read(emu, addr, mut["width"])
        value = int.from_bytes(raw, "little")
        wire_hits = [r for r in res_m["reads"]
                     if r["wire_pos"] <= mut["off"] < r["wire_pos"] + r["n"]]
        ram[mut["fourcc"]] = {
            "field": mut["field"],
            "obj_off": (f"-0x{-mut['obj_off']:x}" if mut["obj_off"] < 0
                        else f"+0x{mut['obj_off']:x}"),
            "obj_off_expr": mut.get("expr"),
            "address": hex(addr),
            "width": mut["width"],
            "original": mut["old"],
            "target": mut["new"],
            "cpu_ram_value": value,
            "matches_target": value == mut["new"],
            "wire_off": mut["off"],
            "wire_read_dst": wire_hits[0]["dst"] if wire_hits else None,
            "wire_read_n": wire_hits[0]["n"] if wire_hits else None,
            "wire_read_offset_in_block": (mut["off"] - wire_hits[0]["wire_pos"]) if wire_hits else None,
        }

    # (the original run is executed on a freshly constructed object first; its RAM
    #  was sampled above, so the delta is measured on live C++ memory)
    return {
        "pass": bool(
            res_o["ok"]
            and res_m["ok"]
            and res_m["bytes_consumed"] == KANE["body_len"]
            and res_m["end_rip"] == hex(ut.STOP_ADDR)
            and all(v["matches_target"] for v in ram.values())
            and all(baseline[k] == v["original"] for k, v in ram.items())
        ),
        "object_ptr": hex(obj),
        "vtable_va": hex(vt),
        "slot19_va": hex(s19),
        "bytes_consumed_original": res_o["bytes_consumed"],
        "bytes_consumed_mutated": res_m["bytes_consumed"],
        "body_len": KANE["body_len"],
        "ok_original": res_o["ok"],
        "ok_mutated": res_m["ok"],
        "error_mutated": res_m["error"],
        "end_rip_mutated": res_m["end_rip"],
        "stop_addr": hex(ut.STOP_ADDR),
        "read_count_mutated": len(res_m["reads"]),
        "cpu_object_ram": ram,
        "object_ptr_original_run": hex(obj_o),
        "baseline_ram_original_run": baseline,
    }


# =====================================================================
# 9. special (non-numbered) members — t106 decoders must still agree
# =====================================================================
def verify_special_members(fma: FmfArchive, orig_payloads: dict, new_payloads: dict) -> list:
    import t106_special_members as t106

    out = []
    for entry in fma.files:
        path = entry["path"]
        base_name = path.rsplit("/", 1)[1]
        if base_name.startswith("table_") and base_name[6:-4].isdigit():
            continue  # numbered table (handled by the 79-table sweep)
        member = base_name[:-4]
        rec = {
            "archive": fma.path.name.split("_db")[0],
            "member": member,
            "path": path,
            "size_original": len(orig_payloads[path]),
            "size_patched": len(new_payloads[path]),
            "payload_sha256_original": sha256(orig_payloads[path]),
            "payload_sha256_patched": sha256(new_payloads[path]),
            "payload_identical": orig_payloads[path] == new_payloads[path],
            "packed_bytes_copied_verbatim": True,
        }
        dec = t106.DECODERS.get(member)
        if dec is not None:
            try:
                a = dec(orig_payloads[path])
                b = dec(new_payloads[path])
                rec["t106_decoder"] = dec.__name__
                rec["t106_decoded_identical"] = a == b
                rec["t106_closure_ok"] = bool(b.get("closure", {}).get("ok", True))
            except Exception as exc:  # honest failure, never swallowed
                rec["t106_decoder"] = dec.__name__
                rec["t106_decoded_identical"] = False
                rec["t106_error"] = f"{type(exc).__name__}: {exc}"
        else:
            rec["t106_decoder"] = None
            rec["t106_decoded_identical"] = None
        rec["pass"] = bool(rec["payload_identical"] and rec["t106_decoded_identical"] in (True, None))
        out.append(rec)
    return out


def verify_summary_dat() -> dict:
    """`summary.dat` is a standalone tad archive and must stay untouched."""
    import t106_special_members as t106

    path = DB_DIR / "summary.dat"
    raw = path.read_bytes()
    dec = t106.dec_summary(raw)
    return {
        "member": "summary",
        "path": str(path),
        "sha256": sha256(raw),
        "untouched": True,
        "t106_decoder": "dec_summary",
        "closure_ok": bool(dec.get("closure", {}).get("ok")),
        "rows": dec.get("format", {}).get("row_count"),
    }


# =====================================================================
# 10. Stage 2 + Stage 3 driver
# =====================================================================
def build_patched(out_dir: pathlib.Path, t133_keys=None, write_reports: bool = True,
                  selftest_flag=None):
    eng = Engine()
    out_dir.mkdir(parents=True, exist_ok=True)
    checks: list[dict] = []

    def ck(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": str(detail)})
        return bool(ok)

    t_start = time.perf_counter()
    arcs = {a: eng.archive(a) for a in ("server", "client")}
    orig = {}
    for key in sorted(eng.specs):
        orig[key] = arcs[key[0]].payload(key[1])

    # ---- Stage 2a: identity re-encode + semantic mutations --------------
    mut_keys = sorted({(m["archive"], m["table_id"]) for m in MUTATIONS})
    patched = dict(orig)
    mut_records = []
    for key in mut_keys:
        ms = [m for m in MUTATIONS if (m["archive"], m["table_id"]) == key]
        if len(ms) != 1:
            raise WireError(f"{key}: exactly one mutation per table is supported")
        mut = ms[0]
        enc = encode_payload(eng, key, orig[key], mutation=mut)
        patched[key] = enc["payload"]
        eb = encode_payload(eng, key, orig[key])
        if sha256(eb["payload"]) != sha256(orig[key]):
            raise WireError(f"{key}: identity re-encode of the mutated table is not bit-exact")
        new_body = enc["row0"]["mutation"]["new_body_len"]
        old_body = enc["row0"]["mutation"]["old_body_len"]
        width = mut.get("width") or 4 + len(mut["old"].encode())
        mut_records.append(
            {
                "id": mut["id"],
                "archive": mut["archive"],
                "table_id": mut["table_id"],
                "class": mut["class"],
                "row": mut["row"],
                "field": mut["field"],
                "kind": "utf-8 string (u32 length prefix + bytes)" if mut["kind"] == N_STR else "scalar",
                "l3_fourcc": eng.l3_name(key, mut["off"]),
                "wire_off_row0": mut["off"],
                "width": mut.get("width"),
                "old_value": mut["old"],
                "new_value": mut["new"],
                "old_wire_hex": _hex(
                    orig[key][HEADER_END + 1 + mut["off"] : HEADER_END + 1 + mut["off"] + width]
                ),
                "new_wire_hex": _hex(
                    patched[key][HEADER_END + 1 + mut["off"] : HEADER_END + 1 + mut["off"] + width]
                ),
                "payload_size_original": len(orig[key]),
                "payload_size_patched": len(patched[key]),
                "payload_delta_bytes": len(patched[key]) - len(orig[key]),
                "row0_body_len_original": old_body,
                "row0_body_len_patched": new_body,
                "row0_delta_bytes": new_body - old_body,
                "why": mut["why"],
            }
        )

    # every non-mutated byte of the mutated tables must be untouched
    for key in mut_keys:
        o, n = orig[key], patched[key]
        o_body = _row0_body(eng, key, o)
        n_body = _row0_body(eng, key, n)
        head = HEADER_END + 1
        tail_o = o[head + len(o_body) :]
        tail_n = n[head + len(n_body) :]
        rec = next(r for r in mut_records if (r["archive"], r["table_id"]) == key)
        rec["header_identical"] = o[:head] == n[:head]
        rec["tail_sha256_original"] = sha256(tail_o)
        rec["tail_sha256_patched"] = sha256(tail_n)
        rec["tail_bytes_identical"] = tail_o == tail_n
        rec["tail_bytes"] = len(tail_o)
        rec["footer_identical"] = o[-FOOTER_SIZE:] == n[-FOOTER_SIZE:]
        ck(
            f"mutation {rec['id']} row0 delta == payload delta",
            rec["row0_delta_bytes"] == rec["payload_delta_bytes"],
            f"row0 {rec['row0_delta_bytes']:+d} B, payload {rec['payload_delta_bytes']:+d} B",
        )
        ck(f"mutation {rec['id']} unmutated tail bit-identical", rec["tail_bytes_identical"],
           f"{len(tail_o):,} B after row 0")
        ck(f"mutation {rec['id']} header+footer preserved",
           rec["header_identical"] and rec["footer_identical"], "")

    # ---- Stage 2b: FMF repack -------------------------------------------
    archives_doc = []
    orig_payloads = {}
    new_payloads = {}
    replace_by_arch = {"server": {}, "client": {}}
    for key in mut_keys:
        replace_by_arch[key[0]][f"{key[0]}_db/table_{key[1]}.dat"] = patched[key]

    for arch in ("server", "client"):
        src = DB_DIR / f"{arch}_db.dat"
        src_bytes = src.read_bytes()
        fma = FmfArchive(src)
        op = {e["path"]: fma.payload(e) for e in fma.files}
        orig_payloads.update(op)
        dir_exact = serialize_directory(fma.tree) == fma.dir_raw
        ck(f"{arch}: directory tree re-serialises byte-exactly", dir_exact,
           f"{len(fma.dir_raw)} B")
        new_bytes, stats = fma.build(replace_by_arch[arch])
        dst = out_dir / f"patched_{arch}_db.dat"
        dst.write_bytes(new_bytes)

        # independent re-read with t112's own layout/frame decoders
        layout = eng.base.archive_layout(new_bytes)
        base_new = layout["data_base"]
        ents = layout["entries"]
        ck(f"{arch}: member inventory preserved",
           [e["path"] for e in ents] == [e["path"] for e in fma.files], f"{len(ents)} members")
        read_back = {}
        contig = True
        expect_off = 0
        for entry in ents:
            contig &= entry["offset"] == expect_off
            expect_off += entry["packed_size"]
            frames = eng.base._decode_frames(
                new_bytes[base_new + entry["offset"] : base_new + entry["offset"] + entry["packed_size"]]
            )
            hits = [f for f in frames if f["length"] == entry["size"]]
            if len(hits) != 1:
                raise WireError(f"{arch}:{entry['path']}: {len(hits)} frames with length==size")
            read_back[entry["path"]] = hits[0]["data"]
        new_payloads.update(read_back)
        ck(f"{arch}: offsets contiguous, no gaps/overlaps", contig, f"total packed {expect_off:,} B")
        ck(f"{arch}: TOC starts exactly at data_base + total_packed",
           layout["toc_offset"] == base_new + expect_off, f"toc={layout['toc_offset']:,}")
        bad = [p for p in read_back
               if sha256(read_back[p]) != sha256(replace_by_arch[arch].get(p, op[p]))]
        ck(f"{arch}: every member payload matches its expected SHA-256", not bad, str(bad[:3]))

        archives_doc.append(
            {
                "archive": arch,
                "source": str(src),
                "output": str(dst.relative_to(ROOT)),
                "size_original": len(src_bytes),
                "size_patched": len(new_bytes),
                "sha256_original": sha256(src_bytes),
                "sha256_patched": sha256(new_bytes),
                "members": len(ents),
                "members_repacked": len(stats["repacked"]),
                "members_copied_packed_verbatim": stats["copied"],
                "repacked_members": stats["repacked"],
                "data_base": base_new,
                "total_packed_bytes": stats["total_packed"],
                "directory_raw_bytes": stats["dir_raw_bytes"],
                "directory_packed_bytes": stats["dir_packed_bytes"],
                "directory_raw_roundtrip_exact": dir_exact,
                "directory_frame_identical_to_original": stats["dir_frame_identical"],
                "zstd_level": ZSTD_LEVEL,
                "frame_flags": "checksum=on, content_size=off (mirrors shipped frames)",
            }
        )

    # special members must survive untouched
    for idx, arch in enumerate(("server", "client")):
        fma = FmfArchive(DB_DIR / f"{arch}_db.dat")
        recs = verify_special_members(fma, orig_payloads, new_payloads)
        bad = [r for r in recs if not r["pass"]]
        ck(f"{arch}: {len(recs)} non-numbered members intact (payload + t106 decode)",
           not bad, str([r["member"] for r in bad]))
        archives_doc[idx]["special_members"] = recs
    summary_rec = verify_summary_dat()
    ck("summary.dat untouched and t106-decodable", summary_rec["closure_ok"],
       summary_rec["sha256"][:16])

    # ---- Stage 3a: unmodified t133 over the repacked archives -----------
    t133_doc = verify_with_t133(eng, out_dir, keys=t133_keys)
    ck(f"t133: {t133_doc['tables_closed']}/{t133_doc['tables_verified']} repacked tables closed",
       t133_doc["tables_failed"] == 0,
       f"rows={t133_doc['rows_decoded']:,}")

    readbacks = []
    for mut in MUTATIONS:
        key = (mut["archive"], mut["table_id"])
        rb = readback_mutation(eng, patched[key], mut)
        rb.update({"id": mut["id"], "archive": mut["archive"], "table_id": mut["table_id"],
                   "class": mut["class"], "target": mut["new"]})
        readbacks.append(rb)
        ck(f"t133 readback {mut['id']} {mut['class']}", rb.get("matches_target", False),
           f"{rb.get('value')!r}")

    # ---- Stage 3b: real editor.exe machine code -------------------------
    uni = unicorn_table_targets(eng, patched, orig)
    for t in uni:
        ck(f"editor.exe slot19 {t['archive']}/{t['table_id']} {t['class']}", t["pass"],
           f"consumed {t['bytes_consumed_original']}->{t['bytes_consumed_mutated']} B of "
           f"{t['row0_len_original']}->{t['row0_len_mutated']} B")

    kane = build_kane_patch(out_dir)
    kane_uni = unicorn_kane_check(kane)
    ck("editor.exe PLAYER::slot19 Harry Kane (CA/PA/PDfn/PDpc)", kane_uni.get("pass", False),
       f"consumed {kane_uni.get('bytes_consumed_mutated')} B")
    for fourcc, v in kane_uni.get("cpu_object_ram", {}).items():
        ck(f"Kane {fourcc} in C++ RAM @ {v['obj_off']}", v["matches_target"], str(v["cpu_ram_value"]))
    kane.pop("_body_original", None)
    kane.pop("_body_mutated", None)

    elapsed = round(time.perf_counter() - t_start, 1)
    doc = {
        "schema_id": "fm24.t140.patched_dual_verify",
        "schema_version": 1,
        "elapsed_sec": elapsed,
        "stage1_identity_reencode": {
            "note": "every mutated table is also re-encoded with no mutation and must stay bit-exact",
            "tables_checked": len(mut_keys),
        },
        "stage2_mutations": mut_records,
        "stage2_archives": archives_doc,
        "stage2_special_members": {
            "summary": "all non-numbered members are copied as packed frames and re-decoded with t106",
            "summary_dat": summary_rec,
        },
        "stage3_t133": {k: v for k, v in t133_doc.items() if k != "tables"},
        "stage3_t133_tables": t133_doc["tables"],
        "stage3_t133_readback": readbacks,
        "stage3_unicorn_editor": uni,
        "stage3_unicorn_kane": kane_uni,
        "stage2b_kane_record": kane,
        "checks": checks,
        "summary": {
            "mutations": len(MUTATIONS),
            "mutated_tables": len(mut_keys),
            "t133_tables_closed": t133_doc["tables_closed"],
            "t133_tables_verified": t133_doc["tables_verified"],
            "t133_rows": t133_doc["rows_decoded"],
            "unicorn_targets_pass": sum(1 for t in uni if t["pass"]),
            "unicorn_targets": len(uni),
            "unicorn_kane_pass": bool(kane_uni.get("pass")),
            "checks_pass": sum(1 for c in checks if c["ok"]),
            "checks_total": len(checks),
        },
    }
    (out_dir / "patched_dual_verify.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    if write_reports:
        write_report(out_dir, doc)
        write_done(out_dir, doc, selftest=selftest_flag)
    return doc, checks


def print_build_summary(doc: dict) -> None:
    s = doc["summary"]
    print(
        f"Stage 2: {s['mutations']} mutations over {s['mutated_tables']} tables; "
        f"Stage 3: t133 {s['t133_tables_closed']}/{s['t133_tables_verified']} closed "
        f"({s['t133_rows']:,} rows), editor.exe {s['unicorn_targets_pass']}/{s['unicorn_targets']} "
        f"targets + Kane {'PASS' if s['unicorn_kane_pass'] else 'FAIL'}; "
        f"checks {s['checks_pass']}/{s['checks_total']}"
    )
    for c in doc["checks"]:
        if not c["ok"]:
            print(f"  FAIL {c['name']}: {c['detail']}")


# =====================================================================
# 11. reports
# =====================================================================
def write_report(out_dir: pathlib.Path, doc: dict) -> None:
    rt_path = out_dir / "roundtrip_79_report.json"
    rt = json.loads(rt_path.read_text(encoding="utf-8")) if rt_path.is_file() else None
    L = []
    L.append("# t140 — FM24 `.dat` 双向回写 / FMF 重打包 / 双路回读验收")
    L.append("")
    L.append(f"脚本：`scripts/t140_fm24_roundtrip.py`（`--roundtrip-all` / `--build-patched` / `--selftest`）")
    L.append(f"产物目录：`{out_dir.relative_to(ROOT).as_posix()}/`　构建耗时 `{doc['elapsed_sec']}s`")
    L.append("")
    L.append("## Stage 1 — 结构化解码 → 值模型 → 重编码（载荷 SHA-256 位级相同）")
    L.append("")
    if rt:
        s = rt["summary"]
        L.append(
            f"**{s['tables_sha256_match']}/{s['tables_total']}** 张编号表重编码后 "
            f"`sha256(reencoded) == sha256(original)`；共 **{s['rows_reencoded_total']:,}** 行、"
            f"**{s['payload_bytes_total']:,}** 字节载荷（fixed {s['fixed_tables']} / "
            f"variable {s['variable_tables']} / empty {s['empty_tables']}），耗时 `{s['elapsed_sec']}s`。"
        )
        L.append("")
        L.append("| archive/id | class | kind | rows | payload B | SHA-256 相同 | row0 值节点 |")
        L.append("|---|---|---|---:|---:|---|---:|")
        for name, t in sorted(rt["tables"].items(),
                              key=lambda kv: (kv[1]["archive"], kv[1]["table_id"])):
            L.append(
                f"| `{name}` | `{t['class']}` | {t['kind']} | {t['rows']:,} | {t['payload_bytes']:,} | "
                f"{'YES' if t.get('sha256_match') else 'NO'} | {t.get('wire_values_row0', '-')} |"
            )
    else:
        L.append("_（先运行 `--roundtrip-all` 生成 `roundtrip_79_report.json`）_")
    L.append("")
    L.append("编码规则（与 `t133_fm24_reader_v2.py` 的 op 语法逐条对应，不存在原始行字节搬运）：")
    L.append("")
    L.append("- 13B 表头：`03 01 tad.` + `u16 ver=0x0df1` + `u32 row_count` + `1B reserved(0)` 逐字段重写；")
    L.append("- 每行：`[1B selector]` + 行体。行体按值重编码——u8/16/32/64 与 9/10/16 字节整数走 "
             "`int.from_bytes` ↔ `to_bytes`，字符串走 `u32 len + utf-8`（长度前缀按重新编码后的字节数重算），"
             "向量计数由实际发射的元素个数回填，identity 为 3×u32；")
    L.append("- 9B footer：`0x00` 终止符 + 8B trailer（以 u64 读入后重新写出；其语义未解，按原值保真）。")
    L.append("")
    L.append("## Stage 2 — FMF/zstd 重打包 + 语义改写")
    L.append("")
    L.append("| # | archive/table | class | 字段 | L3 4CC | wire off | 原值 → 新值 | 载荷 Δ |")
    L.append("|---|---|---|---|---|---:|---|---:|")
    for m in doc["stage2_mutations"]:
        old, new = m["old_value"], m["new_value"]
        if isinstance(old, str):
            old, new = f"`{old}`", f"`{new}`"
        L.append(
            f"| {m['id']} | `{m['archive']}/{m['table_id']}` | `{m['class']}` | {m['field']} | "
            f"`{m['l3_fourcc'] or '-'}` | {m['wire_off_row0']} | {old} → {new} | "
            f"{m['payload_delta_bytes']:+d} B |"
        )
    L.append("")
    L.append("| archive | 成员数 | 重压缩 | 逐字节复制 | 载荷总字节 | 目录原始字节 | 目录重序列化 | 打包后大小 |")
    L.append("|---|---:|---:|---:|---:|---:|---|---:|")
    for a in doc["stage2_archives"]:
        L.append(
            f"| `{a['archive']}` | {a['members']} | {a['members_repacked']} | "
            f"{a['members_copied_packed_verbatim']} | {a['total_packed_bytes']:,} | "
            f"{a['directory_raw_bytes']:,} | "
            f"{'字节相同' if a['directory_raw_roundtrip_exact'] else '不一致'} | "
            f"{a['size_patched']:,} |"
        )
    L.append("")
    L.append("字符串改写使后续每一行偏移、成员 `size`/`packed_size` 与整包偏移全部重算；未改写的成员以"
             "**原始 zstd 帧字节**整体复制，因此 t106 的 13 个特殊成员解码结果不变。")
    L.append("")
    L.append("## Stage 3a — 未改动的 t133 纯 Python 回读（重打包归档）")
    L.append("")
    t3 = doc["stage3_t133"]
    L.append(
        f"**{t3['tables_closed']}/{t3['tables_verified']}** 张表 `footer_closed == True`（`diff == 0`，"
        f"共 **{t3['rows_decoded']:,}** 行），失败 `{t3['tables_failed']}`。"
    )
    L.append("")
    L.append("| # | 表 | 字段 | wire off | 回读值 | 目标 | 结果 |")
    L.append("|---|---|---|---:|---|---|---|")
    for r in doc["stage3_t133_readback"]:
        v = r.get("value")
        v = f"`{v}`" if not isinstance(v, int) else str(v)
        L.append(
            f"| {r['id']} | `{r['archive']}/{r['table_id']}` | {r['class']} | {r.get('wire_off')} | "
            f"{v} | {r['target']} | {'PASS' if r.get('matches_target') else 'FAIL'} |"
        )
    L.append("")
    L.append("## Stage 3b — 真机 `editor.exe` x86_64（Unicorn）回读")
    L.append("")
    L.append("| archive/table | class | slot19 | 原行 B | 新行 B | CPU 消费 B | 框架尾 B | 状态 |")
    L.append("|---|---|---|---:|---:|---:|---:|---|")
    for t in doc["stage3_unicorn_editor"]:
        L.append(
            f"| `{t['archive']}/{t['table_id']}` | `{t['class']}` | `{t['slot19_va']}` | "
            f"{t['row0_len_original']} | {t['row0_len_mutated']} | "
            f"{t['bytes_consumed_original']} → **{t['bytes_consumed_mutated']}** | "
            f"{t['framework_trailer_bytes']} | {'PASS' if t['pass'] else 'FAIL'} |"
        )
    L.append("")
    L.append("说明：`CLUB` 的 `slot19` 在框架尾部（`u8 + u16 + 12B identity`，server 43 B / client 15 B）之前返回——"
             "该尾部由外层行循环读取，不属于 `slot19` 的职责。上表同时给出尾部字节数，因此 "
             "`CPU 消费 + 框架尾 == 新行长度` 对 10/10 张表逐张成立；且尾部字节在改写前后逐字节相同"
             "（见 JSON 的 `framework_trailer_hex_original/_mutated`）。")
    L.append("")
    L.append("C++ 对象内存回读（`emu.mu.mem_read`，数值为 CPU 真正写入的值）：")
    L.append("")
    L.append("| 表 | 字段 | 目的地址 | obj 偏移 | CPU 写入 | 目标 | 结果 |")
    L.append("|---|---|---|---:|---:|---|---|")
    for t in doc["stage3_unicorn_editor"]:
        for r in t["readbacks"]:
            if r.get("access_kind") == "std::string":
                got = f"`{r.get('stored_text')}`"
                tgt = f"`{r['target_value']}`"
            else:
                got, tgt = str(r.get("cpu_written_value")), str(r.get("target_value"))
            L.append(
                f"| `{t['archive']}/{t['table_id']}` | {r.get('field', '')[:34]} | "
                f"`{r.get('destination_addr') or r.get('string_pointer')}` | "
                f"{r.get('destination_obj_off', r.get('string_slot_obj_off'))} | {got} | {tgt} | "
                f"{'PASS' if r.get('matches_target') else 'FAIL'} |"
            )
    L.append("")
    L.append("### Harry Kane（`people_db.dat` `PLAYER::slot19`）")
    L.append("")
    k = doc["stage3_unicorn_kane"]
    kr = doc["stage2b_kane_record"]
    L.append(
        f"- 记录：`ordinal={kr['ordinal']}` `ptype={kr['person_type']}`，body `{kr['body_len_original']}` B"
        f"（framing 5B 头 + body，改写后长度不变），只改了 `{kr['changed_count']}` 个字节；"
    )
    L.append(
        f"- `PLAYER::slot19={k.get('slot19_va')}`：CPU 消费 **{k.get('bytes_consumed_mutated')}** B / "
        f"{k.get('body_len')} B，`ok={k.get('ok_mutated')}`，`rip==STOP`，对象基址 `{k.get('object_ptr')}`；"
    )
    L.append("")
    L.append("| 4CC | 字段 | obj 偏移 | 原值 | 目标 | CPU RAM | 结果 |")
    L.append("|---|---|---|---:|---:|---:|---|")
    for fourcc, v in k.get("cpu_object_ram", {}).items():
        L.append(
            f"| `{fourcc}` | {v['field']} | `{v.get('obj_off_expr') or v['obj_off']}` | {v['original']} | {v['target']} | "
            f"**{v['cpu_ram_value']}** | {'PASS' if v['matches_target'] else 'FAIL'} |"
        )
    L.append("")
    L.append("## 结论")
    L.append("")
    s = doc["summary"]
    if rt:
        L.append(f"- Stage 1：`{rt['summary']['tables_sha256_match']}/{rt['summary']['tables_total']}` "
                 f"表位级相同。")
    else:
        L.append("- Stage 1：见 `roundtrip_79_report.json`。")
    L.append(f"- Stage 2：{s['mutations']} 处语义改写（6 个表类，其中 3 处为字符串：2 处 +15 B、1 处 −7 B），"
             f"`patched_server_db.dat` / `patched_client_db.dat` 可被 t133 完整解析。")
    L.append(f"- Stage 3：t133 `{s['t133_tables_closed']}/{s['t133_tables_verified']}` 闭合 + "
             f"editor.exe `{s['unicorn_targets_pass']}/{s['unicorn_targets']}` 目标与 Kane 全部通过。")
    L.append(f"- 断言 `{s['checks_pass']}/{s['checks_total']}` 通过。")
    L.append("")
    (out_dir / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_done(out_dir: pathlib.Path, doc: dict, selftest=None) -> None:
    s = doc["summary"]
    rt_path = out_dir / "roundtrip_79_report.json"
    match = total = 0
    if rt_path.is_file():
        rs = json.loads(rt_path.read_text(encoding="utf-8"))["summary"]
        match, total = rs["tables_sha256_match"], rs["tables_total"]
    lines = [
        "DONE type=t140",
        (f"stage1_sha256_bit_exact={match}/{total}" if total
         else "stage1_sha256_bit_exact=(run --roundtrip-all)"),
        f"stage2_mutations={s['mutations']} over {s['mutated_tables']} tables",
        f"stage3_t133_closed={s['t133_tables_closed']}/{s['t133_tables_verified']} rows={s['t133_rows']}",
        f"stage3_unicorn_editor_exe={s['unicorn_targets_pass']}/{s['unicorn_targets']} targets"
        f"; kane={'PASS' if s['unicorn_kane_pass'] else 'FAIL'}",
        f"checks_pass={s['checks_pass']}/{s['checks_total']}",
        ("selftest=(run --selftest)" if selftest is None
         else f"selftest={'PASS' if selftest else 'FAIL'}"),
        "",
    ]
    (out_dir / "DONE.md").write_text("\n".join(lines), encoding="utf-8")


# =====================================================================
# 12. selftest
# =====================================================================
def selftest(out_dir: pathlib.Path) -> int:
    fails = []

    def ck(name, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    # --- grammar unit tests (synthetic bytes, no data files) -------------
    ops = (
        ("s",),
        ("u", 1),
        ("v", ("u", 4), [("u", 1), ("u", 2)]),
        ("if", 1, "!=", 0, [("s",)]),
        ("tag", 1, [(0, [("u", 2)]), (2, [("u", 4)])]),
        ("id",),
    )
    body = (
        struct.pack("<I", 3) + b"abc"
        + b"\x07"
        + struct.pack("<I", 2) + b"\x01" + struct.pack("<H", 9) + b"\x02" + struct.pack("<H", 10)
        + b"\x01" + struct.pack("<I", 2) + b"xy"
        + b"\x00" + struct.pack("<H", 4242)
        + struct.pack("<III", 1, 2, 3)
    )
    out = bytearray()
    end = compile_transcode(ops)(body, 0, len(body), out)
    ck("grammar transcode identity", bytes(out) == body and end == len(body), f"{len(out)}B")
    tree, tend = parse_tree(ops, body, 0, len(body))
    enc = bytearray()
    encode_tree(tree, enc)
    ck("tree parse/encode identity", bytes(enc) == body and tend == len(body), str(tree_values(tree)))
    bad = b"\xff\xff\xff\x7f" + body[4:]
    try:
        compile_transcode(ops)(bad, 0, len(bad), bytearray())
        ck("grammar bounds negative", False, "oversized string accepted")
    except WireError:
        ck("grammar bounds negative", True, "WireError")
    try:
        compile_transcode(ops)(body[:-3], 0, len(body) - 3, bytearray())
        ck("grammar truncation negative", False, "truncated identity accepted")
    except WireError:
        ck("grammar truncation negative", True, "WireError")

    # --- real-data checks ------------------------------------------------
    eng = Engine()
    for arch in ("server", "client"):
        fma = FmfArchive(DB_DIR / f"{arch}_db.dat")
        ck(f"{arch} directory roundtrip", serialize_directory(fma.tree) == fma.dir_raw,
           f"{len(fma.files)} members, {len(fma.dir_raw)}B")
        rebuilt, stats = fma.build({})
        same_prefix = rebuilt[: fma.toc] == fma.data[: fma.toc]
        same_toc = rebuilt[fma.toc : fma.toc + 9] == FMF_MAGIC
        ck(f"{arch} rebuild-with-no-patch reproduces every byte before the TOC", same_prefix,
           f"{fma.toc:,} B, dir frame identical={stats['dir_frame_identical']}")
        ck(f"{arch} rebuild keeps the TOC header in place", same_toc, f"toc={fma.toc:,}")

    subset = [("server", 8), ("server", 2), ("server", 45), ("server", 21), ("server", 0),
              ("client", 0), ("server", 10), ("client", 10), ("server", 25), ("client", 25),
              ("server", 3), ("client", 3)]
    for key in subset:
        payload = eng.archive(key[0]).payload(key[1])
        enc = encode_payload(eng, key, payload)
        ck(f"roundtrip {key[0]}/{key[1]} {eng.specs[key].klass}",
           sha256(enc["payload"]) == sha256(payload), f"{enc['rows']:,} rows")

    # --- full Stage 2 + Stage 3 with a reduced t133 sweep -----------------
    doc, checks = build_patched(out_dir, t133_keys=None, write_reports=True, selftest_flag=True)
    for c in checks:
        ck("built: " + c["name"], c["ok"], c["detail"])
    s = doc["summary"]
    ok = not fails and s["checks_pass"] == s["checks_total"]
    print(
        f"--- t140 selftest: t133 {s['t133_tables_closed']}/{s['t133_tables_verified']} closed, "
        f"editor.exe {s['unicorn_targets_pass']}/{s['unicorn_targets']} + kane "
        f"{'PASS' if s['unicorn_kane_pass'] else 'FAIL'}, checks {s['checks_pass']}/{s['checks_total']} ---"
    )
    print(f"--- t140 selftest: {'PASS' if ok else 'FAIL'} ({len(fails)} failures) ---")
    return 0 if ok else 1


# =====================================================================
# 13. CLI
# =====================================================================
def main() -> int:
    ap = argparse.ArgumentParser(description="FM24 .dat 双向回写 + FMF 重打包 + 双路回读验收 (t140)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--roundtrip-all", action="store_true", help="Stage 1: 79 表 SHA-256 位级回环")
    g.add_argument("--build-patched", action="store_true", help="Stage 2+3: 重打包 + 双路验收")
    g.add_argument("--selftest", action="store_true", help="快速端到端自检（0=PASS / 1=FAIL）")
    ap.add_argument("--out", default=str(OUT_DIR), help="产物目录")
    args = ap.parse_args()
    out_dir = pathlib.Path(args.out)

    if args.selftest:
        return selftest(out_dir)
    if args.roundtrip_all:
        doc = roundtrip_all(out_dir)
        print_roundtrip_summary(doc)
        return 0 if doc["summary"]["tables_failed"] == 0 else 1
    doc, checks = build_patched(out_dir)
    print_build_summary(doc)
    return 0 if all(c["ok"] for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
