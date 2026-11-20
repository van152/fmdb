"""Exhaustive static audit for t82:
1. Identify [db+0x80] (vtable 0x187d538 / pool string 0x1930155) and verify CBW*/CBD*/63 record 4CCs.
2. Disassemble kit/colour/squad helpers: 0x3ae7420, 0x11dc460, 0x11de6c0, 0x3eaba00, 0xe8f34a, 0x3bf9220, 0x3ebcf40, 0x11f6cf0, 0x3ebc520.
3. Audit ALL external calls/jmps from CLUB_GET, CLUB_SET, TC_GET, TC_GET2, TC_SET, TC_SET2 to ensure no extra_3 getter/setter helper is missed.
4. Check EVERY club.xml 4CC (all 433 occurrences) against CLUB_GET, CLUB_SET, CLUB_EXTRA_SET, TC_GET, TC_GET2, TC_SET, TC_SET2, TC_EXTRA_SET, SUPPORTER_GET (0x1520050), SUPPORTER_SET (0x43419b0), ELECTION_GET (0xe96f20), ELECTION_SET (0x3aeb720).
5. Inspect extra+0xda bitfield decoder (0x4348ef0) and all readers/fixups for extra+0x28, extra+0x68, base+0x18, base+0x30, base+0x48, base+0x00 (8 virtual readers).
"""
import json, struct, sys
from pathlib import Path
from collections import defaultdict, Counter
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
def cstr(o):
    z = raw.find(b'\x00', o)
    return raw[o:z].decode('ascii', 'replace') if z != -1 else ''
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
        if i0.mnemonic == 'jmp' and i0.operands[0].type == 2:
            return off(i0.operands[0].imm)
    except Exception:
        pass
    return fo
def rtti_for_vtable(vt_fo):
    try:
        col_va = struct.unpack_from('<Q', raw, vt_fo - 8)[0]
        col_fo = off(col_va)
        td_rva = struct.unpack_from('<I', raw, col_fo + 12)[0]
        td_fo = pe.get_offset_from_rva(td_rva)
        return cstr(td_fo + 16)
    except Exception as e:
        return f'<err:{e}>'

# 1. Inspect [db+0x80] record type
print('=== 1. [db+0x80] record object (TC_RECORD_GET/SET) ===')
print('  pool string @ 0x1930155:', repr(cstr(0x1930155)))
print('  vtable @ 0x187d538 RTTI:', rtti_for_vtable(0x187d538))
# Check vtable slots of 0x187d538 (reader/writer/etc.)
for s in range(10):
    try:
        slot_va = struct.unpack_from('<Q', raw, 0x187d538 + s*8)[0]
        sfo = off(slot_va)
        print(f'  vt[{s}] -> 0x{sfo:x} (thunk->0x{resolve_thunk(sfo):x})')
    except Exception:
        pass
# Also check RECORD_GET @ 0x1543ca0 and RECORD_SET @ 0x1544c80 (first few 4CCs)
for nm, ffo in [('RECORD_GET', 0x1543ca0), ('RECORD_SET', 0x1544c80)]:
    b = find_fn(resolve_thunk(ffo))
    if b:
        fcs = set()
        for i in md.disasm(raw[b[0]:b[1]], va(b[0])):
            if len(i.operands) >= 2 and i.operands[1].type == 2:
                fc = is_4cc(i.operands[1].imm)
                if fc: fcs.add(fc)
        print(f'  {nm} @ 0x{b[0]:x}..0x{b[1]:x} (len=0x{b[1]-b[0]:x}) 4CCs ({len(fcs)}): {sorted(fcs)}')

# 2. Disassemble key helpers
def dump_fn(fo, label, max_b=0x600):
    fo = resolve_thunk(fo)
    b = find_fn(fo)
    s, e = b if b else (fo, fo + max_b)
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
        elif i.mnemonic == 'lea' and i.operands[1].type == 3 and i.reg_name(i.operands[1].mem.base) == 'rip':
            try:
                rfo = off(i.address + i.size + i.operands[1].mem.disp)
                ex = f'  ; rip->0x{rfo:x}'
            except Exception: pass
        out.append(f'  0x{ifo:07x}: {i.mnemonic:8s} {i.op_str}{ex}')
    return out

