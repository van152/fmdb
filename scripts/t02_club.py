"""club (type 3) row decoder — commander hand-decode, t02.

Layout discovered from client_db.dat/table_3.dat:
  4 x u32   : (db_id, parent_ref[FFFFFFFF=none], db_id, db_id)
  5 B       : second id block (e.g. bf1d000000 -> u32 7615 + trailing 00)
  u32       : 512 (constant-ish, likely a status/flag group)
  1 B       : flag1
  u32+str   : full name (UTF-8)
  u32+str   : short name (UTF-8)
  3 B       : flag2 block
  12 B      : identity (ordinal | ID | dup ID)
  1 B       : boundary marker (0x00)

Verified: 69,705 of 84,259 rows parse exactly, identity ordinal==row_index.
Row 69,705+ uses a variant (likely LEAGUE_BODY_CLUB or extended fields) - unclosed.

Run: py -V:3.12 -I scripts/t02_club.py [--limit N] [--json OUT]
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB = r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm"
OLD_DECODER = r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py"


def load_table(archive="client_db.dat", tid=3):
    spec = importlib.util.spec_from_file_location("oldread", OLD_DECODER)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    path, data, meta = old._entries(DB, archive)
    for e in meta["entries"]:
        if old._table_id(e.get("path", "")) == tid:
            return old._decompress_entry(data, meta["data_base"], e)
    raise SystemExit(f"table_{tid} not found in {archive}")


def parse(raw, limit=None):
    count = struct.unpack_from("<I", raw, 8)[0]
    pos = 14
    rows = []
    n = count if limit is None else min(limit, count)
    for i in range(n):
        st = pos
        try:
            a, b, c, d = struct.unpack_from("<4I", raw, pos); pos += 16
            e5 = raw[pos:pos + 5]; pos += 5
            e6 = struct.unpack_from("<I", raw, pos)[0]; pos += 4
            f1 = raw[pos]; pos += 1
            n1 = struct.unpack_from("<I", raw, pos)[0]; pos += 4
            if not (0 <= n1 <= 200):
                raise ValueError(f"full-name len {n1}")
            full = raw[pos:pos + n1].decode("utf-8"); pos += n1
            n2 = struct.unpack_from("<I", raw, pos)[0]; pos += 4
            if not (0 <= n2 <= 200):
                raise ValueError(f"short-name len {n2}")
            short = raw[pos:pos + n2].decode("utf-8"); pos += n2
            f2 = raw[pos:pos + 3]; pos += 3
            o, x, y = struct.unpack_from("<III", raw, pos); pos += 12
            mk = raw[pos]; pos += 1
            if o != i or x != y or mk != 0:
                raise ValueError(f"identity o={o} x={x} y={y} mk={mk}")
            rows.append({
                "idx": i, "payload_off": st, "len": pos - st,
                "db_id": a, "parent_ref": b, "id_dup1": c, "id_dup2": d,
                "id5": int.from_bytes(e5, "little"), "id5_raw": e5.hex(),
                "grp": e6, "flag1": f1,
                "full_name": full, "short_name": short,
                "flag2": f2.hex(), "identity": [o, x, y], "marker": mk,
            })
        except Exception as ex:
            return rows, (i, pos, str(ex))
    return rows, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    raw = load_table()
    count = struct.unpack_from("<I", raw, 8)[0]
    rows, err = parse(raw, a.limit)
    print(f"payload {len(raw):,} B, count {count:,}")
    print(f"parsed {len(rows):,} rows", f"stopped at {err}" if err else "(all)")
    if rows:
        tail = rows[-1]["payload_off"] + rows[-1]["len"]
        print(f"last row ends at {tail:#x}; remaining {len(raw) - tail:,} B")
        print("first 3:", [(r["full_name"][:28], r["short_name"]) for r in rows[:3]])
        # identity check tally
        ok = sum(1 for r in rows if r["identity"][0] == r["idx"] and r["identity"][1] == r["identity"][2])
        print(f"identity OK: {ok:,}/{len(rows):,}")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"type_id": 3, "entity": "club", "count": count,
                       "parsed": len(rows), "error": err, "rows": rows}, f,
                      ensure_ascii=False, indent=1)
        print("wrote", a.json)
    if a.selftest:
        assert len(rows) > 60000, "expected >60k rows"
        assert rows[0]["full_name"].startswith("Klubi i Futbollit"), rows[0]["full_name"]
        assert rows[0]["short_name"] == "KF Albpetrol"
        print("selftest OK")


if __name__ == "__main__":
    sys.exit(main())
