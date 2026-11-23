"""Commander's independent spot-check of t01f (gpt-6.2-sol) claims against raw editor.exe bytes.

Read-only. Each check: file offset -> expected bytes (and computed jump targets where claimed).
Run: py -V:3.12 -I scripts/t01f_spotcheck.py
"""
from __future__ import annotations
import struct, sys

ED = r"D:\tmp2b\fm24\input\editor.exe"
VA_DELTA = 0xA00          # .rdata/.debug-ish: VA = fileoff + 0xA00 (+0x140000000)
RELOC_DELTA = 0x16B600    # .reloc

def off2va(off: int, delta: int = VA_DELTA) -> int:
    return 0x140000000 + off + delta

checks = []  # (name, off, expected_bytes, note)

def chk(name, off, hexbytes, note=""):
    checks.append((name, off, bytes.fromhex(hexbytes.replace(" ", "")), note))

# --- 18-field table spot checks (access instructions & stream width immediates) ---
chk("cmnl access movsx r9d,[r12+0x154]", 0xec33aa, "41 0f bf 84 24 54 01 00 00")
chk("cmnl stream width=2 (mov r8d,2)", 0xeb7a74, "41 b8 02 00 00 00")
chk("cmnw stream width=2", 0xeb7a9a, "41 b8 02 00 00 00")
chk("cmxl stream width=2", 0xeb7ac2, "41 b8 02 00 00 00")
chk("cnor access mov [r12+0x80]", 0xec0fe7, "49 8b 8c 24 80 00 00 00")
chk("cnor stream width=4", 0xeb7bd0, "41 b8 04 00 00 00")
chk("csou access [r12+0x88]", 0xec39f4, "49 8b 8c 24 88 00 00 00")
chk("csou stream width=4", 0xeb7bf6, "41 b8 04 00 00 00")
chk("cwes stream width=4", 0xeb7c19, "41 b8 04 00 00 00")
chk("ceas stream width=4", 0xeb7c3c, "41 b8 04 00 00 00")
chk("levl stream width=1", 0xeb70ab, "41 b8 01 00 00 00")
chk("CTty stream width=1", 0xeb711a, "41 b8 01 00 00 00")
chk("wbcl stream width=2 @reloc", 0x3502604, "41 b8 02 00 00 00")
chk("wbst access lea rcx,[rbx+0x140]", 0xeb7cba, "48 8d 8b 40 01 00 00")
chk("wben access lea rcx,[rbx+0x144]", 0xeb7cd1, "48 8d 8b 44 01 00 00")
chk("cuae access mov [r12+0xf7]", 0xec10bc, "41 8a 9c 24 f7 00 00 00")
chk("cuae stream width=1", 0xeb7cf5, "41 b8 01 00 00 00")
chk("csso access mov [r12+0xf8]", 0xec21e9, "41 8a 9c 24 f8 00 00 00")
chk("csso stream width=1", 0xeb7d18, "41 b8 01 00 00 00")
chk("cfcl access mov [r12+0x120]", 0xec0f7b, "41 8b 8c 24 20 01 00 00")
chk("cbcl access [r12+0x124]", 0xec353a, "41 8b 8c 24 24 01 00 00")
chk("ctcl access [r12+0x128]", 0xec38f7, "41 8b 8c 24 28 01 00 00")

# --- 5 original L2 anchors (object-side leas) ---
chk("ccti obj+0x58 lea rdx,[rbx+0x58]", 0xeb725c, "48 8d 53 58")
chk("cnti obj+0x60 lea rdx,[rbx+0x60]", 0xeb727c, "48 8d 53 60")
chk("cpcm obj+0x68 lea rdx,[rbx+0x68]", 0xeb72bc, "48 8d 53 68")

# --- identity block 12B read: 0xeb7d84 e8 -> 0x3c60106 lea rdi? lea [rdi+8]; mov r8d,12 ---
chk("identity caller call @0xeb7d84", 0xeb7d84, "e8 b7 65 0f 00")
chk("identity lea [rdi+8] @0x3c60106", 0x3c60106, "48 8d 5f 08")
chk("identity width 12B mov r8d,12 @0x3c6010d", 0x3c6010d, "41 b8 0c 00 00 00")

# --- registration slot1 'PLgn' (known, regression) ---
chk("reg slot1 imm 'PLgn' (little-endian bytes)", 0xebf060, "c7 45 f0 6e 67 4c 50")

# --- helperB trace: thunk + slow path inside .reloc ---
chk("helperB thunk e9 @0x83caf0", 0x83caf0, "e9 7b 0e f4 02")
chk("helperB global read mov rax,[rip+...] @0x3612d74", 0x3612d74, "48 8b 05 15 c1 3d fe")
chk("helperB slowpath alloc 0xd8 @0x3612dc0", 0x3612dc0, "b9 d8 00 00 00")
chk("helperB traits+0x40=2 @0x3612e4a", 0x3612e4a, "c6 40 40 02")
chk("helperB store to +0x38 @0x3612e55", 0x3612e55, "48 89 48 38")

