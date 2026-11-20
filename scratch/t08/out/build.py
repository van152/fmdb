from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
T07_TABLE = ROOT / "scratch/t07/out/4cc_table.json"
T07_NAMING = ROOT / "scratch/t07/out/naming_result.json"
LAYOUTS = ROOT / "scratch/t05/layouts.json"
READER_WIDTHS = ROOT / "scratch/t05/reader_widths.json"
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
GAP_LIMIT = 512
MIN_CODES = 5
NARROW_SIZES = {1: "byte", 2: "word", 4: "dword"}
OBJECT_REGS = {"rsi", "rdi", "rcx", "rbx", "rdx", "r8", "r9", "r12", "r13", "r14", "r15"}
RE_MEM = re.compile(r"\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]", re.I)
RE_IMM = re.compile(r"^([a-z0-9]+),\s*0x([0-9a-f]+)$", re.I)
CONDITIONALS = {"je", "jz", "jne", "jnz", "jg", "jge", "jl", "jle", "ja", "jae", "jb", "jbe", "js", "jns", "jo", "jno", "jp", "jnp"}
DIRECT_FIELD_BRANCHES = {"je", "jz", "jne", "jnz"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_pe():
    spec = importlib.util.spec_from_file_location("t08_pe", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.default()


def code_from_imm(value: int) -> str | None:
    try:
        text = value.to_bytes(4, "little")[::-1].decode("ascii")
    except (OverflowError, UnicodeDecodeError):
        return None
    return text if len(text) == 4 and text.isalnum() and text.isascii() else None


def decode_site(pe, md, file_off: int):
    va = pe.f2va(file_off)
    if va is None:
        return None
    ins = list(md.disasm(pe.raw[file_off:file_off + 24], va))
    if not ins or ins[0].mnemonic != "cmp":
        return None
    match = RE_IMM.match(ins[0].op_str.lower())
    if not match:
        return None
    code = code_from_imm(int(match.group(2), 16))
    if code is None:
        return None
    branch = ins[1] if len(ins) > 1 and ins[1].mnemonic in CONDITIONALS else None
    target_va = None
    if branch:
        try:
            target_va = int(branch.op_str.strip(), 0)
        except ValueError:
            pass
    return {"code": code, "cmp_va": va, "cmp_file_off": file_off,
            "branch": branch.mnemonic if branch else None,
            "branch_target_va": target_va,
            "branch_target_file_off": pe.va2f(target_va) if target_va is not None else None,
            "branch_insn": f"{branch.mnemonic} {branch.op_str}" if branch else None}


def access_of(ins):
    op = ins.op_str.lower()
    mem = RE_MEM.search(op)
    if not mem or mem.group(1) not in OBJECT_REGS:
        return None
    size = None
    kind = "read"
    if ins.mnemonic in ("mov", "movzx", "movsx", "movsxd", "movss", "movsd"):
        # The memory operand width is explicit in Capstone's operand text.
        size_match = re.search(r"\b(byte|word|dword|qword)\s+ptr\s*\[", op)
        if not size_match:
            return None
        size = {"byte": 1, "word": 2, "dword": 4, "qword": 8}[size_match.group(1)]
        if ins.mnemonic == "mov" and op.startswith(("byte ptr [", "word ptr [", "dword ptr [", "qword ptr [")):
            kind = "write"
    else:
        return None
    off = int(mem.group(2), 16) if mem.group(2) else 0
    if not (0x20 <= off <= 0x400) or size not in (1, 2, 4):
        return None
    return {"object_off": off, "width": size, "kind": kind,
            "access_va": ins.address, "instruction": f"{ins.mnemonic} {ins.op_str}"}


def branch_target(ins):
    if ins.mnemonic not in CONDITIONALS and ins.mnemonic != "jmp":
        return None
    try:
        return int(ins.op_str.strip(), 0)
    except ValueError:
        return None


def getter_accesses(pe, md, site, max_span=0x600):
    target = site["branch_target_va"]
    if site["branch"] not in ("je", "jz") or target is None:
        return []
    queue = [(target, 0)]
    seen = set()
    found = []
    while queue and len(seen) < 24:
        block, depth = queue.pop(0)
        if block in seen or abs(block - target) > max_span:
            continue
        seen.add(block)
        off = pe.va2f(block)
        if off is None:
            continue
        for ins in md.disasm(pe.raw[off:off + 0x100], block):
            acc = access_of(ins)
            if acc:
                acc.update({"depth": depth, "route": "je_target"})
                found.append(acc)
            if ins.mnemonic == "ret":
                break
            if ins.mnemonic == "jmp":
                dest = branch_target(ins)
                if dest is not None and abs(dest - target) <= max_span:
                    queue.append((dest, depth + 1))
                break
            dest = branch_target(ins)
            if dest is not None:
                if abs(dest - target) <= max_span:
                    queue.append((dest, depth + 1))
                queue.append((ins.address + ins.size, depth + 1))
                break
    seen_keys = set()
    unique = []
    for item in sorted(found, key=lambda x: (x["depth"], x["access_va"])):
        key = (item["object_off"], item["width"], item["kind"], item["access_va"])
        if key not in seen_keys:
            seen_keys.add(key)
            unique.append(item)
    return unique


def fallthrough_accesses(pe, md, site):
    if site["branch"] not in ("jne", "jnz"):
        return []
    start = site["cmp_va"]
    cmp_file = site["cmp_file_off"]
    cmp_ins = next(iter(md.disasm(pe.raw[cmp_file:cmp_file + 8], start)), None)
    if cmp_ins is None:
        return []
    begin_va = cmp_ins.address + cmp_ins.size
    branch_ins = next(iter(md.disasm(pe.raw[pe.va2f(begin_va):pe.va2f(begin_va) + 8], begin_va)), None)
    if branch_ins is None:
        return []
    begin_va = branch_ins.address + branch_ins.size
    off = pe.va2f(begin_va)
    if off is None:
        return []
    for ins in list(md.disasm(pe.raw[off:off + 0x180], begin_va))[:64]:
        if ins.mnemonic == "cmp":
            m = RE_IMM.match(ins.op_str.lower())
            if m and code_from_imm(int(m.group(2), 16)):
                break
        acc = access_of(ins)
        if acc:
            acc.update({"depth": 0, "route": "jne_fallthrough"})
            return [acc]
        if ins.mnemonic == "ret":
            break
    return []


def local_accesses(pe, md, site):
    if site["branch"] not in DIRECT_FIELD_BRANCHES:
        return []
    if site["branch"] in ("je", "jz"):
        return getter_accesses(pe, md, site)
    return fallthrough_accesses(pe, md, site)


def provisional_groups(points):
    result = []
    current = []
    for point in sorted(points):
        if current and point - current[-1] > GAP_LIMIT:
            result.append(current)
            current = []
        current.append(point)
    if current:
        result.append(current)
    return result


def local_cmp_sites(pe, md, start_off, end_off):
    start_va = pe.f2va(start_off)
    if start_va is None:
        return []
    raw_end = min(len(pe.raw), end_off + 16)
    sites = {}
    for ins in md.disasm(pe.raw[start_off:raw_end], start_va):
        if ins.mnemonic != "cmp":
            continue
        match = RE_IMM.match(ins.op_str.lower())
        if not match:
            continue
        code = code_from_imm(int(match.group(2), 16))
        if code is None:
            continue
        file_off = pe.va2f(ins.address)
        if file_off is None:
            continue
        site = decode_site(pe, md, file_off)
        if site:
            sites[file_off] = site
    return [sites[k] for k in sorted(sites)]


def connectivity(pe, sites):
    targets = [s for s in sites if s["branch_target_va"] is not None]
    if not targets:
        return {"status": "no_direct_targets", "target_count": 0, "same_section": False,
                "target_va_span": None, "shared_targets": []}
    target_offsets = [s["branch_target_file_off"] for s in targets]
    sections = {pe.section_of(x) for x in target_offsets if x is not None}
    target_vas = [s["branch_target_va"] for s in targets]
    span = max(target_vas) - min(target_vas)
    counts = Counter(s["branch_target_va"] for s in targets)
    shared = sorted(hex(v) for v, n in counts.items() if n >= 2)
    same_section = len(sections) == 1 and None not in target_offsets
    # Direct conditional edges establish reachability; bounded target span and a shared
    # local successor are the available function-coherence checks without symbols/CFG metadata.
    coherent = same_section and span <= 0x10000 and (len(shared) > 0 or len(targets) >= 5)
    return {"status": "passed" if coherent else "review", "target_count": len(targets),
            "same_section": same_section, "target_sections": sorted(sections),
            "target_va_span": hex(span), "shared_targets": shared,
            "basis": "direct conditional edges; target blocks in one PE section and bounded VA span; shared successor when present"}


def build_chains(table, pe, md):
    codes = table.get("codes", {})
    records_by_off = defaultdict(list)
    for code, records in codes.items():
        for record in records:
            try:
                fo = int(record["file_off"], 16)
            except (KeyError, ValueError, TypeError):
                continue
            records_by_off[fo].append({"table_code": code, **record})
    anchors = sorted(records_by_off)
    provisional = provisional_groups(anchors)
    chains = []
    discarded = []
    code_mismatches = []
    global_id = 0
    for group in provisional:
        sites = local_cmp_sites(pe, md, group[0], group[-1])
        site_by_off = {s["cmp_file_off"]: s for s in sites}
        # Keep every 4CC cmp decoded from the bounded provisional region; table records are
        # anchors, not a reason to trust a wrong neighboring branch association.
        accesses = []
        for site in sites:
            for acc in local_accesses(pe, md, site):
                accesses.append({"code": site["code"], "file_off": hex(site["cmp_file_off"]),
                                 "target_va": hex(site["branch_target_va"]) if site["branch_target_va"] else None,
                                 **acc})
        present = {s["cmp_file_off"]: s["code"] for s in sites}
        for fo in group:
            site = site_by_off.get(fo)
            for rec in records_by_off[fo]:
                if site and rec["table_code"] != site["code"]:
                    code_mismatches.append({"file_off": hex(fo), "table_code": rec["table_code"],
                                            "decoded_code": site["code"], "why": "candidate record code differs from cmp immediate"})
        all_codes = sorted(set(present.values()))
        # Candidate evidence is keyed by exact code/off/width, and only from a branch
        # immediately following that code's cmp. This removes t07's adjacent-boundary bleed.
        evidence_by_key = {}
        for acc in accesses:
            key = (acc["code"], acc["object_off"], acc["width"], acc["kind"], acc["file_off"], acc["access_va"])
            evidence_by_key[key] = acc
        evidence = list(evidence_by_key.values())
        conn = connectivity(pe, sites)
        if len(all_codes) < MIN_CODES:
            discarded.append({"file_off_range": [hex(group[0]), hex(group[-1])],
                              "n_anchor_points": len(group), "n_codes": len(all_codes),
                              "reason": "n_codes_below_5", "candidate_pairs": [
                                  {"code": x["code"], "object_off": x["object_off"], "width": x["width"]} for x in evidence]})
            continue
        global_id += 1
        # Check direct targets belong to an executable-mapped section and are tightly clustered.
        # Keep a review flag rather than silently deleting a chain when PE metadata is insufficient.
        chain = {"chain_id": f"chain_{global_id:04d}",
                 "file_off_range": [hex(group[0]), hex(group[-1])],
                 "codes": all_codes, "targets": [
                     {"code": s["code"], "cmp_file_off": hex(s["cmp_file_off"]),
                      "branch": s["branch"], "target_va": hex(s["branch_target_va"]) if s["branch_target_va"] else None,
                      "target_file_off": hex(s["branch_target_file_off"]) if s["branch_target_file_off"] is not None else None}
                     for s in sites if s["branch_target_va"] is not None],
                 "n_codes": len(all_codes), "n_anchor_points": len(group),
                 "candidate_pairs": [{"code": x["code"], "object_off": x["object_off"],
                                      "width": x["width"], "kind": x["kind"],
                                      "file_off": x["file_off"], "access_va": hex(x["access_va"]),
                                      "instruction": x["instruction"], "route": x["route"],
                                      "depth": x["depth"]} for x in evidence],
                 "connectivity": conn}
        chains.append(chain)
    return chains, discarded, code_mismatches, len(anchors), len(provisional)


def build_reader_sets(layouts, naming, reader_widths):
    named_by_type = {x["type_id"]: x for x in naming.get("results", [])}
    widths_by_type = {x["type_id"]: x for x in reader_widths.get("results", [])}
    result = []
    for layout in layouts.get("layouts", []):
        tid = layout["type_id"]
        named = named_by_type.get(tid, {})
        width_info = widths_by_type.get(tid, {})
        seq = width_info.get("obj_seq", [])
        archives = {}
        pair_to_slots = defaultdict(list)
        for archive, spec in layout.get("archives", {}).items():
            n_archive = named.get("archives", {}).get(archive, {})
            start = (spec.get("window") or [0, 0])[0]
            slots = []
            for field in spec.get("fields", []):
                nfield = next((f for f in n_archive.get("fields", []) if f.get("idx") == field.get("idx")), {})
                off = nfield.get("object_off")
                if not isinstance(off, int):
                    seq_idx = start + field["idx"]
                    off = seq[seq_idx] if seq_idx < len(seq) else None
                slot = {"idx": field["idx"], "row_off": field["row_off"], "width": field["width"],
                        "object_off": off}
                slots.append(slot)
                if isinstance(off, int):
                    pair_to_slots[(off, field["width"])].append({"archive": archive, **slot})
            archives[archive] = slots
        result.append({"type_id": tid, "entity": layout.get("entity"), "archives": archives,
                       "pairs": pair_to_slots})
    return result


def pair_chains(chains, readers):
    matrix = []
    for reader in readers:
        reader_pairs = set(reader["pairs"])
        candidates = []
        for chain in chains:
            chain_pairs = {(x["object_off"], x["width"]) for x in chain["candidate_pairs"]}
            chain_offsets = {x["object_off"] for x in chain["candidate_pairs"]}
            reader_offsets = {off for off, _width in reader_pairs}
            matched = sorted(reader_pairs & chain_pairs)
            offset_only = sorted(reader_offsets & chain_offsets)
            if not matched and not offset_only:
                continue
            per_pair = []
            for off, width in matched:
                code_records = [x for x in chain["candidate_pairs"] if x["object_off"] == off and x["width"] == width]
                per_pair.append({"object_off": off, "width": width,
                                 "slots": reader["pairs"][(off, width)],
                                 "codes": sorted({x["code"] for x in code_records}),
                                 "evidence": code_records})
            ratio = (len(matched) / len(offset_only)) if offset_only else 0.0
            candidates.append({"chain_id": chain["chain_id"], "score": len(matched),
                               "width_consistency": round(ratio, 4),
                               "offset_overlap_count": len(offset_only),
                               "matched": per_pair,
                               "offset_only_mismatches": [off for off in offset_only
                                                          if not any(x[0] == off for x in matched)]})
        candidates.sort(key=lambda x: (-x["score"], -x["width_consistency"],
                                       -sum(len(p["codes"]) for p in x["matched"]), x["chain_id"]))
        eligible = [x for x in candidates if x["score"] >= 3]
        primary = eligible[0]["chain_id"] if eligible else None
        if primary:
            reason = (f"最高 exact (object_off,width) 命中 {eligible[0]['score']}，"
                      f"width_consistency={eligible[0]['width_consistency']}; 按 score/宽度一致率裁决。"
                      f"候选链数={len(eligible)}；其余为落选链。")
        elif candidates:
            reason = f"最高 exact 命中 {candidates[0]['score']} (<3 门槛)，不建立主链。"
        else:
            reason = "所有保留链均无 reader object_off 重叠。"
        matrix.append({"type_id": reader["type_id"], "entity": reader["entity"],
                       "reader_archives": list(reader["archives"]),
                       "reader_slots": [slot for slots in reader["archives"].values() for slot in slots],
                       "top3": candidates[:3], "candidates": candidates,
                       "primary_chain": primary, "decision_reason": reason})
    return matrix


def schema_types_by_code(schema):
    result = defaultdict(set)
    for entity in schema.get("entities", {}).values():
        for field in entity.get("fields", []):
            if field.get("code") and field.get("type"):
                result[field["code"]].add(field["type"])
    return result


def allowed_codes(schema, entity_name):
    entity = schema.get("entities", {}).get(entity_name, {})
    return {f.get("code") for f in entity.get("fields", []) if f.get("code")}


def type_compatible(code, width, types_by_code):
    types = types_by_code.get(code, set())
    if not types:
        return True
    constraints = {"boolean": {1}, "real": {4}, "float": {4},
                   "database_record_unique_id": {4}, "cash": {4}, "day_of_week": {1},
                   "date": {2, 4}, "integer": {1, 2, 4}, "enum": {1, 2, 4},
                   "multiple_enum": {1, 2, 4}, "short_distance": {1, 2}}
    non_scalar = {"string", "text", "list", "array", "struct", "unique_id", "picture"}
    accepted = set()
    for t in types:
        accepted |= constraints.get(t, set())
    if not accepted and types & non_scalar:
        return False
    return not accepted or width in accepted


def make_naming(base, pairing, chains, schema):
    result = json.loads(json.dumps(base))
    chain_by_id = {c["chain_id"]: c for c in chains}
    pair_by_type = {x["type_id"]: x for x in pairing}
    types_by_code = schema_types_by_code(schema)
    stats = Counter()
    for entity in result.get("results", []):
        tid = entity["type_id"]
        match = pair_by_type.get(tid, {})
        chain_id = match.get("primary_chain")
        chain = chain_by_id.get(chain_id)
        if chain is None:
            continue
        # Code compatibility is applied only when the reader entity has a schema identity.
        entity_allowed = allowed_codes(schema, entity.get("entity"))
        by_pair = defaultdict(set)
        evidence_by_pair = defaultdict(list)
        for candidate in chain["candidate_pairs"]:
            pair = (candidate["object_off"], candidate["width"])
            by_pair[pair].add(candidate["code"])
            evidence_by_pair[pair].append(candidate)
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                if field.get("confidence") != "unresolved":
                    continue
                off = field.get("object_off")
                width = field.get("width")
                if not isinstance(off, int):
                    continue
                raw_candidates = set(by_pair.get((off, width), set()))
                if not raw_candidates:
                    continue
                compatible = {code for code in raw_candidates
                              if (not entity_allowed or code in entity_allowed)
                              and type_compatible(code, width, types_by_code)}
                # Keep raw collisions visible. Schema compatibility may rank a candidate,
                # but chain_unique is reserved for a structurally unique (off,width) pair.
                candidates = raw_candidates
                evidence = [x for x in evidence_by_pair[(off, width)] if x["code"] in candidates]
                codes = sorted(candidates)
                if len(codes) == 1:
                    code = codes[0]
                    field["field"] = code
                    field["codes"] = [code]
                    field["confidence"] = "chain_unique"
                    field["why"] = [f"{chain_id} 内唯一直接窄访问 {code} @+{off:#x}/{width}B；"
                                    f"reader (object_off,width) 精确命中。"]
                    field["accesses"] = [{"code": x["code"], "object_off": x["object_off"],
                                          "size": x["width"], "kind": x["kind"],
                                          "file_off": x["file_off"], "access_va": x["access_va"],
                                          "instruction": x["instruction"], "route": x["route"],
                                          "chain_id": chain_id} for x in evidence]
                    field["chain_id"] = chain_id
                    stats["chain_unique"] += 1
                else:
                    field["field"] = "|".join(codes)
                    field["codes"] = codes
                    field["confidence"] = "chain_ambiguous"
                    preference = (f" schema/type-compatible={sorted(compatible)}，" if compatible and compatible != candidates else "")
                    field["why"] = [f"{chain_id} 的精确槽位 +{off:#x}/{width}B 有多个结构候选；{preference}仍保留全部码，不强行裁决。"]
                    field["accesses"] = [{"code": x["code"], "object_off": x["object_off"],
                                          "size": x["width"], "kind": x["kind"],
                                          "file_off": x["file_off"], "access_va": x["access_va"],
                                          "instruction": x["instruction"], "route": x["route"],
                                          "chain_id": chain_id} for x in evidence]
                    field["chain_id"] = chain_id
                    stats["chain_ambiguous"] += 1
    summary = Counter()
    named = 0
    for entity in result.get("results", []):
        for archive in entity.get("archives", {}).values():
            for field in archive.get("fields", []):
                summary[field.get("confidence", "unresolved")] += 1
                if field.get("field") is not None:
                    named += 1
    result["status"] = "complete_chain_index"
    result["note"] = ("t07 命名逐槽原样保留；新增命名仅来自主 dispatch 链内的直接窄访问与 reader "
                      "(object_off,width) 精确匹配。row_off/width 沿用布局，不重写。")
    result["summary"] = {"slots": sum(summary.values()), "named_slots": named,
                          "confidence": dict(sorted(summary.items())),
                          "new_chain_unique": stats["chain_unique"],
                          "new_chain_ambiguous": stats["chain_ambiguous"]}
    return result


def selftest():
    assert code_from_imm(0x536f6c64) == "Sold"
    assert code_from_imm(0x00000000) is None
    assert len(provisional_groups([0x1000, 0x1100, 0x1301, 0x1502])) == 3
    assert provisional_groups([1, 514]) == [[1], [514]]
    assert type_compatible("x", 4, defaultdict(set))
    print("build.py selftest: OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build t08 dispatch-chain index, reader pairing matrix, and additive naming result.")
    ap.add_argument("--outdir", default=str(OUT), help="output directory (default: scratch/t08/out)")
    ap.add_argument("--selftest", action="store_true", help="run pure helper tests")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    outdir = Path(args.outdir)
    try:
        save_json(outdir / "chains.json", {"status": "in_progress", "chains": []})
        table = load_json(T07_TABLE)
        base = load_json(T07_NAMING)
        layouts = load_json(LAYOUTS)
        widths = load_json(READER_WIDTHS)
        schema = load_json(SCHEMA)
        pe = load_pe()
        from capstone import CS_ARCH_X86, CS_MODE_64, Cs
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        chains, discarded, mismatches, anchors, provisional_count = build_chains(table, pe, md)
        save_json(outdir / "chains.json", {
            "status": "complete_direct_target_reviewed",
            "source": "scratch/t07/out/4cc_table.json; bounded local disassembly around its candidate cmp sites only",
            "exe_sha256": table.get("exe_sha256"),
            "grouping": {"adjacent_file_off_gap_max": GAP_LIMIT, "minimum_codes": MIN_CODES,
                         "anchor_points": anchors, "provisional_clusters": provisional_count,
                         "retained_chains": len(chains), "discarded_clusters": len(discarded)},
            "code_mismatches": mismatches,
            "discarded_clusters": discarded,
            "chains": chains})
        save_json(outdir / "pairing.json", {"status": "in_progress", "readers": []})
        readers = build_reader_sets(layouts, base, widths)
        matrix = pair_chains(chains, readers)
        save_json(outdir / "pairing.json", {
            "status": "complete_one_primary_per_reader",
            "method": "exact intersection of chain candidate (object_off,width) pairs and reader slots; score >= 3",
            "reader_count": len(matrix), "chain_count": len(chains), "readers": matrix})
        save_json(outdir / "naming_result.json", {"status": "in_progress", "results": []})
        naming = make_naming(base, matrix, chains, schema)
        naming["exe_sha256"] = table.get("exe_sha256")
        save_json(outdir / "naming_result.json", naming)
        print(f"anchors={anchors} provisional={provisional_count} chains={len(chains)} readers={len(matrix)}")
        print(f"named={naming['summary']['named_slots']}/240; chain_unique={naming['summary']['new_chain_unique']}; "
              f"ambiguous={naming['summary']['new_chain_ambiguous']}")
        for item in matrix:
            p = item.get("primary_chain")
            top = item.get("top3", [])
            if p:
                lead = next(c for c in top if c["chain_id"] == p)
                print(f"type {item['type_id']:>2} {item['entity']}: {p} score={lead['score']}")
        return 0
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
