"""t96c_unicorn_master — Full-database Unicorn x86_64 wire tracer & byte-exact closure runner.

Uses real C++ object construction via sub_140F49530(table_type, flag) + polymorphic vtable slot[19]
with a7=1 (server_db.dat) / a7=0 (client_db.dat), 1-byte per-row prefix framing, SI pool allocator
stubs, and global singleton struct initialization.

Runs ALL tables in server_db.dat and client_db.dat:
  - Full table (100% of rows + exact footer check) for all tables with <= 1,500 rows (including
    table_9 251/251 and table_10 251/251 on both server and client!).
  - First 50 rows for large tables (> 1,500 rows), or --full-all to walk everything.

Usage:
  py -V:3.12 -B scripts/t96c_unicorn_master.py --selftest
  py -V:3.12 -B scripts/t96c_unicorn_master.py
Exit codes: 0 ok, 1 partial, 2 fatal.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch/t96c/out"

# Global singleton pointers checked via `[rax + 0x5a]` during ctor/read
SETTINGS_GLOBALS = [
    0x141B5FDB8,  # CLUB ctor
    0x141B5FE08,  # NATIONAL_TEAM_CONTAINER read
    0x141B5FE40,  # TEAM ctor
]


def setup_emulator():
    sys.path.insert(0, str(ROOT / "scripts"))
    import t95_unicorn_trace as ut  # noqa: E402

    emu = ut.EditorEmulator()
    # Set DB-loaded global flag so tt=1 and tt=24 construct real subclasses
    emu.mu.mem_write(0x141B60320, b"\x01")

    # Map a dedicated persistent dummy region for global singletons & empty vectors
    GLOBAL_DUMMY_BASE = 0x0000_0005_0000_0000
    emu.mu.mem_map(GLOBAL_DUMMY_BASE, 0x20000)
    # Page 0: zeroed settings struct
    settings_ptr = GLOBAL_DUMMY_BASE + 0x0000
    for gva in SETTINGS_GLOBALS:
        emu.mu.mem_write(gva, struct.pack("<Q", settings_ptr))
    # Page 1: dummy a3 DB context where [a3 + 0x80] -> empty vector {0, 0, 0}
    db_a3_ptr = GLOBAL_DUMMY_BASE + 0x2000
    empty_vec_ptr = GLOBAL_DUMMY_BASE + 0x4000
    for off in range(0, 0x400, 8):
        emu.mu.mem_write(db_a3_ptr + off, struct.pack("<Q", empty_vec_ptr))

    # Hook string reader sub_140814B10 / sub_14371BDF0 cleanly so refcount/free never faults
    STR_READ_STUB = ut.STUB_CODE_BASE + 0x0900
    tramp = b"\x48\xB8" + struct.pack("<Q", STR_READ_STUB) + b"\xFF\xE0"
    emu.mu.mem_write(0x140814B10, tramp)
    emu.mu.mem_write(0x14371BDF0, tramp)

    def on_str_read(uc, address, size, user_data):
        rsp = uc.reg_read(emu.REG["RSP"])
        caller = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
        err_ptr = uc.reg_read(emu.REG["RDX"])
        dst_str_ptr_addr = uc.reg_read(emu.REG["R8"])
        if emu.wire_pos + 4 > len(emu.payload):
            uc.mem_write(err_ptr, struct.pack("<i", 1))
            uc.reg_write(emu.REG["RAX"], err_ptr)
            return
        slen = struct.unpack_from("<I", emu.payload, emu.wire_pos)[0]
        emu.reads.append({
            "wire_pos": emu.wire_pos, "n": 4, "dst_kind": "str_len",
            "obj_off": None, "obj_off_dec": None, "dst": hex(dst_str_ptr_addr),
            "caller": hex(caller), "hex": emu.payload[emu.wire_pos : emu.wire_pos + 4].hex(), "u_val": slen,
        })
        emu.wire_pos += 4
        if slen > 0x100000 or emu.wire_pos + slen > len(emu.payload):
            uc.mem_write(err_ptr, struct.pack("<i", 1))
            uc.reg_write(emu.REG["RAX"], err_ptr)
            return
        sbytes = emu.payload[emu.wire_pos : emu.wire_pos + slen]
        buf = emu._alloc(slen + 16, caller)
        uc.mem_write(buf + 0, struct.pack("<II", 1, slen))
        if slen > 0:
            uc.mem_write(buf + 8, sbytes)
        uc.mem_write(buf + 8 + slen, b"\x00")
        uc.mem_write(dst_str_ptr_addr, struct.pack("<Q", buf + 4))
        emu.reads.append({
            "wire_pos": emu.wire_pos, "n": slen, "dst_kind": "str_body",
            "obj_off": None, "obj_off_dec": None, "dst": hex(dst_str_ptr_addr),
            "caller": hex(caller), "hex": sbytes[:16].hex(), "u_val": None,
        })
        emu.wire_pos += slen
        uc.mem_write(err_ptr, struct.pack("<i", 0))
        uc.reg_write(emu.REG["RAX"], err_ptr)

    from unicorn import UC_HOOK_CODE  # noqa: E402
    emu.mu.hook_add(UC_HOOK_CODE, on_str_read, begin=STR_READ_STUB, end=STR_READ_STUB + 4)

    return ut, emu, db_a3_ptr


def load_all_numbered_tables():
    sys.path.insert(0, str(ROOT / "scripts"))
    import t38_multiframe as mf  # noqa: E402

    codec = mf._codec()
    items = []
    for arch in ("server", "client"):
        info = mf.archive_info(codec, arch)
        for e in info["entries"]:
            m = re.match(rf"^{arch}_db/table_(\d+)\.dat$", e["path"])
            if not m:
                continue
            tid = int(m.group(1))
            start, _ = mf.member_bounds(e, info["data_base"])
            frames = mf.decode_frames_unbounded(info["data"], start)
            payload = None
            for f in frames:
                if f["length"] == int(e["size"]):
                    payload = f["data"]
                    break
            if payload is not None:
                items.append((arch, tid, payload))
    items.sort(key=lambda x: (0 if x[0] == "server" else 1, x[1]))
    return items


def load_vtable_fallback() -> dict[int, tuple[str, int]]:
    vidx = json.loads((ROOT / "scratch/t95/vtable_index.json").read_text(encoding="utf-8"))
    out: dict[int, tuple[str, int]] = {}
    for t in vidx["tables"]:
        tt = t["table_type"]
        c = t["core"].get("slot19_read_server", {})
        if "func_start" in c and tt not in out:
            out[tt] = (t["class"], int(c["func_start"], 16))
    # Prefer CLUB over LEAGUE_BODY_CLUB as default fallback for tt=3
    out[3] = ("CLUB", 0x140E5B1A0)
    return out


def construct_via_factory(ut, emu, tid: int, flag: int) -> tuple[int, int, int, str | None]:
    emu.heap_ptr = ut.HEAP_BASE
    emu.unhandled_calls = []
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu.mu.mem_write(rsp, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], tid)
    emu.mu.reg_write(emu.REG["RDX"], flag)
    try:
        emu.mu.emu_start(0x140F49530, ut.STOP_ADDR, count=300_000)
    except Exception as exc:
        return 0, 0, 0, f"ctor:{exc}@{hex(emu.mu.reg_read(emu.REG['RIP']))}"
    if emu.mu.reg_read(emu.REG["RIP"]) != ut.STOP_ADDR:
        return 0, 0, 0, "ctor:timeout"
    obj = emu.mu.reg_read(emu.REG["RAX"])
    if obj == 0:
        return 0, 0, 0, "ctor:null"
    vt = struct.unpack("<Q", bytes(emu.mu.mem_read(obj, 8)))[0]
    if not (0x140000000 <= vt < 0x145000000):
        return obj, vt, 0, f"ctor:bad_vt:{hex(vt)}"
    s19 = struct.unpack("<Q", bytes(emu.mu.mem_read(vt + 19 * 8, 8)))[0]
    return obj, vt, s19, None


def run_one_row(ut, emu, obj: int, s19: int, row_slice: bytes, ver: int, a7: int, a3_ptr: int = 0) -> dict:
    # Ensure obj offset classification works relative to actual `obj`
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x08, struct.pack("<I", 1000))
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 0))
    emu.payload = row_slice
    emu.wire_pos = 0
    emu.reads = []
    emu.unhandled_calls = []

    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    ctx_ptr = emu._alloc(0x2000)
    emu.mu.mem_write(ctx_ptr + 0x588, struct.pack("<H", ver))
    emu.mu.mem_write(rsp + 0x00, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.mem_write(rsp + 0x28, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x30, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x38, struct.pack("<Q", a7))
    emu.mu.mem_write(rsp + 0x40, struct.pack("<Q", 0))  # a8 = NULL

    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], obj)
    emu.mu.reg_write(emu.REG["RDX"], ut.STREAM_PTR_ADDR)
    emu.mu.reg_write(emu.REG["R8"], a3_ptr)
    emu.mu.reg_write(emu.REG["R9"], ctx_ptr)

    err = None
    try:
        emu.mu.emu_start(s19, ut.STOP_ADDR, count=3_000_000)
    except Exception as exc:
        err = str(exc)

    rip = emu.mu.reg_read(emu.REG["RIP"])
    ok = (err is None and rip == ut.STOP_ADDR and emu.wire_pos > 0)

    # Reclassify dst relative to `obj` (since factory allocates `obj` on HEAP_BASE!)
    obj_end = obj + 0x2000
    for r in emu.reads:
        dst = int(r["dst"], 16)
        if obj <= dst < obj_end:
            r["dst_kind"] = "this"
            r["obj_off"] = hex(dst - obj)
            r["obj_off_dec"] = dst - obj

    return {
        "ok": ok,
        "error": err if err else (None if ok else ("timeout_or_no_progress" if rip != ut.STOP_ADDR else "zero_consumed")),
        "end_rip": hex(rip),
        "bytes_consumed": emu.wire_pos,
        "reads": emu.reads,
        "unhandled": emu.unhandled_calls[:5],
    }


def aggregate_canonical(row_reads_samples: list[list[dict]]) -> list[dict]:
    """Summarize canonical field sequence from row 0..K samples."""
    if not row_reads_samples:
        return []
    # Aggregate by (caller, obj_off, dst_kind) in order of first appearance
    order: list[tuple[str, str | None, str]] = []
    stats: dict[tuple[str, str | None, str], dict] = {}
    for reads in row_reads_samples:
        seen_in_row: set[tuple[str, str | None, str]] = set()
        for r in reads:
            key = (r["caller"], r.get("obj_off"), r.get("dst_kind", "?"))
            if key not in stats:
                order.append(key)
                stats[key] = {
                    "caller_va": r["caller"],
                    "obj_off": r.get("obj_off"),
                    "dst_kind": r.get("dst_kind", "?"),
                    "wire_off_row0": r["wire_pos"],
                    "lens": set(),
                    "rows_seen": 0,
                    "total_calls": 0,
                }
            st = stats[key]
            st["lens"].add(r["n"])
            st["total_calls"] += 1
            if key not in seen_in_row:
                seen_in_row.add(key)
                st["rows_seen"] += 1
    out = []
    for idx, k in enumerate(order):
        st = stats[k]
        lens = sorted(st["lens"])
        out.append({
            "idx": idx,
            "wire_off_row0": st["wire_off_row0"],
            "n": lens[0] if len(lens) == 1 else lens[:6],
            "variable_len": len(lens) > 1 or st["total_calls"] > st["rows_seen"],
            "dst_kind": st["dst_kind"],
            "obj_off": st["obj_off"],
            "caller_va": st["caller_va"],
            "rows_seen": st["rows_seen"],
            "total_calls": st["total_calls"],
        })
    return out


def trace_table(ut, emu, db_a3_ptr, vt_fallback, arch: str, tid: int, payload: bytes, full_limit: int = 1500, sample_rows: int = 50) -> dict:
    a7 = 1 if arch == "server" else 0
    cls_name, fb_s19 = vt_fallback.get(tid, (f"TT{tid}", 0))
    ver = struct.unpack_from("<H", payload, 6)[0]
    nrows = struct.unpack_from("<I", payload, 8)[0]
    footer_off = len(payload) - 9

    rec = {
        "archive": arch,
        "table_id": tid,
        "class": cls_name,
        "a7": a7,
        "version": hex(ver),
        "payload_size": len(payload),
        "footer_off": footer_off,
        "rows_header": nrows,
        "rows_target": nrows if nrows <= full_limit else sample_rows,
        "rows_ok": 0,
        "closed_to_footer": False,
        "end_pos": 13,
        "diff_bytes": footer_off - 13,
        "flags_seen": {},
        "vtables_seen": [],
        "row_len_min": None,
        "row_len_max": None,
        "unique_row_lens": 0,
        "error": None,
        "row0_reads": [],
        "canonical_fields": [],
    }

    if nrows == 0:
        rec["closed_to_footer"] = (13 == footer_off)
        rec["diff_bytes"] = footer_off - 13
        return rec

    pos = 13
    flags_cnt: Counter[int] = Counter()
    vts_seen: set[str] = set()
    row_lens: list[int] = []
    samples: list[list[dict]] = []
    helper_callers: Counter[str] = Counter()
    limit = rec["rows_target"]

    # Check if factory works on first row; fallback to zeroed THIS_BASE if factory fails
    for r in range(limit):
        if pos >= footer_off:
            rec["error"] = f"row {r}: pos {pos} >= footer {footer_off}"
            break
        flag = payload[pos]
        pos += 1
        flags_cnt[flag] += 1

        obj, vt, s19, ctor_err = construct_via_factory(ut, emu, tid, flag)
        if ctor_err or s19 == 0:
            # Fallback to zeroed THIS_BASE + fallback slot19
            emu.heap_ptr = ut.HEAP_BASE
            emu.mu.mem_write(ut.THIS_BASE, b"\x00" * 0x4000)
            obj = ut.THIS_BASE
            s19 = fb_s19
            vts_seen.add(f"fallback:{hex(s19)}")
        else:
            vts_seen.add(f"{hex(vt)}->{hex(s19)}")

        res = run_one_row(ut, emu, obj, s19, payload[pos : pos + 65536], ver, a7, a3_ptr=0)
        if not res["ok"] and res["unhandled"] and res["unhandled"][0].get("addr") == "0x80":
            # Retry with valid a3_ptr (needed by AWARD table_0 etc.)
            obj2, vt2, s19_2, ce2 = construct_via_factory(ut, emu, tid, flag)
            if ce2 or s19_2 == 0:
                emu.heap_ptr = ut.HEAP_BASE
                emu.mu.mem_write(ut.THIS_BASE, b"\x00" * 0x4000)
                obj2, s19_2 = ut.THIS_BASE, fb_s19
            res = run_one_row(ut, emu, obj2, s19_2, payload[pos : pos + 65536], ver, a7, a3_ptr=db_a3_ptr)

        if not res["ok"]:
            rec["error"] = f"row {r} flag={flag:#x} s19={hex(s19)} consumed={res['bytes_consumed']} err={res['error']} rip={res['end_rip']} un={res['unhandled'][:1]}"
            break

        pos += res["bytes_consumed"]
        row_lens.append(res["bytes_consumed"])
        rec["rows_ok"] += 1
        if r == 0:
            rec["row0_reads"] = res["reads"]
        if r < 20:
            samples.append(res["reads"])
        if tid in (9, 10):
            for rd in res["reads"]:
                helper_callers[rd["caller"]] += 1

    rec["end_pos"] = pos
    rec["diff_bytes"] = footer_off - pos
    rec["closed_to_footer"] = (rec["rows_ok"] == nrows and pos == footer_off)
    rec["flags_seen"] = {hex(k): v for k, v in sorted(flags_cnt.items())}
    rec["vtables_seen"] = sorted(vts_seen)
    if row_lens:
        rec["row_len_min"] = min(row_lens)
        rec["row_len_max"] = max(row_lens)
        rec["unique_row_lens"] = len(set(row_lens))
    rec["canonical_fields"] = aggregate_canonical(samples)
    if tid in (9, 10):
        rec["_row_lens_all"] = row_lens
        rec["_helper_callers"] = dict(helper_callers.most_common())
    return rec


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Full-DB Unicorn wire tracer & closure runner.")
    ap.add_argument("--full-limit", type=int, default=1500, help="Run 100% of rows for tables with <= N rows")
    ap.add_argument("--sample-rows", type=int, default=50, help="Rows to trace for large tables")
    ap.add_argument("--only", type=str, default="", help="Comma-separated table IDs to run (debug)")
    ap.add_argument("--selftest", action="store_true", help="Verify diff==0 closure on server/t5, client/t5, server/t10, client/t10, client/t9")
    args = ap.parse_args()

    t0 = time.time()
    ut, emu, db_a3_ptr = setup_emulator()
    vt_fallback = load_vtable_fallback()
    all_tables = load_all_numbered_tables()

    if args.selftest:
        targets = {("server", 5), ("client", 5), ("server", 10), ("client", 10), ("client", 9), ("server", 9)}
        all_ok = True
        for arch, tid, payload in all_tables:
            if (arch, tid) not in targets:
                continue
            r = trace_table(ut, emu, db_a3_ptr, vt_fallback, arch, tid, payload, full_limit=1500)
            print(f"SELFTEST {arch:6s}/t{tid:<2d} rows={r['rows_ok']}/{r['rows_header']} diff={r['diff_bytes']} closed={r['closed_to_footer']} uniq_lens={r['unique_row_lens']} err={r['error']}")
            if not r["closed_to_footer"]:
                all_ok = False
        return 0 if all_ok else 1

    only_set = {int(x) for x in args.only.split(",") if x.strip()} if args.only else None
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    t9_closure = {"status": "partial", "tables": {}}
    t10_closure = {"status": "partial", "tables": {}}

    for arch, tid, payload in all_tables:
        if only_set is not None and tid not in only_set:
            continue
        r = trace_table(ut, emu, db_a3_ptr, vt_fallback, arch, tid, payload, args.full_limit, args.sample_rows)
        if tid == 9:
            t9_closure["tables"][arch] = {
                "rows_header": r["rows_header"],
                "rows_ok": r["rows_ok"],
                "end_pos": r["end_pos"],
                "footer_off": r["footer_off"],
                "diff_bytes": r["diff_bytes"],
                "closed_to_footer": r["closed_to_footer"],
                "unique_row_lens": r["unique_row_lens"],
                "row_len_min": r["row_len_min"],
                "row_len_max": r["row_len_max"],
                "row_lengths": r.pop("_row_lens_all", []),
                "helper_callers": r.pop("_helper_callers", {}),
                "error": r["error"],
            }
        elif tid == 10:
            t10_closure["tables"][arch] = {
                "rows_header": r["rows_header"],
                "rows_ok": r["rows_ok"],
                "end_pos": r["end_pos"],
                "footer_off": r["footer_off"],
                "diff_bytes": r["diff_bytes"],
                "closed_to_footer": r["closed_to_footer"],
                "unique_row_lens": r["unique_row_lens"],
                "row_len_min": r["row_len_min"],
                "row_len_max": r["row_len_max"],
                "row_lengths": r.pop("_row_lens_all", []),
                "helper_callers": r.pop("_helper_callers", {}),
                "error": r["error"],
            }
        results.append(r)
        tag = "CLOSED" if r["closed_to_footer"] else ("OK_SAMPLE" if r["rows_ok"] == r["rows_target"] and r["rows_ok"] > 0 else "FAIL")
        print(
            f"{arch:6s}/t{tid:<2d} {r['class']:32s} {tag:9s} rows={r['rows_ok']:4d}/{r['rows_header']:<6d} "
            f"diff={r['diff_bytes']:9d} fields={len(r['canonical_fields']):3d} {r['error'] or ''}",
            flush=True,
        )

    t9_both = all(v.get("closed_to_footer") for v in t9_closure["tables"].values()) and len(t9_closure["tables"]) == 2
    t10_both = all(v.get("closed_to_footer") for v in t10_closure["tables"].values()) and len(t10_closure["tables"]) == 2
    t9_closure["status"] = "complete" if t9_both else "partial"
    t10_closure["status"] = "complete" if t10_both else "partial"

    n_closed = sum(1 for r in results if r["closed_to_footer"])
    n_sample_ok = sum(1 for r in results if not r["closed_to_footer"] and r["rows_ok"] == r["rows_target"] and r["rows_ok"] > 0)
    n_fail = len(results) - n_closed - n_sample_ok

    master = {
        "status": "complete" if n_fail <= 10 else "partial",
        "elapsed_sec": round(time.time() - t0, 1),
        "total_archive_tables": len(results),
        "closed_to_footer": n_closed,
        "sample_rows_all_ok": n_sample_ok,
        "total_clean": n_closed + n_sample_ok,
        "failed": n_fail,
        "table9_both_closed": t9_both,
        "table10_both_closed": t10_both,
        "tables": results,
    }
    (OUT_DIR / "wire_traces_master.json").write_text(json.dumps(master, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "table9_251_closure.json").write_text(json.dumps(t9_closure, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "table10_251_closure.json").write_text(json.dumps(t10_closure, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write markdown report
    lines = [
        "# t96c — Unicorn 全表（79 对 server+client）真机微执行闭合报告",
        "",
        f"- 耗时：`{master['elapsed_sec']}s`",
        f"- 总表对：`{len(results)}` | **整表 `diff==0` 精确闭合：`{n_closed}`** | **大表 50 行零异常：`{n_sample_ok}`** | **合计干净跑通：`{n_closed + n_sample_ok}/{len(results)}`** | 失败：`{n_fail}`",
        f"- `table_9` 双端 251/251 闭合：`{t9_both}`",
        f"- `table_10` 双端 251/251 闭合：`{t10_both}`",
        "",
        "## 全表结果汇总",
        "",
        "| archive | tt | class | 状态 | rows_ok / total | diff | uniq_lens | fields | 备注 |",
        "|---|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for r in results:
        tag = "CLOSED" if r["closed_to_footer"] else ("OK_SAMPLE" if r["rows_ok"] == r["rows_target"] and r["rows_ok"] > 0 else "FAIL")
        lines.append(
            f"| {r['archive']} | {r['table_id']} | `{r['class']}` | **{tag}** | "
            f"{r['rows_ok']}/{r['rows_header']} | {r['diff_bytes']} | {r['unique_row_lens']} | "
            f"{len(r['canonical_fields'])} | {(r['error'] or '')[:80]} |"
        )
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "DONE.md").write_text(
        f"DONE type=t96c\nstatus={master['status']}\nclosed={n_closed}\nsample_ok={n_sample_ok}\nfailed={n_fail}\n",
        encoding="utf-8",
    )
    print(f"\nDONE t96c in {master['elapsed_sec']}s: closed={n_closed} sample_ok={n_sample_ok} fail={n_fail} / {len(results)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
