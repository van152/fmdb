#!/usr/bin/env python3
"""Commander independent spot for t47 nation unknown item-bearing parent discovery.
Does NOT import t47 builder/verify. Re-decodes table_10/9 payloads via codec size-select,
independently re-derives row framing/identity/footer closure, extracts ALL Ntxr tax items
and validates wire field offsets/domains/grades/held counterexamples, t37 baseline SHA.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path('D:/tmp2b/fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
CODEC = ROOT.parent/'fm24/scripts/modding_read_dbdat.py'
ENV = dict(os.environ, FM24_DB_DIR=str(DATA))
PASS = FAIL = 0

def ck(ok, msg):
    global PASS, FAIL
    if ok: PASS += 1; print(f'[PASS] {msg}')
    else: FAIL += 1; print(f'[FAIL] {msg}')

def H(b): return sha256(b).hexdigest()

def main():
    ind = runpy.run_path(str(CODEC))
    z = ind['_zstd_module']()
    disc = json.load(open(ROOT/'scratch/t47/out/discovery_nation_unknown.json', encoding='utf-8'))
    cur = json.load(open(ROOT/'scratch/t47/out/cursor_nation_tax.json', encoding='utf-8'))
    fld = json.load(open(ROOT/'scratch/t47/out/fields_nation_tax.json', encoding='utf-8'))

    def payload(archive, member):
        _, blob, d = ind['_entries'](DATA/f'{archive}_db.dat')
        base = d['data_base']
        es = [e for e in d['entries'] if e['path'].endswith('/'+member)]
        if not es: return None, None, None
        e = es[0]
        st = base + e['offset']; part = blob[st:st+e['packed_size']]
        obj = z.ZstdDecompressor().decompressobj(); out = obj.decompress(part)
        if len(out) != e['size']:
            pos = 0; out = None
            while pos+4 <= len(part) and part[pos:pos+4] == bytes.fromhex('28b52ffd'):
                o2 = z.ZstdDecompressor().decompressobj(); r = o2.decompress(part[pos:])
                if len(r) == e['size']: out = r; break
                consumed = (len(part)-pos)-len(o2.unused_data)
                if not o2.eof or consumed <= 0: break
                pos += consumed
        return out, e, base

    # 1. independent payload decode + canonical anchors
    srv, se, _ = payload('server', 'table_10.dat')
    cli, ce, _ = payload('client', 'table_10.dat')
    ck(srv is not None and len(srv) == 422345, f'server t10 payload 422345 (got {len(srv) if srv else None})')
    ck(cli is not None and len(cli) == 24732, f'client t10 payload 24732 (got {len(cli) if cli else None})')
    ck(H(srv) == '19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f', f'server t10 SHA 19337841 {H(srv)[:16]}')
    ck(H(cli) == '7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34', f'client t10 SHA 7e9d740b {H(cli)[:16]}')
    ck(se['offset']+34 == 8529015 and ce['offset']+34 == 5128013, f'E80 member start data_base+offset srv{se["offset"]+34}/cli{ce["offset"]+34}')

    # 2. row framing / identity / closure independently from cursor rows
    for arch, pay, mode, sigma, tot in (('server', srv, 1, 422323, 422345), ('client', cli, 0, 24710, 24732)):
        rows = cur[arch]['rows']
        ck(cur[arch]['mode'] == mode, f'{arch} mode=={mode}')
        ck(len(rows) == 251, f'{arch} 251 rows (got {len(rows)})')
        ck(rows[0]['wire13'] == 13, f'{arch} first wire13==13')
        contig = all(rows[i]['end'] == rows[i+1]['wire13'] for i in range(len(rows)-1))
        ck(contig, f'{arch} rows contiguous end[i]==wire13[i+1]')
        idok = all(r['identity_at'] == r['end']-12 and r['identity'][0] == r['row']
                   and r['identity'][1] == r['identity'][2] for r in rows)
        ck(idok, f'{arch} identity_at==end-12, ordinal==row, repeated lanes equal')
        sl = sum(r['length'] for r in rows)
        ck(sl == sigma, f'{arch} sum row_len=={sigma} (got {sl})')
        ck(13+sl+9 == tot and rows[-1]['end']+9 == tot, f'{arch} closure 13+{sl}+9=={tot}')
        # footer: u32 count0 | u8 flag1 | u32 max identity
        le = rows[-1]['end']
        fcnt = struct.unpack_from('<I', pay, le)[0]
        fflag = pay[le+4]
        fval = struct.unpack_from('<I', pay, le+5)[0]
        maxid = max(r['identity'][1] for r in rows)
        ck(fcnt == 0 and fflag == 1 and fval == maxid, f'{arch} footer count0/flag1/maxid {fcnt}/{fflag}/{fval}=={maxid}')

    # 3. Ntxr tax items: independent extraction + wire field domains
    WIRE = {'lowa': (1, '<i'), 'uppa': (5, '<i'), 'capa': (9, '<i'), 'year': (13, '<H'),
            'ppty': (15, '<b'), 'txty': (16, '<b'), 'perc': (17, '<f'), 'fram': (21, '<b'), 'leve': (22, '<b')}
    rows = cur['server']['rows']
    items = 0; taxrows = 0; zerorows = 0; firstzero = None
    dom = {k: [] for k in WIRE}
    fram_missing = leve_neg = ppty_zero = 0
    fram_live = set(); leve_live = set(); ppty_raw = set(); txty_raw = set()
    tagok = lenok = cntok = True
    for r in rows:
        tx = r['tax']
        if tx is None:
            continue
        cp, cnt, s, e = tx
        if cnt == 0:
            zerorows += 1
            if firstzero is None: firstzero = r['row']
            continue
        taxrows += 1
        region = srv[s:e]
        if len(region) != cnt*25: lenok = False
        if struct.unpack_from('<i', srv, cp)[0] != cnt: cntok = False
        for j in range(cnt):
            it = region[j*25:(j+1)*25]
            if it[0] != 2: tagok = False
            items += 1
            for k, (off, fmt) in WIRE.items():
                v = struct.unpack_from(fmt, it, off)[0]
                dom[k].append(v)
            fr = dom['fram'][-1]; lv = dom['leve'][-1]; pp = dom['ppty'][-1]; tt = dom['txty'][-1]
            if fr <= 0: fram_missing += 1
            else: fram_live.add(fr)
            if lv == -1: leve_neg += 1
            else: leve_live.add(lv)
            if pp == 0: ppty_zero += 1
            ppty_raw.add(pp); txty_raw.add(tt)
    ck(tagok, 'all tax item tag byte==2')
    ck(lenok, 'all tax regions len==count*25')
    ck(cntok, 'all tax i32 count@count_pos matches cursor count')
    ck(items == 1899, f'total tax items 1899 (got {items})')
    ck(taxrows == 221, f'tax-bearing rows 221 (got {taxrows})')
    ck(zerorows == 30, f'zero-tax rows 30 (got {zerorows})')
    ck(firstzero == 31, f'first zero-tax row 31 (got {firstzero})')
    ck(all(t is None for t in (r['tax'] for r in cur['client']['rows'])), 'client rows all tax==null (mode0 bypass)')
    # domains
    ck(min(dom['lowa']) >= 0 and max(dom['lowa']) == 11037528, f'lowa 0..11037528 (got {min(dom["lowa"])}..{max(dom["lowa"])})')
    ck(min(dom['uppa']) >= 0 and max(dom['uppa']) == 11037527, f'uppa 0..11037527 (got {min(dom["uppa"])}..{max(dom["uppa"])})')
    ck(min(dom['capa']) >= 0 and max(dom['capa']) == 132334, f'capa 0..132334 (got {min(dom["capa"])}..{max(dom["capa"])})')
    ck(min(dom['year']) == 1900 and max(dom['year']) == 2028, f'year 1900..2028 (got {min(dom["year"])}..{max(dom["year"])})')
    ck(min(dom['perc']) >= 0 and max(dom['perc']) == 60.0, f'perc f32 0..60 (got {min(dom["perc"])}..{max(dom["perc"])})')
    ck(fram_live <= {1, 2, 3, 4, 5} and fram_missing == 1842, f'fram live1..5 missing1842 (live{sorted(fram_live)} miss{fram_missing})')
    ck(leve_live <= {0, 1, 2, 3, 4, 5} and leve_neg == 1880, f'leve live0..5 neg1880 (live{sorted(leve_live)} neg{leve_neg})')
    ck(ppty_raw <= {0, 1, 2, 3, 4, 5} and ppty_zero == 99, f'ppty raw0..5 zeros99 (raw{sorted(ppty_raw)} z{ppty_zero})')
    ck(txty_raw <= set(range(1, 12)), f'txty raw1..11 (got {sorted(txty_raw)})')

    # 4. held first counterexamples (absolute payload offsets)
    ck(srv[29265] == 0, f'ppty held row48@29265==0 (got {srv[29265]})')
    ck(srv[70] == 4, f'txty held row0@70==4 (got {srv[70]})')
    ck(srv[75] == 0, f'fram row0@75==0 (got {srv[75]})')
    ck(struct.unpack_from('<b', srv, 76)[0] == -1, f'leve row0@76==-1 (got {srv[76]})')

    # 5. t9 / table_extra_9 member sizes + header count (NOT wire-closed by t47)
    for arch, t9sz, ex9sz in (('client', 31956, 83927), ('server', 307564, 105228)):
        p9, e9, _ = payload(arch, 'table_9.dat')
        px, ex, _ = payload(arch, 'table_extra_9.dat')
        ck(p9 is not None and len(p9) == t9sz, f'{arch} table_9 size {t9sz} (got {len(p9) if p9 else None})')
        ck(px is not None and len(px) == ex9sz, f'{arch} table_extra_9 size {ex9sz} (got {len(px) if px else None})')
        ck(p9 is not None and p9[:8] == bytes.fromhex('03017461642ef10d') and struct.unpack_from('<I', p9, 8)[0] == 251, f'{arch} table_9 tad shell + u32 count@8==251')
        ck(px is not None and px[:8] == bytes.fromhex('03017461642ef10d') and struct.unpack_from('<I', px, 8)[0] == 251, f'{arch} table_extra_9 tad shell + u32 count@8==251')
    pex10, _, _ = payload('server', 'table_extra_10.dat')
    ck(pex10 is None, 'table_extra_10 absent both archives')

    # 6. t37 baseline preserved verbatim
    prov = disc['provenance']
    bu = prov['baseline_unchanged']
    for rel, want in bu.items():
        got = H((ROOT/rel).read_bytes())
        ck(got == want, f't37 baseline {rel} SHA preserved {got[:16]}')
    ck(H((ROOT.parent/'fm24/input/editor.exe').read_bytes()) == prov['editor_sha256'], 'editor.exe SHA b82ebe8e (read-only)')
    ck(H((ROOT/'evidence/fm24/reports/editor_schema/master.json').read_bytes()) == prov['frozen_snapshots']['evidence/fm24/reports/editor_schema/master.json'], 'frozen master SHA 7d57477e')

    # 7. discovery accounting + Ntxr detail + extents/factory
    ck(disc['status'] == 'partial_static_discovery', f'status partial_static_discovery')
    ck(disc['closed_parents'] == 1 and disc['new_L3'] == 7, f'closed_parents1/new_L3 7')
    ck(disc['static_inline_links'] == 9 and disc['unknown_links'] == 6, f'static_inline9/unknown6')
    ck(disc['L4'] == 0, 'L4==0')
    nt = disc['parents']['Ntxr']
    ck(nt['status'] == 'cursor_closed' and nt['item_count'] == 1899 and nt['persisted_item_stride'] == [23, 25], 'Ntxr cursor_closed/1899/[23,25]')
    ck(nt['independent_list_table'] is None and nt['owner_type'] == 10, 'Ntxr no independent list table, owner10')
    ck(nt['schema_index'] == 232 and len(nt['schema']['list_item_fields']) == 9, 'Ntxr schema idx232 9 item fields')
    inline = [k for k, v in disc['parents'].items() if v['status'] == 'inline_static_reader_link_archive_replay_open']
    partial = [k for k, v in disc['parents'].items() if v['status'] == 'partial']
    ck(len(inline) == 8 and all(disc['parents'][k]['owner_type'] == 9 for k in inline), f'8 inline owner9 {inline}')
    ck(len(partial) == 6 and set(partial) == {'Nftb', 'EDfx', 'EDsc', 'Nrvn', 'Calt', 'TCrs'}, f'6 unknown partial {partial}')
    ex = disc['extents']
    ck(ex['17038016']['reachable'] == 992 and ex['17038016']['external_edges'] == [], 'NATION reader extent 992 reachable no external edges')
    ck(ex['69257456']['reachable'] == 111 and ex['69257456']['external_edges'] == [], 'tax helper extent 111 reachable no external edges')
    ck(disc['factory']['9']['rtti'] == '.?AVNATIONAL_TEAM_CONTAINER@db@@', 'factory cell9 RTTI NATIONAL_TEAM_CONTAINER')
    ck(fld['L3'] == 7 and fld['L4'] == 0 and len(fld['fields']) == 9, 'fields L3=7/L4=0/9 names')

    # 8. builder selftest + verify + anchors
    rb = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t47_nation_unknown.py'), '--selftest'],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rb.returncode == 0, f't47 builder --selftest rc0 (rc={rb.returncode}) {rb.stdout.strip().splitlines()[-1] if rb.stdout.strip() else rb.stderr.strip()[-120:]}')
    rv = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scratch/t47/out/verify.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rv.returncode == 0, f't47 verify.py rc0 (rc={rv.returncode}) {rv.stdout.strip().splitlines()[-1] if rv.stdout.strip() else rv.stderr.strip()[-120:]}')
    ra = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t01_anchors.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(ra.returncode == 0 and '7/7' in ra.stdout, f't01_anchors 7/7 (rc={ra.returncode})')

    print(f'\n=== t47 spot: {PASS}/{PASS+FAIL} ===')
    return 0 if FAIL == 0 else 1

if __name__ == '__main__':
    sys.exit(main())