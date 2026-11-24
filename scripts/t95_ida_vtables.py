"""t95 — Batch vtable slot extraction & Hex-Rays decompilation for all 74 FM24 DB tables.

Opens a scratch copy of D:/tmp2b/fm24/ida/editor_merge_v2.i64 via IDA Pro 9.4 idalib
(read-only source preserved), extracts vtable slots 0..31 for every table class in
scratch/t14/out/census.json (plus extra classes), and decompiles:
  - slot[2]  (get_property)
  - slot[3]  (set_property)
  - slot[5]  (register_properties, when non-trivial)
  - slot[19] (read_server / read_db)
  - slot[20] (read_client)
  - slot[21] (write_db)
plus 1-hop direct callees of thin wrapper slots (<= 20 lines).

Usage:
  py -V:3.12 -I -B scripts/t95_ida_vtables.py --selftest
  py -V:3.12 -I -B scripts/t95_ida_vtables.py [--limit N]
Exit codes: 0 ok, 1 partial misses, 2 bad usage/fatal.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import re
import shutil
import struct
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDA_LIB = str(_cfg.IDA_LIB_DIR)
SRC_I64 = Path(str(_cfg.IDA_DB))
DEFAULT_PE = Path(str(_cfg.EDITOR_EXE))
CENSUS = ROOT / "scratch/t14/out/census.json"
DEFAULT_OUT = ROOT / "scratch/t95"

# Core virtual slots across DATABASE_OBJECT hierarchy
CORE_SLOTS = {
    2: "slot02_get_prop",
    3: "slot03_set_prop",
    5: "slot05_reg_prop",
    19: "slot19_read_server",
    20: "slot20_read_client",
    21: "slot21_write",
}

# Known trivial shared stub VAs (return 0 / return 1 / ret)
TRIVIAL_STUBS = {
    0x1400015A0,
    0x1400015B0,
    0x1400015E0,
    0x1407EB2D0,
    0x140DD2B10,
    0x140DD2B30,
    0x140DD2B40,
    0x140DD5500,
    0x140843500,
    0x140FE6F80,
    0x140FE7190,
}

# Extra vtables discovered in sub_140F49530 or base classes
EXTRA_VTABLES = [
    # (table_type_or_neg, class_name, vtable_va)
    (3, "CLUB", 0x14187CD08),
    (9, "TEAM_CONTAINER", 0x14188E548),
    (24, "TEAM", 0x14188E2D8),
]


def load_pe_vtable_reader(pe_path: Path):
    sys.path.insert(0, str(_cfg.LEGACY_TOOLS_DIR))
    import pefile  # noqa: E402

    pe = pefile.PE(str(pe_path), fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    raw = pe_path.read_bytes()
    sections = [
        (s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData)
        for s in pe.sections
    ]

    def va_to_fo(va: int) -> int | None:
        rva = va - base
        for va_s, sz_s, fo_s in sections:
            if va_s <= rva < va_s + sz_s:
                return fo_s + (rva - va_s)
        return None

    def read_slots(vt_va: int, n: int = 32) -> list[int]:
        fo = va_to_fo(vt_va)
        if fo is None or fo + n * 8 > len(raw):
            return []
        vals = list(struct.unpack_from(f"<{n}Q", raw, fo))
        out = []
        for v in vals:
            if 0x140000000 <= v < 0x145000000:
                out.append(v)
            else:
                break
        return out

    def resolve_thunk(va: int) -> tuple[int, str | None]:
        """Follow leading unconditional jmp (or 1-2 setup insns + jmp) thunks into .reloc/impl."""
        import capstone  # noqa: E402
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        cur = va
        note = None
        for _ in range(3):
            fo = va_to_fo(cur)
            if fo is None or fo + 24 > len(raw):
                break
            insns = list(md.disasm(raw[fo : fo + 24], cur))
            if not insns:
                break
            if insns[0].mnemonic == "jmp" and insns[0].op_str.startswith("0x"):
                tgt = int(insns[0].op_str, 16)
                if 0x140000000 <= tgt < 0x145000000:
                    note = f"jmp:{hex(cur)}->{hex(tgt)}"
                    cur = tgt
                    continue
            if (
                len(insns) >= 2
                and insns[0].mnemonic in ("mov", "xor", "lea")
                and insns[1].mnemonic == "jmp"
                and insns[1].op_str.startswith("0x")
            ):
                tgt = int(insns[1].op_str, 16)
                if 0x140000000 <= tgt < 0x145000000:
                    note = f"setup+jmp({insns[0].mnemonic} {insns[0].op_str}):{hex(cur)}->{hex(tgt)}"
                    cur = tgt
                    continue
            break
        return cur, note

    return base, read_slots, resolve_thunk


def collect_vtables(census_path: Path) -> list[dict]:
    d = json.loads(census_path.read_text(encoding="utf-8"))
    entries: list[dict] = []
    seen: set[tuple[int, int]] = set()
    for t in d["tables"]:
        tt = t["table_type"]
        for v in t.get("vtables", []):
            va = int(v["vtable_va"], 16)
            key = (tt, va)
            if key not in seen:
                seen.add(key)
                entries.append({
                    "table_type": tt,
                    "class": v.get("class") or t.get("primary_class") or f"TT{tt}",
                    "entity_tag": t.get("entity_tag"),
                    "vtable_va": va,
                    "source": "census",
                })
    for tt, cls, va in EXTRA_VTABLES:
        key = (tt, va)
        if key not in seen:
            seen.add(key)
            entries.append({
                "table_type": tt,
                "class": cls,
                "entity_tag": None,
                "vtable_va": va,
                "source": "extra",
            })
    entries.sort(key=lambda x: (x["table_type"], x["vtable_va"]))
    return entries


def extract_4ccs_from_text(text: str) -> list[str]:
    """Find plausible ASCII 4CC integer constants in Hex-Rays pseudocode."""
    found: set[str] = set()
    # Hex constants like 0x636E616D or decimal ints in switch cases
    for m in re.finditer(r"\b0x([0-9A-Fa-f]{8})\b", text):
        val = int(m.group(1), 16)
        b = struct.pack(">I", val)
        if all(32 <= c <= 126 for c in b) and any(65 <= c <= 90 or 97 <= c <= 122 for c in b):
            found.add(b.decode("ascii"))
    for m in re.finditer(r"\bcase\s+(\d{9,10})\b|==\s*(\d{9,10})\b", text):
        s = m.group(1) or m.group(2)
        val = int(s)
        if 0x20202020 <= val <= 0x7E7E7E7E:
            b = struct.pack(">I", val)
            if all(32 <= c <= 126 for c in b) and any(65 <= c <= 90 or 97 <= c <= 122 for c in b):
                found.add(b.decode("ascii"))
    return sorted(found)


def extract_callees_from_text(text: str) -> list[int]:
    """Extract sub_14xxxxxxx / unk_14xxxxxxx call targets from decompiled text."""
    vas: list[int] = []
    seen: set[int] = set()
    for m in re.finditer(r"\b(?:sub|unk|loc|nullsub)_([0-9A-Fa-f]{9,12})\b", text):
        va = int(m.group(1), 16)
        if 0x140000000 <= va < 0x145000000 and va not in seen:
            seen.add(va)
            vas.append(va)
    return vas


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Batch decompile all FM24 DB table vtable methods via IDA 9.4 idalib.")
    ap.add_argument("--census", type=Path, default=CENSUS)
    ap.add_argument("--pe", type=Path, default=DEFAULT_PE)
    ap.add_argument("--i64", type=Path, default=SRC_I64)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--limit", type=int, default=0, help="Only process first N vtables")
    ap.add_argument("--no-i64", action="store_true", help="Open raw editor.exe with -a- instead of i64 copy")
    ap.add_argument("--selftest", action="store_true", help="Validate census + PE vtable slot extraction without IDA")
    args = ap.parse_args()

    _, read_slots, resolve_thunk = load_pe_vtable_reader(args.pe)
    vtables = collect_vtables(args.census)
    for e in vtables:
        e["slots"] = read_slots(e["vtable_va"], 32)

    unique_core_vas: set[int] = set()
    for e in vtables:
        for idx in CORE_SLOTS:
            if idx < len(e["slots"]):
                va = e["slots"][idx]
                if va not in TRIVIAL_STUBS:
                    unique_core_vas.add(va)

    if args.selftest:
        ok_vt = sum(1 for e in vtables if len(e["slots"]) >= 22)
        print(f"vtables={len(vtables)} with_>=22_slots={ok_vt} unique_core_methods={len(unique_core_vas)}")
        for e in vtables[:5]:
            s19 = hex(e["slots"][19]) if len(e["slots"]) > 19 else "-"
            s2 = hex(e["slots"][2]) if len(e["slots"]) > 2 else "-"
            print(f"  tt={e['table_type']:2d} {e['class']:25s} vt={hex(e['vtable_va'])} slot2={s2} slot19={s19}")
        return 0 if ok_vt >= 60 else 1

    out = args.out
    funcs_dir = out / "funcs"
    tables_dir = out / "tables"
    funcs_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    todo = vtables if args.limit <= 0 else vtables[: args.limit]

    # Prepare unwind lookup fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import t94_focus_disasm as fd  # noqa: E402
    fd.set_pe(args.pe)

    sys.path.insert(0, IDA_LIB)
    import idapro  # noqa: E402
    import ida_auto  # noqa: E402
    import ida_funcs  # noqa: E402
    import ida_hexrays  # noqa: E402
    import ida_name  # noqa: E402
    import ida_ua  # noqa: E402

    t0 = time.time()
    if args.no_i64 or not args.i64.exists():
        db_target = str(args.pe)
        extra_args = f"-o{(out / 'ida_tmp.i64').resolve()} -a-"
        print(f"Opening PE directly: {db_target}", flush=True)
        rc = idapro.open_database(db_target, False, extra_args)
    else:
        work_i64 = out / "editor_work.i64"
        if not work_i64.exists() or work_i64.stat().st_size != args.i64.stat().st_size:
            print(f"Copying {args.i64} -> {work_i64} ...", flush=True)
            shutil.copy2(args.i64, work_i64)
        print(f"Opening i64 copy: {work_i64}", flush=True)
        rc = idapro.open_database(str(work_i64), False)
    print(f"open_database rc={rc} elapsed={time.time()-t0:.1f}s", flush=True)
    if rc:
        return 2

    ida_auto.enable_auto(False)
    hr_ok = ida_hexrays.init_hexrays_plugin()
    print(f"Hex-Rays={hr_ok}", flush=True)
    if not hr_ok:
        idapro.close_database(False)
        return 2

    decomp_cache: dict[int, dict] = {}
    misses: list[dict] = []

    def ensure_func(va: int) -> int:
        f = ida_funcs.get_func(va)
        if f is not None:
            return f.start_ea
        rec = fd.owner(va)
        if rec:
            start = fd.IMAGE_BASE + rec[0]
            end = fd.IMAGE_BASE + rec[1]
            ea = start
            while ea < end:
                sz = ida_ua.create_insn(ea)
                ea += sz or 1
            ida_funcs.add_func(start, end)
            ida_auto.enable_auto(True)
            ida_auto.plan_and_wait(start, end)
            ida_auto.enable_auto(False)
            return start
        ida_ua.create_insn(va)
        ida_funcs.add_func(va)
        ida_auto.enable_auto(True)
        ida_auto.plan_and_wait(va, va + 0x100)
        ida_auto.enable_auto(False)
        f = ida_funcs.get_func(va)
        return f.start_ea if f else va

    def decompile_va(va: int, tag: str) -> dict:
        if va in decomp_cache:
            return decomp_cache[va]
        start = ensure_func(va)
        if start in decomp_cache:
            decomp_cache[va] = decomp_cache[start]
            return decomp_cache[start]
        name = ida_name.get_name(start) or f"sub_{start:x}"
        info = {
            "va": hex(va),
            "func_start": hex(start),
            "name": name,
            "ok": False,
            "lines": 0,
            "bytes": 0,
            "fourccs": [],
            "callees": [],
            "file": f"funcs/{start:x}.c",
        }
        try:
            cfunc = ida_hexrays.decompile(start, flags=ida_hexrays.DECOMP_NO_WAIT)
            if cfunc is None:
                cfunc = ida_hexrays.decompile(start)
            if cfunc is not None:
                text = str(cfunc)
                (funcs_dir / f"{start:x}.c").write_text(text, encoding="utf-8")
                info["ok"] = True
                info["lines"] = text.count("\n") + 1
                info["bytes"] = len(text)
                info["fourccs"] = extract_4ccs_from_text(text)
                info["callees"] = [hex(c) for c in extract_callees_from_text(text) if c != start]
            else:
                misses.append({"va": hex(va), "tag": tag, "why": "decompile returned None"})
        except Exception as exc:
            misses.append({"va": hex(va), "tag": tag, "why": str(exc)})
            (funcs_dir / f"{start:x}.err.txt").write_text(traceback.format_exc(), encoding="utf-8")
        decomp_cache[start] = info
        decomp_cache[va] = info
        return info

    # Pass 1: decompile all core slots for all tables
    index_tables = []
    wrapper_callees: list[tuple[int, str]] = []
    for e in todo:
        tt = e["table_type"]
        cls = e["class"]
        slots = e["slots"]
        t_rec = {
            "table_type": tt,
            "class": cls,
            "entity_tag": e["entity_tag"],
            "vtable_va": hex(e["vtable_va"]),
            "slot_count": len(slots),
            "slots_hex": [hex(s) for s in slots],
            "core": {},
        }
        for sidx, sname in CORE_SLOTS.items():
            if sidx >= len(slots):
                continue
            va = slots[sidx]
            if va in TRIVIAL_STUBS:
                t_rec["core"][sname] = {"va": hex(va), "trivial": True}
                continue
            resolved_va, thunk_note = resolve_thunk(va)
            if resolved_va in TRIVIAL_STUBS:
                t_rec["core"][sname] = {"va": hex(va), "resolved_va": hex(resolved_va), "thunk": thunk_note, "trivial": True}
                continue
            info = decompile_va(resolved_va, f"tt{tt}_{cls}_{sname}")
            if thunk_note:
                info = dict(info)
                info["slot_va"] = hex(va)
                info["thunk"] = thunk_note
            t_rec["core"][sname] = info
            # If thin wrapper (<= 25 lines), queue direct callees for 1-hop decompilation
            if info["ok"] and info["lines"] <= 25 and info["callees"]:
                for c_hex in info["callees"][:4]:
                    c_va = int(c_hex, 16)
                    if c_va not in TRIVIAL_STUBS:
                        wrapper_callees.append((c_va, f"tt{tt}_{cls}_{sname}_hop1"))
        index_tables.append(t_rec)
        s19_i = t_rec["core"].get("slot19_read_server", {})
        s2_i = t_rec["core"].get("slot02_get_prop", {})
        print(
            f"tt={tt:2d} {cls:30s} s2={s2_i.get('lines','-'):>4}L(4cc={len(s2_i.get('fourccs',[])):>3}) "
            f"s19={s19_i.get('lines','-'):>4}L",
            flush=True,
        )

    # Pass 2: decompile up to 2 hops of callees from thin wrappers (<=25 lines)
    seen_hop: set[int] = set()
    hop_results = {}
    frontier = list(wrapper_callees)
    for hop_depth in (1, 2):
        next_frontier: list[tuple[int, str]] = []
        for c_va, tag in frontier:
            r_va, tnote = resolve_thunk(c_va)
            if r_va in TRIVIAL_STUBS or r_va in seen_hop or r_va in decomp_cache:
                continue
            seen_hop.add(r_va)
            info = decompile_va(r_va, tag)
            if tnote:
                info = dict(info)
                info["thunk"] = tnote
            hop_results[hex(r_va)] = info
            print(f"  hop{hop_depth} {tag:40s} {hex(r_va)} -> {info['lines']}L ok={info['ok']}", flush=True)
            if hop_depth == 1 and info["ok"] and info["lines"] <= 25 and info["callees"]:
                for nc_hex in info["callees"][:4]:
                    nc_va = int(nc_hex, 16)
                    if nc_va not in TRIVIAL_STUBS:
                        next_frontier.append((nc_va, f"{tag}_hop2"))
        frontier = next_frontier

    idapro.close_database(False)

    # Write per-table convenient summary/links
    summary = {
        "status": "complete" if not misses else "partial",
        "elapsed_sec": round(time.time() - t0, 1),
        "tables_processed": len(index_tables),
        "unique_functions_decompiled": sum(1 for v in {id(x): x for x in decomp_cache.values()}.values() if v["ok"]),
        "misses_count": len(misses),
        "misses": misses[:50],
        "tables": index_tables,
        "hop1_functions": hop_results,
    }
    (out / "vtable_index.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        f"\nDONE in {summary['elapsed_sec']}s: tables={summary['tables_processed']} "
        f"funcs={summary['unique_functions_decompiled']} misses={summary['misses_count']}",
        flush=True,
    )
    return 0 if not misses else 1


if __name__ == "__main__":
    sys.exit(main())
