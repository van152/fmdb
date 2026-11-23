import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib

def parse_pool(raw):
    cnt = struct.unpack_from('<I', raw, 8)[0]
    pos, recs = 12, []
    while pos + 8 <= len(raw):
        idx, ln = struct.unpack_from('<II', raw, pos)
        recs.append((idx, raw[pos+8:pos+8+ln]))
        pos += 8 + ln
    return cnt, recs

POOLS = {}
for n in (0,1,2):
    cnt, recs = parse_pool(lib.load_member('client', f'name_table_extra_{n}.dat'))
    POOLS[n] = recs

needles = [b'Albpetrol', b'Liverpool', b'Premier Division', b'England', b'Klubi i Futbollit']
for n, recs in POOLS.items():
    for nd in needles:
        hits = [(i, s) for i, s in recs if nd in s]
        print(f'pool{n} {nd!r}: {len(hits)} hits, first {hits[:3]}')
