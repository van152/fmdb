r"""t132_ida_hop2 — Decompile:
  1. All 11 priority_undecompiled 2nd-hop VAs from scratch/t125/out/remaining_gaps_v3.json
  2. Missing sub-helpers for t112's remaining 13 skipped tables (t29 STARTING_LOAN sub_1445195D0,
     t32/t71 sub_1411919D0, t71 sub_1415782C0, t72 sub_141541000/141541480/141726770,
     t36 sub_14145xxx, plus CLUB/COMP/NTC/NATIONAL_TEAM callees).

Strictly uses scratch/t95/editor_work.i64 (never modifies editor_merge_v2.i64).
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(_cfg.IDA_LIB_DIR))

ROOT = Path(__file__).resolve().parents[1]
WORK_I64 = ROOT / "scratch/t95/editor_work.i64"
OUT_DIR = ROOT / "scratch/t132/out"
FUNCS_DIR = OUT_DIR / "funcs"

TARGETS = [
    # t125 Big-3 2nd-hop priority_undecompiled (11 VAs)
    ("big3_hop2_38gaps", 0x14083DFA0),
    ("big3_hop2_4gaps", 0x1411EACB0),
    ("big3_hop2_3gaps", 0x144026350),
    ("big3_hop2_2gaps", 0x1407E4490),
    ("big3_hop2_1gap_a", 0x14083B0A0),
    ("big3_hop2_1gap_b", 0x14083DB80),
    ("big3_hop2_1gap_c", 0x140E58670),
    ("big3_hop2_1gap_d", 0x140E5F8C0),
    ("big3_hop2_1gap_e", 0x140FC9D50),
    ("big3_hop2_1gap_f", 0x141078DE0),
    ("big3_hop2_1gap_g", 0x141521AA0),
    # Missing helpers for t112's 13 remaining tables
    ("t29_loan_sub", 0x1445195D0),
    ("t32_t71_shared_sub", 0x1411919D0),
    ("t71_sub_1415782C0", 0x1415782C0),
    ("t72_sub_141541000", 0x141541000),
    ("t72_sub_141541480", 0x141541480),
    ("t72_sub_141726770", 0x141726770),
    ("t72_sub_1443E8FD0", 0x1443E8FD0),
    # Also scan t24 NATIONAL_TEAM & t36 HOF & t3 CLUB & t9 NTC top callees if missing
    ("t24_nt_s19", 0x14103B420),
    ("t36_hof_s19", 0x141455260),
]


def main() -> int:
    t0 = time.time()
    FUNCS_DIR.mkdir(parents=True, exist_ok=True)
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
            break
        return cur

    records = []
    for tag, va in TARGETS:
        real_va = unwrap(va)
        out_file = FUNCS_DIR / f"{real_va:x}.c"
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
            "ok": ok, "lines": lines, "file": str(out_file.relative_to(ROOT)), "err": err,
        }
        records.append(rec)
        print(f"  {tag:24s} {hex(va)} -> {hex(real_va)} ok={ok} lines={lines} err={err}", flush=True)

    idapro.close_database(False)
    (OUT_DIR / "ida_hop2_index.json").write_text(
        json.dumps({"elapsed_sec": round(time.time() - t0, 2), "records": records}, indent=2),
        encoding="utf-8",
    )
    ok_cnt = sum(1 for r in records if r["ok"])
    print(f"DONE in {time.time() - t0:.1f}s: {ok_cnt}/{len(records)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
