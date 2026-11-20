"""t76c scratch: identify weather block rel1 and rel22 semantics."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
raw = core['load_payload']('client', 27)
M, pos, NM = [], 14, []
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    NM.append(raw[pos + 4:pos + 4 + ln].decode('utf-8', 'replace'))
    pos = end
n = len(M)


def grp(m, b, o, L):
    base = 3 + 23 * b
    return m[base + o:base + o + L]


print('=== rel1 == 1  =>  is that block all-zero in p/w/t ?')
for b in range(4):
    one = [j for j in range(n) if grp(M[j], b, 1, 1)[0] == 1]
    zero_all = sum(1 for j in one
                   if sum(grp(M[j], b, 2, 5)) == 0 and sum(grp(M[j], b, 7, 5)) == 0
                   and sum(grp(M[j], b, 12, 10)) == 0)
    print(f'  block{b}: rel1==1 rows={len(one)}  of which p/w/t all zero={zero_all}')
    print(f'           rel1==0 rows={n-len(one)}  seed(sd) vals={sorted({M[j][3+23*b] for j in range(n) if grp(M[j],b,1,1)[0]==1})[:8]}')

print('\n=== rel22 (byte 25/48/71/94, identical across blocks) vs climate')
print('  distinct per row set:', {len({M[j][3+23*b+22] for b in range(4)}) for j in range(n)})
print('  20 rows with 100:')
for j in range(n):
    if M[j][25] == 100:
        print('   ', NM[j].encode('ascii', 'replace').decode(),
              'block temps:', [sum(grp(M[j], b, 12, 10)) for b in range(4)])

print('\n=== DAWN/NIGHT (w*bdn, 0..50): search every byte of the row for a 0..50 column')
import collections
lens = []
for j in range(n):
    lens.append(len(NM[j]))
for off in range(95):
    v = [m[off] for m in M]
    if max(v) <= 50 and len(set(v)) >= 3 and off not in (25, 48, 71, 94):
        print(f'  mid off{off}: [{min(v)},{max(v)}] d={len(set(v))} '
              f'z={v.count(0)}')

print('\n=== sanity: 4 blocks x 22 schema fields vs 23 bytes')
print('  schema block = sd + p0..p4 + w0..w4 + te,tv,t0..t7 + dn = ',
      1 + 5 + 5 + 10 + 1, 'bytes; block size =', 23)
