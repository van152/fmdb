import json, struct, sys
from pathlib import Path
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
def find_fn(fo):
    for a, z in fn_bounds.items():
        if a <= fo < z:
            return a, z
    return None

def disasm_fn(start, name, out_lines, max_ins=5000):
    end = fn_bounds.get(start)
    if not end:
        out_lines.append(f'=== {name} @ 0x{start:x}: NO PDATA ===')
        return
    out_lines.append(f'=== {name} @ 0x{start:x}..0x{end:x} (VA 0x{va(start):x}) ===')
    for idx, i in enumerate(md.disasm(raw[start:end], va(start))):
        if idx >= max_ins:
            out_lines.append('... truncated ...')
            break
        fo = off(i.address)
        extra = ''
        if i.mnemonic in ('call', 'jmp') and len(i.operands) == 1 and i.operands[0].type == 2:
            try:
                tgt = off(i.operands[0].imm)
                extra = f'  ; -> fo 0x{tgt:x}'
                # check if thunk
                tins = next(md.disasm(raw[tgt:tgt+15], va(tgt), 1))
                if tins.mnemonic == 'jmp' and tins.operands[0].type == 2:
                    tgt2 = off(tins.operands[0].imm)
                    extra += f' (thunk -> 0x{tgt2:x})'
            except Exception:
                pass
        elif any(o.type == 3 and i.reg_name(o.mem.base) == 'rip' for o in i.operands):
            for o in i.operands:
                if o.type == 3 and i.reg_name(o.mem.base) == 'rip':
                    rip_va = i.address + i.size + o.mem.disp
                    try:
                        rip_fo = off(rip_va)
                        extra = f'  ; rip -> fo 0x{rip_fo:x} (VA 0x{rip_va:x})'
                    except Exception:
                        pass
        out_lines.append(f'  0x{fo:07x}: {i.mnemonic:8s} {i.op_str}{extra}')

lines = []
# Check CLUB vtable slots 0..45
vptr = 0x187c308
lines.append('=== CLUB vtable @ 0x187c308 ===')
for s in range(46):
    q = struct.unpack_from('<Q', raw, vptr + s*8)[0]
    try:
        t = off(q)
        tins = next(md.disasm(raw[t:t+15], va(t), 1))
        th = ''
        if tins.mnemonic == 'jmp' and tins.operands[0].type == 2:
            th = f' -> 0x{off(tins.operands[0].imm):x}'
        lines.append(f'  slot {s:2d} (+0x{s*8:03x}): VA 0x{q:x} fo 0x{t:x}{th}')
    except Exception:
        lines.append(f'  slot {s:2d} (+0x{s*8:03x}): VA 0x{q:x}')

# Disassemble extra ctor 0x3aaba20, aux_row_reader 0xe5d210, base aux reader 0x11d3200
disasm_fn(0x3aaba20, 'CLUB_EXTRA_ctor', lines)
disasm_fn(0xe5d210, 'CLUB_aux_row_reader', lines)
disasm_fn(0x11d3200, 'BASE_aux_row_reader', lines)

Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_core.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Wrote {len(lines)} lines to disasm_core.txt')

# Also inspect club.xml fields and t63/t71/t79 status
master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
t57 = json.loads((ROOT/'scratch/t57/out/field_map.json').read_bytes())
t63 = json.loads((ROOT/'scratch/t63/out/field_map_r2.json').read_bytes())
t71 = json.loads((ROOT/'scratch/t71/out/field_map_r3.json').read_bytes())
t79 = json.loads((ROOT/'scratch/t79/out/field_map.json').read_bytes())

print(f'club.xml total fields: {len(club_fields)}')
# Count unique codes vs duplicate codes
from collections import Counter
cc = Counter(f['field'] for f in club_fields)
print('Duplicate codes in club.xml:', {k:v for k,v in cc.items() if v > 1})

# Print summary of t57/t63/t71/t79 club fields
print('t57 grades:', Counter(f['grade'] for f in t57['fields']))
print('t63 grades:', Counter(f['grade'] for f in t63['fields']))
print('t71 grades:', Counter(f['grade'] for f in t71['fields']))
print('t79 club keys:', list(t79.keys()))

# List CBW*, CBD*, 1s*, 2s*, 3s*, 2t*, 3t*, C1*, C2* etc in club.xml
interesting = []
for idx, f in enumerate(club_fields):
    c = f['field']
    if c.startswith(('CB', '1s', '2s', '3s', '2t', '3t', 'C1', 'C2')):
        interesting.append((idx, c, f.get('type'), f.get('name'), f.get('enum_ref'), f.get('dependencies')))
print(f'\nInteresting prefix fields ({len(interesting)}):')
for row in interesting:
    print(' ', row)
