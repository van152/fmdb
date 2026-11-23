"""Full-archive vectorized profiler of EVERY field in client_db & server_db table_extra_3.dat (84,259 x 2 rows)
plus exact master.json metadata check for all enum/multiple_enum/list/colour candidates.
"""
import json, os, struct, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd

ROOT = Path(r'D:\tmp2b\fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR', ROOT / 'scratch/data'))
HEAD = bytes.fromhex('03017461642ef10d')

# 1. Inspect exact master.json entries for enum / multiple_enum / list candidates
master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
club_by_code = defaultdict(list)
for idx, f in enumerate(club_fields): club_by_code[f['field']].append((idx, f))

print('=== 1. Exact club.xml schema dicts for enum/multiple_enum/real/string/colour/list candidates ===')
for fc in ['CScP', 'Cown', 'Chti', 'Cepr', 'Cpfr', 'C2pf', 'Cdfo', 'Cafo',
           'Cuf1', 'Cf10', 'TCht', 'TCnn', 'ttcl', 'tbcl', '1scl', 'Tko1', 'Cspb', 'Cren', 'TCrs',
           'Camc', 'Cbbl', 'Csoc', 'pcpt', 'CPsL', 'Cscm', 'Crkt', 'Csly', 'Ctlv', 'Csth']:
    for idx, f in club_by_code.get(fc, []):
        print(f'  [{idx:3d}] {fc}: {json.dumps(f, ensure_ascii=False)}')

# 2. Extract table_extra_3.dat from both archives (and table_3.dat for club UIDs)
def extract_member(side, member_rel):
    b = (DATA / f'{side}_db.dat').read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from('<QQ', b, 17))
    assert base == 34 and b[8:17] == b[toc:toc+9] == b'\x02\x01fmf.\x08\x00\x00'
    def frame(buf):
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(buf)
        return v, len(buf) - len(d.unused_data)
    directory, used = frame(b[toc+9:])
    assert toc + 9 + used == len(b)
    p = 0; entries = {}
    def pull(n):
        nonlocal p; r = directory[p:p+n]; p += n; return r
    def num(): return struct.unpack('<I', pull(4))[0]
    def text(): return pull(num()).decode('utf-8')
    def node(parent):
        prefix = parent + text() + '/'
        for _ in range(num()):
            name = prefix + text() + text()
            off, size, unpacked, _, _ = struct.unpack('<5Q', pull(40))
            entries[name] = (base + off, base + off + size, unpacked)
        for _ in range(num()): node(prefix)
    node('')
    lo, hi, n = entries[member_rel]
    q = lo; out = None
    while q < hi:
        pl, w = frame(b[q:hi]); q += w
        if len(pl) == n: out = pl
    assert out is not None and out[:8] == HEAD
    return out, entries

cli_b, cli_ent = extract_member('client', 'client_db/table_extra_3.dat')
srv_b, srv_ent = extract_member('server', 'server_db/table_extra_3.dat')
N_cli = struct.unpack_from('<I', cli_b, 8)[0]
N_srv = struct.unpack_from('<I', srv_b, 8)[0]
print(f'\n=== 2. Extracted table_extra_3.dat: client={len(cli_b)}B (N={N_cli}), server={len(srv_b)}B (N={N_srv}) ===')
assert N_cli == N_srv == 84259
N = N_srv

# Helper: date4 validation (u16 doy_bits, u16 year) -> low 9 bits = day 1..366, high 7 bits = 0, year >= 1
def check_date4_arr(arr_u32):
    year = (arr_u32 >> 16) & 0xffff
    doy = arr_u32 & 0x1ff
    mid = (arr_u32 >> 9) & 0x7f
    leap = ((year % 4 == 0) & ((year % 100 != 0) | (year % 400 == 0))).astype(np.uint32)
    sentinel = (arr_u32 == 0x076c0001)  # 1900-01-01 default sentinel!
    valid = (year >= 1) & (doy >= 1) & (doy <= 365 + leap) & (mid == 0)
    return valid, sentinel

