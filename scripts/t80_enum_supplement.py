"""t80: enum supplement dictionary + read-only rescan of the t61 / t75 enum debt.

Builds three machine-readable artefacts under ``scratch/t80/out/``:

* ``enum_supplement.json`` - every enum that the snapshotted legacy evidence
  carries (``enums.json`` / ``enum_extras.json`` / ``EXE_ENUMS.md``), with the
  manifest SHA-256 of its source, its declared file, numeric domain, value
  names, and the *field-code bindings* that the frozen master join dropped.
* ``rescan_t61.json`` - the 67 ``no_enum_source`` held occurrences of
  ``scratch/t61/out/enum_inventory.json`` re-decided against that dictionary.
* ``rescan_t75.json`` - the 13 unfrozen 4CC getter keys of
  ``scratch/t75/out/xref_reverse.json`` re-decided against the same dictionary.

Read-only: the frozen ``master.json`` is opened, hashed and never written. No
``.dat`` payload is touched, so ``FM24_DB_DIR`` is not required.

Evidence levels follow AGENTS.md: the dictionary itself is L2/L3 static
provenance (manifest SHA + declaring file + builder VA where the legacy record
carries one); an upgraded *field* keeps its own pre-existing static chain and
only gains a scoped enum domain, which is reported as a candidate, never as a
done deal.

Exit codes: 0 success, 1 check failed, 2 usage or fatal error.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t80/out'
SCHEMA = 'evidence/fm24/reports/editor_schema/'
MANIFEST = 'evidence/MANIFEST.json'
MASTER = SCHEMA + 'master.json'
FROZEN_MASTER_SHA = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
T61_INVENTORY = 'scratch/t61/out/enum_inventory.json'
T75_XREF = 'scratch/t75/out/xref_reverse.json'
BASELINE = 'reports/club_nation_subtable_schema.json'

# file -> (role, expected presence in evidence/MANIFEST.json)
SOURCES = {
    'enums.json': ('scoped enum dictionary extracted from comp editor format XML',
                   'values[].enum / enum_id / name + record file'),
    'enum_extras.json': ('15 editor.exe recovered enums (missing from format XML)',
                         'same shape as enums.json plus provenance'),
    'EXE_ENUMS.md': ('reverse-engineering narrative for the 15 extras',
                     'section 0 overview table + 3.2 job-table value list'),
    'enum_crrp_static.json': ('crrp builder 0x141cf5f10 static reconstruction',
                              'value ranges + evidence_level + residual_risk'),
    'enum_crrp_unicorn.json': ('crrp unicorn snippet (0x141cf6055..)',
                               'instruction bytes + snippet sha'),
    'database_ui.json': ('database ui field references', 'db_field / insert_fields'),
    'rule_groups.json': ('rule group field declarations', 'field + enum_ref'),
    'entities.json': ('database entity field declarations', 'field + enum_ref'),
}

ENTITY_FILES = ('nation.xml', 'club.xml', 'comp.xml')


class Check(Exception):
    pass


def need(ok, detail):
    if not ok:
        raise Check(detail)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def read_bytes(rel):
    return (ROOT / rel).read_bytes()


def load_json(rel):
    return json.loads(read_bytes(rel))


def basename(value):
    return os.path.basename(str(value or '').replace('\\', '/'))


def to_int(token):
    if isinstance(token, bool) or token is None:
        return None
    try:
        return int(str(token).strip())
    except (TypeError, ValueError):
        return None


def normalize_values(record):
    """Return (values, domain, kind) with int coercion kept explicit."""
    values, numeric = [], True
    for item in record.get('values') or []:
        raw = item.get('enum')
        num = to_int(raw)
        if num is None:
            numeric = False
        entry = {'value': num if num is not None else raw,
                 'raw': raw,
                 'enum_id': item.get('enum_id'),
                 'name': item.get('name')}
        for extra in ('label', 'range', 'source'):
            if extra in item:
                entry[extra] = item[extra]
        values.append(entry)
    domain = sorted({v['value'] for v in values}) if numeric else []
    return values, (domain if numeric else None), ('numeric' if numeric else 'token')


# --- CONT ---
class Sources:
    """Manifest-pinned read-only view of the snapshotted legacy evidence."""

    def __init__(self):
        self.manifest = load_json(MANIFEST)
        self.files = {x['path']: x for x in self.manifest['files']}
        self.pinned = {}
        for name in SOURCES:
            rel = SCHEMA + name
            need(rel in self.files, f'{name} not registered in MANIFEST')
            self.pinned[name] = self.files[rel]
        self.raw = {}
        for name, entry in self.pinned.items():
            b = read_bytes(SCHEMA + name)
            need(sha256_bytes(b) == entry['sha256'], f'{name} MANIFEST SHA mismatch')
            self.raw[name] = b
        need(self.files[MASTER]['sha256'] == FROZEN_MASTER_SHA, 'frozen master SHA')
        need(sha256_bytes(read_bytes(MASTER)) == FROZEN_MASTER_SHA, 'master on disk')

    def sha(self, name):
        return self.pinned[name]['sha256']

    def json(self, name):
        return json.loads(self.raw[name])

    def text(self, name):
        return self.raw[name].decode('utf-8')

    def pointer(self, name):
        return {'path': SCHEMA + name, 'manifest_sha256': self.sha(name),
                'bytes': self.pinned[name]['bytes']}


def parse_exe_enums_md(text):
    """Extract the machine-readable parts of EXE_ENUMS.md (L3 narrative)."""
    overview, references, section = {}, {}, None
    for line in text.splitlines():
        stripped = line.strip()
        heading = re.match(r'^(#{2,4})\s*(\d+(?:\.\d+)*)', stripped)
        if heading:
            section = heading.group(2)
            continue
        if not stripped.startswith('|'):
            continue
        cells = [c.strip() for c in stripped.strip('|').split('|')]
        if len(cells) < 4 or set(cells[0]) <= set('-: '):
            continue
        head = cells[0].strip('`')
        if not re.match(r'^[A-Za-z0-9+]{2,6}$', head):
            continue
        if section == '0' and len(cells) == 5:
            count = re.match(r'^(\d+)', cells[3])
            overview[head] = {
                'semantics': cells[1],
                'value_source': cells[2],
                'declared_count': int(count.group(1)) if count else None,
                'names': cells[4],
            }
        elif section == '2' and len(cells) == 4 and '.xml' in cells[1]:
            file_token, _, line_no = cells[1].partition(':')
            field_token = re.match(r'^([A-Za-z0-9_+]+)', cells[2].strip('`'))
            references[head] = {'file': basename(file_token), 'xml_line': line_no or None,
                                'field': field_token.group(1) if field_token else cells[2],
                                'field_verbatim': cells[2], 'meaning': cells[3]}
    job_numbers = []
    fence = re.search(r'```[a-z]*\r?\n([\d,\s]+?)```', text, re.S)
    if fence:
        job_numbers = [int(x) for x in re.findall(r'\d+', fence.group(1))]
    return {'overview': overview, 'references': references,
            'job_table_numbers': job_numbers,
            'sha256_of_markdown': sha256_bytes(text.encode('utf-8'))}


def iter_fields(node, path, out):
    for field in node or []:
        out.append((path, field))
        iter_fields(field.get('list_item_fields'), path + '/' + str(field.get('field')), out)


def declared_entities(master):
    """code -> [(file, record id)] straight out of the frozen entity join."""
    index = {}
    for file_name, records in master['entities'].items():
        for record in records:
            flat = []
            iter_fields(record.get('fields'), str(record.get('id')), flat)
            for path, field in flat:
                code = field.get('field')
                if not code:
                    continue
                index.setdefault(code, []).append({
                    'file': file_name, 'record': record.get('id'), 'path': path,
                    'name': field.get('name'), 'type': field.get('type'),
                    'enum_ref': field.get('enum_ref'),
                })
    return index


def declared_rules(rule_groups):
    index = {}
    def walk(node, file_name):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'enum_ref' and isinstance(value, str):
                    code = node.get('field')
                    if code:
                        index.setdefault(code, []).append(
                            {'file': file_name, 'record': node.get('id'), 'field': code,
                             'name': node.get('name'), 'type': node.get('type'),
                             'enum_ref': value})
                else:
                    walk(value, file_name)
        elif isinstance(node, list):
            for value in node:
                walk(value, file_name)
    for file_name, payload in rule_groups.items():
        walk(payload, file_name)
    return index


def collect_refs(master):
    """Every enum_ref the frozen schema actually declares, with its sites."""
    refs = {}
    for code, sites in declared_entities(master).items():
        for site in sites:
            if site['enum_ref']:
                refs.setdefault(site['enum_ref'], []).append(
                    {'code': code, 'file': site['file'], 'record': site['record'],
                     'binding': 'explicit_enum_ref', 'declared_in': 'entities.json'})
    return refs


def enum_record(name, source_name, record, src, origin):
    values, domain, kind = normalize_values(record)
    ids = sorted({x['enum_id'] for x in values if to_int(x['enum_id']) is not None}) if values else []
    id_domain = sorted(int(x['enum_id']) for x in values if to_int(x['enum_id']) is not None)
    named = sum(1 for x in values if (x.get('name') or '').strip())
    return {
        'enum': name,
        'scope': origin,
        'declared_file': record.get('file'),
        'declared_file_basename': basename(record.get('file')),
        'kind': kind,
        'value_count': len(values),
        'named_value_count': named,
        'unnamed_values': [x['value'] for x in values if not (x.get('name') or '').strip()],
        'domain': domain,
        'enum_id_domain': id_domain,
        'enum_id_tokens': ids if kind == 'token' else [],
        'values': values,
        'source': dict(src.pointer(source_name), legend=SOURCES[source_name][0],
                       payload_shape=SOURCES[source_name][1]),
        'provenance': record.get('provenance'),
    }


def build_dictionary(src):
    """Merge the dictionaries without ever overriding the frozen master."""
    master = load_json(MASTER)
    frozen = master['enums']
    enums_json = src.json('enums.json')
    extras = src.json('enum_extras.json')
    md = parse_exe_enums_md(src.text('EXE_ENUMS.md'))
    crrp = src.json('enum_crrp_static.json')
    crrp_uni = src.json('enum_crrp_unicorn.json')
    entities = declared_entities(master)
    rules = declared_rules(src.json('rule_groups.json'))
    refs = collect_refs(master)

    entries, conflicts, unchanged = {}, [], []
    for origin, payload, source_name in (
        ('format_xml', enums_json, 'enums.json'),
        ('editor_exe_recovered', extras, 'enum_extras.json'),
    ):
        for name in sorted(payload):
            record = payload[name]
            entry = enum_record(name, source_name, record, src, origin)
            in_master = name in frozen
            entry['in_frozen_master'] = in_master
            if in_master:
                same = canon(record.get('values')) == canon(frozen[name].get('values'))
                entry['identical_to_master_values'] = same
                entry['master_declared_file'] = frozen[name].get('file')
                if not same:
                    conflicts.append({
                        'enum': name, 'against': 'master.json',
                        'master_file': frozen[name].get('file'),
                        'candidate_file': record.get('file'),
                        'master_value_count': len(frozen[name].get('values') or []),
                        'candidate_value_count': len(record.get('values') or []),
                        'decision': 'not_adjudicated',
                        'note': 'master wins; candidate kept verbatim in conflicts',
                        'master_values': frozen[name].get('values'),
                        'candidate_values': record.get('values'),
                    })
                unchanged.append({'enum': name, 'source': source_name,
                                  'identical_to_master': same})
            else:
                entry['identical_to_master_values'] = None
            entries[name] = entry

    # Which field codes could this enum be bound to? master kept the field but
    # dropped the reference; entities.json / enums.json still name the file.
    master_codes = master.get('field_codes') or {}
    for name, entry in entries.items():
        bindings = []
        for code, sites in sorted(entities.items()):
            hit = [s for s in sites
                   if s['enum_ref'] == name
                   or (s['file'] and entry['declared_file_basename']
                       and basename(s['file']) == entry['declared_file_basename'])]
            explicit = [s for s in hit if s['enum_ref'] == name]
            if not hit:
                continue
            bindings.append({
                'code': code,
                'frozen': code in master_codes,
                'frozen_type': (master_codes.get(code) or {}).get('type'),
                'binding': 'explicit_enum_ref' if explicit else 'same_declaring_file_only',
                'sites': [{'file': s['file'], 'record': s['record'], 'path': s['path']}
                          for s in hit][:8],
            })
        for code, sites in sorted(rules.items()):
            explicit = [s for s in sites if s['enum_ref'] == name]
            if not explicit:
                continue
            bindings.append({'code': code, 'frozen': code in master_codes,
                             'frozen_type': (master_codes.get(code) or {}).get('type'),
                             'binding': 'explicit_enum_ref_rule_group',
                             'sites': [{'file': s['file'], 'record': s['record'],
                                        'path': s['field']} for s in explicit][:8]})
        entry['candidate_bindings'] = bindings
        entry['bound_to_frozen_field'] = any(b['binding'] != 'same_declaring_file_only'
                                             and b['frozen'] for b in bindings)
        # how many frozen fields claim this enum by ref
        entry['frozen_ref_sites'] = len(refs.get(name, []))
    delta = sorted(set(entries) - set(frozen))
    master_only = sorted(set(frozen) - set(entries))
    return dict(master=master, md=md, crrp=crrp, crrp_unicorn=crrp_uni,
                entries=entries, conflicts=conflicts, unchanged=unchanged,
                delta_missing_from_master=delta, master_only=master_only,
                entities=entities, rules=rules, refs=refs)


def wire_domain(entry):
    """Integers the wire can carry: numeric enums use values, token enums use enum_id."""
    if entry['kind'] == 'token':
        return set(entry['enum_id_domain'])
    return set(entry['domain'] or [])


def names_present(entry):
    return entry['named_value_count'] > 0 and entry['named_value_count'] == entry['value_count']


def histogram(occurrence):
    hist, sides = {}, {}
    for side in ('client', 'server'):
        per = {}
        for art in (occurrence.get('archives') or {}).get(side) or []:
            if art.get('status') != 'scanned':
                continue
            for key, count in (art.get('histogram') or {}).items():
                per[int(key)] = per.get(int(key), 0) + count
        if per:
            sides[side] = per
            for key, count in per.items():
                hist[key] = hist.get(key, 0) + count
    return hist, sides


def bind_code(code, declaring_files, entities, rules, entries, master_codes):
    """Rank every dictionary enum that could be bound to this field code."""
    out = []
    for name, entry in entries.items():
        if name.lower() != code.lower():
            continue
        explicit = [s for s in entities.get(code, []) if s['enum_ref'] == name]
        explicit += [s for s in rules.get(code, []) if s['enum_ref'] == name]
        same_file = bool(entry['declared_file_basename']
                         and entry['declared_file_basename'] in declaring_files)
        if explicit:
            strength, why = 3, 'explicit_enum_ref'
        elif same_file and name == code:
            strength, why = 2, 'code_name_and_declaring_file'
        elif name == code:
            strength, why = 1, 'code_name_only'
        elif same_file:
            strength, why = 1, 'declaring_file_only'
        else:
            strength, why = 0, 'no_binding'
        out.append({'enum': name, 'strength': strength, 'binding': why,
                    'explicit_sites': [{'file': s['file'], 'record': s['record']}
                                       for s in explicit][:6],
                    'frozen_field': master_codes.get(code)})
    out.sort(key=lambda x: (-x['strength'], x['enum']))
    return out


def rescan_t61(dict_result, master_codes):
    inventory = load_json(T61_INVENTORY)
    occurrences = [o for o in inventory['occurrences'] if o['decision'] == 'no_enum_source']
    need(len(occurrences) == 67, 't61 no_enum_source count')
    entries, entities, rules = (dict_result['entries'], dict_result['entities'],
                                dict_result['rules'])
    master_enums = dict_result['master']['enums']
    upgraded, held, flags = [], [], []
    for occ in occurrences:
        code = occ['code']
        declaring = {basename(s['file']) for s in entities.get(code, [])}
        hist, sides = histogram(occ)
        frozen_ref = occ.get('enum_ref')
        rec = {
            'entity': occ['entity'], 'layer': occ['layer'], 'code': code,
            'xml_path': occ['xml_path'], 'prior_grade': occ['grade'],
            'prior_decision': occ['decision'],
            'schema_type': (occ.get('schema') or {}).get('type'),
            'declaring_files': sorted(declaring),
            'frozen_enum_ref': frozen_ref,
            'wire_histogram': {str(k): v for k, v in sorted(hist.items())},
            'wire_sides': sorted(sides),
            'existing_l3_chain': bool(occ.get('existing_l3_chain')),
            'slot': occ.get('slot'),
            'prior_first_counterexample': occ.get('prior_first_counterexample'),
        }
        if frozen_ref:
            rec['outcome'] = 'still_held'
            rec['reason'] = 'frozen enum_ref already present; t61 domain conflict stands'
            held.append(rec)
            continue
        candidates = bind_code(code, declaring, entities, rules, entries, master_codes)
        usable = []
        for cand in candidates:
            entry = entries[cand['enum']]
            domain = wire_domain(entry)
            missing = sorted(set(hist) - domain)
            usable.append(dict(cand, value_count=entry['value_count'],
                               named_value_count=entry['named_value_count'],
                               all_values_named=names_present(entry),
                               domain=sorted(domain)[:64],
                               domain_size=len(domain),
                               wire_minus_domain=missing,
                               domain_covered=not missing,
                               declared_file=entry['declared_file']))
        rec['candidates'] = usable
        # Domain self-consistency needs both: a real binding and a covered wire.
        ok = [c for c in usable if c['domain_covered'] and c['strength'] >= 2]
        ambiguous = [c for c in usable if c['domain_covered'] and c['strength'] >= 2]
        if ok:
            best = ok[0]
            entry = entries[best['enum']]
            rec['outcome'] = 'candidate_L3'
            rec['reason'] = ('enum_ref now scoped by the supplement dictionary; '
                             'static slot unchanged')
            rec['candidate_grade'] = 'L3'
            rec['chosen_enum'] = best['enum']
            rec['binding'] = best['binding']
            rec['ambiguous_with'] = [c['enum'] for c in ambiguous[1:]]
            rec['evidence'] = {
                'dictionary': entry['source'],
                'scope': entry['scope'],
                'declared_file': entry['declared_file'],
                'value_count': entry['value_count'],
                'named_value_count': entry['named_value_count'],
                'wire_values': sorted(hist),
                'domain': sorted(wire_domain(entry)),
                'grade_note': 'L2/L3 static dictionary + full-archive domain cover; '
                              'no new disassembly, no L4',
            }
            upgraded.append(rec)
        else:
            covered_but_weak = [c['enum'] for c in usable if c['domain_covered']]
            if covered_but_weak:
                rec['outcome'] = 'held_binding_insufficient'
                rec['reason'] = ('domain covers the wire but the dictionary carries no '
                                 'scoped reference for this code')
                rec['domain_cover_without_binding'] = covered_but_weak
            elif usable:
                rec['outcome'] = 'held_domain_conflict'
                rec['reason'] = 'dictionary entry exists but the wire exceeds its domain'
            else:
                rec['outcome'] = 'held_not_in_dictionary'
                rec['reason'] = 'dictionary contains no entry for this code'
            held.append(rec)
        if usable and hist and not names_present(entries[usable[0]['enum']]):
            flags.append({'code': code, 'issue': 'dictionary values carry empty names',
                          'enum': usable[0]['enum']})
    counts = {}
    for rec in upgraded + held:
        counts[rec['outcome']] = counts.get(rec['outcome'], 0) + 1
    return {
        'task': 't80/rescan_t61',
        'input': {'path': T61_INVENTORY,
                  'sha256': sha256_bytes(read_bytes(T61_INVENTORY)),
                  'occurrences': len(occurrences),
                  'prior_decision': 'no_enum_source'},
        'dictionary': {'path': SCHEMA + 'enum_supplement.json (built by this run)'},
        'counts': dict(sorted(counts.items())),
        'upgraded': upgraded,
        'held': held,
        'flags': flags,
        'L4': 0,
    }


def rescan_t75(dict_result, master_codes):
    xref = load_json(T75_XREF)
    entries, entities, rules = (dict_result['entries'], dict_result['entities'],
                                dict_result['rules'])
    master_enums = dict_result['master']['enums']
    frozen_domains = {}
    for name, record in master_enums.items():
        values, domain, kind = normalize_values(record)
        frozen_domains[name] = (kind, set(domain or []) | {
            int(x['enum_id']) for x in values if to_int(x['enum_id']) is not None})

    # Collect the unfrozen getter keys, keeping every slot they were seen on.
    unfrozen = {}
    for slot in xref['slots']:
        for key in slot.get('codes') or []:
            if key.get('master_locations'):
                continue
            rec = unfrozen.setdefault(key['code'], {'code': key['code'], 'slots': []})
            rec['slots'].append({
                'table': slot['table'], 'slot': slot['slot'],
                'nominal_width': slot.get('nominal_width'),
                'reader_site': slot.get('reader_site'),
                'blocker_verbatim': slot.get('blocker'),
                'prior_ids': slot.get('prior_ids'),
                'gate': next((g['gate'] for x in slot.get('displacement_xrefs_untyped') or []
                              for g in x.get('keyed_prefix') or []
                              if g.get('code') == key['code']), None),
                'wire': (slot.get('archives') or {}).get('server') or {},
            })
    decisions = []
    for code in sorted(unfrozen):
        rec = unfrozen[code]
        per_slot = []
        for slot in rec['slots']:
            wire = slot['wire']
            hist = {int(k): v for k, v in ((wire.get('t72') or {}).get('value_histogram') or {}).items()}
            covered, best = [], None
            for name, (kind, domain) in frozen_domains.items():
                if hist and set(hist) <= domain:
                    covered.append(name)
            cands = bind_code(code, {f for s in entities.get(code, [])
                                     for f in [basename(s['file'])]},
                              entities, rules, entries, master_codes)
            # an unfrozen key cannot have an explicit ref; keep same-file/name hits
            for cand in cands:
                entry = entries[cand['enum']]
                dom = wire_domain(entry)
                cand['domain_size'] = len(dom)
                cand['wire_minus_domain'] = sorted(set(hist) - dom)
                cand['domain_covered'] = bool(hist) and not cand['wire_minus_domain']
                cand['declared_file'] = entry['declared_file']
                cand['all_values_named'] = names_present(entry)
            cands = [c for c in cands if c['domain_covered']]
            cands.sort(key=lambda c: (not c['all_values_named'], c['domain_size'], c['enum']))
            if cands:
                best = cands[0]
            per_slot.append({
                'table': slot['table'], 'slot': slot['slot'],
                'nominal_width': slot['nominal_width'],
                'reader_site': slot['reader_site'],
                'blocker_verbatim': slot['blocker_verbatim'],
                'prior_ids': slot['prior_ids'],
                'gate': slot['gate'],
                'wire_histogram': {str(k): v for k, v in sorted(hist.items())},
                'wire_distinct': len(hist),
                'frozen_domains_covering_wire': covered[:12],
                'supplement_candidates': cands[:6],
                'chosen': best,
            })
        verdicts = [s['chosen'] for s in per_slot]
        entry = {'code': code, 'slot_count': len(per_slot), 'slots': per_slot}
        if all(verdicts):
            names = {v['enum'] for v in verdicts}
            entry['outcome'] = 'candidate_single_enum' if len(names) == 1 else 'candidate_multi_enum'
            entry['verdict'] = ('4CC has no frozen field_code, but the supplement '
                                'dictionary scopes it to the wire domain')
            entry['candidate_grade'] = 'L3-candidate'
        elif any(verdicts):
            entry['outcome'] = 'partial'
            entry['verdict'] = 'some slots covered, others still have no scoped domain'
        else:
            entry['outcome'] = 'still_held'
            entry['verdict'] = 'no supplement entry covers the wire; blocker verbatim kept'
        entry['blocker_verbatim'] = [s['blocker_verbatim'] for s in per_slot]
        decisions.append(entry)
    counts = {}
    for d in decisions:
        counts[d['outcome']] = counts.get(d['outcome'], 0) + 1
    return {
        'task': 't80/rescan_t75',
        'input': {'path': T75_XREF, 'sha256': sha256_bytes(read_bytes(T75_XREF)),
                  'slots': len(xref['slots'])},
        'counts': dict(sorted(counts.items())),
        'named_in_prompt': ['Ccre', 'cosr', 'Npop', 'Ncpi', 'CICF'],
        'unfrozen_key_count': len(decisions),
        'decisions': decisions,
        'L4': 0,
    }


def crosscheck_t73(dict_result):
    """Re-decide the enum-shaped unmapped slots of t73 / t76c against the dictionary."""
    entries = dict_result['entries']
    master_enums = dict_result['master']['enums']
    files = sorted((ROOT / 'scratch/t73/out').glob('slots_*.json'))
    files += sorted((ROOT / 'scratch/t76c/out').glob('slots_*.json'))
    need(files, 'no t73/t76c slot files found')
    rows, dbvw = [], None
    for path in files:
        doc = json.loads(path.read_bytes())
        rel = path.relative_to(ROOT).as_posix()
        for slot in doc.get('slots') or []:
            evidence = slot.get('evidence') or []
            enumish = bool(evidence) or 'enum' in str(slot.get('why') or '').lower()
            if not enumish:
                continue
            code = slot.get('field')
            enum = master_enums.get(code)
            entry = entries.get(code)
            row = {'file': rel, 'table': doc.get('table'), 'archive': doc.get('archive'),
                   'field': code, 'grade': slot.get('grade'), 'why_verbatim': slot.get('why'),
                   'offset': slot.get('offset'), 'width': slot.get('width'),
                   'byte_columns': [{'offset': e.get('offset'), 'values': e.get('values'),
                                     'subset_of_enum': e.get('subset_of_enum')}
                                    for e in evidence],
                   'frozen_enum_present': bool(enum),
                   'frozen_value_count': len((enum or {}).get('values') or []),
                   'frozen_named_values': sum(1 for x in (enum or {}).get('values') or []
                                              if (x.get('name') or '').strip()),
                   'supplement_present': bool(entry)}
            if enum:
                _, domain, kind = normalize_values(enum)
                row['frozen_domain'] = sorted(domain or [])
                row['frozen_kind'] = kind
                row['frozen_names'] = [x.get('name') for x in enum.get('values') or []]
            if entry:
                row['supplement_domain'] = sorted(wire_domain(entry))
                row['supplement_names'] = [v.get('name') for v in entry['values']]
            if code == 'DBvw':
                dbvw = row
            rows.append(row)
    names_recovered = bool(dbvw and any((n or '').strip() for n in
                                        (dbvw.get('supplement_names') or [])))
    return {
        'task': 't80/crosscheck_t73',
        'inputs': sorted({r['file'] for r in rows}),
        'slots': rows,
        'dbvw_section': {
            'slot': dbvw,
            'master_defect': ('master.json DBvw carries 4 values (0..3) with empty names, so '
                              'domain-subset matching cannot decide a column'),
            'supplement_recovers_names': names_recovered,
            'conclusion': ('unchanged: the snapshotted dictionaries carry the same empty '
                           'names for DBvw; the defect is upstream of t80')
            if not names_recovered else 'names recovered from the supplement',
        },
        'L4': 0,
    }


def supplement_document(src, dict_result):
    master = dict_result['master']
    entries = dict_result['entries']
    frozen = master['enums']
    md = dict_result['md']
    crrp = dict_result['crrp']
    crrp_unicorn = dict_result['crrp_unicorn']
    named = {k: v for k, v in entries.items() if names_present(v)}
    unnamed = {k: v for k, v in entries.items() if not names_present(v)}
    bindings = {k: v for k, v in entries.items() if v['candidate_bindings']}
    return {
        'task': 't80/enum_supplement',
        'role': ('supplement dictionary layered on top of the frozen master.json; '
                 'read-only, master is never rewritten'),
        'frozen_master': {'path': MASTER, 'sha256': FROZEN_MASTER_SHA,
                          'enums': len(frozen),
                          'manifest_pointer': SCHEMA + 'master.json'},
        'sources': {name: dict(src.pointer(name), legend=SOURCES[name][0],
                               payload_shape=SOURCES[name][1])
                    for name in SOURCES},
        'reconciliation': {
            'enums_json_keys': len(src.json('enums.json')),
            'enum_extras_keys': len(src.json('enum_extras.json')),
            'union_keys': len(src.json('enums.json')) + len(src.json('enum_extras.json')),
            'frozen_master_keys': len(frozen),
            'delta_missing_from_master': dict_result['delta_missing_from_master'],
            'master_only': dict_result['master_only'],
            'identical_to_master': len(dict_result['unchanged']) - len(
                {c['enum'] for c in dict_result['conflicts']}),
            'conflicts': len(dict_result['conflicts']),
            'verdict': ('the frozen master already carries every dictionary key, so the '
                        'supplement adds provenance + field bindings, not new enum names'),
        },
        'counts': {
            'entries': len(entries),
            'entries_all_values_named': len(named),
            'entries_with_unnamed_values': len(unnamed),
            'entries_with_field_bindings': len(bindings),
            'entries_bound_to_frozen_field': sum(v['bound_to_frozen_field'] for v in entries.values()),
            'unnamed_enum_names': sorted(unnamed),
            'conflicts': len(dict_result['conflicts']),
        },
        'enums': entries,
        'conflicts': dict_result['conflicts'],
        'unchanged_keys': dict_result['unchanged'],
        'exe_enums_md': {
            'source': src.pointer('EXE_ENUMS.md'),
            'overview': md['overview'],
            'references': md['references'],
            'job_table_numbers': md['job_table_numbers'],
            'job_table_numbers_count': len(md['job_table_numbers']),
        },
        'crrp_static': {
            'source': src.pointer('enum_crrp_static.json'),
            'unicorn_source': src.pointer('enum_crrp_unicorn.json'),
            'evidence_level': crrp.get('evidence_level'),
            'builder': crrp.get('builder'),
            'id_range': crrp.get('id_range'),
            'display_value_range': crrp.get('display_value_range'),
            'residual_risk': crrp.get('residual_risk'),
            'status': crrp.get('status'),
            'confidence': crrp.get('confidence'),
            'unicorn_va': [crrp_unicorn.get('va_start'), crrp_unicorn.get('va_end_exclusive')],
            'unicorn_snippet_sha256': crrp_unicorn.get('snippet_sha256'),
            'cross_reference': 'also embedded as enums.crrp in master.json',
        },
        'L4': 0,
    }


def write_json(name, payload):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    text = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=False)
    path.write_text(text + '\n', encoding='utf-8')
    return path, sha256_bytes(text.encode('utf-8'))


def build():
    src = Sources()
    dict_result = build_dictionary(src)
    master_codes = dict_result['master'].get('field_codes') or {}
    supplement = supplement_document(src, dict_result)
    t61 = rescan_t61(dict_result, master_codes)
    t75 = rescan_t75(dict_result, master_codes)
    t73 = crosscheck_t73(dict_result)
    # cross-artefact pointers so a reader can walk the chain
    digest = sha256_bytes(canon(supplement).encode('utf-8'))
    supplement['self_sha256_canonical'] = digest
    t61['dictionary']['sha256_canonical'] = digest
    t75['dictionary'] = {'sha256_canonical': digest}
    t73['dictionary'] = {'sha256_canonical': digest}
    outputs = {}
    for name, payload in (('enum_supplement.json', supplement),
                          ('rescan_t61.json', t61),
                          ('rescan_t75.json', t75),
                          ('crosscheck_t73.json', t73)):
        path, sha = write_json(name, payload)
        outputs[name] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha,
                         'bytes': path.stat().st_size}
    need(sha256_bytes(read_bytes(MASTER)) == FROZEN_MASTER_SHA,
         'frozen master changed during the run')
    return {'supplement': supplement, 't61': t61, 't75': t75, 't73': t73,
            'outputs': outputs, 'sources': src}


def selftest():
    checks = []
    def ok(label, cond):
        checks.append((label, bool(cond)))
        need(cond, label)

    ok('sha256 of empty', sha256_bytes(b'') ==
       'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
    ok('to_int numeric', to_int('12') == 12 and to_int('-1') == -1)
    ok('to_int token', to_int('male') is None and to_int(None) is None)
    ok('basename windows', basename('format' + chr(92) + 'database' + chr(92) + 'club.xml') == 'club.xml')
    ok('basename posix', basename('database/database/city.xml') == 'city.xml')

    vals, domain, kind = normalize_values({'values': [
        {'enum': '1', 'enum_id': None, 'name': 'A'},
        {'enum': '3', 'enum_id': None, 'name': 'B'}]})
    ok('numeric enum', (domain, kind, len(vals)) == ([1, 3], 'numeric', 2))
    vals, domain, kind = normalize_values({'values': [
        {'enum': 'male', 'enum_id': '0', 'name': 'Male'},
        {'enum': 'female', 'enum_id': '1', 'name': 'Female'}]})
    ok('token enum', (domain, kind) == (None, 'token'))
    ok('wire domain from enum_id', wire_domain(
        {'kind': 'token', 'enum_id_domain': [0, 1], 'domain': None}) == {0, 1})

    # EXE_ENUMS.md parser against the pinned snapshot text
    src = Sources()
    md = parse_exe_enums_md(src.text('EXE_ENUMS.md'))
    ok('md overview rows', len(md['overview']) == 15)
    ok('md subs count', md['overview']['subs']['declared_count'] == 82)
    ok('md crrp count', md['overview']['crrp']['declared_count'] == 20)
    ok('md job table', len(md['job_table_numbers']) == 177)
    ok('md references', md['references'].get('crrp', {}).get('field') == 'repu')

    master = load_json(MASTER)
    frozen = master['enums']
    ok('frozen enum count', len(frozen) == 304)
    ok('DBvw all unnamed', all(not (x.get('name') or '').strip()
                               for x in frozen['DBvw']['values']))
    ok('cdbt covers Ccre wire', {0, 1, 2, 3, 4, 8} <=
       set(normalize_values(frozen['cdbt'])[1]))

    # binding helpers
    entities = {'Ngct': [{'file': 'nation.xml', 'record': 'nati', 'path': 'nati',
                          'name': 'Gain Nationality Type', 'type': 'enum',
                          'enum_ref': 'Ngct'}]}
    cands = bind_code('Ngct', {'nation.xml'}, entities, {}, {
        'Ngct': {'enum': 'Ngct', 'declared_file_basename': 'nation.xml',
                 'declared_file': 'format' + chr(92) + 'database' + chr(92) + 'nation.xml'}}, {})
    ok('explicit ref ranks highest', cands and cands[0]['strength'] == 3)
    cands = bind_code('Ngct', {'nation.xml'}, {}, {}, {
        'Ngct': {'enum': 'Ngct', 'declared_file_basename': 'nation.xml',
                 'declared_file': 'format' + chr(92) + 'database' + chr(92) + 'nation.xml'}}, {})
    ok('file+name binding strength 2', cands and cands[0]['strength'] == 2)
    cands = bind_code('Ngct', {'other.xml'}, {}, {}, {
        'Ngct': {'enum': 'Ngct', 'declared_file_basename': 'nation.xml',
                 'declared_file': 'format' + chr(92) + 'database' + chr(92) + 'nation.xml'}}, {})
    ok('name-only binding strength 1', cands and cands[0]['strength'] == 1)

    hist, sides = histogram({'archives': {'client': [
        {'status': 'scanned', 'histogram': {'1': 2}},
        {'status': 'mode_bypass', 'histogram': {'9': 9}}],
        'server': [{'status': 'scanned', 'histogram': {'2': 3}}]}})
    ok('histogram skips non-scanned', hist == {1: 2, 2: 3})
    ok('histogram sides', sorted(sides) == ['client', 'server'])

    # artifact invariants from the last build (if present)
    supp = OUT / 'enum_supplement.json'
    if supp.exists():
        doc = json.loads(supp.read_bytes())
        ok('supplement keeps master count', doc['frozen_master']['enums'] == 304)
        ok('supplement never invents keys',
           set(doc['enums']) == set(frozen) or not doc['enums'])
        ok('supplement sha pinned', doc['frozen_master']['sha256'] == FROZEN_MASTER_SHA)
        ok('no conflict silently dropped',
           len(doc['conflicts']) == doc['counts']['conflicts'])
    t61p = OUT / 'rescan_t61.json'
    if t61p.exists():
        doc = json.loads(t61p.read_bytes())
        ok('t61 rescan covers 67', doc['input']['occurrences'] == 67)
        ok('t61 outcomes sum', sum(doc['counts'].values()) == 67)
        ok('t61 L4 zero', doc['L4'] == 0)
    t75p = OUT / 'rescan_t75.json'
    if t75p.exists():
        doc = json.loads(t75p.read_bytes())
        ok('t75 covers every unfrozen key',
           len(doc['decisions']) == doc['unfrozen_key_count'])
        ok('t75 named keys present',
           set(doc['named_in_prompt']) <= {d['code'] for d in doc['decisions']})
        ok('t75 blockers kept verbatim', all('blocker_verbatim' in d for d in doc['decisions']))
    for label, passed in checks:
        print(f'  [{"ok" if passed else "FAIL"}] {label}')
    print(f'selftest: {len(checks)} checks, 0 failed')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='t80_enum_supplement.py',
        description=('Build the t80 enum supplement dictionary and rescan the t61 / '
                     't75 enum debt. Read-only over evidence/ and scratch/ inputs; '
                     'writes only scratch/t80/out/.'),
        epilog=('examples:\n'
                '  py -V:3.12 -I -B scripts/t80_enum_supplement.py --build\n'
                '  py -V:3.12 -I -B scripts/t80_enum_supplement.py --selftest\n'
                'exit codes: 0 ok, 1 check failed, 2 usage/fatal'))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--build', action='store_true',
                       help='rebuild enum_supplement.json / rescan_t61.json / rescan_t75.json / crosscheck_t73.json')
    group.add_argument('--selftest', action='store_true',
                       help='run built-in checks (needs the snapshotted evidence only)')
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        result = build()
        supp = result['supplement']
        print('frozen master    :', FROZEN_MASTER_SHA, '(unchanged)')
        print('dictionary entries:', supp['counts']['entries'],
              '| all-named:', supp['counts']['entries_all_values_named'],
              '| unnamed:', supp['counts']['entries_with_unnamed_values'],
              '| conflicts:', supp['counts']['conflicts'])
        print('t61 outcomes      :', json.dumps(result['t61']['counts'], ensure_ascii=False))
        print('t75 outcomes      :', json.dumps(result['t75']['counts'], ensure_ascii=False),
              '| unfrozen keys:', result['t75']['unfrozen_key_count'])
        print('t73/t76c enum slots:', len(result['t73']['slots']),
              '| DBvw names recovered:', result['t73']['dbvw_section']['supplement_recovers_names'])
        for name, info in result['outputs'].items():
            print(f'wrote {info["path"]} ({info["bytes"]} B) sha256={info["sha256"]}')
        return 0
    except Check as exc:
        print(f'CHECK FAILED: {exc}', file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError) as exc:
        print(f'FATAL: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
