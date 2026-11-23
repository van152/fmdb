"""Targeted disassembly of record get/set (CBW/CBD), TC extra fixup, kit/colour arms, and remaining extra/base members."""
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
        if a <= fo < z:
            return a, z
    return None

def resolve_thunk(fo):
    if fo in fn_bounds:
        return fo
    i0 = next(md.disasm(raw[fo:fo+15], va(fo), 1))
    if i0.mnemonic == 'jmp' and i0.operands[0].type == 2:
        return off(i0.operands[0].imm)
    return fo

def dump_range(start, end, label):
    out = [f'=== {label} @ 0x{start:x}..0x{end:x} (VA 0x{va(start):x}) ===']
    for i in md.disasm(raw[start:end], va(start)):
        ifo = off(i.address)
        ex = ''
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            try:
                t = off(i.operands[0].imm)
                ex = f'  ; -> 0x{t:x}'
                if not (start <= t < end):
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
                try:
                    rfo = off(i.address + i.size + i.operands[1].mem.disp)
                    ex = f'  ; rip->0x{rfo:x}'
                except Exception:
                    pass
        out.append(f'  0x{ifo:07x}: {i.mnemonic:8s} {i.op_str}{ex}')
    return out

def dump_fn_any(fo, label, max_bytes=0x600):
    fo = resolve_thunk(fo)
    b = find_fn(fo)
    if b:
        return dump_range(b[0], b[1], f'{label} (pdata 0x{b[0]:x}..0x{b[1]:x})')
    # Linear until int3/nop pad after ret
    return dump_range(fo, fo + max_bytes, f'{label} (no-pdata raw)')

lines = []
# 1. Record get 0x3ebad50 & record set 0x11e8b40 -> ?
lines.extend(dump_fn_any(0x3ebad50, 'TC_RECORD_GET_3ebad50', 0x400))
lines.extend(dump_fn_any(0x11e8b40, 'TC_RECORD_SET_11e8b40', 0x400))
# 2. TC extra fixup 0x3ea1030
lines.extend(dump_fn_any(0x3ea1030, 'TC_EXTRA_FIXUP_3ea1030', 0x800))
# 3. Supporter profile setter 0x43419b0
lines.extend(dump_fn_any(0x43419b0, 'SUPPORTER_SET_43419b0', 0x600))
# 4. Kit helper 0x3ec2f60 and colour helper 0x3eae6f0
lines.extend(dump_fn_any(0x3ec2f60, 'KIT_HELPER_3ec2f60', 0x600))
lines.extend(dump_fn_any(0x3eae6f0, 'COLOUR_HELPER_3eae6f0', 0x600))

Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_targets.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Wrote {len(lines)} lines to disasm_targets.txt')

# 5. Decode ALL record-type (dl, sub_4cc) entries in TC_GET2 (0x11f0690) and TC_SET2 (0x11f4570)!
master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_by_code = {f['field']: (idx, f) for idx, f in enumerate(club_fields)}

