#!/usr/bin/env python3
"""Independently verify server_db.dat table payload boundaries.

Usage: py -V:3.12 -I -B verify.py [--selftest]
Default mode reads the installed archive read-only and checkpoints boundaries.json
inside this task's OUTDIR after each numeric table.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
BOUNDARIES = HERE / "boundaries.json"
CENSUS_PATH = Path(r"D:\tmp2b\fm24\reports\dbdat_decode\server_tables_census.json")
ARCHIVE = Path(r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\server_db.dat")
HEADER = 14
FOOTER = 8
TAD_HEADER = bytes.fromhex("03 01 74 61 64 2e f1 0d")


class CheckFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CheckFailure(message)


def u32(data: bytes, pos: int) -> int:
    require(0 <= pos and pos + 4 <= len(data), f"u32 out of bounds at {pos:#x}")
    return struct.unpack_from("<I", data, pos)[0]


def inspect_header(raw: bytes, expected_count: int | None = None) -> int:
    require(len(raw) >= HEADER + FOOTER, "payload is shorter than header plus footer")
    require(raw[:8] == TAD_HEADER, f"unexpected tad. header: {raw[:8].hex()}")
    count = u32(raw, 8)
    if expected_count is not None:
        require(count == expected_count, f"header count {count} != census count {expected_count}")
    return count


def fixed_identity(raw: bytes, count: int, stride: int) -> dict[str, Any]:
    """Find all-row ordinal or unique repeated-u32 slots in fixed rows."""
    require(count > 0 and stride > 0, "fixed identity requires nonempty rows")
    require(HEADER + count * stride + FOOTER == len(raw), "fixed row arithmetic does not close")
    row0 = HEADER
    rdui_candidates = [
        off for off in range(max(0, stride - 3))
        if u32(raw, row0 + off) == 0
    ]
    rdui_valid: list[int] = []
    for off in rdui_candidates:
        for i in range(count):
            if u32(raw, HEADER + i * stride + off) != i:
                break
        else:
            rdui_valid.append(off)

    repeated_valid: list[int] = []
    for off in range(max(0, stride - 7)):
        first = u32(raw, row0 + off)
        if first != u32(raw, row0 + off + 4):
            continue
        seen: set[int] = set()
        good = True
        for i in range(count):
            pos = HEADER + i * stride + off
            left, right = u32(raw, pos), u32(raw, pos + 4)
            if left != right or left in seen:
                good = False
                break
            seen.add(left)
        if count == 1 and first == 0:
            good = False
        if good:
            repeated_valid.append(off)

    # A repeated 8-byte ID also creates 1-3 byte-shifted equal-u32 windows;
    # retain the leftmost offset of each contiguous run as its canonical slot.
    repeated_roots = [off for off in repeated_valid if off - 1 not in repeated_valid]

    chosen_rdui: int | None = None
    if len(rdui_valid) == 1:
        chosen_rdui = rdui_valid[0]
    elif len(rdui_valid) > 1 and len(repeated_roots) == 1:
        adjacent = [off for off in rdui_valid if off + 4 == repeated_roots[0]]
        if len(adjacent) == 1:
            chosen_rdui = adjacent[0]

    if chosen_rdui is not None:
        result: dict[str, Any] = {
            "offset": chosen_rdui,
            "kind": "rdui",
            "verified_rows": f"{count}/{count}",
            "rdui_offset": chosen_rdui,
        }
        paired = chosen_rdui + 4
        if paired in repeated_valid:
            result["paired_repeated_u32_offset"] = paired
        elif len(repeated_roots) == 1:
            result["paired_repeated_u32_offset"] = repeated_roots[0]
        return result
    if len(repeated_roots) == 1:
        return {
            "offset": repeated_roots[0],
            "kind": "repeated_u32",
            "verified_rows": f"{count}/{count}",
        }
    return {
        "offset": None,
        "kind": "none",
        "verified_rows": f"0/{count}",
        "rdui_candidates": rdui_valid[:8],
        "repeated_u32_candidates": repeated_valid[:8],
    }


def walk_identity_suffix(raw: bytes, count: int, max_row_span: int = 1 << 20) -> dict[str, Any]:
    """Walk variable rows ending in ordinal|ID|same-ID|marker (opaque body)."""
    footer_start = len(raw) - FOOTER
    pos = HEADER
    marker_counts: Counter[int] = Counter()
    min_span: int | None = None
    max_span = 0
    first_spans: list[int] = []
    last_span = 0
    last_identity_pos: int | None = None
    last_row_start = pos
    last_id: int | None = None

    for index in range(count):
        start = pos
        needle = struct.pack("<I", index)
        search_start = start
        # q+12 is the one-byte marker; q+13 must not pass the footer start.
        search_end = footer_start - 9
        q = raw.find(needle, search_start, search_end)
        while q >= 0:
            repeated = raw[q + 4 : q + 8] == raw[q + 8 : q + 12]
            marker = raw[q + 12] if q + 13 <= footer_start else 0x100
            if repeated and marker in (0, 12):
                break
            q = raw.find(needle, q + 1, search_end)
        if q < 0:
            return {
                "ok": False,
                "rows_walked": index,
                "last_row_start_payload": pos,
                "footer_start_payload": footer_start,
                "reason": f"row {index}: no ordinal|repeated-u32|00-or-0c suffix after payload+0x{start:x}",
                "marker_counts": dict(marker_counts),
            }
        row_end = q + 13
        span = row_end - start
        if span > max_row_span:
            return {
                "ok": False,
                "rows_walked": index,
                "last_row_start_payload": start,
                "footer_start_payload": footer_start,
                "reason": f"row {index}: first matching suffix is {span} bytes away (limit {max_row_span})",
                "marker_counts": dict(marker_counts),
            }
        if row_end > footer_start:
            return {
                "ok": False,
                "rows_walked": index,
                "last_row_start_payload": start,
                "footer_start_payload": footer_start,
                "reason": f"row {index}: identity marker crosses footer boundary",
                "marker_counts": dict(marker_counts),
            }
        marker = raw[q + 12]
        marker_counts[marker] += 1
        min_span = span if min_span is None else min(min_span, span)
        max_span = max(max_span, span)
        if len(first_spans) < 5:
            first_spans.append(span)
        last_span = span
        last_identity_pos = q
        last_row_start = start
        last_id = u32(raw, q + 4)
        pos = row_end

    if pos != footer_start:
        return {
            "ok": False,
            "rows_walked": count,
            "last_row_start_payload": last_row_start,
            "last_row_end_payload": pos,
            "footer_start_payload": footer_start,
            "reason": f"last row ends at payload+0x{pos:x}; footer starts at payload+0x{footer_start:x}",
            "marker_counts": dict(marker_counts),
        }
    return {
        "ok": True,
        "rows_walked": count,
        "row_span_sum": pos - HEADER,
        "last_row_start_payload": last_row_start,
        "last_row_span": last_span,
        "last_row_end_payload": pos,
        "footer_start_payload": footer_start,
        "identity_offset": "row_end-13",
        "repeated_u32_offset": "row_end-9",
        "last_identity_payload_offset": last_identity_pos,
        "last_identity_id": last_id,
        "marker_counts": dict(marker_counts),
        "min_row_span": min_span,
        "max_row_span": max_span,
        "first_row_spans": first_spans,
    }


def walk_identity_suffix_reverse(raw: bytes, count: int, max_row_span: int = 1 << 20) -> dict[str, Any]:
    """Walk the same ordinal/repeated-ID frame from the footer backwards."""
    footer_start = len(raw) - FOOTER
    if count == 0:
        return {"ok": footer_start == HEADER, "rows_walked": 0, "last_row_end_payload": HEADER,
                "footer_start_payload": footer_start, "reason": "empty reverse walk"}
    last_q = footer_start - 13
    if (last_q < HEADER or raw[last_q:last_q + 4] != struct.pack("<I", count - 1)
            or raw[last_q + 4:last_q + 8] != raw[last_q + 8:last_q + 12]
            or raw[last_q + 12] not in (0, 12)):
        return {"ok": False, "rows_walked": 0, "footer_start_payload": footer_start,
                "reason": f"last-row identity does not exactly meet footer at payload+0x{footer_start:x}"}
    anchors = [last_q]
    next_q = last_q
    markers: Counter[int] = Counter({raw[last_q + 12]: 1})
    for index in range(count - 2, -1, -1):
        needle = struct.pack("<I", index)
        lower = max(HEADER, next_q - max_row_span)
        q = raw.rfind(needle, lower, next_q)
        while q >= 0:
            valid = (q + 13 <= next_q
                     and raw[q + 4:q + 8] == raw[q + 8:q + 12]
                     and raw[q + 12] in (0, 12))
            if valid:
                break
            q = raw.rfind(needle, lower, q)
        if q < 0:
            return {"ok": False, "rows_walked": count - 1 - index,
                    "footer_start_payload": footer_start,
                    "last_row_start_payload": next_q + 13,
                    "reason": f"reverse row {index}: no ordinal|repeated-u32|marker suffix within {max_row_span} bytes"}
        span_to_next_anchor = next_q - q
        if span_to_next_anchor < 13 or span_to_next_anchor > max_row_span:
            return {"ok": False, "rows_walked": count - 1 - index,
                    "footer_start_payload": footer_start,
                    "reason": f"reverse row {index}: implausible adjacent-anchor distance {span_to_next_anchor}"}
        anchors.append(q)
        markers[raw[q + 12]] += 1
        next_q = q
    oldest_q = anchors[-1]
    first_span = oldest_q + 13 - HEADER
    if not (13 <= first_span <= max_row_span):
        return {"ok": False, "rows_walked": count, "footer_start_payload": footer_start,
                "reason": f"reverse first row span {first_span} does not start at header+14"}
    ordered = list(reversed(anchors))
    spans = [first_span] + [ordered[i] - ordered[i - 1] for i in range(1, len(ordered))]
    require(len(spans) == count and all(13 <= span <= max_row_span for span in spans),
            "reverse suffix spans are inconsistent")
    return {
        "ok": True,
        "rows_walked": count,
        "row_span_sum": sum(spans),
        "last_row_start_payload": ordered[-2] + 13 if count > 1 else HEADER,
        "last_row_span": spans[-1],
        "last_row_end_payload": footer_start,
        "footer_start_payload": footer_start,
        "identity_offset": "row_end-13",
        "repeated_u32_offset": "row_end-9",
        "last_identity_payload_offset": last_q,
        "marker_counts": dict(markers),
        "min_row_span": min(spans),
        "max_row_span": max(spans),
        "first_row_spans": spans[:5],
    }


def walk_currency(raw: bytes, expected_count: int | None = None) -> dict[str, Any]:
    """Parse table_41's four strings, rate, history vector, and 13-byte trailer."""
    count = inspect_header(raw, expected_count)
    footer_start = len(raw) - FOOTER
    pos = HEADER
    marker_counts: Counter[int] = Counter()
    total_history = 0
    min_span: int | None = None
    max_span = 0
    last_row_start = pos
    last_span = 0
    for index in range(count):
        start = pos
        for string_index in range(4):
            require(pos + 4 <= footer_start, f"currency row {index}: missing string length {string_index}")
            size = u32(raw, pos)
            pos += 4
            require(size <= 1 << 20 and pos + size <= footer_start,
                    f"currency row {index}: invalid UTF-8 string length {size}")
            raw[pos : pos + size].decode("utf-8")
            pos += size
        require(pos + 8 <= footer_start, f"currency row {index}: truncated rate/history count")
        pos += 4  # f32 current rate
        history_count = u32(raw, pos)
        pos += 4
        require(history_count <= 256, f"currency row {index}: history count {history_count} > 256")
        require(pos + history_count * 7 + 13 <= footer_start,
                f"currency row {index}: history items/trailer exceed payload")
        total_history += history_count
        pos += history_count * 7
        ordinal, id_a, id_b = struct.unpack_from("<III", raw, pos)
        marker = raw[pos + 12]
        require(ordinal == index, f"currency row {index}: trailer ordinal {ordinal}")
        require(id_a == id_b, f"currency row {index}: repeated u32 identity differs")
        require(marker == 0, f"currency row {index}: trailer marker {marker:#x}")
        marker_counts[marker] += 1
        pos += 13
        last_row_start = start
        last_span = pos - start
        min_span = last_span if min_span is None else min(min_span, last_span)
        max_span = max(max_span, last_span)
    require(pos == footer_start,
            f"currency rows end at payload+0x{pos:x}; footer at payload+0x{footer_start:x}")
    return {
        "ok": True,
        "rows_walked": count,
        "row_span_sum": pos - HEADER,
        "last_row_start_payload": last_row_start,
        "last_row_span": last_span,
        "last_row_end_payload": pos,
        "footer_start_payload": footer_start,
        "identity_offset": "row_end-13",
        "repeated_u32_offset": "row_end-9",
        "marker_counts": dict(marker_counts),
        "total_history_items": total_history,
        "min_row_span": min_span,
        "max_row_span": max_span,
    }


