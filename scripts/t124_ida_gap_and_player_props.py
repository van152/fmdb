r"""t124_ida_gap_and_player_props — Batch idalib Hex-Rays decompilation of:
  1. All undecompiled helper_va blockers from scratch/t109/out/remaining_gaps.json (Big-3 294 gaps!)
  2. Real DATABASE_OBJECT vtable slot[2]/slot[3]/slot[5] (get_prop/set_prop/reg_prop) of all 6 people_db classes
     returned by sub_1410992C0 (PLAYER 0x141879b18, NON_PLAYER 0x141877008, etc.) so we unlock all 69 PLAYER_DATA 4CCs!

Strictly read-only on D:\tmp2b\fm24\ida\editor_merge_v2.i64 (uses scratch/t95/editor_work.i64).
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import json
import re
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(_cfg.IDA_LIB_DIR))

ROOT = Path(__file__).resolve().parents[1]
WORK_I64 = ROOT / "scratch/t95/editor_work.i64"
GAP_JSON = ROOT / "scratch/t109/out/remaining_gaps.json"
OUT_DIR = ROOT / "scratch/t124/out"
FUNCS_DIR = OUT_DIR / "funcs"

PEOPLE_VTABLES = {
    "NON_PLAYER": 0x141877008,
    "PLAYER": 0x141879B18,
    "ACTUAL_PLAYER_AND_NON_PLAYER": 0x1418C5458,
    "OFFICIAL": 0x1418C0658,
    "RETIRED_PERSON": 0x14188A548,
    "JOURNALIST": 0x1418C5D68,
}


def collect_gap_helpers() -> list[tuple[str, int]]:
    txt = GAP_JSON.read_text(encoding="utf-8")
    d = json.loads(txt)
    vas: dict[int, str] = {}
    for h in d.get("top30_helper_va", []):
        va = int(h["va"], 16)
        vas[va] = f"big3_gap_top_{h['rows']}rows"
    for m in re.findall(r"0x14[0-9a-fA-F]{7}", txt):
        va = int(m, 16)
        if 0x140001000 <= va < 0x145000000:
            vas.setdefault(va, "big3_gap_ref")
    return [(tag, va) for va, tag in sorted(vas.items())]


def main() -> int:
    t0 = time.time()
    FUNCS_DIR.mkdir(parents=True, exist_ok=True)
    gap_targets = collect_gap_helpers()
    print(f"Collected {len(gap_targets)} Big-3 gap helper VAs", flush=True)

    import idapro
    idapro.open_database(str(WORK_I64), run_auto_analysis=False)
    import ida_bytes
    import ida_funcs
    import ida_hexrays
    import ida_lines
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    ida_hexrays.init_hexrays_plugin()

    def unwrap(va: int) -> int:
        cur = va
        for _ in range(5):
            raw = ida_bytes.get_bytes(cur, 32)
            if not raw:
                break
            insns = list(md.disasm(raw, cur))
            if not insns:
                break
            if insns[0].mnemonic == "jmp" and insns[0].op_str.startswith("0x"):
                cur = int(insns[0].op_str, 16)
                continue
            # Follow short this-adjuster thunks (up to 6 instructions ending in jmp 0x...)
            jumped = False
            for k in range(1, min(6, len(insns))):
                if insns[k].mnemonic == "jmp" and insns[k].op_str.startswith("0x"):
                    # Ensure no calls/branches before it
                    if all(insns[j].mnemonic not in ("call", "ret", "je", "jne", "jz", "jnz") for j in range(k)):
                        cur = int(insns[k].op_str, 16)
                        jumped = True
                        break
            if jumped:
                continue
            break
        return cur

    # Read real slot 2/3/5/21 VAs directly from editor.exe PE (ida_bytes.get_bytes misses unbacked .rdata in i64)
    import pefile
    pe = pefile.PE(str(_cfg.EDITOR_EXE), fast_load=True)
    ib = pe.OPTIONAL_HEADER.ImageBase
    people_targets: list[tuple[str, int]] = []
    for cls, vt_va in PEOPLE_VTABLES.items():
        off = pe.get_offset_from_rva(vt_va - ib)
        slots = struct.unpack_from("<22Q", pe.__data__, off)
        for slot_idx, sname in ((2, "get_prop"), (3, "set_prop"), (5, "reg_prop"), (21, "write")):
            fn_va = slots[slot_idx]
            if 0x140001000 <= fn_va < 0x145000000 and fn_va != 0x1400015B0:
                people_targets.append((f"{cls}_slot{slot_idx:02d}_{sname}", fn_va))

    all_targets = people_targets + gap_targets
    seen_real: dict[int, dict] = {}
    records = []

    for tag, va in all_targets:
        real_va = unwrap(va)
        if real_va in seen_real:
            rec = dict(seen_real[real_va])
            rec["tag"] = tag
            rec["input_va"] = hex(va)
            records.append(rec)
            continue

        out_file = FUNCS_DIR / f"{real_va:x}.c"
        # Check if already decompiled in scratch/t95/funcs or scratch/t113/out/funcs
        existing = ROOT / "scratch/t95/funcs" / f"{real_va:x}.c"
        if existing.exists():
            txt = existing.read_text(encoding="utf-8", errors="replace")
            out_file.write_text(txt, encoding="utf-8")
            rec = {
                "tag": tag, "input_va": hex(va), "real_va": hex(real_va),
                "ok": True, "lines": txt.count("\n") + 1,
                "file": str(out_file.relative_to(ROOT)), "source": "copied_t95", "err": None,
            }
            seen_real[real_va] = rec
            records.append(rec)
            continue

        if ida_funcs.get_func(real_va) is None:
            ida_funcs.add_func(real_va)

        ok = False
        lines = 0
        err = None
        try:
            cfunc = ida_hexrays.decompile(real_va)
            if cfunc is not None:
                text = "\n".join(ida_lines.tag_remove(ln.line) for ln in cfunc.get_pseudocode())
                out_file.write_text(text + "\n", encoding="utf-8")
                ok = True
                lines = text.count("\n") + 1
            else:
                err = "decompile_none"
        except Exception as exc:
            err = str(exc)

        rec = {
            "tag": tag, "input_va": hex(va), "real_va": hex(real_va),
            "ok": ok, "lines": lines, "file": str(out_file.relative_to(ROOT)), "source": "idalib", "err": err,
        }
        seen_real[real_va] = rec
        records.append(rec)
        if tag.startswith(tuple(PEOPLE_VTABLES.keys())) or not ok or lines >= 100:
            print(f"  {tag:40s} {hex(va)} -> {hex(real_va)} ok={ok} lines={lines} err={err}", flush=True)

    idapro.close_database(False)

    ok_cnt = sum(1 for r in records if r["ok"])
    uniq_ok = sum(1 for r in seen_real.values() if r["ok"])
    idx = {
        "schema_id": "fm24.t124.ida_gap_and_player_props",
        "elapsed_sec": round(time.time() - t0, 2),
        "total_targets": len(records),
        "ok_targets": ok_cnt,
        "unique_real_vas": len(seen_real),
        "unique_ok": uniq_ok,
        "records": records,
    }
    (OUT_DIR / "ida_index.json").write_text(json.dumps(idx, indent=2), encoding="utf-8")
    print(f"DONE in {time.time() - t0:.1f}s: {ok_cnt}/{len(records)} targets ({uniq_ok}/{len(seen_real)} unique VAs)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
