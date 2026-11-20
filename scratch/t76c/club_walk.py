"""t76c scratch: validated club walker (t02 layout A/B) -> real club UID set."""
import runpy, struct

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
raw = load('client', 3)
FOOT = len(raw) - 8
print('payload', len(raw), 'footer at', FOOT)


def try_len(pos, base_full, base_short, const):
    """Row length from name-length fields; return (rowlen, identity_ok, uid)."""
    if pos + base_short + 4 > len(raw):
        return None
    fl = struct.unpack_from('<I', raw, pos + base_full)[0]
    sl = struct.unpack_from('<I', raw, pos + base_short)[0]
    if not (1 <= fl <= 120 and 0 <= sl <= 60):
        return None
    rowlen = const + fl + sl
    end = pos + rowlen
    if end > len(raw):
        return None
    a, b = struct.unpack_from('<II', raw, end - 9)
    return (rowlen, a == b != 0 and raw[end - 1] == 0, a)


rows, pos, j, stats = [], 14, 0, {'A': 0, 'B': 0, 'fail': 0}
while pos < FOOT:
    pick = None
    for tag, bf, bs, c in (('A', 26, 63, 50), ('B', 25, 62, 49)):
        t = try_len(pos, bf, bs, c)
        if t and t[1]:
            pick = (tag, t)
            break
    if pick is None:
        # fallback: scan for identity
        found = None
        for ln in range(20, 260):
            end = pos + ln
            if end > FOOT:
                break
            a, b = struct.unpack_from('<II', raw, end - 9)
            if a == b and raw[end - 1] == 0:
                found = (ln, a)
                break
        if found is None:
            print('STUCK at', pos, 'row', j)
            break
        stats['fail'] += 1
        rows.append((j, found[1]))
        pos += found[0]
        j += 1
        continue
    tag, (rowlen, _, uid) = pick
    stats[tag] += 1
    rows.append((j, uid))
    pos += rowlen
    j += 1

print('rows', len(rows), 'end', pos, 'expected', FOOT, 'match', pos == FOOT)
print('stats', stats)
uids = [u for _, u in rows]
print('distinct uids', len(set(uids)), 'min', min(uids), 'max', max(uids))
print('ordinal == row idx:', sum(1 for i, (j, _) in enumerate(rows) if j == i), '/', len(rows))
import json, pathlib
pathlib.Path('scratch/t76c/club_uids.json').write_text(json.dumps(uids))
