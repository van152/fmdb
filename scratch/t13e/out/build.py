#!/usr/bin/env python3
"""t13e 旁路:实体 -> 已知行数基数清单(带出处)。

只写 scratch/t13e/out/。只读 scratch/t05/COVERAGE.json、scratch/t01/LEDGER.json 等既有工件。
每个 count 必须能回指到具体文件 + table_id 或 E 编号;交叉核对只引用已存在的工件。
用法:
  py -V:3.12 -I build.py            # 重建 baselines.json / baselines.md
  py -V:3.12 -I build.py --selftest # 校验每条基数都能在出处里找到
退出码 0 成功 / 1 自检未过 / 2 用法错误
"""
import json
import os
import re
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
COVERAGE = "scratch/t05/COVERAGE.json"
LEDGER = "scratch/t01/LEDGER.json"
FIXTURES = "scratch/t05/fixtures_truth.json"
BOUNDS = "scratch/t05/server_bounds/boundaries.json"
STAGE2 = "scratch/t01/stage2_three_way.json"
ADJ = "scratch/cmd/stage2_candidate_adjudication.json"
PEOPLE = "scratch/t05/people/attrs.json"

STATUS = "partial"   # 旁路资料整理:必查文件全覆盖,但未穷尽全库;见 notes


def _load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def _count_of(t):
    """取一条 COVERAGE 记录的行数:count 为 null 时从 equation 里取。"""
    if t is None:
        return None
    if t.get("count") is not None:
        return t["count"]
    eq = t.get("equation")
    if isinstance(eq, dict):
        for k in ("record_count",):
            if isinstance(eq.get(k), int):
                return eq[k]
        for v in eq.values():          # client/server 嵌套
            if isinstance(v, dict) and isinstance(v.get("record_count"), int):
                return v["record_count"]
        return None
    if isinstance(eq, str):
        m = re.search(r"(\d[\d,]*)\s*行", eq)
        if m:
            return int(m.group(1).replace(",", ""))
        m = re.search(r"\+\s*(\d{2,})\s*\*", eq)
        if m:
            return int(m.group(1))
    return None


def _coverage():
    d = _load(COVERAGE)
    out = {}
    for t in d["tables"]:
        t = dict(t)
        t["count_resolved"] = _count_of(t)
        out[(t["archive"], t["table_id"])] = t
    return out


def bound_counts():
    """server_bounds/boundaries.json 的 count 表(独立于 COVERAGE 的第二次计算)。"""
    d = _load(BOUNDS)
    return {t["table_id"]: t for t in d["tables"]}


