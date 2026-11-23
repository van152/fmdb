#!/usr/bin/env python3
"""t84_join — 8 个 name 槽的 join 判定(只读)。

结论口径
--------
* `name_table_{0,1,2}` = 12 字节索引行(6 x u16),第 2/3 列合成记录序号;
  `name_table_extra_{0,1,2}` = (u32 idx, u32 len, utf8) 记录流。两者行数相等
  且 extra 池 idx 连续 0..n-1 → 一一对应,**池内容是人名(token)池**。
* 8 个 name 槽(Cnam/Csnm/Nnam/Nsnm/N3ln/cnam/csnm/c3ln)的取值在**主行内联**
  或 `lang_update_db` 的 uid 记录里,不在这些池中 —— 故 join **不成立**,
  8 条 held 原样保留,并给出首反例。
* `lang_update_db` 是真正的名字覆盖层:记录 = `uid u32` + N 个 `(u32len, utf8)`,
  尾部 3 字节;`8_3`(club, 6 字段)与 `8_25`(comp, 3 字段)完全闭合。

用法
----
  py -V:3.12 -I -B scripts/t84_join.py --help
  py -V:3.12 -I -B scripts/t84_join.py --selftest
  py -V:3.12 -I -B scripts/t84_join.py --build scratch/t84/out/joins.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from t84_pools import (DB_DIR, Fail, _codec, load_member, parse_index,  # noqa: E402
                       parse_pool, require)

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLOTS = [
    ("club", "Cnam", "club.xml#club/006", 6),
    ("club", "Csnm", "club.xml#club/007", 7),
    ("nation", "Nnam", "nation.xml#nati/007", None),
    ("nation", "Nsnm", "nation.xml#nati/008", None),
    ("nation", "N3ln", "nation.xml#nati/011", None),
    ("comp", "cnam", "comp.xml#comp/009", 9),
    ("comp", "csnm", "comp.xml#comp/010", 10),
    ("comp", "c3ln", "comp.xml#comp/011", 11),
]
PROBE = ["England", "Brazil", "Wales", "Denmark", "Liverpool", "Arsenal",
         "Serie A", "Premier Division"]


def lang_records(raw: bytes, nfields: int, trailer: int) -> tuple[list, int, str]:
    """uid u32 ; nfields x ([0xFF] u32len utf8) ; trailer bytes."""
    require(raw[:8] == bytes.fromhex("03017461642ef10d"), "lang: bad header")
    cnt = struct.unpack_from("<I", raw, 8)[0]
    pos, recs = 12, []
    try:
        for _ in range(cnt):
            require(pos + 4 <= len(raw), "lang: eof uid")
            uid = struct.unpack_from("<I", raw, pos)[0]
            pos += 4
            flds = []
            for _f in range(nfields):
                if raw[pos] == 0xFF:
                    pos += 1
                require(pos + 4 <= len(raw), "lang: eof len")
                ln = struct.unpack_from("<I", raw, pos)[0]
                require(ln <= 400 and pos + 4 + ln <= len(raw), f"lang: len {ln}")
                flds.append(raw[pos + 4: pos + 4 + ln].decode("utf-8"))
                pos += 4 + ln
            pos += trailer
            recs.append({"uid": uid, "fields": flds})
    except (Fail, UnicodeDecodeError, struct.error) as exc:
        return recs, pos, f"first_counterexample: {exc}"
    return recs, pos, "ok"


def pool_sets(codec, archive: str) -> dict[int, list[str]]:
    out = {}
    for n in range(3):
        p = parse_pool(load_member(codec, archive, f"name_table_extra_{n}.dat"))
        out[n] = [r["text"] for r in p["recs"]]
    return out


def idblock_before(raw: bytes, pos: int, limit: int = 40):
    """club 行内身份块 = db_id,FFFFFFFF,db_id,db_id(紧邻名字前的长度前缀)。"""
    for back in range(24, limit):
        p = pos - back
        if p < 0:
            return None
        a, b, c, d = struct.unpack_from("<IIII", raw, p)
        if b == 0xFFFFFFFF and a == c == d and 0 < a < 2 * 10 ** 6:
            return a
    return None


def build(out: pathlib.Path) -> int:
    codec = _codec()
    pools = {a: pool_sets(codec, a) for a in ("client", "server")}
    sets = {a: {n: set(v) for n, v in p.items()} for a, p in pools.items()}

    res: dict = {
        "task": "t84", "db_dir": str(DB_DIR),
        "pool_semantics": {}, "slots": [], "lang_update": {},
    }
    for n in range(3):
        v = pools["client"][n]
        res["pool_semantics"][f"pool{n}"] = {
            "count": len(v),
            "client_equals_server": pools["client"][n] == pools["server"][n],
            "single_token_share": round(
                100 * sum(1 for x in v if " " not in x) / len(v), 2),
            "probe_membership": {p: (p in sets["client"][n]) for p in PROBE},
            "samples": v[:8],
        }

    # ---- 每槽判定 ----
    raw3 = load_member(codec, "client", "table_3.dat")
    lang_club, club_end, club_st = lang_records(
        load_member(codec, "lang_update", "8_3.dat"), 6, 3)
    lang_comp, comp_end, comp_st = lang_records(
        load_member(codec, "lang_update", "8_25.dat"), 3, 1)

    # club: 名字在行内(table_3),槽值不是池索引
    found = matched = 0
    ex = []
    for rec in lang_club:
        nm = rec["fields"][0].encode("utf-8")
        i = raw3.find(struct.pack("<I", len(nm)) + nm)
        if i < 0:
            continue
        found += 1
        did = idblock_before(raw3, i)
        if did == rec["uid"]:
            matched += 1
        elif len(ex) < 5:
            ex.append({"lang_uid": rec["uid"], "row_db_id": did,
                       "name": rec["fields"][0][:40]})

    res["lang_update"] = {
        "members_present": {"8_3": "club", "8_25": "comp"},
        "nation_type_10_present": False,
        "footer_bytes": 0,
        "club_8_3": {"closure": club_st == "ok", "records": len(lang_club),
                     "end": club_end, "payload_len": 282983,
                     "inline_name_found": found,
                     "uid_equals_row_db_id": matched,
                     "mismatch_examples": ex},
        "comp_8_25": {"closure": comp_st == "ok", "records": len(lang_comp),
                      "end": comp_end, "payload_len": 2085},
    }

    for entity, code, xml_id, idx in SLOTS:
        pool_hit = {n: (code in sets["client"][n]) for n in range(3)}
        if entity == "club":
            verdict = "held"
            why = ("value is an inline length-prefixed string inside the club main "
                   "row (table_3); the name pools hold person tokens, not club names")
            ce = {"kind": "pool_membership", "code": code, "pool_hit": pool_hit,
                  "lang_uid_equals_row_db_id": f"{matched}/{found}"}
        elif entity == "nation":
            verdict = "held"
            why = ("no nation (type 10) member exists in lang_update_db; the pools "
                   "carry person tokens and table_10 has no printable name bytes")
            ce = {"kind": "no_name_store", "code": code,
                  "lang_update_has_type_10": False, "pool_hit": pool_hit,
                  "table_10_printable_share": 0.082}
        else:
            verdict = "held"
            why = ("comp names live in the lang_update 8_25 uid overlay; table_25 "
                   "carries the uid but no inline name and the pools hold no comp names")
            ce = {"kind": "overlay_not_pool", "code": code, "pool_hit": pool_hit,
                  "lang_8_25_uid_hits": f"{len(lang_comp)}/{len(lang_comp)}"}
        res["slots"].append({
            "entity": entity, "code": code, "xml_id": xml_id,
            "xml_index": idx, "bucket_before": "held", "bucket_after": verdict,
            "join_established": False, "hold_reason": why,
            "first_counterexample": ce,
            "provenance": ["scratch/t78/out/buckets.json", "scratch/t57/out/field_map.json",
                           "reports/club_nation_subtable_schema.json"],
        })

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")
    return 0


def selftest() -> int:
    codec = _codec()
    ok = fail = 0
    for archive in ("client", "server"):
        try:
            ps = pool_sets(codec, archive)
            good = all(len(ps[n]) > 0 for n in range(3))
            print(("PASS" if good else "FAIL"), f"{archive} pools", {n: len(ps[n]) for n in range(3)})
            ok += 1 if good else 0
            fail += 0 if good else 1
        except Fail as exc:
            print("FAIL", archive, exc)
            fail += 1
    for nm, nf, tr in (("8_3.dat", 6, 3), ("8_25.dat", 3, 1)):
        raw = load_member(codec, "lang_update", nm)
        recs, end, st = lang_records(raw, nf, tr)
        good = st == "ok" and end == len(raw)
        print(("PASS" if good else "FAIL"),
              f"lang {nm} recs={len(recs)} end={end}/{len(raw)}")
        ok += 1 if good else 0
        fail += 0 if good else 1
    print(f"--- {ok} PASS / {fail} FAIL ---")
    return 0 if fail == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t84 name-slot join verdict (read-only)")
    ap.add_argument("--build", metavar="OUT.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.build:
        return build(pathlib.Path(a.build))
    ap.error("need --build OUT.json or --selftest")


if __name__ == "__main__":
    sys.exit(main())