def analyze_table(raw: bytes, table_id: int, census_row: dict[str, Any]) -> dict[str, Any]:
    count = inspect_header(raw, census_row.get("record_count_header"))
    payload_len = len(raw)
    result: dict[str, Any] = {
        "table_id": table_id,
        "count": count,
        "header_extra_hex": raw[12:14].hex(),
        "payload_len": payload_len,
        "payload_sha256": hashlib.sha256(raw).hexdigest(),
        "entity": (census_row.get("entity_mapping") or {}).get("entity"),
        "source_row_model": census_row.get("row_model"),
        "model": "unresolved",
        "verified": False,
        "status": "partial_negative",
        "identity": {"offset": None, "kind": "none", "verified_rows": f"0/{count}"},
        "closure": None,
        "evidence": "独立解压；payload 头、count、长度和 SHA-256 均从原始字节复算。",
    }

    if count == 0:
        require(payload_len == HEADER + FOOTER, f"table_{table_id}: empty payload length {payload_len} != 22")
        result.update({
            "model": "empty",
            "verified": True,
            "status": "complete",
            "closure": f"14 + 0 + 8 == {payload_len}",
            "identity": {"offset": None, "kind": "none", "verified_rows": "0/0"},
            "evidence": "header count=0；payload 恰为 14-byte header + 8-byte footer。",
        })
        return result

    row_area = payload_len - HEADER - FOOTER
    if row_area > 0 and row_area % count == 0:
        candidate_stride = row_area // count
        ident = fixed_identity(raw, count, candidate_stride)
        if ident["kind"] != "none":
            result.update({
                "model": "fixed",
                "stride": candidate_stride,
                "verified": True,
                "status": "complete",
                "identity": ident,
                "closure": f"14 + {count}*{candidate_stride} + 8 == {payload_len}",
                "evidence": "整除闭包精确成立；对每一行复算 identity 槽，rdui 顺序或唯一 repeated-u32 检查全行通过。",
            })
            return result
        result["arithmetic_candidate_stride"] = candidate_stride
        result["candidate_closure"] = f"14 + {count}*{candidate_stride} + 8 == {payload_len}"
        result["evidence"] += " 行区整除，但没有唯一、全行成立的 rdui/repeated-u32 identity 槽，因此不把步长确认为事实。"

    if table_id == 41:
        parsed = walk_currency(raw, count)
        reverse_check = walk_identity_suffix_reverse(raw, count)
        result.update({
            "model": "variable",
            "verified": True,
            "status": "complete",
            "identity": {"offset": "row_end-13", "kind": "rdui", "verified_rows": f"{count}/{count}",
                         "paired_repeated_u32_offset": "row_end-9"},
            "closure": f"last_row_end_payload={parsed['last_row_end_payload']}; footer_len=8; {parsed['last_row_end_payload']}+8 == {payload_len}",
            "boundary_grammar": "4×(u32 UTF-8长度 + UTF-8字节)；f32 rate；u32 history_count；history_count×7-byte item；13-byte trailer=(u32 ordinal,u32 ID,u32 same-ID,u8 00)。",
            "row_span_sum": parsed["row_span_sum"],
            "last_row_start_payload": parsed["last_row_start_payload"],
            "last_row_end_payload": parsed["last_row_end_payload"],
            "footer_len": FOOTER,
            "identity_rows": parsed["rows_walked"],
            "reverse_boundary_check": {"ok": reverse_check["ok"], "rows_walked": reverse_check.get("rows_walked"),
                                        "reason": reverse_check.get("reason")},
            "evidence": "独立逐行消费四个 UTF-8 字符串、rate、history count/items 与 identity trailer；UTF-8、ordinal、重复-u32、marker 和 footer 闭合全部全表通过。另对尾锚独立执行倒序闭合复核。",
        })
        return result

    forward_attempt = walk_identity_suffix(raw, count)
    reverse_attempt = walk_identity_suffix_reverse(raw, count)
    walked = forward_attempt
    walk_direction = "forward"
    if not walked["ok"] and reverse_attempt["ok"]:
        walked = reverse_attempt
        walk_direction = "reverse"
    if walked["ok"]:
        result.update({
            "model": "variable",
            "verified": True,
            "status": "complete",
            "identity": {"offset": "row_end-13", "kind": "rdui", "verified_rows": f"{count}/{count}",
                         "paired_repeated_u32_offset": "row_end-9"},
            "closure": f"last_row_end_payload={walked['last_row_end_payload']}; footer_len=8; {walked['last_row_end_payload']}+8 == {payload_len}",
            "boundary_grammar": "每行 body 长度可变；body 后缀为 u32le ordinal(逐行等于 0..count-1) | u32le ID | 同值 u32le | 1-byte marker(本表观察值 00/0c)；下一行紧接 marker 后。body 字段语义未解。",
            "walk_direction": walk_direction,
            "reverse_boundary_check": {"ok": reverse_attempt["ok"], "rows_walked": reverse_attempt.get("rows_walked"),
                                        "reason": reverse_attempt.get("reason")},
            "row_span_sum": walked["row_span_sum"],
            "last_row_start_payload": walked["last_row_start_payload"],
            "last_row_end_payload": walked["last_row_end_payload"],
            "footer_len": FOOTER,
            "row_span_min": walked["min_row_span"],
            "row_span_max": walked["max_row_span"],
            "marker_counts": {str(k): v for k, v in walked["marker_counts"].items()},
            "evidence": "逐行在原始 payload 中定位 ordinal|重复-u32|marker 后缀；每行 ordinal 顺序、重复-u32、marker 和最后一行/footer 精确相接均通过。变长 body 仍作为 opaque bytes。",
        })
        return result

    result.update({
        "model": "unresolved",
        "status": "partial_negative",
        "identity": {"offset": "row_end-13" if walked.get("rows_walked", 0) else None,
                     "kind": "rdui" if walked.get("rows_walked", 0) else "none",
                     "verified_rows": f"{walked.get('rows_walked', 0)}/{count}"},
        "partial_rows_walked": walked.get("rows_walked", 0),
        "last_row_start_payload": walked.get("last_row_start_payload"),
        "footer_start_payload": walked.get("footer_start_payload"),
        "blocking_point": forward_attempt.get("reason"),
        "reverse_blocking_point": reverse_attempt.get("reason"),
        "closure": "未建立；无法给出最后一行结束位置 + 8 == payload 长度的精确等式。",
        "evidence": "独立尝试 ordinal|repeated-u32|marker 变长后缀走查；失败点已保留，不将未封口的候选边界写成结论。",
    })
    return result


