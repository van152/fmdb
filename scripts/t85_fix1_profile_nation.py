#!/usr/bin/env python3
"""t85-fix1 任务3 — 命中候选的结构 profile(nation 侧)。

对 table_9 / table_10(client/server)给:
  * 头 13B / 尾 12B / footer 9B 的三段闭合证据
  * 行体长度分布 + 行体首段字节域(逐 offset 的 distinct/range)
  * 与 t75 nation 槽位 body_relative 的 getter 域对照(只比对,不新增语义)
  * 行内条目文法:两轮探测结论原样保留(未定 → held + 首反例)

输出: scratch/t85/out2/profile_nation.json
退出码 0 成功 / 1 自检未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import t85_common as C  # noqa: E402
from t85_fix1_wire import FOOTER, TRAILER, member_size, strict_chain  # noqa: E402

OUT = "scratch/t85/out2/profile_nation.json"
TARGETS = [("client", "table_9", 251), ("server", "table_9", 251),
           ("client", "table_10", 251), ("server", "table_10", 251)]


def bodies(raw: bytes, rows: list[dict]) -> list[bytes]:
    out, st = [], 13
    for r in rows:
        end = r["body_start"] + r["body_len"]
        out.append(raw[st:end])
        st = end + TRAILER
    return out


def lane_domain(bs: list[bytes], width: int, limit: int = 40) -> list[dict]:
    """行体前 limit 字节逐 offset 的取值域(只报统计,不赋语义)。"""
    out = []
    for off in range(0, limit):
        vals = [int.from_bytes(b[off:off + 1], "little") for b in bs if len(b) > off]
        if not vals:
            continue
        u16 = [int.from_bytes(b[off:off + 2], "little") for b in bs if len(b) > off + 1]
        out.append({
            "offset": off,
            "u8_distinct": len(set(vals)),
            "u8_min": min(vals), "u8_max": max(vals),
            "u8_top": collections.Counter(vals).most_common(3),
            "u16_distinct": len(set(u16)),
        })
    return out


def item_grammar_probe(bs: list[bytes]) -> dict:
    """两轮探测:9B 条目网格(严格递增 u32 key + 尾部 0)。第二轮未定即 held。"""
    rounds = []
    for tag, shift0 in (("round1_raw", False), ("round2_row0_shift1", True)):
        work = [bs[0][1:]] + bs[1:] if shift0 else bs
        hits, counts = 0, []
        for b in work:
            best = None
            for s in range(0, min(64, len(b))):
                k = (len(b) - s) // 9
                if k < 2:
                    continue
                keys = [struct.unpack_from("<I", b, s + 9 * j)[0] for j in range(k)]
                if not all(b[s + 9 * j + 8] == 0 for j in range(k)):
                    continue
                if not all(keys[j] < keys[j + 1] for j in range(k - 1)):
                    continue
                if best is None or k > best[1]:
                    best = (s, k)
            if best:
                hits += 1
                counts.append(best[1])
        rounds.append({"round": tag, "rows_with_grid": hits, "rows": len(work),
                       "rate": round(hits / max(1, len(work)), 4),
                       "item_counts_head": counts[:8]})
    # 首反例:第一行无法铺成网格
    first_fail = None
    for i, b in enumerate(bs):
        ok = False
        for s in range(0, min(64, len(b))):
            k = (len(b) - s) // 9
            if k < 2:
                continue
            keys = [struct.unpack_from("<I", b, s + 9 * j)[0] for j in range(k)]
            if all(b[s + 9 * j + 8] == 0 for j in range(k)) and \
               all(keys[j] < keys[j + 1] for j in range(k - 1)):
                ok = True
                break
        if not ok:
            first_fail = {"row": i, "body_len": len(b), "body_head_hex": b[:24].hex(" ")}
            break
    return {
        "rounds": rounds,
        "verdict": "held_no_item_grammar",
        "reason": "两轮探测均未取得全表一致的条目网格;不做第三轮猜测",
        "first_counterexample": first_fail,
    }


def ordinal_lane(bs: list[bytes]) -> dict:
    """行体内是否存在 ordinal 备份轨(排除 framing 污染)。"""
    hits = {}
    for off in range(0, 24):
        eq = sum(1 for i, b in enumerate(bs) if len(b) > off and b[off] == (i & 0xFF))
        if eq > len(bs) // 2:
            hits[off] = eq
    return {"lanes_matching_ordinal_lowbyte": hits, "rows": len(bs)}


def build() -> dict:
    xref = C.jload("scratch/t75/out/xref_reverse.json")
    slots = [x for x in xref["slots"] if x["table"] == "nation"]
    res = {"schema": "t85.profile_nation.v1", "task": "t85-fix1", "members": {}}
    for arch, name, n in TARGETS:
        path = f"{arch}_db/{name}.dat"
        raw = C.payload(arch, path, member_size(arch, path))
        rows, nsol = strict_chain(raw, n)
        bs = bodies(raw, rows)
        lens = [len(b) for b in bs]
        key = f"{arch}|{name}"
        res["members"][key] = {
            "archive": arch, "path": path, "payload": len(raw),
            "framing": {"header": 13, "trailer": TRAILER, "footer": FOOTER,
                        "closure_ok": rows[-1]["body_start"] + rows[-1]["body_len"] + TRAILER + FOOTER == len(raw),
                        "header_hex": raw[:13].hex(" "),
                        "header_count": struct.unpack_from("<I", raw, 8)[0],
                        "footer_hex": raw[-FOOTER:].hex(" ")},
            "rows": len(rows), "strict_tiling_solutions": nsol,
            "uid_ladder_head": [r["uid"] for r in rows[:5]],
            "uid_ladder_tail": [r["uid"] for r in rows[-2:]],
            "body_len": {"min": min(lens), "max": max(lens),
                         "mean": round(sum(lens) / len(lens), 2),
                         "distinct": len(set(lens)),
                         "sum": sum(lens)},
            "ordinal_lane": ordinal_lane(bs),
            "item_grammar": item_grammar_probe(bs),
            "lane_domain_first32": lane_domain(bs, 1, 32),
        }
        # t75 getter 域对照(只在 t75 声明 rows==251 的槽上做口径自检)
        # 口径:legacy14 origin = body_start+1(跳 1 字节 selector),依据 t51 cursor 的 wire13/legacy14 双字段。
        # 条件覆盖(rows<251)与集合宽槽(w>8 或 t75 未记 distinct)不参与比对,原样标注。
        LEGACY = 1
        cmp_slots = []
        for s in slots:
            a = s["archives"].get(arch) or {}
            ref = a.get("first")
            t75_rows = a.get("rows") or 0
            t75_distinct = a.get("distinct")
            if not ref or t75_rows == 0:
                cmp_slots.append({"slot": s["slot"],
                                  "status": "no_data_in_this_archive",
                                  "t75_rows": t75_rows})
                continue
            br, w = ref["body_relative"], ref["width"]
            vals = []
            for r in rows:
                p = r["body_start"] + LEGACY + br
                if p + w <= r["body_start"] + r["body_len"]:
                    vals.append(int.from_bytes(raw[p:p + w], "little"))
            entry = {
                "slot": s["slot"], "object_displacement": s["object_displacement"],
                "grammar_ref": s.get("grammar_ref"),
                "body_relative": br, "width": w, "origin": "legacy14 = body_start+1",
                "recomputed_rows": len(vals), "recomputed_distinct": len(set(vals)),
                "recomputed_min": min(vals) if vals else None,
                "recomputed_max": max(vals) if vals else None,
                "t75_rows": t75_rows, "t75_distinct": t75_distinct,
                "t75_min": a.get("minimum"), "t75_max": a.get("maximum"),
            }
            if t75_rows != n:
                entry["status"] = "conditional_coverage_not_compared"
            elif t75_distinct is None or w > 8:
                entry["status"] = "collection_wide_no_distinct_recorded"
            else:
                entry["status"] = ("domain_reproduced" if len(set(vals)) == t75_distinct
                                   else "domain_mismatch")
            cmp_slots.append(entry)
        res["members"][key]["t75_nation_slot_domain"] = cmp_slots
    return res


def selftest() -> int:
    res = build()
    ok = True
    for k, v in res["members"].items():
        if v["strict_tiling_solutions"] != 1:
            print("FAIL 非唯一解:", k); ok = False
        if not v["framing"]["closure_ok"]:
            print("FAIL 闭合:", k); ok = False
        if v["item_grammar"]["verdict"] != "held_no_item_grammar":
            print("FAIL 条目文法应保持 held:", k); ok = False
        for s in v["t75_nation_slot_domain"]:
            if s.get("status") == "domain_mismatch":
                print(f'FAIL 取值域未复现 {k} {s["slot"]}: {s["recomputed_distinct"]} vs {s["t75_distinct"]}')
                ok = False
    if ok:
        print("PASS selftest:", len(res["members"]), "members profiled")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t85-fix1 任务3:nation 侧结构 profile")
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
    for k, v in res["members"].items():
        bl, ig = v["body_len"], v["item_grammar"]
        print(f'{k:22s} rows={v["rows"]:4d} bodylen {bl["min"]}..{bl["max"]} '
              f'grid={ig["rounds"][0]["rows_with_grid"]}/{ig["rounds"][0]["rows"]} '
              f'verdict={ig["verdict"]}')
    if a.build:
        p = pathlib.Path(__file__).resolve().parents[1] / OUT
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
