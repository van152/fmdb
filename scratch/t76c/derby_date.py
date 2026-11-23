"""t76c scratch: derby date hypothesis + Dfg slots + weather block scan + nation domain."""
import runpy, struct, json
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def derby_rows(arch):
    num = 36 if arch == 'client' else 42
    raw = load(arch, 18)
    pos, out = 14, []
    for j in range(1567):
        p, nb, names = pos, 0, []
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            names.append(raw[p + 4:p + 4 + ln].decode('utf-8'))
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        out.append(dict(row=j, names=names, num=raw[pos + 16 + nb:end - 13]))
        pos = end
    return out


D = derby_rows('client')
print('=== date hypothesis: u16@0 = day-of-year, u16@2 = year')
import datetime
ok = 0
for r in D[:8]:
    doy = int.from_bytes(r['num'][0:2], 'little')
    yr = int.from_bytes(r['num'][2:4], 'little')
    try:
        dt = datetime.date(yr, 1, 1) + datetime.timedelta(days=doy - 1)
    except Exception:
        dt = None
    print(f'  row{r["row"]:4} name={r["names"][0]!r:22} doy={doy:3} year={yr} -> {dt}')
doy_all = [int.from_bytes(r['num'][0:2], 'little') for r in D]
yr_all = [int.from_bytes(r['num'][2:4], 'little') for r in D]
print(f'  doy range {min(doy_all)}..{max(doy_all)}  year range {min(yr_all)}..{max(yr_all)}')
print('  doy<=366 rate', sum(1 for x in doy_all if x <= 366) / len(doy_all))
print('  year in [1850,2025] rate', sum(1 for x in yr_all if 1850 <= x <= 2025) / len(yr_all))

print('\n=== b28/b29 distributions (client)')
print('  b28', Counter(r['num'][28] for r in D).most_common(8))
print('  b29', Counter(r['num'][29] for r in D).most_common(8))
print('  both non-FF rows:', sum(1 for r in D if r['num'][28] != 255 and r['num'][29] != 255))
print('  b28==255 & b29==255:', sum(1 for r in D if r['num'][28] == 255 and r['num'][29] == 255))
print('  sample non-FF pairs:', [(r['num'][28], r['num'][29]) for r in D if r['num'][28] != 255][:15])
print('  b30..b33 all zero:', all(r['num'][30:34] == b'\0\0\0\0' for r in D))
print('  b24..b27 all FF:', all(r['num'][24:28] == b'\xff\xff\xff\xff' for r in D))
print('  b34 range', min(r['num'][34] for r in D), max(r['num'][34] for r in D))
print('  b35 range', min(r['num'][35] for r in D), max(r['num'][35] for r in D))

print('\n=== server-only 6B insert: 3 u16')
S = derby_rows('server')
for off in (28, 30, 32):
    v = [int.from_bytes(r['num'][off:off + 2], 'little') for r in S]
    nn = [x for x in v if x != 0xFFFF]
    print(f'  u16@{off}: null={v.count(0xFFFF)} nonnull={len(nn)} '
          f'min={min(nn) if nn else None} max={max(nn) if nn else None} '
          f'<=10000 rate={sum(1 for x in nn if x <= 10000)/max(1,len(nn)):.4f}')
print('  all three null together:', sum(1 for r in S if r['num'][28:34] == b'\xff' * 6))
print('  client b28/b29 == server b34/b35:',
      all(c['num'][28:30] == s['num'][34:36] for c, s in zip(D, S)))
print('  client[0:28] == server[0:28]:', all(c['num'][:28] == s['num'][:28] for c, s in zip(D, S)))

print('\n=== nation domain (t10)')
raw10 = load('client', 10)
print('  t10 payload', len(raw10), 'count@8', struct.unpack_from('<I', raw10, 8)[0])
fr = core['resolve_frame'](raw10, min_rows=1)
print('  resolve:', fr['resolved'], fr['closed_candidates'])
