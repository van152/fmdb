"""Final static deep-dive for t82:
1. Disassemble CPsL(0x3b16350), Cscm(0x3b16b40), Css*(0x3ebcd50), Cmls(0x3ebf730),
   item serializers Cspb(0x3af8a90), Cren(0x3b144b0), pcpt(0x3b01860), Camc/Cbbl/Csoc(0x3affe90), TCrs(0x3ec74d0).
2. Inspect exact CLUB_GET arms for Camc, Cbbl, Csoc, Crkt, CPsL, Cscm, CssE/P/S/T, Cown, Chti, CScP, CWsc, Cf10, Cuf1..9,
   plus CLUB_SET / CLUB_EXTRA_SET / TC_SET2 / TC_EXTRA_SET arms for ALL extra_3 candidates.
3. Inspect all 8 observed base+0x00 virtual classes (vtable[+0x38] tag getter, vtable[+0x18] fixup, and wire reader).
4. Count ALL club.xml 4CCs routing to STARTING_RECORD (0x3ebad50) via TC_GET2 or CLUB_GET.
5. Inspect club.xml schema details + t57/t63/t71/t79 prior grades for ALL extra_3-touching club.xml fields.
"""
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

def dump_fn(fo, label, max_b=0x380):
    fo = resolve_thunk(fo)
    b = find_fn(fo)
    s, e = b if b else (fo, fo + max_b)
    if e - s > 0x900: e = s + max_b
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

# 1. Dump key helpers
lines = []
for lbl, fo in [
    ('CPsL_GET_3b16350', 0x3b16350),
    ('Cscm_GET_3b16b40', 0x3b16b40),
    ('Css_HELPER_3ebcd50', 0x3ebcd50),
    ('Cmls_HELPER_3ebf730', 0x3ebf730),
    ('Cspb_ITEM_3af8a90', 0x3af8a90),
    ('Cren_ITEM_3b144b0', 0x3b144b0),
    ('pcpt_ITEM_3b01860', 0x3b01860),
    ('CLAUSE_ITEM_3affe90', 0x3affe90),
    ('TCrs_ITEM_3ec74d0', 0x3ec74d0),
]:
    lines.extend(dump_fn(fo, lbl, 0x350))

# Also dump all 8 observed base+0x00 virtual readers + vtable[+0x38] (type tag) + vtable[+0x18] (fixup)
vts = [
    (4,  0x18b86b8, 0x42c8f90, 'COMPETITION_BONUS_INFO'),
    (5,  0x18b8768, 0x42d2710, 'NEXT_SALE_PERCENTAGE_INFO'),
    (6,  0x18b8818, 0x42d6a10, 'APPEARANCE_MONEY_INFO'),
    (7,  0x18b8608, 0x42c66f0, 'PLAYER_BUY_BACK_INFO'),
    (9,  0x18b9208, 0x42dba50, 'STARTING_PLAYER_RECORD_INFO'),
    (16, 0x18b9a88, 0x14d7530, 'CLUB_CUP_POINTS'),
    (37, 0x18b88d8, 0x42d9380, 'EPPP_APPEARANCE_MONEY_INFO'),
    (38, 0x18b9428, 0x14da470, 'TESTIMONIAL_INFO'),
]
print('=== 1. base+0x00 polymorphic vtables (tag, fixup, reader) ===')
for tag, vt, rdr, nm in vts:
    fixup_va = struct.unpack_from('<Q', raw, vt + 0x18)[0]
    tagfn_va = struct.unpack_from('<Q', raw, vt + 0x38)[0]
    fixup_fo = resolve_thunk(off(fixup_va))
    tagfn_fo = resolve_thunk(off(tagfn_va))
    # disasm first 5 insns of tagfn
    ti = '; '.join(f'{i.mnemonic} {i.op_str}' for i in list(md.disasm(raw[tagfn_fo:tagfn_fo+24], va(tagfn_fo)))[:4])
    print(f'  tag={tag:2d} {nm:30s}: vt=0x{vt:x} rdr=0x{rdr:x} fixup=0x{fixup_fo:x} tagfn=0x{tagfn_fo:x} [{ti}]')
    lines.extend(dump_fn(rdr, f'VTAG{tag}_{nm}_READER', 0x250))

Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_recon9.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Wrote {len(lines)} lines to disasm_recon9.txt')

