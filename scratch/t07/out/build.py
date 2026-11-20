from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
LAYOUTS = ROOT / "scratch/t05/layouts.json"
READER_WIDTHS = ROOT / "scratch/t05/reader_widths.json"
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
ASSIGNMENTS = ROOT / "scratch/t06/out/assignments.json"

CMP_PREFIXES = tuple(bytes((0x81, x)) for x in (0xFA, 0xFB, 0xF9, 0xF8, 0xFE, 0xFF, 0xFD, 0xFC)) + (b"\x3d",)
BUF_REGS = {"rsi", "rdi", "rcx", "rbx", "rdx", "r8", "r9", "r12", "r13", "r14", "r15"}
OFF_MIN, OFF_MAX = 0x20, 0x400
SIZE = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
RE_READ = re.compile(r"^(?:mov|movzx|movsx|movsxd|movss|movsd)\s+([a-z0-9]+),\s*(byte|word|dword|qword)?\s*ptr\s*\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]$")
RE_WRITE = re.compile(r"^mov\s+(byte|word|dword|qword)\s+ptr\s*\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\],\s*([a-z0-9]+)$")
RE_LEA = re.compile(r"^([a-z0-9]+),\s*\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]$")
RE_MOV_REG = re.compile(r"^([a-z0-9]+),\s*([a-z0-9]+)$")
RE_IMM_CMP = re.compile(r"^([a-z0-9]+),\s*0x([0-9a-f]+)$")
RE_ANY_MEM = re.compile(r"\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]")


