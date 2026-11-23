#!/usr/bin/env python3
"""Offline Big-3 occurrence audit; only write scratch/t136/out (Python 3.12)."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from functools import cache
from hashlib import sha256
import json
from pathlib import Path
import re
import struct

import t112_fm24_reader as db
import t133_fm24_reader_v2 as wire
import t82_extra3_remaining as x3
import t53_crs_wire as x9
import t125_big3_gap_closure as v3

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t136/out'
OLD = 'scratch/t125/out/'
INDEX = 'scratch/t132/out/ida_hop2_index.json'
X9 = 'scratch/t53/out/discovery_crs_wire.json'
X3 = 'scratch/t82/out/field_map.json'
SPECIAL = 'scratch/t106/out/special_members_schema.json'
VERIFY = 'scratch/t133/out/reader_v2_verify.json'
ENTITIES = {'club': 433, 'nation': 346, 'comp': 255}
EX = 'excluded_non_db_l3'
ROUTE = 'L3_subtable_routed'
OWN = 'L3_unicorn_or_subobject_closed'
HEAD = bytes.fromhex('03017461642ef10d')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(b):
    return sha256(b).hexdigest()


@cache
def load(path):
    return json.loads((ROOT / path).read_bytes())


@cache
def lines(path):
    return (ROOT / path).read_text(encoding='utf-8').splitlines()


def save(name, data):
    if not isinstance(data, str):
        data = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    dest = OUT / name
    if dest.is_file() and dest.read_bytes() == data.encode('utf-8'):
        return
    tmp = dest.with_suffix(dest.suffix + '.tmp')
    tmp.write_text(data, encoding='utf-8', newline='\n')
    tmp.replace(dest)


def cpath(va, where=None):
    for base in ([where] if where else ['scratch/t124/out/funcs', 'scratch/t95/funcs', 'scratch/t133/out/static']):
        path = f'{base}/{va}.c'
        if (ROOT / path).is_file():
            return path
    raise FileNotFoundError(va)


def cite(path, n, expected=''):
    s = lines(path)[n-1].strip()
    require(expected in s, (path, n, expected, s))
    return dict(source_file=path, line_no=n, text=s)


def c(va, n, expected='', where=None):
    return cite(cpath(va, where), n, expected)


def pointer(path, p):
    item = load(path)
    for key in p.split('/')[1:]:
        k = key.replace('~1', '/').replace('~0', '~')
        item = item[int(k)] if isinstance(item, list) else item[k]
    return item


def artifact(path, p):
    pointer(path, p)
    return dict(artifact=path, pointer=p)


def insns(task, wanted):
    """Read and check already captured offline PE witnesses (file offsets)."""
    result = {}
    for f in sorted((ROOT / f'scratch/{task}/out').glob('instructions.part*.json')):
        path = f.relative_to(ROOT).as_posix()
        entries = load(path)
        for i, row in enumerate(entries if isinstance(entries, list) else entries['instructions']):
            address = row['file_offset']
            address = int(address, 0) if isinstance(address, str) else address
            if address in wanted:
                require(wanted[address] in row['instruction'], (task, address, row))
                binary = bytes.fromhex(row['bytes'])
                require(bool(binary) and v3.Engine.pe_bytes(address, len(binary)) == binary, (task, address, 'PE drift'))
                result[address] = dict(artifact=path, pointer=f'/{i}' if isinstance(entries, list) else f'/instructions/{i}', **row)
    require(result.keys() == wanted.keys(), (task, set(wanted) - set(result)))
    return list(result.values())


def named(archive, member):
    e = archive.entries[f'{archive.name}_db/{member}.dat']
    a = archive.data_base + e['offset']
    z = a + e['packed_size']
    obj_factory = db._zstd().ZstdDecompressor()
    hits = []
    tail = archive.data[a:z]
    while tail.startswith(db.ZSTD_MAGIC):
        obj = obj_factory.decompressobj()
        b = obj.decompress(tail)
        require(obj.eof and len(obj.unused_data) < len(tail), (member, 'incomplete frame'))
        tail = obj.unused_data
        if len(b) == e['size']:
            hits.append(b)
    require(len(hits) == 1 and hits[0].startswith(HEAD), (archive.name, member, 'frame'))
    return hits[0]


def aux9(b, side):
    """Sequential reader: no marker search. Names are UTF-8 lengths; ordinal is a check."""
    require(b[:8] == HEAD and struct.unpack_from('<I', b, 8)[0] == 251, 'extra9 header')
    q = x9.Span(b, 12, len(b), 0)
    rows = []
    for i in range(251):
        p = q.p
        q.row = i
        require(q.num(4, 0x3bb9748) == i, ('extra9 ordinal', side, i, p))
        lanes = {}

        def take(key, n, site):
            a = q.p
            q.take(n, site)
            lanes[key] = [a, q.p]

        def string(key, site):
            a = q.p
            q.string(site).decode('utf-8')
            lanes[key] = [a, q.p]

        string('name90', 0x11d34ab)
        take('word_ae', 2, 0x11d358e)
        string('hashtag98', 0x11d35c7)
        a = q.p
        count = q.count(1, 0x11d365d, 27)
        kit_buckets = Counter()
        for _ in range(count):
            raw = q.take(27, 0x11d38b3)
            require(raw[0] == 1, ('extra9 kit selector', raw[0]))
            kit_buckets[f'{raw[23]}:{int(bool(raw[26]))}'] += 1
        lanes['kits78'] = [a, q.p]
        take('colour_a8', 4, 0x11d3f72)
        take('colour_a0', 4, 0x11d4062)
        base_end = q.p
        vec = None
        typed = []
        if side == 'server':
            for key, w, stride, site in [('vec18', 2, 20, 0x11d41ca), ('vec30', 1, 6, 0x11d44a5)]:
                a = q.p
                n = q.count(w, site, stride, True)
                q.take(n * stride, site)
                lanes[key] = [a, q.p]
            for j in range(4):
                take(f'formation{0x74+j:x}', 1, 0x11d4765)
            for j in range(3):
                take(f'attendance{0x68+4*j:x}', 4, 0x11d47de)
            for _ in range(q.count(2, 0x11d4866, 37)):
                a = q.p
                require(q.num(1, 0x11d494d) == 9, ('unreduced extra9 polymorphic tag', i, a))
                q.take(20, 0x42dba7a)
                for _ in range(4):
                    q.string(0x42dbb34)
                typed.append([a, q.p])
            a = q.p
            flag = q.num(1, 0x11d4b5a)
            require(flag in (0, 1), ('extra9 TCrs gate', i))
            if flag:
                vec = x9.observed(q)
            lanes['TCrs'] = [a, q.p]
        rows.append(dict(row=i, start=p, end=q.p, sha256=digest(b[p:q.p]), base_end=base_end, lanes=lanes,
                         kits=count, kit_buckets=dict(kit_buckets), typed_records=typed, responsibility_items=0 if vec is None else vec['count']))
    require(q.p == len(b), ('extra9 EOF', side, q.p, len(b)))
    return rows


def comp_wage_profile(raw):
    end = len(raw)-9
    p = 13
    start = wire.compile_walk(wire.COMP[:35])
    stop = wire.compile_walk(wire.COMP[:36])
    walk = wire.compile_walk(wire.COMP)
    result = {}
    owners = 0
    for i in range(7047):
        q = start(raw,p+1,end)
        marker = raw[q]
        q += 1
        require(marker in (0,1), ('wage gate',i,marker))
        if marker:
            owners += 1
            q += 1  # leading tag; reader does not branch on its value
            n = struct.unpack_from('<I',raw,q)[0]
            q += 4
            for _ in range(n):
                _, group, m = struct.unpack_from('<BBI',raw,q)
                q += 6
                for _ in range(m):
                    _, sub, _, _, low, high = struct.unpack_from('<BBBBii',raw,q)
                    profile = result.setdefault(f'{group}:{sub}',dict(low=Counter(),high=Counter(),first=None))
                    profile['low'][low] += 1
                    profile['high'][high] += 1
                    if low != -1 and profile['first'] is None:
                        profile['first'] = dict(row=i,offset=q+4,raw=raw[q+4:q+8].hex(),value=low)
                    q += 12
        require(q == stop(raw,p+1,end), ('wage block end',i,q))
        p = walk(raw,p+1,end)
    require(p == end and owners == 315, 'wage profile footer/count')
    return dict(owners=owners,by_key=result)


def team_profiles(raw):
    ordinals, uids, people = x9.people(ROOT/'scratch/data')  # identity only, no PDxx
    end = len(raw)-9
    p = 13
    walkers = {k:wire.compile_walk(v) for k,v in wire.SELECTORS['server',24].items()}
    result = {sel:dict(rep=Counter(), captain=Counter(), vice=Counter(), first={}) for sel in walkers}
    roles = {'captain':0,'vice':4}
    for i in range(84507):
        flag = raw[p]
        j = p+1
        if flag == 11:
            j += 49+10*raw[j+48]
        n = struct.unpack_from('<H',raw,j+33)[0]
        lane = j+35+4*n
        r = result[flag]
        rep = struct.unpack_from('<h',raw,j+2)[0]
        r['rep'][rep] += 1
        for role, d in roles.items():
            v = struct.unpack_from('<i',raw,lane+d)[0]
            r[role]['null' if v == -1 else 'live'] += 1
            if v != -1:
                r[role]['ordinal_hits'] += v in ordinals
                r[role]['uid_hits'] += v in uids
                r['first'].setdefault(role,dict(row=i,offset=lane+d,raw=raw[lane+d:lane+d+4].hex(),value=v))
        p = walkers[flag](raw,p+1,end)
    require(p == end and sum(result[11]['rep'].values()) == 251, 'TEAM profile footer/count')
    return dict(by_selector=result,person_identity_fixture=people)


def numeric(archives):
    verify = load(VERIFY)
    traces, specs = wire.registry(load('scratch/t121/out/wire_traces_79of79.json'))
    l3 = db.load_l3()
    wanted = {3, 9, 10, 24, 25, 29, 32, 33, 34, 36, 37, 45, 48, 71, 72}
    info = {}
    for label, src in verify['tables'].items():
        key = (src['archive'], src['table_id'])
        if key[1] not in wanted:
            continue
        spec = specs[key]
        raw = archives[key[0]].payload(key[1])
        result = wire.verify_table(spec, traces[key], l3, raw, samples=1)
        keys = ('rows_decoded', 'rows_header', 'footer_closed', 'footer_off', 'footer9_hex', 'flags_seen')
        require(result['footer_closed'] and all(result[k] == src[k] for k in keys), ('numeric', key, result['error']))
        info[label] = dict({k: result[k] for k in keys}, **artifact(VERIFY, f'/tables/{label.replace("/", "~1")}'),
                           payload_sha256=digest(raw))
        if key == ('server',25):
            info[label]['wage_profile'] = comp_wage_profile(raw)
        if key == ('server',24):
            info[label]['team_profiles'] = team_profiles(raw)
    return info


def archive_audit():
    archives = {s: db.Archive(s) for s in ('client', 'server')}
    require(all(a.path.resolve() == (ROOT / 'scratch/data' / f'{s}_db.dat').resolve() for s, a in archives.items()), 'use the checked-in fixture paths')
    extra = {}
    for s, a in archives.items():
        b = named(a, 'table_extra_9')
        rows = aux9(b, s)
        prior = load(f'scratch/t53/out/cursor_crs_extra_{s}.json')
        require(prior['payload_sha256'] == digest(b) and len(prior['rows']) == len(rows), ('extra9 base', s))
        for r, p in zip(rows, prior['rows'], strict=True):
            require((r['start'], r['end'], r['base_end'], r['sha256']) == (p['start'], p['end'], p['base_end'], p['row_sha256']), ('extra9 layout', s, r['row']))
        profiles = {}
        for key in rows[-1]['lanes']:
            vals = [(r['row'], *r['lanes'][key]) for r in rows]
            i, lo, hi = vals[0]
            profile = dict(first=dict(row=i, offset=lo, width=hi-lo, raw=b[lo:min(lo+40,hi)].hex()),
                           distinct=len({b[lo:hi] for _,lo,hi in vals}), widths=dict(sorted(Counter(hi-lo for _,lo,hi in vals).items())))
            if key.startswith(('formation', 'attendance')):
                profile['signed_values'] = dict(sorted(Counter(int.from_bytes(b[lo:hi], 'little', signed=True) for _,lo,hi in vals).items()))
            profiles[key] = profile
        extra[s + '/extra_9'] = dict(bytes=len(b), payload_sha256=digest(b), rows=rows, header=12, footer=0,
                                      kits=sum(r['kits'] for r in rows), typed_records=sum(len(r['typed_records']) for r in rows),
                                      responsibility_items=sum(r['responsibility_items'] for r in rows), profiles=profiles)
        d3 = x3.replay_table_extra_3(named(a, 'table_extra_3'), s == 'server')
        require(d3['rows'] == 84259, ('extra3 rows', s))
        require(len(d3['tcht_map']) > 1 and d3['tcht_bad_utf8'] == 0, ('extra3 hashtag', s))
        profiles3 = {k: dict(sorted(Counter(int(v) for v in d3[k]).items()))
                     for k in ('base_a0', 'base_a8', 'CScP', 'Cown', 'Chti', 'Cepr', 'Csth', 'Cpfr', 'C2pf', 'Cdfo', 'Cafo') if k in d3}
        extra[s + '/extra_3'] = dict(bytes=d3['bytes'], rows=d3['rows'], payload_sha256=d3['stream_sha256'],
                                     kits=d3['kit_total'], kit_buckets={f'{k[0]}:{k[1]}': v for k,v in d3['kit_buckets'].items()},
                                     tagged_records=dict(d3.get('b0_tags', {})), profiles=profiles3)
    b = named(archives['server'], 'table_extra_24')
    n = struct.unpack_from('<I', b, 8)[0]
    require(n == 84507 and len(b) == 12 + 82*n and all(struct.unpack_from('<I', b, 12 + 82*i)[0] == i for i in range(n)), 'extra24 framing')
    extra['server/extra_24'] = dict(bytes=len(b), rows=n, stride=82, payload_sha256=digest(b))
    special = load(SPECIAL)
    members = special['members']
    require(special['all_closed'] and special['members_closed'] == len(members) == 13, 'special inventory')
    a = archives['server']
    b = named(a, 'club_links')
    n = struct.unpack_from('<I', b, 8)[0]
    require(n == 9261 and len(b) == 12 + 47*n, 'club links framing')
    require('client_db/club_links.dat' not in archives['client'].entries, 'club links client')
    require(all(struct.unpack_from('<I', b, 12 + 47*i + j)[0] < 84259 for i in range(n) for j in (0, 9)), 'club links ordinal domain')
    require(load('scratch/t44/out/discovery_cafl_cvfl.json')['archives']['server']['payload_sha256'] == digest(b), 'club links match t44')
    extra['server/club_links'] = dict(bytes=len(b), rows=n, stride=47, payload_sha256=digest(b))
    return dict(schema_id='fm24.t136.archive_audit', numeric=numeric(archives), auxiliary=extra,
                special_schema=SPECIAL, special_members=list(members) if isinstance(members, dict) else [x['member'] for x in members])


# Each entry names the start of the feeder slice for the t125 boxing-site hit;
# the shared tail or lookups are retained separately from the copied operand.
BOX_START = {
    'club': {10: 4124, 24: 1085, 25: 1014, 34: 3980, 47: 1641, 55: 1274,
             70: 2828, 71: 2814, 72: 2700, 73: 2732, 74: 2932, 75: 2908, 76: 1085, 77: 1014,
             78: 2760, 79: 2714, 80: 2982, 81: 2967, 109: 1465, 110: 1437, 111: 1451,
             112: 1410, 146: 3296, 147: 521},
    'nation': {6: 1122, 9: 327, 10: 1561, 18: 1085, 19: 1014, 23: 1454, 24: 1489,
               25: 1497, 68: 1530, 69: 1666, 70: 1144, 71: 662},
    'comp': {13: 3703, 14: 3499}}
BOX_SOURCE = {
    'club': {10: 4134, 24: 1086, 25: 1016, 34: 3984, 47: 1645, 55: 1305, 70: 2834, 71: 2820,
             72: 2707, 73: 2739, 74: 2945, 75: 2921, 76: 1086, 77: 1016, 78: 2767, 79: 2721,
             80: 2988, 81: 2973, 109: 1473, 110: 1445, 111: 1456, 112: 1415, 146: 3310, 147: 3310},
    'nation': {6: 1132, 9: 340, 10: 1608, 18: 1086, 19: 1016, 23: 1455, 24: 1491, 25: 1499,
               68: 1534, 69: 1670, 70: 1148, 71: 666},
    'comp': {13: 3706, 14: 3502}}
HOPS = {
    '0x14083dfa0': ([6,8,9,10,11,12,13], 'Move-assign boxed value; virtual destroy of old target, copy two words, reset source. No archive input.'),
    '0x1411eacb0': ([23,27,30,31,36,97,100,101,102], 'Find/create a polymorphic item by tag and two virtual keys in receiver+176, not a scalar read.'),
    '0x144026350': ([1,4597,4614,4626,4637,4638], 'Decompiler recovers containing CLUB getter entry. An interior/shared JUMPOUT is not a receiver-correct independent callee; recorded incoming branch still needs a tail/target join.'),
    '0x1407e4490': ([13,20,27,40,46], 'Allocation path; no original name or tax data supplied by this helper.'),
    '0x14083b0a0': ([17,24,43,57,77], 'Variant/vector teardown; no archive input.'),
    '0x14083db80': ([15,22,28,29,30,32,34], 'Build variant from range/collection; source remains the caller vector.'),
    '0x140e58670': ([11,15,30,36,55,62], 'Queued callback/deferred bookkeeping around ownership mutation, not a serialized byte.'),
    '0x140e5f8c0': ([3,7,19,22], 'TLS-backed initialization around ownership mutation, not wire input.'),
    '0x140fc9d50': ([7,8,13,16,18], 'Clamp and assign TEAM reputation at +168 through guarded mutation.'),
    '0x141078de0': ([31,40,76,90,134,146,165,189], 'Structured editor command for wage vector (selectors, element lookup/change, clear); trace wrapped vector back through 1415d1d00.'),
    '0x141521aa0': ([14,27,29,32,38], 'Election-related validation invoked on Cown change; not the Cown getter operand.')}


def hop_audit(gaps):
    prior = gaps['priority_undecompiled']
    seen = {}
    for r in load(INDEX)['records']:
        va = r['input_va']
        if va not in HOPS:
            continue
        path = r['file'].replace('\\', '/')
        witnesses, role = HOPS[va]
        require(r['ok'] and len(lines(path)) == r['lines'], (va, r))
        seen[va] = dict(input_va=va, real_va=r['real_va'], path=path, lines=r['lines'],
                        sha256=digest((ROOT / path).read_bytes()), role=role,
                        citations=[cite(path, i) for i in witnesses])
    require(set(seen) == set(HOPS) == {p['va'] for p in prior}, 'missing second hop')
    result = {}
    for row in gaps['rows']:
        key = row['id']
        local = {x['va']: x for x in row['next_hops'] if x['va'] in seen}
        result[key] = dict(second_hops=list(local))
        for h in local.values():
            if h['site']:
                s = h['site']
                cite(s['source_file'], s['line_no'], s['text'])
        if '0x14083dfa0' not in local:
            continue
        entity, i = row['entity'], int(key[-3:])
        site = local['0x14083dfa0']['site']
        path, end = site['source_file'], site['line_no']
        start = BOX_START[entity][i]
        source = BOX_SOURCE[entity][i]
        require(start <= source < end, (key, start, source, end))
        if entity == 'club' and i == 147:
            selected = [*range(start, 528), *range(3308, end+1)]
        else:
            selected = range(start, end+1)
        helper = {'ttcl':cs('1411de680',20,21,22,24), 'tbcl':cs('1411de560',25,26,37,40)}.get(row['code'], []) if row['code'] in ('ttcl','tbcl') else []
        result[key]['boxing'] = dict(operand=cite(path, source), call=cite(path, end, 'sub_14083DFA0('),
                                      slice=[cite(path, n) for n in selected if lines(path)[n-1].strip()],
                                      producer_citations=helper)
    require(sum('boxing' in x for x in result.values()) == 38, '38 boxing paths')
    for p in prior:
        require([k for k, x in result.items() if p['va'] in x['second_hops']] == p['ids'], p['va'])
    return dict(schema_id='fm24.t136.hop_audit', functions=seen, gaps=result)


MASTER = 'evidence/fm24/reports/editor_schema/master.json'
START45 = 'scratch/t98/out/table45_full_schema.json'
START48 = 'scratch/t98/out/table48_comparison.json'
T47 = 'scratch/t47/out/discovery_nation_unknown.json'
T44 = 'scratch/t44/out/discovery_cafl_cvfl.json'
T63 = 'scratch/t63/out/field_map_r2.json'
TEAM = 'scratch/t133/out/team_field_map_check.json'


def fourcc(tag):
    return str(int.from_bytes(tag.encode('ascii'), 'big'))


def cs(va, *ns):
    return [c(va, n) for n in ns]


def proof(kind, target, reason, cites=(), refs=(), **extra):
    require(cites or refs, (kind, target, reason))
    return dict(classification=kind, target_table=target, reason=reason,
                citations=list(cites), artifacts=list(refs), **extra)


def extra9_rules(archive):
    checks = insns('t53', {0x3bb9748: 'call qword ptr [rax + 0x28]', 0x11d349d: '[rdi + 0x90]',
                          0x11d35b9: '[rdi + 0x98]', 0x11d3f5f: '[r15 + 0xab]', 0x11d3fc7: '[r15 + 0xa8]',
                          0x11d3fef: '[r15 + 0xa3]', 0x11d404b: '[r15 + 0xa0]', 0x11d4736: '[r13 + 0x74]',
                          0x11d478c: '[rax + 0x68]', 0x11d47e8: '0xc', 0x11d4b5a: 'call 0x1412e70a0'})
    a = archive['auxiliary']
    ref = artifact(X9, '/TCrs/evidence_table/getter_extension')
    require(pointer(X9, ref['pointer'])['owner_path'] == [176, 72], 'extra9 owner')
    out = {}
    for i, lane, off, width, vv, get in [
        (9, 'name90', 144, None, '1410668f0', [327,328,329,330,337,340]),
        (18, 'colour_a0', 160, 4, '1411de680', [20,21,22,24]),
        (19, 'colour_a8', 168, 4, '1411de560', [25,26,31,37]),
        (23, 'attendance68', 104, 4, '1411f1090', [1454,1455]),
        (24, 'attendance6c', 108, 4, '1411f1090', [1489,1491]),
        (25, 'attendance70', 112, 4, '1411f1090', [1497,1499])]:
        tag = load(MASTER)['entities']['nation.xml'][0]['fields'][i]
        profiles = {s: a[s+'/extra_9']['profiles'][lane] for s in ('client','server') if lane in a[s+'/extra_9']['profiles']}
        require(all(p['distinct'] > 1 for p in profiles.values()), ('extra9 live lane', i))
        if tag['type'] == 'integer':
            require(set(profiles) == {'server'} and all(int(tag['min_value']) <= int(n) <= int(tag['max_value'])
                    for n in profiles['server']['signed_values']), ('attendance domain', tag))
        detail = 'This is the persisted override; getter can instead select a kit/fallback.' if tag['type'] == 'colour' else 'The getter and verified named-member reader use the same extension leaf.'
        out[i] = proof(ROUTE, 'table_extra_9', detail, cs(vv, *get), [ref],
                       object_path=[176,off], wire_width=width, lane=lane, profiles=profiles, pe=checks,
                       encoding='u32 length + UTF-8' if i == 9 else ('reversed RGBA bytes' if width == 4 and tag['type'] == 'colour' else 'i32 LE'))
    require(a['server/extra_9']['responsibility_items'] == 76 and a['client/extra_9']['responsibility_items'] == 0, 'extra9 responsibility witness')
    out[64] = proof(ROUTE, 'table_extra_9', 'Correct prior non-DB exclusion: t53 proves the getter uses the auxiliary +72 vector, distinct from the table_9 +392 vector. Parent only; no nested field promotion.',
                    cs('1411f1090',789,791,792), [ref, artifact(X9, '/TCrs/evidence_table/main')],
                    pe=checks, object_path=[176,72], server_items=76, client_mode='bypassed')
    return out


def record_rules(engine, archive):
    result = defaultdict(dict)
    # The integer in each entry is a scope index, not a wire offset.
    routes = {'club': {
        216: ('CBDo', 9, 'otht', '1411f4f70', [308,309,310,1089,1090,1091]),
        226: ('CHLo', 30, 'otht', '140e834a0', [605,606,607,608,609,644,645,646]),
        259: ('CMAp', 1, 'stid', '140e834a0', [559,561,562,563,564,874]),
        263: ('CMGn', 2, 'stnm', '140e834a0', [514,516,517,518,874]),
        264: ('CMGg', 2, 'gols', '140e834a0', [506,508,509,510,874]),
        265: ('CMOp', 22, 'stid', '140e834a0', [480,482,483,484,874]),
        266: ('CMOn', 22, 'stnm', '140e834a0', [472,474,475,476,874]),
        267: ('CMOg', 22, 'gols', '140e834a0', [499,501,502,503,874]),
        310: ('CGLo', 21, 'otht', '140e834a0', [774,775,776,777,644,645,646]),
        320: ('CHFs', 5, 'otht', '140e834a0', [818,819,820,821,644,645,646])},
        'nation': {88: ('CBDo',9,'otht','1411f4f70',[308,309,310,1089,1090,1091]),
                   201: ('NMEb',31,'otht','141063f30',[2010,2011,2012,2013,2038])}}
    cols = load(START45)['physical_columns']
    direct = load(START45)['direct_starting_record_4cc']
    counts = engine.record_keys[45]
    require(archive['numeric']['server/45']['payload_sha256'] == load(START45)['table_45']['sha256'], 'starting record fixture')
    for entity, group in routes.items():
        for idx, (tag, typ, inner, func, ns) in group.items():
            branch = cs(func, *ns)
            require(fourcc(tag) in branch[0]['text'], ('outer tag', entity, tag, branch[0]))
            require(any(f' = {typ};' in x['text'] for x in branch), ('record type', entity, tag))
            require(any(f' = {fourcc(inner)};' in x['text'] for x in branch), ('inner tag', entity, tag))
            require(any('sub_1411E9540(' in x['text'] for x in branch), ('record sink', tag, branch))
            owner = '3' if entity == 'club' else '9'
            require(counts[typ][owner] > counts[typ]['25'], ('record owner, even subtracting every possible COMP overlap', tag))
            j, d = next((j, d) for j,d in enumerate(direct) if d['tag'] == inner)
            k, col = next((k, col) for k,col in enumerate(cols) if col['id'] == d['physical_col'])
            readfile, n = col['read_source'].rsplit(':',1)
            outer = [c('144026550', 10, 'a1 + 12'), c('144026550', 11, '141B60190'),
                     c('144026550', 17, '+ 94'), c('144026550', 18, 'sub_141545680')]
            result[entity][idx] = proof(ROUTE, 45, 'Outer tag selects constant record type and inner tag; keyed persistence confirmed with parent UID and opposite-table control. Leaf coordinates are STARTING_RECORD-relative.',
                                         branch+outer+[cite(readfile, int(n))]+cs('1415446a0', *d['get']),
                                         [artifact(START45,f'/direct_starting_record_4cc/{j}'), artifact(START45,f'/physical_columns/{k}')],
                                         code=tag, rec_type=typ, inner_tag=inner, mem_off=col['mem_off'], wire_width=col['wire_width'],
                                         physical_column=col, key_controls=dict(counts[typ]), factory=engine.factory_anchor(45))
    return result


def collection_rules(archive):
    result = {}
    for i, tag, off, child, items, samples in [(225,'Nctp',264,'cont',640,[1144,1150,1151,1159]),
                                  (226,'Nrtp',288,'regi',254,[1163,1169,1170,1178]),
                                  (229,'NWGv',1088,'valu',2280,[1427,1435])]:
        p = f'scratch/t49/out/fields_{tag}.json'
        data = load(p)
        require(data['fields'][child]['grade'] == 'L3' and data['archives']['server']['wire_items'] == items, ('t9 lane', tag))
        src = load('scratch/t49/out/discovery_t9_wire.json')['archives']
        for side in ('client','server'):
            require(archive['numeric'][side+'/9']['payload_sha256'] == src[side]['members']['table_9.dat']['payload_sha256'], ('t49 fixture', side))
        get = cs('1410668f0', 654,658,564,565) + cs('1415d1d00',51,52,55,59) if i == 229 else []
        result[i] = proof(OWN, 9, 'Persisted collection parent in the NTC receiver, not a scalar or a separate table. Unresolved item fields do not inherit this grade.',
                          get+cs('14105d510',*samples), [artifact(T47,'/parents/'+tag),artifact(p,'/fields/'+child),artifact(p,'/archives')],
                          code=tag, mem_off=off, wire_width=None, item_stride=data['item_stride'], server_items=items)
    tax = pointer(T47, '/parents/Ntxr')
    require(tax['status'] == 'cursor_closed' and tax['item_count'] == 1899 and tax['schema_index'] == 232, 'tax vectors')
    result[232] = proof(OWN,10,'Table_10 outer NATION tax-rule vector, distinct from the NTC and both auxiliary name lanes. Server only; not a claim about all nested tax items.',
                        cs('141042940',633),[artifact(T47,'/parents/Ntxr')],code='Ntxr',mem_off=96,wire_width=None,server_items=1899)
    return result


def kit_rules(archive):
    result = defaultdict(dict)
    records = {r['xml_index']:(j,r) for j,r in enumerate(load(X3)['fields'])}
    a = archive['auxiliary']
    # Parent identity and filter are independently provable; do not grade
    # any internal lane of the 27-byte item as a schema occurrence.
    pe = insns('t53',{0x11d35b9:'[rdi + 0x98]',0x11d365d:'call'})
    for entity, base, member in [('club',178,'extra_3'),('nation',77,'extra_9')]:
        for k in range(5):
            i = base+k
            j,r = records[178+k]
            d = r['domain']
            code = r['code']
            require(schema(entity)[i]['field'] == code and 'list_item_fields' not in schema(entity)[i], ('kit scope',entity,i))
            bucket = f"{d['kit_type_b22']}:{d['outfield_b25']}"
            prof = {}
            for side in ('client','server'):
                arc = a[side+'/'+member]
                counts = Counter(arc.get('kit_buckets',{}))
                if member == 'extra_9':
                    for row in arc['rows']:
                        counts.update(row['kit_buckets'])
                require(sum(counts.values()) == arc['kits'] and counts[bucket] > 0, ('kit archive',entity,side,i))
                if entity == 'club':
                    require(d['items'] == counts[bucket], ('kit t82 filter',i))
                prof[side] = dict(count=counts[bucket],total=arc['kits'])
            require(prof['client'] == prof['server'], ('kit modes',entity,i))
            for x in r['static_chain'].values():
                if isinstance(x,dict) and {'bytes','file_offset'} <= x.keys():
                    raw = bytes.fromhex(x['bytes'])
                    require(v3.Engine.pe_bytes(int(x['file_offset'],0),len(raw)) == raw, ('kit static chain',i))
            result[entity][i] = proof(ROUTE,'table_'+member,'Persisted filtered TEAM_KIT_FOR_YEAR parent view, with nonempty exact buckets in both archives. No nested field is named or graded.',
                refs=[artifact(X3,f'/fields/{j}')]+([artifact(X9,'/TCrs/evidence_table/getter_extension')] if entity=='nation' else []),
                code=code,object_path=[176,120],item_stride=27,filter=dict(type=d['kit_type_b22'],outfield=d['outfield_b25']),profiles=prof,
                reader_pe=pe if entity=='nation' else [])
    return result


def team_rules(archive):
    profiles = archive['numeric']['server/24']['team_profiles']['by_selector']
    require(pointer(TEAM,'/table_24/rows_compared') == 84507 and pointer(TEAM,'/table_24/diff') == 0,'t79 TEAM walk')
    result = defaultdict(dict)
    require(all(0 <= k <= 10000 for k in profiles[11]['rep']), 'Nrep scoped integer bounds')
    result['nation'][22] = proof(ROUTE,24,'Nrep reads first TEAM+168, falling back to 1500 without a team. Reader normalizes raw zero reputation to 1; boxed reputation is not written to NTC+24.',
                                 cs('1410668f0',1565,1567,1568,1569,1573)+cs('1411a1280',39,40,41),[artifact(TEAM,'/table_24/team_offsets/Trep')],
                                 code='Nrep',object_path=[24,168],wire_width=2,body_offset=2,raw_histogram=profiles[11]['rep'])
    for entity,i,code,role,sel,off,outer,inner,read,fix in [
        ('nation',73,'Tcap','captain',11,136,1392,1164,94,90),
        ('nation',74,'Tvcp','vice',11,144,1163,692,98,92),
        ('club',189,'Tvcp','vice',10,144,1163,692,98,92)]:
        profile = profiles[sel][role]
        require(profile['ordinal_hits'] == profile['live'] > profile['uid_hits'] and profile['live']+profile['null'] == sum(profiles[sel]['rep'].values()), ('TEAM person ordinal domain',entity,code,profile))
        query = c('1411f1090',outer,fourcc(code))
        dispatch = cs('1411f1090', *(range(1394,1397) if role=='captain' else range(1215,1218)))
        require(any('sub_1411F4BD0(v57, 0, v58, v7)' in s['text'] for s in dispatch), ('first team forwarding',entity,code))
        result[entity][i] = proof(ROUTE,24,'Primary TEAM virtual property forwarding; stored signed ordinal with -1 null, fixed up to a person handle. Live ordinals independently validated against basic_people_db identities.',
                        [query]+dispatch+cs('1411f4bd0',11,22,33,35)+[c('1411b01b0',inner,fourcc(code)),c('1411b01b0',inner+(6 if role=='captain' else 2),f'a1 + {off}'),
                           c('1411a1280',read,f'a1 + {off}, 4'),c('1411a1640',fix,f'a1 + {off}')],
                        [artifact(TEAM,'/table_24')],code=code,object_path=[24,off],wire_width=4,
                        wire_offset_expression='TEAM body + 35 + 4*squad_count'+(' + 4' if role=='vice' else ''),profile=profile,first=profiles[sel]['first'][role])
    return result


def wages(archive):
    result = {}
    profiles = archive['numeric']['server/25']['wage_profile']['by_key']
    for i,code,g,k,gate in [(83,'ssCi',2,6,4200),(85,'syCi',3,7,4188),(87,'sfMi',1,8,4245),
                             (89,'ssMi',2,9,4191),(91,'syMi',3,10,4183),(93,'sfSi',1,11,4203)]:
        row = schema('comp')[i]
        p = profiles[f'{g}:{k}']
        observed = {val:n for val,n in p['low'].items() if val != -1}
        require(row['field']==code and observed and all(int(row['min_value']) <= v <= int(row['max_value']) for v in observed), ('COMP wages',i))
        result[i] = proof(OWN,25,'COMP+192 optional grouped wage table: select outer +24 group, inner +8 subtype and +4 minimum. -1 is the getter suppression sentinel, not a live wage.',
            [c('140ec0a60',gate,fourcc(code))]+cs('140ec0a60',4116,4123,4131,4150,4152,4161,4215,4229,4266,4269)+
            cs('140eb7a00',361,371,372)+cs('14155d840',10,12)+cs('14155da10',201,287,297),
            code=code,object_path=[192],group=g,subtype=k,element_mem_off=4,wire_width=4,wire_offset_from_item=4,
            raw_histogram=p['low'],first=p['first'])
    return result


def rules(archive):
    engine = v3.Engine()
    result = record_rules(engine, archive)
    result['nation'].update(extra9_rules(archive))
    result['nation'].update(collection_rules(archive))
    club, nation, comp = (result[s] for s in ENTITIES)
    for group in (kit_rules(archive),team_rules(archive)):
        for e, subset in group.items():
            require(result[e].keys().isdisjoint(subset), ('rule collision',e))
            result[e].update(subset)
    comp.update(wages(archive))
    for j,r in enumerate(load(X3)['fields']):
        i = r['xml_index']
        if i not in (*range(70,76),*range(78,82)):
            continue
        require(r['first_counterexample']['kind']=='derived_read_only_no_setter' and r['domain']['setter_exists'] is False, ('kit derived projection',i))
        club[i] = proof(EX,None,'Read-only colour projection through parent-club lookup, kit search and contrast/palette helpers. Only inputs are persisted; the boxed projected result has no standalone serialized slot.',
                        cs('140e8a400',BOX_START['club'][i],BOX_SOURCE['club'][i]),[artifact(X3,f'/fields/{j}')],code=r['code'])
    p59 = 'scratch/t59/out/field_map.json'
    contract = pointer(p59,'/fields/75')
    require(contract['code']=='Pchd' and contract['status']=='L3' and contract['lane']==13 and
            all(r['live']==7047 and r['violations']==0 for r in contract['domain_profiles'].values()), 'Pchd scoped enum')
    comp[75] = proof(OWN,25,'COMP contract status byte +406. Helper reads +393+13; legacy tags synthesize the byte, modern tags transfer it. Both archive profiles validate against cnst.',
                     cs('140ec0a60',3026,3030)+cs('14151ef00',418,420)+cs('140eb7a00',140)+cs('14151e110',17,32,34),
                     [artifact(p59,'/fields/75')],code='Pchd',mem_off=406,wire_width=1)
    for i, code in [(91,'Ccba'),(97,'Cesd'),(98,'Ceed'),(99,'Cead'),(100,'CteA'),(102,'Chaf'),(107,'Cmtp')]:
        j, r = next((j,r) for j,r in enumerate(load(T63)['fields']) if r['id'] == f'E97/club.xml#club/{i:03d}')
        require(r['code'] == code and r['grade'] == 'L3' and r['domain_profiles']['server']['violations'] == 0, ('t63 scope',i))
        # Legacy subtype-0 finance and adjacent projections are CLUB row data,
        # not offsets of the outer getter receiver or extra_3.
        w = r['wire']
        club[i] = proof(OWN,3,'Scoped getter-to-wire projection with live data in the t63 full walk and reverified t133 CLUB grammar. Client mode bypasses the relevant server projection.',
                       refs=[artifact(T63,f'/fields/{j}')],code=code,wire=w, first=r['domain_profiles']['server']['first'],
                       server_values=r['domain_profiles']['server']['values'])
    li = archive['auxiliary']['server/club_links']
    pe = insns('t44',{0xe8c1e8:'0x4376666c',0xe8c217:'call',0x15322f3:'0x118',0x15322fa:'0x120'})
    for i, tag, ns in [(209,'Cafl',[4509,4519,4520]),(210,'Cvfl',[2293,2295,2297,2298,2299])]:
        view = pointer(T44,'/views/'+tag)
        require(view['wire_storage'] == 'shared' and view['mode'] == i-209, ('link view',tag))
        club[i] = proof(ROUTE,'club_links','CLUB+280/+288 view of server-side CLUB_LINK records. The runtime validation wrapper is not another persisted table or field.',
                        cs('140e8a400',*ns),[artifact(T44,'/views/'+tag),artifact(T44,'/static_chain'),artifact(SPECIAL,'/members/club_links')],
                        code=tag,object_path=[280],item_stride=47,server_items=li['rows'],pe=pe)
    for i in (8,9,10,177):
        j, r = next((j,r) for j,r in enumerate(load(X3)['negative_not_extra3']) if r['xml_index'] == i)
        # This is more than a missing sink: the three name lanes are constructed
        # overrides; Crkt is dispatched as a mutation action with no stored value.
        if i == 177:
            require('0x' in r['reason'], r)
            club[i] = proof(EX,None,'Kit randomization is an editor action, not a stored boolean. The command can change persisted kits, not its own value.',
                            refs=[artifact(X3,f'/negative_not_extra3/{j}')], code=r['code'])
    for i, code, off, call_ln, reader_ln in [(13,'cbcl',292,3708,36),(14,'ctcl',296,3504,45)]:
        require(archive['numeric']['server/25']['rows_decoded'] == 7047, 'COMP corpus')
        comp[i] = proof(OWN,25,'COMP slot19 calls the RGB555 decoder on this+288. Boxed dword is the expanded RGBA destination, not a 4-byte raw wire field.',
                        cs('140ec0a60', call_ln-2, call_ln) + [c('140eb7a00',115,'sub_14150F650(a1 + 288'),
                        c('14150f650',reader_ln, 'a3: 2'), c('14150f650',reader_ln+6,f'a1[{off-288}]')],
                        code=code,mem_off=off,wire_width=2,wire_offset_from_row_body=3+2*((off-288)//4),encoding='RGB555 expanded to RGBA')
    # The NATION fallback is on the same receiver; this is not a foreign tag hit.
    nation[1] = proof(OWN,10,'Generic DATABASE_RECORD getter returns duni at this+12 on the NATION fallback. Common reader writes +8..+19; duni is the middle u32, not the ordinal.',
                      [c('141042940',1428,'sub_140FE3F20(v6, a2'),c('141042940',1431,'sub_140FE3F20(v6, a2'),
                       c('140fe3f20',405,fourcc('duni')),c('140fe3f20',412,'LABEL_105'),c('140fe3f20',570,'a1[3]'),
                       c('1410404c0',675,'sub_140FAED40'),c('140faed40',4,'sub_143DCB6F0'),c('143dcb6f0',20,'a1 + 8, 12')],
                      code='duni',mem_off=12,wire_width=4,identity_offset_from_row_end=-8)
    return result


@cache
def schema(entity):
    records = load(MASTER)['entities'][entity + '.xml']
    require(len(records) == 1 and len(records[0]['fields']) == ENTITIES[entity], entity)
    return records[0]['fields']


def cov(rows):
    by = Counter(r['new_class'] for r in rows)
    l3 = sum(n for k,n in by.items() if k.startswith('L3_'))
    n, ex = len(rows), by[EX]
    gaps = n-l3-ex
    require(gaps == sum(c for k,c in by.items() if k.startswith('gap_')), by)
    return dict(denominator=n,l3=l3,excluded_non_db=ex,gaps=gaps,net_denominator=n-ex,
                gross_pct=round(100*l3/n,4),net_pct=round(100*l3/(n-ex),4),by_class=dict(sorted(by.items())))


def blocked(g, h, archive):
    ent, i, tag = g['entity'], int(g['id'][-3:]), g['code']
    status, why, refs = 'await_receiver_to_sink', g['reason_t125'], []
    main = {'club':['client/3','server/3'], 'nation':['client/9','server/9','client/10','server/10'],
            'comp':['client/25','server/25']}[ent]
    if ent == 'nation':
        auxiliary = dict(status='no_receiver_to_named_member_join', member='table_extra_9')
        if i == 10:
            status, why = 'no_live_value', 'Getter takes [NTC+176]+152; both decoded hashtag98 string lanes contain only zero-length strings. No live binding promoted.'
            auxiliary.update(status=status, lane='hashtag98')
        elif 68 <= i <= 71:
            lane = f'formation{0x74+i-68:x}'
            enum = schema(ent)[i]['enum_ref']
            values = load(MASTER)['enums'][enum]['values']
            bad = sorted(set(map(int,archive['auxiliary']['server/extra_9']['profiles'][lane]['signed_values'])) - {int(r['enum_id']) for r in values} - {0})
            status = 'scoped_enum_conflict' if bad else 'enum_projection_unresolved'
            why = 'The boxing path loads the sidecar formation byte. A complete semantic mapping to the scoped editor enum is not proven.'
            auxiliary.update(status=status,lane=lane,enum_ref=enum,nonzero_out_of_domain=bad)
        elif 77 <= i <= 81:
            status, why = 'shared_kit_vector_child_scope_open', 'Selector-1 kit vector decodes on both sides; getter filter still needs an occurrence-specific semantic join. No child schema or extra9 leaf is inferred.'
            auxiliary.update(status=status,lane='kits78')
        elif i == 231:
            status, why = 'no_live_items', 'Table_9 server reads 251 presence flags, all zero. Need a live NCro item and its target join, not a synthetic substitute or attribution to extra9.'
            refs.append(artifact(T47,'/parents/NCro'))
        elif i in (7,8,11,12):
            why = 'Outer NATION/localization getter is not the NTC sidecar name90 or hashtag98 slot. Need the locale-key/pool-to-owner write path; string type is not proof.'
        elif i in (73,74,22):
            why = 'Requires first-team selection, actual TEAM property receiver and wire/reference validation; NTC +24 or a matching aux sidecar displacement is not the persisted leaf.'
    else:
        auxiliary = None
    if ent == 'club':
        field = next(((j,x) for j,x in enumerate(load(X3)['fields']) if x['xml_index'] == i),None)
        if field is not None and field[1]['grade'] == 'held':
            j,r = field
            status, why = 'held_domain_or_projection', r['hold_reason']
            refs.append(artifact(X3, f'/fields/{j}'))
        if i in (8,9,10):
            status, why = 'runtime_or_localized_source_open', 'CLUB extension name cache slots +0/+8/+16 are not read by the extra_3 reader; need other-loader/localization proof or complete runtime-only writer census.'
            j = next(j for j,r in enumerate(load(X3)['negative_not_extra3']) if r['xml_index'] == i)
            refs.append(artifact(X3, f'/negative_not_extra3/{j}'))
        if i == 193:
            why = 'Primary TEAM forwarding to Tsqi is identified, but the editor view needs the team squad vector/person reference join, not CLUB+24 as a wire scalar.'
    if ent == 'comp' and i == 96:
        profile = archive['numeric']['server/25']['wage_profile']['by_key']
        require('3:13' not in profile, 'unexpected new sySx witness')
        status, why = 'no_live_wage_subtype', 'Getter selects group 3, subtype 13, maximum at object +0. No 3:13 entry among the 315 server COMP wage containers.'
        refs.extend(cs('140ec0a60',4091,4116,4123,4144,4161,4179,4249))
    if ent == 'comp' and i in (194,195,196,197):
        typ = 36 if i <= 195 else 37
        require(str(typ) not in load(START48)['rec_type_profiles'], ('COMP record type', typ))
        status, why = 'no_live_keyed_record_type', f'Getter selects type {typ} through COMP STARTING_RECORD manager (table_48); no such record type in this payload. Do not substitute the same inner tag in table_45.'
        refs.append(artifact(START48,'/rec_type_profiles'))
    if ent == 'comp' and i in (135,136,138,139,140,141):
        status, why = 'assembled_view', 'Per-level result built from manager rows (sub_141563520/sub_140ECA610); no persisted scalar slot established. Need producer class, row join and exact output semantics before either route or exclusion.'
    if g['next_hops']:
        deps = g['next_hops']
    else:
        deps = g['reviewed_dispatch']
    require(deps or refs or g.get('getter_cite'), ('missing next evidence target',g['id']))
    return dict(status=status, blocker=why, sidecar9_check=auxiliary, source_candidates=deps,
                audited_hops=h['second_hops'], boxing=h.get('boxing'), verified_owner_members=main, artifacts=refs)


def text_report(s, gap, hops, archive):
    a = s['t136']
    report = ['# t136 — Big-3 持久化字段复核','',
        '| 阶段 | 毛覆盖 | 净覆盖 | 未闭合 |','|---|---:|---:|---:|',
        '| Baseline | 110/1,034 (10.6%) | — | — |']
    for t in ('t109','t125','t136'):
        d = s[t]
        report.append(f"| {t} | {d['l3']:,}/{d['denominator']:,} ({d['gross_pct']:.1f}%) | {d['l3']:,}/{d['net_denominator']:,} ({d['net_pct']:.1f}%) | {d['gaps']} |")
    report += ['', f"守恒：**1,034 = {a['l3']} L3 + {a['excluded_non_db']} 排除 + {a['gaps']} 缺口**。"
               + ('达到 85% 净覆盖目标。' if s['target_85_met'] else '未达到 85% 净覆盖；不以推定绑定或缩小分母凑数。'),
        '', '| 实体 | L3 | 排除 | 缺口 | 净覆盖 |','|---|---:|---:|---:|---:|']
    for ent in ENTITIES:
        d=s['per_entity'][ent]['t136']
        report.append(f"| {ent} | {d['l3']} | {d['excluded_non_db']} | {d['gaps']} | {d['net_pct']:.1f}% |")
    report += ['', '## 证据与口径', '',
        f"- `hop_audit_v4.json` 核对 {len(hops['functions'])}/11 个 t132 函数及 38/38 个装箱点的上游切片。装箱、析构、分配及修改回调不能单独证明持久化。",
        f"- `archive_audit_v4.json` 复跑 {len(archive['numeric'])} 个 numeric 成员；`table_extra_3` 双档各 84,259 行，`table_extra_24` 84,507×82 B，`club_links` server 9,261×47 B。未将特殊成员的同类数据当成字段绑定。",
        '- `table_extra_9` 双档各 251 行，从 12 B 头连续解到 EOF；client 83,927 B，server 105,228 B，无 footer。共同段为 ordinal、UTF-8 名、u16、UTF-8 hashtag、定长 kit 列表、两组 RGBA；server 再读两向量、4 阵型字节、3 个 attendance、tag-9 记录及独立 TCrs。保留每行跨度和 SHA-256；未套用 table_9 的数值成员 slot19。',
        '- 修正的 v3 排除均逐项列在 coverage JSON。父集合封闭不让其子项自动升格；重复 4CC 仍以 occurrence ID 计，不以代码名字串合并。',
        '', '## 新裁决', '']
    for target,n in sorted(s['upgrades_by_target'].items()):
        report.append(f'- `{target}`：{n} 项。')
    report += ['', '## 剩余缺口', '',
        f"逐 occurrence 阻断点见 `remaining_gaps_v4.json`（club {gap['by_entity']['club']}、nation {gap['by_entity']['nation']}、comp {gap['by_entity']['comp']}）。未证明的 getter/reader 同对象链、读到默认值的门控、未命中型别和域冲突均不视为排除。",
        '- 特别保留：Nation `TCht` 为全空串；阵型值未通过作用域枚举验证；`NCro` 无实档 item。CLUB 重复 `ttcl`/`tbcl` 不强配；COMP `sySx` 无对应档内子型，`HCA*`/`LCA*` 无匹配的 table_48 记录型。',
        '', '运行：`py -V:3.12 -B scripts/t136_big3_final_closure.py`，再加 `--selftest`。不启动游戏、Editor 或 IDA。', '']
    return '\n'.join(report)


def same_output(name, expected):
    path = OUT / name
    if isinstance(expected, str):
        require(path.read_text(encoding='utf-8') == expected, (name, 'not reproduced'))
    else:
        require(load(path) == json.loads(json.dumps(expected, ensure_ascii=False, allow_nan=False)), (name, 'not reproduced'))


def finish(g, hops, archive, selftest):
    base = load(OLD+'big3_l3_v3.json')
    prior = load(OLD+'coverage_summary_v3.json')
    old = base['rows']
    require(len(old) == len({r['id'] for r in old}) == sum(ENTITIES.values()), 'occurrence conservation')
    require(Counter(r['entity'] for r in old) == ENTITIES and cov(old) == prior['t125'], 'v3 coverage drift')
    gaps_by_id = {r['id']:r for r in g['rows']}
    require(len(gaps_by_id) == 160 and set(gaps_by_id) == {r['id'] for r in old if r['new_class'].startswith('gap_')}, 'v3 gap inventory')
    mapping = rules(archive)
    output, gaps, repairs, changes = [], [], [], []
    for r in old:
        e, id_, code = (r[k] for k in ('entity','id','code'))
        i = int(id_[-3:])
        require(schema(e)[i]['field'] == code, (id_, code))
        p = mapping[e].pop(i,None)
        if p is None:
            output.append(r)
            if id_ in gaps_by_id:
                x = gaps_by_id[id_]
                gaps.append(dict(x,t136=blocked(x,hops['gaps'][id_],archive)))
            continue
        require(p.get('code',code) == code, (id_,p))
        before = r['new_class']
        if before == EX:
            require((e,i) in {('nation',64),('club',209)} and p['classification'] == ROUTE, (id_, 'not a verified repair'))
            repairs.append(dict(id=id_,code=code,prior=before,corrected_to=p['classification'],reason=p['reason']))
        else:
            require(id_ in gaps_by_id and before == gaps_by_id[id_]['new_class'], ('attempted overwrite',id_))
        changes.append(dict(id=id_,code=code,prior=before,new=p['classification'],target=p['target_table']))
        output.append(dict(r,new_class=p['classification'],t136=dict(p,prior_class=before,boxing=hops['gaps'].get(id_,{}).get('boxing'))))
    require(not any(mapping.values()), 'unused classifications')
    require(all(a == b for a,b in zip(old,output,strict=True) if a['new_class'].startswith('L3_')), 'v3 L3 not preserved')
    after = cov(output)
    require(after['gaps'] == len(gaps) == 160 - len(changes) + len(repairs), 'transition conservation')
    summary = dict(schema_id='fm24.t136.coverage_summary_v4',conservation=ENTITIES,
                   original_baseline=prior['original_baseline'],t109=prior['t109'],t125=prior['t125'],t136=after,
                   per_entity={e:dict(prior['per_entity'][e],t136=cov([r for r in output if r['entity']==e])) for e in ENTITIES},
                   upgrades_by_target=dict(Counter(str(r['target']) for r in changes if r['new'].startswith('L3_'))),
                   transitions=changes,exclusion_repairs=repairs,l3_downgrades=0,
                   target_85_met=100*after['l3'] >= 85*after['net_denominator'])
    pending = dict(schema_id='fm24.t136.remaining_gaps_v4',gap_total=len(gaps),
                   by_class=dict(Counter(r['new_class'] for r in gaps)),
                   by_blocker=dict(Counter(r['t136']['status'] for r in gaps)),
                   by_entity=dict(Counter(r['entity'] for r in gaps)),rows=gaps)
    fields = dict(schema_id='fm24.t136.big3_l3_v4',denominator=len(output),L4=0,coverage=after,
                  inputs={p:digest((ROOT/p).read_bytes()) for p in (OLD+'big3_l3_v3.json',OLD+'remaining_gaps_v3.json',INDEX,VERIFY,MASTER)},
                  evidence=['hop_audit_v4.json','archive_audit_v4.json'],rows=output)
    report = text_report(summary,pending,hops,archive)
    payloads = {'big3_l3_v4.json':fields,'coverage_summary_v4.json':summary,'remaining_gaps_v4.json':pending,'REPORT.md':report}
    if selftest:
        for name,data in {**payloads,'archive_audit_v4.json':archive,'hop_audit_v4.json':hops}.items():
            same_output(name,data)
        b = named(db.Archive('server'),'table_extra_9')
        for wrong, side in [(b[:-1],'server'),(b+b'\x00','server'),(b,'client'),(b[:12]+b'\x01'+b[13:],'server')]:
            try:
                aux9(wrong,side)
            except (x9.Check, ValueError, struct.error):
                pass
            else:
                raise ValueError('extra9 malformed control passed')
        done = (f"# DONE type=t136\n\n"
                f"Baseline 110/1,034 (10.6%) → t109 379/1,034 (net 56.3%) → t125 512/1,034 (net 76.2%) → "
                f"t136 {after['l3']}/1,034 (net {after['l3']}/{after['net_denominator']} = {after['net_pct']:.1f}%).\n\n"
                f"{after['gaps']} gaps; {after['excluded_non_db']} exclusions; 85% target {'met' if summary['target_85_met'] else 'not met'}.\n\n"
                "`--selftest` PASS — reproduced v4 outputs, prior occurrence conservation, PE witnesses, archive walks, four malformed extra9 controls.\n")
        save('DONE.md',done)
        print('--selftest PASS')
    else:
        for name,data in payloads.items():
            save(name,data)
    print(f"L3 {after['l3']}/1034 (gross {after['gross_pct']:.1f}%); net {after['l3']}/{after['net_denominator']} ({after['net_pct']:.1f}%); {after['excluded_non_db']} exclusions, {after['gaps']} gaps; 85% {'met' if summary['target_85_met'] else 'not met'}")
    print('scratch/t136/out/: ' + ', '.join([*payloads, *(['DONE.md'] if selftest else []), 'archive_audit_v4.json','hop_audit_v4.json']))


def main(argv=None):
    ap = ArgumentParser(description=__doc__)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--stage', choices=['evidence', 'final'], default='final')
    args = ap.parse_args(argv)
    require(not args.selftest or args.stage == 'final', 'selftest requires final stage')
    g = load(OLD + 'remaining_gaps_v3.json')
    hops = hop_audit(g)
    archive = archive_audit()
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.selftest:
        save('hop_audit_v4.json', hops)
        save('archive_audit_v4.json', archive)
        print(f"Evidence: {len(hops['functions'])} second hops, 38 boxing occurrences, {len(archive['numeric'])} numeric members, extra9 251+251 rows")
    if args.stage == 'final':
        finish(g, hops, archive, args.selftest)


if __name__ == '__main__':
    main()
