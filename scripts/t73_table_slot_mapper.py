#!/usr/bin/env python3
"""t73 — generic FM24 packed-table slot mapper (CLI shell).

    py -V:3.12 -I -B scripts/t73_table_slot_mapper.py --table 2 --archive client --json OUT
    py -V:3.12 -I -B scripts/t73_table_slot_mapper.py --help
    py -V:3.12 -I -B scripts/t73_table_slot_mapper.py --selftest

Exit codes: 0 success / 1 check failed / 2 usage or fatal.

Method and grading live in scripts/t73_mapper_core.py; this file is the CLI
surface only. Payload decoding is reused from scripts/fm24_dump.py unchanged.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import t73_mapper_core as core  # noqa: E402

# xml entity per table id, for the four tables in scope plus their FK targets
XML_BY_TABLE = {2: "city.xml", 5: "continent.xml", 19: "region.xml", 41: "currency.xml"}
VAR_TABLES = {41}


def build(archive: str, tid: int) -> dict:
    """Frame + slots for one (archive, table). Never raises for data reasons."""
    out: dict = {"archive": archive, "table": tid, "tool": "t73_table_slot_mapper"}
    try:
        raw = core.load_payload(archive, tid)
    except Exception as exc:  # noqa: BLE001 - preserved verbatim as a negative
        out.update(status="escalate_to_sol",
                   why=f"payload decode failed: {type(exc).__name__}: {exc}")
        return out
    cf = core.canonical_frame(raw)
    out["payload_len"] = len(raw)
    out["payload_sha256"] = __import__("hashlib").sha256(raw).hexdigest()
    if tid in VAR_TABLES and not cf["resolved"]:
        return build_var(out, raw, archive, tid, cf)
    out["frame"] = cf.get("frame")
    out["closure"] = cf.get("closure")
    out["alias_group"] = cf.get("alias_group")
    out["header_origin_data_unique"] = cf.get("header_origin_data_unique")
    out["footer"] = cf.get("footer")
    if not cf["resolved"]:
        out.update(status="escalate_to_sol", why=cf.get("why"))
        return out
    out["status"] = "closed"
    xml = XML_BY_TABLE.get(tid)
    if xml is None:
        out["slots"] = "escalate_to_sol"
        out["why"] = "no editor_schema entity bound to this table id yet"
        return out
    out.update(core.align(raw, archive, tid, xml, cf))
    return out


def build_var(out: dict, raw: bytes, archive: str, tid: int, cf: dict) -> dict:
    """Variable-length tables: header from the frozen 14B origin, rows self-verified."""
    w = core.walk_var(raw, core.H0, 8)
    n_header = w["count_from_header"]
    ok = w["identity_ok_rows"]
    out["frame"] = {"header": core.H0, "footer": w["footer_len"],
                    "count": n_header, "model": "variable"}
    out["closure"] = (f"{core.H0} + sum(row_len) + {w['footer_len']} = {len(raw)} "
                      f"({n_header} rows, {n_header} self-verified trailers)")
    out["footer"] = {"footer_len": w["footer_len"], "footer_hex": w["footer_hex"]}
    out["variable"] = {
        "grammar": "4x(u32 len + utf8) + f32 rate + u32 count + count x 7B"
                   "(u8 kind, u16 year, f32 value) + 13B trailer"
                   "(u32 ordinal, u32 uid, u32 uid, u8 marker)",
        "rows": len(w["rows"]), "identity_ok": ok, "bad": w["bad"],
        "len_hist": w["len_hist"], "footer_hex": w["footer_hex"],
        "min_row_len": min(w["len_hist"]), "max_row_len": max(w["len_hist"]),
        "history_items": sum(r["history_count"] for r in w["rows"]),
        "history_kinds": sorted({it[0] for r in w["rows"] for it in r["history"]}),
    }
    if ok != len(w["rows"]) or w["bad"] or w["footer_len"] != 8:
        out["status"] = "escalate_to_sol"
        out["why"] = (f"variable walk did not close: {ok}/{len(w['rows'])} rows "
                       f"identity-ok, footer {w['footer_len']}B")
        return out
    out["status"] = "closed"
    xml = XML_BY_TABLE.get(tid)
    if xml is None:
        out["slots"] = "escalate_to_sol"
        return out
    out["slots"] = core.align_var(raw, archive, tid, xml, w)
    return out


def selftest() -> int:
    """Offline checks of the pure predicates; no archive access."""
    import struct

    # 1. frame arithmetic + identity on a synthetic table
    n, S, H, F = 5, 16, 14, 8
    body = bytearray()
    for j in range(n):
        row = bytearray(S)
        struct.pack_into("<III", row, S - 12, j, 100 + j, 100 + j)
        body += row
    hdr = b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", n) + bytes(2)
    assert len(hdr) == H, len(hdr)
    raw = hdr + bytes(body) + struct.pack(">I", 1) + struct.pack("<I", 104)
    assert len(raw) == H + n * S + F, (len(raw), H + n * S + F)
    cf = core.canonical_frame(raw, min_rows=1)
    assert cf["resolved"], cf
    assert (cf["stride"], cf["count"], cf["header"]) == (S, n, H), cf
    assert cf["footer"]["footer_len"] == F, cf
    assert cf["identity_offset"] == S - 12, cf

    # 2. footer sensitivity: a 7/8/9 wrap is one alias group, not three answers
    assert cf["alias_size"] >= 1
    assert cf["footer"]["flag_be1"] is True

    # 3. var-length walker round-trips a synthetic currency row
    row = bytearray()
    for s_ in ("A", "B", "", "C"):
        row += struct.pack("<I", len(s_)) + s_.encode()
    row += struct.pack("<f", 1.5) + struct.pack("<I", 1)
    row += bytes([1]) + struct.pack("<H", 2020) + struct.pack("<f", 2.0)
    row += struct.pack("<III", 0, 7, 7) + b"\x00"
    raw2 = (b"\x03\x01tad." + b"\xf1\x0d" + struct.pack("<I", 1) + bytes(2)
            + bytes(row) + struct.pack(">I", 1) + struct.pack("<I", 7))
    assert len(raw2) - len(row) - 14 == 8, len(raw2)
    w = core.walk_var(raw2, 14, 8)
    assert w["bad"] == [], w["bad"]
    assert w["identity_ok_rows"] == 1, w["identity_ok_rows"]
    assert w["rows"][0]["strings"] == ["A", "B", "", "C"]
    assert w["rows"][0]["rate"] == 1.5
    assert w["footer_len"] == 8

    # 4. schema loader sees the four entities
    for xml in ("city.xml", "continent.xml", "region.xml", "currency.xml"):
        assert core.entity(xml)["id"], xml
    print("selftest ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="t73_table_slot_mapper",
        description="Generic FM24 packed-table frame + slot mapper (city/continent/"
                    "region/currency reference set).")
    ap.add_argument("--table", type=int, help="database table id, e.g. 2")
    ap.add_argument("--archive", choices=("client", "server"),
                    help="which .dat archive to read")
    ap.add_argument("--json", metavar="OUT", help="write the result JSON here")
    ap.add_argument("--selftest", action="store_true", help="run offline checks")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.table is None or a.archive is None:
        ap.print_help()
        return 2
    try:
        res = build(a.archive, a.table)
    except Exception as exc:  # noqa: BLE001 - fatal, not a data verdict
        print(f"fatal: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.json:
        p = Path(a.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")
    fr = res.get("frame") or {}
    print(f"table {a.table} {a.archive}: status={res.get('status')} "
          f"closure={res.get('closure')} identity@{fr.get('identity_offset')}")
    for s in (res.get("slots") or []):
        if isinstance(s, dict):
            print(f"  {str(s['field']):8} {str(s['offset']):5} {s['grade']:9} "
                  f"{s['why'][:70]}")
    if res.get("variable"):
        v = res["variable"]
        print(f"  variable rows={v['rows']} identity_ok={v['identity_ok']} "
              f"footer={v['footer_hex']}")
    return 0 if res.get("status") == "closed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
