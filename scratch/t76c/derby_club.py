"""t76c scratch: club name resolution to test derby Dtm1/Dtm2 as club ordinals."""
import runpy, struct, json

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

raw3 = load('client', 3)
rows = []
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
        break
    rows.append(raw3[pos:pos + picked])
    pos += picked
    j += 1
print('club rows', len(rows))


def club_name(b):
    """Extract the leading length-prefixed UTF-8 string if present."""
    for off in (0, 4, 8, 12, 16, 20, 24):
        if off + 4 > len(b):
            break
        k = struct.unpack_from('<I', b, off)[0]
        if 1 <= k <= 60 and off + 4 + k <= len(b):
            try:
                s = b[off + 4:off + 4 + k].decode('utf-8')
            except UnicodeDecodeError:
                continue
            if all(31 < ord(c) for c in s) and s.strip():
                return off, s
    return None, None


print('\n=== club row name probe (rows 560, 586, 0, 1, 2)')
for idx in (0, 1, 2, 560, 586):
    b = rows[idx]
    off, nm = club_name(b)
    print(f'  row{idx} len={len(b)} name_off={off} name={nm!r} hex0..40={b[:40].hex(" ")}')

print('\n=== derby rows: resolve Dtm1/Dtm2 as club ordinals')
NUM = {'client': 36}
rawd = load('client', 18)
pos, DD = 14, []
for j in range(1567):
    p, nb = pos, 0
    names = []
    for _ in range(4):
        ln = struct.unpack_from('<I', rawd, p)[0]
        names.append(rawd[p + 4:p + 4 + ln].decode('utf-8'))
        nb += ln
        p += 4 + ln
    end = pos + 16 + nb + 36 + 13
    DD.append((names, rawd[pos + 16 + nb:end - 13]))
    pos = end

hits = 0
for i in (0, 1, 2, 3, 4, 85):
    names, num = DD[i]
    t1 = int.from_bytes(num[4:8], 'little')
    t2 = int.from_bytes(num[8:12], 'little')
    n1 = club_name(rows[t1])[1] if t1 < len(rows) else None
    n2 = club_name(rows[t2])[1] if t2 < len(rows) else None
    print(f'  derby{i} names={names[:2]} -> club[{t1}]={n1!r} club[{t2}]={n2!r}')

print('\n=== same as UID lookup (wrong-UID control): treat @4 as club UID')
club_by_uid = {}
for i, b in enumerate(rows):
    u = struct.unpack_from('<I', b, len(b) - 9)[0]
    club_by_uid[u] = i
for i in (0, 1, 2):
    names, num = DD[i]
    t1 = int.from_bytes(num[4:8], 'little')
    print(f'  derby{i} @4={t1} as club UID -> row {club_by_uid.get(t1)}'
          f' name={club_name(rows[club_by_uid[t1]])[1] if t1 in club_by_uid else None!r}')