# 3. Full sequential replay collecting EVERY field across all 84,259 rows!
def parse_extra3(b, server):
    n = struct.unpack_from('<I', b, 8)[0]
    p = 12
    # Fixed-per-row arrays
    res = {
        'd8': np.empty(n, dtype='<u2'),
        'cc': np.empty(n, dtype='<u4'),
        'base_ac': np.empty(n, dtype='<u2'),
        'base_a0': np.empty(n, dtype='<u4'),
        'base_a8': np.empty(n, dtype='<u4'),
        'base78_cnt': np.empty(n, dtype=np.uint8),
        'tcht_len': np.empty(n, dtype='<u4'),
        'tcht_nonempty': [],
        'tcht_bad_utf8': 0,
        'kit_types': Counter(),
        'kit_years': Counter(),
        'kit_flags': Counter(),
        'kit_b23': Counter(),
        'kit_b24': Counter(),
        'kit_b25': Counter(),
        'kit_comp_nz': 0,
        'kit_total': 0,
    }
    if server:
        for k, dt in [
            ('e120', 'i1'), ('e121', 'i1'), ('e122', 'i1'),
            ('e18_cnt', '<u2'),
            ('eda_tag', 'u1'), ('eda_b1', 'u1'), ('eda_b2', 'u1'), ('eda_b3', 'u1'), ('eda_b4', 'u1'),
            ('e123', 'i1'), ('ec0', '<i4'),
            ('edates_flag', 'u1'),
            ('ede', '<u2'), ('eb8', '<u4'), ('e125', 'i1'), ('e84', '<u4'), ('e80', '<u4'),
            ('elec_flag', 'u1'),
            ('elec_club', '<i4'), ('elec_d1', '<u4'), ('elec_d2', '<u4'),
            ('Cepr', '<i2'), ('Cetl', 'i1'), ('Cmtm', 'i1'), ('Cect', 'i1'), ('Cemn', 'i1'), ('Cemx', 'i1'),
            ('e126', 'i1'), ('e127', 'i1'), ('e128', 'i1'), ('e129', 'i1'), ('e12a', 'i1'),
            # supporter profile 1 (+f8) & 2 (+10c)
            ('f8_ver', 'u1'), ('f8_CsSF', '<i4'), ('f8_CsSS', '<i2'), ('f8_CsST', '<i2'),
            ('Csly', 'i1'), ('Csps', 'i1'), ('Cspt', 'i1'), ('Csaf', 'i1'), ('Cste', 'i1'), ('Cspe', 'i1'),
            ('f8_0e', 'i1'), ('f8_0f', 'i1'), ('f8_10', 'i1'), ('f8_11', 'i1'), ('f8_12', 'i1'), ('f8_13', 'i1'),
            ('p10c_ver', 'u1'), ('p10c_00', '<i4'), ('p10c_04', '<i2'), ('p10c_06', '<i2'),
            ('p10c_08', 'i1'), ('p10c_09', 'i1'), ('p10c_0a', 'i1'), ('p10c_0b', 'i1'), ('p10c_0c', 'i1'), ('p10c_0d', 'i1'),
            ('ebc', '<u4'), ('ec4', '<i4'), ('ec8', '<i4'),
            ('e12b', 'i1'), ('e12c', 'i1'), ('e12d', 'i1'), ('e12e', 'i1'), ('e12f', 'i1'),
            ('ed0', '<i4'), ('ed4', '<i4'),
            ('e28_cnt', 'i1'), ('e20_cnt', 'u1'),
            ('e48_flag', 'u1'), ('e48_cnt', 'u1'), ('e48_head', 'u1'),
            ('e68_cnt', '<u2'), ('edc', '<u2'),
            # base server tail
            ('b18_cnt', '<i2'), ('b30_cnt', 'i1'),
            ('Cpfr', 'i1'), ('C2pf', 'i1'), ('Cdfo', 'i1'), ('Cafo', 'i1'),
            ('Catd', '<i4'), ('Cmna', '<i4'), ('Cmxa', '<i4'),
            ('b0_cnt', '<u2'), ('b48_flag', 'u1'), ('b48_cnt', '<u4'),
        ]:
            res[k] = np.full(n, -1 if dt.endswith(('i1','i2','i4')) else 0, dtype=dt)
        res['e88_dates'] = np.empty((n, 6), dtype='<u4')
        res['ea0_dates'] = np.zeros((n, 6), dtype='<u4')
        res['cuf'] = np.full((n, 10), np.nan, dtype=np.float64)
        res['cuf_raw'] = np.zeros((n, 10), dtype='<i4')
        res['cuf_has'] = np.zeros((n, 10), dtype=bool)
        res['e48_fixed'] = []
        res['e18_items'] = []
        res['e28_items'] = []
        res['e20_items'] = []
        res['e68_items'] = []
        res['b18_items'] = []
        res['b30_items'] = []
        res['b0_tags'] = Counter()
        res['b0_tag_rows'] = defaultdict(int)
        res['b0_samples'] = defaultdict(list)
        res['b48_ver'] = Counter()
        res['b48_item_ver'] = Counter()
        res['b48_items'] = []

    mv = memoryview(b)
    for i in range(n):
        o = struct.unpack_from('<I', b, p)[0]; p += 4
        assert o == i, (i, o, p)
        if server:
            res['e120'][i], res['e121'][i], res['e122'][i] = struct.unpack_from('<bbb', b, p); p += 3
            c18 = struct.unpack_from('<H', b, p)[0]; p += 2
            res['e18_cnt'][i] = c18
            if c18:
                for _ in range(c18):
                    res['e18_items'].append((i, struct.unpack_from('<I', b, p)[0])); p += 4
            res['eda_tag'][i], res['eda_b1'][i], res['eda_b2'][i], res['eda_b3'][i], res['eda_b4'][i] = struct.unpack_from('<5B', b, p); p += 5
            res['e123'][i] = struct.unpack_from('<b', b, p)[0]; p += 1
            res['ec0'][i] = struct.unpack_from('<i', b, p)[0]; p += 4
            res['e88_dates'][i] = struct.unpack_from('<6I', b, p); p += 24
            ef = b[p]; p += 1
            res['edates_flag'][i] = ef
            if ef:
                res['ea0_dates'][i] = struct.unpack_from('<6I', b, p); p += 24
            res['ede'][i], res['eb8'][i], res['e125'][i], res['e84'][i], res['e80'][i] = struct.unpack_from('<HIbII', b, p); p += 15
            elf = b[p]; p += 1
            res['elec_flag'][i] = elf
            if elf:
                ec, ed1, ed2, cepr, cetl, cmtm, cect, cemn, cemx = struct.unpack_from('<iIIhbbbbb', b, p); p += 19
                res['elec_club'][i] = ec; res['elec_d1'][i] = ed1; res['elec_d2'][i] = ed2
                res['Cepr'][i] = cepr; res['Cetl'][i] = cetl; res['Cmtm'][i] = cmtm
                res['Cect'][i] = cect; res['Cemn'][i] = cemn; res['Cemx'][i] = cemx
            res['e126'][i], res['e127'][i], res['e128'][i], res['e129'][i], res['e12a'][i] = struct.unpack_from('<5b', b, p); p += 5
            # +0xf8 supporter profile 1
            t = b[p]; p += 1; res['f8_ver'][i] = t
            assert t == 3, ('f8 ver', i, t)
            v0, v4, v6, b8, b9, ba, bb, bc, bd, be, bf, b10, b11, b12, b13 = struct.unpack_from('<ihh12b', b, p); p += 20
            res['f8_CsSF'][i] = v0; res['f8_CsSS'][i] = v4; res['f8_CsST'][i] = v6
            res['Csly'][i] = b8; res['Csps'][i] = b9; res['Cspt'][i] = ba
            res['Csaf'][i] = bb; res['Cste'][i] = bc; res['Cspe'][i] = bd
            res['f8_0e'][i] = be; res['f8_0f'][i] = bf; res['f8_10'][i] = b10
            res['f8_11'][i] = b11; res['f8_12'][i] = b12; res['f8_13'][i] = b13
            # +0x10c supporter profile 2
            t2 = b[p]; p += 1; res['p10c_ver'][i] = t2
            assert t2 == 3, ('p10c ver', i, t2)
            v0, v4, v6, b8, b9, ba, bb, bc, bd = struct.unpack_from('<ihh6b', b, p); p += 20
            res['p10c_00'][i] = v0; res['p10c_04'][i] = v4; res['p10c_06'][i] = v6
            res['p10c_08'][i] = b8; res['p10c_09'][i] = b9; res['p10c_0a'][i] = ba
            res['p10c_0b'][i] = bb; res['p10c_0c'][i] = bc; res['p10c_0d'][i] = bd
            # A & B (cnst, skip)
            ta = b[p]; p += 1; p += (7 if ta > 1 else 6)
            tb = b[p]; p += 1; p += (12 if tb < 2 else 14 if tb == 2 else 15)
            # +bc(4), +c4(4), +c8(4), +12b..+12f(5), +d0(4), +d4(4)
            res['ebc'][i], res['ec4'][i], res['ec8'][i], res['e12b'][i], res['e12c'][i], res['e12d'][i], res['e12e'][i], res['e12f'][i], res['ed0'][i], res['ed4'][i] = struct.unpack_from('<Iiibbbbbii', b, p); p += 25
            # +28 (Cscm): i8 cnt x 22B
            c28 = struct.unpack_from('<b', b, p)[0]; p += 1
            res['e28_cnt'][i] = c28
            for _ in range(c28):
                item = b[p:p+22]; p += 22
                if len(res['e28_items']) < 2000: res['e28_items'].append((i, item.hex()))
            # +20 (INT_DUTY_PLAYER_COUNT): u8 cnt x 10B
            c20 = b[p]; p += 1
            res['e20_cnt'][i] = c20
            for _ in range(c20):
                item = b[p:p+10]; p += 10
                if len(res['e20_items']) < 2000: res['e20_items'].append((i, item.hex()))
            # +48 (UEFA coeff ring buffer)
            f48 = b[p]; p += 1
            res['e48_flag'][i] = f48
            if f48:
                t48 = struct.unpack_from('<b', b, p)[0]; p += 1
                if t48 > 0:
                    w44, b46, b47, d00, d04, d08, d3c, d40 = struct.unpack_from('<HBB5i', b, p); p += 24
                else:
                    w44, b46, b47, d00, d04, d3c = struct.unpack_from('<HBB3i', b, p); p += 16
                    d08 = d40 = -1
                cnt48 = b[p]; p += 1
                res['e48_cnt'][i] = cnt48
                vals48 = list(struct.unpack_from(f'<{cnt48}i', b, p)) if cnt48 else []
                p += 4 * cnt48
                if len(res['e48_fixed']) < 20:
                    res['e48_fixed'].append((i, t48, w44, b46, b47, d00, d04, d08, d3c, d40, cnt48, vals48))
                # Replay ring buffer insertion from 0x39aa1f0:
                # head starts at 0, count starts at 0; push into ring[(head+count)%10] until count==10, then ring[head]=v, head=(head+1)%10
                ring = [0]*10; head = 0; rcnt = 0
                for v in vals48:
                    if rcnt < 10:
                        ring[(head + rcnt) % 10] = v
                        rcnt += 1
                    else:
                        ring[head] = v
                        head = (head + 1) % 10
                res['e48_head'][i] = head
                for slot in range(10):
                    if slot < rcnt:
                        rv = ring[(head + slot) % 10]
                        res['cuf_raw'][i, slot] = rv
                        res['cuf'][i, slot] = np.float32(rv / 1000.0)
                        res['cuf_has'][i, slot] = True
            # zero-count conditional blocks (+30, +38, +70, +50)
            assert b[p:p+7] == b'\x00'*7, ('nonzero 30/38/70/50', i, b[p:p+7].hex())
            p += 7
            # +68 (CPsL): u16 cnt x (1B tag + 10B item)
            c68 = struct.unpack_from('<H', b, p)[0]; p += 2
            res['e68_cnt'][i] = c68
            for _ in range(c68):
                tg = b[p]; it = b[p+1:p+11]; p += 11
                if len(res['e68_items']) < 2000: res['e68_items'].append((i, tg, it.hex()))
            assert b[p] == 0, ('nonzero e40', i, b[p])
            p += 1
            res['edc'][i] = struct.unpack_from('<H', b, p)[0]; p += 2

        # Common tail (both client and server)
        res['d8'][i], res['cc'][i], res['base_ac'][i] = struct.unpack_from('<HIH', b, p); p += 8
        tlen = struct.unpack_from('<I', b, p)[0]; p += 4
        res['tcht_len'][i] = tlen
        if tlen:
            sb = b[p:p+tlen]; p += tlen
            try:
                s = sb.decode('utf-8')
                res['tcht_nonempty'].append((i, s))
            except UnicodeDecodeError:
                res['tcht_bad_utf8'] += 1
        kcnt = b[p]; p += 1
        res['base78_cnt'][i] = kcnt
        for _ in range(kcnt):
            ot = b[p]; p += 1
            assert ot == 1
            # 12B colour block + 14B tail: +18(4B), +1c(4B), +20(2B year), +22(1B kit_type), +23(1B), +24(1B), +25(1B)
            c18, c1c, kyr, b22, b23, b24, b25 = struct.unpack_from('<iiHBBBB', b, p+12)
            p += 26
            res['kit_total'] += 1
            res['kit_types'][b22] += 1
            res['kit_years'][kyr] += 1
            res['kit_b23'][b23] += 1
            res['kit_b24'][b24] += 1
            res['kit_b25'][b25] += 1
            if c18 > 0: res['kit_comp_nz'] += 1
        # base scalars: 0xa0 (ttcl) & 0xa8 (tbcl) — stored as 4B reversed RGBA each (read +a3,+a2,+a1,+a0 then +ab,+aa,+a9,+a8)!
        # Let's unpack raw wire 4 bytes as little-endian u32 AND reconstruct memory dword!
        a3, a2, a1, a0, b3, b2, b1, b0 = b[p:p+8]; p += 8
        res['base_a0'][i] = a0 | (a1 << 8) | (a2 << 16) | (a3 << 24)
        res['base_a8'][i] = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)

        if server:
            # base+0x18 (Cspb): i16 cnt x 20B
            c18b = struct.unpack_from('<h', b, p)[0]; p += 2
            res['b18_cnt'][i] = c18b
            for _ in range(c18b):
                it = b[p:p+20]; p += 20
                if len(res['b18_items']) < 2000: res['b18_items'].append((i, it.hex()))
            # base+0x30 (Cren): i8 cnt x 6B
            c30b = struct.unpack_from('<b', b, p)[0]; p += 1
            res['b30_cnt'][i] = c30b
            for _ in range(c30b):
                it = b[p:p+6]; p += 6
                if len(res['b30_items']) < 2000: res['b30_items'].append((i, it.hex()))
            # base +74..+77 (4B) +68..+70 (12B)
            res['Cpfr'][i], res['C2pf'][i], res['Cdfo'][i], res['Cafo'][i], res['Catd'][i], res['Cmna'][i], res['Cmxa'][i] = struct.unpack_from('<bbbbiii', b, p); p += 16
            # base+0x00 polymorphic virtual dispatch
            cb0 = struct.unpack_from('<H', b, p)[0]; p += 2
            res['b0_cnt'][i] = cb0
            seen_tags = set()
            for _ in range(cb0):
                t = b[p]; p += 1
                res['b0_tags'][t] += 1
                seen_tags.add(t)
                start_p = p
                if t in (4, 5, 6, 7, 37):
                    sz = {4:43, 5:24, 6:19, 7:24, 37:27}[t]
                    p += sz
                elif t == 9:
                    p += 20
                    for _ in range(4):
                        sl = struct.unpack_from('<I', b, p)[0]; p += 4 + sl
                elif t == 16:
                    c16 = struct.unpack_from('<b', b, p)[0]; p += 1 + 4 * c16
                elif t == 38:
                    c38 = struct.unpack_from('<I', b, p)[0]; p += 4
                    for _ in range(c38):
                        p += 1 # ver
                        m38 = struct.unpack_from('<I', b, p)[0]; assert m38 == 0; p += 4
                        p += 14
                        sl = struct.unpack_from('<I', b, p)[0]; p += 4 + sl
                else:
                    raise RuntimeError(('unknown tag', i, t))
                if len(res['b0_samples'][t]) < 5:
                    res['b0_samples'][t].append((i, b[start_p:p].hex()))
            for t in seen_tags: res['b0_tag_rows'][t] += 1
            # base+0x48 (TCrs)
            f48b = b[p]; p += 1
            res['b48_flag'][i] = f48b
            if f48b:
                v48 = struct.unpack_from('<I', b, p)[0]; p += 4
                c48 = struct.unpack_from('<I', b, p)[0]; p += 4
                res['b48_ver'][v48] += 1
                res['b48_cnt'][i] = c48
                for _ in range(c48):
                    iv = struct.unpack_from('<h', b, p)[0]; p += 2
                    res['b48_item_ver'][iv] += 1
                    sz = 8 + (iv >= 2) + (iv >= 3)
                    it = b[p:p+sz]; p += sz
                    if len(res['b48_items']) < 50: res['b48_items'].append((i, iv, it.hex()))
    assert p == len(b), (p, len(b))
    return res

