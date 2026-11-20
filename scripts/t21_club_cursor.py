#!/usr/bin/env python3
"""Audit club row framing and independently recheck RTTI reader evidence."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EDITOR = Path(r"<OLD_REPO>\input\editor.exe")
RTTI_CENSUS = ROOT / "scratch/t01/inbox/t01h/output.json"
OUT = ROOT / "scratch/t21/out"
EXPECTED_ROWS = 84259
COMPACT_ROWS = {69706, 69707, 69708}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def import_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_standard_row(raw: bytes, start: int, ordinal: int) -> dict[str, Any] | None:
    if start + 30 > len(raw):
        return None
    try:
        ids = struct.unpack_from("<4I", raw, start)
        full_len = struct.unpack_from("<I", raw, start + 26)[0]
        if full_len > 4096:
            return None
        full_start = start + 30
        short_len_at = full_start + full_len
        if short_len_at + 4 > len(raw):
            return None
        full_name = raw[full_start:short_len_at].decode("utf-8")
        short_len = struct.unpack_from("<I", raw, short_len_at)[0]
        if short_len > 4096:
            return None
        short_start = short_len_at + 4
        identity_at = short_start + short_len + 3
        if identity_at + 13 > len(raw):
            return None
        short_name = raw[short_start:short_start + short_len].decode("utf-8")
        row_id, duni_a, duni_b = struct.unpack_from("<III", raw, identity_at)
        marker = raw[identity_at + 12]
        if row_id != ordinal or duni_a != duni_b or marker not in (0, 12):
            return None
        end = identity_at + 13
        return {
            "ordinal": ordinal, "start": start, "end": end,
            "length": end - start, "standard": True, "ids": ids,
            "full_name": full_name, "short_name": short_name,
            "full_len": full_len, "short_len": short_len,
            "identity_at": identity_at, "identity_relative": identity_at - start,
            "duni": duni_a, "marker": marker,
        }
    except (UnicodeDecodeError, struct.error):
        return None


def find_compact_row(raw: bytes, start: int, ordinal: int) -> dict[str, Any]:
    needle = struct.pack("<I", ordinal)
    stop = min(start + 8192, len(raw))
    hits = []
    at = raw.find(needle, start + 20, stop)
    while at >= 0:
        row_id, duni_a, duni_b = struct.unpack_from("<III", raw, at)
        marker = raw[at + 12]
        if row_id == ordinal and duni_a == duni_b and marker in (0, 12):
            hits.append((at, duni_a, marker))
        at = raw.find(needle, at + 1, stop)
    if len(hits) != 1:
        raise ValueError(f"compact row {ordinal}: expected one identity hit, got {len(hits)}")
    identity_at, duni, marker = hits[0]
    if identity_at - start != 42:
        raise ValueError(f"compact row {ordinal}: identity offset {identity_at - start} != 42")
    return {
        "ordinal": ordinal, "start": start, "end": identity_at + 13,
        "length": identity_at + 13 - start, "standard": False,
        "ids": struct.unpack_from("<4I", raw, start),
        "full_name": None, "short_name": None, "full_len": None,
        "short_len": None, "identity_at": identity_at,
        "identity_relative": 42, "duni": duni, "marker": marker,
    }


def walk_club(raw: bytes) -> list[dict[str, Any]]:
    if len(raw) < 22:
        raise ValueError("club payload is shorter than header and footer")
    count = struct.unpack_from("<I", raw, 8)[0]
    if count != EXPECTED_ROWS:
        raise ValueError(f"club row count {count} != expected {EXPECTED_ROWS}")
    footer_at = len(raw) - 8
    rows = []
    pos = 14
    for ordinal in range(count):
        row = (find_compact_row(raw, pos, ordinal) if ordinal in COMPACT_ROWS
               else parse_standard_row(raw, pos, ordinal))
        if row is None:
            raise ValueError(f"standard row parse failed at ordinal {ordinal}, offset {pos:#x}")
        if row["end"] <= pos or row["end"] > footer_at:
            raise ValueError(f"invalid row end at ordinal {ordinal}: {row['end']:#x}")
        rows.append(row)
        pos = row["end"]
    if pos != footer_at:
        raise ValueError(f"row end {pos:#x} does not meet footer {footer_at:#x}")
    return rows


def profile_rows(raw: bytes, rows: list[dict[str, Any]]) -> dict[str, Any]:
    relations = Counter()
    byte20 = Counter()
    marker_counts = Counter()
    row_lengths = Counter()
    for row in rows:
        start = row["start"]
        values = {off: struct.unpack_from("<I", raw, start + off)[0]
                  for off in (0, 4, 8, 12, 16)}
        for a, b in ((0, 8), (0, 12), (8, 12), (0, 16)):
            relations[f"u32@{a}==u32@{b}"] += values[a] == values[b]
        byte20[raw[start + 20]] += 1
        marker_counts[row["marker"]] += 1
        row_lengths[row["length"]] += 1
    ranges = []
    for label, lo, hi in (("before_69705", 0, 69705), ("from_69705", 69705, len(rows))):
        subset = rows[lo:hi]
        equal_0_8 = sum(row["ids"][0] == row["ids"][2] for row in subset)
        equal_0_12 = sum(row["ids"][0] == row["ids"][3] for row in subset)
        ranges.append({
            "label": label, "ordinal_start_inclusive": lo,
            "ordinal_end_exclusive": hi, "row_count": len(subset),
            "u32_at_0_equals_8": equal_0_8,
            "u32_at_0_equals_8_ratio": equal_0_8 / len(subset) if subset else None,
            "u32_at_0_equals_12": equal_0_12,
        })
    samples = []
    for ordinal in (69704, 69705, 69706, 69707, 69708, 69709, 69710):
        row = rows[ordinal]
        start = row["start"]
        samples.append({
            "ordinal": ordinal, "member_offset": hex(start),
            "row_length": row["length"], "standard_name_parse": row["standard"],
            "fixed_u32": {str(off): struct.unpack_from("<I", raw, start + off)[0]
                          for off in (0, 4, 8, 12)},
            "marker": row["marker"], "identity_relative": row["identity_relative"],
        })
    return {
        "row_count": len(rows),
        "standard_rows": sum(row["standard"] for row in rows),
        "compact_rows": [row["ordinal"] for row in rows if not row["standard"]],
        "footer_offset": hex(len(raw) - 8), "footer_hex": raw[-8:].hex(" "),
        "row_end_offset": hex(rows[-1]["end"]),
        "footer_exact": rows[-1]["end"] == len(raw) - 8,
        "row_length_classes": len(row_lengths),
        "marker_counts": {str(k): v for k, v in sorted(marker_counts.items())},
        "fixed_word_relations": dict(sorted(relations.items())),
        "fixed_byte_20_counts": {str(k): v for k, v in byte20.most_common(16)},
        "ordinal_window_diagnostics": ranges,
        "transition_samples": samples,
        "compact_row_details": [{
            "ordinal": row["ordinal"], "member_offset": hex(row["start"]),
            "length": row["length"], "identity_relative": row["identity_relative"],
            "id_words_0_4_8_12": list(row["ids"]), "marker": row["marker"],
        } for row in rows if not row["standard"]],
    }


def normalize_instruction(text: str) -> str:
    return " ".join(text.strip().split())


def verify_static_sources(pe, md, raw: bytes, census: dict[str, Any]) -> dict[str, Any]:
    item = next((x for x in census.get("census", []) if x.get("type_id") == 3), None)
    if item is None:
        raise ValueError("type 3 is absent from t01h RTTI census")
    targets = {".?AVCLUB@db@@": "CLUB",
               ".?AVLEAGUE_BODY_CLUB@db@@": "LEAGUE_BODY_CLUB"}
    results = []
    branch_mnemonics = {"ja", "jae", "jb", "jbe", "je", "jg", "jge", "jl", "jle",
                        "jne", "jno", "jnp", "jns", "jnz", "jo", "jp", "js", "jz"}
    for cls in item.get("constructor_classes", []):
        name = (cls.get("rtti") or {}).get("name")
        if name not in targets:
            continue
        reader = cls.get("slot19_reader") or {}
        checks = []
        refs = []
        for group in ("width_instructions", "stream_calls", "counted_loop_evidence"):
            entries = reader.get(group, [])
            if group == "counted_loop_evidence":
                entries = [entry.get("branch", {}) for entry in entries]
            for rec in entries:
                if not rec.get("file_offset") or not rec.get("bytes"):
                    continue
                off = int(rec["file_offset"], 16)
                expected = bytes.fromhex(rec["bytes"])
                actual = raw[off:off + len(expected)]
                va = pe.f2va(off)
                decoded = next(md.disasm(actual, va), None) if va is not None else None
                instruction = f"{decoded.mnemonic} {decoded.op_str}" if decoded else ""
                wanted = rec.get("instruction", "")
                checks.append({
                    "file_offset": rec["file_offset"],
                    "expected_bytes": rec["bytes"], "actual_bytes": actual.hex(" "),
                    "instruction_expected": wanted, "instruction_actual": instruction,
                    "bytes_match": actual == expected,
                    "instruction_match": normalize_instruction(instruction) ==
                                         normalize_instruction(wanted),
                })
        for function in reader.get("functions_scanned", []):
            start = int(function["file_offset"], 16)
            va = pe.f2va(start)
            if va is None:
                continue
            for ins in md.disasm(raw[start:start + 0x3000], va):
                if ins.mnemonic in branch_mnemonics or ins.mnemonic == "call":
                    target = None
                    if ins.operands and ins.operands[0].type == 2:
                        target_off = pe.va2f(ins.operands[0].imm)
                        target = hex(target_off) if target_off is not None else hex(ins.operands[0].imm)
                    off = pe.va2f(ins.address)
                    refs.append({"file_offset": hex(off) if off is not None else None,
                                 "instruction": f"{ins.mnemonic} {ins.op_str}",
                                 "target": target,
                                 "backward_branch": bool(target and off is not None and
                                     ins.mnemonic in branch_mnemonics and
                                     int(target, 16) <= off)})
                if ins.mnemonic in ("ret", "retf", "iret", "iretq", "int3", "jmp"):
                    break
        results.append({
            "class": targets[name], "rtti_name": name,
            "reader_mode": reader.get("mode"),
            "entry_file_offset": reader.get("entry_file_offset"),
            "unwrapped_file_offset": reader.get("unwrapped_file_offset"),
            "width_count_in_census": reader.get("width_count"),
            "stream_call_count_in_census": reader.get("stream_call_count"),
            "backedge_count_in_census": reader.get("backedge_count"),
            "instruction_check_count": len(checks),
            "instruction_checks_passed": sum(c["bytes_match"] and c["instruction_match"] for c in checks),
            "instruction_checks": checks,
            "call_and_branch_refs": refs[:300],
        })
    found = {result["class"] for result in results}
    if found != set(targets.values()):
        raise ValueError(f"expected both club RTTI readers, found {sorted(found)}")
    return {
        "editor_sha256": hashlib.sha256(raw).hexdigest(),
        "source_census_editor_sha256": item.get("editor_sha256"),
        "classes": results,
        "all_instruction_checks_pass": all(
            c["bytes_match"] and c["instruction_match"]
            for cls in results for c in cls["instruction_checks"]
        ),
        "interpretation_limit": (
            "Instruction bytes and local reader traces are rechecked. The source census does not "
            "establish a per-row RTTI discriminator or an executed path-to-row cursor."
        ),
    }


def make_fixture_row(ordinal: int) -> bytes:
    name = b"Test Club"
    short = b"Test"
    return (struct.pack("<4I", 7, 0xFFFFFFFF, 7, 7) + b"\x01\x02\x03\x04\x00" +
            struct.pack("<I", 2) + b"\x00" + struct.pack("<I", len(name)) + name +
            struct.pack("<I", len(short)) + short + b"\x00\x00\x00" +
            struct.pack("<III", ordinal, 12345, 12345) + b"\x00")


def selftest() -> int:
    row = make_fixture_row(0)
    parsed = parse_standard_row(row, 0, 0)
    assert parsed is not None
    assert parsed["length"] == 50 + len("Test Club") + len("Test")
    assert parsed["full_name"] == "Test Club" and parsed["short_name"] == "Test"
    assert parsed["ids"][0] == parsed["ids"][2]
    assert parse_standard_row(row, 0, 1) is None
    compact = b"\xff" * 42 + struct.pack("<III", 1, 77, 77) + b"\x0c"
    parsed_compact = find_compact_row(compact, 0, 1)
    assert parsed_compact["length"] == 55 and parsed_compact["marker"] == 12
    print("SELFTEST PASS")
    return 0


def build(output_dir: Path) -> dict[str, Any]:
    if not EDITOR.is_file() or not RTTI_CENSUS.is_file():
        raise FileNotFoundError("editor.exe or t01h RTTI census is missing")
    dump = import_script("_fm24_dump_t21", ROOT / "scripts/fm24_dump.py")
    payload = dump.load_payload(dump._reader(), "client", 3)
    rows = walk_club(payload)
    pe_mod = import_script("_t05_pe_t21", ROOT / "scripts/t05_pe.py")
    pe = pe_mod.PE(EDITOR)
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    static = verify_static_sources(pe, md, pe.raw, load_json(RTTI_CENSUS))
    if not static["all_instruction_checks_pass"]:
        raise ValueError("one or more editor.exe source instruction checks failed")
    row_audit = profile_rows(payload, rows)
    equal_0_8 = row_audit["fixed_word_relations"]["u32@0==u32@8"]
    result = {
        "task": "t21",
        "status": "partial_row_audit_complete_cursor_unreconciled",
        "scope": "read-only club table row walk and editor.exe reader evidence audit",
        "data_sha256": hashlib.sha256(payload).hexdigest(),
        "row_audit": row_audit,
        "static_reader_audit": static,
        "field_mapping_result": {
            "new_row_coordinate_mappings": 0,
            "Cccn_disposition": "do_not_promote; equality with row+0 quantified by independent row audit",
            "class_to_ordinal_discriminator": "unresolved",
            "compact_row_body_semantics": "unresolved for ordinals 69706..69708",
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    class_lines = []
    for cls in static["classes"]:
        class_lines.append(
            f"- `{cls['class']}`: reader `{cls['entry_file_offset']}` to "
            f"`{cls['unwrapped_file_offset']}`; source trace has "
            f"{cls['width_count_in_census']} width instructions, "
            f"{cls['stream_call_count_in_census']} stream calls and "
            f"{cls['backedge_count_in_census']} backedges; "
            f"fresh byte/instruction checks {cls['instruction_checks_passed']}/"
            f"{cls['instruction_check_count']} pass."
        )
    report = [
        "# t21 club cursor follow-up", "", "## Result", "",
        f"- Status: `{result['status']}`. This follow-up independently walks the local table and "
        "rechecks existing static reader evidence; it does not claim a complete serializer cursor.",
        f"- Row framing: {row_audit['row_count']} rows, {row_audit['standard_rows']} standard rows, "
        f"compact ordinals {row_audit['compact_rows']}; row end `{row_audit['row_end_offset']}` "
        f"matches footer `{row_audit['footer_offset']}`: `{row_audit['footer_exact']}`.",
        f"- u32 at row+0 equals u32 at row+8 in {equal_0_8}/{row_audit['row_count']} rows. "
        "This is counterevidence to treating row+8 as a distinct Cccn field without a stronger "
        "class-specific explanation; the field remains unpromoted.",
        "- New schema-to-row mappings: 0. The ordinal transition around 69,705 is data only, "
        "not an RTTI class discriminator.", "", "## Static Reader Recheck", "", *class_lines,
        "", "Static instruction checks confirm recorded bytes and disassembly at cited addresses. "
        "They do not prove which branch executes for each row or align either reader to the complete row cursor.",
        "", "## Remaining Blockers", "",
        "- Recover an independently supported per-row class selector or reconcile both class tracks against "
        "row bytes without assuming the contiguous ordinal split.",
        "- Resolve the mixed CLUB reader's conditional/helper paths and the separate LEAGUE_BODY_CLUB count-loop path.",
        "- Decode the three compact row bodies and preserve the exact footer closure.",
        "- Keep `Cccn@row+8` unpromoted until its duplicate-ID behavior is explained.",
        "", "## Inputs and Reproduction", "",
        "- Local decoded payload from `FM24_DB_DIR` via `scripts/fm24_dump.py`; read-only `editor.exe`; "
        "frozen `scratch/t01/inbox/t01h/output.json` trace.",
        "- Run `py -V:3.12 -I scripts/t21_club_cursor.py --help`, `--selftest`, then "
        "`FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I scripts/t21_club_cursor.py`.",
        "- No game, editor, IDA or network access is used.", "",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT,
                        help="write audit.json and REPORT.md here")
    parser.add_argument("--selftest", action="store_true", help="run parser helper assertions")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        result = build(args.output_dir)
    except (FileNotFoundError, ImportError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"status={result['status']}; rows={result['row_audit']['row_count']}; "
          f"footer_exact={result['row_audit']['footer_exact']}; "
          f"new_row_mappings={result['field_mapping_result']['new_row_coordinate_mappings']}; "
          f"output={args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
