"""Fix-test: isolated CTX/OBJ arenas + dbctx globals, run the 4 real failures + stability."""
import struct
import sys
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t96c_unicorn_master as M  # noqa: E402
import t95_unicorn_trace as ut  # noqa: E402

# Dedicated arenas (disjoint from everything t95 maps)
OBJ_BASE = 0x0000_0006_0000_0000      # object slots, 1 MB each
OBJ_SLOT = 0x0010_0000
OBJ_ZERO = 0x0001_0000                # zero 64 KB per row (covers 62 KB blobs)
OBJ_SLOTS = 16
CTX_BASE = 0x0000_0007_0000_0000      # ctx slots, 16 KB each
CTX_SLOT = 0x0000_4000
CTX_SLOTS = 64

# DB-context singletons dereferenced by slot19 helpers ([g] -> ctx; [ctx+0x80] -> vector)
DBCTX_GLOBALS = [0x141B5FDC8, 0x141B5FDD0, 0x141B5FE00, 0x141B5FE10, 0x141BF7E10]
# Schema/feature version gates read as globals inside slot19 readers
VER_GLOBALS = [0x141B60330, 0x141B60332, 0x141B60334]


def setup_v2():
    ut_, emu, db_a3 = M.setup_emulator()
    emu.mu.mem_map(OBJ_BASE, OBJ_SLOT * OBJ_SLOTS)
    emu.mu.mem_map(CTX_BASE, CTX_SLOT * CTX_SLOTS)
    emu._obj_bump = 0
    emu._ctx_bump = 0
    emu._alloc_mode = "heap"
    emu._ctx_addr = 0

    orig_alloc = emu._alloc

    def alloc_v2(size, caller=0):
        mode = getattr(emu, "_alloc_mode", "heap")
        if mode == "obj":
            slot = OBJ_BASE + emu._obj_bump
            emu.mu.mem_write(slot, b"\x00" * OBJ_ZERO)
            addr = slot
            emu._obj_bump += OBJ_SLOT
            emu._obj_bump %= OBJ_SLOT * OBJ_SLOTS
            emu.heap_ptr = addr + size  # ctor bump continues inside slot
            return addr
        if mode == "ctx":
            slot = CTX_BASE + emu._ctx_bump
            emu._ctx_bump += CTX_SLOT
            emu._ctx_bump %= CTX_SLOT * CTX_SLOTS
            emu._ctx_addr = slot
            return slot
        return orig_alloc(size, caller)

    emu._alloc = alloc_v2

    # DB-context globals -> db_a3 page ([+0x80] = empty vec {0,0,0})
    for g in DBCTX_GLOBALS:
        emu.mu.mem_write(g, struct.pack("<Q", db_a3))
    return ut_, emu, db_a3


def construct_v2(emu, ut_, tid, flag):
    emu.heap_ptr = ut_.HEAP_BASE
    emu.unhandled_calls = []
    emu.heap_allocs = []
    rsp = ut_.STACK_BASE + ut_.STACK_SIZE - 0x2000
    emu.mu.mem_write(rsp, struct.pack("<Q", ut_.STOP_ADDR))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], tid)
    emu.mu.reg_write(emu.REG["RDX"], flag)
    emu._alloc_mode = "obj"
    try:
        emu.mu.emu_start(0x140F49530, ut_.STOP_ADDR, count=300_000)
    except Exception:
        emu._alloc_mode = "heap"
        return 0, 0, 0
    emu._alloc_mode = "heap"
    obj = emu.mu.reg_read(emu.REG["RAX"])
    if obj == 0:
        return 0, 0, 0
    vt = struct.unpack("<Q", bytes(emu.mu.mem_read(obj, 8)))[0]
    if not (0x140000000 <= vt < 0x145000000):
        return obj, vt, 0
    s19 = struct.unpack("<Q", bytes(emu.mu.mem_read(vt + 19 * 8, 8)))[0]
    return obj, vt, s19


