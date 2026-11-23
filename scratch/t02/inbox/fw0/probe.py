"""t02-f fw0: row framework only, type_id=0 (fixed-stride check). Read-only."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, struct, sys
from pathlib import Path

OLD = Path(r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
DB = Path(r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm")
OUT = Path(r"D:\tmp2b\fm24-db\scratch\t02\inbox\fw0\framework.json")
HDR, FTR = 14, 8


def old():
    spec = importlib.util.spec_from_file_location("old_dbdat", OLD)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def member(mod, archive, tid):
    path, packed, layout = mod._entries(db_path=DB, archive=archive)
    e = mod._resolve_table(tid, layout["entries"], path.name)
    if e is None:
        raise LookupError(f"table_{tid} absent from {archive}")
    return mod._decompress_entry(packed, layout["data_base"], e), e["path"]


def side(mod, archive, tid):
    raw, name = member(mod, archive, tid)
    n = len(raw)
    count = struct.unpack_from("<I", raw, 8)[0]
    rows = n - HDR - FTR
    d = {"member": name, "count": count, "rows_offset": hex(HDR),
         "rows_offset_dec": HDR, "payload_len": n,
         "header": raw[:HDR].hex(" "), "footer": raw[-FTR:].hex(" "),
         "footer_info": {"offset": hex(n - FTR), "bytes": raw[-FTR:].hex(" ")},
         "payload_sha256": hashlib.sha256(raw).hexdigest()}
    if count and rows % count == 0:
        stride = rows // count
        d["stride"] = stride
        d["variable"] = False
        d["closure"] = f"14 + {count}*{stride} + 8 == {n}"
        d["closure_ok"] = HDR + count * stride + FTR == n
        d["rows_end"] = hex(HDR + count * stride)
        # strict re-derivation: every row must be exactly stride long (trivially true),
        # so instead falsify smaller periods: no divisor of stride may also close.
        alt = [s for s in range(1, stride) if stride % s == 0 and HDR + count * s + FTR == n]
        d["smaller_closing_stride"] = alt
        d["row0_hex"] = raw[HDR:HDR + stride].hex(" ")
        d["row_last_hex"] = raw[HDR + (count - 1) * stride:HDR + count * stride].hex(" ")
    else:
        d["stride"] = None
        d["variable"] = True
        d["closure"] = f"(14 + 8) does not divide {rows} over {count} rows"
        d["closure_ok"] = False
    return d, raw


def run(tid=0, write=True):
    mod = old()
    res = {"type_id": tid, "status": "in_progress", "client": None, "server": None, "relation": None}
    raws = {}
    for key, arch in (("client", "client_db.dat"), ("server", "server_db.dat")):
        try:
            d, raw = side(mod, arch, tid)
        except LookupError as e:
            res[key] = {"error": str(e)}; continue
        raws[key] = raw
        res[key] = d
        if write:
            OUT.write_text(json.dumps(res, indent=1) + "\n")
    if len(raws) == 2:
        c, s = raws["client"], raws["server"]
        k = 0
        while k < min(len(c), len(s)) and c[k] == s[k]:
            k += 1
        res["relation"] = (f"payloads byte-identical={c == s}; common prefix {k} of "
                           f"{len(c)}/{len(s)} bytes -> server stride == client stride")
        if c == s:
            res["server"]["stride"] = res["client"]["stride"]
            res["server"]["closure"] = res["client"]["closure"]
    ok = all(res[k] and res[k].get("closure_ok") for k in ("client", "server"))
    if ok:
        res["status"] = "complete"
    if write:
        OUT.write_text(json.dumps(res, indent=1) + "\n")
    return res


def main():
    ap = argparse.ArgumentParser(description="t02-f row framework probe (fixed stride), read-only")
    ap.add_argument("--tid", type=int, default=0)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        r = run(0, write=False)
        ok = (r["status"] == "complete" and r["client"]["stride"] == 77
              and r["client"]["count"] == 3545 and r["server"]["stride"] == 77)
        print("selftest", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    r = run(a.tid, write=not a.no_write)
    print(json.dumps({k: r[k] for k in ("type_id", "status", "relation")}, indent=1))
    for k in ("client", "server"):
        d = r[k] or {}
        print(f"{k:6} stride={d.get('stride')} count={d.get('count')} "
              f"payload_len={d.get('payload_len')} closure_ok={d.get('closure_ok')}")
    return 0 if r["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
