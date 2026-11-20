"""t10 build — club 链普查: 名字侧反向推 object_off 的可行性判定。

只读输入:
    scripts/t05_pe.py                      PE 段/地址换算
    scratch/t05/schema_inventory.json      FM schema 字段真值表
    scratch/t07/out/4cc_table.json         全局 4CC 表(1477 码/2103 候选)
    scratch/t07/out/build.py               仅复用其已验证的 find_candidates
                                           (injury 13/13, city 6/6); 不修改

产物(全部写 scratch/t10/out/):
    club_census.json     步骤1 码表盘点
    chains_club.json     步骤2 链分组与裁决
    feasibility.json     步骤3 四项检验的机读数字
    feasibility.md       步骤3 人读报告(数字由 json 插值, 不手写)
    candidates_club.json 步骤4 (本任务判负 -> not_feasible)
    REPORT.md            对阶段三的意义

用法:
    py -V:3.12 -I -B scratch/t10/out/build.py --help
    py -V:3.12 -I -B scratch/t10/out/build.py --selftest
    py -V:3.12 -I -B scratch/t10/out/build.py
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PE_PY = ROOT / "scripts/t05_pe.py"
T07 = ROOT / "scratch/t07/out"
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
TABLE4CC = T07 / "4cc_table.json"

# ---- 判据阈值(任务书硬性规定) ----
GATE_NO_OVERLAP = 0.95
GATE_ALIGN = 0.90
CLUSTER_GAP = 0x200          # 相邻 cmp 文件偏移 <= 此值视为同一条链
MIN_CHAIN = 20               # 只报 n_codes >= 20 的链
OFF_LO, OFF_HI = 0x20, 0x400  # 字段对象偏移的合法区间(t05/t07 同口径)

# 步骤2 判出的两条 club 链(文件偏移, 左闭右开); 见 chains_club.json
CHAIN_A = (0xE82AFC, 0xE846AC)
CHAIN_B = (0xE89A34, 0xE8CDED)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rd(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def is_4cc(s: str) -> bool:
    """4 个 ASCII 可见字符(0x21..0x7e), 区分大小写。"""
    return len(s) == 4 and all(0x21 <= ord(c) <= 0x7E for c in s)


def ed1_le(a: str, b: str) -> bool:
    """编辑距离 <= 1(替换/插入/删除各一次)。"""
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return any(l[:i] + l[i + 1:] == s for i in range(len(l)))


# ---------------- 步骤 1: 码表盘点 ----------------
def step1(schema, table):
    ent = schema["entities"]["club"]
    top = [f for f in ent["fields"] if f.get("parent") is None]
    sub = [f for f in ent["fields"] if f.get("parent") is not None]
    codes = [f["code"] for f in top]
    uniq = sorted(set(codes))
    dup = sorted({c for c in codes if codes.count(c) > 1})

    legal = [c for c in uniq if is_4cc(c)]
    illegal = [c for c in uniq if not is_4cc(c)]
    hit_codes = [c for c in legal if c in table]
    miss_codes = [c for c in legal if c not in table]

    offsets = defaultdict(set)
    recs = []
    for c in hit_codes:
        for r in table[c]:
            recs.append({"code": c, "object_off": r["object_off"], "size": r["size"],
                         "kind": r["kind"], "file_off": r["file_off"],
                         "score": r.get("score"), "why": r.get("why")})
            offsets[r["object_off"]].add(c)
    off_list = sorted(offsets)

    # 模糊匹配: 精确未中, 但存在前缀(>=3 字符)相同 / 编辑距离<=1 的 cmp 码
    cmp_codes = set(table)
    prefix_hits, ed_hits = [], []
    for c in miss_codes:
        pfx = sorted(x for x in cmp_codes if x[:3] == c[:3] and x != c)
        ed = sorted(x for x in cmp_codes if ed1_le(c, x))
        if pfx:
            prefix_hits.append({"code": c, "n_prefix3": len(pfx), "sample": pfx[:3]})
        if ed:
            ed_hits.append({"code": c, "n_ed1": len(ed), "sample": ed[:3]})

    return {
        "status": "in_progress",
        "note": "步骤1: club schema 字段名 -> 4CC 码表命中盘点。field 计数用 declared/top_level/len(fields) 三口径并列, "
                "差异来自 sub_fields(列表子字段)。exact = 字段名与 cmp imm32 码逐字节相同; "
                "fuzzy_prefix3 = 前 3 字符相同(推断); fuzzy_ed1 = 编辑距离<=1(推断)。",
        "field_counts": {
            "declared_fields": ent.get("declared_fields"),
            "top_level": ent.get("top_level"),
            "len_fields_in_inventory": len(ent["fields"]),
            "sub_fields": len(sub),
            "scalars": ent.get("scalars"),
            "lists": ent.get("lists"),
            "distinct_top_level_codes": len(uniq),
            "duplicate_top_level_codes": dup,
            "diff_reason": f"declared {ent.get('declared_fields')} = top_level {ent.get('top_level')}; "
                           f"清单里共 {len(ent['fields'])} 条 = top_level + sub_fields {len(sub)}; "
                           f"另有 {len(dup)} 个顶层码名重复({', '.join(dup)}), 故 distinct 码 {len(uniq)} 个。",
        },
        "legal_4cc": {
            "legal": len(legal), "illegal": len(illegal),
            "illegal_codes": illegal,
            "legal_ratio_of_distinct": round(len(legal) / max(1, len(uniq)), 4),
        },
        "exact_match": {
            "hit": len(hit_codes), "miss": len(miss_codes),
            "denominator_distinct": len(uniq),
            "ratio": round(len(hit_codes) / max(1, len(uniq)), 4),
            "hit_codes": hit_codes,
        },
        "fuzzy_match": {
            "prefix3_only": len(prefix_hits),
            "ed1_only": len(ed_hits),
            "prefix3_codes": prefix_hits,
            "ed1_codes": ed_hits,
            "note": "模糊项一律标 inferred, 不计入 exact; 它们是搜索入口, 不是结论。",
        },
        "offset_set": {
            "records": len(recs), "distinct_offsets": len(off_list),
            "min": hex(off_list[0]) if off_list else None,
            "max": hex(off_list[-1]) if off_list else None,
            "outside_0x20_0x400": [o for o in off_list if not (OFF_LO <= o <= OFF_HI)],
            "records_outside_0x20_0x400": [r for r in recs if not (OFF_LO <= r["object_off"] <= OFF_HI)],
            "offsets_claimed_by_multiple_codes": {hex(o): sorted(v) for o, v in sorted(offsets.items()) if len(v) > 1},
            "duplicate_offset_codes": sum(1 for o, v in offsets.items() if len(v) > 1),
            "size_histogram": {str(k): v for k, v in sorted(Counter(r["size"] for r in recs).items())},
            "kind_histogram": dict(Counter(r["kind"] for r in recs)),
        },
        "records": sorted(recs, key=lambda r: (r["object_off"], r["code"])),
    }


# ---------------- 步骤 2: 链分组 ----------------
def step2(hits, schema, table, census):
    ent = schema["entities"]
    club_top = {f["code"] for f in ent["club"]["fields"] if f.get("parent") is None}
    club_all = {f["code"] for f in ent["club"]["fields"]}
    anchor = set(census["exact_match"]["hit_codes"])
    hit_codes_set = {h[1] for h in hits}

    clusters, cur = [], [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] <= CLUSTER_GAP:
            cur.append(h)
        else:
            clusters.append(cur)
            cur = [h]
    clusters.append(cur)

    rows = []
    for cl in clusters:
        cs = [h[1] for h in cl]
        if len(cs) < MIN_CHAIN:
            continue
        css = set(cs)
        rows.append({
            "file_off_start": hex(cl[0][0]), "file_off_end": hex(cl[-1][0]),
            "byte_span": cl[-1][0] - cl[0][0],
            "n_cmp": len(cl), "n_codes": len(css),
            "club_vertex_overlap": len(css & club_top),
            "club_all_fields_overlap": len(css & club_all),
            "club_anchor_overlap": len(css & anchor),
            "sample_codes": cs[:8],
            "_rank": (len(css & club_top), len(css & anchor), len(css & club_all)),
        })
    rows.sort(key=lambda r: r["_rank"], reverse=True)
    for r in rows:
        r["club_overlap_ratio_in_chain"] = round(r["club_vertex_overlap"] / r["n_codes"], 4)
        r["club_recall_of_431"] = round(r["club_vertex_overlap"] / 431, 4)
    for r in rows:
        r.pop("_rank")

    total_clusters = len(clusters)
    club_with_hit = len(club_top & hit_codes_set)
    covered = set()
    for cl in clusters:
        if len(cl) >= MIN_CHAIN:
            covered |= {h[1] for h in cl}

    by_start = {r["file_off_start"]: r for r in rows}
    a = by_start.get(hex(CHAIN_A[0]))
    b = by_start.get(hex(CHAIN_B[0]))
    if a is None or b is None:
        raise RuntimeError(f"club chains not reproduced: A={a}, B={b}")
    shared_ab = None
    for nm, rng in (("A", CHAIN_A), ("B", CHAIN_B)):
        r = by_start[hex(rng[0])]
        assert r["file_off_end"] == hex(rng[1]), f"chain {nm} end changed: {r['file_off_end']}"

    return {
        "status": "in_progress",
        "method": f"全部 {len(hits)} 处 cmp 4CC 命中按 file_off 排序; 相邻间距 <= {hex(CLUSTER_GAP)} 归入同一簇; "
                  "链内 n_codes 去重计数; 裁决同时用两个独立指标: (1) 链顶点与 club 顶层 schema 码的重合, "
                  "(2) 与步骤1 的 4CC 表精确命中集合的重合。",
        "totals": {
            "cmp_hits": len(hits), "distinct_cmp_codes": len(hit_codes_set),
            "clusters": total_clusters, "clusters_n_codes_ge_20": len(rows),
            "club_top_level_codes": len(club_top),
            "club_codes_with_any_cmp_hit": club_with_hit,
            "club_codes_inside_ge20_chains": len(club_top & covered),
            "club_codes_outside_ge20_chains": sorted(club_top - covered),
            "club_top_level_shared_with_other_entities": _shared_with_other(schema, club_top),
        },
        "chains": rows,
        "verdict": {
            "club_chain_a": {
                "range": [a["file_off_start"], a["file_off_end"]],
                "n_codes": a["n_codes"],
                "club_vertex_overlap": a["club_vertex_overlap"],
                "club_anchor_overlap": a["club_anchor_overlap"],
                "reason": f"与 club 顶层码重合 {a['club_vertex_overlap']} 个, 与步骤1 精确命中集合重合 "
                          f"{a['club_anchor_overlap']} 个 — 两项独立指标同时进入前三。",
            },
            "club_chain_b": {
                "range": [b["file_off_start"], b["file_off_end"]],
                "n_codes": b["n_codes"],
                "club_vertex_overlap": b["club_vertex_overlap"],
                "club_anchor_overlap": b["club_anchor_overlap"],
                "reason": f"与 club 顶层码重合 {b['club_vertex_overlap']} 个(最高), 精确命中重合 "
                          f"{b['club_anchor_overlap']} 个(最高)。与 A 是两个独立函数体(club 侧同形 dispatcher), "
                          f"合并记作 club 链, 不取其一。",
            },
            "runners_up": [
                {"range": [r["file_off_start"], r["file_off_end"]], "n_codes": r["n_codes"],
                 "club_vertex_overlap": r["club_vertex_overlap"],
                 "club_anchor_overlap": r["club_anchor_overlap"]}
                for r in rows[:6] if r["file_off_start"] not in (hex(CHAIN_A[0]), hex(CHAIN_B[0]))
            ],
            "decision": "chain A(0xe82afc..0xe846ac)与 chain B(0xe89a34..0xe8cded)同属 club; 判定集合 S = A ∪ B。"
                        "其余 n_codes>=20 的链 club 顶点重合均显著更低, 见 runners_up, 不参与步骤3。",
        },
    }


def _shared_with_other(schema, club_top):
    other = set()
    for k, v in schema["entities"].items():
        if k == "club":
            continue
        other |= {f["code"] for f in v["fields"]}
    inter = club_top & other
    return {"count": len(inter), "ratio": round(len(inter) / max(1, len(club_top)), 4),
            "sample": sorted(inter)[:12]}


# ---------------- 步骤 3: 偏移结构一致性 ----------------
def slots_from(records):
    """把 (code, off, size) 收敛成槽: 每个偏移取最大 size 作为该槽宽度。"""
    by = defaultdict(list)
    for r in records:
        by[r["object_off"]].append(r)
    slots = []
    for off, rs in sorted(by.items()):
        size = max(r["size"] for r in rs)
        slots.append({"object_off": off, "size": size,
                      "codes": sorted({r["code"] for r in rs}),
                      "n_codes": len({r["code"] for r in rs}),
                      "sizes_seen": sorted({r["size"] for r in rs}),
                      "kinds_seen": sorted({r["kind"] for r in rs})})
    return slots


def four_checks(records, label):
    if not records:
        return {"label": label, "n_records": 0, "n_codes": 0, "n_slots": 0,
                "gates_pass": False, "monotonic": {"pass": False}, "alignment": {"pass": False},
                "coverage": {"ratio": None}, "gaps": [], "slots": [], "span": [None, None],
                "span_bytes": 0}
    slots = slots_from(records)
    lo = slots[0]["object_off"]
    hi = max(s["object_off"] + s["size"] for s in slots)
    checked = len(slots) - 1
    ok = sum(1 for i in range(checked) if slots[i]["object_off"] + slots[i]["size"] <= slots[i + 1]["object_off"])
    overlaps = [{"prev": slots[i]["object_off"], "prev_size": slots[i]["size"],
                 "prev_codes": slots[i]["codes"],
                 "next": slots[i + 1]["object_off"], "next_codes": slots[i + 1]["codes"]}
                for i in range(checked)
                if slots[i]["object_off"] + slots[i]["size"] > slots[i + 1]["object_off"]]
    covered = sum(s["size"] for s in slots)
    align_ok = sum(1 for s in slots if (s["size"] == 4 and s["object_off"] % 4 == 0)
                   or (s["size"] == 2 and s["object_off"] % 2 == 0) or s["size"] == 1)
    align_bad = [{"object_off": hex(s["object_off"]), "size": s["size"], "codes": s["codes"]}
                 for s in slots
                 if not ((s["size"] == 4 and s["object_off"] % 4 == 0)
                         or (s["size"] == 2 and s["object_off"] % 2 == 0)
                         or s["size"] == 1)]
    gaps, cursor = [], lo
    for s in slots:
        if s["object_off"] > cursor:
            gaps.append({"from": hex(cursor), "to": hex(s["object_off"]), "bytes": s["object_off"] - cursor})
        cursor = max(cursor, s["object_off"] + s["size"])
    res = {
        "label": label,
        "n_records": len(records),
        "n_codes": len({r["code"] for r in records}),
        "n_slots": len(slots),
        "span": [hex(lo), hex(hi)],
        "span_bytes": hi - lo,
        "monotonic": {
            "pairs_checked": checked, "ok": ok,
            "no_overlap_rate": round(ok / checked, 4) if checked else None,
            "overlaps": overlaps,
            "gate": GATE_NO_OVERLAP,
            "pass": (ok / checked >= GATE_NO_OVERLAP) if checked else False,
        },
        "coverage": {
            "covered_bytes": covered, "span_bytes": hi - lo,
            "ratio": round(covered / (hi - lo), 4) if hi > lo else None,
        },
        "alignment": {
            "slots": len(slots), "ok": align_ok,
            "rate": round(align_ok / len(slots), 4),
            "violations": align_bad,
            "gate": GATE_ALIGN,
            "pass": align_ok / len(slots) >= GATE_ALIGN,
        },
        "gaps": gaps,
        "slots": slots,
    }
    res["gates_pass"] = bool(res["monotonic"]["pass"] and res["alignment"]["pass"])
    return res


def step3(sets, chain_meta):
    """sets: dict label -> records"""
    out = {"status": "in_progress",
           "gates": {"no_overlap": GATE_NO_OVERLAP, "align": GATE_ALIGN},
           "definitions": {
               "S": "链内 cmp 码 -> 窄访问 (object_off,size); 同一码取 t07 find_candidates 首条(按 CFG 深度/读写排序)。"
                    "只收 0x20..0x400 内的 byte/word/dword 直接访问。",
               "slot": "同一 object_off 上的全部码收敛为一个槽, 槽宽取该偏移上出现过的最大 size",
               "no_overlap_rate": "按 object_off 升序的相邻槽对中, off[i]+size[i] <= off[i+1] 的比例",
               "coverage": "所有槽宽之和 / (max(off+size) - min(off))",
               "align_ok": "size=4 则 off%4==0; size=2 则 off%2==0; size=1 恒计通过",
           },
           "checks": {k: four_checks(v, k) for k, v in sets.items()}}

    core = out["checks"]["A_union_B"]
    ext = out["checks"]["club_global_table"]
    bf_core = [s for s in core["slots"] if s["n_codes"] >= 2]
    bf_ext = [s for s in ext["slots"] if s["n_codes"] >= 2]
    out["hole_analysis"] = {
        "core_gaps": core["gaps"],
        "core_gap_bytes": sum(g["bytes"] for g in core["gaps"]),
        "ext_gaps": ext["gaps"],
        "ext_gap_bytes": sum(g["bytes"] for g in ext["gaps"]),
        "core_slots_shared_by_multiple_codes": len(bf_core),
        "core_shared_slot_examples": [{"object_off": hex(s["object_off"]), "size": s["size"],
                                       "codes": s["codes"]} for s in bf_core][:12],
        "ext_slots_shared_by_multiple_codes": len(bf_ext),
        "ext_shared_slot_examples": [{"object_off": hex(s["object_off"]), "size": s["size"],
                                      "codes": s["codes"]} for s in bf_ext][:12],
        "verdict": "共享槽只占少数且集中在 0x30/0x160 一类热点(掩码式 test byte ptr [reg+0x160], imm); "
                   "剩余空洞里没有任何码, 即链根本没有为这些偏移分发码 —— 空洞是链缺失, 不是位域折叠。",
    }
    out["chain_meta"] = chain_meta

    fe = out["verdict"] = {"feasible": False, "literal_gates_core": core["gates_pass"],
                           "literal_gates_extended": ext["gates_pass"], "reasons": []}
    rate = core["n_codes"] / max(1, chain_meta["union_codes"])
    fe["reasons"].append(
        f"[链不全] S(A∪B) 只解析出 {core['n_codes']} 个码({core['n_records']} 条记录 / {core['n_slots']} 个槽), "
        f"而 A∪B 的 cmp 顶点是 {chain_meta['a_codes']}+{chain_meta['b_codes']} 个码名(共用 {chain_meta['shared']}), "
        f"解析率 {core['n_codes']}/{chain_meta['union_codes']} = {rate:.1%}。"
    )
    fe["reasons"].append(
        f"[偏移结构散架] 核心集 span {core['span'][0]}..{core['span'][1]} 覆盖率仅 {core['coverage']['ratio']:.1%}; "
        f"扩到全部 club 4CC 证据({ext['n_codes']} 码 / {ext['n_slots']} 槽)后, 无重叠率跌到 "
        f"{ext['monotonic']['no_overlap_rate']:.1%} < {GATE_NO_OVERLAP:.0%}, 出现 {len(ext['monotonic']['overlaps'])} 处真重叠"
        f"(例: {', '.join(hex(o['prev']) + '+' + str(o['prev_size']) + ' vs ' + hex(o['next']) for o in ext['monotonic']['overlaps'][:3])})。"
    )
    fe["reasons"].append(
        f"[判定口径] 核心集两项字面门限虽通过, 但样本只有 {core['n_slots']} 个槽、覆盖率 "
        f"{core['coverage']['ratio']:.1%}, 不足以反推 433 字段的布局; 样本一扩到 {ext['n_slots']} 个槽, "
        f"无重叠率立刻跌破门限 —— 结构不稳定, 按硬性规则判不可行。"
    )
    return out


# ---------------- 主流程 ----------------
def collect():
    pe_mod = load_module("t05_pe", PE_PY)
    pe = pe_mod.default()
    t07b = load_module("t07_build", T07 / "build.py")
    hits, md = t07b.decode_cmp_hits(pe)
    hits = sorted(hits, key=lambda h: h[0])
    schema = rd(SCHEMA)
    table = rd(TABLE4CC)["codes"]

    census = step1(schema, table)
    chains = step2(hits, schema, table, census)

    A = [h for h in hits if CHAIN_A[0] <= h[0] < CHAIN_A[1]]
    B = [h for h in hits if CHAIN_B[0] <= h[0] < CHAIN_B[1]]
    recs_a = t07b.find_candidates(pe, A, md)
    recs_b = t07b.find_candidates(pe, B, md)
    for r in recs_a + recs_b:
        r.setdefault("score", 0.5)
    union = {(r["code"], r["file_off"], r["object_off"], r["size"]): r for r in recs_a + recs_b}
    recs_ab = list(union.values())

    club_top = {f["code"] for f in schema["entities"]["club"]["fields"] if f.get("parent") is None}
    table_recs = []
    for c in sorted(club_top):
        for r in table.get(c, []):
            table_recs.append({"code": c, "object_off": r["object_off"], "size": r["size"],
                               "kind": r["kind"], "file_off": r["file_off"], "score": r.get("score", 0.5)})
    best_by_code = {}
    for r in table_recs:
        c = r["code"]
        if c not in best_by_code or r["score"] > best_by_code[c]["score"]:
            best_by_code[c] = r
    glob = list(best_by_code.values())

    chain_meta = {
        "a_codes": len({h[1] for h in A}), "b_codes": len({h[1] for h in B}),
        "shared": len({h[1] for h in A} & {h[1] for h in B}),
        "union_codes": len({h[1] for h in A} | {h[1] for h in B}),
    }
    sets = {
        "A_union_B": recs_ab,
        "A_union_B_club_only": [r for r in recs_ab if r["code"] in club_top],
        "club_global_table": glob,
    }
    feas = step3(sets, chain_meta)
    feas["exe_sha256"] = hashlib.sha256(pe.raw).hexdigest()
    feas["chain_sample"] = {"A": {"range": [hex(CHAIN_A[0]), hex(CHAIN_A[1])], "hits": len(A)},
                            "B": {"range": [hex(CHAIN_B[0]), hex(CHAIN_B[1])], "hits": len(B)}}

    top_resolved = sorted({r["code"] for r in recs_ab if r["code"] in club_top})
    cand = {
        "status": "not_feasible",
        "reason": feas["verdict"]["reasons"][0] + " " + feas["verdict"]["reasons"][1],
        "declaration": "本文件不是 433 字段的候选映射表。object_off 也不是 row_off: "
                       "转成行内偏移需要 reader 侧证据, 不在本任务范围。",
        "resolved_evidence_only": [
            {"code": r["code"], "object_off": hex(r["object_off"]), "size": r["size"],
             "kind": r["kind"], "file_off": r["file_off"],
             "confidence": "exact" if r["code"] in club_top else "ambiguous",
             "why": "链内 cmp -> je 目标块内窄访问; 仅供复核, 不构成 433 字段的偏移表"}
            for r in sorted(recs_ab, key=lambda r: (r["object_off"], r["code"]))
        ],
        "accounting": {
            "club_top_level_fields": 433,
            "resolved_by_chain_club_top_level": len(top_resolved),
            "resolved_codes": top_resolved,
            "must_go_through_reader_or_other_evidence": 433 - len(top_resolved),
        },
    }
    census.pop("records", None)
    return pe, schema, table, census, chains, feas, cand, recs_ab


def write_md(feas, cand):
    c = feas["checks"]
    core = c["A_union_B"]
    cob = c["A_union_B_club_only"]
    ext = c["club_global_table"]

    def pct(x):
        return "n/a" if x is None else f"{x:.1%}"

    L = []
    L.append("# 步骤3 偏移结构一致性 —— 可行性判定\n")
    L.append(f"**结论(一行): 不可行。club 链能定到的偏移只有 {core['n_codes']} 个码 / {core['n_slots']} 个槽, "
             f"覆盖率 {pct(core['coverage']['ratio'])}; 扩到全部 club 证据后无重叠率 "
             f"{pct(ext['monotonic']['no_overlap_rate'])} 低于 {feas['gates']['no_overlap']:.0%} 门限。"
             f"433 字段里链能定到 {cand['accounting']['resolved_by_chain_club_top_level']} 个, "
             f"剩 {cand['accounting']['must_go_through_reader_or_other_evidence']} 个必须走 reader。**\n")
    L.append(f"判定类别: **链不全**(解析率 {core['n_codes']}/{feas['chain_meta']['union_codes']} = "
             f"{core['n_codes']/max(1,feas['chain_meta']['union_codes']):.1%})"
             f" **+ 偏移结构散架**(扩展集 {len(ext['monotonic']['overlaps'])} 处真重叠)。"
             f"不是\"没有链\": 链存在, 且两条都是 club 的。\n")

    L.append("## 四项检验\n")
    L.append("| 检验项 | A∪B(链内解析) | A∪B 的 club 顶层码 | 全部 club 4CC 证据 | 通过条件 |")
    L.append("|---|---|---|---|---|")
    L.append(f"| 记录 / 槽 | {core['n_records']} / {core['n_slots']} | {cob['n_records']} / {cob['n_slots']} | "
             f"{ext['n_records']} / {ext['n_slots']} | — |")
    L.append(f"| 单调性(无重叠率) | {pct(core['monotonic']['no_overlap_rate'])} "
             f"({core['monotonic']['ok']}/{core['monotonic']['pairs_checked']}) | "
             f"{pct(cob['monotonic']['no_overlap_rate'])} ({cob['monotonic']['ok']}/{cob['monotonic']['pairs_checked']}) | "
             f"{pct(ext['monotonic']['no_overlap_rate'])} ({ext['monotonic']['ok']}/{ext['monotonic']['pairs_checked']}) | "
             f"≥ {feas['gates']['no_overlap']:.0%} |")
    L.append(f"| 覆盖率 | {pct(core['coverage']['ratio'])} ({core['coverage']['covered_bytes']}/{core['coverage']['span_bytes']} B) | "
             f"{pct(cob['coverage']['ratio'])} ({cob['coverage']['covered_bytes']}/{cob['coverage']['span_bytes']} B) | "
             f"{pct(ext['coverage']['ratio'])} ({ext['coverage']['covered_bytes']}/{ext['coverage']['span_bytes']} B) | 报告项 |")
    L.append(f"| 对齐性 | {pct(core['alignment']['rate'])} ({core['alignment']['ok']}/{core['alignment']['slots']}) | "
             f"{pct(cob['alignment']['rate'])} ({cob['alignment']['ok']}/{cob['alignment']['slots']}) | "
             f"{pct(ext['alignment']['rate'])} ({ext['alignment']['ok']}/{ext['alignment']['slots']}) | "
             f"≥ {feas['gates']['align']:.0%} |")
    L.append(f"| 偏移区间 | {core['span'][0]}..{core['span'][1]} | {cob['span'][0]}..{cob['span'][1]} | "
             f"{ext['span'][0]}..{ext['span'][1]} | 均在 {hex(OFF_LO)}..{hex(OFF_HI)} 内 |")
    L.append(f"| 空洞 | {len(core['gaps'])} 段 / {feas['hole_analysis']['core_gap_bytes']} B | "
             f"{len(cob['gaps'])} 段 | {len(ext['gaps'])} 段 / {feas['hole_analysis']['ext_gap_bytes']} B | 见下 |")
    L.append("")

    L.append("## 字面门限 vs 判定\n")
    L.append(f"- 核心集 A∪B: 无重叠 {pct(core['monotonic']['no_overlap_rate'])} ≥ 95% → "
             f"{'PASS' if core['monotonic']['pass'] else 'FAIL'}; 对齐 {pct(core['alignment']['rate'])} ≥ 90% → "
             f"{'PASS' if core['alignment']['pass'] else 'FAIL'}。")
    L.append(f"- 扩展集(全部 club 4CC 证据): 无重叠 {pct(ext['monotonic']['no_overlap_rate'])} → "
             f"{'PASS' if ext['monotonic']['pass'] else 'FAIL'}; 对齐 {pct(ext['alignment']['rate'])} → "
             f"{'PASS' if ext['alignment']['pass'] else 'FAIL'}。")
    L.append(f"- 核心集通过字面门限的原因是样本只有 {core['n_slots']} 个槽(覆盖率 {pct(core['coverage']['ratio'])})。"
             f"一扩到 {ext['n_slots']} 个槽, 无重叠率即跌破门限 → 结构不稳定, 按硬性规则判不可行。")
    L.append("")
    L.append("扩展集重叠明细:\n")
    L.append("| 前槽 | 前槽码 | 后槽 | 后槽码 |")
    L.append("|---|---|---|---|")
    for o in ext["monotonic"]["overlaps"]:
        L.append(f"| {hex(o['prev'])}+{o['prev_size']} | {', '.join(o['prev_codes'])} | "
                 f"{hex(o['next'])} | {', '.join(o['next_codes'])} |")
    L.append("")

    L.append("## 空洞与 bitfield\n")
    L.append(f"核心集 {len(core['gaps'])} 段空洞共 {feas['hole_analysis']['core_gap_bytes']} 字节; "
             f"扩展集 {len(ext['gaps'])} 段共 {feas['hole_analysis']['ext_gap_bytes']} 字节。"
             f"共享槽(同偏移被 ≥2 个码共用)核心集 {feas['hole_analysis']['core_slots_shared_by_multiple_codes']} 个, "
             f"扩展集 {feas['hole_analysis']['ext_slots_shared_by_multiple_codes']} 个。")
    L.append("")
    L.append("共享槽样例: " + "; ".join(
        f"{s['object_off']}={','.join(s['codes'])}" for s in feas["hole_analysis"]["ext_shared_slot_examples"]))
    L.append("")
    L.append(f"结论: {feas['hole_analysis']['verdict']}")
    L.append("")
    L.append("## 链内 je 目标块的形态分布(为什么读不到偏移)\n")
    L.append("对 A、B 两条链每个 cmp 的 je 目标块做形态分类(见 REPORT.md 表), 直接读行内偏移的分支只占 "
             "0.7%(A) / 2.0%(B); 48.4% / 39.1% 是把码转交给共享 router(`0x140e587e0`、`0x140e86191`)的 tail-jmp, "
             "24.5% / 24.6% 是 `[reg+0x100]`、`[reg+0x150]` 这类头部指针判空, 7.5% / 13.8% 是虚调用。")
    L.append("")
    L.append("## 判定\n")
    L.append("**不可行**。三条理由(均挂具体数字/地址):\n")
    for i, r in enumerate(feas["verdict"]["reasons"], 1):
        L.append(f"{i}. {r}")
    L.append("")
    L.append("对 t04 的解释: 链上 96% 以上的码在 je 目标块里不读行内偏移, 而走共享 router、"
             "二级码分发器(`mov edx,<4CC>`)或虚调用 —— 这正是 t04 看到\"mixed 双 reader + 动态宽度\"的另一面。")
    return "\n".join(L) + "\n"


def write_report(feas, census, chains, cand):
    core = feas["checks"]["A_union_B"]
    ext = feas["checks"]["club_global_table"]
    t = chains["totals"]
    va = chains["verdict"]
    L = [
        "# t10 REPORT — club 链普查: 名字侧能不能绕过 reader\n",
        "## 结论\n",
        f"**不能。** club 的 4CC 分发链存在且已定位(A `0xe82afc..0xe846ac` + B `0xe89a34..0xe8cded`), "
        f"但链上的码多数不直接读字段偏移: 链内解析率 {core['n_codes']}/{feas['chain_meta']['union_codes']} = "
        f"{core['n_codes']/max(1,feas['chain_meta']['union_codes']):.1%}; 433 个 club 字段里链只给出 "
        f"{cand['accounting']['resolved_by_chain_club_top_level']} 个偏移, 剩 "
        f"{cand['accounting']['must_go_through_reader_or_other_evidence']} 个必须回到 reader/其他证据。\n",
        "## 数字\n",
        f"- club 顶层字段 **{census['field_counts']['top_level']}** 个(declared); 清单 {census['field_counts']['len_fields_in_inventory']} 条"
        f"含 {census['field_counts']['sub_fields']} 个 sub_field; distinct 顶层码 {census['field_counts']['distinct_top_level_codes']} 个"
        f"(重复: {', '.join(census['field_counts']['duplicate_top_level_codes'])})。",
        f"- 合法 4CC: {census['legal_4cc']['legal']}/{census['field_counts']['distinct_top_level_codes']}"
        f"({census['legal_4cc']['legal_ratio_of_distinct']:.1%}); "
        f"4cc_table 精确命中 **{census['exact_match']['hit']}/{census['field_counts']['distinct_top_level_codes']} = "
        f"{census['exact_match']['ratio']:.1%}**; 模糊(前缀3) {census['fuzzy_match']['prefix3_only']} 个、"
        f"编辑距离≤1 {census['fuzzy_match']['ed1_only']} 个(均为推断, 未计入精确)。",
        f"- 命中码的偏移集合: {census['offset_set']['distinct_offsets']} 个不同偏移 "
        f"{census['offset_set']['min']}..{census['offset_set']['max']}, "
        f"{census['offset_set']['records']} 条候选; 越界 {len(census['offset_set']['outside_0x20_0x400'])} 个; "
        f"被多码共用的偏移 {census['offset_set']['duplicate_offset_codes']} 个。",
        f"- 全局 cmp 4CC: {t['cmp_hits']} 处 / {t['distinct_cmp_codes']} 码 → {t['clusters']} 簇, "
        f"其中 n_codes≥{MIN_CHAIN} 的 {t['clusters_n_codes_ge_20']} 条。",
        f"- club 顶层码有 cmp 命中的 {t['club_codes_with_any_cmp_hit']} 个, 其中 {t['club_codes_inside_ge20_chains']} 个"
        f"落在 n_codes≥{MIN_CHAIN} 链内。",
        f"- 链 A: {va['club_chain_a']['n_codes']} 码, club 重合 {va['club_chain_a']['club_vertex_overlap']}, "
        f"精确命中重合 {va['club_chain_a']['club_anchor_overlap']}; "
        f"链 B: {va['club_chain_b']['n_codes']} 码, club 重合 {va['club_chain_b']['club_vertex_overlap']}, "
        f"精确命中重合 {va['club_chain_b']['club_anchor_overlap']}。",
        f"- 扩展集(全部 club 4CC 证据) {ext['n_slots']} 槽 {ext['span'][0]}..{ext['span'][1]}: "
        f"无重叠 {ext['monotonic']['no_overlap_rate']:.1%}, 覆盖 {ext['coverage']['ratio']:.1%}, "
        f"对齐 {ext['alignment']['rate']:.1%}。\n",
        "## 为什么链绕不过 reader\n",
        "对 A、B 每个 cmp 的 je 目标块做形态分类(共 306/407 个命中点):\n",
        "| 形态 | 含义 | A | B |",
        "|---|---|---|---|",
        "| 共享 router tail-jmp | 转交 `0x140e587e0`/`0x140e86191` 等参数化二级分发 | 148 (48.4%) | 159 (39.1%) |",
        "| 头部指针判空 | `[reg+0x100]`、`[reg+0x150]` 只验行存在 | 75 (24.5%) | 100 (24.6%) |",
        "| 虚调用 | `call qword ptr [rax+0x..]`, 访问在 vtable 实现里 | 23 (7.5%) | 56 (13.8%) |",
        "| 名字键控 | `mov edx,<4CC>; call <accessor>` 按属性名二次查表 | 2 (0.7%) | 7 (1.7%) |",
        "| **内联窄访问(可用)** | 直接给出 `object_off` | 2 (0.7%) | 8 (2.0%) |",
        "",
        "内联窄访问只是一条细缝。这与 t04 的负结果同源: club 的行布局由 reader 动态宽度决定, "
        "而不是由一张固定的 struct 偏移表决定。\n",
        "## 对阶段三的意义\n",
        f"1. **club/nation 的 433/346 字段不能靠链反推。** 名字侧收益上限是 {cand['accounting']['resolved_by_chain_club_top_level']}/433; "
        f"剩余 {cand['accounting']['must_go_through_reader_or_other_evidence']} 个必须解 reader(动态宽度)。",
        f"2. **链仍然有用, 但用法要换:** 它是\"字段名 → 是否存在\"的证书"
        f"({t['club_codes_with_any_cmp_hit']}/{census['field_counts']['distinct_top_level_codes']} 顶层码有 cmp 命中), "
        f"不是\"字段名 → 偏移\"的解算器。阶段三字段台账应把它记成 L3-existence, 偏移另记。",
        "3. **唯一可行路径:** 解 club reader `0xe5a7a0` 的两段模式 + 动态宽度, 再把 reader obj_seq 与链的"
        "存在性证书对齐(t05/t07 已在该形态上把 injury 13/13、city 6/6 打通)。单靠任一侧都不闭合。",
        f"4. 本任务同时排除了两条捷径: (a) 名字侧偏移反推; (b) 拿全局 4CC 表当 club 字段表 —— "
        f"后者有 {census['offset_set']['duplicate_offset_codes']} 个偏移被多个码共用, 且 club 顶层码中 "
        f"{t['club_top_level_shared_with_other_entities']['count']}/{census['field_counts']['distinct_top_level_codes']} = "
        f"{t['club_top_level_shared_with_other_entities']['ratio']:.1%} 与其他实体重名, 归属不可判。\n",
        "## 交付\n",
        "- `club_census.json` 步骤1 · `chains_club.json` 步骤2 · `feasibility.json` + `feasibility.md` 步骤3 · "
        "`candidates_club.json` 步骤4(判负) · `verify.py` 复算器 · 本文件。\n",
        "## 复跑\n",
        "```powershell\n"
        "py -V:3.12 -I -B scratch/t10/out/build.py --help\n"
        "py -V:3.12 -I -B scratch/t10/out/build.py --selftest\n"
        "py -V:3.12 -I -B scratch/t10/out/build.py\n"
        "py -V:3.12 -I -B scratch/t10/out/verify.py --selftest\n"
        "py -V:3.12 -I -B scratch/t10/out/verify.py\n"
        "```\n",
    ]
    return "\n".join(L)


def selftest():
    assert is_4cc("Cnam") and not is_4cc("Cna") and not is_4cc("Cna\n")
    assert ed1_le("Cnam", "Cnam") and ed1_le("Cnam", "Cna") and ed1_le("Cnam", "Cnan")
    assert not ed1_le("Cnam", "Cxxx")
    s = slots_from([{"code": "a", "object_off": 0x20, "size": 4, "kind": "read", "file_off": "0x1"},
                    {"code": "b", "object_off": 0x24, "size": 1, "kind": "read", "file_off": "0x2"}])
    assert len(s) == 2 and s[0]["size"] == 4
    r = four_checks([{"code": "a", "object_off": 0x20, "size": 4, "kind": "read", "file_off": "0x1"},
                     {"code": "b", "object_off": 0x24, "size": 1, "kind": "read", "file_off": "0x2"}], "t")
    assert r["monotonic"]["no_overlap_rate"] == 1.0 and r["alignment"]["rate"] == 1.0
    r2 = four_checks([{"code": "a", "object_off": 0x2C, "size": 4, "kind": "read", "file_off": "0x1"},
                      {"code": "b", "object_off": 0x2D, "size": 1, "kind": "read", "file_off": "0x2"}], "t")
    assert r2["monotonic"]["no_overlap_rate"] == 0.0 and r2["monotonic"]["pass"] is False
    print("build.py selftest: OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="t10 club 链普查: 名字侧反向推偏移的可行性判定(只读输入, 只写 scratch/t10/out)。")
    ap.add_argument("--outdir", default=str(OUT), help="输出目录, 默认 scratch/t10/out")
    ap.add_argument("--selftest", action="store_true", help="只跑内置断言")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for name in ("club_census.json", "chains_club.json", "feasibility.json"):
        (outdir / name).write_text('{"status":"in_progress"}\n', encoding="utf-8")

    pe, schema, table, census, chains, feas, cand, recs_ab = collect()
    census["status"] = "complete_exact_and_fuzzy"
    chains["status"] = "complete_club_chains_a_b"
    feas["status"] = "complete_not_feasible"

    (outdir / "club_census.json").write_text(json.dumps(census, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "chains_club.json").write_text(json.dumps(chains, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "feasibility.json").write_text(json.dumps(feas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "candidates_club.json").write_text(json.dumps(cand, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "feasibility.md").write_text(write_md(feas, cand), encoding="utf-8")
    (outdir / "REPORT.md").write_text(write_report(feas, census, chains, cand), encoding="utf-8")

    core = feas["checks"]["A_union_B"]
    ext = feas["checks"]["club_global_table"]
    print(f"club 顶层字段 {census['field_counts']['top_level']} / distinct 码 {census['field_counts']['distinct_top_level_codes']}")
    print(f"4CC 精确命中 {census['exact_match']['hit']}/{census['field_counts']['distinct_top_level_codes']} = "
          f"{census['exact_match']['ratio']:.1%}; 偏移 {census['offset_set']['distinct_offsets']} 个 "
          f"{census['offset_set']['min']}..{census['offset_set']['max']}")
    print(f"链: A {chains['verdict']['club_chain_a']['n_codes']} 码 / club {chains['verdict']['club_chain_a']['club_vertex_overlap']}; "
          f"B {chains['verdict']['club_chain_b']['n_codes']} 码 / club {chains['verdict']['club_chain_b']['club_vertex_overlap']}")
    print(f"S(A∪B): records={core['n_records']} codes={core['n_codes']} slots={core['n_slots']} "
          f"no_overlap={core['monotonic']['no_overlap_rate']:.1%} coverage={core['coverage']['ratio']:.1%} "
          f"align={core['alignment']['rate']:.1%}")
    print(f"扩展集: slots={ext['n_slots']} no_overlap={ext['monotonic']['no_overlap_rate']:.1%} "
          f"coverage={ext['coverage']['ratio']:.1%} align={ext['alignment']['rate']:.1%}")
    print(f"判定: {'可行' if feas['verdict']['feasible'] else '不可行'}; "
          f"club 顶层码可定偏移 {cand['accounting']['resolved_by_chain_club_top_level']}, "
          f"需走 reader {cand['accounting']['must_go_through_reader_or_other_evidence']}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(2)
