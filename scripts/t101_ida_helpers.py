"""t101 — decompile the nested read helpers reached from slot19 readers (batch 2).

Read-only static analysis with IDA Pro 9.4 idalib on a scratch copy of the
merged .i64. Nothing outside scratch/t101/ is written.

Usage:
  py -V:3.12 -I -B scripts/t101_ida_helpers.py --selftest
  py -V:3.12 -I -B scripts/t101_ida_helpers.py --va 0x141731da0 [--va ...]
  py -V:3.12 -I -B scripts/t101_ida_helpers.py --from-index      # all hop targets
Exit codes: 0 ok, 1 partial misses, 2 bad usage/fatal.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import shutil
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDA_LIB = str(_cfg.IDA_LIB_DIR)
SRC_I64 = Path(str(_cfg.IDA_DB))
DEFAULT_PE = Path(str(_cfg.EDITOR_EXE))
OUT = ROOT / "scratch/t101/ida"

# helpers reached from the batch-2 slot19 readers that t95 did not decompile
DEFAULT_VAS = [
    0x141731DA0,  # tt65/67/68/69 nested block read (a1+24)
    0x1411919D0,  # tt71/STARTING_FUTURE_TRANSFER sub-record
    0x141199360,  # tt71 prelude
    0x1415786E0,  # tt71 trailing optional sub-object
    0x140DB89D0,  # 4-byte ref wrapper
    0x140DB8980,  # 4-byte ref wrapper (tt72)
    0x141726770,  # tt72 sub-record
    0x1417266E0,  # tt72 sub-record
    0x141541000,  # tt72 date pair
    0x141541480,  # tt72 date pair
    0x14153F930,  # tt72 date pair
    0x14153F9C0,  # tt72 date pair
    0x140F82F50,  # tt72 entry
    0x1415782C0,  # tt71 sub-object body
    0x141192180,  # tt71 collection entry
    0x1411999A0,  # tt71 help (peer of 1411919D0)
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Decompile t101 nested read helpers via idalib.")
    ap.add_argument("--va", action="append", default=[], help="VA to decompile (0x...), repeatable")
    ap.add_argument("--from-index", action="store_true", help="also use DEFAULT_VAS")
    ap.add_argument("--pe", type=Path, default=DEFAULT_PE)
    ap.add_argument("--i64", type=Path, default=SRC_I64)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--selftest", action="store_true", help="no IDA: check inputs only")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    targets = [int(v, 16) if isinstance(v, str) else v for v in args.va]
    if args.from_index:
        targets = DEFAULT_VAS + targets
    targets = sorted(set(targets))

    if args.selftest:
        ok = SRC_I64.exists() and args.pe.exists() and Path(IDA_LIB).is_dir()
        print(f"i64={SRC_I64.exists()} pe={args.pe.exists()} idalib={Path(IDA_LIB).is_dir()} targets={len(targets)}")
        return 0 if ok else 1
    if not targets:
        ap.error("need --va or --from-index")

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ROOT / "scripts"))
    import t94_focus_disasm as fd  # noqa: E402

    fd.set_pe(args.pe)

    sys.path.insert(0, IDA_LIB)
    import idapro  # noqa: E402
    import ida_auto  # noqa: E402
    import ida_funcs  # noqa: E402
    import ida_hexrays  # noqa: E402
    import ida_name  # noqa: E402
    import ida_ua  # noqa: E402

    work = out / "editor_work_t101.i64"
    if not work.exists() or work.stat().st_size != args.i64.stat().st_size:
        print(f"copy {args.i64} -> {work}", flush=True)
        shutil.copy2(args.i64, work)
    t0 = time.time()
    rc = idapro.open_database(str(work), False)
    print(f"open rc={rc} {time.time()-t0:.1f}s", flush=True)
    if rc:
        return 2
    ida_auto.enable_auto(False)
    if not ida_hexrays.init_hexrays_plugin():
        print("hexrays unavailable", file=sys.stderr)
        idapro.close_database(False)
        return 2

    misses = []
    index = {}
    for va in targets:
        f = ida_funcs.get_func(va)
        if f is None:
            rec = fd.owner(va)
            if rec is None:
                misses.append({"va": hex(va), "why": "no unwind record"})
                continue
            start, end = fd.IMAGE_BASE + rec[0], fd.IMAGE_BASE + rec[1]
            ea = start
            while ea < end:
                ea += ida_ua.create_insn(ea) or 1
            ida_funcs.add_func(start, end)
            ida_auto.enable_auto(True)
            ida_auto.plan_and_wait(start, end)
            ida_auto.enable_auto(False)
            f = ida_funcs.get_func(va)
            if f is None:
                misses.append({"va": hex(va), "why": "add_func failed"})
                continue
        start = f.start_ea
        try:
            cf = ida_hexrays.decompile(start)
        except Exception:
            cf = None
        if cf is None:
            misses.append({"va": hex(va), "why": "decompile None", "tb": traceback.format_exc()[-400:]})
            continue
        text = str(cf)
        p = out / f"{start:x}.c"
        p.write_text(text, encoding="utf-8")
        index[hex(va)] = {
            "va": hex(va),
            "func_start": hex(start),
            "name": ida_name.get_name(start) or "",
            "path": str(p.relative_to(ROOT)),
            "lines": text.count("\n") + 1,
        }
        print(f"{hex(va)} -> {p.name} {index[hex(va)]['lines']}L", flush=True)

    idapro.close_database(False)
    (out / "index.json").write_text(
        json.dumps({"targets": len(targets), "ok": len(index), "misses": misses, "functions": index},
                   indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"DONE ok={len(index)}/{len(targets)} misses={len(misses)}")
    return 0 if not misses else 1


if __name__ == "__main__":
    sys.exit(main())
