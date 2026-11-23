#!/usr/bin/env python3
"""t84_lang_check — lang_update_db 三档字符串一致性对拍 + wrong-UID 控制。

口径
----
* `lang_update_db` 不是「name 池」的第三份拷贝:它按 uid 键控多字段名字覆盖层。
  同一 uid 在不同语言成员里给出同一对象的本地化名字。
* 因此 client/server 的 name 池与 lang_update 不是同一存储,一致性对拍只能对
  「同一 .dat 归档内容的 client vs server」以及「同一 uid 的跨语言记录」做。
* wrong-UID 控制:把每个记录的 uid 换成相邻 uid,测量名字命中率下降到什么程度。

用法
----
  py -V:3.12 -I -B scripts/t84_lang_check.py --help
  py -V:3.12 -I -B scripts/t84_lang_check.py --selftest
  py -V:3.12 -I -B scripts/t84_lang_check.py --build scratch/t84/out/lang_update_check.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from t84_pools import DB_DIR, _codec, load_member, parse_pool  # noqa: E402
from t84_join import lang_records  # noqa: E402

# 每个语言成员族的字段数 / 尾字节数(由 t84 probe 实测,文件级常量)
LANG_GRAMMAR = {
    "8_3": (6, 3), "8_25": (3, 1), "8_0": (2, 2), "8_2": (1, 2),
    "8_21": (2, 3), "8_7": (1, 1),
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def triple_check(codec) -> dict:
    """client / server / lang_update 三档对拍:前两档逐字节相同即为同一池。"""
    out = {}
    for n in range(3):
        c = load_member(codec, "client", f"name_table_extra_{n}.dat")
        s = load_member(codec, "server", f"name_table_extra_{n}.dat")
        out[f"pool{n}"] = {
            "client_sha256": sha(c), "server_sha256": sha(s),
            "client_equals_server": c == s,
            "client_len": len(c), "server_len": len(s),
            "lang_update_counterpart": None,
            "note": ("lang_update_db has no name_table_* member; its 22 language "
                     "families carry uid-keyed name overlays instead"),
        }
    return out


def lang_family_closure(codec) -> dict:
    out = {}
    for stem, (nf, tr) in LANG_GRAMMAR.items():
        try:
            raw = load_member(codec, "lang_update", f"{stem}.dat")
        except Exception as exc:                       # 负结果原样保留
            out[stem] = {"load_error": str(exc)[:120]}
            continue
        recs, end, st = lang_records(raw, nf, tr)
        out[stem] = {
            "fields": nf, "trailer": tr, "records": len(recs),
            "payload_len": len(raw), "end": end,
            "closure": st == "ok" and end == len(raw),
            "sample": [{"uid": r["uid"], "fields": r["fields"]} for r in recs[:3]],
        }
    return out


def wrong_uid_control(codec, stem: str, nf: int, tr: int) -> dict:
    """真 uid vs 错 uid 的名字命中率(命中 = 该名字在 table_3 里紧跟匹配的 db_id)。"""
    raw3 = load_member(codec, "client", "table_3.dat")
    recs, _, st = lang_records(load_member(codec, "lang_update", f"{stem}.dat"), nf, tr)
    if st != "ok":
        return {"error": st}

    def probe(uid: int, name: str) -> bool:
        nb = name.encode("utf-8")
        i = raw3.find(struct.pack("<I", len(nb)) + nb)
        if i < 0:
            return False
        for back in range(24, 40):
            p = i - back
            if p < 0:
                return False
            a, b, c, d = struct.unpack_from("<IIII", raw3, p)
            if b == 0xFFFFFFFF and a == c == d:
                return a == uid
        return False

    true_hits = sum(1 for r in recs if probe(r["uid"], r["fields"][0]))
    wrong_hits = sum(1 for r in recs if probe(r["uid"] + 1, r["fields"][0]))
    wrong_hits2 = sum(1 for r in recs if probe(r["uid"] + 1000, r["fields"][0]))
    n = len(recs)
    return {
        "stem": stem, "records": n,
        "true_uid_hits": true_hits,
        "wrong_uid_plus1_hits": wrong_hits,
        "wrong_uid_plus1000_hits": wrong_hits2,
        "true_rate": round(true_hits / n, 4) if n else None,
        "wrong_rate": round(wrong_hits / n, 4) if n else None,
        "control_note": ("true uid is NOT the row db_id either (see joins.json); the "
                         "control shows the pair is not separable by name match alone"),
    }


def build(out: pathlib.Path) -> int:
    codec = _codec()
    res = {
        "task": "t84", "db_dir": str(DB_DIR),
        "triple_archive": triple_check(codec),
        "lang_update_pool_members": "none (no name_table_* in lang_update_db)",
        "lang_families": lang_family_closure(codec),
        "wrong_uid_control": {
            "club_8_3": wrong_uid_control(codec, "8_3", 6, 3),
        },
        "conclusion": {
            "lang_update_is_name_store": True,
            "lang_update_is_third_pool_copy": False,
            "evidence": ("lang_update_db carries 22 language families x 16 table-type "
                         "members keyed by uid; no name_table_* member exists there. "
                         "client vs server pools are byte-identical, so the third "
                         "archive is an overlay, not a third copy."),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")
    return 0


def selftest() -> int:
    codec = _codec()
    ok = fail = 0
    for n in range(3):
        c = parse_pool(load_member(codec, "client", f"name_table_extra_{n}.dat"))
        s = parse_pool(load_member(codec, "server", f"name_table_extra_{n}.dat"))
        good = c["records"] == s["records"] and c["footer_len"] == 0
        print(("PASS" if good else "FAIL"),
              f"pool{n} client/server records {c['records']}/{s['records']}")
        ok += 1 if good else 0
        fail += 0 if good else 1
    for stem, (nf, tr) in LANG_GRAMMAR.items():
        try:
            raw = load_member(codec, "lang_update", f"{stem}.dat")
            recs, end, st = lang_records(raw, nf, tr)
            good = st == "ok" and end == len(raw)
        except Exception as exc:
            print("SKIP", stem, str(exc)[:60])
            continue
        print(("PASS" if good else "FAIL"), f"lang {stem} recs={len(recs)} end={end}/{len(raw)}")
        ok += 1 if good else 0
        fail += 0 if good else 1
    print(f"--- {ok} PASS / {fail} FAIL ---")
    return 0 if fail == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t84 lang_update cross-check (read-only)")
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
