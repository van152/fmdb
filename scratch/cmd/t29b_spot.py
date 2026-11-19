# -*- coding: utf-8 -*-
"""t29b_spot.py — commander independent check of luna t29b subtable_inventory.
Re-loads each profiled table payload, verifies payload_size + SHA-256 + count*stride
bound + rows_file hash; checks parent->table link consistency and unknown nulls.
NOTE: luna's own verify.py has ROOT=HERE.parents[3] bug (resolves to tmp2b not fm24-db).
"""
import sys, os, json, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, load_payload, DB_DIR, MAGIC
import zstandard

OUT = Path("D:/tmp2b/fm24-db/scratch/t29/out")

def frames_payload(codec, archive, tid):
    """Enumerate all zstd frames in a member; return list of decompressed frames.
    Handles E66 multi-frame members (empty stub first frame + real payload second)."""
    fn = f"{archive}_db.dat"; p = DB_DIR/fn
    ents = codec["list_tables"](p, fn)
    e = codec["_resolve_table"](tid, ents, fn)
    off = e["offset"]; db = p.read_bytes()
    hit = next((off+d for d in range(64) if db[off+d:off+d+4] == MAGIC), None)
    if hit is None: raise RuntimeError(f"t{tid}: no frame")
    data = db[hit:]; out = []; dctx = zstandard.ZstdDecompressor()
    while data[:4] == MAGIC:
        do = dctx.decompressobj()
        chunk = do.decompress(data)
        out.append(chunk)
        data = do.unused_data
        if not do.eof or not data: break
    return out

def pick_frame(codec, archive, tid, size, sha):
    for fr in frames_payload(codec, archive, tid):
        if len(fr) == size and hashlib.sha256(fr).hexdigest() == sha:
            return fr
    return None

def main():
    inv = json.load(open(OUT/"subtable_inventory.json", encoding="utf-8"))
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    tables = inv["tables"]; parents = inv["parents"]
    ck("parent_count_38", len(parents) == 38, f"{len(parents)}")
    ck("profiled_tables_13", len(tables) == 13, f"{len(tables)}")
    codec = _reader()
    bad_size = bad_sha = bad_bound = bad_rows = 0
    for t in tables:
        tid = t["table_type"]; arch = t["archive"]
        raw = pick_frame(codec, arch, tid, t["payload_size"], t["payload_sha256"])
        if raw is None:
            bad_size += 1; bad_sha += 1; print(f"  no frame matches size+sha t{tid}"); continue
        if t["count"]*t["stride"] > len(raw): bad_bound += 1; print(f"  bound t{tid}: {t['count']}*{t['stride']} > {len(raw)}")
        rf = OUT/t["rows_file"]
        if rf.exists():
            if hashlib.sha256(rf.read_bytes()).hexdigest() != t["rows_jsonl_sha256"]: bad_rows += 1; print(f"  rows sha t{tid}")
        else: bad_rows += 1; print(f"  rows missing t{tid}")
    ck("all_payload_size_sha", bad_size == 0 and bad_sha == 0, f"bad={bad_size}/13 (multi-frame aware)")
    ck("count_stride_bound", bad_bound == 0, f"bad={bad_bound}/13")
    ck("rows_file_hash", bad_rows == 0, f"bad={bad_rows}/13")
    # unknown parents encode table_type='unknown' (string), confidence='unknown'
    unknown = [p for p in parents if p.get("confidence") == "unknown"]
    linked = [p for p in parents if p.get("confidence") != "unknown"]
    unk_ok = all(p.get("table_type") == "unknown" and p.get("count") is None for p in unknown)
    ck("unknown_encoding", unk_ok and len(unknown) == 29, f"unknown={len(unknown)} linked={len(linked)}")
    # high-confidence parents reference profiled tables OR sol-closed (22/37/62)
    tids = {t["table_type"] for t in tables}
    sol_closed = {22, 37, 62}
    high = [p for p in parents if p.get("confidence") == "high"]
    high_ok = all(p["table_type"] in tids or p["table_type"] in sol_closed for p in high)
    ck("high_conf_linked", high_ok, f"high={[(p['parent_4cc'],p['table_type']) for p in high]}")
    # cross-check sol-closed subtables present in profiles (37/62); 22 is t27-only
    cmap = {t["table_type"]: t for t in tables}
    for tid, cnt, strd in [(37, 465712, 40), (62, 37214, 42)]:
        if tid in cmap:
            t = cmap[tid]
            ck(f"sol_closed_t{tid}", t["count"] == cnt and t["stride"] == strd, f"inv {t['count']}/{t['stride']} vs sol {cnt}/{strd}")
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t29b spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())