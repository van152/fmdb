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
def cstr(fo, maxlen=120):
    z = raw.find(b'\x00', fo, fo + maxlen)
    return raw[fo:z].decode('ascii', errors='replace') if z != -1 else raw[fo:fo+maxlen].hex()

def get_rtti(vtable_fo):
    try:
        col_va = struct.unpack_from('<Q', raw, vtable_fo - 8)[0]
        col_fo = off(col_va)
        td_rva = struct.unpack_from('<I', raw, col_fo + 12)[0]
        td_fo = off(base + td_rva)
        return cstr(td_fo + 16, 160)
    except Exception as e:
        return f'<ERR: {e}>'

print('=== Pool / debug strings ===')
for label, fo in [
    ('CLUB+0x100 pool', 0x1931296),
    ('CLUB+0xb0 pool', 0x1931268),
    ('base+0x78 item pool', 0x192b099),
]:
    print(f'  {label} @ 0x{fo:x}: {cstr(fo)!r}')

print('\n=== RTTI of known vtables ===')
vtables = [
    ('CLUB', 0x187c308),
    ('extra+0x20 item', 0x187c9d8),
    ('base0 tag 4', 0x18b86b8),
    ('base0 tag 5', 0x18b8768),
    ('base0 tag 6', 0x18b8818),
    ('base0 tag 7', 0x18b8608),
    ('base0 tag 9', 0x18b9208),
    ('base0 tag 16', 0x18b9a88),
    ('base0 tag 37', 0x18b88d8),
    ('base0 tag 38', 0x18b9428),
]
for name, vt in vtables:
    print(f'  {name:18s} @ 0x{vt:x}: {get_rtti(vt)}')

# Also scan ALL cases in base0 factory 0x14cf6d0 (table 0x14d0184)
print('\n=== ALL base0 factory tags @ 0x14cf6d0 ===')
f_start, f_end = 0x14cf6d0, fn_bounds[0x14cf6d0]
# find max switch bound in 0x14cf6d0
for i in md.disasm(raw[f_start:f_start+0x80], va(f_start)):
    print(f'  0x{off(i.address):x}: {i.mnemonic} {i.op_str}')

# Inspect ALL 41+ entries of 0x14d0184
tb = 0x14d0184
for t in range(42):
    rel = struct.unpack_from('<i', raw, tb + t*4)[0]
    arm = off(va(tb) + rel)
    # find first lea of vtable in arm..arm+0x60
    rtti = None
    vt_fo = None
    for i in md.disasm(raw[arm:min(arm+0x70, f_end)], va(arm)):
        if i.mnemonic == 'lea' and i.operands[1].type == 3 and i.reg_name(i.operands[1].mem.base) == 'rip':
            cand = off(i.address + i.size + i.operands[1].mem.disp)
            r = get_rtti(cand)
            if r.startswith('.?AV'):
                vt_fo, rtti = cand, r
                break
        if i.mnemonic in ('jmp', 'ret'):
            break
    if rtti:
        print(f'  tag {t:2d}: arm=0x{arm:x} vt=0x{vt_fo:x} RTTI={rtti}')

# Inspect t63 projections.json for all occurrences referencing +0x100 or +0xb0!
proj = json.loads((ROOT/'scratch/t63/out/projections.json').read_bytes())
print(f'\n=== t63 projections.json summary ({len(proj["occurrences"])} occs) ===')
hit_100 = []
hit_b0 = []
for occ in proj['occurrences']:
    s = json.dumps(occ)
    code = occ['code']
    p = occ.get('projection') or {}
    op = p.get('object_path')
    if '+ 0x100' in s or (op and op[0] == 0x100):
        hit_100.append((code, occ.get('xml_index'), op, p.get('family'), p.get('stop_reason') or p.get('status')))
    if '+ 0xb0' in s or (op and op[0] == 0xb0):
        hit_b0.append((code, occ.get('xml_index'), op, p.get('family'), p.get('stop_reason') or p.get('status')))

print(f'Mentions +0x100 ({len(hit_100)}):')
for x in hit_100: print(' ', x)
print(f'Mentions +0xb0 ({len(hit_b0)}):')
for x in hit_b0: print(' ', x)

# Also find ALL instructions in CLUB_GET (0xe89a00), CLUB_SET (0xe82aa0), and their base functions
# that access +0x100 or +0xb0!
def scan_fn_for_offsets(fn_fo, label, target_disps=(0x100, 0xb0)):
    end = fn_bounds.get(fn_fo)
    if not end:
        print(f'No pdata for {label} @ 0x{fn_fo:x}')
        return
    print(f'\n=== {label} @ 0x{fn_fo:x}..0x{end:x} ===')
    calls = set()
    hits = []
    for i in md.disasm(raw[fn_fo:end], va(fn_fo)):
        fo = off(i.address)
        if i.mnemonic in ('call', 'jmp') and len(i.operands) == 1 and i.operands[0].type == 2:
            try:
                tgt = off(i.operands[0].imm)
                if not (fn_fo <= tgt < end):
                    calls.add((fo, i.mnemonic, tgt))
            except Exception:
                pass
        for o in i.operands:
            if o.type == 3 and o.mem.disp in target_disps and i.reg_name(o.mem.base) not in ('rsp', 'rbp', 'rip'):
                hits.append((fo, f'{i.mnemonic} {i.op_str}'))
    print(f'  Hits on +0x100/+0xb0 ({len(hits)}):')
    for fo, ins in hits:
        print(f'    0x{fo:07x}: {ins}')
    # Print tail jumps / external calls to base class getters/setters
    tail_jmps = [(fo, m, t) for fo, m, t in sorted(calls) if m == 'jmp']
    print(f'  External tail jmps ({len(tail_jmps)}):')
    for fo, m, t in tail_jmps[:30]:
        print(f'    0x{fo:07x}: {m} 0x{t:x}')

scan_fn_for_offsets(0xe89a00, 'CLUB_GET')
scan_fn_for_offsets(0xe82aa0, 'CLUB_SET')
scan_fn_for_offsets(0xe5c550, 'CLUB_fixup')
scan_fn_for_offsets(0xe5f3d0, 'CLUB_slot43_extra_fixup')
