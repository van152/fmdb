"""t72 row 0 with bit2: hook div site + allocator fnptr call, dump regs."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t111_unicorn_last11 as T
from diff_t3 import load_specific
from unicorn import UC_HOOK_CODE
import unicorn

tabs = load_specific([("server", 72)])
p = tabs[("server", 72)]
footer = len(p) - 9
ut, emu, db_a3 = T.setup_emulator_v2()
T.set_version_globals(emu, 0x0DF1)

mu = emu.mu
def hook(uc, addr, size, ud):
    r15 = uc.reg_read(unicorn.x86_const.UC_X86_REG_R15)
    r14 = uc.reg_read(unicorn.x86_const.UC_X86_REG_R14)
    rcx = uc.reg_read(unicorn.x86_const.UC_X86_REG_RCX)
    rdx = uc.reg_read(unicorn.x86_const.UC_X86_REG_RDX)
    rsp = uc.reg_read(unicorn.x86_const.UC_X86_REG_RSP)
    ret = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
    print(f"HIT {addr:#x} r14={r14:#x} r15={r15:#x} rcx={rcx:#x} rdx={rdx:#x} ret={ret:#x}")
    if addr == 0x144105b38 and r15 == 0:
        uc.emu_stop()

mu.hook_add(UC_HOOK_CODE, hook, begin=0x144105b1e, end=0x144105b3b)
# allocator fnptr call site
def hook2(uc, addr, size, ud):
    fn = struct.unpack("<Q", bytes(uc.mem_read(0x1419475D0, 8)))[0]
    rcx = uc.reg_read(unicorn.x86_const.UC_X86_REG_RCX)
    print(f"ALLOCSITE {addr:#x} fnptr={fn:#x} req={rcx:#x}")
mu.hook_add(UC_HOOK_CODE, hook2, begin=0x1444e26ad, end=0x1444e26ad)

pos = 13
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
try:
    emu.mu.emu_start(s19, ut.STOP_ADDR, count=3_000_000)
except Exception as e:
    print("EMU ERR:", e)
print("wire_pos:", emu.wire_pos)