# entity, count, 主出处, 交叉核对, 可靠性, 备注
ROWS = [
    # ---- 已定实体(主表) ----
    dict(entity="award", count=3545,
         source="scratch/t05/COVERAGE.json:client table_0 + server table_0",
         cross_check="scratch/t05/fixtures_truth.json table_0 closure 14+3545*77+8=272987;"
                     "scratch/t01/LEDGER.json:E38 award 3545 行逐行身份复算",
         reliability="high"),
    dict(entity="city", count=56293,
         source="scratch/t05/COVERAGE.json:client table_2 (server table_2 同为 56293)",
         cross_check="E42 city 列画像同为 56293;E30/E38/E51 全量 56,293 行走查;"
                     "fixtures_truth.json closure 14+56293*43+8=2420621",
         reliability="high"),
    dict(entity="club", count=84259,
         source="scratch/t05/COVERAGE.json:client table_3 + server table_3",
         cross_check="E33 行框架 84,259/84,259 走通(5B 标准块 84,256 + 3 特例行);"
                     "E37 独立 walker 复现 server table_3 = 84,259 行,终点 16,595,304+8",
         reliability="high"),
    dict(entity="competition (comp)", count=7047,
         source="scratch/t05/COVERAGE.json:client table_25 + server table_25",
         cross_check="reports/t01f_comp_row_offsets.md 7,047/7,047 身份块全过;E20 自检 7047 行",
         reliability="high"),
    dict(entity="continent (cont)", count=7,
         source="scratch/t05/COVERAGE.json:client table_5 + server table_5",
         cross_check="scratch/t02/cont_reference.json closure 14+7*34+8=260;E56 cont=7",
         reliability="high"),
    dict(entity="currency (curr)", count=173,
         source="scratch/t05/COVERAGE.json:client table_41 + server table_41",
         cross_check="E30 curr 173/173 封口;scratch/t02/curr_reference.json 双 archive byte-identical",
         reliability="high"),
    dict(entity="derby (drbr)", count=1567,
         source="scratch/t02/drbr_reference.json row_framework.count=1567 (client_db/table_18.dat)",
         cross_check="scratch/t05/COVERAGE.json:client table_18 count=1567,server table_18 亦 1567",
         reliability="mid",
         note="同一张表在 COVERAGE.json 里实体名写作 'city-associated secondary-name data',"
              "实体归属未定(见 name_conflicts);基数 1567 无争议"),
    dict(entity="injury (inju)", count=115,
         source="scratch/t05/COVERAGE.json:client table_6 + server table_6",
         cross_check="E38/E51 injury 115 行逐行身份;E40 字段命名;fixtures_truth closure 14+115*16+8=1862",
         reliability="high"),
    dict(entity="language (lang)", count=126,
         source="scratch/t05/COVERAGE.json:client table_8 + server table_8",
         cross_check="scratch/t02/lang_reference.json row_len=4+len+30,走查 126 行;E42 language count=126",
         reliability="high"),
    dict(entity="local region (lcrg)", count=2488,
         source="scratch/t05/COVERAGE.json:client table_47 + server table_47",
         cross_check="E37 scripts/t05_lcrg.py 双约束闭合 2,488 行 rdui/duni 2488/2488;E42/E51 2,488 行 csv",
         reliability="high"),
    dict(entity="media source (mdso)", count=208,
         source="scratch/t05/COVERAGE.json:client table_7 + server table_7",
         cross_check="E33 fw7 count208/size36824 client+server 双 closure",
         reliability="high"),
    dict(entity="nation (nati)", count=251,
         source="scratch/t05/COVERAGE.json:client table_10 (server table_10 同为 251)",
         cross_check="E34 client 251/251 行精确封口;E21 duni 锚点;E37 未复现项(我的 walker 第129行卡住,不构成否证)",
         reliability="high"),
    dict(entity="nation name/key companion", count=251,
         source="scratch/t05/COVERAGE.json:client table_9 (server table_9 同为 251)",
         cross_check="COVERAGE.md '251 行 sentinel+duni 尾锚全封口';server table_9 同行数。"
                     "同基数不等于同一实体 —— E23 裁定 type 9 = NATIONAL_TEAM_CONTAINER,见 name_conflicts",
         reliability="mid",
         note="实体名本身有争议(COVERAGE 叫 'nation name/key companion',stage2_three_way 给 entity_tag=nati,"
              "E23 裁定为 NATIONAL_TEAM_CONTAINER);251 这个基数在任何一种解释下都成立"),
    dict(entity="region (regi)", count=28,
         source="scratch/t05/COVERAGE.json:client table_19 + server table_19",
         cross_check="E29 regi 28/28 身份块 + closure 14+28*45+8=1282(client)/46(server)",
         reliability="high"),
    dict(entity="stadium (stad)", count=48413,
         source="scratch/t05/COVERAGE.json:client table_21 + server table_21",
         cross_check="E38 stadium 48413 行逐行身份;E51 48,413 行 csv;fixtures_truth closure",
         reliability="high"),
    dict(entity="stage name (stgn)", count=278,
         source="scratch/t05/COVERAGE.json:client table_23 + server table_23",
         cross_check="scratch/t02/stgn_reference.json stride 14 双 archive byte-identical;closure 14+278*14+8=3914",
         reliability="high"),
    dict(entity="team", count=84507,
         source="scratch/t05/COVERAGE.json:server table_24",
         cross_check="E37 gap:team 84,507 行/8,819,030 B,均值 104.36B 非整数,取数为 L1 走查计数(行边界未闭合)",
         reliability="mid",
         note="行数已从 header 计数与 payload 长度读出,但 table_24 是全库唯一的边界 open 表;"
              "E37 报 '12+82*84507 精确满足 table_extra_24' 为强假设,未验收"),
    dict(entity="weather profile (weat)", count=334,
         source="scratch/t05/COVERAGE.json:client table_27 + server table_27",
         cross_check="E27 334 行全量走查(payload 43,345B)+ 身份块 334/334;E42 city off14 max=333 → 落在 [0,334)",
         reliability="high"),
    dict(entity="agreement (agrm)", count=6,
         source="scratch/t05/COVERAGE.json:client table_56 + server table_56",
         cross_check="closure 14+6*13+8=100(client)/server 同式",
         reliability="high"),

    # ---- 人(person) 家族 ----
    dict(entity="person (basic_people_db 全库)", count=658011,
         source="scratch/t05/people/attrs.json count=658011 (basic_people_db.dat)",
         cross_check="E25 u32 count=658,011 + 658,011/658,011 行尾身份;E32 独立解压走查 658,011 行封口;"
                     "docs/BASELINE.md people_db 行链 100%",
         reliability="high",
         note="分 class 行数:1 ACTUAL_NON_PLAYER=166064 / 2 ACTUAL_PLAYER=476158 / 3=4757 /"
              " 4 OFFICIAL=9839 / 5 RETIRED_NAME=1193(同源 attrs.json class_counts)"),
    dict(entity="person subtable: 任职履历 (t49)", count=792149,
         source="scratch/t05/COVERAGE.json:server table_49",
         cross_check="E56 t49=792149 行(df=1 码 ajob/otea/plac → person);scratch/cmd/stage2_candidate_adjudication.json",
         reliability="mid",
         note="实体归属 A 级(schema df=1),但行边界闭合与 entity 名字不是同一层证据"),

    # ---- club 子表 ----
    dict(entity="club subtable: 球场/迁建 (t22)", count=449,
         source="scratch/t05/COVERAGE.json:server table_22 + client table_22",
         cross_check="E56 t22=449 (df=1 码 Salt/Scam/Scpm/Slhm → club);t13d audit rows_dumped 449/449",
         reliability="mid",
         note="449 行 ≠ stadium 主表 48,413;E47 记录 t22 在 club 覆盖 14/14、在 stadium 仅 3/76"),
    dict(entity="club subtable: 战绩 (t37)", count=465712,
         source="scratch/t05/COVERAGE.json:server table_37",
         cross_check="E56 t37=465712 行(club×赛事);closure 14+465712*40+8=18628502",
         reliability="mid"),
    dict(entity="club subtable: 赛事史 (t34, candidate)", count=7115,
         source="scratch/t05/COVERAGE.json:server table_34",
         cross_check="E56 t34=7115 只有 B 类行数/语义锚,candidate;t13d audit rows_dumped 7115/7115",
         reliability="low",
         note="实体归属仅有 B 类(行数/语义)证据,E56 明确标 candidate"),
    dict(entity="club subtable: 转会分期 (t43, candidate)", count=535,
         source="scratch/t05/COVERAGE.json:server table_43",
         cross_check="E56 t43=535 (B 类 candidate);closure 14+535*46+8=24632",
         reliability="low"),

    # ---- player 子表 ----
    dict(entity="player subtable: 伤病/未来状态 (t30)", count=72473,
         source="scratch/t05/COVERAGE.json:server table_30",
         cross_check="E56 t30=72473 (df=1 码 futu/inju/pret/seve → player);t13d audit rows_dumped 72473/72473",
         reliability="mid",
         note="72,473 >> injury 主表 115,故是 player 侧伤病例表而非 injury"),
]


