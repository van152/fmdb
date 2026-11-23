"""Trace ALL 4CCs in CLUB_GET, CLUB_SET, TC_GET2, TC_SET2, and their helpers -> +0x100/+0xb0 accesses."""
import json, struct, sys
from pathlib import Path
from collections import defaultdict, deque
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
    if all(0x20 <= x <= 0x7e for x in b):
        return b.decode('ascii')
    return None

master = json.loads((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_codes = {f['field'] for f in club_fields}
all_field_codes = set(master['field_codes'].keys())

def analyze_dispatch_fn(fn_fo, name):
    if fn_fo not in fn_bounds:
        i0 = next(md.disasm(raw[fn_fo:fn_fo+15], va(fn_fo), 1))
        if i0.mnemonic == 'jmp' and i0.operands[0].type == 2:
            fn_fo = off(i0.operands[0].imm)
    end = fn_bounds[fn_fo]
    insns = list(md.disasm(raw[fn_fo:end], va(fn_fo)))
    by_fo = {off(i.address): i for i in insns}
    fos = [off(i.address) for i in insns]
    idx_of = {fo: k for k, fo in enumerate(fos)}

    # Build CFG edges (direct jcc/jmp, plus resolved rel32 jump tables!)
    # Detect rel32 jump table pattern:
    #   add/sub reg, imm  (or lea reg, [reg + imm])  -> base_key
    #   cmp reg, max_idx
    #   ja default
    #   lea base_reg, [rip + disp]  -> table_fo
    #   movsxd r, dword ptr [base_reg + idx*4]
    #   add r, base_reg
    #   jmp r
    succs = defaultdict(list)
    preds = defaultdict(list)
    jtables = {}  # jmp_fo -> {table_fo, max_idx, offset_base, arms: [(idx, key_u32, arm_fo)]}
    direct_cmps = []  # (cmp_fo, key_u32, code_str, eq_arm_fo)

    for k, i in enumerate(insns):
        fo = fos[k]
        nxt = fos[k+1] if k+1 < len(fos) else None
        m = i.mnemonic
        if m == 'ret' or m == 'int3':
            continue
        elif m == 'jmp':
            if i.operands[0].type == 2:
                tgt = off(i.operands[0].imm)
                if fn_fo <= tgt < end:
                    succs[fo].append(('jmp', tgt))
                    preds[tgt].append(fo)
                else:
                    succs[fo].append(('tail', tgt))
            else:
                # Indirect jmp! Scan backwards up to 18 insns for lea rip, cmp max, add/sub key
                tb_fo = None
                max_idx = None
                base_imm = None
                for bk in range(max(0, k-20), k):
                    bi = insns[bk]
                    if bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) == 'rip':
                        tb_fo = off(bi.address + bi.size + bi.operands[1].mem.disp)
                    elif bi.mnemonic == 'cmp' and len(bi.operands) == 2 and bi.operands[1].type == 2 and bi.operands[1].imm < 0x10000:
                        if bk+1 < k and insns[bk+1].mnemonic in ('ja', 'jae'):
                            max_idx = bi.operands[1].imm + (0 if insns[bk+1].mnemonic == 'ja' else -1)
                    elif bi.mnemonic in ('add', 'sub') and len(bi.operands) == 2 and bi.operands[1].type == 2:
                        imm = bi.operands[1].imm & 0xffffffff
                        if imm > 0x1000000:
                            base_imm = (-imm) & 0xffffffff if bi.mnemonic == 'add' else imm
                    elif bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) != 'rip':
                        disp = bi.operands[1].mem.disp
                        if abs(disp) > 0x1000000:
                            base_imm = (-disp) & 0xffffffff
                if tb_fo is not None and max_idx is not None:
                    arms = []
                    for j in range(max_idx + 1):
                        rel = struct.unpack_from('<i', raw, tb_fo + j*4)[0]
                        arm = off(va(tb_fo) + rel)
                        key = (base_imm + j) & 0xffffffff if base_imm is not None else j
                        arms.append((j, key, arm))
                        if fn_fo <= arm < end:
                            succs[fo].append((f'jt[{j}]', arm))
                            preds[arm].append(fo)
                    jtables[fo] = dict(table_fo=tb_fo, max_idx=max_idx, base_imm=base_imm, arms=arms)
        elif m.startswith('j'):
            tgt = off(i.operands[0].imm)
            if fn_fo <= tgt < end:
                succs[fo].append((m, tgt))
                preds[tgt].append(fo)
            if nxt is not None:
                succs[fo].append(('fall', nxt))
                preds[nxt].append(fo)
            # Check if previous insn was cmp reg, 4CC
            if m in ('je', 'jne') and k >= 1:
                pi = insns[k-1]
                if pi.mnemonic == 'cmp' and len(pi.operands) == 2 and pi.operands[1].type == 2:
                    fc = is_4cc(pi.operands[1].imm)
                    if fc:
                        eq_arm = tgt if m == 'je' else nxt
                        direct_cmps.append((fos[k-1], pi.operands[1].imm & 0xffffffff, fc, eq_arm))
                elif pi.mnemonic == 'sub' and len(pi.operands) == 2 and pi.operands[1].type == 2:
                    fc = is_4cc(pi.operands[1].imm)
                    if fc:
                        eq_arm = tgt if m == 'je' else nxt
                        direct_cmps.append((fos[k-1], pi.operands[1].imm & 0xffffffff, fc, eq_arm))
        else:
            if nxt is not None:
                succs[fo].append(('fall', nxt))
                preds[nxt].append(fo)

    # Also detect bit-test masks: sub/add reg, base_imm -> cmp <= 63 -> movabs mask -> bt -> jc/jb
    btests = []
    for k, i in enumerate(insns):
        if i.mnemonic == 'bt' and k+1 < len(insns) and insns[k+1].mnemonic in ('jb', 'jae', 'jc', 'jnc'):
            # look back for movabs mask and add/sub/lea base_imm
            mask = None
            base_imm = None
            max_idx = 63
            for bk in range(max(0, k-10), k):
                bi = insns[bk]
                if bi.mnemonic == 'movabs' and bi.operands[1].type == 2:
                    mask = bi.operands[1].imm & 0xffffffffffffffff
                elif bi.mnemonic == 'mov' and bi.operands[1].type == 2 and bi.operands[1].imm > 1:
                    mask = bi.operands[1].imm & 0xffffffffffffffff
                elif bi.mnemonic in ('add', 'sub') and bi.operands[1].type == 2:
                    imm = bi.operands[1].imm & 0xffffffff
                    if imm > 0x1000000:
                        base_imm = (-imm) & 0xffffffff if bi.mnemonic == 'add' else imm
                elif bi.mnemonic == 'lea' and bi.operands[1].type == 3 and bi.reg_name(bi.operands[1].mem.base) != 'rip':
                    disp = bi.operands[1].mem.disp
                    if abs(disp) > 0x1000000:
                        base_imm = (-disp) & 0xffffffff
                elif bi.mnemonic == 'cmp' and bi.operands[1].type == 2 and bi.operands[1].imm <= 63:
                    max_idx = bi.operands[1].imm
            if mask is not None and base_imm is not None:
                ji = insns[k+1]
                tgt = off(ji.operands[0].imm)
                nxt = fos[k+2] if k+2 < len(fos) else None
                hit_arm = tgt if ji.mnemonic in ('jb', 'jc') else nxt
                codes = []
                for bit in range(max_idx + 1):
                    if (mask >> bit) & 1:
                        fc = is_4cc((base_imm + bit) & 0xffffffff)
                        if fc:
                            codes.append((bit, fc))
                btests.append((fos[k], base_imm, mask, hit_arm, codes))

    # Map every target arm_fo -> list of 4CCs that jump directly to it
    arm_to_codes = defaultdict(list)
    for cfo, key, fc, arm in direct_cmps:
        arm_to_codes[arm].append((fc, f'cmp@0x{cfo:x}'))
    for jfo, jt in jtables.items():
        # Filter default arm (most frequent arm in table)
        cnt = defaultdict(int)
        for j, key, arm in jt['arms']:
            cnt[arm] += 1
        default_arm = max(cnt, key=cnt.get) if len(cnt) > 1 else None
        for j, key, arm in jt['arms']:
            if arm == default_arm and cnt[arm] > 3:
                continue
            fc = is_4cc(key)
            if fc:
                arm_to_codes[arm].append((fc, f'jt@0x{jfo:x}[{j}]'))
    for bfo, base_imm, mask, hit_arm, codes in btests:
        for bit, fc in codes:
            arm_to_codes[hit_arm].append((fc, f'bt@0x{bfo:x}[{bit}]'))

    # For each instruction accessing +0x100 or +0xb0, BFS backwards up to 150 steps (stopping at 4CC dispatch or entry)
    # Also trace forward from each +0x100/+0xb0 hit to see what offsets on the loaded pointer are used!
    hits = []
    for k, i in enumerate(insns):
        fo = fos[k]
        for o in i.operands:
            if o.type == 3 and o.mem.disp in (0x100, 0xb0) and i.reg_name(o.mem.base) not in ('rsp', 'rbp', 'rip'):
                # backward BFS to find all reaching 4CCs
                vis = {fo}
                q = deque([fo])
                reached_codes = []
                while q:
                    cur = q.popleft()
                    if cur in arm_to_codes:
                        reached_codes.extend(arm_to_codes[cur])
                        continue
                    for p in preds[cur]:
                        if p not in vis and len(vis) < 400:
                            vis.add(p)
                            q.append(p)
                # forward snippet (next 25 insns linearly/following short jumps)
                fwd = []
                for fk in range(k, min(len(insns), k+25)):
                    fi = insns[fk]
                    ffo = fos[fk]
                    ex = ''
                    if fi.mnemonic in ('call', 'jmp') and fi.operands[0].type == 2:
                        try:
                            t = off(fi.operands[0].imm)
                            ex = f' ; -> 0x{t:x}'
                            tins = next(md.disasm(raw[t:t+15], va(t), 1))
                            if tins.mnemonic == 'jmp' and tins.operands[0].type == 2:
                                ex += f' (thunk->0x{off(tins.operands[0].imm):x})'
                        except Exception: pass
                    fwd.append(f'0x{ffo:x}: {fi.mnemonic} {fi.op_str}{ex}')
                    if fi.mnemonic in ('ret', 'jmp') and fk > k and ' ; -> 0x' in ex:
                        t = off(fi.operands[0].imm)
                        if not (fn_fo <= t < end):
                            break
                hits.append((fo, o.mem.disp, f'{i.mnemonic} {i.op_str}', reached_codes, fwd))

    print(f'\n================ {name} @ 0x{fn_fo:x}..0x{end:x} ================')
    print(f'  direct_cmps={len(direct_cmps)}, jtables={len(jtables)}, btests={len(btests)}, +0x100/+0xb0 hits={len(hits)}')
    for fo, disp, ins, rcodes, fwd in hits:
        uniq_codes = sorted(set(rcodes))
        club_mark = [c for c, _ in uniq_codes if c in club_codes]
        print(f'\n  HIT 0x{fo:x} (+0x{disp:x}): {ins}')
        print(f'    Reaching 4CCs ({len(uniq_codes)}, in club.xml={len(club_mark)}): {uniq_codes[:25]}')
        for fl in fwd[:14]:
            print(f'      {fl}')

for fn_fo, name in [
    (0xe89a00, 'CLUB_GET'),
    (0xe82aa0, 'CLUB_SET'),
    (0x11f0690, 'TC_GET2'),
    (0x11f4570, 'TC_SET2'),
    (0xe96f20, 'ELECTION_GET'),
    (0xe878d0, 'ELECTION_SET'),
]:
    analyze_dispatch_fn(fn_fo, name)
