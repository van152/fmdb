#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t118 static people schema extraction and byte-level archive probe.

Reads existing Hex-Rays listings and tad/Zstandard inputs only. Outputs are
written incrementally to scratch/t118/out; no decompressed archive is persisted.
"""
from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import hashlib
import importlib.util
import json
import re
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t118" / "out"
T113 = ROOT / "scratch" / "t113" / "out"
T113_FUNCS = T113 / "funcs"
T95_FUNCS = ROOT / "scratch" / "t95" / "funcs"
VTABLE_JSON = T113 / "people_vtables_full.json"
PEOPLE_DAT = ROOT / "scratch" / "data" / "people_db.dat"
BASIC_DAT = ROOT / "scratch" / "data" / "basic_people_db.dat"
PEOPLE_SIZE = 400_443_970
BASIC_SIZE = 54_060_043
ROW_COUNT = 658_011
BASIC_WIDTH = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
CLASS_HINTS = {
    1: ("NON_PLAYER", "prompts/t115_basic_people_full.md:10"),
    2: ("PLAYER", "prompts/t115_basic_people_full.md:10"),
    3: ("ACTUAL_PLAYER_AND_NON_PLAYER", "prompts/t115_basic_people_full.md:10; vtable class alias"),
    4: ("OFFICIAL", "prompts/t115_basic_people_full.md:10"),
    5: (None, "unresolved; factory initializes vtable 0x14188a548"),
    6: ("JOURNALIST", "prompts/t115_basic_people_full.md:10"),
    7: ("VIRTUAL_PLAYER", "vtable match"),
    8: (None, "unresolved; factory initializes vtable 0x1418c6598"),
    9: (None, "unresolved; factory calls constructor 0x1410050f0"),
    16: (None, "unresolved; factory initializes vtable 0x14188ada8"),
    17: ("BASIC_PERSON", "vtable match"),
    18: (None, "unresolved; factory calls constructor 0x141434f00"),
    19: (None, "unresolved; factory initializes vtable 0x14188b5b8"),
}
TYPE_TO_VTABLE_CLASS = {
    2: "PLAYER",
    3: "ACTUAL_PLAYER_AND_NON_PLAYER",
    7: "VIRTUAL_PLAYER",
    17: "BASIC_PERSON",
}
SLOT_NAMES = {
    "slot02_get_prop": "get_prop",
    "slot03_set_prop": "set_prop",
    "slot05_reg_prop": "reg_prop",
    "slot19_read_server": "read_from_stream_server",
    "slot20_read_client": "read_from_stream_client",
    "slot21_write": "write_to_stream",
}


def load_t97():
    path = ROOT / "scripts" / "t97_extract_4cc_mem.py"
    spec = importlib.util.spec_from_file_location("t118_t97", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load proven parser: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


T97 = load_t97()


def jwrite(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def textwrite(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_va(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, int):
        return f"0x{value:x}"
    value = str(value)
    try:
        return f"0x{int(value, 16):x}"
    except ValueError:
        return value


def find_func_file(va: str | int) -> Path | None:
    stem = f"{int(str(va), 16) if isinstance(va, str) else va:x}.c"
    for directory in (T113_FUNCS, T95_FUNCS):
        candidate = directory / stem
        if candidate.exists():
            return candidate
    return None


def func_file_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def sha256_view(view: memoryview) -> str:
    h = hashlib.sha256()
    step = 1 << 20
    for pos in range(0, len(view), step):
        h.update(view[pos:pos + step])
    return h.hexdigest()


class _ZstdIn(ctypes.Structure):
    _fields_ = [("src", ctypes.c_void_p), ("size", ctypes.c_size_t), ("pos", ctypes.c_size_t)]


class _ZstdOut(ctypes.Structure):
    _fields_ = [("dst", ctypes.c_void_p), ("size", ctypes.c_size_t), ("pos", ctypes.c_size_t)]


def zstd_decompress_in_memory(path: Path, expected_size: int):
    """Stream one zstd frame into a fixed in-memory buffer; never write raw data."""
    archive = path.read_bytes()
    if len(archive) < 13 or archive[:6] != bytes.fromhex("03017461642e") or archive[8:12] != bytes.fromhex("28b52ffd"):
        raise ValueError(f"unexpected tad/zstd header: {path}")
    libname = ctypes.util.find_library("libzstd") or ctypes.util.find_library("zstd")
    if not libname:
        raise RuntimeError("libzstd was not found by ctypes.util.find_library")
    lib = ctypes.CDLL(libname)
    create = lib.ZSTD_createDStream
    create.restype = ctypes.c_void_p
    init = lib.ZSTD_initDStream
    init.argtypes = [ctypes.c_void_p]
    init.restype = ctypes.c_size_t
    decompress = lib.ZSTD_decompressStream
    decompress.argtypes = [ctypes.c_void_p, ctypes.POINTER(_ZstdOut), ctypes.POINTER(_ZstdIn)]
    decompress.restype = ctypes.c_size_t
    free = lib.ZSTD_freeDStream
    free.argtypes = [ctypes.c_void_p]
    free.restype = ctypes.c_size_t
    is_error = lib.ZSTD_isError
    is_error.argtypes = [ctypes.c_size_t]
    is_error.restype = ctypes.c_uint
    get_error = lib.ZSTD_getErrorName
    get_error.argtypes = [ctypes.c_size_t]
    get_error.restype = ctypes.c_char_p

    source = ctypes.create_string_buffer(archive, len(archive))
    target = ctypes.create_string_buffer(expected_size)
    stream = create()
    if not stream:
        raise RuntimeError("ZSTD_createDStream failed")
    try:
        status = init(stream)
        if is_error(status):
            raise RuntimeError(get_error(status).decode("ascii", "replace"))
        inp = _ZstdIn(ctypes.addressof(source) + 8, len(archive) - 8, 0)
        out_pos = 0
        last_in = -1
        while True:
            if out_pos >= expected_size:
                raise ValueError("zstd output exceeded the expected decompressed size")
            out = _ZstdOut(ctypes.addressof(target) + out_pos, expected_size - out_pos, 0)
            before = inp.pos
            status = decompress(stream, ctypes.byref(out), ctypes.byref(inp))
            if is_error(status):
                raise RuntimeError(get_error(status).decode("ascii", "replace"))
            out_pos += out.pos
            if status == 0:
                break
            if inp.pos == len(archive) - 8 and out.pos == 0:
                raise ValueError("truncated zstd frame")
            if inp.pos == before and out.pos == 0 and inp.pos == last_in:
                raise ValueError("zstd stream made no progress")
            last_in = inp.pos
        if out_pos != expected_size or inp.pos != len(archive) - 8:
            raise ValueError(f"zstd size/closure mismatch: output={out_pos}, input={inp.pos}")
        view = memoryview(target).cast("B")[:out_pos]
        return target, view, {"archive_bytes": len(archive), "archive_sha256": hashlib.sha256(archive).hexdigest(),
                              "decompressed_bytes": out_pos, "payload_sha256": sha256_view(view),
                              "decompressor": "libzstd ZSTD_decompressStream", "raw_dump_written": False}
    finally:
        free(stream)


def class_method_index(vt_json: dict) -> dict:
    classes = {}
    for cls in vt_json.get("vtables", []):
        c = {"class_name": cls["class"], "vtable_va": cls.get("vtable_va"),
             "slot_count": cls.get("slot_count"), "slots": cls.get("slots", []),
             "methods": {}}
        for slot_name, entry in (cls.get("core") or {}).items():
            if slot_name not in SLOT_NAMES:
                continue
            entry = entry or {}
            slot_va = entry.get("slot_va")
            func_va = entry.get("func_start") or slot_va
            path = find_func_file(func_va) if func_va else None
            c["methods"][SLOT_NAMES[slot_name]] = {
                "slot": slot_name, "slot_va": fmt_va(slot_va), "func_va": fmt_va(func_va),
                "thunk": entry.get("thunk"), "file": func_file_rel(path) if path else None,
                "decompiled": bool(path), "lines": entry.get("lines") or None,
            }
        classes[c["class_name"]] = c
    return classes


def extract_factory(vt_json: dict) -> dict:
    path = T113_FUNCS / "1410992c0.c"
    source = path.read_text(encoding="utf-8", errors="replace")
    lines = source.splitlines()
    labels = []
    for i, line in enumerate(lines):
        m = re.match(r"\s*case\s+(\d+)\s*:", line)
        if m:
            labels.append((int(m.group(1)), i))
    classes = class_method_index(vt_json)
    class_vas = {int(v["vtable_va"], 16): name for name, v in classes.items() if v.get("vtable_va")}
    dispatch = []
    for idx, (case, start) in enumerate(labels):
        stop = labels[idx + 1][1] if idx + 1 < len(labels) else len(lines)
        body = "\n".join(lines[start:stop])
        alloc = re.search(r"sub_1407E58C0\s*\([^;]*?,\s*(0x[0-9A-Fa-f]+|\d+)\s*\)", body)
        alloc_size = int(alloc.group(1), 16 if alloc.group(1).lower().startswith("0x") else 10) if alloc else None
        vtable_literals = []
        for m in re.finditer(r"(?:\*\s*\([^\n;]*?\)\s*\([^\n;]*?\)|\*\([^\n;]*?\))\s*=\s*(0x141[0-9A-Fa-f]+)LL", body):
            va = int(m.group(1), 16)
            if va not in vtable_literals:
                vtable_literals.append(va)
        if not vtable_literals:
            vtable_literals = [int(x, 16) for x in re.findall(r"=\s*(0x141[0-9A-Fa-f]+)LL", body)]
            vtable_literals = list(dict.fromkeys(vtable_literals))
        class_name, name_source = CLASS_HINTS.get(case, (None, "no class label in current evidence"))
        vtable_class = TYPE_TO_VTABLE_CLASS.get(case)
        if vtable_class:
            vtable = classes.get(vtable_class, {}).get("vtable_va")
        else:
            known = next((class_vas[x] for x in vtable_literals if x in class_vas), None)
            vtable = fmt_va(next((x for x in vtable_literals if x in class_vas), None)) if known else None
        if vtable is None and vtable_literals:
            vtable = fmt_va(vtable_literals[0])
        ctor = None
        for m in re.finditer(r"\bsub_([0-9A-Fa-f]{7,12})\s*\(\s*(v\d+)\s*,\s*1\s*\)", body):
            va = int(m.group(1), 16)
            if va not in (0x1407E58C0,):
                ctor = fmt_va(va)
                break
        return_match = re.search(r"return\s+([^;]+);", body)
        calls = list(dict.fromkeys(fmt_va(int(x, 16)) for x in re.findall(r"\bsub_([0-9A-Fa-f]{7,12})\s*\(", body)))
        cleanup = re.search(r"sub_141751048\s*\(\s*sub_([0-9A-Fa-f]+)\s*\)", body)
        method_class = TYPE_TO_VTABLE_CLASS.get(case)
        method_bundle = classes.get(method_class, {}).get("methods", {}) if method_class else {}
        methods = {}
        for name in ("get_prop", "set_prop", "read_from_stream_server", "read_from_stream_client", "write_to_stream"):
            methods[name] = method_bundle.get(name, {}).get("func_va")
        dispatch.append({
            "person_type": case, "class_name": class_name, "class_name_evidence": name_source,
            "allocation_size_bytes": alloc_size, "constructor_va": ctor,
            "constructor_kind": "direct_call" if ctor else ("inline_or_not_visible" if alloc_size else "not_allocator_case"),
            "pool_cleanup_callback_va": fmt_va(int(cleanup.group(1), 16)) if cleanup else None,
            "factory_vtable_literals": [fmt_va(x) for x in vtable_literals], "vtable_va": vtable,
            "vtable_evidence": "class vtable index" if method_class else ("literal initialized by factory" if vtable else "not resolved"),
            "return_expression": return_match.group(1).strip() if return_match else None,
            "method_vas": methods, "called_vas": calls,
            "source": f"{func_file_rel(path)}:{start + 1}",
        })
    missing = []
    priorities = {
        ("PERSON", "read_from_stream_server"): 0,
        ("PLAYER", "read_from_stream_server"): 0,
        ("PERSON", "write_to_stream"): 0,
        ("ACTUAL_PLAYER", "get_prop"): 1,
        ("ACTUAL_PLAYER", "set_prop"): 1,
        ("PLAYER", "write_to_stream"): 1,
    }
    for cls_name, cls in classes.items():
        for method_name, info in cls["methods"].items():
            if info.get("func_va") and not info.get("decompiled"):
                key = (cls_name, method_name)
                missing.append({"priority": priorities.get(key, 2), "class_name": cls_name,
                                "slot": info["slot"], "va": info["func_va"],
                                "reason": "vtable function has no matching t113/t95 decompiled C file"})
    missing.extend([
        {"priority": 0, "class_name": "PERSON", "slot": "slot19_read_server", "va": "0x141084540",
         "reason": "base PERSON reader absent; blocks semantic wire-field closure"},
        {"priority": 0, "class_name": "PLAYER", "slot": "slot19_read_server", "va": "0x140e3fb20",
         "reason": "PLAYER subclass reader absent; blocks player-body closure"},
        {"priority": 1, "class_name": "PERSON", "slot": "slot21_write", "va": "0x141084680",
         "reason": "PERSON writer absent; needed to cross-check serialization order"},
    ])
    unique = {}
    for rec in missing:
        unique[(rec["class_name"], rec["slot"], rec["va"])] = rec
    need = sorted(unique.values(), key=lambda r: (r["priority"], r["class_name"], r["va"]))
    cases = {x["person_type"] for x in dispatch}
    return {
        "schema_version": 1, "status": "partial_static", "factory_va": "0x1410992c0",
        "source": func_file_rel(path), "dispatch_cases_found": sorted(cases),
        "dispatch": dispatch,
        "not_dispatched_by_factory": sorted(set(range(1, 20)) - cases),
        "need_ida_vas": need,
        "need_ida_symbols_without_grounded_va": [
            {"priority": 1, "symbol": "PLAYER_DATA/NON_PLAYER_DATA slot19/slot21 serializers",
             "reason": "these class names are not represented in the supplied seven-vtable index; do not invent VAs"}
        ],
        "notes": [
            "Cases 1, 2, 3, 4, and 6 class labels come from the existing t115 brief, not from symbol names in this factory listing.",
            "Factory cases outside 1..6 are retained; many are not proven to be person archive types.",
            "A factory vtable literal is not treated as a named C++ class unless it matches the saved vtable index.",
        ],
    }


def property_roots(vt_json: dict) -> list[dict]:
    roots = []
    seen = set()
    for cls in vt_json.get("vtables", []):
        for slot_name in ("slot02_get_prop", "slot03_set_prop"):
            entry = (cls.get("core") or {}).get(slot_name) or {}
            va = entry.get("func_start") or entry.get("slot_va")
            if not va:
                continue
            path = find_func_file(va)
            if not path:
                continue
            key = (cls["class"], slot_name, str(path))
            if key in seen:
                continue
            seen.add(key)
            roots.append({"class_name": cls["class"], "slot": "get_prop" if slot_name == "slot02_get_prop" else "set_prop",
                          "va": fmt_va(va), "path": path})
    return roots


def extract_4cc(vt_json: dict) -> dict:
    mappings = []
    method_stats = []
    all_codes = set()
    grouped_codes = defaultdict(set)
    for root in property_roots(vt_json):
        func = T97.CFunc(root["path"], int(root["va"], 16))
        branches = func.find_branches()
        method_codes = set()
        for branch in branches:
            info = T97.analyze_branch(func, branch)
            code = branch.get("fourcc")
            if not code:
                continue
            code_int = branch.get("code_int")
            helpers = info.get("helper_calls") or []
            off = info.get("primary_off")
            access = info.get("access_kind")
            direct_helper = "direct" if off is not None and access in ("direct_field", "bitfield", "subobj_deref") else ("helper" if helpers else "computed_or_delegated")
            offsets = []
            for item in info.get("mem_offsets", []):
                offsets.append({"mem_off": item.get("off"), "width": item.get("width"),
                                "type": item.get("c_type"), "access": item.get("how"),
                                "source_line": item.get("line"), "bitop": item.get("bitop")})
            mappings.append({
                "class_name": root["class_name"], "slot": root["slot"], "fourcc": code,
                "hex_id": f"0x{(code_int if code_int is not None else T97.code_to_int(code)):08x}",
                "mem_off": off, "width": info.get("width"), "type": info.get("c_type"),
                "direct_or_helper": direct_helper, "helper_va": helpers[0] if helpers else None,
                "helper_vas": helpers, "access_kind": access,
                "file": func_file_rel(root["path"]), "line": branch.get("line_no"),
                "source": f"{func_file_rel(root['path'])}:{branch.get('line_no')}",
                "mem_offset_evidence": offsets, "bitmask_or_shift": info.get("bitmask_or_shift"),
                "delegate_va": info.get("delegate_va"), "branch_kind": branch.get("kind"),
            })
            all_codes.add(code)
            grouped_codes[root["class_name"]].add(code)
            method_codes.add(code)
        method_stats.append({"class_name": root["class_name"], "slot": root["slot"], "func_va": root["va"],
                             "file": func_file_rel(root["path"]), "dispatch_branches": len(branches),
                             "fourcc_branches": sum(1 for b in branches if b.get("fourcc")),
                             "unique_fourccs": len(method_codes)})
    # Stable deduplication keeps getter and setter evidence as separate records.
    mappings.sort(key=lambda r: (r["class_name"], r["slot"], r["fourcc"], r["line"] or 0))
    counts = Counter(r["class_name"] for r in mappings)
    return {
        "schema_version": 1, "status": "partial_static", "mapping_count": len(mappings),
        "unique_fourcc_count_global": len(all_codes),
        "unique_fourcc_by_class": {k: len(v) for k, v in sorted(grouped_codes.items())},
        "mapping_rows_by_class": dict(sorted(counts.items())), "method_stats": method_stats,
        "mappings": mappings,
        "parser_note": "Uses scripts/t97_extract_4cc_mem.py CFunc/analyze_branch offset analysis; byte offsets follow pointer-cast element size and are not guessed from register width.",
        "coverage_note": "Only property methods reachable from the saved seven-vtable index and present in scratch/t113/out/funcs or scratch/t95/funcs are included.",
    }


def _conditional_context(func, line_index: int) -> list[str]:
    out = []
    for idx, raw in enumerate(func.clean):
        if idx >= line_index:
            break
        stripped = raw.strip()
        if not (stripped.startswith("if (") or stripped.startswith("else if (")):
            continue
        block = func._block_after(idx)
        if block and block[0] <= line_index <= block[1]:
            out.append(stripped)
    return out[-6:]


def parse_wire_method(cls_name: str, method_name: str, va: str, file_path: Path, fourcc_by_off: dict) -> dict:
    func = T97.CFunc(file_path, int(va, 16))
    is_read = "read_from_stream" in method_name
    steps = []
    for idx, raw in enumerate(func.clean):
        line_no = idx + 1
        if idx <= (func.sig_line or 0):
            continue
        if not raw.strip():
            continue
        lowered = raw.lower()
        if is_read:
            # Slot-19 stream reads use the stream vtable's read-byte method (+40).
            if "+ 40" not in raw and "+ 0x28" not in raw.lower() and not re.search(r"\bsub_[0-9a-f]+\s*\(\s*a2\s*,", raw, re.I):
                continue
        else:
            # Keep actual writer calls and calls that pass the persistent object to a helper.
            if not any(token in raw for token in ("sub_", "(*", "a1 +", "a1[")):
                continue
        offsets = []
        for base, elem in func.base_vars_at(idx).items():
            if base in raw:
                offsets.extend(T97.extract_offsets(raw, base, elem, line_no))
        # In serializer code, only the current object's address arguments are relevant.
        unique_offsets = []
        seen = set()
        for off in offsets:
            key = (off["off_int"], off["width"], off["how"])
            if key not in seen:
                seen.add(key)
                unique_offsets.append(off)
        helper_vas = [fmt_va(x) for x in T97.extract_callees(raw)]
        if not unique_offsets and not helper_vas:
            continue
        literal_widths = [x["width"] for x in unique_offsets if x.get("width")]
        for off in unique_offsets:
            linked = fourcc_by_off.get((cls_name, off["off"]), [])
            steps.append({
                "step_idx": len(steps), "stream_op": "read" if is_read else "write_or_helper",
                "width": off.get("width"), "width_expression": None if off.get("width") else "not statically literal",
                "mem_off": off.get("off"), "mem_off_int": off.get("off_int"),
                "version_gate": _conditional_context(func, idx), "callee_va": helper_vas[0] if helper_vas else None,
                "helper_vas": helper_vas, "linked_4ccs": linked,
                "source_line": line_no, "source": f"{func_file_rel(file_path)}:{line_no}",
                "source_expression": raw.strip(), "offset_access": off.get("how"),
                "ctype": off.get("c_type"), "branch_execution_order": "source-order; conditions may skip steps",
            })
        if not unique_offsets:
            steps.append({
                "step_idx": len(steps), "stream_op": "helper_call", "width": None, "mem_off": None,
                "version_gate": _conditional_context(func, idx), "callee_va": helper_vas[0] if helper_vas else None,
                "helper_vas": helper_vas, "linked_4ccs": [], "source_line": line_no,
                "source": f"{func_file_rel(file_path)}:{line_no}", "source_expression": raw.strip(),
                "branch_execution_order": "source-order; conditions may skip steps",
            })
    return {"class_name": cls_name, "method": method_name, "func_va": va,
            "file": func_file_rel(file_path), "decompiled": True,
            "step_count": len(steps), "steps": steps}


def parse_basic_payload(view: memoryview) -> dict:
    if len(view) != BASIC_SIZE or struct.unpack_from("<I", view, 0)[0] != ROW_COUNT:
        raise ValueError("basic_people_db header/size mismatch")
    pos = 5
    hist = Counter()
    for row in range(ROW_COUNT):
        if pos + 2 > len(view) - 9 or view[pos] != 0x11:
            raise ValueError(f"basic_people marker mismatch at row={row}, offset={pos}")
        kind = view[pos + 1]
        width = BASIC_WIDTH.get(kind)
        if width is None or pos + width > len(view) - 9:
            raise ValueError(f"unknown/truncated basic_people type={kind} at row={row}")
        hist[kind] += 1
        pos += width
    if pos != len(view) - 9:
        raise ValueError(f"basic_people closure mismatch: {pos} != {len(view) - 9}")
    return {"row_count": ROW_COUNT, "row_chain_end": pos, "footer_offset": pos,
            "footer_hex": bytes(view[pos:]).hex(), "histogram": dict(sorted(hist.items())),
            "closure_diff": pos - (len(view) - 9)}


def probe_people_payload(view: memoryview, basic_hist: dict) -> dict:
    if len(view) != PEOPLE_SIZE or bytes(view[:2]) != b"\0\0":
        raise ValueError("people_db header or decompressed size mismatch")
    declared = struct.unpack_from("<I", view, 2)[0]
    if declared != ROW_COUNT:
        raise ValueError(f"people_db count mismatch: {declared}")
    pos = 6
    type5_rows = []
    for index in range(declared):
        if pos + 5 > len(view):
            raise ValueError(f"people_db truncated before record {index}")
        ordinal = struct.unpack_from("<I", view, pos)[0]
        kind = view[pos + 4]
        if kind != 5:
            transition = {"record_index": index, "record_offset": pos, "ordinal_u32": ordinal,
                          "person_type": kind, "body_offset": pos + 5,
                          "body_prefix_hex": bytes(view[pos + 5:pos + 5 + 48]).hex()}
            break
        body = pos + 5
        zero_word, name_len = struct.unpack_from("<II", view, body)
        if name_len > 4096:
            raise ValueError(f"implausible type-5 name length {name_len} at record {index}")
        name_start = body + 8
        name_end = name_start + name_len
        tail = name_end
        end = tail + 20
        if end > len(view):
            raise ValueError(f"truncated type-5 record {index}")
        name = bytes(view[name_start:name_end]).decode("utf-8", "replace")
        tail8 = bytes(view[tail:tail + 8])
        repeated_id, opaque_a, opaque_b = struct.unpack_from("<III", view, tail + 8)
        if zero_word != 0 or tail8 != bytes(8) or repeated_id != ordinal or opaque_a != opaque_b:
            raise ValueError(f"type-5 wire invariant mismatch at record {index}, offset={pos}")
        if index < 20:
            type5_rows.append({
                "record_index": index, "record_offset": pos, "record_end_offset_exclusive": end,
                "record_byte_length": end - pos, "ordinal_u32": ordinal, "person_type": kind,
                "person_type_offset": pos + 4, "body_offset": body,
                "body_fields": [
                    {"name": "opaque_u32_0", "offset": body, "width": 4, "value": zero_word, "semantic_status": "unknown"},
                    {"name": "utf8_name_length", "offset": body + 4, "width": 4, "value": name_len, "semantic_status": "byte-verified"},
                    {"name": "full_name_utf8", "offset": name_start, "width": name_len, "value": name, "semantic_status": "byte-verified"},
                    {"name": "opaque_zero_8", "offset": tail, "width": 8, "value_hex": tail8.hex(), "semantic_status": "byte-verified; meaning unknown"},
                    {"name": "repeated_ordinal_u32", "offset": tail + 8, "width": 4, "value": repeated_id, "semantic_status": "value equals record ordinal"},
                    {"name": "opaque_u32_a", "offset": tail + 12, "width": 4, "value": opaque_a, "semantic_status": "unknown"},
                    {"name": "opaque_u32_b", "offset": tail + 16, "width": 4, "value": opaque_b, "semantic_status": "equals preceding opaque_u32_a"},
                ],
                "name": name, "subclass_body_begin": body,
                "raw_record_hex": bytes(view[pos:end]).hex(),
            })
        pos = end
    else:
        transition = None
    if len(type5_rows) != 20:
        raise ValueError("the first 20 people_db records were not parsed as type 5")
    if index != basic_hist.get(5):
        raise ValueError(f"type-5 run does not meet basic class-5 count: {index} != {basic_hist.get(5)}")
    if transition is None or transition["record_index"] != basic_hist.get(5) or transition["person_type"] != 2:
        raise ValueError(f"unexpected first non-type-5 transition: {transition}")
    if type5_rows[0]["name"] != "Zarko Serafimovski":
        raise ValueError("row zero name anchor mismatch")
    return {
        "status": "partial_static_and_byte_verified_type5_prefix",
        "archive": {"decompressed_bytes": len(view), "header_zero_prefix_hex": bytes(view[:2]).hex(),
                    "declared_record_count_u32": declared, "first_record_offset": 6,
                    "payload_sha256": sha256_view(view)},
        "record_header": {"ordinal_u32_offset": 0, "ordinal_u32_width": 4,
                          "person_type_offset": 4, "person_type_width": 1,
                          "body_starts_at_record_plus": 5,
                          "evidence": "repeatedly verified on 1,193 consecutive type-5 records"},
        "type5_prefix": {"rows_closed": index, "next_record_offset": transition["record_offset"],
                         "histogram": {"5": index}, "basic_people_class5_count": basic_hist.get("5"),
                         "all_type5_rows_match": True, "first_20_rows": type5_rows},
        "first_non_type5_record": {**transition, "class_name_hint": "PLAYER" if transition["person_type"] == 2 else None,
                                   "class_name_hint_source": "t115 brief/factory case 2; not independently named by row bytes",
                                   "body_begin_verified": True},
        "semantic_header_fields": {
            "uid": "not identified by this type-5 parser; ordinal is retained without renaming",
            "first_name_id": "not located / not proven",
            "second_name_id": "not located / not proven",
            "common_name_id": "not located / not proven",
            "dob": "not located / not proven",
            "nation": "not located / not proven",
        },
        "known_star_uid_byte_hits": scan_star_uid_hits(view),
        "type1_to_type6_samples": {"5": "first 20 records parsed; type 5 prefix closes to count 1,193",
                                   "1": "not reached with a closed record parser",
                                   "2": f"record header at offset {transition['record_offset']}; body begins at {transition['body_offset']}; body end unknown",
                                   "3": "not reached with a closed record parser", "4": "not reached with a closed record parser",
                                   "6": "not reached with a closed record parser"},
        "limitations": ["Only the type-5 body grammar is currently closed from bytes.",
                        "No 400 MB decompressed file was written to disk.",
                        "The full PERSON and PLAYER readers are missing from the supplied C corpus, so names/UID/DOB/nation fields and later row boundaries are not claimed."],
    }


def scan_star_uid_hits(view: memoryview) -> list[dict]:
    anchors = [(28049320, "Harry Kane"), (735216, "Cristiano Ronaldo"), (7458500, "Lionel Messi")]
    hits = []
    for uid, label in anchors:
        needle = struct.pack("<I", uid)
        found = []
        start = 0
        chunk_size = 1 << 20
        overlap = len(needle) - 1
        while len(found) < 8 and start < len(view):
            stop = min(len(view), start + chunk_size)
            chunk = bytes(view[start:stop + (overlap if stop < len(view) else 0)])
            at = 0
            while len(found) < 8:
                rel = chunk.find(needle, at)
                if rel < 0:
                    break
                absolute = start + rel
                if absolute >= start and absolute + len(needle) <= stop:
                    found.append({"payload_offset": absolute, "following_byte": int(view[absolute + 4]) if absolute + 4 < len(view) else None,
                                  "context_hex": bytes(view[max(0, absolute - 8):absolute + 12]).hex()})
                at = rel + 1
            start = stop
        hits.append({"uid": uid, "label": label, "raw_byte_occurrences_sample": found,
                     "record_membership_verified": False})
    return hits


def build_wire(vt_json: dict, fourcc_map: dict, basic_info: dict, people_info: dict) -> dict:
    by_off = defaultdict(list)
    for rec in fourcc_map["mappings"]:
        if rec.get("mem_off"):
            by_off[(rec["class_name"], rec["mem_off"])].append(rec["fourcc"])
    by_off = {key: sorted(set(values)) for key, values in by_off.items()}
    methods = []
    for cls in vt_json.get("vtables", []):
        cls_name = cls["class"]
        core = cls.get("core") or {}
        for slot_name in ("slot19_read_server", "slot20_read_client", "slot21_write"):
            entry = core.get(slot_name) or {}
            slot_va = entry.get("slot_va")
            func_va = entry.get("func_start") or slot_va
            method_name = SLOT_NAMES[slot_name]
            path = find_func_file(func_va) if func_va else None
            if not func_va:
                methods.append({"class_name": cls_name, "method": method_name, "slot_va": None,
                                "func_va": None, "decompiled": False, "status": "no function VA in vtable snapshot",
                                "steps": []})
            elif not path:
                methods.append({"class_name": cls_name, "method": method_name, "slot_va": fmt_va(slot_va),
                                "func_va": fmt_va(func_va), "decompiled": False,
                                "status": "missing decompilation", "steps": []})
            else:
                parsed = parse_wire_method(cls_name, method_name, fmt_va(func_va), path, by_off)
                parsed.update({"slot_va": fmt_va(slot_va), "thunk": entry.get("thunk"),
                               "status": "static steps extracted" if parsed["steps"] else "decompiled body has no recognized direct stream steps"})
                methods.append(parsed)
    return {
        "schema_version": 1, "status": "partial", "serialization_methods": methods,
        "people_db_probe": people_info, "basic_people_db_validation": basic_info,
        "wire_step_count": sum(len(m.get("steps", [])) for m in methods),
        "wire_step_note": "Steps are source-order observations; conditional branches are retained as version_gate/condition context and are not linearized as one unconditional execution path.",
        "semantic_status": "Static-only for present methods. Byte-verified type-5 frame is a separate raw-data result; PERSON and PLAYER wire headers remain open.",
    }


def static_selftest() -> None:
    assert T97.int4cc(0x41424344) == "ABCD"
    # Pointer-to-DWORD arithmetic is scaled by four, while byte casts remain bytes.
    dword = T97.extract_offsets("x = *((_DWORD *)a1 + 3);", "a1", 1, 1)
    byte = T97.extract_offsets("x = *((_BYTE *)a1 + 7);", "a1", 1, 1)
    assert dword and dword[0]["off_int"] == 12, dword
    assert byte and byte[0]["off_int"] == 7, byte
    assert 0x140E3FB20 == int("140e3fb20", 16)


def binary_selftest() -> dict:
    _, basic, _ = zstd_decompress_in_memory(BASIC_DAT, BASIC_SIZE)
    basic_info = parse_basic_payload(basic)
    assert basic_info["closure_diff"] == 0
    assert basic_info["histogram"] == {1: 166064, 2: 476158, 3: 4757, 4: 9839, 5: 1193}
    _, people, _ = zstd_decompress_in_memory(PEOPLE_DAT, PEOPLE_SIZE)
    probe = probe_people_payload(people, basic_info["histogram"])
    assert probe["type5_prefix"]["rows_closed"] == 1193
    assert probe["type5_prefix"]["first_20_rows"][0]["name"] == "Zarko Serafimovski"
    return {"basic_histogram": basic_info["histogram"], "people_type5_rows": 1193,
            "people_first_non_type5": probe["first_non_type5_record"]["person_type"]}


def render_report(factory: dict, fourcc: dict, wire: dict, basic_meta: dict, people_meta: dict) -> str:
    dispatch_rows = "\n".join(
        f"| {r['person_type']} | {r['class_name'] or 'unresolved'} | {r['allocation_size_bytes'] if r['allocation_size_bytes'] is not None else '?'} | {r['constructor_va'] or 'inline/unknown'} | {r['vtable_va'] or 'unresolved'} |"
        for r in factory["dispatch"]
    )
    hist = ", ".join(f"{k}={v:,}" for k, v in wire["basic_people_db_validation"]["histogram"].items())
    missing = "\n".join(f"- P{m['priority']}: `{m['class_name']}::{m['slot']}` at `{m['va']}`: {m['reason']}" for m in factory["need_ida_vas"])
    return f"""# t118 People Schema Extraction