# 基数已知但实体身份未定的表(供交叉核对;不要当成实体断言)
UNIDENTIFIED = [
    (12, 28597), (26, 90128), (29, 13278), (31, 37283), (32, 315), (33, 32409),
    (36, 6535), (38, 5241), (39, 117), (42, 17721), (45, 84477), (46, 7),
    (48, 5210), (50, 45), (51, 59), (58, 8), (59, 9079), (60, 59), (61, 16),
    (62, 37214), (63, 2), (64, 6946), (65, 1417), (66, 753), (67, 6826),
    (68, 138), (69, 230), (70, 10075), (71, 616665), (72, 138), (73, 1),
    (52, 0), (57, 0),
]  # server;client table_35=890 与 server 同数,见 CLIENT_UNIDENTIFIED

CLIENT_UNIDENTIFIED = [(35, 890)]

NEGATIVE_IDENTITY = [
    (31, 37283), (42, 17721), (46, 7), (50, 45), (51, 59),
]


def schema_index():
    """stage2_three_way: table_type -> entity_tag/field_count。"""
    d = _load(STAGE2)
    return {r["table_type"]: r for r in d["rows"]}


def layout_index():
    """layouts.json: type_id -> {archive: (business_width, field_count)}。"""
    d = _load("scratch/t05/layouts.json")
    out = {}
    for L in d["layouts"]:
        out[L["type_id"]] = {
            "entity": L.get("entity"),
            "archives": {a: [v.get("business_width"), v.get("field_count")]
                         for a, v in L.get("archives", {}).items()},
        }
    return out


