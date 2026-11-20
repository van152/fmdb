#!/usr/bin/env python3
"""Independent t14 verification against editor.exe and frozen local artifacts.

Usage: py -V:3.12 -I scratch/t14/out/verify.py [--help|--selftest]
Read-only. Exit 0=pass, 1=verification failure, 2=usage/fatal error.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EDITOR = Path(r"<OLD_REPO>\input\editor.exe")
FM = Path(r"<OLD_REPO>\input\fm.exe")
JUMP_BASE = 0xF49D38
DEFAULT_HANDLER = 0xF49CA9
DEFAULT_TYPES = {11,13,15,16,17,20,28,40,53,54,55}
DEDICATED_TYPES = {0,1,2,3,4,5,6,7,8,9,10,12,14,18,19,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,50,51,52,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73}
KNOWN = {0:"AWARD",2:"CITY",8:"LANGUAGE",18:"DERBY",19:"REGION",23:"STAGE_NAME",27:"WEATHER",56:"AGREEMENT"}


class VerifyFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise VerifyFailure(message)


def load(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_hex(text: str) -> int:
    return int(text, 16)


def class_from_decorated(raw: bytes) -> str | None:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        return None
    if not text.startswith(".?AV"):
        return None
    if text.endswith("@db@@"):
        return text[4:-5]
    if text.endswith("@@"):
        return text[4:-2]
    return None


def cstring(raw: bytes, off: int, limit: int = 256) -> bytes:
    if off < 0 or off >= len(raw):
        return b""
    end = raw.find(b"\0", off, min(len(raw), off + limit))
    return raw[off:end if end >= 0 else min(len(raw), off + limit)]


def selftest() -> None:
    require(parse_hex("0xf49d38") + 4 * 73 == 0xF49E5C, "selftest: jump-table indexing")
    require(class_from_decorated(b".?AVDERBY@db@@") == "DERBY", "selftest: namespaced TD")
    require(class_from_decorated(b".?AVRGB_COLOUR@@") == "RGB_COLOUR", "selftest: namespace-free TD")
    require(len(DEDICATED_TYPES) == 63 and len(DEFAULT_TYPES) == 11, "selftest: type partition")


def import_local_modules():
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import t05_pe  # type: ignore[import-not-found]
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs  # type: ignore[import-not-found]
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return t05_pe, md


def disasm_at(pe, md, off: int, size: int = 0x80):
    va = pe.f2va(off)
    require(va is not None, f"file_off {off:#x} does not map to VA")
    return list(md.disasm(pe.raw[off:off + size], va))


def validate_assignment(pe, md, inst_off: int) -> int:
    insns = disasm_at(pe, md, inst_off, 0x40)
    require(insns and insns[0].mnemonic == "lea", f"{inst_off:#x}: declared vtable instruction is not LEA")
    lea = insns[0]
    require(len(lea.operands) == 2 and lea.operands[0].type == 1 and lea.operands[1].type == 3
            and lea.operands[1].mem.base == 41, f"{inst_off:#x}: not RIP-relative LEA")
    target = lea.address + lea.size + lea.operands[1].mem.disp
    reg = lea.operands[0].reg
    for nxt in insns[1:6]:
        if nxt.mnemonic == "mov" and len(nxt.operands) == 2:
            dst, src = nxt.operands
            if dst.type == 3 and src.type == 1 and src.reg == reg:
                return target
            if dst.type == 1 and src.type == 1 and src.reg == reg:
                reg = dst.reg
        if nxt.mnemonic == "jmp" and nxt.operands and nxt.operands[0].type == 2:
            helper_off = pe.va2f(nxt.operands[0].imm)
            require(helper_off is not None, f"{inst_off:#x}: tail assignment helper unmapped")
            helper_insns = disasm_at(pe, md, helper_off, 0x80)
            for helper in helper_insns[:6]:
                if helper.mnemonic == "mov" and len(helper.operands) == 2:
                    dst, src = helper.operands
                    if dst.type == 3 and src.type == 1 and src.reg == reg:
                        return target
            break
    raise VerifyFailure(f"{inst_off:#x}: LEA does not store its vtable register to object memory")


def verify_col(pe, vtable_va: int, declared_col_off: int, class_name: str) -> dict[str, Any]:
    vt_off = pe.va2f(vtable_va)
    require(vt_off is not None and vt_off >= 8, f"vtable VA {vtable_va:#x} unmapped")
    col_va = struct.unpack_from("<Q", pe.raw, vt_off - 8)[0]
    col_off = pe.va2f(col_va)
    require(col_off is not None, f"vtable {vtable_va:#x}: preceding COL VA unmapped")
    require(col_off == declared_col_off, f"COL file_off mismatch: {col_off:#x} != {declared_col_off:#x}")
    sig, obj_off, cd_off, td_rva, chd_rva = struct.unpack_from("<IIIII", pe.raw, col_off)
    require(sig == 1, f"COL {col_off:#x}: signature {sig}, expected 1")
    td_off = pe.r2f(td_rva)
    chd_off = pe.r2f(chd_rva)
    require(td_off is not None and chd_off is not None, f"COL {col_off:#x}: TD/CHD RVA unmapped")
    require(pe.f2va(col_off) == col_va and pe.f2r(td_off) == td_rva and pe.f2r(chd_off) == chd_rva,
            f"COL {col_off:#x}: PE RVA/file-offset self-check failed")
    decorated = cstring(pe.raw, td_off + 16)
    observed = class_from_decorated(decorated)
    require(observed == class_name, f"TD class mismatch at {td_off + 16:#x}: {observed!r} != {class_name!r}")
    chd_sig, chd_attr, chd_count = struct.unpack_from("<III", pe.raw, chd_off)
    require(chd_sig in (0,1) and chd_count <= 0x10000, f"CHD header implausible at {chd_off:#x}")
    return {"decorated":decorated.decode("ascii"),"td_off":td_off,"chd_off":chd_off,"col_va":col_va}


def fm_td_names() -> set[str]:
    require(FM.is_file(), f"missing read-only fm.exe: {FM}")
    t05_pe, _ = import_local_modules()
    pe = t05_pe.PE(FM)
    raw = pe.raw
    names: set[str] = set()
    for match in re.finditer(rb"\.\?AV[^\x00]{1,160}?(?:@db)?@@\x00", raw):
        td_off = match.start() - 16
        if td_off < 0 or pe.f2va(td_off) is None:
            continue
        vfptr = struct.unpack_from("<Q", raw, td_off)[0]
        if pe.va2f(vfptr) is None:
            continue
        name = class_from_decorated(raw[match.start():match.end()-1])
        if name:
            names.add(name)
    return names


def verify_all() -> list[str]:
    census = load(HERE / "census.json")
    stage2 = load(HERE / "stage2_map.json")
    jump_anchor = load(ROOT / "scratch/t01/t01h_jump_table_anchor.json")
    require(census.get("status") == "complete", "census.json is not complete")
    require(set(jump_anchor.get("dedicated_types", [])) == DEDICATED_TYPES, "t01h dedicated type set changed")
    require(set(jump_anchor.get("default_types", [])) == DEFAULT_TYPES, "t01h default type set changed")
    tables = census.get("tables", [])
    require(len(tables) == 74 and {x.get("table_type") for x in tables} == set(range(74)),
            "census does not cover all type IDs 0..73 exactly once")
    by_id = {x["table_type"]: x for x in tables}

    t05_pe, md = import_local_modules()
    pe = t05_pe.PE(EDITOR)
    targets: dict[int, int] = {}
    for tid in range(74):
        rel = struct.unpack_from("<i", pe.raw, JUMP_BASE + 4 * tid)[0]
        targets[tid] = JUMP_BASE + rel
        declared = parse_hex(by_id[tid]["handler_off"])
        require(targets[tid] == declared, f"type {tid}: jump-table target {targets[tid]:#x} != census {declared:#x}")
    require(targets[10] == 0xF48F27 and targets[25] == 0xF49129, "factory negative controls mismatch")
    require(all(targets[t] == DEFAULT_HANDLER for t in (53,54,55)), "default handler slots 53..55 mismatch")

    fm_names = fm_td_names()
    checked_d = 0
    for tid in sorted(DEDICATED_TYPES):
        row = by_id[tid]
        require(row.get("status") == "dedicated", f"type {tid}: not marked dedicated")
        hits = row.get("vtables", [])
        # User requires each dedicated type be named or explicitly negative.
        require(bool(hits) or (row.get("adjudication") == "negative" and row.get("negative_reason")),
                f"type {tid}: neither RTTI class nor explicit negative trace")
        for hit in hits:
            inst_off = parse_hex(hit["inst_off"])
            vtable_va = parse_hex(hit["vtable_va"])
            col_off = parse_hex(hit["col_off"])
            actual_vtable = validate_assignment(pe, md, inst_off)
            require(actual_vtable == vtable_va,
                    f"type {tid} at {inst_off:#x}: LEA points to {actual_vtable:#x}, not declared {vtable_va:#x}")
            details = verify_col(pe, vtable_va, col_off, hit["class"])
            require(hit.get("fm_cross") == "td-only", f"type {tid}: fm.exe TD cross status is not td-only")
            require(hit["class"] in fm_names, f"type {tid}: editor class {hit['class']} missing from fm.exe TD names")
            checked_d += 1

    for tid, expected in KNOWN.items():
        classes = {x["class"] for x in by_id[tid].get("vtables", [])}
        require(expected in classes, f"known entity cross-check type {tid}: expected {expected}, saw {sorted(classes)}")

    server = stage2.get("tables", [])
    require(len(server) == 59 and all(r.get("archive") == "server" for r in server),
            "stage2_map must use the 59 server rows from COVERAGE")
    stage2_by_id = {r["table_type"]: r for r in server}
    require(len(stage2_by_id) == 59, "stage2_map duplicate type IDs")
    resolved = sum(r.get("status") == "resolved" for r in server)
    require(resolved >= 45, f"stage2 resolved {resolved}/59, need >=45")
    for tid in (52,57):
        require(stage2_by_id[tid].get("status") == "empty" and stage2_by_id[tid].get("count") == 0,
                f"type {tid}: empty table was not preserved")

    t13 = load(ROOT / "scratch/t13/out/anchors.json")
    t13_by_id = {x["table_type"]: x for x in t13.get("tables", [])}
    for r in server:
        tid = r["table_type"]
        require(r.get("status") in {"resolved", "candidate", "negative", "empty"},
                f"type {tid}: invalid stage2 status")
        if r["status"] == "resolved":
            require(bool(r.get("entity")), f"type {tid}: resolved row has no entity")
            kinds = {e.get("kind") for e in r.get("evidence", [])}
            require(bool(kinds & {"A", "B", "D"}), f"type {tid}: resolved without A/B/D evidence")
        if r["status"] == "empty":
            require(r.get("count") == 0 and r.get("entity") is None,
                    f"type {tid}: malformed empty row")
        if tid in {26,29,32,36,38,39}:
            old = t13_by_id.get(tid, {})
            retained = [c for c in r.get("conflicts", [])
                        if c.get("source") == "scratch/t13/out/anchors.json" and "original" in c]
            require(bool(retained), f"type {tid}: historical negative was not retained")
            require(retained[0]["original"].get("why_unresolved") == old.get("why_unresolved"),
                    f"type {tid}: original t13 negative text changed")
        for evidence in r.get("evidence", []):
            if evidence.get("kind") != "D":
                continue
            details = evidence.get("details", {})
            require(details.get("independence"), f"type {tid}: D evidence lacks independence rationale")
            require(details.get("handler_off") == by_id[tid].get("handler_off"),
                    f"type {tid}: D handler_off does not match census")
            match = [v for v in by_id[tid].get("vtables", [])
                     if v.get("inst_off") == details.get("inst_off")
                     and v.get("vtable_va") == details.get("vtable_va")
                     and v.get("col_off") == details.get("col_off")
                     and v.get("class") == details.get("class_name")]
            require(bool(match), f"type {tid}: D evidence is not present in census")

    return [f"jump-table entries: 74/74 (63 dedicated, 11 default)",
            f"RTTI D chains independently decoded: {checked_d}; all COL/TD/CHD self-checks passed",
            f"fm.exe TD string cross-checks: {checked_d}/{checked_d} (TD-only; no vtable claim)",
            f"known entity cross-checks: {len(KNOWN)}/8, zero contradiction",
            f"stage2_map: {resolved}/59 resolved; types 52/57 empty"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently verify t14 RTTI anchors and stage2 map against local exes/artifacts.")
    parser.add_argument("--selftest", action="store_true", help="run offline verifier self-tests")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
            print("SELFTEST PASS")
            return 0
        messages = verify_all()
        print("VERIFY PASS")
        for message in messages:
            print(message)
        return 0
    except VerifyFailure as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, struct.error) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