cli = parse_extra3(cli_b, False)
srv = parse_extra3(srv_b, True)
print('=== 3. Byte-exact full-archive replay PASSED (client & server EOF exact) ===')

def summ(name, arr, min_v=None, max_v=None, allowed=None, ctor_def=None):
    uvals, cnts = np.unique(arr, return_counts=True)
    ndist = len(uvals)
    mn, mx = int(uvals[0]), int(uvals[-1])
    z = int(np.count_nonzero(arr == 0))
    m1 = int(np.count_nonzero(arr == -1)) if arr.dtype.kind == 'i' else 0
    ff = int(np.count_nonzero(arr == 0xffffffff)) if arr.dtype == np.dtype('<u4') else 0
    cd = int(np.count_nonzero(arr == ctor_def)) if ctor_def is not None else None
    viol = 0; fce = None
    if min_v is not None or max_v is not None:
        bad = np.zeros(len(arr), dtype=bool)
        if min_v is not None: bad |= (arr < min_v)
        if max_v is not None: bad |= (arr > max_v)
        bidx = np.flatnonzero(bad)
        viol = len(bidx)
        if viol: fce = (int(bidx[0]), int(arr[bidx[0]]))
    elif allowed is not None:
        aset = set(allowed)
        bad = np.array([int(x) not in aset for x in arr])
        bidx = np.flatnonzero(bad)
        viol = len(bidx)
        if viol: fce = (int(bidx[0]), int(arr[bidx[0]]))
    hist_s = dict(zip(uvals.tolist(), cnts.tolist())) if ndist <= 15 else f'<{ndist} distinct>'
    print(f'  {name:18s}: min={mn:10d} max={mx:10d} dist={ndist:6d} zero={z:5d} m1={m1:5d} def({ctor_def})={cd} viol={viol} fce={fce} | {hist_s}')

