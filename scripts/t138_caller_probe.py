"""t138_caller_probe — disassemble context around each wire-read caller VA so every read in the
t120 traces can be pinned to its exact C statement."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import json
import sys
from pathlib import Path

sys.path.insert(0, str(_cfg.IDA_LIB_DIR))

ROOT = Path(__file__).resolve().parents[1]
WORK_I64 = ROOT / "scratch/t95/editor_work.i64"
OUT = ROOT / "scratch/t138/out/caller_context.json"

CALLERS = [
    0x140dd85d5, 0x140dd8604, 0x140dd862a, 0x140dd8654, 0x140dd8676, 0x140dd86a4,
    0x140dd86d2, 0x140dd8705, 0x140dd8788, 0x140dd8c37, 0x140dd8c64, 0x140dd8d40,
    0x140dd8f1b, 0x140dd983b, 0x140dd9a99, 0x140dd9c90, 0x140dda03c, 0x140dda123,
    0x140dda41a, 0x140dda44a, 0x140dda47b, 0x140dda4af, 0x140dda4ea, 0x140dda51b,
    0x140dda547, 0x140dda57f, 0x140dda5ab, 0x140dc2ea1, 0x140e07d16, 0x140e07ed9,
    0x1413fed0d, 0x1413fee71, 0x1413fee90, 0x141400666, 0x14146d39d, 0x14146db77,
    0x14151d795, 0x143b48dd7, 0x14432a60d, 0x14439f215,
]


def main() -> int:
    import idapro
    idapro.open_database(str(WORK_I64), run_auto_analysis=False)
    import ida_ua
    import ida_lines
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    out = {}
    for cva in CALLERS:
        # walk back up to 160 bytes, decode forward, keep last 12 insns ending at cva
        start = cva - 0x60
        best = []
        for s in range(start, cva):
            ins = []
            pc = s
            ok = True
            while pc < cva:
                raw = ida_bytes.get_bytes(pc, 16) if False else None
                try:
                    raw = ida_bytes.get_bytes(pc, 15)
                except Exception:
                    ok = False
                    break
                if not raw:
                    ok = False
                    break
                try:
                    i = next(md.disasm(raw, pc))
                except StopIteration:
                    ok = False
                    break
                ins.append(f"{i.mnemonic} {i.op_str}")
                pc += i.size
                if len(ins) > 40:
                    ok = False
                    break
            if ok and pc == cva and ins:
                best = ins[-14:]
        out[hex(cva)] = best
        print(f"{hex(cva)}: " + " | ".join(best[-6:]), flush=True)
    idapro.close_database(False)
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"saved -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
