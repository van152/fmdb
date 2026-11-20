"""Extract exact machine-verified PE file offsets, VAs, and instruction bytes for ALL getters, setters,
readers, fixups, and the 100 STARTING_RECORD negative proofs."""
import json, struct, sys
from pathlib import Path
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import pefile, capstone

ROOT = Path(r'D:\tmp2b\fm24-db')
EXE = Path(r'D:\tmp2b\fm24\input\editor.exe')
PE = EXE.read_bytes()
pe = pefile.PE(data=PE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
va = lambda fo: IB + pe.get_rva_from_offset(fo)
fo_va = lambda v: pe.get_offset_from_rva(v - IB)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_codes = {f['field']: i for i, f in enumerate(club_fields)}

# 1. Exact 100 STARTING_RECORD 4CCs in TC_GET2 (0x11f0690..0x11f3200) and CLUB_GET (0xe89a00..0xe91db0)
# Find all cmp reg, 4CC near branches to 0x11f2a60 (in TC_GET2) or 0xe8f1bf (in CLUB_GET), OR just scan record-family prefixes!
# Better: scan ALL 4CC immediates in CLUB_GET, TC_GET2, CLUB_SET, TC_SET2, CLUB_EXTRA_SET, TC_EXTRA_SET, ELECTION_GET, ELECTION_SET, SUPPORTER_GET, SUPPORTER_SET!
def scan_4cc(start, end):
    hits = {}
    sva = va(start)
    for ins in md.disasm(PE[start:end], sva):
        cfo = ins.address - sva + start
        if ins.mnemonic in ('cmp', 'mov', 'sub', 'lea'):
            for op in ins.op_str.split(','):
                op = op.strip()
                if op.startswith('0x') and len(op) == 10:
                    val = int(op, 16)
                    bs = val.to_bytes(4, 'big')
                    if all(32 <= b < 127 for b in bs):
                        s = bs.decode()
                        hits.setdefault(s, []).append((cfo, ins.mnemonic + ' ' + ins.op_str, ins.bytes.hex()))
    return hits

h_cg = scan_4cc(0xe89a00, 0xe91db0)
h_tg = scan_4cc(0x11f0690, 0x11f3400)
h_cs = scan_4cc(0xe82aa0, 0xe86b54)
h_ts = scan_4cc(0x11f4200, 0x11f6600)
h_ces = scan_4cc(0xe57d50, 0xe58698)
h_tes = scan_4cc(0x11cf800, 0x11d0200)
h_eg = scan_4cc(0xe96f20, 0xe97320)
h_es = scan_4cc(0x3aeb720, 0x3aebd00)
h_sg = scan_4cc(0x1520050, 0x1520a00)
h_ss = scan_4cc(0x43419b0, 0x4342500)

all_extra3_codes = [
    'Ctlv','Cmle','Cyim','Cyfb','Cytv','Crcb','Csth','CScP','Cown','Chti',
    'Cetl','Cmtm','Cect','Cemn','Cemx','Cepr',
    'Csly','Csps','Cspt','Csaf','Cste','Cspe',
    'Cuf1','Cuf2','Cuf3','Cuf4','Cuf5','Cuf6','Cuf7','Cuf8','Cuf9','Cf10',
    'TCht','TCnn','ttcl','tbcl','Catd','Cmna','Cmxa','Cpfr','C2pf','Cdfo','Cafo',
    'Cscm','CPsL','Cspb','Cren','TCrs','Tko1','Tkg1','Tko2','Tkg2','Tko3','Tkg3',
    'Csoc','Camc','Cbbl','pcpt','CssT','CssP','CssS','CssE',
    '1scl','1sbc','2scl','2sbc','3scl','3sbc','2tcl','2tbc','3tcl','3tbc',
]
print('=== EXACT GETTER/SETTER SITES FOR ALL 71 EXTRA3 CODES ===')
for c in all_extra3_codes:
    g = []
    for nm, mp in [('CG', h_cg), ('TG', h_tg), ('EG', h_eg), ('SG', h_sg)]:
        if c in mp: g.append(f'{nm}@0x{mp[c][0][0]:x}')
    s = []
    for nm, mp in [('CS', h_cs), ('TS', h_ts), ('CES', h_ces), ('TES', h_tes), ('ES', h_es), ('SS', h_ss)]:
        if c in mp: s.append(f'{nm}@0x{mp[c][0][0]:x}')
    print(f'  {c:5s}: GET={g}  SET={s}')

# Check jump tables for Cuf1..9 in CLUB_GET (0xe91db0) & CLUB_SET (0xe86b54), and 1scl..3tbc, and TC_SET2 for ttcl/tbcl, and C2pf/Cafo in TC_EXTRA_SET!
print('\n=== CHECK MISSING SITES (Cuf1..9, C2pf, Cafo, ttcl/tbcl, Cbbl, 1scl..3tbc, CssT..E, Csps..Cspe) ===')
# C2pf/Cafo in TC_EXTRA_SET (maybe jump table or sub?)
for ins in md.disasm(PE[0x11cf900:0x11cfd00], va(0x11cf900)):
    if any(k in ins.op_str for k in ('+ 0x74]', '+ 0x75]', '+ 0x76]', '+ 0x77]', '+ 0x68]', '+ 0x6c]', '+ 0x70]', '+ 0x98]', '+ 0x90]', '0x43327066', '0x4361666f', '0x4362626c')):
        print(f'  TES 0x{fo_va(ins.address):x}: {ins.mnemonic} {ins.op_str}')
# Check CLUB_SET for Cown, Chti, Cscm, CPsL, Cuf1..9, Cf10, Cebd/Cetl..Cepr
for ins in md.disasm(PE[0xe82aa0:0xe86b54], va(0xe82aa0)):
    if any(k in ins.op_str for k in ('+ 0x129]', '+ 0x12a]', '+ 0x78]', '0x43756631', '0x43663130', '0x436f776e', '0x43687469', '0x4373636d', '0x4350734c', '0x3aeb720')):
        print(f'  CS 0x{fo_va(ins.address):x}: {ins.mnemonic} {ins.op_str}')
# Check CLUB_GET jump table for Cuf1..9 @ 0xe91db0 & CLUB_SET jump table @ 0xe86b54
for name, base_fo, cnt in [('CLUB_GET_CUF_JT', 0xe91db0, 9), ('CLUB_SET_CUF_JT', 0xe86b54, 9)]:
    print(f'  {name} @ 0x{base_fo:x}:')
    for idx in range(cnt):
        rel = struct.unpack_from('<i', PE, base_fo + 4*idx)[0]
        print(f'    [{idx}] Cuf{idx+1} -> 0x{base_fo + rel:x} (rel32={rel})')

# Check ALL 100 club.xml record fields (CBW*, CBD*, CHA*, CYP*, COP*, CWR*, CLR*, CWL*, CWW*, CWC*, CWS*, CFG*, CHS*, CLA*, CYS*, COS*, CMA*, CMG*, CHR*, CHG*, CGL*, CMO*, CAA*, CHL*, CMC*)!
rec_prefixes = ('CBW','CBD','CHA','CYP','COP','CWR','CLR','CWL','CWW','CWC','CWS','CFG','CHS','CLA','CYS','COS',
                'CMA','CMG','CHR','CHG','CGL','CMO','CAA','CHL','CMC')
rec_fields = [(i, f['field'], f['name']) for i, f in enumerate(club_fields) if f['field'][:3] in rec_prefixes]
print(f'\n=== RECORD FIELDS BY PREFIX: {len(rec_fields)} fields ===')
in_tg = []; in_cg = []; neither = []
for i, c, nm in rec_fields:
    if c in h_tg: in_tg.append((i, c))
    elif c in h_cg: in_cg.append((i, c))
    else: neither.append((i, c, nm))
print(f'  in TC_GET2: {len(in_tg)}, in CLUB_GET: {len(in_cg)}, neither(check jump table/cmp): {len(neither)}')
for x in neither: print('    neither:', x)
