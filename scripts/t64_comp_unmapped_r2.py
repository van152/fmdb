#!/usr/bin/env python3
"""t64: second-round bounded survey of unmapped COMP table_25 fields.

This is an evidence increment over t59. It does not rewrite t59 mappings and
never treats a getter projection as a wire binding.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
T59 = ROOT / "scratch" / "t59" / "out"
OUT = ROOT / "scratch" / "t64" / "out"
EXE = ROOT.parent / "fm24" / "input" / "editor.exe"
MASTER = ROOT / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
SAMPLES = ROOT / "evidence" / "fm24" / "reports" / "dbdat_decode" / "client_table_25_competition_samples.json"
MANIFEST = ROOT / "evidence" / "MANIFEST.json"
EXEH = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
MASTERH = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
SAMPLEH = "d4930a397c9452cf8a81b820d26e35775720ab23ba70eae3f1a7a0079a7af85a"
HEAD = bytes.fromhex("03017461642ef10d")
FOOT = bytes.fromhex("00000000014ec43a77")
SIDES = ("client", "server")
N = 7047


class Check(Exception):
    pass


def ck(ok: bool, detail: object) -> None:
    if not ok:
        raise Check(detail)


def H(data: bytes) -> str:
    return sha256(data).hexdigest()


def U(data: bytes, at: int = 0) -> int:
    return S.unpack_from("<I", data, at)[0]


def emit(name: str, value: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def manifest_check() -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_path = {x["path"]: x for x in manifest["files"]}
    checks = {}
    for path, expected in (
        ("evidence/fm24/reports/editor_schema/master.json", MASTERH),
        ("evidence/fm24/reports/dbdat_decode/client_table_25_competition_samples.json", SAMPLEH),
    ):
        entry = by_path.get(path)
        actual = H((ROOT / path).read_bytes())
        ck(entry is not None, ("manifest missing", path))
        ck(actual == expected == entry["sha256"], ("snapshot hash", path, actual, entry["sha256"]))
        checks[path] = {"sha256": actual, "bytes": (ROOT / path).stat().st_size}
    ck(manifest["snapshot_date"] == "2026-11-18", "unexpected evidence snapshot date")
    return {"snapshot_date": manifest["snapshot_date"], "files": checks}


def load_archives() -> tuple[dict[tuple[str, int], bytes], dict[str, object]]:
    depot = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch" / "data")))
    if depot.drive.upper() == "Z:":
        raise Check("Z: access is forbidden")
    old = ROOT.parent / "fm24"
    tools = old / "tools" / "python"
    if str(tools) not in sys.path:
        sys.path.append(str(tools))
    import zstandard as zstd

    entries = runpy.run_path(str(old / "scripts" / "modding_read_dbdat.py"))["_entries"]
    raw: dict[tuple[str, int], bytes] = {}
    meta: dict[str, object] = {}
    for side in SIDES:
        _, blob, directory = entries(depot / f"{side}_db.dat")
        base = directory["data_base"]
        index = {entry["path"]: entry for entry in directory["entries"]}
        ck(base == 34, (side, "data_base", base))
        name = f"{side}_db/table_25.dat"
        entry = index[name]
        start = base + entry["offset"]
        finish = start + entry["packed_size"]
        bound = min(
            (base + x["offset"] for x in index.values() if x["offset"] > entry["offset"]),
            default=directory["toc_offset"],
        )
        ck(base <= start < finish <= bound, (side, "table range"))
        frames = []
        candidates = []
        p = start
        while p < finish:
            ck(blob[p : p + 4] == b"\x28\xb5\x2f\xfd", (side, "zstd magic", p))
            dec = zstd.ZstdDecompressor().decompressobj()
            payload = dec.decompress(blob[p:finish])
            q = finish - len(dec.unused_data)
            ck(dec.eof and q > p, (side, "zstd frame", p))
            frames.append([p, q, len(payload)])
            if len(payload) == entry["size"]:
                candidates.append(payload)
            p = q
        ck(len(candidates) == 1, (side, "declared-size frame selector"))
        payload = candidates[0]
        ck(payload[:8] == HEAD and U(payload, 8) == N, (side, "table header"))
        raw[side, 25] = payload
        meta[side] = {
            "member": name,
            "compressed_range": [start, finish],
            "frames": frames,
            "declared_size": entry["size"],
            "payload_sha256": H(payload),
            "compressed_sha256": H(blob[start:finish]),
            "count": U(payload, 8),
        }
    return raw, meta


class Cursor:
    def __init__(self, payload: bytes, side: str):
        self.payload = payload
        self.side = side
        self.p = 13
        self.end = len(payload) - len(FOOT)
        self.row = -1

    def take(self, width: int, label: str) -> bytes:
        ck(width >= 0 and self.p + width <= self.end, (self.side, self.row, label, self.p, width))
        out = self.payload[self.p : self.p + width]
        self.p += width
        return out

    def u(self, width: int, label: str) -> int:
        return int.from_bytes(self.take(width, label), "little", signed=False)

    def s(self, width: int, label: str) -> int:
        return int.from_bytes(self.take(width, label), "little", signed=True)

    def count(self, width: int, unit: int, label: str, signed: bool = False) -> int:
        n = self.s(width, label) if signed else self.u(width, label)
        ck(0 <= n <= (self.end - self.p) // unit, (self.side, self.row, label, "invalid count", n))
        return n


def parse_table25(payload: bytes, side: str) -> dict[str, object]:
    """Parse only the native main-row envelope and count optional payloads.

    The parser intentionally does not assign XML fields. It is an independent
    framing check for the two static payload entry conditions and their sibling
    extension spans.
    """
    c = Cursor(payload, side)
    events: dict[str, list[tuple[int, int, int]]] = {}
    values: dict[str, list[tuple[int, int]]] = {}
    rows = []

    def record(key: str, start: int, finish: int, value: int | None = None) -> None:
        events.setdefault(key, []).append((c.row, start, finish - start))
        if value is not None:
            values.setdefault(key, []).append((c.row, value))

    def take(key: str, width: int) -> int:
        start = c.p
        value = c.u(width, key)
        record(key, start, c.p, value)
        return value

    def raw(key: str, width: int) -> None:
        start = c.p
        c.take(width, key)
        record(key, start, c.p)

    for row in range(N):
        c.row = row
        row_start = c.p
        selector = take("selector", 1)
        m15c = take("m15c", 1)
        m15d = take("m15d", 1)
        colour_tag = take("colour_tag", 1)
        for key in ("m120", "m124", "m128", "m12c", "m130"):
            take(key, 2)
        take("m134", 1)
        m1a0 = take("m1a0", 1)
        for key in ("m1a2", "m1a3", "m1a4", "m1a5"):
            take(key, 1)
        stat_a = take("stat_a_tag", 1)
        for key in ("m198", "m199", "m19a", "m19b", "m19c", "m19d", "m19e"):
            take(key, 1)
        stat_b = take("stat_b_tag", 1)
        raw("m189_197", 15)
        take("mf6", 1)
        for key in ("m138", "m13c", "m58", "m60", "m70", "m68"):
            take(key, 4)
        take("m150", 2)
        ck((selector, m15c, m15d, colour_tag, stat_a, stat_b) == (0, 0, 0, 1, 2, 3),
           (side, row, "fixed tags"))
        ck(m1a0 != 4, (side, row, "inline-name tag-4 alternative"))

        if side == "server":
            for key, width in (("m180", 2), ("mb8", 4), ("m188", 1), ("m184", 2),
                               ("m186", 2), ("m182", 2), ("m160", 8), ("m168", 8),
                               ("m170", 8), ("m178", 8)):
                take(key, width)
            start = c.p
            n = c.count(4, 2, "vec30-count")
            c.take(2 * n, "vec30-body")
            record("vec30", start, c.p)

            a8_present = take("a8_present", 1)
            if a8_present:
                start = c.p
                version = c.u(1, "a8-version")
                c.take(32 + 4 * (version >= 2) + 9 + (2 if version >= 3 else 1) + 4 + 4, "obj_a8-body")
                record("obj_a8", start, c.p)

            for key, width in (("mf0", 4), ("m1a1", 1), ("m1a8", 1), ("mf4", 1), ("mf5", 1)):
                take(key, width)

            e0_present = take("e0_present", 1)
            if e0_present:
                # The data set has no e0 object. A nonzero object requires a
                # dedicated type-erased grammar and is deliberately not guessed.
                raise Check((side, row, "nonzero e0 payload outside t64 scope"))

            start = c.p
            vec18_n = c.count(4, 8, "vec18-count", signed=True)
            for item in range(vec18_n):
                version = c.s(1, f"vec18[{item}]-version")
                c.take(7 + (version >= 2), f"vec18[{item}]-body")
            record("vec18", start, c.p)

            e8_present = take("e8_present", 1)
            if e8_present:
                start = c.p
                c.take(4, "obj_e8-header")
                n = c.count(4, 8, "obj_e8-count")
                for item in range(n):
                    version = c.s(2, f"obj_e8[{item}]-version")
                    c.take(6 + (2 if version >= 2 else 1) + 1 + (version >= 3), f"obj_e8[{item}]-body")
                record("obj_e8", start, c.p)

            c0_present = take("c0_present", 1)
            if c0_present:
                start = c.p
                c.take(1, "obj_c0-header")
                n = c.count(4, 6, "obj_c0-count")
                for item in range(n):
                    c.take(2, f"obj_c0[{item}]-header")
                    subn = c.count(4, 12, f"obj_c0[{item}]-count")
                    c.take(12 * subn, f"obj_c0[{item}]-body")
                record("obj_c0", start, c.p)

            c8_present = take("c8_present", 1)
            if c8_present:
                raw("obj_c8", 25)
            take("m1a7", 1)
            d0_present = take("d0_present", 1)
            if d0_present:
                raw("obj_d0", 15)
            d8_present = take("d8_present", 1)
            if d8_present:
                raw("obj_d8", 15)
            start = c.p
            n = c.s(2, "vec100-count")
            ck(n >= 0 and n <= (c.end - c.p) // 5, (side, row, "vec100 count", n))
            c.take(5 * n, "vec100-body")
            record("vec100", start, c.p)

        for key, width in (("m148", 4), ("m152", 2), ("m154", 2), ("m156", 2),
                           ("m158", 2), ("m15a", 2), ("m80", 4), ("m88", 4),
                           ("m90", 4), ("m98", 4)):
            take(key, width)
        wbcl = take("wbcl_present", 1)
        if wbcl:
            raw("m14c", 2)
        for key, width in (("m140", 4), ("m144", 4), ("mf7", 1), ("mf8", 1), ("mf9", 1)):
            take(key, width)
        identity_start = c.p
        row_id = c.u(4, "identity-row")
        uid = c.u(4, "identity-uid")
        repeat = c.u(4, "identity-repeat")
        record("identity", identity_start, c.p)
        ck((row_id, uid, repeat) == (row, uid, uid) and uid > (rows[-1][2] if rows else 0),
           (side, row, "identity", row_id, uid, repeat))
        rows.append((row_start, c.p, uid))

    ck(payload[c.p:] == FOOT, (side, "footer", c.p, payload[c.p : c.p + 9].hex()))
    return {"rows": rows, "events": events, "values": values, "end": c.p}


def instruction_record(pe, md, file_offset: int) -> dict[str, object]:
    va = pe.f2va(file_offset)
    ins = next(md.disasm(pe.raw[file_offset : file_offset + 15], va, 1))
    result = {
        "file_offset": file_offset,
        "va": hex(ins.address),
        "bytes": pe.raw[file_offset : file_offset + ins.size].hex(),
        "instruction": (ins.mnemonic + " " + ins.op_str).strip(),
    }
    if ins.operands and ins.operands[0].type == 2 and ins.mnemonic in ("call", "jmp", "je", "jne", "jl", "jle", "jg", "ja", "jae", "jb", "jbe"):
        result["direct_target_va"] = hex(ins.operands[0].imm)
        target = pe.va2f(ins.operands[0].imm)
        result["direct_target_file_offset"] = target
    return result


def code_from_imm(value: int) -> str | None:
    if not 0 <= value < (1 << 32):
        return None
    try:
        code = value.to_bytes(4, "big").decode("ascii")
    except UnicodeDecodeError:
        return None
    return code if all(32 <= ord(ch) < 127 for ch in code) else None


def static_scan():
    from capstone import CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM, Cs

    sys.path.insert(0, str(ROOT / "scripts"))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG

    pe = PE(EXE)
    ck(H(pe.raw) == EXEH, ("editor.exe sha256", H(pe.raw)))
    pe.pe.parse_data_directories(directories=[3])
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def root_scan(root: int) -> dict[str, object]:
        graph = ReaderCFG(pe, md, root)
        code_sites: dict[str, list[dict[str, object]]] = {}
        direct_calls = []
        helper_calls = []
        for va, ins in sorted(graph.instructions.items()):
            off = pe.va2f(va)
            if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == CS_OP_MEM and ins.operands[0].mem.disp == 0x28:
                direct_calls.append(off)
            elif ins.mnemonic == "call" and ins.operands and ins.operands[0].type == CS_OP_IMM:
                target_va = ins.operands[0].imm
                helper_calls.append({
                    "site": off,
                    "target_va": hex(target_va),
                    "target_file_offset": pe.va2f(target_va),
                })
            if ins.mnemonic != "cmp":
                continue
            for operand in ins.operands:
                if operand.type != CS_OP_IMM:
                    continue
                code = code_from_imm(operand.imm)
                if code is None:
                    continue
                nxt = graph.instructions.get(va + ins.size)
                equality_target = None
                if nxt is not None and nxt.mnemonic == "je":
                    equality_target = pe.va2f(nxt.operands[0].imm)
                elif nxt is not None and nxt.mnemonic == "jne":
                    equality_target = pe.va2f(nxt.address + nxt.size)
                code_sites.setdefault(code, []).append({
                    "compare": instruction_record(pe, md, off),
                    "equality_target_file_offset": equality_target,
                    "equality_target_va": None if equality_target is None else hex(pe.f2va(equality_target)),
                })
        return {
            "root_file_offset": root,
            "root_va": hex(pe.f2va(root)),
            "end_exclusive": graph.function_end_off,
            "reachable": len(graph.instructions),
            "conditional_branches": sum(1 for va in graph.instructions if graph.instructions[va].mnemonic.startswith("j") and graph.instructions[va].mnemonic != "jmp"),
            "code_sites": code_sites,
            "direct_stream_calls": direct_calls,
            "direct_helper_calls": helper_calls,
        }

    roots = {
        "main_reader": 0xEB7000,
        "comp_getter": 0xEC0060,
        "slot5_getter": 0xEBF040,
    }
    scans = {name: root_scan(root) for name, root in roots.items()}
    return pe, md, scans


def static_payloads(pe, md, replay: dict[str, dict[str, object]]) -> dict[str, object]:
    def direct_target(file_offset: int) -> int | None:
        from capstone import CS_OP_IMM
        ins = next(md.disasm(pe.raw[file_offset : file_offset + 15], pe.f2va(file_offset), 1))
        if ins.operands and ins.operands[0].type == CS_OP_IMM:
            return pe.va2f(ins.operands[0].imm)
        return None

    def record(file_offset: int) -> dict[str, object]:
        return instruction_record(pe, md, file_offset)

    def data_summary(presence: str, obj: str) -> dict[str, object]:
        result = {}
        for side in SIDES:
            events = replay[side]["events"]
            values = replay[side]["values"]
            present_values = [v for _, v in values.get(presence, [])]
            result[side] = {
                "presence_events": len(events.get(presence, [])),
                "presence_nonzero": sum(v != 0 for v in present_values),
                "presence_values": Counter(map(str, present_values)),
                "object_events": len(events.get(obj, [])),
            }
        return result

    return {
        "a8": {
            "member_offset": 0xA8,
            "presence_read": record(0xEB7532),
            "presence_test": record(0xEB753F),
            "skip_target": record(0xEB7544),
            "allocator": record(0xEB754A),
            "member_store": record(0xEB75BD),
            "reader": record(0xEB75CA),
            "data": data_summary("a8_present", "obj_a8"),
            "entry_condition": "presence byte at [rsp+0x5f] != 0",
            "conclusion": "static payload exists; no payload object is entered in either table_25 sample",
        },
        "e0": {
            "member_offset": 0xE0,
            "presence_read": record(0xEB76C0),
            "presence_test": record(0xEB76CD),
            "skip_target": record(0xEB76D2),
            "allocator": record(0xEB76D9),
            "constructor": record(0xEB76E4),
            "member_store": record(0xEB76E9),
            "reader": record(0xEB76FB),
            "data": data_summary("e0_present", "obj_e0"),
            "entry_condition": "presence byte at [rsp+0x5e] != 0",
            "conclusion": "static payload exists; no payload object is entered in either table_25 sample",
        },
    }


def static_routes(scans: dict[str, object], pe, md, replay, base: dict[str, object]) -> dict[str, object]:
    getter = scans["comp_getter"]
    slot5 = scans["slot5_getter"]

    def table_case(table_file_offset: int, index: int, expected_target: int) -> dict[str, object]:
        entry = table_file_offset + 4 * index
        rel = int.from_bytes(pe.raw[entry : entry + 4], "little", signed=True)
        target_va = pe.f2va(table_file_offset) + rel
        target_file_offset = pe.va2f(target_va)
        ck(target_file_offset == expected_target, ("rules jump-table target", hex(entry), target_file_offset, expected_target))
        return {
            "entry_file_offset": entry,
            "relative_value": rel,
            "handler_file_offset": target_file_offset,
            "handler": instruction_record(pe, md, target_file_offset),
        }

    def string_getter_path(code: str, expected_member: int, member_add_site: int | None = None) -> dict[str, object]:
        sites = getter["code_sites"].get(code, [])
        ck(len(sites) == 1, ("string getter compare count", code, len(sites)))
        site = sites[0]
        equality_entry = site["equality_target_file_offset"]
        ck(isinstance(equality_entry, int), ("string getter target", code, site))
        member_site = equality_entry if member_add_site is None else member_add_site
        target_record = instruction_record(pe, md, member_site)
        ck(target_record["instruction"] == f"add r12, 0x{expected_member:x}", (code, target_record))
        return {
            "compare": site["compare"],
            "equality_path_entry_file_offset": equality_entry,
            "equality_path_entry_va": site["equality_target_va"],
            "member_add": target_record,
            "member_offset": expected_member,
            "status": "getter_member_candidate_only; no main-row string wire transfer proved; t59 held status unchanged",
        }

    def nested_family(prefix: str, base_imm: int, table: int, handlers: dict[int, int]) -> dict[str, object]:
        codes = {index: code_from_imm(base_imm + index) for index in (0, 9, 15, 16, 18)}
        ck(all(code == prefix + suffix for code, suffix in zip(codes.values(), ("d", "m", "s", "t", "v"))), (prefix, codes))
        return {
            "table_file_offset": table,
            "base_code": codes[0],
            "cases": [
                {"code": codes[index], "index": index, **table_case(table, index, target)}
                for index, target in sorted(handlers.items())
            ],
        }

    hke_table = 0xEB5AB4
    var_table = 0xEB5A68
    hke_cases = nested_family("HKE", 0x484B4564, hke_table, {0: 0xEB5787, 9: 0xEB5822, 15: 0xEB5837, 16: 0xEB570B, 18: 0xEB5866})
    var_cases = nested_family("VAR", 0x56415264, var_table, {0: 0xEB5787, 9: 0xEB5822, 15: 0xEB5837, 16: 0xEB58C2, 18: 0xEB5866})
    held = {x["code"]: x for x in base["fields"] if x["status"] == "held"}
    tag4 = {}
    for side in SIDES:
        vals = [value for _, value in replay[side]["values"].get("m1a0", [])]
        tag4[side] = {"rows": len(vals), "tag4_rows": sum(value == 4 for value in vals)}

    return {
        "bounded_roots": {
            "main_reader": {k: scans["main_reader"][k] for k in ("root_file_offset", "root_va", "end_exclusive", "reachable", "conditional_branches")},
            "comp_getter": {k: getter[k] for k in ("root_file_offset", "root_va", "end_exclusive", "reachable", "conditional_branches")},
            "slot5_getter": {k: slot5[k] for k in ("root_file_offset", "root_va", "end_exclusive", "reachable", "conditional_branches")},
        },
        "field_code_site_counts": {
            "comp_getter": {code: len(sites) for code, sites in getter["code_sites"].items()},
            "slot5_getter": {code: len(sites) for code, sites in slot5["code_sites"].items()},
        },
        "rules_context_chain": {
            "VARt": {
                "baseline_status": held["VARt"]["status"],
                "row_object_load": instruction_record(pe, md, 0xEC04A8),
                "field_code_compare": instruction_record(pe, md, 0xEC04B0),
                "code_mismatch_branch": instruction_record(pe, md, 0xEC04B6),
                "object_null_test": instruction_record(pe, md, 0xEC04BC),
                "object_nonnull_branch": instruction_record(pe, md, 0xEC04BF),
                "context_dispatch_sequence": [instruction_record(pe, md, x) for x in (0xEC1830, 0xEC183A, 0xEC1843, 0xEC1846, 0xEC184E, 0xEC1852, 0xEC1862, 0xEC186B)],
                "same_comp_scalar_wire_binding_proved": False,
            },
            "HKEt": {
                "baseline_status": held["HKEt"]["status"],
                "row_object_load": instruction_record(pe, md, 0xEC0880),
                "field_code_compare": instruction_record(pe, md, 0xEC0888),
                "code_mismatch_branch": instruction_record(pe, md, 0xEC088E),
                "object_null_test": instruction_record(pe, md, 0xEC0894),
                "object_nonnull_branch": instruction_record(pe, md, 0xEC0897),
                "context_dispatch_sequence": [instruction_record(pe, md, x) for x in (0xEC1830, 0xEC183A, 0xEC1843, 0xEC1846, 0xEC184E, 0xEC1852, 0xEC1862, 0xEC186B)],
                "same_comp_scalar_wire_binding_proved": False,
            },
            "separate_nested_rules_dispatch": {
                "shared_entry": [instruction_record(pe, md, x) for x in (0xEC0E30, 0xEC0E33, 0xEC0E39, 0xEC0E58)],
                "nested_helper_entry": instruction_record(pe, md, 0xEB56C0),
                "jump_table_families": {"VAR": var_cases, "HKE": hke_cases},
                "direct_successor_from_VARt_HKEt_compare_asserted": False,
            },
            "first_counterchain": [
                "the VARt/HKEt compare blocks load COMP+0xd0/+0xd8, then test the matching field code and loaded pointer",
                "for a matching code with a non-null object, the branch reaches file offset 0xec1830; nonmatching codes also enter that shared context path",
                "0xec1830 reads and compares context-object +0xc0/+0xc8, calls helper VA 0x140eba600, and continues through shared context checks; this is not a same-row scalar wire transfer",
                "0xec0e30 -> 0xeb56c0 is a separate nested-rules dispatch arm and is not asserted as the direct successor of these compare blocks",
            ],
            "falsification_checklist": [
                "identify a main-row stream transfer into a distinct same-COMP scalar member for VARt/HKEt",
                "prove the corresponding getter consumes that scalar rather than branching on COMP+0xd0/+0xd8 object state",
                "reconcile optional +0xd0/+0xd8 objects across all 7,047 rows and validate the complete field domain",
            ],
            "data_boundary": {"d0_server_presence": 121, "d8_server_presence": 51, "rows_per_archive": N, "field_domain_gate_passed": False},
        },
        "string_getter_paths": {
            "cnam": string_getter_path("cnam", 0x40),
            "csnm": string_getter_path("csnm", 0x48, 0xEC1024),
            "c3ln": string_getter_path("c3ln", 0x50),
            "inline_tag4_path": {
                "tag_test": instruction_record(pe, md, 0xEB71B9),
                "name_reader_offsets": [0x48, 0x40],
                "m1a0_data": tag4,
                "first_t59_counterexamples": {code: held[code]["first_counterexample"] for code in ("cnam", "csnm", "c3ln")},
            },
            "bounded_root_scope": "main_reader + COMP getter + slot-5 getter only; derived collection roots are not read or scanned by t64",
        },
    }


def direct_stream_accounting(scans: dict[str, object], field_slots: dict[str, object], base: dict[str, object], pe, md) -> dict[str, object]:
    slots = field_slots["slots"]
    slot_by_site = {int(x["site"]): x for x in slots if isinstance(x.get("site"), int)}
    slot_by_offset = {x.get("object_offset"): x for x in slots if x.get("object_offset") is not None}
    fields_by_xml = {x["xml_index"]: x for x in base["fields"]}

    def consumers(slot):
        if not slot:
            return []
        result = []
        for xml_index in slot.get("xml_indices", []):
            field = fields_by_xml.get(xml_index)
            if field:
                result.append({"xml_index": xml_index, "code": field["code"], "baseline_status": field["status"]})
        return result

    alternate = {
        0xEB7218: {
            "destination_offset": 0x58,
            "classification": "tag4_alternate_reference_dispatch_same_m58_member",
            "raw_value_range": [2, 7],
            "dispatch_index_range": [1, 6],
            "dispatch_branch_file_offset": 0xEB7254,
        },
        0xEB72F8: {
            "destination_offset": 0x60,
            "classification": "tag4_alternate_reference_resolver_same_m60_member",
            "helper_file_offset": 0x55EB0,
        },
        0xEB7332: {
            "destination_offset": 0x68,
            "classification": "tag4_alternate_reference_resolver_same_m68_member",
            "helper_file_offset": 0xF453B0,
        },
    }
    entries = []
    for site in scans["main_reader"]["direct_stream_calls"]:
        if site in alternate:
            alt = alternate[site]
            slot = slot_by_offset.get(alt["destination_offset"])
            item = {"site": site, "kind": "alternate", **alt,
                    "existing_slot": None if slot is None else slot["key"],
                    "xml_consumers": consumers(slot)}
        else:
            slot = slot_by_site.get(site)
            item = {"site": site, "kind": "outer_slot", "slot": None if slot is None else slot["key"],
                    "object_offset": None if slot is None else slot.get("object_offset"),
                    "xml_consumers": consumers(slot)}
        item["call_instruction"] = instruction_record(pe, md, site)
        entries.append(item)
    outer = [x for x in entries if x["kind"] == "outer_slot"]
    return {
        "direct_call_count": len(entries),
        "outer_observed_call_count": len(outer),
        "alternate_call_count": len(entries) - len(outer),
        "calls": entries,
        "unmapped_new_direct_calls": [],
        "interpretation": "the three tag4 calls feed existing m58/m60/m68 slots; their XML consumers are inherited from t59, not new wire bindings",
    }


def helper_call_accounting(scans: dict[str, object], field_slots: dict[str, object], base: dict[str, object], pe, md) -> dict[str, object]:
    slots = field_slots["slots"]
    slot_by_site = {int(x["site"]): x for x in slots if isinstance(x.get("site"), int)}
    slot_by_offset = {x.get("object_offset"): x for x in slots if x.get("object_offset") is not None}
    fields_by_xml = {x["xml_index"]: x for x in base["fields"]}

    def consumers(slot):
        if not slot:
            return []
        return [
            {"xml_index": i, "code": fields_by_xml[i]["code"], "baseline_status": fields_by_xml[i]["status"]}
            for i in slot.get("xml_indices", []) if i in fields_by_xml
        ]

    alternate_destination = {0xEB7311: 0x60, 0xEB734B: 0x68}
    payload_sites = {
        0xEB754A: ("+0xa8 payload allocator/initializer", 0xA8),
        0xEB75CA: ("+0xa8 payload reader", 0xA8),
        0xEB76D9: ("+0xe0 payload allocator", 0xE0),
        0xEB76E4: ("+0xe0 payload constructor", 0xE0),
        0xEB76FB: ("+0xe0 payload reader", 0xE0),
    }
    string_sites = {
        0xEB71CB: 0x48,
        0xEB71E7: 0x40,
    }
    related_rules = {
        0xEB78F2: {"object_offset": 0xD0, "field_family": ["VARt", "VARv", "VARm", "VARs", "VARd"]},
        0xEB7961: {"object_offset": 0xD8, "field_family": ["HKEt", "HKEv", "HKEm", "HKEs", "HKEd"]},
    }

    calls = []
    for raw in scans["main_reader"]["direct_helper_calls"]:
        site = raw["site"]
        slot = slot_by_site.get(site)
        item = {**raw, "call_instruction": instruction_record(pe, md, site), "xml_consumers": consumers(slot), "classification": "opaque_helper_no_field_consumer_proved", "field_mapping_status": "unmapped_no_member_or_xml_consumer_proved"}
        if site in string_sites:
            item.update({
                "classification": "tag4_name_string_reader_candidate",
                "member_offset": string_sites[site],
                "candidate_xml_fields": ["cnam", "csnm", "c3ln"],
                "wire_binding_asserted": False,
                "field_mapping_status": "candidate_only; main-row wire transfer not proved",
            })
        elif site in alternate_destination:
            dest = alternate_destination[site]
            target_slot = slot_by_offset.get(dest)
            item.update({
                "classification": "alternate_reference_object_resolver",
                "destination_offset": dest,
                "destination_slot": None if target_slot is None else target_slot["key"],
                "xml_consumers": consumers(target_slot),
                "field_mapping_status": "existing slot consumer; no new field mapping",
            })
        elif site in related_rules:
            item.update({
                "classification": "optional_nested_rules_object_reader",
                "nested_object": related_rules[site],
                "xml_consumers": [],
                "field_mapping_status": "held/unmapped family retained; no per-field wire binding asserted",
            })
        elif site in payload_sites:
            label, member = payload_sites[site]
            item.update({
                "classification": "conditional_payload_helper",
                "role": label,
                "member_offset": member,
                "xml_consumers": [],
                "observed_entry_count": 0,
                "field_mapping_status": "conditional optional payload; not an XML field occurrence",
            })
        elif slot:
            item.update({
                "slot": slot["key"],
                "member_offset": slot.get("object_offset"),
                "classification": "existing_slot_helper" if consumers(slot) else "unmapped_slot_helper",
                "field_mapping_status": "existing slot consumer" if consumers(slot) else "unmapped; no XML occurrence on this member",
            })
        calls.append(item)

    return {
        "direct_non_stream_call_count": len(calls),
        "calls": calls,
        "unmapped_slot_helpers": [x["site"] for x in calls if x["classification"] == "unmapped_slot_helper"],
        "opaque_helper_sites": [x["site"] for x in calls if x["classification"] == "opaque_helper_no_field_consumer_proved"],
        "method": "every reachable direct immediate call in the bounded main-reader CFG is listed; indirect stream+0x28 calls are in the separate main-reader ledger",
    }


def route_for_field(field: dict[str, object], scans: dict[str, object]) -> tuple[str, str, dict[str, object]]:
    code = field["code"]
    main_codes = scans["comp_getter"]["code_sites"]
    slot5_codes = scans["slot5_getter"]["code_sites"]
    if code in slot5_codes:
        return "slot5_context_out_of_scope", "slot-5 getter registration/context path; no main-row scalar transfer", {
            "falsification": "prove a table_25 main reader transfer to the field's same-object member",
        }
    if code == "WpBn":
        return "projection_candidate", "getter computes Band from held +0xf4 state; not a raw wire binding", {
            "candidate_dependency": {"object_offset": 0xF4, "same_slot": "mf4", "helper": 0xEC9C30, "post_operation": "result + 1"},
            "falsification": "show direct returned value equals the main-row byte for all relevant states and exclude the helper/gate",
        }
    if code == "IsAC":
        return "derived_parent_or_global_state", "equal path returns a derived boolean without a same-COMP wire load", {
            "falsification": "trace the shared return into a main-row member transfer",
        }
    if code in {"cmtc", "nytc"}:
        return "derived_count", "count is selected from an external/context table using COMP +0x8 as an index", {
            "member_observed": {"object_offset": 8, "use": "index only"},
            "falsification": "find a direct stream transfer to COMP +0x8 and separate it from the external count table",
        }
    if code in {"CTMS", "CNTM", "OTMS", "NSOD", "CRtm"}:
        return "derived_list_or_shared_handler", "list/debug view is routed to a shared handler; no main-row scalar binding", {
            "falsification": "decode the shared list handler and prove a main-row scalar wire lane",
        }
    if code in {"HKEv", "HKEm", "HKEs", "HKEd"}:
        return "rules_context_sibling", "goal-line fields belong to the +0xd8 rules/context family", {
            "falsification": "prove a main-row scalar transfer independent of the +0xd8 rules object",
        }
    if code in {"EFBR", "HsAR", "NoBR", "AXML"}:
        return "advanced_rules_or_debug", "advanced-rules/debug field has no literal case in the bounded COMP roots", {
            "falsification": "decode its range/helper dispatch and connect it to a main-row wire transfer",
        }
    if code in main_codes:
        return "bounded_getter_without_wire_closure", "literal getter compare exists, but t64 found no new main-reader wire closure", {
            "falsification": "prove an additional main-reader transfer and same-object getter member path",
        }
    return "no_bounded_comp_getter_case", "no literal 4CC compare in the two bounded COMP getter roots", {
        "falsification": "follow range dispatch or helper roots outside the bounded scan before claiming absence",
    }


def build_field_map(base: dict[str, object], scans: dict[str, object], direct: dict[str, object], manifest: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    fields = []
    exclusions = []
    for original in base["fields"]:
        if original["status"] != "unmapped":
            continue
        classification, reason, extra = route_for_field(original, scans)
        code = original["code"]
        roots = []
        for root_name in ("comp_getter", "slot5_getter"):
            sites = scans[root_name]["code_sites"].get(code, [])
            if sites:
                roots.append({"root": root_name, "sites": sites})
        item = {
            "xml_index": original["xml_index"],
            "code": code,
            "schema": original["schema"],
            "baseline_status": original["status"],
            "r2_status": "candidate" if classification == "projection_candidate" else "unmapped",
            "classification": classification,
            "wire_binding": None,
            "bounded_root_presence": roots,
            "reason": reason,
            "falsification": extra.pop("falsification"),
        }
        item.update(extra)
        fields.append(item)
        exclusions.append({
            "xml_index": original["xml_index"],
            "code": code,
            "classification": classification,
            "reason": reason,
            "falsification": item["falsification"],
            "bounded_roots": [x["root"] for x in roots],
        })
    ck(len(fields) == base["summary"]["unmapped"] == 196, ("unmapped occurrence count", len(fields)))
    r2 = {
        "status": "t64_evidence_increment",
        "scope": "COMP table_25 main row only; t59 L3/held map is frozen",
        "baseline": {
            "path": "scratch/t59/out/field_map.json",
            "sha256": H((T59 / "field_map.json").read_bytes()),
            "summary": base["summary"],
            "inversion_count": len(base["inversions"]),
        },
        "provenance": {
            "editor_sha256": EXEH,
            "master_sha256": MASTERH,
            "evidence_manifest": manifest,
            "coordinates": "PE file offsets unless a va field is explicitly present",
        },
        "summary": {
            "reviewed_unmapped_occurrences": len(fields),
            "r2_candidates": sum(x["r2_status"] == "candidate" for x in fields),
            "new_L3": 0,
            "baseline_L3_unchanged": True,
            "baseline_held_unchanged": True,
            "baseline_inversions_unchanged": True,
            "bounded_main_getter_literal_occurrences": sum(bool(x["bounded_root_presence"]) and any(r["root"] == "comp_getter" for r in x["bounded_root_presence"]) for x in fields),
            "no_main_or_slot5_literal_occurrences": sum(not any(r["root"] in {"comp_getter", "slot5_getter"} for r in x["bounded_root_presence"]) for x in fields),
        },
        "fields": fields,
    }
    ex = {
        "status": "t64_negative_and_boundary_ledger",
        "scope": r2["scope"],
        "baseline_field_map_sha256": r2["baseline"]["sha256"],
        "categories": dict(sorted(Counter(x["classification"] for x in exclusions).items())),
        "fields": exclusions,
        "payload_boundary": {
            "a8": "static entry exists; data presence byte is zero for all server rows and absent from client mode",
            "e0": "static entry exists; data presence byte is zero for all server rows and absent from client mode",
            "d0_d8": "not conflated with a8/e0; server presence counts are recorded in helpers.json",
        },
    }
    return r2, ex


def make_helpers(base: dict[str, object], scans, direct, helper_calls, payloads, archive_meta, replay, manifest, pe, md) -> dict[str, object]:
    data = {}
    for side in SIDES:
        events = replay[side]["events"]
        values = replay[side]["values"]
        data[side] = {
            "payload_sha256": archive_meta[side]["payload_sha256"],
            "row_count": len(replay[side]["rows"]),
            "presence": {
                key: {
                    "events": len(events.get(key, [])),
                    "nonzero": sum(value != 0 for _, value in values.get(key, [])),
                }
                for key in ("a8_present", "e0_present", "d0_present", "d8_present")
            },
            "object_events": {key: len(events.get(key, [])) for key in ("obj_a8", "obj_e0", "obj_d0", "obj_d8")},
        }
    return {
        "status": "t64_helper_and_branch_ledger",
        "provenance": {
            "editor_sha256": EXEH,
            "master_sha256": MASTERH,
            "evidence_manifest": manifest,
            "baseline_field_map_sha256": H((T59 / "field_map.json").read_bytes()),
        },
        "main_reader": {
            "root_file_offset": 0xEB7000,
            "scope_extent": [0xEB7000, 0xEB7E42],
            "direct_stream_call_accounting": direct,
            "direct_helper_call_accounting": helper_calls,
            "alternate_reference_path": {
                "tag_test": 0xEB71B9,
                "tag_value": 4,
                "name_reader_calls": [
                    {"site": 0xEB71CB, "target_file_offset": 0x814110, "member_offset": 0x48},
                    {"site": 0xEB71E7, "target_file_offset": 0x814110, "member_offset": 0x40},
                ],
                "flag_test": 0xEB71FF,
                "flag_provenance": "local flag at [rsp+0xf8]; no stronger source claim",
                "scalar_reads": [
                    {"site": 0xEB7218, "width": 4, "destination_offset": 0x58, "dispatch": 0xEB7CE0},
                    {"site": 0xEB72F8, "width": 4, "destination_offset": 0x60, "helper_file_offset": 0x55EB0},
                    {"site": 0xEB7332, "width": 4, "destination_offset": 0x68, "helper_file_offset": 0xF453B0},
                ],
                "conclusion": "same m58/m60/m68 slots; no new XML binding",
            },
            "payload_entry_conditions": payloads,
        },
        "bounded_getter_routes": static_routes(scans, pe, md, replay, base),
        "data_replay": data,
        "scope_boundary": {
            "derived_collections": "not read or scanned by t64; no t66 output imported",
            "rules_objects": "+0xd0/+0xd8 are distinct optional nested context objects; they are not conflated with the +0xa8/+0xe0 static-zero pair",
        },
    }


def verifier_source() -> str:
    return textwrap.dedent(r'''#!/usr/bin/env python3
"""Independent t64 verifier: frozen ledger checks plus a fresh table_25 replay."""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch" / "t64" / "out"
EXE = ROOT.parent / "fm24" / "input" / "editor.exe"
EXEH = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
HEAD = bytes.fromhex("03017461642ef10d")
FOOT = bytes.fromhex("00000000014ec43a77")
SIDES = ("client", "server")
N = 7047

class Check(Exception): pass

def ck(ok, detail):
    if not ok: raise Check(detail)

def H(b): return sha256(b).hexdigest()
def verify_instruction(record, binary):
    off=record["file_offset"]; raw=bytes.fromhex(record["bytes"])
    ck(bool(raw) and binary[off:off+len(raw)] == raw, ("instruction bytes", hex(off)))
def U(b, at=0): return S.unpack_from("<I", b, at)[0]

def load_table25():
    depot = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch" / "data")))
    ck(depot.drive.upper() != "Z:", "Z: access is forbidden")
    old = ROOT.parent / "fm24"
    sys.path.append(str(old / "tools" / "python"))
    import zstandard as zstd
    entries = runpy.run_path(str(old / "scripts" / "modding_read_dbdat.py"))["_entries"]
    raw = {}
    for side in SIDES:
        _, blob, directory = entries(depot / f"{side}_db.dat")
        base = directory["data_base"]
        index = {x["path"]: x for x in directory["entries"]}
        entry = index[f"{side}_db/table_25.dat"]
        start = base + entry["offset"]
        finish = start + entry["packed_size"]
        bound = min((base + x["offset"] for x in index.values() if x["offset"] > entry["offset"]), default=directory["toc_offset"])
        candidates = []
        p = start
        while p < finish:
            ck(blob[p:p+4] == b"\x28\xb5\x2f\xfd", (side, "zstd magic", p))
            dec = zstd.ZstdDecompressor().decompressobj()
            payload = dec.decompress(blob[p:finish])
            q = finish - len(dec.unused_data)
            ck(dec.eof and q > p and q <= bound, (side, "zstd frame", p))
            if len(payload) == entry["size"]: candidates.append(payload)
            p = q
        ck(len(candidates) == 1, (side, "declared-size selector"))
        raw[side] = candidates[0]
        ck(raw[side][:8] == HEAD and U(raw[side], 8) == N, (side, "header"))
    return raw

class Cursor:
    def __init__(self, b, side): self.b=b; self.side=side; self.p=13; self.end=len(b)-9; self.row=-1
    def take(self, n, label):
        ck(n >= 0 and self.p+n <= self.end, (self.side,self.row,label,self.p,n))
        x=self.b[self.p:self.p+n]; self.p += n; return x
    def u(self,n,label): return int.from_bytes(self.take(n,label),"little")
    def s(self,n,label): return int.from_bytes(self.take(n,label),"little",signed=True)
    def count(self,n,unit,label,signed=False):
        x=self.s(n,label) if signed else self.u(n,label)
        ck(0 <= x <= (self.end-self.p)//unit, (self.side,self.row,label,x)); return x

def replay(b, side):
    c=Cursor(b,side); events={}; values={}; rows=[]
    def rec(k,a,z,v=None):
        events.setdefault(k,[]).append((c.row,a,z-a))
        if v is not None: values.setdefault(k,[]).append((c.row,v))
    def take(k,n):
        a=c.p; v=c.u(n,k); rec(k,a,c.p,v); return v
    def raw(k,n):
        a=c.p; c.take(n,k); rec(k,a,c.p)
    for i in range(N):
        c.row=i; start=c.p
        vals=[take("selector",1),take("m15c",1),take("m15d",1),take("colour_tag",1)]
        for k in ("m120","m124","m128","m12c","m130"): take(k,2)
        take("m134",1); tag=take("m1a0",1)
        for k in ("m1a2","m1a3","m1a4","m1a5"): take(k,1)
        vals += [take("stat_a_tag",1)]
        for k in ("m198","m199","m19a","m19b","m19c","m19d","m19e"): take(k,1)
        vals += [take("stat_b_tag",1)]
        raw("m189_197",15); take("mf6",1)
        for k in ("m138","m13c","m58","m60","m70","m68"): take(k,4)
        take("m150",2)
        ck(tuple(vals) == (0,0,0,1,2,3), (side,i,"fixed tags")); ck(tag != 4, (side,i,"tag4"))
        if side == "server":
            for k,n in (("m180",2),("mb8",4),("m188",1),("m184",2),("m186",2),("m182",2),("m160",8),("m168",8),("m170",8),("m178",8)): take(k,n)
            a=c.p; n=c.count(4,2,"vec30-count"); c.take(2*n,"vec30-body"); rec("vec30",a,c.p)
            p=take("a8_present",1)
            if p:
                a=c.p; v=c.u(1,"a8-version"); c.take(32+4*(v>=2)+9+(2 if v>=3 else 1)+8,"obj_a8-body"); rec("obj_a8",a,c.p)
            for k,n in (("mf0",4),("m1a1",1),("m1a8",1),("mf4",1),("mf5",1)): take(k,n)
            p=take("e0_present",1); ck(p == 0, (side,i,"nonzero e0 outside verifier scope"))
            a=c.p; n=c.count(4,8,"vec18-count",True)
            for j in range(n):
                v=c.s(1,"vec18-version"); c.take(7+(v>=2),"vec18-body")
            rec("vec18",a,c.p)
            p=take("e8_present",1)
            if p:
                a=c.p; c.take(4,"e8-header"); n=c.count(4,8,"e8-count")
                for j in range(n):
                    v=c.s(2,"e8-version"); c.take(6+(2 if v>=2 else 1)+1+(v>=3),"e8-body")
                rec("obj_e8",a,c.p)
            p=take("c0_present",1)
            if p:
                a=c.p; c.take(1,"c0-header"); n=c.count(4,6,"c0-count")
                for j in range(n): c.take(2,"c0-item"); c.take(12*c.count(4,12,"c0-subcount"),"c0-body")
                rec("obj_c0",a,c.p)
            p=take("c8_present",1)
            if p: raw("obj_c8",25)
            take("m1a7",1); p=take("d0_present",1)
            if p: raw("obj_d0",15)
            p=take("d8_present",1)
            if p: raw("obj_d8",15)
            a=c.p; n=c.s(2,"vec100-count"); ck(n >= 0 and n <= (c.end-c.p)//5,(side,i,"vec100")); c.take(5*n,"vec100-body"); rec("vec100",a,c.p)
        for k,n in (("m148",4),("m152",2),("m154",2),("m156",2),("m158",2),("m15a",2),("m80",4),("m88",4),("m90",4),("m98",4)): take(k,n)
        p=take("wbcl_present",1)
        if p: raw("m14c",2)
        for k,n in (("m140",4),("m144",4),("mf7",1),("mf8",1),("mf9",1)): take(k,n)
        a=c.p; row,uid,repeat=S.unpack_from("<III",b,a); c.take(12,"identity"); rec("identity",a,c.p)
        ck((row,uid,repeat)==(i,uid,uid) and uid > (rows[-1][2] if rows else 0),(side,i,"identity")); rows.append((start,c.p,uid))
    ck(b[c.p:] == FOOT,(side,"footer")); return rows,events,values

def check_static():
    helpers=json.loads((OUT/"helpers.json").read_text())
    binary=EXE.read_bytes()
    ck(H(binary) == EXEH == helpers["provenance"]["editor_sha256"], "editor.exe sha256")
    main=helpers["main_reader"]["direct_stream_call_accounting"]
    ck(main["direct_call_count"] == 55 and main["outer_observed_call_count"] == 52 and main["alternate_call_count"] == 3, "stream call accounting")
    ck(len(main["calls"]) == 55, "stream call ledger completeness")
    sites={x["site"] for x in main["calls"]}
    ck({0xEB7218,0xEB72F8,0xEB7332,0xEB7C8F} <= sites, "alternate and extra marker sites")
    wbcl=next(x for x in main["calls"] if x["site"] == 0xEB7C8F)
    ck(wbcl["slot"] == "wbcl_present", "additional marker reconciliation")
    for item in main["calls"]:
        verify_instruction(item["call_instruction"], binary)
    helper_calls=helpers["main_reader"]["direct_helper_call_accounting"]
    ck(len(helper_calls["calls"]) == helper_calls["direct_non_stream_call_count"] == 43, "helper call ledger completeness")
    ck(all(isinstance(item.get("field_mapping_status"), str) and item["field_mapping_status"] for item in helper_calls["calls"]), "helper mapping-status completeness")
    for item in helper_calls["calls"]:
        verify_instruction(item["call_instruction"], binary)
        ck(item["call_instruction"].get("direct_target_file_offset") == item["target_file_offset"], ("helper target", hex(item["site"])))
    payloads=helpers["main_reader"]["payload_entry_conditions"]
    ck(payloads["a8"]["member_offset"] == 0xA8 and payloads["e0"]["member_offset"] == 0xE0, "payload offsets")
    ck(payloads["a8"]["presence_test"]["file_offset"] == 0xEB753F and payloads["e0"]["presence_test"]["file_offset"] == 0xEB76CD, "payload tests")
    for payload in payloads.values():
        for key in ("presence_read","presence_test","skip_target","allocator","reader"):
            verify_instruction(payload[key], binary)
        for key in ("member_store","constructor"):
            if key in payload: verify_instruction(payload[key], binary)
    routes=helpers["bounded_getter_routes"]
    for code, member in (("cnam",0x40),("csnm",0x48),("c3ln",0x50)):
        item=routes["string_getter_paths"][code]
        ck(item["member_offset"] == member, (code,"member offset"))
        verify_instruction(item["compare"], binary)
        verify_instruction(item["member_add"], binary)
    chain=routes["rules_context_chain"]
    for code in ("VARt","HKEt"):
        item=chain[code]
        ck(item["same_comp_scalar_wire_binding_proved"] is False, (code,"wire closure"))
        for key in ("row_object_load","field_code_compare","code_mismatch_branch","object_null_test","object_nonnull_branch"):
            verify_instruction(item[key], binary)
        for record in item["context_dispatch_sequence"]:
            verify_instruction(record, binary)
    separate=chain["separate_nested_rules_dispatch"]
    for record in separate["shared_entry"]:
        verify_instruction(record, binary)
    verify_instruction(separate["nested_helper_entry"], binary)
    for family in separate["jump_table_families"].values():
        base_va=None
        for case in family["cases"]:
            entry=case["entry_file_offset"]
            ck(entry == family["table_file_offset"] + 4*case["index"], "rules table entry offset")
            rel=S.unpack_from("<i", binary, entry)[0]
            ck(rel == case["relative_value"], "rules table relative value")
            target_va=int(case["handler"]["va"],16)
            this_base=target_va-rel
            if base_va is None: base_va=this_base
            ck(this_base == base_va, "rules table target base")
            verify_instruction(case["handler"], binary)

def check():
    base_path=ROOT/"scratch"/"t59"/"out"/"field_map.json"
    base_bytes=base_path.read_bytes()
    base=json.loads(base_bytes)
    r2=json.loads((OUT/"field_map_r2.json").read_text())
    ex=json.loads((OUT/"exclusions.json").read_text())
    helpers=json.loads((OUT/"helpers.json").read_text())
    base_sha=H(base_bytes)
    ck(base["summary"] == {"L3":49,"held":10,"unmapped":196}, "t59 baseline summary")
    ck(base_sha == r2["baseline"]["sha256"] == ex["baseline_field_map_sha256"] == helpers["provenance"]["baseline_field_map_sha256"], "t59 baseline hash")
    ck(r2["summary"]["reviewed_unmapped_occurrences"] == 196 and r2["summary"]["new_L3"] == 0, "r2 summary")
    ck(len(r2["fields"]) == len(ex["fields"]) == 196, "field ledger count")
    expected=[(x["xml_index"],x["code"]) for x in base["fields"] if x["status"] == "unmapped"]
    observed=[(x["xml_index"],x["code"]) for x in r2["fields"]]
    ck(observed == expected, "unmapped occurrence identity/order")
    ck(all(x["baseline_status"] == "unmapped" and x["wire_binding"] is None for x in r2["fields"]), "baseline or wire mutation")
    ck(r2["baseline"]["inversion_count"] == len(base["inversions"]) == 818, "inversion freeze")
    ck(r2["summary"]["baseline_L3_unchanged"] and r2["summary"]["baseline_held_unchanged"] and r2["summary"]["baseline_inversions_unchanged"], "frozen t59 closure")
    check_static()
    raw=load_table25()
    runs={side:replay(raw[side],side) for side in SIDES}
    for side in SIDES:
        rows,events,values=runs[side]
        ck(len(rows) == N, (side,"row count"))
        for key in ("a8_present","e0_present","d0_present","d8_present"):
            if side == "client": ck(not events.get(key), (side,key,"unexpected client event"))
            else: ck(len(events.get(key,[])) == N, (side,key,"event count"))
        if side == "server":
            ck(sum(v != 0 for _,v in values["a8_present"]) == 0 and sum(v != 0 for _,v in values["e0_present"]) == 0, (side,"zero payload presence"))
            ck(len(events.get("obj_a8",[])) == len(events.get("obj_e0",[])) == 0, (side,"payload objects"))
            ck(sum(v != 0 for _,v in values["d0_present"]) == 121 and sum(v != 0 for _,v in values["d8_present"]) == 51, (side,"rules presence"))
    print("t64 verify: PASS; 196 unmapped occurrences reviewed, t59 baseline frozen, a8/e0 presence zero")

def main(argv=None):
    ap=argparse.ArgumentParser(description="independently verify t64 outputs")
    ap.add_argument("--selftest",action="store_true",help="run the verifier")
    ap.parse_args(argv)
    try: check()
    except (Check, OSError, ValueError, ImportError) as exc:
        print(f"t64 verify: FAIL: {exc}", file=sys.stderr); return 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
''').lstrip()


def report_text(r2, ex, helpers) -> str:
    cats = ex["categories"]
    data = helpers["data_replay"]
    helper_ledger = helpers["main_reader"]["direct_helper_call_accounting"]
    return f"""# t64 COMP unmapped round 2\n\n## Scope\n\nThis is an evidence increment over the frozen t59 `comp` `table_25` main-row map. It surveys all 196 t59 `unmapped` occurrences and the static `COMP+0xa8` / `COMP+0xe0` payload entries. It does not reopen t59's 49 L3 fields, 10 held fields, or 818 inversion records, and it does not decode derived collections owned by t66.\n\nCoordinates in the machine-readable files are PE file offsets unless a record includes an explicit `va`. The binary is `editor.exe` SHA-256 `{EXEH}`.\n\n## Result\n\n- Reviewed occurrences: **196/196**.\n- New L3 closures: **0**. The t59 L3/held map and 818 inversions remain byte-for-byte frozen as inputs.\n- Candidate only: `WpBn`, whose getter computes a Band projection using the already-read `+0xf4` state; it is not promoted to a wire binding.\n- Bounded COMP getter literal-code hits: **{r2['summary']['bounded_main_getter_literal_occurrences']}** unmapped occurrences; the slot-5 root separately contains `VARv`/`VARm`/`VARs`/`VARd`. Derived collection roots were not scanned. The remaining occurrences are only negative within the two bounded getter roots, not a whole-binary absence claim.\n\nExclusion category counts are: `{json.dumps(cats, sort_keys=True)}`. Per-occurrence reasons and falsification conditions are in `exclusions.json`; the full field ledger is in `field_map_r2.json`.\n\n## Main-reader ledger\n\nThe main reader extent is `0xeb7000..0xeb7e42`. The bounded CFG and the frozen t59 instruction records enumerate 55 direct `stream+0x28` calls: 52 outer slots plus three tag-4 alternate calls at `0xeb7218`, `0xeb72f8`, and `0xeb7332`. The t59 report states 54/51; the additional outer marker is `wbcl_present` at `0xeb7c8f`, already recorded in t59 `field_slots.json`. This is a call-accounting correction only: no t59 field status, L3 closure, or inversion record changes. The alternate calls reuse `m58/m60/m68`, whose existing XML consumers are `ccti/cnti/cpcm`. The non-stream helper ledger contains {helper_ledger['direct_non_stream_call_count']} reachable direct calls, listed site by site in `helpers.json`.\n\nThe tag-4 arm is gated at `0xeb71b9` and uses name readers at `COMP+0x48` and `COMP+0x40`; the local `[rsp+0xf8]` flag remains source-unresolved. Outside that arm, COMP getter equal paths add `r12+0x40` for `cnam`, `r12+0x48` for `csnm`, and `r12+0x50` for `c3ln`. These are getter-member candidates only: the main-row stream does not prove their wire transfer, tag-4 is absent in both archives, and the t59 held statuses are unchanged.\n\n`VARt` loads `COMP+0xd0` and `HKEt` loads `COMP+0xd8`, then each compare block tests the field code and object pointer. The matching-code/non-null branch reaches file offset `0xec1830`, where the code reads and compares context-object `+0xc0/+0xc8`, calls helper VA `0x140eba600`, and continues through shared context checks. The `0xec0e30 -> 0xeb56c0` nested-rules dispatch is recorded separately and is not asserted as the direct successor of those compare blocks. No same-COMP scalar wire transfer is proved; both t59 fields remain held. The first counterchain and falsification checklist are in `helpers.json`.\n\n## Static payloads\n\n`+0xa8` is entered only when the presence byte read at `0xeb7532` is nonzero; `cmp` at `0xeb753f` followed by `je` at `0xeb7544` skips on zero, while nonzero reaches the allocator at `0xeb754a` and reader at `0xeb75ca`. `+0xe0` is entered only when the presence byte read at `0xeb76c0` is nonzero; `cmp` at `0xeb76cd` followed by `je` at `0xeb76d2` skips on zero, while nonzero reaches allocation/construction at `0xeb76d9/0xeb76e4` and reader at `0xeb76fb`. Exact branch targets and instruction bytes are recorded in `helpers.json`.\n\nThe independent row replay found:\n\n- client: no `a8_present` or `e0_present` event because client mode has no extension block;\n- server: 7,047 presence events for each, all zero; `obj_a8` and `obj_e0` events are 0/0;\n- server sibling rules objects are separate: `+0xd0` presence is 121 and `+0xd8` presence is 51.\n\nThe helper scan also separates `+0xd0/+0xd8` nested rules objects from the requested pair. Generic reader calls at `0xeb718b/0xeb71a2` target `+0x138/+0x13c` and have no XML consumer; the same helper at `0xeb7cc4/0xeb7cdb` maps existing slots `+0x140/+0x144` to `wbst/wben` (XML 25/26).

