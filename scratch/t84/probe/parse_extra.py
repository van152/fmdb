import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib

def parse_pool(raw):
    assert raw[:8] == b'\x03\x01tad.\xf1\x0d'
    cnt = struct.unpack_from('<I', raw, 8)[0]
    pos, recs, bad = 12, [], []
    while pos + 8 <= len(raw):
        idx, ln = struct.unpack_from('<II', raw, pos)
        if ln > 4096 or pos + 8 + ln > len(raw):
            bad.append((pos, idx, ln)); break
        recs.append((idx, raw[pos+8:pos+8+ln]))
        pos += 8 + ln
    return cnt, recs, pos, len(raw), bad

for a in ('client','server'):
    for n in (0,1,2):
        raw = lib.load_member(a, f'name_table_extra_{n}.dat')
        cnt, recs, pos, total, bad = parse_pool(raw)
        idxs = [r[0] for r in recs]
        print(a, n, 'count_hdr', cnt, 'parsed', len(recs), 'end', pos, 'len', total,
              'monotone', idxs == list(range(len(recs))), 'bad', bad[:1])
        print('   first5', [r[1] for r in recs[:5]])
