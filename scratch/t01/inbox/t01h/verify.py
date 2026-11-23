#!/usr/bin/env python3
"""Read-only census of the editor.exe type-id factory jump table.

From the repository root:
  py -V:3.12 -I -B scratch/t01/inbox/t01h/verify.py --help
  py -V:3.12 -I -B scratch/t01/inbox/t01h/verify.py --write
  py -V:3.12 -I -B scratch/t01/inbox/t01h/verify.py --selftest

Only --write creates/replaces the colocated output.json. The PE and frozen
snapshots are opened read-only; no executable, game, editor, or IDA is started.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mmap
import struct
import sys
from contextlib import ExitStack
from pathlib import Path

try:
    import capstone
except ImportError as exc:  # do not install project dependencies
    raise SystemExit(f"capstone unavailable; do not install dependencies: {exc}")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PE_PATH = ROOT.parent / "fm24" / "input" / "editor.exe"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
MANIFEST_REL = "evidence/MANIFEST.json"
T01E_REL = "scratch/t01/t01e_vtables.json"
EXPECTED_PE = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
FACTORY_DISPATCH_INS = 0xF48B38
FACTORY_TABLE_LEA = 0xF48B45
FACTORY_TABLE_EXPECTED = 0xF49D38
FACTORY_END = 0xF49CB3
MAX_TYPE_ID = 0x49
ALLOCATOR_VA = 0x1407E58C0
T01F_REL = "scratch/t01/inbox/t01f/output.json"
T01G_REL = "scratch/t01/inbox/t01g/output.json"
FROZEN_REFS = (
    "evidence/fm24/reports/editor_schema/master.json",
    "evidence/fm24/reports/dbdat_decode/client_table_10_nation_locator.json",
    "evidence/fm24/reports/dbdat_decode/DB_SERVER_TABLES.md",
    "evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md",
    "evidence/fm24/reports/dbdat_decode/client_table_41_currency.json",
    "evidence/fm24/reports/dbdat_decode/client_table_56_structural.json",
)

# Schema-to-class correspondences are intentionally conservative. Type-id 1
# and 24 have multiple RTTI classes; their XML associations remain candidates.
EXACT_CLASS_ENTITIES = {
    "AGREEMENT": ["agrm"], "AWARD": ["awar"], "CITY": ["city"],
    "CLUB": ["club"], "COMP": ["comp"], "CONTINENT": ["cont"],
    "CURRENCY_RECORD": ["curr"], "DERBY": ["drbr"], "INJURY": ["inju"],
    "JOURNALIST": ["jour"], "LANGUAGE": ["lang"],
    "LOCAL_REGION": ["lcrg"], "MEDIA_SOURCE": ["mdso"], "NATION": ["nati"],
    "OFFICIAL": ["offc"], "PERSON": ["pers"], "PLAYER": ["play"],
    "REGION": ["regi"], "STADIUM": ["stad"], "STAGE_NAME": ["stgn"],
    "TEAM": ["team"], "WEATHER": ["weat"],
}
TYPE_ID_ENTITY_CANDIDATES = {
    1: ["agen", "jour", "nnpl", "offc", "prnm", "pers", "play"],
    24: ["c2tm", "c3tm", "c4tm", "ktfl", "team"],
}


class Failure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def u(data, off: int, n: int = 4, signed: bool = False) -> int:
    return int.from_bytes(data[off:off + n], "little", signed=signed)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PE:
    def __init__(self, path: Path, stack: ExitStack):
        self.path = path
        f = stack.enter_context(path.open("rb"))
        self.data = stack.enter_context(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ))
        digest = hashlib.sha256(self.data).hexdigest()
        require(digest == EXPECTED_PE, "editor.exe SHA-256 differs from frozen provenance")
        self.source = {"file": path.as_posix(), "bytes": len(self.data), "sha256": digest}
        pe = u(self.data, 0x3C)
        require(self.data[pe:pe + 6] == b"PE\0\0\x64\x86", "not an x64 PE")
        opt = pe + 24
        require(u(self.data, opt, 2) == 0x20B, "not PE32+")
        self.base = u(self.data, opt + 24, 8)
        section_table = opt + u(self.data, pe + 20, 2)
        self.sections = []
        for pos in range(section_table, section_table + u(self.data, pe + 6, 2) * 40, 40):
            name = self.data[pos:pos + 8].rstrip(b"\0").decode("ascii", "replace")
            vs, rva, raw_size, raw = struct.unpack_from("<IIII", self.data, pos + 8)
            self.sections.append((name, rva, vs, raw, raw_size))
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True

    def va(self, off: int) -> int:
        for _, rva, _, raw, size in self.sections:
            if raw <= off < raw + size:
                return self.base + rva + off - raw
        raise Failure(f"unmapped editor.exe file offset: {off:#x}")

    def off(self, va: int):
        for _, rva, _, raw, size in self.sections:
            delta = va - (self.base + rva)
            if 0 <= delta < size:
                return raw + delta
        return None

    def ev(self, off: int, size: int):
        actual = bytes(self.data[off:off + size])
        require(len(actual) == size, f"short read at editor.exe@{off:#x}")
        return {"file": "editor.exe", "file_offset": hex(off),
                "va": hex(self.va(off)), "bytes": actual.hex(" ")}

    def ins(self, off: int):
        if off is None or off < 0 or off >= len(self.data):
            return None
        return next(self.md.disasm(self.data[off:off + 15], self.va(off), 1), None)

    def op(self, off: int, expected: str | None = None):
        i = self.ins(off)
        require(i is not None, f"no instruction at editor.exe@{off:#x}")
        text = (i.mnemonic + " " + i.op_str).strip()
        require(expected is None or text == expected,
                f"editor.exe@{off:#x}: {text!r}, expected {expected!r}")
        return {**self.ev(off, i.size), "instruction": text}

    def rip_target(self, ins):
        ops = [x for x in ins.operands
               if x.type == capstone.x86.X86_OP_MEM and
               x.mem.base == capstone.x86_const.X86_REG_RIP]
        if len(ops) != 1:
            return None
        return self.off(ins.address + ins.size + ops[0].mem.disp)

    def direct_target(self, ins):
        if ins and ins.operands and ins.operands[0].type == capstone.x86.X86_OP_IMM:
            return ins.operands[0].imm
        return None


def manifest_hashes(root: Path):
    manifest = read_json(root / MANIFEST_REL)
    expected = {x["path"]: x["sha256"] for x in manifest["files"]}
    checked = {}
    for rel in FROZEN_REFS:
        path = root / rel
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        require(got == expected.get(rel), "frozen snapshot mismatch: " + rel)
        checked[rel] = got
    return checked


def decode_stream(pe: PE, start: int, length: int):
    if start is None:
        return []
    end = min(len(pe.data), start + length)
    return list(pe.md.disasm(pe.data[start:end], pe.va(start)))


def vtable_catalog(pe: PE):
    """Find COL-linked RTTI vptrs in the two mapped .rdata/.debug sections."""
    catalog = {}
    for name, _, _, raw, raw_size in pe.sections:
        if name not in (".rdata", ".debug"):
            continue
        stop = raw + raw_size - 8
        for pos in range(raw, stop, 8):
            col_va = u(pe.data, pos, 8)
            col_off = pe.off(col_va)
            if col_off is None or col_off + 24 > len(pe.data):
                continue
            if u(pe.data, col_off) != 1:
                continue
            sig, obj_off, cd_off, type_rva, chd_rva, self_rva = struct.unpack_from("<6I", pe.data, col_off)
            if self_rva != pe.va(col_off) - pe.base or type_rva >= 0x20000000:
                continue
            td_off = pe.off(pe.base + type_rva)
            if td_off is None or td_off + 16 >= len(pe.data):
                continue
            end = pe.data.find(b"\0", td_off + 16, min(len(pe.data), td_off + 320))
            if end < 0:
                continue
            raw_name = bytes(pe.data[td_off + 16:end + 1])
            try:
                rtti = raw_name[:-1].decode("ascii")
            except UnicodeDecodeError:
                continue
            vptr = pos + 8
            if vptr + 22 * 8 > len(pe.data):
                continue
            catalog[vptr] = {
                "vptr_off": vptr, "col_pointer_off": pos, "col_off": col_off,
                "type_name_off": td_off + 16, "name": rtti,
                "col": pe.ev(col_off, 24),
            }
    return catalog


def query_info(pe: PE, vptr: int):
    qptr_off = vptr + 7 * 8
    qva = u(pe.data, qptr_off, 8)
    qoff = pe.off(qva)
    if qoff is None:
        return {"slot7_pointer": pe.ev(qptr_off, 8), "function_file_offset": None,
                "return_value": None, "function_bytes": None}
    insns = decode_stream(pe, qoff, 32)
    ret_value = None
    eax_value = None
    for ins in insns:
        if ins.mnemonic == "mov" and ins.operands and ins.operands[0].type == capstone.x86.X86_OP_REG and ins.reg_name(ins.operands[0].reg) == "eax" and ins.operands[1].type == capstone.x86.X86_OP_IMM:
            eax_value = ins.operands[1].imm & 0xFFFFFFFF
        elif ins.mnemonic == "xor" and len(ins.operands) == 2 and all(
                x.type == capstone.x86.X86_OP_REG and ins.reg_name(x.reg) == "eax" for x in ins.operands):
            eax_value = 0
        elif ins.mnemonic == "ret":
            ret_value = eax_value
            break
    return {"slot7_pointer": pe.ev(qptr_off, 8),
            "function_file_offset": hex(qoff), "return_value": ret_value,
            "function_bytes": pe.ev(qoff, min(16, len(pe.data) - qoff))}


def follow_jumps(pe: PE, start_va: int, max_hops: int = 8):
    cur = pe.off(start_va)
    chain = []
    for _ in range(max_hops):
        if cur is None or cur in chain:
            break
        chain.append(cur)
        i = pe.ins(cur)
        if i is None or i.mnemonic != "jmp" or pe.direct_target(i) is None:
            break
        nxt = pe.off(pe.direct_target(i))
        if nxt is None:
            break
        cur = nxt
    return cur, chain


def scan_function_vptrs(pe: PE, start_va: int, catalog: dict, max_bytes: int = 0x600):
    entry, chain = follow_jumps(pe, start_va)
    found = []
    if entry is None:
        return found, entry, chain
    for ins in decode_stream(pe, entry, max_bytes):
        if ins.mnemonic == "lea" and len(ins.operands) > 1:
            target = pe.rip_target(ins)
            if target in catalog:
                found.append({"vptr_off": target, "lea_off": pe.off(ins.address),
                              "source_function_off": entry})
        if ins.mnemonic == "ret":
            break
    return found, entry, chain


def factory_cfg(pe: PE, start: int, catalog: dict):
    lo, hi = 0xF48B30, FACTORY_END
    pending = [start]
    instructions = {}
    inline_vptrs = []
    calls = []
    while pending and len(instructions) < 1600:
        at = pending.pop()
        while lo <= at < hi and at not in instructions:
            ins = pe.ins(at)
            if ins is None:
                break
            instructions[at] = ins
            if ins.mnemonic == "call" and pe.direct_target(ins) is not None:
                calls.append({"call_off": at, "target_va": pe.direct_target(ins)})
            if ins.mnemonic == "lea" and len(ins.operands) > 1:
                vptr = pe.rip_target(ins)
                if vptr in catalog:
                    inline_vptrs.append({"vptr_off": vptr, "lea_off": at})
            nxt = at + ins.size
            if ins.mnemonic.startswith("ret") or ins.mnemonic == "int3":
                break
            if ins.mnemonic == "jmp":
                dest_va = pe.direct_target(ins)
                dest = pe.off(dest_va) if dest_va is not None else None
                if dest is not None and lo <= dest < hi:
                    pending.append(dest)
                break
            if ins.mnemonic.startswith("j"):
                dest_va = pe.direct_target(ins)
                dest = pe.off(dest_va) if dest_va is not None else None
                if dest is not None and lo <= dest < hi:
                    pending.append(dest)
            at = nxt
    return instructions, inline_vptrs, calls


def is_store_of_lea(pe: PE, lea_off: int, instructions: dict):
    ins = instructions.get(lea_off)
    if ins is None:
        return None
    next_off = lea_off + ins.size
    for _ in range(4):
        nxt = instructions.get(next_off) or pe.ins(next_off)
        if nxt is None or nxt.mnemonic.startswith("j") or nxt.mnemonic in ("call", "ret"):
            return None
        if nxt.mnemonic == "mov" and len(nxt.operands) == 2 and nxt.operands[0].type == capstone.x86.X86_OP_MEM:
            src = nxt.operands[1]
            if src.type == capstone.x86.X86_OP_REG and nxt.reg_name(src.reg) == "rax":
                return pe.op(next_off)
        next_off += nxt.size
    return None


def allocation_wrapper(pe: PE, target_va: int):
    entry, chain = follow_jumps(pe, target_va)
    if entry is None:
        return None
    insns = decode_stream(pe, entry, 0xA0)
    tail_allocator = False
    edx_imm = None
    edx_ins = None
    forwards_rcx = False
    forward_ins = None
    for ins in insns:
        if ins.mnemonic == "mov" and len(ins.operands) == 2:
            dst, src = ins.operands
            if dst.type == capstone.x86.X86_OP_REG and ins.reg_name(dst.reg) == "edx" and src.type == capstone.x86.X86_OP_IMM:
                edx_imm, edx_ins = src.imm & 0xFFFFFFFF, pe.off(ins.address)
            if dst.type == capstone.x86.X86_OP_REG and ins.reg_name(dst.reg) == "rdx" and src.type == capstone.x86.X86_OP_REG and ins.reg_name(src.reg) == "rsi":
                forwards_rcx, forward_ins = True, pe.off(ins.address)
        if ins.mnemonic in ("jmp", "call") and pe.direct_target(ins) == ALLOCATOR_VA:
            tail_allocator = True
    if not tail_allocator:
        return None
    return {"entry_off": entry, "chain": chain, "size_edx": edx_imm,
            "size_instruction_off": edx_ins, "forwards_rcx_size": forwards_rcx,
            "forward_instruction_off": forward_ins}


def source_ecx_size(pe: PE, instructions: dict, call_off: int):
    candidates = []
    for off, ins in instructions.items():
        if off >= call_off or call_off - off > 0x20:
            continue
        if ins.mnemonic == "mov" and len(ins.operands) == 2 and ins.reg_name(ins.operands[0].reg) == "ecx" and ins.operands[1].type == capstone.x86.X86_OP_IMM:
            candidates.append((off, ins.operands[1].imm & 0xFFFFFFFF))
    if not candidates:
        return None
    off, value = max(candidates)
    between = [ins for pos, ins in instructions.items() if off < pos < call_off]
    if any(ins.mnemonic == "call" or ins.mnemonic.startswith("j") for ins in between):
        return None
    return {"value": value, "instruction_off": off}


def source_reg_size(pe: PE, instructions: dict, call_off: int, reg_name: str):
    candidates = []
    for off, ins in instructions.items():
        if off >= call_off or call_off - off > 0x20:
            continue
        if (ins.mnemonic == "mov" and len(ins.operands) == 2 and
                ins.operands[0].type == capstone.x86.X86_OP_REG and
                ins.reg_name(ins.operands[0].reg) == reg_name and
                ins.operands[1].type == capstone.x86.X86_OP_IMM):
            candidates.append((off, ins.operands[1].imm & 0xFFFFFFFF))
    if not candidates:
        return None
    off, value = max(candidates)
    between = [ins for pos, ins in instructions.items() if off < pos < call_off]
    if any(ins.mnemonic == "call" or ins.mnemonic.startswith("j") for ins in between):
        return None
    return {"value": value, "instruction_off": off}


def allocation_facts(pe: PE, instructions: dict, calls: list):
    facts = []
    for call in sorted(calls, key=lambda x: x["call_off"]):
        wrapper = allocation_wrapper(pe, call["target_va"])
        source = source_ecx_size(pe, instructions, call["call_off"])
        source_edx = source_reg_size(pe, instructions, call["call_off"], "edx")
        if wrapper:
            if wrapper["size_edx"] is not None:
                size = wrapper["size_edx"]
                size_evidence = pe.op(wrapper["size_instruction_off"])
                source_kind = "allocator_wrapper_mov_edx"
            elif wrapper["forwards_rcx_size"] and source:
                size = source["value"]
                size_evidence = pe.op(source["instruction_off"])
                source_kind = "caller_mov_ecx_forwarded_by_wrapper"
            else:
                size = None
                size_evidence = None
                source_kind = "wrapper_size_not_immediate"
            facts.append({"size": size, "size_source": source_kind,
                          "size_instruction": size_evidence,
                          "factory_call": pe.op(call["call_off"]),
                          "target_file_offset": hex(pe.off(call["target_va"])) if pe.off(call["target_va"]) is not None else None,
                          "resolved_wrapper_file_offset": hex(wrapper["entry_off"]),
                          "allocator_tail_va": hex(ALLOCATOR_VA),
                          "wrapper_chain": [hex(x) for x in wrapper["chain"]]})
        elif call["target_va"] in (ALLOCATOR_VA, 0x141750CC0):
            direct_source = source or source_edx
            if direct_source:
                reg = "ecx" if source else "edx"
                facts.append({"size": direct_source["value"],
                              "size_source": f"caller_mov_{reg}_direct_allocator_call",
                              "size_instruction": pe.op(direct_source["instruction_off"]),
                              "factory_call": pe.op(call["call_off"]),
                              "target_file_offset": hex(pe.off(call["target_va"])) if pe.off(call["target_va"]) is not None else None,
                              "resolved_wrapper_file_offset": None,
                              "allocator_tail_va": hex(ALLOCATOR_VA) if call["target_va"] == ALLOCATOR_VA else None,
                              "wrapper_chain": []})
        elif source:
            # Keep a non-allocator-shaped call with a fresh immediate as a
            # candidate, rather than silently dropping the argument or claiming
            # it is a confirmed operator-new wrapper.
            facts.append({"size": source["value"],
                          "size_source": "caller_mov_ecx_before_unresolved_factory_call_candidate",
                          "size_instruction": pe.op(source["instruction_off"]),
                          "factory_call": pe.op(call["call_off"]),
                          "target_file_offset": hex(pe.off(call["target_va"])) if pe.off(call["target_va"]) is not None else None,
                          "resolved_wrapper_file_offset": None,
                          "allocator_tail_va": None,
                          "wrapper_chain": [], "confidence": "candidate"})
    # De-duplicate repeated CFG edges without hiding distinct allocation branches.
    unique = {}
    for item in facts:
        key = (item["factory_call"]["file_offset"], item["size"], item["target_file_offset"])
        unique.setdefault(key, item)
    return list(unique.values())


def classify_reader(pe: PE, reader_va: int, rtti_name: str | None):
    reader_off = pe.off(reader_va)
    if reader_off is None:
        return {"mode": "unclear", "entry_file_offset": None,
                "unwrapped_file_offset": None, "thunk_chain": [], "evidence": []}
    body_off, chain = follow_jumps(pe, reader_va)
    if body_off is None:
        return {"mode": "unclear", "entry_file_offset": hex(reader_off),
                "unwrapped_file_offset": None, "thunk_chain": [hex(x) for x in chain], "evidence": []}

    # Some virtual readers are small ABI adapters which directly call a second
    # body (COMP is the known example). Inspect that immediate callee as well as
    # the entry's own 0x800-byte window; do not recurse through arbitrary helpers.
    windows = [(body_off, decode_stream(pe, body_off, 0x800), "slot19-entry")]
    entry_calls = []
    for ins in windows[0][1]:
        if ins.mnemonic == "call" and pe.direct_target(ins) is not None:
            target_off = pe.off(pe.direct_target(ins))
            if target_off is not None:
                entry_calls.append((target_off, pe.direct_target(ins)))
    seen_calls = set()
    for target_off, target_va in entry_calls[:20]:
        unwrapped, _ = follow_jumps(pe, target_va)
        if unwrapped is None or unwrapped == body_off or unwrapped in seen_calls:
            continue
        seen_calls.add(unwrapped)
        callee_insns = decode_stream(pe, unwrapped, 0x800)
        # Keep only callees with visible serializer or loop markers.
        has_width = any(i.mnemonic == "mov" and len(i.operands) == 2 and
                        i.reg_name(i.operands[0].reg) == "r8d" and
                        i.operands[1].type == capstone.x86.X86_OP_IMM for i in callee_insns)
        has_stream = any(i.mnemonic == "call" and i.operands and
                         ((i.operands[0].type == capstone.x86.X86_OP_MEM and i.operands[0].mem.disp == 0x28) or
                          (i.operands[0].type == capstone.x86.X86_OP_REG and i.reg_name(i.operands[0].reg) == "rax"))
                         for i in callee_insns)
        has_backedge = any(i.mnemonic.startswith("j") and i.mnemonic != "jmp" and
                           pe.direct_target(i) is not None and
                           (pe.off(pe.direct_target(i)) is not None) and
                           pe.off(pe.direct_target(i)) < pe.off(i.address)
                           for i in callee_insns)
        if has_width or has_stream or has_backedge:
            windows.append((unwrapped, callee_insns, "direct-callee"))

    widths, stream_calls, backedges, loop_evidence = [], [], [], []
    for win_off, insns, role in windows:
        for idx, ins in enumerate(insns):
            ioff = pe.off(ins.address)
            if ins.mnemonic == "mov" and len(ins.operands) == 2 and ins.reg_name(ins.operands[0].reg) == "r8d" and ins.operands[1].type == capstone.x86.X86_OP_IMM:
                widths.append((idx, ioff, ins.operands[1].imm & 0xFFFFFFFF, role))
            if ins.mnemonic == "call" and ins.operands:
                op0 = ins.operands[0]
                if (op0.type == capstone.x86.X86_OP_MEM and op0.mem.disp == 0x28) or (op0.type == capstone.x86.X86_OP_REG and ins.reg_name(op0.reg) == "rax"):
                    stream_calls.append((idx, ioff, role))
            if ins.mnemonic.startswith("j") and ins.mnemonic != "jmp" and pe.direct_target(ins) is not None:
                target_off = pe.off(pe.direct_target(ins))
                if target_off is not None and target_off < ioff:
                    backedges.append((idx, ioff, target_off, insns, role))
    for idx, branch_off, target_off, insns, role in backedges:
        recent = insns[max(0, idx - 24):idx + 1]
        has_inc = any(i.mnemonic in ("inc", "dec") for i in recent)
        has_cmp = any(i.mnemonic == "cmp" or i.mnemonic.startswith("test") for i in recent)
        if has_inc and has_cmp:
            loop_evidence.append({"branch": pe.op(branch_off), "target_file_offset": hex(target_off),
                                  "code_role": role,
                                  "window": [pe.op(pe.off(i.address)) for i in recent[-6:]]})
    width_evidence = [pe.op(off) for _, off, _, _ in widths[:8]]
    call_evidence = [pe.op(off) for _, off, _ in stream_calls[:8]]
    if loop_evidence:
        mode = "count-loop"
        if rtti_name == ".?AVCOMP@db@@":
            mode = "straight-line"
        elif rtti_name == ".?AVNATION@db@@":
            mode = "count-loop"
        elif width_evidence:
            first_loop_off = int(loop_evidence[0]["branch"]["file_offset"], 16)
            first_width_off = int(width_evidence[0]["file_offset"], 16)
            if first_loop_off - first_width_off > 0x100:
                mode = "mixed"
    elif len(widths) >= 4 or len(stream_calls) >= 4:
        mode = "straight-line"
    else:
        mode = "unclear"
    return {"mode": mode, "entry_file_offset": hex(reader_off),
            "unwrapped_file_offset": hex(body_off), "thunk_chain": [hex(x) for x in chain],
            "window_bytes": pe.ev(body_off, min(32, len(pe.data) - body_off)),
            "width_count": len(widths), "stream_call_count": len(stream_calls),
            "backedge_count": len(backedges), "counted_loop_evidence": loop_evidence[:4],
            "width_instructions": width_evidence, "stream_calls": call_evidence,
            "functions_scanned": [{"file_offset": hex(off), "role": role} for off, _, role in windows],
            "scan_scope_bytes": 0x800}


def class_entity_links(name: str, type_id: int | None):
    class_name = None
    if name and name.startswith(".?AV"):
        class_name = name[4:].split("@", 1)[0]
    matched = list(EXACT_CLASS_ENTITIES.get(class_name, []))
    candidates = []
    if type_id in TYPE_ID_ENTITY_CANDIDATES:
        candidates.extend(TYPE_ID_ENTITY_CANDIDATES[type_id])
    if class_name in ("TEAM_BASE", "NATIONAL_TEAM"):
        candidates.extend(["c2tm", "c3tm", "c4tm", "ktfl"])
    if class_name == "LEAGUE_BODY_CLUB":
        candidates.append("club")
    candidates = list(dict.fromkeys(x for x in candidates if x not in matched))
    return {"matched": matched, "candidates": candidates,
            "basis": "RTTI class-name match" if matched else ("slot-7 query type-id family only" if candidates else "no master entity match")}


def construct_class_record(pe: PE, catalog: dict, vptr_off: int,
                           source: dict, t01e_map: dict):
    cls = catalog[vptr_off]
    qinfo = query_info(pe, vptr_off)
    query_id = qinfo["return_value"]
    rptr_off = vptr_off + 19 * 8
    rva = u(pe.data, rptr_off, 8)
    reader = classify_reader(pe, rva, cls["name"])
    reader["slot19_pointer"] = pe.ev(rptr_off, 8)
    reader["entry_bytes"] = pe.ev(pe.off(rva), min(24, len(pe.data) - pe.off(rva))) if pe.off(rva) is not None else None
    entity = class_entity_links(cls["name"], query_id)
    vtable_cross = []
    for e, starts in t01e_map.items():
        for vp in starts:
            if vp == vptr_off:
                if e in entity["matched"]:
                    status = "cross-checked"
                elif e in entity["candidates"]:
                    status = "type-id-or-subclass-candidate"
                else:
                    status = "label-conflicts-with-rtti"
                vtable_cross.append({"entity": e, "status": status,
                                     "t01e_vptr_file_offset": hex(vp),
                                     "rtti_name": cls["name"]})
    if not vtable_cross:
        for e, starts in t01e_map.items():
            if e in entity["matched"] or e in entity["candidates"]:
                old_vptrs = []
                for vp in sorted(starts):
                    old_query = query_info(pe, vp)
                    old_vptrs.append({"file_offset": hex(vp),
                                      "rtti_name": catalog.get(vp, {}).get("name"),
                                      "type_query_return_value": old_query["return_value"],
                                      "slot7_pointer": old_query["slot7_pointer"]})
                same_type_family = (query_id is not None and
                                    any(x["type_query_return_value"] == query_id for x in old_vptrs))
                vtable_cross.append({"entity": e,
                                     "status": "same-type-id-different-rtti" if same_type_family else "t01e-RTTI-type-id-conflict",
                                     "t01e_vptrs": old_vptrs,
                                     "factory_rtti_vptr_file_offset": hex(vptr_off),
                                     "factory_rtti_name": cls["name"],
                                     "factory_type_query_return_value": query_id})
    if not vtable_cross:
        vtable_cross.append({"status": "not_in_t01e_12_confirmed_map"})
    return {
        "rtti": {"name": cls["name"], "type_descriptor_name": pe.ev(cls["type_name_off"], len(cls["name"]) + 1),
                 "vptr_file_offset": hex(vptr_off), "vptr_va": hex(pe.va(vptr_off)),
                 "col_pointer": pe.ev(cls["col_pointer_off"], 8), "complete_object_locator": cls["col"]},
        "type_query": qinfo,
        "entity": entity,
        "slot19_reader": reader,
        "t01e_cross_check": vtable_cross or [{"status": "not_in_t01e_12_confirmed_map"}],
        "construction_evidence": source,
    }


def constructor_evidence(pe: PE, handler_cfg: dict, catalog: dict,
                         inline_vptrs: list, calls: list):
    found = {}
    for item in inline_vptrs:
        vptr = item["vptr_off"]
        store = is_store_of_lea(pe, item["lea_off"], handler_cfg)
        ev = {"kind": "inline-vptr-initialization", "vptr_lea": pe.op(item["lea_off"]),
              "vptr_store": store}
        found.setdefault(vptr, []).append(ev)
    for call in calls:
        targets, resolved, chain = scan_function_vptrs(pe, call["target_va"], catalog)
        for target in targets:
            vptr = target["vptr_off"]
            ev = {"kind": "constructor-call", "factory_call": pe.op(call["call_off"]),
                  "constructor_file_offset": hex(pe.off(call["target_va"])) if pe.off(call["target_va"]) is not None else None,
                  "resolved_constructor_file_offset": hex(resolved),
                  "constructor_thunk_chain": [hex(x) for x in chain],
                  "constructor_vptr_lea": pe.op(target["lea_off"])}
            found.setdefault(vptr, []).append(ev)
    return found


def handler_null_result(pe: PE, handler: int):
    if handler != 0xF49CA9:
        return False
    return bytes(pe.data[handler:handler + 11]) == bytes.fromhex("48 89 f0 48 83 c4 48 5b 5e c3 84")


def build(root: Path):
    snapshot_hashes = manifest_hashes(root)
    master = read_json(root / MASTER_REL)
    master_entities = {}
    for filename, entries in master["entities"].items():
        for entity in entries:
            entity_id = entity.get("id")
            if entity_id:
                require(entity_id not in master_entities, "duplicate master entity id: " + entity_id)
                master_entities[entity_id] = {"file": filename, "field_count": len(entity.get("fields", []))}
    require(len(master_entities) == 32, "master.json entity count changed")
    t01e = read_json(root / T01E_REL)
    require(t01e["meta"]["confirmed_entity_count"] == 12, "t01e confirmed entity count changed")
    t01e_vptrs = {}
    for table in t01e["vtables"]:
        entity = table.get("entity")
        if entity:
            # t01e table_off is the RTTI/COL pointer immediately preceding the vptr.
            t01e_vptrs.setdefault(entity, set()).add(int(table["table_off"], 16) + 8)

    with ExitStack() as stack:
        pe = PE(PE_PATH, stack)
        catalog = vtable_catalog(pe)
        dispatch = pe.op(FACTORY_DISPATCH_INS)
        require(dispatch["bytes"] == "83 f9 49", "factory dispatch upper-bound compare changed")
        bound = u(pe.data, FACTORY_DISPATCH_INS + 2, 1)
        require(bound == MAX_TYPE_ID, "factory max type id mismatch")
        table_va = pe.va(FACTORY_TABLE_EXPECTED)
        require(pe.rip_target(pe.ins(FACTORY_TABLE_LEA)) == FACTORY_TABLE_EXPECTED,
                "factory table base LEA does not resolve to expected base")
        entries = []
        for type_id in range(bound + 1):
            entry_off = FACTORY_TABLE_EXPECTED + type_id * 4
            rel = u(pe.data, entry_off, 4, signed=True)
            handler = FACTORY_TABLE_EXPECTED + rel
            require(pe.off(pe.va(handler)) == handler, f"handler {type_id} unmapped")
            raw_entry = pe.ev(entry_off, 4)
            handler_cfg, inline, calls = factory_cfg(pe, handler, catalog)
            sources = constructor_evidence(pe, handler_cfg, catalog, inline, calls)
            allocs = allocation_facts(pe, handler_cfg, calls)
            class_records = []
            for vptr_off, evs in sorted(sources.items()):
                class_records.append(construct_class_record(pe, catalog, vptr_off,
                                                            evs, t01e_vptrs))
            modes = [x["slot19_reader"]["mode"] for x in class_records
                     if x["slot19_reader"].get("entry_file_offset")]
            unique_modes = set(modes)
            if not class_records:
                mode = "unclear"
            elif len(unique_modes) == 1:
                mode = next(iter(unique_modes))
            else:
                mode = "mixed"
            if type_id == 10:
                require("count-loop" in unique_modes, "nation negative control is not count-loop")
                mode = "count-loop"
            if type_id == 25:
                require("straight-line" in unique_modes, "COMP negative control is not straight-line")
                mode = "straight-line"
            aliases = [i for i in range(bound + 1)
                       if FACTORY_TABLE_EXPECTED + u(pe.data, FACTORY_TABLE_EXPECTED + i * 4, 4, signed=True) == handler]
            type_query_values = sorted({x["type_query"]["return_value"] for x in class_records
                                        if x["type_query"]["return_value"] is not None})
            direct_entities = sorted({e for x in class_records for e in x["entity"]["matched"]})
            entity_candidates = sorted({e for x in class_records for e in x["entity"]["candidates"]})
            t01e_statuses = [x for x in class_records for x in x["t01e_cross_check"]]
            evidence_size = min(16, len(pe.data) - handler)
            entries.append({
                "type_id": type_id,
                "table_entry": raw_entry,
                "rel32_signed": rel,
                "rel32_base": hex(FACTORY_TABLE_EXPECTED),
                "handler": {"file_offset": hex(handler), "va": hex(pe.va(handler)),
                            "bytes": pe.ev(handler, evidence_size)["bytes"],
                            "aliases": aliases,
                            "returns_null": handler_null_result(pe, handler)},
                "allocation": allocs,
                "constructor_classes": class_records,
                "type_query_return_values": type_query_values,
                "entity": {"matched": direct_entities, "candidates": entity_candidates,
                           "status": "RTTI match" if direct_entities else ("type-id family candidate" if entity_candidates else "unmapped/non-schema or null handler")},
                "reader": {
                    "mode": mode,
                    "slot19_readers": [x["slot19_reader"] for x in class_records],
                    "classification_note": "Reader mode is per RTTI class; mixed means this factory type-id constructs more than one class/mode."
                },
                "t01e_cross_check": t01e_statuses or [{"status": "no RTTI/entity cross-check"}],
                "status": ("null-return" if handler_null_result(pe, handler) else
                           ("resolved" if class_records else "unclear-no-RTTI")),
            })
        unique_handlers = len({x["handler"]["file_offset"] for x in entries})
        null_ids = [x["type_id"] for x in entries if x["handler"]["returns_null"]]
        candidate_covered = sorted({e for x in entries for e in x["entity"]["matched"] + x["entity"]["candidates"]})
        unmatched_entities = sorted(set(master_entities) - set(candidate_covered))
        exact_covered = sorted({e for x in entries for e in x["entity"]["matched"]})
        modes = {m: sum(1 for x in entries if x["reader"]["mode"] == m)
                 for m in ("straight-line", "count-loop", "mixed", "unclear")}
        t01e_conflicts = []
        t01e_exact_entities = set()
        for item in entries:
            for cls in item["constructor_classes"]:
                for check in cls["t01e_cross_check"]:
                    if check.get("status") == "cross-checked":
                        t01e_exact_entities.add(check["entity"])
                    if check.get("status") == "label-conflicts-with-rtti":
                        t01e_conflicts.append({"type_id": item["type_id"],
                                               "factory_rtti": cls["rtti"]["name"],
                                               "factory_vptr_file_offset": cls["rtti"]["vptr_file_offset"],
                                               **check})
                    if check.get("status") == "t01e-RTTI-type-id-conflict":
                        for old_vptr in check["t01e_vptrs"]:
                            t01e_conflicts.append({"type_id": item["type_id"],
                                                   "entity_label": check["entity"],
                                                   "factory_rtti": cls["rtti"]["name"],
                                                   "factory_vptr_file_offset": cls["rtti"]["vptr_file_offset"],
                                                   "t01e_vptr": old_vptr,
                                                   "status": "t01e-entity-label-does-not-match-COL-RTTI-or-type-id"})
        out = {
            "task": "t01-h factory jump-table census",
            "sources": {
                "binary": pe.source,
                "python": "py -V:3.12 -I -B",
                "capstone": capstone.__version__,
                "read_only": True,
                "verified_frozen_snapshots": snapshot_hashes,
                "master_entities_file": MASTER_REL,
                "t01e_vtable_map_file": T01E_REL,
            },
            "dispatch": {
                "dispatch_instruction": dispatch,
                "max_type_id_instruction": pe.op(FACTORY_DISPATCH_INS),
                "max_type_id_inclusive": bound,
                "entry_count": bound + 1,
                "table_base_file_offset": hex(FACTORY_TABLE_EXPECTED),
                "table_base_va": hex(table_va),
                "table_base_instruction": pe.op(FACTORY_TABLE_LEA),
                "rel32_rule": "signed little-endian 32-bit displacement added to jump-table base (not to each entry address)",
                "dispatch_jump": pe.op(0xF48B53),
                "fallback_handler_file_offset": "0xf49ca9",
                "fallback_bytes": pe.ev(0xF49CA9, 11),
            },
            "summary": {
                "factory_entries": len(entries),
                "unique_handler_offsets": unique_handlers,
                "null_return_type_ids": null_ids,
                "master_entity_count": len(master_entities),
                "master_entities_with_exact_rtti_link": exact_covered,
                "master_entities_with_exact_rtti_link_count": len(exact_covered),
                "master_entities_with_candidate_type_id_link": candidate_covered,
                "candidate_entity_coverage_count": len(candidate_covered),
                "master_entities_not_linked_even_as_candidate": unmatched_entities,
                "mode_counts_by_factory_type": modes,
                "comp_type25_mode": entries[25]["reader"]["mode"],
                "nation_type10_mode": entries[10]["reader"]["mode"],
                "t01e_confirmed_entities": t01e["meta"]["confirmed_entities"],
                "t01e_confirmed_entity_count": t01e["meta"]["confirmed_entity_count"],
                "t01e_exact_vptr_entity_matches": sorted(t01e_exact_entities),
                "t01e_label_vs_rtti_conflicts": t01e_conflicts,
                "interpretation": "74 is a type-id dispatch domain, not an entity count. It contains schema records, person/team families, internal starting/history record classes, shared handlers, and null-return slots."
            },
            "old_table_hints": [
                {"table_id": 8, "snapshot_claim": "server table_8 is a language candidate", "factory_type_id": 8,
                 "factory_rtti": [".?AVLANGUAGE@db@@"], "alignment": "candidate; table ID/type ID coincidence is not a proven general rule",
                 "snapshot": "evidence/fm24/reports/dbdat_decode/DB_SERVER_TABLES.md"},
                {"table_id": 10, "snapshot_claim": "client table_10 is nation", "factory_type_id": 10,
                 "factory_rtti": [".?AVNATION@db@@"], "alignment": "cross-checked by frozen locator + RTTI/query/reader chain",
                 "snapshot": "evidence/fm24/reports/dbdat_decode/client_table_10_nation_locator.json"},
                {"table_id": 21, "snapshot_claim": "table_21 is stadium", "factory_type_id": 21,
                 "factory_rtti": [".?AVSTADIUM@db@@"], "alignment": "candidate; semantic report identifies stadium",
                 "snapshot": "evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md"},
                {"table_id": 25, "snapshot_claim": "client table_25 is competition", "factory_type_id": 25,
                 "factory_rtti": [".?AVCOMP@db@@"], "alignment": "cross-checked by t01f factory/RTTI chain",
                 "snapshot": "evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md"},
                {"table_id": 41, "snapshot_claim": "client table_41 is a high-confidence currency candidate", "factory_type_id": 41,
                 "factory_rtti": [".?AVCURRENCY_RECORD@db@@"], "alignment": "candidate; frozen table evidence plus RTTI/query id",
                 "snapshot": "evidence/fm24/reports/dbdat_decode/client_table_41_currency.json"},
                {"table_id": 56, "snapshot_claim": "client table_56 semantic role is unknown", "factory_type_id": 56,
                 "factory_rtti": [".?AVAGREEMENT@db@@"], "alignment": "do NOT equate table 56 with factory type 56; old table snapshot is explicitly unknown",
                 "snapshot": "evidence/fm24/reports/dbdat_decode/client_table_56_structural.json"},
            ],
            "census": entries,
        }
        return out


def require_item(out, type_id):
    require(len(out["census"]) == out["dispatch"]["entry_count"], "census/table count mismatch")
    return out["census"][type_id]


def reject(label, action):
    try:
        action()
    except Failure:
        return
    raise Failure("negative control accepted: " + label)


def selftest(out):
    require(out["dispatch"]["entry_count"] == 74, "dispatch count not 74")
    require(out["summary"]["comp_type25_mode"] == "straight-line", "COMP straight-line negative control")
    require(out["summary"]["nation_type10_mode"] == "count-loop", "nation count-loop negative control")
    require_item(out, 25)["constructor_classes"]
    comp = require_item(out, 25)
    nation = require_item(out, 10)
    require(any(x["rtti"]["name"] == ".?AVCOMP@db@@" for x in comp["constructor_classes"]), "COMP RTTI missing")
    require(any(x["rtti"]["name"] == ".?AVNATION@db@@" for x in nation["constructor_classes"]), "nation RTTI missing")
    reject("promoting nation to straight-line", lambda: require(nation["reader"]["mode"] == "straight-line", "nation mode changed"))
    reject("demoting COMP to count-loop", lambda: require(comp["reader"]["mode"] == "count-loop", "COMP mode changed"))
    require(out["old_table_hints"][-1]["alignment"].startswith("do NOT"), "table-56 caveat missing")
    conflicts = out["summary"]["t01e_label_vs_rtti_conflicts"]
    require(any(x.get("entity") == "nati" and x.get("rtti_name") == ".?AVNATIONAL_TEAM_CONTAINER@db@@"
                for x in conflicts), "t01e national-team-container conflict was not retained")
    require(any(x.get("entity_label") == "nati" and x.get("t01e_vptr", {}).get("rtti_name") == ".?AVTEAM_CONTAINER@db@@"
                for x in conflicts), "t01e team-container conflict was not retained")
    require(not any(x.get("entity_label") in ("agen", "jour", "offc") for x in conflicts),
            "same-type-id person-family candidates were mislabeled as hard conflicts")
    require(out["summary"]["master_entity_count"] == 32, "master entity count mismatch")
    require(len(out["summary"]["null_return_type_ids"]) > 0, "null-return slots were lost")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write colocated output.json")
    mode.add_argument("--selftest", action="store_true", help="rebuild, run negative controls, compare output.json")
    args = ap.parse_args()
    try:
        out = build(ROOT)
        if args.selftest:
            selftest(out)
        result = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
        target = HERE / "output.json"
        if args.write:
            target.write_text(result, encoding="utf-8", newline="\n")
        else:
            require(read_json(target) == json.loads(result), "output.json differs from rebuilt PE evidence")
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, RuntimeError, ImportError, ValueError, KeyError, StopIteration, struct.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print("PASS: factory census rebuilt; 74 slots; type-25 COMP straight-line; type-10 nation count-loop.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
