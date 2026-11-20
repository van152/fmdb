"""t76c scratch: lcrg business-region column profile (row-relative, pre-identity)."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def rows_lcrg(raw):
    pos, rows = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                rows.append(dict(row=j, start=pos, end=end, ln=ln, k=k,
                                 biz=raw[pos:end - 13],
                                 uid=a))
                pos = end
                break
    return rows


def main(arch):
    raw = load(arch, 47)
    rows = rows_lcrg(raw)
    print('rows', len(rows), 'end', rows[-1]['end'], 'payload', len(raw))
    print('k histogram', dict(sorted(Counter(r['k'] for r in rows).items())))
    # aligned u32 columns within business region (all rows share >=28 bytes)
    n = len(rows)
    print('\n--- u32 columns at fixed offsets 0,4,8,12,16,20,24 over all rows')
    for off in (0, 4, 8, 12, 16, 20, 24):
        vals = [int.from_bytes(r['biz'][off:off + 4], 'little') for r in rows]
        u = sorted(set(vals))
        print(f'@{off:3} distinct={len(u):5} min={min(vals):<12} max={max(vals):<12} '
              f'n_zero={vals.count(0)} n_ff={vals.count(0xFFFFFFFF)} sample={u[:6]}')
    print('\n--- u8/u16 columns 0..27')
    for off in range(0, 28):
        v = [r['biz'][off] for r in rows]
        u = sorted(set(v))
        print(f'u8 @{off:3} distinct={len(u):4} min={min(v):<5} max={max(v):<5} sample={u[:8]}')
    # u16 at even offsets
    print('\n--- u16 columns')
    for off in range(0, 26, 2):
        v = [int.from_bytes(r['biz'][off:off + 2], 'little') for r in rows]
        u = sorted(set(v))
        print(f'u16 @{off:3} distinct={len(u):5} min={min(v):<8} max={max(v):<8} sample={u[:8]}')
    # tail 5k bytes: dump for k=1 and k=2 rows
    for kk in (1, 2, 3):
        r = next(r for r in rows if r['k'] == kk)
        print(f'\n--- k={kk} row{r["row"]} len={r["ln"]} biz={r["biz"].hex(" ")}')
    # are the extra 5 bytes at the end of biz region or spread?
    r0 = next(r for r in rows if r['k'] == 0)
    r1 = next(r for r in rows if r['k'] == 1)
    print('\nk=0 biz', r0['biz'].hex(' '))
    print('k=1 biz', r1['biz'].hex(' '))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'client')
