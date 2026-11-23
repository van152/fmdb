"""t76c scratch: decisive domain tests WITH shuffle controls (wrong-UID control)."""
import runpy, struct, json, random
from collections import Counter
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
D = json.loads(Path('scratch/t76c/domains_client.json').read_text())
CITY = set(D['city']['uid_set'])
STAD = set(D['stadium']['uid_set'])
LANG = set(D['language']['uid_set'])
WEAT = set(D['weather']['uid_set'])
LCRG = set(D['local_region']['uid_set'])
REGN = set(D['region']['uid_set'])
CONT = set(D['continent']['uid_set'])
AGRM = set(D['agreement']['uid_set'])

# club (t3) real UID set via the frozen club_block grammar (duni at row_end-9)
raw3 = load('client', 3)
CLUB = []
pos, j = 14, 0
while j < 84259:
    picked = None
    for ln in range(20, 200):
        t = pos + ln - 9
        if t + 9 > len(raw3):
            break
        a, b = struct.unpack_from('<II', raw3, t)
        if a == b and raw3[t + 8] == 0:
            picked = ln
            break
    if picked is None:
        print('club stuck at', pos, j)
        break
    CLUB.append(struct.unpack_from('<I', raw3, pos + picked - 9)[0])
    pos += picked
    j += 1
print('club rows', len(CLUB), 'distinct uids', len(set(CLUB)), 'end', pos,
      'payload', len(raw3))
CLUBS = set(CLUB)


def shuffle_ctrl(vals, S, trials=40):
    rng = random.Random(20261120)
    out = []
    v = list(vals)
    for _ in range(trials):
        rng.shuffle(v)
        out.append(sum(1 for x in v if x in S) / max(1, len(v)))
    return round(sum(out) / len(out), 4), round(max(out), 4)


def rep(label, vals, S, sname):
    vals = [x for x in vals if x != 0xFFFFFFFF]
    if not vals:
        print(f'  {label}: empty')
        return
    obs = sum(1 for x in vals if x in S) / len(vals)
    mean, mx = shuffle_ctrl(vals, S)
    print(f'  {label}: n={len(vals)} distinct={len(set(vals))} '
          f'hit={obs:.4f} shuffle_mean={mean:.4f} shuffle_max={mx:.4f} '
          f'verdict={"SIGNAL" if obs > mx + 0.02 else "no-signal"}')


NUM = {'client': 36, 'server': 42}
for arch in ('client', 'server'):
    raw = load(arch, 18)
    pos, DD = 14, []
    for j in range(1567):
        p, nb = pos, 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + NUM[arch] + 13
        DD.append(raw[pos + 16 + nb:end - 13])
        pos = end
    print('=' * 20, 'derby', arch)
    for off, w in ((4, 4), (8, 4), (12, 4), (16, 4), (20, 4)):
        v = [int.from_bytes(d[off:off + w], 'little') for d in DD]
        nn = [x for x in v if x != 0xFFFFFFFF]
        print(f' @{off} w{w}: null={v.count(0xFFFFFFFF)} nonnull={len(nn)} '
              f'min={min(nn)} max={max(nn)}')
    v4 = [int.from_bytes(d[4:8], 'little') for d in DD]
    v8 = [int.from_bytes(d[8:12], 'little') for d in DD]
    print(' Dtm1 vs club UID set:'); rep('  @4', v4, CLUBS, 'club')
    print(' Dtm2 vs club UID set:'); rep('  @8', v8, CLUBS, 'club')
    print(' Dtm1 vs city UID set (wrong control):'); rep('  @4', v4, CITY, 'city')
    print(' Dtm1 vs stadium UID set (wrong control):'); rep('  @4', v4, STAD, 'stad')
    print(' ordinal-domain test (v < N):')
    for nm, N in (('club/team 84507', 84507), ('club 84259', 84259),
                  ('comp 7047', 7047), ('stadium 48413', 48413)):
        for lbl, v in (('@4', v4), ('@8', v8), ('@12', [int.from_bytes(d[12:16], 'little') for d in DD]),
                       ('@16', [int.from_bytes(d[16:20], 'little') for d in DD])):
            nn = [x for x in v if x != 0xFFFFFFFF]
            r = sum(1 for x in nn if x < N) / max(1, len(nn))
            if r > 0.99:
                print(f'   {lbl} < {nm}: {r:.4f} ({len(nn)})')
    # b28..b35
    print(' b28..b35 profile:')
    for off in range(28, NUM[arch]):
        v = [d[off] for d in DD]
        print(f'   b{off}: d={len(set(v)):4} min={min(v):3} max={max(v):3} '
              f'zero={v.count(0):4} ff={v.count(255):4}')
    if arch == 'server':
        for k, off in enumerate((28, 30, 32)):
            v = [int.from_bytes(d[off:off + 2], 'little') for d in DD]
            nn = [x for x in v if x != 0xFFFF]
            print(f'   u16@{off} (D1t{k}): null={v.count(0xFFFF)} nonnull={len(nn)} '
                  f'min={min(nn)} max={max(nn)} distinct={len(set(nn))}')
    else:
        for off in (28, 30, 32):
            v = [int.from_bytes(d[off:off + 2], 'little') for d in DD]
            nn = [x for x in v if x != 0xFFFF]
            print(f'   u16@{off}: null={v.count(0xFFFF)} nonnull={len(nn)} '
                  f'min={min(nn) if nn else None} max={max(nn) if nn else None}')