**Status: partial, evidence-bounded.** The supplied t113 directory contains {len(list(T113_FUNCS.glob('*.c')))} C listings (not the 428-function corpus described in the task brief). Available code, the seven-vtable index, and the real archive were analyzed; missing functions are not inferred as decompiled.

## Factory

`sub_1410992c0` has {len(factory['dispatch'])} explicit cases: `{', '.join(map(str, factory['dispatch_cases_found']))}`. All cases are emitted in `people_factory_map.json`; class labels without a vtable identity are explicitly marked as hints.

| Type | Class label | Allocation bytes | Constructor VA | Vtable VA |
|---:|---|---:|---|---|
{dispatch_rows}

## 4CC Map

Extracted {fourcc['mapping_count']:,} getter/setter branch records and {fourcc['unique_fourcc_count_global']:,} distinct 4CCs across present vtable-root property handlers. PERSON and CONTRACT getter evidence is static-only; helper-only branches remain labeled as helper/computed and preserve source lines. The extractor reuses `t97`'s cast-aware `CFunc` offset analysis.

## Wire and Archive Probe

Basic archive byte closure: {wire['basic_people_db_validation']['row_count']:,} rows, diff {wire['basic_people_db_validation']['closure_diff']}; class histogram: {hist}.

`people_db.dat`: {wire['people_db_probe']['archive']['decompressed_bytes']:,} in-memory decompressed bytes; header is two zero bytes plus count {wire['people_db_probe']['archive']['declared_record_count_u32']:,}. The first 1,193 records have byte-verified type 5 bodies and close exactly at offset {wire['people_db_probe']['first_non_type5_record']['record_offset']:,}; the next record is type {wire['people_db_probe']['first_non_type5_record']['person_type']} at that offset, with body beginning at {wire['people_db_probe']['first_non_type5_record']['body_offset']:,}. First 20 names include row 0 `Zarko Serafimovski`. The type-5 grammar is not used to guess later record boundaries.

