"""Verify the frozen t69 handoff and spot-read only four COMP slots from both archives."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import iter_unpack, pack, unpack_from, error as StructError
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCHEMA = 'reports/club_nation_subtable_schema.json'
V8 = 'scratch/t60/out/club_nation_subtable_schema.v8.json'
M57 = 'scratch/t57/out/field_map.json'
M59 = 'scratch/t59/out/field_map.json'
S59 = 'scratch/t59/out/field_slots.json'
I61 = 'scratch/t61/out/enum_inventory.json'
C66 = 'scratch/t66/out/collections.json'
R66 = 'scratch/t66/out/census.json'
X68 = 'scratch/t68/out/crosswalk.json'
SIDES = ('client', 'server')
N = 7047
SLOTS = {'+0xa8': ('a8_present', 'obj_a8'), '+0xe0': ('e0_present', 'obj_e0'),
         'vec30': ('vec30',), '+0x100': ('vec100',)}


class Failed(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Failed(message)


def read(path):
    return json.loads((ROOT / path).read_bytes())


def sha(data):
    return sha256(data).hexdigest()


def hist(values):
    return {str(k): n for k, n in sorted(Counter(values).items())}


def local(path):
    for p in (path, path.absolute()):
        if p.drive.upper() == 'Z:' or str(p).upper().replace('\\', '/').startswith(('Z:', '/Z/')):
            raise ValueError('Z: forbidden')
    resolved = path.resolve()
    if resolved.drive.upper() == 'Z:':
        raise ValueError('Z: forbidden')
    return resolved


def archive(path, side, meta):
    # Same local Python-3.12 zstandard dependency as the delivered t59 verifier.
    try:
        import zstandard as z
    except ModuleNotFoundError:
        sys.path.append(str(local(ROOT.parent / 'fm24/tools/python')))
        import zstandard as z

    def frame(data):
        need(data.startswith(bytes.fromhex('28b52ffd')), (side, 'zstd magic'))
        d = z.ZstdDecompressor().decompressobj()
        out = d.decompress(data)
        span = len(data) - len(d.unused_data)
        need(d.eof and span > 0, (side, 'zstd frame EOF'))
        return out, span

    blob = local(path).read_bytes()
    need(sha(blob) == meta['archive_sha256'], (side, 'frozen archive SHA'))
    toc, base = (value + 17 for value in unpack_from('<QQ', blob, 17))
    shell = bytes.fromhex('0201666d662e080000')
    need(base == 34 == meta['data_base'] and blob[8:17] == blob[toc:toc+9] == shell,
         (side, 'archive shell'))
    directory, span = frame(blob[toc+9:])
    need(toc + 9 + span == len(blob), (side, 'TOC EOF'))
    p, entries = 0, {}

    def take(w):
        nonlocal p
        need(w <= len(directory) - p, (side, 'short TOC'))
        p += w
        return directory[p-w:p]

    def u32():
        return int.from_bytes(take(4), 'little')

    def text():
        return take(u32()).decode('utf-8')

    def walk(parent, depth=0):
        need(depth < 40, (side, 'TOC depth'))
        folder = parent / text()
        for _ in range(u32()):
            name = (folder / (text() + text())).as_posix()
            offset, width, size, _, _ = unpack_from('<5Q', take(40))
            need(name not in entries, (side, 'duplicate TOC entry', name))
            entries[name] = base + offset, width, size
        for _ in range(u32()):
            walk(folder, depth+1)

    walk(PurePosixPath())
    need(p == len(directory) and len(entries) == meta['entries'], (side, 'TOC closure'))
    name = f'{side}_db/table_25.dat'
    lo, width, size = entries[name]
    hi = lo + width
    bound = min((a for a, *_ in entries.values() if a > lo), default=toc)
    m = meta['members']['25']
    need(base <= lo < hi <= bound == m['bound'] and name == m['member'] and
         [lo, hi] == m['range'] and size == m['declared_size'] and
         sha(blob[lo:hi]) == m['compressed_sha256'], (side, 'packed bounds/SHA'))
    frames, found = [], []
    while lo < hi:
        raw, span = frame(blob[lo:hi])
        frames.append([lo, lo+span, len(raw)])
        if len(raw) == size:
            found.append(raw)
        lo += span
    need(lo == hi and len(found) == 1 and frames == m['frames'], (side, 'unique sized frame'))
    raw, = found
    need(sha(raw) == m['payload_sha256'] and unpack_from('<I', raw, 8)[0] == m['count'] == N,
         (side, 'payload SHA/count'))
    return raw, m


def point(raw, i, at, width, value):
    return {'row': i, 'at': at, 'raw': raw[at:at+width].hex(), 'value': value}


def probe(raw, rows, events, key, side, prof, prior):
    optional = len(SLOTS[key]) == 2
    if side == 'client':
        need(not events and all(p['events'] == p['bytes'] == 0 for p in prof) and
             prior['events'] == prior['payload_rows'] == prior['items'] == 0 and
             prior['mode_skipped_rows'] == len(rows), (key, 'client mode skip'))
        return dict(status='mode_skipped', rows=len(rows), values_read=0, histogram={},
                    nonzero_rows=0, item_rows=0, items=0, first=None, payload_events=0)
    need(len(rows) == len(events) == prior['events'] and prior['mode_skipped_rows'] == 0,
         (key, 'server event count'))
    coords, content, values, nonzero, items = [], [], [], [], []
    first = first_nonzero = None
    for i, ((start, ident, _, _), (ordinal, flag, at, end, count_at, count, item_spans)) in enumerate(zip(rows, events)):
        need(ordinal == i, (key, i, 'ordinal'))
        if optional:
            need(flag == start + (120 if key == '+0xa8' else 129) < ident and
                 (at, end, count_at, count, item_spans) == (None, None, None, None, []),
                 (key, i, 'presence coordinate or unexpected payload'))
            a, w, value = flag, 1, raw[flag]
            need(value == 0, (key, i, 'observed nonzero presence'))
        else:
            w = 4 if key == 'vec30' else 2
            need(flag is None and at == count_at and start+71 <= at <= ident-w,
                 (key, i, 'count bounds'))
            a = at
            value = unpack_from('<I' if w == 4 else '<h', raw, a)[0]
            stride = 2 if w == 4 else 5
            need(0 <= value == count and a+w+stride*value == end <= ident and
                 item_spans == [[j, j+stride, []] for j in range(a+w, end, stride)],
                 (key, i, 'item span/count'))
            if key == 'vec30':
                need(a == start+116 and value == 0, (key, i, 'zero count'))
            else:
                items.extend(iter_unpack('<BHH', raw[a+w:end]))
        if i == 0:
            first = point(raw, i, a, w, value)
        if value:
            nonzero.append(i)
            if first_nonzero is None:
                first_nonzero = point(raw, i, a, w, value)
        width = w if optional else end-a
        coords.append(pack('<III', i, a, width))
        content.append(raw[a:a+width])
        values.append(value)
    csha, bsha = sha(b''.join(coords)), sha(b''.join(content))
    need(prof[0]['events'] == len(values) and prof[0]['bytes'] == sum(map(len, content)) and
         (csha, bsha) == (prof[0]['coordinate_sha256'], prof[0]['content_sha256']) and
         {k: first[k] for k in ('row', 'at', 'raw')} == {k: prof[0]['first'][k] for k in ('row', 'at', 'raw')},
         (key, 't59 slot coordinates and bytes'))
    h = hist(values)
    need(h == prior['presence_histogram' if optional else 'count_histogram'] and
         nonzero == prior['nonempty_ordinals'] and len(items) == prior['items'] and
         (not optional or (prior['payload_rows'] == prof[1]['events'] == prof[1]['bytes'] == 0)),
         (key, 't66 histograms / untriggered payload'))
    profile = dict(status='presence_read' if optional else 'count_read', rows=len(rows),
                   values_read=len(values), histogram=h, nonzero_rows=len(nonzero), item_rows=len(nonzero),
                   items=len(items), first=first, first_nonzero=first_nonzero, coordinate_sha256=csha,
                   content_sha256=bsha, payload_events=0 if optional else len(values))
    if key == '+0x100':
        lanes = {f'item.+{p}': hist(x[i] for x in items) for i, p in enumerate((0, 1, 3))}
        need(all(lanes[k] == prior['fields'][k]['histogram'] for k in lanes) and
             prior['item_width_histogram'] == {'5': len(items)}, (key, 't66 raw item distributions'))
        profile['item_histograms_unsigned_LE'] = lanes
    return profile


def comp_raw(slots, census, collections, db):
    lookup = {r['key']: r for r in slots['slots']}
    result = {k: {} for k in SLOTS}
    archive_meta, public, diagnostic = {}, {}, {}
    for side in SIDES:
        raw, archive_meta[side] = archive(db / f'{side}_db.dat', side, slots['archives'][side])
        env, records = slots['envelopes'][side], census['sides'][side]
        rows = records['rows']
        need(len(rows) == env['count'] == N and raw[:13].hex() == env['header_hex'] and
             raw[-9:].hex() == env['footer_hex'], (side, 'frozen envelope'))
        end = 13
        slices = []
        for i, (start, ident, stop, uid) in enumerate(rows):
            need(start == end and start < ident and stop == ident+12 <= len(raw)-9 and
                 raw[start] == 0 and unpack_from('<III', raw, ident) == (i, uid, uid), (side, i, 'row witness'))
            need(side != 'client' or stop-start == 127, (side, i, 'no extension span'))
            end = stop
            slices.append((raw[start:start+71], raw[stop-56:stop]))
        need(end == len(raw)-9 and sha(b''.join(pack('<III', a, z, v) for a, _, z, v in rows)) ==
             env['row_trace_sha256'], (side, 't59 row trace'))
        public[side] = slices
        seqs = slots['execution_templates'][side]
        mode = slots['external_modes'][side]
        need(mode['mode'] == SIDES.index(side) and sum(x['rows'] for x in seqs) == N,
             (side, 'frozen mode/template'))
        diagnostic[side] = (f'vec30: row 0 @129: invalid count {unpack_from("<I", raw, 129)[0]}' if side == 'client'
                            else f'row 0 @128: identity {unpack_from("<III", raw, 128)}')
        need(diagnostic[side] == mode['forced_opposite_first_failure'], (side, 'opposite mode counterexample'))
        for key, keys in SLOTS.items():
            need(all((keys[0] in x['sequence']) == (side == 'server') for x in seqs) and
                 all(k not in x['sequence'] for x in seqs for k in keys[1:]), (side, key, 'template membership'))
            result[key][side] = probe(raw, rows, records['collections'][key], key, side,
                                      [lookup[k]['profiles'][side] for k in keys], collections[key]['sides'][side])
    need(public['client'] == public['server'], 'common 71B prefix and 56B suffix, paired identity')
    return result, archive_meta, diagnostic


def ref(path, pointer='', **info):
    return dict(path=path, pointer=pointer, **info)


def club_entries(schema, v8, m57):
    t, a = schema['tables'], schema['club_auxiliary_sources']
    need(schema['schema_version'] == 9 and v8['schema_version'] == 8 and
         (t, a) == (v8['tables'], v8['club_auxiliary_sources']) and len(t) == 8 and len(a) == 1,
         'v8/v9 numeric and auxiliary inheritance')
    aux, = a
    skipped = [(i, r) for i, r in enumerate(m57['fields']) if r['grade'] == 'skipped_separate_member']
    need(len(skipped) == 10 == m57['grade_counts']['skipped_separate_member'] and
         [r['code'] for _, r in skipped] == schema['club_main_row_fields']['grade_membership']['skipped_separate_member'],
         't57 skip population')
    for i, r in skipped:
        key = r['code']
        refs = [ref(M57, f'/fields/{i}')]
        hits = [(f'/tables/{j}', s) for j, s in enumerate(t) if s['parent_code'] == key and s['server_payload']['closure_ok']]
        views = [(f'/club_auxiliary_sources/0/views/{j}', v) for j, v in enumerate(aux['views'])
                 if v['view'] == key and aux['source_id'] == 'CLUB_LINK' and aux['server_payload']['closure_ok']]
        row = dict(id=f'club.{key}', table='club', kind='skipped', source_grade=r['grade'], evidence_refs=refs)
        if len(hits) + len(views) != 1:
            yield row | dict(status='unresolved_handoff', grade='pending', 承接=None)
            continue
        if hits:
            (ptr, s), = hits
            task, payload = s['source_task'], s['server_payload']
            need(f"table_{s['table_type']}," in r['reason'] and s['fields'][0]['grade'].startswith('L3'), (key, 'numeric handoff'))
            owner = {'table_type': s['table_type'], 'rtti_class': s['rtti_class'], 'scope': s['entity']}
            child = '/fields/0'
            if key == 'Tchl':
                owner['qualification'] = s['supplemental_evidence']['shared_dispatch_and_owner_scope']
                refs.append(ref(SCHEMA, ptr+'/supplemental_evidence/shared_dispatch_and_owner_scope'))
            if key == 'Csme':
                owner['qualification'] = s['owner_scope']['scope_caveat']
                refs.append(ref(SCHEMA, ptr+'/owner_scope'))
            code = s['fields'][0]['code']
            member, present = payload['path'], s['client_observation']['present']
        else:
            (ptr, v), = views
            task, payload = aux['provenance']['source_task'], aux['server_payload']
            v44 = read('scratch/t44/out/fields_cafl_cvfl.json')
            child = '/occurrences/0'
            code = v['occurrences'][0]['code']
            need(v44['occurrences'][key][0]['code'] == code and v44['source'] == aux['member'] and
                 v44['occurrence_grades'][key] == v['occurrence_grade_counts'] and
                 aux['table_type'] is None and 'club_links.dat' in r['reason'], (key, 'shared view handoff'))
            member, present = aux['member'], aux['client_observation']['present']
            owner = dict(source_id='CLUB_LINK', table_type=None, view_mode=v['view_mode'],
                         occurrence_grade_counts=v['occurrence_grade_counts'])
            refs.extend([ref(SCHEMA, '/club_auxiliary_sources/0/server_payload'),
                         ref('scratch/t44/out/fields_cafl_cvfl.json', f'/occurrences/{key}/0')])
        refs.extend(ref(path, ptr) for path in (SCHEMA, V8))
        refs.append(ref(SCHEMA, ptr+child, code=code))
        yield row | dict(status='handed_off', grade='L2', 承接=dict(task=task, scope='existing source only'),
                         member=member, client_member_present=present, server_rows=payload['row_count'],
                         server_closure=payload['closure_formula'], owner=owner, accepted_child_example=code)


def static_excerpt(slots):
    wanted = {'mode': (0xeb739d, 0xeb73a0), '+0xa8': (0xeb7532, 0xeb753f, 0xeb7544, 0xeb75ca),
              '+0xe0': (0xeb76c0, 0xeb76cd, 0xeb76d2, 0xeb76fb)}
    outdir = ROOT / 'scratch/t59/out'
    parts = {}
    for pattern, key in (('branches.part*.json', 'site'), ('instructions.part*.json', 'file_offset')):
        parts[key] = {r[key]: (f.relative_to(ROOT).as_posix(), i, r)
                      for f in sorted(outdir.glob(pattern)) for i, r in enumerate(read(f.relative_to(ROOT)))}
    result = {}
    for label, sites in wanted.items():
        flow = sites[1] if label == 'mode' else sites[2]
        path, i, b = parts['site'][flow]
        refs, instructions = [ref(path, f'/{i}')], []
        for site in sites:
            path, i, ins = parts['file_offset'][site]
            refs.append(ref(path, f'/{i}'))
            instructions.append(dict(file_offset=hex(site), VA=hex(ins['VA']), bytes=ins['bytes'], text=ins['instruction']))
        j = instructions[sites.index(flow)]
        need(j['text'].startswith('je ') and int(j['text'].split()[1], 16) - int(j['VA'], 16) == b['taken']-flow,
             (label, 'zero predicate edge'))
        result[label] = dict(editor=slots['source']['editor'], sha256=slots['source']['editor_sha256'],
                             predicate=b['predicate_instruction'], zero_taken_to=hex(b['taken']),
                             nonzero_fallthrough=hex(b['fallthrough']), instructions=instructions, refs=refs)
    return result


def expected(db):
    schema, v8, m57, m59, slots = map(read, (SCHEMA, V8, M57, M59, S59))
    t61, c66, r66, t68 = map(read, (I61, C66, R66, X68))
    tasks = {t: {'status': 'delivered', 'report': f'scratch/{t}/out/REPORT.md', 'done': f'scratch/{t}/out/DONE.md'}
             for t in ('t61', 't66', 't68')}
    for t in tasks.values():
        need(all((ROOT / t[k]).stat().st_size > 0 for k in ('report', 'done')), ('delivery marker', t))
    need(m59['summary'] == schema['comp_main_row_fields']['field_census']['grade_counts'] and
         schema['comp_main_row_fields']['outer_sequence_closure']['static_untriggered_positions'] == ['obj_a8', 'obj_e0'],
         't59 to v9 fold')
    need(c66['mode_tests'] == slots['external_modes'] and c66['t59_negatives'] == m59['fixtures']['falsified_t01f'] and
         all(sha((ROOT / 'scratch/t59/out' / name).read_bytes()) == h for name, h in c66['t59_input_sha256'].items()),
         't66 inherited t59 snapshot')
    need(t68['scope']['only_table_3'] and not t68['scope']['reads_club_link'] and
         t68['claims'][3]['id'] == 'selector_templates' and t68['claims'][3]['status'] == 'pass', 't68 context only')
    dist, members, ctrl = comp_raw(slots, r66, c66['collections'], db)
    branches = static_excerpt(slots)
    rows = list(club_entries(schema, v8, m57))
    nation = [(i, x) for i, x in enumerate(t61['occurrences']) if x['entity'] == 'nation' and x['layer'] == 'main']
    need([x['code'] for _, x in nation] == ['Necf', 'Nygn', 'Ngct', 'Nsod'], 'four located nation records')
    for i, x in nation:
        src = x['source']
        need(x['grade'] == src['grade'] == 'held' and x['decision'] == 'no_enum_source' and
             x['enum_ref'] is None and x['code'] in schema['nation_main_row_fields']['grade_membership']['held'], (x['code'], 't61 decision'))
        rows.append(dict(id=f"nation.{x['code']}", table='nation', kind='held', grade='held',
                         status='t61_confirmed_no_promotion', decision=x['decision'],
                         evidence_refs=[ref(src['path'], src['pointer']), ref(I61, f'/occurrences/{i}')],
                         diagnostics=x['archives'], prior_first_counterexample=x['prior_first_counterexample'],
                         承接=dict(task='t61', scope='existing enum review; no rejudgment')))
    s_index = {s['key']: i for i, s in enumerate(slots['slots'])}
    for key, ks in SLOTS.items():
        c = c66['collections'][key]
        qualified = key == '+0x100'
        need(c['grade'] == ('L3' if qualified else 'held') and c['grade_scope'] == 'physical item grammar only' and
             c['inline_member'] == 'table_25.dat' and not c['reference_lanes'], (key, 't66 scope'))
        refs = [ref(S59, f'/slots/{s_index[k]}') for k in ks]
        refs += [ref(C66, f'/collections/{key}')] + [ref(R66, f'/sides/{side}/collections/{key}') for side in SIDES]
        if len(ks) == 2:
            refs += branches['mode']['refs'] + branches[key]['refs']
        open_edge = {'+0xa8': 'presence != 0 payload: no archive witness', '+0xe0': 'presence != 0 payload: no archive witness',
                     'vec30': 'N > 0 item arm: no archive witness', '+0x100': 'business name / getter binding not established'}[key]
        rows.append(dict(id=f'comp.{key}', table='comp', kind='edge-pending' if qualified else 'static-zero',
                         status='physical_grammar_only' if qualified else 'untriggered_item_or_payload', grade='L2',
                         inherited_grade=c['grade'], inherited_grade_scope=c['grade_scope'], existing_grammar=c['grammar'],
                         evidence_refs=refs, data=dist[key], open_edge=open_edge,
                         承接=dict(task='t66', scope='physical record only; open edge has no assigned successor')))
    totals = {table: dict(Counter(r['kind'] for r in rows if r['table'] == table)) for table in ('club', 'nation', 'comp')}
    return dict(task='t69', schema_versions=[8, 9], grade_target='L2', new_L3=0, L4=0, count=len(rows), totals=totals,
                unresolved_club=[r['id'] for r in rows if r['status'] == 'unresolved_handoff'], delivery_status=tasks,
                context_refs=[ref('scratch/t50/out/REPORT.md', section='§4 / §6'), ref(X68, '/claims/3'),
                              ref(X68, '/scope'), ref(SCHEMA, '/comp_main_row_fields/outer_sequence_closure')],
                comp_archive_members=members, comp_preserved_wrong_mode=ctrl, comp_static_predicates=branches, entries=rows)


def selftest():
    for value in (0, 1):
        b = bytearray(156)
        b[120] = value
        p = {'events': 1, 'bytes': 1, 'coordinate_sha256': sha(pack('<III', 0, 120, 1)),
             'content_sha256': sha(b'\x00'), 'first': {'row': 0, 'at': 120, 'raw': '00'}}
        prior = {'events': 1, 'mode_skipped_rows': 0, 'presence_histogram': {'0': 1},
                 'nonempty_ordinals': [], 'items': 0, 'payload_rows': 0}
        try:
            out = probe(b, [[0, 140, 152, 1]], [[0, 120, None, None, None, None, []]], '+0xa8', 'server',
                        [p, {'events': 0, 'bytes': 0}], prior)
        except Failed:
            need(value == 1, 'selftest rejected correct zero')
        else:
            need(value == 0 and out['histogram'] == {'0': 1}, 'selftest accepted changed presence')
    empty = {'events': 0, 'bytes': 0, 'payload_rows': 0, 'items': 0, 'mode_skipped_rows': 1}
    out = probe(b'', [[0, 115, 127, 1]], [], 'vec30', 'client', [empty], empty)
    need(out['values_read'] == 0 and out['histogram'] == {}, 'selftest client skip is not a zero value')
    return 'PASS --selftest (synthetic zero, nonzero rejection, client skip)'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group()
    g.add_argument('--check', action='store_true', help='verify delivery and targeted archive bytes (default)')
    g.add_argument('--selftest', action='store_true', help='test zero/skip handling without opening archives')
    a = p.parse_args()
    try:
        if a.selftest:
            print(selftest())
        else:
            db = local(Path(os.environ.get('FM24_DB_DIR', ROOT / 'scratch/data')))
            saved = read(HERE / 'tail_ledger.json')
            actual = expected(db)
            need(saved == actual, 'tail_ledger.json differs from checked sources/data')
            print(f"PASS --check: {actual['count']} items; 2 x {N} COMP row witnesses, 4 selected slots")
        return 0
    except Failed as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    except (OSError, ImportError, ValueError, KeyError, IndexError, TypeError, StructError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
