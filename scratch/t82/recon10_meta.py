"""Quick inspection of:
1. t57, t63, t71, t79 JSON structures & prior grades/negatives for all extra_3 candidates + CBW*/CBD*.
2. club.xml duplicate ttcl/tbcl XML paths & all candidate enums in master.json.
3. Static micro-check: Crkt in CLUB_EXTRA_SET/TC_EXTRA_SET, remaining extra+0xda/+0xdc/+0xde/+0x10c/+0x122/+0x123/+0x125/+0x128/+0x12e, base+0xac, and which table_XX.dat loads STARTING_RECORD ([db+0x80]).
4. List files in FM24_DB_DIR and verify exact table numbers for club/comp/person/nation/stadium.
"""
import json, os, struct, sys
from pathlib import Path
from collections import defaultdict
sys.path.append(r'D:\tmp2b\fm24\tools\python')
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r'D:\tmp2b\fm24-db')
DATA = Path(r'D:\tmp2b\fm24-db\scratch\data')
EXE = Path(r'D:\tmp2b\fm24\input\editor.exe')

print('=== 1. Data dir contents ===')
for p in sorted(DATA.glob('*')):
    print(' ', p.name, p.stat().st_size if p.is_file() else '<DIR>')
for sub in ('client_db', 'server_db'):
    d = DATA / sub
    if d.exists():
        print(f'  {sub}/:', len(list(d.glob('*'))), 'files, sample:', [x.name for x in sorted(d.glob('*'))[:10]])

# Check JSON keys of t57, t63, t71
t57 = json.loads((ROOT/'scratch/t57/out/field_map.json').read_bytes())
t63 = json.loads((ROOT/'scratch/t63/out/field_map_r2.json').read_bytes())
t71 = json.loads((ROOT/'scratch/t71/out/field_map_r3.json').read_bytes())
print('\n=== 2. Prior field_map keys ===')
print('  t57 keys:', list(t57.keys()), 'sample field:', list(t57['fields'][0].keys()) if 'fields' in t57 else None)
print('  t63 keys:', list(t63.keys()), 'sample field:', list(t63['fields'][0].keys()) if 'fields' in t63 else None)
print('  t71 keys:', list(t71.keys()), 'sample field:', list(t71['fields'][0].keys()) if 'fields' in t71 else None)
# Check t57 & t63 exact keys for indexing
t57_by_idx = {f['xml_index']: f for f in t57['fields']} if 'xml_index' in t57['fields'][0] else {f.get('index', i): f for i, f in enumerate(t57['fields'])}
t63_by_idx = {}
for f in t63['fields']:
    k = f.get('xml_index', f.get('index', f.get('occurrence')))
    t63_by_idx[k] = f
print('  t57 sample[0]:', t57['fields'][0])
print('  t63 sample[0]:', t63['fields'][0])

master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_by_code = defaultdict(list)
for idx, f in enumerate(club_fields): club_by_code[f['field']].append((idx, f))

print('\n=== 3. Duplicate ttcl/tbcl in club.xml ===')
for fc in ('ttcl', 'tbcl'):
    for idx, f in club_by_code[fc]:
        print(f'  [{idx}] {fc}: {f}')

print('\n=== 4. All extra_3 candidate fields in club.xml + prior grades + enums ===')
cand_codes = [
    'Ctlv','Cmle','Csth','Cyim','CScP','Cown','Chti','Cyfb','Cytv','Crcb',
    'Cepr','Cetl','Cmtm','Cect','Cemn','Cemx',
    'Csly','Csps','Cspt','Csaf','Cste','Cspe',
    'Cuf1','Cuf2','Cuf3','Cuf4','Cuf5','Cuf6','Cuf7','Cuf8','Cuf9','Cf10',
    'CPsL','Cscm','Csxn','Cl3n','Ca3n','CWsc',
    'Catd','Cmna','Cmxa','Cpfr','C2pf','Cdfo','Cafo','TCnn','TCht','ttcl','tbcl',
    '1scl','1sbc','2scl','2sbc','3scl','3sbc','2tcl','2tbc','3tcl','3tbc',
    'Tko1','Tkg1','Tko2','Tkg2','Tko3','Tkg3','Cspb','Cren','TCrs',
    'Camc','Cbbl','Csoc','pcpt','CssT','CssP','CssS','CssE','Crkt',
]
needed_enums = set()
for fc in cand_codes:
    for idx, f in club_by_code.get(fc, []):
        p57 = t57_by_idx.get(idx, {})
        p63 = t63_by_idx.get(idx, {})
        g57 = p57.get('grade', '-')
        g63 = p63.get('grade', '-')
        r57 = p57.get('reason', p57.get('first_counterexample', ''))
        r63 = p63.get('reason', p63.get('first_counterexample', ''))
        er = f.get('enum_ref')
        if er: needed_enums.add(er)
        print(f"  [{idx:3d}] {fc:4s} | {f['type']:26s} | min={str(f.get('min_value')):6s} max={str(f.get('max_value')):10s} enum={str(er):10s} | t57={g57:10s} t63={g63:8s} | {f.get('name')} | r63={str(r63)[:70]}")