The zero result is a data counterexample to entry, not proof that the static payloads do not exist.\n\n## Verification\n\n`verify.py` reopens the raw client/server `table_25` payloads and independently parses the native row envelope. The expected command environment is `py -V:3.12 -I -B` with `FM24_DB_DIR=<WORKSPACE>/scratch/data`.\n\nPost-build checks completed: generated `verify.py` passed, and `scripts/t01_anchors.py` passed all 7/7 checks.\n"""


def done_text() -> str:
    return """# t64 Done\n\nGenerated deliverables:\n\n- `scripts/t64_comp_unmapped_r2.py`\n- `scratch/t64/out/helpers.json`\n- `scratch/t64/out/field_map_r2.json`\n- `scratch/t64/out/exclusions.json`\n- `scratch/t64/out/verify.py`\n- `scratch/t64/out/REPORT.md`\n- `scratch/t64/out/DONE.md`\n\nAcceptance recorded by the builder:\n\n- 196/196 t59 unmapped occurrences surveyed.\n- t59 summary `{L3: 49, held: 10, unmapped: 196}` and 818 inversions unchanged.\n- 55 main-reader direct stream calls accounted for; 52 outer slots plus 3 alternate m58/m60/m68 calls. The one-call discrepancy against the t59 report is recorded without changing t59 mappings or inversions.\n- `+0xa8` and `+0xe0` static entry conditions recorded; both are zero-present in all 7,047 server rows and absent from client extension mode.\n- `+0xd0` / `+0xd8` retained separately at 121 / 51 server rows.\n\nPost-build checks completed:

- `scratch/t64/out/verify.py`: PASS.
- `scripts/t01_anchors.py`: PASS, 7/7 checks.
- Builder `--help` and `--selftest`: PASS.\n"""


