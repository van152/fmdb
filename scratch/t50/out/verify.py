#!/usr/bin/env python3
"""t50 independent verifier for the data-side table_9 profile.

Deliberately self-contained: it does not import the t50 builder, t49, or any
other task module. Archive decoding, framing, closure and identity checks are
re-derived here from the payload bytes and compared against the delivered JSON.

Run with Python 3.12:
  py -V:3.12 -I -B scratch/t50/out/verify.py --help
  py -V:3.12 -I -B scratch/t50/out/verify.py --selftest
  FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scratch/t50/out/verify.py
Exit codes: 0 all checks passed / 1 check failed / 2 usage or fatal error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import runpy
import struct
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
PROFILE = OUT / "profile_t9.json"
DIFF = OUT / "grammar_diff_t9.json"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data")).resolve()
CODEC = pathlib.Path(r"<OLD_REPO>\scripts\modding_read_dbdat.py")
TAD_MAGIC = bytes.fromhex("03017461642ef10d")
IDENT = 13
SIDES = ("client", "server")


class VerifyError(RuntimeError):
    pass


def require(cond: Any, msg: Any) -> None:
    if not cond:
        raise VerifyError(msg)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def u32(b: bytes, p: int) -> int:
    return struct.unpack_from("<I", b, p)[0]


def read_json(path: pathlib.Path) -> dict[str, Any]:
    require(path.is_file(), f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"missing {path}")
    return [json.loads(line) for line in path.read_text(encoding="ascii").splitlines() if line]


def zstd_module():
    sys.path.append(r"<OLD_REPO>\tools\python")
    import zstandard  # noqa: PLC0415
    return zstandard


def payload_for(zstd, k, blob: bytes, lay: dict[str, Any], name: str) -> tuple[bytes, dict[str, Any]]:
    """Independent E80 member decode: member start = data_base + entry.offset."""
    entries = {pathlib.PurePosixPath(e["path"]).name: e for e in lay["entries"]}
    entry = entries.get(name)
    require(entry is not None, f"{name}: directory entry")
    lo = int(lay["data_base"]) + int(entry["offset"])
    part = blob[lo:lo + int(entry["packed_size"])]
    require(part[:4] == b"\x28\xb5\x2f\xfd", f"{name}: zstd magic")
    pos = 0
    found = []
    while pos < len(part):
        dec = zstd.ZstdDecompressor().decompressobj()
        payload = dec.decompress(part[pos:])
        used = len(part) - pos - len(dec.unused_data)
        require(dec.eof and used > 0, f"{name}: frame EOF")
        if len(payload) == int(entry["size"]):
            found.append((payload, pos, used))
        pos += used
    require(len(found) == 1, f"{name}: one frame matches entry.size")
    payload, foff, fused = found[0]
    return payload, {
        "entry_offset": int(entry["offset"]),
        "packed_size": int(entry["packed_size"]),
        "declared_size": int(entry["size"]),
        "member_start": lo,
        "frame_offset": lo + foff,
        "frame_compressed": fused,
        "packed_sha256": sha(part),
        "payload_sha256": sha(payload),
        "payload_size": len(payload),
        "count": u32(payload, 8),
        "head": payload[:24].hex(),
    }


def identity_positions(body: bytes, ordinal: int, floor: int) -> list[tuple[int, int]]:
    out = []
    needle = struct.pack("<I", ordinal)
    p = body.find(needle, floor)
    while p >= 0:
        if p + IDENT <= len(body):
            a, b = struct.unpack_from("<II", body, p + 4)
            if a == b and body[p + 12] == 0:
                out.append((p, a))
        p = body.find(needle, p + 1)
    return out


def closure_walks(body: bytes, header: int, footer: int, allow_zero: bool = False) -> int:
    """Count complete tilings under the increasing-row_id + non-zero-id rule."""
    count = u32(body, 8)
    stop = len(body) - footer
    table = {i: identity_positions(body, i, header) for i in range(count)}
    states = {(header, -1): 1}
    for i in range(count):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, last), ways in states.items():
            for at, rid in table[i]:
                if at < pos or at + IDENT > stop:
                    continue
                if rid == 0 and not allow_zero:
                    continue
                if not rid > last:
                    continue
                key = (at + IDENT, rid)
                nxt[key] = nxt.get(key, 0) + ways
        states = nxt
        if not states:
            return 0
    return sum(w for (pos, _l), w in states.items() if pos == stop)


def x9_blocks(body: bytes, header: int, name_max: int = 120) -> list[int] | None:
    count = u32(body, 8)
    table: dict[int, list[int]] = {}
    for i in range(count):
        hits = []
        needle = struct.pack("<I", i)
        p = body.find(needle, header)
        while p >= 0:
            if p + 8 <= len(body):
                n = u32(body, p + 4)
                if 0 <= n <= name_max and p + 8 + n <= len(body):
                    if all(x >= 0x20 for x in body[p + 8:p + 8 + n]):
                        hits.append(p)
            p = body.find(needle, p + 1)
        table[i] = hits
    states = {header}
    for i in range(count):
        nxt = set()
        for pos in states:
            for at in table[i]:
                if at >= pos:
                    nxt.add(at)
        states = nxt
        if not states:
            return None
    return sorted(states)


def load_all() -> dict[tuple[str, str], bytes]:
    zstd = zstd_module()
    k = runpy.run_path(str(CODEC))
    out: dict[tuple[str, str], bytes] = {}
    for side in SIDES:
        blob = (DBDIR / f"{side}_db.dat").read_bytes()
        lay = k["_archive_layout"](blob)
        for name in ("table_9.dat", "table_extra_9.dat", "table_10.dat"):
            payload, _meta = payload_for(zstd, k, blob, lay, name)
            out[side, name] = payload
    return out


def verify(verbose: bool) -> int:
    profile = read_json(PROFILE)
    diff = read_json(DIFF)
    payloads = load_all()
    checks = 0

    # --- 1. anchors and shell ------------------------------------------------
    for side in SIDES:
        archive = profile["archives"][side]
        require(archive["data_base"] == 34, f"{side}: data_base 34")
        require(archive["directory_entries"] == (31 if side == "client" else 77), f"{side}: directory count")
        for name, member in archive["members"].items():
            require(member["present"], f"{side}/{name}: present")
            payload = payloads[side, name.replace("table_", "table_")]
            require(payload.startswith(TAD_MAGIC), f"{side}/{name}: tad shell")
            require(len(payload) == member["declared_size"], f"{side}/{name}: declared size == payload size")
            require(sha(payload) == member["payload_sha256"], f"{side}/{name}: payload SHA matches delivered")
            require(u32(payload, 8) == 251 == member["record_count_header"], f"{side}/{name}: count 251")
            require(member["packed_sha256"] == archive_side_packed(profile, side, name),
                    f"{side}/{name}: packed sha recorded")
            require(len(member["packed_sha256"]) == 64, f"{side}/{name}: packed sha hex length")
            require(member["frame_count"] == 1 and member["frame_lengths"] == [member["declared_size"]],
                    f"{side}/{name}: single frame")
            checks += 1
    presence = profile["archives"]["member_presence"]
    require(presence["client"]["table_extra_10.dat"] is False
            and presence["server"]["table_extra_10.dat"] is False, "table_extra_10 absent both sides")
    checks += 1

    # --- 2. t9 row closure re-derived ---------------------------------------
    for side in SIDES:
        body = payloads[side, "table_9.dat"]
        block = profile["members"][f"{side}/table_9.dat"]["closure"]
        rows = read_rows(OUT / "profiles" / f"table_{side}_9.rows.jsonl")
        require(len(rows) == 251 == block["count"], f"{side} t9: 251 rows delivered")
        total = sum(r["len"] for r in rows)
        require(total == block["sum_row_lens"], f"{side} t9: delivered len sum")
        require(13 + total + 8 == len(body), f"{side} t9: 13 + sum + 8 == payload")
        require(block["closure_exact"] is True, f"{side} t9: closed flag")
        # rows must tile the payload body with no gaps or overlaps
        pos = 13
        for r in rows:
            require(r["offset"] == pos, f"{side} t9 row {r['row']}: contiguous at {pos}")
            raw = bytes.fromhex(r["raw_hex"])
            require(raw == body[pos:pos + r["len"]], f"{side} t9 row {r['row']}: raw_hex matches payload")
            require(len(raw) == r["len"], f"{side} t9 row {r['row']}: len matches raw_hex")
            pos += r["len"]
        require(pos == len(body) - 8, f"{side} t9: tiling ends exactly at payload-8")
        require(closure_walks(body, 13, 8) == 1, f"{side} t9: exactly one closure under delivered rule")
        checks += 1

    # --- 3. identity census -------------------------------------------------
    id_lists = {}
    for side in SIDES:
        rows = read_rows(OUT / "profiles" / f"table_{side}_9.rows.jsonl")
        census = profile["members"][f"{side}/table_9.dat"]["closure"]["identity_census"]
        ordinals = [r["identity"]["ordinal"] for r in rows]
        ids = [r["identity"]["row_id"] for r in rows]
        require(ordinals == list(range(251)), f"{side}: ordinal sequence 0..250")
        require(all(r["identity"]["row_id"] == r["identity"]["repeated_id"] for r in rows), f"{side}: repeated lanes")
        require(all(r["identity"]["marker"] == 0 for r in rows), f"{side}: marker 00")
        require(len(set(ids)) == 251, f"{side}: row_id unique")
        require(all(a < b for a, b in zip(ids, ids[1:])), f"{side}: row_id increasing")
        require(0 not in ids, f"{side}: no zero row_id chosen")
        body = payloads[side, "table_9.dat"]
        require(ids[-1] == u32(body, len(body) - 4), f"{side}: last row_id == footer u32")
        for r in rows:
            off = r["identity"]["tail_offset_in_row"]
            require(off == r["len"] - IDENT, f"{side} row {r['row']}: identity tail at row end")
        require(census["row_id_unique"] is True, f"{side}: census flag")
        id_lists[side] = ids
        checks += 1
    require(id_lists["client"] == id_lists["server"], "t9 identity row-by-row client == server")
    checks += 1

    # --- 4. extra_9 block framing -------------------------------------------
    for side in SIDES:
        body = payloads[side, "table_extra_9.dat"]
        block = profile["members"][f"{side}/table_extra_9.dat"]["closure"]
        rows = read_rows(OUT / "profiles" / f"table_{side}_extra_9.rows.jsonl")
        require(len(rows) == 251 == block["count"], f"{side} extra_9: 251 blocks")
        pos = 12
        for r in rows:
            require(r["offset"] == pos, f"{side} extra_9 row {r['row']}: contiguous")
            raw = bytes.fromhex(r["raw_hex"])
            require(raw == body[pos:pos + r["len"]], f"{side} extra_9 row {r['row']}: raw_hex")
            require(u32(raw, 0) == r["row"] == r["marker"]["ordinal"], f"{side} extra_9 row {r['row']}: ordinal marker")
            require(u32(raw, 4) == r["marker"]["name_len"], f"{side} extra_9 row {r['row']}: name_len marker")
            pos += r["len"]
        require(pos == len(body), f"{side} extra_9: blocks tile to payload end")
        require(12 + sum(r["len"] for r in rows) == len(body), f"{side} extra_9: closure equation")
        require(block["closure_exact"] is True, f"{side} extra_9: closed flag")
        requires = x9_blocks(body, 12)
        require(requires is not None, f"{side} extra_9: independent marker walk survives")
        checks += 1

    # --- 5. identity structure differs on extra_9 ---------------------------
    xrows = read_rows(OUT / "profiles" / "table_client_extra_9.rows.jsonl")
    first = bytes.fromhex(xrows[0]["raw_hex"])
    require(not (struct.unpack_from("<I", first, 0)[0] == 0
                 and struct.unpack_from("<I", first, 4)[0] == 0), "extra_9 row0 is not an identity tail")
    for side in SIDES:
        block = profile["members"][f"{side}/table_extra_9.dat"]["closure"]
        require(block["identity_structure_present"] is False, f"{side} extra_9: identity recorded absent")
        trial = block["identity_predicate_trial"]
        require(all(r["complete_walks"] == 0 for r in trial["results"]),
                f"{side} extra_9: t9 identity predicate closes nothing (negative preserved)")
        require(trial["verdict"].startswith("NEGATIVE"), f"{side} extra_9: negative verdict preserved verbatim")
        body_x = payloads[side, "table_extra_9.dat"]
        require(closure_walks(body_x, 13, 8) == 0, f"{side} extra_9: independent re-run also 0 walks")
    checks += 1

    # --- 6. cross-archive grammar diff --------------------------------------
    require(diff["status"] == "client_server_row_grammar_not_isomorphic", "diff status")
    t9 = diff["table_9"]
    require(t9["count"]["equal"] is True and t9["count"]["client"] == 251, "diff: equal 251 count")
    require(t9["identity_agrees_row_by_row"] is True, "diff: identity agrees")
    require(t9["identity_first_difference"] is None, "diff: no identity difference")
    require(t9["identical_row_count"] == 0, "diff: no byte-identical rows")
    require(t9["row_len"]["client"] != t9["row_len"]["server"], "diff: row length stats differ")
    for probe in diff["same_offset_probe_row0"]:
        require(probe["meaning"], "probe keeps its unassigned wording")
    ct = diff["cross_table"]
    require(ct["t9_ids_equal_t10_ids"]["client"] is True and ct["t9_ids_equal_t10_ids"]["server"] is True,
            "cross-table: t9 and t10 row_id ladder identical")
    require(ct["t9_row_spans_differ_from_t10"]["client"] is True
            and ct["t9_row_spans_differ_from_t10"]["server"] is True, "cross-table: spans differ")
    # re-derive the cross-table agreement from bytes
    for side in SIDES:
        t10 = payloads[side, "table_10.dat"]
        require(closure_walks(t10, 13, 8) == 1, f"{side}: t10 closes under same predicate")
    checks += 1

    # --- 7. evidence-level discipline --------------------------------------
    lv = profile["evidence_level"]
    require(lv["L3"] == 0 and lv["L4"] == 0, "L3/L4 must be 0")
    require(profile["framing_rules_are_candidates"] is True, "framing rules flagged as candidates")
    for key in ("reads_editor_exe", "follows_reader_or_VA", "names_semantic_fields", "joins_target_ordinals"):
        require(profile["scope"][key] is False, f"scope {key} must be false")
    require(diff["evidence_level"]["L3"] == 0 and diff["evidence_level"]["L4"] == 0, "diff L3/L4 zero")
    checks += 1

    if verbose:
        print(f"rows: {len(read_rows(OUT / 'profiles' / 'table_server_9.rows.jsonl'))} server t9 rows verified")
        print(f"extra_9 block walks: client=1 server={profile['members']['server/table_extra_9.dat']['closure']['block_walks']}")
    print(f"t50 verify PASS ({checks} check groups)")
    return 0


def archive_side_packed(profile: dict[str, Any], side: str, name: str) -> str:
    return profile["archives"][side]["members"][name]["packed_sha256"]


# --------------------------------------------------------------------------
def selftest() -> int:
    # identity predicate must reject a row whose repeated lane differs.
    # Filler is 0xEE so a zero ordinal cannot match decoy runs of padding.
    body = bytearray(b"\xEE" * 32)
    struct.pack_into("<III", body, 4, 0, 7, 8)
    body[16] = 0x00
    require(identity_positions(bytes(body), 0, 0) == [], "selftest: unequal lanes rejected")
    struct.pack_into("<III", body, 4, 0, 7, 7)
    body[16] = 0x00
    require(identity_positions(bytes(body), 0, 0) == [(4, 7)], "selftest: equal lanes accepted")
    # marker byte is load bearing
    body[16] = 0x01
    require(identity_positions(bytes(body), 0, 0) == [], "selftest: non-zero marker rejected")
    # closure_walks needs a real header with count@8
    synth = TAD_MAGIC + struct.pack("<I", 2) + b"\x00"
    for i in range(2):
        synth += b"\xAA" * 6 + struct.pack("<III", i, 3 + i, 3 + i) + b"\x00"
    synth += b"\x00" * 8
    require(closure_walks(synth, 13, 8) == 1, "selftest: synthetic payload closes once")
    require(closure_walks(synth, 13, 9) == 0, "selftest: wrong footer closes nothing")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Independent verifier for scratch/t50/out (data side only).",
        epilog="Exit codes: 0 all checks passed / 1 check failed / 2 usage or fatal error.",
    )
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true", help="run internal predicate selftests")
    group.add_argument("--check", action="store_true", help="verify scratch/t50/out against the archives")
    ap.add_argument("--verbose", action="store_true", help="print extra detail")
    args = ap.parse_args()
    try:
        if args.selftest:
            selftest()
            print("t50 verify selftest PASS")
            return 0
        return verify(args.verbose)
    except VerifyError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