helpers = [
    (0x3ae7420, 'CLUB_GET_FIRST_TEAM_3ae7420'),
    (0x11dc460, 'TC_KIT_FIND_11dc460'),
    (0x11de6c0, 'TC_COLOUR_GET_11de6c0'),
    (0x3eaba00, 'TC_KIT_COUNT_3eaba00'),
    (0xe8f34a,  'CLUB_GET_FORWARD_e8f34a'),
    (0x3bf9220, 'FIXUP_BASE30_ITEM_3bf9220'),
    (0x4348ef0, 'EXTRA_DA_DECODER_4348ef0'),
    (0x3ea5150, 'BASE18_READER_3ea5150'),
    (0x4387ab0, 'BASE48_READER_4387ab0'),
    (0x3ebcf40, 'TC_SET2_HELPER_3ebcf40'),
    (0x11f6cf0, 'TC_SET2_HELPER_11f6cf0'),
    (0x3ebc520, 'TC_SET2_HELPER_3ebc520'),
]
hlines = []
for fo, lbl in helpers:
    hlines.extend(dump_fn(fo, lbl, 0x350))
Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_recon7.txt').write_text('\n'.join(hlines) + '\n', encoding='utf-8')
print(f'\nWrote {len(hlines)} lines to disasm_recon7.txt')

# 3. Exhaustive 4CC extraction (both direct cmp/sub and jump tables!) from ALL CLUB/TC/sub-helper functions
def extract_all_4ccs_and_targets(fn_fo):
    fn_fo = resolve_thunk(fn_fo)
    s, e = find_fn(fn_fo)
    insns = list(md.disasm(raw[s:e], va(s)))
    fos = [off(i.address) for i in insns]
    found = {} # fc -> list of (kind, site_fo, arm_fo)
    # Direct cmps/subs
    for k, i in enumerate(insns):
        if i.mnemonic in ('cmp', 'sub') and len(i.operands) == 2 and i.operands[1].type == 2:
            fc = is_4cc(i.operands[1].imm)
            if fc and k+1 < len(insns) and insns[k+1].mnemonic in ('je', 'jne'):
                ji = insns[k+1]
                arm = off(ji.operands[0].imm) if ji.mnemonic == 'je' else fos[k+2]
                found.setdefault(fc, []).append(('cmp', fos[k], arm))
        elif i.mnemonic == 'jmp' and i.operands[0].type != 2:
            tb_fo = max_idx = base_imm = None
            for bk in range(max(0, k-20), k):
                bi = insns[bk]
                if bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) == 'rip':
                    try: tb_fo = off(bi.address + bi.size + bi.operands[1].mem.disp)
                    except Exception: pass
                elif bi.mnemonic == 'cmp' and len(bi.operands) == 2 and bi.operands[1].type == 2 and bi.operands[1].imm < 0x200:
                    if bk+1 < k and insns[bk+1].mnemonic in ('ja', 'jae', 'jbe'):
                        max_idx = bi.operands[1].imm
                elif bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) != 'rip':
                    if abs(bi.operands[1].mem.disp) > 0x1000000:
                        base_imm = (-bi.operands[1].mem.disp) & 0xffffffff
                elif bi.mnemonic in ('add', 'sub') and bi.operands[1].type == 2 and (bi.operands[1].imm & 0xffffffff) > 0x1000000:
                    imm = bi.operands[1].imm & 0xffffffff
                    base_imm = (-imm) & 0xffffffff if bi.mnemonic == 'add' else imm
            if tb_fo is not None and (base_imm is None or max_idx is None):
                for pk, pi in enumerate(insns):
                    if pi.mnemonic in ('jbe', 'jb') and pi.operands[0].type == 2:
                        t = off(pi.operands[0].imm)
                        if fos[max(0, k-5)] <= t <= fos[k]:
                            for b2 in range(max(0, pk-6), pk):
                                b2i = insns[b2]
                                if b2i.mnemonic == 'cmp' and b2i.operands[1].type == 2 and b2i.operands[1].imm < 0x200:
                                    max_idx = b2i.operands[1].imm
                                elif b2i.mnemonic == 'lea' and b2i.operands[1].type == 3 and b2i.reg_name(b2i.operands[1].mem.base) != 'rip':
                                    if abs(b2i.operands[1].mem.disp) > 0x1000000:
                                        base_imm = (-b2i.operands[1].mem.disp) & 0xffffffff
                                elif b2i.mnemonic in ('add', 'sub') and b2i.operands[1].type == 2 and (b2i.operands[1].imm & 0xffffffff) > 0x1000000:
                                    imm = b2i.operands[1].imm & 0xffffffff
                                    base_imm = (-imm) & 0xffffffff if b2i.mnemonic == 'add' else imm
            if tb_fo is not None and max_idx is not None and base_imm is not None:
                # Find default/else target via ja right after cmp if possible
                for j in range(max_idx + 1):
                    rel = struct.unpack_from('<i', raw, tb_fo + j*4)[0]
                    arm = off(va(tb_fo) + rel)
                    fc = is_4cc((base_imm + j) & 0xffffffff)
                    if fc:
                        found.setdefault(fc, []).append((f'jt@0x{tb_fo:x}[{j}]', tb_fo + j*4, arm))
    return found

