#!/usr/bin/env python3
"""Replay C, captured Unicorn reads and independent sidecar evidence for the t109 gaps.

No binary is executed. Offsets are local to a proved receiver, not table-independent
keys. The t108 index is a dispatch locator, not an authority on widths/persistence.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter, defaultdict, deque
from functools import cached_property, lru_cache
import hashlib
import json
import runpy
from pathlib import Path
import re
import struct

from t109_big3_l3_join import SerializerParser, split_args, TYPE_BYTES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t125/out'
T95 = 'scratch/t95/funcs'
T124 = 'scratch/t124/out/funcs'
JOIN = 'scratch/t109/out/big3_l3_join.json'
GAPS = 'scratch/t109/out/remaining_gaps.json'
OLD = 'scratch/t109/out/coverage_summary.json'
INDEX = 'scratch/t124/out/ida_index.json'
MAP = 'scratch/t108/out/fourcc_mem_map_v2.json'
VTABLE = 'scratch/t95/vtable_index.json'
TRACE = 'scratch/t121/out/wire_traces_79of79.json'
T98 = 'scratch/t98/out/table45_full_schema.json'
T48 = 'scratch/t98/out/table48_comparison.json'
T71 = 'scratch/t71/out/field_map_r3.json'
T82 = 'scratch/t82/out/field_map.json'
T79 = 'scratch/t79/out/field_map.json'
EDITOR = Path(str(_cfg.EDITOR_EXE))
ENTITIES = {'club': 433, 'nation': 346, 'comp': 255}
OWN = {'club': (3,), 'nation': (9, 10), 'comp': (25,)}
DIRECT = 'L3_unicorn_or_subobject_closed'
INLINE = 'L3_helper_inlined_closed'
CHILD = 'L3_subtable_routed'
EXCLUDED = 'excluded_non_db_l3'
NUM = r'(?:0x[0-9a-fA-F]+|[0-9]+)'
CALL = re.compile(r'\bsub_([0-9a-f]+)\s*\(', re.I)
DEREF = re.compile(r'\*\(([^()*]+)\s*\*\)\s*\(a1\s*\+\s*(' + NUM + r')(?:LL)?\)')


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def save(name, value):
    dest = OUT / name
    tmp = dest.with_suffix(dest.suffix + '.tmp')
    tmp.write_text(text(value), encoding='utf-8')
    tmp.replace(dest)


def fourcc(s):
    return int.from_bytes(s.encode('ascii'), 'big')


def contains(start, n, off, width):
    return n > 0 and width > 0 and start <= off and off + width <= start + n


class Corpus:
    def __init__(self):
        self.old = {p.stem: p for p in (ROOT / T95).glob('*.c')}
        self.new = {p.stem: p for p in (ROOT / T124).glob('*.c')}
        self.index = read_json(INDEX)['records']
        self.alias = {a['input_va'][2:]: a['real_va'][2:] for a in self.index if a['ok']}

    @lru_cache(maxsize=None)
    def get(self, va):
        va = va.removeprefix('0x').lower()
        key = self.alias.get(va, va)
        p = self.new.get(key) or self.old.get(key)
        if p is None:
            return None, ()
        lines = self.lines(p)
        m = re.match(r'// THUNK ALIAS -> sub_([0-9a-f]+)', lines[0], re.I) if lines else None
        if m and m[1].lower() in (self.old.keys() | self.new.keys()):
            return self.get(m[1])
        return p, lines

    @staticmethod
    @lru_cache(maxsize=None)
    def lines(p):
        return tuple(p.read_text(encoding='utf-8').splitlines())

    def blocker_inventory(self):
        result = []
        for a in self.index:
            m = re.fullmatch(r'big3_gap_top_(\d+)rows', a['tag'])
            if not m and a['tag'] != 'big3_gap_ref':
                continue
            p, ls = self.get(a['input_va'])
            assert a['ok'] and p and ls
            result.append({'input_va': a['input_va'], 'real_va': a['real_va'], 'prior_gap_rows': int(m[1]) if m else None,
                           'source_file': p.relative_to(ROOT).as_posix(), 'line_count': len(ls),
                           'normalized_text_sha256': hashlib.sha256('\n'.join(ls).encode('utf-8')).hexdigest()})
        assert len(result) == 33
        return result

    def cite(self, va, line, expect=None):
        p, ls = self.get(va)
        assert p and 1 <= line <= len(ls), (va, line)
        s = ls[line - 1].strip()
        if expect is not None:
            assert re.search(expect, s, re.I), (va, line, s, expect)
        return {'source_file': p.relative_to(ROOT).as_posix(), 'line_no': line,
                'helper_va': '0x' + p.stem, 'text': s}

    def locate(self, va, regex, first=1, last=None):
        p, ls = self.get(va)
        for i in range(first, min(last or len(ls), len(ls)) + 1):
            if re.search(regex, ls[i - 1], re.I):
                return self.cite(va, i)
        return None

    def anchor(self, node, code):
        # t108 cites the t95 export, which may include a leading alias/signature line.
        va, line = node['func_va'][2:], node['line_no']
        p, ls = self.get(va)
        if not p:
            return None
        tag = fourcc(code)
        old = self.old.get(va)
        text = self.lines(old)[line - 1].strip() if old and line <= len(self.lines(old)) else ''
        for i in sorted(range(max(1, line - 5), min(len(ls), line + 5) + 1), key=lambda i: abs(i - line)):
            if tag in {int(m, 0) for m in re.findall(r'(?<![\w])' + NUM + r'(?![\w])', ls[i - 1])} and re.search(r'case|\bif\b', ls[i - 1]):
                if not text or text == ls[i - 1].strip() or i == line:
                    return self.cite(va, i)
        return None

    def branch(self, node, code):
        """Locate a t108 branch; return its body as *candidates*, not a CFG proof."""
        a = self.anchor(node, code)
        if not a:
            return None
        delta = a['line_no'] - node['line_no']
        _, ls = self.get(node['func_va'])
        lo, hi = node.get('body_span') or [node['line_no'], node['line_no'] + 2]
        lo, hi = max(1, lo + delta), min(len(ls), hi + delta)
        return a, [(i, ls[i - 1].strip()) for i in range(lo, hi + 1)]


class Engine:
    def __init__(self):
        self.c = Corpus()
        self.base = read_json(JOIN)
        self.gaps = {r['id']: r for r in read_json(GAPS)['rows']}
        self.old = read_json(OLD)['summary']
        self.map = read_json(MAP)['tables']
        self.vt = read_json(VTABLE)['tables']
        self.t98 = read_json(T98)
        self.t48 = read_json(T48)
        self.trace = read_json(TRACE)
        self.events = defaultdict(list)
        for ti, t in enumerate(self.trace['tables']):
            if not t['rows_ok'] or t.get('error'):
                continue
            for ri, r in enumerate(t.get('row0_reads', [])):
                if r.get('dst_kind') == 'this' and type(r.get('obj_off_dec')) is int and type(r.get('n')) is int and r['n'] > 0 and r.get('caller') and type(r.get('wire_pos')) is int:
                    assert int(r['obj_off'], 0) == r['obj_off_dec']
                    self.events[t['table_id']].append(dict(artifact=TRACE, pointer=f'/tables/{ti}/row0_reads/{ri}', archive=t['archive'], table_id=t['table_id'], object_class=t['class'], wire_off=r['wire_pos'], obj_off=r['obj_off_dec'], width=r['n'], caller_va=r['caller']))
        self.side = {r['id'].split('/', 1)[1]: (p, i, r) for p in (T71, T82)
                     for i, r in enumerate(read_json(p)['fields']) if r['grade'] == 'L3'}
        self.serial = SerializerParser(ROOT / T95)

    def spans(self, table, off, width):
        return [r for r in self.events[table] if contains(r['obj_off'], r['width'], off, width)]

    def branches(self, row):
        seen = set()
        for t in self.map:
            if t['table_type'] not in OWN[row['entity']]:
                continue
            rec = t['fourccs'].get(row['code']) or {}
            for n in (rec, rec.get('alt') or {}):
                if not n:
                    continue
                k = n['func_va'], n['line_no']
                if k in seen:
                    continue
                seen.add(k)
                b = self.c.branch(n, row['code'])
                if b:
                    yield n, *b

    def read_span(self, va, off, width, pointer=None):
        """Literal raw-read destinations, including a proved pointer subobject.

        Use the real signature scale for bare `a1 + N`, and require full width.
        The stream vcall must have a receiver and exactly three arguments.
        """
        _, ls = self.c.get(va)
        if not ls:
            return None
        _, elem, _ = self.serial.signature(ls)
        for i, s in enumerate(ls, 1):
            if not re.search(r'\+ 40(?:LL)?\)\)\(', s):
                continue
            chunk = '\n'.join(ls[i - 1:i + 5]).split(';', 1)[0]
            rhs = re.split(r'\+ 40(?:LL)?\)\)\(', chunk, maxsplit=1)[-1].replace('\n', ' ').rstrip().removesuffix(')')
            args = split_args(rhs)
            if len(args) != 3 or not re.fullmatch(NUM, args[2]):
                continue
            dst = args[1].strip()
            if pointer is None:
                m = re.fullmatch(r'a1(?:\s*\+\s*(' + NUM + r')(?:LL)?)?', dst)
                start = int(m[1] or '0', 0) * elem if m else None
            else:
                m = re.fullmatch(r'\*\(_QWORD \*\)\(a1 \+ ' + str(pointer) + r'\)(?: \+ (' + NUM + r')(?:LL)?)?', dst)
                start = int(m[1] or '0', 0) if m else None
            n = int(args[2], 0)
            if start is not None and contains(start, n, off, width):
                return dict(self.c.cite(va, i), obj_off=start, width=n, destination_line_end=i + chunk.count('\n'), destination_expr=dst)
        return None

    def ntc_fields(self, row, branches):
        if row['entity'] != 'nation':
            return None
        for n, gate, body in branches:
            if n['func_va'] != '0x141063f30' or n['slot'] != 'slot03_set_prop':
                continue
            for i, s in body:
                m = DEREF.match(s) if re.search(r'\)\s*=(?!=)', s) else None
                if m:
                    width, off = TYPE_BYTES.get(m[1].strip()), int(m[2], 0)
                else:
                    # v5 is (_WORD *)a1, not an independently allocated object.
                    m = re.match(r'v5\[(\d+)\] = ', s)
                    if not m:
                        continue
                    alias = self.c.locate('141063f30', r'v5 = \(_WORD \*\)a1;')
                    if not alias:
                        continue
                    width, off = 2, 2 * int(m[1])
                # Only the explicit numeric-setting lanes here, not an arbitrary
                # store in a multi-branch list setter or a secondary side effect.
                if off != row['mem_off'] or off not in {562, *range(1924, 1934, 2), *range(1949, 1974)} or not width:
                    continue
                serializer = self.read_span('14105d510', off, width)
                if not serializer:
                    continue
                route = [self.c.cite('141063e50', 4, r'sub_143F00000'),
                         self.c.cite('143f00000', 39, r'sub_141063f30\(a1, a2, a3\)')]
                if s.startswith('v5['):
                    route.append(alias)
                return self.proof(DIRECT, self.c.cite(n['func_va'], i), off, width, 9,
                                  [gate, *route, serializer], 'Table-9 setter and reader use the same NATIONAL_TEAM_CONTAINER receiver.', self.spans(9, off, width))
        return None

    @staticmethod
    def proof(cls, anchor, off, width, table, cites, reason, trace=None, **extra):
        return dict(anchor, classification=cls, mem_off=off, width=width, target_table=table,
                    citations=cites, reason=reason, unicorn=trace or [], **extra)

    @cached_property
    def record_keys(self):
        # The two physical members share a row vtable. Disambiguate with
        # independently decoded parent UID sets, not with an assumed address.
        from t98_table45_closure import load_server_payload
        scan = runpy.run_path(str(ROOT / 'scratch/t79/out/verify.py'))['scan_uids']
        uids = {i: set(scan(load_server_payload(i)).tolist()) for i in (3, 9, 10, 25)}
        profiles = {}
        for i, meta in ((45, self.t98['table_45']), (48, self.t48['table_48'])):
            raw = load_server_payload(i)
            assert hashlib.sha256(raw).hexdigest() == meta['sha256']
            counts = defaultdict(Counter)
            pos = meta['header_size']
            for ordinal in range(meta['record_count_decoded']):
                key, typ = struct.unpack_from('<IB', raw, pos)
                pos += 80 + struct.unpack_from('<I', raw, pos+37)[0]
                assert struct.unpack_from('<I', raw, pos-13)[0] == ordinal
                counts[typ]['rows'] += 1
                for t, keys in uids.items():
                    counts[typ][str(t)] += key in keys
            assert pos == meta['row_end']
            profiles[i] = counts
        return profiles

    @staticmethod
    @lru_cache(maxsize=None)
    def pe_bytes(off, n):
        with EDITOR.open('rb') as f:
            f.seek(off)
            data = f.read(n)
        assert len(data) == n
        return data

    def factory_anchor(self, table):
        off = {45: 0xf06c70, 48: 0xf06daf}[table]
        b = self.pe_bytes(off, 13)
        va = off + 0x140000a00
        assert b[:9] == bytes([0xba, table, 0, 0, 0, 0x45, 0x31, 0xc0, 0xe8])
        assert va + 13 + struct.unpack_from('<i', b, 9)[0] == 0x140ffa310
        return {'artifact': EDITOR.as_posix(), 'file_off': off, 'va': hex(va), 'bytes': b.hex(),
                'scope': 'table type constructor, not a direct global assignment'}

    def child_path(self, n, gate, body):
        """Recognize constant type and tag at the actual routed call.

        Only the three setter layouts used below. Shared tails reached by
        unconditional goto are visited, with constant arguments carried across.
        """
        setups = {
            '0x140e834a0': ('v7', 'v15', '1411e9540', 45),
            '0x1411f4f70': ('a2', 'v7', '1411e9540', 45),
            '0x141063f30': ('a2', 'v6', '1411e9540', 45),
            '0x140ecb5c0': ('a2', 'v12', '140ecdfe0', 48),
        }
        info = setups.get(n['func_va'])
        if not info or not body or n['slot'] != 'slot03_set_prop':
            return None
        typevar, tagvar, dest, table = info
        _, ls = self.c.get(n['func_va'])
        labels = {s.strip().removesuffix(':'): i for i, s in enumerate(ls, 1) if re.fullmatch(r'LABEL_\d+:', s.strip())}
        # Reviewed lexical exits out of the switch/if region; no arbitrary
        # break fall-through into the next case. Endpoints are verified below.
        break_tail = {'0x141063f30': 2038, '0x140ecb5c0': 823}
        i = body[0][0]
        typ = tag = None
        path = [gate]
        visited = set()
        for _ in range(30):
            if i in visited or not 1 <= i <= len(ls):
                return None
            visited.add(i)
            s = ls[i-1].strip()
            m = re.fullmatch(r'LOBYTE\(' + typevar + r'\) = (' + NUM + r');', s)
            if m:
                typ = int(m[1], 0)
                path.append(self.c.cite(n['func_va'], i))
            else:
                m = re.fullmatch(tagvar + r' = (' + NUM + r');', s)
                if m:
                    tag = int(m[1], 0)
                    path.append(self.c.cite(n['func_va'], i))
                elif re.fullmatch(r'(?:v14 = a1;|LABEL_\d+:)', s):
                    pass
                elif s == '}' and n['func_va'] == '0x140e834a0' and typ is not None and tag is not None and i in {729, 737, 850, 872}:
                    # Reviewed arms in the if/else tree ending at the shared call.
                    path.append(self.c.cite(n['func_va'], i, r'^}$'))
                    i = 874
                    continue
                elif (m := re.fullmatch(r'goto (LABEL_\d+);', s)):
                    path.append(self.c.cite(n['func_va'], i))
                    i = labels[m[1]]
                    continue
                elif s == 'break;' and n['func_va'] in break_tail and typ is not None and tag is not None:
                    # These two switch exits are at the outer tail; 140ecb5c0
                    # may also return from an inner arm without taking a break.
                    if n['func_va'] == '0x141063f30' and not 2009 <= i <= 2034:
                        return None
                    if n['func_va'] == '0x140ecb5c0' and not 68 <= i <= 819:
                        return None
                    path.append(self.c.cite(n['func_va'], i))
                    i = break_tail[n['func_va']]
                    continue
                elif re.fullmatch(r'return sub_' + dest + r'\((v14|a1), ' + typevar + ', ' + tagvar + r', (a3|v[34])\);', s, re.I):
                    if typ is None or tag is None:
                        return None
                    path.append(self.c.cite(n['func_va'], i))
                    if table == 45:
                        path += [self.c.cite('144026550', 10, r'a1 \+ 12'), self.c.cite('144026550', 11, '141B60190'),
                                 self.c.cite('144026550', 17, r'\+ 76.*\+ 94'), self.c.cite('144026550', 18, 'sub_141545680')]
                    else:
                        path += [self.c.cite('143ca4a20', 11, '141B60198'), self.c.cite('143ca4a20', 16, r'a1 \+ 12'),
                                 self.c.cite('143ca4a20', 23, r'\+ 76.*\+ 94'), self.c.locate('143ca4a20', 'return sub_141545680')]
                    return table, typ, tag, path
                else:
                    return None
            i += 1
        return None

    def child(self, row, branches):
        for n, gate, body in branches:
            hit = self.child_path(n, gate, body)
            if hit is None:
                continue
            table, typ, tag_n, path = hit
            tag = tag_n.to_bytes(4, 'big').decode('ascii')
            # No extant record of this type in this DB member: code can create
            # it but cannot prove an actual persisted route in these archives.
            profiles = self.t98['rec_type_profiles'] if table == 45 else self.t48['rec_type_profiles']
            if table == 48 and typ == 20 and '22' in profiles:
                # Manager explicitly accepts either type; preserve both lanes.
                profile_types = [20, 22]
            else:
                profile_types = [typ]
            if not any(str(x) in profiles for x in profile_types):
                continue
            parent = {'club': '3', 'nation': '9', 'comp': '25'}[row['entity']]
            control = '3' if table == 48 else '25'
            keys = {str(t): dict(self.record_keys[table][t]) for t in profile_types if t in self.record_keys[table]}
            overall = {k: sum(p[k] for p in self.record_keys[table].values()) for k in ('rows', parent, control)}
            # Some setters support nation routes for record types that occur
            # only on clubs in this build. Require actual parent/type examples.
            if not sum(p[parent] for p in keys.values()) or sum(p[control] for p in keys.values()) > sum(p[parent] for p in keys.values()):
                continue
            direct = next((x for x in self.t98['direct_starting_record_4cc'] if x['tag'] == tag and x['set']), None)
            if not direct:
                continue
            col = next(x for x in self.t98['physical_columns'] if x['id'] == direct['physical_col'])
            off = col['mem_off']
            width = 8 if col['kind'] == 'utf8_len32' or col['id'] == 'name' else col['wire_width']
            if type(width) is not int:
                continue
            # t98 spans can include the preceding branch; exact typed store is
            # verified in the refreshed body instead of citing the span start.
            dr = re.compile(r'^\*\(([^*]+)\*\)\(a1 \+ ' + str(off) + r'\) = ')
            _, ls = self.c.get('141545680')
            stores = [self.c.cite('141545680', i) for i in range(direct['set'][0], min(len(ls), direct['set'][-1]+5)+1)
                      if (m := dr.match(ls[i-1].strip())) and TYPE_BYTES.get(m[1].strip()) == width]
            # Conditional name replacement is outside the early t98 range in
            # some IDA versions; its same-case use is verified by the nearby tag.
            if tag == 'stnm':
                stores = [s for s in [self.c.locate('141545680', r'\*\(_QWORD \*\)\(a1 \+ 56\) =', 230, 243)] if s]
            if not stores:
                continue
            cf, ln = col['read_source'].rsplit(':', 1)
            ser = self.c.cite(Path(cf).stem, int(ln))
            anchors = [a for a in self.t98['accessor_codes'] if a['code'] == row['code']]
            return self.proof(CHILD, stores[0], off, width, table, path + [ser],
                              'Constant record type and inner tag reach the STARTING_RECORD setter on the keyed DB member.',
                              self.spans(table, off, width), factory=self.factory_anchor(table), rec_type=typ, inner_tag=tag,
                              key_controls={'by_rec_type': keys, 'overall': overall, 'parent_table': int(parent), 'opposite_parent_table': int(control)},
                              getter_citations=[self.c.cite('1415446a0', i) for i in direct['get']],
                              physical_column=col, rec_type_counts={str(t): profiles[str(t)]['n'] for t in profile_types if str(t) in profiles},
                              t98_accessor_check=[{k:a[k] for k in ('tag', 'mem_off', 'mapping_tuple')} for a in anchors],
                              t98_tag_agrees=all(a['tag'] == tag for a in anchors))
        return None

    def check_pe(self, off, hex_bytes):
        b = bytes.fromhex(hex_bytes)
        assert b and self.pe_bytes(off, len(b)) == b, (hex(off), hex_bytes)
        return dict(artifact=EDITOR.as_posix(), file_off=off, bytes=hex_bytes)

    def sidecar(self, row, branches):
        if row['entity'] != 'club':
            return None
        hit = self.side.get(row['id'])
        if hit:
            p, i, r = hit
            assert r['code'] == row['code'] and r['grade'] == 'L3'
            path, width, pe = [], None, []
            if p == T71:
                w = r['wire']
                path, width = w['object_path'], w['width']
                assert path == r['static_getter']['object_path'] and path[0] == 256
                for stage in ('gate', 'helper'):
                    for x in [r['static_getter'].get(stage, {}).get('cell'), *r['static_getter'].get(stage, {}).get('direct_rel32', [])]:
                        if x and 'bytes' in x:
                            pe.append(self.check_pe(x['offset'], x['bytes']))
                if not pe:  # Cyfn / Cebd store instruction FOs, not bytes.
                    for j, off in enumerate(r['static_getter']['getter']):
                        pe.append(dict(artifact=EDITOR.as_posix(), file_off=off,
                                       bytes=self.pe_bytes(off, 6).hex(), role=f't71_getter_site_{j}'))
                wire = w
            else:
                path = [int(n, 16) for n in re.findall(r'\+0x([0-9a-f]+)', r['object_path'])]
                m = re.match(r'^[iu](8|16|32)$', r['wire_type'])
                width = int(m[1])//8 if m else {'u32_len_utf8': None, 'i32_milli_ring_to_f32': 4, 'poly_tag7_24B': 24}.get(r['wire_type'])
                for role in ('getter', 'setter', 'reader'):
                    x = r['static_chain'][role]
                    pe.append(dict(self.check_pe(int(x['file_offset'], 0), x['bytes']), role=role, va=x['va']))
                wire = {'scope': r['wire_scope'], 'wire_type': r['wire_type'], 'object_path_note': r['object_path']}
            if len(path) < 2 or path[0] not in (176, 256) or not pe:
                return None
            if not branches:
                return None
            anchors = [g for n, g, _ in branches if n['func_va'] in {'0x140e8a400','0x140e834a0','0x1411f1090','0x1411f4f70','0x140e882d0','0x140e97920'}]
            if not anchors:
                return None
            return self.proof(CHILD, anchors[0], path[-1], width, 'table_extra_3', anchors[1:],
                              'Independent full-archive sidecar cursor; scope and persisted leaf are not the parent pointer slot.',
                              artifact=p, pointer=f'/fields/{i}', object_path=path, verified_pe=pe, wire=wire)
        t79 = read_json(T79)
        items = t79['table_extra_24']['fields']
        for i, r in enumerate(items):
            match = re.fullmatch(r'club.xml#club\[(\d+)\]', next(iter(r['schema_locations']), ''))
            if not match or r['field'] != row['code'] or int(row['id'].rsplit('/', 1)[1]) != int(match[1]) or r['grade'] != 'L3' or not branches:
                continue
            pos = self.c.locate('140e8a400', r'\b' + str(fourcc(row['code'])) + r'\b') or branches[0][1]
            offsets = [int(x, 0) for x in re.findall(r'0x[0-9a-f]+', r['member_off'])]
            pe = []
            for k in ('reader_fo', 'team_getter_fo', 'team_setter_fo'):
                off = int(r[k], 0)
                pe.append(dict(artifact=EDITOR.as_posix(), file_off=off, bytes=self.pe_bytes(off, 8).hex(), role=k))
            return self.proof(CHILD, pos, offsets[-1], r['width'], 'table_extra_24', [b[1] for b in branches],
                              'Club primary TEAM forwarding, then TEAM sidecar cursor.',
                              artifact=T79, pointer=f'/table_extra_24/fields/{i}', object_path=[24, *offsets],
                              wire={'wire_off': r['wire_off'], 'scope': r['scope']}, pe_sites=pe)
        for i, r in enumerate(t79['club_base18_forwarded_6']):
            if r['field'] != row['code'] or r['grade'] != 'L3' or r['club_xml_index'] != int(row['id'].rsplit('/', 1)[1]) or not branches:
                continue
            inner = fourcc(r['target_team_4cc'])
            routes = [self.c.cite(n['func_va'], ln) for n, _, body in branches
                      for ln, s in body if re.search(r'\b' + str(inner) + r'\b', s)]
            if not routes:
                continue
            off = int(r['target_member_off'].split('+')[-1], 0)
            m = re.search(r'TEAM\+(\d+)\.\.(\d+)', r['target_wire_pos'])
            wire_off, end = map(int, m.groups())
            return self.proof(CHILD, branches[0][1], off, end-wire_off+1, 24,
                              routes + [b[1] for b in branches[1:]], 'Verified forwarding through the primary TEAM of CLUB+0x18; reference wire width differs from in-memory handle width.',
                              artifact=T79, pointer=f'/club_base18_forwarded_6/{i}', object_path=[24, off],
                              inner_tag=r['target_team_4cc'], wire={'wire_off': wire_off, 'interpretation': r['target_wire_pos']})
        return None

    def collection(self, row, branches):
        if row['entity'] != 'nation':
            return None
        for n, gate, b in branches:
            if n['func_va'] != '0x141063f30' or row['mem_off'] != 1056:
                continue
            m = next((re.match(r'v45 = (\d+);', s) for _, s in b if re.match(r'v45 = (\d+);', s)), None)
            ga = [(ng, gg, gb) for ng, gg, gb in branches if ng['func_va'] == '0x1410668f0']
            if not m or not ga or not any(re.search(r' = a1 \+ 1056;', s) for _, s in b):
                continue
            idx = int(m[1])
            gn, gg, gb = ga[0]
            get = next((i for i, s in gb if (idx == 0 and s == 'v42 = *v41;') or (idx > 0 and re.fullmatch(r'v42 = \*\(_DWORD \*\)\(v\d+ \+ '+str(idx*4)+r'\);', s))), None)
            if get is None or not any('a1 + 1056' in s for _, s in gb):
                continue
            cites = [gg, self.c.cite(gn['func_va'], get), *[self.c.cite(n['func_va'], i) for i, _ in b[:4]],
                     self.c.cite('14105d510', 449, r'&v218, 1'),
                     self.c.cite('14105d510', 452, r'v223 = a1 \+ 1056'),
                     self.c.cite('14105d510', 460, r'v234, 4'),
                     self.c.cite('14105d510', 463, r'sub_14105FB30\(v223, v234\)')]
            return self.proof(DIRECT, gate, 1056, 4, 9, cites, 'NTC counted vector deserializes temporary 4-byte values into backing storage; getter selects index, not an inline slot.',
                              object_path=[1056, idx*4], element_index=idx)
        seg_path = 'scratch/t55/out/abc_closure.json'
        segments = self.nation_segments
        for k, seg in segments.items():
            if seg['parent'] != row['code'] or seg['frozen_index'] != int(row['id'].rsplit('/', 1)[1]):
                continue
            getters = [(n, g, b) for n, g, b in branches if n['func_va'] == '0x141042940']
            if not getters or not all(v['rows'] == 251 for v in seg['profiles'].values()):
                continue
            n, gate, b = getters[0]
            off = seg['object_displacement']
            ln, pat = {72: (539, r'v98 \+ 9,'), 144: (586, r'v98 \+ 18,'), 168: (561, r'v98 \+ 21,'), 192: (611, r'v98 \+ 24,')}[off]
            _, lines = self.c.get('1410404c0')
            ser = self.c.locate('1410404c0', pat, ln-4, ln+4)
            assert ser and 'v10 = a1;' in lines[135] and 'v98 = v10;' in lines[531]
            getter = [self.c.cite(n['func_va'], i) for i, _ in b[:4]]
            if off == 192:
                member = self.c.locate('14104ff00', r'\+ 192LL')
                assert member
                getter.append(member)
            result = INLINE if row['new_class'] == 'gap_helper_computed' else DIRECT
            return self.proof(result, gate, off, None, 10, [*getter, ser],
                              'NATION collection parent and both archive cursors independently close; not a flat scalar.',
                              artifact=seg_path, pointer=f'/segments/{k}', wire={'item_stride': seg['item_stride'], 'profiles': seg['profiles']})
        return None

    @cached_property
    def nation_segments(self):
        return read_json('scratch/t55/out/abc_closure.json')['segments']

    def exclusion(self, row, branches):
        # A positive proof of no-op dispatch. A missing read or wrong-table tag
        # alone is never an exclusion; aliases with actual writes stay held.
        if row['entity'] == 'comp' and row['code'] == 'IsAC':
            num = str(fourcc(row['code']))
            for n, gate, b in branches:
                if n['func_va'] != '0x140ec0a60' or b != [(2723, 'goto LABEL_5;')]:
                    continue
                if any(self.c.locate(x, r'\b' + num + r'\b') for x in ('140ecb5c0', '140fe2700')):
                    continue
                _, get = self.c.get('140ec0a60')
                assert tuple(s.strip() for s in get[461:464]) == ('LABEL_5:', 'LOBYTE(v3) = 1;', 'return (unsigned int)v3;')
                return self.proof(EXCLUDED, gate, None, None, None,
                                  [self.c.cite(n['func_va'], i) for i in (2723, 462, 463, 464)],
                                  'Exact COMP getter arm reports handled without writing the result; no matching COMP/base setter arm.',
                                  exclusion_reason='getter-only handled no-op')
        return None

    @cached_property
    def readers(self):
        standard = {3: 'CLUB', 9: 'NATIONAL_TEAM_CONTAINER', 10: 'NATION', 25: 'COMP'}
        result = {}
        for t in self.vt:
            no = t['table_type']
            if standard.get(no) != t['class'] or no not in standard:
                continue
            result[no] = {}
            for slot in (19, 20):
                root = t['slots_hex'][slot]
                q = deque([(root, 0)])
                visited, calls, joins = {}, [], []
                while q:
                    va, depth = q.popleft()
                    if va in visited:
                        continue
                    p, ls = self.c.get(va)
                    visited[va] = p.relative_to(ROOT).as_posix() if p else None
                    for i, s in enumerate(ls, 1):
                        if i == 1 or s.strip().startswith('//'):
                            continue
                        for m in CALL.finditer(s):
                            v = '0x' + m[1].lower()
                            first = s[m.end():].split(',', 1)[0].strip()
                            same = first in {'a1', '(_DWORD)a1', '(__int64)a1'}
                            calls.append({'va': v, 'caller': '0x'+p.stem, 'line_no': i, 'arg0_text': first,
                                          'same_this': same, 'decompiled': bool(self.c.get(v)[0])})
                            if depth == 0 or (depth < 4 and same):
                                q.append((v, depth + 1))
                            if same:
                                joins.append((va, v, i))
                result[no][slot] = {'root': root, 'vtable': t['vtable_va'], 'reviewed_bodies': visited,
                                   'call_sites': calls, 'same_this_edges': joins}
        return result

    def direct_member(self, row, branches):
        # Inlined typed setters (COMP/CLUB/NATION only, not ancestor address
        # matches from a different registered vtable). Confirm a same-this
        # literal serializer write. A naked pointer word isn't a payload.
        handlers = {'0x140e834a0': 3, '0x141045d50': 10, '0x140ecb5c0': 25}
        for n, gate, body in branches:
            table = handlers.get(n['func_va'])
            if not table or n['slot'] != 'slot03_set_prop':
                continue
            for i, s in body:
                m = DEREF.match(s)
                if not m or not re.match(r' = ', s[m.end():]):
                    continue
                width, off = TYPE_BYTES.get(m[1].strip()), int(m[2], 0)
                if not width or width > 4 or (row['mem_off'] is not None and off != row['mem_off']):
                    continue
                if not ('+ 64LL' in s or '+ 48LL' in s or re.fullmatch(r'\*\(_DWORD \*\)\(a1 \+ (292|296)\) = \(_DWORD\)v66;', s)):
                    continue
                for slot, model in self.readers[table].items():
                    paths = {model['root']: []}
                    for _ in range(4):
                        for src, dst, ln in model['same_this_edges']:
                            if src in paths and dst not in paths:
                                paths[dst] = paths[src] + [self.c.cite(src, ln)]
                    for va, path in paths.items():
                        ser = self.read_span(va, off, width)
                        if ser:
                            cls = INLINE if row['new_class'] in {'gap_helper_computed', 'gap_delegated_or_empty'} else DIRECT
                            return self.proof(cls, self.c.cite(n['func_va'], i), off, width, table,
                                              [gate, *path, ser], 'Typed setter and same-object reader overlap for the full member width.',
                                              self.spans(table, off, width), reader_slot=slot)
        return None

    def blockers(self, row, branches):
        """Resolve only local constant goto tails, then collect exact branch callsites."""
        all_cites, hops = [], {}
        for n, gate, body in branches:
            va = n['func_va']
            _, ls = self.c.get(va)
            labels = {s.strip().removesuffix(':'): i for i, s in enumerate(ls, 1) if re.fullmatch(r'LABEL_\d+:', s.strip())}
            all_cites.append(gate)
            queue = deque(body)
            seen = set()
            while queue and len(seen) < 160:
                i, s = queue.popleft()
                if i in seen:
                    continue
                seen.add(i)
                if s != gate['text'] and i > gate['line_no'] and re.match(r'case |default:', s):
                    break
                cites = []
                for m in re.finditer(r'\b(?:sub_|JUMPOUT\(0x)([0-9a-f]{8,})(?:LL)?', s, re.I):
                    dest = '0x' + m[1].lower()
                    if dest not in hops:
                        cite = self.c.cite(va, i)
                        hops[dest] = {'va': dest, 'decompiled': bool(self.c.get(dest)[0]), 'site': cite}
                        cites.append(cite)
                all_cites.extend(cites)
                m = re.fullmatch(r'goto (LABEL_\d+);', s)
                if m and m[1] in labels:
                    j = labels[m[1]]
                    all_cites.append(self.c.cite(va, i))
                    # t108 body spans may stop before a shared label; inventory
                    # only its straight-line prefix, not neighbouring branches.
                    for k in range(j+1, min(j+13, len(ls)+1)):
                        ss = ls[k-1].strip()
                        if re.match(r'case |default:|if |else|LABEL_|while|\}', ss):
                            break
                        queue.append((k, ss))
                        if ss.startswith(('return ', 'goto ')):
                            break
        for cite in row.get('blocker_helpers', []) or []:
            if isinstance(cite, str) and cite.startswith('0x') and cite not in hops:
                hops[cite] = {'va': cite, 'decompiled': bool(self.c.get(cite)[0]), 'site': None}
        return all_cites, sorted(hops.values(), key=lambda h: (h['decompiled'], h['va']))

    def classify(self, row):
        b = list(self.branches(row))
        hit = (self.sidecar(row, b) or self.ntc_fields(row, b) or self.collection(row, b)
               or self.child(row, b) or self.direct_member(row, b) or self.exclusion(row, b))
        if hit:
            return hit, None
        cites, hops = self.blockers(row, b)
        base_loc = re.fullmatch(r'funcs/([0-9a-f]+)\.c:(\d+)', row.get('getter_cite') or '')
        if base_loc:
            va, ln = base_loc.groups()
            f, ls = self.c.get(va)
            if f and int(ln) <= len(ls):
                old_cite = self.c.cite(va, int(ln))
                if old_cite not in cites:
                    cites.append(old_cite)
        off = row['mem_off']
        traces = {str(t): self.spans(t, off, 1) for t in OWN[row['entity']]} if type(off) is int else {}
        old = row['new_class']
        why = {
            'gap_off_not_in_read_stream': 'No same-receiver persisted leaf proved. Read hits, if any, are unbound candidate byte spans, not proof of the getter path.',
            'gap_helper_computed': 'Helper input/output or branch-to-wire data flow is not closed.',
            'gap_delegated_or_empty': 'Delegation, conditional no-op, or shared label does not establish a persisted sink or a full exclusion.',
            'gap_child_off_not_in_child_stream': 'No supported on-archive parent/type/column route proved; an inner tag or record vtable alone does not establish it.',
            'gap_other_table_same_tag': 'Foreign 4CC match is not proof of owner forwarding; require an actual receiver path.',
        }[old]
        return None, dict(row, reason_t125=why, reviewed_dispatch=cites, candidate_trace_hits=traces,
                          next_hops=hops, undecompiled_next_hop_vas=[h['va'] for h in hops if not h['decompiled']])


def coverage(rows):
    classes = Counter(r['new_class'] for r in rows)
    l3 = sum(v for c, v in classes.items() if c.startswith('L3_'))
    excluded = classes[EXCLUDED]
    n = len(rows)
    gaps = n - l3 - excluded
    assert gaps == sum(v for c, v in classes.items() if c.startswith('gap_'))
    return dict(denominator=n, l3=l3, excluded_non_db=excluded, gaps=gaps,
                net_denominator=n-excluded, gross_pct=round(100*l3/n, 4),
                net_pct=round(100*l3/(n-excluded), 4), by_class=dict(sorted(classes.items())))


def assemble(e):
    original = e.base['rows']
    assert len(original) == len({r['id'] for r in original}) == 1034
    assert Counter(r['entity'] for r in original) == ENTITIES
    assert [r['id'] for r in original if r['new_class'].startswith('gap_')] == list(e.gaps)
    assert len(e.gaps) == 294 and len(e.t98['physical_columns']) == 18 and len(e.t98['accessor_codes']) == 117
    inputs = [JOIN, GAPS, OLD, INDEX, T95, T124, MAP, VTABLE, TRACE, T98, T48, T71, T82, T79,
              'scratch/t55/out/abc_closure.json', 'scratch/data/server_db.dat', EDITOR.as_posix()]
    rows, remain = [], []
    changes, transitions, targets = Counter(), defaultdict(Counter), Counter()
    for row in original:
        if row['id'] not in e.gaps:
            rows.append(row)
            continue
        g = e.gaps[row['id']]
        hit, gap = e.classify(g)
        if not hit:
            rows.append(dict(row, t125_review={'status': 'held', 'pointer': f'/rows/{len(remain)}'}))
            remain.append(gap)
            continue
        cls = hit['classification']
        changes[cls] += 1
        transitions[row['new_class']][cls] += 1
        if hit['target_table'] is not None:
            targets[str(hit['target_table'])] += 1
        off = hit['mem_off']
        sc = hit['citations'][-1] if hit['citations'] else None
        serializer_cite = (f"{hit['artifact']}#{hit['pointer']}" if 'artifact' in hit else
                           f"{sc['source_file']}:{sc['line_no']}" if sc and hit['target_table'] is not None else None)
        own = 'sidecar_leaf' if 'object_path' in hit and cls == CHILD else ('child_object' if cls == CHILD else 'same_receiver')
        rows.append(dict(row, prior_class_t109=row['new_class'], prior_mem_off_t109=row['mem_off'],
                         new_class=cls, mem_off=off, mem_off_hex=hex(off) if off is not None else None,
                         mem_off_space=own if off is not None else None,
                         getter_cite=f"{hit['source_file']}:{hit['line_no']}",
                         serializer_cite=serializer_cite,
                         child_table=hit['target_table'] if cls == CHILD else None,
                         wire_width=hit['width'], gap_reason=None, resolution=hit['reason'], t125_evidence=hit))
    old, new = coverage(original), coverage(rows)
    assert (old['l3'], old['excluded_non_db'], old['gaps']) == (379, 361, 294)
    assert new['l3'] == 379 + sum(v for c, v in changes.items() if c.startswith('L3_'))
    assert new['excluded_non_db'] == 361 + changes[EXCLUDED]
    assert new['gaps'] == len(remain) == 294-sum(changes.values())
    priority = defaultdict(list)
    for g in remain:
        for va in g['undecompiled_next_hop_vas']:
            priority[va].append(g['id'])
    per = {name: {'t109': coverage([r for r in original if r['entity'] == name]),
                  't125': coverage([r for r in rows if r['entity'] == name])} for name in ENTITIES}
    summary = dict(schema_id='fm24.t125.coverage_summary_v3', conservation=ENTITIES,
                   original_baseline=e.old['old_scope'], t109=old, t125=new, per_entity=per,
                   upgrades_by_class=dict(sorted(changes.items())), transitions_by_gap_class={k: dict(v) for k, v in sorted(transitions.items())},
                   upgrades_by_target=dict(sorted(targets.items())), l3_downgrades=[], excluded_downgrades=[])
    audit = {str(t): {str(slot): model for slot, model in modes.items()} for t, modes in e.readers.items()}
    trace_status = [{k: t[k] for k in ('archive', 'table_id', 'class', 'rows_ok', 'closed_to_footer')}
                    for t in e.trace['tables'] if t['table_id'] in (3, 9, 10, 25, 45, 48)]
    full = dict(schema_id='fm24.t125.big3_l3_v3', inputs=inputs, denominator=1034, L4=0,
                engine='static + captured Unicorn + independently decoded archives', coverage=new,
                trace_status=trace_status, reader_call_audit=audit, blocker_helper_audit=e.c.blocker_inventory(), rows=rows)
    remaining = dict(schema_id='fm24.t125.remaining_gaps_v3', gap_total=len(remain),
                     by_class=dict(sorted(Counter(g['new_class'] for g in remain).items())),
                     priority_undecompiled=[dict(va=va, gap_count=len(ids), ids=ids)
                                           for va, ids in sorted(priority.items(), key=lambda kv: (-len(kv[1]), kv[0]))],
                     notes='Next-hop VAs are branch-local candidate calls. Some blockers require a missing receiver, virtual target, CFG path, or cursor binding rather than decompilation.',
                     rows=remain)
    return {'big3_l3_v3.json': full, 'coverage_summary_v3.json': summary, 'remaining_gaps_v3.json': remaining}


def report(bundle):
    s = bundle['coverage_summary_v3.json']
    remaining = bundle['remaining_gaps_v3.json']
    full = bundle['big3_l3_v3.json']
    a, b = s['t109'], s['t125']
    lines = ['# t125 — Big-3 persisted field closure', '',
             f"Original {s['original_baseline']['text']}; t109 → t125: gross **{a['l3']}/1034 → {b['l3']}/1034 ({b['gross_pct']:.1f}%)**, net **{a['l3']}/{a['net_denominator']} → {b['l3']}/{b['net_denominator']} ({b['net_pct']:.1f}%)**, gaps **294 → {b['gaps']}**.",
             'All 379 t109 L3 rows and 361 exclusions are unchanged. Counts are top-level XML occurrences, not unique tags or physical columns.', '',
             '| Entity | N | L3 old → new | Net denominator old → new | Excluded old → new | Gaps old → new |',
             '|---|---:|---:|---:|---:|---:|']
    for name, p in s['per_entity'].items():
        x, y = p['t109'], p['t125']
        lines.append(f"| {name} | {y['denominator']} | {x['l3']} → {y['l3']} | {x['net_denominator']} → {y['net_denominator']} | {x['excluded_non_db']} → {y['excluded_non_db']} | {x['gaps']} → {y['gaps']} |")
    lines += ['', '## Reclassified gaps', '', '| Class | Occurrences |', '|---|---:|']
    lines.extend(f'| `{c}` | {n} |' for c, n in s['upgrades_by_class'].items())
    lines += ['', 'Persisted target distribution: ' + ', '.join(f'`{k}`: {v}' for k, v in s['upgrades_by_target'].items()) + '.',
              '', '| Prior gap class | Resolved | Remaining |', '|---|---:|---:|']
    for c, n in a['by_class'].items():
        if c.startswith('gap_'):
            rem = remaining['by_class'].get(c, 0)
            lines.append(f'| `{c}` | {n-rem} | {rem} |')
    lines += ['', '## Evidence and receiver boundaries', '',
              '- `140e8a400`/`140e834a0` are CLUB get/set dispatchers. CLUB server slot19 calls the TEAM_CONTAINER base reader on the same `this`. That base serializer does not make `[CLUB+0xb0]` or `[CLUB+0x100]` into main-row data: `table_extra_3` leaf paths are imported only from matched t71/t82 occurrence proofs and checked against dispatch/PE sites. `table_extra_24` is a separate TEAM sidecar. `table_extra_9` remains unbound.',
              '- `141063f30`/`1410668f0` operate on the table-9 NATIONAL_TEAM_CONTAINER. The table-9 setter thunk (`143f00000.c:31–39`) can try the linked table-10 NATION and then an NTC before falling back to the incoming NTC. Shared Nation XML is not identity of runtime receivers. `14105d510.c:449–463` reads a counted vector through a temporary, so the trace must not be mistaken for inline bytes at the vector pointer; each `Neu*` index is bound to its branch. Table-10 collection proofs retain the t55 client/server cursors and distinct object displacements.',
              '- `1411f1090`/`1411f4f70` dispatch TEAM_CONTAINER properties; some select a STARTING_RECORD type rather than a container member. `140ec0a60`/`140ecb5c0` do the analogous COMP dispatch through a different record manager. `144026550.c:10–18` and `143ca4a20.c:11–23` select by `(parent UID, rec_type)` before calling `141545680`; table 48 is distinguished from table 45 by controls against decoded CLUB/NTC/COMP identity sets, not the shared row vtable. The PE constructor bytes corroborate table IDs; they are not claimed to be assignments to the record-manager globals.',
              '- `141545680.c:134` stores `gams`/`apps` at `STARTING_RECORD+0x54` (u16); `:200` stores `stdt` at `+0x40` (date). t109’s `:89` anchor is not the `gams` store. `CMCs` routes to **`gams` in the proved CLUB and COMP branches**; the name/t98 hint is not allowed to overrule the actual dispatch. No owner-compatible NATION branch was proved for that occurrence. `1415446a0` is the corresponding getter; t98 semantic/profile claims and this physical routing result are separate.',
              '- `140fe3f20` is also a base property handler. Its appearance in the table-4 map is not a receiver proof. Conversely a `this` trace span at a reused offset does not imply that a property accesses the same field. `IsAC` is a positive no-op getter case, not excluded because a trace missed it.',
              '', '### Reader / trace audit', '',
              f"The machine-readable audit fingerprints all {len(full['blocker_helper_audit'])} t124 gap helpers. The call census inventories both registered reader slots, all visible direct callsites at each root and bounded same-`this` continuations. Indirect virtual sites, unresolved aliases and unproven composed arguments cannot establish a new field on their own.", '',
              '| Table | Server reader | Client reader | Trace rows client / server | Footer client / server |', '|---|---|---|---|---|']
    for table, model in full['reader_call_audit'].items():
        tt = {t['archive']: t for t in full['trace_status'] if str(t['table_id']) == table}
        lines.append(f"| {table} | `{model['19']['root']}` | `{model['20']['root']}` | {tt['client']['rows_ok']} / {tt['server']['rows_ok']} | {tt['client']['closed_to_footer']} / {tt['server']['closed_to_footer']} |")
    lines += ['', '## Remaining work', '', 'A held row keeps its original class and gives exact dispatch sites, candidate trace hits (never closure by themselves), and any branch-local call targets. Partial traces cannot prove absence. A missing decompilation is not necessarily the only blocker.', '']
    for x in remaining['priority_undecompiled'][:10]:
        lines.append(f"- `{x['va']}`: {x['gap_count']} held occurrence(s)")
    lines += ['', 'Inputs are read-only. The t108 filename used is `fourcc_mem_map_v2.json` (on disk). No game/editor/IDA execution or live collection was needed.', '',
              '```text', 'py -V:3.12 -B scripts/t125_big3_gap_closure.py',
              'py -V:3.12 -B scripts/t125_big3_gap_closure.py --selftest', '```', '']
    return '\n'.join(lines)


def follow(d, path):
    for k in path.strip('/').split('/'):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def verify(e, bundle):
    assert contains(8, 8, 10, 6) and not contains(8, 8, 10, 7) and not contains(8, 8, 16, 1)
    assert e.read_span('14105d510', 562, 2) and not e.read_span('14105d510', 563, 2)
    index = tuple(read_json(INDEX)['records'])
    assert len(index) == 56 and all(x['ok'] for x in index)
    assert e.readers[3][19]['root'] == '0x140e5b1a0' and e.readers[9][19]['root'] != e.readers[10][19]['root']
    fixed = bundle['big3_l3_v3.json']['rows']
    gaps = bundle['remaining_gaps_v3.json']['rows']
    held = {r['id'] for r in gaps}
    assert len(held) == len(gaps) and set(e.gaps) == held | {r['id'] for r in fixed if 't125_evidence' in r}
    assert Counter(r['entity'] for r in fixed) == ENTITIES
    lookup = {}
    for before, after in zip(e.base['rows'], fixed, strict=True):
        assert (before['id'], before['code']) == (after['id'], after['code'])
        if before['id'] not in e.gaps:
            assert before == after
            continue
        if before['id'] in held:
            assert before['new_class'] == after['new_class']
            continue
        ev = after['t125_evidence']
        lookup[before['entity'], before['code']] = ev
        assert ev['classification'] == after['new_class']
        assert ev['mem_off'] is not None or ev.get('exclusion_reason')
        for c in [ev, *ev['citations'], *ev.get('getter_citations', [])]:
            assert e.c.lines(ROOT / c['source_file'])[c['line_no']-1].strip() == c['text']
            assert Path(c['source_file']).stem == c['helper_va'][2:]
        for t in ev['unicorn']:
            raw = follow(e.trace, t['pointer'])
            assert raw['caller'] == t['caller_va'] and raw['wire_pos'] == t['wire_off']
            assert raw['obj_off_dec'] == t['obj_off'] and contains(t['obj_off'], t['width'], ev['mem_off'], ev['width'])
            assert t['table_id'] == ev['target_table']
        if 'artifact' in ev:
            obj = follow(read_json(ev['artifact']), ev['pointer'])
            assert before['code'] == (obj.get('code') or obj.get('field') or obj.get('parent'))
        for p in [*ev.get('verified_pe', []), *ev.get('pe_sites', []), *([ev['factory']] if 'factory' in ev else [])]:
            b = bytes.fromhex(p['bytes'])
            assert e.pe_bytes(p['file_off'], len(b)) == b
    for row in gaps:
        assert row['undecompiled_next_hop_vas'] == [h['va'] for h in row['next_hops'] if not h['decompiled']]
        assert all(e.c.get(va)[0] is None for va in row['undecompiled_next_hop_vas'])
    for entity, table in [('club', 45), ('nation', 45), ('comp', 48)]:
        ev = lookup[entity, 'CWRg']
        assert (ev['target_table'], ev['mem_off'], ev['inner_tag'], ev['width']) == (table, 84, 'gams', 2)
    for entity in ('club', 'comp'):
        assert lookup[entity, 'CMCs']['inner_tag'] == 'gams'
    assert ('nation', 'CMCs') not in lookup
    assert lookup['nation', 'Nfrp']['target_table'] == 9
    assert lookup['club', 'TCht']['target_table'] == 'table_extra_3'
    assert all(t['target_table'] != 'table_extra_9' for t in lookup.values())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest', action='store_true', help='Recompute and verify the saved evidence and conservation; does not write files.')
    args = ap.parse_args(argv)
    e = Engine()
    bundle = assemble(e)
    verify(e, bundle)
    markdown = report(bundle)
    if args.selftest:
        for name, data in bundle.items():
            path = OUT / name
            assert not path.exists() or path.read_text(encoding='utf-8') == text(data), f'stale output: {path}'
        path = OUT / 'REPORT.md'
        assert not path.exists() or path.read_text(encoding='utf-8') == markdown
        print('t125 --selftest PASS')
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, data in bundle.items():
            save(name, data)
            print((OUT / name).relative_to(ROOT).as_posix())
        save('REPORT.md', markdown)
        print((OUT / 'REPORT.md').relative_to(ROOT).as_posix())
    s = bundle['coverage_summary_v3.json']['t125']
    print(f"gross {s['l3']}/1034 ({s['gross_pct']:.1f}%); net {s['l3']}/{s['net_denominator']} ({s['net_pct']:.1f}%); gaps 294 -> {s['gaps']}; excluded {s['excluded_non_db']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
