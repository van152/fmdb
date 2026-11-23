#!/usr/bin/env python3
"""Commander independent spot for t48 schema v4 (Cafl/Cvfl CLUB_LINK merge).
Does NOT import t48 builder/verify. Re-decodes club_links.dat independently,
checks v3 eight tables verbatim, dual-accounting arithmetic, t44 grades,
CLUB_LINK closure/SHAs vs E84, negatives, nation t46 status.
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
    v4 = json.load(open(ROOT/'reports/club_nation_subtable_schema.json', encoding='utf-8'))
    v3 = json.load(open(ROOT/'scratch/t48/out/club_nation_subtable_schema.v3.json', encoding='utf-8'))
    cov = v4['coverage']

    # 1. v3 eight tables verbatim + baseline snapshot SHA
    ck(v4['schema_version'] == 4, f'schema_version==4 (got {v4["schema_version"]})')
    ck(len(v4['tables']) == 8, f'v4 8 numeric tables (got {len(v4["tables"])})')
    ck(json.dumps(v4['tables'], sort_keys=True) == json.dumps(v3['tables'], sort_keys=True), 'v4 tables == v3 snapshot tables VERBATIM')
    ck(json.dumps(v4['negative_regressions'], sort_keys=True) == json.dumps(v3['negative_regressions'], sort_keys=True), 'v4 negative_regressions == v3 VERBATIM')
    vb = v4['v3_baseline']
    ck(H((ROOT/vb['json_path']).read_bytes()) == vb['json_sha256'], f'v3 snapshot JSON SHA matches v3_baseline {vb["json_sha256"][:16]}')
    ck(v3['coverage']['club_L3_fields'] == 52, 'v3 snapshot club_L3_fields==52')

    # 2. dual-accounting arithmetic
    ck(cov['club_L3_fields'] == 52, f'club_L3_fields==52 (v3 retained)')
    ck(cov['club_L3_occurrences'] == 94 == 52+26+16, f'club_L3_occurrences==94==52+26+16 (got {cov["club_L3_occurrences"]})')
    ck(cov['club_L3_unique_wire_fields'] == 59 == 52+7, f'club_L3_unique_wire_fields==59==52+7 (got {cov["club_L3_unique_wire_fields"]})')
    ck(cov['held_fields'] == 21 == 16+3+2, f'held_fields==21==16+3+2 (got {cov["held_fields"]})')
    ck(cov['held_fields_v3_numeric_tables'] == 16 and cov['held_occurrences_added_t44'] == 5, 'held v3 16 + t44 5')
    ck(cov['held_unique_candidate_wire_slots_t44'] == 3, 't44 unique held wire slots==3 (type/yfee/msls)')
    ck(cov['negative_regressions'] == 4 and len(v4['negative_regressions']) == 4, 'negative_regressions==4')
    ck(cov['L4'] == 0, 'L4==0')
    ck(cov['club_auxiliary_sources'] == 1 and cov['club_auxiliary_views'] == 2, 'auxiliary sources1/views2 (Cafl+Cvfl)')
    ck(cov['runtime_only_no_wire_slot_occurrences'] == 1, 'runtime_only_no_wire_slot==1 (Cvfl.clfr excluded)')
    g = cov['t44_occurrence_grade_counts']
    ck(g['Cafl'] == {'L3': 26, 'held_all_missing': 1, 'held_domain_conflict': 2}, f'Cafl grades 26/1/1... {g["Cafl"]}')
    ck(g['Cvfl'] == {'L3': 16, 'held_domain_conflict': 2, 'runtime_only_no_wire_slot': 1}, f'Cvfl grades {g["Cvfl"]}')
    ck(cov['t44_unique_wire_slot_count'] == 7, 't44 unique wire slot count==7')
    dap = cov['dual_accounting_policy']
    ck('clfr' in dap['club_L3_unique_wire_fields'].lower() or 'clfr' in dap['club_L3_unique_wire_fields'], 'unique-wire policy excludes clfr')
    ck('20 bool' in dap['club_L3_unique_wire_fields'] and 'one u32' in dap['club_L3_unique_wire_fields'], '20 bool share one u32 wire word')
    ck('affl' in dap['club_L3_unique_wire_fields'] and 'ismc' in dap['club_L3_unique_wire_fields'], 'affl/ismc share endpoint lanes no extra slot')

    # 3. CLUB_LINK auxiliary source closure/SHAs vs E84
    aux = v4['club_auxiliary_sources']
    ck(len(aux) == 1 and aux[0]['source_id'] == 'CLUB_LINK', 'one CLUB_LINK auxiliary source')
    a = aux[0]
    ck(a['source_kind'] == 'named_auxiliary_pod' and a['table_type'] is None and a['factory_case'] is None, 'CLUB_LINK named POD, no numeric table_type/factory case')
    ck(a['member'] == 'server_db/club_links.dat', 'member server_db/club_links.dat')
    sp = a['server_payload']
    ck(sp['row_count'] == 9261 and sp['row_stride_bytes'] == 47 and sp['payload_bytes'] == 435279, 'CLUB_LINK 9261x47=435279')
    ck(sp['closure_formula'] == '12 + 9261 * 47 + 0 = 435279' and sp['closure_ok'] and 12+9261*47+0 == 435279, 'closure 12+9261*47+0==435279 ok')
    ck(sp['header_bytes'] == 12 and sp['count_offset'] == 8 and sp['count_value'] == 9261 and sp['footer_bytes'] == 0, 'header12/count@8=9261/footer0')
    ck(sp['payload_sha256'] == '8933328064b13a9d8dc153dd5b455970a7c28ada1e24f4ecc9df35735f42f3d2', 'CLUB_LINK payload SHA 89333280 (E84)')
    ck(sp['row_block_sha256'] == '17a167f0bb5945c19eacaf3a7884ea3c14b29eb4185aaf533e57f9a7ce89e75c', 'row_block SHA 17a167f0 (E84)')
    ck(sp['compressed_region_sha256'] == '894f1efb9caf18482402198ed19294d04725a583ca262a6a01b2ed95c2222fe0' and sp['packed_bytes'] == 63944, 'compressed SHA 894f1efb/packed63944 (E84)')

    # 4. INDEPENDENT re-decode of club_links.dat from archive
    ind = runpy.run_path(str(CODEC))
    z = ind['_zstd_module']()
    _, blob, d = ind['_entries'](DATA/'server_db.dat')
    base = d['data_base']
    e = [x for x in d['entries'] if x['path'].endswith('/club_links.dat')][0]
    st = base + e['offset']; part = blob[st:st+e['packed_size']]
    out = z.ZstdDecompressor().decompressobj().decompress(part)
    ck(len(out) == 435279 == e['size'], f'independent club_links payload 435279 (got {len(out)})')
    ck(H(out) == sp['payload_sha256'], f'independent payload SHA matches v4/E84 {H(out)[:16]}')
    ck(H(part) == sp['compressed_region_sha256'], f'independent compressed region SHA matches {H(part)[:16]}')
    ck(out[:8] == bytes.fromhex('03017461642ef10d') and struct.unpack_from('<I', out, 8)[0] == 9261, 'independent tad shell + u32 count@8==9261')
    ck(H(out[12:12+9261*47]) == sp['row_block_sha256'], f'independent row_block SHA matches {H(out[12:12+9261*47])[:16]}')
    ck(12 + 9261*47 == len(out), 'independent closure header12+rows==payload_len (footer0)')

    # 5. nation t46 data-side status folded
    ns = cov['nation_side']
    ck(ns['summary']['new_L3_claims'] == 0 and ns['summary']['L4'] == 0, 'nation_side new_L3=0/L4=0 (v4 scope pre-t47)')
    t46 = ns['t46_data_side_status']
    ck(t46['server_table_10_rows'] == 251 and t46['server_payload_sha256'] == '19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f', 't46 server t10 251 rows SHA 19337841 folded')
    ck(t46['A_B_C_D_internal_grammar'] == 'open' and t46['new_L3_claims'] == 0, 't46 A_B_C_D grammar open, L3=0')

    # 6. builder selftest + independent verify + anchors
    rb = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scratch/t48/out/consolidate_v4.py'), '--selftest'],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rb.returncode == 0 and 'SELFTEST PASS' in rb.stdout, f'consolidate_v4 --selftest PASS rc0 (rc={rb.returncode})')
    rv = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scratch/t48/out/verify.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rv.returncode == 0 and 'VERIFY PASS' in rv.stdout, f't48 verify.py PASS rc0 (rc={rv.returncode})')
    ra = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t01_anchors.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(ra.returncode == 0 and '7/7' in ra.stdout, f't01_anchors 7/7 (rc={ra.returncode})')

    print(f'\n=== t48 spot: {PASS}/{PASS+FAIL} ===')
    return 0 if FAIL == 0 else 1

if __name__ == '__main__':
    sys.exit(main())