print('\n=== 5. Needed enums in master.json ===')
enums = master.get('enums', {})
for er in sorted(needed_enums):
    vals = enums.get(er)
    print(f'  enum {er}: {vals}')

# Also check t63 grades of CBW*/CBD*!
print('\n=== 6. Prior grades of CBW*/CBD* ===')
for fc in ['CBWo','CBWf','CBWa','CBWd','CBWc','CBDo','CBDf','CBDa','CBDd','CBDc']:
    for idx, f in club_by_code.get(fc, []):
        p63 = t63_by_idx.get(idx, {})
        print(f"  [{idx:3d}] {fc}: t57={t57_by_idx.get(idx,{}).get('grade')} t63={p63.get('grade')} r63={p63.get('first_counterexample', p63.get('reason'))}")

# 7. Static micro-check: Crkt in CLUB_EXTRA_SET & TC_EXTRA_SET, and check extra+0xda/+0xdc/+0xde/+0x10c/+0x122/+0x123/+0x125/+0x128/+0x12e & base+0xac
raw = EXE.read_bytes()
pe = pefile.PE(data=raw, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
pe.parse_data_directories(directories=[3])
fn_bounds = {pe.get_offset_from_rva(x.struct.BeginAddress): pe.get_offset_from_rva(x.struct.EndAddress) for x in pe.DIRECTORY_ENTRY_EXCEPTION}
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
def va(o): return base + pe.get_rva_from_offset(o)
def off(v): return pe.get_offset_from_rva(v - base)
def resolve_thunk(fo):
    if fo in fn_bounds: return fo
    try:
        i0 = next(md.disasm(raw[fo:fo+15], va(fo), 1))
        if i0.mnemonic == 'jmp' and i0.operands[0].type == 2: return off(i0.operands[0].imm)
    except Exception: pass
    return fo

print('\n=== 7. Crkt in CLUB_EXTRA_SET (0xe581ff) and TC_EXTRA_SET (0x11cfc78) ===')
for lbl, fo in [('CLUB_EXTRA_SET_Crkt', 0xe5820c), ('TC_EXTRA_SET_Crkt', 0x11cfc78)]:
    print(f'  {lbl}:')
    for i in list(md.disasm(raw[fo:fo+0x50], va(fo)))[:14]:
        ex = ''
        if i.mnemonic in ('call','jmp') and i.operands[0].type == 2:
            t = off(i.operands[0].imm)
            ex = f' -> 0x{t:x} (thunk->0x{resolve_thunk(t):x})'
        print(f'    0x{off(i.address):x}: {i.mnemonic} {i.op_str}{ex}')
        if i.mnemonic in ('jmp','ret'): break

# Check exact DB table offsets for STARTING_RECORD, DEBT, etc. by reading db_tables_big.json
db_big = json.loads((ROOT/'evidence/fm24/reports/dbdat_decode/db_tables_big.json').read_bytes())
print('\n=== 8. db_tables_big.json summary ===')
if isinstance(db_big, dict):
    print('  keys:', list(db_big.keys())[:10])
    for k, v in list(db_big.items())[:5]:
        print(' ', k, str(v)[:120])
elif isinstance(db_big, list):
    print('  len:', len(db_big), 'sample:', db_big[:3])

# Also inspect all references to 0x187d538 (STARTING_RECORD vtable) in .text to find its table loader!
print('\n=== 9. References to STARTING_RECORD vtable 0x187d538 (VA 0x14187df38) ===')
vt_va = va(0x187d538)
# Search LEA rip-relative: 48 8d .. or 4c 8d ..
text_sec = next(s for s in pe.sections if s.Name.startswith(b'.text'))
ts, te = text_sec.PointerToRawData, text_sec.PointerToRawData + text_sec.SizeOfRawData
# Fast scan for RIP-rel target == vt_va: target = va(pos+7) + rel32 -> rel32 = vt_va - va(pos+7)
# Instead scan for pool string 0x1930155 ('STARTING_RECORD') and vtable 0x187d538 in .text/.pdata
for target_lbl, target_fo in [('STARTING_RECORD_vt', 0x187d538), ('STARTING_RECORD_str', 0x1930155)]:
    tva = va(target_fo)
    hits = []
    # 7-byte LEA [rip+disp32]: opcode 8D with modrm (byte & 0xc7 == 0x05)
    pos = ts
    while pos < te - 7:
        idx = raw.find(b'\x8d', pos, te - 6)
        if idx == -1: break
        modrm = raw[idx+1]
        if (modrm & 0xc7) == 0x05:
            disp = struct.unpack_from('<i', raw, idx+2)[0]
            if va(idx + 6) + disp == tva:
                # find owning function
                fn = None
                for a, z in fn_bounds.items():
                    if a <= idx < z: fn = (a, z); break
                hits.append((idx, fn))
        pos = idx + 1
    print(f'  {target_lbl} hits ({len(hits)}):', [(hex(h[0]), (hex(h[1][0]), hex(h[1][1])) if h[1] else None) for h in hits[:15]])
