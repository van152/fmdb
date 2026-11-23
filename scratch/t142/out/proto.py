import sys, time, json, struct
sys.path.insert(0, r"D:\tmp2b\fm24-db\scripts")
sys.dont_write_bytecode = True
import t133_fm24_reader_v2 as t133
import t112_fm24_reader as base
import numpy as np

records, specs = t133.registry(t133.load(t133.TRACE))
l3 = t133.load(t133.L3)
print(len(records), len(specs))


def walk_scalars(prog, data, start, end):
    """(path, off, width, kind, value) for scalar u/id/tag fields; strings skipped."""
    out = []
    p = start
    NUMl = {1: lambda at: data[at], 2: lambda at: struct.unpack_from('<H', data, at)[0],
            4: lambda at: struct.unpack_from('<I', data, at)[0],
            8: lambda at: struct.unpack_from('<Q', data, at)[0]}

    def walk(block, path, tag):
        nonlocal p
        for i, op in enumerate(block):
            key = path + (i,)
            off = p - start
            kind = op[0]
            if kind == 'u':
                n = op[1]
                v = NUMl[n](p) if n in NUMl else int.from_bytes(data[p:p+n], 'little')
                out.append((key, off, n, 'u', v))
                p += n
            elif kind == 's':
                ln = struct.unpack_from('<I', data, p)[0]
                p += 4 + ln
            elif kind == 'id':
                o, u, d = struct.unpack_from('<III', data, p)
                out.append((key, off, 4, 'ord', o))
                out.append((key, off + 4, 4, 'uid', u))
                p += 12
            elif kind in ('v', 'rep'):
                if kind == 'v':
                    w = op[1][1]
                    cnt = NUMl[w](p) if w in NUMl else int.from_bytes(data[p:p+w], 'little')
                    p += w
                    body, count = op[2], cnt
                else:
                    body, count = op[2], op[1]
                for j in range(count):
                    walk(body, key + (j,), tag)
            elif kind in ('if', 'zero', 'tag', 'switch'):
                w = op[1] if kind != 'if' else op[1] if isinstance(op[1], int) else None
                v = NUMl[w](p) if w in NUMl else data[p]
                out.append((key, off, w, 'gate', v))
                p += w
                if kind == 'if':
                    if {'!=': v != op[3], '==': v == op[3]}[op[2]]:
                        walk(op[4], key, tag)
                elif kind == 'tag':
                    for j, (th, b) in enumerate(op[2]):
                        if not th or v >= th:
                            walk(b, key + (j,), v)
                elif kind == 'switch':
                    walk(op[2][v], key + (v,), tag)
            elif kind == 'match':
                if tag == op[1]:
                    walk(op[2], key, tag)
            elif kind == 'choose':
                j = 2 if tag >= op[1] else 3
                walk(op[j], key + (j,), tag)
            else:
                raise ValueError(op)
        return

    walk(prog, (), None)
    return out


def decode_columns(key, limit_rows=None):
    spec = specs[key]
    data = base.Archive(key[0]).payload(key[1])
    nrows = struct.unpack_from('<I', data, 8)[0]
    end = len(data) - base.FOOTER_SIZE
    cols = {}
    t0 = time.perf_counter()
    if key in t133.SELECTORS:
        variants = t133.SELECTORS[key]
        fasts = {k: t133.compile_walk(v) for k, v in variants.items()}
        buckets, flags = {}, {}
        p = base.HEADER_END
        for i in range(nrows):
            flag = data[p]
            if flag not in variants:
                raise SystemExit(f'unexpected selector {flag}')
            body = p + 1
            q = fasts[flag](data, body, end)
            for path, off, w, kind, v in walk_scalars(variants[flag], data, body, q):
                buckets.setdefault((flag, path, off, w, kind), []).append(v)
            flags[flag] = flags.get(flag, 0) + 1
            p = q
        for k, b in buckets.items():
            cols[k] = np.array(b, dtype=np.int64)
        print(key, spec.klass, 'selector flags', flags, 'cols', len(cols), f'{time.perf_counter()-t0:.1f}s')
        return cols, nrows, flags
    if spec.kind == 'fixed':
        reader = base.TableReader(spec, l3)
        reader._fixed_setup()
        fmt = reader._fixed_fmt
        fields = reader._fixed_fields
        p = base.HEADER_END
        mv = memoryview(data)
        # collect per field index
        buckets = [[] for _ in fields]
        for i in range(nrows):
            vals = fmt.unpack_from(mv, p + 1)
            p += 1 + fmt.size
            for b, v in zip(buckets, vals):
                if isinstance(v, int):
                    b.append(v)
        for (nm, off, w, sub), b in zip(fields, buckets):
            name = (nm if sub is None else f'identity.{sub}')
            if b:
                cols[(name, off, w)] = np.array(b, dtype=np.int64)
    else:
        fast = t133.compile_walk(spec.prog)
        buckets = {}
        p = base.HEADER_END
        for i in range(nrows):
            body = p + 1
            q = fast(data, body, end)
            for path, off, w, kind, v in walk_scalars(spec.prog, data, body, q):
                buckets.setdefault((path, off, w, kind), []).append(v)
            p = q
        for k, b in buckets.items():
            if len(b) == nrows:
                cols[k] = np.array(b, dtype=np.int64)
    print(key, spec.klass, spec.kind, nrows, 'cols', len(cols), f'{time.perf_counter()-t0:.1f}s')
    return cols, nrows, None


t0 = time.perf_counter()
if sys.argv[1:2] and sys.argv[1] == 'nat':
    c, n, f = decode_columns(('server', 10))
    nat_ord = c[(('id',), 0, 4, 'ord')] if (('id',), 0, 4, 'ord') in c else None
    # find identity keys
    for k in c:
        if k[3] in ('ord', 'uid'):
            print('IDENT', k, c[k].min(), c[k].max(), c[k].size)
    print()
    c2, n2, f2 = decode_columns(('server', 3))
    for k in c2:
        if k[0] == 0 and k[4] == 'u':
            print('CLUB', k, c2[k].min(), c2[k].max(), len(np.unique(c2[k])))
else:
    c, n, f = decode_columns(('server', 3))
    print('CLUB total', time.perf_counter() - t0)
    for k in list(c):
        a = c[k]
        print(' ', k, 'min', a.min(), 'max', a.max(), 'distinct', len(np.unique(a)), 'n', a.size)
