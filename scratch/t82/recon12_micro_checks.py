"""Micro-checks to achieve 100% static + semantic closure for t82:
1. Disassemble exact getter arms for Csth, Cpfr/C2pf/Cdfo/Cafo, Csly..Cspe (0x1520050), Cuf1..9/Cf10, TCht, Catd/Cmna/Cmxa, Election (0xe96f20), Crkt (0xe586a0).
2. Disassemble item getters for list fields: Cscm(0xeaf720), CPsL(0x3b0c770), Cspb(0x11f8990), Cren(0x3ec49f0), TCrs(0x155a320), pcpt(0x42f5660), and vtable[+0x28] for tags 4,5,6,7,9,16,37.
3. Find ALL callers of 0x3ebcd50 (11ea010) and 0x43462a0 (1522180) and 0x3ebd740 (11ea2b0) across the executable.
4. Scan executable for references to extra+0xda, extra+0x123, base+0xac (in CLUB/TC code) and STARTING_RECORD (0x187d538 / 0x1930155).
5. Check master.json['enums']['foms'] for values 62, 63, 64, and check if any prior task (t57/t63/t71/t79) ever gave L3 to an enum with enum_ref=None.
"""
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
fn_bounds = {pe.get_offset_from_rva(x.struct.BeginAddress): pe.get_offset_from_rva(x.struct.EndAddress) for x in pe.DIRECTORY_ENTRY_EXCEPTION}
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

def va(o): return base + pe.get_rva_from_offset(o)
def off(v): return pe.get_offset_from_rva(v - base)
def is_4cc(v):
    v &= 0xffffffff
    b = v.to_bytes(4, 'big')
    return b.decode('ascii') if all(0x20 <= x <= 0x7e for x in b) else None
def find_fn(fo):
    for a, z in fn_bounds.items():
        if a <= fo < z: return a, z
    return None
def resolve_thunk(fo):
    if fo in fn_bounds: return fo
    try:
        i0 = next(md.disasm(raw[fo:fo+15], va(fo), 1))
        if i0.mnemonic == 'jmp' and i0.operands[0].type == 2: return off(i0.operands[0].imm)
    except Exception: pass
    return fo

def dump_range(s, e, label):
    out = [f'=== {label} @ 0x{s:x}..0x{e:x} (VA 0x{va(s):x}) ===']
    for i in md.disasm(raw[s:e], va(s)):
        ifo = off(i.address)
        ex = ''
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            try:
                t = off(i.operands[0].imm)
                ex = f'  ; -> 0x{t:x}'
                if not (s <= t < e):
                    t2 = resolve_thunk(t)
                    if t2 != t: ex += f' (thunk->0x{t2:x})'
            except Exception: pass
        elif len(i.operands) >= 2 and i.operands[1].type == 2:
            fc = is_4cc(i.operands[1].imm)
            if fc: ex = f"  ; 4CC '{fc}'"
        out.append(f'  0x{ifo:07x}: {i.mnemonic:8s} {i.op_str}{ex}')
    return out

def dump_fn(fo, label, max_b=0x450):
    fo = resolve_thunk(fo)
    b = find_fn(fo)
    s, e = b if b else (fo, fo + max_b)
    if e - s > 0x900: e = s + max_b
    return dump_range(s, e, label)

lines = []
# 1. Exact getter arms
for lbl, s, e in [
    ('CLUB_GET_Csth', 0xe8cedb, 0xe8cf50),
    ('CLUB_GET_Cpfr', 0xe8bb15, 0xe8bb80),
    ('CLUB_GET_C2pf', 0xe8e422, 0xe8e490),
    ('CLUB_GET_Cdfo', 0xe8e016, 0xe8e080),
    ('CLUB_GET_Cafo', 0xe8b4f3, 0xe8b560),
    ('CLUB_GET_Cf10', 0xe8c907, 0xe8c990),
    ('CLUB_GET_Cuf2..Cuf9', 0xe8ed46, 0xe8f0f0),
    ('TC_GET2_TCht', 0x11f1fd0, 0x11f2055),
    ('TC_GET2_Catd', 0x11f21bf, 0x11f2220),
    ('TC_GET2_Cmna', 0x11f1b9a, 0x11f1bf0),
    ('TC_GET2_Cmxa', 0x11f0e5a, 0x11f0ec0),
]:
    lines.extend(dump_range(s, e, lbl))

lines.extend(dump_fn(0xe586a0, 'Crkt_HELPER_e586a0', 0x200))
lines.extend(dump_fn(0x1520050, 'SUPPORTER_GET_1520050', 0x900))
lines.extend(dump_fn(0xe96f20, 'ELECTION_GET_e96f20', 0x400))

# 2. Item getters for list fields
for lbl, fo in [
    ('Cscm_ITEM_eaf720', 0xeaf720),
    ('CPsL_ITEM_3b0c770', 0x3b0c770),
    ('Cspb_ITEM_GET_11f8990', 0x11f8990),
    ('Cren_ITEM_GET_3ec49f0', 0x3ec49f0),
    ('TCrs_ITEM_GET_155a320', 0x155a320),
    ('pcpt_ITEM_GET_42f5660', 0x42f5660),
]:
    lines.extend(dump_fn(fo, lbl, 0x400))

