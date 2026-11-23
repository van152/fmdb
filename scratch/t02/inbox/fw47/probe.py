"""t02-f fw47: row framework only for table_47 (fixed stride + preamble).

Findings (L1, own decode):
  * payload header `03 01 74 61 64 2e f1 0d`, count = u32le @ payload+8 => 2488
  * 11-byte table preamble @ 0xe  (8b 00 00 00 7e c1 83 00 00 00 00 00)
  * rows start @ 0x19?  -> no: rows region starts right after the preamble
  * closure: 14 + 11 + count*44 + 8 == payload_len (exact, both archives)
Caveat (recorded, not resolved here): per-row `u32 == row_index` tags inside the
rows region are spaced 41/46/51/56 bytes (all == 1 mod 5), i.e. a candidate
variable formula row_len = 41 + 5*n with sum(n) = 1495. That chain does not close
to the byte (sum 109474 vs required 109483), so it stays a candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path

ROOT = Path("D:/tmp2b/fm24-db")
OLD = Path("D:/tmp2b/fm24/scripts/modding_read_dbdat.py")
DB = Path("Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm")
OUT = ROOT / "scratch/t02/inbox/fw47/framework.json"
HDR, FTR, PRE = 14, 8, 11


def old():
    spec = importlib.util.spec_from_file_location("old_dbdat", OLD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def member(mod, archive: str, tid: int):
    path, packed, layout = mod._entries(db_path=DB, archive=archive)
    e = mod._resolve_table(tid, layout["entries"], path.name)
    if e is None:
        return None, None
    return mod._decompress_entry(packed, layout["data_base"], e), e["path"]


def tag_spacings(raw: bytes, count: int, limit: int = 502) -> dict:
    """Candidate variable framing: first u32==i after previous tag (greedy chain)."""
    n = len(raw)
    u32 = lambda p: struct.unpack_from("<I", raw, p)[0]
    tags, cur = [], HDR
    for i in range(min(count, limit)):
        p = next((q for q in range(cur, min(n - 3, cur + 4096)) if u32(q) == i), None)
        if p is None:
            return {"chain_rows": len(tags), "stopped_at_row": i}
        tags.append(p)
        cur = p + 4
    d = [tags[i + 1] - tags[i] for i in range(len(tags) - 1)]
    return {"chain_rows": len(tags), "chain_limit": limit,
            "spacings": sorted(set(d)), "spacing_hist": {str(k): d.count(k) for k in sorted(set(d))}}


def side(mod, archive: str, tid: int) -> dict:
    raw, name = member(mod, archive, tid)
    if raw is None:
        return {"member": f"{archive}/table_{tid}.dat", "error": "absent"}
    n = len(raw)
    count = int.from_bytes(raw[8:12], "little")
    body = n - HDR - FTR
    stride = body // count if count else 0
    preamble = body - count * stride
    ok = (HDR + PRE + count * stride + FTR == n) and preamble == PRE
    d = {
        "member": name,
        "count": count,
        "stride": stride,
        "rows_offset": "0xe",
        "table_preamble_len": preamble,
        "table_preamble_hex": raw[HDR:HDR + preamble].hex(" "),
        "rows_region_offset": hex(HDR + preamble),
        "payload_len": n,
        "header": raw[:HDR].hex(" "),
        "footer": raw[-FTR:].hex(" "),
        "payload_sha256": hashlib.sha256(raw).hexdigest(),
        "closure": f"14 + {preamble} + {count}*{stride} + 8 == {n}",
        "closure_ok": bool(ok),
        "variable": False,
        "evidence": "L1 (own decode of Z:/SteamLibrary .dat, no schema/field work)",
    }
    if not ok:
        d["remainder_non_stride_bytes"] = preamble
    d["_tag_probe"] = tag_spacings(raw, count)
    d["_raw"] = raw
    return d


def run(tid: int, write: bool = True) -> dict:
    mod = old()
    res = {"type_id": tid, "status": "in_progress", "client": None, "server": None,
           "relation": None}
    raws = {}
    for key, arch in (("client", "client_db.dat"), ("server", "server_db.dat")):
        s = side(mod, arch, tid)
        if "_raw" in s:
            raws[key] = s["_raw"]
        tp = s.pop("_tag_probe", None)
        s.pop("_raw", None)
        res[key] = s
        if tp and key == "client":
            res["tag_spacing_probe"] = tp
        if write:                                    # write after each side lands
            OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    if len(raws) == 2:
        c, o = raws["client"], raws["server"]
        k = 0
        while k < min(len(c), len(o)) and c[k] == o[k]:
            k += 1
        res["relation"] = (f"payloads byte-identical={c == o}; "
                           f"common prefix {k} of {len(c)}/{len(o)} bytes")
        res["payload_identical"] = c == o
    if all(isinstance(res[s], dict) and res[s].get("closure_ok") for s in ("client", "server")):
        res["status"] = "complete"
    res["candidate_variable_formula"] = (
        "row_len = 41 + 5*n (candidate only: inner u32==row_index tags are spaced "
        "41/46/51/56, all == 1 mod 5; greedy chain sum 109474 vs required 109483, "
        "so this framing does NOT close and is not adopted)")
    res["caveat"] = (
        "stride 44 is a length-only fit (body not divisible by count); it is exact only "
        "because an 11-byte table preamble is absorbed. Row-internal index tags do not "
        "align to any 44-byte column, so per-row boundaries here are candidate-level.")
    if write:
        OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="t02-f row framework probe (row frame only, read-only)")
    ap.add_argument("--tid", type=int, default=47)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        r = run(47, write=False)
        print(json.dumps(r, indent=1, ensure_ascii=False)[:2000])
        print("selftest", "PASS" if r["status"] == "complete" else "FAIL")
        return 0 if r["status"] == "complete" else 1
    r = run(a.tid, write=not a.no_write)
    print(json.dumps(r, indent=1, ensure_ascii=False))
    return 0 if r["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
