#!/usr/bin/env python3
"""Commander independent spot for t43 fm24_dump.load_payload data_base integration (E80 fix).
Does NOT import t43 verify/builder. Cross-checks fm24_dump.load_payload against t38
load_payload_mf AND an independent size-select decode over the full numbered-table census.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import runpy
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
    fd = runpy.run_path(str(ROOT/'scripts/fm24_dump.py'))
    codec = fd['_reader']()
    lp = fd['load_payload']
    mf = runpy.run_path(str(ROOT/'scripts/t38_multiframe.py'))
    lpmf = mf['load_payload_mf']
    independent = runpy.run_path(str(CODEC))
    z = independent['_zstd_module']()

    # 1. selftest 50/0/0
    r = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/fm24_dump.py'), '--selftest'],
                       capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    line = [l for l in r.stdout.splitlines() if 'fixed' in l and 'PASS' in l]
    ck(r.returncode == 0 and line and '50 PASS / 0 FAIL / 0 SKIP' in line[-1],
       f'fm24_dump --selftest 50 PASS/0 FAIL/0 SKIP (rc={r.returncode}) {line[-1] if line else ""}')

    # 2. full numbered-table census: fm24_dump == t38 mf == independent size-select
    total = identical_mf = identical_ind = len_ok = 0
    affected = []
    canon = {}
    for archive in ('client', 'server', 'lang_update'):
        p = DATA/f'{archive}_db.dat'
        if not p.exists():
            continue
        _, blob, d = independent['_entries'](p)
        base = d['data_base']
        ents = d['entries']
        # predecessor packed_size for affected predicate
        by_off = sorted(ents, key=lambda e: e['offset'])
        prev = {}
        for i, e in enumerate(by_off):
            prev[e['path']] = by_off[i-1]['packed_size'] if i > 0 else None
        # affected predicate over ALL members (incl lang_update 8_N.dat / named)
        for e in ents:
            pp = prev.get(e['path'])
            if pp is not None and pp < base:
                affected.append((archive, e['path'], e['size'], pp, base, e['offset'], e['packed_size']))
        for e in ents:
            m = re.search(r'/table_(\d+)\.dat$', e['path'])
            if not m:
                continue
            tid = int(m.group(1))
            total += 1
            a = base + e['offset']; b = a + e['packed_size']
            size = e['size']
            # independent size-select within member
            part = blob[a:b]
            raw_ind = None
            pos = 0
            while pos + 4 <= len(part) and part[pos:pos+4] == bytes.fromhex('28b52ffd'):
                obj = z.ZstdDecompressor().decompressobj()
                out = obj.decompress(part[pos:])
                if len(out) == size:
                    raw_ind = out; break
                consumed = (len(part)-pos) - len(obj.unused_data)
                if not obj.eof or consumed <= 0: break
                pos += consumed
            try:
                raw_fd = lp(codec, archive, tid)
            except Exception as ex:
                ck(False, f'{archive} table_{tid} fm24_dump raised {ex}')
                continue
            try:
                raw_mf = lpmf(codec, archive, tid)
            except Exception:
                raw_mf = None
            if len(raw_fd) == size: len_ok += 1
            if raw_mf is not None and raw_fd == raw_mf: identical_mf += 1
            if raw_ind is not None and raw_fd == raw_ind: identical_ind += 1
            if (archive, tid) in (('server',34),('server',59),('server',10),('client',10)):
                canon[(archive,tid)] = (len(raw_fd), H(raw_fd)[:16])

    ck(total > 0, f'numbered-table census total {total}')
    ck(len_ok == total, f'all {total} fm24_dump payloads len==entry.size ({len_ok})')
    ck(identical_mf == total, f'fm24_dump == t38 load_payload_mf byte-identical {identical_mf}/{total}')
    ck(identical_ind == total, f'fm24_dump == independent size-select decode {identical_ind}/{total}')

    # 3. canonical anchors
    ck(canon.get(('server',34)) == (313082, 'a07b2bb76fb8796b'), f'server34 313082/a07b2bb7 (E80 stub fixed) {canon.get(("server",34))}')
    ck(canon.get(('server',59)) == (224880, '7eee0ecc59ee306a'), f'server59 224880/7eee0ecc {canon.get(("server",59))}')
    ck(canon.get(('server',10)) == (422345, '19337841e40d0128'), f'server10 422345/19337841 {canon.get(("server",10))}')
    ck(canon.get(('client',10)) == (24732, '7e9d740b9ee69009'), f'client10 24732/7e9d740b {canon.get(("client",10))}')

    # 4. affected predicate: predecessor packed_size < data_base(34)
    ck(len(affected) == 119, f'affected entries (pred packed_size<34) == 119 (got {len(affected)})')
    per = {}
    for a, pth, size, pp, base, off, psz in affected:
        per[a] = per.get(a, 0) + 1
    ck(per == {'server': 2, 'lang_update': 117}, f'affected per_archive server2/lang117 {per}')
    # affected sample: independent member-bounded decode len==size (covers lang_update named members)
    aff_ok = True
    for a, pth, size, pp, base, off, psz in affected[:25]:
        _, blob, d = independent['_entries'](DATA/f'{a}_db.dat')
        st = base + off; part = blob[st:st+psz]
        out = None; pos = 0
        while pos + 4 <= len(part) and part[pos:pos+4] == bytes.fromhex('28b52ffd'):
            obj = z.ZstdDecompressor().decompressobj(); o = obj.decompress(part[pos:])
            if len(o) == size: out = o; break
            consumed = (len(part)-pos) - len(obj.unused_data)
            if not obj.eof or consumed <= 0: break
            pos += consumed
        if out is None or len(out) != size: aff_ok = False
    ck(aff_ok, 'affected sample (25) independent member-bounded decode len==size')

    # 5. anchors + t38 regression
    ra = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t01_anchors.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(ra.returncode == 0 and '7/7' in ra.stdout, f't01_anchors 7/7 (rc={ra.returncode})')

    print(f'\n=== t43 spot: {PASS}/{PASS+FAIL} ===')
    return 0 if FAIL == 0 else 1

if __name__ == '__main__':
    sys.exit(main())