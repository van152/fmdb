# -*- coding: utf-8 -*-
"""t35_spot.py — commander independent check of luna t35 Cafl/Cvfl discovery.
Validates negative result integrity: copy_ready unknown, schema fields preserved,
scan 0 candidates over 74 types, view no_data_vote, client table3 parent payload
(multi-frame +34) len/SHA/header count. NOTE: luna verify.py missing (incomplete).
"""
import sys, os, json, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, DB_DIR, MAGIC
import zstandard

OUT = Path("D:/tmp2b/fm24-db/scratch/t35/out")

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
    d = json.load(open(OUT/"cafl_cvfl_discovery.json", encoding="utf-8"))
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    ck("status_negative", d["status"] == "partial_no_semantic_candidate", d["status"])
    cr = {c["parent_4cc"]: c for c in d["copy_ready"]}
    ck("cafl_cvfl_unknown", all(cr[p]["candidate_table_type"] == "unknown" and cr[p]["item_field_candidates"] == [] for p in ("Cafl", "Cvfl")), "Cafl/Cvfl copy_ready unknown, no candidates")
    ck("schema_fields_preserved", len(cr["Cafl"]["schema_item_fields_not_mapped"]) == 29 and len(cr["Cvfl"]["schema_item_fields_not_mapped"]) == 19, f"Cafl={len(cr['Cafl']['schema_item_fields_not_mapped'])} Cvfl={len(cr['Cvfl']['schema_item_fields_not_mapped'])}")
    scan = d["semantic_candidate_scan"]
    ck("scan_zero_candidates", scan["candidate_count"] == 0 and scan["scan_scope"]["t14_types"] == 74, f"candidates={scan['candidate_count']} scope={scan['scan_scope']}")
    ck("near_miss_6", len(d["near_miss_club_classes"]) == 6, f"{len(d['near_miss_club_classes'])}")
    ck("view_no_data_vote", d["view_hypothesis"]["conclusion_tendency"] == "no_data_vote", d["view_hypothesis"]["conclusion_tendency"])
    # client table3 parent payload (multi-frame +34)
    pc = d["parent_container_context"]["archives"]["client"]
    sel = pc["selected_frame"]
    codec = _reader()
    frs = frames_payload(codec, "client", 3)
    match = [f for f in frs if len(f) == sel["payload_bytes"] and hashlib.sha256(f).hexdigest() == sel["payload_sha256"]]
    ck("client_table3_payload", len(match) == 1 and len(match[0]) == 6932082, f"frames={len(frs)} match={len(match)} len={sel['payload_bytes']}")
    ck("client_table3_sha", sel["payload_sha256"] == "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f", sel["payload_sha256"][:16])
    ck("client_table3_header_count", sel["row_count_header"] == 84259, f"{sel['row_count_header']}")
    ck("table3_is_club_parent", d["parent_container_context"]["stage2_table_type_3"]["entity"] == "club", d["parent_container_context"]["t14_table_type_3"]["primary_class"])
    ck("luna_verify_missing", not (OUT/"verify.py").exists(), "verify.py absent (incomplete delivery, commander spot is gate)")
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t35 spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())