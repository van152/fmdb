#!/usr/bin/env python3
"""Read-only t01-g nation serializer reconnaissance and evidence self-test.

From the repository root:
  py -V:3.12 -I -B scratch/t01/inbox/t01g/verify.py --help
  py -V:3.12 -I -B scratch/t01/inbox/t01g/verify.py --write
  py -V:3.12 -I -B scratch/t01/inbox/t01g/verify.py --selftest

Only --write creates/replaces the colocated output.json. PE, snapshots and
client_db.dat are opened read-only; no PE is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mmap
import runpy
import struct
import sys
from contextlib import ExitStack
from pathlib import Path

try:
    import capstone
except ImportError as exc:  # pragma: no cover - environment diagnostic
    raise SystemExit(f"capstone unavailable; do not install dependencies for this task: {exc}")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = ROOT.parent / "fm24"
DEFAULT_DB = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
EXPECTED_PE = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXPECTED_ARCHIVE = "5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1"
EXPECTED_PAYLOAD = "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34"
SNAPSHOT_FILES = (
    "evidence/fm24/reports/editor_schema/master.json",
    "evidence/fm24/reports/dbdat_decode/client_table_10_nation_locator.json",
    "evidence/fm24/reports/qa/IDA_PROVENANCE.md",
)

# File offsets; all instructions below are in editor.exe. .rdata/.debug VA mapping
# is derived from PE headers rather than assumed in the emitted evidence.
NATION_NAME_OFF = 0x1AACAC0
NATION_VPTR_OFF = 0x18889B8
NATION_CTOR_OFF = 0x103EBF0
FACTORY_SWITCH_INSN = 0xF48B45
FACTORY_TYPE10_OFF = 0xF48F27
GETTER_START_OFF = 0x1041F30
GETTER_SCAN_LO = 0x1041930
GETTER_SCAN_HI = 0x1045300
READER_OFF = 0x103FAC0
WRITER_OFF = 0x1041460

# (code, field member offset, row-body cursor offset, width, reader destination,
#  reader mov-r8d, reader stream-vcall, getter compare, getter member access,
#  compare edge kind, member access offset).
LINKS = (
    ("Ngct", 0x1CB, 0, 1, 0x10405B4, 0x10405BE, 0x10405C7, 0x1042385, 0x1042A47, "je", 0x1CB),
    ("Ncti", 0x0F0, 1, 4, 0x10405D8, 0x10405E2, 0x10405EB, 0x104218A, 0x1042ED7, "je", 0x0F0),
    ("Nrgi", 0x0F8, 5, 4, 0x10405FC, 0x1040606, 0x104060F, 0x10424E5, 0x10424F1, "jne-fallthrough", 0x0F8),
    ("Ncur", 0x100, 13, 4, 0x1040644, 0x104064E, 0x1040657, 0x1042196, 0x1042C7D, "je", 0x100),
    ("Nsod", 0x1CC, 17, 1, 0x1040668, 0x1040672, 0x104067B, 0x1042268, 0x1042E6F, "je", 0x1CC),
    ("Necf", 0x1D0, 18, 1, 0x104068C, 0x1040696, 0x104069F, 0x10421A2, 0x10421AE, "jne-fallthrough", 0x1D0),
    ("Nygn", 0x1CD, 23, 1, 0x10406D4, 0x10406DE, 0x10406E7, 0x1042078, 0x1042AAF, "je", 0x1CD),
)

# Early serializer operations not yet linked to a schema field are intentionally
# retained as opaque rather than assigned a guessed meaning.
PREFIX_IO = (
    (0, 1, 0x1CB, 0x10405B4, 0x10405BE, 0x10405C7, "Ngct"),
    (1, 4, 0x0F0, 0x10405D8, 0x10405E2, 0x10405EB, "Ncti"),
    (5, 4, 0x0F8, 0x10405FC, 0x1040606, 0x104060F, "Nrgi"),
    (9, 4, 0x0E8, 0x1040620, 0x104062A, 0x1040633, None),
    (13, 4, 0x100, 0x1040644, 0x104064E, 0x1040657, "Ncur"),
    (17, 1, 0x1CC, 0x1040668, 0x1040672, 0x104067B, "Nsod"),
    (18, 1, 0x1D0, 0x104068C, 0x1040696, 0x104069F, "Necf"),
    (19, 4, 0x1B4, 0x10406B0, 0x10406BA, 0x10406C3, None),
    (23, 1, 0x1CD, 0x10406D4, 0x10406DE, 0x10406E7, "Nygn"),
    (24, 1, None, 0x1040709, 0x104070E, 0x1040717, None),
)

class Failure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def u(data: bytes | mmap.mmap, off: int, n: int = 4, signed: bool = False) -> int:
    return int.from_bytes(data[off:off + n], "little", signed=signed)


class PE:
    def __init__(self, path: Path, stack: ExitStack):
        self.path = path
        f = stack.enter_context(path.open("rb"))
        self.data = stack.enter_context(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))
        digest = hashlib.sha256(self.data).hexdigest()
        require(digest == EXPECTED_PE, "editor.exe SHA-256 differs from frozen IDA provenance")
        self.source = {"file": path.as_posix(), "bytes": len(self.data), "sha256": digest}
        pe = u(self.data, 0x3C)
        require(self.data[pe:pe + 6] == b"PE\0\0\x64\x86", "not an x64 PE")
        opt = pe + 24
        require(u(self.data, opt, 2) == 0x20B, "not PE32+")
        self.base = u(self.data, opt + 24, 8)
        section_table = opt + u(self.data, pe + 20, 2)
        self.sections = []
        for pos in range(section_table, section_table + u(self.data, pe + 6, 2) * 40, 40):
            name = self.data[pos:pos + 8].rstrip(b"\0").decode("ascii", errors="replace")
            virtual_size, rva, raw_size, raw = struct.unpack_from("<IIII", self.data, pos + 8)
            self.sections.append((name, rva, virtual_size, raw, raw_size))
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True

    def va(self, off: int) -> int:
        for _, rva, _, raw, raw_size in self.sections:
            if raw <= off < raw + raw_size:
                return self.base + rva + off - raw
        raise Failure(f"editor.exe file offset unmapped: {off:#x}")

    def off(self, va: int) -> int:
        for _, rva, _, raw, raw_size in self.sections:
            delta = va - (self.base + rva)
            if 0 <= delta < raw_size:
                return raw + delta
        raise Failure(f"editor.exe VA has no file bytes: {va:#x}")

    def ev(self, off: int, n: int | None = None, exact: str | None = None):
        expected = bytes.fromhex(exact) if exact is not None else None
        if expected is not None:
            n = len(expected)
        require(n is not None and n > 0, "empty evidence span")
        actual = bytes(self.data[off:off + n])
        require(len(actual) == n and (expected is None or actual == expected),
                f"editor.exe@{off:#x}: unexpected bytes {actual.hex(' ')}")
        return {"file": "editor.exe", "file_offset": hex(off), "va": hex(self.va(off)), "bytes": actual.hex(" ")}

    def ins(self, off: int):
        i = next(self.md.disasm(self.data[off:off + 15], self.va(off), 1), None)
        require(i is not None, f"editor.exe@{off:#x}: invalid instruction")
        return i

    def op(self, off: int, expected: str | None = None):
        i = self.ins(off)
        text = (i.mnemonic + " " + i.op_str).strip()
        require(expected is None or text == expected,
                f"editor.exe@{off:#x}: {text!r}, expected {expected!r}")
        return {**self.ev(off, i.size), "instruction": text}

    def rip_target(self, off: int) -> int:
        i = self.ins(off)
        ops = [x for x in i.operands if x.type == capstone.x86.X86_OP_MEM and x.mem.base == capstone.x86.X86_REG_RIP]
        require(len(ops) == 1, f"editor.exe@{off:#x}: no unique RIP-relative operand")
        return i.address + i.size + ops[0].mem.disp

    def rel_target(self, off: int) -> int:
        i = self.ins(off)
        require(i.mnemonic in ("call", "jmp", "je", "jne", "jge"), f"editor.exe@{off:#x}: not a relative edge")
        return i.operands[0].imm


def manifest_hashes(root: Path):
    manifest = read_json(root / "evidence/MANIFEST.json")
    expected = {x["path"]: x["sha256"] for x in manifest["files"]}
    checked = {}
    for rel in SNAPSHOT_FILES:
        got = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        require(got == expected.get(rel), "frozen snapshot mismatch: " + rel)
        checked[rel] = got
    return checked


def scan_getter_cases(p: PE, fields: list[dict]):
    found = []
    for field in fields:
        code = field["field"]
        if not isinstance(code, str) or len(code) != 4 or not code.isascii():
            continue
        pattern = b"\x81\xfe" + struct.pack("<I", int.from_bytes(code.encode("ascii"), "big"))
        pos = GETTER_SCAN_LO
        while True:
            pos = p.data.find(pattern, pos, GETTER_SCAN_HI)
            if pos < 0:
                break
            cmp = p.ins(pos)
            if cmp.mnemonic == "cmp" and cmp.reg_name(cmp.operands[0].reg) == "esi" and cmp.operands[1].imm == int.from_bytes(code.encode("ascii"), "big"):
                edge = p.ins(pos + cmp.size)
                if edge.mnemonic in ("je", "jne"):
                    found.append({"code": code, "compare_off": pos, "edge_off": pos + cmp.size,
                                  "edge": edge.mnemonic, "edge_target_file_offset": hex(p.off(edge.operands[0].imm)),
                                  "case_entry_file_offset": hex(p.off(edge.operands[0].imm) if edge.mnemonic == "je" else pos + cmp.size + edge.size)})
            pos += 1
    # Match one first occurrence per schema code; this window has no duplicate valid labels.
    unique = {}
    for item in sorted(found, key=lambda x: x["compare_off"]):
        unique.setdefault(item["code"], item)
    return unique


def linked_case(p: PE, entry):
    code, obj_off, row_off, width, dst, size_at, call, cmp_off, member_off, edge_kind, disp = entry
    cmp_ins = p.ins(cmp_off)
    edge_off = cmp_off + cmp_ins.size
    edge_ins = p.ins(edge_off)
    require(cmp_ins.mnemonic == "cmp" and cmp_ins.operands[1].imm == int.from_bytes(code.encode("ascii"), "big"), code + " compare")
    if edge_kind == "je":
        require(edge_ins.mnemonic == "je" and p.off(edge_ins.operands[0].imm) == member_off,
                code + " equality target")
    else:
        require(edge_ins.mnemonic == "jne" and edge_off + edge_ins.size == member_off,
                code + " equality fallthrough")
    access = p.ins(member_off)
    mems = [x for x in access.operands if x.type == capstone.x86.X86_OP_MEM and access.reg_name(x.mem.base) == "r12"]
    require(mems and mems[0].mem.disp == disp, code + " object member displacement")
    item = next(x for x in PREFIX_IO if x[0] == row_off and x[1] == width and x[2] == obj_off and x[6] == code)
    _, _, _, dest_off, width_off, call_off, _ = item
    require((dest_off, width_off, call_off) == (dst, size_at, call), code + " cursor link")
    name = code
    if code == "Ngct": human = "Gain Nationality Type"
    elif code == "Ncti": human = "Continent"
    elif code == "Nrgi": human = "Region"
    elif code == "Ncur": human = "Currency"
    elif code == "Nsod": human = "State Of Development"
    elif code == "Necf": human = "Economic Factor"
    else: human = "Years To Gain Nationality"
    return {
        "code": code, "schema_name": human, "row_offset": row_off, "width": width,
        "object_offset": hex(obj_off), "evidence_level": "L3 instruction chain + L1 prefix spot-check",
        "serializer": {"destination": p.op(dst), "width_instruction": p.op(size_at, f"mov r8d, {width}"),
                       "stream_vcall": p.op(call, "call qword ptr [rax + 0x28]")},
        "field_getter_link": {"compare": p.op(cmp_off), "branch": p.op(edge_off),
                              "edge_semantics": "equality target" if edge_kind == "je" else "equality falls through; jne is default edge",
                              "member_access": p.op(member_off)},
    }


def source_table10(db_dir: Path):
    library = runpy.run_path(str(OLD / "scripts/modding_read_dbdat.py"))
    archive_path, blob, layout = library["_entries"](db_dir, "client_db.dat")
    entry = next(x for x in layout["entries"] if x["path"] == "client_db/table_10.dat")
    start = layout["data_base"] + entry["offset"]
    require(hashlib.sha256(blob).hexdigest() == EXPECTED_ARCHIVE, "client_db.dat SHA-256 mismatch")
    require(blob[start:start + 4] == bytes.fromhex("28 b5 2f fd"), "table_10 member is not Zstd")
    raw = library["_decompress_entry"](blob, layout["data_base"], entry)
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_PAYLOAD, "table_10 payload SHA-256 mismatch")
    require(len(raw) == 24732 and u(raw, 6, 2) == 3569 and u(raw, 8) == 251, "table_10 version/count/size mismatch")
    return archive_path, blob, layout, entry, start, raw


def build(db_dir: Path):
    hashes = manifest_hashes(ROOT)
    master_path = ROOT / SNAPSHOT_FILES[0]
    master = read_json(master_path)
    nation_entry = next(x for x in master["entities"]["nation.xml"] if x.get("id") == "nati")
    nation_fields = nation_entry["fields"]
    schema_codes = {x["field"] for x in nation_fields}
    require(len(nation_fields) == 346 and len(schema_codes) == 346, "master nation schema is not 346 distinct codes")
    locator = read_json(ROOT / SNAPSHOT_FILES[1])
    require(locator["table_id"] == 10 and locator["record_count"] == 251, "frozen table_10 locator facts mismatch")
    archive_path, blob, layout, entry, compressed_start, raw = source_table10(db_dir)
    prefix = bytes.fromhex("01 00 00 00 00 07 00 00 00 a3 04 00 00 01 00 00 00 02 0d 00 00 00 00 07 03")
    require(raw[14:14 + len(prefix)] == prefix, "table_10 initial payload prefix differs")

    with ExitStack() as stack:
        p = PE(OLD / "input/editor.exe", stack)
        # RTTI -> COL -> type descriptor -> name.
        col_va = u(p.data, NATION_VPTR_OFF - 8, 8)
        col_off = p.off(col_va)
        col = struct.unpack_from("<6I", p.data, col_off)
        require(col[0:3] == (1, 0, 0), "nation complete-object-locator header")
        type_descriptor_off = p.off(p.base + col[3])
        name_off = type_descriptor_off + 16
        require(name_off == NATION_NAME_OFF, "nation RTTI name does not match COL")
        require(bytes(p.data[name_off:name_off + 16]) == b".?AVNATION@db@@\0", "nation RTTI name mismatch")
        require(p.rip_target(0x103EC17) == p.va(NATION_VPTR_OFF), "nation constructor vptr target")
        require(p.off(p.rel_target(0xF48F37)) == NATION_CTOR_OFF, "type-10 factory does not call nation constructor")

        table_va = p.rip_target(FACTORY_SWITCH_INSN)
        table_off = p.off(table_va)
        type10_entry = table_off + 10 * 4
        type25_entry = table_off + 25 * 4
        type10_target = p.off(table_va + u(p.data, type10_entry, 4, signed=True))
        type25_target = p.off(table_va + u(p.data, type25_entry, 4, signed=True))
        require(type10_target == FACTORY_TYPE10_OFF and type25_target == 0xF49129 and type10_target != type25_target,
                "factory type-10/type-25 switch entries")
        vtable_query_off = p.off(u(p.data, NATION_VPTR_OFF + 7 * 8, 8))
        require(p.data[vtable_query_off:vtable_query_off + 6] == bytes.fromhex("b8 0a 00 00 00 c3"), "nation slot-7 query does not return type 10")
        reader_ptr_off = p.off(u(p.data, NATION_VPTR_OFF + 19 * 8, 8))
        writer_ptr_off = p.off(u(p.data, NATION_VPTR_OFF + 21 * 8, 8))
        require((reader_ptr_off, writer_ptr_off) == (READER_OFF, WRITER_OFF), "nation slot 19/21 targets")

        # The first ordinary reader path has ten transfers (nine object fields + one scratch byte).
        cursor_layout = []
        for row_off, width, obj_off, dst_off, width_off, call_off, code in PREFIX_IO:
            dest = p.ins(dst_off)
            require(dest.mnemonic == "lea", f"destination instruction at {dst_off:#x}")
            if obj_off is not None:
                require(any(x.type == capstone.x86.X86_OP_MEM and dest.reg_name(x.mem.base) == "r15" and x.mem.disp == obj_off for x in dest.operands),
                        f"reader object displacement at {dst_off:#x}")
            else:
                require("rsp + 0x44" in dest.op_str, "scratch-byte destination")
            p.op(width_off, f"mov r8d, {width}")
            p.op(call_off, "call qword ptr [rax + 0x28]")
            sample_off = 14 + row_off
            item = {"step": code or f"opaque_{obj_off:x}" if obj_off is not None else "scratch_byte",
                    "row_offset_in_body": row_off, "width": width,
                    "object_offset": hex(obj_off) if obj_off is not None else None,
                    "reader": {"destination": p.op(dst_off), "width_instruction": p.op(width_off), "stream_vcall": p.op(call_off)},
                    "client_payload_prefix_spotcheck": {"payload_offset": hex(sample_off),
                        "bytes": raw[sample_off:sample_off + width].hex(" "), "value_le": u(raw, sample_off, width)}}
            cursor_layout.append(item)
        # This is a prefix correspondence, not a recovered 251-row parser.
        require(sum(x[1] for x in PREFIX_IO) == 25, "prefix cursor width")

        links = {x[0]: linked_case(p, x) for x in LINKS}
        getter_cases = scan_getter_cases(p, nation_fields)
        require(len(getter_cases) == 19, f"nation slot-2 getter scan case count changed: {len(getter_cases)}")
        require(set(links).issubset(getter_cases), "a mapped property is absent from the getter switch scan")

        # Read-only frozen sample: raw_byte_offset points at the duni pair, not at
        # the beginning of context_hex and is not a recovered row start.
        loc = locator["raw_byte_offset"]
        context = bytes.fromhex(locator["context_hex"])
        context_off = loc - 12
        require(raw[loc:loc + 8] == bytes.fromhex(locator["duni_little_endian_hex"]), "nation duni locator bytes")
        require(raw[context_off:context_off + len(context)] == context, "nation locator context mismatch")
        require(u(raw, loc, 8) == locator["lookup_db_unique_id"], "nation duni numeric anchor")

        # Dynamic mode/collection proof: arg8 selects a second path, and that path
        # reads a 16-bit count then loops over 4-byte elements.
        branch_off = 0x103FAE6
        branch_target = p.off(p.rel_target(branch_off))
        require(branch_target == 0x10405B0, "nation reader arg8==0 branch target")
        require(p.op(0x103FB2E, "mov r8d, 2") and p.op(0x103FB37, "call qword ptr [rax + 0x28]"), "nation count read")
        require(p.op(0x103FCB1, "mov r8d, 4") and p.op(0x103FCBD, "call qword ptr [rax + 0x28]"), "nation vector element read")
        require(p.ins(0x103FC98).mnemonic == "cmp" and p.ins(0x103FC9B).mnemonic == "jge", "nation vector loop edge")
        ordinary_list = {
            "count_source": p.op(0x1040728, "movsx rdx, byte ptr [rsp + 0x44]"),
            "helper_call": p.op(0x1040731, "call 0x1410418b0"),
            "count_test": p.op(0x1040736, "cmp byte ptr [rsp + 0x44], 0"),
            "empty_list_edge": p.op(0x104073B),
            "per_item_helper": p.op(0x104075B, "call 0x141060550"),
            "per_item_append": p.op(0x104076E, "call 0x1408c9770"),
            "loop_increment": p.op(0x1040773, "inc bl"),
            "loop_compare": p.op(0x1040775, "cmp bl, byte ptr [rsp + 0x44]"),
            "loop_back_edge": p.op(0x1040779),
            "payload_count_sample": {"payload_offset": "0x26", "bytes": raw[14 + 24:15 + 24].hex(" "), "value": raw[14 + 24]},
            "next_dword_count_width": p.op(0x10407A7, "mov r8d, 4"),
            "next_dword_count_call": p.op(0x10407B0, "call qword ptr [rax + 0x28]"),
            "next_dword_loop_test": p.op(0x10407D1, "cmp dword ptr [rsp + 0x70], 0"),
            "next_dword_loop_empty_edge": p.op(0x10407D6),
            "next_dword_loop_increment": p.op(0x1040841, "inc ebx"),
            "next_dword_loop_compare": p.op(0x1040843, "cmp ebx, dword ptr [rsp + 0x70]"),
            "next_dword_loop_back_edge": p.op(0x1040847),
        }

        out = {
            "task": "t01-g",
            "acceptance": {
                "met": True,
                "outcome": "negative_result_entity_serializer_differs_from_COMP",
                "l3_named_client_prefix_fields": len(links),
                "required_ten_field_mapping": False,
                "negative_result_proven": True,
                "nation_schema_fields": len(nation_fields),
                "plain_4cc_cases_in_nation_slot2_getter_window": len(getter_cases),
                "three_row_field_value_crosscheck": False,
                "L4": 0,
            },
            "sources": {
                "binary": [p.source],
                "verified_frozen_snapshots": hashes,
                "client_table_10": {
                    "archive_path": archive_path.as_posix(), "archive_sha256": hashlib.sha256(blob).hexdigest(),
                    "archive_member": entry["path"], "compressed_file_offset": hex(compressed_start),
                    "compressed_size": entry["packed_size"], "compressed_magic": blob[compressed_start:compressed_start + 4].hex(" "),
                    "payload_size": len(raw), "payload_sha256": hashlib.sha256(raw).hexdigest(),
                    "payload_version": u(raw, 6, 2), "record_count": u(raw, 8),
                    "payload_offset_domain": "Offsets in the decompressed client_db/table_10.dat member; not archive file offsets.",
                    "decoder": (OLD / "scripts/modding_read_dbdat.py").as_posix(),
                },
                "python": "py -V:3.12 -I -B", "capstone": capstone.__version__,
                "read_only": True,
            },
            "nation_record": {
                "rtti": {
                    "name": p.ev(name_off, exact="2e 3f 41 56 4e 41 54 49 4f 4e 40 64 62 40 40 00"),
                    "vptr_file_offset": hex(NATION_VPTR_OFF), "vptr_va": hex(p.va(NATION_VPTR_OFF)),
                    "vptr_minus_8_col_pointer": p.ev(NATION_VPTR_OFF - 8, 8),
                    "complete_object_locator": p.ev(col_off, 24),
                    "type_descriptor_name_file_offset": hex(name_off),
                },
                "factory_type10": {
                    "switch_base": p.op(FACTORY_SWITCH_INSN), "switch_table_file_offset": hex(table_off),
                    "type10_entry": p.ev(type10_entry, 4), "type10_target_file_offset": hex(type10_target),
                    "allocation_size_argument": p.ev(FACTORY_TYPE10_OFF, exact="b9 d8 01 00 00"),
                    "constructor_call": p.op(0xF48F37), "constructor_file_offset": hex(NATION_CTOR_OFF),
                    "constructor_vptr_lea": p.op(0x103EC17), "constructor_vptr_store": p.op(0x103EC1E),
                    "constructor_vptr_target": hex(p.off(p.rip_target(0x103EC17))),
                    "slot7_type_query_pointer": p.ev(NATION_VPTR_OFF + 7 * 8, 8),
                    "slot7_type_query_return_10": p.ev(vtable_query_off, exact="b8 0a 00 00 00 c3"),
                    "size_note": "Factory allocation request is 0x1d8 bytes; reported as allocator size, not compiler debug sizeof metadata.",
                    "type25_negative_control_entry": p.ev(type25_entry, 4),
                    "type25_target_file_offset": hex(type25_target),
                },
                "vtable": {
                    "base_file_offset": hex(NATION_VPTR_OFF),
                    "slot19_reader_pointer": p.ev(NATION_VPTR_OFF + 19 * 8, 8),
                    "slot19_reader_entry": p.ev(READER_OFF, 24),
                    "slot21_writer_pointer": p.ev(NATION_VPTR_OFF + 21 * 8, 8),
                    "slot21_writer_entry": p.ev(WRITER_OFF, 24),
                    "indices_are_zero_based": True,
                },
            },
            "row_offset_map": links,
            "row_codec": {
                "scope": "Partial prefix only. Reader cursor starts after the common framing/header bytes; no complete variable-row parser is claimed.",
                "reader_arg8_branch": {"argument_load": p.op(0x103FADC), "test": p.op(0x103FAE4),
                    "zero_path_edge": p.op(branch_off), "zero_path_target_file_offset": hex(branch_target),
                    "zero_path_first_transfer": p.op(0x10405C7)},
                "writer_prefix_crosscheck": {
                    "prelude_zero_byte": p.op(0x1041478, "mov byte ptr [rsp + 0x20], 0"),
                    "prelude_width": p.op(0x1041485, "mov r8d, 1"),
                    "prelude_stream_vcall": p.op(0x104148E, "call qword ptr [rax + 0x28]"),
                    "zero_mode_test": p.op(0x10414A6, "test r15b, r15b"),
                    "zero_mode_edge": p.op(0x10414A9),
                    "first_body_member": p.op(0x1041832), "first_width": p.op(0x104183C),
                    "first_stream_vcall": p.op(0x1041845),
                    "note": "Writer emits a separate one-byte prelude before the normal body; the table payload's 14-byte framing is not treated as a fixed row stride.",
                },
                "cursor_layout": cursor_layout,
                "variable_collection_path": {
                    "count_width_instruction": p.op(0x103FB2E), "count_stream_vcall": p.op(0x103FB37),
                    "element_width_instruction": p.op(0x103FCB1), "element_stream_vcall": p.op(0x103FCBD),
                    "loop_increment": p.op(0x103FC90), "loop_compare": p.op(0x103FC98),
                    "loop_exit": p.op(0x103FC9B),
                    "interpretation": "arg8!=0 path: conditional 16-bit count followed by a loop of 4-byte transfers; do not assign this path to client/server without caller evidence.",
                },
                "ordinary_path_counted_collections": ordinary_list,
            },
            "switch_extraction": {
                "method": "Nation record vtable slot 2 getter; separate from the COMP switch regions in t01b.",
                "getter_entry_file_offset": hex(GETTER_START_OFF),
                "scan_file_offset_range": [hex(GETTER_SCAN_LO), hex(GETTER_SCAN_HI)],
                "schema_field_count": len(nation_fields), "unique_plain_cmp_4cc_cases_found": len(getter_cases),
                "case_codes": sorted(getter_cases),
                "mapped_prefix_cases": {k: v["field_getter_link"] for k, v in links.items()},
                "coverage_note": "Only exact cmp esi,imm32 labels in this getter window are counted. This is not a claim that the other schema codes are absent from all executable paths.",
            },
            "data_anchor": {
                "snapshot_locator": locator,
                "raw_byte_offset_is_duni_start": True,
                "duni_payload_evidence": {"payload_offset": hex(loc), "bytes": raw[loc:loc + 8].hex(" "),
                    "uint64_le": u(raw, loc, 8), "preceding_u32_unassigned": {"payload_offset": hex(loc - 4),
                    "bytes": raw[loc - 4:loc].hex(" "), "value": u(raw, loc - 4)}},
                "context": {"payload_offset": hex(context_off), "bytes": raw[context_off:context_off + len(context)].hex(" ")},
                "prefix_spotcheck": {"payload_offset": "0xe", "bytes": raw[14:39].hex(" "),
                    "status": "Matches the first 25-byte serializer cursor prefix; record boundary/index has not been independently recovered."},
            },
            "negative_result": {
                "claim": "Nation's serializer is not demonstrated to be COMP's unconditional fixed-order scalar stream.",
                "evidence": [
                    "slot-19 reader tests arg8 and branches around a separate path",
                    "even arg8==0 path uses the row+24 byte as a loop count, then later reads a dword count and loops; the alternate path has another 16-bit-count/4-byte-element loop",
                    "the writer emits a separate one-byte prelude before the ordinary body",
                    "only 7 of the initial 10 transfers currently have a schema 4CC-to-member link; two object slots and one scratch byte remain opaque",
                ],
                "unproven": [
                    "full client row boundaries and all 251 row starts",
                    "three-or-more-row value checks for each named field",
                    "the meanings of object+0xe8 and object+0x1b4 in the initial prefix",
                    "full mapping of 346 master codes to object and row offsets",
                ],
            },
            "falsified_or_rejected": [
                {"hypothesis": "COMP's 0xEC0000/0xECA000 4CC windows directly cover nation", "result": "not used as nation evidence; nation slot-2 getter is in a separate class-specific code window", "evidence": "switch_extraction"},
                {"hypothesis": "helperB()+0x38 supplies nation row offsets", "result": "not tested or reused; row offsets here come from slot-19 stream widths", "evidence": "row_codec.cursor_layout"},
                {"hypothesis": "the dword preceding the frozen duni sample is verified rdui/row index", "result": "kept unassigned; snapshot only establishes the repeated-u32 duni bytes at payload offset 4166", "evidence": "data_anchor"},
            ],
            "verification": {"payload_header": phex(raw[:14]), "table10_rows": u(raw, 8),
                "checked_prefix_bytes": len(prefix), "checked_mapped_field_links": len(links),
                "complete_rows_verified": 0, "negative_controls": "run with --selftest"},
        }
        return out


def phex(data: bytes) -> str:
    return data.hex(" ")


def reject(label: str, action):
    try:
        action()
    except Failure:
        return
    raise Failure("negative control accepted: " + label)


def selftest(out):
    require(out["acceptance"]["negative_result_proven"], "negative-result evidence absent")
    require(out["acceptance"]["l3_named_client_prefix_fields"] == 7, "field-count guard")
    require(out["row_codec"]["cursor_layout"][0]["row_offset_in_body"] == 0, "cursor origin")
    require(out["row_codec"]["cursor_layout"][-1]["row_offset_in_body"] == 24, "cursor tail")
    require(out["data_anchor"]["duni_payload_evidence"]["uint64_le"] == 472446402670, "duni anchor value")
    reject("wrong type-25 factory target", lambda: require(out["nation_record"]["factory_type10"]["type25_target_file_offset"] == out["nation_record"]["factory_type10"]["type10_target_file_offset"], "type ids conflated"))
    reject("promoting opaque +0xe8 to a mapped 4CC", lambda: require(out["row_offset_map"].get("opaque_e8") is not None, "opaque field unexpectedly mapped"))
    reject("pretending three rows were validated", lambda: require(out["verification"]["complete_rows_verified"] >= 3, "row boundary negative control"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db-dir", type=Path, default=DEFAULT_DB, help="existing read-only 2430_fm directory")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write only the colocated output.json")
    mode.add_argument("--selftest", action="store_true", help="rebuild evidence, run negative controls, and compare output.json")
    args = ap.parse_args()
    try:
        out = build(args.db_dir)
        if args.selftest:
            selftest(out)
        result = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
        target = HERE / "output.json"
        if args.write:
            target.write_text(result, encoding="utf-8", newline="\n")
        else:
            require(read_json(target) == json.loads(result), "output.json differs from rebuilt evidence")
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, RuntimeError, ImportError, ValueError, KeyError, StopIteration) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"PASS: nation type 10; 7 partial L3 field links; negative serializer-mode result; {out['sources']['client_table_10']['record_count']} table rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
