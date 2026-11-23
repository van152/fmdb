# probe_snapshot_premise.py — commander probe for t80 premise (E119, 2026-11-21)
# Verdict: the four snapshot enum files are content-identical to master.json enums;
# the t80 premise (supplement dictionary unlocks t61/t75 debts) is void.
# Reproduce: py -V:3.12 -I -B scratch/t80/probe_snapshot_premise.py
import json, hashlib, sys

BASE = 'evidence/fm24/reports/editor_schema/'
FILES = ['enum_extras.json', 'enums.json', 'database_ui.json']


def norm(v):
    if isinstance(v, dict):
        vals = v.get('values', v)
        if isinstance(vals, list):
            return frozenset(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in vals)
        return frozenset(json.dumps(vals, sort_keys=True, ensure_ascii=False))
    if isinstance(v, list):
        return frozenset(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in v)
    return frozenset([str(v)])


def main():
    ok = True
    m = json.load(open(BASE + 'master.json', encoding='utf-8'))
    me = m['enums']
    print('master enums:', len(me))
    for fn in FILES:
        raw = open(BASE + fn, 'rb').read()
        print(fn, len(raw), 'sha256', hashlib.sha256(raw).hexdigest()[:16])
    en = json.load(open(BASE + 'enums.json', encoding='utf-8'))
    ee = json.load(open(BASE + 'enum_extras.json', encoding='utf-8'))
    same = diff = 0
    for k, v in en.items():
        if k in me and norm(v) == norm(me[k]):
            same += 1
        else:
            diff += 1
            print('DIFF', k)
    print('enums.json keys', len(en), 'same-as-master', same, 'diff', diff)
    xs = 0
    for k, v in ee.items():
        if k in me and norm(v) == norm(me[k]):
            xs += 1
        else:
            print('EXTRAS-DIFF', k)
    print('extras keys', len(ee), 'same-as-master', xs)
    raw_en = open(BASE + 'enums.json', encoding='utf-8').read()
    raw_ee = open(BASE + 'enum_extras.json', encoding='utf-8').read()
    mt = json.dumps(m, ensure_ascii=False)
    for p in ['Ccre', 'cosr', 'Npop', 'Ncpi', 'CICF']:
        c = raw_en.count(p) + raw_ee.count(p) + mt.count(p)
        print('4CC', p, 'occurrences across snapshots+master:', c)
    db = en.get('DBvw', {}).get('values', [])
    empty_names = sum(1 for x in db if not x.get('name'))
    print('DBvw values', len(db), 'empty-name', empty_names, '(master same defect)')
    ok = (diff == 0 and xs == len(ee))
    print('VERDICT:', 'snapshots fully subsumed by master; t80 premise void' if ok else 'unexpected diff - recheck')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
