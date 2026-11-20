#!/usr/bin/env python3
"""t33 independent verifier: recompute row closure + sample column statistics.

Deliberately does NOT import scripts/t33_profile_batch.py. It re-reads the
read-only archive, re-derives row boundaries with its own code, and compares
against the delivered profiles. It also re-computes a random-but-fixed sample
of column statistics from the delivered rows.jsonl files.

Usage
  py -V:3.12 -I -B scratch/t33/out/verify.py --help
  py -V:3.12 -I -B scratch/t33/out/verify.py [--sample 40]
Exit 0 all checks pass / 1 a check failed / 2 usage or fatal
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import pathlib
import struct
import sys

def _find_root(start: pathlib.Path) -> pathlib.Path:
    for cand in [start, *start.parents]:
        if (cand / "AGENTS.md").is_file() and (cand / "scratch").is_dir():
            return cand
    raise VerifyError("workspace root (AGENTS.md + scratch/) not found")


ROOT = _find_root(pathlib.Path(__file__).resolve().parent)
OUTDIR = ROOT / "scratch/t33/out"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR", ROOT / "scratch/data")).resolve()
DAT_HEADERS = ROOT / "evidence/fm24/reports/dbdat_decode/dat_headers.json"
SERVER_CENSUS = ROOT / "evidence/fm24/reports/dbdat_decode/server_tables_census.json"
ZSTD_MAGIC = bytes.fromhex("28b52ffd")
TAD_MAGIC = bytes.fromhex("03017461642ef10d")
TABLES = (12, 39, 45, 48, 58, 59, 73)


class VerifyError(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zstd(frame: bytes, size: int) -> bytes:
    lib = ctypes.CDLL(os.environ.get("FM24_ZSTD_DLL",
                                     r"C:\Program Files\Git\mingw64\bin\libzstd.dll"))
    lib.ZSTD_decompress.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                    ctypes.c_void_p, ctypes.c_size_t]
    lib.ZSTD_decompress.restype = ctypes.c_size_t
    lib.ZSTD_isError.argtypes = [ctypes.c_size_t]
    lib.ZSTD_isError.restype = ctypes.c_uint
    src = ctypes.create_string_buffer(frame)
    cap = size
    while True:
        dst = ctypes.create_string_buffer(cap)
        got = lib.ZSTD_decompress(dst, cap, src, len(frame))
        if not lib.ZSTD_isError(got):
            return dst.raw[:got]
        cap *= 2
        if cap > 512 * 1024 * 1024:
            raise VerifyError("zstd output exceeds cap")


def fmf_directory(blob: bytes) -> tuple[int, dict[str, dict[str, int]]]:
    toc_off = struct.unpack_from("<I", blob, 17)[0] + 17
    raw = zstd(blob[toc_off + 9:], 16 * 1024 * 1024)
    pos = 0
    root_len = struct.unpack_from("<I", raw, pos)[0]
    pos += 4
    root = raw[pos:pos + root_len].decode()
    pos += root_len
    count = struct.unpack_from("<I", raw, pos)[0]
    pos += 4
    out: dict[str, dict[str, int]] = {}
    for _ in range(count):
        nl = struct.unpack_from("<I", raw, pos)[0]
        pos += 4
        name = raw[pos:pos + nl].decode()
        pos += nl
        el = struct.unpack_from("<I", raw, pos)[0]
        pos += 4
        ext = raw[pos:pos + el].decode()
        pos += el
        off, packed, size = struct.unpack_from("<QQQ", raw, pos)
        pos += 40
        out[f"{root}/{name}{ext}"] = {"offset": off, "packed_size": packed, "size": size}
    return 34, out


def load_payloads(tids) -> dict[int, bytes]:
    allowed = (ROOT / "scratch/data").resolve()
    if DBDIR != allowed:
        raise VerifyError(f"FM24_DB_DIR must be exactly {allowed}")
    header = next(h for h in json.loads(DAT_HEADERS.read_text(encoding="utf-8"))
                  if h.get("file") == "server_db.dat")
    archive = (DBDIR / "server_db.dat").read_bytes()
    if sha256(archive) != header["sha256"] or len(archive) != header["size"]:
        raise VerifyError("server_db.dat differs from frozen dat_headers.json")
    base, directory = fmf_directory(archive)
    census = {e["path"]: e for e in
              json.loads(SERVER_CENSUS.read_text(encoding="utf-8"))["entries"]}
    out = {}
    for tid in tids:
        path = f"server_db/table_{tid}.dat"
        toc, cen = directory[path], census[path]
        start = base + toc["offset"]
        member = archive[start:start + toc["packed_size"]]
        got = None
        search = 0
        while True:
            rel = member.find(ZSTD_MAGIC, search)
            if rel < 0:
                break
            search = rel + 4
            cand = zstd(member[rel:], cen["payload_size"])
            if len(cand) == cen["payload_size"] and sha256(cand) == cen["payload_sha256"]:
                got = cand
                break
        if got is None:
            raise VerifyError(f"table {tid}: cannot reproduce frozen payload")
        out[tid] = got
    return out


def walk_fixed(raw: bytes) -> list[bytes]:
    """Own implementation: derive stride from arithmetic, then prove it by framing."""
    count = struct.unpack_from("<I", raw, 8)[0]
    for header, footer in ((14, 8), (13, 9)):
        body = len(raw) - header - footer
        if body <= 0 or body % count:
            continue
        stride = body // count
        rows = [raw[header + i * stride:header + (i + 1) * stride] for i in range(count)]
        ok = all(struct.unpack_from("<I", r, len(r) - 13)[0] == i
                 and r[-13 + 4:-13 + 8] == r[-13 + 8:-13 + 12]
                 and r[-1] in (0x00, 0x0C) for i, r in enumerate(rows))
        if ok:
            return rows
    raise VerifyError("fixed framing cannot be proven")


def walk_variable(raw: bytes) -> list[bytes]:
    count = struct.unpack_from("<I", raw, 8)[0]
    body = raw[14:len(raw) - 8]
    pos, rows = 0, []
    for i in range(count):
        hit = None
        for length in range(13, min(2048, len(body) - pos) + 1):
            t = pos + length - 13
            if t + 13 > len(body):
                break
            o, a, b = struct.unpack_from("<III", body, t)
            if o == i and a == b and body[t + 12] in (0x00, 0x0C):
                hit = length
                break
        if hit is None:
            raise VerifyError(f"variable framing stuck at row {i}")
        rows.append(body[pos:pos + hit])
        pos += hit
    if pos != len(body):
        raise VerifyError(f"variable framing ends at {pos} != {len(body)}")
    return rows


def col_stats(rows: list[bytes], off: int, width: int, from_end: bool) -> tuple:
    """off is signed for the row_end frame in the delivered profile."""
    vals = []
    for r in rows:
        p = len(r) - abs(off) if from_end else off
        if p < 0 or p + width > len(r):
            continue
        vals.append(int.from_bytes(r[p:p + width], "little"))
    if not vals:
        return (0, None, None, 0)
    return (len(vals), min(vals), max(vals), sum(1 for v in vals if v == 0))


def main() -> int:
    ap = argparse.ArgumentParser(description="Independently verify t33 profiles.")
    ap.add_argument("--sample", type=int, default=40,
                    help="number of column samples to recheck per table")
    args = ap.parse_args()
    results: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append({"check": name, "ok": bool(ok), "detail": detail})

    try:
        payloads = load_payloads(TABLES)
    except (VerifyError, OSError, KeyError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2

    for tid in TABLES:
        prof = json.loads((OUTDIR / "profiles" /
                           f"table_server_{tid}.profile.json").read_text(encoding="utf-8"))
        rows_path = OUTDIR / prof["full_rows_file"]
        raw = payloads[tid]
        c = prof["row_closure"]
        digest = sha256(raw)
        check(f"t{tid}_payload_sha",
              digest == prof["payload"]["payload_sha256"]
              and len(raw) == prof["payload"]["payload_size"], digest[:16])
        try:
            rows = walk_fixed(raw) if c["model"] == "fixed" else walk_variable(raw)
        except VerifyError as exc:
            check(f"t{tid}_reframe", False, str(exc))
            continue
        check(f"t{tid}_count", len(rows) == c["count"], f"{len(rows)} vs {c['count']}")
        if c["model"] == "fixed":
            check(f"t{tid}_stride", all(len(r) == c["stride"] for r in rows),
                  f"stride {c['stride']}")
        check(f"t{tid}_closure", c["row_start"] + sum(len(r) for r in rows) +
              c["footer_bytes"] == len(raw),
              f"{c['row_start']}+{sum(len(r) for r in rows)}+{c['footer_bytes']}"
              f"={len(raw)}")
        check(f"t{tid}_rows_sha", sha256(b"".join(rows)) == c["rows_sha256"],
              sha256(b"".join(rows))[:16])

        # delivered rows.jsonl must equal the independent re-walk
        delivered = [json.loads(line) for line in
                     rows_path.read_text(encoding="ascii").splitlines()]
        same = (len(delivered) == len(rows)
                and all(bytes.fromhex(d["raw_hex"]) == r
                        for d, r in zip(delivered, rows)))
        check(f"t{tid}_rows_jsonl_matches", same, f"{len(delivered)} rows")
        check(f"t{tid}_rows_jsonl_sha",
              sha256(rows_path.read_bytes()) == prof["full_rows_sha256"],
              prof["full_rows_sha256"][:16])

        # sample column statistics straight from the delivered bytes
        cols = prof["columns"]["row_start"] + prof["columns"].get("row_end", [])
        step = max(1, len(cols) // max(1, args.sample))
        bad = 0
        for col in cols[::step][:args.sample]:
            n, mn, mx, zero = col_stats(rows, col["offset"], col["width"],
                                        col["offset_frame"] == "row_end")
            if (n != col["count"] or mn != col["min_unsigned"]
                    or mx != col["max_unsigned"] or zero != col["zero_count"]):
                bad += 1
        check(f"t{tid}_column_sample", bad == 0,
              f"{len(cols[::step][:args.sample])} columns, {bad} mismatches")

    failed = [r for r in results if not r["ok"]]
    for r in results:
        print(("PASS " if r["ok"] else "FAIL ") + r["check"] + "  " + r["detail"])
    print(f"--- {len(results) - len(failed)} PASS / {len(failed)} FAIL ---")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