# 2. Inspect exact CLUB_GET arms for Camc, Cbbl, Csoc, Crkt, CPsL, Cscm, CssE/P/S/T, Cown, Chti, CScP, CWsc
def dump_arms(fn_fo, codes):
    s, e = find_fn(fn_fo)
    insns = list(md.disasm(raw[s:e], va(s)))
    fos = [off(i.address) for i in insns]
    by_fo = {fo: (k, i) for k, (fo, i) in enumerate(zip(fos, insns))}
    # find cmp or jt
    arms = {}
    for k, i in enumerate(insns):
        if i.mnemonic in ('cmp', 'sub') and len(i.operands) == 2 and i.operands[1].type == 2:
            fc = is_4cc(i.operands[1].imm)
            if fc in codes and k+1 < len(insns) and insns[k+1].mnemonic in ('je', 'jne'):
                ji = insns[k+1]
                arm = off(ji.operands[0].imm) if ji.mnemonic == 'je' else fos[k+2]
                arms[fc] = (f'cmp@0x{fos[k]:x}', arm)
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
            if tb_fo is not None and max_idx is not None and base_imm is not None:
                for j in range(max_idx + 1):
                    fc = is_4cc((base_imm + j) & 0xffffffff)
                    if fc in codes:
                        rel = struct.unpack_from('<i', raw, tb_fo + j*4)[0]
                        arm = off(va(tb_fo) + rel)
                        arms[fc] = (f'jt@0x{tb_fo:x}[{j}]', arm)
    for fc in codes:
        if fc not in arms:
            print(f'  {fc}: NOT FOUND in 0x{fn_fo:x}')
            continue
        src, arm = arms[fc]
        print(f'  {fc} ({src} -> 0x{arm:x}):')
        ak, _ = by_fo[arm]
        for x in insns[ak:ak+14]:
            ex = ''
            if x.mnemonic in ('call', 'jmp') and x.operands[0].type == 2:
                t = off(x.operands[0].imm)
                ex = f' -> 0x{t:x} (thunk->0x{resolve_thunk(t):x})'
            print(f'    0x{off(x.address):x}: {x.mnemonic} {x.op_str}{ex}')
            if x.mnemonic in ('jmp', 'ret'): break

print('\n=== 2. Specific CLUB_GET arms ===')
dump_arms(0xe89a00, ['Camc','Cbbl','Csoc','Crkt','CPsL','Cscm','CssE','CssP','CssS','CssT','Cown','Chti','CScP','CWsc','Cmls'])

print('\n=== 3. Specific CLUB_SET arms ===')
dump_arms(0xe82ae0, ['Cuf1','Cuf2','Cuf9','Cf10','Cown','Chti','Crkt','CPsL','Cscm','CssE','CssP','CssS','CssT','Camc','Cbbl','Csoc','Cspb','Cren','pcpt','1scl','1sbc','2scl','2sbc','2tcl','2tbc','3scl','3sbc','3tcl','3tbc'])

print('\n=== 4. Specific TC_SET2 arms ===')
dump_arms(0x11f4570, ['ttcl','tbcl','TCht','TCnn','Catd','Cmna','Cmxa','Cpfr','C2pf','Cdfo','Cafo','Tko1','Tkg1','Crkt','TCrs','Cren'])

# 5. Count ALL club.xml codes routing to STARTING_RECORD (0x3ebad50) via CLUB_GET (0xe8f1bf)!
print('\n=== 5. CLUB_GET arms jumping to 0xe8f1bf (STARTING_RECORD) ===')
master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_by_code = defaultdict(list)
for idx, f in enumerate(club_fields): club_by_code[f['field']].append((idx, f))

s, e = find_fn(0xe89a00)
cinsns = list(md.disasm(raw[s:e], va(s)))
cfos = [off(i.address) for i in cinsns]
cby = {fo: (k, i) for k, (fo, i) in enumerate(zip(cfos, cinsns))}
def hits_rec_tail(arm):
    dl = r8 = None
    cur = arm
    for _ in range(10):
        if cur not in cby: return None
        k, i = cby[cur]
        if i.mnemonic == 'mov' and len(i.operands) == 2 and i.operands[1].type == 2:
            dst = i.op_str.split(',')[0].strip()
            if dst in ('dl','edx'): dl = i.operands[1].imm & 0xff
            elif dst in ('r8d','r8'): r8 = is_4cc(i.operands[1].imm)
        elif i.mnemonic == 'xor' and i.op_str in ('edx, edx','dl, dl'): dl = 0
        elif i.mnemonic == 'jmp' and i.operands[0].type == 2:
            t = off(i.operands[0].imm)
            if t == 0xe8f1bf: return (dl, r8)
            cur = t; continue
        elif i.mnemonic in ('call','ret') or i.mnemonic.startswith('j'): return None
        if k+1 < len(cfos): cur = cfos[k+1]
        else: break
    return None