print('\n=== 4. CLUB+0x100 Server-Only Direct Scalars ===')
summ('Ctlv (+0x120)', srv['e120'], 0, 20, ctor_def=0)
summ('Cmle (+0x121)', srv['e121'], 0, 20, ctor_def=10)
summ('e122 (+0x122)', srv['e122'])
summ('e123 (+0x123)', srv['e123'])
summ('Csth (+0xc0)',  srv['ec0'], 0, 200000, ctor_def=-1)
summ('e125 (+0x125)', srv['e125'])
summ('Cyim (+0x126)', srv['e126'], -1, 20, ctor_def=0)
summ('CScP (+0x127)', srv['e127'], ctor_def=0)
summ('e128 (+0x128)', srv['e128'])
summ('Cown (+0x129)', srv['e129'], ctor_def=0)
summ('Chti (+0x12a)', srv['e12a'], ctor_def=1)
summ('Cyfb (+0x12b)', srv['e12b'], -1, 20, ctor_def=0)
summ('Cytv (+0x12c)', srv['e12c'], -1, 20, ctor_def=10)
summ('Crcb (+0x12d)', srv['e12d'], -1, 20, ctor_def=10)
summ('e12e (+0x12e)', srv['e12e'])
summ('Cels (+0x12f)', srv['e12f'], ctor_def=-1)
summ('ec4  (+0xc4)',  srv['ec4'])
summ('CMwg (+0xc8)',  srv['ec8'], ctor_def=0)
summ('ed0  (+0xd0)',  srv['ed0'])
summ('ed4  (+0xd4)',  srv['ed4'])
summ('ede  (+0xde)',  srv['ede'])
summ('edc  (+0xdc)',  srv['edc'])
summ('eda_tag', srv['eda_tag']); summ('eda_b1', srv['eda_b1']); summ('eda_b2', srv['eda_b2']); summ('eda_b3', srv['eda_b3']); summ('eda_b4', srv['eda_b4'])

