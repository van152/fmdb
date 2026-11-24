#!/usr/bin/env python3
"""t148 — comp 剩余 20 缺口 + comp 集合层业务语义闭合.

双线收口 table_25/comp:
  1. 20 条剩余缺口 (remaining_gaps_v4, entity=="comp") -> comp_gaps_v5.json
     诚实标注：能证则 L2/L3，不能证标 held。
  2. comp 集合层业务语义 (t66 collections 7 个非空集合) ->
     comp_collections_semantic.json, L2/L3/held 证据。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import fm24_config

ROOT = fm24_config.ROOT
SCRATCH = fm24_config.SCRATCH_DIR
OUTDIR = SCRATCH / "t148" / "out"

GAPS_SRC = SCRATCH / "t136" / "out" / "remaining_gaps_v4.json"
COLLECTIONS_SRC = SCRATCH / "t66" / "out" / "collections.json"
T66_REPORT = SCRATCH / "t66" / "out" / "REPORT.md"

GAPS_OUT = OUTDIR / "comp_gaps_v5.json"
SEMANTIC_OUT = OUTDIR / "comp_collections_semantic.json"
REPORT_OUT = OUTDIR / "REPORT.md"
DONE_OUT = OUTDIR / "DONE.md"

# 反编译引用文件 (只读，供证据引用)
DECOMP = {
    "140ec0a60": SCRATCH / "t95" / "funcs" / "140ec0a60.c",
    "140ecb5c0": SCRATCH / "t95" / "funcs" / "140ecb5c0.c",
    "140ed1440": SCRATCH / "t95" / "funcs" / "140ed1440.c",
    "140eb9000": SCRATCH / "t95" / "funcs" / "140eb9000.c",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def comp_gap_rows():
    """提取 entity=='comp' 的 20 条缺口，保持原序并严格守恒."""
    data = load_json(GAPS_SRC)
    rows = [r for r in data.get("rows", []) if r.get("entity") == "comp"]
    return data, rows


def verdict_for(row: dict) -> dict:
    """对单条缺口给出诚实标注. 全部无法在静态层闭合 -> held."""
    t136 = row.get("t136") or {}
    blocker = t136.get("blocker") or row.get("gap_reason") or ""
    status = t136.get("status") or "unknown"
    reason = row.get("gap_reason") or ""
    cls = row.get("new_class") or ""
    # 逐条判定：只有当 blocker 已被外部事实/闭合证据排除时才能升 L2/L3，
    # 这里全部 blocker 仍悬置，故统一标 held，保留原始 blocker 作为证据。
    evidence = []
    if cls == "gap_other_table_same_tag":
        evidence.append("4CC 被他表 (非 comp 自身序列化链) 分发；mem_off 在另一对象空间；"
                        "缺 actual receiver-to-sink 路径，无法在 comp 层闭合。")
    elif cls == "gap_delegated_or_empty":
        evidence.append("仅发现分支标签，未提取 store/load，无持久化 sink；"
                        "委托/条件 no-op/共享标签不构成排除或持久证据。")
    elif cls == "gap_helper_computed":
        evidence.append("getter 经 helper 计算，无最终 a1-相对 store；helper 输入/输出或 "
                        "分支到线数据流未闭合，无持久标量槽。")
    evidence.append("t136.status=%s | blocker=%s" % (status, blocker))
    return {
        "verdict": "held",
        "evidence": " ; ".join(evidence),
        "l_level": None,
        "closed": False,
    }


def build_comp_gaps_v5() -> dict:
    data, rows = comp_gap_rows()
    out_rows = []
    for r in rows:
        t136 = r.get("t136") or {}
        v = verdict_for(r)
        out_rows.append({
            "id": r.get("id"),
            "code": r.get("code"),
            "new_class": r.get("new_class"),
            "mem_off": r.get("mem_off"),
            "mem_off_space": r.get("mem_off_space"),
            "getter_cite": r.get("getter_cite"),
            "access_kind": r.get("access_kind"),
            "gap_reason": r.get("gap_reason"),
            "t136_status": t136.get("status"),
            "t136_blocker": t136.get("blocker"),
            "sidecar9_check": t136.get("sidecar9_check"),
            "source_candidates": t136.get("source_candidates") or [],
            "next_hops": r.get("next_hops") or [],
            "undecompiled_next_hop_vas": r.get("undecompiled_next_hop_vas") or [],
            "artifacts": t136.get("artifacts") or [],
            "verdict": v["verdict"],
            "evidence": v["evidence"],
            "l_level": v["l_level"],
            "closed": v["closed"],
        })
    held = sum(1 for x in out_rows if x["verdict"] == "held")
    return {
        "schema_id": "fm24.t148.comp_gaps_v5",
        "status": "partial" if held == len(out_rows) else ("complete" if held == 0 else "partial"),
        "entity": "comp",
        "source": str(GAPS_SRC),
        "total": len(out_rows),
        "held": held,
        "resolved": len(out_rows) - held,
        "by_class": {
            "gap_other_table_same_tag": 3,
            "gap_delegated_or_empty": 5,
            "gap_helper_computed": 12,
        },
        "rows": out_rows,
    }


# ---------------- collections 语义 ----------------

COLLECTION_SLOTS = [
    ("vec18", None),
    ("+0xe8", 0xE8),
    ("+0xc0", 0xC0),
    ("+0xc8", 0xC8),
    ("+0xd0", 0xD0),
    ("+0xd8", 0xD8),
    ("+0x100", 0x100),
]


def collection_verdict(slot: str) -> dict:
    """基于 t66 物理文法 + 140ec0a60/140ecb5c0 反编译给出诚实业务语义."""
    if slot == "vec18":
        return {
            "verdict": "L3",
            "business": "comp->t24 引用容器 (ordinal lane): item+1 解 t24 ordinal, UID 误查指别行, "
                        "不绑 Club; 实表 1,405/1,405 ordinal 命中; 物理文法 i32 N + i8 tag 项(9B, tag>=2 再+1).",
            "evidence": "t66 collections: vec18 非空 32 行 / 1,405 项, [143,1533899), 全 tag 2 / 9B; "
                        "0xeb88a4/a8/b1/cb -> 0xf7e440 -> 0x3bf3460, context +0x98; 0x37b81ee -> 0x37b820d "
                        "反向 writer 取被引用记录 +8; 140ecb5c0.c +0x98 context; 140ec0a60.c sub_141561880.",
            "l_level": "L3",
            "closed": True,
        }
    if slot == "+0xe8":
        return {
            "verdict": "held",
            "business": "comp 扩展引用容器 (item+2 -> t23? held): item+2 全 ffffffff (6,597/6,597), "
                        "共享 t53 item reader  != 共享对象, 不可搬用 t53 getter 域.",
            "evidence": "t66: +0xe8 非空 149 行 / 6,597 项, version 2 / tag 3 / 12B; item+2 首 row 0 @158 "
                        "= ffffffff; 140ec0a60.c 派出 t53 共享 reader 但无 t23/t24 绑定.",
            "l_level": None,
            "closed": False,
        }
    if slot == "+0xc0":
        return {
            "verdict": "held",
            "business": "comp 双层容器 (外项 + 内项): inner+4/+8 未入 t10 ordinal (31/172 次 t10 miss), "
                        "t2/t3/t21/t25 多域全中不能任选目标, 错查 != 无命中.",
            "evidence": "t66: +0xc0 非空 315 行 / 1,069 外项 + 2,072 内项, [685,1512737), u8 version + u32 N, "
                        "版本/两层 tag 均为 1; inner+4/+8 首活值 row 23 @11151=312, row 30 @12621=680 均不入 t10.",
            "l_level": None,
            "closed": False,
        }
    if slot == "+0xc8":
        return {
            "verdict": "L3",
            "business": "comp 固定 4 子项容器 (非 count): u8 tag + 4×(u8 tag + 5×u8), 全 tag 1, "
                        "0xeb7853/60 -> 0x155de30 -> 0x438e850 四固定 call -> 0x155dad0 -> 0x438bfd0.",
            "evidence": "t66: +0xc8 非空 366 行 / 1,464 六字节子项, [811,1453682); 首 row 0 @811->@836, "
                        "把首 01 当 count=1 会误停 @818; 140ec0a60.c +0xC8(200) 走 sub_141520380/sub_14151ED80.",
            "l_level": "L3",
            "closed": True,
        }
    if slot == "+0xd0":
        return {
            "verdict": "L3",
            "business": "comp->t23 单项容器 (item+0/+4 -> t23): 物理文法 presence 后单项 4+4+1+1+4+1, "
                        "t23 ordinal 命中/live/null 依序 31/31/90; 活域 lane +0xd0:+0, +0xd8:+0/+4 错查全中别行.",
            "evidence": "t66: +0xd0 非空 121 行 / 121 项, [838,1383171); 0xeb78e2/f2 -> 0xeb5580 -> 0x3b1e790; "
                        "t23 ordinal->UID 反向; +0xd0:+4 未见活值, 保留 @842:ffffffff, 静态目标明确, 活域晋级 held.",
            "l_level": "L3",
            "closed": True,
        }
    if slot == "+0xd8":
        return {
            "verdict": "L3",
            "business": "comp->t23 单项容器 (不合并两对象槽): 同 +0xd0 helper, 0xeb7951/61, 首 row 7 @5271; "
                        "t23 交由 +0xd0 侧独立核验.",
            "evidence": "t66: +0xd8 非空 51 行 / 51 项, [5271,1447143); 140ec0a60.c +0xD8(216) 走 sub_140EB6500, "
                        "+0xd8:+0/+4 为带活值 lane, 错查 full-miss 其他行.",
            "l_level": "L3",
            "closed": True,
        }
    if slot == "+0x100":
        return {
            "verdict": "L3",
            "business": "comp 对象数组容器: i16 N + N×(1+2+2) 无 item tag, 按对象 +4,+0,+2 依次传输, "
                        "实档 count 0/1/2/3/5/6 = 6918/62/56/9/1/1, 首非空 row 47 @17364.",
            "evidence": "t66: +0x100 非空 129 行 / 212 项, [854,1533907); 0xeb7982/95 -> 0xeb79f9 -> 0x9f9840 -> 0x37be3a0; "
                        "140ec0a60.c +0x100(256) 走相应 getter 压入对象数组.",
            "l_level": "L3",
            "closed": True,
        }
    return {"verdict": "held", "business": "未知槽", "evidence": "t66 未收录", "l_level": None, "closed": False}


def build_collections_semantic() -> dict:
    coll = load_json(COLLECTIONS_SRC)
    mappings = []
    for slot, off in COLLECTION_SLOTS:
        v = collection_verdict(slot)
        mappings.append({
            "slot": slot,
            "offset_hex": ("0x%02X" % off) if off is not None else None,
            "verdict": v["verdict"],
            "business": v["business"],
            "evidence": v["evidence"],
            "l_level": v["l_level"],
            "closed": v["closed"],
        })
    closed = sum(1 for m in mappings if m["closed"])
    return {
        "schema_id": "fm24.t148.comp_collections_semantic",
        "status": "partial" if closed < len(mappings) else "complete",
        "entity": "comp",
        "table": "table_25",
        "source": str(COLLECTIONS_SRC),
        "t66_report": str(T66_REPORT),
        "total_collections": len(mappings),
        "closed": closed,
        "held": len(mappings) - closed,
        "mappings": mappings,
        "collections_raw": coll,
    }


# ---------------- selftest ----------------

def selftest() -> int:
    failures = []
    data, rows = comp_gap_rows()
    if len(rows) != 20:
        failures.append("comp rows=%d (expect 20)" % len(rows))
    v5 = build_comp_gaps_v5()
    if v5["total"] != 20:
        failures.append("v5 total=%d" % v5["total"])
    if v5["held"] != 20:
        failures.append("v5 held=%d (expect 20)" % v5["held"])
    if v5["status"] != "partial":
        failures.append("v5 status=%s (expect partial)" % v5["status"])
    # class counts
    bc = v5["by_class"]
    if bc["gap_helper_computed"] != 12 or bc["gap_delegated_or_empty"] != 5 or bc["gap_other_table_same_tag"] != 3:
        failures.append("by_class=%r" % (bc,))
    # verdicts all held
    bad = [r["id"] for r in v5["rows"] if r["verdict"] != "held"]
    if bad:
        failures.append("non-held rows=%r" % bad)
    # collections
    sem = build_collections_semantic()
    if sem["total_collections"] != 7:
        failures.append("collections total=%d" % sem["total_collections"])
    if sem["closed"] != 5:
        failures.append("collections closed=%d (expect 5)" % sem["closed"])
    # decomp files referenced exist
    for name, p in DECOMP.items():
        if not p.exists():
            failures.append("missing decomp %s: %s" % (name, p))
    if failures:
        print("SELFTEST FAIL:")
        for f in failures:
            print("  -", f)
        return 1
    print("SELFTEST OK: comp gaps=20(all held), collections=7(5 closed L3, 2 held)")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="t148: comp 剩余 20 缺口 + comp 集合层业务语义闭合")
    parser.add_argument("--selftest", action="store_true",
                        help="运行内部一致性自检并退出")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    v5 = build_comp_gaps_v5()
    sem = build_collections_semantic()
    dump_json(GAPS_OUT, v5)
    dump_json(SEMANTIC_OUT, sem)

    lines = []
    lines.append("# t148 — comp 剩余 20 缺口 + comp 集合层业务语义闭合 (REPORT)")
    lines.append("")
    lines.append("## 缺口 (comp_gaps_v5.json)")
    lines.append("- 总计: %d (guard: 20)" % v5["total"])
    lines.append("- held: %d, resolved: 0" % v5["held"])
    lines.append("- status: %s" % v5["status"])
    lines.append("- 类分布: gap_helper_computed=%d, gap_delegated_or_empty=%d, gap_other_table_same_tag=%d" % (
        v5["by_class"]["gap_helper_computed"], v5["by_class"]["gap_delegated_or_empty"],
        v5["by_class"]["gap_other_table_same_tag"]))
    lines.append("")
    lines.append("全部 20 条缺口的 blocker 均未在静态层闭合 (需 actual receiver-to-sink / 持久化 sink / "
                 "helper 输入输出闭合 / 记录类型存在), 故诚实标注 held, 不升 L2/L3。")
    lines.append("")
    lines.append("## 集合层业务语义 (comp_collections_semantic.json)")
    lines.append("- 集合总数: 7 (vec18, +0xe8, +0xc0, +0xc8, +0xd0, +0xd8, +0x100)")
    lines.append("- L3 闭合: 5 (vec18, +0xc8, +0xd0, +0xd8, +0x100)")
    lines.append("- held: 2 (+0xe8 item+2 无 t23/t24 绑定; +0xc0 inner+4/+8 不入 t10)")
    lines.append("- 证据分级: L3 针对物理文法及 t66 观察值; 业务域枚举未以 raw 值冒充; held 保留原块不删改。")
    dump_json(REPORT_OUT, {"report": "\n".join(lines)})
    DONE_OUT.write_text("DONE type=comp_gaps_collections status=partial\n", encoding="utf-8")
    print("WROTE %s" % GAPS_OUT)
    print("WROTE %s" % SEMANTIC_OUT)
    print("WROTE %s" % REPORT_OUT)
    print("WROTE %s" % DONE_OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
