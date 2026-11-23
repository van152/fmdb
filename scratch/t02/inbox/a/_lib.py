"""Shared read-only helpers: editor.exe PE mapping, archive member access, decode."""
from __future__ import annotations

import hashlib
import importlib.util
import struct
import sys
from pathlib import Path

import capstone
import capstone.x86_const as x86

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                       # D:/tmp2b/fm24-db
EDITOR = ROOT.parent / "fm24" / "input" / "editor.exe"
OLD_DECODER = ROOT.parent / "fm24" / "scripts" / "modding_read_dbdat.py"
DB_DIR = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
T01H = ROOT / "scratch/t01/inbox/t01h/output.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PE:
    def __init__(self, data: bytes):
        self.data = data
        pe = int.from_bytes(data[0x3C:0x40], "little")
        if data[pe:pe + 4] != b"PE\0\0":
            raise SystemExit("editor.exe is not PE")
        opt = pe + 24
        machine = int.from_bytes(data[pe + 4:pe + 6], "little")
        if machine != 0x8664:
            raise SystemExit("editor.exe is not x64")
        self.base = int.from_bytes(data[opt + 24:opt + 32], "little")
        nsec = int.from_bytes(data[pe + 6:pe + 8], "little")
        table = opt + int.from_bytes(data[pe + 20:pe + 22], "little")
        self.sections = []
        for pos in range(table, table + nsec * 40, 40):
            name = data[pos:pos + 8].rstrip(b"\0").decode("ascii", "replace")
            vs, rva, raw_size, raw = struct.unpack_from("<IIII", data, pos + 8)
            self.sections.append((name, rva, vs, raw, raw_size))
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True

    def va(self, off: int) -> int:
        for _, rva, _, raw, size in self.sections:
            if raw <= off < raw + size:
                return self.base + rva + off - raw
        raise SystemExit(f"editor.exe file offset unmapped: {off:#x}")

    def off(self, v: int):
        for _, rva, _, raw, size in self.sections:
            d = v - (self.base + rva)
            if 0 <= d < size:
                return raw + d
        return None

    def ins(self, off: int):
        return next(self.md.disasm(self.data[off:off + 16], self.va(off), 1), None)

    def dis(self, off: int, size: int):
        return list(self.md.disasm(self.data[off:off + size], self.va(off)))

    def ev(self, off: int, size: int) -> dict:
        val = bytes(self.data[off:off + size])
        return {"file_offset": hex(off), "va": hex(self.va(off)), "bytes": val.hex(" ")}

    def op(self, off: int) -> dict:
        i = self.ins(off)
        assert i is not None, hex(off)
        return {**self.ev(off, i.size), "instruction": (i.mnemonic + " " + i.op_str).strip()}

    def resolve_jmp(self, off: int):
        """Follow direct-jmp thunks."""
        seen = set()
        while off not in seen:
            seen.add(off)
            i = self.ins(off)
            if i is not None and i.mnemonic == "jmp" and i.operands and \
                    i.operands[0].type == x86.X86_OP_IMM:
                t = self.off(i.operands[0].imm)
                if t is None:
                    return off
                off = t
                continue
            return off
        return off

    def qword(self, off: int) -> int:
        return int.from_bytes(self.data[off:off + 8], "little")


def load_old_decoder():
    spec = importlib.util.spec_from_file_location("t02a_old_dbdat", OLD_DECODER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def member(mod, archive: str, table: int) -> dict:
    path, packed, layout = mod._entries(db_path=DB_DIR, archive=archive)
    entry = mod._resolve_table(table, layout["entries"], path.name)
    if entry is None:
        raise SystemExit(f"table_{table} absent from {archive}")
    raw = mod._decompress_entry(packed, layout["data_base"], entry)
    absolute = layout["data_base"] + entry["offset"]
    return {
        "archive": archive,
        "path": path.as_posix(),
        "archive_sha256": sha256(packed),
        "member": entry["path"],
        "member_archive_file_offset": hex(absolute),
        "member_archive_file_offset_bytes": packed[absolute:absolute + 16].hex(" "),
        "member_packed_bytes": entry["packed_size"],
        "payload_bytes": len(raw),
        "payload_sha256": sha256(raw),
        "payload_header": raw[:14].hex(" "),
        "payload_footer": {"offset": hex(len(raw) - 8), "bytes": raw[-8:].hex(" ")},
        "count": int.from_bytes(raw[8:12], "little"),
        "_raw": raw,
    }
