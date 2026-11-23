"""Deep static inspection of all remaining CLUB+0x100 and CLUB+0xb0 helpers, jump tables, and fixups."""
import json, struct, sys
from pathlib import Path
from collections import defaultdict
sys.path.append(r'D:\tmp2b\fm24\tools\python')
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r'D:\tmp2b\fm24-db')
EXE = Path(r'D:\tmp2b\fm24\input\editor.exe')
raw = EXE.read_bytes()
pe = pefile.PE(data=raw, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
pe.parse_data_directories(directories=[3])
fn_bounds = {
    pe.get_offset_from_rva(x.struct.BeginAddress): pe.get_offset_from_rva(x.struct.EndAddress)
    for x in pe.DIRECTORY_ENTRY_EXCEPTION
}
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

def va(o): return base + pe.get_rva_from_offset(o)
def off(v): return pe.get_offset_from_rva(v - base)
def is_4cc(v):
    v &= 0xffffffff
    b = v.to_bytes(4, 'big')
    return b.decode('ascii') if all(0x20 <= x <= 0x7e for x in b) else None

def resolve_thunk(fo):
    if fo in fn_bounds:
        return fo
    i0 = next(md.disasm(raw[fo:fo+15], va(fo), 1))
    if i0.mnemonic == 'jmp' and i0.operands[0].type == 2:
        return off(i0.operands[0].imm)
    return fo

def dump_fn(fo, label, max_ins=2000):
    fo = resolve_thunk(fo)
    end = fn_bounds.get(fo)
    if not end:
        return [f'=== {label} @ 0x{fo:x}: NO PDATA ===']
    out = [f'=== {label} @ 0x{fo:x}..0x{end:x} (VA 0x{va(fo):x}) ===']
    for k, i in enumerate(md.disasm(raw[fo:end], va(fo))):
        if k >= max_ins:
            out.append('... truncated ...')
            break
        ifo = off(i.address)
        ex = ''
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            try:
                t = off(i.operands[0].imm)
                ex = f'  ; -> 0x{t:x}'
                if not (fo <= t < end):
                    t2 = resolve_thunk(t)
                    if t2 != t: ex += f' (thunk->0x{t2:x})'
            except Exception: pass
        elif len(i.operands) >= 2 and i.operands[1].type == 2:
            imm = i.operands[1].imm & 0xffffffff
            fc = is_4cc(imm)
            if fc: ex = f"  ; 4CC '{fc}'"
            else:
                fc2 = is_4cc((-imm) & 0xffffffff)
                if fc2: ex = f"  ; -4CC '{fc2}'"
        elif i.mnemonic == 'lea' and i.operands[1].type == 3:
            if i.reg_name(i.operands[1].mem.base) == 'rip':
                rfo = off(i.address + i.size + i.operands[1].mem.disp)
                ex = f'  ; rip->0x{rfo:x}'
            else:
                disp = i.operands[1].mem.disp
                fc2 = is_4cc((-disp) & 0xffffffff)
                if fc2: ex = f"  ; -4CC '{fc2}'"
        out.append(f'  0x{ifo:07x}: {i.mnemonic:8s} {i.op_str}{ex}')
    return out

# 1. Dump key functions
lines = []
for label, fo in [
    ('CLUB_extra_fixup_slot42', 0x3aae490),
    ('CLUB_EXTRA_SET_e57de0', 0xe57de0),
    ('TC_EXTRA_SET_11cf6e0', 0x11cf6e0),
    ('TC_GET2_tail_11f2a60', 0x11f2a60),  # inside TC_GET2! Let's dump from 0x11f2000..0x11f2f64 separately
    ('ttcl_helper_3eaca60', 0x3eaca60),
    ('kit_helper_44df7b0', 0x44df7b0),
    ('BASE_extra_writer_11d53f0', 0x11d53f0),
]:
    if fo == 0x11f2a60:
        continue
    lines.extend(dump_fn(fo, label))

# Also dump TC_GET2 tail 0x11f2800..0x11f2f64
lines.append('=== TC_GET2 tail 0x11f2800..0x11f2f64 ===')
for i in md.disasm(raw[0x11f2800:0x11f2f64], va(0x11f2800)):
    ifo = off(i.address)
    ex = ''
    if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
        try:
            t = off(i.operands[0].imm)
            ex = f'  ; -> 0x{t:x}'
            t2 = resolve_thunk(t)
            if t2 != t: ex += f' (thunk->0x{t2:x})'
        except Exception: pass
    elif len(i.operands) >= 2 and i.operands[1].type == 2:
        fc = is_4cc(i.operands[1].imm)
        if fc: ex = f"  ; 4CC '{fc}'"
    lines.append(f'  0x{ifo:07x}: {i.mnemonic:8s} {i.op_str}{ex}')

Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_deep.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Wrote {len(lines)} lines to disasm_deep.txt')

# 2. Decode ALL jump tables in 0x1520050, TC_GET2 (0x11f0690), TC_SET2 (0x11f4570), CLUB_GET (0xe89a00), CLUB_SET (0xe82aa0)
# Specifically decode 0x1520f2c (CfpC + 0..0x2f)
print('\n=== 0x1520050 jump table @ 0x1520f2c (base CfpC, 0..0x2f) ===')
tb = 0x1520f2c
for j in range(0x30):
    rel = struct.unpack_from('<i', raw, tb + j*4)[0]
    arm = off(va(tb) + rel)
    fc = is_4cc(0x43667043 + j)
    if arm != 0x1520225:  # default
        # show first 3 insns
        ins = [f'{x.mnemonic} {x.op_str}' for x in list(md.disasm(raw[arm:arm+24], va(arm)))[:4]]
        print(f"  [{j:2d}] '{fc}' -> 0x{arm:x}: {ins}")

# Check double constant at 0xe8a50d (rip + 0x9152fb)
i_div = next(md.disasm(raw[0xe8a50d:0xe8a520], va(0xe8a50d), 1))
c_fo = off(i_div.address + i_div.size + i_div.operands[1].mem.disp)
print(f'\nCuf1..9 double divisor @ 0x{c_fo:x}: {struct.unpack_from("<d", raw, c_fo)[0]}')

# Check what 0xe8c099 receives in rcx! Disassemble 0xe8c070..0xe8c0c5
print('\n=== Context before 0xe8c099 (supporter profile dispatch) ===')
for i in md.disasm(raw[0xe8c060:0xe8c0c5], va(0xe8c060)):
    print(f'  0x{off(i.address):x}: {i.mnemonic} {i.op_str}')
# Check all callers/jumps to 0xe8c090..0xe8c0a0 inside CLUB_GET
for i in md.disasm(raw[0xe89a00:fn_bounds[0xe89a00]], va(0xe89a00)):
    if i.mnemonic.startswith('j') and i.operands[0].type == 2:
        t = off(i.operands[0].imm)
        if 0xe8c088 <= t <= 0xe8c0a5:
            print(f'  jump to 0x{t:x} from 0x{off(i.address):x}')
# Also check 0xe8b330..0xe8b3e0 and 0xe8bf50..0xe8bfa0
print('\n=== Check +0xf8 vs +0x10c in CLUB_GET ===')
for i in md.disasm(raw[0xe89a00:fn_bounds[0xe89a00]], va(0xe89a00)):
    if any(o.type == 2 and o.imm in (0xf8, 0x10c) for o in i.operands) or '+ 0xf8]' in i.op_str or '+ 0x10c]' in i.op_str:
        print(f'  0x{off(i.address):x}: {i.mnemonic} {i.op_str}')

# Check 1scl/1sbc/2scl/2sbc/3scl/3sbc/2tcl/2tbc/3tcl/3tbc in CLUB_GET, CLUB_SET, TC_GET2, TC_SET2, and ENTIRE .text!
print('\n=== Search for kit colour 4CCs (1scl..3tbc, ttcl, tbcl, C1sq) in CLUB_GET/SET and TC_GET2/SET2 ===')
target_codes = ['1scl','1sbc','2scl','2sbc','3scl','3sbc','2tcl','2tbc','3tcl','3tbc','ttcl','tbcl','C1sq','CBWa','CBWc','CBWd','CBWf','CBWo','CBDa','CBDc','CBDd','CBDf','CBDo']
target_ints = {int.from_bytes(c.encode(), 'big'): c for c in target_codes}
for fn_name, fn_fo in [('CLUB_GET', 0xe89a00), ('CLUB_SET', 0xe82aa0), ('TC_GET2', 0x11f0690), ('TC_SET2', 0x11f4570)]:
    end = fn_bounds[fn_fo]
    for i in md.disasm(raw[fn_fo:end], va(fn_fo)):
        for o in i.operands:
            if o.type == 2:
                u = o.imm & 0xffffffff
                if u in target_ints:
                    print(f'  {fn_name} 0x{off(i.address):x}: {i.mnemonic} {i.op_str}  ({target_ints[u]})')
                elif (-u)&0xffffffff in target_ints:
                    print(f'  {fn_name} 0x{off(i.address):x}: {i.mnemonic} {i.op_str}  (-{target_ints[(-u)&0xffffffff]})')
            elif o.type == 3 and o.mem.disp != 0:
                d = (-o.mem.disp) & 0xffffffff
                if d in target_ints:
                    print(f'  {fn_name} 0x{off(i.address):x}: {i.mnemonic} {i.op_str}  (-{target_ints[d]})')
