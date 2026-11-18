#!/usr/bin/env python3
"""Read-only FM24 table_21 stadium row / editor.exe slot verifier.

From the fm24-db root:
  py -V:3.12 -I -B scratch/t01/inbox/t01m/verify.py --help
  py -V:3.12 -I -B scratch/t01/inbox/t01m/verify.py --selftest
  py -V:3.12 -I -B scratch/t01/inbox/t01m/verify.py --write

--selftest reads both database archives, the frozen evidence snapshot, editor.exe,
and output.json. --write only creates/replaces this directory's output.json.
No game/editor/IDA is launched; no input file is written.
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
EDITOR = ROOT.parent / "fm24" / "input" / "editor.exe"
OLD_DECODER = ROOT.parent / "fm24" / "scripts" / "modding_read_dbdat.py"
DB_DIR = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
MANIFEST = ROOT / "evidence/MANIFEST.json"
OLD_TABLES = ROOT / "evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md"
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
T01H = HERE.parents[0] / "t01h" / "output.json"
EXPECTED_EDITOR_SHA = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXPECTED_CLIENT_SHA = "5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1"
EXPECTED_OLD_TABLES_SHA = "453c0f0be8326dcb966b15632b56194a0982dbdfa9d5e169c9fdb2a2def572e7"
EXPECTED_MASTER_SHA = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
COUNT = 48_413
CLIENT_STRIDE = 38
SERVER_STRIDE = 181
CLIENT_HEADER = SERVER_HEADER = 14
FOOTER_SIZE = 8
READER_START = 0x1183F30
READER_RET = 0x11844DD
READER_WINDOW = 0x800
GETTER_START = 0x1185EB0
GETTER_END = 0x1189250  # immediately before Stadium vtable slot 3's entry at 0x1189260
SERVER_COMMON_START = 0x11843B6

# {field code: getter compare, first member read(s), reader destination, reader width,
# reader stream call, row-relative offset, width, storage-domain}. All addresses are
# editor.exe file offsets; exact bytes and VAs are emitted by the verifier.
FIELD_SPECS = [
    ("Scpy", 0x118688C, [0x1186898], 0x6C, 0x1183F5A, 0x1183F65, 0x1183F6E, 0, 4, "server_prefix"),
    ("Sscy", 0x1186840, [0x118684C], 0x70, 0x1183F71, 0x1183F7C, 0x1183F85, 4, 4, "server_prefix"),
    ("Secy", 0x11867F4, [0x1186800], 0x7C, 0x1183F88, 0x1183F93, 0x1183F99, 8, 4, "server_prefix"),
    ("Scas", 0x1186283, [0x1186ECA], 0x78, 0x1183F9C, 0x1183FA7, 0x1183FAD, 12, 4, "server_prefix"),
    ("Sowi", 0x11864E8, [0x11864F4], 0x80, 0x1183FB4, 0x1183FBE, 0x1183FC7, 16, 4, "server_prefix"),
    ("Sdcy", 0x1186112, [0x1186E42], 0x9A, 0x1183FD8, 0x1183FE2, 0x1183FEB, 20, 1, "server_prefix"),
    ("Spln", 0x1186307, [0x1186F2A], 0x88, 0x1184010, 0x118401A, 0x1184023, 25, 2, "server_prefix"),
    ("Spwd", 0x1186BB2, [0x1187611], 0x8A, 0x1184034, 0x118403E, 0x1184047, 27, 2, "server_prefix"),
    ("SlIM", 0x1186AAE, [0x1186ABA], 0x8C, 0x1184058, 0x1184062, 0x118406B, 29, 2, "server_prefix"),
    ("SwIM", 0x11866CF, [0x11866DB], 0x8E, 0x118407C, 0x1184086, 0x118408F, 31, 2, "server_prefix"),
    ("Spty", 0x1186603, [0x118660F], 0x9D, 0x11840A0, 0x11840AA, 0x11840B3, 33, 1, "server_prefix"),
    ("Sste", 0x1186B0D, [0x11875A4], 0x9F, 0x11840C4, 0x11840CE, 0x11840D7, 34, 1, "server_prefix"),
    ("Senv", 0x1186514, [0x118705B], 0xA0, 0x11840E8, 0x11840F2, 0x11840FB, 35, 1, "server_prefix"),
    ("Sitg", 0x1186AA2, [0x1187567], 0x9B, 0x118410C, 0x1184116, 0x118411F, 36, 1, "server_prefix"),
    ("Scti", 0x1186B5D, [0x11875DC], 0x50, 0x1184427, 0x118442E, 0x1184437, 3, 4, "common_tail"),
    ("Sptc", 0x11865F7, [0x118710D], 0x98, 0x1184465, 0x118446F, 0x1184478, 11, 2, "common_tail"),
    ("Slat", 0x1186330, [0x1186F74], 0x60, 0x1184495, 0x118449C, 0x11844A5, 17, 4, "common_tail"),
    ("Slon", 0x118633C, [0x1186348], 0x64, 0x11844B2, 0x11844B9, 0x11844C2, 21, 4, "common_tail"),
]

# Five stadiums cover the four frozen L2 city anchors plus a first-row control.
SAMPLES = {
    0: {"name": "first-row control", "city_rdui": 1039},
    67: {"name": "Anfield", "city_rdui": 1061, "dbid": 676, "capacity": 50109, "city": "Liverpool"},
    71: {"name": "Old Trafford", "city_rdui": 1075, "dbid": 680, "capacity": 74031, "city": "Manchester"},
    430: {"name": "Santiago Bernabéu", "city_rdui": 316, "dbid": 1056, "capacity": 81044, "city": "Madrid"},
    12048: {"name": "Munich Stadium", "city_rdui": 540, "dbid": 8700726, "capacity": 75000, "seating_capacity": 54511, "city": "München"},
}


class Failure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_old_decoder():
    require(OLD_DECODER.is_file(), f"read-only decoder unavailable: {OLD_DECODER}")
    spec = importlib.util.spec_from_file_location("t01m_old_dbdat_reader", OLD_DECODER)
    require(spec is not None and spec.loader is not None, "cannot load the frozen-workspace decoder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PE:
    def __init__(self, data: bytes):
        self.data = data
        pe = int.from_bytes(data[0x3C:0x40], "little")
        require(data[pe:pe + 6] == b"PE\0\0\x64\x86", "editor.exe is not x64 PE")
        opt = pe + 24
        require(int.from_bytes(data[opt:opt + 2], "little") == 0x20B, "editor.exe is not PE32+")
        self.base = int.from_bytes(data[opt + 24:opt + 32], "little")
        table = opt + int.from_bytes(data[pe + 20:pe + 22], "little")
        self.sections = []
        for pos in range(table, table + int.from_bytes(data[pe + 6:pe + 8], "little") * 40, 40):
            name = data[pos:pos + 8].rstrip(b"\0").decode("ascii", "replace")
            vs, rva, raw_size, raw = struct.unpack_from("<IIII", data, pos + 8)
            self.sections.append((name, rva, vs, raw, raw_size))
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True

    def va(self, off: int) -> int:
        for _, rva, _, raw, size in self.sections:
            if raw <= off < raw + size:
                return self.base + rva + off - raw
        raise Failure(f"editor.exe file offset is unmapped: {off:#x}")

    def off(self, va: int) -> int | None:
        for _, rva, _, raw, size in self.sections:
            delta = va - (self.base + rva)
            if 0 <= delta < size:
                return raw + delta
        return None

    def ev(self, off: int, size: int) -> dict:
        value = bytes(self.data[off:off + size])
        require(len(value) == size, f"short editor.exe read at {off:#x}")
        return {"file": "editor.exe", "file_offset": hex(off), "va": hex(self.va(off)),
                "bytes": value.hex(" ")}

    def ins(self, off: int):
        return next(self.md.disasm(self.data[off:off + 15], self.va(off), 1), None)

    def op(self, off: int, expected: str | None = None) -> dict:
        i = self.ins(off)
        require(i is not None, f"no instruction at editor.exe@{off:#x}")
        text = (i.mnemonic + " " + i.op_str).strip()
        require(expected is None or text == expected,
                f"editor.exe@{off:#x}: {text!r} != {expected!r}")
        return {**self.ev(off, i.size), "instruction": text}

    def disasm(self, off: int, size: int):
        return list(self.md.disasm(self.data[off:off + size], self.va(off)))

    def direct_target_off(self, instruction):
        if instruction is None or not instruction.operands or instruction.operands[0].type != x86.X86_OP_IMM:
            return None
        return self.off(instruction.operands[0].imm)


def decoded_member_disp(ins, expected: int, base_names=("rbx",)) -> bool:
    for operand in ins.operands:
        if operand.type == x86.X86_OP_MEM and ins.reg_name(operand.mem.base) in base_names:
            if (operand.mem.disp & 0xFFFFFFFFFFFFFFFF) == expected:
                return True
    return False


def source_entry(mod, archive: str) -> dict:
    path, packed, layout = mod._entries(db_path=DB_DIR, archive=archive)
    entry = mod._resolve_table(21, layout["entries"], path.name)
    raw = mod._decompress_entry(packed, layout["data_base"], entry)
    absolute = layout["data_base"] + entry["offset"]
    return {
        "archive": archive,
        "path": path.as_posix(),
        "archive_bytes": len(packed),
        "archive_sha256": sha256(packed),
        "member": entry["path"],
        "member_archive_file_offset": hex(absolute),
        "member_archive_file_offset_bytes": packed[absolute:absolute + 16].hex(" "),
        "member_packed_bytes": entry["packed_size"],
        "member_payload_bytes": len(raw),
        "member_payload_sha256": sha256(raw),
        "payload_header": {"payload_offset": "0x0", "bytes": raw[:14].hex(" ")},
        "payload_footer": {"payload_offset": hex(len(raw) - 8), "bytes": raw[-8:].hex(" ")},
        "_packed": packed,
        "_raw": raw,
    }


def payload_ev(source: dict, payload_offset: int, size: int) -> dict:
    raw = source["_raw"]
    value = raw[payload_offset:payload_offset + size]
    require(len(value) == size, f"short {source['archive']} payload at {payload_offset:#x}")
    return {"file": source["member"], "file_offset_domain": "decompressed member",
            "payload_offset": hex(payload_offset), "bytes": value.hex(" ")}


def load_manifest_hashes() -> dict:
    manifest = read_json(MANIFEST)
    expected = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    refs = ["evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md",
            "evidence/fm24/reports/editor_schema/master.json"]
    checked = {}
    for rel in refs:
        got = sha256((ROOT / rel).read_bytes())
        require(got == expected.get(rel), f"frozen manifest mismatch for {rel}")
        checked[rel] = got
    require(checked[refs[0]] == EXPECTED_OLD_TABLES_SHA, "old table snapshot SHA differs")
    require(checked[refs[1]] == EXPECTED_MASTER_SHA, "master.json snapshot SHA differs")
    return checked


def getter_evidence(pe: PE, code: str, cmp_off: int, access_offsets: list[int], obj_off: int) -> dict:
    compare = pe.ins(cmp_off)
    require(compare is not None and compare.mnemonic == "cmp", f"{code}: missing getter cmp")
    imm = next((o.imm & 0xFFFFFFFF for o in compare.operands if o.type == x86.X86_OP_IMM), None)
    require(imm == int.from_bytes(code.encode("ascii"), "big"),
            f"{code}: getter compare immediate does not match 4CC")
    branch = pe.ins(cmp_off + compare.size)
    require(branch is not None and branch.mnemonic in ("je", "jne"),
            f"{code}: no equality/fallthrough branch after cmp")
    handler = (pe.direct_target_off(branch) if branch.mnemonic == "je"
               else cmp_off + compare.size + branch.size)
    require(handler is not None, f"{code}: getter dispatch target unmapped")
    accesses = []
    for access_off in access_offsets:
        ins = pe.ins(access_off)
        require(ins is not None and decoded_member_disp(ins, obj_off, ("rdi",)),
                f"{code}: getter at {access_off:#x} does not access object+{obj_off:#x}")
        # The direct case target/fallthrough must lead to the recorded member access.
        require(handler <= access_off < handler + 0x80,
                f"{code}: member access is not in its equality handler")
        accesses.append(pe.op(access_off))
    return {"schema_4cc": code, "getter_compare": pe.op(cmp_off),
            "equality_branch": pe.op(cmp_off + compare.size),
            "handler_file_offset": hex(handler), "object_offset": hex(obj_off),
            "member_accesses": accesses}


def reader_transfer(pe: PE, code: str, dest_off: int, width_off: int,
                    call_off: int, obj_off: int, width: int) -> dict:
    dest = pe.ins(dest_off)
    width_ins = pe.ins(width_off)
    call = pe.ins(call_off)
    require(dest is not None and dest.mnemonic == "lea" and
            decoded_member_disp(dest, obj_off, ("rbx",)),
            f"{code}: reader destination is not object+{obj_off:#x}")
    require(width_ins is not None and width_ins.mnemonic == "mov" and
            width_ins.reg_name(width_ins.operands[0].reg) == "r8d" and
            width_ins.operands[1].type == x86.X86_OP_IMM and
            (width_ins.operands[1].imm & 0xFFFFFFFF) == width,
            f"{code}: reader width differs from {width}")
    require(call is not None and call.mnemonic == "call" and call.bytes == bytes.fromhex("ff 50 28"),
            f"{code}: reader stream call is not [rax+0x28]")
    return {"object_offset": hex(obj_off), "destination": pe.op(dest_off),
            "width": width, "width_instruction": pe.op(width_off),
            "stream_call": pe.op(call_off)}


def archive_rows(client: dict, server: dict):
    c, s = client["_raw"], server["_raw"]
    require(c[:6] == b"\x03\x01tad." and s[:6] == b"\x03\x01tad.", "table_21 payload magic mismatch")
    cc, sc = int.from_bytes(c[8:12], "little"), int.from_bytes(s[8:12], "little")
    require(cc == sc == COUNT, f"table_21 count mismatch: client={cc}, server={sc}")
    require(len(c) == CLIENT_HEADER + COUNT * CLIENT_STRIDE + FOOTER_SIZE,
            "client table_21 fixed-stride arithmetic failed")
    require(len(s) == SERVER_HEADER + COUNT * SERVER_STRIDE + FOOTER_SIZE,
            "server table_21 fixed-stride arithmetic failed")
    client_rows = [c[CLIENT_HEADER + i * CLIENT_STRIDE:CLIENT_HEADER + (i + 1) * CLIENT_STRIDE]
                   for i in range(COUNT)]
    server_rows = [s[SERVER_HEADER + i * SERVER_STRIDE:SERVER_HEADER + (i + 1) * SERVER_STRIDE]
                   for i in range(COUNT)]
    require(all(len(r) == CLIENT_STRIDE for r in client_rows), "truncated client row")
    require(all(len(r) == SERVER_STRIDE for r in server_rows), "truncated server row")
    return client_rows, server_rows


def build() -> dict:
    frozen = load_manifest_hashes()
    master_bytes = MASTER.read_bytes()
    master = json.loads(master_bytes)
    schema = master["entities"]["stadium.xml"][0]
    fields = {entry["field"]: entry for entry in schema["fields"]}
    require(schema["id"] == "stad" and len(fields) == 60, "master stadium schema differs")
    for spec in FIELD_SPECS:
        require(spec[0] in fields, f"mapped 4CC {spec[0]} absent from stadium.xml#stad")

    mod = load_old_decoder()
    client = source_entry(mod, "client_db.dat")
    server = source_entry(mod, "server_db.dat")
    require(client["archive_sha256"] == EXPECTED_CLIENT_SHA, "client_db.dat SHA differs from t01l frozen input")
    client_rows, server_rows = archive_rows(client, server)

    identity_ok = 0
    repeated_client = set()
    refs_ok = 0
    splice_ok = 0
    optional_flag_clear = sum((row[0] & 0x10) == 0 for row in client_rows)
    require(optional_flag_clear == COUNT, "client common-tail optional-helper flag was set in one or more rows")
    for idx, (cr, sr) in enumerate(zip(client_rows, server_rows)):
        crdui = int.from_bytes(cr[25:29], "little")
        cduni_lo = int.from_bytes(cr[29:33], "little")
        cduni_hi = int.from_bytes(cr[33:37], "little")
        srdui = int.from_bytes(sr[168:172], "little")
        sduni_lo = int.from_bytes(sr[172:176], "little")
        sduni_hi = int.from_bytes(sr[176:180], "little")
        city = int.from_bytes(cr[3:7], "little")
        identity_ok += crdui == idx and srdui == idx and cduni_lo == cduni_hi and sduni_lo == sduni_hi
        repeated_client.add(cduni_lo)
        refs_ok += city < 56_293
        splice_ok += sr[143:181] == cr
    require(identity_ok == COUNT, f"identity/ordinal validation {identity_ok}/{COUNT}")
    require(len(repeated_client) == COUNT, "client repeated-u32 DUNI is not unique")
    require(refs_ok == COUNT, f"city rdui legality {refs_ok}/{COUNT}")
    require(splice_ok == COUNT, f"server[143:181] == client validation {splice_ok}/{COUNT}")

    editor_bytes = EDITOR.read_bytes()
    editor_sha = sha256(editor_bytes)
    require(editor_sha == EXPECTED_EDITOR_SHA, "editor.exe SHA differs from frozen provenance")
    pe = PE(editor_bytes)

    t01h = read_json(T01H)
    census = next(x for x in t01h["census"] if x.get("type_id") == 21)
    static_reader = census["constructor_classes"][0]["slot19_reader"]
    require(static_reader["entry_file_offset"] == hex(READER_START) and
            static_reader["width_count"] == 77, "t01h type-21 reader anchor mismatch")
    reader_window = pe.disasm(READER_START, READER_WINDOW)
    body = []
    for ins in reader_window:
        body.append(ins)
        if ins.mnemonic == "ret":
            break
    require(body and pe.off(body[-1].address) == READER_RET, "reader function first-ret boundary changed")

    def is_width(ins):
        return (ins.mnemonic == "mov" and len(ins.operands) == 2 and
                ins.operands[0].type == x86.X86_OP_REG and
                ins.reg_name(ins.operands[0].reg) == "r8d" and
                ins.operands[1].type == x86.X86_OP_IMM)

    def is_stream_call(ins):
        return (ins.mnemonic == "call" and len(ins.operands) == 1 and
                ins.operands[0].type == x86.X86_OP_MEM and ins.operands[0].mem.disp == 0x28)

    widths_body = [i for i in body if is_width(i)]
    calls_body = [i for i in body if is_stream_call(i)]
    entry_window_widths = [i for i in reader_window if is_width(i)]
    entry_window_calls = [i for i in reader_window if is_stream_call(i)]
    require((len(widths_body), sum(i.operands[1].imm for i in widths_body), len(calls_body)) == (34, 74, 34),
            "reader bounded direct-width/call count differs")
    prefix_first_37 = [i for i in widths_body if pe.off(i.address) < 0x1184133]
    require((len(prefix_first_37), sum(i.operands[1].imm for i in prefix_first_37)) == (15, 37),
            "first 37 server-prefix bytes no longer match 15 direct transfers")
    require((len(entry_window_widths), len(entry_window_calls)) == (34, 34),
            "entry-window width/call count differs")

    census_window_details = []
    census_width_total = census_call_total = 0
    for window in static_reader["functions_scanned"]:
        win_off = int(window["file_offset"], 16)
        win_ins = pe.disasm(win_off, READER_WINDOW)
        win_widths = [i for i in win_ins if is_width(i)]
        win_calls = [i for i in win_ins if i.mnemonic == "call" and i.operands and (
            (i.operands[0].type == x86.X86_OP_MEM and i.operands[0].mem.disp == 0x28) or
            (i.operands[0].type == x86.X86_OP_REG and i.reg_name(i.operands[0].reg) == "rax"))]
        census_width_total += len(win_widths)
        census_call_total += len(win_calls)
        census_window_details.append({
            "scan_start_file_offset": hex(win_off), "role_from_t01h": window["role"],
            "scan_bytes": READER_WINDOW, "static_width_count": len(win_widths),
            "static_width_immediate_sum_not_a_row_length": sum(i.operands[1].imm & 0xFFFFFFFF for i in win_widths),
            "stream_call_count": len(win_calls),
            "width_instructions": [pe.op(pe.off(i.address)) for i in win_widths],
        })
    require((census_width_total, census_call_total) == (77, 76),
            "t01h combined entry/helper scan counts not reproduced")

    branch_test = pe.op(0x1183F51, "test bpl, bpl")
    branch = pe.ins(0x1183F54)
    require(branch is not None and branch.mnemonic == "je" and
            pe.direct_target_off(branch) == SERVER_COMMON_START,
            "client/common-tail mode branch target differs")
    common_sites = [i for i in widths_body if pe.off(i.address) >= SERVER_COMMON_START]
    require(len(common_sites) == 7 and sum(i.operands[1].imm for i in common_sites) == 21,
            "common-tail direct widths differ")
    prefix_sites = [i for i in widths_body if pe.off(i.address) < SERVER_COMMON_START]
    require(len(prefix_sites) == 27 and sum(i.operands[1].imm for i in prefix_sites) == 53,
            "server-prefix direct widths differ")

    # Exact full-register raw scan (81 f8..ff) plus EAX's 3d immediate form.
    getter_bytes = editor_bytes[GETTER_START:GETTER_END]
    getter_decoded = {pe.off(i.address): i for i in pe.disasm(GETTER_START, GETTER_END - GETTER_START)}
    reg_names = {0xF8: "eax", 0xF9: "ecx", 0xFA: "edx", 0xFB: "ebx",
                 0xFC: "esp", 0xFD: "ebp", 0xFE: "esi", 0xFF: "edi"}
    raw_reg_hits, raw_eax_hits, schema_cmp_hits = [], [], []
    schema_codes = {int.from_bytes(code.encode("ascii"), "big"): code for code in fields}
    for pos in range(GETTER_START, GETTER_END):
        if pos + 6 <= GETTER_END and editor_bytes[pos] == 0x81 and editor_bytes[pos + 1] in reg_names:
            imm = int.from_bytes(editor_bytes[pos + 2:pos + 6], "little")
            decoded = getter_decoded.get(pos)
            valid = bool(decoded and decoded.mnemonic == "cmp" and decoded.size == 6 and
                         decoded.operands[-1].type == x86.X86_OP_IMM and
                         (decoded.operands[-1].imm & 0xFFFFFFFF) == imm)
            hit = {**pe.ev(pos, 6), "register": reg_names[editor_bytes[pos + 1]],
                   "imm32": hex(imm), "ascii_be": imm.to_bytes(4, "big").decode("latin1"),
                   "decoded_instruction_boundary": valid}
            raw_reg_hits.append(hit)
            if valid and imm in schema_codes:
                schema_cmp_hits.append({**hit, "schema_4cc": schema_codes[imm],
                                        "instruction": pe.op(pos)["instruction"]})
        if pos + 5 <= GETTER_END and editor_bytes[pos] == 0x3D:
            imm = int.from_bytes(editor_bytes[pos + 1:pos + 5], "little")
            decoded = getter_decoded.get(pos)
            valid = bool(decoded and decoded.mnemonic == "cmp" and decoded.size == 5 and
                         decoded.operands[-1].type == x86.X86_OP_IMM and
                         (decoded.operands[-1].imm & 0xFFFFFFFF) == imm)
            raw_eax_hits.append({**pe.ev(pos, 5), "register": "eax", "imm32": hex(imm),
                                 "ascii_be": imm.to_bytes(4, "big").decode("latin1"),
                                 "decoded_instruction_boundary": valid})
    require(any(x["schema_4cc"] == "Scpy" and x["register"] == "ebx" for x in schema_cmp_hits),
            "full-register getter scan missed cmp ebx, Scpy")
    scanned_schema_codes = {x["schema_4cc"] for x in schema_cmp_hits}
    require(all(spec[0] in scanned_schema_codes for spec in FIELD_SPECS),
            "full-register getter scan missed a mapped 4CC compare")
    require(not any(x["ascii_be"] == "Scpy" and x["decoded_instruction_boundary"] for x in raw_eax_hits),
            "EAX-only negative control unexpectedly found Scpy")

    # Check vtable slot 2 is the getter entry; its next slot is not merged into the scan.
    stadium_vptr = 0x188D1D8
    slot2_ptr_off = stadium_vptr + 2 * 8
    slot2_va = int.from_bytes(editor_bytes[slot2_ptr_off:slot2_ptr_off + 8], "little")
    require(pe.off(slot2_va) == GETTER_START, "Stadium vtable slot 2 no longer points at getter window")
    slot3_va = int.from_bytes(editor_bytes[stadium_vptr + 3 * 8:stadium_vptr + 4 * 8], "little")
    require(pe.off(slot3_va) == 0x1189260, "Stadium vtable slot 3 boundary changed")

    row_offset_map = []
    for code, cmp_off, accesses, obj_off, dest_off, width_off, call_off, row_off, width, domain in FIELD_SPECS:
        getter = getter_evidence(pe, code, cmp_off, accesses, obj_off)
        reader = reader_transfer(pe, code, dest_off, width_off, call_off, obj_off, width)
        if domain == "server_prefix":
            client_offset = None
            server_offset = row_off
        else:
            client_offset = row_off
            server_offset = 143 + row_off
        row_offset_map.append({
            "4cc": code, "schema_name": fields[code].get("name"),
            "schema_type": fields[code].get("type"),
            "L3": ("conditional getter fallback/backing-slot association; excluded from acceptance count"
                   if code in ("Spln", "Spwd") else "editor.exe getter + virtual reader"),
            "reader_branch_domain": domain, "object_offset": hex(obj_off), "width": width,
            "client_row_offset": client_offset, "server_row_offset": server_offset,
            "getter": getter, "reader_transfer": reader,
            "payload_sample_bytes": {},
        })

    # The four-byte helper at object+0x34 sits between Sptc and coordinate reads.
    helper_call = pe.ins(0x1184488)
    require(helper_call is not None and helper_call.mnemonic == "call" and
            helper_call.operands[0].type == x86.X86_OP_IMM and
            helper_call.operands[0].imm == 0x140DB8980, "common-tail 4-byte helper call differs")
    helper_thunk = pe.ins(0xDB7F80)
    require(helper_thunk is not None and helper_thunk.mnemonic == "jmp", "4-byte helper thunk missing")
    helper_body_off = pe.off(helper_thunk.operands[0].imm)
    require(helper_body_off == 0x39DD7B0, "4-byte helper body target changed")
    helper_width_off, helper_call_off = 0x39DD7C8, 0x39DD7D4
    helper_width = pe.ins(helper_width_off)
    helper_stream = pe.ins(helper_call_off)
    require(helper_width is not None and is_width(helper_width) and helper_width.operands[1].imm == 4,
            "object+0x34 helper is not a 4-byte stream read")
    require(helper_stream is not None and is_stream_call(helper_stream), "4-byte helper stream call missing")
    helper_evidence = {
        "reader_callsite": pe.op(0x1184488),
        "object_destination": pe.op(0x1184481),
        "helper_thunk": pe.op(0xDB7F80),
        "helper_width": pe.op(helper_width_off),
        "helper_stream_call": pe.op(helper_call_off),
    }
    common_trace = [
        {"row_offset": 0, "object_offset": "0xa6", "width": 2, "site": reader_transfer(pe, "common+0", 0x11843BA, 0x11843C4, 0x11843D0, 0xA6, 2)},
        {"row_offset": 2, "object_offset": "0xa8", "width": 1, "site": reader_transfer(pe, "common+2", 0x1184403, 0x118440D, 0x1184416, 0xA8, 1)},
        {"row_offset": 3, "object_offset": "0x50", "width": 4, "site": reader_transfer(pe, "common+3", 0x1184427, 0x118442E, 0x1184437, 0x50, 4)},
        {"row_offset": 7, "object_offset": "0x58", "width": 4, "site": reader_transfer(pe, "common+7", 0x1184448, 0x118444F, 0x1184458, 0x58, 4)},
        {"row_offset": 11, "object_offset": "0x98", "width": 2, "site": reader_transfer(pe, "common+11", 0x1184465, 0x118446F, 0x1184478, 0x98, 2)},
        {"row_offset": 13, "object_offset": "0x34", "width": 4, "site": helper_evidence},
        {"row_offset": 17, "object_offset": "0x60", "width": 4, "site": reader_transfer(pe, "common+17", 0x1184495, 0x118449C, 0x11844A5, 0x60, 4)},
        {"row_offset": 21, "object_offset": "0x64", "width": 4, "site": reader_transfer(pe, "common+21", 0x11844B2, 0x11844B9, 0x11844C2, 0x64, 4)},
    ]
    require(sum(item["width"] for item in common_trace) == 25,
            "client/common reader body no longer spans row+0..24")
    flag_ins = pe.op(0x11843DD, "test byte ptr [rsi], 0x10")
    optional_name_call = pe.op(0x11843EF)

    samples = []
    for idx, anchor in SAMPLES.items():
        cr, sr = client_rows[idx], server_rows[idx]
        city = int.from_bytes(cr[3:7], "little")
        rdui = int.from_bytes(cr[25:29], "little")
        duni = int.from_bytes(cr[29:37], "little")
        require(city == anchor["city_rdui"], f"city anchor mismatch at row {idx}")
        require(rdui == idx, f"row sequence anchor mismatch at row {idx}")
        require(duni & 0xFFFFFFFF == duni >> 32, f"DUNI repeated-u32 mismatch at row {idx}")
        require(sr[143:181] == cr, f"server suffix differs at sample row {idx}")
        require(cr[0] & 0x10 == 0, f"optional helper flag is set in client row {idx}")
        field_values = {}
        for item in row_offset_map:
            row_data = sr if item["reader_branch_domain"] == "server_prefix" else cr
            off = item["server_row_offset"] if item["reader_branch_domain"] == "server_prefix" else item["client_row_offset"]
            field_values[item["4cc"]] = {
                "row_offset": off,
                "bytes": row_data[off:off + item["width"]].hex(" "),
            }
            item["payload_sample_bytes"][str(idx)] = payload_ev(
                server if item["reader_branch_domain"] == "server_prefix" else client,
                (SERVER_HEADER + idx * SERVER_STRIDE if item["reader_branch_domain"] == "server_prefix" else CLIENT_HEADER + idx * CLIENT_STRIDE) + off,
                item["width"])
        capacity = int.from_bytes(sr[0:4], "little")
        seating = int.from_bytes(sr[4:8], "little")
        require(capacity == anchor.get("capacity", capacity), f"capacity anchor mismatch row {idx}")
        if "seating_capacity" in anchor:
            require(seating == anchor["seating_capacity"], f"seating capacity anchor mismatch row {idx}")
        samples.append({
            "row_index": idx, "anchor": anchor["name"],
            "client_payload_row_offset": hex(CLIENT_HEADER + idx * CLIENT_STRIDE),
            "server_payload_row_offset": hex(SERVER_HEADER + idx * SERVER_STRIDE),
            "city_rdui": city, "row_sequence": rdui, "duni_repeated_u32": duni & 0xFFFFFFFF,
            "Scpy_candidate": capacity, "Sscy_candidate": seating,
            "client_row_bytes": payload_ev(client, CLIENT_HEADER + idx * CLIENT_STRIDE, CLIENT_STRIDE),
            "server_row_prefix_0_36": payload_ev(server, SERVER_HEADER + idx * SERVER_STRIDE, 37),
            "field_values": field_values,
        })

    # Old snapshot content is not adopted as fresh proof; it is a frozen comparator.
    old_text = OLD_TABLES.read_text(encoding="utf-8")
    for anchor_text in ["Anfield | 676 / 67", "Old Trafford | 680 / 71",
                        "Santiago Bernabéu | 1,056 / 430", "Munich Stadium"]:
        require(anchor_text in old_text, f"frozen city anchor missing: {anchor_text}")
    old_anchor_checks = [
        {"name": "Anfield", "stadium_row": 67, "client_Scti_rdui": 1061, "table_2_city": "Liverpool",
         "server_Scpy_candidate": 50109, "expected_row_offsets": {"Scti": 146, "Scpy": 0}},
        {"name": "Old Trafford", "stadium_row": 71, "client_Scti_rdui": 1075, "table_2_city": "Manchester",
         "server_Scpy_candidate": 74031, "negative_capacity_fact": "74031 != 74140",
         "expected_row_offsets": {"Scti": 146, "Scpy": 0}},
        {"name": "Santiago Bernabéu", "stadium_row": 430, "client_Scti_rdui": 316, "table_2_city": "Madrid",
         "server_Scpy_candidate": 81044, "expected_row_offsets": {"Scti": 146, "Scpy": 0}},
        {"name": "Munich Stadium", "stadium_row": 12048, "client_Scti_rdui": 540, "table_2_city": "München",
         "server_Scpy_candidate": 75000, "server_Sscy_candidate": 54511,
         "expected_row_offsets": {"Scti": 146, "Scpy": 0, "Sscy": 4}},
    ]
    for a in old_anchor_checks:
        cr, sr = client_rows[a["stadium_row"]], server_rows[a["stadium_row"]]
        require(int.from_bytes(cr[3:7], "little") == a["client_Scti_rdui"],
                f"old Scti anchor differs: {a['name']}")
        require(int.from_bytes(sr[0:4], "little") == a["server_Scpy_candidate"],
                f"old capacity sample differs: {a['name']}")

    # Negative controls: wrong stride, shifted Scti, wrong server/client splice,
    # and an EAX-only getter scan that misses the actual EBX 4CC compare.
    wrong_stride_rejected = (CLIENT_HEADER + COUNT * 181 + FOOTER_SIZE) != len(client["_raw"])
    shifted_scti = int.from_bytes(client_rows[67][4:8], "little")
    shifted_scti_rejected = shifted_scti != SAMPLES[67]["city_rdui"]
    wrong_splice_rejected = server_rows[67][142:180] != client_rows[67]
    require(wrong_stride_rejected and shifted_scti_rejected and wrong_splice_rejected,
            "one or more negative controls failed")

    # Stable evidence payloads (remove private byte buffers before JSON encoding).
    sources = {
        "database": {
            "client": {k: v for k, v in client.items() if not k.startswith("_")},
            "server": {k: v for k, v in server.items() if not k.startswith("_")},
        },
        "binary": {"file": EDITOR.as_posix(), "bytes": len(editor_bytes),
                   "sha256": editor_sha, "evidence_level": "L3 static"},
        "frozen_snapshots": frozen,
        "python": sys.version.split()[0], "capstone": capstone.__version__,
        "read_only": True,
    }
    getter_window_info = {
        "vtable_pointer": pe.ev(stadium_vptr, 8),
        "slot2_getter_pointer": pe.ev(slot2_ptr_off, 8),
        "slot2_entry_file_offset": hex(GETTER_START),
        "slot3_pointer": pe.ev(stadium_vptr + 3 * 8, 8),
        "scan_window_file_offsets": [hex(GETTER_START), hex(GETTER_END)],
        "scan_rule": "raw 81 f8..ff (all register forms) and 3d (EAX); decoded-boundary validation",
        "raw_81_register_hits": raw_reg_hits,
        "raw_3d_eax_hits": raw_eax_hits,
        "schema_4cc_compare_hits": schema_cmp_hits,
    }
    reader_info = {
        "entry": pe.ev(READER_START, 16),
        "first_ret": pe.op(READER_RET, "ret"),
        "first_ret_file_offset": hex(READER_RET),
        "census_each_scan_window_bytes": READER_WINDOW,
        "census_combined_width_instructions_77": census_width_total,
        "census_combined_stream_calls_76": census_call_total,
        "entry_window_width_instructions": len(entry_window_widths),
        "direct_callee_windows_width_sites": census_width_total - len(entry_window_widths),
        "t01h_scan_windows": census_window_details,
        "bounded_reader_width_instructions": len(widths_body),
        "bounded_reader_direct_width_sum_bytes": sum(i.operands[1].imm for i in widths_body),
        "bounded_reader_stream_calls": len(calls_body),
        "branch_parameter": {"test": branch_test, "conditional_jump": pe.op(0x1183F54),
                              "false_target_file_offset": hex(SERVER_COMMON_START),
                              "interpretation": "false skips server-prefix transfer block and enters shared client/server tail"},
        "server_prefix_direct_site_count": len(prefix_sites),
        "server_prefix_direct_width_sum_bytes": sum(i.operands[1].imm for i in prefix_sites),
        "first_37_server_prefix_direct_site_count": len(prefix_first_37),
        "first_37_server_prefix_direct_width_sum_bytes": sum(i.operands[1].imm for i in prefix_first_37),
        "common_tail_direct_site_count": len(common_sites),
        "common_tail_direct_width_sum_bytes": sum(i.operands[1].imm for i in common_sites),
        "common_client_trace": common_trace,
        "optional_payload_gate": {"test": flag_ins, "conditional_helper_call": optional_name_call,
                                   "client_rows_with_flag_0x10": COUNT - optional_flag_clear},
        "interpretation": (
            "77 is t01h's combined static mov r8d,imm count over the entry plus seven direct-callee "
            "0x800-byte scan windows, not 77 field widths in one row. The first ret is at 0x11844dd; "
            "the bounded slot-19 body has 34 width sites/34 direct stream calls (74 immediate bytes), "
            "while 43 additional immediates come from helper scan windows and may be conditional, "
            "dynamic-helper internals, or non-row candidates. "
            "The reader has a mode branch; the client/common-tail path emits 21 direct bytes plus "
            "a verified 4-byte helper, then the 12-byte identity suffix and 1-byte row tail lie "
            "outside this virtual reader body. The server direct prefix and helper/list paths are "
            "not equal to the client stride; the separate server row prefix is 143 bytes."
        ),
    }
    result = {
        "task": "t01-m stadium table_21 row offsets",
        "acceptance": {
            "met": True,
            "L3_mapped_schema_fields": sum(x["4cc"] not in ("Spln", "Spwd") for x in row_offset_map),
            "L3_field_codes": [x["4cc"] for x in row_offset_map if x["4cc"] not in ("Spln", "Spwd")],
            "conditional_getter_backing_slot_associations_not_counted": ["Spln", "Spwd"],
            "client_rows_checked": COUNT, "server_rows_checked": COUNT,
            "four_city_anchors_checked": len(old_anchor_checks),
            "five_row_samples": len(samples), "client_server_suffix_matches": splice_ok,
            "identity_rows_checked_L1": identity_ok,
            "L4": 0,
        },
        "sources": sources,
        "row_codec": {
            "client": {"header_size": CLIENT_HEADER, "count": COUNT, "stride": CLIENT_STRIDE,
                       "payload_size": len(client["_raw"]), "size_formula": f"14 + {COUNT}*38 + 8 = {len(client['_raw'])}",
                       "first_row_start": "0xe", "last_row_start": hex(CLIENT_HEADER + (COUNT - 1) * CLIENT_STRIDE),
                       "footer_size": FOOTER_SIZE},
            "server": {"header_size": SERVER_HEADER, "count": COUNT, "stride": SERVER_STRIDE,
                       "payload_size": len(server["_raw"]), "size_formula": f"14 + {COUNT}*181 + 8 = {len(server['_raw'])}",
                       "first_row_start": "0xe", "last_row_start": hex(SERVER_HEADER + (COUNT - 1) * SERVER_STRIDE),
                       "footer_size": FOOTER_SIZE, "client_suffix_start": 143,
                       "suffix_relation": "server row[143:181] == corresponding 38-byte client row",
                       "suffix_matches": splice_ok},
            "identity_and_references": {
                "client_row_sequence": {"historical_label": "rdui; E20 correction: row ordinal, not native rdui",
                                         "row_offset": 25, "width": 4, "valid_rows": COUNT,
                                         "reader_body_boundary": "slot-19 reader directly ends after common-tail row+24; identity suffix not claimed as this body's L3 transfer"},
                "client_duni": {"row_offset": 29, "width": 8, "repeated_u32_rows": COUNT,
                                "unique_low_u32": len(repeated_client)},
                "server_row_sequence": {"historical_label": "rdui in frozen L1 table; treated as ordinal here",
                                         "row_offset": 168, "width": 4, "valid_rows": COUNT},
                "server_duni": {"row_offset": 172, "width": 8, "repeated_u32_rows": COUNT},
                "Scti_city_rdui_legal_rows": refs_ok,
            },
        },
        "reader": reader_info,
        "getter_scan": getter_window_info,
        "row_offset_map": row_offset_map,
        "old_L1_anchor_crosscheck": {
            "snapshot": "evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md",
            "snapshot_sha256_manifest_verified": frozen["evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md"],
            "anchors": old_anchor_checks,
            "claim_boundary": "L1 snapshot facts remain L1; the new getter/reader field positions are L3. Old capacity labels remain candidates, including the Old Trafford mismatch.",
        },
        "five_row_samples": samples,
        "negative_controls": {
            "client_stride_181_rejected": wrong_stride_rejected,
            "Scti_shifted_by_one_byte_rejected": shifted_scti_rejected,
            "server_suffix_start_142_rejected": wrong_splice_rejected,
            "eax_only_getter_scan_misses_Scpy": True,
            "77_widths_are_not_bounded_reader_width_sites": census_width_total != len(widths_body),
        },
        "limitations": [
            "Client offsets +25..36 (row ordinal at +25, historically mislabeled rdui by the L1 table; DUNI at +29) are revalidated against all rows as L1 structure/identity. The stadium slot-19 body returns after the coordinate transfer at client row+24, so these identity slots are not upgraded to L3."
            "Only the first 37 bytes of the 143-byte server-only prefix receive field mappings here; later server-only fields/list payloads remain opaque. Spln/Spwd use conditional fallback getter paths and are excluded from the 16-field L3 acceptance count. The server row's full 181-byte stride and 143-byte prefix boundary are L1 framing, not a claim that 77 instruction widths sum to 181."
            "The Old Trafford capacity value 74,031 differs from the independent 74,140 reference and remains an explicit negative; Scpy/Sscy schema names have L3 slot evidence, while their semantic capacity validation remains candidate/L2 with the old caveat.",
            "No game/editor/IDA execution or L4 validation; all external archives are read-only and all generated files remain in this inbox directory.",
        ],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only t01-m stadium row/slot verifier")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--selftest", action="store_true", help="rebuild and compare all read-only evidence")
    action.add_argument("--write", action="store_true", help="write only this directory's output.json")
    args = parser.parse_args()
    try:
        result = build()
        output = HERE / "output.json"
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.write:
            output.write_text(encoded, encoding="utf-8")
            print(f"wrote {output}")
        else:
            require(output.is_file(), "output.json is missing; run --write first")
            existing = json.loads(output.read_text(encoding="utf-8"))
            require(existing == result, "output.json differs from rebuilt evidence")
            print("t01-m --selftest: PASS (all rows, reader/getter bytes, frozen anchors, negative controls)")
        return 0
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, IndexError, struct.error) as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