def load_pe():
    spec = importlib.util.spec_from_file_location("t05_pe", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.default()


def code_from_imm(imm: bytes) -> str | None:
    chars = imm[::-1]
    if len(chars) != 4 or not all((48 <= c <= 57) or (65 <= c <= 90) or (97 <= c <= 122) for c in chars):
        return None
    return chars.decode("ascii")


def decode_cmp_hits(pe):
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    raw = pe.raw
    hits = []
    for sec in pe._secs:
        if not sec["exec"] or not sec["rawsize"]:
            continue
        start, end = sec["raw"], min(sec["raw"] + sec["rawsize"], len(raw))
        for prefix in CMP_PREFIXES:
            pos = start
            while True:
                pos = raw.find(prefix, pos, end)
                if pos < 0:
                    break
                imm_at = pos + len(prefix)
                if imm_at + 4 <= end:
                    raw_imm = raw[imm_at:imm_at + 4]
                    code = code_from_imm(raw_imm)
                    if code:
                        va = pe.f2va(pos)
                        decoded = list(md.disasm(raw[pos:pos + 12], va or 0)) if va else []
                        if decoded and decoded[0].mnemonic == "cmp":
                            m = RE_IMM_CMP.match(decoded[0].op_str.lower())
                            if m and int(m.group(2), 16) == int.from_bytes(raw_imm, "little"):
                                hits.append((pos, code, va, decoded[0]))
                pos += 1
    unique = {(h[0], h[1]): h for h in hits}
    return sorted(unique.values(), key=lambda h: h[0]), md


def access_of(ins):
    """Return only direct narrow field accesses; a qword pointer load is deliberately excluded."""
    text = (ins.mnemonic + " " + ins.op_str).lower()
    m = RE_READ.match(text)
    if m and m.group(3) in BUF_REGS:
        size = SIZE.get(m.group(2) or "dword", 4)
        off = int(m.group(4), 16) if m.group(4) else 0
        if OFF_MIN <= off <= OFF_MAX and size in (1, 2, 4):
            return off, size, "read", f"{ins.mnemonic} {ins.op_str}"
    m = RE_WRITE.match(text)
    if m and m.group(2) in BUF_REGS:
        size = SIZE[m.group(1)]
        off = int(m.group(3), 16) if m.group(3) else 0
        if OFF_MIN <= off <= OFF_MAX and size in (1, 2, 4):
            return off, size, "write", f"{ins.mnemonic} {ins.op_str}"
    return None


def any_member_operand(ins):
    """Return a direct memory operand on an object-like register, including qword wrappers."""
    m = RE_ANY_MEM.search(ins.op_str.lower())
    if not m or m.group(1) not in BUF_REGS:
        return None
    off = int(m.group(2), 16) if m.group(2) else 0
    if OFF_MIN <= off <= OFF_MAX:
        return off
    return None


def conditional_target(ins):
    if ins.mnemonic not in {"je", "jz", "jne", "jnz", "ja", "jae", "jb", "jbe", "jg", "jge", "jl", "jle", "js", "jns", "jo", "jno", "jp", "jnp"}:
        return None
    try:
        return int(ins.op_str.strip(), 0)
    except ValueError:
        return None


def target_accesses(pe, md, target_va, max_span=0x600):
    """Walk reachable local getter blocks using VA-based disassembly and respecting branches."""
    q = [(target_va, 0)]
    seen, found = set(), []
    while q and len(seen) < 24:
        block_va, depth = q.pop(0)
        if block_va in seen or abs(block_va - target_va) > max_span:
            continue
        seen.add(block_va)
        file_off = pe.va2f(block_va)
        if file_off is None:
            continue
        for ins in md.disasm(pe.raw[file_off:file_off + 0x100], block_va):
            acc = access_of(ins)
            if acc:
                found.append((depth, ins.address, acc))
            if ins.mnemonic == "ret":
                break
            if ins.mnemonic == "jmp":
                try:
                    jva = int(ins.op_str.strip(), 0)
                except ValueError:
                    break
                if abs(jva - target_va) <= max_span:
                    q.append((jva, depth + 1))
                break
            jva = conditional_target(ins)
            if jva is not None:
                if abs(jva - target_va) <= max_span:
                    q.append((jva, depth + 1))
                q.append((ins.address + ins.size, depth + 1))
                break
    found.sort(key=lambda h: (h[0], h[1]))
    return found


def fallthrough_accesses(pe, md, branch, code):
    """Read or write on a `jne skip` fall-through; stop at the first qualifying narrow access."""
    if branch.mnemonic not in ("jne", "jnz"):
        return []
    start_va = branch.address + branch.size
    off = pe.va2f(start_va)
    if off is None:
        return []
    for ins in list(md.disasm(pe.raw[off:off + 0x180], start_va))[:64]:
        if ins.mnemonic == "cmp":
            m = RE_IMM_CMP.match(ins.op_str.lower())
            if m and code_from_imm(int(m.group(2), 16).to_bytes(4, "little")):
                break
        acc = access_of(ins)
        if acc:
            return [(0, ins.address, acc)]
        if ins.mnemonic == "ret":
            break
    return []


def make_record(pe, file_off, code, access, access_va, route, depth, score):
    off, size, kind, insn = access
    route_text = "je 目标块" if route == "getter" else "jne fall-through"
    if depth:
        route_text += f"（CFG 深度 {depth}）"
    return {"code": code, "file_off": hex(file_off), "object_off": off, "size": size,
            "kind": kind, "access_va": hex(access_va), "score": round(score, 3),
            "why": f"{route_text}内 {insn}", "section": pe.section_of(file_off), "_route": route}


def find_candidates(pe, hits, md):
    records = []
    for file_off, code, cmp_va, _cmp in hits:
        cmp_off = pe.va2f(cmp_va)
        if cmp_off is None:
            continue
        block = list(md.disasm(pe.raw[cmp_off:cmp_off + 0x20], cmp_va))
        branch = next((x for x in block[1:4] if x.mnemonic in ("je", "jz", "jne", "jnz")), None)
        if branch is None:
            continue
        if branch.mnemonic in ("je", "jz"):
            try:
                target = int(branch.op_str.strip(), 0)
            except ValueError:
                target = None
            if target is not None:
                for depth, access_va, acc in target_accesses(pe, md, target):
                    if acc[2] == "read":
                        score = 0.91 - min(depth, 4) * 0.025 + (0.02 if acc[3].startswith("movss ") else 0)
                        records.append(make_record(pe, file_off, code, acc, access_va, "getter", depth, score))
                        if sum(1 for r in records if r["file_off"] == hex(file_off) and r["code"] == code) >= 3:
                            break
        if branch.mnemonic in ("jne", "jnz"):
            for depth, access_va, acc in fallthrough_accesses(pe, md, branch, code):
                score = 0.89 if acc[2] == "read" else 0.82
                records.append(make_record(pe, file_off, code, acc, access_va, "setter", depth, score))
    best = {}
    for rec in records:
        key = (rec["code"], rec["file_off"], rec["object_off"], rec["size"], rec["kind"])
        if key not in best or rec["score"] > best[key]["score"]:
            best[key] = rec
    return list(best.values())


def reader_objects(pe, md, body_off, scan_bytes=0x3000):
    """Recover object offsets passed to serializer calls, including LEA aliases moved to RDX."""
    va = pe.f2va(body_off)
    if va is None:
        return []
    aliases, objects = {}, []
    last_width = None
    for ins in md.disasm(pe.raw[body_off:body_off + scan_bytes], va):
        m = RE_LEA.match(ins.op_str.lower()) if ins.mnemonic == "lea" else None
        if m:
            dst, _base, disp = m.groups()
            aliases[dst] = int(disp, 16) if disp else 0
            continue
        m = RE_MOV_REG.match(ins.op_str.lower()) if ins.mnemonic == "mov" else None
        if m:
            dst, src = m.groups()
            if src in aliases:
                aliases[dst] = aliases[src]
            else:
                aliases.pop(dst, None)
        if ins.mnemonic == "mov" and ins.op_str.lower().startswith("r8d,"):
            try:
                last_width = int(ins.op_str.split(",", 1)[1].strip(), 0)
            except ValueError:
                last_width = None
        if ins.mnemonic == "call" and re.search(r"\[rax\s*\+\s*0x28\]", ins.op_str.lower()):
            objects.append(aliases.get("rdx"))
            last_width = None
    return objects


def build_reader_maps(pe, md, layouts, rw):
    rw_by_type = {r["type_id"]: r for r in rw.get("results", [])}
    maps = {}
    for layout in layouts.get("layouts", []):
        tid = layout["type_id"]
        body = layout.get("reader_body")
        derived = reader_objects(pe, md, int(body, 16)) if body else []
        existing = rw_by_type.get(tid, {}).get("obj_seq") or []
        n = max(len(derived), len(existing))
        maps[tid] = [(derived[i] if i < len(derived) and derived[i] is not None else (existing[i] if i < len(existing) else None)) for i in range(n)]
    return maps


def reader_pairs(layouts, objects_by_type):
    exact, spans = set(), []
    for layout in layouts.get("layouts", []):
        seq = objects_by_type.get(layout["type_id"], [])
        for archive in layout.get("archives", {}).values():
            start = (archive.get("window") or [0, 0])[0]
            for field in archive.get("fields", []):
                idx = start + field["idx"]
                off = seq[idx] if idx < len(seq) else None
                if isinstance(off, int):
                    exact.add((off, field["width"]))
                    spans.append((off, field["width"]))
    return exact, spans


def apply_reader_corroboration(records, layouts, objects_by_type):
    exact, spans = reader_pairs(layouts, objects_by_type)
    for rec in records:
        off, size = rec["object_off"], rec["size"]
        if (off, size) in exact:
            rec["score"] = min(0.99, round(rec["score"] + 0.065, 3))
            rec["why"] += "; reader obj_seq 全局偏移/宽度命中"
        elif size == 4 and any(w == 8 and o <= off < o + w for o, w in spans):
            rec["score"] = min(0.98, round(rec["score"] + 0.04, 3))
            rec["why"] += "; reader obj_seq 8B 槽内子字段命中"
    return records


def reduce_table(records, limit=4):
    by_code = defaultdict(list)
    for rec in records:
        by_code[rec["code"]].append(rec)
    table = {}
    for code, values in by_code.items():
        unique = {}
        for rec in values:
            key = (rec["object_off"], rec["size"], rec["kind"])
            if key not in unique or rec["score"] > unique[key]["score"]:
                unique[key] = rec
        ranked = sorted(unique.values(), key=lambda r: (-r["score"], r["object_off"], r["file_off"]))[:limit]
        table[code] = [{k: v for k, v in rec.items() if not k.startswith("_") and k != "code"} for rec in ranked]
    return dict(sorted(table.items()))


def schema_codes(schema):
    by_name = {}
    for key, entity in schema.get("entities", {}).items():
        by_name[key] = {f["code"] for f in entity.get("fields", []) if f.get("code")}
        if entity.get("code"):
            by_name[entity["code"]] = by_name[key]
    return by_name


def schema_field_types(schema):
    result = defaultdict(set)
    for entity in schema.get("entities", {}).values():
        for field in entity.get("fields", []):
            if field.get("code") and field.get("type"):
                result[field["code"]].add(field["type"])
    return dict(result)


def plausible_schema_width(code, access_size, types_by_code):
    types = types_by_code.get(code, set())
    if not types:
        return True
    non_scalar = {"string", "text", "list", "array", "struct", "unique_id"}
    if all(t in non_scalar for t in types):
        return False
    if "real" in types or "float" in types:
        return access_size == 4
    if "database_record_unique_id" in types:
        return access_size == 4
    if "boolean" in types:
        return access_size == 1
    return access_size in (1, 2, 4)


def entity_codes(layout, schemas):
    return schemas.get(layout.get("entity"), set())


def assignment_components(slot):
    codes = slot.get("component_codes") or ([slot.get("code")] if slot.get("code") not in (None, "unresolved") else [])
    codes = [c for c in codes if c and c != "unresolved"]
    if not codes:
        return []
    validation = slot.get("validation") or {}
    offsets = validation.get("offsets") or []
    if len(offsets) != len(codes):
        offsets = [slot.get("row_off", 0) + (i * max(1, slot.get("width", 1) // len(codes))) for i in range(len(codes))]
    width = max(1, slot.get("width", 1) // len(codes))
    return [(code, int(rowoff), width) for code, rowoff in zip(codes, offsets)]


def city_ref_records(pe, md, hits, layouts, objects_by_type, table, assignments, schemas):
    """Import only explicit prior independent assignments, paired through the current reader map."""
    if not assignments:
        return []
    eligible = []
    for hit in hits:
        eligible.append(hit)
    # Locate the densest nearby cluster of distinct schema codes; this avoids embedding a city VA/file offset.
    codes_needed = set()
    for item in assignments.get("assignments", []):
        if item.get("entity") == "city" and item.get("type_id") == 2:
            codes_needed |= entity_codes({"entity": item.get("entity")}, schemas)
    ordered = sorted((h for h in eligible if h[1] in codes_needed), key=lambda h: h[0])
    best_cluster = []
    left = 0
    for right, hit in enumerate(ordered):
        while hit[0] - ordered[left][0] > 0x2000:
            left += 1
        cluster = ordered[left:right + 1]
        if len({h[1] for h in cluster}) > len({h[1] for h in best_cluster}):
            best_cluster = cluster
    by_code = defaultdict(list)
    for h in best_cluster:
        by_code[h[1]].append(h)
    additions = []
    layouts_by_type = {l["type_id"]: l for l in layouts.get("layouts", [])}
    for assignment in assignments.get("assignments", []):
        tid = assignment.get("type_id")
        layout = layouts_by_type.get(tid)
        if not layout or assignment.get("entity") != layout.get("entity"):
            continue
        allowed = entity_codes(layout, schemas)
        arch = assignment.get("archive")
        arc_layout = layout.get("archives", {}).get(arch)
        if not arc_layout:
            continue
        start = (arc_layout.get("window") or [0, 0])[0]
        for slot in assignment.get("slots", []):
            if slot.get("confidence") in (None, "unresolved"):
                continue
            for code, rowoff, width in assignment_components(slot):
                if code not in allowed:
                    continue
                idx = slot.get("idx")
                # Convert component offsets inside a packed reader slot into object offsets.
                base_idx = start + (idx if isinstance(idx, int) else slot.get("idx", 0))
                seq = objects_by_type.get(tid, [])
                base_obj = seq[base_idx] if base_idx < len(seq) else None
                if not isinstance(base_obj, int):
                    continue
                base_row = slot.get("row_off", rowoff)
                obj_off = base_obj + (rowoff - base_row)
                already = any(r.get("object_off") == obj_off and r.get("size") == width and r.get("kind") in ("read", "write") for r in table.get(code, []))
                if already:
                    continue
                variants = by_code.get(code, [])
                if not variants:
                    continue
                # Prefer an occurrence whose first getter/fall-through member reference is nearest this reader offset.
                choices = []
                for cmp_off, _c, cmp_va, _ins in variants:
                    branch = next((x for x in list(md.disasm(pe.raw[pe.va2f(cmp_va):pe.va2f(cmp_va) + 0x20], cmp_va))[1:4]
                                   if x.mnemonic in ("je", "jz", "jne", "jnz")), None)
                    if not branch:
                        continue
                    access_va, wrapper_off = None, None
                    if branch.mnemonic in ("je", "jz"):
                        try:
                            target = int(branch.op_str.strip(), 0)
                        except ValueError:
                            target = None
                        toff = pe.va2f(target) if target is not None else None
                        probe = list(md.disasm(pe.raw[toff:toff + 0x80], target)) if toff is not None else []
                    else:
                        start_va = branch.address + branch.size
                        so = pe.va2f(start_va)
                        probe = list(md.disasm(pe.raw[so:so + 0x80], start_va)) if so is not None else []
                    for ins in probe:
                        moff = any_member_operand(ins)
                        if moff is not None:
                            access_va, wrapper_off = ins.address, moff
                            break
                    delta = abs(wrapper_off - obj_off) if wrapper_off is not None else 0x1000
                    # The code remains explicit about a wrapper-offset discrepancy; it is not promoted to read evidence.
                    choices.append((delta, cmp_off, access_va, wrapper_off))
                if not choices:
                    continue
                delta, cmp_off, access_va, wrapper_off = min(choices)
                why = (f"reader obj_seq 连接 row+{slot.get('row_off')}，宽度 {width}；独立 assignments 的验证为 ref-only。"
                       f"分发分支首个对象成员指针在 +{wrapper_off:#x}。" if wrapper_off is not None else
                       f"reader obj_seq 连接 row+{slot.get('row_off')}，宽度 {width}；独立 assignments 的验证为 ref-only，未发现窄成员访问。")
                additions.append({"code": code, "file_off": hex(cmp_off), "object_off": obj_off, "size": width,
                                  "kind": "ref_only", "access_va": hex(access_va) if access_va is not None else hex(cmp_va),
                                  "score": 0.90, "why": why, "section": pe.section_of(cmp_off), "_route": "ref_only"})
    # Deduplicate identical slot assignments from client/server archives.
    unique = {}
    for rec in additions:
        key = (rec["code"], rec["object_off"], rec["size"])
        unique.setdefault(key, rec)
    return list(unique.values())


def table_with_ref_only(direct_table, ref_records, limit=4):
    out = {k: list(v) for k, v in direct_table.items()}
    by_code = defaultdict(list)
    for rec in ref_records:
        by_code[rec["code"]].append({k: v for k, v in rec.items() if not k.startswith("_") and k != "code"})
    for code, refs in by_code.items():
        direct = out.get(code, [])
        # Retain the supported reader-anchored ref candidate plus the best direct candidates up to the cap.
        direct = [x for x in direct if not (x["object_off"], x["size"]) in {(r["object_off"], r["size"]) for r in refs}]
        out[code] = (refs + direct[:max(0, limit - len(refs))])[:limit]
    return dict(sorted(out.items()))


def assignment_codes_for_slot(assignments, tid, arch, idx):
    result = []
    for item in (assignments or {}).get("assignments", []):
        if item.get("type_id") != tid or item.get("archive") != arch:
            continue
        for slot in item.get("slots", []):
            if slot.get("idx") == idx and slot.get("confidence") not in (None, "unresolved"):
                result.extend(c for c, _row, _w in assignment_components(slot))
    return result


def make_naming(layouts, objects_by_type, table, schemas, types_by_code, assignments):
    records = [{"code": code, **r} for code, values in table.items() for r in values]
    results = []
    for layout in layouts.get("layouts", []):
        tid, allowed = layout["type_id"], entity_codes(layout, schemas)
        seq, archives = objects_by_type.get(tid, []), {}
        for arch, spec in layout.get("archives", {}).items():
            start = (spec.get("window") or [0, 0])[0]
            fields = []
            for f in spec.get("fields", []):
                seq_idx = start + f["idx"]
                obj_off = seq[seq_idx] if seq_idx < len(seq) else None
                width = f["width"]
                # Ignore prior assignment labels absent from this entity's authoritative schema inventory;
                # the current executable/reader pair can supersede such stale hypotheses.
                anchored_codes = [c for c in assignment_codes_for_slot(assignments, tid, arch, f["idx"]) if c in allowed]
                matched = []
                for r in records:
                    if r["code"] not in allowed or r["score"] < 0.84:
                        continue
                    if not plausible_schema_width(r["code"], r["size"], types_by_code):
                        continue
                    exact = r["object_off"] == obj_off and r["size"] == width
                    packed_part = width == 8 and r["size"] == 4 and isinstance(obj_off, int) and obj_off <= r["object_off"] < obj_off + 8
                    ref_for_slot = r["code"] in anchored_codes and r["kind"] == "ref_only"
                    if exact or packed_part or ref_for_slot:
                        matched.append(r)
                # Existing independent assignments constrain the slot when they name a field.
                # Without such a constraint, ambiguous same-slot candidates remain unresolved.
                if anchored_codes:
                    matched = [r for r in matched if r["code"] in anchored_codes]
                matched.sort(key=lambda r: (r["code"] not in anchored_codes, r["kind"] == "ref_only", -r["score"], r["code"]))
                by_code = {}
                for r in matched:
                    by_code.setdefault(r["code"], r)
                choices = list(by_code.values())
                if not anchored_codes and len(choices) > 1:
                    # Multiple one-byte boolean tags can legitimately share a packed byte.
                    bit_tags = width == 1 and all("boolean" in types_by_code.get(r["code"], set()) for r in choices)
                    if not bit_tags:
                        choices.sort(key=lambda r: (-r["score"], r["code"]))
                        if len(choices) > 1 and choices[0]["score"] - choices[1]["score"] < 0.04:
                            choices = []
                        else:
                            choices = choices[:1]
                selected = choices
                codes = [r["code"] for r in selected]
                if codes:
                    confidence = "ref_only" if all(r["kind"] == "ref_only" for r in selected) else "readpair"
                else:
                    confidence = "unresolved"
                fields.append({"idx": f["idx"], "row_off": f["row_off"], "width": width, "object_off": obj_off,
                               "field": "+".join(codes) if codes else None, "codes": codes, "confidence": confidence,
                               "accesses": [{"code": r["code"], "object_off": r["object_off"], "size": r["size"],
                                             "kind": r["kind"], "file_off": r["file_off"], "access_va": r["access_va"],
                                             "score": r["score"], "why": r["why"]} for r in selected],
                               "why": [r["why"] for r in selected]})
            archives[arch] = {"business_width": spec["business_width"], "window": spec.get("window"), "fields": fields}
        results.append({"type_id": tid, "entity": layout.get("entity"), "reader_body": layout.get("reader_body"), "archives": archives})
    return {"note": "字段名由全局 4CC 窄访问候选和 reader obj_seq.object_off 连接；已有独立 assignment 仅用作显式证据/歧义约束。ref_only 不伪装成窄读。row_off/width 原样保留。",
            "entities": len(results), "results": results}


def selftest():
    assert code_from_imm(b"talC") == "Clat"
    assert code_from_imm(b"\x00abc") is None
    assert SIZE["dword"] == 4 and OFF_MIN == 0x20
    assert assignment_components({"code": "x", "row_off": 1, "width": 4, "validation": {"offsets": [1]}}) == [("x", 1, 4)]
    print("build.py selftest: OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build the global 4CC candidate table and reader-aligned naming result.")
    ap.add_argument("--outdir", default=str(OUT))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "4cc_table.json").write_text('{"status":"in_progress"}\n', encoding="utf-8")
    pe = load_pe()
    layouts = json.loads(LAYOUTS.read_text(encoding="utf-8"))
    rw = json.loads(READER_WIDTHS.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assignments = json.loads(ASSIGNMENTS.read_text(encoding="utf-8")) if ASSIGNMENTS.exists() else None
    schemas = schema_codes(schema)
    types_by_code = schema_field_types(schema)
    hits, md = decode_cmp_hits(pe)
    objects = build_reader_maps(pe, md, layouts, rw)
    recs = apply_reader_corroboration(find_candidates(pe, hits, md), layouts, objects)
    direct_table = reduce_table(recs)
    ref_records = city_ref_records(pe, md, hits, layouts, objects, direct_table, assignments, schemas)
    table = table_with_ref_only(direct_table, ref_records)
    has_ref_only = bool(ref_records)
    result = {"status": "complete_with_ref_only" if has_ref_only else "complete_with_unresolved",
              "note": "Verified global cmp imm32 4CC scan. read/write candidates require narrow direct accesses. ref_only records are separated and sourced from independent assignments plus reader obj_seq; they do not claim a narrow getter access.",
              "exe_sha256": hashlib.sha256(pe.raw).hexdigest(),
              "scan": {"validated_cmp_hits": len(hits), "distinct_4cc_cmp_codes": len({h[1] for h in hits}),
                       "codes_with_evidence": len(table), "direct_narrow_codes": len(direct_table),
                       "candidate_records": sum(map(len, table.values())), "ref_only_records": len(ref_records)},
              "codes": table}
    (outdir / "4cc_table.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    naming = make_naming(layouts, objects, table, schemas, types_by_code, assignments)
    naming["exe_sha256"] = result["exe_sha256"]
    (outdir / "naming_result.json").write_text(json.dumps(naming, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cmp 4CC: validated={len(hits)}, distinct={len({h[1] for h in hits})}; table codes={len(table)}; ref_only={len(ref_records)}")
    for code in ("Clat", "Clon", "Cnti", "Cwea", "Clgi", "Clri", "icla", "iscl", "Imnd", "Iexd", "Iiar", "Irec", "Iocr", "Imip", "Iagr", "Icms", "Icon", "inSr", "Icdp"):
        print(code, table.get(code, []))
    for r in naming["results"]:
        if r["type_id"] in (2, 6):
            print("named", r["type_id"], {a: [(f["row_off"], f["width"], f["object_off"], f["field"], f["confidence"]) for f in d["fields"]]
                                            for a, d in r["archives"].items()})
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(2)
