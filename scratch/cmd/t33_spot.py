# -*- coding: utf-8 -*-
"""t33_spot.py — commander independent check of devseek t33 profile batch II.
Verifies 7 tables: multi-frame payload size+SHA, fixed-table closure arithmetic,
rows_jsonl line count == claimed count, rows hash. Variable tables: payload+rows
integrity (closure equation re-checked arithmetically). L2 data-side, no L3.
"""
import sys, os, json, hashlib, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, DB_DIR, MAGIC
import zstandard

OUT = Path("D:/tmp2b/fm24-db/scratch/t33/out")

def frames_payload(codec, archive, tid):
    fn = f"{archive}_db.dat"; p = DB_DIR/fn
    ents = codec["list_tables"](p, fn)
    e = codec["_resolve_table"](tid, ents, fn)
    off = e["offset"]; db = p.read_bytes()
    hit = next((off+d for d in range(64) if db[off+d:off+d+4] == MAGIC), None)
    data = db[hit:]; out = []; dctx = zstandard.ZstdDecompressor()
    while data[:4] == MAGIC:
        do = dctx.decompressobj(); chunk = do.decompress(data); out.append(chunk)
        data = do.unused_data
        if not do.eof or not data: break
    return out

def main():
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    codec = _reader()
    profs = sorted(glob.glob(str(OUT/"profiles/*.profile.json")))
    ck("seven_profiles", len(profs) == 7, f"{len(profs)}")
    bad_payload = bad_closure = bad_rows = bad_count = 0
    for fn in profs:
        d = json.load(open(fn, encoding="utf-8"))
        tid = d["table_type"]; p = d["payload"]; rc = d["row_closure"]
        frs = frames_payload(codec, p["archive"], tid)
        match = [f for f in frs if len(f) == p["payload_size"] and hashlib.sha256(f).hexdigest() == p["payload_sha256"]]
        if len(match) != 1: bad_payload += 1; print(f"  t{tid}: payload match={len(match)} frames={len(frs)}"); continue
        raw = match[0]
        if len(raw) != rc["payload_bytes"]: bad_closure += 1; print(f"  t{tid}: payload_bytes {rc['payload_bytes']} != len {len(raw)}")
        if rc["model"] == "fixed":
            eq = 14 + rc["count"]*rc["stride"] + 8
            if eq != len(raw): bad_closure += 1; print(f"  t{tid}: fixed closure {eq} != {len(raw)}")
        rf = OUT/d["full_rows_file"]
        if not rf.exists(): bad_rows += 1; print(f"  t{tid}: rows missing"); continue
        rb = rf.read_bytes()
        if hashlib.sha256(rb).hexdigest() != d["full_rows_sha256"]: bad_rows += 1; print(f"  t{tid}: rows sha mismatch")
        nlines = sum(1 for _ in rb.splitlines() if _.strip())
        if nlines != rc["count"]: bad_count += 1; print(f"  t{tid}: rows lines {nlines} != count {rc['count']}")
    ck("all_payload_size_sha", bad_payload == 0, f"bad={bad_payload}/7 (multi-frame aware)")
    ck("closure_arithmetic", bad_closure == 0, f"bad={bad_closure}/7")
    ck("rows_file_hash", bad_rows == 0, f"bad={bad_rows}/7")
    ck("rows_count_match", bad_count == 0, f"bad={bad_count}/7")
    cand = json.load(open(OUT/"subtable_candidates.json", encoding="utf-8"))
    ck("candidates_no_L3", "L3" not in json.dumps(cand.get("summary", {})) or cand["summary"].get("l3_count", 0) == 0, f"status={cand['status']}")
    ck("devseek_verify_status", (OUT/"verify.py").exists(), "verify.py present" if (OUT/"verify.py").exists() else "verify.py absent (devseek still finalizing)")
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t33 spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())