# --- COMP RTTI / constructor / vtable re-interpretation ---
chk("RTTI '.?AVCOMP@db@@' @0x1aaccb0", 0x1aaccb0, "2e 3f 41 56 43 4f 4d 50 40 64 62 40 40 00")
chk("ctor vptr write @0xeb5dd5", 0xeb5dd5, "48 8d 05 dc 74 9c 00 48 89 01")
chk("vtable slot5 (0-based) = 0x140ebfa40 @0x187d2e0", 0x187d2e0, "40 fa eb 40 01 00 00 00")
chk("DATABASE_TABLE RTTI prefix @0x1aad160", 0x1aad160, "2e 3f 41 56 3f 24 44 41 54 41")
chk("factory alloc 0x1b0 @0xf49129", 0xf49129, "b9 b0 01 00 00")
chk("type query returns 25 @0xed0a30", 0xed0a30, "b8 19 00 00 00 c3")

# --- COMP slot19 reader / slot21 writer dispatch ---
chk("slot19 entry =0x140ed1440 @0x187d350", 0x187d350, "40 14 ed 40 01 00 00 00")
chk("slot21 entry =0x140ed1480 @0x187d360", 0x187d360, "80 14 ed 40 01 00 00 00")
chk("slot19 jmp @0xed0a40", 0xed0a40, "e9 8b 92 dd 02")
chk("slot21 jmp @0xed0a86", 0xed0a86, "e9 95 7e fe ff")
chk("read body entry @0x3b3f0f9 (xor/init arg8)", 0x3b3f0f9, "c6 44 24 38 00 45 31 c0")
chk("read body RBX=this @0xeb7016", 0xeb7016, "48 89 cb")
chk("write body lead marker 0 @0xeb893b", 0xeb893b, "c6 44 24 28 00")

# --- computed jump targets ---
def rel32_target(off, delta=VA_DELTA):
    with open(ED, "rb") as f:
        f.seek(off)
        b = f.read(5)
    if b[0] not in (0xE8, 0xE9):
        return None, f"not e8/e9 at {off:#x}: {b.hex()}"
    rel = struct.unpack_from("<i", b, 1)[0]
    return off2va(off, delta) + 5 + rel, None

def qword(off):
    with open(ED, "rb") as f:
        f.seek(off)
        return struct.unpack("<Q", f.read(8))[0]

with open(ED, "rb") as f:
    data = f.read()

results = []
ok = 0
for name, off, expect, note in checks:
    got = data[off:off + len(expect)]
    good = got == expect
    ok += good
    results.append(("PASS" if good else "FAIL", name, off, got.hex(), expect.hex(), note))

# computed checks
t, err = rel32_target(0x83caf0)          # helperB thunk target
if err is None:
    good = t == off2va(0x3612d70, RELOC_DELTA)
    ok += good
    results.append(("PASS" if good else "FAIL", "helperB thunk -> reloc VA 0x14377e370", 0x83caf0,
                    hex(t), hex(off2va(0x3612d70, RELOC_DELTA)), ""))

t, err = rel32_target(0xed0a40)
if err is None:
    # read body entry claimed off 0x3b3f0f9 pre-loop; the e9 lands somewhere near; check the xor seq right after landing
    land_off = t - 0x140000000 - RELOC_DELTA if t >= off2va(0x3612d70, RELOC_DELTA) else t - 0x140000000 - VA_DELTA
    # determine which delta applies by range: reloc region starts at file off ~0x36110000? use VA test instead
    results.append(("INFO", "slot19 jmp lands at VA", 0xed0a40, hex(t), "", ""))

t2, err = rel32_target(0xed0a86)
if err is None:
    results.append(("INFO", "slot21 jmp lands at VA", 0xed0a86, hex(t2), "", ""))

# ctor lea target
lea_va_after = off2va(0xeb5dd5) + 7
tgt = lea_va_after + struct.unpack_from("<i", data, 0xeb5dd5 + 3)[0]
good = tgt == 0x14187DCB8
ok += good
results.append(("PASS" if good else "FAIL", "ctor lea rip+disp -> 0x14187dcb8", 0xeb5dd5, hex(tgt), hex(0x14187DCB8), ""))

# vtable slot0 at 0x187d2b8 should be a code VA; 0x187d2b0 should be a .rdata (RTTI) VA
v0 = qword(0x187d2b8); rtti = qword(0x187d2b0)
results.append(("INFO", "vptr slot0", 0x187d2b8, hex(v0), "", ""))
results.append(("INFO", "vtable[-1] (RTTI*)", 0x187d2b0, hex(rtti), "", ""))

fails = [r for r in results if r[0] == "FAIL"]
for s, name, off, got, exp, note in results:
    print(f"{s:4} {name} @ {off:#x} got={got}" + (f" exp={exp}" if exp and s == "FAIL" else "") + (f"  # {note}" if note else ""))
print(f"\n{ok} PASS / {len(fails)} FAIL / {len(results) - ok - len(fails)} INFO")
sys.exit(1 if fails else 0)