# Also list all unique external call/jmp targets from CLUB_GET and CLUB_SET and TC_GET and TC_GET2
print('\n=== 2. External calls/jmps from CLUB_GET, TC_GET, TC_GET2 ===')
for nm, ffo in [('CLUB_GET', 0xe89a00), ('TC_GET', 0x11ef3e0), ('TC_GET2', 0x11f0690)]:
    s, e = find_fn(ffo)
    tgts = Counter()
    for i in md.disasm(raw[s:e], va(s)):
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            t = off(i.operands[0].imm)
            if not (s <= t < e):
                t2 = resolve_thunk(t)
                tgts[(t, t2)] += 1
    print(f'  {nm} ({len(tgts)} unique external targets):')
    for (t, t2), cnt in tgts.most_common(30):
        print(f'    0x{t:x} (thunk->0x{t2:x}): {cnt}x')

# 4. Sweep ALL 433 club.xml fields!
master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
print(f'\n=== 3. Club.xml field sweep ({len(club_fields)} occurrences) ===')
# Load prior grades (t57, t63, t71, t79)
t57_fm = json.loads((ROOT/'scratch/t57/out/field_map.json').read_bytes())
t63_fm = json.loads((ROOT/'scratch/t63/out/field_map_r2.json').read_bytes())
t71_fm = json.loads((ROOT/'scratch/t71/out/field_map_r3.json').read_bytes())
t79_fm = json.loads((ROOT/'scratch/t79/out/field_map.json').read_bytes())

funcs = {
    'CLUB_GET': 0xe89a00,
    'CLUB_SET': 0xe82ae0,
    'CLUB_EXTRA_SET': 0xe57de0,
    'ELECTION_GET': 0xe96f20,
    'ELECTION_SET': 0x3aeb720,
    'SUPPORTER_GET': 0x1520050,
    'SUPPORTER_SET': 0x43419b0,
    'CNST_GET': 0x151d9b0,
    'TC_GET': 0x11ef3e0,
    'TC_GET2': 0x11f0690,
    'TC_SET': 0x11f40b0,
    'TC_SET2': 0x11f4570,
    'TC_EXTRA_SET': 0x11cf6e0,
}
fmaps = {k: extract_all_4ccs_and_targets(v) for k, v in funcs.items()}
for k, m in fmaps.items():
    in_c = [c for c in m if any(f['field'] == c for f in club_fields)]
    print(f'  {k:16s}: {len(m):3d} total 4CCs, {len(in_c):3d} in club.xml')

