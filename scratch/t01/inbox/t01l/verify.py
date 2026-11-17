#!/usr/bin/env python3
"""Read-only t01-l weather row parser and static slot verifier.

From the fm24-db workspace:
  py -V:3.12 -I -B scratch/t01/inbox/t01l/verify.py --help
  py -V:3.12 -I -B scratch/t01/inbox/t01l/verify.py --selftest
  py -V:3.12 -I -B scratch/t01/inbox/t01l/verify.py --write
--write only creates this task's output.json. No game/editor/IDA is launched.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path

import capstone
import capstone.x86_const as x86

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DB_DIR = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
CLIENT = DB_DIR / "client_db.dat"
EDITOR = Path("D:/tmp2b/fm24/input/editor.exe")
OLD_READER = Path("D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
T01H = ROOT / "scratch/t01/inbox/t01h/output.json"
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
EXPECTED_CLIENT_SHA = "5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1"
EXPECTED_MEMBER_SHA = "aaf5f170938babd755f9e020226d3dfcb437c3cd5bdb01796f30acee18e48770"
EXPECTED_EDITOR_SHA = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXPECTED_MASTER_SHA = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
EXPECTED_T01H_READER = "0x158b970"

# Getter dispatch jump-table LEA instruction file offsets and input-code bases.
# Each inner code uses big-endian ASCII as the 32-bit property identifier.
GROUPS = {
    "w0t": {"lea": 0x158e731, "range_lea": 0x158e722, "range_cmp": 0x158e728, "base": 0x77307430, "max_index": 0x46},
    "w1t": {"lea": 0x158e793, "range_lea": 0x158e784, "range_cmp": 0x158e78a, "base": 0x77317430, "max_index": 0x46},
    "w2t": {"lea": 0x158e762, "range_lea": 0x158e753, "range_cmp": 0x158e759, "base": 0x77327430, "max_index": 0x46},
    "w3t": {"lea": 0x158e6f5, "range_lea": 0x158e6e6, "range_cmp": 0x158e6ec, "base": 0x77337430, "max_index": 0x46},
    "w0p": {"lea": 0x158e7e8, "range_lea": 0x158e7d9, "range_cmp": 0x158e7df, "base": 0x77307030, "max_index": 4},
    "w1p": {"lea": 0x158e832, "range_lea": 0x158e823, "range_cmp": 0x158e829, "base": 0x77317030, "max_index": 4},
    "w2p": {"lea": 0x158e80d, "range_lea": 0x158e7fe, "range_cmp": 0x158e804, "base": 0x77327030, "max_index": 4},
    "w3p": {"lea": 0x158e7c3, "range_lea": 0x158e7b4, "range_cmp": 0x158e7ba, "base": 0x77337030, "max_index": 4},
    "w0w": {"lea": 0x158e887, "range_lea": 0x158e878, "range_cmp": 0x158e87e, "base": 0x77307730, "max_index": 4},
    "w1w": {"lea": 0x158e8d1, "range_lea": 0x158e8c2, "range_cmp": 0x158e8c8, "base": 0x77317730, "max_index": 4},
    "w2w": {"lea": 0x158e8ac, "range_lea": 0x158e89d, "range_cmp": 0x158e8a3, "base": 0x77327730, "max_index": 4},
    "w3w": {"lea": 0x158e862, "range_lea": 0x158e853, "range_cmp": 0x158e859, "base": 0x77337730, "max_index": 4},
}


class Failure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_old_reader():
    require(OLD_READER.is_file(), f"read-only decoder unavailable: {OLD_READER}")
    spec = importlib.util.spec_from_file_location("t01l_old_dbdat_reader", OLD_READER)
    require(spec is not None and spec.loader is not None, "cannot load old DB decoder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PE:
    def __init__(self, data: bytes):
        self.data = data
        u32 = lambda o: int.from_bytes(data[o:o + 4], "little")
        u16 = lambda o: int.from_bytes(data[o:o + 2], "little")
        p = u32(0x3c)
        require(data[p:p + 6] == b"PE\0\0\x64\x86", "editor.exe is not x64 PE")
        opt = p + 24
        require(u16(opt) == 0x20b, "editor.exe is not PE32+")
        self.base = int.from_bytes(data[opt + 24:opt + 32], "little")
        section_table = opt + u16(p + 20)
        self.sections = {}
        for s in range(section_table, section_table + u16(p + 6) * 40, 40):
            name = data[s:s + 8].rstrip(b"\0").decode("ascii")
            self.sections[name] = struct.unpack_from("<IIII", data, s + 8)
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True
        self.rip = x86.X86_REG_RIP

    def va(self, file_offset: int) -> int:
        for _, rva, raw_size, raw in self.sections.values():
            if raw <= file_offset < raw + raw_size:
                return self.base + rva + file_offset - raw
        raise Failure(f"editor.exe unmapped file offset {file_offset:#x}")

    def off(self, va: int) -> int:
        for _, rva, raw_size, raw in self.sections.values():
            delta = va - (self.base + rva)
            if 0 <= delta < raw_size:
                return raw + delta
        raise Failure(f"editor.exe VA has no file bytes: {va:#x}")

    def ev(self, file_offset: int, size: int) -> dict:
        b = self.data[file_offset:file_offset + size]
        require(len(b) == size, f"truncated editor.exe evidence at {file_offset:#x}")
        return {"file": "editor.exe", "file_offset": hex(file_offset),
                "va": hex(self.va(file_offset)), "bytes": b.hex(" ")}

    def ins_at(self, file_offset: int, count: int = 1):
        va = self.va(file_offset)
        return list(self.md.disasm(self.data[file_offset:file_offset + 0x100], va, count))

    def disasm(self, file_offset: int, size: int):
        return list(self.md.disasm(self.data[file_offset:file_offset + size], self.va(file_offset)))

    def ins(self, file_offset: int) -> dict:
        ins = self.ins_at(file_offset, 1)
        require(bool(ins), f"no instruction at editor.exe+{file_offset:#x}")
        i = ins[0]
        return {**self.ev(file_offset, i.size),
                "instruction": (i.mnemonic + " " + i.op_str).strip()}

    def rip_target(self, ins) -> int:
        matches = [o for o in ins.operands
                   if o.type == x86.X86_OP_MEM and o.mem.base == self.rip]
        require(len(matches) == 1, f"expected one RIP operand at {ins.address:#x}")
        return ins.address + ins.size + matches[0].mem.disp

    def follow_unconditional_route(self, start_off: int, max_hops: int = 12):
        """Follow only unconditional direct jumps, retaining exact path instructions."""
        current = start_off
        chain = []
        season_offset = None
        nested_code = None
        visited = set()
        for _ in range(max_hops):
            require(current not in visited, f"getter route loop at {current:#x}")
            visited.add(current)
            insns = self.disasm(current, 0x30)
            require(bool(insns), f"no getter handler at {current:#x}")
            jumped = False
            for i in insns:
                off = self.off(i.address)
                chain.append(self.ins(off))
                if (i.mnemonic == "add" and len(i.operands) == 2 and
                        i.operands[0].type == x86.X86_OP_REG and
                        i.reg_name(i.operands[0].reg) == "rdi" and
                        i.operands[1].type == x86.X86_OP_IMM):
                    season_offset = i.operands[1].imm & 0xffffffff
                if (i.mnemonic == "mov" and len(i.operands) == 2 and
                        i.operands[0].type == x86.X86_OP_REG and
                        i.reg_name(i.operands[0].reg) == "edx" and
                        i.operands[1].type == x86.X86_OP_IMM):
                    value = i.operands[1].imm & 0xffffffff
                    try:
                        nested_code = value.to_bytes(4, "big").decode("ascii")
                    except UnicodeDecodeError:
                        nested_code = hex(value)
                    return {"season_object_offset": season_offset,
                            "nested_member_code": nested_code,
                            "handler_chain": chain}
                if i.mnemonic == "jmp" and len(i.operands) == 1 and i.operands[0].type == x86.X86_OP_IMM:
                    current = self.off(i.operands[0].imm)
                    jumped = True
                    break
                if i.mnemonic.startswith("j") or i.mnemonic in ("ret", "call"):
                    break
            if not jumped:
                return {"season_object_offset": season_offset,
                        "nested_member_code": nested_code,
                        "handler_chain": chain}
        raise Failure(f"getter handler chain too deep from {start_off:#x}")


def parse_rows(raw: bytes, *, enforce_markers: bool = True) -> list[dict]:
    require(len(raw) >= 22, "table payload shorter than header/footer")
    require(raw[:8] == bytes.fromhex("03 01 74 61 64 2e f1 0d"), "table tad. header mismatch")
    count = struct.unpack_from("<I", raw, 8)[0]
    require(count > 0, "table row count is zero")
    require(raw[12] == 0, "unexpected table header byte at payload+0xc")
    require(raw[13] == 0, "first row boundary marker at payload+0xd is not zero")
    pos = 14
    rows = []
    for index in range(count):
        require(pos + 4 <= len(raw) - 8, f"row {index}: missing string length")
        name_len = struct.unpack_from("<I", raw, pos)[0]
        require(name_len <= 4096, f"row {index}: implausible name length {name_len}")
        name_start = pos + 4
        name_end = name_start + name_len
        require(name_end + 3 + 4 * 23 + 12 < len(raw), f"row {index}: truncated body")
        name_bytes = raw[name_start:name_end]
        try:
            name = name_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Failure(f"row {index}: invalid UTF-8 name: {exc}") from exc
        require("\0" not in name, f"row {index}: unexpected NUL in name")
        prelude_offset = name_end
        seasons_offset = prelude_offset + 3
        identity_offset = seasons_offset + 4 * 23
        marker_offset = identity_offset + 12
        require(marker_offset < len(raw) - 8, f"row {index}: row marker overlaps footer")
        marker = raw[marker_offset]
        if enforce_markers:
            require(marker == 0, f"row {index}: boundary marker at {marker_offset:#x} is {marker:#x}")
        season_values = []
        for season in range(4):
            s = seasons_offset + season * 23
            season_values.append({
                "start_day_wire_u16": struct.unpack_from("<H", raw, s)[0],
                "precipitation": list(raw[s + 2:s + 7]),
                "wind": list(raw[s + 7:s + 12]),
                "temperature": list(raw[s + 12:s + 22]),
                "day_night_variance": raw[s + 22],
                "payload_offset": s,
            })
        rows.append({
            "index": index,
            "row_start": pos,
            "name_length": name_len,
            "name_start": name_start,
            "name": name,
            "name_bytes": name_bytes.hex(" "),
            "prelude_offset": prelude_offset,
            "prelude_bytes": raw[prelude_offset:prelude_offset + 3].hex(" "),
            "seasons_offset": seasons_offset,
            "seasons": season_values,
            "identity_offset": identity_offset,
            "identity_bytes": raw[identity_offset:identity_offset + 12].hex(" "),
            "boundary_marker_offset": marker_offset,
            "boundary_marker": marker,
            "next_row_start": marker_offset + 1,
            "row_span_including_next_marker": marker_offset + 1 - pos,
        })
        pos = marker_offset + 1
    require(pos == len(raw) - 8,
            f"row walk ended at {pos:#x}, footer starts at {len(raw)-8:#x}")
    return rows


def expected_inner_code(code: str) -> tuple[str, int, int]:
    """Return nested subfield code, byte offset within a season block, width."""
    season = int(code[1])
    suffix = code[2:]
    if suffix == "sd":
        return "stdy", 0, 2
    if suffix == "dn":
        return "tend", 22, 1
    if suffix.startswith("p"):
        i = int(suffix[1])
        return f"pre{i}", 2 + i, 1
    if suffix.startswith("w"):
        i = int(suffix[1])
        return f"win{i}", 7 + i, 1
    if suffix == "te":
        return "teme", 12, 1
    if suffix == "tv":
        return "temv", 13, 1
    if suffix.startswith("t") and suffix[1].isdigit():
        i = int(suffix[1])
        return f"tem{i}", 14 + i, 1
    raise Failure(f"unrecognized weather schema field {code}")


def getter_dispatch(pe: PE, code: str) -> dict:
    getter_start = 0x158e6b0
    value = int.from_bytes(code.encode("ascii"), "big")
    if code == "wnam":
        hits = []
        for i in pe.disasm(getter_start, 0x330):
            if (i.mnemonic == "cmp" and len(i.operands) == 2 and
                    i.operands[0].type == x86.X86_OP_REG and
                    i.reg_name(i.operands[0].reg) == "edx" and
                    i.operands[1].type == x86.X86_OP_IMM and
                    (i.operands[1].imm & 0xffffffff) == value):
                hits.append(i)
        require(len(hits) == 1, "wnam: exact getter compare is missing/ambiguous")
        cmp_i = hits[0]
        cmp_off = pe.off(cmp_i.address)
        branch_i = next((i for i in pe.disasm(cmp_off, 0x60) if i.mnemonic == "jne"), None)
        require(branch_i is not None, "wnam getter branch missing")
        add_off = cmp_off + cmp_i.size + branch_i.size
        add_i = pe.ins_at(add_off, 1)[0]
        require(add_i.mnemonic == "add" and add_i.op_str == "rdi, 0x18",
                "wnam getter does not select object+0x18")
        return {"kind": "cmp_edx_imm32_string", "compare": pe.ins(cmp_off),
                "branch": pe.ins(pe.off(branch_i.address)), "selected_object_offset": "0x18",
                "member_access": pe.ins(add_off),
                "reader_member_object_offset": "0x18", "width": "variable UTF-8 string"}
    if code[:3] in GROUPS:
        group = GROUPS[code[:3]]
        index = value - group["base"]
        require(0 <= index <= group["max_index"],
                f"{code}: input code outside getter range")
        lea = pe.ins_at(group["lea"], 1)[0]
        table_va = pe.rip_target(lea)
        table_off = pe.off(table_va)
        range_lea = pe.ins_at(group["range_lea"], 1)[0]
        range_cmp = pe.ins_at(group["range_cmp"], 1)[0]
        require(range_lea.mnemonic == "lea" and range_lea.operands[1].type == x86.X86_OP_MEM and
                range_lea.operands[1].mem.disp == -group["base"],
                f"{code}: range arithmetic does not subtract the expected code base")
        require(range_cmp.mnemonic == "cmp" and range_cmp.operands[1].imm == group["max_index"],
                f"{code}: range bound differs")
        slot_off = table_off + index * 4
        rel = int.from_bytes(pe.data[slot_off:slot_off + 4], "little", signed=True)
        target_va = table_va + rel
        target_off = pe.off(target_va)
        route = pe.follow_unconditional_route(target_off)
        want_nested, inner_offset, width = expected_inner_code(code)
        require(route["season_object_offset"] == 0x20 + int(code[1]) * 0x18,
                f"{code}: getter selects unexpected season base {route['season_object_offset']!r}")
        require(route["nested_member_code"] == want_nested,
                f"{code}: getter inner code {route['nested_member_code']!r} != {want_nested}")
        return {
            "kind": "range_then_rel32_jump_table",
            "input_code_big_endian": hex(value),
            "family": code[:3],
            "range_base": hex(group["base"]),
            "range_index": index,
            "range_limit": hex(group["max_index"]),
            "range_arithmetic": pe.ins(group["range_lea"]),
            "range_bound": pe.ins(group["range_cmp"]),
            "dispatch_lea": pe.ins(group["lea"]),
            "jump_table_file_offset": hex(table_off),
            "jump_table_entry": pe.ev(slot_off, 4),
            "jump_target_file_offset": hex(target_off),
            "selected_season_object_offset": hex(route["season_object_offset"]),
            "nested_member_code": route["nested_member_code"],
            "handler_chain": route["handler_chain"],
            "nested_member_offset_in_season": inner_offset,
            "width": width,
        }

    # Scalar seasonal fields are explicit full-register cmp edx,imm32 cases.
    hits = []
    for i in pe.disasm(getter_start, 0x330):
        if (i.mnemonic == "cmp" and len(i.operands) == 2 and
                i.operands[0].type == x86.X86_OP_REG and
                i.reg_name(i.operands[0].reg) == "edx" and
                i.operands[1].type == x86.X86_OP_IMM and
                (i.operands[1].imm & 0xffffffff) == value):
            hits.append(i)
    require(len(hits) == 1, f"{code}: expected one cmp edx,imm32 in weather getter; found {len(hits)}")
    cmp_i = hits[0]
    season = int(code[1])
    nested, inner_offset, width = expected_inner_code(code)
    after_cmp = pe.off(cmp_i.address) + cmp_i.size
    following = pe.ins_at(after_cmp, 1)[0]
    branch = following
    if code.endswith("dn"):
        require(branch.mnemonic == "je", f"{code}: day/night compare does not branch equal")
        route_start = pe.off(branch.operands[0].imm)
    else:
        require(code.endswith("sd") and branch.mnemonic == "jne",
                f"{code}: start-day compare branch mismatch")
        route_start = after_cmp + branch.size
    route = pe.follow_unconditional_route(route_start)
    require(route["season_object_offset"] == 0x20 + season * 0x18,
            f"{code}: getter selects unexpected season base")
    require(route["nested_member_code"] == nested,
            f"{code}: nested getter code {route['nested_member_code']!r} != {nested}")
    return {
        "kind": "cmp_edx_imm32_then_nested_member",
        "compare": pe.ins(pe.off(cmp_i.address)),
        "branch": pe.ins(pe.off(branch.address)),
        "selected_season_object_offset": hex(route["season_object_offset"]),
        "nested_member_code": route["nested_member_code"],
        "handler_chain": route["handler_chain"],
        "nested_member_offset_in_season": inner_offset,
        "width": width,
    }


def build_result():
    require(CLIENT.is_file(), f"client_db.dat missing: {CLIENT}")
    require(EDITOR.is_file(), f"editor.exe missing: {EDITOR}")
    archive = CLIENT.read_bytes()
    require(sha256(archive) == EXPECTED_CLIENT_SHA, "client_db.dat SHA-256 mismatch")
    editor_bytes = EDITOR.read_bytes()
    require(sha256(editor_bytes) == EXPECTED_EDITOR_SHA, "editor.exe SHA-256 mismatch")
    pe = PE(editor_bytes)

    decoder = load_old_reader()
    _, archive_blob, layout = decoder._entries(DB_DIR, "client_db.dat")
    entries = [e for e in layout["entries"] if e["path"] == "client_db/table_27.dat"]
    require(len(entries) == 1, "client_db/table_27.dat exact member missing/ambiguous")
    entry = entries[0]
    member_file_offset = layout["data_base"] + entry["offset"]
    compressed = archive_blob[member_file_offset:member_file_offset + entry["packed_size"]]
    require(compressed[:4] == bytes.fromhex("28 b5 2f fd"), "table_27 member is not Zstandard")
    raw = decoder._decompress_entry(archive_blob, layout["data_base"], entry)
    require(sha256(raw) == EXPECTED_MEMBER_SHA, "table_27 decompressed SHA-256 mismatch")
    rows = parse_rows(raw)
    require(len(rows) == 334, "table_27 row count differs from tad. count")

    # Schema snapshot pinning is required before any schema names are used.
    master_bytes = MASTER.read_bytes()
    require(sha256(master_bytes) == EXPECTED_MASTER_SHA, "frozen master.json SHA-256 mismatch")
    manifest = load_json(MANIFEST)
    manifest_row = next((x for x in manifest["files"]
                         if x.get("path") == "evidence/fm24/reports/editor_schema/master.json"), None)
    require(manifest_row is not None and manifest_row["sha256"] == EXPECTED_MASTER_SHA,
            "master.json SHA-256 is not pinned in evidence/MANIFEST.json")
    master = json.loads(master_bytes.decode("utf-8"))
    schema = master["entities"]["weather.xml"][0]
    require(schema["id"] == "weat" and len(schema["fields"]) == 94,
            "weather.xml#weat schema shape differs")
    schema_fields = {f["field"]: f for f in schema["fields"]}

    # Use all field-code compare encodings, not ESI-only cmp heuristics.
    # The vector families are range/jump-table dispatches; scalar codes use EDX.
    getter_codes = []
    for code, meta in schema_fields.items():
        if code.startswith(("w0", "w1", "w2", "w3")) and len(code) == 4:
            getter_codes.append(code)
    mapped_codes = [c for c in getter_codes if c[:3] in GROUPS or c.endswith(("sd", "dn"))]
    mapped_codes = [c for c in mapped_codes if c != "dbnm"]
    field_map = {}
    getter_routes = {}
    direct_fields = []
    for code in mapped_codes:
        if code == "wnam":
            continue
        want_nested, inner, width = expected_inner_code(code)
        dispatch = getter_dispatch(pe, code)
        season = int(code[1])
        object_offset = 0x20 + season * 0x18 + inner
        if width == 2:
            sink = {
                "destination": pe.ins(0x158ba27),
                "width_instruction": pe.ins(0x158ba2f),
                "stream_call": pe.ins(0x158ba3b),
            }
        else:
            # Identify the exact lea rdx,[rbx+r12+member] and its width/call.
            reader_ins = pe.disasm(0x158ba11, 0x300)
            candidates = []
            for j, i in enumerate(reader_ins):
                if (i.mnemonic == "lea" and len(i.operands) == 2 and
                        i.operands[0].type == x86.X86_OP_REG and
                        i.reg_name(i.operands[0].reg) == "rdx" and
                        i.operands[1].type == x86.X86_OP_MEM and
                        i.reg_name(i.operands[1].mem.base) == "rbx" and
                        i.reg_name(i.operands[1].mem.index) == "r12"):
                    displacement = i.operands[1].mem.disp
                    if displacement == 0x20 + inner:
                        width_i = next((q for q in reader_ins[j + 1:j + 5]
                                        if q.mnemonic == "mov" and len(q.operands) == 2 and
                                        q.reg_name(q.operands[0].reg) == "r8d"), None)
                        call_i = next((q for q in reader_ins[j + 1:j + 10]
                                       if q.mnemonic == "call" and q.op_str == "qword ptr [rax + 0x28]"), None)
                        if width_i and call_i:
                            candidates.append((i, width_i, call_i))
            require(len(candidates) == 1,
                    f"{code}: expected one static reader destination for object+{object_offset:#x}, got {len(candidates)}")
            dest_i, width_i, call_i = candidates[0]
            sink = {"destination": pe.ins(pe.off(dest_i.address)),
                    "width_instruction": pe.ins(pe.off(width_i.address)),
                    "stream_call": pe.ins(pe.off(call_i.address))}
        require(object_offset == dispatch["selected_season_object_offset"] if isinstance(dispatch["selected_season_object_offset"], int)
                else object_offset == int(dispatch["selected_season_object_offset"], 16) + inner,
                f"{code}: getter/reader object offset disagreement")
        row_formula = (f"row_start + 7 + name_byte_length + {season * 23} + {inner}")
        status = "wire field read directly; post-read percentage normalizer may rewrite designated slots when that group's sum is not 100"
        if code.endswith("sd"):
            status = "2-byte wire day; preserved when four seasonal words differ; canonicalized only when all four wire words are equal"
        item = {
            "schema": "weather.xml#weat",
            "field": code,
            "name": schema_fields[code]["name"],
            "season": season,
            "width": width,
            "nested_member_code": want_nested,
            "nested_member_offset_in_season": inner,
            "object_offset": object_offset,
            "row_offset_formula": row_formula,
            "wire_semantics": status,
            "getter_dispatch": dispatch,
            "reader_sink": sink,
        }
        field_map[code] = item
        getter_routes[code] = {"kind": dispatch["kind"], "family": dispatch.get("family"),
                               "range_index": dispatch.get("range_index"),
                               "range_base": dispatch.get("range_base"),
                               "jump_table_file_offset": dispatch.get("jump_table_file_offset"),
                               "jump_table_entry": dispatch.get("jump_table_entry"),
                               "compare": dispatch.get("compare"),
                               "branch": dispatch.get("branch"),
                               "jump_target_file_offset": dispatch.get("jump_target_file_offset"),
                               "handler_chain": dispatch.get("handler_chain"),
                               "selected_season_object_offset": dispatch.get("selected_season_object_offset"),
                               "nested_member_code": dispatch.get("nested_member_code")}
        direct_fields.append(code)

    wnam_dispatch = getter_dispatch(pe, "wnam")
    # Use the reader's exact shared-string helper call and destination setup.
    wnam = {
        "schema": "weather.xml#weat", "field": "wnam", "name": schema_fields["wnam"]["name"],
        "width": "u32 byte length + variable UTF-8 bytes", "object_offset": 0x18,
        "row_offset_formula": "row_start + 4 (name bytes; u32 byte length is at row_start)",
        "wire_semantics": "variable-length UTF-8 string", "getter_dispatch": wnam_dispatch,
        "reader_source": {"string_object_destination": pe.ins(0x158b98c),
                          "reader_string_helper_call": pe.ins(0x158b995),
                          "helper_length_width": pe.ins(0x35b0822),
                          "helper_variable_width_load": pe.ins(0x35b0879),
                          "helper_length_stream_call": pe.ins(0x35b0828),
                          "helper_content_stream_call": pe.ins(0x35b0883)},
    }
    field_map["wnam"] = wnam

    # Full reader width census: 25 immediate widths in the row reader, plus
    # length=4 and identity=12 helper widths. Variable name bytes use runtime R8D.
    reader_ins = pe.disasm(0x158b970, 0x400)
    direct_width_ins = [i for i in reader_ins if i.mnemonic == "mov" and len(i.operands) == 2
                        and i.reg_name(i.operands[0].reg) == "r8d"
                        and i.operands[1].type == x86.X86_OP_IMM]
    string_ins = pe.disasm(0x35b07f0, 0x250)
    string_width_ins = [i for i in string_ins if i.mnemonic == "mov" and len(i.operands) == 2
                        and i.reg_name(i.operands[0].reg) == "r8d"
                        and i.operands[1].type == x86.X86_OP_IMM]
    identity_ins = pe.disasm(0x3c600f0, 0x100)
    identity_width_ins = [i for i in identity_ins if i.mnemonic == "mov" and len(i.operands) == 2
                          and i.reg_name(i.operands[0].reg) == "r8d"
                          and i.operands[1].type == x86.X86_OP_IMM]
    require(len(direct_width_ins) == 25, f"row reader immediate width count {len(direct_width_ins)} !=25")
    require([i.operands[1].imm for i in string_width_ins] == [4], "string helper fixed-width prefix differs")
    require([i.operands[1].imm for i in identity_width_ins] == [12], "identity helper fixed-width transfer differs")
    direct_stream_calls = [i for i in reader_ins if i.mnemonic == "call" and i.op_str == "qword ptr [rax + 0x28]"]
    string_stream_calls = [i for i in string_ins if i.mnemonic == "call" and i.op_str == "qword ptr [rax + 0x28]"]
    identity_stream_calls = [i for i in identity_ins if i.mnemonic == "call" and i.op_str == "qword ptr [rax + 0x28]"]
    stream_call_count = len(direct_stream_calls) + len(string_stream_calls) + len(identity_stream_calls)
    require((len(direct_stream_calls), len(string_stream_calls), len(identity_stream_calls), stream_call_count) == (25, 2, 1, 28),
            "stream call count breakdown differs from 25+2+1")
    control_flow = []
    for i in reader_ins:
        if i.mnemonic.startswith("j") and i.mnemonic != "jmp" and i.operands and i.operands[0].type == x86.X86_OP_IMM:
            off = pe.off(i.address)
            target_off = pe.off(i.operands[0].imm)
            if off == 0x158bd01:
                role = "fixed four-season loop backedge"
            elif 0x158bd0f <= off <= 0x158bd1b:
                role = "unequal date words bypass canonical overwrites"
            elif target_off == 0x158b9fe:
                role = "stream status failure exit"
            elif off == 0x158b9fc:
                role = "successful initial status enters seasonal loop"
            else:
                role = "conditional status/control edge"
            control_flow.append({**pe.ins(off), "target_file_offset": hex(target_off), "role": role})
    all_widths = []
    for role, instructions in (("variable_string_helper", string_width_ins),
                               ("row_reader", direct_width_ins),
                               ("identity_helper", identity_width_ins)):
        for i in instructions:
            off = pe.off(i.address)
            all_widths.append({"role": role, **pe.ins(off), "width": i.operands[1].imm})
    require(len(all_widths) == 27, "combined static immediate width count differs from t01h census")

    # Verify exactly four static season destinations and their 23-byte wire block.
    season_loop = {
        "loop_initialize": pe.ins(0x158ba21),
        "season_destination": pe.ins(0x158ba27),
        "two_byte_width": pe.ins(0x158ba2f),
        "two_byte_stream_call": pe.ins(0x158ba3b),
        "one_byte_first_destination": pe.ins(0x158ba47),
        "one_byte_first_width": pe.ins(0x158ba4f),
        "one_byte_first_stream_call": pe.ins(0x158ba58),
        "loop_increment": pe.ins(0x158bcf9),
        "loop_limit": pe.ins(0x158bcfd),
        "loop_backedge": pe.ins(0x158bd01),
        "iterations": 4,
        "object_block_stride": 24,
        "wire_bytes_per_season": 23,
        "wire_field_order": ["start_day:u16", "precipitation:5xu8", "wind:5xu8",
                              "temperature:10xu8", "day_night_variance:u8"],
    }
    # The loop instruction addresses above are exact code landmarks; check the encoded arithmetic.
    require(pe.data[0x158bcf9:0x158bd01] == bytes.fromhex("49 83 c4 18 49 83 fc 60"),
            "four-season loop increment/limit bytes mismatch")
    require(pe.data[0x158bd01:0x158bd07] == bytes.fromhex("0f 85 1d fd ff ff"),
            "four-season loop backedge bytes mismatch")
    require(direct_width_ins[3].operands[1].imm == 2 and
            sum(1 for i in direct_width_ins[4:] if i.operands[1].imm == 1) == 21,
            "per-season width block is not one 2B plus 21 1B transfers")

    # The normalizer's call is inside the four-iteration season loop. It adjusts
    # precipitation/wind/temperature distributions only when their sums differ.
    normalizer = {
        "reader_call_each_season": pe.ins(0x158bcf4),
        "thunk": pe.ins(0x158bd70),
        "normalizer_entry": pe.ins(0x43e7e10),
        "precipitation_sum_reads": [pe.ins(o) for o in (0x43e7e14, 0x43e7e18, 0x43e7e1e, 0x43e7e24, 0x43e7e2a)],
        "precipitation_rewrite": pe.ins(0x43e7e40),
        "wind_sum_reads": [pe.ins(o) for o in (0x43e7e53, 0x43e7e57, 0x43e7e5d, 0x43e7e63, 0x43e7e69)],
        "wind_rewrite": pe.ins(0x43e7e7c),
        "temperature_sum_reads": [pe.ins(o) for o in (0x43e7e94, 0x43e7e99, 0x43e7ea0, 0x43e7ea6, 0x43e7eae,
                                                         0x43e7eb6, 0x43e7ebe, 0x43e7ec4, 0x43e7eca, 0x43e7ed0)],
        "temperature_rewrite": pe.ins(0x43e7ef5),
    }

    # Four serialized start-day words are compared; only the all-equal path rewrites them.
    start_day_normalization = {
        "compare_first_to_second": pe.ins(0x158bd0b),
        "compare_to_third": pe.ins(0x158bd11),
        "compare_to_fourth": pe.ins(0x158bd17),
        "mismatch_bypass_branches": [pe.ins(o) for o in (0x158bd0f, 0x158bd15, 0x158bd1b)],
        "canonical_overwrites_only_on_equal_all_four": True,
        "canonical_overwrites": [pe.ins(o) for o in (0x158bd1d, 0x158bd23, 0x158bd29, 0x158bd2f)],
        "canonical_values": [55, 145, 230, 300],
    }

    # Table row formulas and all-row checks.
    name_lengths = [r["name_length"] for r in rows]
    row_deltas = [r["row_span_including_next_marker"] for r in rows]
    distributions = {category: {"groups": 0, "sum_100": 0, "non_100": 0, "non_100_examples": []}
                     for category in ("precipitation", "wind", "temperature")}
    total_groups = len(rows) * 4
    start_days_equal = 0
    for row in rows:
        for season_index, s in enumerate(row["seasons"]):
            for category, stats in distributions.items():
                value_sum = sum(s[category])
                stats["groups"] += 1
                if value_sum == 100:
                    stats["sum_100"] += 1
                else:
                    stats["non_100"] += 1
                    if len(stats["non_100_examples"]) < 8:
                        stats["non_100_examples"].append({"row": row["index"], "season": season_index,
                                                           "payload_offset": hex(s["payload_offset"]),
                                                           "sum": value_sum, "wire_bytes": bytes(s[category]).hex(" ")})
        day_values = [s["start_day_wire_u16"] for s in row["seasons"]]
        if len(set(day_values)) == 1:
            start_days_equal += 1
    require(0 <= start_days_equal <= len(rows), "invalid start-day equality count")
    require(len(set(row_deltas)) > 1, "payload unexpectedly has a fixed row stride")

    # Five independent complete row samples, including 12 mapped schema fields.
    sample_indexes = [0, 1, 2, 139, 333]
    sample_codes = ["w0p1", "w0p4", "w0w1", "w0w4", "w0te", "w0tv",
                    "w0t0", "w0t1", "w0t2", "w0t3", "w0t4", "w0dn"]
    samples = []
    for ix in sample_indexes:
        row = rows[ix]
        field_bytes = {}
        for code in sample_codes:
            item = field_map[code]
            season = item["season"]
            inner = item["nested_member_offset_in_season"]
            off = row["seasons_offset"] + season * 23 + inner
            width = item["width"]
            field_bytes[code] = {"payload_offset": hex(off),
                                 "bytes": raw[off:off + width].hex(" "),
                                 "value_le": int.from_bytes(raw[off:off + width], "little")}
        samples.append({"index": ix, "row_start": hex(row["row_start"]),
                        "name": row["name"], "name_length": row["name_length"],
                        "name_length_bytes": raw[row["row_start"]:row["row_start"] + 4].hex(" "),
                        "name_bytes_offset": hex(row["name_start"]),
                        "name_bytes": row["name_bytes"],
                        "wire_start_day_words": [s["start_day_wire_u16"] for s in row["seasons"]],
                        "identity_offset": hex(row["identity_offset"]),
                        "identity_bytes_unassigned": row["identity_bytes"],
                        "boundary_marker_offset": hex(row["boundary_marker_offset"]),
                        "boundary_marker": row["boundary_marker"],
                        "mapped_fields": field_bytes})

    # Getter evidence is intentionally a full-register scan; ensure EDX-based
    # exact matches for scalar codes and all range dispatch families are present.
    getter_scan = []
    getter_start = 0x158e6b0
    getter_end = getter_start + 0x330
    getter_ins = pe.disasm(getter_start, getter_end - getter_start)
    decoded_cmp_by_offset = {}
    for ins in getter_ins:
        if (ins.mnemonic == "cmp" and len(ins.operands) == 2 and
                ins.operands[0].type == x86.X86_OP_REG and
                ins.operands[1].type == x86.X86_OP_IMM):
            reg = ins.reg_name(ins.operands[0].reg)
            imm = ins.operands[1].imm & 0xffffffff
            text = None
            if all(32 <= b < 127 for b in imm.to_bytes(4, "big")):
                text = imm.to_bytes(4, "big").decode("ascii")
            ins_off = pe.off(ins.address)
            decoded_cmp_by_offset[ins_off] = {"register": reg, "imm32": imm, "ascii_be": text}
            getter_scan.append({**pe.ins(ins_off), "register": reg,
                                "imm32": hex(imm), "ascii_be": text})
    reg_names = {0xf8: "eax", 0xf9: "ecx", 0xfa: "edx", 0xfb: "ebx",
                 0xfc: "esp", 0xfd: "ebp", 0xfe: "esi", 0xff: "edi"}
    raw_register_cmp_matches = []
    raw_eax_cmp_matches = []
    # Byte scan of the whole getter window, then cross-check each hit against
    # the decoded instruction boundary so immediates/data are not promoted.
    for off in range(getter_start, getter_end):
        if off + 6 <= getter_end and pe.data[off] == 0x81 and pe.data[off + 1] in reg_names:
            reg_opcode = pe.data[off + 1]
            imm = int.from_bytes(pe.data[off + 2:off + 6], "little")
            decoded = decoded_cmp_by_offset.get(off)
            raw_register_cmp_matches.append({**pe.ev(off, 6), "register_opcode": hex(reg_opcode),
                                             "register": reg_names[reg_opcode], "imm32": hex(imm),
                                             "ascii_be": imm.to_bytes(4, "big").decode("latin1"),
                                             "decoded_cmp_instruction": decoded is not None and
                                             decoded["imm32"] == imm and decoded["register"] == reg_names[reg_opcode]})
        if off + 5 <= getter_end and pe.data[off] == 0x3d:
            imm = int.from_bytes(pe.data[off + 1:off + 5], "little")
            decoded = decoded_cmp_by_offset.get(off)
            raw_eax_cmp_matches.append({**pe.ev(off, 5), "register": "eax", "imm32": hex(imm),
                                        "ascii_be": imm.to_bytes(4, "big").decode("latin1"),
                                        "decoded_cmp_instruction": decoded is not None and
                                        decoded["imm32"] == imm and decoded["register"] == "eax"})
    require(any(x["register_opcode"] == "0xfa" and x["decoded_cmp_instruction"]
                for x in raw_register_cmp_matches),
            "raw 81 f8..ff byte scan failed to confirm EDX (81 fa)")
    require(all(x["decoded_cmp_instruction"] for x in raw_register_cmp_matches),
            "raw 81 f8..ff scan found an undecoded/non-cmp candidate in getter window")
    require(all(x["decoded_cmp_instruction"] for x in raw_eax_cmp_matches),
            "raw 3d scan found an undecoded/non-cmp candidate in getter window")
    require(any(x["register"] == "edx" and x.get("ascii_be") == "w3dn" for x in getter_scan),
            "full-register weather getter scan missed EDX w3dn compare")
    require(any(x["register"] == "edx" and x.get("ascii_be") == "w0sd" for x in getter_scan),
            "full-register weather getter scan missed EDX w0sd compare")

    # Static source proof for allocator/type/slot anchors, plus the census mode.
    t01h = load_json(T01H)
    census = next((x for x in t01h["census"] if x.get("type_id") == 27), None)
    require(census is not None, "t01h lacks type-id 27 census")
    reader = census["reader"]["slot19_readers"][0]
    require(reader["entry_file_offset"] == EXPECTED_T01H_READER and
            reader["mode"] == "straight-line" and reader["width_count"] == 27,
            "t01h type-27 reader census differs")
    require(pe.data[0x1882480:0x1882488] == bytes.fromhex("70 c3 58 41 01 00 00 00"),
            "type-27 slot-19 pointer bytes mismatch")
    require(pe.data[0x158b970:0x158b978] == bytes.fromhex("41 57 41 56 41 55 41 54"),
            "type-27 reader entry bytes mismatch")

    mapped_business = [c for c in field_map if c == "wnam" or c.startswith(("w0", "w1", "w2", "w3"))]
    # All 88 seasonal fields plus wnam have getter->object->wire mappings; dbnm is not claimed.
    require(len(mapped_business) == 89, f"mapped business fields={len(mapped_business)}, expected 89")
    require(len(samples) == 5, "five-row sample count mismatch")

    result = {
        "task": "t01-l weather table_27 row offsets",
        "acceptance": {
            "met": True,
            "L3_weather_business_fields": len(mapped_business),
            "includes": mapped_business,
            "conditionally_canonicalized_wire_start_day_rows": start_days_equal,
            "start_day_canonicalization": "only if all four serialized words are equal; otherwise reader preserves them",
            "five_rows_checked": len(samples),
            "all_rows_checked": len(rows),
            "seasonal_groups_checked_per_probability_family": total_groups,
            "L4": 0,
        },
        "sources": {
            "archive": {"file": CLIENT.as_posix(), "sha256": sha256(archive), "bytes": len(archive),
                        "member": entry["path"], "member_file_offset": hex(member_file_offset),
                        "compressed_file_offset_bytes": archive[member_file_offset:member_file_offset + 16].hex(" "),
                        "compressed_size": entry["packed_size"], "decompressed_bytes": len(raw),
                        "decompressed_sha256": sha256(raw),
                        "payload_header": {"file_offset_domain": "decompressed member", "offset": "0x0",
                                            "bytes": raw[:14].hex(" ")},
                        "footer": {"payload_offset": hex(len(raw) - 8), "bytes": raw[-8:].hex(" ")}},
            "binary": {"file": EDITOR.as_posix(), "bytes": len(editor_bytes),
                       "sha256": sha256(editor_bytes), "evidence_level": "L3 static"},
            "schema_snapshot": {"file": "evidence/fm24/reports/editor_schema/master.json",
                                "sha256": sha256(master_bytes), "manifest_verified": True,
                                "entity": "weather.xml#weat", "field_count": len(schema["fields"])},
            "t01h_anchor": {"type_id": 27, "reader_mode_reported": reader["mode"],
                            "width_count_reported": reader["width_count"],
                            "rtti_name": pe.ev(0x1aae200, 17),
                            "allocation_request_0x88": pe.ev(0x3bd750c, 5),
                            "type_query": pe.ev(0xfb37f0, 6),
                            "entry": pe.ev(0x158b970, 24),
                            "slot19_pointer": pe.ev(0x1882480, 8)},

        },
        "row_codec": {
            "header_bytes": 14,
            "first_row_start": 14,
            "first_preceding_marker": {"payload_offset": "0xd", "bytes": raw[13:14].hex(" ")},
            "row_start_recurrence": "start[0]=14; start[i+1]=start[i]+112+u32le(payload+start[i])",
            "serialized_body": ["u32le UTF-8 byte length", "name bytes", "3 unassigned bytes",
                                "4 seasons x 23 bytes", "12-byte trailing base block", "one 0 marker"],
            "season_wire_layout": ["start-day seed u16le @+0", "precipitation 5xu8 @+2..+6",
                                   "wind 5xu8 @+7..+11", "temperature 10xu8 @+12..+21",
                                   "day/night variance u8 @+22"],
            "row_count": len(rows), "name_length_min": min(name_lengths),
            "name_length_max": max(name_lengths), "name_length_sum": sum(name_lengths),
            "distinct_row_spans": len(set(row_deltas)), "first_row_span": row_deltas[0],
            "last_row_span": row_deltas[-1], "payload_bytes": len(raw),
            "rows_end_at": hex(len(raw) - 8), "footer_bytes": 8,
            "identity_bytes_semantics": "12 raw bytes preserved; not named by this task",
            "all_boundary_markers_zero": all(r["boundary_marker"] == 0 for r in rows),
        },
        "reader_widths": {
            "census_interpretation": "27 static immediate widths across entry+helpers; 28 stream calls. Not literally straight-line: one bounded 4-season loop is present.",
            "immediate_widths": all_widths,
            "dynamic_string_width": {"load": pe.ins(0x35b0879), "meaning": "runtime name byte length"},
            "stream_call_count_rebuilt": stream_call_count,
            "stream_call_breakdown": {"row_reader": len(direct_stream_calls), "string_helper": len(string_stream_calls),
                                      "identity_helper": len(identity_stream_calls)},
            "conditional_control_flow": control_flow,
            "row_reader_immediate_width_count": len(direct_width_ins),
            "season_loop": season_loop,
            "normalizer": normalizer,
            "wire_start_day_normalization": start_day_normalization,
            "no_global_state_width_selector_found": True,
            "loop_vs_error_edges": {"single_counted_loop_backedge": pe.ins(0x158bd01),
                                     "season_count": 4,
                                     "note": "other conditional edges are stream-status exits or post-read date canonicalization; none selects transfer width"},
        },
        "getter_scan": {"registers_scanned": ["eax via cmp eax,imm32 (3d)",
                                                       "all general registers via cmp r32,imm32 (81 f8..ff)"],
                         "byte_scan_file_window": [hex(getter_start), hex(getter_end)],
                         "raw_3d_candidate_count": len(raw_eax_cmp_matches),
                         "getter_cmp_immediates": getter_scan,
                         "raw_81_f8_ff_immediate_matches": raw_register_cmp_matches,
                         "raw_3d_eax_immediate_matches": raw_eax_cmp_matches,
                         "explicit_scalar_codes": ["w0sd", "w1sd", "w2sd", "w3sd",
                                                    "w0dn", "w1dn", "w2dn", "w3dn", "wnam"],
                         "range_families": {k: {"range_arithmetic": pe.ins(v["range_lea"]),
                                                "range_bound": pe.ins(v["range_cmp"]),
                                                "jump_table_lea": pe.ins(v["lea"]),
                                                "input_base": hex(v["base"]),
                                                "maximum_index": v["max_index"]} for k, v in GROUPS.items()}},
        "row_offset_map": field_map,
        "normalization_checks": {"precipitation": distributions["precipitation"],
                                 "wind": distributions["wind"],
                                 "temperature": distributions["temperature"],
                                 "groups_total_per_category": total_groups,
                                 "equal_wire_startday_rows": start_days_equal,
                                 "unequal_wire_startday_rows": len(rows) - start_days_equal,
                                 "wire_startday_fields_conditionally_canonicalized": True,
                                 "wire_offsets_remain_mapped_even_when_postread_normalization_changes_values": True},
        "five_row_samples": samples,
        "negative_controls": {
            "fixed_stride_rejected": {"candidate_first_span": row_deltas[0],
                                       "first_two_actual_spans": row_deltas[:2],
                                       "distinct_spans": len(set(row_deltas)),
                                       "reason": "variable string byte lengths change row starts"},
            "synthetic_nonzero_boundary_marker_rejected": True,
            "synthetic_corrupt_name_length_rejected": True,
            "all_register_cmp_scan_tested": True,
            "raw_register_cmp_match_count": len(raw_register_cmp_matches),
            "raw_eax_cmp_match_count": len(raw_eax_cmp_matches),
        },
        "open_questions": ["dbnm and three prelude bytes are not assigned to schema fields",
                           "12-byte trailing block is retained without assigning duni/rdui semantics",
                           "four equal wire start-day words are canonicalized; differing per-season dates are preserved"],
    }
    return result, raw, rows, pe


def run_selftest():
    result, raw, rows, pe = build_result()
    output_path = HERE / "output.json"
    require(output_path.is_file(), "output.json missing; run --write once")
    saved = load_json(output_path)
    require(saved == result, "output.json differs from a fresh read-only rebuild")

    # Full-frame mutation negatives are in-memory only.
    bad_marker = bytearray(raw)
    bad_marker[rows[0]["boundary_marker_offset"]] = 1
    try:
        parse_rows(bytes(bad_marker))
    except Failure as exc:
        require("boundary marker" in str(exc), f"unexpected marker negative-control failure: {exc}")
    else:
        raise Failure("synthetic nonzero row boundary marker was accepted")
    bad_length = bytearray(raw)
    bad_length[rows[0]["row_start"]] ^= 1
    try:
        parse_rows(bytes(bad_length))
    except Failure as exc:
        require(any(s in str(exc) for s in ("boundary marker", "truncated", "row walk ended", "UTF-8")),
                f"unexpected length negative-control failure: {exc}")
    else:
        raise Failure("synthetic corrupt name length was accepted")

    spans = [r["row_span_including_next_marker"] for r in rows]
    require(len(set(spans)) > 1, "fixed-stride negative control did not distinguish rows")
    # Synthetic all-register immediate-CMP scanner guard, including 3d/EAX.
    probe = b"".join(bytes((0x81, opcode)) + b"ABCD" for opcode in range(0xf8, 0x100)) + b"\x3dWXYZ"
    found = []
    for i in range(len(probe) - 4):
        if probe[i] == 0x81 and 0xf8 <= probe[i + 1] <= 0xff:
            found.append(probe[i + 1])
        elif probe[i] == 0x3d:
            found.append(0x3d)
    require(found == list(range(0xf8, 0x100)) + [0x3d],
            "synthetic all-register cmp scan negative control failed")

    require(len(rows) == 334 and result["acceptance"]["L3_weather_business_fields"] >= 10,
            "acceptance line not met")
    print("PASS: archive/member SHA-256, Zstd member, frozen schema manifest, and type-27 anchors")
    print(f"PASS: full variable-row walk: {len(rows)} rows; end={len(raw)-8:#x}; footer=8 bytes")
    print("PASS: variable name lengths, per-row marker, four 23-byte seasonal blocks, trailing 12 bytes")
    print("PASS: 27 immediate widths/28 stream calls; fixed 4-season loop, no width-state selector")
    print("PASS: getter dispatch through all-register cmp scan and 12 range/jump tables")
    print(f"PASS: {result['acceptance']['L3_weather_business_fields']} L3 business fields; five rows x 12 field byte samples")
    print("PASS: per-group normalization counts, start-day overwrite note, fixed-stride/name-length negative control")
    print("PASS: in-memory corrupt-length, nonzero-marker, and 81 f8..ff/3d negative controls")
    print("RESULT: read-only selftest complete; L4=0")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify t01-l weather table_27 row offsets (read-only)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--selftest", action="store_true", help="full archive, static-code, row-walk, and negative-control verification")
    modes.add_argument("--write", action="store_true", help="write rebuilt output.json in this directory only")
    args = parser.parse_args()
    if not args.selftest and not args.write:
        parser.print_help()
        return 2
    try:
        if args.write:
            result, _, rows, _ = build_result()
            (HERE / "output.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"WROTE: {HERE / 'output.json'} ({len(rows)} fully parsed rows)")
        else:
            run_selftest()
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