def run_row_v2(emu, ut_, obj, s19, row_slice, ver, a7, a3_ptr=0):
    emu.mu.mem_write(ut_.STREAM_OBJ_ADDR + 0x08, struct.pack("<I", 1000))
    emu.mu.mem_write(ut_.STREAM_OBJ_ADDR + 0x10, struct.pack("<I", 0))
    emu.payload = row_slice
    emu.wire_pos = 0
    emu.reads = []
    emu.unhandled_calls = []

    rsp = ut_.STACK_BASE + ut_.STACK_SIZE - 0x2000
    emu._alloc_mode = "ctx"
    ctx_ptr = emu._alloc(0x2000)
    emu._alloc_mode = "heap"
    emu.mu.mem_write(ctx_ptr + 0x588, struct.pack("<H", ver))
    emu.mu.mem_write(rsp + 0x00, struct.pack("<Q", ut_.STOP_ADDR))
    emu.mu.mem_write(rsp + 0x28, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x30, struct.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x38, struct.pack("<Q", a7))
    emu.mu.mem_write(rsp + 0x40, struct.pack("<Q", 0))

    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], obj)
    emu.mu.reg_write(emu.REG["RDX"], ut_.STREAM_PTR_ADDR)
    emu.mu.reg_write(emu.REG["R8"], a3_ptr)
    emu.mu.reg_write(emu.REG["R9"], ctx_ptr)

    err = None
    try:
        emu.mu.emu_start(s19, ut_.STOP_ADDR, count=3_000_000)
    except Exception as exc:
        err = str(exc)
    rip = emu.mu.reg_read(emu.REG["RIP"])
    ok = err is None and rip == ut_.STOP_ADDR and emu.wire_pos > 0
    return {
        "ok": ok,
        "error": err,
        "end_rip": hex(rip),
        "bytes_consumed": emu.wire_pos,
        "reads": emu.reads,
        "unhandled": emu.unhandled_calls[:5],
    }


def from_diff_t3():  # reuse loader
    from diff_t3 import load_specific
    return load_specific


def main():
    load_specific = from_diff_t3()
    targets = [
        ("server", 0), ("client", 0), ("server", 72), ("server", 32), ("server", 71),
        ("server", 3), ("client", 3), ("server", 41), ("server", 45), ("server", 5),
    ]
    tabs = load_specific(targets)

    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for rep in range(repeats):
        for arch, tid in targets:
            payload = tabs[(arch, tid)]
            a7 = 1 if arch == "server" else 0
            ver = struct.unpack_from("<H", payload, 6)[0]
            nrows = struct.unpack_from("<I", payload, 8)[0]
            footer = len(payload) - 9
            # t32 whole-table single-call probe (no per-row framing)
            if tid == 32:
                ut_, emu, db_a3 = setup_v2()
                for label, start in (("no-flag", 13), ("flag", 14)):
                    obj, vt, s19 = construct_v2(emu, ut_, tid, 0)
                    res = run_row_v2(emu, ut_, obj, s19, payload[start:start + 2_000_000], ver, a7)
                    print(f"r{rep} t32 {label}: ok={res['ok']} cons={res['bytes_consumed']} end={start + res['bytes_consumed']} footer={footer} err={str(res['error'])[:50]} un={res['unhandled'][:1]}")
                continue
            ut_, emu, db_a3 = setup_v2()
            pos = 13
            nok, limit = 0, min(nrows, 50)
            err = None
            for r in range(limit):
                if pos >= footer:
                    err = f"row {r}: pos {pos} >= footer {footer}"
                    break
                flag = payload[pos]
                pos += 1
                obj, vt, s19 = construct_v2(emu, ut_, tid, flag)
                if s19 == 0:
                    err = f"row {r}: ctor fail flag={flag:#x}"
                    break
                res = run_row_v2(emu, ut_, obj, s19, payload[pos:pos + 65536], ver, a7)
                if not res["ok"]:
                    err = f"row {r} flag={flag:#x} cons={res['bytes_consumed']} err={str(res['error'])[:60]} rip={res['end_rip']} un={res['unhandled'][:1]}"
                    break
                pos += res["bytes_consumed"]
                nok += 1
            tag = "OK" if nok == limit else "FAIL"
            print(f"r{rep} {arch}/t{tid}: {tag} rows={nok}/{limit} end={pos} diff={footer - pos} :: {err or ''}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
