"""t72 row 0 with bit2 + allocator hooks routed to emu._alloc."""
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

fires = []
def make_hook(name, size_reg):
    def on_alloc(uc, address, size, ud):
        sz = uc.reg_read(size_reg)
        rsp = uc.reg_read(XC.UC_X86_REG_RSP)
        ret = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
        ptr = emu._alloc(max(sz, 16), address)
        uc.reg_write(XC.UC_X86_REG_RAX, ptr)
        uc.reg_write(XC.UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(XC.UC_X86_REG_RIP, ret)
        fires.append((name, sz, ptr, hex(ret)))
        print(f"{name}: size={sz:#x} -> {ptr:#x} ret={ret:#x}", flush=True)
    return on_alloc

mu.hook_add(UC_HOOK_CODE, make_hook("fallback_0x1412d31c0", XC.UC_X86_REG_R8), begin=0x1412d31c0, end=0x1412d31c0)
mu.hook_add(UC_HOOK_CODE, make_hook("grow_0x1412d2f90", XC.UC_X86_REG_RDX), begin=0x1412d2f90, end=0x1412d2f90)

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
rip = mu.reg_read(emu.REG["RIP"])
print(f"wire_pos={emu.wire_pos} end_rip={rip:#x}")
for rd in emu.reads[12:]:
    print("  ", {k: rd.get(k) for k in ("wire_pos","n","dst_kind","u_val","hex","caller") if rd.get(k) is not None or k in ("wire_pos","n","dst_kind")})
