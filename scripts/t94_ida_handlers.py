"""t94 — decompile all DATABASE_TABLE handlers from t14 census via IDA 9.4 idalib.

Static-only (tools-inventory authorized): opens editor.exe with auto-analysis
disabled, builds each handler function from PE unwind bounds, decompiles with
Hex-Rays, writes scratch/t94/out/decompiled/function_<va>.c.

Usage:
  py -V:3.12 -I -B scripts/t94_ida_handlers.py --selftest
  py -V:3.12 -I -B scripts/t94_ida_handlers.py            # full run (74 targets)
Exit codes: 0 ok, 1 partial/misses, 2 bad usage.
"""
import argparse
import json
import sys
import traceback
from pathlib import Path

IDA_LIB = r'C:\Program Files\IDA Professional 9.4\idalib\python'
CENSUS = 'scratch/t14/out/census.json'


def load_targets(census_path):
    d = json.loads(Path(census_path).read_text(encoding='utf-8'))
    out = []
    for tt in d['tables']:
        out.append({
            'table_type': tt.get('table_type'),
            'status': tt.get('status'),
            'handler_off': int(tt['handler_off'], 16),
            'vtable_va': [int(v, 16) for v in
                          [x.get('vtable_va', '0') for x in tt.get('vtables', [])]],
        })
    return out


def main():
    ap = argparse.ArgumentParser(description='Decompile t14 census table handlers via idalib.')
    ap.add_argument('--census', default=CENSUS)
    ap.add_argument('--pe', default=r'D:/tmp2b/fm24/input/editor.exe')
    ap.add_argument('--out', default='scratch/t94/out')
    ap.add_argument('--limit', type=int, default=0, help='only first N targets (debug)')
    ap.add_argument('--selftest', action='store_true',
                    help='no IDA: check census parse + unwind hits for VA interpretation')
    args = ap.parse_args()

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import t94_focus_disasm as fd
    fd.set_pe(args.pe)
    targets = load_targets(args.census)
    if args.selftest:
        base = fd.IMAGE_BASE
        hit_va = sum(1 for t in targets for v in t['vtable_va'] if fd.owner(v))
        hit_rva = sum(1 for t in targets if fd.owner(base + t['handler_off']))
        hit_abs = sum(1 for t in targets if fd.owner(t['handler_off']))
        n_vt = sum(len(t['vtable_va']) for t in targets)
        print('targets=%d vtables=%d owner(vtable_va)=%d/%d' %
              (len(targets), n_vt, hit_va, n_vt))
        print('handler_off as RVA: %d/%d ; as absolute VA: %d/%d' %
              (hit_rva, len(targets), hit_abs, len(targets)))
        return 0 if hit_va and (hit_rva or hit_abs) else 1

    out = Path(args.out)
    (out / 'decompiled').mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, IDA_LIB)
    import idapro  # noqa: E402
    import ida_auto  # noqa: E402
    import ida_funcs  # noqa: E402
    import ida_hexrays  # noqa: E402
    import ida_ua  # noqa: E402
    import idautils  # noqa: E402

    base = fd.IMAGE_BASE
    todo = targets if args.limit <= 0 else targets[:args.limit]
    print('opening', args.pe, 'targets', len(todo), flush=True)
    rc = idapro.open_database(args.pe, False,
                              '-o' + str((out / 'ida_tmp.i64').resolve()) + ' -a-')
    print('open rc', rc, flush=True)
    if rc:
        return 2
    ida_auto.enable_auto(False)
    hexrays = ida_hexrays.init_hexrays_plugin()
    print('Hex-Rays', hexrays, flush=True)
    results, misses = [], []
    for t in todo:
        va = base + t['handler_off']
        rec = fd.owner(va)
        if not rec:
            misses.append({'table_type': t['table_type'], 'va': hex(va), 'why': 'no unwind record'})
            continue
        start, end = rec[0] + base, rec[1] + base
        ea = start
        while ea < end:
            size = ida_ua.create_insn(ea)
            ea += size or 1
        if ida_funcs.get_func(start) is None:
            ida_funcs.add_func(start, end)
        ida_auto.enable_auto(True)
        ida_auto.plan_and_wait(start, end)
        ida_auto.enable_auto(False)
        r = {'table_type': t['table_type'], 'status': t['status'],
             'va': hex(start), 'end': hex(end)}
        try:
            cfunc = ida_hexrays.decompile(start, flags=ida_hexrays.DECOMP_NO_WAIT)
            text = str(cfunc) if cfunc else 'Decompilation returned None'
        except Exception:
            text = traceback.format_exc()
            r['error'] = True
        (out / 'decompiled' / ('tt%03d_%x.c' % (t['table_type'], start))).write_text(
            text, encoding='utf8')
        r['xrefs_in'] = len(list(idautils.XrefsTo(start)))
        results.append(r)
        print('tt%-3d %s-%s len=%d' % (t['table_type'], hex(start), hex(end), len(text)), flush=True)
    idapro.close_database(False)
    summary = {'decompiled': len(results), 'misses': misses,
               'hexrays': bool(hexrays), 'targets': len(todo)}
    (out / 'summary.json').write_text(json.dumps(summary, indent=1), encoding='utf8')
    print('SUMMARY', json.dumps(summary), flush=True)
    return 0 if not misses else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--selftest' in a:
        sys.exit(main())
    sys.exit(main())
