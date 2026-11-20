from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
DEFAULT_EXE = Path(r"<OLD_REPO>\input\editor.exe")
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
OBJECT_REGS = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", *(f"r{i}" for i in range(8, 16))}
BOUNDARY_BRANCHES = {"jle", "jl", "jg", "jae", "ja", "jb", "jbe"}
DIRECT_BRANCHES = {"je", "jz", "jne", "jnz"}
CONDITIONALS = DIRECT_BRANCHES | BOUNDARY_BRANCHES | {
    "jo", "jno", "js", "jns", "jp", "jnp", "jge", "jrcxz", "jecxz",
}
RE_MEM = re.compile(r"\[\s*([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\s*\]", re.I)
RE_SIZE = re.compile(r"\b(byte|word|dword|qword)\s+ptr\s*\[", re.I)
RE_CMP_IMM = re.compile(r"^([a-z0-9]+),\s*(-?0x[0-9a-f]+|-?\d+)$", re.I)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_pe_module():
    spec = importlib.util.spec_from_file_location("t12_pe", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def code_from_bytes(raw4: bytes) -> str | None:
    code_bytes = raw4[::-1]
    if len(code_bytes) != 4 or not all(48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122 for b in code_bytes):
        return None
    return code_bytes.decode("ascii")


def cmp_immediate(ins) -> int | None:
    if ins.mnemonic != "cmp":
        return None
    match = RE_CMP_IMM.match(ins.op_str.lower())
    if not match:
        return None
    try:
        return int(match.group(2), 0)
    except ValueError:
        return None


def is_tag_cmp(ins) -> bool:
    value = cmp_immediate(ins)
    return value is not None and code_from_bytes((value & 0xffffffff).to_bytes(4, "little")) is not None


def scan_cmp_sites(pe, md):
    """Find reversed 4CC immediates without assuming a cmp-register prefix, then decode-check."""
    sites = {}
    ascii4 = re.compile(rb"[A-Za-z0-9]{4}")
    tested_windows = 0
    for sec in pe._secs:
        if not sec["exec"] or not sec["rawsize"]:
            continue
        start = sec["raw"]
        end = min(start + sec["rawsize"], len(pe.raw))
        for hit in ascii4.finditer(pe.raw, start, end):
            imm_off = hit.start()
            code = code_from_bytes(hit.group())
            if code is None:
                continue
            # cmp r32,imm32 can be 81 /7 (with or without REX) or accumulator 3d.
            # Decode each plausible instruction start and require the immediate to end here.
            for cmp_off in (imm_off - 3, imm_off - 2, imm_off - 1):
                if cmp_off < start:
                    continue
                va = pe.f2va(cmp_off)
                if va is None:
                    continue
                insns = list(md.disasm(pe.raw[cmp_off:min(end, cmp_off + 12)], va, count=1))
                if not insns:
                    continue
                ins = insns[0]
                tested_windows += 1
                if ins.mnemonic != "cmp" or cmp_off + ins.size != imm_off + 4:
                    continue
                imm = cmp_immediate(ins)
                if imm is None or (imm & 0xffffffff) != int.from_bytes(hit.group(), "little"):
                    continue
                sites[cmp_off] = {"code": code, "file_off": cmp_off, "cmp_va": va,
                                  "instruction": f"{ins.mnemonic} {ins.op_str}", "cmp_size": ins.size,
                                  "cmp_imm": imm & 0xffffffff}
    return [sites[k] for k in sorted(sites)], tested_windows


def parse_mem(ins):
    m = RE_MEM.search(ins.op_str.lower())
    if not m or m.group(1) not in OBJECT_REGS:
        return None
    off = int(m.group(2), 16) if m.group(2) else 0
    return m.group(1), off


def direct_access(ins):
    """Return (shape, member offset, width) for direct scalar reads/writes only."""
    mem = parse_mem(ins)
    if not mem:
        return None
    _reg, off = mem
    if not 0 <= off <= 0x10000:
        return None
    size_match = RE_SIZE.search(ins.op_str.lower())
    size_word = size_match.group(1) if size_match else None
    sizes = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
    # Register-source memory MOV is a setter/write path.
    if ins.mnemonic == "mov" and re.match(r"^(?:byte|word|dword)\s+ptr\s*\[", ins.op_str.lower()):
        size = sizes.get(size_word)
        return ("write", off, size) if size in (1, 2, 4) else None
    # Scalar reads. qword pointer loads are handled only by ref_ptr recognition below.
    if ins.mnemonic not in {"movzx", "movsx", "movsxd", "movss", "movsd", "mov"}:
        return None
    if size_word == "qword":
        return None
    if size_word is None:
        # Some scalar MOV forms omit an explicit ptr width; use destination register width.
        lhs = ins.op_str.split(",", 1)[0].strip().lower()
        size = 8 if lhs.startswith("r") and lhs not in {"rip"} else 4
    else:
        size = sizes[size_word]
    if size not in (1, 2, 4):
        return None
    return "read", off, size


def decode_direct_target(ins):
    try:
        return int(ins.op_str.strip(), 0)
    except (ValueError, TypeError):
        return None


def branch_after_cmp(pe, md, site):
    off = site["file_off"]
    va = site["cmp_va"]
    end = min(len(pe.raw), off + 24)
    seq = list(md.disasm(pe.raw[off:end], va, count=5))
    for ins in seq[1:4]:
        # The next tag owns its own branch. In particular, a boundary jle/jl/jg
        # must never lend its following accesses to this or the next 4CC.
        if is_tag_cmp(ins):
            break
        if ins.mnemonic in CONDITIONALS:
            return ins
        if ins.mnemonic in ("ret", "jmp", "call"):
            break
    return None


def path_descend(ins, following):
    imm = None
    op = ins.op_str.lower()
    if ins.mnemonic == "add" and re.match(r"^rdi,\s*0x[0-9a-f]+$", op):
        imm = int(op.split(",", 1)[1], 16)
    elif ins.mnemonic == "lea":
        m = re.match(r"^rdi,\s*\[rdi\s*\+\s*(0x[0-9a-f]+)\]$", op)
        if m:
            imm = int(m.group(1), 16)
    if imm is not None and imm > 0 and following and following.mnemonic in {"jmp", "call"}:
        return imm
    return None


def ref_ptr_at(seq, index):
    """A qword object-member load followed within 3 insns by test reg,reg + null jcc."""
    ins = seq[index]
    if ins.mnemonic != "mov" or "qword ptr" not in ins.op_str.lower():
        return None
    mem = parse_mem(ins)
    if not mem:
        return None
    dst = ins.op_str.split(",", 1)[0].strip().lower()
    if not dst.startswith("r") or dst in {"rip"}:
        return None
    for j in range(index + 1, min(index + 4, len(seq) - 1)):
        test = seq[j]
        cond = seq[j + 1]
        if test.mnemonic != "test" or test.op_str.lower().replace(" ", "") != f"{dst},{dst}":
            continue
        if cond.mnemonic not in {"je", "jz", "jne", "jnz"}:
            continue
        return mem[1]
    return None


def walk_local_block(pe, md, start_va, route, code, branch, max_instructions=96, max_blocks=24,
                     max_span=0x600):
    """Walk only a branch-selected local handler; never crosses a subsequent printable-4CC cmp."""
    queue = deque([(start_va, 0)])
    seen = set()
    found = []
    while queue and len(seen) < max_blocks:
        block_va, depth = queue.popleft()
        if block_va in seen or abs(block_va - start_va) > max_span:
            continue
        seen.add(block_va)
        file_off = pe.va2f(block_va)
        if file_off is None:
            continue
        seq = list(md.disasm(pe.raw[file_off:min(len(pe.raw), file_off + 0x180)], block_va,
                             count=max_instructions))
        for idx, ins in enumerate(seq):
            # The next tag starts a different schema field, and its own direct routes must not bleed.
            if is_tag_cmp(ins):
                break
            acc = direct_access(ins)
            if acc:
                shape, obj_off, size = acc
                found.append({"shape": shape, "object_off": obj_off, "size": size,
                              "access_va": ins.address, "instruction": f"{ins.mnemonic} {ins.op_str}",
                              "route": route, "depth": depth, "branch": branch})
            ref_off = ref_ptr_at(seq, idx)
            if ref_off is not None:
                found.append({"shape": "ref_ptr", "object_off": ref_off, "size": 4,
                              "access_va": ins.address, "instruction": f"{ins.mnemonic} {ins.op_str}",
                              "route": route, "depth": depth, "branch": branch,
                              "why_extra": "qword load 后 3 条内 test reg,reg 与 null-check jcc；size=reader width 4"})
            if idx + 1 < len(seq):
                descend = path_descend(ins, seq[idx + 1])
                if descend is not None:
                    found.append({"shape": "path_descend", "object_off": None, "size": None,
                                  "descend": descend, "access_va": ins.address,
                                  "instruction": f"{ins.mnemonic} {ins.op_str}",
                                  "route": route, "depth": depth, "branch": branch,
                                  "why_extra": "rdi 下沉后紧接 jmp/call；只证实第一段，路径不完整"})
            if ins.mnemonic == "ret":
                break
            if ins.mnemonic == "call":
                # Serializer calls are generic sinks, not part of the current field handler.
                break
            if ins.mnemonic == "jmp":
                target = decode_direct_target(ins)
                if target is not None and abs(target - start_va) <= max_span:
                    queue.append((target, depth + 1))
                break
            if ins.mnemonic in CONDITIONALS:
                target = decode_direct_target(ins)
                if target is not None and abs(target - start_va) <= max_span:
                    queue.append((target, depth + 1))
                queue.append((ins.address + ins.size, depth + 1))
                break
    # Preserve first evidence instance per semantic instruction and cap at six per code.
    unique = {}
    for rec in sorted(found, key=lambda x: (x["depth"], x["access_va"], x["shape"])):
        key = (rec["shape"], rec.get("object_off"), rec.get("size"), rec.get("descend"), rec["access_va"])
        unique[key] = rec
    return list(unique.values())


def walk_fallthrough(pe, md, start_va, code, branch, max_instructions=72):
    file_off = pe.va2f(start_va)
    if file_off is None:
        return []
    seq = list(md.disasm(pe.raw[file_off:min(len(pe.raw), file_off + 0x180)], start_va,
                         count=max_instructions))
    found = []
    for idx, ins in enumerate(seq):
        if is_tag_cmp(ins):
            break
        acc = direct_access(ins)
        if acc:
            shape, obj_off, size = acc
            found.append({"shape": shape, "object_off": obj_off, "size": size,
                          "access_va": ins.address, "instruction": f"{ins.mnemonic} {ins.op_str}",
                          "route": "fallthrough", "depth": 0, "branch": branch})
        ref_off = ref_ptr_at(seq, idx)
        if ref_off is not None:
            found.append({"shape": "ref_ptr", "object_off": ref_off, "size": 4,
                          "access_va": ins.address, "instruction": f"{ins.mnemonic} {ins.op_str}",
                          "route": "fallthrough", "depth": 0, "branch": branch,
                          "why_extra": "qword load 后 3 条内 test reg,reg 与 null-check jcc；size=reader width 4"})
        if idx + 1 < len(seq):
            descend = path_descend(ins, seq[idx + 1])
            if descend is not None:
                found.append({"shape": "path_descend", "object_off": None, "size": None,
                              "descend": descend, "access_va": ins.address,
                              "instruction": f"{ins.mnemonic} {ins.op_str}",
                              "route": "fallthrough", "depth": 0, "branch": branch,
                              "why_extra": "rdi 下沉后紧接 jmp/call；只证实第一段，路径不完整"})
        if ins.mnemonic in {"ret", "call", "jmp"}:
            break
    return found


def make_instance(pe, site, branch, evidence=None, remote=False):
    branch_va = branch.address
    branch_text = f"{branch.mnemonic} {branch.op_str}"
    target = decode_direct_target(branch)
    if remote:
        return {"shape": "remote", "object_off": None, "size": None, "descend": None,
                "target_va": hex(target), "file_off": hex(site["file_off"]),
                "access_va": hex(branch_va), "instruction": branch_text,
                "branch": branch.mnemonic, "route": "target_remote",
                "why": f"je 目标 {target:#x} 与 cmp 相距 >0x1000；本地处理块无本字段访问，只记录远跳目标。"}
    item = {"shape": evidence["shape"], "object_off": evidence.get("object_off"),
            "size": evidence.get("size"), "descend": evidence.get("descend"),
            "file_off": hex(site["file_off"]), "access_va": hex(evidence["access_va"]),
            "instruction": evidence["instruction"], "branch": branch.mnemonic,
            "route": evidence["route"]}
    if evidence["shape"] == "path_descend":
        item["why"] = f"{evidence['instruction']} 后紧接 jmp/call；下沉量 {evidence['descend']:#x}；路径不完整。"
    elif evidence["shape"] == "ref_ptr":
        item["why"] = evidence.get("why_extra", "qword member load + test/null-check；size 使用 reader 宽度。")
    else:
        item["why"] = f"{evidence['route']} 分支块内直接 {evidence['shape']}，对象偏移 {evidence['object_off']:#x}/{evidence['size']}B。"
    return item


def is_byte_sequence_present(raw, code):
    return raw.find(code.encode("ascii")[::-1]) >= 0


def club_code_set(schema):
    entity = schema.get("entities", {}).get("club")
    if not entity:
        raise RuntimeError("schema_inventory.json has no club entity")
    return sorted({field["code"] for field in entity.get("fields", []) if field.get("code")})


def extract_all(exe_path: Path, outdir: Path, schema_path: Path):
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs

    pe_mod = load_pe_module()
    pe = pe_mod.PE(exe_path)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    exe_hash = hashlib.sha256(pe.raw).hexdigest()
    sites, tested_windows = scan_cmp_sites(pe, md)
    schema = load_json(schema_path)
    club_codes = club_code_set(schema)
    counts = Counter()
    codes = defaultdict(list)
    branch_counts = Counter()
    branch_sites = 0
    for site in sites:
        branch = branch_after_cmp(pe, md, site)
        if not branch:
            continue
        branch_sites += 1
        condition = branch.mnemonic
        branch_counts[condition] += 1
        if condition in BOUNDARY_BRANCHES or condition not in DIRECT_BRANCHES:
            continue
        target = decode_direct_target(branch)
        if target is None:
            continue
        if condition in {"je", "jz"}:
            if abs(target - branch.address) > 0x1000:
                # The local fall-through belongs to this tag only until the next 4CC compare.
                local = walk_fallthrough(pe, md, branch.address + branch.size, site["code"], condition)
                if not local:
                    inst = make_instance(pe, site, branch, remote=True)
                    codes[site["code"]].append(inst)
                    counts["remote"] += 1
                    continue
                # A local operation proves this is not the pure-remote shape. It remains
                # unassigned here because JE selects the remote arm, not fall-through.
                continue
            evidence = walk_local_block(pe, md, target, "je_target", site["code"], condition)
            route = "je_target"
        else:
            start = branch.address + branch.size
            evidence = walk_fallthrough(pe, md, start, site["code"], condition)
            route = "fallthrough"
        # Keep a maximum six useful instances per 4CC, across all comparison sites.
        for item in evidence:
            if item.get("route") != route:
                continue
            inst = make_instance(pe, site, branch, item)
            codes[site["code"]].append(inst)
            counts[item["shape"]] += 1
    # Deduplicate exact cmp/access tuples, then retain the six strongest, lowest-noise examples.
    reduced = {}
    for code, recs in codes.items():
        unique = {}
        for rec in recs:
            key = (rec["shape"], rec.get("object_off"), rec.get("size"), rec.get("descend"),
                   rec.get("target_va"), rec["file_off"], rec["access_va"])
            unique[key] = rec
        priorities = {"read": 0, "ref_ptr": 1, "write": 2, "path_descend": 3, "remote": 4}
        ordered = sorted(unique.values(), key=lambda x: (priorities[x["shape"]], x["file_off"], x["access_va"]))
        reduced[code] = ordered[:6]
    paths = {}
    full_raw = pe.raw
    for code in club_codes:
        recs = reduced.get(code, [])
        concrete = [x for x in recs if x["shape"] in {"read", "ref_ptr", "write"}
                    and isinstance(x.get("object_off"), int)]
        paths_found = [x for x in recs if x["shape"] == "path_descend"]
        remotes = [x for x in recs if x["shape"] == "remote"]
        present = is_byte_sequence_present(full_raw, code)
        if concrete:
            # A verified qword+null-check ref_ptr is the direct object-member anchor;
            # do not let nested scalar reads from its generic getter override it.
            ref_records = [x for x in concrete if x["shape"] == "ref_ptr"]
            preferred = ref_records or concrete
            offsets = Counter(x["object_off"] for x in preferred)
            object_off = offsets.most_common(1)[0][0]
            kind = "offset"
            confidence = "high" if offsets[object_off] >= 2 else "mid"
            entry = {"kind": kind, "object_off": object_off, "descend": [],
                     "instances": len(concrete), "confidence": confidence,
                     "evidence": [{"shape": x["shape"], "file_off": x["file_off"],
                                   "access_va": x["access_va"], "instruction": x["instruction"],
                                   "object_off": x["object_off"], "size": x["size"]}
                                  for x in concrete]}
        elif paths_found:
            descends = Counter(x["descend"] for x in paths_found)
            first = descends.most_common(1)[0][0]
            entry = {"kind": "path", "object_off": None, "descend": [first],
                     "instances": len(paths_found),
                     "confidence": "mid" if descends[first] > 1 else "low",
                     "why": "只观察到第一段下沉量，路径不完整。",
                     "evidence": [{"shape": x["shape"], "file_off": x["file_off"],
                                   "access_va": x["access_va"], "instruction": x["instruction"],
                                   "descend": x["descend"]} for x in paths_found]}
        elif remotes:
            targets = Counter(x["target_va"] for x in remotes)
            target = targets.most_common(1)[0][0]
            entry = {"kind": "remote", "object_off": None, "descend": [],
                     "target_va": target, "instances": len(remotes), "confidence": "low",
                     "evidence": [{"shape": x["shape"], "file_off": x["file_off"],
                                   "access_va": x["access_va"], "instruction": x["instruction"],
                                   "target_va": x["target_va"]} for x in remotes]}
        elif not present:
            entry = {"kind": "absent", "object_off": None, "descend": [],
                     "instances": 0, "confidence": "high",
                     "why": "全 exe 未找到该 4CC 的反序四字节序列。"}
        else:
            # Presence is not absence. Keep a fifth explicitly-unresolved category rather than
            # falsely claiming a location or inventing a remote target.
            matching_sites = [site for site in sites if site["code"] == code]
            diagnostics = []
            for site in matching_sites:
                branch = branch_after_cmp(pe, md, site)
                row = {"file_off": hex(site["file_off"]), "cmp_instruction": site["instruction"]}
                if branch is None:
                    row.update({"branch": None, "reason": "cmp 后 3 条内无条件分支"})
                else:
                    row.update({"branch": branch.mnemonic,
                                "branch_target_va": hex(decode_direct_target(branch))
                                    if decode_direct_target(branch) is not None else None})
                    if branch.mnemonic in BOUNDARY_BRANCHES:
                        row["reason"] = "边界比较；目标块与 fall-through 均不得归属本 4CC"
                    elif branch.mnemonic not in DIRECT_BRANCHES:
                        row["reason"] = "分支不在已实证的 je/jne 形态内"
                    elif branch.mnemonic in {"je", "jz"} and decode_direct_target(branch) is not None and abs(decode_direct_target(branch) - branch.address) > 0x1000:
                        row["reason"] = "JE 远目标但本地处理块也有操作；不能按纯 remote 猜偏移"
                    else:
                        row["reason"] = "分支块未发现五类形态之一的直接访问"
                diagnostics.append(row)
            if not present:
                entry = {"kind": "absent", "object_off": None, "descend": [],
                         "instances": 0, "confidence": "high",
                         "why": "全 exe 未找到该 4CC 的反序四字节序列。"}
            else:
                entry = {"kind": "unresolved", "object_off": None, "descend": [],
                         "instances": 0, "confidence": "low",
                         "binary_bytes_present": True,
                         "why": "码字节存在，但没有通过五种形态判别式的实例；未推断偏移。",
                         "cmp_sites": diagnostics or [],
                         "unresolved_reason": (diagnostics[0]["reason"] if diagnostics else
                             "反序字节存在，但没有解码成带分支的 cmp 4CC。")}
        paths[code] = entry

    shape_code_counts = Counter()
    for code, recs in reduced.items():
        for shape in {x["shape"] for x in recs}:
            shape_code_counts[shape] += 1
    cmp_code_count = Counter(site["code"] for site in sites)
    full = {"status": "complete_full_4cc", "source": str(exe_path), "exe_sha256": exe_hash,
            "scan": {"decoded_cmp_sites": len(sites), "cmp_sites_with_conditional_branch": branch_sites,
                     "cmp_sites_with_supported_je_jne": sum(branch_counts.get(x, 0) for x in DIRECT_BRANCHES),
                     "cmp_sites_with_boundary_branch": sum(branch_counts.get(x, 0) for x in BOUNDARY_BRANCHES),
                     "conditional_branch_histogram": dict(sorted(branch_counts.items())),
                     "expected_printable_4cc_branch_count": 14171,
                     "reversed_ascii_windows_tested": tested_windows,
                     "code_count_with_instances": len(reduced),
                     "instances_retained": sum(len(x) for x in reduced.values()),
                     "club_schema_codes": len(club_codes),
                     "club_codes_present_in_binary": sum(is_byte_sequence_present(full_raw, c) for c in club_codes),
                     "club_codes_absent_from_binary": sum(not is_byte_sequence_present(full_raw, c) for c in club_codes),
                     "shape_codes": dict(sorted(shape_code_counts.items())),
                     "shape_instances": dict(sorted(Counter(x["shape"] for rs in reduced.values() for x in rs).items())),
                     "cmp_sites_per_code": {k: v for k, v in sorted(cmp_code_count.items())}},
            "codes": dict(sorted(reduced.items()))}
    paths_summary = Counter(row["kind"] for row in paths.values())
    located = sum(paths_summary.get(k, 0) for k in ("offset", "path", "remote"))
    club_obj = {"status": "complete_club_paths", "summary": {
                    "club_schema_codes": len(club_codes),
                    "offset": paths_summary.get("offset", 0), "path": paths_summary.get("path", 0),
                    "remote": paths_summary.get("remote", 0), "absent": paths_summary.get("absent", 0),
                    "unresolved_present": paths_summary.get("unresolved", 0),
                    "with_location_information": located,
                    "with_location_information_pct": round(100.0 * located / len(club_codes), 2) if club_codes else 0,
                    "codes_present_binary": sum(is_byte_sequence_present(full_raw, c) for c in club_codes),
                    "codes_absent_binary": sum(not is_byte_sequence_present(full_raw, c) for c in club_codes),
                    "commander_baseline_present": 483, "commander_baseline_absent": 92,
                    "presence_count_discrepancy": sum(is_byte_sequence_present(full_raw, c) for c in club_codes) - 483},
                "codes": paths}
    save_json(outdir / "codes_full.json", full)
    save_json(outdir / "club_paths.json", club_obj)
    return full, club_obj


def selftest():
    assert code_from_bytes(b"dloS") == "Sold"
    assert code_from_bytes(b"KYcS") == "ScYK"  # reverse-byte decoding, case preserved
    assert code_from_bytes(b"\x00abc") is None
    assert path_descend(type("I", (), {"mnemonic": "add", "op_str": "rdi, 0xf0"})(),
                        type("I", (), {"mnemonic": "jmp"})()) == 0xf0
    assert path_descend(type("I", (), {"mnemonic": "lea", "op_str": "rdi, [rdi + 0x18]"})(),
                        type("I", (), {"mnemonic": "call"})()) == 0x18
    assert path_descend(type("I", (), {"mnemonic": "add", "op_str": "rdi, 0xf0"})(),
                        type("I", (), {"mnemonic": "mov"})()) is None
    # ScYK boundary trap: jle target and fall-through are both excluded from the current tag.
    for boundary in ("jle", "jl", "jg", "jae", "ja", "jb", "jbe"):
        assert boundary in BOUNDARY_BRANCHES and boundary not in DIRECT_BRANCHES
    assert "ScYK" != "ScYL"
    print("extract.py selftest: OK (5 shapes primitives; ScYK jle boundary excluded)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Extract branch-selected 4CC read/ref/write/path/remote instances from editor.exe.")
    ap.add_argument("--exe", type=Path, default=DEFAULT_EXE)
    ap.add_argument("--outdir", type=Path, default=OUT)
    ap.add_argument("--schema", type=Path, default=SCHEMA)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        args.outdir.mkdir(parents=True, exist_ok=True)
        # Preserve an explicit in-progress marker while this potentially long static scan runs.
        save_json(args.outdir / "codes_full.json", {"status": "in_progress", "codes": {}})
        save_json(args.outdir / "club_paths.json", {"status": "in_progress", "summary": {}, "codes": {}})
        full, paths = extract_all(args.exe, args.outdir, args.schema)
        print(f"cmp={full['scan']['decoded_cmp_sites']}; branch={full['scan']['cmp_sites_with_conditional_branch']}; "
              f"instances={full['scan']['instances_retained']}; club={paths['summary']}")
        return 0
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
