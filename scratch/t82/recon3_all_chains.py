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
    if not (0 <= v <= 0xffffffff): return None
    b = v.to_bytes(4, 'big')
    if all(0x20 <= x <= 0x7e for x in b):
        return b.decode('ascii')
    return None

def disasm_fn_to_list(start, name):
    end = fn_bounds.get(start)
    if not end:
        # check if thunk
        i0 = next(md.disasm(raw[start:start+15], va(start), 1))
        if i0.mnemonic == 'jmp' and i0.operands[0].type == 2:
            t = off(i0.operands[0].imm)
            return [f'=== {name} @ 0x{start:x} THUNK -> 0x{t:x} ==='] + disasm_fn_to_list(t, f'{name}_impl')
        return [f'=== {name} @ 0x{start:x}: NO PDATA ===']
    out = [f'=== {name} @ 0x{start:x}..0x{end:x} (VA 0x{va(start):x}) ===']
    for i in md.disasm(raw[start:end], va(start)):
        fo = off(i.address)
        extra = ''
        if i.mnemonic in ('call', 'jmp') and len(i.operands) == 1 and i.operands[0].type == 2:
            try:
                tgt = off(i.operands[0].imm)
                extra = f'  ; -> fo 0x{tgt:x}'
                if not (start <= tgt < end):
                    tins = next(md.disasm(raw[tgt:tgt+15], va(tgt), 1))
                    if tins.mnemonic == 'jmp' and tins.operands[0].type == 2:
                        extra += f' (thunk -> 0x{off(tins.operands[0].imm):x})'
            except Exception:
                pass
        elif i.mnemonic in ('cmp', 'add', 'sub', 'mov') and len(i.operands) >= 2 and i.operands[1].type == 2:
            imm = i.operands[1].imm & 0xffffffff
            fc = is_4cc(imm)
            if fc:
                extra = f"  ; 4CC '{fc}'"
            else:
                fc2 = is_4cc((-imm) & 0xffffffff)
                if fc2:
                    extra = f"  ; -4CC '{fc2}'"
        for o in i.operands:
            if o.type == 3 and i.reg_name(o.mem.base) == 'rip':
                rip_va = i.address + i.size + o.mem.disp
                try:
                    rip_fo = off(rip_va)
                    extra += f'  ; rip -> fo 0x{rip_fo:x}'
                except Exception:
                    pass
        out.append(f'  0x{fo:07x}: {i.mnemonic:8s} {i.op_str}{extra}')
    return out

# 1. Dump all leaf readers & fixups
leaf_lines = []
leaves = [
    ('CLUB_slot43_extra_fixup', 0xe5f3d0),
    ('extra_da_reader_4348ef0', 0x4348ef0),
    ('extra_78_election_4342940', 0x4342940),
    ('extra_f8_10c_4340450', 0x4340450),
    ('extra_28_item_3aaf9e0', 0x3aaf9e0),
    ('extra_20_item_3ab0750', 0x3ab0750),
    ('extra_48_39aa1f0', 0x39aa1f0),
    ('extra_30_13f86a0', 0x13f86a0),
    ('extra_38_13fd6e0', 0x13fd6e0),
    ('extra_70_item_42674a0', 0x42674a0),
    ('extra_50_ea3bc0', 0xea3bc0),
    ('extra_68_item_4349ce0', 0x4349ce0),
    ('extra_40_2468290', 0x2468290),
    ('base_78_kit_4330ce0', 0x4330ce0),
    ('base_18_item_3ea5150', 0x3ea5150),
    ('base_48_4387ab0', 0x4387ab0),
    ('base0_t4_42c8f90', 0x42c8f90),
    ('base0_t5_42d2710', 0x42d2710),
    ('base0_t6_42d6a10', 0x42d6a10),
    ('base0_t7_42c66f0', 0x42c66f0),
    ('base0_t9_42dba50', 0x42dba50),
    ('base0_t16_14d7530', 0x14d7530),
    ('base0_t37_42d9380', 0x42d9380),
    ('base0_t38_14da470', 0x14da470),
]
for name, fo in leaves:
    leaf_lines.extend(disasm_fn_to_list(fo, name))
Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_leaves.txt').write_text('\n'.join(leaf_lines) + '\n', encoding='utf-8')
print(f'Wrote {len(leaf_lines)} lines to disasm_leaves.txt')

# 2. Inspect TEAM_CONTAINER_GET/SET and ALL helpers called/tail-jumped from CLUB_GET/SET
helper_fns = [
    ('helper_get_1520050', 0x1520050),
    ('helper_get_e96f20', 0xe96f20),
    ('helper_get_e96a10', 0xe96a10),
    ('helper_get_e97a10', 0xe97a10),
    ('helper_get_15356f0', 0x15356f0),
    ('TC_GET_11e8af0', 0x11e8af0),
    ('TC_GET2_11f0690', 0x11f0690),
    ('TC_SET_11e8b40', 0x11e8b40),
    ('TC_SET2_11f4570', 0x11f4570),
    ('helper_set_e57de0', 0xe57de0),
    ('helper_set_e878d0', 0xe878d0),
    ('helper_set_e71650', 0xe71650),
    ('helper_set_e87200', 0xe87200),
    ('helper_set_e71520', 0xe71520),
    ('helper_set_e87be0', 0xe87be0),
    ('helper_set_1536380', 0x1536380),
]
h_lines = []
for name, fo in helper_fns:
    lines = disasm_fn_to_list(fo, name)
    h_lines.extend(lines)
    # quick summary of +0x100/+0xb0/4CC hits
    b0_hits = [l for l in lines if '+ 0xb0]' in l or '+ 0x100]' in l]
    fc_hits = [l for l in lines if '; 4CC ' in l or '; -4CC ' in l]
    print(f'  {name:22s}: {len(lines):4d} ins, +0x100/+0xb0={len(b0_hits):2d}, 4CC_imms={len(fc_hits):3d}')
Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_helpers.txt').write_text('\n'.join(h_lines) + '\n', encoding='utf-8')
print(f'Wrote {len(h_lines)} lines to disasm_helpers.txt')
