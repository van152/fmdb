# commander probe: external uid anchors (ext/fm-editor FM24 doc) vs our table_45 wire data
# inputs: scratch/t88/out2/{_p_server_45.bin,_starts.bin} ; ext tags = hypothesis, tested on our data
import sys, struct, json, os

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = 'D:/tmp2b/fm24-db'
pay = open(BASE + '/scratch/t88/out2/_p_server_45.bin', 'rb').read()
st_raw = open(BASE + '/scratch/t88/out2/_starts.bin', 'rb').read()

n = 84477
if len(st_raw) == 4 * n:
    starts = list(struct.unpack_from('<%dI' % n, st_raw, 0))
elif len(st_raw) == 8 * n:
    starts = list(struct.unpack_from('<%dQ' % n, st_raw, 0))
else:
    print('starts format? size=%d n=%d' % (len(st_raw), n)); sys.exit(2)

rows = []
for s in starts:
    nl = struct.unpack_from('<I', pay, s + 37)[0]
    name = pay[s + 41:s + 41 + nl]
    club = struct.unpack_from('<I', pay, s)[0]
    rt = pay[s + 4]
    person = struct.unpack_from('<I', pay, s + 5)[0]
    rows.append((club, rt, person, name))

res = {'rows': len(rows), 'tests': {}}

# T1/T2: name contains Kane / Ronaldo
kane = [r for r in rows if b'Kane' in r[3]]
ron = [r for r in rows if b'Ronaldo' in r[3]]
res['tests']['kane_rows'] = len(kane)
res['tests']['kane_person_uids'] = sorted({r[2] for r in kane})[:10]
res['tests']['kane_sample'] = [
    {'club': r[0], 'rt': r[1], 'person': r[2], 'name': r[3].decode('utf-8', 'replace')}
    for r in kane[:5]]
res['tests']['ronaldo_rows'] = len(ron)
res['tests']['ronaldo_person_uids'] = sorted({r[2] for r in ron})[:10]

# T3: club-uid set membership (external: Bayern=915, Tottenham=728, Antalyaspor=1865)
cset = {r[0] for r in rows}
for tag, uid in (('bayern', 915), ('tottenham', 728), ('antalyaspor', 1865)):
    res['tests']['club_' + tag] = {'uid': uid, 'member': uid in cset,
                                   'rows': sum(1 for r in rows if r[0] == uid)}

# T4: person set + Kane anchor membership
pset = {r[2] for r in rows}
res['tests']['person_set_size'] = len(pset)
res['tests']['kane_uid_28049320_member'] = 28049320 in pset
res['tests']['ronaldo_uid_735216_member'] = 735216 in pset
res['tests']['person_max'] = max(pset) if pset else None
res['tests']['person_min'] = min(pset) if pset else None

# T5: Kane rows rec_type distribution (accessor-model families)
from collections import Counter
res['tests']['kane_rt_hist'] = dict(Counter(r[1] for r in kane))
res['tests']['rt_hist_top'] = dict(Counter(r[1] for r in rows).most_common(10))

with open(BASE + '/scratch/cmd/t93_ext_probe.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

print('rows=%d kane_rows=%d ronaldo_rows=%d' % (len(rows), len(kane), len(ron)))
print('kane_uid 28049320 member:', res['tests']['kane_uid_28049320_member'])
print('ronaldo_uid 735216 member:', res['tests']['ronaldo_uid_735216_member'])
for tag in ('bayern', 'tottenham', 'antalyaspor'):
    t = res['tests']['club_' + tag]
    print('%s uid=%d member=%s rows=%d' % (tag, t['uid'], t['member'], t['rows']))
print('kane_rt_hist:', res['tests']['kane_rt_hist'])
for s in res['tests']['kane_sample']:
    print('  ', s)