# Print ALL club.xml fields found in CLUB_EXTRA_SET, ELECTION_GET/SET, SUPPORTER_GET/SET, TC_EXTRA_SET, TC_GET, TC_GET2 (non-record!)
for fn in ['CLUB_EXTRA_SET', 'ELECTION_GET', 'ELECTION_SET', 'SUPPORTER_GET', 'SUPPORTER_SET', 'TC_EXTRA_SET']:
    print(f'\n  --- {fn} ALL 4CCs ---')
    for fc in sorted(fmaps[fn]):
        matches = [(idx, f['type'], f.get('name')) for idx, f in enumerate(club_fields) if f['field'] == fc]
        print(f'    {fc}: {fmaps[fn][fc][0]} | club.xml={matches}')

# Check ALL club.xml codes that hit TC_GET or TC_GET2 or TC_SET or TC_SET2
print('\n  --- club.xml codes in TC_GET / TC_SET ---')
for fn in ['TC_GET', 'TC_SET']:
    for fc in sorted(fmaps[fn]):
        matches = [(idx, f['type'], f.get('name')) for idx, f in enumerate(club_fields) if f['field'] == fc]
        if matches:
            print(f'    {fn} {fc}: {fmaps[fn][fc][0]} | club.xml={matches}')

# Check club.xml codes in TC_GET2 NOT calling 0x11f2a60 (i.e. NOT [db+0x80] record!)
print('\n  --- club.xml codes in TC_GET2 (all!) ---')
tc2_end = fn_bounds[0x11f0690]
tc2_insns = list(md.disasm(raw[0x11f0690:tc2_end], va(0x11f0690)))
tc2_fos = [off(i.address) for i in tc2_insns]
tc2_by_fo = {fo: (k, i) for k, (fo, i) in enumerate(zip(tc2_fos, tc2_insns))}
def arm_summary(by_fo, fos, insns, arm):
    out = []
    cur = arm
    seen = set()
    for _ in range(14):
        if cur in seen or cur not in by_fo: break
        seen.add(cur)
        k, i = by_fo[cur]
        s = f'{i.mnemonic} {i.op_str}'
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            t = off(i.operands[0].imm)
            t2 = resolve_thunk(t)
            s += f' [->0x{t:x}/0x{t2:x}]'
            out.append(s)
            if i.mnemonic == 'jmp':
                if t in by_fo:
                    cur = t
                    continue
                break
        else:
            out.append(s)
            if i.mnemonic == 'ret': break
        if k+1 < len(fos): cur = fos[k+1]
        else: break
    return ' | '.join(out)

tc2_nonrec = []
for fc in sorted(fmaps['TC_GET2']):
    matches = [(idx, f['type'], f.get('name')) for idx, f in enumerate(club_fields) if f['field'] == fc]
    if matches:
        kind, site, arm = fmaps['TC_GET2'][fc][0]
        summ = arm_summary(tc2_by_fo, tc2_fos, tc2_insns, arm)
        if '0x11f2a60' not in summ and '0x3ebad50' not in summ:
            tc2_nonrec.append((fc, matches, kind, arm, summ))
print(f'  TC_GET2 non-record club.xml codes ({len(tc2_nonrec)}):')
for fc, matches, kind, arm, summ in tc2_nonrec:
    print(f'    {fc} ({matches[0][0]} {matches[0][1]} {matches[0][2]}) [{kind} -> 0x{arm:x}]: {summ[:180]}')

# Also check TC_GET2 ALL non-record codes (even NOT in club.xml) to find internal 4CCs on base+0xb0!
print('\n  --- TC_GET2 non-club.xml codes touching +0xb0 ---')
for fc in sorted(fmaps['TC_GET2']):
    if any(f['field'] == fc for f in club_fields): continue
    kind, site, arm = fmaps['TC_GET2'][fc][0]
    summ = arm_summary(tc2_by_fo, tc2_fos, tc2_insns, arm)
    if '0xb0' in summ or '0x3ea' in summ or '0x11d' in summ:
        print(f'    {fc} [{kind} -> 0x{arm:x}]: {summ[:180]}')
