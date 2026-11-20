#!/usr/bin/env python3
"""Enumerate editor factory handlers and RTTI construction anchors for t14.

Read-only inputs: editor.exe, fm.exe, and existing local evidence artifacts.
Writes only scratch/t14/out/census.json. Exit codes: 0 success, 1 checks fail,
2 usage/fatal error. Run with: py -V:3.12 -I scripts/t14_rtti_census.py
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t14/out/census.json"
EDITOR = Path(r"<OLD_REPO>\input\editor.exe")
FM = Path(r"<OLD_REPO>\input\fm.exe")
JUMP_BASE = 0xF49D38
DEFAULT_HANDLER = 0xF49CA9
TAIL_VA = 0x140F4A6A9

# Class-family to FM schema entity tag. Exact schema-name matches use the tag
# in schema_inventory.json; STARTING_* record names use their owning entity
# family (the same normalization used by the t14 task instructions).
CLASS_TAG = {
    "AWARD":"awar", "BASIC_PERSON":"pers", "CITY":"city", "LEAGUE_BODY_CLUB":"club",
    "CONTINENT":"cont", "INJURY":"inju", "MEDIA_SOURCE":"mdso", "LANGUAGE":"lang",
    "NATIONAL_TEAM_CONTAINER":"nati", "NATION":"nati", "DERBY":"drbr", "REGION":"regi",
    "STADIUM":"stad", "STADIUM_CHANGE":"stad", "STAGE_NAME":"stgn", "NATIONAL_TEAM":"team",
    "TEAM":"team", "COMP":"comp", "COMP_HISTORY_RECORD":"comp", "WEATHER":"weat",
    "STARTING_AWARD_HISTORY":"awar", "PLAYING_HISTORY":"pers", "STARTING_LOAN":"pers",
    "STARTING_INJURY":"play", "STARTING_CONFIDENCE":"play", "STARTING_FUTURE_TRANSFER":"pers",
    "STARTING_CLUB_DEBT":"club", "STARTING_TEAM_CUP_HISTORY":"club", "PLAYER_TYPE":"play",
    "STARTING_MANAGER_HOF_RECORD":"pers", "STARTING_TEAM_LEAGUE_HISTORY":"club",
    "STARTING_BAN":"pers", "STARTING_AVERAGE_POINTS":"team", "CURRENCY_RECORD":"curr",
    "STARTING_RETIREMENT":"pers", "STARTING_MONTHLY_INSTALLMENT":"club",
    "NON_PLAYING_HISTORY":"pers", "STARTING_DRAFT_TRANSFER":"pers", "LOCAL_REGION":"lcrg",
    "STARTING_PERSON_HISTORY":"pers", "STARTING_MLS_TRADED_SLOT":"club",
    "STARTING_MLS_GENERAL_ALLOCATION_MONEY":"club", "STARTING_PLAYER_HAPPINESS":"play",
    "STARTING_WEEKLY_WAGE_CONTRIBUTION":"club", "STARTING_MEDIA_EXPECTATIONS":"play",
    "STARTING_MLS_TARGETED_ALLOCATION_MONEY":"club",
    "STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT":"club",
    "STARTING_RESERVE_TEAM":"club", "STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER":"club",
    "STARTING_CLUB_STAFF_JOB_STATUS":"club", "STARTING_NEWGEN_PARAMETER":"pers",
    "STARTING_CLUB_TRANSFER_PREFERENCE":"club", "STARTING_VISION_OBJECTIVE":"club",
    "STARTING_PAST_TRANSFER":"pers", "STARTING_PAST_TRADE":"pers",
    "STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT":"play",
    "AGREEMENT":"agrm",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def hx(n: int | None) -> str | None:
    return None if n is None else f"0x{n:x}"


def cstring(raw: bytes, off: int, limit: int = 256) -> bytes:
    if off < 0 or off >= len(raw):
        return b""
    end = raw.find(b"\0", off, min(len(raw), off + limit))
    return raw[off:end if end >= 0 else min(len(raw), off + limit)]


def class_from_decorated(s: bytes) -> str | None:
    try:
        text = s.decode("ascii")
    except UnicodeDecodeError:
        return None
    if not text.startswith(".?AV"):
        return None
    if text.endswith("@db@@"):
        name = text[4:-5]
    elif text.endswith("@@"):
        name = text[4:-2]
    else:
        return None
    return name or None


def load_pe(path: Path):
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import t05_pe  # type: ignore[import-not-found]
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs  # type: ignore[import-not-found]
    pe = t05_pe.PE(path)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return pe, md


def jump_targets(pe) -> dict[int, int]:
    out = {}
    for tid in range(74):
        cell = JUMP_BASE + tid * 4
        rel = struct.unpack_from("<i", pe.raw, cell)[0]
        out[tid] = JUMP_BASE + rel
    return out


def decode_instructions(pe, md, off: int, max_bytes: int, stop_ret: bool):
    va = pe.f2va(off)
    if va is None or not (0 <= off < len(pe.raw)):
        return []
    insns = []
    for ins in md.disasm(pe.raw[off:min(len(pe.raw), off + max_bytes)], va):
        insns.append(ins)
        if ins.mnemonic in ("ret", "retf", "iret", "iretq", "int3"):
            if stop_ret:
                break
        if ins.mnemonic == "jmp":
            # Each emitted factory/constructor basic block ends at an
            # unconditional jump. Do not linear-scan into the adjacent table's
            # block or a shared dispatcher target.
            break
        if ins.address - va > max_bytes:
            break
    return insns


def rip_target(ins) -> int | None:
    try:
        if ins.mnemonic != "lea" or len(ins.operands) != 2:
            return None
        dst, src = ins.operands
        if dst.type != 1 or src.type != 3 or src.mem.base != 41:  # X86_REG_RIP
            return None
        return ins.address + ins.size + src.mem.disp
    except Exception:
        return None


def assigned_vtable(insns, index: int, pe=None, md=None) -> bool:
    """Validate a LEA target store, directly or through a shared tail helper."""
    try:
        reg = insns[index].operands[0].reg
        for nxt in insns[index + 1:index + 6]:
            if nxt.mnemonic == "jmp" and nxt.operands and nxt.operands[0].type == 2 and pe is not None and md is not None:
                target_off = pe.va2f(nxt.operands[0].imm)
                if target_off is not None:
                    helper = decode_instructions(pe, md, target_off, 0x80, stop_ret=True)
                    for h in helper[:6]:
                        if h.mnemonic == "mov" and len(h.operands) == 2:
                            hd, hs = h.operands
                            if hd.type == 3 and hs.type == 1 and hs.reg == reg:
                                return True
            if nxt.mnemonic != "mov" or len(nxt.operands) != 2:
                continue
            dst, src = nxt.operands
            if dst.type == 3 and src.type == 1 and src.reg == reg:
                return True
            # A register may be copied between LEA and the memory store.
            if dst.type == 1 and src.type == 1 and src.reg == reg:
                reg = dst.reg
        return False
    except Exception:
        return False


def parse_rtti(pe, vtable_va: int) -> dict[str, Any] | None:
    vtoff = pe.va2f(vtable_va)
    if vtoff is None or vtoff < 8 or vtoff + 8 > len(pe.raw):
        return None
    col_va = struct.unpack_from("<Q", pe.raw, vtoff - 8)[0]
    col_off = pe.va2f(col_va)
    if col_off is None or col_off + 20 > len(pe.raw):
        return None
    sig, obj_off, cd_off, td_rva, chd_rva = struct.unpack_from("<IIIII", pe.raw, col_off)
    if sig != 1:
        return None
    td_va = pe.base + td_rva
    chd_va = pe.base + chd_rva
    td_off = pe.va2f(td_va)
    chd_off = pe.va2f(chd_va)
    if td_off is None or chd_off is None:
        return None
    decorated = cstring(pe.raw, td_off + 16)
    name = class_from_decorated(decorated)
    if not name:
        return None
    # Self-consistency: vfptr slot -1 resolves to this COL, all RVA fields map
    # back through PE section mappings, and the TD string begins at TD+16.
    if pe.f2va(col_off) != col_va or pe.f2r(td_off) != td_rva or pe.f2r(chd_off) != chd_rva:
        return None
    # Validate the CHD header is addressable and has a plausible bounded count.
    chd_sig, chd_attr, chd_count = struct.unpack_from("<III", pe.raw, chd_off)
    if chd_sig not in (0, 1) or chd_count > 0x10000:
        return None
    return {
        "vtable_va": vtable_va, "vtable_off": vtoff, "col_va": col_va,
        "col_off": col_off, "td_rva": td_rva, "td_off": td_off,
        "chd_rva": chd_rva, "chd_off": chd_off, "class": name,
        "decorated": decorated.decode("ascii", errors="replace"),
        "col_sig": sig, "col_obj_off": obj_off, "col_cd_off": cd_off,
        "chd_sig": chd_sig, "chd_attr": chd_attr, "chd_count": chd_count,
    }


def scan_handler(pe, md, handler_off: int, depth_limit: int = 4) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """BFS direct callees; depth zero is the factory block, max 4 call edges."""
    q = deque([(handler_off, 0)])
    seen: set[int] = set()
    hits: dict[tuple[int, int], dict[str, Any]] = {}
    trace = {"visited_functions": [], "calls_by_depth": {}, "limit": depth_limit}
    while q:
        off, depth = q.popleft()
        if off in seen or depth > depth_limit or len(seen) >= 512:
            continue
        seen.add(off)
        insns = decode_instructions(pe, md, off, 0x700 if depth == 0 else 0x500, stop_ret=depth > 0)
        trace["visited_functions"].append({"file_off": hx(off), "depth": depth, "instruction_count": len(insns)})
        call_targets = []
        tail_targets = []
        for i, ins in enumerate(insns):
            target = rip_target(ins)
            if target is not None and assigned_vtable(insns, i, pe, md):
                vta = pe.va2f(target)
                if vta is not None:
                    rtti = parse_rtti(pe, target)
                    if rtti is not None:
                        key = (target, ins.address)
                        hits[key] = {"inst_off": pe.va2f(ins.address), "vtable_va": target,
                                     "depth": depth, "source_function_off": off, "rtti": rtti}
            if ins.mnemonic in ("call", "jmp") and ins.operands and ins.operands[0].type == 2:
                target_va = ins.operands[0].imm
                target_off = pe.va2f(target_va)
                if target_off is not None and target_va != TAIL_VA and pe.section_of(target_off) in (".rdata", ".reloc"):
                    (call_targets if ins.mnemonic == "call" else tail_targets).append(target_off)
        trace["calls_by_depth"].setdefault(str(depth), 0)
        trace["calls_by_depth"][str(depth)] += len(call_targets)
        if depth < depth_limit:
            for target_off in dict.fromkeys(call_targets + tail_targets):
                if target_off not in seen:
                    q.append((target_off, depth + 1))
    results = []
    for hit in sorted(hits.values(), key=lambda x: (x["depth"], x["inst_off"])):
        r = hit.pop("rtti")
        results.append({"inst_off": hx(hit["inst_off"]), "vtable_va": hx(hit["vtable_va"]),
                        "col_off": hx(r["col_off"]), "class": r["class"], "depth": hit["depth"],
                        "fm_cross": "n/a", "_details": r,
                        "_source_function_off": hx(hit["source_function_off"])})
    return results, trace


def fm_td_names(fm_path: Path) -> set[str] | None:
    if not fm_path.is_file():
        return None
    import re as _re
    fm_pe, _ = load_pe(fm_path)
    raw = fm_pe.raw
    # A TD is accepted only when its string is exactly at TD+16 and its vfptr
    # and TD file location both map through the FM PE section table.
    names: set[str] = set()
    for m in _re.finditer(rb"\.\?AV[^\x00]{1,160}?(?:@db)?@@\x00", raw):
        start = m.start()
        td_off = start - 16
        if td_off < 0 or fm_pe.f2va(td_off) is None:
            continue
        vfptr = struct.unpack_from("<Q", raw, td_off)[0]
        if fm_pe.va2f(vfptr) is None:
            continue
        candidate = raw[start:m.end() - 1]
        if class_from_decorated(candidate):
            names.add(candidate.decode("ascii"))
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description="Enumerate table_type factory handlers and RTTI vtable construction anchors.")
    parser.add_argument("--output", type=Path, default=OUT, help="output census.json (must be in scratch/t14/out)")
    parser.add_argument("--selftest", action="store_true", help="run offline unit checks")
    args = parser.parse_args()
    try:
        if args.selftest:
            assert JUMP_BASE + 4 * 73 == 0xF49E5C
            assert class_from_decorated(b".?AVDERBY@db@@") == "DERBY"
            assert class_from_decorated(b".?AVBASIC_SCORELINE@SCORELINE@db@@") == "BASIC_SCORELINE@SCORELINE"
            print("SELFTEST PASS")
            return 0
        output = args.output.resolve()
        if ROOT / "scratch/t14/out" not in output.parents:
            raise ValueError("output must be under scratch/t14/out")
        if not EDITOR.is_file():
            raise FileNotFoundError(EDITOR)
        jump_doc = load_json(ROOT / "scratch/t01/t01h_jump_table_anchor.json")
        pe, md = load_pe(EDITOR)
        targets = jump_targets(pe)
        dedicated = set(jump_doc["dedicated_types"])
        defaults = set(jump_doc["default_types"])
        if len(dedicated) != 63 or len(defaults) != 11 or dedicated & defaults:
            raise ValueError("t01h jump-table type census is inconsistent")
        if targets[10] != 0xF48F27 or targets[25] != 0xF49129:
            raise ValueError("factory jump-table negative controls changed")
        if targets[53] != DEFAULT_HANDLER or targets[54] != DEFAULT_HANDLER or targets[55] != DEFAULT_HANDLER:
            raise ValueError("default handler controls changed")

        # Preserve independently confirmed pre-task class names as an audit
        # expectation; findings still come only from bytes and the COL chain.
        expected_classes = {
            0:"AWARD",2:"CITY",3:"LEAGUE_BODY_CLUB",4:"RGB_COLOUR",8:"LANGUAGE",18:"DERBY",
            19:"REGION",23:"STAGE_NAME",26:"COMP_HISTORY_RECORD",27:"WEATHER",30:"STARTING_INJURY",
            31:"STARTING_CONFIDENCE",34:"STARTING_TEAM_CUP_HISTORY",35:"PLAYER_TYPE",
            37:"STARTING_TEAM_LEAGUE_HISTORY",38:"STARTING_BAN",42:"STARTING_RETIREMENT",
            43:"STARTING_MONTHLY_INSTALLMENT",45:"STARTING_RECORD",46:"STARTING_DRAFT_TRANSFER",
            48:"STARTING_RECORD",49:"STARTING_PERSON_HISTORY",50:"STARTING_MLS_TRADED_SLOT",
            51:"STARTING_MLS_GENERAL_ALLOCATION_MONEY",52:"STARTING_PLAYER_HAPPINESS",56:"AGREEMENT",
            57:"FIXTURE_NAME",58:"STARTING_WEEKLY_WAGE_CONTRIBUTION",59:"STARTING_MEDIA_EXPECTATIONS",
            60:"STARTING_MLS_TARGETED_ALLOCATION_MONEY",61:"STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT",
            62:"STARTING_RESERVE_TEAM",63:"STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER",
            64:"STARTING_CLUB_STAFF_JOB_STATUS",65:"STARTING_NEWGEN_PARAMETER",66:"STARTING_CLUB_TRANSFER_PREFERENCE",
            67:"STARTING_NEWGEN_PARAMETER",68:"STARTING_NEWGEN_PARAMETER",69:"STARTING_NEWGEN_PARAMETER",
            70:"STARTING_VISION_OBJECTIVE",73:"STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT",
            32:"STARTING_FUTURE_TRANSFER",39:"STARTING_AVERAGE_POINTS",
        }
        fm_names = fm_td_names(FM)
        rows = []
        mismatches = []
        for tid in range(74):
            handler = targets[tid]
            if tid in defaults:
                rows.append({"table_type":tid,"status":"default","handler_off":hx(handler),"vtables":[],
                             "entity_tag":None,"adjudication":"default",
                             "trace":{"reason":"dispatcher/default handler; no dedicated construction block"}})
                continue
            hits, trace = scan_handler(pe, md, handler, 4)
            # Keep distinct constructor sites/classes; collapse exact duplicate
            # discoveries reached through alternate BFS paths.
            uniq = {}
            for hit in hits:
                k = (hit["inst_off"], hit["vtable_va"], hit["class"])
                uniq[k] = hit
            hits = list(uniq.values())
            for hit in hits:
                decorated = hit["_details"]["decorated"]
                hit["fm_cross"] = "td-only" if fm_names is not None and decorated in fm_names else "n/a"
                hit.pop("_details", None)
                hit.pop("_source_function_off", None)
            classes = sorted({x["class"] for x in hits})
            min_depth = min((x["depth"] for x in hits), default=None)
            primary_classes = sorted({x["class"] for x in hits if x["depth"] == min_depth}) if hits else []
            expected = expected_classes.get(tid)
            if expected and expected not in classes:
                mismatches.append({"table_type":tid,"expected":expected,"observed":classes,
                                   "reason":"commander supplied class name not found by independent handler/COL scan"})
            primary = primary_classes[0] if len(primary_classes) == 1 else None
            entity = CLASS_TAG.get(primary) if primary else None
            adjudication = ("resolved" if entity else "candidate") if classes else "negative"
            if len(primary_classes) > 1:
                # Multiple different classes at the same shallowest constructor
                # depth remain a genuine ambiguity; deeper helper/base refs do not
                # erase an independently direct handler assignment.
                entity = None
                adjudication = "candidate"
            row = {"table_type":tid,"status":"dedicated","handler_off":hx(handler),"vtables":hits,
                   "primary_class":primary,"entity_tag":entity,"adjudication":adjudication,
                   "trace":trace}
            if expected:
                row["expected_class_check"] = {"expected":expected,"observed":classes,"match":expected in classes}
            if not hits:
                row["negative_reason"] = (f"dedicated handler {handler:#x}; BFS reached depth {trace['limit']} "
                                          f"across {len(trace['visited_functions'])} functions; no assigned RIP-vtable "
                                          "LEA resolved through a self-consistent relative COL/TD chain")
                row["adjudication"] = "negative"
            rows.append(row)
        doc = {"status":"complete" if len(rows)==74 and not mismatches else "partial_rtti_census",
               "method":{"jump_base":hx(JUMP_BASE),"rel32":"handler = jump_base + signed_i32(table_base + 4*type)",
                         "default_handler":hx(DEFAULT_HANDLER),"bfs_depth_limit":4,
                         "rtti":"vtable[-1] COL VA; COL+0x0 sig; COL+0xC TD RVA; COL+0x10 CHD RVA; TD+16 decorated class",
                         "editor":"D:\\tmp2b\\fm24\\input\\editor.exe","fm":"D:\\tmp2b\\fm24\\input\\fm.exe",
                         "fm_td_names_found":len(fm_names) if fm_names is not None else None},
               "summary":{"types":len(rows),"dedicated":len(dedicated),"default":len(defaults),
                          "named":sum(bool(x.get("vtables")) for x in rows if x["status"]=="dedicated"),
                          "no_rtti":sum(not x.get("vtables") for x in rows if x["status"]=="dedicated"),
                          "expected_class_mismatches":len(mismatches),
                          "fm_td_missing":sorted({v["class"] for r in rows for v in r.get("vtables",[]) if v["fm_cross"]=="n/a"})},
               "class_check_mismatches":mismatches,"tables":rows}
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"wrote {output}; types={len(rows)} named={doc['summary']['named']} no_rtti={doc['summary']['no_rtti']} mismatches={len(mismatches)}")
        return 0 if len(rows)==74 else 1
    except (OSError, ValueError, KeyError, struct.error, AssertionError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
