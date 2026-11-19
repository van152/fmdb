#!/usr/bin/env python3
"""Independently replay t27 from archived bytes and check the published evidence."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
from struct import unpack_from, pack
import sys

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))

# Independent audit table, not imported from the builder or taken from its JSON.
# (reader call file offset, row coordinate, width, object displacement)
LAYOUT = (
    (0x1537834, 0, 4, 0x18), (0x1537854, 4, 4, 0x20), (0x1537874, 8, 4, 0x28),
    (0x1537888, 12, 4, 0x30), (0x153789c, 16, 4, 0x34), (0x15378bc, 20, 4, 0x3c),
    (0x15378dc, 24, 1, 0x64), (0x15378fc, 25, 4, 0x48), (0x153791c, 29, 1, 0x65),
    (0x153793c, 30, 4, 0x40), (0x153795c, 34, 4, 0x50), (0x153797c, 38, 4, 0x54),
    (0x153799c, 42, 4, 0x58), (0x15379bc, 46, 4, 0x5c), (0x15379d0, 50, 4, 0x38),
    (0x15379f0, 54, 1, 0x66), (0x1537a10, 55, 4, 0x60), (0x1537a2c, 59, 1, 0x69),
    (0x1537a48, 60, 1, 0x67), (0x1537a64, 61, 1, 0x68), (0x1537a80, 62, 4, 0x44),
    (0x1537ab4, 66, 12, 8),
)
NAMED = {'Slea': 12, 'Scap': 20, 'Salt': 25, 'Scpm': 29, 'Sscp': 30, 'Snxa': 34, 'Snmn': 38,
         'Snmx': 42, 'Stks': 46, 'Slmd': 50, 'Slhm': 54, 'ScTL': 60, 'ScYL': 61, 'Sceb': 62}
HELD = {'Sold': (4,449), 'Snew': (8,449), 'Ssta': (16,449),
        'Styp': (24,361), 'Scam': (55,446), 'Scns': (59,426)}
EXPECTED_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'


class Reject(Exception):
    pass


def req(cond, reason):
    if not cond:
        raise Reject(reason)


def json_at(path):
    return json.loads(path.read_text(encoding='utf-8'))


def read_part(files, key):
    for f in files:
        yield from json_at(OUT/f)[key]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def split(raw, stride):
    req(raw[:8] == bytes.fromhex('03017461642ef10d') and len(raw) >= 22, 'member header')
    n = unpack_from('<I', raw, 8)[0]
    req(raw[12] == 0 and len(raw) == 13+n*stride+9, 'count × stride')
    terminal = 13+n*stride
    req(raw[terminal:] == pack('<IBI', 0, 1, n), 'physical 9B footer')
    bodies = []
    for i in range(n):
        row = raw[13+i*stride:13+(i+1)*stride]
        req(row[0] == 0, 'selector')
        req(unpack_from('<III', row, stride-12) == (i,i+1,i+1), 'identity tail')
        bodies.append(row[1:])
    return terminal, bodies


def get_rule_count(master, cells, schema):
    w = len(cells[0])
    xs = [int.from_bytes(c, 'little', signed=True) for c in cells]
    kind = schema['type']
    if kind == 'date':
        mask = [1850 <= y <= 2100 and 1 <= d <= 366 for d, y in (unpack_from('<HH', c) for c in cells)]
    elif kind == 'database_record_unique_id':
        req(schema['database_table_type'] == 'stadium' and w == 4, 'reference schema')
        mask = [x == -1 or (0 <= x < 48413 and x < 84259) for x in xs]
    elif kind == 'boolean':
        req(schema['field'] == 'Scpm' and w == 1, 'boolean packing')
        mask = [x in (0,2,4,6) for x in xs]
    elif kind == 'enum':
        vals = {int(v['enum']) for v in master['enums'][schema['field']]['values']}
        if schema.get('is_optional') == 'true':
            vals.add(-1)
        mask = [x in vals for x in xs]
    else:
        req(kind == 'integer', 'unknown type')
        lo, hi = (int(schema[key]) for key in ['min_value','max_value'])
        mask = [x == -1 or lo <= x <= hi for x in xs]
    return sum(mask)


def verify():
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from t05_pe import PE
    os.environ['FM24_DB_DIR'] = 'D:/tmp2b/fm24-db/scratch/data'
    import fm24_dump as db
    codec = db._reader()
    c = json_at(OUT/'cursor_t22.json')
    f = json_at(OUT/'fields_t22.json')
    req(c['status'] == 'complete_observed_row_cursor_partial_runtime_only_edges'
        and f['status'] == 'partial_Cstc_ledger', 'published statuses')
    pe = PE(Path('D:/tmp2b/fm24/input/editor.exe'))
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    req(digest(pe.raw) == c['provenance']['editor_sha256'] == EXPECTED_SHA, 'PE hash')
    snap = {x['path']: x['sha256'] for x in json_at(ROOT/'evidence/MANIFEST.json')['files']}
    for path in ('evidence/fm24/reports/qa/IDA_PROVENANCE.md', 'evidence/fm24/reports/editor_schema/master.json'):
        req(digest((ROOT/path).read_bytes()) == snap[path] == c['provenance']['snapshot_manifest'][path], path)
    req(EXPECTED_SHA in (ROOT/'evidence/fm24/reports/qa/IDA_PROVENANCE.md').read_text(encoding='utf-8'), 'provenance digest')
    vt = pe.va2f(0x1418bd5a8)
    req(unpack_from('<Q', pe.raw, vt+19*8)[0] == 0x141538200 and pe.va2f(0x141538200) == 0x1537800, 'slot19')
    req(unpack_from('<Q', pe.raw, vt+2*8)[0] == 0x1415398e0, 'getter slot')

    def decode(r):
        o, va, bytes_ = int(r['file_offset'],16), int(r['VA'],16), bytes.fromhex(r['bytes'])
        i = next(md.disasm(pe.raw[o:o+15], va, count=1))
        req(pe.va2f(va) == o and pe.f2va(o) == va and i.bytes == bytes_
            and f'{i.mnemonic} {i.op_str}'.rstrip() == r['instruction'], f'drift at {o:#x}')
        return i

    ins = {r['file_offset']: decode(r) for r in read_part(c['instruction_shards'], 'instructions')}
    blocks = {b['start']: b for b in c['cfg']['blocks']}
    covered = []
    stack = ['0x1537800']
    visited = set()
    while stack:
        key = stack.pop()
        if key in visited:
            continue
        visited.add(key)
        block = blocks[key]
        addrs = block['instructions']
        req(addrs[0] == key and addrs[-1] == block['end_instruction'], 'block endpoints')
        covered.extend(addrs)
        for a,b in zip(addrs, addrs[1:]):
            req(not ins[a].mnemonic.startswith(('j', 'ret')) and ins[a].address+ins[a].size == ins[b].address, 'noncontiguous block')
        last = ins[addrs[-1]]
        targets = set()
        if last.mnemonic.startswith('j'):
            targets.add(hex(pe.va2f(last.operands[0].imm)))
        if last.mnemonic not in ('jmp', 'ret'):
            targets.add(hex(pe.va2f(last.address+last.size)))
        req(targets == set(block['successors']), 'block successor graph')
        stack.extend(targets)
    req(len(visited) == len(blocks) == 35 and len(set(covered)) == len(covered) == 210, 'CFG coverage')
    conds = {a for a in covered if ins[a].mnemonic.startswith('j') and ins[a].mnemonic != 'jmp'}
    branch = list(read_part(c['branch_shards'], 'branches'))
    req({b['branch']['file_offset'] for b in branch} == conds and len(branch) == len(conds) == 28
        and sum(b['in_t20_23'] for b in branch) == 23, 'branch ledger coverage')
    req([b['branch']['file_offset'] for b in branch if b['class'] == 'wire_data'] == ['0x1537acc'], 'wire body predicate set')
    for b in branch:
        i = decode(b['branch'])
        prev = decode(b['predicate'])
        req(prev.address+prev.size == i.address and b['taken_to'] == hex(pe.va2f(i.operands[0].imm))
            and b['fallthrough_to'] == hex(pe.va2f(i.address+i.size)), 'branch endpoints')
        for a in ('server','client'):
            req(b['observed'][a] == c['archives'][a]['branch_outcomes'][b['branch']['file_offset']], 'branch totals sync')
    transfers = {int(r['site']['file_offset'],16): r for r in read_part(c['transfer_shards'], 'transfers')}
    req(len(transfers) == len(LAYOUT), 'transfer count')
    n_calls = Counter(ins[a].mnemonic for a in covered)
    req(n_calls['call'] == len(LAYOUT)+2, 'unclassified reader calls')
    p = 0
    for site, off, w, obj in LAYOUT:
        r = transfers[site]
        req(p == off and r['width'] == w and r['object_off'] == obj, 'transfer coordinate')
        p += w
        for i in (r['site'], r['stream_call'], *r['setup']):
            decode(i)
    req(p == 78 and all(transfers[a]['stream_call']['file_offset'] == '0x39dd7d4' for a in (0x1537888, 0x153789c, 0x15379d0)), 'three helper transfers')

    decoded, payload = {}, {}
    for a,s in (('server',79), ('client',13)):
        fn = a+'_db.dat'
        entries = [e for e in codec['list_tables'](db.DB_DIR/fn,fn) if e['table_id'] == 22]
        d = c['archives'][a]
        req(len(entries) == 1 and entries[0] == d['archive_member'], f'{a} member')
        raw = payload[a] = db.load_payload(codec,a,22)
        foot, rows = split(raw, s)
        req(len(rows) == d['row_count'] == 449 and digest(raw) == d['payload_sha256'], 'archive digest/count')
        req(d['wire_footer_start'] == foot and d['legacy_footer_start'] == foot+1
            and bytes.fromhex(d['wire_footer_hex']) == raw[foot:] and len(raw[foot+1:]) == 8, 'both footer conventions')
        req(d['stride'] == s and d['mode'] == (a == 'server') and d['swapped_mode_rejection'], 'archive mode')
        tpl = d['trace_templates']
        expected = [(hex(k), o, w) for k,o,w,_ in LAYOUT] if a == 'server' else [('0x1537ab4',0,12)]
        req(len(tpl) == 1 and [tuple(r) for r in tpl[0]['transfers']] == [('0xf2ba0e', -1, 1), *expected], 'trace template geometry')
        take = {'0x1537acc','0x1537af3'} | ({'0x1537a87'} if a == 'server' else {'0x153781b'})
        req(set(tpl[0]['taken_conditions']) == take, 'branch outcomes on observed path')
        req(all(unpack_from('<I', r, s-13)[0] < 10000001 for r in rows), 'identity comparator taken')
        req(all(v['taken'] == (449 if k in take else 0) and
                v['fallthrough'] == (0 if (a == 'client' and 0x153781b < int(k,16) <= 0x1537a87) or k in take else 449)
                for k,v in d['branch_outcomes'].items()), 'branch visit counts')
        decoded[a] = rows
    bodies = decoded['server']
    req(all(s[-12:] == t for s,t in zip(bodies, decoded['client'])), 'bulk byte-for-byte client/server')
    recorded = list(read_part(c['archives']['server']['rows'], 'rows'))
    req(len(recorded) == 449, 'trace row shard count')
    with (ROOT/'scratch/t13d/out/t22.csv').open(encoding='utf-8', newline='') as stream:
        csv_rows = list(csv.DictReader(stream))
    req(len(csv_rows) == 449, 'legacy CSV rows')
    for i, (b, r, csv_row) in enumerate(zip(bodies, recorded, csv_rows)):
        at = 14+i*79
        req(r == dict(ordinal=i, selector_start=at-1, body_start=at, body_end=at+78, trace_variant=0,
                      id_u32=[i,i+1,i+1], body_sha256=digest(b)), f'row {i} trace')
        req(int(csv_row['offset']) == at and bytes.fromhex(csv_row['raw_hex']) == b + payload['server'][at+78:at+79], 't13d row')
    dates = next(t['date_cols'] for t in json_at(ROOT/'scratch/t13d/out/audit.json')['tables'] if t['table_type'] == 22)
    for a in dates:
        cells = [unpack_from('<HH', b, a['u32_off']) for b in bodies]
        days, years = zip(*cells)
        req(min(years) == a['year_min'] and max(years) == a['year_max'] and len(set(years)) == a['year_distinct']
            and min(days) >= 1 and max(days) == a['day_max'] and a['ratio_of_live'] == 1.0, 't13d packed date profile')
    live = [x for b in bodies if (x := unpack_from('<I',b)[0]) != 0xffffffff]
    req((len(live), len(set(live)), min(live), max(live)) == (361,310,86,82403), 'unnamed +0 reference')
    stadium = db.load_payload(codec,'client',21)
    req(len(stadium) == 14+48413*38+8 and all(unpack_from('<I', stadium, 14+i*38+25)[0] == i for i in range(48413)), 'reference target ordinal domain')
    master = json_at(ROOT/'evidence/fm24/reports/editor_schema/master.json')
    schema = next(x for x in master['entities']['club.xml'][0]['fields'] if x['field'] == 'Cstc')['list_item_fields']
    fields = list(read_part(f['fields'], 'fields'))
    req([(int(x['file_offset'],16),x['wire_offset'],x['width'],x['object_off']) for x in fields] == list(LAYOUT), 'ledger join')
    named = {}
    held = {}
    for x in fields:
        o, w, tag = x['wire_offset'], x['width'], x['candidate_code']
        req(transfers[int(x['file_offset'],16)]['site']['bytes'] == x['bytes'] and
            pe.va2f(int(x['VA'],16)) == int(x['file_offset'],16), 'ledger instruction bytes')
        cells = [b[o:o+w] for b in bodies]
        p = x['data_profile']
        req(p['n'] == len(cells) and p['distinct'] == len(set(cells))
            and all(p['sample_hex'][str(i)] == cells[i].hex() for i in (0,224,448)), f'{tag} samples')
        if not tag:
            req(x['row_offset'] is None and x['name'] is None, 'unnamed slots not promoted')
            continue
        occurrences = [s for s in schema if s['field'] == tag]
        req(occurrences == [{k:v for k,v in occ.items() if k != 'idx'} for occ in x['schema_occurrences']], 'schema join')
        for ev in x['getter']:
            cmp_i, jump_i = map(decode, ev['cmp_and_branch'])
            dst = decode(ev['access'])
            req(cmp_i.operands[1].imm == int.from_bytes(tag.encode(), 'big') and
                dst.operands[1].mem.disp == ev['object_off'], '4CC dispatch and object displacement')
            start = jump_i.operands[0].imm if jump_i.mnemonic == 'je' else jump_i.address+jump_i.size
            path = list(map(decode,ev['matched_path']))
            req(path[0].address == start and path[-1].address == dst.address, 'getter matched route')
            for i,j in zip(path,path[1:]):
                req(i.address+i.size == j.address or (i.mnemonic.startswith('j') and i.operands[0].imm == j.address), 'getter route edge')
        req({e['object_off'] for e in x['getter']} == ({x['object_off'],x['object_off']+2} if occurrences[0]['type']=='date' else {x['object_off']}), 'getter sink join')
        for r in x['getter_extra']:
            decode(r)
        matches = get_rule_count(master, cells, occurrences[0])
        req(matches == p['matches'], 'data profile count')
        if x['code']:
            req(len(occurrences) == 1 and matches == 449 and x['name'] == occurrences[0]['name']
                and x['code'] == tag and x['row_offset'] == o and x['grade'] == 'L3_named_row_coordinate', 'promotion gate')
            named[tag] = o
        else:
            req(x['row_offset'] is None and x['name'] is None and (matches < 449 or len(occurrences) > 1), 'unpromoted field')
            held[tag] = (o,matches)
    req(named == NAMED and held == HELD and len(named) == f['fields_named'] == 14
        and f['baseline_named'] == 0 and f['schema_occurrences'] == len(schema) == 28, 'named increment')
    req({(x['code'],x['t20_row_offset']) for x in f['negative_regressions']}
        == {('Scap',12),('Styp',16),('Sceb',50),('Salt',17)}, 't20 negative regressions')
    scout = json_at(OUT/'scout.json')['rows']
    req({(r['parent'],r['schema_fields'],r['table_id']) for r in scout if r['parent'] in ('Cafl','Cvfl')}
        == {('Cafl',29,None),('Cvfl',19,None)}, 'scout distinction')
    print('t27 verify PASS: 449 server + 449 client; 35 CFG blocks / 28 conditions; 14 L3 (+14), 6 held codes; 9B physical footer')


def selftest():
    h = bytes.fromhex('03017461642ef10d0100000000')
    b = b'\x00'+pack('<III',0,1,1)
    f = pack('<IBI',0,1,1)
    req(split(h+b+f,13) == (26,[b[1:]]), 'positive fixture')
    for bad in (h+b+f[:-1], h+b'\x01'+b[1:]+f, h+b[:-1]+b'\x01'+f):
        try:
            split(bad,13)
        except Reject:
            continue
        raise Reject('negative fixture accepted')
    print('t27 verify selftest PASS')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest', action='store_true', help='test header, framing and identity on synthetic rows')
    args = ap.parse_args()
    try:
        selftest() if args.selftest else verify()
        return 0
    except Reject as exc:
        print(f't27 verify FAIL: {exc}', file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, ImportError, RuntimeError, KeyError, IndexError, StopIteration) as exc:
        print(f't27 verify fatal: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
