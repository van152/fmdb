#!/usr/bin/env python3
"""Build t62: bounded static EDfx/EDsc dispatcher, source/sink and exclusion audit."""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import deque
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
from struct import unpack_from
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t62/out'
EXE = Path('D:/tmp2b/fm24/input/editor.exe')
EXE_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
IDA = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
LEDGER = 'reports/club_nation_subtable_schema.json'
OLD = 'scratch/t53/out/discovery_crs_wire.json'
SHELL = bytes.fromhex('0201666d662e080000')
TARGETS = ('EDfx', 'EDsc')


class Check(Exception):
    pass


def ck(cond, msg):
    if not cond:
        raise Check(str(msg))


def h(data):
    return sha256(data).hexdigest()


def j(path):
    return json.loads((ROOT / path).read_bytes())


def patterns(key):
    return {f'{codec}_{order}': word.encode(codec) for codec in ('ascii', 'utf-16le', 'utf-16be')
            for order, word in (('forward', key), ('reverse', key[::-1]))}


def signed32(x):
    return (x + 0x80000000) % 0x100000000 - 0x80000000


def branch(cc, a, b):
    if cc in ('jg', 'jle', 'jl', 'jge'):
        a, b = signed32(a), signed32(b)
    return {'jg': a > b, 'jle': a <= b, 'jl': a < b, 'jge': a >= b,
            'ja': a > b, 'jbe': a <= b, 'je': a == b, 'jne': a != b}[cc]


