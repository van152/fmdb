"""t138_ida_callees — idalib Hex-Rays decompilation of every function that participates in the
people_db.dat slot19 wire-read grammar (direct callees + containing functions of every read
caller VA seen in the t120 Unicorn samples).

Works strictly on scratch/t95/editor_work.i64 (never touches editor_merge_v2.i64).
Writes decompilations to scratch/t138/out/ida/<funcva>.c and an index json.
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
OUT_DIR = ROOT / "scratch/t138/out/ida"

# Known direct callees of the six slot19 readers (plus flush helpers).
DIRECT = [
    0x140DD8520,  # PLAYER/NON_PLAYER tail part 1 (0x140dd8520)
    0x140DFB5C0,  # PLAYER/NON_PLAYER/OFFICIAL tail part 2
    0x14145D260,  # PLAYER near-tail
    0x1415F6ED0,  # CONTRACT sub-read 1
    0x14172A440,  # CONTRACT optional 1
    0x14145E300,  # CONTRACT optional 2
    0x14172A120,  # CONTRACT optional 3
    0x14146E9F0,  # CONTRACT tail
    0x1413C40A0,  # career temp-object ctor
    0x14096BA90,  # OFFICIAL optional object read
    0x140DC3060,  # NON_PLAYER club-history loop helper
    0x140DC33A0,  # NON_PLAYER helper
    0x1413F97A0,  # NON_PLAYER conditional (old)
    0x1413F90A0,  # NON_PLAYER conditional (new)
    0x1413FE0E0,  # NON_PLAYER optional obj 1
    0x1413FE6B0,  # NON_PLAYER optional obj 2
    0x1413FECE0,  # NON_PLAYER optional obj 3
    0x1413FF240,  # NON_PLAYER optional obj 4
    0x140DC3550,  # alloc helper
    0x140DC3600,  # alloc helper
    0x140DC36B0,  # helper
    0x140DC3790,  # NON_PLAYER post (version<=0xDE2)
    0x140DC4DB0,  # NON_PLAYER post helper
    0x140E01FF0,  # NON_PLAYER version<=0xDDB
    0x14121A480,  # RETIRED prep
    0x1412E70A0,  # stream flush A
    0x1412E6FF0,  # stream flush B
    0x141084540,  # PERSON slot19 base (thunk?)
    0x143F2B820,  # PERSON base body
    0x14146AD40,  # PLAYER conditional obj 1
    0x14144AD70,  # PLAYER conditional obj 2
    0x14146D370,  # PLAYER conditional obj 3
    0x140E06080,  # PLAYER conditional obj 4
    0x140E07FB0,  # PLAYER alloc
    0x140E08060,  # PLAYER helper
    0x140E06E90,  # PLAYER helper
    0x140E080A0,  # PLAYER helper
    0x140E08120,  # PLAYER alloc
    0x14144AD20,  # PLAYER init
    0x140E081D0,  # PLAYER alloc
    0x140E40630,  # PLAYER move
    0x140E08430,  # PLAYER init
    0x140E08640,  # PLAYER alloc
    0x14087A360,  # position-validity check helper
    0x14371BDF0,  # string reader variant
    0x140814B10,  # string reader
    # round 2 — branch bodies surfaced while aligning the full 673B PLAYER trace
    0x14145CE40,  # called by sub_140E06080 (PLAYER u8!=0 branch)
    0x14103ACF0,  # career case1 vtable setter (sub_140EE7C20 case 1)
    0x141727D70,  # callee of sub_141727C60 (case0 obj chain)
    0x14141D290,  # callee of sub_141727790
    0x140F80B80,  # callee of sub_141727790
    0x1413C4990,  # career case6 tail
    # round 4 — basic_people_db wrapper chain (same tad. family container;
    # the walker may reveal the container footer grammar on the SAVE side)
    0x140F2FE70,  # basic_people_db walker (called from sub_140F566E0)
    0x140F237E0,  # prep called at sub_140F566E0 entry
    0x140FFAFD0,  # family footer/index reader (tail of sub_140F2FE70)
    0x140F50EC0,  # save orchestrator commit helper (a8=18) — container tail writer?
    0x140F59C40,  # save orchestrator tail helper
    # round 3 — leaves under the round-2 bodies
    0x14145C5A0,  # under sub_14145CE40
    0x14145C700,  # under sub_14145CE40 (x7)
    0x141727530,  # under sub_14141D290
    0x14103B0D0,  # career case1 object vtable(0x141889138) slot4 reader
    0x14156ADD0,  # under sub_141727D70 element loop
    0x14145CF20,  # under sub_14145C5A0 (validate?)
    0x141454210,  # under sub_141727530 (v16<3 path)
    0x141454230,  # under sub_141727530 (v16<3 path)
    0x14156AF70,  # under sub_14103B0D0 element loop
    0x141441770,  # under sub_14103B0D0 (175-byte obj)
    0x1414C4670,  # sub_140EDFB90 count-loop element reader
    0x1413F94B0,  # element of sub_1413F90A0/sub_1413F97A0 vectors
    0x1408386A0,  # element of sub_14145E300 (CONTRACT v59 vector)
    0x140F938D0,  # under sub_14146D370 (v81<=25 DB-ref vector)
    0x14146DE90,  # under sub_14146D370 tail
    0x14146CFC0,  # under sub_14146D370 tail (v82!=0)
    0x14141F7B0,  # under sub_14146D370 tail
    0x140F83460,  # sub_14146D370 element REF4 path
    0x140F92E30,  # under sub_140F80B80 complex path
    0x140F92AB0,  # under sub_140F80B80 complex path
    0x141470930,  # sub_14146AD40 case readers
    0x141470F40,
    0x1413C60C0,
    0x1413C62C0,
    0x14146B8B0,
    0x14146BA90,
    0x14146BD20,
    0x14146BF70,
    0x14146CD70,  # ctor helpers (may read)
    0x14146CE20,
]

# Functions whose xrefs we enumerate to find the row-loop / footer walker
# (factory sub_1410992C0 is called once per row by the people_db stream walker).
XREF_PROBE_VAS = [
    0x1410992C0,  # people factory: person_type -> obj (vtable slot19 reader)
    0x140F64530,  # people_db stage machine (rows + case3 tables + cleanup)
    0x141438DB0,  # case3 pass-1 element reader (type id 14)
    0x141454370,  # case3 pass-2 element reader (type id 44)
    0x1418E2C24,  # "people_db" section name string (writers/readers of the section)
]

# Round 4 — find the people_db WRITER (the 28-byte footer after the last row is
# written by the save path, never read by the load path we already decompiled).
# Probe: code refs to the named-section opener + every function that references
# the "people_db" string as DATA (code refs were already probed above).
XREF_PROBE_VAS_ROUND4 = [
    0x1407D0F70,  # named-section opener (reader side); callers include save paths
]

# Every read caller VA observed in t120 samples (all 5 types).
CALLER_VAS = [
    0x14096bbd8, 0x14096bf7a, 0x140dc1dd9, 0x140dc213a, 0x140dc21a3, 0x140dc21c8,
    0x140dc227a, 0x140dc235c, 0x140dc2388, 0x140dc23fd, 0x140dc2436, 0x140dc2469,
    0x140dc2559, 0x140dc2652, 0x140dc2753, 0x140dc2847, 0x140dc29ff, 0x140dc2bf8,
    0x140dc2ea1, 0x140dd85d5, 0x140dd8604, 0x140dd862a, 0x140dd8654, 0x140dd8676,
    0x140dd86a4, 0x140dd86d2, 0x140dd8705, 0x140dd8788, 0x140dd8c37, 0x140dd8c64,
    0x140dd8d40, 0x140dd8f1b, 0x140dd983b, 0x140dd9a99, 0x140dd9c90, 0x140dda03c,
    0x140dda123, 0x140dda41a, 0x140dda44a, 0x140dda47b, 0x140dda4af, 0x140dda4ea,
    0x140dda51b, 0x140dda547, 0x140dda57f, 0x140dda5ab, 0x140dfb6ba, 0x140dfb75b,
    0x140dfb863, 0x140dfb8ae, 0x140dfb92c, 0x140dfb9fc, 0x140dfba3d, 0x140dfbb2f,
    0x140e06f71, 0x140e06f9d, 0x140e06fd3, 0x140e06fff, 0x140e07068, 0x140e07094,
    0x140e070c1, 0x140e0711e, 0x140e07152, 0x140e071e6, 0x140e0720e, 0x140e0723a,
    0x140e072ac, 0x140e072d0, 0x140e072f4, 0x140e07318, 0x140e073ae, 0x140e073f4,
    0x140e0756e, 0x140e075df, 0x140e07652, 0x140e076fc, 0x140e079c6, 0x140e07b4f,
    0x140e07c5b, 0x140e07d16, 0x140e07ed9, 0x140edf6fb, 0x140edf7ae, 0x140edf809,
    0x140edf8ae, 0x140edf92f, 0x140edf9b0, 0x140edfbfb, 0x140edfc30, 0x140edfc84,
    0x140edfcc5, 0x140ee0013, 0x140ee0044, 0x140ee0075, 0x140ee00a1, 0x140ee00ca,
    0x140ee00f3, 0x1412e7024, 0x1413fed0d, 0x1413fee71, 0x1413fee90, 0x141400269,
    0x141400324, 0x141400337, 0x141400666, 0x141400687, 0x1414006b2, 0x1414006d3,
    0x1414006f4, 0x141400715, 0x141400804, 0x1414210fd, 0x1414211c9, 0x14142122a,
    0x141421270, 0x1414212a1, 0x1414212d8, 0x141421865, 0x141421956, 0x141421ae9,
    0x14145d296, 0x14145d2e0, 0x14145d322, 0x14145d3c1, 0x14145d4cf, 0x14145d4fd,
    0x14145d594, 0x14145d623, 0x14145d645, 0x14145d667, 0x14145f840, 0x14145f86c,
    0x14145f92e, 0x14145f9f7, 0x14145fd74, 0x14145fe41, 0x14145feeb, 0x14145ff1d,
    0x14145ff2f, 0x14145ffdf, 0x141460009, 0x14146002b, 0x141460051, 0x14146d39d,
    0x14146d3bd, 0x14146d3e3, 0x14146db77, 0x14146dc47, 0x14146dc6b, 0x14146dd04,
    0x14146dd2c, 0x14146dd76, 0x14146dd9a, 0x14146ddbe, 0x14146dddf, 0x14146de1a,
    0x14151d795, 0x14158571c, 0x14158573c, 0x14158575c, 0x14158577c, 0x14158579c,
    0x1415857bc, 0x1415857dc, 0x1415857fc, 0x14158581c, 0x14158583c, 0x141585858,
    0x141585874, 0x141585890, 0x1415858b2, 0x141585c44, 0x141585c78, 0x143b48dd7,
    0x143b93527, 0x143b93569, 0x143c07dab, 0x143c07dfe, 0x143c07e10, 0x143eb4efc,
    0x143eb4f2b, 0x143eb4f56, 0x143eb4f8b, 0x143eb4fb9, 0x143f2b84d, 0x143f2b88a,
    0x143f89207, 0x143f8921f, 0x14412d653, 0x1442ffc08, 0x1442ffc24, 0x1442ffc4d,
    0x1442ffc72, 0x14432a60d, 0x14432a63d, 0x14432a683, 0x14432a6fa, 0x14432a7c0,
    0x14432ad95, 0x14432adbe, 0x14432adf2, 0x14432ae1b, 0x14432ae4b, 0x14432ae7a,
    0x14439f215, 0x14439f234, 0x14439f25d, 0x14439f29a, 0x14439f2ca, 0x14439f2e6,
    0x14439f302, 0x14439f31e, 0x14439f348, 0x1443a1194, 0x1443a11b4, 0x1443a11d3,
    0x1443a11ef, 0x1443a120b, 0x1443a1227, 0x1443a1243, 0x1443a1270, 0x1443a128c,
    0x1443a12a8, 0x1443a12c7, 0x14447e099, 0x14447e0e3, 0x14447e794, 0x14447e7b3,
    0x14447e7d3, 0x14447e7f5, 0x14447e82c, 0x1446580d4, 0x144658164,
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
        for _ in range(6):
            raw = ida_bytes.get_bytes(cur, 30)
            if not raw:
                break
            insns = list(md.disasm(raw, cur))
            if not insns:
                break
            if insns[0].mnemonic == "jmp" and insns[0].op_str.startswith("0x"):
                cur = int(insns[0].op_str, 16)
                continue
            if len(insns) >= 5 and insns[4].mnemonic == "jmp" and insns[4].op_str.startswith("0x"):
                cur = int(insns[4].op_str, 16)
                continue
            break
        return cur

    ida_hexrays.init_hexrays_plugin()

    # Map every caller VA to its containing function start.
    targets: dict[int, str] = {}
    for va in DIRECT:
        targets[unwrap(va)] = f"direct_{va:x}"
    for cva in CALLER_VAS:
        f = ida_funcs.get_func(cva)
        if f is None:
            print(f"  caller {hex(cva)}: NO FUNC", flush=True)
            continue
        start = unwrap(f.start_ea)
        targets.setdefault(start, f"caller_{cva:x}")

    # Xref probe: decompile every function that calls the probe VAs (row loop / footer).
    import idautils
    for pva in XREF_PROBE_VAS:
        n = 0
        for xr in idautils.CodeRefsTo(pva, 0):
            f = ida_funcs.get_func(xr)
            if f is None:
                print(f"  xref {hex(xr)} -> {hex(pva)}: NO FUNC", flush=True)
                continue
            start = unwrap(f.start_ea)
            if targets.setdefault(start, f"xref_{pva:x}_at_{xr:x}") == f"xref_{pva:x}_at_{xr:x}":
                print(f"  xref caller {hex(start)} (call site {hex(xr)})", flush=True)
            n += 1
        print(f"  xref probe {hex(pva)}: {n} refs", flush=True)

    # Round 4: data refs to the "people_db" string (finds the writer) + code refs
    # to the named-section opener (save paths call the same section machinery).
    for xr in idautils.DataRefsTo(0x1418E2C24):
        f = ida_funcs.get_func(xr)
        if f is None:
            print(f"  dataref {hex(xr)} -> people_db string: NO FUNC", flush=True)
            continue
        start = unwrap(f.start_ea)
        if targets.setdefault(start, f"dataref_people_db_at_{xr:x}") == f"dataref_people_db_at_{xr:x}":
            print(f"  dataref caller {hex(start)} (site {hex(xr)})", flush=True)
    for pva in XREF_PROBE_VAS_ROUND4:
        n = 0
        for xr in idautils.CodeRefsTo(pva, 0):
            f = ida_funcs.get_func(xr)
            if f is None:
                print(f"  xref {hex(xr)} -> {hex(pva)}: NO FUNC", flush=True)
                continue
            start = unwrap(f.start_ea)
            if targets.setdefault(start, f"xref_{pva:x}_at_{xr:x}") == f"xref_{pva:x}_at_{xr:x}":
                print(f"  opener xref caller {hex(start)} (site {hex(xr)})", flush=True)
            n += 1
        print(f"  opener xref probe {hex(pva)}: {n} refs", flush=True)

    summary = []
    for real_va, why in sorted(targets.items()):
        f = ida_funcs.get_func(real_va)
        if f is None:
            ida_funcs.add_func(real_va)
            f = ida_funcs.get_func(real_va)
        ok = False
        lines = 0
        err = None
        out_file = OUT_DIR / f"{real_va:x}.c"
        if out_file.exists():
            ok = True
            lines = out_file.read_text(encoding="utf-8", errors="replace").count("\n") + 1
            summary.append({"va": hex(real_va), "why": why, "ok": ok, "lines": lines, "cached": True})
            continue
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
        summary.append({"va": hex(real_va), "why": why, "ok": ok, "lines": lines, "err": err})
        print(f"  {hex(real_va):>14s} ({why}) ok={ok} lines={lines} {err or ''}", flush=True)

    idapro.close_database(False)
    idx_path = OUT_DIR / "index.json"
    idx_path.write_text(json.dumps({"elapsed_sec": round(time.time() - t0, 2), "targets": summary}, indent=2),
                        encoding="utf-8")
    n_ok = sum(1 for s in summary if s["ok"])
    print(f"Done: {n_ok}/{len(summary)} decompiled in {time.time() - t0:.1f}s -> {idx_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
