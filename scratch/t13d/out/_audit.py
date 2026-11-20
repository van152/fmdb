#!/usr/bin/env python3
"""t13d 旁路:四张 server 表的候选实体数据侧诊断(只读;产物只写 scratch/t13d/out/)。

输入:fm24_dump.py 导出的 t22/t30/t34/t49 CSV(raw_hex 每行一字节串)。
输出:quick_audit.md + audit.json。

判据口径
--------
* 行数量级比对用**本仓既有 L1/L2 基线**(club=server table_3 84,259;person=792,149;
  player≈7万;nation=251),基线来源逐条写进 audit.json 的 baselines。
* "量级吻合"只表示行数落在该实体基数附近,**不等于**实体确认。
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch/t13d/out"
FF = 0xFFFFFFFF

BASELINES = {
    "club": {"rows": 84259, "source": "scratch/t05/COVERAGE.json server table_3; scratch/t02/inbox/club_v2/output.json",
             "note": "任务书写作\"club 约几千\",与仓内基线 84,259 冲突;两种口径都保留"},
    "club_low_thousands": {"rows": 3000, "source": "任务书口头口径(\"club 主表行数约几千\")",
                           "note": "仅作敏感性对照,不是证据"},
    "player": {"rows": 72473, "source": "任务书\"player 约 7 万\";量级口径", "note": "本表自身行数,非独立基数"},
    "nation": {"rows": 251, "source": "scratch/t05/COVERAGE.json client/server table_10 = 251"},
    "person": {"rows": 792149, "source": "任务书\"person 约 79 万\";与本表行数一致,量级口径"},
    "comp": {"rows": 7047, "source": "scratch/t05/COVERAGE.json server table_25"},
    "city": {"rows": 56293, "source": "scratch/t05/COVERAGE.json server table_2"},
}

TABLES = {
    22: {"csv": "t22.csv", "stride": 79, "candidates": ["club"],
         "cols": [0, 1, 3, 12]},
    30: {"csv": "t30.csv", "stride": 34, "candidates": ["player"],
         "cols": [0, 1, 10]},
    34: {"csv": "t34.csv", "stride": 44, "candidates": ["club", "nation"],
         "cols": [0, 1, 3, 4]},
    49: {"csv": "t49.csv", "stride": 36, "candidates": ["person"],
         "cols": [0, 8, 2]},
}


def load(p: pathlib.Path):
    with open(p, newline="", encoding="utf-8") as f:
        return [bytes.fromhex(r["raw_hex"]) for r in csv.DictReader(f)]


def u32(rows, off):
    return [int.from_bytes(r[off:off + 4], "little") for r in rows]


def u16(rows, off):
    return [int.from_bytes(r[off:off + 2], "little") for r in rows]


def colstat(rows, off, width=4):
    vals = u32(rows, off) if width == 4 else u16(rows, off)
    n = len(vals)
    live = [v for v in vals if v not in (0, FF)]
    cnt = collections.Counter(live)
    dom = {}
    for k, b in BASELINES.items():
        if k == "club_low_thousands":
            continue
        dom[k] = round(sum(1 for v in live if v < b["rows"]) / max(1, len(live)), 4)
    return {
        "u32_off": off, "u16_off": off,
        "distinct_live": len(cnt),
        "min_live": min(live) if live else None,
        "max_live": max(live) if live else None,
        "zero_ratio": round(sum(1 for v in vals if v == 0) / n, 4),
        "ff_ratio": round(sum(1 for v in vals if v == FF) / n, 4),
        "top5": [[v, c] for v, c in cnt.most_common(5)],
        "in_domain_of_candidate": dom,
    }


def identity_probe(rows, stride):
    """找行内 u32 == 行号 / 行号+1 的偏移(通用行记录尾块)。"""
    n = len(rows)
    hits = []
    for o in range(0, min(stride, 64) - 3):
        vals = u32(rows, o)
        for delta in (0, 1, 2):
            eq = sum(1 for i, v in enumerate(vals) if v == i + delta)
            if eq >= 0.99 * n:
                hits.append({"off": o, "delta": delta, "hits": eq, "of": n})
    return hits


def year_probe(rows, stride, lo=1900, hi=2035):
    out = []
    n = len(rows)
    for o in range(0, stride - 1):
        vals = u16(rows, o)
        ok = sum(1 for v in vals if lo <= v <= hi)
        if ok >= 0.9 * n:
            live = [v for v in vals if lo <= v <= hi]
            out.append({"u16_off": o, "ratio": round(ok / n, 4),
                        "distinct": len(set(live)), "min": min(live), "max": max(live)})
    return out


def date_probe(rows, stride):
    """server 侧日期文法:u32 = lo16(日/年内序号 0..366) | hi16(年 1900..2035)。"""
    out = []
    n = len(rows)
    for o in range(0, stride - 3):
        vals = u32(rows, o)
        ok = 0
        for v in vals:
            d, y = v & 0xFFFF, v >> 16
            if y in (0, 0xFFFF):
                continue
            if 1900 <= y <= 2035 and d <= 366:
                ok += 1
        live = sum(1 for v in vals if (v >> 16) not in (0, 0xFFFF))
        if live and ok / live >= 0.95:
            ys = [(v >> 16) for v in vals if 1900 <= (v >> 16) <= 2035]
            out.append({"u32_off": o, "ratio_of_live": round(ok / live, 4),
                        "year_min": min(ys), "year_max": max(ys), "year_distinct": len(set(ys)),
                        "day_max": max((v & 0xFFFF) for v in vals)})
    return out


def domain_refs(rows, stride, identity_offs=()):
    """扫全行找"整列都落在某实体 ID 空间内"的 u32 —— 说明本表引用该实体。

    注意语义边界:这是**引用**证据,不是本表实体证据。行号恒等列(identity_offs)排除,
    否则 0..n-1 < 7047 会对 comp 域造成假阳。
    """
    dom = [("nation", 251), ("comp", 7047), ("club", 84259), ("city", 56293)]
    id_offs = {h["off"] - h["delta"] for h in identity_offs} | {h["off"] for h in identity_offs}
    out = []
    for o in range(0, stride - 3):
        if o in id_offs:
            continue
        raw = u32(rows, o)
        has_null = any(v == FF for v in raw)
        vals = [v for v in raw if v != FF]
        if not vals:
            continue
        for name, lim in dom:
            if all(v < lim for v in vals):
                out.append({"u32_off": o, "domain": name, "domain_size": lim,
                            "distinct": len(set(vals)), "min": min(vals), "max": max(vals),
                            "has_null": has_null,
                            "note": "含 null(0xFFFFFFFF)" if has_null else "整列无 null"})
                break
    return out


def name_probe(rows):
    """行内是否有 >=5 字节可打印且含字母的连续串(粗略);用于说明"表内无姓名文本"。"""
    hit = 0
    for r in rows:
        best = 0
        cur = 0
        alpha = False
        for b in r:
            if 32 <= b < 127:
                cur += 1
                if 65 <= b <= 90 or 97 <= b <= 122:
                    alpha = True
            else:
                if cur >= 5 and alpha:
                    best = max(best, cur)
                cur = 0
                alpha = False
        if cur >= 5 and alpha:
            best = max(best, cur)
        if best >= 5:
            hit += 1
    return {"rows_with_name_like_ascii": hit, "of": len(rows)}


def analyse(tid, spec):
    p = OUT / spec["csv"]
    rows = load(p)
    n = len(rows)
    st = spec["stride"]
    identity_rows = identity_probe(rows, st)
    res = {
        "table_type": tid,
        "csv": f"scratch/t13d/out/{spec['csv']}",
        "rows_dumped": n,
        "stride": st,
        "candidates_from_t11": spec["candidates"],
        "cols": [dict({"col": c}, **colstat(rows, c * 4)) for c in spec["cols"]],
        "identity_rows": identity_rows,
        "domain_refs": domain_refs(rows, st, identity_rows),
        "date_cols": date_probe(rows, st),
        "year_cols": year_probe(rows, st),
        "name_probe": name_probe(rows[:5000]),
    }
    # 行数量级判定
    verdicts = []
    for cand in spec["candidates"]:
        b = BASELINES[cand]["rows"]
        ratio = n / b
        if 0.8 <= ratio <= 1.25:
            v = "量级吻合"
        elif ratio < 0.2 or ratio > 5:
            v = "量级不吻合"
        else:
            v = "无法判断"
        verdicts.append({"entity": cand, "baseline_rows": b, "ratio": round(ratio, 3), "verdict": v})
    if len({x["verdict"] for x in verdicts}) == 1:
        res["magnitude_verdict"] = verdicts[0]["verdict"]
    else:
        res["magnitude_verdict"] = "混合:" + "/".join(f"{x['entity']}={x['verdict']}" for x in verdicts)
    res["magnitude_detail"] = verdicts
    # 敏感性:若按任务书"club 约几千"口径
    if "club" in spec["candidates"]:
        res["sensitivity_club_3000"] = round(n / 3000, 3)
    return res


CONCLUSIONS = {
    22: ("449 行相对 club 基线 84,259 只占 0.53%,相对 nation 251 也差 79%:两种量级都不吻合,"
         "数据侧不支持把 t22 当作 club 主表。但 c0 的 362 个非哨兵值全部落在 [86, 82403] ⊂ club ID 空间,"
         "且行内无任何姓名字符串,更像是\"按 club 引用 + 日期\"的子表(每 club 平均 1.4 行)。"),
    30: ("72,473 行与 player 的 7 万量级吻合(比值 1.000),且第 10/14 字节为 1900..2024 的年份列(birth-like)、"
         "c1 为 0..114 的国家域引用、c5..c7 每行唯一。数据侧与 player 不矛盾;但 player 基线本身取自 7 万量级口径,"
         "不是独立基数,量级吻合不构成确认。"),
    34: ("7,115 行:相对 club 基线 84,259 差 12 倍(不吻合),相对 nation 251 差 28 倍(不吻合)。"
         "c3/c4 的值域 ⊆ [0,251) 但只有 81/54 个不同值 —— 这形态是\"7,115 行各自引用一个国家\","
         "不是\"每国一行\";故 nation 说法在数据侧也不成立。真正的结构像 (c0 ∈ comp 域 7,047 / 89 个值, "
         "c1 ∈ club 域 84,259 / 207 个值, 两组 1900..2023 年份) 的多行历史表。两种候选都不吻合,判无法判断。"),
    49: ("792,149 行与 person 的 79 万量级吻合(比值 1.000),c7/off23 每行唯一(行号恒等),"
         "u16@2 为 1900..2024 年份列,c8 为 3,094 个 256 行一组的连续分块(非身份键)。"
         "数据侧与 person 不矛盾;同样属量级口径,不构成确认。"),
}


def to_md(audit):
    L = []
    L.append("# t13d 旁路:四张 server 表的候选实体数据侧诊断\n")
    L.append("> 性质:**旁路交叉检查**,只做量级与列形态比对;实体裁决归主线锚点。"
             "本文所有\"量级吻合\"均**不表示实体确认**。\n")
    L.append(f"数据来源:`scripts/fm24_dump.py --archive server --table N` 只读导出到 "
             f"`scratch/t13d/out/t{{22,30,34,49}}.csv`;分析脚本 `scratch/t13d/out/_audit.py`。\n")
    L.append("基线口径(逐条见 `audit.json.baselines`):club = server table_3 **84,259**(L1 闭合,"
             "`scratch/t05/COVERAGE.json`);nation = **251**;person/player 用任务书的 79 万 / 7 万量级。"
             "**注意**:任务书写\"club 主表行数约几千\",与仓内 84,259 冲突,下表同时给出两种口径的敏感性。\n")
    L.append("---\n")
    for t in audit["tables"]:
        tid = t["table_type"]
        L.append(f"## table_{tid} — {t['rows_dumped']:,} 行 × {t['stride']} B,候选 "
                 f"{'/'.join(t['candidates_from_t11'])}\n")
        L.append(f"**量级判断:{t['magnitude_verdict']}**\n")
        L.append("| 候选 | 基线行数 | 本表/基线 | 判定 |")
        L.append("|---|---:|---:|---|")
        for d in t["magnitude_detail"]:
            L.append(f"| {d['entity']} | {d['baseline_rows']:,} | {d['ratio']} | {d['verdict']} |")
        if "sensitivity_club_3000" in t:
            L.append(f"\n敏感性:若按任务书\"club 约几千\"(取 3,000),比值 = {t['sensitivity_club_3000']}。")
        L.append("\n最有信息量的列(u32 小端切列;live = 剔除 0 与 0xFFFFFFFF 后):\n")
        L.append("| 列 | u32@ | distinct(live) | min..max(live) | 0 占比 | FF 占比 | top-3 |")
        L.append("|---|---:|---:|---|---:|---:|---|")
        for c in t["cols"]:
            top = ", ".join(f"{v}×{n}" for v, n in c["top5"][:3])
            L.append(f"| c{c['col']} | +{c['u32_off']} | {c['distinct_live']:,} | "
                     f"{c['min_live']}..{c['max_live']} | {c['zero_ratio']} | {c['ff_ratio']} | {top} |")
        if t["year_cols"]:
            ys = "; ".join(f"u16@{y['u16_off']} = {y['min']}..{y['max']} "
                           f"({y['distinct']} 值, {y['ratio']:.0%} 落在 1900..2035)" for y in t["year_cols"])
            L.append(f"\n年份型列:{ys}")
        if t["identity_rows"]:
            idh = "; ".join(f"u32@{h['off']} == row{'+'+str(h['delta']) if h['delta'] else ''} "
                            f"({h['hits']}/{h['of']})" for h in t["identity_rows"])
            L.append(f"\n行号恒等块:{idh} —— 说明行是按父实体顺序排列的定长槽,行内另有小整数计数器/标志位副本,"
                     "四张表共用同一行尾文法(非本表身份 ID)。")
        else:
            L.append("\n行号恒等块:未检出。")
        np_ = t["name_probe"]
        L.append(f"\n姓名文本探针:前 {np_['of']:,} 行中带 >=5 字节字母串的行 = "
                 f"{np_['rows_with_name_like_ascii']}(FM 姓名可能走独立 name 表,故此条只作弱旁证)。")
        L.append(f"\n**结论(数据侧,一句):**{t['conclusion']}\n")
        L.append("---\n")
    L.append("## 交叉注意\n")
    for c in audit["caveats"]:
        L.append(f"- {c}")
    L.append("")
    return "\n".join(L)


CAVEATS = [
    "t34 的 `fm24_dump.py` 导出会失败:`load_payload` 取 offset 后 64 B 内**第一个** zstd magic,"
    "而 table_34 在 +9 处有一个解出 12 B 的伪帧(真帧在 +34)。旁路用 `_dump34.py` 枚举候选帧、"
    "取能闭合 14+7115*44+8 = 313,082 的那个重导;`scripts/fm24_dump.py` 本身未改动(只读)。"
    "建议主线修 `load_payload` 的帧校验(加 payload 闭合/长度断言),否则任意表都可能静默取到伪帧。",
    "四条\"量级吻合\"都不是独立基数:player/person 的 7 万/79 万直接取自本表行数的量级,"
    "只有 club 84,259(server table_3)与 nation 251(table_10)是仓内可复核的独立基线。",
    "四张表行内均无姓名文本,无法用\"样例姓名\"做实体侧证;姓名判据不适用于 server 侧这些表。",
    "c0/t22 全部落在 club ID 域、c1/t34 全部落在 club ID 域,只能说明\"引用了该实体\","
    "不能说明本表实体是该实体 —— 这是本次诊断里最容易误读的一处。",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(OUT / "audit.json"))
    ap.add_argument("--md", default=str(OUT / "quick_audit.md"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        rows = [i.to_bytes(4, "little") + b"\x00" * 4 for i in range(3)]
        cs = colstat(rows, 0)
        assert cs["distinct_live"] == 2, cs          # 0 视为哨兵被剔除 → {1,2}
        assert cs["min_live"] == 1 and cs["max_live"] == 2, cs
        assert cs["zero_ratio"] == round(1 / 3, 4), cs
        assert colstat(rows, 4)["distinct_live"] == 0  # 全 0 列
        assert identity_probe(rows, 8) == [{"off": 0, "delta": 0, "hits": 3, "of": 3}], identity_probe(rows, 8)
        print("selftest ok")
        return 0

    audit = {"status": "ok", "task": "t13d quick audit", "baselines": BASELINES,
             "caveats": CAVEATS, "tables": []}
    missing = [s["csv"] for s in TABLES.values() if not (OUT / s["csv"]).exists()]
    for tid, spec in sorted(TABLES.items()):
        if not (OUT / spec["csv"]).exists():
            audit["tables"].append({"table_type": tid, "error": "csv missing"})
            continue
        t = analyse(tid, spec)
        t["conclusion"] = CONCLUSIONS[tid]
        audit["tables"].append(t)
    if missing or any("error" in t for t in audit["tables"]):
        audit["status"] = "partial"

    pathlib.Path(a.json).write_text(json.dumps(audit, ensure_ascii=False, indent=1), encoding="utf-8")
    pathlib.Path(a.md).write_text(to_md(audit), encoding="utf-8")
    print(f"wrote {a.json}\nwrote {a.md}")
    for t in audit["tables"]:
        if "error" in t:
            print("MISSING", t["table_type"])
            continue
        print(f"  table_{t['table_type']:<3d} {t['rows_dumped']:>7,} 行  {t['magnitude_verdict']}")
    return 0 if audit["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