def decode_tc_records(fn_fo, label, target_jmp_fo):
    end = fn_bounds[fn_fo]
    insns = list(md.disasm(raw[fn_fo:end], va(fn_fo)))
    fos = [off(i.address) for i in insns]
    by_fo = {fo: (k, i) for k, (fo, i) in enumerate(zip(fos, insns))}

    # Helper: given an arm_fo, simulate/trace straight-line mov dl, imm; mov r8d, imm; jmp target
    def trace_arm(arm_fo):
        dl_val = None
        r8d_val = None
        cur = arm_fo
        for _ in range(12):
            if cur not in by_fo: break
            k, i = by_fo[cur]
            if i.mnemonic == 'mov' and len(i.operands) == 2 and i.operands[1].type == 2:
                dst = i.op_str.split(',')[0].strip()
                if dst in ('dl', 'edx'): dl_val = i.operands[1].imm & 0xff
                elif dst in ('r8d', 'r8', 'r9d'): r8d_val = i.operands[1].imm & 0xffffffff
                elif dst in ('ecx', 'cl'): pass
            elif i.mnemonic == 'xor' and i.op_str in ('edx, edx', 'dl, dl'):
                dl_val = 0
            elif i.mnemonic == 'jmp' and i.operands[0].type == 2:
                tgt = off(i.operands[0].imm)
                if tgt == target_jmp_fo or (tgt in by_fo and by_fo[tgt][1].mnemonic == 'jmp' and off(by_fo[tgt][1].operands[0].imm) == target_jmp_fo):
                    return (dl_val, is_4cc(r8d_val) if r8d_val else None, tgt)
                cur = tgt
                continue
            elif i.mnemonic in ('ret', 'call') or i.mnemonic.startswith('j'):
                return None
            if k+1 < len(fos): cur = fos[k+1]
            else: break
        return None

    # Find ALL direct cmps and ALL jump tables in fn_fo
    results = []
    # Direct cmps
    for k, i in enumerate(insns):
        if i.mnemonic in ('cmp', 'sub') and len(i.operands) == 2 and i.operands[1].type == 2:
            fc = is_4cc(i.operands[1].imm)
            if fc and k+1 < len(insns) and insns[k+1].mnemonic in ('je', 'jne'):
                ji = insns[k+1]
                arm = off(ji.operands[0].imm) if ji.mnemonic == 'je' else fos[k+2]
                res = trace_arm(arm)
                if res and res[0] is not None:
                    results.append((fc, f'cmp@0x{fos[k]:x}', arm, res[0], res[1]))
        elif i.mnemonic == 'jmp' and i.operands[0].type != 2:
            # jump table
            tb_fo = max_idx = base_imm = None
            for bk in range(max(0, k-20), k):
                bi = insns[bk]
                if bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) == 'rip':
                    tb_fo = off(bi.address + bi.size + bi.operands[1].mem.disp)
                elif bi.mnemonic == 'cmp' and len(bi.operands) == 2 and bi.operands[1].type == 2 and bi.operands[1].imm < 0x100:
                    if bk+1 < k and insns[bk+1].mnemonic in ('ja', 'jae', 'jbe'):
                        max_idx = bi.operands[1].imm
                elif bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) != 'rip':
                    disp = bi.operands[1].mem.disp
                    if abs(disp) > 0x1000000:
                        base_imm = (-disp) & 0xffffffff
                elif bi.mnemonic in ('add', 'sub') and bi.operands[1].type == 2:
                    imm = bi.operands[1].imm & 0xffffffff
                    if imm > 0x1000000:
                        base_imm = (-imm) & 0xffffffff if bi.mnemonic == 'add' else imm
            # Some jump tables share a previous lea/cmp (jumped to via jbe)! Find all jbe targeting a block near k!
            if tb_fo is not None and (base_imm is None or max_idx is None):
                # search predecessors jumping to block start of k-4..k
                for pk, pi in enumerate(insns):
                    if pi.mnemonic in ('jbe', 'jb') and pi.operands[0].type == 2:
                        t = off(pi.operands[0].imm)
                        if fos[max(0,k-4)] <= t <= fos[k]:
                            for b2 in range(max(0, pk-5), pk):
                                b2i = insns[b2]
                                if b2i.mnemonic == 'cmp' and b2i.operands[1].type == 2 and b2i.operands[1].imm < 0x100:
                                    max_idx = b2i.operands[1].imm
                                elif b2i.mnemonic == 'lea' and b2i.operands[1].type == 3 and b2i.reg_name(b2i.operands[1].mem.base) != 'rip':
                                    if abs(b2i.operands[1].mem.disp) > 0x1000000:
                                        base_imm = (-b2i.operands[1].mem.disp) & 0xffffffff
                                elif b2i.mnemonic in ('add', 'sub') and b2i.operands[1].type == 2 and (b2i.operands[1].imm & 0xffffffff) > 0x1000000:
                                    imm = b2i.operands[1].imm & 0xffffffff
                                    base_imm = (-imm) & 0xffffffff if b2i.mnemonic == 'add' else imm
            if tb_fo is not None and max_idx is not None and base_imm is not None:
                for j in range(max_idx + 1):
                    rel = struct.unpack_from('<i', raw, tb_fo + j*4)[0]
                    arm = off(va(tb_fo) + rel)
                    fc = is_4cc((base_imm + j) & 0xffffffff)
                    if fc:
                        res = trace_arm(arm)
                        if res and res[0] is not None:
                            results.append((fc, f'jt@0x{tb_fo:x}[{j}]', arm, res[0], res[1]))
    print(f'\n=== {label} record mappings ({len(results)} total) ===')
    in_club = [r for r in results if r[0] in club_by_code]
    not_club = [r for r in results if r[0] not in club_by_code]
    print(f'  In club.xml: {len(in_club)}, Not in club.xml: {len(not_club)}')
    for fc, src, arm, rec_t, sub in sorted(in_club, key=lambda x: (x[3], x[0])):
        idx, f = club_by_code[fc]
        print(f"    CLUB[{idx:3d}] {fc} ({f.get('type'):26s} {f.get('name')}): rec_type={rec_t:2d} sub={sub} via {src} -> 0x{arm:x}")
    print('  Not in club.xml (grouped by rec_type):')
    by_rt = defaultdict(list)
    for fc, src, arm, rec_t, sub in not_club:
        by_rt[rec_t].append((fc, sub))
    for rt in sorted(by_rt):
        print(f'    rec_type={rt:2d}: {sorted(by_rt[rt])}')

