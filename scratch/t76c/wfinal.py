"""t76c scratch: decisive weather block field map (correct windows) + dn conflict."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
raw = core['load_payload']('client', 27)
M, pos, NM = [], 14, []
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    NM.append(raw[pos + 4:pos + 4 + ln].decode())
    pos = end
n = len(M)

print('=== windows under A = 3 + 4*23 (correct offsets)')
for b in range(4):
    base = 3 + 23 * b
    p = [sum(m[base + 2:base + 7]) for m in M]
    w = [sum(m[base + 7:base + 12]) for m in M]
    t = [sum(m[base + 12:base + 22]) for m in M]
    sd = [m[base] for m in M]
    print(f' block{b} sd[{min(sd)},{max(sd)}] p100={p.count(100)} w100={w.count(100)} '
          f't100={t.count(100)} p0rows={p.count(0)} w0rows={w.count(0)} t0rows={t.count(0)}')

print('\n=== rel22 ({0,100}) vs all-zero temperature rows')
z = {j for j in range(n) if sum(M[j][15:25]) == 0}
h = {j for j in range(n) if M[j][25] == 100}
print('  allzero-temp rows:', len(z), ' rel22==100 rows:', len(h))
print('  overlap:', len(z & h), ' h-z:', len(h - z), ' z-h:', len(z - h))
print('  names of rel22==100 rows:', [NM[j].encode('ascii','replace').decode() for j in sorted(h)][:6])
print('  names of allzero rows:', [NM[j].encode('ascii','replace').decode() for j in sorted(z)][:6])

print('\n=== is rel22 exactly == 100 iff block0 temp all-zero?')
print('  block0 allzero == rel22 100 :', z == h)

print('\n=== dn candidates: any byte in block with range <=50 and not already used?')
for b in range(4):
    base = 3 + 23 * b
    for rel in range(23):
        v = [m[base + rel] for m in M]
        if max(v) <= 50 and len(set(v)) > 1:
            print(f'  block{b} rel{rel}: [{min(v)},{max(v)}] d={len(set(v))}')

print('\n=== does temp group sum to 100 when excluding rel12/rel21?')
for b in range(4):
    base = 3 + 23 * b
    for lo, hi, nm in ((12, 22, 'rel12..21'), (13, 22, 'rel13..21'),
                       (12, 21, 'rel12..20'), (14, 22, 'rel14..21')):
        s = [sum(m[base + lo:base + hi]) for m in M]
        print(f'  block{b} {nm}: sum100={s.count(100)}')