class Image:
    def __init__(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from t05_pe import PE
        self.p = p = PE(EXE)
        ck(h(p.raw) == EXE_SHA, 'editor.exe SHA-256 mismatch')
        p.pe.parse_data_directories(directories=[3])
        self.ranges = sorted((e.struct.BeginAddress, e.struct.EndAddress) for e in p.pe.DIRECTORY_ENTRY_EXCEPTION)
        self.starts = [a for a, _ in self.ranges]
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.ins = {}

    def extent(self, off):
        r = self.p.f2r(off)
        i = bisect_right(self.starts, r) - 1
        if i >= 0 and r < self.ranges[i][1]:
            return tuple(self.p.r2f(x) for x in self.ranges[i])
        return None

    def dec(self, off):
        if off not in self.ins:
            self.ins[off] = next(self.md.disasm(self.p.raw[off:off+15], self.p.f2va(off), count=1))
        return self.ins[off]

    def target(self, i):
        return self.p.va2f(i.operands[0].imm)

    def cfg(self, entry, selected_edge=None):
        begin, end = self.extent(entry)
        ck(begin == entry and end - begin <= 0x20000, f'extent {entry:#x}')
        todo = deque([entry]); seen = set(); outside = []; indirect = []; edges = []
        while todo:
            a = todo.popleft()
            if a in seen:
                continue
            seen.add(a)
            i = self.dec(a); n = a + i.size
            if i.mnemonic.startswith('j'):
                if i.operands[0].type != 2:
                    if selected_edge and a == selected_edge[0]:
                        out = [selected_edge[1]]
                    else:
                        indirect.append(a); out = []
                else:
                    out = [self.target(i)] + ([n] if i.mnemonic != 'jmp' else [])
            elif i.mnemonic in ('ret', 'retf', 'int3', 'ud2', 'iretq'):
                out = []
            else:
                out = [n]
            ck(n <= end, f'instruction crosses extent {a:#x}')
            for b in out:
                if b is not None and begin <= b < end:
                    todo.append(b); edges.append([a, b])
                else:
                    outside.append([a, b])
        return seen, dict(entry=begin, end_exclusive=end, reachable=len(seen),
                          ip_sha256=h(json.dumps(sorted(seen)).encode()), edge_sha256=h(json.dumps(sorted(edges)).encode()),
                          unknown_indirect_jmps=sorted(indirect), out_of_extent_edges=sorted(outside))

    def disp_key(self, key):
        # Start after prologue/lifecycle setup. Only the key-dependent compare tree.
        value = int.from_bytes(key, 'big'); at = 0x281cb; trace = []
        ecx = flags = None
        for _ in range(40):
            i = self.dec(at); trace.append(at)
            if at == 0x29c43 or at == 0x2a684:
                return dict(input=int.from_bytes(key, 'big'), trace=trace, entry=at)
            if at == 0x282d6:
                # lea table base, movsxd rel32[index], add base, jmp rdx
                lea, load, add, _ = (self.dec(x) for x in (0x282c8, 0x282cf, 0x282d3, at))
                ck((lea.op_str.startswith('rcx, [rip'), load.op_str, add.op_str, i.op_str) ==
                   (True, 'rdx, dword ptr [rcx + rsi*4]', 'rdx, rcx', 'rdx'), 'table base/load/add/jmp')
                va = lea.address + lea.size + lea.operands[1].mem.disp
                size = self.dec(0x282bf).operands[1].imm + 1
                base = self.p.va2f(va); cell = base + 4 * value
                ck(0 <= value < size, 'rel32 index')
                rel = unpack_from('<i', self.p.raw, cell)[0]
                dst = self.p.va2f(va + rel)
                cells = [self.p.va2f(va + unpack_from('<i', self.p.raw, base + 4*k)[0]) for k in range(size)]
                return dict(input=int.from_bytes(key, 'big'), trace=trace, entry=dst, table=base, table_va=va, entries=size,
                            index=value, cell=cell, rel32=rel, cell_bytes=self.p.raw[cell:cell+4].hex(),
                            same_target_indices=[x for x,y in enumerate(cells) if y == dst])
            if i.mnemonic == 'cmp' and i.operands[1].type == 2 and i.reg_name(i.operands[0].reg) in ('esi','ecx'):
                lhs = value if i.reg_name(i.operands[0].reg) == 'esi' else ecx
                flags = (lhs, i.operands[1].imm & 0xffffffff)
            elif i.mnemonic == 'lea' and i.op_str.startswith('ecx, [rsi ') and not i.operands[1].mem.index:
                ecx = (value + i.operands[1].mem.disp) & 0xffffffff
            elif i.mnemonic == 'add' and i.op_str.startswith('esi, ') and i.operands[1].type == 2:
                value = (value + i.operands[1].imm) & 0xffffffff
                flags = None
            elif i.mnemonic.startswith('j'):
                if i.mnemonic == 'jmp' or (flags is not None and branch(i.mnemonic, *flags)):
                    at = self.target(i)
                    continue
            elif at not in (0x282c8, 0x282cf, 0x282d3):
                raise Check(f'unsupported key instruction {at:#x} {i.mnemonic} {i.op_str}')
            at += i.size
        raise Check('key walk exceeded limit')

    def record(self, off):
        i = self.dec(off); rec = dict(offset=off, va=i.address, bytes=i.bytes.hex(), asm=f'{i.mnemonic} {i.op_str}'.strip())
        if (i.mnemonic.startswith('j') or i.mnemonic == 'call') and i.operands[0].type == 2:
            rec['target'] = self.target(i)
        rec['rip_targets'] = [i.address + i.size + o.mem.disp for o in i.operands if o.type == 3 and i.reg_name(o.mem.base) == 'rip']
        ext = self.extent(off)
        if ext:
            rec['extent_entry'] = ext[0]
        return rec


def archives():
    sys.path.append('D:/tmp2b/fm24/tools/python')  # Local zstandard if not installed on the standard path.
    import zstandard as zstd
    root = Path(os.environ.get('FM24_DB_DIR', str(ROOT / 'scratch/data')))
    ck(root.drive.upper() != 'Z:' and root.resolve().drive.upper() != 'Z:', 'Z: forbidden')
    result = {}
    for side, expected in (('client', 31), ('server', 77)):
        raw = (root / (side + '_db.dat')).read_bytes()
        toc, base = (x + 17 for x in unpack_from('<QQ', raw, 17))
        ck(base == 34 and raw[8:17] == raw[toc:toc+9] == SHELL, 'archive shell')
        dec = zstd.ZstdDecompressor().decompressobj()
        toc_bytes = dec.decompress(raw[toc+9:]); ck(dec.eof and not dec.unused_data, 'directory frame end')
        pos = 0; rows = {}
        def take(n):
            nonlocal pos
            ck(pos+n <= len(toc_bytes), 'short directory'); pos += n
            return toc_bytes[pos-n:pos]
        def u32(): return int.from_bytes(take(4), 'little')
        def text(): return take(u32()).decode('utf-8')
        pending = [(PurePosixPath(), 1)]
        while pending:
            parent, count = pending.pop()
            if not count: continue
            pending.append((parent, count-1))
            folder = parent / text()
            for _ in range(u32()):
                path = (folder / (text() + text())).as_posix()
                ck(path not in rows and '..' not in PurePosixPath(path).parts, 'invalid directory name')
                rel, packed, size, _, _ = unpack_from('<5Q', take(40))
                rows[path] = (base+rel, packed, size)
            pending.append((folder, u32()))
        ck(pos == len(toc_bytes) and len(rows) == expected, f'{side}: directory walk')
        controls = {}
        for tid, count in ((10, 251), (25, 7047)):
            path = f'{side}_db/table_{tid}.dat'
            a, w, n = rows[path]; bound = min((t[0] for t in rows.values() if t[0] > a), default=toc)
            ck(base <= a < a+w <= bound and raw[a:a+4] == bytes.fromhex('28b52ffd'), path)
            d = zstd.ZstdDecompressor().decompressobj(); data = d.decompress(raw[a:a+w]); ck(d.eof and not d.unused_data and len(data) == n, path)
            ck(data[2:6] == b'tad.' and unpack_from('<I', data, 8)[0] == count, path)
            controls[path] = dict(start=a, packed=w, size=n, bound=bound, prefix13=data[:13].hex(), count=count, sha256=h(data))
        result[side] = dict(archive_sha256=h(raw), directory_sha256=h(toc_bytes), data_base=base, toc_offset=toc,
                            entries=sorted(rows), literal_names=[s for s in sorted(rows) if any(k.lower() in s.lower() for k in TARGETS)],
                            header_controls=controls)
    return result


# Instruction slices are observations. A hop is not an assertion that all callers take it.
GROUPS = {
    'common_dispatch': '28163 28166 28169 2816b 2816e 2817e 2818e 2819e 281a3 281a6 281b7 281c6 281c8 2a684 2a686 29f68 29f6a 29f7f',
    'generic_ui_caller': '2b47a 2b490 2b495 2b498 2b49d 2b4a2 2b4a7 2b4a9 2b4ab 2b4ba',
    'EDfx_gate': '29c37 29c3d 29c43 29c48 29c4e 29c51 29c57 29c5a 29c66 29c69 29c6c 29c72 29c75 29c78 29c80 29c85',
    'EDfx_rules_input': '90803 9080b 90813 90818 2cdc0 1b7a313 1b7a318 1b7a327 9082e 90864 2ce20 1b7a3e7 1b7a3ec 1b7a3fc 1b7a406 9087b 90880 9088b 90899 908b0 908b8 a2d230 37d5648 a2d350 37d5c47 37d5c5b 37d5c70 37d5cb7 37d5cbc 908bd 908c3 afe0f0 385d63d 385d681 385d6a6 908ce 6288b0 908d8 908e7 908f1 908f6 90906 af8918 af9659 af9876 af9e31 afdf70',
    'EDfx_day_query': '90918 9091e 9097a 9098e 9099d 909b8 909ca 909cf 909d7 909d9 103f9f0 3d5c080 3d5c082 3d5c091 3d5c098 90a18 90a1b 90a1e 90a21 90a24 90a2c b029a3 b029a7 b029aa b029ad b02a88 b02af1 b02af5 b02af9 b02b3e b02bf0 b02bf7 b02bff b02c03 b02c07 b02c7e b02c81 b02ca5 b02ca8 b02cba b02ccd b02cd4 b02e43 b02e48 90a32 90ae0 90aa8 90e1c 90f93',
    'EDfx_ui_return': '90fc3 90fc8 90fd3 90fdb 90fe3 90ffc 83d5d2 83d5d6',
    'EDsc_gate': '29389 2938b 29391 29396 29399 2939f 293a2 293a8 293af 293b6 293c2 293c5 293c8 293ce 293d1 293d4 293dc 293df 293e4 2a238 2a23b 2a23e 2a246 2a24c 2a24f 2a252 2a257',
    'EDsc_comp_consumer': '6c130 6c133 6c138 6c13b 6c146 6c151 6c154 6c157 6c15c 6c163 6c1b4 6c1d1 6c1dc 6c1f2 6c273 6c2f3 6c2fb 6c305 6c30a 6c36b 6c381 6c38e 6c391 6c3a2 6c3b1 6c3e6 6c432 6c517 6c5b0 6c5fa 6c692 6c731 6c20d 6f230 6c21a 6c92c 6c931 6c22a 6c22f 6c237',
    'EDsc_nation_consumer': '6bb13 6bb16 6bb19 6bb37 6bb5b 6bb6e 6bb87 6bb8e 6bb95 6bb9b 6bbeb 6bc03 6bc14 6bc23 6bc2b 6bc6b 6be56 6be59 6be5c 6be5f 6be62 6be6a 6beab 6bed6 6c0ab 6c0c3 6c0c8 6c0d0',
    'separate_collection_control': 'e8b4db e8c1e8 e8c67e 15e9830 44d7c6a 44d7c71 44d7cc5 44d7cd1 44d83ba',
}

HOPS = {
    'EDfx_output': [
        ('29c37 29c3d 29c69 29c6c 29c80', 'Exact EDfx match, non-null selected NATION/type 10, separate context/object/output args.'),
        ('90818 2cdc0 1b7a318 90864 2ce20 1b7a3ec', 'Enumerate context+0x20/fles rule/value rows.'),
        ('9087b 90880 908b0 908b8 a2d350 37d5c47 37d5c70', 'The comp test gates preparation of an in-memory rule wrapper; a2d350 uses +0x18 if non-null, otherwise hunts comp in the supplied object.'),
        ('9082e 908c3 afe0f0 385d681 385d6a6 908ce 6288b0 908d8', 'Remove matching cached entry by pointer, attach +0x1c0 at wrapper+0x38, then call evaluation helper. Not a file open.'),
        ('908e7 90906 af8918 af9659 af9876', 'Prepare calendar context for year; obtains in-memory entries and calls per-entry helper.'),
        ('909d7 909d9 103f9f0 3d5c082 3d5c091 90a21 90a24', 'Pass NATION+0x108 backlink as R9, not as this or as a stream. Both date arguments point to the same day.'),
        ('b029ad b02af5 b02af9 b02b3e b02bf0 b02bf7 b02c03 b02c81 b02cba b02ccd b02cd4', 'Query day-bucket vectors starting at calendar this+0x38 (editor context+0x1f8); conditional filter compares backlink against in-memory record relationships.'),
        ('90aa8 90f93 90fc3 90fc8 90fd3 83d5d2 83d5d6 29c85 29f68', 'Append a projected row (including fallback), then box/move UI list to caller, no observed serialization of the generated list.'),
    ],
    'EDsc_dispatch_and_consumers': [
        ('2b47a 2b490 2b49d 2b4a2 28163 2b4a9 2b4ba', 'Generic UI caller passes computed key + selected object and on success inserts the returned value under the original key. Does not prove which external schema instance invokes this at runtime.'),
        ('282b9 282bf 282c2 282c8 282cf 282d3 282d6', 'One verified indirect edge: EDsc selects rel32 slot 0x32; see xref.json for table bytes and neighboring controls.'),
        ('29389 2938b 29396 2939f 293af 293b6 293c2 293c5 293c8', 'Context gate: AL=0 takes empty success; otherwise requires non-null selected object, BPL=0 and global context+0x54c nonzero. Then split type 25/other.'),
        ('293ce 293d1 293d4 293dc 293df 6c130 6c154 6c157 6c273', 'COMP/type25 enters schedule consumer with R9B=1; preserved into collector (not an archive client/server mode).'),
        ('6c2fb 6c305 6c30a 6c391 6c3a2 6c3b1 6c5fa 6c692 6c731', 'Collector conditionally prepares shared context+0x1c0 from context-side entries, iterates and builds schedule items. Conditions retained; not all run together.'),
        ('6c20d 6f230 6c21a 6c22a 6c22f 6c237 83d5d2 83d5d6', 'COMP-side wrapper processes temporary results and moves boxed output to caller.'),
        ('2a238 2a23b 2a246 2a252 6bb16 6bb19', 'Non-25 rechecks type: only NATION/type10 enters alternate schedule consumer; other types reject via 0x2a684.'),
        ('6bb37 6bb5b 6bb6e 6bb9b 6bc14 6bc6b 6be59 6be5f 6be62 6be6a 6bed6 6c0d0', 'Nation wrapper may return empty value; otherwise enumerates inputs, delegates per picked competition with R9D=0, appends projected rows and returns boxed list.'),
    ],
}

EXCLUSIONS = [
    dict(id='E1', reject='EDfx literal is a file opener, constructor or stream sink', scope='exact literal operand in this PE',
         witness='0x29c39 is inside cmp esi,0x45446678 at 0x29c37; 0x29c3d selects by equality',
         reopen='Find another byte match or a proven computed EDfx key reaching a persistence path.'),
    dict(id='E2', reject='The traced EDfx UI result is persisted by the dispatch arm', scope='0x29c80 call and immediate return path, not upstream rules or arbitrary callers',
         witness='0x90fc8/90fd3 → 0x83d5a0 saves list to caller output. 0x29c85 returns via 0x29f68; no archive stream handed the result on this path.',
         reopen='Provide an alias from the boxed list itself to a concrete writer, not merely a persisted input of the generator.'),
    dict(id='E3', reject='EDsc has no editor dispatch because ASCII and UTF-16 scans are empty', scope='this PE and exact key at 0x28150',
         witness='0x282b9 + 0xbabb8ccf, EDsc index 0x32, cell 0x2a8b8 → 0x29389. EDsb index 0x31 → 0x2a684.',
         reopen='Evidence that the raw key is normalized differently before this entry or that the PE/key replay is wrong; the arm itself is static, not observed UI usage.'),
    dict(id='E4', reject='EDsc dispatch adds a slot to the modern NATION main reader', scope='t55 client/server table_10 replay only',
         witness='New edge belongs to UI dispatcher 0x28150; t55 reader is 0x103fac0. Type-10 input to 0x6bb00 is not a row stream. Old held/no dispatch observation preserved.',
         reopen='Supply an EDsc output/member alias into an actual modern NATION transfer site, with raw cursor and replay.'),
    dict(id='E5', reject='EDfx/EDsc use the shared Tchl helper merely because the v3 inventory groups them', scope='traced UI arms versus t39/t44 positive controls, not all indirect calls',
         witness='0x15e9830 → 0x44d7c6a/71 selects VA 0x141b60158/+0x80, owner match at 0x44d7cc5/cd1. The audited day query takes this=context+0x1c0, indexes date buckets, and filters a backlink.',
         reopen='Show a matching table/element pointer or adapter that passes this precise shared global vector into one of the audited schedule inputs.'),
    dict(id='E6', reject='These stock archives have a member whose path contains EDfx or EDsc', scope='directory names only; not numeric members, packed data, external rule files or other archives',
         witness='Independent FMF directory parses: client 31, server 77, neither contains either substring case-insensitively; t10/t25 header controls present in both.',
         reopen='New directory match in the pinned archives, or separately prove an indirect mapped member using reader and writer.'),
    dict(id='E7', reject='This partial trace binds EDfx to table_10 or table_25 as its backing', scope='identification gate; not an absence claim for either member',
         witness='Type tags and competition/backlink pointers appear but the actual queried vector comes from calendar context. No transfer/write pair for calendar/rule content and no decoded region match.',
         reopen='Trace the producer of the exact rule/fixture content into a specific deserializer and the reverse into a writer, then replay the proven region independently.'),
]


def provenance():
    paths = [MASTER, IDA, LEDGER, OLD, 'scratch/t55/out/REPORT.md', 'scratch/t55/out/field_map.json',
             'scratch/t27/out/replication.md', 'scratch/t39/out/REPORT.md', 'scratch/t44/out/REPORT.md', 'scratch/t59/out/REPORT.md']
    led = j(LEDGER); snap = led['v3_baseline']; paths += [snap['json_path'], snap['markdown_path']]
    d = {p: h((ROOT / p).read_bytes()) for p in paths}
    ck(d[snap['json_path']] == snap['json_sha256'] and d[snap['markdown_path']] == snap['markdown_sha256'], 'v3 digests')
    manifest = j('evidence/MANIFEST.json')
    # MANIFEST is an object containing one path/hash list.
    if isinstance(manifest, dict):
        manifest = next(v for v in manifest.values() if isinstance(v, list) and v and isinstance(v[0], dict) and 'path' in v[0])
    md = {r['path']:r['sha256'] for r in manifest}
    ck(all(d[p] == md[p] for p in (MASTER,IDA)) and EXE_SHA in (ROOT/IDA).read_text(encoding='utf-8'), 'frozen manifest/PE provenance')
    v3 = j(snap['json_path']); old = j(OLD); master = j(MASTER)
    names = {'EDfx','EDsc','AXML','Tchl'}
    scopes = {}
    for family, sources in (('entity', master['entities']), ('rule_group', master['rule_groups'])):
        for name, blocks in sources.items():
            if family == 'entity' and name not in ('club.xml','nation.xml'): continue
            for block in blocks:
                for idx, f in enumerate(block.get('fields', [])):
                    if f['field'] in names and (family == 'entity' or f['field'] in TARGETS):
                        scopes[f'{family}:{name}#{block["id"]}:{idx}'] = f
    ck([f['field'] for f in scopes.values()].count('EDsc') == 2, 'frozen EDsc scopes')
    row = next(r for r in led['nation_main_row_fields']['source_records']['field_map']['fields'] if r['code'] == 'EDsc')
    ck(row['grade'] == 'held' and row['slot'] is None, 't55 source grade')
    ck(v3['negative_regressions'] == led['negative_regressions'], 'negative regressions drift')
    return dict(sources=d, manifest_sha256=h((ROOT/'evidence/MANIFEST.json').read_bytes()), frozen_scopes=scopes,
                v3_baseline=snap, v3_inventory_verbatim=v3['inventory_reconciliation'], negative_regressions_verbatim=led['negative_regressions'],
                t53_edsc_status=old['EDsc']['status'], t55_EDsc_verbatim=row)


def build():
    img = Image(); p = img.p; literal = {}
    for key in TARGETS:
        literal[key] = {}
        for name, seq in patterns(key).items():
            matches = []
            for m in re.finditer(b'(?='+re.escape(seq)+b')', p.raw):
                q = m.start(); ck(key == 'EDfx' and q == 0x29c39 and name == 'ascii_reverse', f'new unclassified literal {key}:{name}:{q:#x}')
                matches.append(dict(offset=q, va=p.f2va(q), section=p.section_of(q), bytes=seq.hex(),
                                    instruction=0x29c37, kind='comparison', roles_excluded=['collection_opener','container_constructor','serialization_sink']))
            literal[key][name] = matches
    ck(len(literal['EDfx']['ascii_reverse']) == 1, 'missing EDfx literal')
    keys = {k:img.disp_key(k.encode()) for k in ('EDfx','EDsc','EDsb','EDsd')}
    ck([keys[k]['entry'] for k in keys] == [0x29c43,0x29389,0x2a684,0x293e9], 'key routes')
    ck(keys['EDsc']['same_target_indices'] == [0x32], 'EDsc table alias')
    image = dict(path=EXE.as_posix(), sha256=EXE_SHA, size=len(p.raw), image_base=p.base, sections=p._secs)
    groups = {k:[int(a,16) for a in v.split()] for k,v in GROUPS.items()}
    groups['key_route'] = sorted({a for r in keys.values() for a in r['trace']})
    all_sites = sorted(set().union(*groups.values()))
    specs = []; reached = {}; proof = (0x282d6,0x29389)
    for entry in sorted({img.extent(a)[0] for a in all_sites if img.extent(a)}):
        reachable, r = img.cfg(entry)
        if entry == 0x28150:
            specs.append(r)
            reachable, r = img.cfg(entry, proof)
            r['extra_edge'] = list(proof)
            r['edge_key'] = 'EDsc only; other jump table arms unresolved here'
        specs.append(r); reached[entry] = reachable
    # The 0x3d5c080 leaf has no unwind entry; only decoded, hand-bounded branch/return slice.
    code = {}
    for a in all_sites:
        r = img.record(a)
        if 'extent_entry' in r:
            ck(a in reached[r['extent_entry']], f'witness not reachable from audited entry {a:#x}')
        else:
            r['reachability'] = 'explicit thunk/leaf witness, no RUNTIME_FUNCTION extent claimed'
        code[f'{a:#x}'] = r
    chain = dict(status='partial', L4=0, image=image, provenance=provenance(),
        conclusions=dict(EDfx=dict(dispatch='confirmed', output='generated UI list on traced arm', reader=None, writer=None, member=None, status='upstream_persistence_unbound'),
                         EDsc=dict(dispatch='confirmed_nonliteral', consumers={'25':0x6c120,'10':0x6bb00},
                                   reader=None, writer=None, member=None, status='ui_consumers_found_no_main_wire_slot_inferred_from_this_dispatch')),
        groups=groups, instructions=code, cfg=specs, hops={k:[dict(sites=[int(x,16) for x in s.split()], observation=n) for s,n in v] for k,v in HOPS.items()},
        limits=['Selected-key dispatch replay starts after the prologue, not a runtime claim or a general symbolic engine.',
                'CFG: no call traversal except explicit hops; unknown indirect branches and extent-external edges are preserved, not dead.',
                'Context gates and R9 helper flag are not an archive-mode result.',
                'No verified assignment from upstream rule/calendar input to a .dat reader or writer. No accepted row_offset.'])
    xref = dict(image=image, scope='Full raw PE overlap search for both byte orders in ASCII and UTF-16LE/BE. Additionally one solved key-specific computed dispatcher; not all symbolic encodings.',
                literal=literal, key_routes=keys, nonliteral=[dict(code='EDsc', kind='computed_dispatch', index_site=0x282b9, jump_site=0x282d6,
                    table_cell=keys['EDsc']['cell'], arm=0x29389, role='generated collection dispatch, not a tagged disk opener or serializer')])
    exclusions = dict(L4=0, excludes=EXCLUSIONS, archive_scope='Directory and t10/t25 header controls only. No EDfx/EDsc member or region accepted for item replay.', archive=archives())
    OUT.mkdir(parents=True, exist_ok=True)
    for name, item in (('xref',xref),('chain',chain),('exclusions',exclusions)):
        (OUT/f'{name}.json').write_text(json.dumps(item, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('t62 partial: EDsc UI dispatch and both consumers proven; EDfx persistent upstream unbound; L4=0')


def selftest():
    ck(branch('jg', 0, 0xffffffff) and not branch('ja',0,0xffffffff), 'signed vs unsigned')
    ck(not branch('ja',0x43,0x43) and branch('ja',0x44,0x43), 'rel32 bound')
    ck((int.from_bytes(b'EDsc','big')+0xbabb8ccf)&0xffffffff == 0x32, 'EDsc normalized key')
    ck(patterns('EDfx')['ascii_reverse'] == b'xfDE' and len(set(patterns('EDsc').values())) == 6,'literal encodings')
    print('t62 builder selftest PASS')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    opts = parser.add_mutually_exclusive_group()
    opts.add_argument('--build', action='store_true', help='rebuild the three JSON ledgers (default)')
    opts.add_argument('--selftest', action='store_true', help='test arithmetic/encoding helpers without inputs')
    args = parser.parse_args()
    try:
        selftest() if args.selftest else build()
    except Check as e:
        print(f't62 check failed: {e}', file=sys.stderr); return 1
    except Exception as e:
        print(f't62 fatal: {type(e).__name__}: {e}', file=sys.stderr); return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