print('\n=== 5. CLUB+0x100 Election (+0x78) ===')
el_mask = srv['elec_flag'] == 1
print(f'  election present rows: {int(el_mask.sum())} / {N}')
summ('elec_club(+00)', srv['elec_club'][el_mask], 0, N-1)
v1, s1 = check_date4_arr(srv['elec_d1'][el_mask])
v2, s2 = check_date4_arr(srv['elec_d2'][el_mask])
print(f'  elec_d1 (Cebd): valid={int(v1.sum())}/{int(el_mask.sum())} sentinel1900={int(s1.sum())}')
print(f'  elec_d2 (+0c) : valid={int(v2.sum())}/{int(el_mask.sum())} sentinel1900={int(s2.sum())}')
summ('Cepr (+0x10)', srv['Cepr'][el_mask])
summ('Cetl (+0x12)', srv['Cetl'][el_mask], 0, 100)
summ('Cmtm (+0x13)', srv['Cmtm'][el_mask], 0, 100)
summ('Cect (+0x14)', srv['Cect'][el_mask], 0, 100)
summ('Cemn (+0x15)', srv['Cemn'][el_mask], 0, 100)
summ('Cemx (+0x16)', srv['Cemx'][el_mask], 0, 100)

print('\n=== 6. CLUB+0x100 Supporter Profile (+0xf8 & +0x10c) ===')
summ('f8_CsSF(+00)', srv['f8_CsSF'])
summ('f8_CsSS(+04)', srv['f8_CsSS'])
summ('f8_CsST(+06)', srv['f8_CsST'])
for nm in ['Csly', 'Csps', 'Cspt', 'Csaf', 'Cste', 'Cspe']:
    summ(f'{nm} (+f8)', srv[nm], 0, 20)
