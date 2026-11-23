"""t113b_people_ida — Scan all db::* person-hierarchy vtables in editor.exe and decompile via IDA 9.4 idalib.

Finds PERSON, BASIC_PERSON, PLAYER, ACTUAL_PLAYER, NON_PLAYER, ACTUAL_NON_PLAYER,
ACTUAL_PLAYER_AND_NON_PLAYER, OFFICIAL, JOURNALIST, SPOKESPERSON, HUMAN_NON_PLAYER,
VIRTUAL_PLAYER, AGENT, CONTRACT, PLAYER_DATA, etc. in the `db::` namespace, plus
factory sub_1410992C0, and decompiles slot02/slot03/slot19/slot20/slot21 with thunk unwrapping.

Usage:
  py -V:3.12 -I -B scripts/t113b_people_ida.py --selftest
  py -V:3.12 -I -B scripts/t113b_people_ida.py
Exit codes: 0 ok, 1 partial, 2 fatal.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDA_LIB = r"C:\Program Files\IDA Professional 9.4\idalib\python"
WORK_I64 = ROOT / "scratch/t95/editor_work.i64"
DEFAULT_PE = Path(r"D:\tmp2b\fm24\input\editor.exe")
OUT_DIR = ROOT / "scratch/t113/out"
FUNCS_DIR = OUT_DIR / "funcs"

TARGET_CLASS_PAT = re.compile(
    r"^(?:BASIC_PERSON|PERSON|PLAYER|ACTUAL_PLAYER|NON_PLAYER|ACTUAL_NON_PLAYER|"
    r"ACTUAL_PLAYER_AND_NON_PLAYER|HUMAN_NON_PLAYER|VIRTUAL_PLAYER|"
    r"OFFICIAL|JOURNALIST|SPOKESPERSON|AGENT|HUMAN|"
    r"PLAYER_DATA|NON_PLAYER_DATA|PERSON_DATA|INTERNATIONAL_PLAYER_DATA|"
    r"CONTRACT|PLAYER_CONTRACT|NON_PLAYER_CONTRACT|STAFF|DIRECTOR|CHAIRPERSON)$"
)

CORE_SLOTS = {
    2: "slot02_get_prop",
    3: "slot03_set_prop",
    5: "slot05_reg_prop",
    19: "slot19_read_server",
    20: "slot20_read_client",
    21: "slot21_write",
}

TRIVIAL_STUBS = {
    0x1400015A0, 0x1400015B0, 0x1400015E0, 0x1407EB2D0,
    0x140DD2B10, 0x140DD2B30, 0x140DD2B40, 0x140DD5500,
    0x140843500, 0x140FE6F80, 0x140FE7190,
}


def scan_db_person_vtables(pe_path: Path) -> list[dict]:
    sys.path.insert(0, r"D:\tmp2b\tools\python")
    import pefile  # noqa: E402

    pe = pefile.PE(str(pe_path), fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    raw = pe_path.read_bytes()
    secs = [(s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData) for s in pe.sections]

    def fo_to_rva(fo: int) -> int | None:
        for va_s, sz_s, fo_s in secs:
            if fo_s <= fo < fo_s + sz_s:
                return va_s + (fo - fo_s)
        return None

    pat = re.compile(rb"\.\?AV([A-Za-z0-9_]+)@db@@\x00")
    td_map: dict[int, str] = {}
    for m in pat.finditer(raw):
        cls = m.group(1).decode("ascii", errors="ignore")
        if TARGET_CLASS_PAT.match(cls):
            td_rva = fo_to_rva(m.start() - 16)
            if td_rva:
                td_map[td_rva] = cls

    col_map: dict[int, str] = {}
    for td_rva, cls in td_map.items():
        # Match sig=1, offset=0, cdOffset=0, pTypeDescriptor=td_rva
        needle = struct.pack("<IIII", 1, 0, 0, td_rva)
        pos = 0
        while True:
            idx = raw.find(needle, pos)
            if idx < 0:
                break
            col_rva = fo_to_rva(idx)
            if col_rva:
                col_map[base + col_rva] = cls
            pos = idx + 4

    out: list[dict] = []
    seen_vt: set[int] = set()
    for col_va, cls in col_map.items():
        needle = struct.pack("<Q", col_va)
        pos = 0
        while True:
            idx = raw.find(needle, pos)
            if idx < 0:
                break
            vt_rva = fo_to_rva(idx + 8)
            if vt_rva:
                vt_va = base + vt_rva
                if vt_va not in seen_vt and idx + 8 + 32 * 8 <= len(raw):
                    slots_raw = struct.unpack_from("<32Q", raw, idx + 8)
                    slots = []
                    for s in slots_raw:
                        if 0x140000000 <= s < 0x145000000:
                            slots.append(s)
                        else:
                            break
                    if len(slots) >= 20:
                        seen_vt.add(vt_va)
                        out.append({
                            "class": cls,
                            "vtable_va": hex(vt_va),
                            "slot_count": len(slots),
                            "slots": [hex(s) for s in slots],
                        })
            pos = idx + 8
    out.sort(key=lambda x: (x["class"], x["vtable_va"]))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Decompile db::* person hierarchy vtables via IDA 9.4 idalib.")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    vtables = scan_db_person_vtables(DEFAULT_PE)
    if args.selftest:
        print(f"Found {len(vtables)} db:: person-hierarchy vtables:")
        for v in vtables:
            s2 = v["slots"][2] if len(v["slots"]) > 2 else "-"
            s19 = v["slots"][19] if len(v["slots"]) > 19 else "-"
            print(f"  {v['class']:32s} vt={v['vtable_va']} slots={v['slot_count']:2d} s2={s2} s19={s19}")
        return 0 if len(vtables) >= 5 else 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FUNCS_DIR.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import t94_focus_disasm as fd  # noqa: E402
    import t95_ida_vtables as vlib  # noqa: E402

    fd.set_pe(DEFAULT_PE)
    _, _, resolve_thunk = vlib.load_pe_vtable_reader(DEFAULT_PE)

    sys.path.insert(0, IDA_LIB)
    import idapro  # noqa: E402
    import ida_auto  # noqa: E402
    import ida_funcs  # noqa: E402
    import ida_hexrays  # noqa: E402
    import ida_name  # noqa: E402
    import ida_ua  # noqa: E402

    t0 = time.time()
    rc = idapro.open_database(str(WORK_I64), False)
    if rc:
        return 2
    ida_auto.enable_auto(False)
    if not ida_hexrays.init_hexrays_plugin():
        idapro.close_database(False)
        return 2

    def ensure_func(va: int) -> int:
        f = ida_funcs.get_func(va)
        if f is not None:
            return f.start_ea
        rec = fd.owner(va)
        if rec:
            start, end = fd.IMAGE_BASE + rec[0], fd.IMAGE_BASE + rec[1]
            ea = start
            while ea < end:
                ea += ida_ua.create_insn(ea) or 1
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

    cache: dict[int, dict] = {}
    misses = []

    def decompile_va(orig_va: int, tag: str) -> dict:
        r_va, tnote = resolve_thunk(orig_va)
        if r_va in cache:
            rec = dict(cache[r_va])
            rec["slot_va"] = hex(orig_va)
            if tnote:
                rec["thunk"] = tnote
            return rec
        start = ensure_func(r_va)
        if start in cache:
            rec = dict(cache[start])
            rec["slot_va"] = hex(orig_va)
            if tnote:
                rec["thunk"] = tnote
            cache[r_va] = cache[start]
            return rec
        info = {
            "slot_va": hex(orig_va),
            "func_start": hex(start),
            "name": ida_name.get_name(start) or f"sub_{start:x}",
            "thunk": tnote,
            "ok": False,
            "lines": 0,
            "fourccs": [],
            "callees": [],
            "file": f"funcs/{start:x}.c",
        }
        try:
            cfunc = ida_hexrays.decompile(start, flags=ida_hexrays.DECOMP_NO_WAIT)
            if cfunc is None:
                cfunc = ida_hexrays.decompile(start)
            if cfunc is not None:
                txt = str(cfunc)
                (FUNCS_DIR / f"{start:x}.c").write_text(txt, encoding="utf-8")
                info["ok"] = True
                info["lines"] = txt.count("\n") + 1
                info["fourccs"] = vlib.extract_4ccs_from_text(txt)
                info["callees"] = [hex(c) for c in vlib.extract_callees_from_text(txt) if c != start]
            else:
                misses.append({"va": hex(orig_va), "tag": tag, "why": "None"})
        except Exception as exc:
            misses.append({"va": hex(orig_va), "tag": tag, "why": str(exc)})
        cache[start] = info
        cache[r_va] = info
        return info

    # 1. Decompile person subclass factory sub_1410992C0
    factory_info = decompile_va(0x1410992C0, "person_factory_1410992C0")
    print(f"Factory 0x1410992C0: ok={factory_info['ok']} lines={factory_info['lines']}", flush=True)

    # 2. Decompile all core slots of all db:: person-hierarchy vtables + 1-hop wrappers
    hops = []
    for v in vtables:
        v["core"] = {}
        for sidx, sname in CORE_SLOTS.items():
            if sidx >= len(v["slots"]):
                continue
            va = int(v["slots"][sidx], 16)
            if va in TRIVIAL_STUBS:
                v["core"][sname] = {"va": hex(va), "trivial": True}
                continue
            info = decompile_va(va, f"{v['class']}_{sname}")
            v["core"][sname] = info
            if info["ok"] and info["lines"] <= 25 and info["callees"]:
                for ch in info["callees"][:3]:
                    cva = int(ch, 16)
                    if cva not in TRIVIAL_STUBS:
                        hops.append((cva, f"{v['class']}_{sname}_hop1"))
        s2 = v["core"].get("slot02_get_prop", {})
        s19 = v["core"].get("slot19_read_server", {})
        print(
            f"  {v['class']:32s} s2={s2.get('lines','-'):>4}L(4cc={len(s2.get('fourccs',[])):>3}) "
            f"s19={s19.get('lines','-'):>4}L",
            flush=True,
        )

    hop_map = {}
    for cva, tag in hops:
        info = decompile_va(cva, tag)
        hop_map[hex(cva)] = info

    idapro.close_database(False)

    all_4cc = set()
    for v in vtables:
        for info in v["core"].values():
            if isinstance(info, dict):
                all_4cc.update(info.get("fourccs", []))
    for info in hop_map.values():
        all_4cc.update(info.get("fourccs", []))

    summary = {
        "status": "complete" if not misses else "partial",
        "elapsed_sec": round(time.time() - t0, 1),
        "vtable_count": len(vtables),
        "unique_4ccs": len(all_4cc),
        "misses_count": len(misses),
        "misses": misses,
        "factory_1410992C0": factory_info,
        "vtables": vtables,
        "hop1_functions": hop_map,
    }
    (OUT_DIR / "people_vtables_full.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDONE t113b in {summary['elapsed_sec']}s: vtables={len(vtables)} 4CCs={len(all_4cc)} misses={len(misses)}", flush=True)
    return 0 if not misses else 1


if __name__ == "__main__":
    sys.exit(main())
