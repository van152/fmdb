"""t120_people_unicorn — Native Unicorn x86_64 wire tracer for 400MB people_db.dat.

Uses real editor.exe people factory sub_1410992C0(person_type) + polymorphic vtable slot[19]
with full database-stream flags, clean isolated string hook, universal DATABASE_TABLE* stub,
empty MSVC std::map sentinel, and localization pool stub.

Usage:
  py -V:3.12 -B scripts/t120_people_unicorn.py --selftest
  py -V:3.12 -B scripts/t120_people_unicorn.py --limit 3000
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import struct
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch/t120/out"
PEOPLE_DAT = ROOT / "scratch/data/people_db.dat"

sys.path.insert(0, str(_cfg.VENDOR_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

PTYPE_NAMES = {
    1: "NON_PLAYER",
    2: "PLAYER",
    3: "ACTUAL_PLAYER_AND_NON_PLAYER",
    4: "OFFICIAL",
    5: "RETIRED_PERSON",
    6: "JOURNALIST",
}


def setup_people_emulator():
    import t119_unicorn_last5 as t119
    from unicorn import UC_HOOK_CODE

    m, ut, emu, db_a3_ptr = t119.setup_patched_emulator()
    emu.mu.mem_write(t119.GLOBAL_DB_VER_VA, struct.pack("<Q", 0x0DF1))
    # people_db.dat uses 8-byte ref slots when HIBYTE(qword_141B6034C) == byte_141B60353 == 1 and byte_141B5FC2C == 0
    emu.mu.mem_write(0x141B60353, b"\x01")
    emu.mu.mem_write(0x141B5FC2C, b"\x00")

    # 1. Clean universal DATABASE_TABLE* stub (zeroed except +0x80 -> empty_vec {0,0,0})
    TBL_STUB = 0x0000_0005_0001_4000
    EMPTY_VEC = 0x0000_0005_0001_5000
    emu.mu.mem_write(TBL_STUB, b"\x00" * 0x1000)
    emu.mu.mem_write(EMPTY_VEC, b"\x00" * 0x100)
    emu.mu.mem_write(TBL_STUB + 0x80, struct.pack("<Q", EMPTY_VEC))
    for gva in range(0x141B5FDB8, 0x141B5FF80, 8):
        emu.mu.mem_write(gva, struct.pack("<Q", TBL_STUB))

    # 1b. Global localization / string-pool singleton at 0x141ABF5C0 (accessed at +0xade8 during PERSON name init)
    STR_POOL_BASE = 0x0000_0006_0001_0000
    emu.mu.mem_map(STR_POOL_BASE, 0x20000)
    emu.mu.mem_write(STR_POOL_BASE, b"\x00" * 0x20000)
    emu.mu.mem_write(0x141ABF5C0, struct.pack("<Q", STR_POOL_BASE))

    # 2. Empty MSVC std::map sentinel node for 0x141B5A740 (PLAYER/ACTUAL_PLAYER_AND_NON_PLAYER ctor)
    MAP_NIL = 0x0000_0005_0001_2000
    emu.mu.mem_write(MAP_NIL + 0x00, struct.pack("<QQQ", MAP_NIL, MAP_NIL, MAP_NIL))
    emu.mu.mem_write(MAP_NIL + 0x18, b"\x01\x01")
    emu.mu.mem_write(0x141B5A740, struct.pack("<Q", MAP_NIL))

    # 3. Dedicated page OUTSIDE STUB_CODE_BASE for clean string-reader hook
    CLEAN_STUB = 0x0000_0006_0000_0000
    emu.mu.mem_map(CLEAN_STUB, 0x10000)
    emu.mu.mem_write(CLEAN_STUB, b"\xC3" * 0x10000)
    tramp = b"\x48\xB8" + struct.pack("<Q", CLEAN_STUB) + b"\xFF\xE0"
    emu.mu.mem_write(0x140814B10, tramp)
    emu.mu.mem_write(0x14371BDF0, tramp)

    def on_str_read_clean(uc, address, size, user_data):
        rsp = uc.reg_read(emu.REG["RSP"])
        caller = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
        err_ptr = uc.reg_read(emu.REG["RDX"])
        dst_ptr = uc.reg_read(emu.REG["R8"])
        if emu.wire_pos + 4 > len(emu.payload):
            uc.mem_write(err_ptr, struct.pack("<i", 1))
            uc.reg_write(emu.REG["RAX"], err_ptr)
            return
        slen = struct.unpack_from("<I", emu.payload, emu.wire_pos)[0]
        emu.reads.append({
            "wire_pos": emu.wire_pos, "n": 4, "dst_kind": "str_len",
            "obj_off": None, "obj_off_dec": None, "dst": hex(dst_ptr),
            "caller": hex(caller), "hex": emu.payload[emu.wire_pos:emu.wire_pos + 4].hex(), "u_val": slen,
        })
        emu.wire_pos += 4
        if slen > 0x100000 or emu.wire_pos + slen > len(emu.payload):
            uc.mem_write(err_ptr, struct.pack("<i", 1))
            uc.reg_write(emu.REG["RAX"], err_ptr)
            return
        sbytes = emu.payload[emu.wire_pos:emu.wire_pos + slen]
        bufp = emu._alloc(slen + 16, caller)
        uc.mem_write(bufp, struct.pack("<II", 1, slen))
        if slen:
            uc.mem_write(bufp + 8, sbytes)
        uc.mem_write(bufp + 8 + slen, b"\x00")
        uc.mem_write(dst_ptr, struct.pack("<Q", bufp + 4))
        emu.reads.append({
            "wire_pos": emu.wire_pos, "n": slen, "dst_kind": "str_body",
            "obj_off": None, "obj_off_dec": None, "dst": hex(dst_ptr),
            "caller": hex(caller), "hex": sbytes[:32].hex(), "u_val": None,
        })
        emu.wire_pos += slen
        uc.mem_write(err_ptr, struct.pack("<i", 0))
        uc.reg_write(emu.REG["RAX"], err_ptr)

    emu.mu.hook_add(UC_HOOK_CODE, on_str_read_clean, begin=CLEAN_STUB, end=CLEAN_STUB + 1)
    return m, ut, emu, db_a3_ptr


def call_people_factory(ut, emu, ptype: int):
    emu.heap_ptr = ut.HEAP_BASE
    emu.unhandled_calls = []
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu.mu.mem_write(rsp, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], ptype)
    try:
        emu.mu.emu_start(0x1410992C0, ut.STOP_ADDR, count=1_000_000)
    except Exception as exc:
        rip = emu.mu.reg_read(emu.REG["RIP"])
        return 0, 0, 0, f"{exc}@{hex(rip)}"
    rip = emu.mu.reg_read(emu.REG["RIP"])
    if rip != ut.STOP_ADDR:
        return 0, 0, 0, f"timeout@{hex(rip)}"
    obj = emu.mu.reg_read(emu.REG["RAX"])
    if not (ut.HEAP_BASE <= obj < ut.HEAP_BASE + ut.HEAP_SIZE):
        return obj, 0, 0, f"bad_obj={hex(obj)}"
    vt = struct.unpack("<Q", bytes(emu.mu.mem_read(obj, 8)))[0]
    s19 = struct.unpack("<Q", bytes(emu.mu.mem_read(vt + 19 * 8, 8)))[0]
    return obj, vt, s19, None


def run_person_row(ut, emu, obj: int, s19: int, slice_bytes: bytes) -> dict:
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x08, struct.pack("<I", 1000))
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 0))
    emu.payload = slice_bytes
    emu.wire_pos = 0
    emu.reads = []
    emu.unhandled_calls = []

    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    ctx_ptr = emu._alloc(0x2000)
    emu.mu.mem_write(ctx_ptr + 0x588, struct.pack("<H", 0x0DF1))
    emu.mu.mem_write(rsp + 0x00, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.mem_write(rsp + 0x28, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x30, struct.pack("<Q", 0xFFFFFFFF))  # a6 = -1 skips a8 callback
    emu.mu.mem_write(rsp + 0x38, struct.pack("<Q", 1))           # a7 = 1
    emu.mu.mem_write(rsp + 0x40, struct.pack("<Q", 0))           # a8 = NULL
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], obj)
    emu.mu.reg_write(emu.REG["RDX"], ut.STREAM_PTR_ADDR)
    emu.mu.reg_write(emu.REG["R8"], 1)                           # a3 = 1 (read base PERSON)
    emu.mu.reg_write(emu.REG["R9"], ctx_ptr)

    run_err = None
    try:
        emu.mu.emu_start(s19, ut.STOP_ADDR, count=3_000_000)
    except Exception as exc:
        run_err = str(exc)

    rip = emu.mu.reg_read(emu.REG["RIP"])
    rax = emu.mu.reg_read(emu.REG["RAX"]) & 0xFF
    ok = (run_err is None and rip == ut.STOP_ADDR and rax != 0 and emu.wire_pos > 0)

    # Reclassify dst relative to base allocation (HEAP_BASE) AND returned DATABASE_OBJECT* (obj)
    for r in emu.reads:
        dst = int(r["dst"], 16)
        if ut.HEAP_BASE <= dst < ut.HEAP_BASE + 0x2000:
            r["dst_kind"] = "obj_mem"
            r["obj_off"] = hex(dst - obj)
            r["obj_off_dec"] = dst - obj
            r["base_off"] = hex(dst - ut.HEAP_BASE)
    return {
        "ok": ok,
        "bytes_consumed": emu.wire_pos,
        "reads": emu.reads,
        "end_rip": hex(rip),
        "error": run_err or ("ret_zero" if rax == 0 else None),
        "unhandled": emu.unhandled_calls[:5],
    }


def walk_people(limit: int = 3000, prefix_mb: int = 8) -> dict:
    import zstandard

    t0 = time.time()
    raw = PEOPLE_DAT.read_bytes()
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(raw[8:]) as rdr:
        buf = rdr.read(prefix_mb * 1024 * 1024)
    total_count = struct.unpack_from("<I", buf, 2)[0]
    m, ut, emu, _ = setup_people_emulator()

    factory_info = {}
    for pt in (1, 2, 3, 4, 5, 6):
        obj, vt, s19, err = call_people_factory(ut, emu, pt)
        factory_info[str(pt)] = {
            "class": PTYPE_NAMES[pt],
            "obj_offset_from_base": hex(obj - ut.HEAP_BASE) if obj else None,
            "vtable_va": hex(vt) if vt else None,
            "slot19_va": hex(s19) if s19 else None,
            "error": err,
        }

    pos = 6
    by_type_cnt: Counter[int] = Counter()
    by_type_lens: dict[int, list[int]] = {}
    samples_by_type: dict[str, list[dict]] = {}
    first_err = None
    rows_ok = 0

    for idx in range(limit):
        if pos + 5 >= len(buf):
            break
        ord_id = struct.unpack_from("<I", buf, pos)[0]
        pt = buf[pos + 4]
        obj, vt, s19, cerr = call_people_factory(ut, emu, pt)
        if cerr or not s19:
            first_err = {"row_idx": idx, "off": pos, "ord": ord_id, "ptype": pt, "error": f"ctor:{cerr}"}
            break
        res = run_person_row(ut, emu, obj, s19, buf[pos + 5:pos + 5 + 65536])
        if not res["ok"]:
            first_err = {
                "row_idx": idx, "off": pos, "ord": ord_id, "ptype": pt,
                "consumed": res["bytes_consumed"], "end_rip": res["end_rip"],
                "error": res["error"], "unhandled": res["unhandled"],
            }
            break
        rows_ok += 1
        by_type_cnt[pt] += 1
        by_type_lens.setdefault(pt, []).append(res["bytes_consumed"])
        skey = str(pt)
        if len(samples_by_type.get(skey, [])) < 3:
            # Extract trailing 12B identity (ordinal, dbid, uid) from last 12B read
            id_rd = next((r for r in reversed(res["reads"]) if r["n"] == 12), None)
            ident = None
            if id_rd and len(id_rd["hex"]) == 24:
                ident = dict(zip(["ordinal", "dbid", "uid"], struct.unpack("<III", bytes.fromhex(id_rd["hex"]))))
            samples_by_type.setdefault(skey, []).append({
                "row_idx": idx,
                "file_off": pos,
                "header_ord": ord_id,
                "ptype": pt,
                "class": PTYPE_NAMES.get(pt, f"TYPE_{pt}"),
                "body_len": res["bytes_consumed"],
                "identity": ident,
                "read_count": len(res["reads"]),
                "reads": res["reads"],
            })
        pos += 5 + res["bytes_consumed"]

    type_stats = {}
    for pt, cnt in sorted(by_type_cnt.items()):
        ls = by_type_lens[pt]
        type_stats[str(pt)] = {
            "class": PTYPE_NAMES.get(pt, f"TYPE_{pt}"),
            "rows_ok": cnt,
            "body_len_min": min(ls),
            "body_len_max": max(ls),
            "unique_lens": len(set(ls)),
        }

    return {
        "schema_id": "fm24.t120.people_unicorn",
        "schema_version": 1,
        "elapsed_sec": round(time.time() - t0, 2),
        "archive_header_count": total_count,
        "prefix_bytes": len(buf),
        "rows_target": limit,
        "rows_ok": rows_ok,
        "end_offset": pos,
        "first_error": first_err,
        "factory": factory_info,
        "type_stats": type_stats,
        "samples_by_type": samples_by_type,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--limit", type=int, default=3000)
    ap.add_argument("--prefix-mb", type=int, default=8)
    args = ap.parse_args()

    if args.selftest:
        doc = walk_people(limit=1210, prefix_mb=2)
        ok = (
            doc["rows_ok"] == 1210
            and doc["first_error"] is None
            and doc["type_stats"].get("5", {}).get("rows_ok") == 1193
            and doc["type_stats"].get("2", {}).get("rows_ok", 0) >= 17
        )
        print(f"t120 selftest {'PASS' if ok else 'FAIL'}: rows_ok={doc['rows_ok']} stats={doc['type_stats']} err={doc['first_error']}", flush=True)
        return 0 if ok else 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = walk_people(limit=args.limit, prefix_mb=args.prefix_mb)
    out_json = OUT_DIR / "people_unicorn_traces.json"
    out_json.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    lines = [
        "# t120: 400 MB `people_db.dat` Native Unicorn Walkthrough",
        "",
        f"- **Rows walked cleanly**: **`{doc['rows_ok']:,} / {doc['rows_target']:,}`** (end_offset=`{doc['end_offset']:,}`, elapsed=`{doc['elapsed_sec']}s`, first_error=`{doc['first_error']}`)",
        f"- **Archive total declared rows**: `{doc['archive_header_count']:,}`",
        "",
        "## Factory & Vtables (`sub_1410992C0`)",
        "| Type | Class | Base->Obj Offset | Vtable VA | `slot19` VA |",
        "|---:|---|---|---|---|",
    ]
    for pt, f in doc["factory"].items():
        lines.append(f"| {pt} | `{f['class']}` | `{f['obj_offset_from_base']}` | `{f['vtable_va']}` | `{f['slot19_va']}` |")
    lines += [
        "",
        "## Walked Person-Type Breakdown",
        "| Type | Class | Rows OK | Body Len Min..Max | Unique Lens |",
        "|---:|---|---:|---|---:|",
    ]
    for pt, st in doc["type_stats"].items():
        lines.append(f"| {pt} | `{st['class']}` | {st['rows_ok']:,} | {st['body_len_min']}..{st['body_len_max']} | {st['unique_lens']} |")
    (OUT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "DONE.md").write_text(
        f"DONE type=t120\nstatus={'complete' if doc['first_error'] is None else 'partial'}\n"
        f"rows_ok={doc['rows_ok']}/{doc['rows_target']}\nend_offset={doc['end_offset']}\n",
        encoding="utf-8",
    )
    print(f"t120 DONE: rows_ok={doc['rows_ok']}/{doc['rows_target']} stats={doc['type_stats']} err={doc['first_error']} ({doc['elapsed_sec']}s)", flush=True)
    return 0 if doc["first_error"] is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