# Also dump vtable[+0x28] (get property) for tags 4, 5, 6, 7, 9, 16, 37
print('=== 1. base+0x00 vtable[+0x28] (get_property) & vtable[+0x30] (set_property) ===')
for tag, vt, nm in [
    (4,  0x18b86b8, 'COMPETITION_BONUS_INFO'),
    (5,  0x18b8768, 'NEXT_SALE_PERCENTAGE_INFO'),
    (6,  0x18b8818, 'APPEARANCE_MONEY_INFO'),
    (7,  0x18b8608, 'PLAYER_BUY_BACK_INFO'),
    (9,  0x18b9208, 'STARTING_PLAYER_RECORD_INFO'),
    (16, 0x18b9a88, 'CLUB_CUP_POINTS'),
    (37, 0x18b88d8, 'EPPP_APPEARANCE_MONEY_INFO'),
]:
    g = resolve_thunk(off(struct.unpack_from('<Q', raw, vt + 0x28)[0]))
    st = resolve_thunk(off(struct.unpack_from('<Q', raw, vt + 0x30)[0]))
    print(f'  tag={tag:2d} {nm:28s}: vt[+28]get=0x{g:x} vt[+30]set=0x{st:x}')
    if tag in (4, 5, 6, 7, 37):
        lines.extend(dump_fn(g, f'VTAG{tag}_{nm}_GET', 0x400))

Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_recon12.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Wrote {len(lines)} lines to disasm_recon12.txt')

# 3. Check sections & scan executable sections for calls to 0x11ea010(3ebcd50) & 0x1522180(43462a0) & LEA to STARTING_RECORD
print('\n=== 2. PE sections ===')
exec_secs = []
for s in pe.sections:
    nm = s.Name.rstrip(b'\x00').decode('ascii', 'replace')
    print(f'  {nm:10s} raw=0x{s.PointerToRawData:x}..0x{s.PointerToRawData+s.SizeOfRawData:x} chars=0x{s.Characteristics:x}')
    if s.Characteristics & 0x20000000:
        exec_secs.append((nm, s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData))

def find_direct_calls_to(target_fo):
    tva = va(target_fo)
    hits = []
    for nm, a, z in exec_secs:
        pos = a
        while pos < z - 5:
            idx = raw.find(b'\xe8', pos, z - 4)
            if idx == -1: break
            disp = struct.unpack_from('<i', raw, idx + 1)[0]
            if va(idx + 5) + disp == tva:
                fn = find_fn(idx)
                hits.append((idx, fn[0] if fn else None))
            pos = idx + 1
    return hits

print('\n=== 3. Callers of base+0x00 lookup/filter helpers ===')
for nm, fo in [('0x11ea010(3ebcd50)', 0x11ea010), ('0x11ea2b0(3ebd740)', 0x11ea2b0), ('0x1522180(43462a0)', 0x1522180)]:
    hits = find_direct_calls_to(fo)
    print(f'  callers of {nm}: {len(hits)} hits')
    for cfo, owner in hits[:25]:
        # inspect preceding 15 bytes for mov dl, imm / mov r8b, imm
        ctx = [f'{i.mnemonic} {i.op_str}' for i in md.disasm(raw[cfo-16:cfo], va(cfo-16))]
        print(f'    call@0x{cfo:x} in fn@0x{owner:x}: {ctx[-3:]}' if owner else f'    call@0x{cfo:x} (no-pdata): {ctx[-3:]}')

print('\n=== 4. References to STARTING_RECORD vtable 0x187d538 & str 0x1930155 ===')
for lbl, tfo in [('STARTING_RECORD_vt', 0x187d538), ('STARTING_RECORD_str', 0x1930155)]:
    tva = va(tfo)
    hits = []
    for nm, a, z in exec_secs:
        pos = a
        while pos < z - 7:
            idx = raw.find(b'\x8d', pos, z - 6)
            if idx == -1: break
            if (raw[idx+1] & 0xc7) == 0x05:
                disp = struct.unpack_from('<i', raw, idx+2)[0]
                if va(idx + 6) + disp == tva:
                    fn = find_fn(idx)
                    hits.append((idx, fn[0] if fn else None))
            pos = idx + 1
    print(f'  {lbl} ({len(hits)}):', [(hex(x), hex(y) if y else None) for x, y in hits])

# 5. Check master.json['enums']['foms'] for values 62, 63, 64 + check prior tasks' enum_ref=None grades
master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
foms = master['enums'].get('foms', {})
fvals = {int(v['enum']): v.get('name') for v in foms.get('values', [])} if foms else {}
print('\n=== 5. master.json foms check ===')
print(f'  foms count={len(fvals)}, max={max(fvals) if fvals else None}')
for k in (3, 4, 7, 27, 28, 29, 30, 35, 62, 63, 64):
    print(f'    foms[{k}] = {fvals.get(k)!r}')

# Check ALL enum/multiple_enum fields in t57, t63, t79 that got L3!
print('\n=== 6. Prior L3 enum fields with enum_ref=None check ===')
for path, ent in [('scratch/t57/out/field_map.json', 'club.xml'), ('scratch/t63/out/field_map_r2.json', 'club.xml')]:
    d = json.loads((ROOT/path).read_bytes())
    cf = master['entities'][ent][0]['fields']
    for f in d['fields']:
        if f.get('grade') == 'L3':
            code = f['code']
            sf = next((x for x in cf if x['field'] == code), None)
            if sf and sf['type'] in ('enum', 'multiple_enum'):
                print(f'  {path} L3 enum: {code} enum_ref={sf.get("enum_ref")}')
t79 = json.loads((ROOT/'scratch/t79/out/field_map.json').read_bytes())
for sec, ent in [('stadium_21', 'stadium.xml'), ('team_24', 'team.xml')]:
    cf = master['entities'][ent][0]['fields']
    for f in t79[sec]['schema_fields']:
        if f.get('grade') == 'L3' and f.get('schema_type') in ('enum', 'multiple_enum'):
            sf = next((x for x in cf if x['field'] == f['field']), None)
            print(f'  t79 {sec} L3 enum: {f["field"]} enum_ref={sf.get("enum_ref") if sf else None}')
