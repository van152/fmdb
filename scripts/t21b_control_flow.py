#!/usr/bin/env python3
"""Audit reachable CFG stream calls for the two club RTTI readers."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import importlib.util
import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EDITOR = Path(str(_cfg.EDITOR_EXE))
RTTI_CENSUS = ROOT / "scratch/t01/inbox/t01h/output.json"
WIDTH_TRACE = ROOT / "scratch/t05/reader_widths.json"
AUDIT = ROOT / "scratch/t21/out/audit.json"
OUT = ROOT / "scratch/t21/out"
MAX_FUNCTION_SPAN = 0x20000


REG_ALIASES = {
    "rax": "rax", "eax": "rax", "ax": "rax", "al": "rax", "ah": "rax",
    "rbx": "rbx", "ebx": "rbx", "bx": "rbx", "bl": "rbx", "bh": "rbx",
    "rcx": "rcx", "ecx": "rcx", "cx": "rcx", "cl": "rcx", "ch": "rcx",
    "rdx": "rdx", "edx": "rdx", "dx": "rdx", "dl": "rdx", "dh": "rdx",
    "rsi": "rsi", "esi": "rsi", "si": "rsi", "sil": "rsi",
    "rdi": "rdi", "edi": "rdi", "di": "rdi", "dil": "rdi",
    "rbp": "rbp", "ebp": "rbp", "bp": "rbp", "bpl": "rbp",
    "rsp": "rsp", "esp": "rsp", "sp": "rsp", "spl": "rsp",
}
for _i in range(8, 16):
    _base = f"r{_i}"
    REG_ALIASES.update({_base: _base, _base + "d": _base, _base + "w": _base, _base + "b": _base})


class ReaderCFG:
    def __init__(self, pe, md, function_off: int):
        self.pe = pe
        self.md = md
        self.start_off = function_off
        self.start_va = pe.f2va(function_off)
        if self.start_va is None:
            raise ValueError(f"function offset {function_off:#x} is not mapped")
        self.section = pe.section_of(function_off)
        if not getattr(pe.pe, "DIRECTORY_ENTRY_EXCEPTION", None):
            raise ValueError("PE exception directory is required for function boundaries")
        begin_rva = self.start_va - pe.base
        runtime = next((entry for entry in pe.pe.DIRECTORY_ENTRY_EXCEPTION
                        if int(entry.struct.BeginAddress) <= begin_rva < int(entry.struct.EndAddress)), None)
        if runtime is None:
            raise ValueError(f"no PE runtime-function extent for {function_off:#x}")
        self.function_begin_rva = int(runtime.struct.BeginAddress)
        self.function_end_rva = int(runtime.struct.EndAddress)
        self.function_begin_off = pe.r2f(self.function_begin_rva)
        self.function_end_off = pe.r2f(self.function_end_rva)
        if self.function_begin_off != function_off or self.function_end_off is None:
            raise ValueError(f"unexpected runtime-function bounds for {function_off:#x}")
        self.instructions: dict[int, Any] = {}
        self.successors: dict[int, list[int]] = {}
        self.external_edges: list[dict[str, Any]] = []
        self._build()

    def _inside(self, va: int) -> bool:
        off = self.pe.va2f(va)
        return (off is not None and self.pe.section_of(off) == self.section and
                self.function_begin_off <= off < self.function_end_off and
                off - self.function_begin_off < MAX_FUNCTION_SPAN)

    def _build(self) -> None:
        queue = deque([self.start_va])
        queued = {self.start_va}
        while queue:
            va = queue.popleft()
            if va in self.instructions:
                continue
            off = self.pe.va2f(va)
            if off is None or not self._inside(va):
                continue
            ins = next(self.md.disasm(self.pe.raw[off:off + 15], va), None)
            if ins is None:
                continue
            self.instructions[va] = ins
            next_va = va + ins.size
            succs: list[int] = []
            m = ins.mnemonic.lower()
            if m.startswith("j") and m != "jmp":
                target_va = ins.operands[0].imm if ins.operands and ins.operands[0].type == 2 else None
                for kind, candidate in (("branch", target_va), ("fallthrough", next_va)):
                    if candidate is None:
                        continue
                    if self._inside(candidate):
                        succs.append(candidate)
                    else:
                        self.external_edges.append({"from": hex(off), "kind": kind,
                                                    "target_va": hex(candidate)})
            elif m == "jmp":
                target_va = ins.operands[0].imm if ins.operands and ins.operands[0].type == 2 else None
                if target_va is not None and self._inside(target_va):
                    succs.append(target_va)
                elif target_va is not None:
                    self.external_edges.append({"from": hex(off), "kind": "tail_jump",
                                                "target_va": hex(target_va)})
            elif m not in ("ret", "retf", "iret", "iretq", "int3", "ud2"):
                if self._inside(next_va):
                    succs.append(next_va)
                else:
                    self.external_edges.append({"from": hex(off), "kind": "fallthrough_out_of_bound",
                                                "target_va": hex(next_va)})
            self.successors[va] = sorted(set(succs))
            for target in succs:
                if target not in queued:
                    queue.append(target)
                    queued.add(target)

    @staticmethod
    def _canon(name: str) -> str:
        return REG_ALIASES.get(name.lower(), name.lower())

    @staticmethod
    def _merge_value(a, b):
        return a if a == b else None

    def _merge_state(self, old, new):
        if old is None:
            return {"width": new["width"], "origins": dict(new["origins"])}
        width = self._merge_value(old["width"], new["width"])
        keys = set(old["origins"]) | set(new["origins"])
        origins = {key: self._merge_value(old["origins"].get(key), new["origins"].get(key))
                   for key in keys}
        return {"width": width, "origins": origins}

    def _transfer(self, ins, state):
        width = state["width"]
        origins = dict(state["origins"])
        m = ins.mnemonic.lower()
        ops = ins.operands
        canonical = lambda regid: self._canon(self.md.reg_name(regid))
        writes = set()
        try:
            _, write_regs = ins.regs_access()
            writes = {self._canon(self.md.reg_name(reg)) for reg in write_regs}
        except Exception:
            pass
        for reg in writes:
            origins.pop(reg, None)
        if m == "mov" and len(ops) == 2 and ops[0].type == 1:
            dst = canonical(ops[0].reg)
            src = ops[1]
            dst_name = self.md.reg_name(ops[0].reg).lower()
            if dst == "r8" and dst_name in ("r8d", "r8"):
                width = int(src.imm) if src.type == 2 and 0 < src.imm <= 0x1000 else None
            if src.type == 1:
                source = canonical(src.reg)
                if origins.get(source) is not None:
                    origins[dst] = origins[source]
            elif dst == "r8":
                width = None
        elif m == "lea" and len(ops) == 2 and ops[0].type == 1 and ops[1].type == 3:
            dst = canonical(ops[0].reg)
            mem = ops[1].mem
            base = canonical(mem.base) if mem.base else None
            index = canonical(mem.index) if mem.index else None
            origin = origins.get(base) if base else None
            if origin is not None and index is None:
                origins[dst] = (origin[0], origin[1] + int(mem.disp))
            else:
                origins.pop(dst, None)
        elif m == "add" and len(ops) == 2 and ops[0].type == 1 and ops[1].type == 2:
            dst = canonical(ops[0].reg)
            if origins.get(dst) is not None:
                origin = origins[dst]
                origins[dst] = (origin[0], origin[1] + int(ops[1].imm))
        return {"width": width, "origins": origins}

    def dataflow(self) -> dict[int, dict[str, Any]]:
        incoming: dict[int, dict[str, Any]] = {
            self.start_va: {"width": None, "origins": {"rcx": ("entry_rcx", 0)}}
        }
        queue = deque([self.start_va])
        queued = {self.start_va}
        while queue:
            va = queue.popleft()
            queued.discard(va)
            ins = self.instructions.get(va)
            if ins is None:
                continue
            state = incoming[va]
            after = self._transfer(ins, state)
            off = self.pe.va2f(va)
            if ins.mnemonic.lower() == "call":
                # Calls can mutate Win64 volatile registers; don't carry stale origins.
                for reg in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                    after["origins"].pop(reg, None)
                if ins.op_str.replace(" ", "").startswith("r8d,"):
                    after["width"] = None
            for target in self.successors.get(va, []):
                merged = self._merge_state(incoming.get(target), after)
                if merged != incoming.get(target):
                    incoming[target] = merged
                    if target not in queued:
                        queue.append(target)
                        queued.add(target)
        return incoming

    def _local_width_before_call(self, va: int, leaders: set[int]) -> int | None:
        """Recover an immediate width constant within the current basic block."""
        ordered = sorted(self.instructions)
        try:
            index = ordered.index(va)
        except ValueError:
            return None
        leader = max((item for item in leaders if item <= va), default=self.start_va)
        for candidate_va in reversed(ordered[:index]):
            if candidate_va < leader:
                break
            candidate = self.instructions[candidate_va]
            if candidate.mnemonic.lower() in ("call", "ret", "retf", "iret", "iretq", "int3", "ud2"):
                break
            if candidate.mnemonic.lower().startswith("j"):
                break
            try:
                _, write_regs = candidate.regs_access()
                writes_r8 = any(self._canon(self.md.reg_name(reg)) == "r8" for reg in write_regs)
            except Exception:
                writes_r8 = False
            if writes_r8:
                ops = candidate.operands
                if (candidate.mnemonic.lower() == "mov" and len(ops) == 2 and
                        ops[0].type == 1 and self._canon(self.md.reg_name(ops[0].reg)) == "r8" and
                        ops[1].type == 2):
                    value = int(ops[1].imm)
                    return value if 0 < value <= 0x1000 else None
                return None
        return None

    def _local_object_origin_before_call(self, va: int, leaders: set[int]):
        """Recover a direct LEA [base+constant] feeding RDX in this block."""
        ordered = sorted(self.instructions)
        try:
            index = ordered.index(va)
        except ValueError:
            return None
        leader = max((item for item in leaders if item <= va), default=self.start_va)
        for candidate_va in reversed(ordered[:index]):
            if candidate_va < leader:
                break
            candidate = self.instructions[candidate_va]
            if candidate.mnemonic.lower() in ("call", "ret", "retf", "iret", "iretq", "int3", "ud2"):
                break
            if candidate.mnemonic.lower().startswith("j"):
                break
            try:
                _, write_regs = candidate.regs_access()
                writes_rdx = any(self._canon(self.md.reg_name(reg)) == "rdx" for reg in write_regs)
            except Exception:
                writes_rdx = False
            if not writes_rdx:
                continue
            if candidate.mnemonic.lower() != "lea" or len(candidate.operands) != 2:
                return None
            dst, src = candidate.operands
            if dst.type != 1 or self._canon(self.md.reg_name(dst.reg)) != "rdx" or src.type != 3:
                return None
            mem = src.mem
            if mem.index != 0:
                return None
            base = self._canon(self.md.reg_name(mem.base)) if mem.base else None
            return {"base_register": base, "offset": int(mem.disp),
                    "instruction_file_offset": hex(self.pe.va2f(candidate_va))}
        return None

    def summarize(self) -> dict[str, Any]:
        incoming = self.dataflow()
        leaders = {self.start_va}
        for va, ins in self.instructions.items():
            succs = self.successors.get(va, [])
            if ins.mnemonic.lower().startswith("j") or ins.mnemonic.lower() in ("ret", "retf", "iret", "iretq"):
                leaders.update(succs)
                if ins.mnemonic.lower() != "jmp" and va + ins.size in self.instructions:
                    leaders.add(va + ins.size)
        transfers = []
        calls = []
        branches = []
        for va in sorted(self.instructions):
            ins = self.instructions[va]
            off = self.pe.va2f(va)
            m = ins.mnemonic.lower()
            state = incoming.get(va, {"width": None, "origins": {}})
            if m == "call":
                target_off = None
                target_va = None
                if ins.operands and ins.operands[0].type == 2:
                    target_va = int(ins.operands[0].imm)
                    target_off = self.pe.va2f(target_va)
                call_item = {"file_offset": hex(off), "va": hex(va),
                             "instruction": f"{ins.mnemonic} {ins.op_str}",
                             "target_file_offset": hex(target_off) if target_off is not None else None,
                             "target_va": hex(target_va) if target_va is not None else None}
                if "[rax + 0x28]" in ins.op_str or "[rax+0x28]" in ins.op_str:
                    rdx = state["origins"].get("rdx")
                    local_width = self._local_width_before_call(va, leaders)
                    local_rdx = self._local_object_origin_before_call(va, leaders)
                    transfers.append({
                        **call_item,
                        "width_before_call": local_width if local_width is not None else state["width"],
                        "width_source": ("same_basic_block_mov_r8d" if local_width is not None
                                         else "dataflow_unique" if state["width"] is not None else "unresolved"),
                        "rdx_origin": (local_rdx if local_rdx is not None else
                                        {"base": rdx[0], "offset": rdx[1]} if rdx else None),
                        "rdx_source": ("same_basic_block_lea_rdx" if local_rdx is not None
                                       else "dataflow_unique" if rdx is not None else "unresolved"),
                        "basic_block_leader": hex(self.pe.va2f(max((x for x in leaders if x <= va), default=self.start_va))),
                    })
                else:
                    calls.append(call_item)
            if m.startswith("j"):
                target_va = int(ins.operands[0].imm) if ins.operands and ins.operands[0].type == 2 else None
                target_off = self.pe.va2f(target_va) if target_va is not None else None
                branches.append({
                    "file_offset": hex(off), "va": hex(va),
                    "instruction": f"{ins.mnemonic} {ins.op_str}",
                    "target_file_offset": hex(target_off) if target_off is not None else None,
                    "conditional": m != "jmp",
                    "backedge": bool(target_va is not None and target_va <= va),
                    "successor_file_offsets": [hex(self.pe.va2f(x)) for x in self.successors.get(va, [])
                                               if self.pe.va2f(x) is not None],
                })
        blocks = []
        for leader in sorted(leaders):
            if leader not in self.instructions:
                continue
            blocks.append(hex(self.pe.va2f(leader)))
        return {
            "entry_file_offset": hex(self.start_off),
            "section": self.section,
            "function_extent": {"begin_file_offset": hex(self.function_begin_off),
                                "end_file_offset_exclusive": hex(self.function_end_off),
                                "rva_begin": hex(self.function_begin_rva),
                                "rva_end_exclusive": hex(self.function_end_rva),
                                "source": "PE exception directory / RUNTIME_FUNCTION"},
            "reachable_instruction_count": len(self.instructions),
            "basic_block_leaders": blocks,
            "reachable_stream_transfer_count": len(transfers),
            "reachable_direct_or_other_calls": len(calls),
            "conditional_branch_count": sum(x["conditional"] for x in branches),
            "backedge_count": sum(x["backedge"] for x in branches),
            "stream_transfers": transfers,
            "calls": calls[:200],
            "branches": branches[:300],
            "external_edges": self.external_edges[:100],
        }


def load_pe():
    spec = importlib.util.spec_from_file_location("_t05_pe_t21b", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pe = module.PE(EDITOR)
    import pefile
    if not getattr(pe.pe, "DIRECTORY_ENTRY_EXCEPTION", None):
        pe.pe.parse_data_directories(
            directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]]
        )
    return pe


def build() -> dict[str, Any]:
    if not all(path.is_file() for path in (EDITOR, RTTI_CENSUS, WIDTH_TRACE, AUDIT)):
        raise FileNotFoundError("required binary or t21 evidence is missing")
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    pe = load_pe()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    census = json.loads(RTTI_CENSUS.read_text(encoding="utf-8"))
    width_doc = json.loads(WIDTH_TRACE.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    t05_club = next(x for x in width_doc["results"] if x.get("type_id") == 3)
    census_item = next(x for x in census["census"] if x.get("type_id") == 3)
    class_sources = {
        item["rtti"]["name"]: item["slot19_reader"]
        for item in census_item["constructor_classes"]
    }
    expected = {
        "CLUB": (0xE5A7A0, class_sources[".?AVCLUB@db@@"]),
        "LEAGUE_BODY_CLUB": (0x43BEBA0, class_sources[".?AVLEAGUE_BODY_CLUB@db@@"]),
    }
    classes = []
    for name, (entry, reader_source) in expected.items():
        cfg = ReaderCFG(pe, md, entry).summarize()
        source_functions = reader_source.get("functions_scanned", [])
        classes.append({
            "class": name,
            "rtti_reader_entry": reader_source.get("entry_file_offset"),
            "rtti_unwrapped_entry": reader_source.get("unwrapped_file_offset"),
            "census_width_count": reader_source.get("width_count"),
            "census_stream_call_count": reader_source.get("stream_call_count"),
            "census_backedge_count": reader_source.get("backedge_count"),
            "source_scanned_functions": source_functions,
            "cfg": cfg,
        })
    club_cfg = next(x["cfg"] for x in classes if x["class"] == "CLUB")
    t05_window_call_count = int(t05_club.get("calls", 0))
    census_club = expected["CLUB"][1]
    linear_calls = census_club.get("stream_calls", [])
    linear_offsets = [item.get("file_offset") for item in linear_calls]
    linear_start = int(t05_club["reader"], 16)
    linear_bound = linear_start + 0x2000
    cfg_transfer_sites = {item["file_offset"] for item in club_cfg["stream_transfers"]}
    linear_in_cfg = 0
    for call_off in linear_offsets:
        if call_off and hex(int(call_off, 16)) in cfg_transfer_sites:
            linear_in_cfg += 1
    result = {
        "task": "t21b",
        "status": "partial_control_flow_audit_complete_row_cursor_unreconciled",
        "editor_sha256": audit["static_reader_audit"]["editor_sha256"],
        "linear_scan_comparison": {
            "t05_scan_window_bytes": "0x2000",
            "t05_window_byte_span": hex(linear_bound - linear_start),
            "t05_window_stream_call_count": t05_window_call_count,
            "t01h_reported_stream_call_count": int(census_club.get("stream_call_count", 0)),
            "t01h_stream_call_site_records": len(linear_calls),
            "t01h_stream_call_sites_matching_cfg_transfer_sites": linear_in_cfg,
            "t01h_stream_call_sites_not_matching_cfg": len(linear_calls) - linear_in_cfg,
            "t05_scan_start": hex(linear_start),
            "t05_scan_end_exclusive": hex(linear_bound),
            "club_cfg_reachable_stream_transfer_count": club_cfg["reachable_stream_transfer_count"],
            "interpretation": "t05.calls is the stream-call count from a 0x2000-byte window; t01h.stream_call_count is its census summary, while t01h.stream_calls contains the retained entry-function records. CFG and census scopes differ; no count is treated as a completed serializer cursor.",
        },
        "classes": classes,
        "row_class_discriminator": {
            "status": "negative_not_established",
            "evidence": [
                "t02 club_v2 reports no per-row class byte and explicitly rejects ordinal/marker/name as class proof",
                "t21 full-row audit validates 84259 boundaries but does not identify an RTTI selector",
            ],
            "row_coordinate_mapping_count": 0,
        },
        "Cccn": {
            "status": "unpromoted",
            "row_0_equals_row_8_count": audit["row_audit"]["fixed_word_relations"]["u32@0==u32@8"],
            "row_count": audit["row_audit"]["row_count"],
            "t19_note": "direct local sink/object+0xf0 exists, but codes_full has path_descend only and row-side field identity is not closed",
        },
        "interpretation_limit": "CFG proves reachability in the bounded static function walk, not runtime row-to-class selection or a complete serialized field cursor.",
    }
    return result


def selftest() -> bool:
    assert MAX_FUNCTION_SPAN == 0x20000
    assert ReaderCFG._canon("r8d") == "r8"
    assert ReaderCFG._merge_value(("rcx", 4), ("rcx", 4)) == ("rcx", 4)
    assert ReaderCFG._merge_value(("rcx", 4), ("rcx", 8)) is None
    print("SELFTEST PASS")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT,
                        help="write control_flow.json and control_flow.md here")
    parser.add_argument("--selftest", action="store_true", help="run deterministic helper checks")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    try:
        result = build()
    except (OSError, RuntimeError, ValueError, KeyError, StopIteration) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "control_flow.json").write_text(
        json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    lines = [
        "# t21b club control-flow audit", "",
        f"Status: `{result['status']}`. Static paths are now CFG-based; row cursor remains unreconciled.", "",
        "## Reachable Reader CFG", "",
    ]
    for item in result["classes"]:
        cfg = item["cfg"]
        lines.append(
            f"- **{item['class']}** `{cfg['entry_file_offset']}`: "
            f"{cfg['reachable_instruction_count']} reachable instructions, "
            f"{len(cfg['basic_block_leaders'])} basic blocks, "
            f"{cfg['reachable_stream_transfer_count']} reachable stream transfers, "
            f"{cfg['conditional_branch_count']} conditional branches, "
            f"{cfg['backedge_count']} backedges."
        )
    cmp = result["linear_scan_comparison"]
    lines.extend([
        "", "## Linear-Scan Reconciliation", "",
        f"The t05 0x2000-byte scan reports {cmp['t05_window_stream_call_count']} stream-call patterns; "
        f"t01h reports {cmp['t01h_reported_stream_call_count']} stream calls and retains "
        f"{cmp['t01h_stream_call_site_records']} entry-function records; "
        f"the reachable CLUB CFG identifies {cmp['club_cfg_reachable_stream_transfer_count']} stream transfers, "
        f"with {cmp['t01h_stream_call_sites_matching_cfg_transfer_sites']} t01h sites matching. "
        "These scopes are distinct and none is a completed reader cursor.",
        "", "## Conclusions", "",
        "- No independent per-row RTTI class discriminator was found in the evidence reviewed.",
        f"- `Cccn` remains unpromoted; row+0 equals row+8 in "
        f"{result['Cccn']['row_0_equals_row_8_count']}/{result['Cccn']['row_count']} rows.",
        "- This audit proves bounded static CFG reachability only. It does not establish runtime row/class pairing, "
        "a full cursor, or new field offsets.",
        "- Newly promoted row-coordinate fields: 0.", "",
        "## Reproduction", "",
        "Run `py -V:3.12 -I scripts/t21b_control_flow.py --help`, `--selftest`, then "
        "`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I scripts/t21b_control_flow.py`.",
        "No game, editor, IDA or network access is used.", "",
    ])
    (args.output_dir / "control_flow.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"status={result['status']}; club_cfg_transfers={cmp['club_cfg_reachable_stream_transfer_count']}; "
          f"t01h_reported_stream_calls={cmp['t01h_reported_stream_call_count']}; "
          f"t01h_records={cmp['t01h_stream_call_site_records']}; "
          f"t05_window_stream_calls={cmp['t05_window_stream_call_count']}; output={args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
