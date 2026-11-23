#!/usr/bin/env python3
"""Build a path-specialized table_22 reader and Cstc field ledger, offline."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t27/out'
EDITOR = Path('D:/tmp2b/fm24/input/editor.exe')
DATA = 'D:/tmp2b/fm24-db/scratch/data'
SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
START, FAIL, TAIL, RET = 0x1537800, 0x1537a89, 0x1537a95, 0x1537a94
THUNK, HELPER, HELPER_READ = 0xdb7f80, 0x39dd7b0, 0x39dd7d4
BULK, SELECT = 0x1537ab4, 0xf2ba0e
FOOT = ((0xffa602, 4), (0xf2baa2, 1), (0xf2bac2, 4))
WRAPPER = [0xf2b670, 0xf2b673, 0xf2b679, 0xf2b691, 0xf2b6b1, 0xf2b9f3, 0xf2b9fa,
           SELECT, 0xf2ba1b, 0xf2ba23, 0xf2ba33, 0xf2ba38, 0xf2ba3d, 0xf2ba4e, 0xf2ba51,
           0xf2ba57, 0xf2ba7f, 0xffa602, 0xf2ba84, 0xf2baa2, 0xf2bac2]


class CheckError(Exception):
    pass


def check(value, text):
    if not value:
        raise CheckError(text)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def integer(raw):
    return int.from_bytes(raw, 'little')


def dump(name, data):
    raw = ''.join(('{\n', ',\n'.join(json.dumps(k) + ':' + compact(v) for k, v in data.items()), '\n}\n'))
    check(len(raw.encode('utf-8')) < 50000, f'shard too large: {name}')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(raw, encoding='utf-8')


def compact(v):
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'))


def shards(stem, key, records, size):
    paths = []
    for start in range(0, len(records), size):
        name = f'{stem}.part{len(paths)+1:03}.json'
        raw = '{' + json.dumps(key) + ':[\n' + ',\n'.join(map(compact, records[start:start+size])) + '\n]}\n'
        check(len(raw.encode('utf-8')) < 50000 and len(raw.splitlines()) <= 400, f'shard too large: {name}')
        (OUT / name).write_text(raw, encoding='utf-8')
        paths.append(name)
    return paths


class Static:
    def __init__(self):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        from t21b_control_flow import ReaderCFG
        manifest = {x['path']: x['sha256'] for x in read_json('evidence/MANIFEST.json')['files']}
        for asset in (PROV, MASTER):
            check(sha((ROOT / asset).read_bytes()) == manifest[asset], f'manifest mismatch: {asset}')
        self.pe = PE(EDITOR)
        check(SHA in (ROOT / PROV).read_text(encoding='utf-8') and SHA == sha(self.pe.raw), 'editor SHA mismatch')
        self.provenance = {'editor_sha256': SHA, 'editor': str(EDITOR),
                           'snapshot_manifest': {p: manifest[p] for p in (PROV, MASTER)}}
        self.pe.pe.parse_data_directories(directories=[3])
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.cfg = ReaderCFG(self.pe, self.md, START)
        self.getter_cfg = ReaderCFG(self.pe, self.md, 0x1538ee0)
        self.census = {r['table_type']: r for r in read_json('scratch/t14/out/census.json')['tables']}
        self.t22 = self.census[22]
        self.vtable = next(int(v['vtable_va'], 16) for v in self.t22['vtables'] if v['class'] == 'STADIUM_CHANGE')
        self.vtable_off = self.pe.va2f(self.vtable)
        check(self.t22['handler_off'] == '0xf49092' and self.slot(19) == self.pe.f2va(START), 'factory/slot19 mismatch')
        check(self.pe.va2f(self.slot(2)) == 0x1538ee0 and self.pe.va2f(self.slot(21)) == 0x1537b90, 'getter/writer mismatch')
        self.records = {}
        self.insns = {self.pe.va2f(k): v for k, v in self.cfg.instructions.items()}
        for k in self.insns:
            self.add(k)
        self.blocks = self.make_blocks()
        self.transfer, self.branches = self.make_transfers()

    def slot(self, n):
        return struct.unpack_from('<Q', self.pe.raw, self.vtable_off + 8*n)[0]

    def ins(self, off):
        va = self.pe.f2va(off)
        check(va is not None and self.pe.va2f(va) == off, f'PE mapping at {off:#x}')
        return next(self.md.disasm(self.pe.raw[off:off+15], va, count=1))

    def add(self, *offs):
        result = []
        for off in offs:
            if off not in self.records:
                i = self.ins(off)
                self.records[off] = {'file_offset': hex(off), 'VA': hex(i.address), 'bytes': i.bytes.hex(),
                                     'instruction': f'{i.mnemonic} {i.op_str}'.rstrip()}
            result.append(self.records[off])
        return result

    def direct(self, off):
        ins = self.ins(off)
        check(len(ins.operands) == 1 and ins.operands[0].type == 2, f'direct edge at {off:#x}')
        return self.pe.va2f(ins.operands[0].imm)

    def getter_path(self, root, access):
        # Bounded getter arm; different dates may first pass a TLS initialization test.
        queue, seen = [(root, [])], set()
        for off, path in queue:
            if off in seen or not root <= off <= root+0x80:
                continue
            seen.add(off)
            i = self.ins(off)
            path = [*path, off]
            if off == access:
                return self.add(*path)
            if i.mnemonic.startswith('j'):
                queue.append((self.direct(off), path))
            if i.mnemonic not in ('jmp', 'ret', 'int3', 'ud2'):
                queue.append((off+i.size, path))
        raise CheckError(f'no getter arm from {root:#x} to {access:#x}')

    def make_blocks(self):
        cfg = self.cfg
        check(len(self.insns) == 210 and cfg.function_end_off == 0x1537b04 and not cfg.external_edges, 'reader CFG drift')
        leaders = {cfg.start_va}
        for va, ins in cfg.instructions.items():
            if ins.mnemonic.startswith('j'):
                leaders.update(cfg.successors[va])
        blocks, covered = [], set()
        for va in sorted(leaders):
            ids = []
            cur = va
            while True:
                i = cfg.instructions[cur]
                off = self.pe.va2f(cur)
                check(off not in covered, 'overlapping basic blocks')
                covered.add(off)
                ids.append(hex(off))
                succ = cfg.successors[cur]
                if len(succ) != 1 or succ[0] in leaders or i.mnemonic.startswith('j'):
                    break
                cur = succ[0]
            blocks.append({'start': ids[0], 'end_instruction': ids[-1], 'instructions': ids,
                           'successors': [hex(self.pe.va2f(x)) for x in succ]})
        check(covered == set(self.insns), 'unpartitioned instructions')
        return blocks

    def make_transfers(self):
        sr = sorted(self.insns)
        transfer, branches = {}, {}
        check(self.direct(THUNK) == HELPER and self.ins(0x39dd7b9).op_str == 'rsi, rsi', 'date thunk drift')
        check(self.ins(0x39dd7c8).op_str == 'r8d, 4' and self.ins(0x39dd7d1).op_str == 'rdx, rax'
              and self.ins(HELPER_READ).op_str == 'qword ptr [rdi + 0x28]', 'date helper transfer drift')
        check(self.ins(0x39dd7be).op_str == 'rax, rcx' and self.ins(0x39dd7d7).op_str == 'edi, dword ptr [rsi + 0x10]'
              and self.ins(0x39dd7ef).op_str == 'al', 'date helper argument/return drift')
        self.add(THUNK, *[self.pe.va2f(i.address) for i in self.md.disasm(
            self.pe.raw[HELPER:0x39dd7f9], self.pe.f2va(HELPER))])
        for index, pc in enumerate(sr):
            i = self.insns[pc]
            if i.mnemonic == 'call' and pc < FAIL:
                if i.op_str == 'qword ptr [rax + 0x28]':
                    sink_pc, width_pc = sr[index-4], sr[index-2]
                    sink = self.insns[sink_pc]
                    width_ins = self.insns[width_pc]
                    check(sink.mnemonic == 'lea' and sink.op_str.startswith('rdx, [rsi + ')
                          and width_ins.op_str.startswith('r8d, '), f'direct setup {pc:#x}')
                    obj, width = sink.operands[1].mem.disp, width_ins.operands[1].imm
                    sites = [sink_pc, width_pc]
                    kind, native = 'direct', pc
                else:
                    sink_pc = sr[index-2]
                    sink = self.insns[sink_pc]
                    check(self.direct(pc) == THUNK and self.insns[sr[index-1]].op_str == 'rdx, rdi'
                          and sink.op_str.startswith('rcx, [rsi + '), f'helper setup {pc:#x}')
                    obj, width = sink.operands[1].mem.disp, 4
                    sites = [sink_pc, sr[index-1], THUNK, 0x39dd7be, 0x39dd7c8, 0x39dd7d1]
                    kind, native = 'date_helper', HELPER_READ
                transfer[pc] = {'site': self.records[pc], 'object_off': obj, 'width': width, 'kind': kind,
                                'stream_call': self.add(native)[0], 'setup': self.add(*sites)}
            if i.mnemonic.startswith('j') and i.mnemonic != 'jmp':
                prev = sr[index-1]
                cond = self.insns[prev].op_str
                guard = self.static_guard(pc, cond)
                branches[pc] = {'branch': self.records[pc], 'predicate': self.records[prev],
                                'taken_to': hex(self.direct(pc)), 'fallthrough_to': hex(pc+i.size),
                                'class': guard[0], 'operand_source': guard[1], 'assumption': guard[2],
                                'in_t20_23': pc < FAIL}
        bulk_setup = self.add(0x1537aa1, 0x1537aa8, 0x1537ab1)
        check([i['instruction'] for i in bulk_setup] == ['lea rbx, [rsi + 8]', 'mov r8d, 0xc', 'mov rdx, rbx']
              and self.insns[BULK].op_str == 'qword ptr [rax + 0x28]', 'bulk setup drift')
        transfer[BULK] = {'site': self.records[BULK], 'object_off': 8, 'width': 12, 'kind': 'identity_bulk',
                          'stream_call': self.records[BULK], 'setup': bulk_setup}
        direct = [x for x in transfer.values() if x['kind'] == 'direct']
        widths = next(x for x in read_json('scratch/t05/reader_widths.json')['results'] if x['type_id'] == 22)
        check([x['width'] for x in direct] + [12] == widths['seq'][:19]
              and [x['object_off'] for x in direct] == widths['obj_seq'][:18], 't05/t20 transfer regression')
        check((len(direct), len(transfer), len(branches), sum(x['in_t20_23'] for x in branches.values()))
              == (18, 22, 28, 23), 'transfer/branch tally')
        return transfer, branches

    @staticmethod
    def static_guard(pc, predicate):
        if predicate == 'dword ptr [rbx + 0x10], 0':
            return ('runtime_external_io', 'stream status', 'successful full transfer; failure returns false')
        if predicate == 'al, al':
            return ('runtime_external_io', 'date helper AL=(stream status==0)', 'successful full transfer; failure returns false')
        expected = {
            0x153780a: ('r9, r9', 'runtime_external_context', 'R9 supplied by loader (R13 from entry R8)', 'live context'),
            0x153781b: ('byte ptr [rsp + 0x70], 0', 'runtime_external_archive_mode', 'caller stack arg from R12B, not selector or Styp', 'server true; client false; disambiguated by independent framing/differential'),
            0x1537a9b: ('rdi, rdi', 'runtime_external_stream', 'stream wrapper pointee', 'nonnull; null would skip 12B'),
            0x1537acc: ('r8d, 0x989681', 'wire_data', 'unsigned first u32 just read by 12B bulk', 'if >=10000001 replace object u32 with caller ordinal; no bytes consumed'),
            0x1537ad9: ('rcx, rcx', 'runtime_external_callback', 'loader supplies its this as optional callback [caller rsp+0x38]', 'nonnull in this modeled caller; indirect callback body not expanded'),
            0x1537aed: ('rdi, rdi', 'runtime_external_stream', 'same stream saved at 0x1537a95', 'nonnull'),
            0x1537af3: ('dword ptr [rdi + 8]', 'runtime_external_refcount', 'ZF after lock dec (paired with local lock inc)', 'non-final under live owning wrapper; otherwise destructor; not observable from payload'),
        }
        pred, cls, src, note = expected[pc]
        check(pred == predicate, f'branch predicate drift at {pc:#x}: {predicate}')
        return cls, src, note


def walk(raw, transfer, branches, successors, *, mode):
    check(raw[:6] == b'\x03\x01tad.' and len(raw) >= 22, 'member header')
    version, count = struct.unpack_from('<HI', raw, 6)
    check(version == 0xdf1, 'unsupported version for specialized reader')
    p, limit = 13, len(raw)
    rows, variants = [], {}
    outcomes = Counter()
    for ordinal in range(count):
        front = p
        trace = []
        taken = []
        origin = front + 1

        def read(site, width):
            nonlocal p
            check(0 < width <= 12 and p+width <= limit, f'row {ordinal}: stream underflow at {site:#x} @{p:#x}')
            trace.append((site, p-origin, width))
            raw_slice = raw[p:p+width]
            p += width
            return raw_slice

        selector = integer(read(SELECT, 1))
        check(selector == 0, f'unknown t22 selector at row {ordinal}')
        pc, identity = START, None
        wire_ordinal = None
        for _ in range(250):
            if pc in transfer:
                v = read(pc, transfer[pc]['width'])
                if pc == BULK:
                    identity = struct.unpack('<3I', v)
            if pc == RET:
                break
            if pc == FAIL:
                raise CheckError(f'row {ordinal}: failure return')
            if pc in branches:
                b = branches[pc]
                if b['class'] == 'runtime_external_archive_mode':
                    jump = not mode
                elif b['class'] == 'wire_data':
                    check(identity is not None, 'range test without identity input')
                    jump = identity[0] < 0x989681
                    wire_ordinal = identity[0] if jump else ordinal
                else:
                    # This path assumes success, nonnull context/stream/callback, live refcount.
                    jump = pc in (0x1537a87, 0x1537af3)
                outcomes[pc, jump] += 1
                if jump:
                    taken.append(pc)
                pc = int(b['taken_to'] if jump else b['fallthrough_to'], 16)
            else:
                next_pcs = successors[pc]
                check(len(next_pcs) == 1, f'unmodeled outgoing edge at {pc:#x}')
                pc = next_pcs[0]
        else:
            raise CheckError('instruction walk exceeded bound')
        check(identity is not None and wire_ordinal == identity[0] == ordinal
              and identity[1] == identity[2] == ordinal+1, f'row {ordinal}: identity postcondition')
        key = tuple(trace), tuple(taken)
        if key not in variants:
            variants[key] = len(variants)
        rows.append({'ordinal': ordinal, 'selector_start': front, 'body_start': origin, 'body_end': p,
                     'trace_variant': variants[key], 'id_u32': list(identity), 'body_sha256': sha(raw[origin:p])})
    footer_at = p
    footer = []
    for site, width in FOOT:
        check(p+width <= limit, 'truncated footer')
        footer.append({'site': hex(site), 'offset': p, 'width': width, 'value': integer(raw[p:p+width])})
        p += width
    check(p == limit and [v['value'] for v in footer] == [0, 1, count], 'physical footer mismatch')
    return rows, [{'id': n, 'transfers': [[hex(s), o, w] for s, o, w in tr],
                   'taken_conditions': [hex(s) for s in taken]} for (tr, taken), n in variants.items()], outcomes, footer, footer_at


def archive_data():
    os.environ['FM24_DB_DIR'] = DATA  # no Z: fallback, even when preconfigured
    import fm24_dump as db
    codec = db._reader()
    indexes = {}
    payloads = {}
    for archive in ('client', 'server'):
        fn = archive + '_db.dat'
        indexes[archive] = {e['table_id']: e for e in codec['list_tables'](db.DB_DIR / fn, fn)
                            if e['table_id'] is not None and e['entry_type'] == 'table'}
        check(22 in indexes[archive], f'missing table_22 in {archive}')
        payloads[archive] = db.load_payload(codec, archive, 22)
        e = indexes[archive][22]
        check(e['size'] == len(payloads[archive]), 'archive index size mismatch')
        check(struct.unpack_from('<HI', payloads[archive], 6) == (e['payload_version'], e['record_count_header']), 'index header mismatch')
    # Independently recover the stadium ordinal set, not the public stable UID set.
    raw = db.load_payload(codec, 'client', 21)
    stad_n = struct.unpack_from('<I', raw, 8)[0]
    check(stad_n == 48413 and len(raw) == 14 + 38*stad_n + 8, 'stadium domain frame')
    stad_ids = {struct.unpack_from('<I', raw, 14+38*i+25)[0] for i in range(stad_n)}
    check(stad_ids == set(range(stad_n)), 'stadium ordinal domain')
    club = read_json('scratch/t24/out/cursor.json')
    club_ids = {r[0] for name in club['rows']['shards'] for r in read_json('scratch/t24/out/'+name)['rows']}
    check(club['row_count'] == 84259 and club_ids == set(range(club['row_count'])), 't24 club ordinal domain')
    return payloads, indexes, stad_ids, club_ids


def date_profile(values):
    live = [v for v in values if v not in (0, 0xffffffff)]
    matches = [(v >> 16, v & 65535) for v in live if 1850 <= v >> 16 <= 2100 and 1 <= v & 65535 <= 366]
    ys = [y for y, _ in matches]
    return dict(ratio_of_live=len(matches)/len(live), year_min=min(ys), year_max=max(ys),
                year_distinct=len(set(ys)), day_max=max(d for _, d in matches))


def profile(data, off, width, rules=None):
    raw = [r[off:off+width] for r in data]
    unsigned = list(map(integer, raw))
    signed = [int.from_bytes(c, 'little', signed=True) for c in raw]
    hist = Counter(signed)
    out = {'n': len(raw), 'distinct': len(hist), 'min_signed': min(hist), 'max_signed': max(hist),
           'sentinel_ff': hist[-1], 'zero': hist[0], 'top_signed_freq': hist.most_common(8),
           'sample_hex': {i: raw[i].hex() for i in (0, len(raw)//2, len(raw)-1)}}
    if not rules:
        return out
    kind = rules['kind']
    if kind == 'date':
        p = date_profile(unsigned)
        out['packed'] = p
        ok = [1850 <= v >> 16 <= 2100 and 1 <= v & 65535 <= 366 for v in unsigned]
    elif kind == 'reference':
        live = [v for v in signed if v != -1]
        out['live'] = {'count': len(live), 'distinct': len(set(live)), 'min': min(live), 'max': max(live),
                       'club_ordinal_matches': sum(v in rules['club'] for v in live)}
        if 'stadium' in rules:
            out['live']['stadium_ordinal_matches'] = sum(v in rules['stadium'] for v in live)
        ok = [v == -1 or (v in rules['club'] and v in rules.get('stadium', rules['club'])) for v in signed]
    elif kind == 'mask':
        ok = [v & ~rules['known_mask'] == 0 for v in unsigned]
        out['decoded_counts'] = dict(Counter((v >> rules['bit']) & 1 for v in unsigned))
    elif kind == 'enum':
        ok = [v in rules['allowed'] for v in signed]
        out['allowed_wire_from_UI'] = rules['allowed']
    else:
        # -1 is an explicitly checked absent value in the integer getter, not an in-range measurement.
        ok = [v == -1 or rules['min'] <= v <= rules['max'] for v in signed]
        out['live_bounds_from_UI'] = [rules['min'], rules['max']]
    out['matches'] = sum(ok)
    out['mismatch_samples'] = [[i, signed[i]] for i, v in enumerate(ok) if not v][:10]
    return out


def ledger(st, data, variant, stad_ids, club_ids):
    source = read_json(MASTER)
    cstc = next(f for f in source['entities']['club.xml'][0]['fields'] if f['field'] == 'Cstc')['list_item_fields']
    inventory = [f for f in read_json('scratch/t05/schema_inventory.json')['entities']['club']['fields'] if f.get('parent') == 'Cstc']
    t24 = [f for path in sorted((ROOT/'scratch/t24/out').glob('subtables.part*.json'))
           for f in read_json(path)['nested_fields'] if f['parent'] == 'Cstc']
    check(len(cstc) == len(inventory) == len(t24) == 28, 'Cstc occurrence count')
    check([(f['idx'], f['code']) for f in inventory] == [(f['idx'], f['code']) for f in t24], 't24 schema join')
    by_code = defaultdict(list)
    for m, f in zip(cstc, inventory):
        check((m['field'], m['name'], m['type']) == (f['code'], f['name'], f['type']), 'schema source mismatch')
        by_code[m['field']].append({'idx': f['idx'], **m})
    code_db = read_json('scratch/t12/out/codes_full.json')
    check(code_db['exe_sha256'] == SHA, 't12 provenance')
    dates = {d['u32_off']: d for d in next(x for x in read_json('scratch/t13d/out/audit.json')['tables']
                                            if x['table_type'] == 22)['date_cols']}
    fields = []
    for site, off, width in variant['transfers']:
        tr = st.transfer.get(int(site, 16))
        if not tr:
            continue
        obj = tr['object_off']
        evidence = []
        for code in by_code:
            for x in code_db['codes'][code]:
                cmp_off = int(x['file_off'], 16)
                same_obj = x.get('object_off') in ([obj, obj+2] if tr['kind'] == 'date_helper' else [obj])
                if not (0x1538ee0 <= cmp_off < 0x1539400 and same_obj and x.get('shape') in ('read', 'ref_ptr')):
                    continue
                if x['size'] != (2 if tr['kind'] == 'date_helper' else width):
                    continue
                cmp_ins = st.ins(cmp_off)
                check(cmp_ins.address in st.getter_cfg.instructions, 'unreachable getter compare')
                check(cmp_ins.mnemonic == 'cmp' and cmp_ins.op_str.startswith('edx, ')
                      and cmp_ins.operands[1].imm == int.from_bytes(code.encode(), 'big'), 'getter dispatch cmp')
                access = st.pe.va2f(int(x['access_va'], 16))
                ins = st.ins(access)
                check(f'{ins.mnemonic} {ins.op_str}' == x['instruction'] and ins.operands[1].mem.disp == x['object_off']
                      and ins.op_str.find('[rbx +') >= 0, 'getter access bytes')
                branch_off = cmp_off+cmp_ins.size
                branch = st.ins(branch_off)
                root = st.direct(branch_off) if branch.mnemonic == 'je' else branch_off+branch.size
                check(branch.mnemonic in ('je', 'jne'), f'getter dispatch route {code} {cmp_off:#x}')
                evidence.append({'code': code, 'object_off': x['object_off'], 'shape': x['shape'],
                                 'cmp_and_branch': st.add(cmp_off, branch_off), 'matched_path': st.getter_path(root, access),
                                 'access': st.add(access)[0]})
        codes = sorted(set(x['code'] for x in evidence))
        check(len(codes) <= 1, 'multi-code object slot requires an explicit new decision')
        code = codes[0] if codes else None
        candidates = by_code[code] if code else []
        grade = 'unnamed'
        why = 'no Cstc getter at object slot'
        extra = []
        p = profile(data, off, width)
        if code or obj == 0x18:
            kind = candidates[0]['type'] if code else 'database_record_unique_id'
            if kind == 'date':
                check({x['object_off'] for x in evidence} == {obj, obj+2}, 'incomplete date getter')
                for ev in evidence:
                    src = int(ev['access']['file_offset'], 16)
                    extra += st.add(*[st.pe.va2f(i.address) for i in st.md.disasm(st.pe.raw[src:src+(15 if ev['object_off'] == obj else 16)], st.pe.f2va(src))])
                rules = {'kind': 'date'}
            elif kind == 'database_record_unique_id':
                check(not code or evidence[0]['shape'] == 'ref_ptr', 'expected reference getter')
                check(not code or {f['database_table_type'] for f in candidates} == {'stadium'}, 'reference domain drift')
                rules = {'kind': 'reference', 'club': club_ids, **({'stadium': stad_ids} if code else {})}
            elif kind == 'boolean':
                check(code == 'Scpm' and [x['instruction'] for x in st.add(0x1539518, 0x153951b)]
                      == ['shr bl, 2', 'and bl, 1'], 'Scpm bit extraction')
                extra = st.add(0x1539518, 0x153951b)
                rules = {'kind': 'mask', 'bit': 2, 'known_mask': 0x06}  # bit 1 retained, not Bools-as-whole-byte
            elif kind == 'enum':
                allowed = [int(v['enum']) for v in source['enums'][code]['values']]
                rules = {'kind': 'enum', 'allowed': allowed + ([-1] if candidates[0].get('is_optional') == 'true' else [])}
            else:
                check(kind == 'integer', 'unknown schema type')
                rules = {'kind': 'integer', 'min': int(candidates[0]['min_value']), 'max': int(candidates[0]['max_value'])}
                # Verify absence sentinel at every integer getter (including 1B signed fields).
                access = int(evidence[0]['access']['file_offset'], 16)
                next_pc = access + st.ins(access).size
                extra = st.add(next_pc)
                check(extra[0]['instruction'] == 'cmp edi, -1', 'integer -1 sentinel not in getter')
            p = profile(data, off, width, rules)
            if kind == 'date':
                check(off in dates and p['packed'] == {k:v for k,v in dates[off].items() if k != 'u32_off'}, 't13d date differential')
                p['t13d_match'] = True
            if not code:
                why = 'writer emits referenced record +8 (or FFFFFFFF); club ordinal compatible; no nested 4CC'
                p['club_domain_basis'] = 't24 walked record ordinals; not stable public UIDs'
            elif len(candidates) != 1:
                grade, why = 'L3_code_row_only', 'one physical getter; repeated schema occurrences not counted'
                p['by_raw_type'] = {t: {'rows': sum(r[24] == t for r in data), 'live': sum(r[24] == t and r[off:off+width] != b'\xff'*width for r in data)} for t in range(1,6)}
            elif p['matches'] == len(data):
                grade, why = 'L3_named_row_coordinate', 'unique scoped getter + walked sink + 449/449 profile'
                if code in ('Scap', 'Sscp'):
                    p['ui_dependency_caveat'] = {'schema_type': 6, 'observed_type_with_non_null_values': 2,
                                                 'storage_only_no_UI_equivalence': True}
            else:
                grade, why = 'L3_coordinate_profile_conflict', 'raw values outside snapshot editor schema domain; no normalization assumed'
        named = grade == 'L3_named_row_coordinate'
        fields.append({'name': candidates[0]['name'] if named else None, 'code': code if named else None,
                       'row_offset': off if named else None, 'wire_offset': off, 'width': width, 'object_off': obj,
                       'VA': tr['site']['VA'], 'bytes': tr['site']['bytes'], 'file_offset': site, 'grade': grade,
                       'candidate_code': code, 'schema_occurrences': candidates, 'getter': evidence, 'getter_extra': extra,
                       'disposition': why, 'data_profile': p})
    check({f['candidate_code'] for f in fields if f['candidate_code']} == set(by_code), 'unmapped schema codes')
    return fields


def scout(st, indexes):
    subtables = [f for path in sorted((ROOT/'scratch/t24/out').glob('subtables.part*.json'))
                 for f in read_json(path)['nested_fields']]
    counts = Counter(f['parent'] for f in subtables)
    # Anchors for a hunt; no identity claims for the inferred prefix join.
    candidates = {'Cstc': 22, 'Cdbt': 33, 'Tchl': 34, 'Clhs': 37, 'Cmti': 43,
                  'Csme': 59, 'CSrs': 62, 'CNtp': 66}
    w = {r['type_id']: r for r in read_json('scratch/t05/reader_widths.json')['results']}
    rows = []
    for code, count in counts.items():
        tid = candidates.get(code)
        reader = w[tid]['reader'] if tid else None
        archives = {a: {'count': e['record_count_header'], 'bytes': e['size']} for a, index in indexes.items()
                    if (e := index.get(tid)) and 'record_count_header' in e}
        known_strides = {22: {'client': 13, 'server': 79}, 34: {'server': 44},
                         37: {'server': 40}, 43: {'server': 46}, 66: {'server': 24}}
        arith = {a: n for a, e in archives.items()
                 if e['count'] and (n := (e['bytes']-22)//e['count']) and (e['bytes']-22) % e['count'] == 0}
        rows.append({'parent': code, 'schema_fields': count, 'table_id': tid,
                     'RTTI': st.census[tid].get('primary_class') if tid else None,
                     'reader_VA': hex(st.pe.f2va(int(reader, 16))) if reader else None,
                     'stride': known_strides.get(tid), 'arithmetic_only_stride': arith if tid not in known_strides else {},
                     'archive_index': archives,
                     'status': ('complete_E56_parent_link' if tid == 22 else 'partial_scout_candidate' if tid else 'partial_unknown')})
    by_parent = {r['parent']: r for r in rows}
    for code, offsets in {'Cafl': (0xe8b4db, 0xe8b4e1, 0xe8f13a, 0xe8f13d, 0x15320b0, 0x436385d, 0x4363864),
                          'Cvfl': (0xe8c1e8, 0xe8c1ee, 0xe8c1f4, 0xe8c1fc, 0xe8c214, 0xe8c217, 0x15322f3, 0x15322fa)}.items():
        ev = st.add(*offsets)
        check(st.ins(offsets[0]).operands[1].imm == int.from_bytes(code.encode(), 'big'), 'affiliation scout dispatch')
        by_parent[code].update({'status': 'partial_club_getter_collection_lead', 'getter_evidence': ev,
                                'notes': 'getter arms inspect +0x118/+0x120; possible shared club-owned collection; storage writer/reader and standalone member unproven'})
    for tid, reason, stride in [(64, 'RTTI club staff job status; exact schema parent unknown', 21),
                                (65, 'RTTI starting newgen parameter; exact schema parent unknown', None),
                                (67, 'shares reader with 65; no club parent assigned', None),
                                (68, 'shares reader with 65; no club parent assigned', None),
                                (69, 'shares reader with 65; no club parent assigned', None)]:
        e = indexes['server'][tid]
        rows.append({'parent': None, 'schema_fields': None, 'table_id': tid, 'RTTI': st.census[tid]['primary_class'],
                     'reader_VA': hex(st.pe.f2va(int(w[tid]['reader'], 16))), 'stride': {'server': stride} if stride else None,
                     'arithmetic_only_stride': {'server': 31} if not stride else {}, 'notes': reason,
                     'archive_index': {'server': {'count': e['record_count_header'], 'bytes': e['size']}},
                     'status': 'partial_unjoined_RTTI_anchor'})
    return rows


def build():
    st = Static()
    OUT.mkdir(parents=True, exist_ok=True)
    # Persist CFG before I/O/data matching: if later phases fail, the evidence survives.
    static = {'status': 'partial_CFG_only', 'provenance': st.provenance,
              'factory_handler': st.add(0xf49092, 0xf490a2, 0x43696d2, 0x43696d9),
              'table_identity': {'scope': 'club.Cstc (E56)', 'RTTI': 'STADIUM_CHANGE', 'table_id': 22},
              'reader': {'VA': hex(st.slot(19)), 'file_offset': hex(START), 'end_exclusive': hex(st.cfg.function_end_off),
                         'vtable_VA': hex(st.vtable), 'vtable_file_offset': hex(st.vtable_off),
                         'getter_slot2_VA': hex(st.slot(2)), 'writer_slot21_VA': hex(st.slot(21))},
              'cfg': {'blocks': st.blocks, 'boundary_source': 'PE exception directory runtime-function extent',
                      'reachable_instructions': len(st.insns),
                      'conditional_t20_window': 23, 'conditional_reader_total': len(st.branches),
                      'unconditional_reader_total': sum(i.mnemonic == 'jmp' for i in st.insns.values()),
                      'external_edges': st.cfg.external_edges,
                      'helper_conditions': [
                          {'branch': st.add(0x39dd7bc)[0], 'predicate': st.add(0x39dd7b9)[0],
                           'class': 'negative_live_stream_null', 'observed_taken': 0,
                           'reason': 'null skips read then dereferences stream+0x10; out of valid live input domain'},
                          {'branch': st.add(0x39dd7de)[0], 'predicate': st.add(0x39dd7da)[0],
                           'class': 'runtime_external_refcount', 'reason': 'non-final local release on owning wrapper assumption'}]},
              'branch_shards': shards('branches', 'branches', list(st.branches.values()), 28),
              'transfer_shards': shards('transfers', 'transfers', list(st.transfer.values()), 22),
              'instruction_shards': shards('instructions', 'instructions', [st.records[x] for x in sorted(st.records)], 140)}
    dump('cursor_t22.json', static)
    payload, indexes, stad_ids, club_ids = archive_data()
    successors = {st.pe.va2f(pc): [st.pe.va2f(x) for x in next_pcs] for pc, next_pcs in st.cfg.successors.items()}
    summaries = {}
    all_rows = {}
    for archive in ('server', 'client'):
        raw = payload[archive]
        mode = archive == 'server'
        rows, variants, path_outcomes, footer, footer_at = walk(raw, st.transfer, st.branches, successors, mode=mode)
        stride = 79 if mode else 13
        check(len(rows) == 449 and len(variants) == 1 and len(raw) == 14 + stride*len(rows) + 8, f'{archive} length')
        check(all(r['selector_start'] == 13+stride*i and r['body_end'] == 13+stride*(i+1)
                  for i, r in enumerate(rows)), f'{archive} row extent')
        try:
            walk(raw, st.transfer, st.branches, successors, mode=not mode)
        except CheckError as e:
            negative = str(e)
        else:
            raise CheckError(f'{archive} unexpectedly accepts swapped mode')
        summaries[archive] = {'status': 'complete_observed_walk', 'archive_member': indexes[archive][22],
                              'payload_sha256': sha(raw), 'mode': mode, 'swapped_mode_rejection': negative, 'row_count': len(rows), 'stride': stride,
                              'legacy_row_origin': 14, 'wire_row_origin': 13, 'header_hex': raw[:13].hex(),
                              'legacy_footer_start': footer_at+1, 'legacy_footer_hex': raw[footer_at+1:].hex(),
                              'wire_footer_start': footer_at, 'wire_footer_hex': raw[footer_at:].hex(), 'footer': footer,
                              'trace_templates': variants,
                              'rows': shards('rows_'+archive, 'rows', rows, 160) if mode else None,
                              'branch_outcomes': {hex(pc): {'taken': path_outcomes[pc, True],
                                                           'fallthrough': path_outcomes[pc, False]}
                                                  for pc in st.branches}}
        all_rows[archive] = rows
    raw = payload['server']
    data = [raw[r['body_start']:r['body_end']] for r in all_rows['server']]
    check(all(s['id_u32'] == c['id_u32'] for s, c in zip(all_rows['server'], all_rows['client'])), 'client/server bulk differential')
    with (ROOT/'scratch/t13d/out/t22.csv').open(encoding='utf-8', newline='') as stream:
        old = list(csv.DictReader(stream))
    check(len(old) == len(data) and all(int(o['offset']) == r['body_start'] and bytes.fromhex(o['raw_hex'])
          == raw[r['body_start']:r['body_end']+1] for o, r in zip(old, all_rows['server'])), 't13d CSV differential')
    for off, bit in [(0x1537bdb, 0x18), (0x1537c0f, 0x20), (0x1537c43, 0x28)]:
        check(st.ins(off).operands[1].mem.disp == bit, 'reference writer operand')
    ref_support = [0x1537bdb, 0x1537be4, 0x1537be9, 0x1537c03, 0x1537c0f, 0x1537c18, 0x1537c43, 0x1537c4c,
                   0x4369fa7, 0x4369fab, 0x4369fc2, 0x4369fc7, 0x4369fd1, 0x4369fd6, 0x4369fe0, 0x4369fe5, 0x4369ff2,
                   0xf7e440, 0x3bf34a0, 0x3bf34b2, 0xf7f340, 0x3bf6ed6, 0x3bf6efb, 0x3bf6f11]
    st.add(*WRAPPER, *ref_support, 0xf4909c, 0xf4909f)
    fields = ledger(st, data, summaries['server']['trace_templates'][0], stad_ids, club_ids)
    named = [f['code'] for f in fields if f['code']]
    check(len(named) > 0, 'no fields promoted')
    old_ledger = read_json('scratch/t20/out/fields_t22.json')
    old_t20 = {f['field_code_candidate']: f['row_offset_candidate'] for f in old_ledger['fields'] if f['field_code_candidate']}
    for f in fields:
        f['t20_linear_candidate'] = old_t20.get(f['candidate_code'])
    conflicts = {'Scap': 12, 'Styp': 16, 'Salt': 17, 'Sceb': 50}
    check(all(not (f['row_offset'] is not None and conflicts.get(f['code']) == f['row_offset']) for f in fields), 'revived t20 conflict')
    negatives = [{'code': code, 't20_row_offset': off, 'status': 'negative_t20_linear_date_conflict'} for code, off in conflicts.items()]
    refs = next(f['data_profile']['live'] for f in fields if f['object_off'] == 24)
    check(refs == {'count': 361, 'distinct': 310, 'min': 86, 'max': 82403, 'club_ordinal_matches': 361}, 'slot0 data mismatch')
    static.update({'status': 'complete_observed_row_cursor_partial_runtime_only_edges', 'archives': summaries,
                   'index_hash_note': 'archive_member.sha256 is the index entry digest from the existing codec, not the newly computed decompressed payload_sha256',
                   'legacy_alignment': '14 + 449*79 + 8 = 35493; legacy +78 is next selector (last row: first zero footer byte)',
                   'wire_alignment': '13 + 449*(1+66+12) + 9 = 35493; 66 = 54 direct + 12 date helper, not t20 54+12 bulk',
                   'wrapper_proof': [hex(x) for x in WRAPPER],
                   'bulk': {'status': 'complete_identity_transport', 'server_row_offset': 66, 'client_row_offset': 0, 'width': 12,
                            'object_off': 8, 'site': hex(BULK), 'lanes': [
                                {'byte': 0, 'object_off': 8, 'pattern': 'u32 ordinal 0..448; range comparator at 0x1537ac5'},
                                {'byte': 4, 'object_off': 12, 'pattern': 'u32 ordinal+1; low lane of UID-like pair'},
                                {'byte': 8, 'object_off': 16, 'pattern': 'u32 equals previous; high lane of UID-like pair'}],
                            'client_server_exact_matches': 449, 'counted_as_nested_fields': 0,
                            'related_identity_source': 't24 base identity object+8 and generic duni chain; do not infer stadium/club FK from the lane values'},
                   'slot0': {'status': 'partial_unnamed_reference', 'server_row_offset': 0, 'width': 4, 'object_off': 24,
                             'shape': 'u32 referenced record ordinal or FFFFFFFF; post-read qword fixup; club-domain compatible',
                             'data_profile': refs, 'evidence': [hex(x) for x in ref_support],
                             'reason_not_named': 'no scoped Cstc getter / no schema occurrence for backlink; no 4CC inferred'},
                   'instruction_shards': shards('instructions', 'instructions', [st.records[x] for x in sorted(st.records)], 140),
                   'scout': 'scout.json',
                   'runtime_limits': ['No archive input determines stream/context/IO/refcount state directly.',
                                      'Callback dispatch and alternate destructor have not been expanded; cursor assumes no extra stream transfer there. Differential closure and CSV support the observed bytes only.',
                                      'Three date helper invocations all take the same successfully read return edge; Styp never drives byte consumption.']})
    OUT.mkdir(parents=True, exist_ok=True)
    dump('scout.json', {'status': 'partial_scout_only', 'rows': scout(st, indexes)})
    dump('fields_t22.json', {'status': 'partial_Cstc_ledger', 'parent': 'Cstc', 'table_id': 22, 'archive': 'server',
                              'baseline_named': old_ledger['fields_named'], 'fields_named': len(named), 'schema_occurrences': 28,
                              'promoted_codes': named, 'unpromoted_count_by_grade': dict(Counter(f['grade'] for f in fields if not f['code'])),
                              'offset_origin': 'first body byte after selector (same as t20 legacy origin)',
                              'fields': shards('fields_t22', 'fields', fields, 8), 'negative_regressions': negatives})
    # Include observed counts at each classified branch as well as row-template bitsets.
    for pc, record in st.branches.items():
        record['observed'] = {archive: doc['branch_outcomes'][hex(pc)] for archive, doc in summaries.items()}
    static['branch_shards'] = shards('branches', 'branches', list(st.branches.values()), 28)
    dump('cursor_t22.json', static)
    print(f"t27: 449 server 79B / 449 client 13B; CFG 23 t20 + 5 tail conditions; {len(named)}/28 named")


def selftest():
    identity = struct.pack('<3I', 0, 1, 1)
    header = b'\x03\x01tad.' + struct.pack('<HI', 0xdf1, 1) + b'\0'
    footer = struct.pack('<IBI', 0, 1, 1)
    raw = header + b'\0' + identity + footer
    tr = {BULK: {'width': 12}}
    b = {0x1537acc: {'class': 'wire_data', 'taken_to': hex(RET), 'fallthrough_to': hex(RET)}}
    edge = {START: [BULK], BULK: [0x1537acc]}
    rows, trace, path, _, p = walk(raw, tr, b, edge, mode=False)
    check(rows[0]['body_end'] == p == 26 and path[0x1537acc, True] == 1 and trace[0]['transfers'][-1][1:] == [0, 12], 'synthetic trace')
    for bad in (raw[:-1], header + b'\0' + struct.pack('<I', 10000001) + identity[4:] + footer):
        try:
            walk(bad, tr, b, edge, mode=False)
        except CheckError:
            continue
        raise CheckError('bad synthetic row accepted')
    check(date_profile([2000 << 16 | 1, 2030 << 16 | 100])['year_max'] == 2030, 'synthetic date')
    print('t27 builder selftest: PASS')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest', action='store_true', help='check the cursor and rejection logic on synthetic data')
    args = ap.parse_args()
    try:
        if args.selftest:
            selftest()
        else:
            build()
        return 0
    except CheckError as exc:
        print(f't27 check failed: {exc}', file=sys.stderr)
        return 1
    except (OSError, ValueError, ImportError, KeyError, IndexError, RuntimeError, StopIteration, TypeError) as exc:
        print(f't27 fatal: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