def persist_progress(result: dict[str, Any]) -> None:
    temp = BOUNDARIES.with_suffix(".json.tmp")
    temp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(BOUNDARIES)


def make_synthetic(count: int, body_rows: list[bytes]) -> bytes:
    return TAD_HEADER + struct.pack("<I", count) + b"\x00\x00" + b"".join(body_rows) + b"\x00\x00\x00\x01\x12\x34\x56\x78"


def run_selftest() -> None:
    # Fixed rows: ordinal at +0 and repeated-u32 ID at +4.
    fixed = make_synthetic(2, [struct.pack("<III", 0, 100, 100), struct.pack("<III", 1, 200, 200)])
    require(len(fixed) == 14 + 2 * 12 + 8, "synthetic fixed size")
    ident = fixed_identity(fixed, 2, 12)
    require(ident["kind"] == "rdui" and ident["offset"] == 0, "fixed rdui identity")
    require(ident.get("paired_repeated_u32_offset") == 4, "fixed repeated-u32 cross-check")

    empty = make_synthetic(0, [])
    require(len(empty) == 22 and inspect_header(empty) == 0, "empty closure")

    suffix_payload = make_synthetic(2, [
        b"alpha" + struct.pack("<III", 0, 123, 123) + b"\x00",
        b"a longer opaque body" + struct.pack("<III", 1, 456, 456) + b"\x0c",
    ])
    suffix = walk_identity_suffix(suffix_payload, 2)
    require(suffix["ok"], f"variable suffix walk: {suffix}")
    require(suffix["last_row_end_payload"] + FOOTER == len(suffix_payload), "variable footer equation")
    require(suffix["marker_counts"] == {0: 1, 12: 1}, "variable marker classes")
    suffix_reverse = walk_identity_suffix_reverse(suffix_payload, 2)
    require(suffix_reverse["ok"], f"reverse variable suffix walk: {suffix_reverse}")
    require(suffix_reverse["last_row_end_payload"] + FOOTER == len(suffix_payload), "reverse footer equation")

    # Currency-like row: four UTF-8 strings, float, empty history list, identity trailer.
    strings = [b"Unit", b"U", b"", b"$"]
    currency_row = b"".join(struct.pack("<I", len(s)) + s for s in strings)
    currency_row += struct.pack("<fI", 1.25, 0) + struct.pack("<IIIB", 0, 700, 700, 0)
    currency = make_synthetic(1, [currency_row])
    parsed_currency = walk_currency(currency, 1)
    require(parsed_currency["ok"] and parsed_currency["rows_walked"] == 1, "currency grammar")
    require(parsed_currency["last_row_end_payload"] + FOOTER == len(currency), "currency footer equation")

    broken = bytearray(suffix_payload)
    broken[14 + len(b"alpha") + 4 : 14 + len(b"alpha") + 8] = struct.pack("<I", 999)
    require(not walk_identity_suffix(bytes(broken), 2)["ok"], "bad repeated identity must fail")
    require(not walk_identity_suffix_reverse(bytes(broken), 2)["ok"], "reverse walker must reject bad repeated identity")
    print("selftest OK: fixed identity, empty closure, forward/reverse variable suffixes, currency grammar and exact footer equations")


