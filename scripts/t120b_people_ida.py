"""t120b_people_ida — Targeted idalib Hex-Rays decompilation of all 6 people_db.dat slot19 readers + PERSON base + sub_14145F800.

Works strictly on scratch/t95/editor_work.i64 (never touches D:\tmp2b\fm24\ida\editor_merge_v2.i64).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")

ROOT = Path(__file__).resolve().parents[1]
WORK_I64 = ROOT / "scratch/t95/editor_work.i64"
OUT_DIR = ROOT / "scratch/t120/out/funcs"

TARGETS = [
    ("PLAYER_slot19_body", 0x140E06EC0),
    ("PLAYER_sub_14145F800", 0x14145F800),
    ("NON_PLAYER_slot19_body", 0x140DC1D30),
    ("ACTUAL_PLAYER_AND_NON_PLAYER_slot19", 0x1415D5110),
    ("OFFICIAL_slot19", 0x1415856B0),
    ("RETIRED_PERSON_slot19", 0x143F891C0),
    ("JOURNALIST_slot19", 0x1415D8630),
    ("PERSON_slot19_base", 0x141084540),
    ("PERSON_slot21_write", 0x141084680),
    ("PLAYER_slot19_v2", 0x143BECCD0),
    ("ACTUAL_PLAYER_get_prop", 0x140E1C630),
    ("ACTUAL_PLAYER_set_prop", 0x140E0F380),
    ("PLAYER_ctor", 0x140E06100),
]


def main() -> int:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    import idapro
    idapro.open_database(str(WORK_I64), run_auto_analysis=False)
    import ida_funcs
    import ida_hexrays
    import ida_lines
    import ida_bytes
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64

    md = Cs(CS_ARCH_X86, CS_MODE_64)

    def unwrap(va: int) -> int:
        cur = va
        for _ in range(4):
            raw = ida_bytes.get_bytes(cur, 20)
            if not raw:
                break
            insns = list(md.disasm(raw, cur))
            if not insns:
                break
            if insns[0].mnemonic == "jmp" and insns[0].op_str.startswith("0x"):
                cur = int(insns[0].op_str, 16)
                continue
            # Check this-adjust thunk: xor eax,eax; sub eax,[rcx-4]; cdqe; add rcx,rax; jmp target
            if len(insns) >= 5 and insns[4].mnemonic == "jmp" and insns[4].op_str.startswith("0x"):
                cur = int(insns[4].op_str, 16)
                continue
            break
        return cur

    ida_hexrays.init_hexrays_plugin()
    summary = []
    for tag, va in TARGETS:
        real_va = unwrap(va)
        f = ida_funcs.get_func(real_va)
        if f is None:
            ida_funcs.add_func(real_va)
            f = ida_funcs.get_func(real_va)
        ok = False
        lines = 0
        out_file = OUT_DIR / f"{real_va:x}.c"
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
            "ok": ok, "lines": lines, "file": str(out_file.relative_to(ROOT)), "err": err,
        }
        summary.append(rec)
        print(f"  {tag:36s} {hex(va)} -> {hex(real_va)} ok={ok} lines={lines} err={err}", flush=True)

    idapro.close_database(False)
    idx_path = OUT_DIR.parent / "people_ida_p0_index.json"
    idx_path.write_text(json.dumps({"elapsed_sec": round(time.time() - t0, 2), "targets": summary}, indent=2), encoding="utf-8")
    print(f"Done in {time.time() - t0:.1f}s -> {idx_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
