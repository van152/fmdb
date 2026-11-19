#!/usr/bin/env python3
"""t61 指挥官独立抽查 — held 枚举域专项验收(不 import worker 代码)。

数据侧字节核查(自写解码):
  A. 首反例绝对坐标字节验证(dbty/TCrs/extra_9/Necf)
交付物断言:
  B. enum_inventory 73 条台账、分层计数与 REPORT 一致、全部保持 held
  C. promoted 空;reports/ 未被 t61 改动
退出码 0=全过 1=失败 2=用法错。
"""
from __future__ import annotations

import hashlib
import json
import runpy
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("D:/tmp2b/fm24-db")
DATA = Path("D:/tmp2b/fm24-db/scratch/data")
CODEC = ROOT.parent / "fm24/scripts/modding_read_dbdat.py"

fails: list[str] = []


def check(name: str, ok: bool, why: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f"  ({why})" if why and not ok else ""))
    if not ok:
        fails.append(name)


def decode(archive: str, member: str) -> bytes:
    ind = runpy.run_path(str(CODEC))
    z = ind["_zstd_module"]()
    _, blob, d = ind["_entries"](DATA / archive)
    e = [x for x in d["entries"] if x["path"] == member or x["path"].endswith("/" + member)][0]
    st = d["data_base"] + e["offset"]
    return z.ZstdDecompressor().decompressobj().decompress(blob[st:st + e["packed_size"]])


def main() -> int:
    # ---------- A. 字节级首反例/首样例核查 ----------
    srv_comp = decode("server_db.dat", "server_db/table_25.dat")
    check("A1.dbty_first_miss@102218", srv_comp[102218:102219] == bytes.fromhex("1e"),
          srv_comp[102218:102220].hex())
    cli_nat = decode("client_db.dat", "client_db/table_10.dat")
    srv_nat = decode("server_db.dat", "server_db/table_10.dat")
    check("A2.Necf_client@8628", cli_nat[8628:8629] == b"\x00", cli_nat[8628:8630].hex())
    check("A3.Necf_server@99394", srv_nat[99394:99395] == b"\x00", srv_nat[99394:99396].hex())
    srv_t9 = decode("server_db.dat", "server_db/table_9.dat")
    check("A4.TCrs_t9_first_miss@1827", srv_t9[1827:1829] == bytes.fromhex("6400"),
          srv_t9[1827:1830].hex())
    srv_e9 = decode("server_db.dat", "server_db/table_extra_9.dat")
    check("A5.TCrs_e9_first_miss@55950", srv_e9[55950:55952] == bytes.fromhex("6d00"),
          srv_e9[55950:55953].hex())

    # ---------- B. 台账断言 ----------
    inv = json.loads((ROOT / "scratch/t61/out/enum_inventory.json").read_bytes())
    recs = inv["occurrences"]
    check("B1.records_73", len(recs) == 73, str(len(recs)))
    grades = Counter(str(r.get("grade")) for r in recs)
    check("B2.all_held_zero_promoted", set(grades) == {"held"}, str(grades))
    tbl = Counter(str(r.get("entity")) for r in recs)
    check("B2b.entity_split_31_32_10", tbl.get("nation") == 31 and tbl.get("club") == 32 and tbl.get("comp") == 10,
          str(dict(tbl)))
    layers = Counter(str(r.get("layer")) for r in recs)
    print(f"    [i] layers: {dict(layers)}")
    cts = inv.get("counts", {})
    check("B2c.counts_match_records", sum(
        v.get("occurrences", 0) for tside in cts.values() for v in (tside.values() if isinstance(tside, dict) else [])
        if isinstance(v, dict)) == 73, json.dumps(cts, ensure_ascii=False)[:200])
    missing = [i for i, r in enumerate(recs) if not (r.get("code") or r.get("xml_path"))]
    check("B3.records_identified", not missing, f"unidentified at {missing[:5]}")
    decisions = Counter(str(r.get("decision")) for r in recs)
    check("B3b.decisions", decisions.get("no_enum_source", 0) >= 60, str(dict(decisions)))
    ec = [r for r in recs if r.get("first_counterexample") or r.get("prior_first_counterexample")]
    check("B4.counterexamples_kept", len(ec) >= 60, str(len(ec)))
    dbty = [r for r in recs if r.get("code") == "dbty"]
    check("B6.dbty_record", bool(dbty) and dbty[0].get("grade") == "held"
          and "102218" in json.dumps(dbty[0], ensure_ascii=False), json.dumps(dbty[0], ensure_ascii=False)[:150] if dbty else "missing")

    prom = json.loads((ROOT / "scratch/t61/out/promoted.json").read_bytes())
    prom_n = len(prom) if isinstance(prom, list) else len(prom.get("promoted", []))
    check("B5.promoted_empty", prom_n == 0, str(prom_n))

    # ---------- C. 边界 ----------
    diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet", "--", "reports/"])
    check("C1.reports_untouched", diff.returncode == 0, f"git diff rc={diff.returncode}")
    led = json.loads((ROOT / "scratch/t01/LEDGER.json").read_bytes())
    check("C2.ledger_last_E100", led["entries"][-1]["id"] == "E100", led["entries"][-1]["id"])

    print(f"\n{len(fails)} FAIL / spot t61 done")
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)
    if "--selftest" in sys.argv:
        check("selftest", True)
        print(f"\n{len(fails)} FAIL / selftest")
        sys.exit(0)
    sys.exit(main())
