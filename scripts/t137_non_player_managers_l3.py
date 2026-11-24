"""L3 map for FM24 NON_PLAYER properties and verified top-CA manager cards.

Usage:
  py -V:3.12 -B scripts/t137_non_player_managers_l3.py
  py -V:3.12 -B scripts/t137_non_player_managers_l3.py --selftest
  py -V:3.12 -B scripts/t137_non_player_managers_l3.py --uid 123456
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import re
import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch/t137/out"
BASIC_DAT = ROOT / "scratch/data/basic_people_db.dat"
PEOPLE_DAT = ROOT / "scratch/data/people_db.dat"
TRACE_JSON = ROOT / "scratch/t120/out/people_unicorn_traces.json"
GET_C = ROOT / "scratch/t124/out/funcs/140dca880.c"
SET_C = ROOT / "scratch/t124/out/funcs/140dc8c00.c"
GET_INDEX_C = OUT_DIR / "ida/140dc4db0.c"
SET_INDEX_C = OUT_DIR / "ida/140dc4e30.c"
NT_DISPATCH_C = OUT_DIR / "ida/140dca530.c"
T108_JSON = ROOT / "scratch/t108/out/fourcc_mem_map_v2.json"

sys.path.insert(0, str(_cfg.VENDOR_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

BASIC_WIDTH = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
BASIC_COUNT_OFF = 0
BASIC_START = 5
UID_OFF = 75
CA_OFF = 48
PA_OFF = 50
YEAR_OFF = 52
OBJECT_BASE_FROM_HEAP = 0xF8
TOP_N = 20

FOURCC_REF_RE = re.compile(r"(?:case\s+|\ba2\s*(?:==|!=)\s*)(0x[0-9a-fA-F]+|\d+)")
FIELD_RE = re.compile(
    r"\*\s*\(\s*([^)]*?)\s*\*\s*\)\s*\(\s*a1\s*([+-])\s*(0x[0-9a-fA-F]+|\d+)\s*\)"
)
HELPER_RE = re.compile(r"sub_140DC4DB0\([^\n]*?a2:\s*(0x[0-9a-fA-F]+|\w+)")
ASSIGN_RE = re.compile(r"(?:LOBYTE\(\s*(\w+)\s*\)|\b(\w+))\s*=\s*(\d+)\s*;")

# FM editor property labels where the 4CC is unambiguous; other properties retain their 4CC.
ATTRIBUTE_LABELS = {
    "Npat": "Attacking",
    "Npde": "Defending",
    "Npfi": "Fitness",
    "Npgk": "Goalkeeping",
    "Npme": "Mental",
    "Npta": "Tactical",
    "Npte": "Technical",
    "Npja": "Judging Player Ability",
    "Npjp": "Judging Player Potential",
    "Npjr": "Judging Player Reputation",
    "Npmm": "Man Management",
    "Npmo": "Motivating",
    "Npad": "Adaptability",
    "Npdi": "Determination",
    "Npld": "Level of Discipline",
    "Npwy": "Working With Youngsters",
    "Nptk": "Tactical Knowledge",
}


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def decompress(path: Path) -> bytes:
    import zstandard

    raw = path.read_bytes()
    with zstandard.ZstdDecompressor().stream_reader(raw[8:]) as rdr:
        return rdr.read()


def fourcc_from_int(value: int) -> str | None:
    if value < 0 or value > 0xFFFFFFFF:
        return None
    raw = struct.pack(">I", value)
    if not all((48 <= c <= 57) or (65 <= c <= 90) or (97 <= c <= 122) for c in raw):
        return None
    return raw.decode("ascii")


def source_refs(path: Path, prefix: str = "N") -> tuple[list[str], dict[str, list[int]]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    refs: dict[str, list[int]] = {}
    for line_no, line in enumerate(lines, 1):
        for match in FOURCC_REF_RE.finditer(line):
            code = fourcc_from_int(int(match.group(1), 0))
            if code and code.startswith(prefix):
                refs.setdefault(code, []).append(line_no)
    return lines, refs


def field_offsets(lines: list[str], start: int, end: int) -> list[dict]:
    found: dict[tuple[int, int], dict] = {}
    for index in range(max(0, start - 1), min(len(lines), end)):
        line = lines[index]
        for match in FIELD_RE.finditer(line):
            sign = 1 if match.group(2) == "+" else -1
            amount = int(match.group(3), 0)
            off = sign * amount
            c_type = re.sub(r"\s+", " ", match.group(1).strip())
            width = 8 if "_QWORD" in c_type or "__int64" in c_type else (
                4 if "_DWORD" in c_type or "int" in c_type else (
                    2 if "_WORD" in c_type or "short" in c_type or "__int16" in c_type else 1
                )
            )
            found[(off, width)] = {"obj_off": off, "width": width, "c_type": c_type, "line": index + 1}
    return list(found.values())


def branch_window(lines: list[str], ref_lines: list[int], code: str, all_refs: dict[str, list[int]]) -> list[tuple[int, int]]:
    windows = []
    all_positions = sorted((ln, fcc) for fcc, lns in all_refs.items() for ln in lns)
    for line_no in ref_lines:
        next_ref = next((ln for ln, fcc in all_positions if ln > line_no and fcc != code), None)
        end_line = min(len(lines), line_no + 42)
        if next_ref is not None:
            end_line = min(end_line, next_ref)
        windows.append((line_no, end_line))
    return windows


def helper_index(lines: list[str], start: int, end: int) -> int | None:
    for index in range(start - 1, min(end, len(lines))):
        match = HELPER_RE.search(lines[index])
        if not match:
            continue
        arg = match.group(1)
        if arg.lower().startswith("0x") or arg.isdigit():
            return int(arg, 0)
        prior = "\n".join(lines[start - 1:index])
        assignments = []
        for assign in ASSIGN_RE.finditer(prior):
            var = assign.group(1) or assign.group(2)
            if var == arg:
                assignments.append(int(assign.group(3)))
        return assignments[-1] if assignments else None
    return None


def analyze_code(lines: list[str], refs: dict[str, list[int]], code: str) -> dict:
    offsets = []
    idxs = []
    windows = branch_window(lines, refs[code], code, refs)
    candidate_lines = []
    for start, end in windows:
        candidate_lines.append(start)
        offsets.extend(field_offsets(lines, start, end))
        idx = helper_index(lines, start, end)
        if idx is not None:
            idxs.append(idx)
    unique = {(x["obj_off"], x["width"]): x for x in offsets}
    return {
        "line": min(candidate_lines) if candidate_lines else None,
        "offsets": list(unique.values()),
        "helper_indices": sorted(set(idxs)),
    }


def parse_index_table(path: Path) -> dict[int, dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    result = {}
    case_re = re.compile(r"\bcase\s+(\d+)\s*:")
    for index, line in enumerate(lines):
        match = case_re.search(line)
        if not match:
            continue
        case_id = int(match.group(1))
        for next_index in range(index + 1, min(len(lines), index + 22)):
            if case_re.search(lines[next_index]):
                break
            field = FIELD_RE.search(lines[next_index])
            if field:
                sign = 1 if field.group(2) == "+" else -1
                raw_off = sign * int(field.group(3), 0)
                result[case_id] = {
                    "obj_off": raw_off - 248,
                    "width": 1,
                    "source_line": next_index + 1,
                    "helper_byte_off": raw_off,
                }
                break
        result.setdefault(case_id, {"obj_off": None, "width": None, "source_line": index + 1, "helper_byte_off": None})
    return result


def parse_nt_dispatch(path: Path) -> dict[str, dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    output = {}
    case_re = re.compile(r"\bcase\s+(\d+)\s*:")
    for index, line in enumerate(lines):
        match = case_re.search(line)
        if not match:
            continue
        code = fourcc_from_int(int(match.group(1)))
        if not code or not code.startswith("NT"):
            continue
        mapped = None
        for next_index in range(index + 1, min(len(lines), index + 12)):
            if case_re.search(lines[next_index]):
                break
            ret = re.search(r"\breturn\s+(-?\d+)\s*;", lines[next_index])
            result = re.search(r"\bresult\s*=\s*(-?\d+)\s*;", lines[next_index])
            if ret:
                mapped = int(ret.group(1))
                break
            if result:
                mapped = int(result.group(1))
                break
        output[code] = {"dispatcher_index": mapped, "dispatcher_line": index + 1}
    return output


def trace_wire_map(traces: dict) -> dict[int, dict]:
    observations: dict[int, list[dict]] = {}
    for sample in traces.get("samples_by_type", {}).get("1", []):
        for read in sample.get("reads", []):
            obj_off = read.get("obj_off_dec")
            width = read.get("n", 0)
            if obj_off is None or width <= 0 or read.get("dst_kind") != "obj_mem":
                continue
            for delta in range(width):
                off = obj_off + delta
                observations.setdefault(off, []).append({
                    "wire_off": read["wire_pos"] + delta,
                    "row_idx": sample["row_idx"],
                    "read_width": width,
                })
    out = {}
    for obj_off, rows in observations.items():
        values = sorted({row["wire_off"] for row in rows})
        out[obj_off] = {
            "wire_off": values[0] if len(values) == 1 else None,
            "wire_off_candidates": values,
            "conditional": len(values) > 1,
            "observations": rows,
        }
    return out


def infer_scale(code: str, get_lines: list[str], set_lines: list[str], get_analysis: dict,
                set_analysis: dict, helper_index_map: dict[int, dict]) -> tuple[int, int | None]:
    idx = next(iter(get_analysis["helper_indices"]), None)
    if idx is not None:
        entry = helper_index_map.get(idx, {})
        # The helper's a3 flag converts 5-point wire values to 0..20 for these indices.
        if idx in set(range(24)) - {3, 13} or idx in (28, 29):
            return 5, 20
    contexts = []
    for lines, analysis in ((get_lines, get_analysis), (set_lines, set_analysis)):
        if analysis["line"] is not None:
            start = analysis["line"] - 1
            contexts.append("\n".join(lines[start:min(len(lines), start + 42)]))
    joined = "\n".join(contexts)
    if re.search(r"\b5\s*\*", joined) or "26215 *" in joined or "26215*" in joined:
        return 5, 20
    if any(x["width"] == 1 for x in get_analysis["offsets"] + set_analysis["offsets"]) and re.search(r"\b20\b", joined):
        return 1, 20
    return 1, None


def build_own_map(traces: dict) -> tuple[list[dict], dict]:
    get_lines, get_refs = source_refs(GET_C)
    set_lines, set_refs = source_refs(SET_C)
    all_codes = sorted(set(get_refs) | set(set_refs))
    helper_index_map = parse_index_table(GET_INDEX_C)
    nt_codes = parse_nt_dispatch(NT_DISPATCH_C)
    wire_map = trace_wire_map(traces)
    get_route = next((i for i, line in enumerate(get_lines, 1) if "sub_140DCA530" in line), None)
    set_route = next((i for i, line in enumerate(set_lines, 1) if "sub_140DCA530" in line), None)
    mappings = []
    for code in all_codes:
        ga = analyze_code(get_lines, get_refs, code) if code in get_refs else {"line": None, "offsets": [], "helper_indices": []}
        sa = analyze_code(set_lines, set_refs, code) if code in set_refs else {"line": None, "offsets": [], "helper_indices": []}
        g_offsets = ga["offsets"]
        s_offsets = sa["offsets"]
        helper_idx = next(iter(ga["helper_indices"]), None)
        helper_entry = helper_index_map.get(helper_idx, {}) if helper_idx is not None else {}
        if helper_entry.get("obj_off") is not None:
            g_offsets = [{"obj_off": helper_entry["obj_off"], "width": 1,
                          "c_type": "helper-indexed byte", "line": helper_entry["source_line"]}]
        g_set = {(x["obj_off"], x["width"]) for x in g_offsets}
        s_set = {(x["obj_off"], x["width"]) for x in s_offsets}
        common = g_set & s_set
        all_single = len(g_set) == 1 and len(s_set) == 1 and len(common) == 1
        if all_single:
            obj_off, width = next(iter(common))
            kind = "scalar"
            reason = None
        else:
            obj_off = width = None
            code_name = code.upper()
            if code_name == "NRCJ":
                kind, reason = "composite", "aggregates multiple coaching capability bytes"
            elif code_name == "NRLS":
                kind, reason = "computed", "derived from registry/list state"
            elif code_name == "NSCR":
                kind, reason = "computed", "scaled composite of reputation words"
            elif g_offsets or s_offsets:
                kind, reason = "computed", "multiple or disagreeing GET/SET storage offsets"
            else:
                kind, reason = "computed", "no single inline object byte field"
        scale, semantic_max = infer_scale(code, get_lines, set_lines, ga, sa, helper_index_map)
        trace = wire_map.get(obj_off, {}) if obj_off is not None else {}
        scalar_attr = bool(kind == "scalar" and width == 1 and semantic_max == 20)
        mappings.append({
            "fourcc": code,
            "code_int": int.from_bytes(code.encode("ascii"), "big"),
            "hex_id": hex(int.from_bytes(code.encode("ascii"), "big")),
            "attribute_name": ATTRIBUTE_LABELS.get(code, code),
            "obj_off": obj_off,
            "obj_off_hex": hex(obj_off) if obj_off is not None else None,
            "base_off": obj_off + OBJECT_BASE_FROM_HEAP if obj_off is not None else None,
            "wire_off": trace.get("wire_off"),
            "wire_off_candidates": trace.get("wire_off_candidates", []),
            "wire_conditional": trace.get("conditional", False),
            "width": width,
            "value_scale": scale,
            "semantic_range": {"min": 0, "max": semantic_max} if semantic_max is not None else None,
            "scalar_attribute": scalar_attr,
            "kind": kind,
            "computed_reason": reason,
            "helper_index": helper_idx,
            "get_line": ga["line"],
            "set_line": sa["line"],
            "get_helper_line": helper_entry.get("source_line") if helper_idx is not None else None,
            "get_offsets": g_offsets,
            "set_offsets": s_offsets,
            "get_set_agree": bool(all_single or (kind in ("computed", "composite") and ga["line"] and sa["line"])),
            "evidence": "static_GET_SET_plus_Unicorn_wire_join",
        })
    for code, nt in sorted(nt_codes.items()):
        if code in all_codes:
            continue
        mappings.append({
            "fourcc": code,
            "code_int": int.from_bytes(code.encode("ascii"), "big"),
            "hex_id": hex(int.from_bytes(code.encode("ascii"), "big")),
            "attribute_name": f"Dynamic indexed property {nt['dispatcher_index']}",
            "obj_off": None,
            "obj_off_hex": None,
            "base_off": None,
            "wire_off": None,
            "wire_off_candidates": [],
            "wire_conditional": False,
            "width": None,
            "value_scale": None,
            "semantic_range": {"min": 0, "max": 20},
            "scalar_attribute": False,
            "kind": "dynamic_indexed",
            "computed_reason": "NTxx dispatches to an indexed external/property array, not a fixed object byte",
            "dispatcher_index": nt["dispatcher_index"],
            "dispatcher_line": nt["dispatcher_line"],
            "get_line": get_route,
            "set_line": set_route,
            "get_set_agree": bool(get_route and set_route),
            "evidence": "static_NT_dispatch_and_GET_SET_dynamic_array_paths",
        })
    mappings.sort(key=lambda x: (x["fourcc"], x["kind"]))
    summary = {
        "own_fourcc_count": len(all_codes),
        "ntxx_dynamic_fourcc_count": sum(1 for item in mappings if item["kind"] == "dynamic_indexed"),
        "ntxx_dispatch_code_count": len(nt_codes),
        "scalar_attribute_count": sum(1 for x in mappings if x["scalar_attribute"]),
        "scalar_with_wire_offset_count": sum(1 for x in mappings if x["scalar_attribute"] and x["wire_off"] is not None),
        "computed_or_composite_count": sum(1 for x in mappings if x["kind"] in ("computed", "composite", "dynamic_indexed")),
        "trace_rows": len(traces.get("samples_by_type", {}).get("1", [])),
        "conditional_obj_offsets": sorted(off for off, info in wire_map.items() if info["conditional"]),
    }
    doc = {
        "schema_id": "fm24.t137.non_player_attributes_l3",
        "schema_version": 1,
        "person_type": 1,
        "person_class": "NON_PLAYER",
        "method": "NON_PLAYER get_prop/set_prop static C branch extraction joined to ptype=1 Unicorn read traces; inherited BASIC_PERSON offsets separately reference t108 L3 map",
        "offset_convention": {
            "unicorn_obj_off": "base_off - 0xf8",
            "direct_get_set": "a1 +/- N is the object-relative byte offset",
            "indexed_helper": "sub_140DC4DB0 receives this - 248; helper byte offset N maps to object offset N - 248",
        },
        "summary": summary,
        "attributes": mappings,
        "trace_wire_map": {str(k): v for k, v in sorted(wire_map.items())},
    }
    return doc, wire_map


def build_inherited_map(wire_map: dict[int, dict]) -> list[dict]:
    if not T108_JSON.exists():
        return []
    root = read_json(T108_JSON)
    table = next((t for t in root.get("tables", []) if t.get("table_type") == 1), None)
    if not table:
        return []
    get_lines = GET_C.read_text(encoding="utf-8", errors="replace").splitlines()
    set_lines = SET_C.read_text(encoding="utf-8", errors="replace").splitlines()
    get_delegate = next((i for i, line in enumerate(get_lines, 1) if "sub_140DEDA40" in line), None)
    set_delegate = next((i for i, line in enumerate(set_lines, 1) if "sub_140DEA4A0" in line), None)
    out = []
    for code, entry in sorted(table.get("fourccs", {}).items()):
        if not isinstance(code, str) or len(code) != 4:
            continue
        off = entry.get("primary_off_int")
        if off is None:
            off = entry.get("alt", {}).get("primary_off_int")
        if entry.get("offset_space") != "this" or off is None:
            off = None
        trace = wire_map.get(off, {}) if off is not None else {}
        alt = entry.get("alt") or {}
        out.append({
            "fourcc": code,
            "code_int": entry.get("code_int"),
            "attribute_name": code,
            "obj_off": off,
            "obj_off_hex": hex(off) if off is not None else None,
            "base_off": off + OBJECT_BASE_FROM_HEAP if off is not None else None,
            "wire_off": trace.get("wire_off"),
            "wire_off_candidates": trace.get("wire_off_candidates", []),
            "wire_conditional": trace.get("conditional", False),
            "width": entry.get("width"),
            "get_line": get_delegate,
            "set_line": set_delegate,
            "source_get_line": alt.get("line_no") if alt.get("slot") == "slot02_get_prop" else entry.get("line_no"),
            "source_set_line": entry.get("line_no") if entry.get("slot") == "slot03_set_prop" else alt.get("line_no"),
            "access_kind": entry.get("access_kind"),
            "offset_space": entry.get("offset_space"),
            "delegated": True,
            "get_set_agree": bool(entry.get("alt")),
            "evidence": "t108_BASIC_PERSON_L3_plus_NON_PLAYER_base_delegation",
        })
    return out


def build_attribute_document() -> tuple[dict, dict]:
    traces = read_json(TRACE_JSON)
    own_doc, wire_map = build_own_map(traces)
    inherited = build_inherited_map(wire_map)
    own_codes = {x["fourcc"] for x in own_doc["attributes"]}
    inherited = [x for x in inherited if x["fourcc"] not in own_codes]
    own_doc["inherited_basic_person"] = inherited
    own_doc["summary"].update({
        "inherited_basic_person_fourcc_count": len(inherited),
        "total_distinct_fourcc_count": len(own_codes) + len(inherited),
        "l3_attributes": sum(1 for x in own_doc["attributes"] if x["scalar_attribute"] and x["get_set_agree"]),
        "inherited_wire_resolved_count": sum(1 for x in inherited if x["wire_off"] is not None),
    })
    return own_doc, wire_map


def parse_basic_people(buf: bytes) -> tuple[list[dict], dict]:
    count = struct.unpack_from("<I", buf, BASIC_COUNT_OFF)[0]
    pos = BASIC_START
    rows = []
    hist: dict[int, int] = {}
    for ordinal in range(count):
        if pos + 2 > len(buf) or buf[pos] != 0x11:
            raise ValueError(f"invalid basic_people marker at ordinal={ordinal} off={pos}")
        ptype = buf[pos + 1]
        width = BASIC_WIDTH.get(ptype)
        if width is None or pos + width > len(buf):
            raise ValueError(f"unsupported basic_people ptype={ptype} ordinal={ordinal}")
        hist[ptype] = hist.get(ptype, 0) + 1
        if ptype == 1:
            rows.append({
                "ordinal": ordinal,
                "record_offset": pos,
                "person_type": ptype,
                "uid": struct.unpack_from("<I", buf, pos + UID_OFF)[0],
                "CA": struct.unpack_from("<H", buf, pos + CA_OFF)[0],
                "PA": struct.unpack_from("<H", buf, pos + PA_OFF)[0],
                "birth_year": struct.unpack_from("<H", buf, pos + YEAR_OFF)[0],
            })
        pos += width
    closure = {"declared_count": count, "row_chain_end": pos, "expected_end": len(buf) - 9,
               "closure_diff": pos - (len(buf) - 9), "ptype_histogram": hist}
    if closure["closure_diff"] != 0:
        raise ValueError(f"basic_people framing did not close: {closure}")
    return rows, closure


def load_name_pools() -> tuple[dict[int, str], dict[int, str], dict[int, str]]:
    # Keep the established t126 parser as the source of truth for the UTF-8 pool format.
    import t126_player_attributes_l3 as t126

    return t126.load_name_pools()


def read_identity(res: dict) -> tuple[int, int, int] | None:
    read = next((r for r in reversed(res.get("reads", [])) if r.get("n") == 12 and len(r.get("hex", "")) == 24), None)
    if not read:
        return None
    return struct.unpack("<III", bytes.fromhex(read["hex"]))


def row_wire_offset(res: dict, obj_off: int) -> int | None:
    positions = set()
    for read in res.get("reads", []):
        base = read.get("obj_off_dec")
        width = read.get("n", 0)
        if base is not None and width > 0 and read.get("dst_kind") == "obj_mem" and base <= obj_off < base + width:
            positions.add(read["wire_pos"] + obj_off - base)
    return next(iter(positions)) if len(positions) == 1 else None


def decode_names(res: dict, pools: tuple[dict[int, str], dict[int, str], dict[int, str]]) -> dict:
    reads = [r for r in res.get("reads", []) if r.get("caller") == "0x143b93527" and r.get("n") == 4]
    nids = [struct.unpack("<i", bytes.fromhex(r["hex"]))[0] for r in reads[:3]]
    while len(nids) < 3:
        nids.append(-1)
    first = pools[0].get(nids[0], "") if nids[0] >= 0 else ""
    second = pools[1].get(nids[1], "") if nids[1] >= 0 else ""
    common = pools[2].get(nids[2], "") if nids[2] >= 0 else ""
    name = common.strip() or f"{first} {second}".strip()
    return {"ids": {"first": nids[0], "second": nids[1], "common": nids[2]},
            "parts": {"first": first, "second": second, "common": common}, "full_name": name}


def locate_person(buf: bytes, target: dict, t120, ut, emu) -> tuple[int, dict, tuple[int, int, int]]:
    ordinal, uid = target["ordinal"], target["uid"]
    identity_pattern = struct.pack("<III", ordinal, uid, uid)
    header_pattern = struct.pack("<IB", ordinal, 1)
    search_from = 0
    while True:
        ident_pos = buf.find(identity_pattern, search_from)
        if ident_pos < 0:
            raise AssertionError(f"identity anchor missing for uid={uid} ordinal={ordinal}")
        lower = max(0, ident_pos - 2605)
        hits = []
        pos = buf.find(header_pattern, lower, ident_pos)
        while pos >= 0:
            distance = ident_pos - pos - 5
            if 0 < distance <= 2600:
                hits.append((pos, distance))
            pos = buf.find(header_pattern, pos + 1, ident_pos)
        for hit, distance in hits:
            obj, _, s19, factory_error = t120.call_people_factory(ut, emu, 1)
            if factory_error or not s19:
                continue
            res = t120.run_person_row(ut, emu, obj, s19, buf[hit + 5:hit + 5 + 65536])
            if not res["ok"] or res["bytes_consumed"] - 12 != distance:
                continue
            identity = read_identity(res)
            if identity == (ordinal, uid, uid):
                return hit, res, identity
        search_from = ident_pos + 1


def normalize_wire_value(body: bytes, wire_off: int, width: int, scale: int) -> tuple[int, int]:
    if wire_off < 0 or wire_off + width > len(body):
        raise ValueError(f"wire span out of bounds: {wire_off}+{width}/{len(body)}")
    raw = int.from_bytes(body[wire_off:wire_off + width], "little", signed=False)
    if scale == 5:
        value = (raw + 2) // 5
    else:
        value = raw
    return raw, value


def decode_manager(target: dict, buf: bytes, t120, ut, emu, pools, attributes: list[dict],
                   wire_map: dict[int, dict]) -> dict:
    hit, res, identity = locate_person(buf, target, t120, ut, emu)
    body = buf[hit + 5:hit + 5 + res["bytes_consumed"]]
    optional_count = struct.unpack_from("<H", body, 0)[0]
    header_wire_off = 2 + optional_count * 3
    if header_wire_off + 10 > len(body):
        raise AssertionError(f"invalid NON_PLAYER header prefix uid={target['uid']} count={optional_count}")
    hrep, crep, wrep, ca, pa = struct.unpack_from("<5h", body, header_wire_off)
    if (ca, pa) != (target["CA"], target["PA"]):
        raise AssertionError(
            f"CA/PA mismatch uid={target['uid']} wire={(ca, pa)} basic={(target['CA'], target['PA'])} "
            f"header_wire_off={header_wire_off} optional_count={optional_count}"
        )
    names = decode_names(res, pools)
    attr_values = []
    for entry in attributes:
        if not entry.get("scalar_attribute"):
            continue
        obj_off = entry.get("obj_off")
        width = entry.get("width")
        if obj_off is None or width is None:
            continue
        wire_off = row_wire_offset(res, obj_off)
        if wire_off is None:
            static = wire_map.get(obj_off, {}).get("wire_off")
            wire_off = static
        if wire_off is None:
            continue
        raw, value = normalize_wire_value(body, wire_off, width, entry.get("value_scale") or 1)
        attr_values.append({
            "fourcc": entry["fourcc"],
            "name": entry["attribute_name"],
            "obj_off": obj_off,
            "wire_off": wire_off,
            "raw_wire_value": raw,
            "value": value,
            "valid_0_20": 0 <= value <= 20,
        })
    all_valid = bool(attr_values) and all(v["valid_0_20"] for v in attr_values)
    return {
        "rank": None,
        "selection": "top20_highest_CA_ptype1",
        "ordinal": target["ordinal"],
        "uid": target["uid"],
        "identity": {
            "ordinal": identity[0], "dbid": identity[1], "uid": identity[2],
            "dbid_equals_uid": identity[1] == identity[2],
            "matches_basic_people": identity == (target["ordinal"], target["uid"], target["uid"]),
        },
        "name_ids": names["ids"],
        "name_parts": names["parts"],
        "full_name": names["full_name"],
        "person_type": 1,
        "class": "NON_PLAYER",
        "people_db_file_offset": hit,
        "body_len": res["bytes_consumed"],
        "header": {
            "home_rep": hrep, "current_rep": crep, "world_rep": wrep,
            "CA": ca, "PA": pa,
            "wire_offset": header_wire_off,
            "optional_tagged_field_count": optional_count,
        },
        "basic_people_cross_check": {
            "CA_at_plus48": target["CA"], "PA_at_plus50": target["PA"],
            "birth_year_at_plus52": target["birth_year"],
            "CA_exact_match": ca == target["CA"], "PA_exact_match": pa == target["PA"],
            "record_offset": target["record_offset"],
        },
        "attributes": attr_values,
        "attributes_by_fourcc": {v["fourcc"]: v["value"] for v in attr_values},
        "scalar_attribute_count": len(attr_values),
        "all_scalar_attributes_in_0_20": all_valid,
        "unicorn": {
            "ok": res["ok"], "bytes_consumed": res["bytes_consumed"],
            "identity_tail_matches": identity == (target["ordinal"], target["uid"], target["uid"]),
            "body_distance_check": True,
        },
    }


def load_progress(path: Path) -> dict[str, dict] | None:
    if not path.exists():
        return None
    try:
        doc = read_json(path)
        cards = doc.get("cards", [])
        return {str(c.get("uid")): c for c in cards if c.get("uid") is not None}
    except (OSError, json.JSONDecodeError, TypeError):
        return None


def build_top20(attribute_doc: dict, wire_map: dict[int, dict], uid: int | None = None) -> dict:
    import t120_people_unicorn as t120

    t0 = time.time()
    basic = decompress(BASIC_DAT)
    rows, closure = parse_basic_people(basic)
    if uid is None:
        targets = sorted(rows, key=lambda r: (-r["CA"], -r["PA"], r["ordinal"]))[:TOP_N]
    else:
        targets = [next((r for r in rows if r["uid"] == uid), None)]
        if targets[0] is None:
            raise ValueError(f"uid {uid} not found in basic_people ptype=1 rows")
    people = decompress(PEOPLE_DAT)
    _, ut, emu, _ = t120.setup_people_emulator()
    pools = load_name_pools()
    own_attributes = attribute_doc["attributes"]
    cards_by_uid = load_progress(OUT_DIR / "top20_managers_cards.json") if uid is None else None
    cards_by_uid = cards_by_uid or {}
    cards = []
    for index, target in enumerate(targets, 1):
        prior = cards_by_uid.get(str(target["uid"]))
        if prior and prior.get("unicorn", {}).get("ok") and prior.get("basic_people_cross_check", {}).get("CA_exact_match") and prior.get("basic_people_cross_check", {}).get("PA_exact_match"):
            card = prior
        else:
            card = decode_manager(target, people, t120, ut, emu, pools, own_attributes, wire_map)
        card["rank"] = index if uid is None else None
        if not card.get("full_name"):
            raise AssertionError(f"could not resolve UTF-8 name for uid={target['uid']}")
        if not card.get("all_scalar_attributes_in_0_20"):
            invalid = [(a["fourcc"], a["value"]) for a in card["attributes"] if not a["valid_0_20"]]
            raise AssertionError(f"scalar attribute out of 0..20 for uid={target['uid']}: {invalid}")
        cards.append(card)
        if uid is None:
            partial = {
                "schema_id": "fm24.t137.top20_non_player_manager_cards",
                "schema_version": 1,
                "status": "partial" if index < len(targets) else "complete",
                "summary": {"target_count": len(targets), "decoded_count": index,
                            "CA_PA_cross_check": f"{index}/{index}", "identity_verified": f"{index}/{index}"},
                "basic_people_framing": closure,
                "cards": cards,
            }
            write_json(OUT_DIR / "top20_managers_cards.json", partial)
            print(f"[stage] manager cards {index}/{len(targets)}: {card['full_name']} (CA {card['header']['CA']})", flush=True)
    if uid is not None:
        return {"uid_card": cards[0], "basic_people_framing": closure,
                "people_db_decompressed_bytes": len(people), "elapsed_sec": round(time.time() - t0, 2)}
    summary = {
        "target_count": len(targets),
        "decoded_count": len(cards),
        "identity_verified": sum(1 for c in cards if c["identity"]["dbid_equals_uid"] and c["identity"]["matches_basic_people"]),
        "CA_exact_match": sum(1 for c in cards if c["basic_people_cross_check"]["CA_exact_match"]),
        "PA_exact_match": sum(1 for c in cards if c["basic_people_cross_check"]["PA_exact_match"]),
        "all_scalar_attributes_in_0_20": sum(1 for c in cards if c["all_scalar_attributes_in_0_20"]),
        "scalar_attributes_per_card": sorted({c["scalar_attribute_count"] for c in cards}),
        "people_db_decompressed_bytes": len(people),
        "basic_people_ptype1_rows": len(rows),
    }
    doc = {
        "schema_id": "fm24.t137.top20_non_player_manager_cards",
        "schema_version": 1,
        "status": "complete",
        "method": "top-20 CA ptype=1 basic_people targets located by trailing identity, then factory + slot19 Unicorn decode",
        "verification": {
            "locating_predicate": "identity <III>(ordinal,uid,uid), prior header <IB>(ordinal,1), 0<body_len<=2600, Unicorn bytes_consumed-12 == identity_pos-hit-5",
            "people_db_header": "u16 optional-tagged-field count; count * 3 bytes; then five i16 values (home/current/world reputation, CA, PA)",
            "CA_PA_offsets": {"CA": "+48 u16", "PA": "+50 u16", "birth_year": "+52 u16", "uid": "+75 u32"},
            "name_pools": "scratch/t106/out/payload_server_name_table_extra_{0,1,2}.bin via scripts/t126_player_attributes_l3.py:load_name_pools",
            "attributes": "every mapped scalar attribute decoded from row-specific Unicorn wire positions and checked in 0..20",
        },
        "summary": summary,
        "basic_people_framing": closure,
        "cards": cards,
    }
    write_json(OUT_DIR / "top20_managers_cards.json", doc)
    print(f"[stage] complete manager cards: {summary['decoded_count']}/20; CA/PA={summary['CA_exact_match']}/{summary['PA_exact_match']}; scalar attrs/card={summary['scalar_attributes_per_card']}", flush=True)
    return doc


def write_report(attribute_doc: dict, cards_doc: dict) -> None:
    lines = [
        "# t137c: NON_PLAYER Attribute L3 Map and Top-20 FM24 Managers",
        "",
        f"- Own NON_PLAYER 4CCs: **{attribute_doc['summary']['own_fourcc_count']}**; NTxx dynamic aliases: **{attribute_doc['summary']['ntxx_dynamic_fourcc_count']}**.",
        f"- L3 scalar attributes with GET/SET agreement: **{attribute_doc['summary']['l3_attributes']}**; inherited BASIC_PERSON 4CCs documented: **{attribute_doc['summary']['inherited_basic_person_fourcc_count']}**.",
        f"- Top-20 manager/staff cards: **{cards_doc['summary']['decoded_count']}/20**; identity verified **{cards_doc['summary']['identity_verified']}/20**; CA/PA exact cross-check **{cards_doc['summary']['CA_exact_match']}/20 and {cards_doc['summary']['PA_exact_match']}/20**.",
        "",
        "## NON_PLAYER Own 4CC Map",
        "| 4CC | Property | Object Offset | Wire Offset | Width | GET Line | SET Line | Kind |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in attribute_doc["attributes"]:
        obj = f"`{item['obj_off_hex']}`" if item["obj_off"] is not None else "computed"
        wire = str(item["wire_off"]) if item["wire_off"] is not None else (
            ",".join(str(x) for x in item.get("wire_off_candidates", [])) or "-"
        )
        prop = item["attribute_name"].replace("|", "\\|")
        lines.append(f"| `{item['fourcc']}` | {prop} | {obj} | {wire} | {item['width'] or '-'} | {item['get_line'] or '-'} | {item['set_line'] or '-'} | {item['kind']} |")
    lines += [
        "",
        "### Inherited BASIC_PERSON Map",
        "| 4CC | Object Offset | Wire Offset | Width | Delegate GET | Delegate SET | Source Kind |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in attribute_doc["inherited_basic_person"]:
        obj = f"`{item['obj_off_hex']}`" if item["obj_off"] is not None else "computed/unresolved"
        wire = str(item["wire_off"]) if item["wire_off"] is not None else (",".join(map(str, item["wire_off_candidates"])) or "-")
        lines.append(f"| `{item['fourcc']}` | {obj} | {wire} | {item['width'] or '-'} | {item['get_line'] or '-'} | {item['set_line'] or '-'} | {item.get('access_kind') or '-'} |")
    lines += [
        "",
        "## Top-20 Highest-CA NON_PLAYER Cards",
        "| Rank | Name | UID | CA / PA | Attacking | Defending | Tactical | Judging Ability | Judging Potential | Man Management | Determination | Scalars In 0..20 |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for card in cards_doc["cards"]:
        attrs = card["attributes_by_fourcc"]
        def val(code: str) -> str:
            return str(attrs[code]) if code in attrs else "-"
        lines.append(
            f"| {card['rank']} | **{card['full_name']}** | {card['uid']} | {card['header']['CA']} / {card['header']['PA']} | "
            f"{val('Npat')} | {val('Npde')} | {val('Npta')} | {val('Npja')} | {val('Npjp')} | {val('Npmm')} | {val('Npdi')} | "
            f"{'PASS' if card['all_scalar_attributes_in_0_20'] else 'FAIL'} |"
        )
    lines += [
        "",
        "### Validation Notes",
        "- Scalar attributes are read from the per-record Unicorn wire trace. Fields with trace disagreement (`obj_off -19..-14`) keep their candidate wire positions in the map; per-card decoding uses that row's exact read map.",
        "- `NRCJ`, `NRLS`, `NSCR`, and `NTxx` are explicitly marked composite, computed, or dynamic-indexed; no single-byte location is asserted for them.",
        "- NON_PLAYER records begin with a u16 optional-tagged-field count and `count * 3` bytes; the following five i16 values contain home/current/world reputation, CA, and PA. CA/PA are checked against `basic_people_db.dat` u16 offsets +48 and +50.",
    ]
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_done(attribute_doc: dict, cards_doc: dict, selftest: str) -> None:
    s = attribute_doc["summary"]
    c = cards_doc["summary"]
    lines = [
        "DONE type=t137c",
        f"L3 attributes={s['l3_attributes']}",
        f"NON_PLAYER own 4CCs={s['own_fourcc_count']}",
        f"NTxx dynamic aliases={s['ntxx_dynamic_fourcc_count']}",
        f"inherited BASIC_PERSON 4CCs={s['inherited_basic_person_fourcc_count']}",
        f"verified managers={c['identity_verified']}/{c['decoded_count']}",
        f"CA cross-check={c['CA_exact_match']}/{c['decoded_count']}",
        f"PA cross-check={c['PA_exact_match']}/{c['decoded_count']}",
        f"scalar attributes 0..20={c['all_scalar_attributes_in_0_20']}/{c['decoded_count']}",
        f"--selftest {selftest}",
    ]
    (OUT_DIR / "DONE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def selftest() -> dict:
    required = [
        OUT_DIR / "non_player_attributes_l3.json",
        OUT_DIR / "top20_managers_cards.json",
        OUT_DIR / "REPORT.md",
    ]
    if not all(path.exists() for path in required):
        raise AssertionError("deliverables missing; run the default build before --selftest")
    attr_doc = read_json(required[0])
    card_doc = read_json(required[1])
    attrs = attr_doc["attributes"]
    by_code = {x["fourcc"]: x for x in attrs}
    assert len(attrs) >= 60, f"expected >=60 own/dynamic codes, got {len(attrs)}"
    assert all(x.get("get_line") for x in attrs), "some own codes lack GET evidence"
    assert all(x.get("set_line") for x in attrs if x["kind"] in ("scalar", "dynamic_indexed")), \
        "a scalar or dynamic alias lacks SET evidence"
    assert attr_doc["summary"]["ntxx_dispatch_code_count"] >= attr_doc["summary"]["ntxx_dynamic_fourcc_count"]
    assert attr_doc["summary"]["inherited_basic_person_fourcc_count"] >= 200
    for code in ("NRCJ", "NRLS", "NSCR"):
        assert code in by_code and by_code[code]["kind"] in ("computed", "composite")
    assert sum(1 for x in attrs if x["fourcc"].startswith("NT")) >= 40
    cards = card_doc["cards"]
    assert card_doc["status"] == "complete" and len(cards) == TOP_N
    assert len({c["uid"] for c in cards}) == TOP_N
    assert all(c["identity"]["dbid_equals_uid"] and c["identity"]["matches_basic_people"] for c in cards)
    assert all(c["basic_people_cross_check"]["CA_exact_match"] and c["basic_people_cross_check"]["PA_exact_match"] for c in cards)
    assert all(c["full_name"] and c["all_scalar_attributes_in_0_20"] and c["scalar_attribute_count"] for c in cards)
    return {"l3_attributes": attr_doc["summary"]["l3_attributes"], "own_fourccs": len(attrs),
            "ntxx_dynamic_aliases": attr_doc["summary"]["ntxx_dynamic_fourcc_count"],
            "ntxx_dispatch_codes": attr_doc["summary"]["ntxx_dispatch_code_count"],
            "inherited_fourccs": len(attr_doc["inherited_basic_person"]), "managers": len(cards),
            "ca_pa": "20/20", "scalar_attrs_per_card": card_doc["summary"]["scalar_attributes_per_card"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--uid", type=int)
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.selftest:
        stats = selftest()
        print(f"t137c --selftest PASS: L3={stats['l3_attributes']} own={stats['own_fourccs']} NTxx aliases={stats['ntxx_dynamic_aliases']}/{stats['ntxx_dispatch_codes']} inherited={stats['inherited_fourccs']} managers={stats['managers']} CA/PA={stats['ca_pa']} scalar/card={stats['scalar_attrs_per_card']}", flush=True)
        return 0

    t0 = time.time()
    attr_doc, wire_map = build_attribute_document()
    write_json(OUT_DIR / "non_player_attributes_l3.json", attr_doc)
    print(f"[stage] attribute map: own={attr_doc['summary']['own_fourcc_count']} NTxx={attr_doc['summary']['ntxx_dynamic_fourcc_count']} inherited={attr_doc['summary']['inherited_basic_person_fourcc_count']} L3={attr_doc['summary']['l3_attributes']}", flush=True)
    if args.uid is not None:
        result = build_top20(attr_doc, wire_map, uid=args.uid)
        print(json.dumps(result["uid_card"], ensure_ascii=False, indent=2), flush=True)
        return 0

    cards_doc = build_top20(attr_doc, wire_map)
    write_report(attr_doc, cards_doc)
    # The final completion marker is intentionally written only after all data and report validations.
    stats = selftest()
    write_done(attr_doc, cards_doc, "PASS")
    print(f"[stage] REPORT.md and DONE.md written in {time.time()-t0:.1f}s", flush=True)
    print("Deliverables: scratch/t137/out/non_player_attributes_l3.json, scratch/t137/out/top20_managers_cards.json, scratch/t137/out/REPORT.md, scratch/t137/out/DONE.md", flush=True)
    print(f"Core stats: L3 attributes={stats['l3_attributes']}; own 4CC={stats['own_fourccs']}; NTxx aliases={stats['ntxx_dynamic_aliases']}/{stats['ntxx_dispatch_codes']}; inherited={stats['inherited_fourccs']}; verified managers=20/20; CA/PA cross-check=20/20; scalar/card={stats['scalar_attrs_per_card']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