def build() -> None:
    ck(EXE.exists(), EXE)
    ck(H(EXE.read_bytes()) == EXEH, "editor.exe sha256")
    ck(H(MASTER.read_bytes()) == MASTERH, "master.json sha256")
    manifest = manifest_check()
    base = json.loads((T59 / "field_map.json").read_text(encoding="utf-8"))
    field_slots = json.loads((T59 / "field_slots.json").read_text(encoding="utf-8"))
    ck(base["summary"] == {"L3": 49, "held": 10, "unmapped": 196}, "t59 baseline summary")
    ck(len(base["inversions"]) == 818, "t59 inversion baseline")

    raw, archive_meta = load_archives()
    replay = {side: parse_table25(raw[side, 25], side) for side in SIDES}
    for side in SIDES:
        ck(len(replay[side]["rows"]) == N, (side, "replay row count"))
    ck(sum(v != 0 for _, v in replay["server"]["values"]["a8_present"]) == 0, "a8 server zero")
    ck(sum(v != 0 for _, v in replay["server"]["values"]["e0_present"]) == 0, "e0 server zero")
    ck(len(replay["server"]["events"].get("obj_a8", [])) == 0, "a8 object absent")
    ck(len(replay["server"]["events"].get("obj_e0", [])) == 0, "e0 object absent")
    ck(sum(v != 0 for _, v in replay["server"]["values"]["d0_present"]) == 121, "d0 presence")
    ck(sum(v != 0 for _, v in replay["server"]["values"]["d8_present"]) == 51, "d8 presence")

    pe, md, scans = static_scan()
    direct = direct_stream_accounting(scans, field_slots, base, pe, md)
    ck(direct["direct_call_count"] == 55 and direct["outer_observed_call_count"] == 52, "main direct calls")
    helper_calls = helper_call_accounting(scans, field_slots, base, pe, md)
    payloads = static_payloads(pe, md, replay)
    r2, exclusions = build_field_map(base, scans, direct, manifest)
    helpers = make_helpers(base, scans, direct, helper_calls, payloads, archive_meta, replay, manifest, pe, md)

    emit("field_map_r2.json", r2)
    emit("exclusions.json", exclusions)
    emit("helpers.json", helpers)
    (OUT / "verify.py").write_text(verifier_source(), encoding="utf-8")
    (OUT / "REPORT.md").write_text(report_text(r2, exclusions, helpers), encoding="utf-8")
    (OUT / "DONE.md").write_text(done_text(), encoding="utf-8")
    print("t64 build: PASS")
    print(f"  fields={len(r2['fields'])} new_L3={r2['summary']['new_L3']} direct_calls={direct['direct_call_count']}")
    print("  a8/e0 server presence=0/0; d0/d8 server presence=121/51")


def selftest() -> None:
    ck(code_from_imm(0x5770426E) == "WpBn", "4CC conversion")
    ck(code_from_imm(0x636E616D) == "cnam", "4CC conversion 2")
    ck(code_from_imm(0xFFFFFFFF) is None, "non-ASCII immediate")
    print("t64 selftest: PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="build the t64 COMP unmapped-field evidence increment")
    parser.add_argument("--build", action="store_true", help="build scratch/t64/out deliverables")
    parser.add_argument("--selftest", action="store_true", help="run local helper self-tests")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            selftest()
        if args.build:
            build()
        if not args.selftest and not args.build:
            parser.error("choose --build or --selftest")
    except (Check, OSError, ValueError, ImportError, KeyError, S.error) as exc:
        print(f"t64: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
