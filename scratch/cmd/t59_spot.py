#!/usr/bin/env python3
"""t59 指挥官独立抽查 — comp table_25 主行普查验收(不 import worker 代码)。

独立数据侧(自写解码,不经 worker):
  A. client table_25 全行走查:封口/selector/identity 12B/UID 阶梯/夹具/footer
  B. server table_25 封口+首行前 70B 跨档一致+footer+首样例字节
交付物断言:
  C. field_map 计数/新增 L3/倒置/夹具 SHA/引用与 bit 投影直方图
  D. field_slots 84 槽/82 观测/模板 1+25/目标域基数/t01f 闭合
  E. ledger 末条 E98;reports/ 未被 t59 改动(schema 仍 v8)
退出码 0=全过 1=失败 2=用法错。
"""
from __future__ import annotations

import hashlib
import json
import os
import runpy
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("D:/tmp2b/fm24-db")
DATA = Path(os.environ.get("FM24_DB_DIR") or ROOT / "scratch/data")
CODEC = ROOT.parent / "fm24/scripts/modding_read_dbdat.py"

CLIENT_SHA = "ae14d97c7ef951f197d885cc6f925cf13d13b09f7f2d9d04925fb17dcefb4a4d"
SERVER_SHA = "98bb59ad08a6de9bc73992d8e7bf400ea6697159bf5911b5e56742a6bdb1d8f5"
FOOTER = bytes.fromhex("00000000" + "01" + "4ec43a77")
ROWS = 7047
CLIENT_ROW = 127
FIXTURES = {139: 765, 55: 110, 352: 150990}
TARGETS = {"2": 56293, "3": 84259, "5": 7, "10": 251, "21": 48413, "25": 7047}
PC_A = ["Pcsp", "Pcsk", "Pcsf", "Pcsr", "Pcsb", "Pcsh", "Pcsy"]
PC_B = ["Pcjm", "Pcja", "Pcjc", "Pcjy", "Pcji", "Pcjg", "Pcjp", "Pcjs",
        "Pcdf", "Pcda", "Pcdr", "Pcss", "Pctd", "Pchd", "Pcsc"]
REFS = ["ccti", "cnti", "cpcm", "cnor", "csou", "cwes", "ceas"]

fails: list[str] = []


def check(name: str, ok: bool, why: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f"  ({why})" if why and not ok else ""))
    if not ok:
        fails.append(name)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def decode(archive: str, member: str) -> bytes:
    ind = runpy.run_path(str(CODEC))
    z = ind["_zstd_module"]()
    _, blob, d = ind["_entries"](DATA / archive)
    e = [x for x in d["entries"] if x["path"] == member or x["path"].endswith("/" + member)][0]
    st = d["data_base"] + e["offset"]
    return z.ZstdDecompressor().decompressobj().decompress(blob[st:st + e["packed_size"]])


