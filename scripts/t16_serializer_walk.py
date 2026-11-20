#!/usr/bin/env python3
"""t16: walk class-reader serializers and align static 4CC evidence to schema.

Read-only inputs: t14 factory/RTTI census, t05 schema/read widths, t08/t12
4CC evidence, and the frozen t01f/t12 golden artifacts. Writes only
scratch/t16/out. Exit codes: 0 checks passed, 1 acceptance check failed,
2 usage or fatal input/dependency error.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from collections import Counter, deque, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t16/out"
EDITOR = Path(r"<OLD_REPO>\input\editor.exe")
CENSUS = ROOT / "scratch/t14/out/census.json"
STAGE2 = ROOT / "scratch/t14/out/stage2_map.json"
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
CODES = ROOT / "scratch/t12/out/codes_full.json"
CHAINS = ROOT / "scratch/t08/out/chains.json"
NAMES = ROOT / "reports/t12_field_names.json"
COMP_GOLD = ROOT / "reports/t01f_comp_row_offsets.json"
CITY_COUNT = 56293
FACTORY_BASE = 0xF49D38
FACTORY_TAIL_VA = 0x140F4A6A9
MAX_DEPTH = 4
MAX_FUNC_BYTES = 0x3000


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def status_ok(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, "missing"
    value = load_json(path).get("status")
    return (value == "complete" or (isinstance(value, str) and value.startswith("complete_"))), str(value)


def norm_tag(value: str) -> str:
    return {
        "nation": "nati", "injury": "inju", "competition": "comp",
        "weather": "weat", "stadium": "stad", "national team": "team",
        "continent": "cont", "language": "lang", "region": "regi",
        "local region": "lcrg", "media source": "mdso", "award": "awar",
    }.get(value.lower(), value.lower())


class Walker:
    def __init__(self) -> None:
        for path in (CENSUS, STAGE2, SCHEMA, CODES, CHAINS, EDITOR):
            if not path.exists():
                raise FileNotFoundError(path)
        valid, observed = status_ok(STAGE2)
        if not valid:
            raise RuntimeError(f"t14 precondition failed: status={observed}")
        try:
            from capstone import CS_ARCH_X86, CS_MODE_64, Cs
            import importlib.util
            scripts = str(ROOT / "scripts")
            if scripts not in sys.path:
                sys.path.insert(0, scripts)
            import t05_pe
        except Exception as exc:
            raise RuntimeError(f"capstone/pefile dependency unavailable: {exc}") from exc
        self.Cs = Cs
        self.CS_ARCH_X86 = CS_ARCH_X86
        self.CS_MODE_64 = CS_MODE_64
        self.pe = t05_pe.PE(EDITOR)
        self.raw = self.pe.raw
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.census = load_json(CENSUS)
        self.stage2 = load_json(STAGE2)
        self.schema = load_json(SCHEMA)
        self.codes = load_json(CODES)["codes"]
        self.chains = load_json(CHAINS)["chains"]
        self.names = load_json(NAMES) if NAMES.exists() else {"slots": []}
        self.comp_gold = load_json(COMP_GOLD) if COMP_GOLD.exists() else {}
        nation_gold_path = ROOT / "scratch/t01/inbox/t01g/output.json"
        self.nation_gold = load_json(nation_gold_path) if nation_gold_path.exists() else {}
        self.rows = self.census.get("tables", [])
        self.by_type = {int(row["table_type"]): row for row in self.rows}
        self.call_fanout = self._factory_call_fanout()
        self.code_chain: dict[str, str] = {}
        for chain in self.chains:
            for code in chain.get("codes", []):
                self.code_chain.setdefault(code, chain.get("chain_id", ""))

    def disasm(self, file_off: int, size: int = MAX_FUNC_BYTES, stop_terminator: bool = True):
        va = self.pe.f2va(file_off)
        if va is None or file_off < 0 or file_off >= len(self.raw):
            return []
        out = []
        for ins in self.md.disasm(self.raw[file_off:min(len(self.raw), file_off + size)], va):
            out.append(ins)
            if stop_terminator and ins.mnemonic in ("ret", "retf", "iret", "iretq", "int3"):
                break
            if stop_terminator and ins.mnemonic == "jmp":
                # Factory tails and thunks terminate the current linear block.
                break
        return out

    def file_off(self, ins) -> int:
        value = self.pe.va2f(ins.address)
        return value if value is not None else -1

    def direct_calls(self, insns) -> list[tuple[int, int]]:
        calls = []
        for ins in insns:
            if ins.mnemonic != "call" or not ins.operands:
                continue
            op = ins.operands[0]
            if op.type == 2:
                target = self.pe.va2f(op.imm)
                if target is not None:
                    calls.append((self.file_off(ins), target))
        return calls

    def _factory_call_fanout(self) -> Counter[int]:
        counts: Counter[int] = Counter()
        for row in self.rows:
            try:
                start = int(row["handler_off"], 16)
            except (KeyError, TypeError, ValueError):
                continue
            for _, target in self.direct_calls(self.disasm(start, 0x400, True)):
                counts[target] += 1
        return counts

    def class_trace(self, row: dict[str, Any]) -> dict[str, Any]:
        handler = int(row["handler_off"], 16)
        cls = row.get("primary_class") or ""
        vt = next((x for x in row.get("vtables", []) if x.get("class") == cls), None)
        if not vt or not vt.get("vtable_va"):
            return {"status": "no_class_vtable", "handler_off": hex(handler), "class": cls,
                    "visited": [], "reader": None, "serializer_functions": []}
        vtable_va = int(vt["vtable_va"], 16)
        visited: list[dict[str, Any]] = []
        seen: set[int] = set()
        queue = deque([(handler, 0)])
        vtable_assignment = False
        while queue:
            off, depth = queue.popleft()
            if off in seen or depth > MAX_DEPTH:
                continue
            seen.add(off)
            insns = self.disasm(off, 0x400 if depth == 0 else MAX_FUNC_BYTES, True)
            visited.append({"file_off": hex(off), "depth": depth, "instructions": len(insns)})
            if self._has_vtable_store(insns, vtable_va):
                vtable_assignment = True
            if depth == MAX_DEPTH:
                continue
            for _, target in self.direct_calls(insns):
                if self.call_fanout.get(target, 0) > 50:
                    continue
                if target not in seen:
                    queue.append((target, depth + 1))
        vtoff = self.pe.va2f(vtable_va)
        reader_va = struct.unpack_from("<Q", self.raw, vtoff + 19 * 8)[0] if vtoff is not None else 0
        reader_off = self.pe.va2f(reader_va)
        if reader_off is None:
            return {"status": "slot19_unmapped", "handler_off": hex(handler), "class": cls,
                    "vtable_va": hex(vtable_va), "vtable_assignment_found": vtable_assignment,
                    "visited": visited, "reader": hex(reader_va), "serializer_functions": []}
        serializer_functions = self.serializer_candidates(reader_off)
        return {"status": "ok" if serializer_functions else "reader_found_no_width_walk",
                "handler_off": hex(handler), "class": cls, "vtable_va": hex(vtable_va),
                "vtable_assignment_found": vtable_assignment, "visited": visited,
                "reader_va": hex(reader_va), "reader_off": hex(reader_off),
                "serializer_functions": serializer_functions}

    def _has_vtable_store(self, insns, vtable_va: int) -> bool:
        for i, ins in enumerate(insns):
            if ins.mnemonic != "lea" or len(ins.operands) != 2:
                continue
            dst, src = ins.operands
            if dst.type != 1 or src.type != 3 or src.mem.base != 41:
                continue
            target = ins.address + ins.size + src.mem.disp
            if target != vtable_va:
                continue
            reg = dst.reg
            for nxt in insns[i + 1:i + 7]:
                if nxt.mnemonic == "mov" and len(nxt.operands) == 2:
                    d, s = nxt.operands
                    if d.type == 3 and s.type == 1 and s.reg == reg:
                        return True
                    if d.type == 1 and s.type == 1 and s.reg == reg:
                        reg = d.reg
        return False

    def follow_thunks(self, start: int, max_hops: int = 8) -> list[int]:
        chain = [start]
        cur = start
        for _ in range(max_hops):
            insns = self.disasm(cur, 16, False)
            if not insns or insns[0].mnemonic != "jmp" or not insns[0].operands:
                break
            op = insns[0].operands[0]
            if op.type != 2:
                break
            nxt = self.pe.va2f(op.imm)
            if nxt is None or nxt in chain:
                break
            chain.append(nxt)
            cur = nxt
        return chain

    def serializer_candidates(self, reader_off: int) -> list[dict[str, Any]]:
        # Follow import/thunk wrappers and then bounded direct-call BFS. More
        # than 50 factory users is treated as shared runtime, not class code.
        roots = self.follow_thunks(reader_off)
        queue = deque((off, 0) for off in roots)
        seen: set[int] = set()
        found: list[dict[str, Any]] = []
        while queue:
            off, depth = queue.popleft()
            if off in seen or depth > MAX_DEPTH:
                continue
            seen.add(off)
            insns = self.disasm(off, MAX_FUNC_BYTES, True)
            events = self.stream_events(insns)
            if events:
                found.append({"function_off": hex(off), "depth": depth, "events": events,
                              "event_count": len(events),
                              "branch_count": sum(i.mnemonic.startswith("j") and i.mnemonic != "jmp" for i in insns)})
            if depth == MAX_DEPTH:
                continue
            for _, target in self.direct_calls(insns):
                if self.call_fanout.get(target, 0) > 50:
                    continue
                if target not in seen:
                    queue.append((target, depth + 1))
        found.sort(key=lambda x: (-x["event_count"], x["depth"], int(x["function_off"], 16)))
        return found

    def stream_events(self, insns) -> list[dict[str, Any]]:
        # Small register-origin tracker: RCX is the record base at a normal
        # x64 member reader entry; LEA/MOV/ADD propagate exact constant offsets.
        from capstone.x86_const import X86_REG_RCX, X86_REG_RDX
        origins: dict[int, int] = {X86_REG_RCX: 0}
        width: int | None = None
        width_inst: int | None = None
        events: list[dict[str, Any]] = []
        branch_count = 0
        for ins in insns:
            m = ins.mnemonic
            ops = ins.operands
            if m.startswith("j") and m != "jmp":
                branch_count += 1
            if m == "mov" and len(ops) == 2 and ops[0].type == 1:
                dst, src = ops
                dst_name = self.md.reg_name(dst.reg)
                if dst_name in ("r8d", "r8"):
                    if src.type == 2:
                        width = int(src.imm) if 0 < src.imm <= 0x1000 else None
                        width_inst = self.file_off(ins) if width is not None else None
                    else:
                        width = None
                        width_inst = None
                if src.type == 1 and src.reg in origins:
                    origins[dst.reg] = origins[src.reg]
                elif dst.reg in origins:
                    origins.pop(dst.reg, None)
            elif m == "lea" and len(ops) == 2 and ops[0].type == 1 and ops[1].type == 3:
                dst, src = ops
                base = origins.get(src.mem.base)
                if base is not None and src.mem.index == 0:
                    origins[dst.reg] = base + int(src.mem.disp)
                else:
                    origins.pop(dst.reg, None)
            elif m == "add" and len(ops) == 2 and ops[0].type == 1 and ops[1].type == 2:
                if ops[0].reg in origins:
                    origins[ops[0].reg] += int(ops[1].imm)
            elif m == "call" and ins.op_str.startswith("qword ptr [") and "+ 0x28" in ins.op_str:
                obj_off = origins.get(X86_REG_RDX)
                if width is not None:
                    events.append({"width": width, "object_off": obj_off,
                                   "inst_off": hex(width_inst) if width_inst is not None else None,
                                   "call_off": hex(self.file_off(ins)), "branch_depth": branch_count,
                                   "instruction": f"mov r8d, {width}"})
                width = None
                width_inst = None
        return events

    def entity_schema(self, entity: str) -> tuple[str, dict[str, Any]]:
        entities = self.schema.get("entities", {})
        if entity in entities:
            return entities[entity].get("code", norm_tag(entity)), entities[entity]
        tag = norm_tag(entity)
        for name, obj in entities.items():
            if obj.get("code") == tag:
                return tag, obj
        raise KeyError(f"unknown schema entity/tag: {entity}")

    def class_rows(self, entity: str) -> list[dict[str, Any]]:
        tag, _ = self.entity_schema(entity)
        rows = [r for r in self.rows if r.get("entity_tag") == tag and r.get("primary_class")]
        if entity.lower() == "nation":
            rows = [r for r in rows if r.get("primary_class") == "NATION"]
        return sorted(rows, key=lambda r: int(r["table_type"]))

    def field_rows(self, entity: str, class_limit: int | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
        tag, entity_schema = self.entity_schema(entity)
        all_schema_fields = entity_schema.get("fields", [])
        schema_fields = [f for f in all_schema_fields if f.get("parent") is None]
        nested_schema_fields = [f for f in all_schema_fields if f.get("parent") is not None]
        type_widths = self.schema.get("type_width_candidates", {})
        preferred_class = {"city":"CITY", "club":"LEAGUE_BODY_CLUB", "comp":"COMP",
                           "nati":"NATION", "stad":"STADIUM", "inju":"INJURY",
                           "weat":"WEATHER", "team":"NATIONAL_TEAM"}.get(tag)
        classes = self.class_rows(entity)
        if class_limit:
            classes = classes[:class_limit]
        selected = next((r for r in classes if r.get("primary_class") == preferred_class), None) if preferred_class else None
        if selected is None and classes:
            selected = classes[0]
        selected_type = selected.get("table_type") if selected else None
        accesses: list[dict[str, Any]] = []
        branch_accesses: list[dict[str, Any]] = []
        traces = []
        for row in classes:
            trace = self.class_trace(row)
            traces.append({"table_type": row["table_type"], "class": row.get("primary_class"), **trace})
            functions = trace.get("serializer_functions", [])
            if functions:
                cursor = 0
                for event in functions[0]["events"]:
                    access = dict(event)
                    access.update({"table_type": row["table_type"], "class": row.get("primary_class"),
                                   "row_offset_candidate": cursor})
                    (accesses if row.get("table_type") == selected_type else branch_accesses).append(access)
                    cursor += int(event["width"])
        by_member: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
        for code, entries in self.codes.items():
            for inst in entries:
                if inst.get("shape") == "read" and inst.get("object_off") is not None and inst.get("size") is not None:
                    by_member[(int(inst["object_off"]), int(inst["size"]))].append(
                        {"code": code, "inst": inst, "chain": self.code_chain.get(code)})
        code_count = Counter(f.get("code") for f in schema_fields)
        outputs = []
        conflicts = []
        claim_slots: dict[tuple[Any, ...], list[int]] = defaultdict(list)
        for field in schema_fields:
            code, typ = field.get("code"), field.get("type", "unknown")
            allowed = set(type_widths.get(typ, {}).get("candidates", []))
            candidates = []
            for access in accesses:
                if access.get("object_off") is None:
                    continue
                width = int(access["width"])
                if allowed and width not in allowed:
                    continue
                for match in by_member.get((int(access["object_off"]), width), []):
                    if match["code"] == code:
                        candidates.append((access, match))
            unique = {(x[0].get("table_type"), x[0].get("row_offset_candidate"),
                       x[0].get("width"), x[0].get("inst_off"), x[1]["code"]): x for x in candidates}
            candidates = list(unique.values())
            duplicate_schema_code = code_count[code] > 1
            if len(candidates) == 1 and not duplicate_schema_code:
                access, match = candidates[0]
                slot_key = (access.get("table_type"), access.get("row_offset_candidate"),
                            access.get("width"), access.get("object_off"), access.get("inst_off"))
                claim_slots[slot_key].append(len(outputs))
                outputs.append({"field": code, "offset": access["row_offset_candidate"],
                                "width": access["width"], "type": typ,
                                "evidence": {"inst_off": access.get("inst_off"),
                                             "instruction": access.get("instruction"),
                                             "4CC_chain": match.get("chain"),
                                             "access_inst_off": match["inst"].get("file_off"),
                                             "serializer_call_off": access.get("call_off"),
                                             "factory_type": access.get("table_type"),
                                             "class": access.get("class"),
                                             "object_off": access.get("object_off")},
                                "grade": "L3", "mapping_status": "unique_static_candidate"})
            else:
                outputs.append({"field": code, "offset": None, "width": None, "type": typ,
                                "evidence": {}, "grade": "unmapped", "mapping_status": "unnamed"})
                if len(candidates) > 1 or duplicate_schema_code:
                    conflicts.append({"field": code,
                                      "reason": "duplicate_schema_code" if duplicate_schema_code else "non_injective_walk_match",
                                      "candidate_count": len(candidates),
                                      "candidates": [{"row_offset": x[0].get("row_offset_candidate"),
                                                      "object_off": x[0].get("object_off"),
                                                      "inst_off": x[0].get("inst_off"),
                                                      "4CC": x[1]["code"]} for x in candidates]})
        # Enforce injection globally: a single serializer slot cannot name two
        # schema fields, even if each field independently had one candidate.
        for slot_key, indexes in claim_slots.items():
            if len(indexes) <= 1:
                continue
            fields = [outputs[i]["field"] for i in indexes]
            for i in indexes:
                outputs[i].update({"offset": None, "width": None, "evidence": {},
                                   "grade": "unmapped", "mapping_status": "conflict"})
                conflicts.append({"field": outputs[i]["field"], "reason": "multiple_schema_fields_claim_same_walk_slot",
                                  "conflicting_fields": fields,
                                  "slot": {"table_type": slot_key[0], "row_offset": slot_key[1],
                                           "width": slot_key[2], "object_off": slot_key[3],
                                           "inst_off": slot_key[4]}})
        # Golden field tables are hard conflict guards: a fresh static walk
        # must not overwrite a known reference offset with a linear-path guess.
        reference_slots: dict[str, tuple[int, int]] = {}
        if tag == "comp":
            for code, item in self.comp_gold.get("row_offset_map", {}).items():
                if item.get("counted_as_new_schema_business_field"):
                    reference_slots[code] = (int(item["row_offset"]), int(item["width"]))
        elif tag == "city":
            for slot in self.names.get("slots", []):
                if slot.get("type_id") != 2 or slot.get("archive") != "client":
                    continue
                codes = slot.get("codes", [])
                for ordinal, code in enumerate(codes):
                    split = int(slot.get("width", 0)) == 8 and len(codes) == 2
                    reference_slots[code] = (int(slot["row_off"]) + (4 * ordinal if split else 0),
                                             4 if split else int(slot["width"]))
        for output in outputs:
            code = output.get("field")
            expected = reference_slots.get(code)
            if output.get("grade") == "L3" and expected and (output.get("offset"), output.get("width")) != expected:
                observed = {"offset": output.get("offset"), "width": output.get("width"),
                            "inst_off": output.get("evidence", {}).get("inst_off")}
                conflicts.append({"field": code, "reason": "fresh_walk_conflicts_with_frozen_golden",
                                  "expected": {"offset": expected[0], "width": expected[1]},
                                  "observed": observed})
                output.update({"offset": None, "width": None, "evidence": {},
                               "grade": "unmapped", "mapping_status": "golden_conflict"})
        nested = [{"field": f.get("code"), "parent": f.get("parent"), "type": f.get("type", "unknown"),
                   "offset": None, "width": None, "grade": "unmapped"} for f in nested_schema_fields]
        doc = {"status": "partial_engine_candidates", "entity": entity, "entity_tag": tag,
               "primary_class": selected.get("primary_class") if selected else None,
               "classes_walked": len(traces), "fields_total": len(schema_fields),
               "fields_named": sum(x["grade"] == "L3" for x in outputs),
               "fields_unnamed": sum(x["grade"] != "L3" for x in outputs),
               "nested_fields_total": len(nested), "nested_fields": nested,
               "conflicts": conflicts, "fields": outputs,
               "walk": {"classes": traces, "accesses": accesses, "other_branch_accesses": branch_accesses}}
        return doc, {"entity": entity, "fields_total": len(schema_fields),
                     "fields_named": doc["fields_named"], "fields_unnamed": doc["fields_unnamed"],
                     "conflicts": len(conflicts), "evidence_grade": "L3_static_candidate",
                     "status": doc["status"]}

    def golden_city(self) -> dict[str, Any]:
        rows = [x for x in self.names.get("slots", []) if x.get("type_id") == 2 and x.get("archive") == "client"]
        required = {"Cnti", "Clgi", "Clri", "Cwea"}
        named_refs = {code for slot in rows if slot.get("field") and slot.get("confidence") == "ref_only"
                      for code in slot.get("codes", []) if code in required and slot.get("evidence", {}).get("file_off")}
        t14_city = next((x for x in self.stage2.get("tables", []) if x.get("table_type") == 2), {})
        walk, _ = self.field_rows("city", class_limit=1)
        engine_refs = sorted({x["field"] for x in walk.get("fields", [])
                              if x.get("grade") == "L3" and x.get("field") in required})
        baseline_ok = len(named_refs) >= 3 and t14_city.get("count") == CITY_COUNT
        passed = baseline_ok and len(engine_refs) >= 3
        return {"entity": "city", "status": "pass" if passed else "fail",
                "baseline_status": "pass" if baseline_ok else "fail",
                "required_reference_fields": sorted(required), "named_reference_fields": sorted(named_refs),
                "engine_named_reference_fields": engine_refs, "engine_fields_named": walk.get("fields_named", 0),
                "engine_conflicts": walk.get("conflicts", []), "expected_min_named": 3, "table_type": 2, "row_count": t14_city.get("count"),
                "row_count_expected": CITY_COUNT,
                "source": "reports/t12_field_names.json + scratch/t14/out/stage2_map.json + fresh t16 reader walk",
                "note": "Gate requires fresh t16 mapping; inherited E55 names alone do not pass."}

    def golden_comp(self) -> dict[str, Any]:
        data = self.comp_gold
        rowmap = data.get("row_offset_map", {})
        layout = data.get("row_codec", {}).get("cursor_layout", [])
        expected = {k: v for k, v in rowmap.items() if v.get("counted_as_new_schema_business_field")}
        checked = []
        failures = []
        for code, field in expected.items():
            item = next((x for x in layout if x.get("step") == code and
                         x.get("row_offset") == field.get("row_offset") and
                         x.get("width") == field.get("width") and
                         x.get("object_offset") == field.get("object_offset")), None)
            if item is None:
                failures.append({"field": code, "reason": "no_cursor_layout_match"})
                continue
            evidence = item.get("evidence", {})
            width_ev = evidence.get("read_bytes") or evidence.get("widths", [{}])[0]
            addr = width_ev.get("file_offset") if isinstance(width_ev, dict) else None
            rawbytes = b""
            try:
                off = int(addr, 16)
                rawbytes = self.raw[off:off + 24]
            except (TypeError, ValueError):
                off = -1
            # Verify actual immediate width plus stream-call opcode somewhere
            # in the documented sequence; the E20 artifact remains the gold map.
            width = int(field.get("width", 0))
            needle = b"\x41\xb8" + struct.pack("<I", width)
            stream_call = any(rawbytes[i] == 0xff and i + 2 < len(rawbytes) and rawbytes[i + 2] == 0x28
                              for i in range(max(0, len(rawbytes) - 2)))
            ok = off >= 0 and needle in rawbytes and stream_call
            checked.append({"field": code, "row_offset": field.get("row_offset"), "width": width,
                            "object_offset": field.get("object_offset"), "inst_off": addr,
                            "instruction_bytes_verified": ok})
            if not ok:
                failures.append({"field": code, "reason": "instruction_width_or_stream_call_mismatch", "inst_off": addr})
        walk, _ = self.field_rows("comp", class_limit=1)
        expected_map = {code: (int(item["row_offset"]), int(item["width"])) for code, item in expected.items()}
        engine_map = {x["field"]: (x.get("offset"), x.get("width")) for x in walk.get("fields", [])
                      if x.get("grade") == "L3"}
        engine_matches = sorted(code for code, value in expected_map.items() if engine_map.get(code) == value)
        baseline_ok = len(expected) == 18 and len(checked) == 18 and not failures
        passed = baseline_ok and len(engine_matches) == 18
        return {"entity": "comp", "status": "pass" if passed else "fail",
                "baseline_status": "pass" if baseline_ok else "fail",
                "expected_fields": len(expected), "rechecked_fields": len(checked),
                "matched_fields": sum(1 for x in checked if x["instruction_bytes_verified"]),
                "engine_reproduced_fields": len(engine_matches), "engine_matched_codes": engine_matches,
                "engine_fields_named": walk.get("fields_named", 0), "engine_conflicts": walk.get("conflicts", []),
                "failures": failures, "fields": checked,
                "source": "reports/t01f_comp_row_offsets.json (E20 baseline) + editor.exe bytes + fresh t16 reader walk",
                "note": "E20 baseline byte checks are separate from fresh t16 serializer-walk reproduction."}

    def golden_weather(self) -> dict[str, Any]:
        entity = self.schema.get("entities", {}).get("weather", {})
        weather_codes = [x.get("code") for x in entity.get("fields", [])
                         if x.get("code") == "wnam" or re.fullmatch(r"w[0-3](?:sd|p[0-4]|w[0-4]|t[ev0-7]|dn)", x.get("code", ""))]
        artifact_candidates = [ROOT / "scratch/t27/out", ROOT / "reports/t27_weather_offsets.json",
                               ROOT / "evidence/fm24/reports/t27_weather_offsets.json"]
        present = [str(p.relative_to(ROOT)) for p in artifact_candidates if p.exists()]
        # Current t12 evidence has only a few path-descend weather codes and no
        # direct 88-field season offset baseline; do not synthesize offsets.
        available_code_instances = [code for code in weather_codes if self.codes.get(code)]
        passed = len(weather_codes) == 89 and bool(present)
        return {"entity": "weather", "status": "pass" if passed else "fail",
                "expected_l3_fields": 89, "schema_target_fields_found": len(weather_codes),
                "available_baseline_artifacts": present,
                "codes_with_any_t12_instance": len(available_code_instances),
                "sample_codes_with_instances": available_code_instances[:12],
                "failure": "E27 89-field offset artifact is absent from this workspace; seasonal 4CCs are not enough to infer row offsets.",
                "source": "scratch/t05/schema_inventory.json, scratch/t12/out/codes_full.json, workspace artifact check"}


def write_json(path: Path, doc: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_golden_tables(w: Walker, results: dict[str, Any]) -> list[dict[str, Any]]:
    ledger = []
    # Preserve the E42 and E20 L3 rows as explicit inherited baselines, and
    # leave all unsupported fields present but unnamed. No inference is added.
    city_tag, city_schema = w.entity_schema("city")
    city_fields = []
    city_slots = [x for x in w.names.get("slots", []) if x.get("type_id") == 2 and x.get("archive") == "client"]
    city_by_code: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for slot in city_slots:
        for code in slot.get("codes", []):
            city_by_code[code].append(slot)
    for f in city_schema.get("fields", []):
        code, typ = f.get("code"), f.get("type", "unknown")
        options = city_by_code.get(code, [])
        if len(options) == 1 and options[0].get("row_off") is not None and options[0].get("evidence", {}).get("file_off"):
            slot = options[0]
            slot_codes = slot.get("codes", [])
            split_pair = int(slot.get("width", 0)) == 8 and len(slot_codes) == 2 and code in slot_codes
            ordinal = slot_codes.index(code) if split_pair else 0
            field_width = 4 if split_pair else slot["width"]
            field_offset = int(slot["row_off"]) + (4 * ordinal if split_pair else 0)
            code_inst = next((x for x in w.codes.get(code, []) if x.get("shape") == "read" and
                              x.get("object_off") == int(slot.get("object_off", -1)) + (4 * ordinal if split_pair else 0) and
                              x.get("size") == field_width), None)
            inst_off = code_inst.get("file_off") if code_inst else slot["evidence"]["file_off"]
            off = int(str(inst_off), 16)
            insns = w.disasm(off, 16, False)
            inst = insns[0] if insns else None
            city_fields.append({"field": code, "offset": field_offset, "width": field_width, "type": typ,
                                "evidence": {"inst_off": inst_off,
                                             "instruction": f"{inst.mnemonic} {inst.op_str}" if inst else None,
                                             "4CC_chain": w.code_chain.get(code),
                                             "source": "reports/t12_field_names.json + t12 direct code instance"},
                                "grade": "L3", "origin": "inherited_named_slot"})
        else:
            city_fields.append({"field": code, "offset": None, "width": None, "type": typ,
                                "evidence": {}, "grade": "unmapped", "origin": "not_reproduced_by_t16"})
    city_named = sum(x["grade"] == "L3" for x in city_fields)
    city_doc = {"status": "partial_golden_gate_failed", "entity": "city", "fields_total": len(city_fields),
                "fields_named": city_named, "fields_unnamed": len(city_fields) - city_named,
                "conflicts": [], "fields": city_fields,
                "note": "Inherited E55 named-slot evidence is kept distinct; no claim of fresh E42 walk reproduction."}
    write_json(OUT / "fields_city.json", city_doc)
    ledger.append({"entity": "city", "fields_total": len(city_fields), "fields_named": city_named,
                   "fields_unnamed": len(city_fields) - city_named, "conflicts": 0,
                   "evidence_grade": "L3_inherited_and_t16_walk_not_closed", "status": city_doc["status"]})

    comp_schema = w.schema.get("entities", {}).get("comp", {})
    comp_top_fields = [f for f in comp_schema.get("fields", []) if f.get("parent") is None]
    comp_types: dict[str, str] = {}
    for f in comp_top_fields:
        comp_types.setdefault(f.get("code"), f.get("type", "unknown"))
    rowmap = w.comp_gold.get("row_offset_map", {})
    comp_fields = []
    for code, item in rowmap.items():
        if not item.get("counted_as_new_schema_business_field"):
            continue
        step = next((x for x in w.comp_gold.get("row_codec", {}).get("cursor_layout", [])
                     if x.get("step") == code and x.get("row_offset") == item.get("row_offset")), {})
        ev = step.get("evidence", {})
        w_ev = ev.get("read_bytes") or (ev.get("widths") or [{}])[0]
        addr = w_ev.get("file_offset") if isinstance(w_ev, dict) else None
        try:
            off = int(addr, 16)
            ins = next(iter(w.md.disasm(w.raw[off:off + 16], w.pe.f2va(off))), None)
            text = f"{ins.mnemonic} {ins.op_str}" if ins else None
        except (TypeError, ValueError):
            text = None
        comp_fields.append({"field": code, "offset": item.get("row_offset"), "width": item.get("width"),
                            "type": comp_types.get(code, "unknown"),
                            "evidence": {"inst_off": addr, "instruction": text,
                                         "4CC_chain": w.code_chain.get(code),
                                         "source": "reports/t01f_comp_row_offsets.json"},
                            "grade": "L3", "origin": "inherited_E20_baseline"})
    known = {x["field"] for x in comp_fields}
    for f in comp_top_fields:
        if f.get("code") not in known:
            comp_fields.append({"field": f.get("code"), "offset": None, "width": None,
                                "type": f.get("type", "unknown"), "evidence": {},
                                "grade": "unmapped", "origin": "not_reproduced_by_t16"})
    comp_named = sum(x["grade"] == "L3" for x in comp_fields)
    comp_doc = {"status": "partial_golden_gate_failed", "entity": "comp", "fields_total": len(comp_top_fields),
                "fields_named": comp_named, "fields_unnamed": len(comp_fields) - comp_named,
                "conflicts": [], "fields": comp_fields,
                "note": "E20's 18 L3 rows are preserved as inherited baseline, not fresh t16 walk output."}
    write_json(OUT / "fields_comp.json", comp_doc)
    ledger.append({"entity": "comp", "fields_total": comp_doc["fields_total"], "fields_named": comp_named,
                   "fields_unnamed": comp_doc["fields_unnamed"], "conflicts": 0,
                   "evidence_grade": "L3_inherited_E20_and_t16_walk_not_closed", "status": comp_doc["status"]})

    _, weather_schema = w.entity_schema("weather")
    weather_fields = [{"field": f.get("code"), "offset": None, "width": None, "type": f.get("type", "unknown"),
                       "evidence": {}, "grade": "unmapped", "origin": "E27_baseline_missing"}
                      for f in weather_schema.get("fields", [])]
    weather_doc = {"status": "partial_missing_E27_baseline", "entity": "weather",
                   "fields_total": len(weather_fields), "fields_named": 0,
                   "fields_unnamed": len(weather_fields), "conflicts": [], "fields": weather_fields}
    write_json(OUT / "fields_weather.json", weather_doc)
    ledger.append({"entity": "weather", "fields_total": len(weather_fields), "fields_named": 0,
                   "fields_unnamed": len(weather_fields), "conflicts": 0,
                   "evidence_grade": "none_E27_reference_missing", "status": weather_doc["status"]})

    nation_schema = w.schema.get("entities", {}).get("nation", {})
    nation_top = [f for f in nation_schema.get("fields", []) if f.get("parent") is None]
    nation_map = w.nation_gold.get("row_offset_map", {})
    nation_fields = []
    for f in nation_top:
        code, typ = f.get("code"), f.get("type", "unknown")
        item = nation_map.get(code)
        if item and item.get("serializer", {}).get("width_instruction", {}).get("file_offset"):
            width_ev = item["serializer"]["width_instruction"]
            nation_fields.append({"field": code, "offset": item.get("row_offset"), "width": item.get("width"),
                                 "type": typ,
                                 "evidence": {"inst_off": width_ev.get("file_offset"),
                                              "instruction": width_ev.get("instruction"),
                                              "4CC_chain": w.code_chain.get(code),
                                              "source": "scratch/t01/inbox/t01g/output.json"},
                                 "grade": "L3", "origin": "inherited_t01g_baseline"})
        else:
            nation_fields.append({"field": code, "offset": None, "width": None, "type": typ,
                                  "evidence": {}, "grade": "unmapped", "origin": "not_reproduced_by_t16"})
    nation_nested = [{"field": f.get("code"), "parent": f.get("parent"), "type": f.get("type", "unknown"),
                      "offset": None, "width": None, "grade": "unmapped"}
                     for f in nation_schema.get("fields", []) if f.get("parent") is not None]
    nation_named = sum(x["grade"] == "L3" for x in nation_fields)
    nation_doc = {"status": "partial_golden_gate_failed", "entity": "nation", "entity_tag": "nati",
                  "fields_total": len(nation_top), "fields_named": nation_named,
                  "fields_unnamed": len(nation_fields) - nation_named, "nested_fields_total": len(nation_nested),
                  "nested_fields": nation_nested, "conflicts": [], "fields": nation_fields,
                  "note": "Seven t01g L3 prefix fields retained as inherited evidence; fresh t16 walk did not reproduce them."}
    write_json(OUT / "fields_nati.json", nation_doc)
    ledger.append({"entity": "nation", "fields_total": len(nation_top), "fields_named": nation_named,
                   "fields_unnamed": len(nation_fields) - nation_named, "conflicts": 0,
                   "evidence_grade": "L3_inherited_t01g_and_t16_walk_not_closed", "status": nation_doc["status"]})
    return ledger


def write_reports(w: Walker, golden: dict[str, Any], ledger: list[dict[str, Any]], status: str) -> None:
    doc = {"status": status, "golden": golden, "entities": ledger,
           "batch_gate": "blocked: all three goldens must pass before batch release"}
    write_json(OUT / "golden_results.json", doc)
    write_json(OUT / "ledger.json", {"status": status, "entities": ledger,
                                      "golden_status": {k: v.get("status") for k, v in golden.items()}})
    lines = ["# t16 ledger", "", f"Status: `{status}`", "", "| entity | total | named | unnamed | conflicts | evidence | result |",
             "|---|---:|---:|---:|---:|---|---|"]
    for x in ledger:
        lines.append(f"| {x['entity']} | {x['fields_total']} | {x['fields_named']} | {x['fields_unnamed']} | {x['conflicts']} | {x['evidence_grade']} | {x.get('status','—')} |")
    lines.extend(["", "## Golden gate", ""])
    for key, value in golden.items():
        lines.append(f"- {key}: `{value.get('status')}`")
    lines.extend(["", "Batch extraction was not run because the golden gate is not fully green."])
    (OUT / "ledger.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    report = ["# t16 serializer walk — partial", "",
              f"Status: `{status}`. t14 stage2_map.json passed precondition with status `{w.stage2.get('status')}`.", "",
              "## Method implemented", "",
              "- Per-class factory handler comes from the frozen t14 census; direct call targets are walked with a visited set to depth 4. Targets called by more than 50 factory handlers are skipped as shared runtime.",
              "- Class RTTI vtable slot 19 is read from the verified class vtable; bounded direct-call BFS follows thunks/wrappers and scans `mov r8d, imm` + stream virtual calls, propagating simple record-base LEA/MOV aliases.",
              "- Exact code matches require a unique `(object_off, width, 4CC)` direct-read instance compatible with the schema type. Ambiguities are kept in conflicts; fields without evidence remain unnamed.",
              "- Engine outputs are candidates only where fixed linear path assumptions are not closed; gold baselines are labeled inherited, never silently attributed to t16.", "",
              "## Golden gate", ""]
    for key, value in golden.items():
        report.append(f"### {key}: `{value.get('status')}`")
        report.append("")
        for k in ("baseline_status", "named_reference_fields", "engine_named_reference_fields", "engine_fields_named",
                  "engine_reproduced_fields", "engine_matched_codes", "engine_conflicts", "row_count", "expected_fields",
                  "rechecked_fields", "matched_fields", "expected_l3_fields", "schema_target_fields_found",
                  "available_baseline_artifacts", "failure"): 
            if k in value:
                report.append(f"- {k}: `{value[k]}`")
        if value.get("failures"):
            report.append(f"- failures: `{value['failures']}`")
        report.append("")
    report.extend(["## Scope and unresolved", "",
                   "Weather E27's 89 L3 expected offsets are not present in this workspace. t12 has sparse weather path-descend records, not the 88 seasonal offsets; these offsets were not synthesized. Because weather fails the gate, no 10-entity batch was released.",
                   "",
                   "City and comp field tables contain explicitly marked inherited E55/E20 baselines; they do not assert fresh full engine reproduction. `fields_nati.json` retains seven t01g L3 prefix fields as inherited evidence; fresh nation walk named none. `fields_weather.json` preserves every schema field as unnamed.",
                   "",
                   "Factory/reader traces for any single debug entity are written by `--entity <name>`; this run does not touch scratch/t05..t14, reports, docs, evidence, game/editor/IDA.", ""])
    (OUT / "REPORT.md").write_text("\n".join(report), encoding="utf-8")


def run_batch(w: Walker) -> list[dict[str, Any]]:
    entities = list(w.schema.get("entities", {}).keys())
    priority = ["club", "nation", "team", "stadium", "injury"]
    ordered = [x for x in priority if x in entities] + [x for x in entities if x not in priority]
    ledger = []
    for name in ordered:
        if name in {"person", "player"}:  # AGENTS.md: PDxx person attribute blocks are out of scope.
            continue
        tag, _ = w.entity_schema(name)
        fields, row = w.field_rows(name)
        write_json(OUT / f"fields_{tag}.json", fields)
        ledger.append(row)
        write_json(OUT / "ledger.json", {"status": "partial_batch_walk", "entities": ledger,
                                         "next_entity": ordered[min(len(ledger), len(ordered) - 1)] if ordered else None})
    return ledger


def main(argv: list[str] | None = None) -> int:
    global OUT
    ap = argparse.ArgumentParser(description="Walk database class serializer readers and map schema 4CC fields.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--entity", help="single schema entity/tag (e.g. club, nation); debug-only, no batch gate bypass")
    g.add_argument("--golden", choices=("city", "weather", "comp"), help="run one frozen golden check")
    g.add_argument("--selftest", action="store_true", help="run all golden checks, including weather's 10-spot E27 test")
    ap.add_argument("--all", action="store_true", help="run all goldens, then batch only if every golden passes (default)")
    ap.add_argument("--outdir", default=str(OUT))
    args = ap.parse_args(argv)
    OUT = Path(args.outdir)
    try:
        w = Walker()
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2

    if args.entity:
        try:
            result, ledger = w.field_rows(args.entity)
            tag = w.entity_schema(args.entity)[0]
            if tag in {"city", "comp", "weat", "nati"}:
                ledger["entity"] = f"debug_{tag}"
            output_name = f"debug_fields_{tag}.json" if tag in {"city", "comp", "weat", "nati"} else f"fields_{tag}.json"
            write_json(OUT / output_name, result)
            write_json(OUT / f"entity_trace_{tag}.json", result.get("walk", {}))
            existing = load_json(OUT / "ledger.json") if (OUT / "ledger.json").exists() else {"status": "partial_single_entity_debug", "entities": []}
            entries = [x for x in existing.get("entities", []) if x.get("entity") != ledger["entity"]]
            entries.append(ledger)
            ledger_status = existing.get("status", "partial_single_entity_debug")
            write_json(OUT / "ledger.json", {"status": ledger_status, "entities": entries})
            ledger_lines = ["# t16 ledger", "", f"Status: `{existing.get('status', 'partial_single_entity_debug')}`", "",
                            "| entity | total | named | unnamed | conflicts | evidence | result |",
                            "|---|---:|---:|---:|---:|---|---|"]
            for item in entries:
                ledger_lines.append(f"| {item.get('entity')} | {item.get('fields_total')} | {item.get('fields_named')} | {item.get('fields_unnamed')} | {item.get('conflicts')} | {item.get('evidence_grade')} | {item.get('status','—')} |")
            ledger_lines.extend(["", "Batch extraction remains gated by city/weather/comp goldens."])
            (OUT / "ledger.md").write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")
            report_path = OUT / "REPORT.md"
            if report_path.exists():
                report_text = report_path.read_text(encoding="utf-8").split("\n## Single-entity debug walks\n", 1)[0]
            else:
                report_text = "# t16 serializer walk — partial\n"
            report_text += "\n## Single-entity debug walks\n\n"
            for trace_path in sorted(OUT.glob("entity_trace_*.json")):
                trace_tag = trace_path.stem.removeprefix("entity_trace_")
                trace_doc = load_json(trace_path)
                field_path = OUT / (f"debug_fields_{trace_tag}.json" if trace_tag in {"city", "comp", "weat", "nati"}
                                   else f"fields_{trace_tag}.json")
                field_doc = load_json(field_path) if field_path.exists() else {}
                report_text += (f"### {field_doc.get('entity', trace_tag)}: walked {field_doc.get('classes_walked', 0)} class branches; "
                                f"{field_doc.get('fields_named', 0)} / {field_doc.get('fields_total', 0)} top-level fields named by fresh walk.\n\n")
                for trace in trace_doc.get("classes", []):
                    funcs = trace.get("serializer_functions", [])
                    counts = ", ".join(f"{fn['function_off']}:{fn['event_count']} events" for fn in funcs[:4]) or "none"
                    report_text += (f"- table {trace.get('table_type')} `{trace.get('class')}`: {trace.get('status')}; "
                                    f"slot19={trace.get('reader_off')}; vtable assignment={trace.get('vtable_assignment_found')}; "
                                    f"candidate serializer branches: {counts}.\n")
                report_text += "\n"
            report_path.write_text(report_text, encoding="utf-8")
            print(json.dumps(ledger, ensure_ascii=False))
            return 0 if result.get("fields_named", 0) > 0 else 1
        except Exception as exc:
            print(f"fatal: {exc}", file=sys.stderr)
            return 2

    checks = {}
    chosen = [args.golden] if args.golden else ["city", "weather", "comp"]
    for name in chosen:
        checks[name] = getattr(w, f"golden_{name}")()
    if args.golden:
        write_json(OUT / f"golden_{args.golden}.json", checks[args.golden])
        print(json.dumps(checks[args.golden], ensure_ascii=False, indent=2))
        return 0 if checks[args.golden]["status"] == "pass" else 1

    passed = all(x.get("status") == "pass" for x in checks.values())
    # Batch is strictly gated behind fresh reproduction of all goldens.
    ledger = write_golden_tables(w, checks)
    if passed:
        ledger = run_batch(w)
        status = "partial_batch_walk"
    else:
        status = "partial_golden_gate_failed"
    write_reports(w, checks, ledger, status)
    write_json(OUT / "status.json", {"status": status,
                                     "t14_status": w.stage2.get("status"),
                                     "batch_released": passed,
                                     "golden_status": {k: v.get("status") for k, v in checks.items()}})
    print(json.dumps({"status": status, "goldens": {k: v.get("status") for k, v in checks.items()},
                      "batch_released": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
