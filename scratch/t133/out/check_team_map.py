#!/usr/bin/env python3
"""Offline t79 field-map cross-check; not imported by the t133 reader."""
from collections import Counter
from pathlib import Path
from struct import unpack_from
import json
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import t133_fm24_reader_v2 as reader
from t79_stad_team_harvest import replay_table_24, self_certify_extra_24


def require(condition, detail):
    if not condition:
        raise ValueError(str(detail))


def main():
    archive = reader.base.Archive('server')
    table = archive.payload(24)
    known = replay_table_24(table)
    walkers = {flag: reader.compile_walk(ops) for flag, ops in reader.SELECTORS['server', 24].items()}
    p, end = 13, len(table) - 9
    prefixes = Counter()
    for i in range(known['n']):
        flag = table[p]
        prefix = 0 if flag == 10 else 49 + 10 * unpack_from('<b', table, p + 49)[0]
        prefixes[flag, prefix] += 1
        team = p + 1 + prefix
        rep, div, last, next_div, stadium = unpack_from('<hiiii', table, team + 2)
        todo, count = unpack_from('<iH', table, team + 29)
        nod = unpack_from('<i', table, team + 48 + 4 * count)[0]
        base = team + 53 + 4 * count
        typ, nation = unpack_from('<bB', table, base)
        owner, long_len = unpack_from('<iI', table, base + 6)
        short_len = unpack_from('<I', table, base + 15 + long_len)[0]
        identity = base + 20 + long_len + short_len
        ordinal, uid, raw_rdui = unpack_from('<III', table, identity)
        q = walkers[flag](table, p + 1, end)
        vals = dict(sel=flag, uid=uid, rdui=raw_rdui, trep=rep, tdvi=div, tldi=last,
                    tndi=next_div, tsti=stadium, todo=todo, v38=count, tnod=nod,
                    ttyp=typ, tisn=nation, own=owner, lna_len=long_len, sna_len=short_len)
        require(ordinal == i and q == identity + 12
                and all(value == known[key][i] for key, value in vals.items()), ('table_24', i))
        p = q
    require(p == end == known['body_end'], 'table_24 footer')

    entry = archive.entries['server_db/table_extra_24.dat']
    start = archive.data_base + entry['offset']
    frames = reader.base._decode_frames(archive.data[start:start + entry['packed_size']])
    payload, = [f['data'] for f in frames if f['length'] == entry['size']]
    cert = self_certify_extra_24(payload, known['n'])
    offsets = (29, 33, 37, 41, 45, 57)
    destinations = (0xe4, 0xe8, 0xec, 0xf0, 0xf4, 0xe0)
    dates = {off: Counter() for off in offsets}
    fields = {name: Counter() for name in ('Twhm', 'Tmhm', 'Tpvr')}
    for i in range(known['n']):
        row = 12 + 82 * i
        require(unpack_from('<I', payload, row)[0] == i, ('extra_24 ordinal', i))
        for off in offsets:
            dates[off][unpack_from('<I', payload, row + off)[0]] += 1
        for name, off, fmt in (('Twhm', 10, '<b'), ('Tmhm', 11, '<b'), ('Tpvr', 21, '<h')):
            fields[name][unpack_from(fmt, payload, row + off)[0]] += 1
    require(all(c == {0x076c0001: known['n']} for c in dates.values()), 'extra_24 dates')
    t79 = reader.load(ROOT / 'scratch/t79/out/field_map.json')
    for f in t79['table_extra_24']['fields']:
        counts = fields[f['field']]
        domain = f['domain']
        require(sum(counts.values()) == domain['rows'], f['field'])
        if 'histogram' in domain:
            require({str(k): v for k, v in counts.items()} == domain['histogram'], f['field'])
        else:
            require((min(counts), max(counts), len(counts)) == (domain['min'], domain['max'], domain['unique']), f['field'])
    result = {
        'source_field_map': 'scratch/t79/out/field_map.json',
        'table_24': {
            'rows_compared': known['n'], 'footer_off': end, 'diff': p - end,
            'prefixes': [{'selector': flag, 'prefix_bytes': width, 'rows': count}
                         for (flag, width), count in sorted(prefixes.items())],
            'team_offsets': {'Trep': 2, 'Tdvi': 4, 'Tldi': 8, 'Tndi': 12, 'Tsti': 16,
                             'Todo': 29, 'squad_count': 33, 'Tnod': '48+4*n',
                             'TEAM_BASE': '53+4*n'},
            'base_offsets': {'Ttyp': 0, 'Tisn': 1, 'owner': 6, 'Tlna': 10,
                             'Tsna': '15+long_len', 'identity': '20+long_len+short_len'},
            'static_readers': ['0x141053680', '0x141053a80 -> 0x143ee68c0', '0x1411a1280',
                               '0x1411c2780 -> 0x143fff990'],
        },
        'table_extra_24': {
            'in_numeric_inventory': False,
            'rows_compared': cert['record_count'], 'size_equation': cert['size_equation'],
            'static_readers': ['0x1411a1f80', '0x140db8980 -> 0x143b48db0'],
            'dates': [{'wire_offset': off, 'object_offset': hex(dst), 'width': 4,
                       'raw_counts': {hex(k): v for k, v in dates[off].items()}}
                      for off, dst in zip(offsets, destinations)],
            'field_offsets': {'Twhm': 10, 'Tmhm': 11, 'Tpvr': 21},
        },
    }
    (OUT / 'team_field_map_check.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f"TEAM/extra_24 cross-check PASS: {known['n']} rows each; {len(dates)} packed-date lanes")


if __name__ == '__main__':
    main()