for nm in ['f8_0e', 'f8_0f', 'f8_10', 'f8_11', 'f8_12', 'f8_13']:
    summ(nm, srv[nm])
print(f'  +0x10c equals +0xf8 on +00..+0d? 00:{int((srv["p10c_00"]==srv["f8_CsSF"]).sum())} 08:{int((srv["p10c_08"]==srv["Csly"]).sum())}')
summ('p10c_00', srv['p10c_00']); summ('p10c_04', srv['p10c_04']); summ('p10c_08', srv['p10c_08'])

print('\n=== 7. CLUB+0x100 UEFA Coeff Ring (+0x48: Cuf1..9, Cf10) ===')
m48 = srv['e48_flag'] == 1
print(f'  e48 present rows: {int(m48.sum())} / {N}')
summ('e48_cnt', srv['e48_cnt'][m48])
print('  sample e48 fixed (first 5):', srv['e48_fixed'][:5])
for j in range(10):
    nm = f'Cuf{j+1}' if j < 9 else 'Cf10'
    has = srv['cuf_has'][:, j]
    vals = srv['cuf'][has, j]
    raws = srv['cuf_raw'][has, j]
    bad = np.flatnonzero((vals < 0.0) | (vals > 50.0))
    nz = int(np.count_nonzero(raws != 0))
    print(f'  {nm:4s}: populated={int(has.sum()):4d} nz={nz:4d} min={float(vals.min()) if len(vals) else None} max={float(vals.max()) if len(vals) else None} viol(0..50)={len(bad)} fce={(int(np.flatnonzero(has)[bad[0]]), float(vals[bad[0]])) if len(bad) else None}')