Byte-verified type-5 fields are ordinal/type, a zero u32, UTF-8 name length and bytes, eight zero bytes, repeated ordinal, and two equal opaque u32 values. Semantic first/second/common-name IDs, DOB, nation, and UID are **not** established. Star UID byte hits are included as unvalidated raw occurrences, not asserted row membership.

The stream-step output is static source-order evidence only. The missing PERSON/PLAYER readers prevent L3 closure of their common/subclass serialization order and prevent a verified type 1..6 histogram or exact player/non-player body ends.

## IDA Follow-up

Prioritized missing VAs:

{missing}

`PLAYER_DATA` / `NON_PLAYER_DATA` serializers have no grounded VA in the supplied vtable JSON; the machine-readable output asks for a targeted symbol/vtable search without fabricating addresses.

## Evidence Levels

- **L3 byte-verified:** basic_people frame closure; first 1,193 type-5 records in people_db; first 20 raw row boundaries/names; next type-2 body start.
- **Static-only:** factory cases, property 4CC-to-memory-offset candidates, and stream calls in decompiled functions.
- **Open:** semantic names/DOB/nation/UID fields in PERSON, types 1/3/4/6 sample boundaries, PLAYER/NON_PLAYER body ends, and missing reader/writer implementations.

Input `.dat` files were read-only; decompressed bytes remained in memory.
"""


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    if not VTABLE_JSON.exists() or not (T113_FUNCS / "1410992c0.c").exists():
        raise FileNotFoundError("t113 factory/vtable inputs are missing")
    vt_json = read_json(VTABLE_JSON)
    # Phase 1: persist factory/vtable dispatch before heavier archive work.
    factory = extract_factory(vt_json)
    jwrite(OUT / "people_factory_map.json", factory)
    print(f"[t118] phase 1/4: factory cases={len(factory['dispatch'])}, need_ida_vas={len(factory['need_ida_vas'])}", flush=True)

    # Phase 2: extract every available property branch from the saved class vtables.
    fourcc = extract_4cc(vt_json)
    jwrite(OUT / "people_4cc_mem.json", fourcc)
    print(f"[t118] phase 2/4: mappings={fourcc['mapping_count']}, unique_4cc={fourcc['unique_fourcc_count_global']}", flush=True)

    # Phase 3: frame validation and in-memory zstd probing; no raw dump is written.
    _, basic_view, basic_meta = zstd_decompress_in_memory(BASIC_DAT, BASIC_SIZE)
    basic_info = parse_basic_payload(basic_view)
    _, people_view, people_meta = zstd_decompress_in_memory(PEOPLE_DAT, PEOPLE_SIZE)
    people_info = probe_people_payload(people_view, basic_info["histogram"])
    wire = build_wire(vt_json, fourcc, basic_info, people_info)
    wire["input_archives"] = {"people_db.dat": people_meta, "basic_people_db.dat": basic_meta}
    jwrite(OUT / "people_wire_steps.json", wire)
    print(f"[t118] phase 3/4: type5_rows={people_info['type5_prefix']['rows_closed']}, first_non5_type={people_info['first_non_type5_record']['person_type']}, wire_steps={wire['wire_step_count']}", flush=True)

    # Phase 4: report and completion marker are written last.
    report = render_report(factory, fourcc, wire, basic_meta, people_meta)
    textwrite(OUT / "REPORT.md", report)
    result = {"factory_cases": len(factory["dispatch"]), "fourcc_mappings": fourcc["mapping_count"],
              "unique_fourcc": fourcc["unique_fourcc_count_global"], "wire_steps": wire["wire_step_count"],
              "basic_rows": basic_info["row_count"], "basic_closure_diff": basic_info["closure_diff"],
              "people_type5_rows": people_info["type5_prefix"]["rows_closed"],
              "people_first_non5_type": people_info["first_non_type5_record"]["person_type"],
              "selftest": "PASS; run invariants were checked during generation"}
    done = ("DONE type=t118\n\n" + json.dumps(result, indent=2, ensure_ascii=False) +
            "\n\nEvidence remains partial where the required Hex-Rays readers/writers are absent.\n")
    textwrite(OUT / "DONE.md", done)
    print("[t118] phase 4/4: REPORT.md and DONE.md written")
    print("[t118] delivery:")
    for name in ("people_factory_map.json", "people_4cc_mem.json", "people_wire_steps.json", "REPORT.md", "DONE.md"):
        print(f"  {OUT / name}")
    print("[t118] core stats: " + json.dumps(result, ensure_ascii=False))
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true", help="run parser and real-input byte-closure tests")
    args = ap.parse_args()
    try:
        static_selftest()
        if args.selftest:
            stats = binary_selftest()
            print("selftest: PASS " + json.dumps(stats, ensure_ascii=False))
            return 0
        run()
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