cg_recs = []
for k, i in enumerate(cinsns):
    if i.mnemonic in ('cmp','sub') and len(i.operands)==2 and i.operands[1].type==2:
        fc = is_4cc(i.operands[1].imm)
        if fc and k+1<len(cinsns) and cinsns[k+1].mnemonic in ('je','jne'):
            arm = off(cinsns[k+1].operands[0].imm) if cinsns[k+1].mnemonic=='je' else cfos[k+2]
            r = hits_rec_tail(arm)
            if r: cg_recs.append((fc, r[0], r[1], fc in club_by_code))
    elif i.mnemonic=='jmp' and i.operands[0].type!=2:
        tb_fo=max_idx=base_imm=None
        for bk in range(max(0,k-20),k):
            bi=cinsns[bk]
            if bi.mnemonic=='lea' and bi.operands[1].type==3 and bi.reg_name(bi.operands[1].mem.base)=='rip':
                try: tb_fo=off(bi.address+bi.size+bi.operands[1].mem.disp)
                except Exception: pass
            elif bi.mnemonic=='cmp' and len(bi.operands)==2 and bi.operands[1].type==2 and bi.operands[1].imm<0x200:
                if bk+1<k and cinsns[bk+1].mnemonic in ('ja','jae','jbe'): max_idx=bi.operands[1].imm
            elif bi.mnemonic=='lea' and bi.operands[1].type==3 and bi.reg_name(bi.operands[1].mem.base)!='rip':
                if abs(bi.operands[1].mem.disp)>0x1000000: base_imm=(-bi.operands[1].mem.disp)&0xffffffff
            elif bi.mnemonic in ('add','sub') and bi.operands[1].type==2 and (bi.operands[1].imm&0xffffffff)>0x1000000:
                imm=bi.operands[1].imm&0xffffffff
                base_imm=(-imm)&0xffffffff if bi.mnemonic=='add' else imm
        if tb_fo and max_idx is not None and base_imm is not None:
            for j in range(max_idx+1):
                rel=struct.unpack_from('<i',raw,tb_fo+j*4)[0]
                arm=off(va(tb_fo)+rel)
                fc=is_4cc((base_imm+j)&0xffffffff)
                if fc:
                    r=hits_rec_tail(arm)
                    if r: cg_recs.append((fc, r[0], r[1], fc in club_by_code))
in_c = [x for x in cg_recs if x[3]]
print(f'  CLUB_GET STARTING_RECORD total={len(cg_recs)}, in club.xml={len(in_c)}:')
for fc, dl, r8, _ in sorted(in_c, key=lambda x: (x[1] or -1, x[0])):
    idx, f = club_by_code[fc][0]
    print(f'    CLUB[{idx:3d}] {fc} ({f["type"]:26s} {f.get("name")}): rec_type={dl} sub={r8}')

# 6. Print full club.xml schema details + prior grades for ALL extra_3 candidates!
t57 = json.loads((ROOT/'scratch/t57/out/field_map.json').read_bytes())
t63 = json.loads((ROOT/'scratch/t63/out/field_map_r2.json').read_bytes())
t71 = json.loads((ROOT/'scratch/t71/out/field_map_r3.json').read_bytes())
t57_by_idx = {f['occurrence']: f for f in t57['fields']} if 'fields' in t57 else {}
t63_by_idx = {}
for f in t63.get('fields', []):
    occ = f.get('occurrence', f.get('index'))
    if occ is not None: t63_by_idx[occ] = f
t71_codes = {f['code'] for f in t71['fields']}

print('\n=== 6. Schema & prior grades for ALL extra_3 candidate club.xml occurrences ===')
cand_codes = [
    # CLUB+0x100 scalars
    'Ctlv','Cmle','Csth','Cyim','CScP','Cown','Chti','Cyfb','Cytv','Crcb',
    # CLUB+0x100 election (excluding Cebd in t71)
    'Cepr','Cetl','Cmtm','Cect','Cemn','Cemx',
    # CLUB+0x100 supporter profile
    'Csly','Csps','Cspt','Csaf','Cste','Cspe',
    # CLUB+0x100 UEFA coefficients
    'Cuf1','Cuf2','Cuf3','Cuf4','Cuf5','Cuf6','Cuf7','Cuf8','Cuf9','Cf10',
    # CLUB+0x100 lists / non-wire strings
    'CPsL','Cscm','Csxn','Cl3n','Ca3n','CWsc',
    # CLUB+0xb0 scalars & strings & colours
    'Catd','Cmna','Cmxa','Cpfr','C2pf','Cdfo','Cafo','TCnn','TCht','ttcl','tbcl',
    '1scl','1sbc','2scl','2sbc','3scl','3sbc','2tcl','2tbc','3tcl','3tbc',
    # CLUB+0xb0 lists & polymorphic & bool
    'Tko1','Tkg1','Tko2','Tkg2','Tko3','Tkg3','Cspb','Cren','TCrs',
    'Camc','Cbbl','Csoc','pcpt','CssT','CssP','CssS','CssE','Crkt',
]
for fc in cand_codes:
    for idx, f in club_by_code.get(fc, []):
        p57 = t57_by_idx.get(idx, {}).get('grade', '-')
        p63 = t63_by_idx.get(idx, {}).get('grade', '-')
        r63 = t63_by_idx.get(idx, {}).get('reason', t63_by_idx.get(idx, {}).get('hold_reason', ''))
        print(f"  [{idx:3d}] {fc:4s} | {f['type']:26s} | min={f.get('min_value')} max={f.get('max_value')} enum={f.get('enum_ref')} | t57={p57} t63={p63} | {f.get('name')} | {str(r63)[:60]}")