print('\n=== 8. CLUB+0x100 Dates (+80..+bc) & Lists (+18, +20, +28, +68) ===')
for nm, arr in [('+80', srv['e80']), ('+84', srv['e84']), ('+b8', srv['eb8']), ('+bc', srv['ebc'])]:
    v, s = check_date4_arr(arr)
    print(f'  date {nm}: valid={int(v.sum())}/{N} sentinel1900={int(s.sum())} non_sentinel={int((~s).sum())} uniq={len(np.unique(arr))}')
for j in range(6):
    v, s = check_date4_arr(srv['e88_dates'][:, j])
    print(f'  date +88[{j}]: valid={int(v.sum())}/{N} sentinel1900={int(s.sum())} non_sentinel={int((~s).sum())}')
print(f'  extra_dates (+a0) flag=1 rows: {int(srv["edates_flag"].sum())}')
summ('e18_cnt (+18)', srv['e18_cnt'])
summ('e20_cnt (+20)', srv['e20_cnt'])
summ('e28_cnt (+28 Cscm)', srv['e28_cnt'])
summ('e68_cnt (+68 CPsL)', srv['e68_cnt'])
print('  sample e18:', srv['e18_items'][:5])
print('  sample e20:', srv['e20_items'][:5])
print('  sample e28 (Cscm):', srv['e28_items'][:5])
print('  sample e68 (CPsL):', srv['e68_items'][:5])