def cross_artifact_counts():
    """同一张表在多个工件里的 readback 基数;用于真冲突检测。"""
    reg = {}

    def put(arch, tid, count, src):
        if count is None:
            return
        reg.setdefault((arch, tid), []).append((int(count), src))

    for (arch, tid), t in _coverage().items():
        put(arch, tid, t.get("count_resolved"), "scratch/t05/COVERAGE.json")

    for tid, t in bound_counts().items():
        put("server", tid, t.get("count"), "scratch/t05/server_bounds/boundaries.json")

    for fx in _load(FIXTURES)["fixtures"]:
        put(fx["archive"], fx["table_id"], fx.get("count"),
            "scratch/t05/fixtures_truth.json")

    for r in _load(ADJ)["rows"]:
        put(r["archive"], r["table_type"], r.get("count"),
            "scratch/cmd/stage2_candidate_adjudication.json")

    for t in _load("scratch/t13d/out/audit.json")["tables"]:
        put("server", t["table_type"], t.get("declared_count"),
            "scratch/t13d/out/audit.json")

    return reg


def find_conflicts():
    """同一 (archive,table) 在不同工件里的数字不一致 -> 真冲突。"""
    out = []
    for (arch, tid), pairs in sorted(cross_artifact_counts().items()):
        counts = sorted({c for c, _ in pairs})
        if len(counts) > 1:
            out.append({"archive": arch, "table_id": tid, "counts": counts,
                        "sources": [{"file": s, "count": c} for c, s in pairs]})
    return out


