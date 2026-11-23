#!/usr/bin/env python3
"""Read-only FM24 database walker for the v0xdf1 server/client archives."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import struct
import sys
import time

sys.dont_write_bytecode = True
import t112_fm24_reader as base

# Prefer the repository's designated vendor directory over site-packages.
if (base.UPSTREAM_ZSTD / 'zstandard').is_dir():
    sys.path.insert(0, str(base.UPSTREAM_ZSTD))

TRACE = base.ROOT / 'scratch/t121/out/wire_traces_79of79.json'
L3 = base.ROOT / 'scratch/t121/out/master_79of79_l3.json'
OUT = base.ROOT / 'scratch/t133/out'
VERSION = 0xDF1
U8, U16, U32, U64 = base._P1, base._P2, base._P4, base._P8
I8, I16, I32 = ('i', 1), ('i', 2), ('i', 4)
STR, ID = base._STR, base._ID
WireError = base.WireError
NUM = {2: struct.Struct('<H').unpack_from, 4: struct.Struct('<I').unpack_from,
       8: struct.Struct('<Q').unpack_from}
IDENT = struct.Struct('<III').unpack_from


def vec(count, *ops):
    return ('v', count, ops)


def when(width, predicate, value, *ops):
    return ('if', width, predicate, value, ops)


def zero(width, callee):
    """Read a proven-empty container; reject rather than guess its element grammar."""
    return ('zero', width, callee)


# 0xdf1 paths only; other payload versions are rejected before any row walk.
# 141191E80 / 14156AF70: the latter's final byte is flushed by 1412E6FF0.
FUTURE = (U32,) * 6 + (U8, U32, U8, U16,
    vec(I16, *([U32] * 8), U8, U32, U8), U8, U8, U8, U64,
    vec(U8, U16, U32, ('u', 10), U8, ('u', 9), U32, U8), U8)
# 1415782C0 -> 144519690, including 14156AB70 -> 144509AC0.
LOAN = (U32,) * 5 + (U8, U32, U32, U8, U32, U64, U8, U32, U32, U16, U32, U8, U32)
HOF = (U32, U32, STR, STR, STR, U32, vec(U32, U32, U32, U16, vec(U32, U16)), ID)
PAST = (U32,) * 5 + (U8, U8, U8, vec(U8, *FUTURE), when(1, '!=', 0, *LOAN), ID)
TRADE_REF = vec(U32, U32)
TRADE_A = vec(U32, U8, U32, U8, U8, U8, U32, U8, U16)
TRADE_B = vec(U32, U8, U32, U32, U8, U8)
TRADE = (U32, U32, TRADE_REF, TRADE_REF, TRADE_REF, TRADE_REF,
         U32, U32, TRADE_A, TRADE_B, TRADE_A, TRADE_B, ID)

# NATIONAL_TEAM_CONTAINER: t49 static read plan, checked against 14105D510.
# Sub-record tag gates from 141571860 and its 141572E80 element loop.
# A guard reads the tag exactly once, then evaluates the rules in wire order.
NTC_PREF = ('tag', 1, (
    (0, (STR, STR, STR, U16, U8, U16, U32, U32)),
    (2, (U32, vec(U32, U8, U32, U16), U8, U32)),
    (0, (U8, U8, U8, U8)), (5, (U8, U32)),
    (0, (U16, U16, U16, U16, U8, U8, U8, U32, U32)),
    (3, (U8,)), (4, (U8,)), (6, (U8,))))
NTC_TAGGED10 = ('tag', -2, ((0, (U32, U8, U8, ('choose', 2, (U16,), (U8,)), U8)),
                           (3, (U8,))))
NTC_PREFIX = (U16, U32, U32, U32, vec(U32, U32, U32),
    U32, U16, U32, U16, U16, U8, U32, U8, U16, U32, U16, U32,
    zero(4, '0x140839290'), zero(4, '0x140839480'),
    vec(U32, U16), vec(U32, U16), vec(U8, U32), vec(U16, U32),
    ('rep', 20, (vec(U8, U32),)), vec(U16, U32),
    vec(U16, NTC_PREF), vec(U16, NTC_PREF),
    when(1, '!=', 0, U8, vec(U32, U8, U32, U32)), vec(U16, U32, U16, U8, U8, U8),
    vec(U32, U8, U8, U32, U8, ('u', 11)), vec(U32, U8, U8, U32, U8, ('u', 11)),
    vec(U16, U32, U32, U32, U8, U8), vec(U32, U8, U8, U32, U8, U8, U8, U8),
    U8, U32, when(1, '!=', 0, U32, vec(U32, NTC_TAGGED10)))
NTC_COMMON = (U32,) + (U8,) * 7 + (U32,) + (U8,) * 16 + (
    vec(U8, U32, U8, U8, U8, U8, U8), vec(U8, U32, U8, U8, U8, U8),
    vec(U8, U32, U8, U8, U8, U8), U16, U16, U16, U16)
NTC_SERVER_TAIL = (U32,) * 7 + (U8, U32, U8, U16, U8) + (vec(U8, U32),) * 3 + (
    (U8,) * 13) + (U32, U32, U16, U8, U8, U16, U8, U16) + (vec(U8, U32),) * 5 + (
    vec(U8, ('u', 16)), vec(U16, U32, U32, U64, U16, U32, U32, U8, U8), ID)

# 1411D1730 TEAM_CONTAINER tail (shared with 14105D510).
CONTAINER_FULL = (vec(U8, U32), vec(U8, U32), vec(I8, U32), vec(I8, U32), vec(U8, U32),
    vec(U8, ('u', 16)), vec(I16, U32, U32, U64, U16, U32, U32, U8, U8))
# 140E5B1A0; selector 12 enters through 14157D9F0 -> 14452A1A0.
CLUB_HEAD = (U32,) * 5 + (('u', 6), STR, STR)
CLUB_EXT = (U8, U16, U32, U8, vec(I8, U32),
    ('switch', 1, {0: (U32, U8, ('u', 3), ('u', 13), U32, ('u', 20)), 2: ()},
     '0x141477160 (CLUB +0x150 subtype 1 not reduced)'),
    vec(I8, U8, U8, U32, U32, U8, U32, U16, U8, U8, U8, U32),
    vec(I8, U32, U32, U32), U16, U32)
CLUB_CLIENT = CLUB_HEAD + (U8, U16, ID)
CLUB_SERVER = CLUB_HEAD + CLUB_EXT + (U8, U16) + CONTAINER_FULL + (ID,)

# 141053680 NATIONAL_TEAM -> 1411A1280 TEAM -> 1411C2780 TEAM_BASE.
TEAM_BASE = (U8,) * 6 + (U32, STR, U8, STR, U8, ID)
TEAM = (U8, U8, U16) + (U32,) * 6 + (U8, U32, vec(U16, U32), U32, U32,
    U8, U8, U8, U8, U8, U32, U8) + TEAM_BASE
NATIONAL_TEAM = (U32, U32, U32, U8) + (U32,) * 7 + (U8,) * 7 + (
    vec(I8, U8, U32, U32, U8),) + TEAM

# 140ED1440 -> 143CAA6D0 -> 140EB7A00; a8=0, a6=1.
# Both stat-A branches transfer seven bytes; older tags then rewrite one in memory.
COMP_STAT_A = ('tag', 1, ((0, (U8,) * 7),))
COMP_STAT_B = ('tag', 1, ((0, (('choose', 3, (U8,) * 15,
                           (('choose', 2, (U8,) * 14, (U8,) * 12),)),)),))
COMP_A8 = ('tag', 1, ((0, (U32, U16, U16) + (U32,) * 6), (2, (U32,)),
    (0, (U32, U32, U8, ('choose', 3, (U16,), (U8,)), U16, U16, U32))))
COMP_E8_ITEM = ('tag', -2, ((0, (U32, U8, U8, ('choose', 2, (U16,), (U8,)), U8)),
                          (3, (U8,))))
COMP_D = (U32, U32, U8, U8, U32, U8)
COMP_NAMES = ('tag', 1, ((0, (U8, U8, U8, U8, COMP_STAT_A, COMP_STAT_B,
                             U8, U32, U32, ('match', 4, (STR, STR)))),))
COMP = (U8, U8, U8, U16, U16, U16, U16, U16, U8, COMP_NAMES,
    U32, U32, U32, U32, U16, U16, U32, U8, U16, U16, U16, U64, U64, U64, U64,
    vec(U32, U16), when(1, '!=', 0, COMP_A8), U32, U8, U8, U8, U8,
    zero(1, '0x140839480 (+0xe0 has no live nonzero witness)'),
    vec(I32, U8, U32, U16, U8, U8), when(1, '!=', 0, U32, vec(U32, COMP_E8_ITEM)),
    when(1, '!=', 0, U8, vec(U32, U8, U8, vec(U32, U8, U8, U8, U8, U32, U32))),
    when(1, '!=', 0, U8, ('rep', 4, (U8, U8, U8, U8, U8, U8))),
    U8, when(1, '!=', 0, *COMP_D), when(1, '!=', 0, *COMP_D), vec(I16, U8, U16, U16),
    U32, U16, U16, U16, U16, U16, U32, U32, U32, U32, when(1, '!=', 0, U16),
    U32, U32, U8, U8, U8, ID)

PROGRAMS = {
    ('server', 29): LOAN + (ID,), ('server', 32): FUTURE + (ID,),
    ('server', 36): HOF, ('server', 71): PAST, ('server', 72): TRADE,
    ('client', 9): NTC_COMMON + (U8, U16, ID),
    ('server', 9): NTC_PREFIX + NTC_COMMON + NTC_SERVER_TAIL,
    ('server', 25): COMP,
}
SELECTORS = {('client', 3): {0: CLUB_CLIENT, 12: (U32, U8) + CLUB_CLIENT},
             ('server', 3): {0: CLUB_SERVER, 12: (U32, U8) + CLUB_SERVER},
             ('server', 24): {10: TEAM, 11: NATIONAL_TEAM}}
NEW_TABLES = PROGRAMS.keys() | SELECTORS.keys()
NEW_FIXED = {('server', 0), ('client', 0)}
# v0xdf1 direct database-reference path of 140E48DB0, in wire order.
AWARD_WIDTHS = (1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 4, 4, 4, 4, 1, 1,
                1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 4, 12)
BLOCKERS = {}
NATION_HELPERS = {
    # Recovered C replaces two of t112's equal-width/empty-string shorthands.
    tuple(base._T10_CFD70): (U8, STR, STR, STR, STR, U32, U32, U32, U32, U32),
    tuple(base._T10_72F60): (U8, U32, U32, U8, U8, U8, U8, U8),
}
# Actual writes in 144519690 / 144509AC0 at v0xdf1. t121's t29
# sample entered an older version path, so join on mem_off, not its offsets.
LOAN_DESTS = (24, 40, 32, 48, 52, None, 60, 64, 68, 56, 72, 102, 88, 92, 100, 84, 103, 96)


def fixed_size(ops):
    total = 0
    for op in ops:
        if op[0] == 'u':
            total += op[1]
        elif op[0] == 'id':
            total += 12
        elif op[0] == 'rep':
            size = fixed_size(op[2])
            if size is None:
                return None
            total += op[1] * size
        else:
            return None
    return total


def compile_walk(ops):
    """Compile only in-process grammar constants, never JSON or payload text."""
    src = ['def walk(b, p, end, H=NUM[2], I=NUM[4]):']
    serial = 0

    def emit(block, indent, tag=None):
        nonlocal serial
        for op in block:
            kind = op[0]
            n = fixed_size((op,))
            if n is not None:
                src.append(f'{indent}p += {n}')
                continue
            serial += 1
            var = f'n{serial}'
            if kind in ('v', 's', 'if', 'zero', 'tag', 'switch'):
                w = op[1][1] if kind == 'v' else 4 if kind == 's' else abs(op[1])
                get = {1: 'b[p]', 2: 'H(b, p)[0]', 4: 'I(b, p)[0]'}[w]
                src.extend((f'{indent}if p + {w} > end: raise WireError(f"short {kind} control at {{p}}")',
                            f'{indent}{var} = {get}', f'{indent}p += {w}'))
                if kind == 'v' and op[1][0] == 'i':
                    src.append(f'{indent}if {var} >= {1 << (8*w-1)}: raise WireError(f"negative vector count at {{p-{w}}}")')
                if kind == 'tag' and op[1] < 0:
                    src.append(f'{indent}if {var} >= {1 << (8*w-1)}: {var} -= {1 << (8*w)}')
            if kind == 's':
                src.append(f'{indent}p += {var}')
            elif kind in ('v', 'rep'):
                count = var if kind == 'v' else op[1]
                width = fixed_size(op[2])
                if width is not None:
                    src.append(f'{indent}p += {count} * {width}')
                else:
                    src.append(f'{indent}for _ in range({count}):')
                    emit(op[2], indent + '    ', tag)
            elif kind == 'if':
                src.append(f'{indent}if {var} {op[2]} {op[3]}:')
                emit(op[4], indent + '    ', tag)
            elif kind == 'zero':
                src.append(f'{indent}if {var}: raise WireError({("missing nonempty path " + op[2])!r})')
            elif kind == 'tag':
                for threshold, body in op[2]:
                    if threshold:
                        src.append(f'{indent}if {var} >= {threshold}:')
                    emit(body, indent + ('    ' if threshold else ''), var)
            elif kind == 'switch':
                for idx, (value, body) in enumerate(op[2].items()):
                    keyword = 'elif' if idx else 'if'
                    src.append(f'{indent}{keyword} {var} == {value}:')
                    if body:
                        emit(body, indent + '    ', tag)
                    else:
                        src.append(f'{indent}    pass')
                src.append(f'{indent}else: raise WireError({op[3]!r})')
            elif kind == 'match':
                src.append(f'{indent}if {tag} == {op[1]}:')
                emit(op[2], indent + '    ', tag)
            elif kind == 'choose':
                src.append(f'{indent}if {tag} >= {op[1]}:')
                emit(op[2], indent + '    ', tag)
                src.append(f'{indent}else:')
                emit(op[3], indent + '    ', tag)
            else:
                raise ValueError(op)

    emit(ops, '    ')
    src.extend(('    if p > end: raise WireError(f"row end {p} exceeds {end}")', '    return p'))
    env = {'NUM': NUM, 'WireError': WireError}
    exec('\n'.join(src), env)
    return env['walk']


def sample_walk(ops, data, start, end):
    """Read sample values; binding uses a stable grammar path, not later wire offsets."""
    fields = []
    p = start

    def take(n):
        nonlocal p
        if p + n > end:
            raise WireError(f'short read of {n} bytes at {p}')
        at = p
        p += n
        return at

    def number(n):
        at = take(n)
        if n == 1:
            return data[at]
        if n in NUM:
            return NUM[n](data, at)[0]
        return data[at:p].hex()

    def walk(block, path, tag=None):
        for i, op in enumerate(block):
            key = path + (i,)
            off = p - start
            kind = op[0]
            if kind == 'id':
                val = dict(zip(('ordinal', 'uid', 'dbid'), IDENT(data, take(12))))
            elif kind == 'u':
                val = number(op[1])
            elif kind == 's':
                n = number(4)
                at = take(n)
                val = data[at:p].decode('utf-8', 'replace')
            elif kind == 'rep':
                for j in range(op[1]):
                    walk(op[2], key + (j,), tag)
                continue
            elif kind == 'v':
                width = op[1][1]
                n = number(width)
                if op[1][0] == 'i' and n >= 1 << (8 * width - 1):
                    raise WireError(f'negative vector count at {p - width}')
                fields.append((key, off, width, 'count', n))
                for j in range(n):
                    walk(op[2], key + (j,), tag)
                continue
            elif kind == 'zero':
                val = number(op[1])
                if val:
                    raise WireError(f'missing nonempty path {op[2]}')
            elif kind == 'if':
                val = number(op[1])
                fields.append((key, off, op[1], 'gate', val))
                if {'!=': val != op[3], '==': val == op[3]}[op[2]]:
                    walk(op[4], key, tag)
                continue
            elif kind == 'tag':
                width = abs(op[1])
                val = number(width)
                if op[1] < 0 and val >= 1 << (8 * width - 1):
                    val -= 1 << (8 * width)
                fields.append((key, off, width, 'tag', val))
                for j, (threshold, body) in enumerate(op[2]):
                    if not threshold or val >= threshold:
                        walk(body, key + (j,), val)
                continue
            elif kind == 'switch':
                val = number(op[1])
                fields.append((key, off, op[1], 'tag', val))
                if val not in op[2]:
                    raise WireError(op[3])
                walk(op[2][val], key + (val,), tag)
                continue
            elif kind == 'match':
                if tag == op[1]:
                    walk(op[2], key, tag)
                continue
            elif kind == 'choose':
                j = 2 if tag >= op[1] else 3
                walk(op[j], key + (j,), tag)
                continue
            else:
                raise ValueError(op)
            fields.append((key, off, p - start - off, kind, val))

    walk(ops, ())
    return fields, p


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def registry(traces):
    # Retain exactly the t112 supported set and baseline grammars. t121 traces
    # can be sample-only, including misframed rows, so are not a stride oracle.
    specs, _ = base.build_registry(base.load_traces())
    by_key = {(s.archive, s.tid): s for s in specs}
    nation = by_key[('server', 10)]
    nation.prog = tuple((op[0], op[1], NATION_HELPERS.get(tuple(op[2]), op[2]))
                        if op[0] == 'v' else op for op in nation.prog)
    records = {(t['archive'], t['table_id']): t for t in traces['tables']}
    if len(records) != len(traces['tables']) or not by_key.keys() <= records.keys():
        raise ValueError('t121 trace inventory inconsistent with baseline')
    for key, t in records.items():
        if key in NEW_TABLES:
            spec = by_key[key] = base.TableSpec(*key, t['class'], 'variable')
            spec.prog = PROGRAMS.get(key)
        elif key in NEW_FIXED:
            spec = by_key[key] = base.TableSpec(*key, t['class'], 'fixed')
            reads = t['row0_reads']
            if tuple(r['n'] for r in reads) != AWARD_WIDTHS:
                raise ValueError(f'{key}: AWARD trace changed')
            offset = 0
            for r in reads:
                if r['wire_pos'] != offset:
                    raise ValueError(f'{key}: noncontiguous AWARD trace')
                offset += r['n']
            spec.rowlen = offset
            spec.row0_reads = reads
    return records, by_key


def bind_sample(fields, trace, l3, key):
    compatible = {(r['wire_pos'], r['n']) for r in trace['row0_reads'] if r['n']}
    l3map = base._l3_name_map(l3, key[1], key[0])
    by_dest = {}
    if key == ('server', 29):
        rec = next(t for t in l3['tables'] if t['table_type'] == 29)
        by_dest = {j['mem_off']: j['fourcc'] for j in rec['joined_l3_fourccs']
                   if j['archive'] == 'server' and j['in_slot_off'] == 0}
    names, named = {}, set()
    for path, off, width, kind, _ in fields:
        nm = None
        if kind == 'u':
            if by_dest:
                nm = by_dest.get(LOAN_DESTS[path[0]])
            elif (off, width) in compatible:
                nm = l3map.get(off)
        names[path] = nm or ('identity' if kind == 'id' else f'col_{off}')
        if nm:
            named.add(nm)
    return names, len(named)


def row0_trace_info(trace, data, body, row_end):
    """Compare only the captured byte prefix if a trace hex field was truncated."""
    cursor = 0
    mismatches = 0
    reads = trace['row0_reads']
    for r in reads:
        off, n = r['wire_pos'], r['n']
        raw = r.get('hex', '').removesuffix('...')
        capture = bytes.fromhex(raw)
        if off != cursor or off + n > row_end - body or len(capture) > n or data[body+off:body+off+len(capture)] != capture:
            mismatches += 1
        cursor = off + n
    return dict(reads=len(reads), canonical_fields=len(trace['canonical_fields']),
                trace_end=cursor, parser_end=row_end-body, mismatches=mismatches,
                status='mismatch' if mismatches else 'exact' if cursor == row_end-body else 'prefix')


def row_sample(fields, names, flag):
    result = {'row_flag': flag}
    for path, _, _, kind, val in fields:
        nm = names.get(path, 'identity' if kind == 'id' else 'op_' + '_'.join(map(str, path)))
        if nm in result:
            nm += '@' + '.'.join(map(str, path))
        result[nm] = val
    return result


def verify_table(spec, trace, l3, data, samples=3, variant_samples=False):
    start = time.perf_counter()
    end, p, done = len(data) - base.FOOTER_SIZE, base.HEADER_END, 0
    nrows = None
    error = None
    flags, sizes = Counter(), Counter()
    rows, examples = [], {}
    reference = None
    named = 0
    key = spec.archive, spec.tid
    try:
        if end < p or not data.startswith(base.DAT_MAGIC) or data[end] != 0:
            raise WireError('invalid payload envelope')
        version = NUM[2](data, 6)[0]
        if version != VERSION:
            raise WireError(f'unsupported database version {version:#x}')
        nrows = NUM[4](data, 8)[0]
        if nrows != trace['rows_header']:
            raise WireError(f'archive row count {nrows} differs from t121 inventory')
        if spec.kind == 'fixed':
            reader = base.TableReader(spec, l3)
            reader._fixed_setup()
            fmt = reader._fixed_fmt
            if fmt.size != spec.rowlen or end != p + nrows * (1 + fmt.size):
                raise WireError('fixed stride/geometry mismatch')
            named = reader.l3_named
            unpack = fmt.unpack_from
            mv = memoryview(data)
            for i in range(nrows):
                flag = data[p]
                if key in NEW_FIXED:
                    if flag != 0:
                        raise WireError(f'AWARD selector {flag}')
                    if NUM[4](data, p + 1 + fmt.size - 12)[0] != i:
                        raise WireError('AWARD identity ordinal mismatch')
                if i == 0:
                    reference = row0_trace_info(trace, data, p + 1, p + 1 + fmt.size)
                flags[flag] += 1
                if i < samples:
                    row, p = reader.decode_row_into(mv, p + 1, end)
                    rows.append({'row_flag': flag, **row})
                else:
                    unpack(data, p + 1)
                    p += 1 + fmt.size
                done += 1
            sizes[fmt.size] = done
        elif spec.kind == 'variable':
            ops = spec.prog
            variants = SELECTORS.get(key)
            fast = compile_walk(ops) if variants is None else None
            variant_fast = {k: compile_walk(v) for k, v in variants.items()} if variants else None
            names = {}
            trace_flag = None
            validate_identity = key in NEW_TABLES
            for i in range(nrows):
                if p >= end:
                    raise WireError('missing row flag')
                flag = data[p]
                if variants is not None:
                    if flag not in variants:
                        raise WireError(f'unexpected selector {flag} at {p}')
                    ops, fast = variants[flag], variant_fast[flag]
                elif key in PROGRAMS and flag != 0:
                    raise WireError(f'unexpected selector {flag} at {p}')
                body = p + 1
                q = fast(data, body, end)
                if validate_identity and NUM[4](data, q - 12)[0] != i:
                    raise WireError(f'identity ordinal mismatch at {q - 12}: expected {i}, got {NUM[4](data, q - 12)[0]}')
                collect_variant = variant_samples and variants is not None and flag not in examples
                if i == 0 or i < samples or collect_variant:
                    fields, sample_end = sample_walk(ops, data, body, end)
                    if sample_end != q:
                        raise WireError('sample walker and compiled walker disagree')
                    if i == 0:
                        names, named = bind_sample(fields, trace, l3, key)
                        trace_flag = flag
                        reference = row0_trace_info(trace, data, body, q)
                        if key == ('server', 29):
                            reference['status'] = 'legacy_version_path'
                    row = row_sample(fields, names if variants is None or flag == trace_flag else {}, flag)
                    if i < samples:
                        rows.append(row)
                    if collect_variant:
                        examples[flag] = dict(row_index=i, row_start=p, row=row)
                flags[flag] += 1
                sizes[q - body] += 1
                p = q
                done += 1
        elif nrows or p != end:
            raise WireError('invalid empty table')
        if p != end:
            raise WireError(f'footer delta {p - end:+d}')
    except (WireError, struct.error) as exc:
        error = f'row {done} at {p}: {exc}'
    return dict(archive=spec.archive, table_id=spec.tid, **{'class': spec.klass}, kind=spec.kind,
                rows_header=nrows, rows_decoded=done, end_pos=p, footer_off=end, diff=p-end,
                footer_closed=error is None and done == nrows and p == end,
                footer9_hex=data[end:].hex() if end >= 0 else '', error=error,
                elapsed_ms=round(1000 * (time.perf_counter() - start), 1),
                flags_seen={hex(k): v for k, v in sorted(flags.items())},
                row_len_min=min(sizes, default=None), row_len_max=max(sizes, default=None),
                l3_named_fields=named, sample_rows=rows, row0_trace=reference,
                selector_samples={hex(k): v for k, v in sorted(examples.items())})


def verify_all(records, specs, l3):
    start = time.perf_counter()
    arcs = {}
    tables = {}
    for key, t in sorted(records.items()):
        arch, tid = key
        spec = specs.get(key)
        status = dict(archive=arch, table_id=tid, **{'class': t['class']},
                      rows_header=t['rows_header'], rows_decoded=0, footer_closed=False,
                      diff=None, l3_named_fields=0, sample_rows=[])
        if spec is None:
            status.update(kind='skipped', reason=BLOCKERS.get(key, 'no proven grammar'))
        else:
            try:
                if arch not in arcs:
                    arc = base.Archive(arch)
                    actual = {name for name in arc.entries if name.startswith(f'{arch}_db/table_')
                              and name.endswith('.dat') and name.rsplit('table_', 1)[1][:-4].isdigit()}
                    expected = {f'{arch}_db/table_{n}.dat' for side, n in records if side == arch}
                    if actual != expected:
                        raise WireError(f'{arch} numeric table inventory does not match t121')
                    arcs[arch] = arc
                status = verify_table(spec, t, l3, arcs[arch].payload(tid), variant_samples=True)
            except (RuntimeError, ValueError, OSError, KeyError, struct.error) as exc:
                status.update(kind=spec.kind, error=f'archive or parser: {exc}')
        tables[f'{arch}/{tid}'] = status
    results = list(tables.values())
    closed = sum(r['footer_closed'] for r in results)
    skipped = sum(r['kind'] == 'skipped' for r in results)
    failed = len(results) - closed - skipped
    return dict(status='complete' if closed == len(results) else 'partial',
                schema_id='fm24.t133.reader_v2_verify', schema_version=1,
                inputs=[str(p.relative_to(base.ROOT)) for p in (TRACE, L3, base.TRACE_JSON, base.DB_DIR)],
                zstandard_module=base._zstd().__file__,
                elapsed_total_ms=round(1000 * (time.perf_counter() - start), 1),
                summary=dict(tables_total=len(results), tables_closed=closed, tables_failed=failed,
                             tables_skipped=skipped, rows_decoded_total=sum(r['rows_decoded'] for r in results),
                             rows_footer_closed_total=sum(r['rows_decoded'] for r in results if r['footer_closed']),
                             l3_named_field_total=sum(r['l3_named_fields'] for r in results if r['footer_closed']),
                             l3_source_mapping_total=l3['summary']['joined_l3_fourccs']),
                tables=tables)


def _test_controls():
    ops = (vec(I16, U32, STR), when(1, '!=', 0, zero(4, 'test guard')), ID)
    fast = compile_walk(ops)
    fixture = struct.pack('<HI', 1, 123) + struct.pack('<I', 3) + b'abc' + b'\x01' + bytes(16)
    fields, end = sample_walk(ops, fixture, 0, len(fixture))
    if end != len(fixture) or fast(fixture, 0, end) != end or fields[2][-1] != 'abc':
        return False
    for damaged in (b'\xff\xff' + fixture[2:], fixture[:14] + b'\x01' + fixture[15:], fixture[:-1],
                    fixture[:6] + b'\xff' * 4 + fixture[10:]):
        for walk in (fast, lambda b, p, end: sample_walk(ops, b, p, end)):
            try:
                walk(damaged, 0, len(damaged))
            except WireError:
                continue
            return False
    return True


def selftest(records, specs, l3):
    all_ok = True

    def check(name, ok, detail=''):
        nonlocal all_ok
        all_ok = all_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")

    check('registry', len(records) == 79 and records.keys() - specs.keys() == BLOCKERS.keys())
    arcs = {a: base.Archive(a) for a in ('client', 'server')}
    for key in sorted(NEW_TABLES | NEW_FIXED | {('server', 45), ('server', 2), ('server', 10), ('client', 10)}):
        data = arcs[key[0]].payload(key[1])
        spec, trace = specs[key], records[key]
        res = verify_table(spec, trace, l3, data, samples=2, variant_samples=True)
        check(f'{spec.key} all rows', res['footer_closed'], res['error'] or f"{res['rows_decoded']} diff={res['diff']}")
        if key in NEW_TABLES | NEW_FIXED:
            # Remove one byte before the footer. Neither path may read into it.
            truncated = data[:-10] + data[-9:]
            negative = verify_table(spec, trace, l3, truncated, samples=0)
            check(f'{spec.key} truncated body', not negative['footer_closed'])
            expected = ('legacy_version_path' if key == ('server', 29) else 'prefix'
                        if key in SELECTORS else 'exact')
            ref = res['row0_trace'] or {}
            check(f'{spec.key} row0 trace', ref.get('status') == expected and ref.get('mismatches') == 0, str(ref))
        if key in SELECTORS:
            modes = {hex(v) for v in SELECTORS[key]}
            check(f'{spec.key} selector coverage', modes == res['selector_samples'].keys())
            wrong = data[:13] + b'\xff' + data[14:]
            negative = verify_table(spec, trace, l3, wrong, samples=0)
            check(f'{spec.key} invalid selector', not negative['footer_closed'] and negative['rows_decoded'] == 0)
    check('bounded nested controls', _test_controls())
    print(f"--- t133 selftest: {'PASS' if all_ok else 'FAIL'} ---")
    return 0 if all_ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    cmds = ap.add_mutually_exclusive_group(required=True)
    cmds.add_argument('--list', action='store_true')
    cmds.add_argument('--dump', nargs=2, metavar=('ARCHIVE', 'TID'))
    cmds.add_argument('--verify-all', action='store_true')
    cmds.add_argument('--selftest', action='store_true')
    ap.add_argument('--limit', type=int, default=5)
    args = ap.parse_args()
    if args.limit < 0:
        ap.error('--limit must be nonnegative')
    records, specs = registry(load(TRACE))
    if args.list:
        for key, t in sorted(records.items()):
            print(f"{key[0]:6} {key[1]:2} {t['class']:36} {t['rows_header']:8} "
                  + (specs[key].kind if key in specs else f'SKIP: {BLOCKERS.get(key, "no proven grammar")}'))
        return 0
    l3 = load(L3)
    if args.selftest:
        return selftest(records, specs, l3)
    if args.dump:
        try:
            key = args.dump[0], int(args.dump[1])
        except ValueError:
            ap.error('TID must be an integer')
        if key not in specs:
            ap.error(BLOCKERS.get(key, f'unknown table {key}'))
        result = verify_table(specs[key], records[key], l3, base.Archive(key[0]).payload(key[1]), args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0 if result['footer_closed'] else 1
    verify = verify_all(records, specs, l3)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'reader_v2_verify.json').write_text(json.dumps(verify, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for key, r in verify['tables'].items():
        if not r['footer_closed']:
            print(f"{r['kind'].upper():8} {key} {r.get('reason') or r.get('error')}")
    print(json.dumps({**verify['summary'], 'elapsed_total_ms': verify['elapsed_total_ms']}))
    return 0 if verify['status'] == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())
