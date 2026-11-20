"""t76c scratch: per-offset statistics over variable-row business regions."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

ID = 13


def rows_weather(raw):
    pos, rows = 14, []
    for j in range(334):
        ln = struct.unpack_from('<I', raw, pos)[0]
        end = pos + 4 + ln + 95 + ID
        rows.append(dict(row=j, start=pos, end=end, namelen=ln,
                         name=raw[pos + 4:pos + 4 + ln].decode('utf-8'),
                         mid=raw[pos + 4 + ln:end - ID],
                         ident=struct.unpack_from('<IIIB', raw, end - 13)))
        pos = end
    return rows, pos


def rows_lcrg(raw):
    pos, rows = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                rows.append(dict(row=j, start=pos, end=end, len=ln, k=k,
                                 biz=raw[pos:end - 13],
                                 ident=(o, a, b)))
                pos = end
                break
    return rows, pos


def rows_derby(raw, const, num=36):
    pos, rows = 14, []
    for j in range(1567):
        p, names, nb = pos, [], 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            if ln > 400:
                break
            names.append(raw[p + 4:p + 4 + ln].decode('utf-8'))
            nb += ln
            p += 4 + ln
        end = pos + nb + 16 + num + ID
        rows.append(dict(row=j, start=pos, end=end, names=names,
                         num=raw[pos + 16 + nb:end - ID],
                         ident=struct.unpack_from('<IIIB', raw, end - 13)))
        pos = end
    return rows, pos


def colstats(rows, key, width, label, maxoff=None):
    cols = {}
    for r in rows:
        b = r[key]
        for off in range(len(b) if maxoff is None else maxoff):
            if off + width <= len(b):
                cols.setdefault(off, []).append(int.from_bytes(b[off:off + width], 'little'))
    print(f'--- {label} width={width}')
    for off in sorted(cols):
        v = cols[off]
        u = sorted(set(v))
        print(f'  @{off:3} ({len(v)}) distinct={len(u):5} min={min(v):<12} max={max(v):<12} '
              f'sample={u[:6]}')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'weather'
    arch = sys.argv[2] if len(sys.argv) > 2 else 'client'
    raw = load(arch, 18 if which == 'derby' else 27 if which == 'weather' else 47)
    if which == 'weather':
        rows, end = rows_weather(raw)
        colstats(rows, 'mid', 1, 'weather mid u8', 95)
    elif which == 'lcrg':
        rows, end = rows_lcrg(raw)
        colstats(rows, 'biz', 1, 'lcrg biz u8', 28)
    print('rows', len(rows), 'end', end, 'taillen', len(raw) - end)
