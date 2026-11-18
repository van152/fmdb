#!/usr/bin/env python3
"""Read-only validator for the t02-g2 client nation row frame.

Run from the workspace root with:
  py -V:3.12 -I -B scratch/t02/inbox/nati/OUTBOX/verify.py --help
  py -V:3.12 -I -B scratch/t02/inbox/nati/OUTBOX/verify.py --selftest

Reads only the colocated client_db_t10.bin; writes nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import struct
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD = HERE.parent / "client_db_t10.bin"
EXPECTED_SHA256 = "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34"
EXPECTED_SIZE = 24732
EXPECTED_ROWS = 251
HEADER_SIZE = 14
FOOTER_SIZE = 8


class CheckFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CheckFailure(message)


def u32(data: bytes, off: int) -> int:
    require(off >= 0 and off + 4 <= len(data), f"u32 out of bounds at {off:#x}")
    return struct.unpack_from("<I", data, off)[0]


def read_count(data: bytes, off: int, width: int, label: str) -> int:
    require(off >= 0 and off + width <= len(data), f"{label} count out of bounds at body+{off:#x}")
    if width == 1:
        value = struct.unpack_from("<b", data, off)[0]
    else:
        value = struct.unpack_from("<i", data, off)[0]
    require(value >= 0, f"{label} has negative signed count {value} at body+{off:#x}")
    return value


def consume(data: bytes, pos: int, size: int, label: str) -> int:
    require(size >= 0 and pos + size <= len(data),
            f"{label} overruns body: body+{pos:#x}+{size:#x} > {len(data):#x}")
    return pos + size


def parse_payload(raw: bytes) -> dict:
    require(len(raw) >= HEADER_SIZE + FOOTER_SIZE, "payload shorter than header/footer")
    require(raw[:8] == bytes.fromhex("03 01 74 61 64 2e f1 0d"), "unexpected tad. header")
    row_count = u32(raw, 8)
    require(row_count == EXPECTED_ROWS, f"row count {row_count}, expected {EXPECTED_ROWS}")
    require(raw[12:14] == b"\x00\x00", "header bytes +0xc..+0xd differ")
    footer_start = len(raw) - FOOTER_SIZE
    body = raw[HEADER_SIZE:footer_start]
    pos = 0
    rows: list[dict] = []

    for index in range(row_count):
        start = pos
        require(start + 25 <= len(body), f"row {index}: truncated 25-byte prefix")

        # Collection A: signed byte count is the tenth prefix transfer at row+24.
        count_a = read_count(body, start + 24, 1, f"row {index} collection A")
        pos = consume(body, start, 25, f"row {index} prefix")
        items_a_start = pos
        pos = consume(body, pos, count_a * 5, f"row {index} collection A items")

        # Collections B and C each have an inline signed i32 count and 28-byte items.
        count_b_off = pos
        count_b = read_count(body, count_b_off, 4, f"row {index} collection B")
        items_b_start = count_b_off + 4
        pos = consume(body, items_b_start, count_b * 28, f"row {index} collection B items")

        count_c_off = pos
        count_c = read_count(body, count_c_off, 4, f"row {index} collection C")
        items_c_start = count_c_off + 4
        pos = consume(body, items_c_start, count_c * 28, f"row {index} collection C items")

        # Collection D has 12-byte items (three u32 transfers).
        count_d_off = pos
        count_d = read_count(body, count_d_off, 4, f"row {index} collection D")
        items_d_start = count_d_off + 4
        pos = consume(body, items_d_start, count_d * 12, f"row {index} collection D items")

        identity_off = pos
        require(identity_off + 13 <= len(body), f"row {index}: truncated identity/marker")
        ordinal = u32(body, identity_off)
        row_id = u32(body, identity_off + 4)
        repeat_id = u32(body, identity_off + 8)
        marker = body[identity_off + 12]
        require(ordinal == index,
                f"row {index}: identity ordinal at body+{identity_off:#x} is {ordinal}")
        require(row_id == repeat_id,
                f"row {index}: repeated identity differs at body+{identity_off + 4:#x}")
        require(marker == 0,
                f"row {index}: boundary byte at body+{identity_off + 12:#x} is {marker:#x}")

        row_end = identity_off + 13
        expected_len = 50 + 5 * count_a + 28 * count_b + 28 * count_c + 12 * count_d
        require(row_end - start == expected_len,
                f"row {index}: span {row_end - start}, formula gives {expected_len}")
        rows.append({
            "index": index,
            "start_body": start,
            "start_payload": HEADER_SIZE + start,
            "end_body": row_end,
            "span": row_end - start,
            "counts": (count_a, count_b, count_c, count_d),
            "count_offsets_body": (start + 24, count_b_off, count_c_off, count_d_off),
            "item_offsets_body": (items_a_start, items_b_start, items_c_start, items_d_start),
            "identity_body": identity_off,
            "identity_payload": HEADER_SIZE + identity_off,
            "ordinal": ordinal,
            "id": row_id,
            "repeat_id": repeat_id,
            "marker": marker,
        })
        pos = row_end

    require(pos == len(body), f"row walk ended at body+{pos:#x}, body ends at {len(body):#x}")
    require(HEADER_SIZE + pos + FOOTER_SIZE == len(raw), "payload closure equation failed")

    totals = [sum(row["counts"][j] for row in rows) for j in range(4)]
    maxima = [max(row["counts"][j] for row in rows) for j in range(4)]
    require(totals == [492, 214, 63, 162], f"count totals changed: {totals}")
    require(maxima == [7, 40, 21, 2], f"count maxima changed: {maxima}")
    spans = {row["span"] for row in rows}
    require(len(spans) == 44 and min(spans) == 50 and max(spans) == 1199,
            f"row-span distribution changed: distinct={len(spans)}, min={min(spans)}, max={max(spans)}")

    anchor = 0x1046
    require(raw[anchor:anchor + 8] == bytes.fromhex("6e 00 00 00 6e 00 00 00"),
            "duni anchor bytes differ")
    row55 = rows[55]
    require(row55["identity_payload"] == 0x1042, "row 55 identity offset does not meet duni anchor")
    require(raw[anchor - 4:anchor] == bytes.fromhex("37 00 00 00"),
            "row 55 ordinal preceding duni does not equal 55")
    require(row55["id"] == 110 and row55["repeat_id"] == 110, "row 55 duni identity mismatch")

    return {
        "rows": rows,
        "body_bytes": len(body),
        "sum_row_spans": pos,
        "footer_start": footer_start,
        "footer_hex": raw[footer_start:].hex(" "),
        "count_totals": totals,
        "count_maxima": maxima,
        "nonzero_count_rows": [sum(row["counts"][j] != 0 for row in rows) for j in range(4)],
        "row55": row55,
    }


def run_selftest() -> None:
    raw = PAYLOAD.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(len(raw) == EXPECTED_SIZE, f"payload size {len(raw)}, expected {EXPECTED_SIZE}")
    require(digest == EXPECTED_SHA256, f"payload SHA-256 mismatch: {digest}")
    parsed = parse_payload(raw)
    rows = parsed["rows"]
    require(len(rows) == 251, "row count mismatch after parse")
    max_row = max(rows, key=lambda row: row["span"])
    require(max_row["index"] == 143 and max_row["span"] == 1199,
            "longest-row guard changed")
    print(
        "PASS: client nati rows=251; formula spans="
        f"{parsed['sum_row_spans']}; closure=14+{parsed['sum_row_spans']}+8={len(raw)}; "
        f"count totals A/B/C/D={parsed['count_totals']}; row55 identity@payload+0x1042; "
        f"duni@payload+0x1046 verified; footer={parsed['footer_hex']}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="verify hashes, all row bounds, identity blocks, and closure")
    args = parser.parse_args()
    try:
        # Default invocation runs the same read-only validation as --selftest.
        run_selftest()
    except CheckFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
