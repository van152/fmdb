#!/usr/bin/env python3
"""Replay the FM24 2430 client nation Ncpi mapping against read-only installed assets."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import runpy
import struct
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT.parent / 'fm24/scripts'
ROW_FRAME = ROOT / 'scratch/t02/inbox/nati/OUTBOX/verify.py'
SCHEMA_MEMBER = 'comp editor/format/database/nation.xml'
NATION_ROWS, CITY_ROWS, CITY_STRIDE = 251, 56293, 43
NONE = 0xffffffff
GUARD_ID = 775
HASHES = {
    'editor': 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4',
    'nation': '7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34',
    'city': '66f8cc27cba587a0b8e8932b1b2fa31fc0ac2b01a42b7201a97a974b9a91ffe9',
    'schema': 'b4667e6e748b2eac97491b0ed05c1d8af362b9876320a2adda91199935fc7ea6',
}
# Prefix transfers, equivalent property branches, and explicit CITY tagging.
ANCHORS = (
    ('reader_byte_0', 0x141040fb4, 0x10405b4, '49 8d 97 cb 01 00 00 48 8b 06 41 b8 01 00 00 00 48 89 f1 ff 50 28'),
    ('reader_continent_1', 0x141040fd8, 0x10405d8, '49 8d 97 f0 00 00 00 48 8b 06 41 b8 04 00 00 00 48 89 f1 ff 50 28'),
    ('reader_region_5', 0x141040ffc, 0x10405fc, '49 8d 97 f8 00 00 00 48 8b 06 41 b8 04 00 00 00 48 89 f1 ff 50 28'),
    ('reader_city_9', 0x141041020, 0x1040620, '49 8d 97 e8 00 00 00 48 8b 06 41 b8 04 00 00 00 48 89 f1 ff 50 28'),
    ('Ncpi_dispatch', 0x141042b44, 0x1042144, '81 fe 69 70 63 4e 0f 85 5b 05 00 00'),
    ('Ncpi_mode_and_775_gate', 0x141042b5a, 0x104215a, 'ff 50 20 84 c0 0f 85 5f 10 00 00 41 81 7c 24 0c 07 03 00 00 0f 84 50 10 00 00'),
    ('Ncpi_city_member', 0x141042b74, 0x1042174, '49 8b 8c 24 e8 00 00 00 48 8b 55 10 e8 1b 4b fa ff'),
    ('Ncpi_typed_city_ref', 0x140fe76ac, 0xfe6cac, '8b 41 0c 8b 49 10 85 c9 0f 44 c8 eb 0a b8 ff ff ff ff b9 ff ff ff ff 89 44 24 20 89 4c 24 24 48 8d 4c 24 20 ba 79 74 69 63 e8 d6 fb ff ff'),
    ('Ncac_dispatch', 0x141042ab9, 0x10420b9, '81 fe 63 61 63 4e 0f 85 e6 05 00 00'),
    ('Ncac_member_and_gate', 0x141042ac5, 0x10420c5, '49 8b 8c 24 e8 00 00 00 48 85 c9 0f 84 d5 05 00 00 41 81 7c 24 0c 07 03 00 00 0f 84 c6 05 00 00'),
    ('Ncac_pack_call', 0x141042aec, 0x10420ec, 'e8 9f 46 fa ff'),
    ('Ncac_pack_thunk', 0x140fe7190, 0xfe6790, 'e9 fb d1 e4 02'),
    ('Ncac_pack_inputs', 0x143e343ca, 0x3cc8dca, '8b 77 08 48 8b 07 48 89 f9 ff 50 38 89 c7'),
    ('Ncac_pack', 0x143e343ed, 0x3cc8ded, '89 f8 21 f0 c1 e7 18 81 e6 ff ff 7f 00 09 fe 83 f8 ff b8 ff ff 7f ff 0f 45 c6 41 89 06'),
    ('Ncac_wrap', 0x141042afb, 0x10420fb, 'e8 00 82 fa ff'),
    ('NcpR_dispatch', 0x141042b38, 0x1042138, '81 fe 52 70 63 4e 0f 84 20 07 00 00'),
    ('NcpR_member_and_null', 0x141043264, 0x1042864, '49 8b b4 24 e8 00 00 00 b3 01 48 85 f6 0f 84 c4 0b 00 00'),
    ('NcpR_pack_inputs', 0x141043292, 0x1042892, '8b 7e 08 48 8b 06 48 89 f1 ff 50 38 89 c6'),
    ('NcpR_pack', 0x1410432b8, 0x10428b8, '89 f0 21 f8 c1 e6 18 81 e7 ff ff 7f 00 09 f7 83 f8 ff b8 ff ff 7f ff 0f 45 c7 89 45 18'),
    ('NcpR_wrap', 0x1410432e9, 0x10428e9, 'e8 12 7a fa ff'),
)
# Holdouts selected before reading the field for these nations; spelling is that of t2 English.
HOLDOUTS = {'Argentina': 'Ciudad de Buenos Aires', 'Australia': 'Canberra',
            'Brazil': 'Brasília (DF)', 'Germany': 'Berlin', 'Japan': 'Tokyo',
            'United States': 'Washington (DC)'}


class CheckFailed(Exception):
    """Evidence check did not pass."""


def require(ok, message):
    if not ok:
        raise CheckFailed(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def checked_hash(kind, data):
    result = sha(data)
    require(result == HASHES[kind], f'unexpected {kind} SHA-256: {result}')
    return result


def entry(layout, name):
    matches = [e for e in layout['entries'] if e['path'] == name]
    require(len(matches) == 1, f'expected one member {name}; found {len(matches)}')
    return matches[0]


def verify_schema(raw):
    xml = ET.fromstring(raw, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
    candidates = [ET.fromstring(node.text.strip()) for node in xml.iter()
                  if node.tag is ET.Comment and 'value="Ncpi"' in (node.text or '')]
    require(len(candidates) == 1, 'expected one commented Ncpi record')
    record = candidates[0]
    require(record.tag == 'record', 'comment does not contain a record')
    flags = {node.attrib['id']: node.attrib['value'] for node in record.findall('flags')}
    booleans = {node.attrib['id']: node.attrib['value'] for node in record.findall('boolean')}
    name = record.find("translation[@id='name']")
    dep = record.find("list[@id='dependencies']/record[@field='duni']")
    active = sum(node.attrib.get('id') == 'field' and node.attrib.get('value') == 'Ncpi'
                 for node in xml.iter('flags'))
    require(flags == {'field': 'Ncpi', 'type': 'database_record_unique_id', 'database_table_type': 'city'}
            and booleans == {'is_client_field': 'true', 'is_optional': 'true'}
            and name is not None and name.attrib.get('value') == 'Capital City'
            and name.attrib.get('translation_id') == '293203'
            and dep is not None and dep.attrib.get('not_equals') == str(GUARD_ID)
            and active == 0, 'Ncpi schema tuple or commented/active status changed')
    return {'member': SCHEMA_MEMBER, 'commented': True, 'active_records': active,
            'properties': flags | booleans, 'name': name.attrib['value'],
            'translation_id': int(name.attrib['translation_id']),
            'dependency': {'field': 'duni', 'not_equals': GUARD_ID}}


def frozen_provenance():
    manifest = json.loads((ROOT / 'evidence/MANIFEST.json').read_text(encoding='utf-8'))
    path = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
    item, = (i for i in manifest['files'] if i['path'] == path)
    data = (ROOT / path).read_bytes()
    require(sha(data) == item['sha256'] and HASHES['editor'].encode() in data,
            'frozen exe provenance mismatch')
    return {'manifest': 'evidence/MANIFEST.json', 'snapshot': path, 'sha256': item['sha256']}


def replay():
    sys.path.insert(0, str(UPSTREAM))
    import modding_read_dbdat as dat
    import modding_read_fmf as fmf
    from modding_db_names import DatabaseNameIndex

    db = dat.DEFAULT_DB_DIR
    game = db.parents[4]
    editor = game.parent / 'Football Manager 2024 Editor/editor.exe'
    image = editor.read_bytes()
    exe_hash = checked_hash('editor', image)
    instructions = {}
    for label, va, off, expect in ANCHORS:
        raw = bytes.fromhex(expect)
        require(image[off:off + len(raw)] == raw, f'{label} bytes differ at {off:#x}')
        instructions[label] = {'va': hex(va), 'file_offset': hex(off), 'bytes': expect}

    schema_path = game / 'data/comp editor.fmf'
    layout = fmf.inspect(schema_path)
    e = entry(layout, SCHEMA_MEMBER)
    with schema_path.open('rb') as handle:
        schema_off = layout['data_base'] + e['offset']
        raw_schema = fmf.read_blocks(handle, schema_off, e['packed_size'], e['size'])
    schema = verify_schema(raw_schema) | {'archive': schema_path.as_posix(),
              'archive_sha256': sha(schema_path.read_bytes()), 'member_sha256': checked_hash('schema', raw_schema),
              'member_archive_offset': hex(schema_off)}

    archive = db / 'client_db.dat'
    data, layout = dat._read_archive(archive)
    nation, city = (dat._decompress_entry(data, layout['data_base'], entry(layout, f'client_db/table_{tid}.dat'))
                    for tid in (10, 2))
    nation_hash, city_hash = checked_hash('nation', nation), checked_hash('city', city)
    frame = runpy.run_path(str(ROW_FRAME))
    try:
        parsed = frame['parse_payload'](nation)
    except frame['CheckFailure'] as exc:
        raise CheckFailed(str(exc)) from exc
    require(len(city) == 14 + CITY_ROWS * CITY_STRIDE + 8
            and struct.unpack_from('<I', city, 8)[0] == CITY_ROWS, 'wrong city table dimensions')
    cities = []
    for i in range(CITY_ROWS):
        p = 14 + i * CITY_STRIDE
        ordinal, id1, id2, marker = struct.unpack_from('<IIIB', city, p + 30)
        require(ordinal == i and id1 == id2 and marker == 0, f'city identity failed at row {i}')
        cities.append((id1, struct.unpack_from('<I', city, p + 10)[0]))
    city_ids = {r[0] for r in cities}
    require(len(city_ids) == CITY_ROWS, 'city IDs are not unique')

    base = db.parent.parent / '2400/2400_fm/lang_db.dat'
    names = DatabaseNameIndex(db, base)
    index = {}
    language_inputs = {}
    lang = 8
    for tid in (2, 9):  # string-table ID 9 is nation; client-db object table ID is 10.
        index[tid] = {}
        for label, layer in (('base', names.base_layer), ('update', names.update_layer)):
            payload = layer.payload(f'{lang}_{tid}')
            slots = layer.rows_for(lang, tid)
            count = struct.unpack_from('<I', payload, 8)[0]
            require(len(slots) == count and len({s['dbid'] for s in slots}) == count
                    and all(s['anchor'] == 'grammar' for s in slots), f'bad language walk {label}:{lang}_{tid}')
            language_inputs[f'{label}:{lang}_{tid}'] = {'archive': layer.lang_path.as_posix(),
                                                       'payload_sha256': sha(payload), 'rows': count}
            index[tid].update({r['dbid']: (r['primary'], label) for r in slots if r['primary']})
    nation_by_ord = {r['ordinal']: r['id'] for r in parsed['rows']}
    records = []
    id_control_hits = 0
    for r in parsed['rows']:
        i, duni = r['ordinal'], r['id']
        field_offset = r['start_payload'] + 9
        value = struct.unpack_from('<I', nation, field_offset)[0]
        source_name, source_layer = index[9][duni]
        item = {'nation_row': i, 'nation_duni': duni, 'nation_name': source_name,
                'nation_name_layer': source_layer, 'field_payload_offset': hex(field_offset),
                'field_wire_hex': nation[field_offset:field_offset + 4].hex(' '),
                'city_row': None if value == NONE else value}
        if value != NONE:
            require(value < CITY_ROWS, f'out-of-range city ordinal {value} at nation row {i}')
            id_control_hits += value in city_ids
            cid, owner = cities[value]
            require(cid in index[2], f'no English name for selected city duni {cid}')
            target_name, target_layer = index[2][cid]
            owner_duni = nation_by_ord.get(owner)
            item.update(city_duni=cid, city_name=target_name, city_name_layer=target_layer,
                        city_nation_row=owner, city_nation_duni=owner_duni,
                        city_nation_name=index[9].get(owner_duni, (None, None))[0])
        records.append(item)

    nonnull = [r for r in records if r['city_row'] is not None]
    cross = [r for r in nonnull if r['city_nation_row'] != r['nation_row']]
    guard, = (r for r in records if r['nation_duni'] == GUARD_ID)
    require((len(nonnull), id_control_hits) == (231, 25), 'city ordinal / ID control counts changed')
    require([r['nation_row'] for r in cross] == [69, 83, 124, 248, 250], 'cross-nation rows changed')
    require(guard['nation_row'] == 149 and guard['nation_name'] == 'Israel' and guard['city_row'] is None,
            '775 check differs')
    holdouts = [r for r in records if r['nation_name'] in HOLDOUTS]
    observed_holdouts = {r['nation_name']: r.get('city_name') for r in holdouts}
    require(len(holdouts) == len(HOLDOUTS) and observed_holdouts == HOLDOUTS,
            f'holdout mismatch: {observed_holdouts!r}')
    result = {
        'status': 'complete', 'scope': 'FM24 2430 client table_10, one field only',
        'field': {'code': 'Ncpi', 'name': 'Capital City', 'row_offset': 9, 'width': 4, 'wire_type': 'u32le',
                  'target': 'client_db/table_2.dat row ordinal (zero-based)', 'null_u32': NONE,
                  'object_offset': '0xe8', 'evidence_level': 'L3'},
        'schema': schema, 'editor_exe': {'path': editor.as_posix(), 'sha256': exe_hash,
                                        'frozen_provenance': frozen_provenance(), 'anchors': instructions},
        'data': {'archive': archive.as_posix(), 'archive_sha256': sha(data), 'nation_payload_sha256': nation_hash,
                 'city_payload_sha256': city_hash, 'language_inputs': language_inputs, 'nation_rows': NATION_ROWS,
                 'city_rows': CITY_ROWS, 'row_span_sum': parsed['sum_row_spans'],
                 'nulls': len(records) - len(nonnull), 'ordinal_hits': len(nonnull), 'duni_control_hits': id_control_hits,
                 'same_nation_row_hits': len(nonnull) - len(cross)},
        'gate': {'ncpi': 'mode check or nation ID 775 selects fallback before reading the member',
                 'ncac': 'requires non-null and nation ID other than 775',
                 'ncpr': 'same member and packed ID formula as Ncac; no 775 check in this branch',
                 'excluded_row': guard},
        'holdouts': holdouts, 'cross_nation': cross,
        'limits': ['Ncpi schema record is disabled by XML comment; no proof of editability or L4',
                   'Getter guards do not establish what originally populated the disk value',
                   'Cross-nation records are observed values, not inferences about political status'],
    }
    return result, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--selftest', action='store_true', help='replay all byte, schema, join and holdout checks')
    group.add_argument('--dump-rows', action='store_true', help='emit the 251 named nation rows as JSON')
    args = parser.parse_args()
    try:
        result, records = replay()
    except (CheckFailed, ET.ParseError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    except (OSError, ImportError, RuntimeError, ValueError, KeyError, struct.error) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    if args.selftest:
        print('PASS: Ncpi row+9 / 4B; 251 nations, 231 city ordinals, 20 nulls, 5 cross-nation rows; 6/6 holdouts')
    else:
        print(json.dumps(records if args.dump_rows else result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
