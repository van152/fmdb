"""Read-only probe for the client nation row+9 city reference hypothesis."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
NATION = ROOT / 'scratch/t02/inbox/nati/client_db_t10.bin'
EMPTY = 0xFFFFFFFF
CITY_COUNT, CITY_STRIDE = 56293, 43


def u32(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def nation_rows(data, count):
    row, end = 14, len(data) - 8
    for ordinal in range(count):
        if row + 25 > end:
            raise ValueError(f'nation row {ordinal}: truncated prefix')
        pos = row + 25 + 5 * data[row + 24]
        for width in (28, 28, 12):
            if pos + 4 > end:
                raise ValueError(f'nation row {ordinal}: truncated counted block')
            qty = struct.unpack_from('<i', data, pos)[0]
            if qty < 0:
                raise ValueError(f'nation row {ordinal}: negative item count')
            pos += 4 + qty * width
        if pos + 13 > end or u32(data, pos) != ordinal or data[pos + 4:pos + 8] != data[pos + 8:pos + 12] or data[pos + 12] != 0:
            raise ValueError(f'nation row {ordinal}: bad identity at payload offset {pos}')
        yield ordinal, u32(data, pos + 4), u32(data, row + 9)
        row = pos + 13
    if row != end:
        raise ValueError('nation payload does not end at footer')


def probe(nation, city):
    if len(nation) != 24732 or len(city) != 14 + CITY_COUNT * CITY_STRIDE + 8:
        raise ValueError('unexpected client payload size')
    city_ids = set()
    for i in range(CITY_COUNT):
        pos = 14 + CITY_STRIDE * i
        if u32(city, pos + 30) != i or u32(city, pos + 34) != u32(city, pos + 38):
            raise ValueError(f'city row {i}: bad identity')
        city_ids.add(u32(city, pos + 34))
    joined = []
    empty = id_hits = 0
    missing = []
    for ordinal, id_, candidate in nation_rows(nation, 251):
        if candidate == EMPTY:
            empty += 1
            continue
        id_hits += candidate in city_ids
        if candidate >= CITY_COUNT:
            missing.append(ordinal)
            continue
        pos = 14 + CITY_STRIDE * candidate
        lat, lon = struct.unpack_from('<ff', city, pos + 1)
        joined.append({'nation_row': ordinal, 'nation_id': id_, 'city_row': candidate,
                       'city_id': u32(city, pos + 34), 'city_nation_row': u32(city, pos + 10),
                       'lat': lat, 'lon': lon})
    return {'nation_payload_sha256': hashlib.sha256(nation).hexdigest(),
            'city_payload_sha256': hashlib.sha256(city).hexdigest(), 'nation_rows': 251,
            'city_rows': CITY_COUNT, 'city_distinct_ids': len(city_ids), 'sentinel_rows': empty,
            'city_id_hits': id_hits, 'city_ordinal_hits': len(joined), 'out_of_range': missing,
            'same_nation_hits': sum(x['nation_row'] == x['city_nation_row'] for x in joined),
            'examples': [x for x in joined if x['nation_row'] in {0, 1, 55, 139}],
            'cross_nation': [x for x in joined if x['nation_row'] != x['city_nation_row']]}


def selftest():
    b = bytearray(14 + 50 + 8)
    struct.pack_into('<I', b, 14 + 9, EMPTY)
    struct.pack_into('<II', b, 14 + 41, 7, 7)
    assert list(nation_rows(b, 1)) == [(0, 7, EMPTY)]
    b[14 + 49] = 1
    try:
        list(nation_rows(b, 1))
    except ValueError:
        print('PASS: valid row, identity and boundary negative control')
        return 0
    raise AssertionError('invalid boundary accepted')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--city-payload', type=Path, help='optional extracted client table_2; default: read the configured game database')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        if args.city_payload is None:
            dump = runpy.run_path(str(ROOT / 'scripts/fm24_dump.py'))
            city = dump['load_payload'](dump['_reader'](), 'client', 2)
        else:
            city = args.city_payload.read_bytes()
        print(json.dumps(probe(NATION.read_bytes(), city), indent=2))
    except ValueError as exc:
        print(f'CHECK FAILED: {exc}', file=sys.stderr)
        return 1
    except (OSError, RuntimeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
