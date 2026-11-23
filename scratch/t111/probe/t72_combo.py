"""t72: stream bit2 + config globals + allocator hook, run rows 0-5."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t111_unicorn_last11 as T
from diff_t3 import load_specific
from unicorn import UC_HOOK_CODE
import unicorn.x86_const as XC

tabs = load_specific([("server", 72)])
p = tabs[("server", 72)]
footer = len(p) - 9
ut, emu, db_a3 = T.setup_emulator_v2()
T.set_version_globals(emu, 0x0DF1)
mu = emu.mu

def on_alloc(uc, address, size, ud):
    sz = uc.reg_read(XC.UC_X86_REG_R8)
    rsp = uc.reg_read(XC.UC_X86_REG_RSP)
    ret = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
    ptr = emu._alloc(max(sz, 16), address)
    uc.reg_write(XC.UC_X86_REG_RAX, ptr)
    uc.reg_write(XC.UC_X86_REG_RSP, rsp + 8)
    uc.reg_write(XC.UC_X86_REG_RIP, ret)
mu.hook_add(UC_HOOK_CODE, on_alloc, begin=0x1412d31c0, end=0x1412d31c0)

# config globals for t72 typed-element layout
for g, v in ((0x141B60352, 1), (0x141B5FC2C, 1), (0x141B55C2C, 1)):
    mu.mem_write(g, struct.pack("<B", v))

pos = 13
n_ok = 0
err = None
for r in range(6):
    if pos >= footer:
        err = f"row {r}: pos>=footer"
        break
    flag = p[pos]; pos += 1
    obj, vt, s19 = T.construct_v2(ut, emu, 72, flag)
    emu.mu.mem_write(ut.STREAM_OBJ_ADDR + 0x0C, struct.pack("<I", 2))
    emu.payload = p[pos:footer]
    emu.wire_pos = 0
    emu.reads = []
    rsp = ut.STACK_BASE + ut.STACK_SIZE - 0x2000
    emu._alloc_mode = "ctx"
    ctx_ptr = emu._alloc(0x2000)
    emu._alloc_mode = "heap"
    emu.mu.mem_write(ctx_ptr + 0x588, struct.pack("<H", 0x0DF1))
    emu.mu.mem_write(rsp, struct.pack("<Q", ut.STOP_ADDR))
    emu.mu.reg_write(emu.REG["RSP"], rsp)
    emu.mu.reg_write(emu.REG["RCX"], obj)
    emu.mu.reg_write(emu.REG["RDX"], ut.STREAM_PTR_ADDR)
    emu.mu.reg_write(emu.REG["R8"], 0)
    emu.mu.reg_write(emu.REG["R9"], ctx_ptr)
    e = None
    try:
        emu.mu.emu_start(s19, ut.STOP_ADDR, count=3_000_000)
    except Exception as exc:
        e = str(exc)
    rip = mu.reg_read(emu.REG["RIP"])
    rax = mu.reg_read(emu.REG["RAX"])
    ok = e is None and rip == ut.STOP_ADDR and rax == 1
    print(f"row{r} flag={flag:#x} ok={ok} consumed={emu.wire_pos} rax={rax:#x} err={e} "
          f"len0={emu.reads[0]['hex'] if emu.reads else '-'}", flush=True)
    if not ok:
        err = f"row {r}: rip={rip:#x} rax={rax:#x} err={e}"
        for rd in emu.reads[-6:]:
            print("   ", {k: rd.get(k) for k in ("wire_pos","n","u_val","hex","caller")})
        break
    pos += emu.wire_pos
    n_ok += 1
print("end_pos:", pos, "footer:", footer, "diff:", footer - pos)
