"""Deep static trace of:
1. ALL arms in CLUB_EXTRA_SET (0xe57de0) & TC_EXTRA_SET (0x11cf6e0) and their getter counterparts in CLUB_GET / TC_GET2.
2. Depth-2 callgraph scan from EVERY club.xml 4CC in CLUB_GET / TC_GET2 / CLUB_SET / TC_SET2 to detect EVERY single club.xml field touching CLUB+0x100 or CLUB+0xb0 (zero missed!).
3. Exact disassembly of list/helper functions: CAmb, Camc, Cbbl, Cdbt, Cffp, Clhs, Cmti, Coin, Crkt, Csoc, Cspb, Cwcl, pcpt, Calt, Cren, TCrs, tbcl(0x3eac7e0), 0xe8f1bf, 0xe8f34a, 0xe8f2f1, and STARTING_RECORD table loader.
4. Check all 8 polymorphic base+0x00 virtual classes' readers and getters/setters.
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

fn_cache = {}
def get_insns(fn_fo):
    fn_fo = resolve_thunk(fn_fo)
    if fn_fo in fn_cache: return fn_cache[fn_fo]
    b = find_fn(fn_fo)
    if not b:
        insns = list(md.disasm(raw[fn_fo:fn_fo+0x200], va(fn_fo)))
    else:
        insns = list(md.disasm(raw[b[0]:b[1]], va(b[0])))
    fn_cache[fn_fo] = (b, insns)
    return fn_cache[fn_fo]

# Check whether a helper function (up to depth 2) accesses [reg + 0x100] or [reg + 0xb0]
def fn_touches_extra_or_base(fn_fo, depth=0, visited=None):
    if visited is None: visited = set()
    fn_fo = resolve_thunk(fn_fo)
    if fn_fo in visited or depth > 2: return set()
    visited.add(fn_fo)
    # skip huge generic / allocator / property helpers
    if fn_fo in (0x83caf0, 0x3612d70, 0x83d5a0, 0x83d3a0, 0x8334b0, 0x832f70, 0x3603bb0,
                 0x7c8b10, 0x34c8f80, 0x1758000, 0x3506770, 0x350b6a0, 0x360f380, 0x40a1d10,
                 0x3cd6910, 0x83abf0, 0x83d180, 0x834980, 0x12ebfa0, 0x3fd6040, 0xfe3560, 0xfe1d00,
                 0xe89a00, 0xe82ae0, 0x11f0690, 0x11f4570):
        return set()
    b, insns = get_insns(fn_fo)
    if b and (b[1] - b[0]) > 0x4000: return set()
    hits = set()
    for i in insns:
        for op in i.operands:
            if op.type == 3 and op.mem.base != 0:
                breg = i.reg_name(op.mem.base)
                if breg not in ('rsp', 'rbp', 'rip'):
                    if op.mem.disp == 0x100:
                        hits.add((f'fn@0x{fn_fo:x}', '+0x100', f'0x{off(i.address):x}:{i.mnemonic} {i.op_str}'))
                    elif op.mem.disp == 0xb0:
                        hits.add((f'fn@0x{fn_fo:x}', '+0xb0', f'0x{off(i.address):x}:{i.mnemonic} {i.op_str}'))
        if depth < 2 and i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            try:
                t = off(i.operands[0].imm)
                if not b or not (b[0] <= t < b[1]):
                    t2 = resolve_thunk(t)
                    if t2 not in visited:
                        hits |= fn_touches_extra_or_base(t2, depth+1, visited)
            except Exception: pass
    return hits

def extract_4cc_arms(fn_fo):
    fn_fo = resolve_thunk(fn_fo)
    b, insns = get_insns(fn_fo)
    s, e = b
    fos = [off(i.address) for i in insns]
    by_fo = {fo: (k, i) for k, (fo, i) in enumerate(zip(fos, insns))}
    found = {}
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
                for j in range(max_idx + 1):
                    rel = struct.unpack_from('<i', raw, tb_fo + j*4)[0]
                    arm = off(va(tb_fo) + rel)
                    fc = is_4cc((base_imm + j) & 0xffffffff)
                    if fc:
                        found.setdefault(fc, []).append((f'jt@0x{tb_fo:x}[{j}]', tb_fo + j*4, arm))
    # Also detect bitmap gates like bt rcx, rax; jb arm (e.g., Cfp*, Ccj*, Ccs*)
    for k, i in enumerate(insns):
        if i.mnemonic == 'bt' and k+1 < len(insns) and insns[k+1].mnemonic in ('jb', 'jc', 'jae'):
            # look backwards for lea/sub/cmp + movabs/mov mask
            base_imm = max_idx = mask = None
            for bk in range(max(0, k-8), k):
                bi = insns[bk]
                if bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) != 'rip':
                    if abs(bi.operands[1].mem.disp) > 0x1000000:
                        base_imm = (-bi.operands[1].mem.disp) & 0xffffffff
                elif bi.mnemonic == 'cmp' and bi.operands[1].type == 2 and bi.operands[1].imm <= 64:
                    max_idx = bi.operands[1].imm
                elif bi.mnemonic in ('mov', 'movabs') and bi.operands[1].type == 2:
                    mask = bi.operands[1].imm & ((1<<64)-1)
            if base_imm is not None and max_idx is not None and mask is not None:
                ji = insns[k+1]
                arm = off(ji.operands[0].imm) if ji.mnemonic in ('jb', 'jc') else fos[k+2]
                for bit in range(max_idx + 1):
                    if (mask >> bit) & 1:
                        fc = is_4cc((base_imm + bit) & 0xffffffff)
                        if fc:
                            found.setdefault(fc, []).append((f'bt@0x{fos[k]:x}[{bit}]', fos[k], arm))
    return (s, e), insns, fos, by_fo, found

def trace_arm_calls(s, e, insns, fos, by_fo, arm, max_steps=35):
    """Collect direct instructions and external calls along straight-line/short CFG from arm."""
    q = [arm]
    seen = set()
    direct_hits = []
    ext_calls = []
    while q and len(seen) < max_steps:
        cur = q.pop(0)
        if cur in seen or cur not in by_fo: continue
        seen.add(cur)
        k, i = by_fo[cur]
        # stop at common epilogue / fallback
        if cur in (0xe8f4c0, 0xe8f796, 0xe8f79f, 0xe8f7a2, 0x11f2aa0, 0x11f2b00): continue
        for op in i.operands:
            if op.type == 3 and op.mem.base != 0:
                breg = i.reg_name(op.mem.base)
                if breg not in ('rsp', 'rbp', 'rip') and op.mem.disp in (0x100, 0xb0):
                    direct_hits.append(f'0x{cur:x}:{i.mnemonic} {i.op_str}')
        if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
            t = off(i.operands[0].imm)
            if not (s <= t < e):
                ext_calls.append((cur, i.mnemonic, t, resolve_thunk(t)))
                if i.mnemonic == 'jmp': continue
            else:
                if i.mnemonic == 'jmp':
                    q.append(t)
                    continue
        elif i.mnemonic.startswith('j') and i.operands[0].type == 2:
            t = off(i.operands[0].imm)
            if s <= t < e: q.append(t)
        elif i.mnemonic == 'ret':
            continue
        if k+1 < len(fos): q.append(fos[k+1])
    return direct_hits, ext_calls

master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_codes = sorted(set(f['field'] for f in club_fields))

print('=== 1. EXHAUSTIVE club.xml -> +0x100/+0xb0 SWEEP in CLUB_GET & TC_GET2 ===')
for fn_name, fn_fo in [('CLUB_GET', 0xe89a00), ('TC_GET2', 0x11f0690)]:
    (s, e), insns, fos, by_fo, found = extract_4cc_arms(fn_fo)
    hits_list = []
    for fc in club_codes:
        if fc not in found: continue
        for kind, site, arm in found[fc]:
            dh, ec = trace_arm_calls(s, e, insns, fos, by_fo, arm)
            # check helper calls
            hh = []
            for cfo, mn, t, t2 in ec:
                if t2 in (0x151d9b0, 0x151e500, 0x1520050, 0xe96f20, 0x3ea1030):
                    hh.append((f'known@0x{t2:x}', '+0x100'))
                else:
                    th = fn_touches_extra_or_base(t2)
                    for item in th:
                        hh.append((f'0x{t2:x}->{item[0]}', item[1], item[2]))
            if dh or hh:
                idxs = [idx for idx, f in enumerate(club_fields) if f['field'] == fc]
                ftype = club_fields[idxs[0]]['type']
                fname = club_fields[idxs[0]].get('name')
                hits_list.append((fc, idxs, ftype, fname, kind, arm, dh[:2], hh[:3]))
                break
    print(f'\n--- {fn_name}: {len(hits_list)} club.xml codes touching +0x100/+0xb0 ---')
    for fc, idxs, ftype, fname, kind, arm, dh, hh in hits_list:
        print(f'  {fc} idx={idxs} ({ftype:26s} {fname}) [{kind}@0x{arm:x}]')
        if dh: print(f'      direct: {dh}')
        if hh: print(f'      helper: {hh}')

# 2. Disassemble key list/setter/getter helpers!
def dump_fn(fo, label, max_b=0x350):
    fo = resolve_thunk(fo)
    b = find_fn(fo)
    s, e = b if b else (fo, fo + max_b)
    if e - s > 0x1000: e = s + max_b
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

# Check CLUB_GET arms for the specific CLUB_EXTRA_SET list codes!
print('\n=== 2. CLUB_GET / TC_GET2 arms for CLUB_EXTRA_SET & TC_EXTRA_SET list/bool codes ===')
(cs, ce), cinsns, cfos, cby, cfound = extract_4cc_arms(0xe89a00)
(ts, te), tinsns, tfos, tby, tfound = extract_4cc_arms(0x11f0690)
interesting = ['CAmb','Camc','Cbbl','Cdbt','Cffp','Clhs','Cmti','Coin','Crkt','Csoc','Cspb','Cwcl','pcpt',
               'Calt','Cren','TCrs','ttcl','tbcl','CWsc','Cf10','Cuf1','Cuf9']
helper_targets = set()
for fc in interesting:
    for fn_name, (s, e, insns, fos, by_fo, found) in [
        ('CLUB_GET', (cs, ce, cinsns, cfos, cby, cfound)),
        ('TC_GET2',  (ts, te, tinsns, tfos, tby, tfound)),
    ]:
        if fc in found:
            kind, site, arm = found[fc][0]
            dh, ec = trace_arm_calls(s, e, insns, fos, by_fo, arm)
            print(f'  {fn_name:8s} {fc} [{kind}->0x{arm:x}]: dh={dh[:2]} calls={[(hex(t),hex(t2)) for _,_,t,t2 in ec if t2 not in (0x3612d70,0x83d5a0,0x3603bb0,0x8334b0)]}')
            for _, _, t, t2 in ec:
                if t2 not in (0x3612d70,0x83d5a0,0x3603bb0,0x8334b0,0x83d3a0,0x360f380,0x3cd6910,0x40a1d10):
                    helper_targets.add((fc, t2))

# Also dump tbcl getter 0x3eac7e0, 0xe8f1bf (CLUB_GET record tail), 0xe8f34a (CLUB_GET team forward), 0xe8f2f1
# and all helper_targets discovered above!
dlines = []
for lbl, fo in [('TBCL_GET_3eac7e0', 0x3eac7e0), ('CLUB_GET_REC_TAIL_e8f1bf', 0xe8f1bf),
                ('CLUB_GET_TEAM_FWD_e8f34a', 0xe8f34a), ('CLUB_GET_TEAM_FWD2_e8f2f1', 0xe8f2f1)]:
    if fo in (0xe8f1bf, 0xe8f34a, 0xe8f2f1):
        dlines.append(f'=== {lbl} @ 0x{fo:x} ===')
        for i in md.disasm(raw[fo:fo+0x60], va(fo)):
            ex = ''
            if i.mnemonic in ('call', 'jmp') and i.operands[0].type == 2:
                t = off(i.operands[0].imm)
                ex = f'  ; -> 0x{t:x} (thunk->0x{resolve_thunk(t):x})'
            dlines.append(f'  0x{off(i.address):07x}: {i.mnemonic:8s} {i.op_str}{ex}')
    else:
        dlines.extend(dump_fn(fo, lbl, 0x300))

seen_ht = set()
for fc, hfo in sorted(helper_targets, key=lambda x: (x[1], x[0])):
    if hfo in seen_ht: continue
    seen_ht.add(hfo)
    dlines.extend(dump_fn(hfo, f'HELPER_{fc}_0x{hfo:x}', 0x300))

Path(r'D:\tmp2b\fm24-db\scratch\t82\disasm_recon8.txt').write_text('\n'.join(dlines) + '\n', encoding='utf-8')
print(f'\nWrote {len(dlines)} lines to disasm_recon8.txt ({len(seen_ht)} unique helpers)')