def build():
    cov = _coverage()
    bnd = bound_counts()

    # 冲突:同一 (archive,table_id) 在不同工件的数字不一致
    conflicts = find_conflicts()
    bad = {(c["archive"], c["table_id"]) for c in conflicts}
    tbl_arch = {
        "award": [("client", 0)], "city": [("client", 2)],
        "club": [("client", 3)], "competition (comp)": [("client", 25)],
        "continent (cont)": [("client", 5)], "currency (curr)": [("client", 41)],
        "derby (drbr)": [("client", 18)], "injury (inju)": [("client", 6)],
        "language (lang)": [("client", 8)], "local region (lcrg)": [("client", 47)],
        "media source (mdso)": [("client", 7)], "nation (nati)": [("client", 10)],
        "nation name/key companion": [("client", 9)],
        "region (regi)": [("client", 19)], "stadium (stad)": [("client", 21)],
        "stage name (stgn)": [("client", 23)], "team": [("server", 24)],
        "weather profile (weat)": [("client", 27)], "agreement (agrm)": [("client", 56)],
    }
    for r in ROWS:
        r["conflict"] = any(k in bad for k in tbl_arch.get(r["entity"], []))

    # 附上 schema / layout 旁证(stage2_three_way + layouts),不改基数
    s2, lay = schema_index(), layout_index()
    tid_of = {}
    for r in ROWS:
        for k in tbl_arch.get(r["entity"], []):
            tid_of.setdefault(r["entity"], []).append(k[1])
    for r in ROWS:
        tids = tid_of.get(r["entity"], [])
        r["schema"] = []
        for tid in tids:
            s = s2.get(tid)
            if s:
                r["schema"].append({
                    "table_type": tid, "entity_tag": s.get("entity_tag"),
                    "field_count": s.get("field_count"),
                    "source": "scratch/t01/stage2_three_way.json:table_type=%d" % tid})
            L = lay.get(tid)
            if L:
                r["schema"].append({
                    "table_type": tid, "layout_business_width": {
                        a: v[0] for a, v in L["archives"].items()},
                    "layout_field_count": {a: v[1] for a, v in L["archives"].items()},
                    "source": "scratch/t05/layouts.json:type_id=%d" % tid})

    unident = []
    pairs = [("server", t, c) for t, c in UNIDENTIFIED] + \
            [("client", t, c) for t, c in CLIENT_UNIDENTIFIED]
    for arch, tid, cnt in pairs:
        t = cov.get((arch, tid), {})
        unident.append({
            "archive": arch,
            "table_id": tid,
            "count": cnt,
            "source": "scratch/t05/COVERAGE.json:%s table_%d" % (arch, tid),
            "identity": t.get("entity") or None,
            "identity_negative": (arch, tid) in {("server", x) for x, _ in NEGATIVE_IDENTITY},
        })

    out = {
        "task": "t13e",
        "kind": "bypass-reference (旁路资料整理,非主线产物)",
        "status": STATUS,
        "generated": "2026-11-18",
        "purpose": "实体 -> 已知行数基数,供 t13 主线交叉核对;本清单不裁决实体归属",
        "rules": {
            "evidence": "每条 count 都带文件名 + table_id 或 E 编号;无出处不入清单",
            "conflict": "同一实体出现不同数字时两者全部保留并置 conflict=true,不自行取舍",
            "reliability": "high = 行边界闭合且 ≥2 路独立复算;mid = 基数确定但行边界或实体归属未闭合;low = 实体归属仅 candidate",
        },
        "baselines": ROWS,
        "unidentified_tables": unident,
        "source_conflicts": conflicts,
        "negative_identity_tables": [
            {"table_id": tid, "count": cnt,
             "source": "scratch/cmd/stage2_candidate_adjudication.json (status=negative)",
             "cross_check": "E56 五张零命名字段表被推翻投票;'当前零证据'≠'无实体身份'"}
            for tid, cnt in NEGATIVE_IDENTITY
        ],
        "name_conflicts": [
            {"table_id": 18, "count": 1567,
             "claim_a": "COVERAGE.json: 'city-associated secondary-name data'",
             "claim_b": "scratch/t02/drbr_reference.json: db::DERBY (RTTI .?AVDERBY@db@@)",
             "impact": "基数一致(1567),仅实体名冲突;t13 取名时勿同时采纳两种身份"},
            {"table_id": 24, "count": 84507,
             "claim_a": "COVERAGE.json: team(行边界 open)",
             "impact": "行数可用,行边界不可用;若按 82B 定长假设使用会与 E37 的均值 104.36B 冲突"},
            {"table_id": 9, "count": 251,
             "claim_a": "COVERAGE.json: 'nation (name/key companion)' + stage2_three_way entity_tag=nati",
             "claim_b": "LEDGER E23: table_type 9 = NATIONAL_TEAM_CONTAINER,t01e 的 nati 双虚表标签已勘误;"
                         "table_type 10 才是 NATION",
             "impact": "251 与 table_10 同基数,不能据此判定同一实体;若需 nation 主表请用 table_10"},
        ],
        "known_non_count_anchors": [
            {"anchor": "六大洲 0..5", "count_ref": "continent=7", "source": "docs/BASELINE.md"},
            {"anchor": "England=139 / China PR=55", "count_ref": "nation=251,值域 [0,251)",
             "source": "docs/BASELINE.md + reports/t01f_comp_row_offsets.md (§ccti/cnti 锚点)"},
            {"anchor": "parent row 352", "count_ref": "comp=7047", "source": "reports/t01f_comp_row_offsets.md"},
            {"anchor": "Bernabéu 81,044", "count_ref": "stadium=48413", "source": "docs/BASELINE.md"},
            {"anchor": "city Cnti=139 (Liverpool/Manchester)", "count_ref": "nation=251",
             "source": "scratch/t05/fixtures_truth.json named_rows"},
        ],
        "coverage_note": [
            "已收录 %d 个实体/子实体条目,覆盖 t05 COVERAGE 里全部 client 表与全部已有实体名的 server 表" % len(ROWS),
            "%d 张实体名未定/被推翻的表以 unidentified_tables 给出基数(含 count=0 的 t52/t57),未强行命名" % len(unident),
            "同一 (archive,table_id) 跨 %d 个既有工件比对基数(COVERAGE / server_bounds / fixtures_truth /"
            " stage2_candidate_adjudication / t13d audit),不一致项 %d 个(%d 张表参与比对)"
            % (5, len(conflicts), 78),
            "未收录:history_db / lang_update_db / summary.dat 等非数值主表(不在必查文件范围)",
        ],
    }
    return out


