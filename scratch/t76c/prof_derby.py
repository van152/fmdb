"""t76c scratch: derby numeric-region structural profile (client vs server)."""
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


def prof(num_blob, label):
    print(f'--- {label}: region len {len(num_blob)}')
    b = num_blob
    print('  hex', b.hex(' '))
    print('  u32', [hex(int.from_bytes(b[i:i + 4], 'little')) if i + 4 <= len(b) else None
                    for i in range(0, len(b), 4)])
    print('  u16', [int.from_bytes(b[i:i + 2], 'little') for i in range(0, len(b) - 1, 2)])


if __name__ == '__main__':
    arch = sys.argv[1] if len(sys.argv) > 1 else 'client'
    raw = load(arch, 18)
    rows, end = rows_derby(raw, NUM[arch])
    print(arch, 'rows', len(rows), 'end', end, 'payload', len(raw), 'trailing', len(raw) - end)
    if arch == 'client':
        sel = [r for r in rows if all(r['names'][2:]) ] if False else None
    # print rows with empty alt names (k=2 set) and with alt names
    a = [r for r in rows if not r['names'][2]][0]
    b = [r for r in rows if r['names'][2]][0]
    prof(a['num'], f'row{a["row"]} 2-name {a["names"]}')
    prof(b['num'], f'row{b["row"]} 4-name {b["names"]}')
    # column stats at fixed offsets
    print(f'\n=== fixed-offset stats ({arch})')
    n = len(rows)
    for off in range(0, NUM[arch] - 1, 2):
        v = [int.from_bytes(r['num'][off:off + 2], 'little') for r in rows]
        u = sorted(set(v))
        print(f'  u16@{off:2} distinct={len(u):6} min={min(v):<6} max={max(v):<10} '
              f'zero={v.count(0):<5} ffff={v.count(0xFFFF):<5} sample={u[:6]}')
    print(f'\n=== u32 stats ({arch})')
    for off in range(0, NUM[arch] - 3, 4):
        v = [int.from_bytes(r['num'][off:off + 4], 'little') for r in rows]
        u = sorted(set(v))
        print(f'  u32@{off:2} distinct={len(u):6} min={min(v):<12} max={max(v):<12} '
              f'zero={v.count(0):<5} ffffffff={v.count(0xFFFFFFFF):<5} sample={u[:5]}')
