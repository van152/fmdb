"""t76c scratch: decisive derby archive delta = the 3 server-only schema fields."""
import runpy, struct, json

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
m = json.load(open('evidence/fm24/reports/editor_schema/master.json', encoding='utf-8'))


def derby(arch):
    num = 36 if arch == 'client' else 42
    raw = load(arch, 18)
    pos, out = 14, []
    for j in range(1567):
        p, nb = pos, 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        out.append(raw[pos + 16 + nb:end - 13])
        pos = end
    assert pos + 8 == len(raw)
    return out


C, S = derby('client'), derby('server')
print('client num=36 server num=42 delta=', 42 - 36)

print('\n=== byte-identity map client vs server, first 28 bytes')
print('  identical[0:28]:', all(c[0:28] == s[0:28] for c, s in zip(C, S)))

print('\n=== client @24..27 and @30..33')
for off, w in ((24, 4), (30, 4)):
    v = [int.from_bytes(c[off:off + w], 'little') for c in C]
    print(f'  client @{off} w={w}: distinct={sorted(set(v))[:4]} '
          f'ff={v.count(0xFFFFFFFF)} zero={v.count(0)}')

print('\n=== server @24..27, @28..33, @36..39')
for off, w in ((24, 4), (28, 2), (30, 2), (32, 2), (34, 1), (35, 1), (36, 4)):
    v = [int.from_bytes(s[off:off + w], 'little') for s in S]
    print(f'  server @{off} w={w}: distinct={sorted(set(v))[:5]} ff/allone={v.count((1<<(8*w))-1)} zero={v.count(0)}')

print('\n=== server[34:36] == client[28:30] ?', all(s[34:36] == c[28:30] for c, s in zip(C, S)))
print('=== server[40:42] == client[34:36] ?', all(s[40:42] == c[34:36] for c, s in zip(C, S)))

print('\n=== server-only fields per schema (no is_client_field)')
ent = m['entities']['derby.xml'][0]
non_client = [f['field'] for f in ent['fields'] if not f.get('is_client_field')]
print('  ', non_client)
print('  count of D1tw/D1td/D1tl =', 3, ' -> 3 x u16 = 6 bytes = the exact delta')

print('\n=== the 3 u16 all-null-together behaviour (server)')
tri = [tuple(int.from_bytes(s[o:o + 2], 'little') for o in (28, 30, 32)) for s in S]
allnull = sum(1 for t in tri if t == (0xFFFF, 0xFFFF, 0xFFFF))
print('  all-null rows:', allnull, 'nonnull rows:', len(tri) - allnull)
part = sum(1 for t in tri if 0xFFFF in t and t != (0xFFFF,) * 3)
print('  partially-null rows (mixed):', part, '<- would break a 3-field optional group')
nn = [t for t in tri if t[0] != 0xFFFF]
print('  nonnull ranges:', [(min(x[i] for x in nn), max(x[i] for x in nn)) for i in range(3)])

print('\n=== weather: any non-client fields? (if so client==server would be violated)')
we = m['entities']['weather.xml'][0]
wnc = [f['field'] for f in we['fields'] if not f.get('is_client_field')]
print('  non-client weather fields:', wnc)

print('\n=== agreement / lcrg non-client fields')
for k in ('agreement.xml', 'local region.xml'):
    e = m['entities'][k][0]
    print(' ', k, [f['field'] for f in e['fields'] if not f.get('is_client_field')])