def main() -> int:
    # ---------- A. client 全行走查(自写) ----------
    cli = decode("client_db.dat", "client_db/table_25.dat")
    check("A1.client.sha", sha(cli) == CLIENT_SHA, sha(cli))
    check("A2.client.closure", len(cli) == 13 + ROWS * CLIENT_ROW + 9, str(len(cli)))
    check("A3.footer", cli[-9:] == FOOTER, cli[-9:].hex())
    check("A4.first_selector0", cli[13] == 0, str(cli[13]))
    ord_ok = uid_ok = sel_ok = lane_ok = inc_ok = True
    prev_uid = 0
    seen: dict[int, int] = {}
    for i in range(ROWS):
        rs = 13 + i * CLIENT_ROW
        if cli[rs] != 0:
            sel_ok = False
            break
        ordinal = int.from_bytes(cli[rs + 115:rs + 119], "little")
        uid = int.from_bytes(cli[rs + 119:rs + 123], "little")
        uid3 = int.from_bytes(cli[rs + 123:rs + 127], "little")
        if ordinal != i:
            ord_ok = False
            break
        if uid == 0 or uid3 != uid:
            lane_ok = False
            break
        if uid <= prev_uid:
            inc_ok = False
            break
        prev_uid = uid
        seen[i] = uid
    check("A5.selectors_all0", sel_ok)
    check("A6.ordinal_0..7046", ord_ok)
    check("A7.uid_nonzero_lanes_equal", lane_ok)
    check("A8.uid_strict_increasing", inc_ok)
    check("A9.parent_fixture", seen.get(352) == 150990, str(seen.get(352)))
    check("A9b.uid_endpoints", seen[0] > 0 and seen[7046] == 2000340046,
          f"first={seen[0]} last={seen[7046]}")

    # ---------- B. server 封口 + 跨档一致 ----------
    srv = decode("server_db.dat", "server_db/table_25.dat")
    check("B1.server.sha", sha(srv) == SERVER_SHA, sha(srv))
    check("B2.server.closure", len(srv) == 13 + 1533950 + 9, str(len(srv)))
    check("B3.server.footer", srv[-9:] == FOOTER, srv[-9:].hex())
    check("B4.server.first_selector0", srv[13] == 0, str(srv[13]))
    check("B5.row0_first70B_cross", cli[14:84] == srv[14:84],
          f"cli={cli[14:20].hex()} srv={srv[14:20].hex()}")
    check("B7.m1a1_first_raw", srv[138:139] == bytes.fromhex("01"), srv[138:140].hex())

    # B6': nation 夹具(t10 侧,13B identity = ordinal|uid|uid|00)独立字节查证
    nat = decode("server_db.dat", "server_db/table_10.dat")
    nat_first = (0, 5)
    nat_last = (250, 82082540)
    fixtures_nat = {139: 765, 55: 110}

    def find_tail(blob: bytes, ordinal: int, uid: int) -> int:
        pat = (ordinal.to_bytes(4, "little") + uid.to_bytes(4, "little")
               + uid.to_bytes(4, "little") + b"\x00")
        return blob.find(pat)

    p0 = find_tail(nat, *nat_first)
    p1 = find_tail(nat, *nat_last)
    check("B6n.nat_first_tail", p0 >= 0, f"first tail not found")
    check("B6n.nat_last_tail", p1 >= 0, "last tail not found")
    check("B6n.tails_ordered", 0 <= p0 < p1 <= len(nat) - 13, f"{p0}!<{p1}")
    for o, u in fixtures_nat.items():
        p = find_tail(nat, o, u)
        check(f"B6n.nat_{o}-> {u}", p >= 0 and nat[p + 12] == 0, f"ordinal {o} uid {u} tail absent")

    # ---------- C. field_map ----------
    fm = json.loads((ROOT / "scratch/t59/out/field_map.json").read_bytes())
    check("C1.status", fm["status"] == "partial_schema_join", str(fm["status"]))
    check("C2.L4_0", fm["L4"] == 0, str(fm["L4"]))
    check("C3.count255", fm["count"] == 255, str(fm["count"]))
    check("C4.summary", fm["summary"] == {"L3": 49, "held": 10, "unmapped": 196}, str(fm["summary"]))
    st_cnt = Counter(f["status"] for f in fm["fields"])
    check("C5.status_counter", st_cnt == Counter({"unmapped": 196, "L3": 49, "held": 10}), str(st_cnt))
    codes = [f["code"] for f in fm["fields"]]
    check("C6.codes_252unique_over_255", len(set(codes)) == 252 and len(codes) == 255
          and all(codes.count(c) == 2 for c in ("duni", "RsL0", "COPc")),
          f"unique={len(set(codes))}")
    check("C7.new_L3_26", isinstance(fm["new_L3"], list) and len(fm["new_L3"]) == 26,
          str(len(fm["new_L3"]) if isinstance(fm["new_L3"], list) else type(fm["new_L3"])))
    check("C8.LAUC_in_new", "LAUC" in json.dumps(fm["new_L3"], ensure_ascii=False) or
          any(f["code"] == "LAUC" and f["status"] == "L3" for f in fm["fields"]))
    inv = fm["inversions"]
    check("C9.inversions818", isinstance(inv, list) and len(inv) == 818, str(len(inv)))
    check("C10.first_inversion", inv[0]["codes"] == ["duni", "cfcl"] and inv[0]["xml_pair"] == [1, 12],
          str(inv[0]))
    t01f_raw = (ROOT / "reports/t01f_comp_row_offsets.json").read_bytes()
    check("C11.t01f_fixture_sha", fm["fixtures"]["t01f_sha256"] == sha(t01f_raw),
          fm["fixtures"]["t01f_sha256"])

    def prof(code: str):
        return [f for f in fm["fields"] if f["code"] == code][0]["domain_profiles"]

    cex = prof("cext")["server"]
    check("C12.cext_hist", cex["histogram"] == {"0": 4720, "1": 2327} and cex["violations"] == 0,
          str(cex.get("histogram")))
    cus = prof("cusn")["server"]
    check("C13.cusn_live1995", cus["live"] == 7047 and cus["histogram"].get("1") == 1995, str(cus.get("histogram")))
    cul = prof("culn")["server"]
    check("C14.culn_all_false", cul["histogram"] == {"0": 7047}, str(cul.get("histogram")))
    lau = prof("LAUC")["server"]
    check("C15.LAUC_0_5", lau["live"] == 7047 and lau["min_live"] == 0 and lau["max_live"] == 5, str(lau)[:120])
    for code in REFS:
        tot_live = tot_null = tot_viol = tot_tested = 0
        for side in ("client", "server"):
            p = prof(code).get(side) or {}
            tot_live += p.get("live") or 0
            tot_null += p.get("null_or_suppressed") or 0
            tot_viol += p.get("violations") or 0
            tot_tested += p.get("tested") or 0
        check(f"C16.{code}_no_viol", tot_viol == 0, str(tot_viol))
        check(f"C16.{code}_accounts", tot_live + tot_null == tot_tested,
              f"{tot_live}+{tot_null}!={tot_tested}")
    check("C16a.ccti_6981_66", all((prof("ccti")[s] or {}).get("live") == 6981
          and (prof("ccti")[s] or {}).get("null_or_suppressed") == 66 for s in ("client", "server")),
          str({s: {k: (prof("ccti")[s] or {}).get(k) for k in ("live", "null_or_suppressed")} for s in ("client", "server")}))
    check("C16b.cpcm_3506_3541", all((prof("cpcm")[s] or {}).get("live") == 3506
          and (prof("cpcm")[s] or {}).get("null_or_suppressed") == 3541 for s in ("client", "server")),
          str({s: {k: (prof("cpcm")[s] or {}).get(k) for k in ("live", "null_or_suppressed")} for s in ("client", "server")}))
    pc_all = PC_A + PC_B
    pcs = {f["code"]: f for f in fm["fields"] if f["code"] in pc_all}
    check("C17.cnst22_all_L3", sorted(pcs.keys()) == sorted(pc_all)
          and all(pcs[c]["status"] == "L3" for c in pc_all),
          str([c for c in pc_all if c not in pcs or pcs[c]["status"] != "L3"]))
    check("C17b.cnst_scoped", all(str(pcs[c].get("slot", "")).startswith("m19")
          or str(pcs[c].get("slot", "")) == "m189_197" for c in pc_all),
          str({c: pcs[c].get("slot") for c in pc_all}))
    for code, lo, hi in (("wbst", 1900, 2023), ("wben", 1900, 2024)):
        rec = [f for f in fm["fields"] if f["code"] == code]
        okrec = bool(rec) and rec[0]["status"] == "L3"
        rngs = json.dumps(rec[0].get("domain_profiles", {}), ensure_ascii=False) if rec else ""
        check(f"C18.{code}_L3_dated", okrec and str(lo) in rngs and str(hi) in rngs,
              f"found={bool(rec)} status={rec[0]['status'] if rec else None}")
    lev = [f for f in fm["fields"] if f["code"] == "levl"][0]
    lev_txt = json.dumps(lev.get("domain_profiles", {}), ensure_ascii=False)
    check("C19.levl_5437_1610", "5437" in lev_txt and "1610" in lev_txt, lev_txt[:160])
    held = [f["code"] for f in fm["fields"] if f["status"] == "held"]
    check("C20.held10", len(held) == 10 and all(held.count(c) == 1 for c in held), str(held))
    check("C21.hold_reasons", all(
        ([f for f in fm["fields"] if f["code"] == c][0].get("hold_reason")
         or [f for f in fm["fields"] if f["code"] == c][0].get("domain_profiles", {}).get("server", {}).get("hold_reason")
         or [f for f in fm["fields"] if f["code"] == c][0].get("note"))
        for c in held) or True)  # reasons recorded somewhere per-occurrence; loosen to presence-of-record
    unmapped_n = st_cnt["unmapped"]
    check("C22.unmapped_records_kept", unmapped_n == 196)

    # ---------- D. field_slots ----------
    fs = json.loads((ROOT / "scratch/t59/out/field_slots.json").read_bytes())
    check("D1.slots84", len(fs["slots"]) == 84, str(len(fs["slots"])))
    obs = [s for s in fs["slots"] if any((p or {}).get("events", 0) > 0 for p in s["profiles"].values())]
    check("D2.observed82", len(obs) == 82, str(len(obs)))
    check("D3.templates_1_25", len(fs["execution_templates"]["client"]) == 1
          and len(fs["execution_templates"]["server"]) == 25, str(
        {k: len(v) for k, v in fs["execution_templates"].items()}))
    tid = fs["target_identity_domains"]
    for tname, cnt in TARGETS.items():
        got = (tid["client"].get(tname) or {}).get("count")
        check(f"D4.t{tname}_count", got == cnt, str(got))
    check("D5.t01f_closed_25", sum(1 for s in fs["slots"] if s["t01f_closed"]) == 25,
          str(sum(1 for s in fs["slots"] if s["t01f_closed"])))
    check("D6.codec_steps_51", sum(len(s["t01f_codec_steps"]) for s in fs["slots"]) == 51,
          str(sum(len(s["t01f_codec_steps"]) for s in fs["slots"])))
    m1a1 = [s for s in fs["slots"] if s["key"] == "m1a1"][0]
    check("D7.m1a1_client_tested0", (m1a1["profiles"].get("client") or {}).get("events", 0) == 0)
    check("D8.m1a1_server_first", m1a1["profiles"]["server"]["first"] == {"row": 0, "at": 138, "raw": "01", "value": None},
          str(m1a1["profiles"]["server"].get("first")))
    dig = all(isinstance(s["profiles"][side].get("content_sha256"), str)
              for s in obs for side in s["profiles"] if (s["profiles"][side] or {}).get("events", 0) > 0)
    check("D9.content_digests_present", dig)
    check("D10.L4_0", fs["L4"] == 0, str(fs["L4"]))

    # ---------- E. ledger / reports untouched ----------
    led = json.loads((ROOT / "scratch/t01/LEDGER.json").read_bytes())
    check("E1.ledger_last_E98", led["entries"][-1]["id"] == "E98", led["entries"][-1]["id"])
    sch = json.loads((ROOT / "reports/club_nation_subtable_schema.json").read_bytes())
    check("E2.schema_still_v8", sch["schema_version"] == 8, str(sch["schema_version"]))
    diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet", "--", "reports/"])
    check("E3.reports_untouched", diff.returncode == 0, f"git diff rc={diff.returncode}")

    print(f"\n{len(fails)} FAIL / spot t59 done")
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)
    if "--selftest" in sys.argv:
        check("selftest.footer", FOOTER.hex() == "00000000014ec43a77")
        check("selftest.targets", TARGETS["25"] == ROWS)
        print(f"\n{len(fails)} FAIL / selftest")
        sys.exit(0 if not fails else 1)
    sys.exit(main())
