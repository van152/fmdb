def write_report(outdir: Path, fourcc_map, xml_out, join_out):
    """REPORT.md - findings, per-table hit rates, 1,034 breakout, missing sub-calls."""
    lines = []
    A = lines.append
    kinds = Counter()
    with_off = 0
    pairs = 0
    for rec in fourcc_map["tables"]:
        for cand in rec["fourccs"].values():
            kinds[cand["access_kind"]] += 1
            pairs += 1
            if cand.get("primary_off_int") is not None:
                with_off += 1
    join_by = {(j["table_type"], j["class"]): j for j in join_out["tables"]}
    t = join_out["totals"]
    s = xml_out["summary"]
    val = xml_out.get("validation_vs_accepted_L3") or {}

    A("# t97 — Hex-Rays 4CC ↔ 内存偏移全量抽取 + 1,034 分母分诊")
    A("")
    A("> 只读输入：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（Hex-Rays 反编译 C）、")
    A("> `reports/xml_denominator_coverage.json`。**本任务不修改 `reports/` 与 `LEDGER.json`**。")
    A("")
    A("## 0. 交付物")
    A("")
    A("| 文件 | 内容 |")
    A("|---|---|")
    A("| `fourcc_mem_map.json` | 67 张表的 4CC → `mem_off` / `access_kind` / `func_va` / `line_no`（`\"status\": \"complete\"`） |")
    A("| `xml_triage.json` | 1,034 条分母逐条分诊 + 分桶变化汇总 + 对已验收 L3 的回归验证 |")
    A("| `static_read_join.json` | 4CC ↔ `mem_off` ↔ slot19/slot20 行号 的静态交叉表 |")
    A("| `REPORT.md` / `DONE.md` | 本报告 / 完成标记（`DONE type=t97`） |")
    A("")
    A("## 1. 覆盖与规模")
    A("")
    A(f"- 表条目（`vtable_index.tables`）：**{fourcc_map['table_count']}**")
    A(f"- 唯一 4CC：**{fourcc_map['unique_fourcc_count']}**（t95 初扫曾见 1,897；本任务因追踪基类/子对象 get_prop 而扩大）")
    A(f"- 表×4CC 分支记录：**{pairs}**，其中有明确字节偏移：**{with_off}**（{with_off / max(pairs, 1):.1%}）")
    A("- 纯静态：只解析 t95 的反编译产物，无数据库 dump、无第三方依赖")
    A("")
    A("| access_kind | 分支数 | 含义 |")
    A("|---|---|---|")
    meaning = {
        "direct_field": "分支内直接解引用 `this + N` 的标量/指针字段",
        "bitfield": "同一字段带 `& mask` / `>> n` 位域操作",
        "subobj_deref": "先取 `this + N` 处的子对象指针，再读其内部字段",
        "helper_computed": "值由 helper 子函数计算（helper 未反编译时无字节偏移）",
        "delegated_or_empty": "分支仅 `return sub_X(this, code, out)` 或直接 `goto`/`break`",
    }
    for k, v in kinds.most_common():
        A(f"| `{k}` | {v} | {meaning.get(k, '')} |")
    A("")
    A("## 2. 每张大表命中率")
    A("")
    A("| tt | class | 链上函数数 | 4CC | 有明确 mem_off | read_server 命中 | slot19 偏移数 |")
    A("|---|---|---|---|---|---|---|")
    big = sorted(fourcc_map["tables"], key=lambda r: -r["fourcc_count"])[:24]
    for rec in big:
        wo = sum(1 for c in rec["fourccs"].values() if c.get("primary_off_int") is not None)
        j = join_by.get((rec["table_type"], rec["class"]), {})
        cnt = j.get("counters") or {}
        s19 = (j.get("slots") or {}).get("slot19_read_server") or {}
        A(
            f"| {rec['table_type']} | {rec['class']} | {len(rec['chain'])} | {rec['fourcc_count']} | "
            f"{wo} ({wo / max(rec['fourcc_count'], 1):.0%}) | {cnt.get('hit_read_server', 0)} | "
            f"{s19.get('offset_count', 0)} |"
        )
    A("")
    A(f"其余 {max(len(fourcc_map['tables']) - len(big), 0)} 张表见 `fourcc_mem_map.json`（多为 2–30 个 4CC 的档案表）。")
    A("")
    A("### 2.1 解析器要点（为什么 `helper_computed` 占比高）")
    A("")
    A("- CLUB/COMP 这类 4,500 行的 `get_prop` 把大量 4CC 直接转交给子对象或 helper，例如")
    A("  `return sub_143CA2E60(v21, 11, code, a3)`（COMP）、`v214 = sub_140E73FB0(a1)`（CLUB）。")
    A("  这些 helper 不在 t95 的 352 份反编译产物中，因此只能记录到 `helper_calls`，无法给出字节偏移。")
    A("- 尾调用到**基类** handler（`CLUB → TEAM_CONTAINER`、`NATIONAL_TEAM_CONTAINER → TEAM_CONTAINER`、")
    A("  `NATION → 1410668F0 / 141063F30 / 141045D50`）已按「同对象」规则追踪至 depth 3，结果标 `delegated`。")
    A("- 共享对象协议 handler（`0x140FE3F20` / `0x140FE2700`，被 13–14 个表条目复用）**不作为基类 getter 追踪**，")
    A("  否则 `BaCP/COPY/DELE/Duni/HiSe/ISTP` 等通用协议码会污染全部 67 张表。")
    A("")
    A("## 3. NATION (tt=10) 专项核对")
    A("")
    nat = next(r for r in fourcc_map["tables"] if r["table_type"] == 10)
    A("| 槽 | 函数 | depth | 分支数 | 关系 |")
    A("|---|---|---|---|---|")
    for c in nat["chain"]:
        rel = "自身槽" if c["depth"] == 0 else (
            "同对象基类/尾调用" if c.get("same_object") else "跨对象（子对象 / hop1 精选）"
        )
        A(f"| `{c['slot']}` | `{c['va']}` (`{c['file']}`) | {c['depth']} | {c['branches']} | {rel} |")
    A("")
    A("任务书点名的四份 nation 侧文件：")
    A("")
    for va, name in (
        ("0x141042940", "141042940.c"),
        ("0x141045d50", "141045d50.c"),
        ("0x141063f30", "141063f30.c"),
        ("0x1410668f0", "1410668f0.c"),
    ):
        in_chain = any(c["va"] == va for c in nat["chain"])
        A(f"- `{name}`：{'在链上 ✔' if in_chain else '未在链上 ✘'}")
    A("")
    nation_missing = [
        m for m in fourcc_map["missing_subcalls"]
        if m["class"] in ("NATION", "NATIONAL_TEAM_CONTAINER")
    ]
    A(f"`NATION`/`NATIONAL_TEAM_CONTAINER` 的 `missing_subcalls`：**{len(nation_missing)}** 条"
      "（转发 4CC 但无反编译文件的直接子调用）")
    A("")
    if nation_missing:
        A("| class | slot | from | 未反编译目标 | arg0 是 this |")
        A("|---|---|---|---|---|")
        for m in nation_missing:
            A(f"| {m['class']} | `{m['slot']}` | `{m['from_va']}` | `{m['va']}` | {m['arg0_is_this']} |")
        A("")
    A("## 4. 1,034 分母分诊")
    A("")
    A(f"分母：**{s['denominator']}** 条（club 433 / nation 346 / comp 255）。")
    A("分桶变化全部落在候选标签上，`reports/` 未被改写（`proposed_bucket` 是静态候选，不是已接受的桶）。")
    A("")
    A("| 原桶（`bucket_after`） | 总数 | 直接 mem_off | subobj_deref | helper_computed | delegated/empty | 同类同 tag 其它表 | 仅共享 handler | 其它表另有 | 全 67 表皆无 |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for bucket, d in s["breakout"].items():
        A(
            "| `{}` | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                bucket, d["total"],
                d.get("hit_direct_mem_off", 0), d.get("hit_subobj_deref", 0),
                d.get("hit_helper_computed", 0), d.get("hit_delegated_or_empty", 0),
                d.get("hit_other_table_same_tag", 0),
                d.get("absent_locally_only_in_shared_handler", 0),
                d.get("absent_locally_code_in_other_table", 0),
                d.get("absent_everywhere_in_67_tables", 0),
            )
        )
    A("")
    A("### 4.1 三个关键桶的突破")
    A("")
    for bucket in ("unresolved_wire_slot", "held", "no_wire_evidence"):
        d = s["breakout"].get(bucket)
        if not d:
            continue
        absent = (
            d.get("absent_everywhere_in_67_tables", 0)
            + d.get("absent_locally_code_in_other_table", 0)
            + d.get("absent_locally_only_in_shared_handler", 0)
        )
        A(
            f"- **`{bucket}`（{d['total']} 条）**：明确 `mem_off` **{d.get('hit_direct_mem_off', 0)}** 条；"
            f"`subobj_deref` {d.get('hit_subobj_deref', 0)} 条；`helper_computed` {d.get('hit_helper_computed', 0)} 条；"
            f"delegated/empty {d.get('hit_delegated_or_empty', 0)} 条；链上不存在 {absent} 条"
            f"（其中全 67 表皆无 {d.get('absent_everywhere_in_67_tables', 0)} 条 = 强证据：纯 UI / 编辑器派生 / 仅存档字段）"
        )
    A("")
    A("### 4.2 分实体")
    A("")
    A("| entity | 直接 mem_off | helper_computed | delegated/empty | 同类同 tag | 其它表另有 | 全表皆无 |")
    A("|---|---|---|---|---|---|---|")
    per_ent = defaultdict(Counter)
    for r in xml_out["rows"]:
        per_ent[r["entity"]][r["proposed_bucket"]] += 1
    for ent in sorted(per_ent):
        c = per_ent[ent]
        A(
            f"| {ent} | {c.get('hit_direct_mem_off', 0)} | {c.get('hit_helper_computed', 0)} | "
            f"{c.get('hit_delegated_or_empty', 0)} | {c.get('hit_other_table_same_tag', 0)} | "
            f"{c.get('absent_locally_code_in_other_table', 0)} | {c.get('absent_everywhere_in_67_tables', 0)} |"
        )
    A("")
    A("## 5. 对已验收 L3 的独立回归（防自欺）")
    A("")
    if val.get("available"):
        vt = val["totals"]
        A(f"来源：`{val['source']['path']}`（只读），逐字段对比 `object_displacement`：")
        A("")
        A(
            f"- 检查 **{vt.get('checked', 0)}** 条：exact **{vt.get('exact', 0)}**、"
            f"within_slot **{vt.get('within_slot', 0)}**、no_static_hit **{vt.get('no_static_hit', 0)}**、"
            f"mismatch **{vt.get('mismatch', 0)}**"
        )
        A("")
        A("> 已验收值是**线槽起点**（slot_width 字节宽），t97 报的是**字段字节偏移**；"
          "位域可能落在槽内几字节处，故单列 `within_slot`。")
        A("")
        A("| section | code | 已验收 disp | 宽度 | t97 off | access_kind | 判定 |")
        A("|---|---|---|---|---|---|---|")
        for it in val["items"]:
            A(
                f"| {it['section'].replace('_main_row_fields', '')} | `{it['code']}` | {it['accepted_displacement']} | "
                f"{it['accepted_slot_width']} | {it['t97_off'] if it['t97_off'] is not None else '—'} | "
                f"`{it['t97_access_kind'] or '—'}` | {it['verdict']} |"
            )
        A("")
        A("`no_static_hit` 的两条（`Cedp` / `Cncl`）其值由未反编译 helper 计算；`duni` 是基类序列化的身份列，")
        A("不走 4CC 分派，属已知特例。")
    else:
        A("（未找到可用的已验收 L3 表）")
    A("")
    A("## 6. slot19/slot20 静态偏移交叉")
    A("")
    A(f"- slot02/03 有明确 `mem_off` 的分支：**{t.get('fourccs_with_off', 0)}**")
    A(f"- 与 `slot19_read_server` 偏移集合相交：**{t.get('hit_read_server', 0)}**")
    A(f"- 与 `slot20_read_client` 偏移集合相交：**{t.get('hit_read_client', 0)}**")
    A(f"- 至少命中一侧：**{t.get('hit_any_read', 0)}**")
    A("")
    A("| tt | class | 有 off | slot19 命中 | slot20 命中 | 至少一侧 |")
    A("|---|---|---|---|---|---|")
    for j in sorted(join_out["tables"], key=lambda x: -x["counters"].get("hit_any_read", 0))[:15]:
        c = j["counters"]
        if not c.get("fourccs_with_off"):
            continue
        A(
            f"| {j['table_type']} | {j['class']} | {c['fourccs_with_off']} | {c['hit_read_server']} | "
            f"{c['hit_read_client']} | {c['hit_any_read']} |"
        )
    A("")
    A("## 7. `missing_subcalls` 清单")
    A("")
    ms = fourcc_map["missing_subcalls"]
    A(f"合计 **{len(ms)}** 条（去重：表 × 槽 × 目标）。这些是 `slot02`/`slot03`（含追踪到的基类）里")
    A("**转发 4CC 但无反编译文件**的直接子调用，是后续扩大反编译的第一优先目标。")
    A("完整清单见 `fourcc_mem_map.json#/missing_subcalls`。")
    A("")
    if ms:
        by_cls = Counter(m["class"] for m in ms)
        A("| class | 条数 |")
        A("|---|---|")
        for cls, n in by_cls.most_common():
            A(f"| {cls} | {n} |")
        A("")
        tgt = Counter(m["va"] for m in ms)
        A("出现最多的未反编译目标：")
        A("")
        A("| 目标 VA | 出现次数 | 存在 this 直传 |")
        A("|---|---|---|")
        for va, n in tgt.most_common(12):
            this_direct = any(m["va"] == va and m["arg0_is_this"] for m in ms)
            A(f"| `{va}` | {n} | {this_direct} |")
        A("")
        A("明细（前 40 条）：")
        A("")
        A("| tt | class | slot | from | 目标 | arg0=this |")
        A("|---|---|---|---|---|---|")
        for m in ms[:40]:
            A(
                f"| {m['table_type']} | {m['class']} | `{m['slot']}` | `{m['from_va']}` | "
                f"`{m['va']}` | {m['arg0_is_this']} |"
            )
        A("")
    A("## 8. 方法与已知限制")
    A("")
    A("1. **分支定位**：`case <int>:`（含多标签 fallthrough）、`if (V == N) {…}`、`if (V != N) <guard>; <body>`，")
    A("   以及 `switch` 表；`V` 取第二个形参及其别名（如 CLUB 的 `v4 = (int)a2`）。")
    A("2. **分支体**：花括号匹配 + 同层终止符（`break` / `goto` / `return` / 下一个 `case` / `}`）。")
    A("3. **字节偏移**：按 base 变量**声明元素宽度**换算（整型局部/形参 = 1 字节寻址，`_DWORD *` = ×4，")
    A("   `_QWORD *` = ×8），并对 `this` 的别名做**逐行 reaching-definition 判定**（Hex-Rays 会复用临时变量，")
    A("   例如 COMP 的 `v5` 在某行之后已改指别的对象，其后不得再当作 `this`）。")
    A("4. **`primary_off`**：分支体内最小的「带宽度解引用」偏移；64 位 `lo|hi` 拼接（如 `a1+40` / `a1+44`）取低位。")
    A("5. **不追踪共享协议 handler**（`0x140FE3F20` / `0x140FE2700`），避免跨表污染；其下 `COPY/DELE/BaCP` 等")
    A("   通用协议码因此不会出现在各表 4CC 集合里。")
    A("6. **限制**：`helper_computed` 分支无字节偏移（helper 未反编译，见第 7 节）；位域偏移可能比已验收")
    A("   线槽起点深 1–5 字节（记 `within_slot`）；`duni` 这类身份列走基类序列化，不在 4CC 分派中。")
    A("")
    A("## 9. 复现")
    A("")
    A("```")
    A("py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest   # 25 项断言，含 STARTING_RECORD 三条")
    A("py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --run        # 写 4 个交付物到 scratch/t97/out")
    A("```")
    A("")
    A("> 备注：任务书示例写 `1869899892 == 0x6F737474 == 'ostt'`，实际 `0x6F746874 = 'otht'`；")
    A("> 自检按真实字节 `'otht' -> 0x28` 断言（偏移结论不受影响）。")
    A("")
    (outdir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[t97] wrote REPORT.md", flush=True)


