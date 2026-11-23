import sys, json, struct
sys.path.insert(0, 'scratch/t85/work')
sys.stdout.reconfigure(encoding='utf-8')
import common as C
out = {}
for archive in ('client', 'server'):
    ents, _ = C.entries(archive)
    for e in ents:
        if e.get('entry_type') != 'table':
            continue
        raw = C.payload(archive, e['path'], int(e['size']))
        n = 0; first = []
        for i in range(0, len(raw) - 13):
            a, b, c = struct.unpack_from('<III', raw, i)
            if b == c and raw[i+12] == 0 and a == n:
                n += 1
                if len(first) < 3:
                    first.append(i)
        out[f'{archive}|{e["path"]}'] = {'payload': len(raw), 'ident_rows': n, 'first': first}
        print(f'{archive:6s} {e["path"]:36s} payload={len(raw):9d} ident_rows={n:6d} first={first}')
json.dump(out, open('scratch/t85/work/ident_census.json', 'w'), indent=1)