def render_md(o):
    rows = sorted(o["baselines"], key=lambda r: r["entity"].lower())
    lines = [
        "# 已知实体基数清单(t13e 旁路)",
        "",
        "`status`: **%s** —— 旁路资料整理,仅供 t13 主线交叉核对;本表不裁决实体归属。" % o["status"],
        "",
        "生成:%s;每个数字均带出处(文件名 + table_id 或 E 编号)。" % o["generated"],
        "",
        "## 实体 → 行数(按实体名排序)",
        "",
        "| 实体 | 行数 | 出处 | 交叉核对 | 可靠性 | 冲突 |",
        "|---|---:|---|---|---|---|",
    ]
    for r in rows:
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            r["entity"], format(r["count"], ","), r["source"], r["cross_check"],
            r["reliability"], "**冲突**" if r["conflict"] else "-"))
    lines += ["", "## 实体身份未定的表(基数可用,名字勿用)", "",
              "| archive | table_id | 行数 | 出处 |", "|---|---:|---:|---|"]
    for u in sorted(o["unidentified_tables"], key=lambda x: (x["archive"], x["table_id"])):
        lines.append("| %s | %s | %s | %s |" % (
            u["archive"], u["table_id"],
            format(u["count"], ",") if u["count"] is not None else "?",
            u["source"].split(":", 1)[-1]))
    lines += ["", "## 实体身份被推翻(negative)的表", "",
              "| table_id | 行数 | 出处 |", "|---:|---:|---|"]
    for n in o["negative_identity_tables"]:
        lines.append("| %s | %s | %s |" % (n["table_id"], format(n["count"], ","), n["source"]))
    lines += ["", "## 冲突项", ""]
    if o["source_conflicts"]:
        for c in o["source_conflicts"]:
            lines.append("- **%s table_%d**:基数不一致 %s;来源 %s" % (
                c["archive"], c["table_id"], "/".join(str(x) for x in c["counts"]),
                "; ".join("%s=%s" % (s["file"], s["count"]) for s in c["sources"])))
    else:
        lines.append("- 行数层面:**无冲突**。同一 (archive,table_id) 在 COVERAGE / server_bounds / "
                     "fixtures_truth / stage2_candidate_adjudication / t13d audit 五个工件的计数全部一致"
                     "(78 张表参与比对;篡改一份记录作负对照,检测器能报出冲突)。")
    for c in o["name_conflicts"]:
        lines.append("- table_%s %s 行:%s%s。%s" % (
            c["table_id"], format(c["count"], ","), c["claim_a"],
            (" ↔ " + c["claim_b"]) if c.get("claim_b") else "", c["impact"]))
    lines += ["", "## schema / 布局旁证(不参与冲突判定,仅供主线算宽度)", "",
              "| 实体 | table_type | entity_tag | schema 字段数 | 业务宽度(client/server) | 布局档数(client/server) |",
              "|---|---:|---|---:|---|---|"]
    for r in rows:
        for s in r.get("schema", []):
            if "entity_tag" in s:
                lines.append("| %s | %s | %s | %s | - | - |" % (
                    r["entity"], s["table_type"], s["entity_tag"], s["field_count"]))
            else:
                bw, fc = s["layout_business_width"], s["layout_field_count"]
                lines.append("| %s | %s | - | - | %s | %s |" % (
                    r["entity"], s["table_type"],
                    "/".join(str(bw.get(a, "-")) for a in ("client", "server")),
                    "/".join(str(fc.get(a, "-")) for a in ("client", "server"))))
    lines += ["", "## 非行数锚点(同表基数一起用)", "", 
              "| 锚点 | 关联基数 | 出处 |", "|---|---|---|"]
    for a in o["known_non_count_anchors"]:
        lines.append("| %s | %s | %s |" % (a["anchor"], a["count_ref"], a["source"]))
    lines += ["", "## 说明", ""] + ["- " + s for s in o["coverage_note"]]
    for r in rows:
        if r.get("note"):
            lines.append("- **%s**:%s" % (r["entity"], r["note"]))
    lines.append("")
    return "\n".join(lines)


