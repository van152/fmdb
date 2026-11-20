"""t76c scratch: robust club name extraction, then derby Dtm1/Dtm2 -> club ordinal proof."""
import runpy, struct

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def club_rows():
    raw = load('client', 3)
    rows, pos, j = [], 14, 0
    while j < 84259:
        picked = None
        for ln in range(20, 200):
            t = pos + ln - 9
            if t + 9 > len(raw):
                break
            a, b = struct.unpack_from('<II', raw, t)
            if a == b and raw[t + 8] == 0:
                picked = ln
                break
        if picked is None:
            break
        rows.append(raw[pos:pos + picked])
        pos += picked
        j += 1
    return rows


def all_strings(b, minlen=3, maxlen=80):
    """Every (offset, text) where a u32 length prefix is followed by printable UTF-8."""
    out = []
    for off in range(0, len(b) - 5):
        k = struct.unpack_from('<I', b, off)[0]
        if minlen <= k <= maxlen and off + 4 + k <= len(b):
            try:
                s = b[off + 4:off + 4 + k].decode('utf-8')
            except UnicodeDecodeError:
                continue
            if all(31 < ord(c) for c in s) and any(c.isalpha() for c in s):
                out.append((off, s))
    return out


C = club_rows()
print('club rows', len(C))
for idx in (0, 1, 2, 560, 586, 10841, 24204, 1380, 1370, 959, 952, 63186, 62910, 84, 73):
    if idx >= len(C):
        continue
    ss = all_strings(C[idx])
    print(f'  club[{idx}] len={len(C[idx])} strings={ss[:3]}')

print('\n=== derby Dtm1/Dtm2 as club ordinals')
rawd = load('client', 18)
pos, DD = 14, []
for j in range(1567):
    p, nb, names = pos, 0, []
    for _ in range(4):
        ln = struct.unpack_from('<I', rawd, p)[0]
        names.append(rawd[p + 4:p + 4 + ln].decode('utf-8'))
        nb += ln
        p += 4 + ln
    end = pos + 16 + nb + 36 + 13
    DD.append((names, rawd[pos + 16 + nb:end - 13]))
    pos = end

for i in (0, 1, 2, 3, 4, 5, 85, 100, 200, 500, 900, 1200):
    names, num = DD[i]
    t1 = int.from_bytes(num[4:8], 'little')
    t2 = int.from_bytes(num[8:12], 'little')
    s1 = all_strings(C[t1]) if t1 < len(C) else []
    s2 = all_strings(C[t2]) if t2 < len(C) else []
    print(f'  derby{i} name={names[0]!r:24} T1={t1:<6}->{(s1[0][1] if s1 else None)!r:34} '
          f'T2={t2:<6}->{(s2[0][1] if s2 else None)!r}')
