#!/usr/bin/env python3
"""Statically map FM24 reader transfers and 4CC getter codes to row offsets.

Only reads editor.exe and the checked-in census/fixture inputs.  Generated output
is confined to this script's directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import capstone
import capstone.x86_const as x86

ROOT = Path(__file__).resolve().parents[4]
OUTDIR = Path(__file__).resolve().parent
DEFAULT_FIXTURES = ROOT / "scratch/t02/field_mapper/fixtures.json"
DEFAULT_CENSUS = ROOT / "scratch/t01/inbox/t01h/output.json"
DEFAULT_EDITOR = ROOT.parent / "fm24/input/editor.exe"
STREAM_DISP = 0x28
MAX_FUNCTION_BYTES = 0x6000


def _hex(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def _is_mem(op: Any) -> bool:
    return op.type == x86.X86_OP_MEM


class PEImage:
    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        self.sha256 = hashlib.sha256(self.data).hexdigest()
        peoff = struct.unpack_from("<I", self.data, 0x3C)[0]
        if self.data[peoff:peoff + 4] != b"PE\0\0":
            raise ValueError(f"not a PE image: {path}")
        opt = peoff + 24
        machine = struct.unpack_from("<H", self.data, peoff + 4)[0]
        if machine != 0x8664:
            raise ValueError(f"expected x64 PE (machine={machine:#x})")
        self.image_base = struct.unpack_from("<Q", self.data, opt + 24)[0]
        nsec = struct.unpack_from("<H", self.data, peoff + 6)[0]
        opt_size = struct.unpack_from("<H", self.data, peoff + 20)[0]
        table = opt + opt_size
        self.sections: list[tuple[str, int, int, int, int]] = []
        for p in range(table, table + nsec * 40, 40):
            name = self.data[p:p + 8].rstrip(b"\0").decode("ascii", "replace")
            virtual_size, rva, raw_size, raw = struct.unpack_from("<IIII", self.data, p + 8)
            self.sections.append((name, rva, virtual_size, raw, raw_size))
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True

    def va(self, off: int) -> int:
        for _, rva, _, raw, size in self.sections:
            if raw <= off < raw + size:
                return self.image_base + rva + off - raw
        raise ValueError(f"file offset not mapped: {off:#x}")

    def off(self, va: int) -> int | None:
        rva = va - self.image_base
        for _, sec_rva, virtual_size, raw, raw_size in self.sections:
            span = max(virtual_size, raw_size)
            delta = rva - sec_rva
            if 0 <= delta < span and delta < raw_size:
                return raw + delta
        return None

    def dis(self, off: int, size: int) -> list[Any]:
        if not (0 <= off < len(self.data)):
            return []
        end = min(len(self.data), off + size)
        try:
            return list(self.md.disasm(self.data[off:end], self.va(off)))
        except ValueError:
            return []

    def ins(self, off: int) -> Any | None:
        ins = self.dis(off, min(16, len(self.data) - off))
        return ins[0] if ins else None

    def qword(self, off: int) -> int | None:
        if off < 0 or off + 8 > len(self.data):
            return None
        return struct.unpack_from("<Q", self.data, off)[0]

    def evidence(self, off: int, size: int) -> dict[str, str]:
        ins = self.ins(off)
        return {
            "file_offset": hex(off),
            "va": hex(self.va(off)),
            "bytes": self.data[off:off + size].hex(" "),
            **({"instruction": f"{ins.mnemonic} {ins.op_str}".strip()} if ins else {}),
        }

    def resolve_jumps(self, start: int) -> list[int]:
        chain: list[int] = []
        seen: set[int] = set()
        off = start
        for _ in range(12):
            if off in seen:
                break
            seen.add(off)
            chain.append(off)
            ins = self.ins(off)
            if not (ins and ins.mnemonic == "jmp" and ins.operands and
                    ins.operands[0].type == x86.X86_OP_IMM):
                break
            target = self.off(ins.operands[0].imm)
            if target is None:
                break
            off = target
        return chain


def _direct_targets(pe: PEImage, insns: list[Any], limit: int = 0x300) -> list[int]:
    targets = []
    base = insns[0].address if insns else 0
    for ins in insns:
        off = pe.off(ins.address)
        if off is None or off - (pe.off(base) or 0) > limit:
            break
        if ins.mnemonic in ("call", "jmp") and ins.operands and ins.operands[0].type == x86.X86_OP_IMM:
            target = pe.off(ins.operands[0].imm)
            if target is not None:
                targets.append(target)
    return targets


def _stream_calls(insns: list[Any]) -> int:
    return sum(1 for ins in insns if ins.mnemonic == "call" and ins.operands and
               _is_mem(ins.operands[0]) and ins.operands[0].mem.disp == STREAM_DISP)


def _reader_body(pe: PEImage, entry: int) -> tuple[int, list[Any], list[int]]:
    """Follow direct thunk/call links, choosing the reachable dense reader body."""
    queue: deque[tuple[int, int]] = deque((x, 0) for x in pe.resolve_jumps(entry))
    seen: set[int] = set()
    ranked: list[tuple[int, int, int, list[Any]]] = []
    while queue and len(seen) < 48:
        off, depth = queue.popleft()
        if off in seen:
            continue
        seen.add(off)
        insns = pe.dis(off, MAX_FUNCTION_BYTES)
        if not insns:
            continue
        calls = _stream_calls(insns)
        widths = sum(1 for i in insns if i.mnemonic == "mov" and len(i.operands) == 2 and
                     i.operands[0].type == x86.X86_OP_REG and i.reg_name(i.operands[0].reg) == "r8d" and
                     i.operands[1].type == x86.X86_OP_IMM)
        ranked.append((calls, min(widths, calls), -depth, off, insns))
        if depth < 2:
            for target in _direct_targets(pe, insns):
                if target not in seen:
                    queue.append((target, depth + 1))
    if not ranked:
        return entry, [], pe.resolve_jumps(entry)
    # Prefer the body with most actual stream transfers; the width pairing breaks ties.
    calls, _, _, body, insns = max(ranked, key=lambda row: (row[0], row[1], row[2]))
    return body, insns, pe.resolve_jumps(entry)


def _reader_call_hops(pe: PEImage, entry: int, body: int) -> list[dict[str, str]]:
    """Record direct e8 links from the census thunk chain to the selected body."""
    queue: deque[tuple[int, int]] = deque((x, 0) for x in pe.resolve_jumps(entry))
    seen: set[int] = set()
    while queue and len(seen) < 24:
        source, depth = queue.popleft()
        if source in seen:
            continue
        seen.add(source)
        insns = pe.dis(source, 0x300)
        for ins in insns:
            if ins.mnemonic != "call" or not ins.operands or ins.operands[0].type != x86.X86_OP_IMM:
                continue
            target = pe.off(ins.operands[0].imm)
            if target is None:
                continue
            resolved = pe.resolve_jumps(target)
            if body in resolved:
                return [pe.evidence(pe.off(ins.address), ins.size)]
            if depth < 2:
                queue.extend((x, depth + 1) for x in resolved if x not in seen)
    return []


def _width_events(pe: PEImage, body: int, insns: list[Any],
                  helper_summaries: dict[int, set[int]] | None = None,
                  unresolved_calls: set[int] | None = None
                  ) -> tuple[list[dict[str, Any]], bool, set[int]]:
    """Abstract-interpret cursor/width over forward CFG edges; backedges are not expanded."""
    if not insns:
        return [], False, set()
    index = {ins.address: n for n, ins in enumerate(insns)}
    # States are (cursor, most recent r8d immediate, its file offset).
    states: list[set[tuple[int | None, int | None, int | None]]] = [set() for _ in insns]
    states[0].add((0, None, None))
    todo = deque([0])
    queued = {0}
    event_states: dict[int, set[tuple[int | None, int | None, int | None]]] = defaultdict(set)
    loop_seen = False
    terminal_cursors: set[int] = set()
    helper_summaries = helper_summaries or {}
    unresolved_calls = unresolved_calls or set()
    updates = 0
    while todo and updates < 500000:
        n = todo.popleft()
        queued.discard(n)
        ins = insns[n]
        incoming = states[n]
        if not incoming:
            continue
        updates += 1
        outstates: set[tuple[int | None, int | None, int | None]] = set()
        is_width = (ins.mnemonic == "mov" and len(ins.operands) == 2 and
                    ins.operands[0].type == x86.X86_OP_REG and
                    ins.reg_name(ins.operands[0].reg) == "r8d" and
                    ins.operands[1].type == x86.X86_OP_IMM)
        for cursor, pending, pending_off in incoming:
            if is_width:
                outstates.add((cursor, ins.operands[1].imm & 0xFFFFFFFF, pe.off(ins.address)))
            elif (ins.mnemonic == "call" and ins.operands and
                  ((_is_mem(ins.operands[0]) and ins.operands[0].mem.disp == STREAM_DISP) or
                   (ins.operands[0].type == x86.X86_OP_REG and
                    ins.reg_name(ins.operands[0].reg) == "rax" and pending is not None))):
                event_states[n].add((cursor, pending, pending_off))
                outstates.add((cursor + pending, None, None) if cursor is not None and pending is not None else (None, None, None))
            elif ins.mnemonic == "call" and pe.off(ins.address) in helper_summaries:
                for consumed in helper_summaries[pe.off(ins.address)]:
                    outstates.add((cursor + consumed, None, None) if cursor is not None else (None, None, None))
            elif ins.mnemonic == "call" and pe.off(ins.address) in unresolved_calls:
                outstates.add((None, None, None))
            else:
                outstates.add((cursor, pending, pending_off))
        succ: list[int] = []
        if ins.mnemonic == "ret":
            terminal_cursors.update(cursor for cursor, _, _ in outstates if cursor is not None)
            succ = []
        elif ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == x86.X86_OP_IMM:
            dest = index.get(ins.operands[0].imm)
            if dest is not None:
                if dest <= n:
                    loop_seen = True
                else:
                    succ = [dest]
        elif ins.mnemonic.startswith("j") and ins.mnemonic != "jmp":
            dest = index.get(ins.operands[0].imm) if ins.operands and ins.operands[0].type == x86.X86_OP_IMM else None
            if dest is not None:
                if dest <= n:
                    loop_seen = True
                else:
                    succ.append(dest)
            if n + 1 < len(insns):
                succ.append(n + 1)
        elif n + 1 < len(insns):
            succ = [n + 1]
        for dest in succ:
            before = len(states[dest])
            states[dest].update(outstates)
            if len(states[dest]) > 512:
                # Retain cursor alternatives, but discard stale width states to bound analysis.
                cursors = {cursor for cursor, _, _ in states[dest]}
                states[dest] = {(cursor, None, None) for cursor in cursors}
            if len(states[dest]) != before and dest not in queued:
                todo.append(dest)
                queued.add(dest)

    events: list[dict[str, Any]] = []
    for n, pairs in sorted(event_states.items()):
        ins = insns[n]
        candidates = []
        # Nearest preceding object-pointer LEA is the serialization destination.
        for prior in reversed(insns[max(0, n - 14):n]):
            if prior.mnemonic != "lea" or len(prior.operands) != 2 or not _is_mem(prior.operands[1]):
                continue
            mem = prior.operands[1].mem
            base_reg = prior.reg_name(mem.base) if mem.base else ""
            if base_reg not in ("rsp", "rbp", "rip"):
                candidates.append((mem.disp, base_reg, pe.off(prior.address), prior.size))
                break
        widths = sorted({w for _, w, _ in pairs if w is not None})
        offsets = sorted({cursor for cursor, _, _ in pairs if cursor is not None})
        width_sites = sorted({width_off for _, width, width_off in pairs
                              if width is not None and width_off is not None})
        event = {
            "call": pe.evidence(pe.off(ins.address), ins.size),
            "widths": widths,
            "row_offset_candidates": offsets,
            "cursor_unknown_on_some_paths": any(cursor is None for cursor, _, _ in pairs),
            "width_instructions": [pe.evidence(off, pe.ins(off).size) for off in width_sites if pe.ins(off)],
            "destination": None,
        }
        if candidates:
            disp, reg, doff, dsize = candidates[0]
            event["destination"] = {"member_disp": disp, "base": reg,
                                    "lea": pe.evidence(doff, dsize)}
        events.append(event)
    if not terminal_cursors and insns:
        terminal_cursors.update(cursor for cursor, _, _ in states[-1] if cursor is not None)
    return events, loop_seen, terminal_cursors


def _fixed_helper_consumption(events: list[dict[str, Any]]) -> int | None:
    """Accept only contiguous, single-path transfers; reject branch alternatives and loops."""
    spans = []
    for event in events:
        offsets = event.get("row_offset_candidates", [])
        widths = event.get("widths", [])
        if len(offsets) != 1 or len(widths) != 1:
            return None
        spans.append((offsets[0], widths[0]))
    if not spans or len({start for start, _ in spans}) != len(spans):
        return None
    cursor = 0
    for start, width in sorted(spans):
        if start != cursor or width <= 0:
            return None
        cursor += width
    return cursor


def _getter_function_starts(pe: PEImage, type_item: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for cls in type_item.get("constructor_classes", []):
        vptr = _hex(cls.get("rtti", {}).get("vptr_file_offset"))
        if vptr is None:
            continue
        fn_va = pe.qword(vptr + 2 * 8)
        fn_off = pe.off(fn_va) if fn_va is not None else None
        if fn_off is not None:
            out.append({"file_offset": fn_off, "vptr_file_offset": vptr,
                        "rtti": cls.get("rtti", {}).get("name")})
    return out


def _member_displacements(pe: PEImage, start: int, code_values: dict[int, str], wanted: set[int]) -> dict[str, list[dict[str, Any]]]:
    """Extract member displacements from 4CC getter equality paths."""
    insns = pe.dis(start, 0x10000)
    found: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for n, ins in enumerate(insns):
        if ins.mnemonic != "cmp" or len(ins.operands) != 2 or ins.operands[1].type != x86.X86_OP_IMM:
            continue
        value = ins.operands[1].imm & 0xFFFFFFFF
        code = code_values.get(value)
        if code is None:
            continue
        if n + 1 >= len(insns):
            continue
        branch = insns[n + 1]
        if branch.mnemonic not in ("je", "jz", "jne", "jnz"):
            continue
        roots = []
        if branch.mnemonic in ("je", "jz") and branch.operands and branch.operands[0].type == x86.X86_OP_IMM:
            target = pe.off(branch.operands[0].imm)
            if target is not None:
                roots.append(target)
        elif branch.mnemonic in ("jne", "jnz"):
            roots.append(pe.off(branch.address) + branch.size)
        for root in roots:
            path = pe.dis(root, 0x180)
            candidates: dict[int, dict[str, Any]] = {}
            for p in path:
                if p.mnemonic in ("ret", "jmp"):
                    break
                # Getter handlers either access [this+disp] or shift the object pointer by disp.
                for operand in p.operands:
                    if _is_mem(operand):
                        mem = operand.mem
                        base = p.reg_name(mem.base) if mem.base else ""
                        if base not in ("rsp", "rbp", "rip") and mem.disp in wanted:
                            candidates.setdefault(mem.disp, pe.evidence(pe.off(p.address), p.size))
                if p.mnemonic == "add" and len(p.operands) == 2 and \
                        p.operands[0].type == x86.X86_OP_REG and p.operands[1].type == x86.X86_OP_IMM:
                    base = p.reg_name(p.operands[0].reg)
                    disp = p.operands[1].imm
                    if base not in ("rsp", "rbp") and disp in wanted:
                        candidates.setdefault(disp, pe.evidence(pe.off(p.address), p.size))
            for disp, ev in candidates.items():
                found[code].append({"member_disp": disp, "evidence": ev,
                                    "cmp": pe.evidence(pe.off(ins.address), ins.size)})
    # Keep independent evidence, but avoid duplicate copies from overlapping getter windows.
    for code, rows in list(found.items()):
        uniq = {}
        for row in rows:
            uniq[(row["member_disp"], row["evidence"]["file_offset"])] = row
        found[code] = list(uniq.values())
    return found


class Mapper:
    def __init__(self, editor: Path, census_path: Path, fixtures_path: Path):
        self.pe = PEImage(editor)
        self.census_doc = json.loads(census_path.read_text(encoding="utf-8"))
        self.fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
        self.census = {x["type_id"]: x for x in self.census_doc.get("census", [])}
        self.cache: dict[int, dict[str, int]] = {}
        self.details: dict[int, dict[str, Any]] = {}

    def analyze_full(self, type_id: int) -> tuple[dict[str, int], dict[str, Any]]:
        if type_id in self.cache:
            return self.cache[type_id], self.details[type_id]
        item = self.census.get(type_id)
        if item is None:
            self.cache[type_id] = {}
            self.details[type_id] = {"error": "type_id absent from census"}
            return self.cache[type_id], self.details[type_id]
        fixtures = [f for f in self.fixtures if f.get("type_id") == type_id]
        code_values: dict[int, str] = {}
        for fixture in fixtures:
            for code in fixture.get("fields", {}):
                if isinstance(code, str) and len(code) == 4:
                    try:
                        code_values[int.from_bytes(code.encode("latin-1"), "big")] = code
                    except UnicodeEncodeError:
                        pass
        reader_items = item.get("reader", {}).get("slot19_readers", [])
        if not reader_items:
            self.cache[type_id] = {}
            self.details[type_id] = {"error": "census has no slot19 reader"}
            return self.cache[type_id], self.details[type_id]

        all_events: list[dict[str, Any]] = []
        reader_evidence = []
        all_member_disps: set[int] = set()
        loop_seen = False
        for desc in reader_items:
            entry = _hex(desc.get("entry_file_offset"))
            if entry is None:
                continue
            body, insns, chain = _reader_body(self.pe, entry)
            helper_summaries: dict[int, set[int]] = {}
            unresolved_calls: set[int] = set()
            helper_evidence = []
            for call_ins in insns:
                if (call_ins.mnemonic != "call" or not call_ins.operands or
                        call_ins.operands[0].type != x86.X86_OP_IMM):
                    continue
                call_off = self.pe.off(call_ins.address)
                target = self.pe.off(call_ins.operands[0].imm)
                if call_off is None or target is None:
                    continue
                callee, callee_insns, _ = _reader_body(self.pe, target)
                if callee == body:
                    continue
                helper_events, helper_loop, _ = _width_events(self.pe, callee, callee_insns)
                consumed = _fixed_helper_consumption(helper_events)
                if consumed is not None:
                    helper_summaries[call_off] = {consumed}
                    helper_evidence.append({"call": self.pe.evidence(call_off, call_ins.size),
                                            "callee_body_file_offset": hex(callee),
                                            "fixed_consumed_bytes": consumed,
                                            "callee_events": len(helper_events),
                                            "callee_backedge_seen": helper_loop})
                elif helper_events:
                    unresolved_calls.add(call_off)
                    helper_evidence.append({"call": self.pe.evidence(call_off, call_ins.size),
                                            "callee_body_file_offset": hex(callee),
                                            "fixed_consumed_bytes": None,
                                            "callee_events": len(helper_events),
                                            "status": "branch-dependent helper; downstream cursor invalidated"})
            events, had_loop, _ = _width_events(self.pe, body, insns, helper_summaries, unresolved_calls)
            loop_seen |= had_loop
            for ev in events:
                ev["reader_body_file_offset"] = hex(body)
                dest = ev.get("destination")
                if dest:
                    all_member_disps.add(dest["member_disp"])
            reader_evidence.append({
                "census_entry_file_offset": hex(entry),
                "census_unwrapped_file_offset": desc.get("unwrapped_file_offset"),
                "resolved_jmp_chain_file_offsets": [hex(x) for x in chain],
                "direct_call_hops_to_body": _reader_call_hops(self.pe, entry, body),
                "body_file_offset": hex(body),
                "reader_mode": desc.get("mode"),
                "thunk_or_callee_chain_evidence": [self.pe.evidence(x, max(1, self.pe.ins(x).size))
                                                    for x in chain if self.pe.ins(x)],
                "transfer_count": len(events),
                "fixed_helper_calls": helper_evidence,
            })
            all_events.extend(events)

        getter_evidence: dict[str, list[dict[str, Any]]] = defaultdict(list)
        getter_functions = _getter_function_starts(self.pe, item)
        for start in getter_functions:
            found = _member_displacements(self.pe, start["file_offset"], code_values, all_member_disps)
            for code, rows in found.items():
                for row in rows:
                    getter_evidence[code].append({**row, "getter_file_offset": hex(start["file_offset"]),
                                                  "vptr_file_offset": hex(start["vptr_file_offset"]),
                                                  "rtti": start["rtti"]})

        by_disp: dict[int, set[int]] = defaultdict(set)
        for ev in all_events:
            dest = ev.get("destination")
            widths = ev.get("widths", [])
            offsets = ev.get("row_offset_candidates", [])
            # Keep alternatives for transparent reporting; a count-loop may still expose
            # a stable first-iteration prefix, which is explicitly labeled as such.
            if dest and len(widths) == 1:
                by_disp[dest["member_disp"]].update(offsets)
        mapping: dict[str, int] = {}
        mapping_evidence: dict[str, Any] = {}
        mode = item.get("reader", {}).get("mode")
        first_iteration_prefix = mode == "count-loop"
        for code, rows in getter_evidence.items():
            disps = {r["member_disp"] for r in rows}
            matching = [(d, sorted(by_disp.get(d, set()))) for d in disps if by_disp.get(d)]
            fixed = {values[0] for _, values in matching if len(values) == 1}
            candidates = {value for _, values in matching for value in values}
            if len(fixed) == 1 and all(len(values) == 1 for _, values in matching):
                mapping[code] = next(iter(fixed))
                basis = "unique-static-cursor"
            elif first_iteration_prefix and len(candidates) > 0 and len(disps) == 1:
                mapping[code] = min(candidates)
                basis = "earliest-first-iteration-prefix; later loop offsets remain alternatives"
            else:
                continue
            if code in mapping:
                mapping_evidence[code] = {
                    "mapping_basis": basis,
                    "getter_member_displacements": sorted(disps),
                    "reader_member_to_row_offset_candidates": matching,
                    "getter": rows,
                    "transfer_sites": [ev for ev in all_events
                                       if (ev.get("destination") or {}).get("member_disp") in disps],
                }
        detail = {
            "type_id": type_id,
            "entity": next((f.get("entity") for f in fixtures if f.get("entity")), ""),
            "census_mode": item.get("reader", {}).get("mode"),
            "loop_backedge_detected": loop_seen,
            "reader_bodies": reader_evidence,
            "getter_functions": getter_functions,
            "transfer_events": all_events,
            "mapped_fields": mapping_evidence,
            "unclosed_reason": ("counted/backedge loops are analyzed only once; branch-dependent cursor alternatives are excluded"
                                if loop_seen else "branch-dependent or helper-contained transfers are excluded"),
        }
        self.cache[type_id] = mapping
        self.details[type_id] = detail
        return mapping, detail

    def selfcheck(self) -> dict[str, Any]:
        rows = []
        for fixture in self.fixtures:
            type_id = fixture["type_id"]
            mapping, detail = self.analyze_full(type_id)
            expected = fixture.get("fields", {})
            reproduced = {code: mapping[code] for code in expected if code in mapping}
            correct = [code for code, value in expected.items()
                       if code in mapping and mapping[code] == value]
            rate = len(correct) / len(expected) if expected else 0.0
            rows.append({
                "source": fixture.get("source"), "type_id": type_id,
                "entity": fixture.get("entity"), "mode": fixture.get("reader", {}).get("mode"),
                "reproduced_fields": len(reproduced), "fixture_fields": len(expected),
                "matching_fields": len(correct), "offset_agreement": rate,
                "reproduced": reproduced,
                "mismatches": {code: {"expected": expected[code], "actual": mapping.get(code)}
                               for code in expected if code in mapping and mapping[code] != expected[code]},
                "missing": [code for code in expected if code not in mapping],
                "analysis": detail,
            })
        avg = sum(r["offset_agreement"] for r in rows) / len(rows) if rows else 0.0
        passed = [r for r in rows if r["offset_agreement"] >= 0.8]
        by_mode: dict[str, dict[str, Any]] = {}
        for row in rows:
            mode = row["mode"] or "unknown"
            item = by_mode.setdefault(mode, {"fixtures": 0, "passed_fixtures": 0, "agreement_sum": 0.0})
            item["fixtures"] += 1
            item["passed_fixtures"] += int(row["offset_agreement"] >= 0.8)
            item["agreement_sum"] += row["offset_agreement"]
        for mode, item in by_mode.items():
            item["mean_agreement"] = item.pop("agreement_sum") / item["fixtures"]
            item["passes_80_percent"] = item["passed_fixtures"] == item["fixtures"]
        return {
            "task": "t03 field_mapper selfcheck",
            "sources": {
                "editor": str(self.pe.path), "editor_bytes": len(self.pe.data),
                "editor_sha256": self.pe.sha256,
                "census": str(DEFAULT_CENSUS), "fixtures": str(DEFAULT_FIXTURES),
                "python": sys.version.split()[0], "capstone": capstone.__version__,
                "read_only_inputs": True,
            },
            "summary": {"fixture_count": len(rows), "passed_80_percent": len(passed),
                        "required_pass_count": 5, "mean_field_agreement": avg,
                        "mean_field_agreement_percent": round(avg * 100, 2),
                        "modes": by_mode},
            "fixtures": rows,
        }


def _active_mapper(editor: Path = DEFAULT_EDITOR, census: Path = DEFAULT_CENSUS,
                   fixtures: Path = DEFAULT_FIXTURES) -> Mapper:
    return Mapper(editor, census, fixtures)


_DEFAULT_MAPPER: Mapper | None = None


def analyze(type_id: int) -> dict[str, int]:
    """Return statically closed 4CC-to-row-offset mappings for one factory type."""
    global _DEFAULT_MAPPER
    if _DEFAULT_MAPPER is None:
        _DEFAULT_MAPPER = _active_mapper()
    result, _ = _DEFAULT_MAPPER.analyze_full(type_id)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selfcheck", action="store_true", help="run all bundled fixture regressions")
    parser.add_argument("--editor", type=Path, default=DEFAULT_EDITOR, help="read-only editor.exe path")
    parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS, help="t01h census JSON path")
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES, help="normalized fixtures JSON path")
    args = parser.parse_args(argv)
    if not args.selfcheck:
        parser.print_help()
        return 2
    try:
        result = _active_mapper(args.editor, args.census, args.fixtures).selfcheck()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2
    output = OUTDIR / "fixtures_result.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in result["fixtures"]:
        print(f"{row['source']}: candidates={row['reproduced_fields']}/{row['fixture_fields']}; "
              f"exact={row['matching_fields']}/{row['fixture_fields']} "
              f"({row['offset_agreement'] * 100:.1f}%; {row['mode']})")
    summary = result["summary"]
    print(f"mean={summary['mean_field_agreement_percent']:.2f}%; "
          f">=80% fixtures={summary['passed_80_percent']}/{summary['fixture_count']}")
    passed_modes = [m for m, v in summary["modes"].items() if v["passes_80_percent"]]
    print("modes passed (all fixture cases >=80%): " + (", ".join(passed_modes) if passed_modes else "none"))
    print(f"wrote {output}")
    return 0 if summary["passed_80_percent"] >= summary["required_pass_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
