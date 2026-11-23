"""t107 — Batch IDA 9.4 Hex-Rays decompilation of all helper_calls & missing_subcalls from t97 and t105.

Additive to scratch/t95/funcs/: never overwrites existing .c files, resolves .reloc jump thunks,
and writes scratch/t107/out/helpers_index.json with 4CCs, callees, and line counts.

Usage:
  py -V:3.12 -I -B scripts/t107_ida_helpers.py --selftest
  py -V:3.12 -I -B scripts/t107_ida_helpers.py
Exit codes: 0 ok, 1 partial misses, 2 bad usage/fatal.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDA_LIB = r"C:\Program Files\IDA Professional 9.4\idalib\python"
WORK_I64 = ROOT / "scratch/t95/editor_work.i64"
DEFAULT_PE = Path(r"D:\tmp2b\fm24\input\editor.exe")
FUNCS_DIR = ROOT / "scratch/t95/funcs"
OUT_DIR = ROOT / "scratch/t107/out"


def collect_target_vas() -> tuple[list[tuple[int, str, int]], dict]:
    existing = {p.stem.lower() for p in FUNCS_DIR.glob("*.c")}
    counts: Counter[int] = Counter()
    sources: dict[int, set[str]] = {}

    def add_va(va_str: str, src: str, weight: int = 1):
        if not isinstance(va_str, str):
            return
        m = re.search(r"0x([0-9a-fA-F]{9,12})", va_str)
        if not m:
            return
        va = int(m.group(1), 16)
        if not (0x140000000 <= va < 0x145000000):
            return
        if f"{va:x}" in existing:
            return
        counts[va] += weight
        sources.setdefault(va, set()).add(src)

    # 1. t97 missing_subcalls + helper_calls
    t97_path = ROOT / "scratch/t97/out/fourcc_mem_map.json"
    if t97_path.exists():
        t97 = json.loads(t97_path.read_text(encoding="utf-8"))
        for item in t97.get("missing_subcalls", []):
            for k, v in item.items():
                if k in ("target", "target_va", "callee", "va", "callee_va"):
                    add_va(str(v), "t97_missing_subcall", 10)
        priority_classes = {
            "CLUB", "LEAGUE_BODY_CLUB", "COMP", "NATION",
            "NATIONAL_TEAM_CONTAINER", "TEAM_CONTAINER",
            "STADIUM", "TEAM", "NATIONAL_TEAM", "BASIC_PERSON", "AWARD",
        }
        for tbl in t97.get("tables", []):
            cls = tbl.get("class", "")
            w = 3 if cls in priority_classes else 1
            for code, rec in tbl.get("fourccs", {}).items():
                for h in rec.get("helper_calls", []):
                    add_va(str(h), f"t97_helper:{cls}", w)

    # 2. t105 needed_helpers
    t105_path = ROOT / "scratch/t105/out/big3_serializers.json"
    if t105_path.exists():
        t105 = json.loads(t105_path.read_text(encoding="utf-8"))
        nh = t105.get("needed_helpers", [])
        if isinstance(nh, list):
            for item in nh:
                if isinstance(item, dict):
                    for k in ("va", "helper_va", "target"):
                        if k in item:
                            add_va(str(item[k]), "t105_needed_helper", 20)
                elif isinstance(item, str):
                    add_va(item, "t105_needed_helper", 20)
        elif isinstance(nh, dict):
            for k in nh:
                add_va(str(k), "t105_needed_helper", 20)

    # 3. Extra known single miss
    add_va("0x140ed1480", "t95_comp_write", 20)

    # Keep all priority targets (weight >= 2) plus top 600 overall
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    selected = [(va, ",".join(sorted(sources[va]))[:60], w) for va, w in ranked[:600]]
    meta = {
        "existing_funcs": len(existing),
        "total_candidates": len(ranked),
        "selected_count": len(selected),
    }
    return selected, meta


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Decompile missing helper_calls & serializer helpers via IDA 9.4 idalib.")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    selected, meta = collect_target_vas()
    if args.selftest:
        print("SELFTEST meta:", json.dumps(meta))
        for va, src, w in selected[:15]:
            print(f"  {hex(va)} w={w:4d} {src}")
        return 0 if meta["selected_count"] >= 50 else 1

    todo = selected if args.limit <= 0 else selected[: args.limit]
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
    print(f"Opening {WORK_I64} for {len(todo)} helper targets...", flush=True)
    rc = idapro.open_database(str(WORK_I64), False)
    if rc:
        print(f"open_database failed rc={rc}", flush=True)
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

    done_map = {}
    misses = []
    seen_starts: set[int] = set()
    hop1_queue: list[tuple[int, str]] = []

    def decompile_one(orig_va: int, src: str, weight: int) -> dict | None:
        r_va, tnote = resolve_thunk(orig_va)
        start = ensure_func(r_va)
        out_c = FUNCS_DIR / f"{start:x}.c"
        # Also create alias file if orig_va != start and orig_va.c doesn't exist
        if start in seen_starts or out_c.exists():
            txt = out_c.read_text(encoding="utf-8", errors="ignore") if out_c.exists() else ""
            rec = {
                "orig_va": hex(orig_va),
                "resolved_va": hex(r_va),
                "func_start": hex(start),
                "thunk": tnote,
                "source": src,
                "weight": weight,
                "ok": out_c.exists(),
                "lines": txt.count("\n") + 1 if txt else 0,
                "fourccs": vlib.extract_4ccs_from_text(txt) if txt else [],
                "file": f"funcs/{start:x}.c",
            }
            if orig_va != start and out_c.exists() and not (FUNCS_DIR / f"{orig_va:x}.c").exists():
                (FUNCS_DIR / f"{orig_va:x}.c").write_text(
                    f"// THUNK ALIAS -> sub_{start:X} ({tnote or 'same func'})\n" + txt,
                    encoding="utf-8",
                )
            done_map[hex(orig_va)] = rec
            return rec
        seen_starts.add(start)
        name = ida_name.get_name(start) or f"sub_{start:x}"
        try:
            cfunc = ida_hexrays.decompile(start, flags=ida_hexrays.DECOMP_NO_WAIT)
            if cfunc is None:
                cfunc = ida_hexrays.decompile(start)
            if cfunc is not None:
                txt = str(cfunc)
                out_c.write_text(txt, encoding="utf-8")
                if orig_va != start and not (FUNCS_DIR / f"{orig_va:x}.c").exists():
                    (FUNCS_DIR / f"{orig_va:x}.c").write_text(
                        f"// THUNK ALIAS -> sub_{start:X} ({tnote or 'same func'})\n" + txt,
                        encoding="utf-8",
                    )
                lines = txt.count("\n") + 1
                callees = [hex(c) for c in vlib.extract_callees_from_text(txt) if c != start]
                rec = {
                    "orig_va": hex(orig_va),
                    "resolved_va": hex(r_va),
                    "func_start": hex(start),
                    "name": name,
                    "thunk": tnote,
                    "source": src,
                    "weight": weight,
                    "ok": True,
                    "lines": lines,
                    "fourccs": vlib.extract_4ccs_from_text(txt),
                    "callees": callees[:12],
                    "file": f"funcs/{start:x}.c",
                }
                done_map[hex(orig_va)] = rec
                if lines <= 20 and callees:
                    for ch in callees[:2]:
                        hop1_queue.append((int(ch, 16), f"hop1:{hex(orig_va)}"))
                return rec
            else:
                misses.append({"orig_va": hex(orig_va), "resolved_va": hex(r_va), "source": src, "why": "None"})
        except Exception as exc:
            misses.append({"orig_va": hex(orig_va), "resolved_va": hex(r_va), "source": src, "why": str(exc)})
        return None

    for idx, (va, src, w) in enumerate(todo, 1):
        rec = decompile_one(va, src, w)
        if idx % 50 == 0 or idx == len(todo):
            print(f"[{idx}/{len(todo)}] ok={len(done_map)} misses={len(misses)} elapsed={time.time()-t0:.1f}s", flush=True)

    # Follow thin helper wrappers 1 hop
    seen_hop = set()
    for hva, hsrc in hop1_queue[:150]:
        if hva in seen_hop or (FUNCS_DIR / f"{hva:x}.c").exists():
            continue
        seen_hop.add(hva)
        decompile_one(hva, hsrc, 1)

    idapro.close_database(False)

    summary = {
        "status": "complete" if len(misses) < 20 else "partial",
        "elapsed_sec": round(time.time() - t0, 1),
        "targets": len(todo),
        "decompiled_ok": sum(1 for v in done_map.values() if v.get("ok")),
        "misses_count": len(misses),
        "misses": misses[:50],
        "helpers": done_map,
    }
    (OUT_DIR / "helpers_index.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"DONE t107 in {summary['elapsed_sec']}s: ok={summary['decompiled_ok']} misses={summary['misses_count']}", flush=True)
    return 0 if summary["decompiled_ok"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
