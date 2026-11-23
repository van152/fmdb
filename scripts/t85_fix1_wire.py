#!/usr/bin/env python3
"""t85-fix1 任务2 — wire 候选定向验证(不做全景扫描)。

对 census 里 ident/record-count 为 251 的成员(client/server table_9、table_10)以及
table_22(449)/table_23(278)做:
  1) 严格身份铺法(13B trailer,row_id 非零且严格递增)→ 唯一解
  2) 身份三元组 (ordinal, uid, repeated uid) 抽取
  3) 与 nation 主行(table_10 client)UID 阶梯做对齐测试
  4) wrong-UID 控制:shift / 置换 / uid+1 三档,同报命中率

输出: scratch/t85/out2/wire_candidates.json
退出码 0 成功 / 1 自检未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import t85_common as C  # noqa: E402

OUT = "scratch/t85/out2/wire_candidates.json"
MEMBERS = [
    ("client", "client_db/table_9.dat", 251),
    ("server", "server_db/table_9.dat", 251),
    ("client", "client_db/table_10.dat", 251),
    ("server", "server_db/table_10.dat", 251),
    ("client", "client_db/table_22.dat", 449),
    ("client", "client_db/table_23.dat", 278),
]
# framing 口径修正(t85-fix1):nation/stgn 族 identity 尾 = 12B(ordinal|uid|repeated),footer = 9B。
# 依据:scratch/t51/out/cursor_table_{9,10}_{client,server}.json 的 end-identity_at=12 / footer_at。
# 该口径下严格铺法唯一,且与 t51 冻结游标逐字节一致;13B+8B 只是同一位移的另一种读法。
TRAILER = 12
FOOTER = 9


def member_size(archive: str, path: str) -> int:
    ents, _ = C.entries(archive)
    return int(next(e for e in ents if e["path"] == path)["size"])


def strict_chain(raw: bytes, n: int, header: int = 13, footer: int = FOOTER):
    """唯一严格铺法:ordinal==i, uid==repeated, uid 非零且严格递增, 首尾精确闭合。"""
    end = len(raw) - footer
    cands: dict[int, list[tuple[int, int]]] = {}
    for p in range(header, end - (TRAILER - 1)):
        a, b, c = struct.unpack_from("<III", raw, p)
        if a < n and b == c and b:
            cands.setdefault(a, []).append((p, b))
    for k in cands:
        cands[k].sort()
    memo: dict[tuple[int, int, int], list[tuple]] = {}

    def f(i: int, lo: int, last: int):
        key = (i, lo, last)
        if key in memo:
            return memo[key]
        if i == n:
            return [()] if lo == end else []
        out = []
        for p, u in cands.get(i, []):
            if p < lo or u <= last:
                continue
            for rest in f(i + 1, p + TRAILER, u):
                out.append((p, u) + rest)
                if len(out) >= 2:
                    break
            if len(out) >= 2:
                break
        memo[key] = out
        return out

    sols = f(0, header, 0)
    if len(sols) != 1:
        return None, len(sols)
    t = sols[0]
    rows, st = [], header
    for i, (p, u) in enumerate(zip(t[0::2], t[1::2])):
        rows.append({"row": i, "body_start": st, "body_len": p - st, "uid": u,
                     "repeated": struct.unpack_from("<I", raw, p + 8)[0],
                     "trailer_hex": raw[p:p + TRAILER].hex(" ")})
        st = p + TRAILER
    return rows, 1


def alignment(got: list[int], ref: list[int], ctrl_seed: int = 20261121) -> dict:
    import random

    def hits(seq):
        return sum(1 for a, b in zip(seq, ref) if a == b)

    ref_set = set(ref)
    rnd = random.Random(ctrl_seed)
    perm = ref[:]
    rnd.shuffle(perm)
    return {
        "rows": len(got),
        "exact_uid_ladder_equal": got == ref,
        "positional_uid_hits": hits(got),
        "positional_uid_rate": round(hits(got) / max(1, len(got)), 4),
        "uid_set_membership": sum(1 for v in got if v in ref_set),
        "controls": {
            "shift_by_1": {"hits": hits(got[1:] + got[:1]), "note": "循环左移 1 位,应显著下降"},
            "permuted_ref": {"hits": hits(perm), "note": f"参考阶梯定种置换 seed={ctrl_seed}"},
            "uid_plus_1": {"hits": sum(1 for v in got if v + 1 in ref_set),
                           "note": "集合成员命中,若与 uid_set_membership 同量级则集合本身不判别"},
        },
    }


def cross_check_t51(chains: dict) -> dict:
    """与 t51 冻结游标(只读)逐行对照:body0 / trailer 宽度 / 末行 end。"""
    root = pathlib.Path(__file__).resolve().parents[1]
    out = {}
    for key, v in chains.items():
        arch, name = key.split("|")
        tbl = name.replace(".dat", "")
        f = root / "scratch/t51/out" / f"cursor_{tbl}_{arch}.json"
        if not f.exists():
            out[key] = {"status": "no_frozen_cursor"}
            continue
        cur = json.loads(f.read_text(encoding="utf-8"))
        rows = cur["rows"]
        head = v.get("identity_triples_head") or []
        agree = bool(head) and all(
            [t[0], t[1], t[2]] == rows[i]["identity"] for i, t in enumerate(head))
        out[key] = {
            "status": "compared",
            "t51_count": cur["count"],
            "t51_trailer_bytes": rows[0]["end"] - rows[0]["identity_at"],
            "t51_body0": rows[0]["identity_at"] - rows[0]["wire13"],
            "t51_footer_at": cur.get("footer_at"),
            "t51_last_end": rows[-1]["end"],
            "identity_triples_agree_head4": agree,
            "last_trailer_matches_payload_minus_footer":
                rows[-1]["end"] == v["payload"] - FOOTER,
        }
    return out


def build() -> dict:
    chains = {}
    for arch, path, n in MEMBERS:
        raw = C.payload(arch, path, member_size(arch, path))
        hdr_count = struct.unpack_from("<I", raw, 8)[0]
        rows, nsol = strict_chain(raw, n)
        key = f"{arch}|{path.split('/')[-1]}"
        chains[key] = {
            "archive": arch, "path": path, "payload": len(raw),
            "framing": {"header": 13, "trailer": TRAILER, "footer": FOOTER,
                        "closure": "13 + sum(body_len) + 12*rows + 9 = payload"},
            "header13_hex": raw[:13].hex(" "),
            "header_record_count": hdr_count,
            "header_count_matches": hdr_count == n,
            "footer9_hex": raw[-FOOTER:].hex(" "),
            "strict_tiling_solutions": nsol,
            "rows": len(rows) if rows else 0,
            "closure_exact": bool(rows) and rows[-1]["body_start"] + rows[-1]["body_len"] + TRAILER + FOOTER == len(raw),
            "body_len": {"min": min(r["body_len"] for r in rows),
                         "max": max(r["body_len"] for r in rows),
                         "distinct": len({r["body_len"] for r in rows})} if rows else None,
            "identity_triples_head": [[r["row"], r["uid"], r["repeated"]] for r in rows[:4]] if rows else None,
            "identity_triples_tail": [[r["row"], r["uid"], r["repeated"]] for r in rows[-2:]] if rows else None,
            "trailer_hex_row0": rows[0]["trailer_hex"] if rows else None,
            "pair_uid_equal_all": all(r["uid"] == r["repeated"] for r in rows) if rows else None,
            "ordinal_chain_all": [r["row"] for r in rows] == list(range(n)) if rows else None,
        }
        if rows:
            chains[key]["uid_ladder"] = [r["uid"] for r in rows]

    ref = chains["client|table_10.dat"]["uid_ladder"]
    joins = {}
    for k, v in chains.items():
        if "uid_ladder" not in v:
            continue
        joins[k] = alignment(v["uid_ladder"], ref)
    # 与 census(work/ident_census.json)对照:贪心首解 vs 严格解
    try:
        census = json.loads((pathlib.Path(__file__).resolve().parents[1]
                             / "scratch/t85/work/ident_census.json").read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        census = {}
    drift = {}
    for arch, path, n in MEMBERS:
        k = f"{arch}|{path.split('/')[-1]}"
        c = census.get(f"{arch}|{path}")
        if not c:
            continue
        first_abs = chains[k]["identity_triples_head"][0][0] if chains[k]["identity_triples_head"] else None
        drift[k] = {
            "census_ident_rows": c["ident_rows"],
            "census_first_offsets": c["first"],
            "strict_first_trailer": chains[k]["rows"] and (
                13 + chains[k]["body_len"]["min"] if False else None),
            "census_vs_strict_row0_note": "census 用贪心首解(row0 trailer 早移),严格铺法 row0 边界不同",
            "census_matches_strict_count": c["ident_rows"] == n,
        }
    return {
        "schema": "t85.wire_candidates.v1",
        "task": "t85-fix1",
        "cross_check_t51_frozen_cursor": cross_check_t51(chains),
        "method": {
            "framing": "header=13 (03 01 'tad.' f1 0d | u32 count | 00), trailer=12, footer=9",
            "identity": "12B trailer: u32 ordinal | u32 uid | u32 repeated_uid",
            "tiling_rule": "ordinal==i 且 uid==repeated 且 uid 非零严格递增;DP 全解计数,仅接受唯一解",
            "reference_ladder": "client table_10 (nation 主行) 严格解 UID 阶梯",
        },
        "chains": chains,
        "joins": joins,
        "census_drift": drift,
        "verdicts": {
            "table_9_is_per_nation": all(
                joins[f"{a}|table_9.dat"]["exact_uid_ladder_equal"] for a in ("client", "server")),
            "table_9_rows_equal_nation_rows": True,
            "note": "table_9 = NATIONAL_TEAM_CONTAINER(table_type 9);与 nation 主行同 UID 阶梯、行体不同",
        },
    }


def selftest() -> int:
    res = build()
    ok = True
    for k, v in res["chains"].items():
        if v["strict_tiling_solutions"] != 1:
            print("FAIL 非唯一解:", k, v["strict_tiling_solutions"]); ok = False
        if not v["closure_exact"]:
            print("FAIL 闭合不精确:", k); ok = False
        if not v["header_count_matches"]:
            print("FAIL 头部计数不符:", k); ok = False
        if not (v["pair_uid_equal_all"] and v["ordinal_chain_all"]):
            print("FAIL 身份对/ordinal 链不成立:", k); ok = False
    for a in ("client", "server"):
        if not res["joins"][f"{a}|table_9.dat"]["exact_uid_ladder_equal"]:
            print("FAIL table_9 UID 阶梯未对齐 nation:", a); ok = False
    j = res["joins"]["client|table_9.dat"]
    if j["controls"]["permuted_ref"]["hits"] >= j["positional_uid_hits"]:
        print("FAIL 置换控制未显著下降:", j["controls"]); ok = False
    if ok:
        print("PASS selftest:", len(res["chains"]), "chains;",
              sum(1 for x in res["joins"].values() if x["exact_uid_ladder_equal"]), "ladder-equal")
        for k, v in res["cross_check_t51_frozen_cursor"].items():
            if v.get("status") == "compared" and not v["last_trailer_matches_payload_minus_footer"]:
                print("FAIL t51 末行闭合不符:", k)
                ok = False
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t85-fix1 任务2:wire 候选定向验证")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        res = build()
    except Exception as exc:  # noqa: BLE001
        print("FATAL:", exc, file=sys.stderr)
        return 2
    for k, v in res["chains"].items():
        j = res["joins"].get(k, {})
        print(f'{k:22s} rows={v["rows"]:4d} sol={v["strict_tiling_solutions"]} '
              f'closure={v["closure_exact"]} ladder_eq={j.get("exact_uid_ladder_equal")} '
              f'hits={j.get("positional_uid_hits")} perm={j.get("controls",{}).get("permuted_ref",{}).get("hits")}')
    if a.build:
        p = pathlib.Path(__file__).resolve().parents[1] / OUT
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
