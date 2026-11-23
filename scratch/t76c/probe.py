"""t76c scratch probe: confirm the four row grammars byte-exactly before slotting."""
import runpy, struct, sys

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def ident_ok(raw, end, j):
    if end + 0 > len(raw) or end - 13 < 0:
        return None
    o, a, b = struct.unpack_from('<III', raw, end - 13)
    m = raw[end - 1]
    return (o == j and a == b != 0 and m == 0), (o, a, b, m)


def walk_derby(raw, n):
    pos, rows, bad = 14, [], []
    for j in range(n):
        hit = None
        for k in (2, 4):
            p = pos
            names = []
            ok = True
            for _ in range(k):
                if p + 4 > len(raw):
                    ok = False; break
                ln = struct.unpack_from('<I', raw, p)[0]
                if ln > 300 or p + 4 + ln > len(raw):
                    ok = False; break
                nm = raw[p + 4:p + 4 + ln]
                try:
                    names.append(nm.decode('utf-8'))
                except UnicodeDecodeError:
                    ok = False; break
                p += 4 + ln
            if not ok:
                continue
            end = p + (65 - 4 * k) + 13
            if end > len(raw):
                continue
            t = ident_ok(raw, end, j)
            if t and t[0]:
                hit = (j, pos, end, k, names, t[1])
                break
        if hit is None:
            bad.append((j, pos)); break
        rows.append(hit); pos = hit[2]
    return rows, pos, bad


def walk_weather(raw, n):
    pos, rows, bad = 14, [], []
    for j in range(n):
        ln = struct.unpack_from('<I', raw, pos)[0]
        if ln > 300:
            bad.append((j, pos, 'name len')); break
        nm = raw[pos + 4:pos + 4 + ln]
        try:
            nmd = nm.decode('utf-8')
        except UnicodeDecodeError:
            bad.append((j, pos, 'utf8')); break
        end = pos + 4 + ln + 95 + 13
        t = ident_ok(raw, end, j)
        if not t or not t[0]:
            bad.append((j, pos, 'ident', t)); break
        rows.append((j, pos, end, nmd, t[1], ln)); pos = end
    return rows, pos, bad


def walk_lcrg(raw, n):
    pos, rows, bad = 14, [], []
    for j in range(n):
        hit = None
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            if end > len(raw) - 8 + 1:
                break
            t = ident_ok(raw, end, j)
            if t and t[0]:
                hit = (j, pos, end, ln); break
        if hit is None:
            bad.append((j, pos)); break
        rows.append(hit); pos = hit[2]
    return rows, pos, bad


def walk_agrm(raw, n):
    pos, rows, bad = 14, [], []
    for j in range(n):
        end = pos + 13
        t = ident_ok(raw, end, j)
        if not t or not t[0]:
            bad.append((j, pos, t)); break
        rows.append((j, pos, end, 13)); pos = end
    return rows, pos, bad


if __name__ == '__main__':
    for arch in ('client', 'server'):
        for tid, fn, n in ((56, walk_agrm, 6), (18, walk_derby, 1567),
                           (27, walk_weather, 334), (47, walk_lcrg, 2488)):
            raw = load(arch, tid)
            rows, end, bad = fn(raw, n)
            L = len(raw)
            print(f'{arch} t{tid}: payload={L} rows={len(rows)} end={end} '
                  f'footer={L - end} bad={bad[:3]}')
            if tid == 18:
                from collections import Counter
                print('   k dist', Counter(r[3] for r in rows))
            if tid == 47:
                from collections import Counter
                print('   len hist', dict(sorted(Counter(r[3] for r in rows).items())))
            if tid == 27:
                print('   name len range', min(r[5] for r in rows), max(r[5] for r in rows))
            if rows:
                print('   row0', rows[0][1:5] if tid in (18, 27) else rows[0][1:4])
