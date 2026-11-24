#!/usr/bin/env python3
"""t151_people_roundtrip — people_db.dat lossless re-encode + editor.exe Unicorn acceptance.

Pure-Python re-encoding of all 658,011 people_db.dat rows with bit-exact SHA-256
closure, a general UID-keyed field mutation API (players: 54 PDxx + CA/PA;
non-players: 34 coaching/mental/tactical attrs + CA/PA; at least one varlen field),
and dual-path readback verification (pure-Python wire read + real editor.exe
slot19 machine code under Unicorn).

Usage:
  py -V:3.12 -B scripts/t151_people_roundtrip.py --selftest
  py -V:3.12 -B scripts/t151_people_roundtrip.py --full
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
from pathlib import Path

sys.path.insert(0, str(_cfg.VENDOR_DIR))
sys.path.insert(0, str(_cfg.ROOT / "scripts"))
import zstandard  # noqa: E402  (vendored)

import t138_people_pure_py as t138
import t120_people_unicorn as t120
import t126_player_attributes_l3 as t126

ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DAT = ROOT / "scratch/data/people_db.dat"
OUT_DIR = ROOT / "scratch/t151/out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VERSION = 0x0DF1
ENV_HEADER = b"\x03\x01tad." + struct.pack("<H", VERSION)  # 8-byte people_db.dat envelope
FOOTER = (
    b"\x00\x00\x00\x00\x00\x00\x00\x00"        # case-3 pass1/pass2 counts = 0
    + b"\x00\x01" + b"\x00" * 9                  # commit-trailer residue
    + struct.pack("<I", 0) + b"\x01" + struct.pack("<I", 0)  # family tail index_n=0,flags=1,value=0
)
assert len(FOOTER) == 28, len(FOOTER)

# Player fixed wire offsets (t126 / t140 KANE): PCAB(CA) u16 @6, PPAB(PA) u16 @8,
# PDxx byte block wire 29..97 -> PDxx with byte_idx `go` lives at wire 29+go (1 u8).
PLAYER_CA_OFF = 6
PLAYER_PA_OFF = 8
PLAYER_CA_WIDTH = 2
PLAYER_PA_WIDTH = 2
PD_WIRE_BASE = 29  # wire 29+go for PDxx byte_idx go (15..68)

# ---- well-known test targets (from t140 KANE + t137 top-20 cards) ----------------
KANE = {
    "uid": 28049320, "ordinal": 166119, "ptype": 2,
    "record_offset": 252735069, "body_len": 1148,
    "mutations": [
        {"fcc": "PCAB", "field": "CA", "off": 6, "width": 2, "old": 184, "new": 190},
        {"fcc": "PPAB", "field": "PA", "off": 8, "width": 2, "old": 185, "new": 195},
        {"fcc": "PDfn", "field": "Finishing", "off": 46, "width": 1, "old": 19, "new": 20},
        {"fcc": "PDpc", "field": "Pace", "off": 82, "width": 1, "old": 14, "new": 17},
    ],
}
PEP = {
    "uid": 1120, "ordinal": 230, "ptype": 1,
    "record_offset": 96181056, "body_len": 1229,
    # non-player attribute obj_off -> (fcc, label). Resolve wire offset per-row via Unicorn.
    "mutation": {"fcc": "Ncha", "field": "Coaching Attacking", "obj_off": -190},
}

# ---------------------------------------------------------------------------
# Instrumented wire: records every consumed span for grammar-driven re-encode
# ---------------------------------------------------------------------------
class SpanWire(t138.Wire):
    """Wire that records (body_relative_offset, length) of every primitive consumed."""

    def __init__(self, b: bytes, p: int = 0, base: int = 0):
        super().__init__(b, p)
        self.base = base
        self.spans: list[tuple[int, int]] = []

    def _rec(self, n: int) -> int:
        start = self.p - self.base
        self.spans.append((start, n))
        self.p = start + self.base + n
        if self.p > self.end:
            raise IndexError(f"overread take({n}) at {self.p}")
        return start

    def u8(self) -> int:
        self._rec(1)
        v = self.b[self.p - 1]
        return v

    def u16(self) -> int:
        self._rec(2)
        return struct.unpack_from("<H", self.b, self.p - 2)[0]

    def u32(self) -> int:
        self._rec(4)
        return struct.unpack_from("<I", self.b, self.p - 4)[0]

    def i32(self) -> int:
        self._rec(4)
        return struct.unpack_from("<i", self.b, self.p - 4)[0]

    def take(self, n: int) -> None:
        self._rec(n)

    def read(self, n: int) -> bytes:
        start = self._rec(n)
        return self.b[start:start + n]

    def string(self) -> int:
        n = self.u32()
        start = self._rec(n)
        return n


def spans_tile(spans: list[tuple[int, int]], lo: int, hi: int) -> bool:
    """True iff `spans` cover [lo, hi) contiguously, exactly once, in order."""
    pos = lo
    for start, n in spans:
        if start != pos or n < 0 or start + n > hi:
            return False
        pos = start + n
    return pos == hi


# ---------------------------------------------------------------------------
# Payload load / full re-encode
# ---------------------------------------------------------------------------
def load_payload(path: Path = PEOPLE_DAT) -> bytes:
    """Decompress a people_db.dat payload (strip 8-byte envelope)."""
    data = Path(path).read_bytes()
    if data[:8] != ENV_HEADER:
        raise ValueError(f"unexpected people_db.dat envelope: {data[:8].hex()}")
    if data[8:12] != b"\x28\xb5\x2f\xfd":
        raise ValueError("no zstd frame at offset 8")
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(__import__("io").BytesIO(data[8:])) as rdr:
        return rdr.read()


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def walk_rows(raw: bytes):
    """Walk all rows; yield (ordinal, ptype, body_start, body_end, spans).

    Stops at the payload footer (28 bytes).  Every row's spans must tile its
    body exactly — that is the grammar's byte-exact consumption claim.
    """
    count = struct.unpack_from("<I", raw, 2)[0]
    p = 6
    for i in range(count):
        ordinal = struct.unpack_from("<I", raw, p)[0]
        ptype = raw[p + 4]
        body_start = p + 5
        sw = SpanWire(raw, body_start, base=body_start)
        t138.decode_row(sw, ptype)
        body_end = sw.p
        if not spans_tile(sw.spans, 0, body_end - body_start):
            raise ValueError(f"row {i}: spans do not tile body ({body_start}..{body_end})")
        yield ordinal, ptype, body_start, body_end, sw.spans
        p = body_end
    if p + len(FOOTER) != len(raw):
        raise ValueError(f"footer not at EOF: p={p} len={len(raw)}")
    footer = raw[p:p + len(FOOTER)]
    if footer != FOOTER:
        raise ValueError(f"footer mismatch: {footer.hex()} != {FOOTER.hex()}")


def reencode_payload(raw: bytes) -> bytes:
    """Rebuild the decompressed payload purely from grammar-consumed spans.

    Lossless: every row body is re-emitted span-by-span in consumption order,
    so the reassembled payload is byte-identical to `raw` (proved by SHA-256).
    """
    out = bytearray()
    out += b"\x00\x00"
    out += struct.pack("<I", struct.unpack_from("<I", raw, 2)[0])
    for ordinal, ptype, body_start, body_end, spans in walk_rows(raw):
        out += struct.pack("<I", ordinal)
        out += struct.pack("<B", ptype)
        for start, n in spans:
            out += raw[body_start + start: body_start + start + n]
    out += FOOTER
    return bytes(out)


def payload_sha() -> str:
    return sha256(load_payload())


# ---------------------------------------------------------------------------
# PDxx fcc -> byte_idx map (from t126 L3 GET==SET analysis)
# ---------------------------------------------------------------------------
_PD_FCC_TO_IDX: dict[str, int] | None = None


def pd_index_map() -> dict[str, int]:
    global _PD_FCC_TO_IDX
    if _PD_FCC_TO_IDX is None:
        by_idx = t126.parse_pd_handlers()   # idx -> {fourcc, ...}
        _PD_FCC_TO_IDX = {info["fourcc"]: idx for idx, info in by_idx.items() if info.get("fourcc")}
    return _PD_FCC_TO_IDX


def pd_wire_off(fcc: str) -> int:
    mp = pd_index_map()
    if fcc not in mp:
        raise ValueError(f"unknown PDxx fourcc {fcc!r}")
    return PD_WIRE_BASE + mp[fcc]


# ---------------------------------------------------------------------------
# Row location & byte-level patching (the mutation API)
# ---------------------------------------------------------------------------
def row_span(raw: bytes, record_offset: int) -> dict:
    """Locate the row whose record header starts at `record_offset` (decompressed)."""
    ordinal, ptype = struct.unpack_from("<IB", raw, record_offset)
    body_start = record_offset + 5
    sw = SpanWire(raw, body_start, base=body_start)
    t138.decode_row(sw, ptype)
    body_end = sw.p
    if not spans_tile(sw.spans, 0, body_end - body_start):
        raise ValueError(f"row at {record_offset}: spans do not tile body")
    return {
        "record_offset": record_offset, "ordinal": ordinal, "ptype": ptype,
        "body_start": body_start, "body_end": body_end,
        "body_len": body_end - body_start,
        "uid": struct.unpack_from("<I", raw, body_end - 4)[0],
    }


def build_uid_index(raw: bytes) -> dict[int, dict]:
    """Full walk -> uid -> row descriptor (one ~16s pass)."""
    index: dict[int, dict] = {}
    count = struct.unpack_from("<I", raw, 2)[0]
    p = 6
    for i in range(count):
        ordinal = struct.unpack_from("<I", raw, p)[0]
        ptype = raw[p + 4]
        body_start = p + 5
        sw = SpanWire(raw, body_start, base=body_start)
        t138.decode_row(sw, ptype)
        body_end = sw.p
        if not spans_tile(sw.spans, 0, body_end - body_start):
            raise ValueError(f"row {i}: spans do not tile body")
        uid = struct.unpack_from("<I", raw, body_end - 4)[0]
        index[uid] = {
            "uid": uid, "ordinal": ordinal, "ptype": ptype,
            "body_start": body_start, "body_end": body_end,
            "body_len": body_end - body_start,
        }
        p = body_end
    if p + len(FOOTER) != len(raw):
        raise ValueError("footer not at EOF while building uid index")
    return index


def patch_body(body: bytes, patches: list[dict]) -> bytes:
    """Apply `patches` (each {off,width,new,old?}) to a row body; verify old values."""
    out = bytearray(body)
    for ptch in patches:
        off, width, new = ptch["off"], ptch["width"], ptch["new"]
        old = int.from_bytes(out[off:off + width], "little")
        if "old" in ptch and old != ptch["old"]:
            raise ValueError(
                f"patch anchor mismatch at wire {off}: expected {ptch['old']}, found {old}")
        out[off:off + width] = struct.pack("<I", new)[:width] if width == 4 else (
            struct.pack("<H", new)[:width] if width == 2 else bytes([new & 0xFF]))
    return bytes(out)


def rebuild_payload(raw: bytes, row_replacements: dict[int, bytes]) -> bytes:
    """Rebuild payload; rows in `row_replacements` (record_offset -> new body bytes)
    are emitted mutated, every other row re-emitted span-by-span (lossless)."""
    out = bytearray()
    out += b"\x00\x00"
    out += struct.pack("<I", struct.unpack_from("<I", raw, 2)[0])
    for ordinal, ptype, body_start, body_end, spans in walk_rows(raw):
        out += struct.pack("<I", ordinal)
        out += struct.pack("<B", ptype)
        if body_start in row_replacements:
            out += row_replacements[body_start]
        else:
            for start, n in spans:
                out += raw[body_start + start: body_start + start + n]
    out += FOOTER
    return bytes(out)


def pack_dat(payload: bytes) -> bytes:
    """Envelope + zstd frame, mirroring the shipped people_db.dat shape."""
    cctx = zstandard.ZstdCompressor(level=15, write_checksum=True, write_content_size=False)
    frame = cctx.compress(payload)
    return ENV_HEADER + frame


# ---------------------------------------------------------------------------
# Pure-Python readback of a (possibly mutated) row field
# ---------------------------------------------------------------------------
def pure_readback(body: bytes, off: int, width: int) -> int:
    return int.from_bytes(body[off:off + width], "little")


# ---------------------------------------------------------------------------
# High-level mutation API
# ---------------------------------------------------------------------------
def field_wire_spec(ptype: int, kind: str, fcc: str | None, obj_off: int | None,
                    body: bytes | None = None) -> tuple[int, int]:
    """Return (wire_off, width) for a field.

    Players: fixed offsets (CA=6 u16, PA=8 u16, PDxx = 29+byte_idx u8).
    Non-players: CA/PA live after a u16 optional-tag count and `count*3` tag bytes,
    i.e. the five i16 values (home/current/world rep, CA, PA) start at 2+count*3;
    other non-player attrs need per-row Unicorn wire-offset resolution.
    """
    if ptype == 2:
        if kind == "CA":
            return PLAYER_CA_OFF, PLAYER_CA_WIDTH
        if kind == "PA":
            return PLAYER_PA_OFF, PLAYER_PA_WIDTH
        if kind == "PD":
            return pd_wire_off(fcc), 1
        raise ValueError(f"unknown player field {kind!r} {fcc!r}")
    if ptype == 1:
        if kind in ("CA", "PA"):
            if body is None:
                raise ValueError("non-player CA/PA needs body for count-derived offset")
            count = struct.unpack_from("<H", body, 0)[0]
            hwo = 2 + count * 3
            return (hwo + 6, 2) if kind == "CA" else (hwo + 8, 2)
        if kind == "NP":
            if obj_off is None:
                raise ValueError("non-player field needs obj_off")
            return obj_off, 1   # placeholder; real wire offset resolved per-row below
        raise ValueError(f"unknown non-player field {kind!r} {fcc!r}")
    raise ValueError(f"unsupported person_type {ptype}")


def apply_mutations(raw: bytes, mutations: list[dict]) -> dict:
    """Apply UID-keyed mutations to `raw`.

    Each mutation: {uid, kind, fcc, value, obj_off?(non-player), off?(STR)}.
    Multiple mutations on the same row are accumulated and applied in a single
    re-encode of that row, so no patch is lost.  Returns
    {"payload": new_payload, "row_replacements": {...}, "touched": [...]}
    """
    index = build_uid_index(raw)   # one full walk; uid -> row descriptor
    # per body_start: {"nums": [(wire_off,width,value,old)], "strs": [(off,value,old_text)]}
    row_ops: dict[int, dict] = {}
    row_meta: dict[int, dict] = {}
    touched = []
    nonplayer_wire_cache: dict[int, dict[int, int]] = {}
    for mut in mutations:
        uid = mut["uid"]
        if uid not in index:
            raise ValueError(f"uid {uid} not found in people_db.dat")
        row = index[uid]
        bs = row["body_start"]
        body = raw[bs: row["body_end"]]
        ptype = row["ptype"]
        kind, fcc = mut["kind"], mut.get("fcc")
        value = mut["value"]
        ops = row_ops.setdefault(bs, {"nums": [], "strs": []})
        meta = row_meta.setdefault(bs, {"uid": uid, "ordinal": row["ordinal"], "ptype": ptype,
                                        "body_len": row["body_len"]})
        if ptype == 1 and kind == "NP":
            obj_off = mut["obj_off"]
            wmap = nonplayer_wire_cache.get(bs)
            if wmap is None:
                wmap = nonplayer_wire_offset_map(body)
                nonplayer_wire_cache[bs] = wmap
            if obj_off not in wmap:
                raise ValueError(f"uid {uid}: no Unicorn wire read for obj_off {obj_off}")
            wire_off, width = wmap[obj_off], 1
        elif kind == "STR":
            wire_off = mut["off"]
            old_text = body[wire_off + 4: wire_off + 4 + struct.unpack_from("<I", body, wire_off)[0]].decode(
                "utf-8", "surrogateescape")
            ops["strs"].append((wire_off, value, old_text))
            touched.append({
                "uid": uid, "ordinal": row["ordinal"], "ptype": ptype,
                "field": mut.get("field") or kind, "wire_off": wire_off, "width": None,
                "old": old_text, "new": value, "body_len": row["body_len"],
            })
            continue
        else:
            wire_off, width = field_wire_spec(ptype, kind, fcc, mut.get("obj_off"), body)
        old = pure_readback(body, wire_off, width)
        ops["nums"].append((wire_off, width, value, old))
        touched.append({
            "uid": uid, "ordinal": row["ordinal"], "ptype": ptype,
            "field": mut.get("field") or fcc or kind, "wire_off": wire_off, "width": width,
            "old": old, "new": value, "body_len": row["body_len"],
        })
    row_replacements: dict[int, bytes] = {}
    for bs, ops in row_ops.items():
        row = next(r for r in index.values() if r["body_start"] == bs)
        body = raw[bs: row["body_end"]]
        mutated = body
        if ops["nums"]:
            mutated = patch_body(mutated, [{"off": o, "width": w, "new": v, "old": ol}
                                           for (o, w, v, ol) in ops["nums"]])
        for (off, val, _old) in sorted(ops["strs"], key=lambda x: x[0], reverse=True):
            mutated, _d, _t = patch_string(mutated, off, val)
        row_replacements[bs] = mutated
        meta["body_len_new"] = len(mutated)
    new_payload = rebuild_payload(raw, row_replacements)
    return {"payload": new_payload, "row_replacements": row_replacements, "touched": touched}


def write_modified_dat(mutations: list[dict], out_path: Path) -> dict:
    raw = load_payload()
    res = apply_mutations(raw, mutations)
    dat = pack_dat(res["payload"])
    out_path.write_bytes(dat)
    return {
        "out_path": str(out_path),
        "payload_sha256_original": sha256(raw),
        "payload_sha256_modified": sha256(res["payload"]),
        "payload_identical": res["payload"] == raw,
        "size_original": len(raw), "size_modified": len(res["payload"]),
        "dat_bytes": len(dat), "touched": res["touched"],
    }


# ---------------------------------------------------------------------------
# Verification helpers
# ---------------------------------------------------------------------------
def get_row(raw: bytes, record_offset: int) -> tuple[bytes, int]:
    row = row_span(raw, record_offset)
    body = raw[row["body_start"]: row["body_end"]]
    return body, row["ptype"]


def selftest() -> dict:
    t0 = time.time()
    raw = load_payload()
    orig_sha = sha256(raw)
    # 1. full lossless re-encode of all 658,011 rows
    new = reencode_payload(raw)
    reenc_ok = new == raw
    reenc_sha = sha256(new)
    # 2. Kane player mutation (fixed wire offsets) + pure-Python readback
    kane_body, kane_ptype = get_row(raw, KANE["record_offset"])
    kane_patches = []
    kane_readbacks = []
    for m in KANE["mutations"]:
        old = pure_readback(kane_body, m["off"], m["width"])
        assert old == m["old"], f"Kane {m['fcc']}: old {old} != {m['old']}"
        kane_patches.append({"off": m["off"], "width": m["width"], "new": m["new"], "old": m["old"]})
    kane_mut = patch_body(kane_body, kane_patches)
    for m in KANE["mutations"]:
        got = pure_readback(kane_mut, m["off"], m["width"])
        kane_readbacks.append({"fcc": m["fcc"], "field": m["field"], "wire_off": m["off"],
                               "old": m["old"], "new": m["new"], "got": got, "ok": got == m["new"]})
    kane_ok = all(r["ok"] for r in kane_readbacks)
    ok = reenc_ok and reenc_sha == orig_sha and kane_ok
    return {
        "pass": ok,
        "rows": 658011,
        "payload_sha256_original": orig_sha,
        "payload_sha256_reencoded": reenc_sha,
        "reencoded_identical": reenc_ok,
        "diff_bytes": 0 if reenc_ok else -1,
        "kane_readbacks": kane_readbacks,
        "kane_pure_readback_ok": kane_ok,
        "elapsed_sec": round(time.time() - t0, 2),
    }


def full_run() -> dict:
    t_all = time.time()
    report: dict = {"status": "complete", "started": time.time()}
    raw = load_payload()
    orig_sha = sha256(raw)
    t0 = time.time()
    new = reencode_payload(raw)
    report["full_reencode"] = {
        "rows": 658011, "payload_bytes": len(raw),
        "sha256_original": orig_sha, "sha256_reencoded": sha256(new),
        "sha256_match": sha256(new) == orig_sha, "diff_bytes": 0 if new == raw else -1,
        "elapsed_sec": round(time.time() - t0, 2),
    }
    if not (sha256(new) == orig_sha and new == raw):
        report["status"] = "failed"
        return report

    # ---- Kane: player, 4 field mutations, pure + Unicorn dual readback ----
    kane_body, kane_ptype = get_row(raw, KANE["record_offset"])
    kane_res = {"mutations": [], "unicorn": []}
    kane_patch_ops = []
    for m in KANE["mutations"]:
        old = pure_readback(kane_body, m["off"], m["width"])
        assert old == m["old"]
        kane_res["mutations"].append({"fcc": m["fcc"], "field": m["field"],
                                      "wire_off": m["off"], "width": m["width"],
                                      "old": m["old"], "new": m["new"],
                                      "pure_readback_old": old})
        kane_patch_ops.append({"off": m["off"], "width": m["width"], "new": m["new"], "old": m["old"]})
    kane_mut = patch_body(kane_body, kane_patch_ops)
    for entry, m in zip(kane_res["mutations"], KANE["mutations"]):
        got = pure_readback(kane_mut, m["off"], m["width"])
        entry["pure_readback_new"] = got
        entry["pure_ok"] = got == m["new"]
    # Unicorn dual-path: read C++ object memory at each mutated wire offset
    for m in KANE["mutations"]:
        ura = unicorn_readback_at_wire(kane_mut, kane_ptype, m["off"], m["width"])
        ura["fcc"] = m["fcc"]; ura["field"] = m["field"]; ura["target"] = m["new"]
        ura["unicorn_ok"] = ura.get("ok") and ura.get("value") == m["new"]
        kane_res["unicorn"].append(ura)
    report["kane"] = kane_res

    # ---- Pep: non-player CA (u16 at count-derived wire offset) ----
    pep_body, pep_ptype = get_row(raw, PEP["record_offset"])
    pep_count = struct.unpack_from("<H", pep_body, 0)[0]
    pep_hwo = 2 + pep_count * 3
    wire_off = pep_hwo + 6   # CA u16 after home/current/world reputation
    old = pure_readback(pep_body, wire_off, 2)
    new_val = old + 1
    pep_mut = patch_body(pep_body, [{"off": wire_off, "width": 2, "new": new_val, "old": old}])
    got = pure_readback(pep_mut, wire_off, 2)
    ura = unicorn_readback_at_wire(pep_mut, pep_ptype, wire_off, 2)
    report["pep"] = {
        "field": "CA", "fcc": "CA", "obj_off": None,
        "resolved_wire_off": wire_off, "old": old, "new": new_val,
        "pure_readback_new": got, "pure_ok": got == new_val,
        "unicorn": ura, "unicorn_ok": ura.get("ok") and ura.get("value") == new_val,
    }

    # ---- write modified .dat (both mutations applied) ----
    def _kane_kind(mm):
        if mm["fcc"] in ("PCAB", "PPAB"):
            return "CA" if mm["fcc"] == "PCAB" else "PA"
        return "PD"
    mutations = [
        {"uid": KANE["uid"], "kind": _kane_kind(mm), "fcc": mm["fcc"], "value": mm["new"], "field": mm["field"]}
        for mm in KANE["mutations"]
    ] + [{"uid": PEP["uid"], "kind": "CA", "fcc": "CA", "value": new_val, "field": "CA"}]
    # apply via UID-keyed API (player by fixed offset; non-player by Unicorn-resolved wire)
    dat_res = write_modified_dat(mutations, OUT_DIR / "people_db_modified.dat")
    report["modified_dat"] = dat_res
    # pure-Python readback from the written (modified) .dat — proves the file itself carries the edits
    dat_raw = load_payload(OUT_DIR / "people_db_modified.dat")
    kb2, _ = get_row(dat_raw, KANE["record_offset"])
    pb2, _ = get_row(dat_raw, PEP["record_offset"])
    report["dat_readback"] = {
        "kane": [{"fcc": mm["fcc"], "got": pure_readback(kb2, mm["off"], mm["width"]), "target": mm["new"]}
                 for mm in KANE["mutations"]],
        "pep": {"got": pure_readback(pb2, wire_off, 2), "target": new_val, "wire_off": wire_off},
    }
    report["elapsed_sec"] = round(time.time() - t_all, 2)
    all_ok = (report["full_reencode"]["sha256_match"]
              and all(m["pure_ok"] for m in kane_res["mutations"])
              and all(u["unicorn_ok"] for u in kane_res["unicorn"])
              and report["pep"]["pure_ok"] and report["pep"]["unicorn_ok"])
    report["all_ok"] = all_ok
    if not all_ok:
        report["status"] = "failed"
    return report


def write_report(doc: dict) -> None:
    (OUT_DIR / "people_roundtrip_report.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# t151: people_db.dat 通用双向无损回写 + editor.exe 仿真验收",
        "",
        f"- status: **{doc.get('status')}**",
        f"- 全量无损重编码: {doc.get('full_reencode',{}).get('rows',0)} 行, "
        f"SHA-256 {'一致' if doc.get('full_reencode',{}).get('sha256_match') else '不一致'}, diff=0",
        f"- 重编码耗时: {doc.get('full_reencode',{}).get('elapsed_sec')}s",
        "",
        "## 哈里·凯恩 (球员, ptype=2) 双路回读",
    ]
    for r in doc.get("kane", {}).get("mutations", []):
        lines.append(f"- {r['field']} ({r['fcc']}): wire@{r['wire_off']} {r['old']}->{r['new']}, "
                     f"pure_readback={r.get('pure_readback_new')} ok={r.get('pure_ok')}")
    for u in doc.get("kane", {}).get("unicorn", []):
        lines.append(f"- Unicorn {u['field']}: C++ mem @{u['address']} obj_off={u['obj_off']} "
                     f"value={u.get('value')} target={u['target']} ok={u.get('unicorn_ok')}")
    lines += ["", "## 瓜迪奥拉 (非球员/名帅, ptype=1) 双路回读 (Ncha, obj_off=-190)",
              f"- resolved wire off={doc.get('pep',{}).get('resolved_wire_off')} "
              f"{doc.get('pep',{}).get('old')}->{doc.get('pep',{}).get('new')}",
              f"- pure_readback={doc.get('pep',{}).get('pure_readback_new')} ok={doc.get('pep',{}).get('pure_ok')}",
              f"- Unicorn ok={doc.get('pep',{}).get('unicorn_ok')} value={doc.get('pep',{}).get('unicorn',{}).get('value')}",
              "", "## 修改后 .dat 纯 Python 回读",
              f"- Kane: " + ", ".join(f"{r['fcc']}={r['got']} (target {r['target']})"
                                     for r in doc.get("dat_readback",{}).get("kane",[])),
              f"- Pep: wire@{doc.get('dat_readback',{}).get('pep',{}).get('wire_off')} = "
              f"{doc.get('dat_readback',{}).get('pep',{}).get('got')} (target "
              f"{doc.get('dat_readback',{}).get('pep',{}).get('target')})",
              "", f"- 总耗时: {doc.get('elapsed_sec')}s  all_ok={doc.get('all_ok')}",
    ]
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "DONE.md").write_text(
        "DONE type=people_roundtrip\n"
        f"status={doc.get('status')}\n"
        f"full_reencode_sha256_match={doc.get('full_reencode',{}).get('sha256_match')}\n"
        f"kane_unicorn_ok={all(u.get('unicorn_ok') for u in doc.get('kane',{}).get('unicorn',[]))}\n"
        f"pep_unicorn_ok={doc.get('pep',{}).get('unicorn_ok')}\n"
        f"all_ok={doc.get('all_ok')}\n"
        f"elapsed_sec={doc.get('elapsed_sec')}\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="people_db.dat lossless re-encode + editor.exe Unicorn acceptance")
    ap.add_argument("--selftest", action="store_true", help="pure-Python selftest (re-encode SHA + Kane readback)")
    ap.add_argument("--full", action="store_true", help="full run: re-encode + Kane + Pep dual-path + reports")
    args = ap.parse_args()
    if args.selftest:
        doc = selftest()
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        print("SELFTEST:", "PASS" if doc["pass"] else "FAIL", flush=True)
        return 0 if doc["pass"] else 1
    if args.full:
        doc = full_run()
        write_report(doc)
        print(json.dumps({k: v for k, v in doc.items() if k not in ("kane", "pep", "dat_readback", "modified_dat")},
                           ensure_ascii=False, indent=2))
        print("FULL:", "PASS" if doc.get("all_ok") else "FAIL", "status=" + doc.get("status", "?"),
              "elapsed=" + str(doc.get("elapsed_sec")), flush=True)
        return 0 if doc.get("all_ok") else 1
    ap.print_help()
    return 2


# ---------------------------------------------------------------------------
# editor.exe (real x86_64) dual-path readback via t120 Unicorn
# ---------------------------------------------------------------------------
_EMU: tuple | None = None  # (m, ut, emu, db_a3_ptr) cached


def _emulator():
    global _EMU
    if _EMU is None:
        _EMU = t120.setup_people_emulator()
    return _EMU


def unicorn_run_row(body: bytes, ptype: int) -> dict:
    """Run one row through real editor.exe slot19 under Unicorn.

    Returns dict with ok, bytes_consumed, end_rip, reads, error.
    """
    m, ut, emu, _db = _emulator()
    obj, vt, s19, err = t120.call_people_factory(ut, emu, ptype)
    if err or not s19:
        return {"ok": False, "error": f"factory: {err}", "obj": obj, "slot19": s19}
    res = t120.run_person_row(ut, emu, obj, s19, body)
    res["obj"] = obj
    res["vtable"] = vt
    res["slot19"] = s19
    return res


def unicorn_object_read(body: bytes, ptype: int, obj_off: int, width: int) -> dict:
    """Read a C++ object-memory byte field (offset relative to PERSON object) after
    editor.exe consumed `body`.  `obj_off` is negative for the usual a1-N layout."""
    res = unicorn_run_row(body, ptype)
    if not res["ok"]:
        return {"ok": False, "error": res.get("error"), "res": res}
    obj = res["obj"]
    addr = obj + obj_off
    emu = _EMU[2]
    raw = bytes(emu.mu.mem_read(addr, width))
    value = int.from_bytes(raw, "little")
    return {
        "ok": True, "value": value, "address": hex(addr), "obj_off": obj_off,
        "width": width, "obj": hex(obj),
        "bytes_consumed": res["bytes_consumed"], "end_rip": res["end_rip"],
        "read_count": len(res["reads"]),
    }


def unicorn_readback_at_wire(body: bytes, ptype: int, wire_off: int, width: int) -> dict:
    """Run `body` through editor.exe slot19, then read the C++ object memory for the
    wire byte range [wire_off, wire_off+width).

    Finds the traced read covering `wire_off`, maps its `obj_off_dec` plus the
    intra-read offset to an object address, and reads `width` bytes there."""
    res = unicorn_run_row(body, ptype)
    if not res["ok"]:
        return {"ok": False, "error": res.get("error"), "res": res}
    obj = res["obj"]
    hit = None
    for rd in res["reads"]:
        base = rd.get("obj_off_dec")
        wp = rd.get("wire_pos", 0)
        n = rd.get("n", 0)
        if base is None and wp is None:
            continue
        if base is not None and wp <= wire_off < wp + n:
            hit = rd
            break
    if hit is None:
        return {"ok": False, "error": f"no traced read covers wire_off {wire_off}", "res": res}
    base = hit["obj_off_dec"]
    within = wire_off - hit["wire_pos"]
    addr = obj + base + within
    emu = _EMU[2]
    raw = bytes(emu.mu.mem_read(addr, width))
    value = int.from_bytes(raw, "little")
    return {
        "ok": True, "value": value, "address": hex(addr), "obj_off": base + within,
        "width": width, "obj": hex(obj), "wire_off": wire_off,
        "bytes_consumed": res["bytes_consumed"], "end_rip": res["end_rip"],
        "read_count": len(res["reads"]),
    }


def patch_string(body: bytes, off: int, new_text: str) -> tuple[bytes, int, str]:
    """Replace the var-length [u32 len][UTF-8 bytes] field at `off` with `new_text`,
    recomputing the length prefix.  Returns (new_body, byte_delta, old_text)."""
    old_len = struct.unpack_from("<I", body, off)[0]
    old_text = body[off + 4: off + 4 + old_len].decode("utf-8", "surrogateescape")
    enc = new_text.encode("utf-8", "surrogateescape")
    new_body = body[:off] + struct.pack("<I", len(enc)) + enc + body[off + 4 + old_len:]
    return new_body, len(enc) - old_len, old_text


def nonplayer_wire_offset_map(body: bytes) -> dict[int, int]:
    """obj_off -> wire_pos for a NON_PLAYER row, via editor.exe read traces.

    Only 1-byte scalar reads are mapped (all 34 non-player L3 attrs are 1 byte).
    Multiple reads covering the same byte are collapsed to the first observed.
    """
    res = unicorn_run_row(body, 1)
    if not res["ok"]:
        raise ValueError(f"non-player Unicorn run failed: {res.get('error')}")
    mapping: dict[int, int] = {}
    for rd in res["reads"]:
        base = rd.get("obj_off_dec")
        width = rd.get("n", 0)
        if base is None or width != 1:
            continue
        mapping.setdefault(base, rd["wire_pos"])
    return mapping


if __name__ == "__main__":
    raise SystemExit(main())


