"""Probe: run t96c trace_table on the 11 failing pairs, dump JSON per pair."""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))

import t96c_unicorn_master as M  # noqa: E402

TARGETS = [
    ("server", 0), ("client", 0),
    ("server", 3), ("client", 3),
    ("server", 32),
    ("server", 36),
    ("server", 41),
    ("server", 45),
    ("server", 48),
    ("server", 71),
    ("server", 72),
]

OUT = ROOT / "scratch/t111/probe"


def main():
    want = sys.argv[1:] if len(sys.argv) > 1 else None
    ut, emu, db_a3_ptr = M.setup_emulator()
    vt_fallback = M.load_vtable_fallback()
    tables = {a: {} for a in ("server", "client")}
    for arch, tid, payload in M.load_all_numbered_tables():
        tables[arch][tid] = payload

    for arch, tid in TARGETS:
        if want and f"{arch}/{tid}" not in want:
            continue
        payload = tables[arch][tid]
        t0 = time.time()
        r = M.trace_table(ut, emu, db_a3_ptr, vt_fallback, arch, tid, payload, full_limit=1500, sample_rows=50)
        dt = round(time.time() - t0, 1)
        tag = "CLOSED" if r["closed_to_footer"] else ("OK" if r["rows_ok"] == r["rows_target"] and r["rows_ok"] > 0 else "FAIL")
        print(f"BASE {arch:6s}/t{tid:<2d} {r['class'][:30]:30s} {tag:6s} rows={r['rows_ok']}/{r['rows_header']} diff={r['diff_bytes']} {dt}s :: {r['error'] or ''}", flush=True)
        print(f"     flags={r['flags_seen']} vt={r['vtables_seen'][:4]}", flush=True)
        if r["error"] and r["row0_reads"]:
            print(f"     last_reads={r['row0_reads'][-3:]}", flush=True)
        (OUT / f"base_{arch}_t{tid}.json").write_text(
            json.dumps({k: v for k, v in r.items() if k != "_row_lens_all"}, indent=1, ensure_ascii=False),
            encoding="utf-8",
        )


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
