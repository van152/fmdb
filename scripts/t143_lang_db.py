#!/usr/bin/env python3
"""Read-only FM24 2400/2430 localization decoder and t133 UID join."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(_cfg.VENDOR_DIR))
import zstandard as zstd
import t133_fm24_reader_v2 as core

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t143/out'
SOURCES = (
    ('lang_db_2400', Path(str(_cfg.LANG_DB_DAT)), 'lang_db', 0x0def),
    ('lang_update_db', ROOT / 'scratch/data/lang_update_db.dat', 'lang_update_db', 0x0df1),
)
MAGIC = bytes.fromhex('03 01 74 61 64 2e')
U32 = struct.Struct('<I')
U16 = struct.Struct('<H')
VARIANT = struct.Struct('<HB')
PERSON_TAIL = struct.Struct('<IHB')
ZERO = bytes(4)
# Tokens describe every byte AFTER the table row key. S = UTF-8 string,
# B = u8, H = u16, V = counted vector of (string, u16 field type, u8 form).
LAYOUTS = {
    0: 'SBSBV', 2: 'SBV', 3: 'SBSBSSSBSVH', 5: 'SBSSSBSBV', 6: 'SBSBV',
    7: 'SB', 9: 'SBSBSSV', 18: 'SSSSBBBBV', 19: 'SV', 21: 'SSBBV',
    23: 'SBSBSBV', 25: 'SBSBSV', 35: 'BBV', 47: 'SBSBV', 56: 'SBSBB',
}
# Localization t9 is NATION text, not the core t9 NATIONAL_TEAM_CONTAINER.
CORE_IDS = {tid: (10 if tid == 9 else tid) for tid in LAYOUTS}
FOCUS = (8, 1000002, 1000003)
SHOWCASE = {
    25: (11, 1301394, 1301396, 31051584, 1301385, 22, 32, 16, 130026, 95, 5624449, 5624451, 23397138),
    9: (765, 796, 771, 769, 776, 1651, 1649, 110, 116, 111, 124, 138),
    3: (679, 680, 1736, 602, 915, 676, 630, 1708, 868, 907, 992, 1135, 1139, 406, 409, 414, 23366052),
    0: (102406, 109375, 150936, 150967, 136386, 106965, 23397143),
    21: (102969, 676, 680, 5114325, 5114336, 1056, 1040, 977, 28096287, 624, 103239, 135465, 131131, 23148989),
    2: (100023, 100062, 341, 270, 370, 553, 103194, 128046, 103195, 103225, 128037, 128042, 128055),
}
# Separately selected from multilingual data for concrete slot/form evidence.
WITNESSES = {(10, 9, 5), (12, 9, 5), (15, 9, 5), (24, 9, 5),
             (10, 35, 1), (32, 9, 5), (12, 21, 676)}
MEMBER = re.compile(r'(\d+)(?:_(\d+)|(person_names))\.dat')


def check(ok, message):
    if not ok:
        raise ValueError(message)


class LanguageArchive:
    def __init__(self, source):
        self.label, self.path, folder, self.version = source
        self.data = self.path.read_bytes()
        self.header = MAGIC + U16.pack(self.version)
        check(self.data.startswith(self.header) and self.data[8:17] == core.base.FMF_MAGIC,
              f'{self.path}: expected 8-byte DAT shell and embedded FMF')
        self.layout = core.base.archive_layout(self.data)
        self.decoder = zstd.ZstdDecompressor()
        entries = self.layout['entries']
        self.entries = {}
        p = self.layout['data_base']
        for e in sorted(entries, key=lambda e: e['offset']):
            off = self.layout['data_base'] + e['offset']
            check(off == p and e['packed_size'] > 0, 'FMF member gap/overlap')
            p += e['packed_size']
        check(p == self.layout['toc_offset'], 'FMF data region does not end at TOC')
        for e in entries:  # Preserve directory order in the exported inventory.
            root, sep, name = e['path'].partition('/')
            m = MEMBER.fullmatch(name)
            check(sep and root == folder and m, f"unexpected FMF path {e['path']}")
            lid, tid = int(m[1]), int(m[2]) if m[2] else None
            check((lid, tid) not in self.entries, f"duplicate member {e['path']}")
            self.entries[lid, tid] = e
        langs = {lid for lid, _ in self.entries}
        check(len(langs) == 22 and self.entries.keys() ==
              {(lid, tid) for lid in langs for tid in (*LAYOUTS, None)}, 'FMF inventory mismatch')

    def payload(self, e):
        start = self.layout['data_base'] + e['offset']
        frame = self.decoder.decompressobj()
        raw = frame.decompress(self.data[start:start + e['packed_size']])
        check(frame.eof and not frame.unused_data and len(raw) == e['size'],
              f"{e['path']}: compressed frame or TOC size mismatch")
        return raw

    def metadata(self):
        return dict(input=str(self.path), file_bytes=len(self.data),
                    sha256=sha256(self.data).hexdigest(), dat_header_hex=self.header.hex(),
                    fmf_header_offset=8, data_base=self.layout['data_base'],
                    toc_offset=self.layout['toc_offset'], member_count=len(self.entries))


class Cursor:
    def __init__(self, raw, p):
        self.raw, self.p = raw, p

    def unpack(self, fmt):
        value = fmt.unpack_from(self.raw, self.p)
        self.p += fmt.size
        return value

    def byte(self):
        value = self.raw[self.p]
        self.p += 1
        return value

    def string(self):
        (size,) = self.unpack(U32)
        if size == 0xffffffff:
            return None
        end = self.p + size
        if end > len(self.raw):
            raise ValueError(f'string overruns member at {self.p - 4:#x} (length {size})')
        text = self.raw[self.p:end].decode('utf-8', errors='strict')
        self.p = end
        return text

    def variants(self):
        return tuple((self.string(), *self.unpack(VARIANT)) for _ in range(self.byte()))


def emit_string(text, out):
    if text is None:
        out.extend(b'\xff' * 4)
    else:
        b = text.encode('utf-8')
        out.extend(U32.pack(len(b)))
        out.extend(b)


def emit_row(key, fields, layout, out):
    out.extend(U32.pack(key))
    for token, value in zip(layout, fields, strict=True):
        if token == 'S':
            emit_string(value, out)
        elif token == 'B':
            out.append(value)
        elif token == 'H':
            out.extend(U16.pack(value))
        else:
            out.append(len(value))
            for text, field_type, form in value:
                emit_string(text, out)
                out.extend(VARIANT.pack(field_type, form))


def decode(raw, tid, header, *, roundtrip=False, visit=None):
    """Stream typed rows; optionally re-encode all fields and compare every byte."""
    check(raw.startswith(header) and len(raw) >= 12, 'bad member header')
    p = Cursor(raw, 8)
    # Assemble the header from its grammar, not a copy of the input bytes.
    rebuilt = bytearray(header) if roundtrip else None
    declared = n = variants = empty = null = texts = variant_texts = 0
    field_forms = Counter()
    if tid is None:
        declared = None
        end = len(raw) - 4
        check(raw[end:] == ZERO, 'person_names missing zero terminator')
        while raw[p.p:p.p + 4] != ZERO:
            offset = p.p
            slots = (p.string(), p.string(), p.string(), p.string())
            tail = p.unpack(PERSON_TAIL)
            check(slots[0] and p.p <= end, f'bad person_names row at {offset:#x}')
            n += 1
            for slot in slots:
                texts += bool(slot)
                empty += slot == ''
                null += slot is None
            if roundtrip:
                for slot in slots:
                    emit_string(slot, rebuilt)
                rebuilt.extend(PERSON_TAIL.pack(*tail))
        if roundtrip:
            rebuilt.extend(ZERO)
    else:
        layout = LAYOUTS[tid]
        (declared,) = p.unpack(U32)
        check(declared <= (len(raw) - 12) // 4, 'impossible record count')
        if roundtrip:
            rebuilt.extend(U32.pack(declared))
        end = len(raw)
        readers = {'S': p.string, 'B': p.byte, 'H': lambda: p.unpack(U16)[0], 'V': p.variants}
        read_fields = tuple(readers[token] for token in layout)
        strings = tuple(i for i, token in enumerate(layout) if token == 'S')
        vi = layout.find('V')
        prior = -1
        for n in range(1, declared + 1):
            offset = p.p
            (key,) = p.unpack(U32)
            if key <= prior:
                raise ValueError(f'unordered or duplicate row key at {offset:#x}')
            prior = key
            fields = tuple(read() for read in read_fields)
            for i in strings:
                text = fields[i]
                texts += bool(text)
                empty += text == ''
                null += text is None
            if vi >= 0:
                vv = fields[vi]
                variants += len(vv)
                for text, field_type, form in vv:
                    variant_texts += bool(text)
                    empty += text == ''
                    null += text is None
                    field_forms[field_type, form] += 1
            if visit is not None:
                visit(key, offset, fields)
            if roundtrip:
                emit_row(key, fields, layout, rebuilt)
    diff = p.p - end
    check(diff == 0, f'closure diff={diff:+d} (cursor {p.p:#x}, boundary {end:#x})')
    check(not roundtrip or rebuilt == raw, 'byte-exact roundtrip differs')
    return dict(records=n, declared_records=declared, string_entries=texts + variant_texts,
                fixed_string_entries=texts, variant_string_entries=variant_texts,
                variant_records=variants, empty_string_slots=empty, null_string_slots=null,
                decoded_end=p.p, footer_offset=end, footer_bytes=len(raw)-end,
                diff=diff, byte_exact=True if roundtrip else None,
                variant_field_forms={f'{f}:{v}': c for (f, v), c in sorted(field_forms.items())})


def core_rows(ar, tid, specs, traces):
    """Adapt the t133 walkers, including selector programs, to stream identities."""
    key = (ar.name, tid)
    spec = specs[key]
    raw = ar.payload(tid)
    p, end = core.base.HEADER_END, len(raw) - core.base.FOOTER_SIZE
    check(raw.startswith(MAGIC + U16.pack(core.VERSION)) and end >= p and raw[end] == 0,
          f'{key}: invalid t133 envelope')
    (count,) = U32.unpack_from(raw, 8)
    check(count == traces[key]['rows_header'], f'{key}: t133 row count changed')
    variants = {sel: core.compile_walk(ops) for sel, ops in core.SELECTORS.get(key, {}).items()}
    walk = core.compile_walk(spec.prog) if spec.kind == 'variable' and not variants else None
    for i in range(count):
        if variants:
            q = variants[raw[p]](raw, p + 1, end)
        elif walk:
            q = walk(raw, p + 1, end)
        else:
            q = p + 1 + spec.rowlen
        check(p + 13 <= q <= end, f'{key}: invalid core record extent')
        ordinal, uid, dbid = core.IDENT(raw, q - 12)
        check(ordinal == i, f'{key}: t133 identity ordinal {ordinal} != {i}')
        yield raw, p, q, ordinal, uid, dbid
        p = q
    check(p == end, f'{key}: t133 footer mismatch')


def core_indexes():
    traces, specs = core.registry(core.load(core.TRACE))
    client = core.base.Archive('client')
    langs = {}
    for raw, p, q, _, uid, dbid in core_rows(client, 8, specs, traces):
        internal_id = U32.unpack_from(raw, q - 16)[0]
        if internal_id != uid or uid != dbid:
            continue  # Legacy aliases outside the selected archive file IDs.
        check(uid not in langs, 'duplicate LANGUAGE identity')
        # Only 22 members' labels are needed; another core row (Guarani) is
        # legacy-encoded. Do not let that unrelated core string affect DAT decoding.
        cursor = Cursor(raw, p + 1)
        try:
            langs[uid] = cursor.string()
        except UnicodeDecodeError:
            langs[uid] = None
    del client
    server = core.base.Archive('server')
    indexes, info = {}, {}
    for tid in sorted(set(CORE_IDS.values()) | {9}):
        info[tid] = dict(path=f'server_db/table_{tid}.dat', entity=specs['server', tid].klass)
        rows = indexes[tid] = {}
        uids = set()
        for raw, p, _, ordinal, uid, dbid in core_rows(server, tid, specs, traces):
            check(dbid not in rows and uid not in uids, f'server/{tid}: duplicate identity')
            uids.add(uid)
            # t57 Cnti (+0xd8) and Cbni (+0xe8): first and third u32 of CLUB_HEAD.
            nations = tuple(U32.unpack_from(raw, p + i)[0] for i in (1, 9)) if tid == 3 else None
            rows[dbid] = (uid, ordinal, p, nations)
        info[tid].update(rows=len(rows), uid_equals_dbid=sum(d == r[0] for d, r in rows.items()))
    identity = lambda rows: {d: (r[0], r[1]) for d, r in rows.items()}
    check(identity(indexes[9]) == identity(indexes[10]), 't9/t10 nation identity mirror differs')
    return langs, indexes, info


def atomic_text(path, text):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(text, encoding='utf-8', newline='\n')
    tmp.replace(path)


def json_text(data):
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def basic_inventory(archive):
    return [{**e, 'language_id': lid, 'table_type': tid,
             'kind': 'person_names' if tid is None else 'entity_table',
             'file_offset': archive.layout['data_base'] + e['offset']}
            for (lid, tid), e in archive.entries.items()]


def enrich(lid, fields, offset, member, archive, tid):
    layout = LAYOUTS[tid]
    primary = fields[0] if layout[0] == 'S' else None
    return dict(language_id=lid, archive=archive, member_path=member, record_offset=offset,
                primary_name=primary, primary_has_han=bool(primary and re.search(r'[\u3400-\u9fff]', primary)),
                slots=[dict(slot=i, type=token, value=(
                    [dict(text=s, field_type=f, form=v) for s, f, v in value]
                    if token == 'V' else value))
                       for i, (token, value) in enumerate(zip(layout, fields, strict=True))])


def scanned_inventory(archives):
    return {ar.label: {**ar.metadata(), 'members': basic_inventory(ar)} for ar in archives}


COUNT_FIELDS = ('records', 'string_entries', 'fixed_string_entries', 'variant_string_entries',
                'variant_records', 'empty_string_slots', 'null_string_slots')


def metrics(members):
    return {**{k: sum(m[k] for m in members) for k in COUNT_FIELDS},
            'members': len(members), 'closed_diff_zero': sum(m['diff'] == 0 for m in members),
            'byte_exact_members': sum(m['byte_exact'] is True for m in members),
            'compressed_member_bytes': sum(m['packed_size'] for m in members),
            'decompressed_member_bytes': sum(m['size'] for m in members)}


def schema_for(archives, inventory):
    langs, indexes, core_info = core_indexes()
    check(archives[0].entries.keys() == archives[1].entries.keys(), 'layer member sets differ')
    lids = sorted({lid for lid, _ in archives[0].entries})
    check(all(langs.get(lid) for lid in lids), 'missing language id in client table_8')
    picks = {tid: set(ids) for tid, ids in SHOWCASE.items()}
    hits = defaultdict(dict)
    witnesses = {}
    archive_results = {}
    for ar in archives:
        members = []
        for e in inventory[ar.label]['members']:
            lid, tid = e['language_id'], e['table_type']
            joined = unmatched = 0
            club_refs = Counter()
            ids = indexes[CORE_IDS[tid]] if tid is not None else None
            interest = picks.get(tid, ()) if lid in FOCUS else ()

            def visit(dbid, offset, fields):
                nonlocal joined, unmatched
                row = ids.get(dbid)
                if row is None:
                    unmatched += 1
                else:
                    joined += 1
                    if tid == 3:
                        nation, based_nation = row[3]
                        val = fields[-1]
                        if val == 0xffff:
                            club_refs['ffff_sentinel'] += 1
                        elif val < len(indexes[10]):
                            club_refs['valid_nation_ordinal'] += 1
                            expected = nation if nation != 0xffffffff else based_nation
                            club_refs['matches_current_cnti_else_cbni'] += val == expected
                        else:
                            club_refs['out_of_range'] += 1
                    if row[0] in interest:
                        hits[tid, row[0]][lid, ar.label] = enrich(
                            lid, fields, offset, e['path'], ar.label, tid)
                key = (lid, tid, dbid)
                if key in WITNESSES and ar is archives[0]:
                    witnesses[f'{lid}/{tid}/{dbid}'] = dict(dbid=dbid, **enrich(
                        lid, fields, offset, e['path'], ar.label, tid))

            try:
                m = decode(ar.payload(e), tid, ar.header, roundtrip=True, visit=visit if ids is not None else None)
            except (ValueError, struct.error, IndexError, zstd.ZstdError) as exc:
                raise ValueError(f"{e['path']}: {exc}") from exc
            if ids is not None:
                check(joined + unmatched == m['records'], 'join accounting mismatch')
            members.append({**e, **m, 'language': langs[lid],
                            'entity': core_info[CORE_IDS[tid]]['entity'] if ids is not None else None,
                            'joined_core_records': joined if ids is not None else None,
                            'unmatched_core_records': unmatched if ids is not None else None,
                            **({'club_nation_comparison': dict(club_refs)} if tid == 3 else {})})
        archive_results[ar.label] = {
            **{k: v for k, v in inventory[ar.label].items() if k != 'members'},
            'totals': metrics(members), 'members': members,
            'by_language': {lid: {'language': langs[lid], **metrics([m for m in members if m['language_id'] == lid])}
                            for lid in lids},
            'by_table': {str(tid) if tid is not None else 'person_names':
                         metrics([m for m in members if m['table_type'] == tid]) for tid in (*LAYOUTS, None)},
        }
    rows = []
    for tid, show in SHOWCASE.items():
        core_tid = CORE_IDS[tid]
        uids = {r[0]: (dbid, r) for dbid, r in indexes[core_tid].items()}
        for uid in show:
            dbid, (_, ordinal, offset, _) = uids[uid]
            localizations = {}
            for lid in FOCUS:
                versions = hits[tid, uid]
                sources = [versions[lid, ar.label] for ar in reversed(archives) if (lid, ar.label) in versions]
                chosen = sources[0] if sources else None  # row-level overlay, no synthetic translation
                localizations[lid] = dict(language=langs[lid], selected=chosen, sources=sources)
            if not all(v['selected'] and v['selected']['primary_name'] for v in localizations.values()):
                continue
            rows.append(dict(entity=core_info[core_tid]['entity'], uid=uid, dbid=dbid,
                             localization_table_type=tid, core_member_path=core_info[core_tid]['path'],
                             core_ordinal=ordinal, core_record_offset=offset, localizations=localizations))
    english_simplified = sum(r['localizations'][1000002]['selected']['primary_has_han'] for r in rows)
    both_han = sum(all(r['localizations'][lid]['selected']['primary_has_han'] for lid in FOCUS[1:]) for r in rows)
    check(both_han >= 25 and {r['localization_table_type'] for r in rows} == set(SHOWCASE),
          'insufficient verified trilingual showcase coverage')
    return dict(task='t143', schema_version=1,
                totals=metrics([m for ar in archive_results.values() for m in ar['members']]),
                archives=archive_results, grammar=grammar(core_info, witnesses), showcase=rows,
                showcase_counts=dict(rows=len(rows), en_and_simplified_has_han=english_simplified,
                                     both_chinese_primary_names_have_han=both_han),
                join=dict(core_reader='scripts/t133_fm24_reader_v2.py', core_tables=core_info,
                          language_labels='client_db/table_8.dat: internal file ID = identity DBID = identity UID',
                          nation_identity_mirror='server/9 and server/10 have identical DBID→(UID, ordinal) maps, 251/251',
                          key='(localization table type, u32 row key) -> (mapped server table, identity DBID) -> identity UID',
                          precedence='Per language and DBID: prefer the entire update row if present, otherwise base. No cross-language fallback.',
                          showcase_language_ids=list(FOCUS)))


def grammar(core_info, witnesses):
    return dict(
        endianness='little', magic_hex=MAGIC.hex(),
        member_header=[dict(offset=0, type='bytes[6]', value_hex=MAGIC.hex()),
                       dict(offset=6, type='u16', base='0x0def', update='0x0df1')],
        entity_table_header=dict(count_offset=8, count_type='u32', record_start=12),
        entity_table_record=dict(key='u32 DBID (strictly increasing within each member)',
                                 table_type='from member filename, not a per-row field',
                                 framing='no record length or per-record selector; table-specific ordered slots',
                                 footer='no footer bytes; exact EOF after declared record count'),
        tokens=dict(S='u32 byte length then strict UTF-8 bytes; 0 empty; 0xffffffff NULL (no bytes)',
                    B='u8; preserve raw per-slot scalar/grammar flag',
                    H='u16; t3 trailing nation-table ordinal or 0xffff sentinel; compare with current t57 Cnti/Cbni in club_nation_comparison',
                    V='u8 count, then count * {S, u16 field_type, u8 form}'),
        tables={tid: dict(entity=core_info[CORE_IDS[tid]]['entity'], core_table=CORE_IDS[tid],
                          layout=layout, slots=[dict(index=i, token=v) for i, v in enumerate(layout)])
                for tid, layout in LAYOUTS.items()},
        person_names=dict(record_start=8, counted=False, record='SSSS + u32 qualifier_id + u16 qualifier + u8 form',
                          slots=['localized name', 'source component A', 'source component B', 'source component C'],
                          footer='u32 zero in place of next nonempty first string length, must be at EOF',
                          key_note='Text-keyed name lexicon; qualifier ID can be 0xffffffff and is not a universal entity UID. Not part of the core entity join.'),
        variant_semantics={
            'field_type': 'Selects a lexical field: t9/type 1 is demonym/adjective; Greek t9 types 24/25 are full/short nation names, t35 types 3/4 select masculine/feminine position term in French.',
            'form': 'Language- and field-dependent inflection index, not a universal gender/plural bitmask. French and Spanish t9/type 1: 1 masc.sg., 2 fem.sg., 3 masc.pl., 4 fem.pl.; Italian same lane: 1 masc.pl., 2 fem.sg., 3 fem.pl. Greek also encodes case.',
            'B': 'For string-associated lanes, noun/article classes; e.g. French t9 has 4 for Algérie (elision), 2 for Bénin (masculine), English t9 uses 0xff. Not all raw scalar codes or all t18/t56 scalar lanes have a proven semantic label.',
            'witnesses': witnesses,
        },
        encoding='UTF-8 strictly decoded and re-encoded for every string including both Chinese scripts; no UTF-16LE branch observed',
        closure='diff = decoded_end - footer_offset (EOF for numeric tables); validate complete terminator for person_names, then compare full reconstructed bytes to the entire decompressed member',
        string_count='Counts every nonempty, non-null physical string field occurrence, including variants and person-name lexicon fields; counts base/update separately, no deduplication.',
    )


def lookup(uid):
    langs, indexes, info = core_indexes()
    matches = []
    for lt, tid in CORE_IDS.items():
        found = next(((d, row) for d, row in indexes[tid].items() if row[0] == uid), None)
        if found is None:
            continue
        dbid, (_, ordinal, offset, _) = found
        matches.append(dict(uid=uid, dbid=dbid, entity=info[tid]['entity'], localization_table_type=lt,
                            core_member_path=info[tid]['path'], core_record_offset=offset,
                            core_ordinal=ordinal, localizations={}))
    if not matches:
        return []
    for source in SOURCES:  # base then update; preserve both, select update if present
        ar = LanguageArchive(source)
        for match in matches:
            tid = match['localization_table_type']
            target = match['dbid']
            for (lid, lt), e in ar.entries.items():
                if lt != tid:
                    continue

                def visit(dbid, offset, fields):
                    if dbid == target:
                        loc = match['localizations'].setdefault(lid, dict(language=langs[lid], sources=[]))
                        item = enrich(lid, fields, offset, e['path'], ar.label, tid)
                        loc['sources'].insert(0, item)
                        loc['selected'] = item

                decode(ar.payload(e), lt, ar.header, visit=visit)
        del ar
    return matches


def cell(text):
    return str(text).replace('|', r'\|').replace('\n', '<br>')


def report(schema):
    base, update = (schema['archives'][s[0]] for s in SOURCES)
    totals = schema['totals']
    lines = ['# t143 — FM24 本地化归档与实体名称', '',
             '| 归档 | 字节精确闭合 | 记录 | 非空字符串 | person_names 记录 / 字符串 |',
             '|---|---:|---:|---:|---:|']
    for name, ar in schema['archives'].items():
        t, pn = ar['totals'], ar['by_table']['person_names']
        lines.append(f"| `{name}.dat` | {t['byte_exact_members']}/{t['members']} | {t['records']:,} | "
                     f"{t['string_entries']:,} | {pn['records']:,} / {pn['string_entries']:,} |")
    lines += ['', f"合计 **{totals['string_entries']:,}** 个非空字符串；计入实体固定槽、变体字符串和 `person_names` 的非空字段。"
              '同文、同记录在不同槽或归档中分别计数；空字符串和 NULL 另计。', '',
              '## 语言分布', '',
              '每个 ID 在每个归档中均有 15 张实体表和 1 个 `person_names` 成员。语言名从 t133 `client/8` 的内部 ID 与 UID/DBID 三重相等取得。', '',
              '| ID | `client/8` 原名 | 2400 记录 | 2400 字符串 | 2430 记录 | 2430 字符串 |',
              '|---:|---|---:|---:|---:|---:|']
    for lid, b in base['by_language'].items():
        u = update['by_language'][lid]
        lines.append(f"| {lid} | {b['language']} | {b['records']:,} | {b['string_entries']:,} | "
                     f"{u['records']:,} | {u['string_entries']:,} |")
    lines += ['', '## 字节文法', '',
              '- 每个归档是 8B `tad.` 外壳 + FMF；目录路径、Zstd frame 偏移、压缩/解压字节数见 JSON。单帧恰好消耗目录给出的整个成员区间。',
              '- 每个解压成员头：`03 01 74 61 64 2e` + LE `u16` 版本（2400=`0x0def`，更新=`0x0df1`）。',
              '- 数字表：`+8 u32 n`，`+12` 开始 `n` 行，每行 `u32 DBID` 后接下表槽位，无独立记录长度、UID、表号或文件尾。表号来自文件名。',
              '- `S` = `u32` 字节长度 + 严格 UTF-8；`0` 是空串，`0xffffffff` 是 NULL。简繁中文也是 UTF-8；无 UTF-16LE 分支。',
              '- `B` = `u8` 原始标量，字符串旁通常是语法分类；`H` = `u16`；`V` = `u8` 数量 + 对应数量的 `S, u16 field_type, u8 form`。`form` 依语言与字段而定，不是全局位掩码。',
              '- 法语 t9/type 1 `algérien / algérienne / algériens / algériennes` 对应 `1/2/3/4`（阳单、阴单、阳复、阴复）；意大利语该槽顺序不同。希腊语另有格变；法语 t35 的 `field_type 3/4` 分别选择阳性/阴性位置术语。',
              '- `person_names`：从 `+8` 开始，无行数；每行是 `S S S S + u32 qualifier_id + u16 qualifier + u8 form`。下一条首串长度为零即读到 4B 终止符，之后必须是 EOF；不是数字表的 UID 索引。',
              '- 验证不靠扫描名称锚点：逐成员按槽位解析，正文游标与 EOF/终止符边界之差 `diff=0`，并用已解析值重编码整个成员进行逐字节比较。未证实的标量语义保留原值。', '',
              '| 本地化表 | t133 实体 | 键之后的槽位 |', '|---:|---|---|']
    for tid, g in schema['grammar']['tables'].items():
        lines.append(f"| {tid} | {g['entity']} | `{g['layout']}` |")
    lines += ['', '## 英文／简体／繁体 UID 联接', '',
              '行键按实体表匹配 t133 的 DBID，再读该行实际 UID。国家名本地化表 **9 → server/10**；'
              '独立复核 server/9（国家队容器）与 server/10 的 251 个 `(DBID, UID, ordinal)` 全等。'
              '球场与俱乐部等不同表可以共享 UID；`--lookup` 分表列出。', '',
              '| 实体 | t133 表 | 2400 命中 / 记录 | 2430 命中 / 记录 |', '|---|---:|---:|---:|']
    for tid in SHOWCASE:
        counts = []
        for ar in (base, update):
            members = [m for m in ar['members'] if m['table_type'] == tid]
            counts.append(f"{sum(m['joined_core_records'] for m in members):,} / {sum(m['records'] for m in members):,}")
        g = schema['grammar']['tables'][tid]
        lines.append(f"| {g['entity']} | {g['core_table']} | {' | '.join(counts)} |")
    for name, ar in schema['archives'].items():
        club = [m for m in ar['members'] if m['table_type'] == 3]
        counts = Counter()
        for m in club:
            counts.update(m['club_nation_comparison'])
        n, d = (counts[k] for k in ('matches_current_cnti_else_cbni', 'valid_nation_ordinal'))
        lines.append(f"\n`t3` 行末 `H`：`{name}` 非空有效国家序号中 {n:,}/{d:,} 与当前 t133 `CLUB_HEAD` 的 "
                     f"t57 `Cnti`（缺失时 `Cbni`）一致；另有 {counts['ffff_sentinel']:,} 个 `0xffff`。")
    c = schema['showcase_counts']
    lines += ['', f"以下 **{c['rows']}** 行均命中英文、简中和繁中语言成员；其中 **{c['both_chinese_primary_names_have_han']}** 行的简繁名称均含汉字。"
              '繁中成员对不少国外实体保存英文原文，本表如实列出。每种语言独立以整行 update 覆盖 base；† 表示来自更新层。'
              '表中保留原始名称、简写和大小写；每行的 core 和语言层字节偏移可在 JSON 复查。', '',
              '| 实体 | UID | English | 简体中文 | 繁體中文 |', '|---|---:|---|---|---|']
    for row in schema['showcase']:
        names = []
        for lid in FOCUS:
            selected = row['localizations'][lid]['selected']
            names.append(cell(selected['primary_name']) + ('†' if selected['archive'] == SOURCES[1][0] else ''))
        lines.append(f"| {row['entity']} | {row['uid']} | {' | '.join(names)} |")
    lines += ['', '## 复算', '',
              '```powershell', 'py -V:3.12 -B scripts/t143_lang_db.py',
              'py -V:3.12 -B scripts/t143_lang_db.py --selftest',
              'py -V:3.12 -B scripts/t143_lang_db.py --lookup 676', '```', '',
              '输入 `.dat` 只读，解压和重编码均只在内存进行；`--lookup` 和 `--selftest` 不写输出。']
    return '\n'.join(lines) + '\n'


def controls():
    header = MAGIC + U16.pack(0x0df1)
    good = header + U32.pack(1) + bytes.fromhex('4d000000 03000000 e4b8ad ff 01 00000000 1900 03')
    result = decode(good, 2, header, roundtrip=True)
    check(result['records'] == result['empty_string_slots'] == result['string_entries'] == 1,
          'synthetic UTF-8 and variant count test failed')
    p = header + bytes.fromhex('01000000 41 00000000 ffffffff 00000000 ffffffff ffff 00 00000000')
    check(decode(p, None, header, roundtrip=True)['null_string_slots'] == 1, 'synthetic person_names NULL test failed')
    for payload, tid in ((good[:-1], 2), (good + ZERO, 2), (p[:-1], None), (p + ZERO, None),
                         (good.replace(b'\xe4\xb8\xad', b'\xff\xb8\xad'), 2)):
        try:
            decode(payload, tid, header, roundtrip=True)
        except (ValueError, struct.error, IndexError):
            continue
        raise ValueError('invalid synthetic input was accepted')


def headline(schema):
    return ', '.join(f"{label} {ar['totals']['byte_exact_members']}/{ar['member_count']} diff=0"
                     for label, ar in schema['archives'].items()) + (
        f"; {schema['totals']['string_entries']:,} localized strings; {len(schema['showcase'])} showcase joins "
        f"({schema['showcase_counts']['both_chinese_primary_names_have_han']} with Han text in both Chinese names)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument('--selftest', action='store_true', help='recompute all rows and compare persisted artifacts')
    modes.add_argument('--lookup', metavar='UID', type=lambda s: int(s, 16) if s.lower().startswith('0x') else int(s))
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if args.lookup is not None:
        if not 0 <= args.lookup <= 0xffffffff:
            ap.error('UID must fit in u32')
        print(json_text(lookup(args.lookup)), end='')
        return
    controls()
    archives = [LanguageArchive(source) for source in SOURCES]
    inventory = scanned_inventory(archives)
    staged = OUT / 'inventory_stage.json'
    if not args.selftest:
        OUT.mkdir(parents=True, exist_ok=True)
        stage_text = json_text(inventory)
        if not staged.exists() or staged.read_text(encoding='utf-8') != stage_text:
            atomic_text(staged, stage_text)
        inventory = json.loads(staged.read_text(encoding='utf-8'))
        print('FMF inventory saved: 352 + 352 members', flush=True)
    schema = schema_for(archives, inventory)
    schema_path, report_path = OUT / 'lang_db_schema.json', OUT / 'REPORT.md'
    if args.selftest:
        check(schema_path.read_text(encoding='utf-8') == json_text(schema), 'persisted JSON differs from recomputation')
        check(report_path.read_text(encoding='utf-8') == report(schema), 'persisted REPORT.md differs from recomputation')
        print('--selftest PASS: ' + headline(schema))
    else:
        atomic_text(schema_path, json_text(schema))
        atomic_text(report_path, report(schema))
        staged.unlink()
        print(headline(schema))
        print('Deliverables: scripts/t143_lang_db.py; scratch/t143/out/{lang_db_schema.json,REPORT.md}')


if __name__ == '__main__':
    main()
