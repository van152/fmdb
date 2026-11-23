"""t119_unicorn_last5 — Close the final 5/79 Unicorn database tables to reach 79/79 (100%).

Fixes identified from t96c failure analysis:
  1. Global DATABASE_TABLE* pointers used by DB-ref lookup helpers (0x140f92cc4 / 0x140f83b02):
     0x141B5FDC8, 0x141B5FDD0, 0x141B5FE00, 0x141B5FE10 -> point to db_a3_ptr (safe empty vector at +0x80).
  2. Global DB version qword_141B60330 -> set to table header version (0x0DF1) so legacy <=0xDDC branches
     in table_71 (sub_141199440) and sub_1411919D0 (shared by table_32 & table_71) do not over-read.

Usage:
  py -V:3.12 -B scripts/t119_unicorn_last5.py --selftest
  py -V:3.12 -B scripts/t119_unicorn_last5.py
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch/t119/out"

TARGETS = [
    ("server", 0),
    ("client", 0),
    ("server", 32),
    ("server", 71),
    ("server", 72),
]

TABLE_REF_GLOBALS = [
    0x141B5FDC0,  # AWARD ref 4 (sub_140F80B80)
    0x141B5FDC8,  # AWARD ref 1 (sub_140F92AB0)
    0x141B5FDD0,  # AWARD ref 2 (sub_140F92E30)
    0x141B5FE00,  # AWARD ref 3 (sub_140F93540)
    0x141B5FE10,  # STARTING_PAST_TRADE ref (sub_140F83B02)
]
GLOBAL_DB_VER_VA = 0x141B60330
SLAB_ALLOC_VA = 0x1412D31C0


def load_target_tables(targets: list[tuple[str, int]]) -> list[tuple[str, int, bytes]]:
    sys.path.insert(0, str(ROOT / "scripts"))
    import t38_multiframe as mf  # noqa: E402

    want_by_arch: dict[str, set[int]] = {}
    for arch, tid in targets:
        want_by_arch.setdefault(arch, set()).add(tid)

    codec = mf._codec()
    items: list[tuple[str, int, bytes]] = []
    for arch, tids in want_by_arch.items():
        info = mf.archive_info(codec, arch)
        for e in info["entries"]:
            m = re.match(rf"^{arch}_db/table_(\d+)\.dat$", e["path"])
            if not m:
                continue
            tid = int(m.group(1))
            if tid not in tids:
                continue
            start, _ = mf.member_bounds(e, info["data_base"])
            frames = mf.decode_frames_unbounded(info["data"], start)
            for f in frames:
                if f["length"] == int(e["size"]):
                    items.append((arch, tid, f["data"]))
                    break
    items.sort(key=lambda x: (0 if x[0] == "server" else 1, x[1]))
    return items


def setup_patched_emulator():
    sys.path.insert(0, str(ROOT / "scripts"))
    import t96c_unicorn_master as m  # noqa: E402

    ut, emu, db_a3_ptr = m.setup_emulator()
    for gva in TABLE_REF_GLOBALS:
        emu.mu.mem_write(gva, struct.pack("<Q", db_a3_ptr))
    # Set stream flags [STREAM_OBJ_ADDR + 0x0C] |= 0x2 (database stream bit),
    # byte_141B60352 = 1 (raw DB-load mode: read 4B DB refs directly without resolving unloaded global table vectors),
    # byte_141B60353 = 0 (32-bit 4-byte DB references, NOT 64-bit 8-byte!).
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x0C, struct.pack("<I", 2))
    emu.mu.mem_write(0x141B60352, b"\x01")
    emu.mu.mem_write(0x141B60353, b"\x00")

    # Hook SI lock-free slab allocator fallback 0x1412D31C0(pool=rcx, elem_size=edx, count=r8d)
    # Note: place trampoline at STUB_CODE_BASE + 0x0880 (inside pool_alloc_stubs range, NOT stream vtable!)
    SLAB_STUB = ut.STUB_CODE_BASE + 0x0880
    tramp = b"\x48\xB8" + struct.pack("<Q", SLAB_STUB) + b"\xFF\xE0"
    emu.mu.mem_write(SLAB_ALLOC_VA, tramp)
    emu.pool_alloc_stubs[SLAB_STUB] = "pool_rdx"
    # Wait: when edx == 0 (uninitialized pool due to high TLS epoch), _alloc(0) gives 16B which may be too small for object!
    # Hook explicitly so we allocate max(512, edx) zeroed bytes cleanly.
    from unicorn import UC_HOOK_CODE  # noqa: E402
    def on_slab_alloc(uc, address, size, user_data):
        sz = uc.reg_read(emu.REG["RDX"]) & 0xFFFFFFFF
        if sz < 512 or sz > 0x100000:
            sz = 512
        ptr = emu._alloc(sz, address)
        uc.mem_write(ptr, b"\x00" * sz)
        uc.reg_write(emu.REG["RAX"], ptr)
    emu.mu.hook_add(UC_HOOK_CODE, on_slab_alloc, begin=SLAB_STUB, end=SLAB_STUB + 1)

    return m, ut, emu, db_a3_ptr


def run_targets(full_limit: int = 1500, sample_rows: int = 50) -> dict:
    t0 = time.time()
    m, ut, emu, db_a3_ptr = setup_patched_emulator()
    vt_fb = m.load_vtable_fallback()
    items = load_target_tables(TARGETS)
    print(f"Loaded {len(items)} target tables in {time.time() - t0:.1f}s", flush=True)

    results = []
    for arch, tid, payload in items:
        ver = struct.unpack_from("<H", payload, 6)[0]
        emu.mu.mem_write(GLOBAL_DB_VER_VA, struct.pack("<Q", ver))
        t_one = time.time()
        r = m.trace_table(ut, emu, db_a3_ptr, vt_fb, arch, tid, payload, full_limit=full_limit, sample_rows=sample_rows)
        dt = time.time() - t_one
        status = "closed" if r["closed_to_footer"] else ("sample_ok" if r["error"] is None and r["rows_ok"] == r["rows_target"] else "failed")
        r["status"] = status
        r["elapsed_sec"] = round(dt, 2)
        results.append(r)
        print(
            f"  {arch}/t{tid} ({r['class']}): status={status} rows_ok={r['rows_ok']}/{r['rows_target']} "
            f"(hdr={r['rows_header']}) closed={r['closed_to_footer']} diff={r['diff_bytes']} "
            f"lens={r['row_len_min']}..{r['row_len_max']} uniq={r['unique_row_lens']} err={r['error']} ({dt:.1f}s)",
            flush=True,
        )

    closed = sum(1 for r in results if r["status"] == "closed")
    sample_ok = sum(1 for r in results if r["status"] == "sample_ok")
    failed = sum(1 for r in results if r["status"] == "failed")
    return {
        "schema_id": "fm24.t119.unicorn_last5",
        "schema_version": 1,
        "elapsed_sec": round(time.time() - t0, 2),
        "fixes_applied": {
            "table_ref_globals": [hex(x) for x in TABLE_REF_GLOBALS],
            "global_db_ver_va": hex(GLOBAL_DB_VER_VA),
        },
        "summary": {
            "targets": len(results),
            "closed": closed,
            "sample_ok": sample_ok,
            "clean": closed + sample_ok,
            "failed": failed,
            "combined_with_t96c_clean": f"{74 + closed + sample_ok}/79",
        },
        "tables": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--full-limit", type=int, default=1500)
    ap.add_argument("--sample-rows", type=int, default=50)
    args = ap.parse_args()

    if args.selftest:
        doc = run_targets(full_limit=50, sample_rows=10)
        ok = doc["summary"]["failed"] == 0 and doc["summary"]["clean"] == 5
        print(f"t119 selftest {'PASS' if ok else 'FAIL'}: {doc['summary']}", flush=True)
        return 0 if ok else 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = run_targets(full_limit=args.full_limit, sample_rows=args.sample_rows)
    out_json = OUT_DIR / "last5_traces.json"
    out_json.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    s = doc["summary"]
    lines = [
        "# t119: Final 5/79 Unicorn Tables Closure",
        "",
        f"- **Result**: `{s['clean']}/{s['targets']}` clean (`{s['closed']}` full closed + `{s['sample_ok']}` sample_ok, `{s['failed']}` failed)",
        f"- **Combined with t96c**: **`{s['combined_with_t96c_clean']}`**",
        f"- **Fixes**: `TABLE_REF_GLOBALS={[hex(x) for x in TABLE_REF_GLOBALS]}`, `GLOBAL_DB_VER_VA={hex(GLOBAL_DB_VER_VA)}`",
        "",
        "| Archive/Table | Class | Status | Rows OK / Target (Hdr) | Closed | Diff | Row Lens | Error |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in doc["tables"]:
        lines.append(
            f"| `{r['archive']}/table_{r['table_id']}` | `{r['class']}` | `{r['status']}` | "
            f"{r['rows_ok']}/{r['rows_target']} ({r['rows_header']}) | {r['closed_to_footer']} | "
            f"{r['diff_bytes']} | {r['row_len_min']}..{r['row_len_max']} (u={r['unique_row_lens']}) | {r['error'] or '-'} |"
        )
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "DONE.md").write_text(
        f"DONE type=t119\nstatus={'complete' if s['failed'] == 0 else 'partial'}\n"
        f"clean={s['clean']}/{s['targets']}\ncombined={s['combined_with_t96c_clean']}\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_json}", flush=True)
    return 0 if s["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
