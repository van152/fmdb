"""t72 row 0 with stream+0xc bit2 set (skip optional 1B after ID-refs)."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t111_unicorn_last11 as T
from diff_t3 import load_specific

tabs = load_specific([("server", 72)])
p = tabs[("server", 72)]
footer = len(p) - 9
ut, emu, db_a3 = T.setup_emulator_v2()
T.set_version_globals(emu, 0x0DF1)
vt_fb = T.load_vtable_fallback()

# patch run_row_v2: after its stream writes, set flags dword bit2
orig = T.run_row_v2
def run_row_v2b(ut, emu, obj, s19, row_slice, ver, a7, a3_ptr=0):
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x0C, struct.pack("<I", 2))
    return orig(ut, emu, obj, s19, row_slice, ver, a7, a3_ptr)
# emulate by re-writing stream flag after orig's writes: orig writes +8/+10 only, so write +0xc AFTER calling orig is too late (orig runs emu). So inline copy:
def run_row_v2c(ut, emu, obj, s19, row_slice, ver, a7, a3_ptr=0):
    import struct as _s
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x08, _s.pack("<I", 1000))
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x10, _s.pack("<I", 0))
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x0C, _s.pack("<I", 2))
    emu.payload = row_slice
    emu.wire_pos = 0
    emu.reads = []
    emu.unhandled_calls = []
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu._alloc_mode = "ctx"
    ctx_ptr = emu._alloc(0x2000)
    emu._alloc_mode = "heap"
    emu.mu.mem_write(ctx_ptr + 0x588, _s.pack("<H", ver))
    emu.mu.mem_write(rsp + 0x00, _s.pack("<Q", ut.STOP_ADDR))
    emu.mu.mem_write(rsp + 0x28, _s.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x30, _s.pack("<Q", 0))
    emu.mu.mem_write(rsp + 0x38, _s.pack("<Q", a7))
    emu.mu.mem_write(rsp + 0x40, _s.pack("<Q", 0))
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
    ok = err is None and rip == ut.STOP_ADDR and emu.wire_pos > 0
    return {"ok": ok, "error": err if err else (None if ok else "timeout"), "end_rip": hex(rip),
            "bytes_consumed": emu.wire_pos, "reads": emu.reads, "unhandled": emu.unhandled_calls[:5]}

pos = 13
flag = p[pos]; pos += 1
obj, vt, s19 = T.construct_v2(ut, emu, 72, flag)
res = run_row_v2c(ut, emu, obj, s19, p[pos:footer], 0x0DF1, 1)
print(f"flag={flag:#x} ok={res['ok']} consumed={res['bytes_consumed']} err={res['error']} rip={res['end_rip']}")
for rd in res["reads"]:
    print("  ", {k: rd.get(k) for k in ("wire_pos", "n", "dst_kind", "u_val", "hex", "caller") if rd.get(k) is not None or k in ("wire_pos","n","dst_kind")})