decode_tc_records(0x11f0690, 'TC_GET2', 0x11f2a60)
# Find actual TC_SET2 record tail
ts_end = fn_bounds[0x11f4570]
ts_insns = list(md.disasm(raw[0x11f4570:ts_end], va(0x11f4570)))
print('\n=== TC_SET2 external calls/jmps ===')
for i in ts_insns:
    if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
        t = off(i.operands[0].imm)
        if not (0x11f4570 <= t < ts_end):
            t2 = resolve_thunk(t)
            print(f'  0x{off(i.address):x}: {i.mnemonic} 0x{t:x} (thunk->0x{t2:x})')

# Also inspect 1scl..3tbc and C1sq in CLUB_GET!
print('\n=== 1scl..3tbc and C1sq in CLUB_GET ===')
club_get_insns = list(md.disasm(raw[0xe89a00:fn_bounds[0xe89a00]], va(0xe89a00)))
cg_fos = [off(i.address) for i in club_get_insns]
cg_by_fo = {fo: (k, i) for k, (fo, i) in enumerate(zip(cg_fos, club_get_insns))}
for code, cfo in [('2sbc', 0xe89c6c), ('3tbc', 0xe8ac67), ('3tcl', 0xe8ac73), ('2tcl', 0xe8b27a),
                  ('1sbc', 0xe8beaf), ('1scl', 0xe8bebb), ('3sbc', 0xe8bf84), ('3scl', 0xe8bf90),
                  ('2scl', 0xe8c80a), ('2tbc', 0xe8c816), ('C1sq', 0xe8c9f0)]:
    k, i = cg_by_fo[cfo]
    ji = club_get_insns[k+1]
    arm = off(ji.operands[0].imm) if ji.mnemonic == 'je' else cg_fos[k+2]
    ak, _ = cg_by_fo[arm]
    snippet = []
    for x in club_get_insns[ak:ak+10]:
        ex = ''
        if x.mnemonic in ('call', 'jmp') and x.operands[0].type == 2:
            t = off(x.operands[0].imm)
            ex = f' -> 0x{t:x} (thunk->0x{resolve_thunk(t):x})'
        snippet.append(f'0x{off(x.address):x}: {x.mnemonic} {x.op_str}{ex}')
    print(f'  {code} (cmp@0x{cfo:x} -> arm@0x{arm:x}):')
    for s in snippet: print('    ', s)
