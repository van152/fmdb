import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def try_simple(raw):
    cnt = struct.unpack_from('<I', raw, 8)[0]
    pos, n = 12, 0
    ok = True
    while pos + 8 <= len(raw):
        i, l = struct.unpack_from('<II', raw, pos)
        if l > 4000 or pos + 8 + l > len(raw):
            ok = False; break
        pos += 8 + l; n += 1
    return cnt, n, pos, len(raw), ok

for nm in ('8_3.dat','8_10.dat','8_25.dat','8_0.dat','8_2.dat','8person_names.dat'):
    raw = lib.load_member('lang_update', nm)
    print(nm, 'len', len(raw), 'simple', try_simple(raw))

# byte-level dump of 8_3 in the ambiguous zone
raw = lib.load_member('lang_update','8_3.dat')
print('\n--- 8_3 bytes 40..200 ---')
for o in range(40, 200, 10):
    chunk = raw[o:o+10]
    print(f'{o:5d}', chunk.hex(' '), ''.join(chr(c) if 32<=c<127 else '.' for c in chunk))