print('\n=== 9. Common Tail (Client vs Server): +cc (TCoi), base+ac, base+98 (TCht), base+78 (kits), base+a0/a8 (ttcl/tbcl) ===')
print(f'  +cc (TCoi): cli_eq_srv={int((cli["cc"]==srv["cc"]).sum())}/{N} all_ffffffff_cli={int((cli["cc"]==0xffffffff).sum())} srv={int((srv["cc"]==0xffffffff).sum())}')
print(f'  base+ac   : cli_eq_srv={int((cli["base_ac"]==srv["base_ac"]).sum())}/{N}')
summ('cli base+ac', cli['base_ac']); summ('srv base+ac', srv['base_ac'])
print(f'  base+98 (TCht): cli_nonempty={len(cli["tcht_nonempty"])} srv_nonempty={len(srv["tcht_nonempty"])} bad_utf8=({cli["tcht_bad_utf8"]},{srv["tcht_bad_utf8"]}) eq={cli["tcht_nonempty"]==srv["tcht_nonempty"]}')
print('    sample TCht:', srv['tcht_nonempty'][:10])
print(f'  base+78 (kits): cli_eq_srv_cnt={int((cli["base78_cnt"]==srv["base78_cnt"]).sum())}/{N} total_kits=({cli["kit_total"]},{srv["kit_total"]}) comp_nz=({cli["kit_comp_nz"]},{srv["kit_comp_nz"]})')
print('    kit_types(b22):', dict(sorted(srv['kit_types'].items())))
print('    kit_years:', dict(sorted(srv['kit_years'].items())[:15]))
print('    kit_b23:', dict(sorted(srv['kit_b23'].items())[:15]))
print('    kit_b24:', dict(sorted(srv['kit_b24'].items())))
print('    kit_b25 (outfield=1/gk=0):', dict(sorted(srv['kit_b25'].items())))
print(f'  base+a0 (ttcl): cli_eq_srv={int((cli["base_a0"]==srv["base_a0"]).sum())}/{N} zero_cli={int((cli["base_a0"]==0).sum())} zero_srv={int((srv["base_a0"]==0).sum())} alpha_ff_srv={int(((srv["base_a0"]>>24)==0xff).sum())}')
print(f'  base+a8 (tbcl): cli_eq_srv={int((cli["base_a8"]==srv["base_a8"]).sum())}/{N} zero_cli={int((cli["base_a8"]==0).sum())} zero_srv={int((srv["base_a8"]==0).sum())} alpha_ff_srv={int(((srv["base_a8"]>>24)==0xff).sum())}')
print(f'  ttcl==tbcl & nz: cli={int(((cli["base_a0"]==cli["base_a8"])&(cli["base_a0"]!=0)).sum())} srv={int(((srv["base_a0"]==srv["base_a8"])&(srv["base_a0"]!=0)).sum())}')
print(f'  ttcl==0 | ttcl==tbcl (triggers kit fallback in 0x3eaca60/0x3eac7e0): srv={int(((srv["base_a0"]==0)|(srv["base_a0"]==srv["base_a8"])).sum())}/{N}')

print('\n=== 10. CLUB+0xb0 Server-Only Tail ===')
summ('Catd (+0x68)', srv['Catd'], 0, 1000000, ctor_def=10000)
summ('Cmna (+0x6c)', srv['Cmna'], 0, 1000000, ctor_def=10000)
summ('Cmxa (+0x70)', srv['Cmxa'], 0, 1000000, ctor_def=10000)
for nm, ek in [('Cpfr','pfms'), ('C2pf','sfms'), ('Cdfo','dfms'), ('Cafo','afms')]:
    allowed = [0] + [int(x['enum']) for x in master['enums'][ek]['values']]
    summ(f'{nm} (allow 0+{ek})', srv[nm], allowed=allowed, ctor_def=0)
summ('b18_cnt (Cspb)', srv['b18_cnt'])
summ('b30_cnt (Cren)', srv['b30_cnt'])
summ('b0_cnt (poly)', srv['b0_cnt'])
print('  base+0x00 polymorphic tags (item_count / row_count):')
for t in sorted(srv['b0_tags']):
    print(f'    tag={t:2d}: items={srv["b0_tags"][t]:6d} rows={srv["b0_tag_rows"][t]:5d} sample={srv["b0_samples"][t][:2]}')
print(f'  base+0x48 (TCrs): flag=1 rows={int(srv["b48_flag"].sum())}/{N} ver={dict(srv["b48_ver"])} item_ver={dict(srv["b48_item_ver"])}')
summ('b48_cnt (TCrs)', srv['b48_cnt'][srv['b48_flag']==1])
print('  sample b18 (Cspb):', srv['b18_items'][:5])
print('  sample b30 (Cren):', srv['b30_items'][:5])
print('  sample b48 (TCrs):', srv['b48_items'][:5])
