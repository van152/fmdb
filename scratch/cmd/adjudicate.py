"""阶段二 12 张已有候选表的锚点裁决(指挥官口径)。

原则:
- 投票只排序不裁决; 归属必须有独立于投票链的锚点。
- A 类 = exe 唯一 4CC 码(df=1 且语义自洽); B 类 = 行数与独立出处基数吻合;
  C 类 = 值域/语义推断, 单独不足以定案。
- 5 张零字段表(31/42/46/50/51)没有 A 类证据, 只给 candidate/negative。
产出: scratch/cmd/stage2_candidate_adjudication.json
"""
from __future__ import annotations
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

COMMON = {"duni", "rdui", "NDBC", "FDBC", "dbnm"}


def load(p):
    with (ROOT / p).open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    schema = load("scratch/t05/schema_inventory.json")["entities"]
    df = collections.Counter()
    owner = collections.defaultdict(list)
    name = {}
    for ent, blob in schema.items():
        for f in blob["fields"]:
            c = f.get("code")
            if c:
                df[c] += 1
                owner[c].append(ent)
                name[c] = f.get("name")
    cov = {}
    for r in load("scratch/t05/COVERAGE.json")["tables"]:
        if r.get("archive") == "server":
            cov[r["table_id"]] = r.get("count")
    naming = {r["type_id"]: r for r in load("scratch/t12/out/naming_result.json")["results"]}
    t11map = {e["type_id"]: e["schema_entity"] for e in load("scratch/t11/out/schema_map.json")["entities"]}

    # 指挥官裁决表: A 类锚点用 df=1 且语义自洽的码; 其余留 candidate。
    verdict = {
        22: dict(entity="club", level="A", tier="subtable", role="club 的球场/迁建属性集",
                 anchors=["Salt=Alternative Stadium(df=1,club)", "Scam=Stadium Rental Cash Amount(df=1,club)",
                          "Scpm=Is Potential Move(df=1,club)", "Slhm=Likelihood of Stadium Move(df=1,club)"],
                 note="449 行, 不是 stadium 主表(48413); 字段语义全为 club 拥有的球场计划, 与 t19(28 行)共享 S 码属同一类不同表"),
        30: dict(entity="player", level="A", tier="subtable", role="球员伤病/未来状态记录",
                 anchors=["futu=Future(df=1,player)", "inju=Injury(df=1,player)",
                          "pret=Prevents Training(df=1,player)", "seve=Severity(df=1,player)"],
                 note="72473 行 >> injury 主表 115, 故是 player 侧的伤病实例/状态表而非 injury 表"),
        31: dict(entity=None, level="negative", tier=None, role="零字段表",
                 anchors=[], note="t11 投给 club 但无任何命名字段、无 A 类证据; 37283 行与 club 主表 84259 不符, 不认可"),
        34: dict(entity="club", level="B", tier="subtable", role="俱乐部赛事历史(起止年/对手/结果)",
                 anchors=["tcop=Opposition(df=2,club+nation)", "mstn=Last Stage(df=2,club+nation)",
                          "edyr=End Year + styr=Start Year(df>=2,club+nation)"],
                 note="6 个码全部 club+nation 共有, 无 df=1 码, 故只有 B 类语义锚: tcop/mstn/edyr/styr 四码共同构成赛事历程; 7115 行与 club 主表 84259 不同, 是子表。不能算 resolved"),
        37: dict(entity="club", level="A", tier="subtable", role="俱乐部战绩/积分榜记录",
                 anchors=["draw=Games Drawn(df=1,club)", "gfor=Goals For(df=1,club)",
                          "gaga=Goals Against(df=1,club)", "poin=Points(df=1,club)", "wins=Games Won(df=1,club)"],
                 note="465712 行 = 俱乐部×赛季/赛事条目; 不是 club 主表(84259)"),
        42: dict(entity=None, level="negative", tier=None, role="零字段表",
                 anchors=[], note="t11 投给 club 但零字段; 17721 行无独立锚点, 不认可"),
        43: dict(entity="club", level="B", tier="subtable", role="转会付款分期",
                 anchors=["mths=Number Months(df=1,club)", "pyiv=Payment Interval(df=1,club)"],
                 note="535 行; 两个唯一码均为财务分期语义, 但与 club 主表的连接仅有码证据, 无行数独立核对"),
        46: dict(entity=None, level="negative", tier=None, role="零字段表",
                 anchors=[], note="7 行与 continent(7) 相同但无字段码; 行数吻合只是候选, 不足以定案"),
        49: dict(entity="person", level="A", tier="subtable", role="人员任职/对阵履历",
                 anchors=["ajob=Job(df=1,person)", "otea=Opposition(df=1,person)", "plac=Type(df=1,person)"],
                 note="792149 行; 3 个唯一码全属 person, 是典型履历子表; t11 投给 club 系投票污染, 已推翻"
                      " [E58补注: t49=792149 > person主库658011(E25/E32封口,E58/t13e), 多20.4%; "
                      "归属由df=1三码维持, 但'履历'语义与行数张力待解]"),
        50: dict(entity=None, level="negative", tier=None, role="零字段表",
                 anchors=[], note="45 行, 零字段; t11 投 club 无证据"),
        51: dict(entity=None, level="negative", tier=None, role="零字段表",
                 anchors=[], note="59 行, 零字段; t11 投 nation 无证据"),
        58: dict(entity=None, level="candidate", tier=None, role="零决定性字段表",
                 anchors=[], note="8 行; 只有 comp/divi/team 三个跨表码(df>=2), 无唯一码; person/club 皆可能, 不定案"),
    }

    rows = []
    for tid in sorted(verdict):
        v = verdict[tid]
        codes = sorted(set(c for a in naming[tid]["archives"].values() for f in a["fields"] for c in f["codes"]) - COMMON)
        uniq = [c for c in codes if df[c] == 1]
        rows.append({
            "table_type": tid, "archive": "server", "count": cov.get(tid),
            "status": "resolved" if v["level"].startswith("A") else ("candidate" if v["level"] in ("B", "candidate") else "negative"),
            "entity": v["entity"], "tier": v["tier"], "role": v["role"],
            "level": v["level"], "anchors": v["anchors"], "note": v["note"],
            "t11_vote": t11map.get(tid), "vote_overridden": (t11map.get(tid) != v["entity"]),
            "codes": codes, "df1_codes": uniq,
        })

    out = {
        "status": "complete",
        "method": "独立锚点优先: A=df1 且语义自洽的唯一 4CC 码; B=行数/独立出处; C=值域推断(单独不定案)。投票仅作排序。",
        "universal_codes_excluded": sorted(COMMON),
        "rows": rows,
        "summary": {
            "resolved": sum(1 for r in rows if r["status"] == "resolved"),
            "candidate": sum(1 for r in rows if r["status"] == "candidate"),
            "negative": sum(1 for r in rows if r["status"] == "negative"),
            "vote_overridden": sum(1 for r in rows if r["vote_overridden"]),
        },
    }
    p = ROOT / "scratch/cmd/stage2_candidate_adjudication.json"
    with p.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["summary"], ensure_ascii=False))
    for r in rows:
        print(f"t{r['table_type']:<3} {r['status']:<9} {str(r['entity']):<8} level={r['level']:<4} vote={str(r['t11_vote']):<8} {'OVERRIDE' if r['vote_overridden'] else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