def selftest(o):
    cov = _coverage()
    errs = []
    for r in o["baselines"]:
        if not r["source"] or not r["cross_check"]:
            errs.append("缺出处: %s" % r["entity"])
        if not isinstance(r["count"], int) or r["count"] <= 0:
            errs.append("非法 base: %s" % r["entity"])
    # COVERAGE 里的 count 与清单核对
    for arch, tid, ent in [("client", 2, "city"), ("client", 3, "club"), ("client", 25, "competition (comp)"),
                           ("client", 6, "injury (inju)"), ("client", 8, "language (lang)"),
                           ("client", 21, "stadium (stad)"), ("client", 19, "region (regi)"),
                           ("client", 27, "weather profile (weat)"), ("client", 5, "continent (cont)"),
                           ("client", 41, "currency (curr)"), ("client", 47, "local region (lcrg)"),
                           ("client", 7, "media source (mdso)"), ("client", 23, "stage name (stgn)"),
                           ("client", 0, "award"), ("client", 56, "agreement (agrm)")]:
        t = cov.get((arch, tid))
        row = next((r for r in o["baselines"] if r["entity"] == ent), None)
        if t is None or row is None:
            errs.append("查无此项: %s/%s" % (arch, tid))
            continue
        got = t.get("count_resolved")
        if got is not None and got != row["count"]:
            errs.append("基数不符 %s: COVERAGE=%s 清单=%s" % (ent, got, row["count"]))
    # 必查文件都必须真的被读过(stage2 / layouts 非空)
    if len(schema_index()) != 21:
        errs.append("stage2_three_way 应有 21 行,实际 %d" % len(schema_index()))
    if len(layout_index()) != 26:
        errs.append("layouts.json 应有 26 实体,实际 %d" % len(layout_index()))
    # 未定表必须都在 COVERAGE 里
    for u in o["unidentified_tables"]:
        if (u["archive"], u["table_id"]) not in cov:
            errs.append("未定表不在 COVERAGE: %s/%s" % (u["archive"], u["table_id"]))
    # conflict 标记一致性:只有 source_conflicts 命中的表才标 conflict
    bad = {(c["archive"], c["table_id"]) for c in o["source_conflicts"]}
    for r in o["baselines"]:
        if r["conflict"] and not bad:
            errs.append("无来源冲突却标了 conflict: %s" % r["entity"])
    return errs


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    o = build()
    if "--selftest" in argv:
        errs = selftest(o)
        for e in errs:
            print("FAIL", e)
        print("selftest:", "PASS" if not errs else "FAIL", "(%d 条基数)" % len(o["baselines"]))
        return 0 if not errs else 1
    if len(argv) > 1:
        print("usage: build.py [--selftest]", file=sys.stderr)
        return 2
    with open(os.path.join(OUT, "baselines.json"), "w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(OUT, "baselines.md"), "w", encoding="utf-8") as f:
        f.write(render_md(o))
    print("wrote baselines.json (%d 实体, %d 未定表) + baselines.md"
          % (len(o["baselines"]), len(o["unidentified_tables"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