def run_archive() -> int:
    common = __import__("runpy").run_path(str(HERE / "common.py"))
    helper, _archive_data, _layout, entries = common["load_environment"](ARCHIVE)
    census_doc = json.loads(CENSUS_PATH.read_text(encoding="utf-8"))
    census_rows = {row["table_id"]: row for row in census_doc["entries"] if row.get("table_id") is not None}
    ids = sorted(census_rows)
    require(len(ids) == 59, f"census numeric table count {len(ids)} != 59")
    directory_ids = sorted(entry["table_id"] for entry in entries if entry.get("table_id") is not None)
    require(directory_ids == ids, "archive numeric table IDs differ from census numeric table IDs")

    result: dict[str, Any] = {
        "status": "in_progress",
        "archive": str(ARCHIVE),
        "payload_sha256_ok": None,
        "payload_sha256_missing_expected": [],
        "tables": [{"table_id": table_id, "status": "in_progress"} for table_id in ids],
    }
    persist_progress(result)
    failed_payloads: list[dict[str, Any]] = []
    known_hash_checks = 0
    for table_id in ids:
        try:
            raw, entry = common["load_payload"](table_id, ARCHIVE)
            expected = census_rows[table_id]
            digest = hashlib.sha256(raw).hexdigest()
            if expected.get("payload_sha256") is None:
                result["payload_sha256_missing_expected"].append(table_id)
            else:
                known_hash_checks += 1
                require(digest == expected["payload_sha256"],
                        f"table_{table_id}: payload SHA-256 mismatch: {digest} != {expected['payload_sha256']}")
            require(len(raw) == expected["payload_size"],
                    f"table_{table_id}: payload size {len(raw)} != census {expected['payload_size']}")
            table_result = analyze_table(raw, table_id, expected)
            table_result["payload_sha256_expected"] = expected.get("payload_sha256")
            table_result["payload_sha256_match"] = (digest == expected["payload_sha256"] if expected.get("payload_sha256") else None)
            table_result["archive_member_size"] = entry["size"]
            result["tables"][len([t for t in result["tables"] if t.get("status") != "in_progress"])] = table_result
            verified = table_result["verified"]
            state = "PASS" if verified else "PARTIAL"
            extra = f" {table_result.get('closure') or table_result.get('blocking_point')}"
            print(f"{state} table_{table_id}: count={table_result['count']} model={table_result['model']}{extra}")
        except Exception as exc:
            failed_payloads.append({"table_id": table_id, "error": f"{type(exc).__name__}: {exc}"})
            replace_index = len([t for t in result["tables"] if t.get("status") != "in_progress"])
            result["tables"][replace_index] = {
                "table_id": table_id, "status": "partial_negative", "model": "unresolved",
                "verified": False, "identity": {"offset": None, "kind": "none", "verified_rows": "0/0"},
                "blocking_point": f"payload load/hash/parse failure: {type(exc).__name__}: {exc}",
            }
            print(f"FAIL table_{table_id}: {type(exc).__name__}: {exc}", file=sys.stderr)
        persist_progress(result)

    verified_count = sum(bool(item.get("verified")) for item in result["tables"])
    negative_ids = [item["table_id"] for item in result["tables"] if not item.get("verified")]
    result["payload_sha256_ok"] = not failed_payloads and known_hash_checks == 58
    result["payload_sha256_checks"] = f"{known_hash_checks}/58 census hashes available; table 21 expected hash missing from census"
    result["summary"] = {
        "numeric_tables": len(result["tables"]),
        "verified_tables": verified_count,
        "unresolved_tables": negative_ids,
        "fully_walked_variable_tables": [item["table_id"] for item in result["tables"]
                                          if item.get("model") == "variable" and item.get("verified")],
        "failed_payloads": failed_payloads,
    }
    result["status"] = "complete_all" if verified_count == 59 else ("complete_partial" if verified_count >= 52 else "partial_negative")
    persist_progress(result)
    print(f"\nSUMMARY: verified={verified_count}/59; variable_walked={len(result['summary']['fully_walked_variable_tables'])}; unresolved={negative_ids}")
    print(f"payload_sha256_ok={result['payload_sha256_ok']} ({result['payload_sha256_checks']})")
    return 0 if not failed_payloads and verified_count >= 52 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run pure offline synthetic checks")
    args = parser.parse_args()
    try:
        if args.selftest:
            run_selftest()
            return 0
        return run_archive()
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
