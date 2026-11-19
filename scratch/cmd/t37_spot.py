# -*- coding: utf-8 -*-
"""t37_spot.py — commander independent check of luna t37 nation inventory.
Verifies: table34 multi-frame payload (size 313082 + SHA a07b2bb7), closure
14+7115*44+8, 29 parents (24 unknown/4 t28/1 low_candidate), Tchl shared
club/nation, schema reconciliation 20 item + 9 zero = 29. L2 data-side, no L3.
"""
import sys, os, json, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/tmp2b/fm24-db/scripts")
sys.path.insert(0, "D:/tmp2b/fm24/tools/python")
os.environ.setdefault("FM24_DB_DIR", "D:/tmp2b/fm24-db/scratch/data")
from fm24_dump import _reader, DB_DIR, MAGIC
import zstandard

OUT = Path("D:/tmp2b/fm24-db/scratch/t37/out")

def pick_frame(codec, archive, tid, size, sha):
    fn = f"{archive}_db.dat"; p = DB_DIR/fn
    ents = codec["list_tables"](p, fn)
    e = codec["_resolve_table"](tid, ents, fn)
    off = e["offset"]; db = p.read_bytes()
    hit = next((off+d for d in range(64) if db[off+d:off+d+4] == MAGIC), None)
    # unbounded search: packed_size is the REAL frame's compressed size, but a stub
    # frame may precede it, so off+packed_size truncates. Match by exact size+SHA.
    data = db[hit:]; dctx = zstandard.ZstdDecompressor(); n = 0
    while data[:4] == MAGIC and n < 64:
        do = dctx.decompressobj(); ch = do.decompress(data); n += 1
        if len(ch) == size and hashlib.sha256(ch).hexdigest() == sha: return ch
        data = do.unused_data
        if not do.eof or not data: break
    return None

def main():
    d = json.load(open(OUT/"nation_subtable_inventory.json", encoding="utf-8"))
    checks = []
    def ck(name, ok, det=""):
        checks.append((name, ok, det)); print(f"[{'OK' if ok else 'FAIL'}] {name}: {det}")
    ck("status_partial", d["status"] == "partial_nation_parent_identity_coverage", d["status"])
    s = d["summary"]
    ck("schema_29_parents", s["nation_list_parent_count"] == 29 and s["item_bearing_parent_count"] == 20 and s["zero_item_parent_count"] == 9, f"29=20+9")
    ck("no_new_L3", s["new_L3_claims"] == 0 and s["L4"] == 0, f"L3={s['new_L3_claims']} L4={s['L4']}")
    parents = d["parents"]
    ck("parents_29", len(parents) == 29, f"{len(parents)}")
    from collections import Counter
    conf = Counter(p.get("confidence") for p in parents)
    ck("confidence_dist", conf["unknown"] == 24 and conf["existing_t28_closed"] == 4 and conf["low_candidate"] == 1, f"{dict(conf)}")
    t28 = sorted(p["parent_4cc"] for p in parents if p.get("link_status") == "complete_linked_by_t28")
    ck("t28_linked_four", t28 == ["Nagr", "Nefr", "Nlns", "Nnfr"], f"{t28}")
    tchl = [p for p in parents if p["parent_4cc"] == "Tchl"]
    ck("tchl_shared_candidate", len(tchl) == 1 and tchl[0].get("link_status") == "partial_shared_schema_candidate", f"{tchl[0].get('link_status') if tchl else 'missing'}")
    # table34 multi-frame payload
    t = d["tables"][0]
    ck("table34_identity", t["table_type"] == 34 and t["rtti_class"] == "STARTING_TEAM_CUP_HISTORY" and t["count"] == 7115 and t["stride"] == 44, f"t{t['table_type']} {t['count']}x{t['stride']}")
    codec = _reader()
    raw = pick_frame(codec, t["archive"], 34, t["payload_size"], t["payload_sha256"])
    ck("table34_payload_multiframe", raw is not None and len(raw) == 313082, f"match={'yes' if raw else 'NO'} len={t['payload_size']}")
    ck("table34_sha", t["payload_sha256"] == "a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812", t["payload_sha256"][:16])
    ck("table34_closure", 14 + 7115*44 + 8 == 313082, "14+7115*44+8=313082")
    pf = OUT/t["profile_file"]
    ck("profile_file_exists", pf.exists(), t["profile_file"])
    npass = sum(1 for _, ok, _ in checks if ok)
    print(f"\n=== t37 spot: {npass}/{len(checks)} ===")
    return 0 if npass == len(checks) else 1

if __name__ == "__main__":
    sys.exit(main())