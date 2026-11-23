"""t76c scratch: byte-level profile of derby numeric region + agreement rows."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

NUM = {'client': 36, 'server': 42}


def rows_derby(raw, num):
    pos, rows = 14, []
    for j in range(1567):
        p, names, nb = pos, [], 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            names.append(raw[p + 4:p + 4 + ln].decode('utf-8'))
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        rows.append(dict(row=j, start=pos, end=end, names=names,
                         num=raw[pos + 16 + nb:end - 13]))
        pos = end
    return rows, pos


for arch in ('client', 'server'):
    raw = load(arch, 18)
    rows, end = rows_derby(raw, NUM[arch])
    n = len(rows)
    print('=' * 20, arch, 'rows', len(rows), 'end', end, 'payload', len(raw))
    print('--- byte profile')
    for off in range(NUM[arch]):
        v = [r['num'][off] for r in rows]
        c = Counter(v)
        top = c.most_common(4)
        print(f'  b{off:2} distinct={len(c):4} min={min(v):<4} max={max(v):<4} '
              f'zero={v.count(0):<5} top={top}')
    print('--- u32 aligned')
    for off in range(0, NUM[arch] - 3, 4):
        v = [int.from_bytes(r['num'][off:off + 4], 'little') for r in rows]
        print(f'  u32@{off:2} distinct={len(set(v)):5} min={min(v):<12} max={max(v):<12} '
              f'ff={v.count(0xFFFFFFFF)}')
    raw56 = load(arch, 56)
    print('--- agreement rows')
    for j in range(6):
        b = raw56[14 + j * 13:14 + j * 13 + 13]
        print(' ', j, b.hex(' '), struct.unpack('<IIIB', b))
