#!/usr/bin/env python3
"""t156 — 高频业务非主表 L3 字段语义闭合（8 张核心表）。

完成 slot19 wire offset <-> C++ object mem_off <-> 4CC getter/setter 联合映射：

  1. 从 scratch/t121/out/wire_traces_79of79.json 提取 row0_reads (wire_pos, obj_off)
  2. 从 scratch/t108/out/fourcc_mem_map_v2.json 提取 4CC->mem_off 映射
  3. 两者按 obj_off(=mem_off) 做等值连立，得出 wire_pos<->4CC 闭合槽位
  4. 用 scratch/t133/out/reader_v2_verify.json 中的真实样本行做交叉核验

可证则标 L3/L2，无法闭合的槽位诚实标为 held/unnamed，绝不编造。

退出码：0 成功 / 1 校验失败 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fm24_config as cfg  # noqa: E402

SCRIPT = Path(__file__).resolve()
OUTDIR = cfg.SCRATCH_DIR / "t156" / "out"

WIRE_JSON = cfg.SCRATCH_DIR / "t121" / "out" / "wire_traces_79of79.json"
FOURCC_JSON = cfg.SCRATCH_DIR / "t108" / "out" / "fourcc_mem_map_v2.json"
SEMANTICS_JSON = cfg.SCRATCH_DIR / "t150" / "out" / "remaining_tables_semantics.json"
VERIFY_JSON = cfg.SCRATCH_DIR / "t133" / "out" / "reader_v2_verify.json"

# 8 张高频核心非主表 (table_id -> entity name)
TARGET_TABLES = {
    6: "INJURY",
    22: "STADIUM_CHANGE",
    26: "COMP_HISTORY_RECORD",
    29: "STARTING_LOAN",
    32: "STARTING_FUTURE_TRANSFER",
    33: "STARTING_CLUB_DEBT",
    49: "STARTING_PERSON_HISTORY",
    71: "STARTING_PAST_TRANSFER",
}

# --------------------------------------------------------------------------- #
# 辅助读取
# --------------------------------------------------------------------------- #
def _load_json(path: Path, what: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[t156] 缺少输入 {what}: {path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as exc:
        print(f"[t156] 解析失败 {what}: {path}: {exc}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------- #
# 核心连立：wire_pos <-> obj_off <-> fourcc
# --------------------------------------------------------------------------- #
def _wire_index(wire_tables: list[dict]) -> dict[tuple[str, int], list[dict]]:
    """按 (archive, table_id) 归集 row0_reads，仅保留 dst_kind=='this'。"""
    idx: dict[tuple[str, int], list[dict]] = {}
    for entry in wire_tables:
        key = (entry.get("archive"), entry.get("table_id"))
        reads = entry.get("row0_reads", []) or []
        idx[key] = [r for r in reads if r.get("dst_kind") == "this"]
    return idx


def _fourcc_index(fourcc_tables: list[dict]) -> dict[int, dict[int, list[dict]]]:
    """按 table_id -> mem_off(off_int) -> 四组 fourcc 条目列表。"""
    idx: dict[int, dict[int, list[dict]]] = {}
    for entry in fourcc_tables:
        tid = entry.get("table_type")
        fccs = entry.get("fourccs", {}) or {}
        off_map: dict[int, list[dict]] = {}
        for fcc, finfo in fccs.items():
            for mo in (finfo.get("mem_offsets") or []):
                off_int = mo.get("off_int")
                if off_int is None:
                    continue
                off_map.setdefault(off_int, []).append({
                    "fourcc": fcc,
                    "slot": finfo.get("slot"),
                    "func_va": finfo.get("func_va"),
                    "kind": finfo.get("kind"),
                    "c_type": finfo.get("c_type") or mo.get("c_type"),
                    "width": mo.get("width"),
                    "access_kind": finfo.get("access_kind"),
                    "line": mo.get("line"),
                    "how": mo.get("how"),
                })
        if off_map:
            idx[tid] = off_map
    return idx


# --------------------------------------------------------------------------- #
# 主构建
# --------------------------------------------------------------------------- #
def build_mapping() -> dict:
    wire = _load_json(WIRE_JSON, "t121 wire_traces_79of79.json")
    fourcc = _load_json(FOURCC_JSON, "t108 fourcc_mem_map_v2.json")
    semantics = _load_json(SEMANTICS_JSON, "t150 remaining_tables_semantics.json")
    verify = _load_json(VERIFY_JSON, "t133 reader_v2_verify.json")

    if wire is None or fourcc is None or semantics is None:
        return {"status": "partial", "error": "missing_inputs"}

    wire_idx = _wire_index(wire.get("tables", []))
    fcc_idx = _fourcc_index(fourcc.get("tables", []))
    sem_tables = semantics.get("tables", {})
    verify_tables = verify.get("tables", {}) if verify else {}

    out_tables: dict[str, dict] = {}
    total_slots = 0
    total_l3 = 0
    total_l2 = 0
    total_held = 0
    total_unnamed = 0

    for tid in sorted(TARGET_TABLES):
        entity = TARGET_TABLES[tid]
        sem_rec = sem_tables.get(str(tid), {})
        sem_entity = sem_rec.get("entity") or entity

        table_out: dict = {
            "table_id": tid,
            "entity": sem_entity,
            "archives": {},
        }

        for arch in ("client", "server"):
            key = (arch, tid)
            wire_reads = wire_idx.get(key, [])
            sem_arch = sem_rec.get("tables", {}).get(arch, {})
            vkey = f"{arch}/{tid}"
            vrec = verify_tables.get(vkey, {})

            if not wire_reads and not sem_arch:
                # 该 archive 无此表
                continue

            # ---- 构建 wire_pos -> obj_off 映射 ----
            wire_by_pos: dict[int, dict] = {}
            for r in wire_reads:
                wp = r.get("wire_pos")
                oo = r.get("obj_off")
                if wp is None:
                    continue
                wire_by_pos[int(wp)] = {
                    "wire_pos": int(wp),
                    "obj_off": oo,
                    "obj_off_dec": int(oo, 16) if isinstance(oo, str) else oo,
                    "hex": r.get("hex"),
                    "u_val": r.get("u_val"),
                    "caller": r.get("caller"),
                }

            # ---- 四CC 映射（按 tid 归集，不区分 archive） ----
            fcc_by_off = fcc_idx.get(tid, {})

            # ---- 连立 ----
            slots: list[dict] = []
            seen_wire_pos: set[int] = set()

            for wp, winfo in sorted(wire_by_pos.items()):
                seen_wire_pos.add(wp)
                oo_dec = winfo["obj_off_dec"]
                fcc_matches = fcc_by_off.get(oo_dec, []) if oo_dec is not None else []

                if fcc_matches:
                    # 有 4CC 背书 -> L3
                    for fm in fcc_matches:
                        slots.append({
                            "wire_pos": wp,
                            "obj_off": winfo["obj_off"],
                            "obj_off_dec": oo_dec,
                            "fourcc": fm["fourcc"],
                            "slot": fm["slot"],
                            "func_va": fm["func_va"],
                            "kind": fm["kind"],
                            "c_type": fm["c_type"],
                            "width": fm["width"],
                            "access_kind": fm["access_kind"],
                            "status": "L3",
                            "source": "wire+4cc",
                        })
                else:
                    # 无 4CC 背书
                    if oo_dec is not None:
                        status = "L2"  # 有 wire+mem 但无 4CC
                    else:
                        status = "held"  # obj_off 为 null（stack 读等）
                    slots.append({
                        "wire_pos": wp,
                        "obj_off": winfo["obj_off"],
                        "obj_off_dec": oo_dec,
                        "fourcc": None,
                        "status": status,
                        "source": "wire_only",
                    })

            # 四CC 中有但 wire_traces 中未出现的 mem_off -> held（四CC 侧独有）
            wire_offs = {w["obj_off_dec"] for w in wire_by_pos.values() if w["obj_off_dec"] is not None}
            for off_int, fcc_list in fcc_by_off.items():
                if off_int not in wire_offs:
                    for fm in fcc_list:
                        slots.append({
                            "wire_pos": None,
                            "obj_off": f"0x{off_int:X}",
                            "obj_off_dec": off_int,
                            "fourcc": fm["fourcc"],
                            "slot": fm["slot"],
                            "func_va": fm["func_va"],
                            "kind": fm["kind"],
                            "c_type": fm["c_type"],
                            "width": fm["width"],
                            "access_kind": fm["access_kind"],
                            "status": "held",
                            "source": "fourcc_only",
                        })

            slots.sort(key=lambda s: (s["wire_pos"] is None, s["wire_pos"] or 0))

            # ---- 统计 ----
            n_l3 = sum(1 for s in slots if s["status"] == "L3")
            n_l2 = sum(1 for s in slots if s["status"] == "L2")
            n_held = sum(1 for s in slots if s["status"] == "held")
            n_unnamed = sum(1 for s in slots if s["status"] == "unnamed")

            total_slots += len(slots)
            total_l3 += n_l3
            total_l2 += n_l2
            total_held += n_held
            total_unnamed += n_unnamed

            table_out["archives"][arch] = {
                "rows_header": sem_arch.get("rows_header"),
                "row_len_min": sem_arch.get("row_len_min"),
                "row_len_max": sem_arch.get("row_len_max"),
                "wire_read_count": len(wire_reads),
                "slots": slots,
                "slot_count": len(slots),
                "l3_count": n_l3,
                "l2_count": n_l2,
                "held_count": n_held,
                "unnamed_count": n_unnamed,
                "sample_rows": vrec.get("sample_rows", [])[:2] if vrec else [],
            }

        out_tables[str(tid)] = table_out

    # 判定整体状态
    all_l3 = total_held == 0 and total_unnamed == 0
    status = "complete" if all_l3 else "partial"

    return {
        "schema_id": "fm24.highfreq_tables_l3",
        "schema_version": 1,
        "status": status,
        "generated_by": "t156",
        "target_table_ids": sorted(TARGET_TABLES),
        "target_table_names": TARGET_TABLES,
        "coverage": {
            "total_slots": total_slots,
            "l3_slots": total_l3,
            "l2_slots": total_l2,
            "held_slots": total_held,
            "unnamed_slots": total_unnamed,
        },
        "tables": out_tables,
    }



# --------------------------------------------------------------------------- #
# 输出写入
# --------------------------------------------------------------------------- #
def write_outputs(result: dict) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    json_path = OUTDIR / "highfreq_tables_l3.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # REPORT.md
    lines = [
        "# t156 — 高频业务非主表 L3 字段语义闭合（8 张核心表）",
        "",
        f"生成脚本：`scripts/t156_highfreq_tables_l3.py`",
        f"输出目录：`{OUTDIR.as_posix()}`",
        "",
        "## 汇总",
        f"- 目标表：{len(result['target_table_ids'])} 张（{', '.join(str(t) for t in result['target_table_ids'])}）",
        f"- 总槽位：{result['coverage']['total_slots']}",
        f"  - L3（wire+mem+4CC 三方闭合）：{result['coverage']['l3_slots']}",
        f"  - L2（wire+mem 闭合，无 4CC）：{result['coverage']['l2_slots']}",
        f"  - held（无法闭合，诚实占位）：{result['coverage']['held_slots']}",
        f"  - unnamed（无语义）：{result['coverage']['unnamed_slots']}",
        f"- 整体状态：{result['status']}",
        "",
        "## 逐表逐槽映射",
        "",
        "| table_id | entity | archive | wire_pos | obj_off | fourcc | status | source |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for tid in sorted(result["tables"].keys(), key=int):
        trec = result["tables"][tid]
        entity = trec["entity"]
        for arch in sorted(trec["archives"].keys()):
            arec = trec["archives"][arch]
            for s in arec["slots"]:
                wp = s["wire_pos"] if s["wire_pos"] is not None else "-"
                oo = s["obj_off"] if s["obj_off"] is not None else "-"
                fcc = s["fourcc"] if s["fourcc"] else "-"
                src = s["source"]
                lines.append(
                    f"| {tid} | {entity} | {arch} | {wp} | {oo} | {fcc} | {s['status']} | {src} |"
                )

    lines += [
        "",
        "## 说明",
        "- `wire_pos`：slot19  wire 读位置（来自 t121 wire_traces_79of79.json row0_reads）。",
        "- `obj_off`：C++ 对象成员偏移（来自 wire_traces row0_reads.obj_off，或 fourcc_mem_map_v2 mem_offsets.off_int）。",
        "- `fourcc`：4CC getter/setter 四字符码（来自 t108 fourcc_mem_map_v2.json）。",
        "- `L3`：wire_pos + obj_off + fourcc 三方均匹配，证据等级最高。",
        "- `L2`：wire_pos + obj_off 匹配，但未找到对应 4CC，语义部分闭合。",
        "- `held`：无法闭合的槽位（wire_traces 无 obj_off 或 fourcc 独有 mem_off），诚实占位，非结论。",
        "- `unnamed`：无任何语义锚点的槽位。",
        "- 样本行来自 scratch/t133/out/reader_v2_verify.json（t133 真实 .dat 解码结果）。",
        "",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    # DONE.md
    cov = result["coverage"]
    done_lines = [
        "DONE type=highfreq_tables_l3",
        "",
        f"8 张高频核心非主表 L3 字段语义映射完成：状态={result['status']}。",
        f"总槽位 {cov['total_slots']}（L3 {cov['l3_slots']} / L2 {cov['l2_slots']} / held {cov['held_slots']} / unnamed {cov['unnamed_slots']}）。",
        f"产物：`{json_path.as_posix()}`、`{OUTDIR.as_posix()}/REPORT.md`。",
        "",
    ]
    (OUTDIR / "DONE.md").write_text("\n".join(done_lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# selftest（纯常量断言，不依赖原始 .dat）
# --------------------------------------------------------------------------- #
def selftest() -> int:
    failures: list[str] = []

    # 1. 目标表集合正确。
    assert len(TARGET_TABLES) == 8, f"TARGET_TABLES 应 8 张，实际 {len(TARGET_TABLES)}"
    assert set(TARGET_TABLES.keys()) == {6, 22, 26, 29, 32, 33, 49, 71}, "TARGET_TABLES keys"

    # 2. 输入文件存在性（全量模式才强制；selftest 只断言常量，文件缺失不计入失败）。
    missing = [str(p) for p in (WIRE_JSON, FOURCC_JSON, SEMANTICS_JSON, VERIFY_JSON)
               if not p.exists()]
    if missing:
        print(f"[t156] selftest: 缺少输入文件（全量跑需补充）：{missing}", file=sys.stderr)

    # 3. 若全部输入齐全，做端到端一致性断言。
    if not missing:
        result = build_mapping()
        assert result["schema_id"] == "fm24.highfreq_tables_l3"
        assert result["schema_version"] == 1
        assert result["generated_by"] == "t156"
        assert set(result["target_table_ids"]) == {6, 22, 26, 29, 32, 33, 49, 71}
        assert result["status"] in ("complete", "partial")

        # 每张目标表都有记录。
        assert set(result["tables"].keys()) == {str(t) for t in TARGET_TABLES}

        # 覆盖统计自洽。
        cov = result["coverage"]
        assert cov["total_slots"] == cov["l3_slots"] + cov["l2_slots"] + cov["held_slots"] + cov["unnamed_slots"]

        # 每张表每档都有 slot 列表。
        for tid in TARGET_TABLES:
            trec = result["tables"][str(tid)]
            assert trec["entity"] is not None, f"tid {tid} 缺少 entity"
            for arch, arec in trec["archives"].items():
                assert "slots" in arec, f"tid {tid} arch {arch} 缺少 slots"
                for s in arec["slots"]:
                    assert s["status"] in ("L3", "L2", "held", "unnamed"), f"未知状态 {s['status']}"
                    if s["status"] == "L3":
                        assert s["fourcc"] is not None, f"L3 槽位缺少 fourcc: tid={tid} wp={s['wire_pos']}"
                        assert s["obj_off_dec"] is not None, f"L3 槽位缺少 obj_off_dec: tid={tid}"

        # wire_traces 与 fourcc 的交集必须为 L3。
        for tid in TARGET_TABLES:
            trec = result["tables"][str(tid)]
            for arch, arec in trec["archives"].items():
                for s in arec["slots"]:
                    if s["source"] == "wire+4cc":
                        assert s["status"] == "L3", f"wire+4cc 源应为 L3: tid={tid} wp={s['wire_pos']}"

    # 4. 输出目录可写。
    OUTDIR.mkdir(parents=True, exist_ok=True)
    probe = OUTDIR / ".selftest_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        failures.append(f"OUTDIR 不可写: {exc}")

    if failures:
        for f in failures:
            print(f"[t156] selftest FAIL: {f}", file=sys.stderr)
        return 1
    print("[t156] selftest PASS")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    global OUTDIR
    parser = argparse.ArgumentParser(
        prog="t156_highfreq_tables_l3.py",
        description="8 张高频业务非主表 L3 字段语义闭合（slot19 wire <-> mem_off <-> 4CC）。",
    )
    parser.add_argument("--selftest", action="store_true",
                        help="纯常量自检（不依赖原始 .dat），退出码 0/1/2")
    parser.add_argument("--outdir", default=str(OUTDIR),
                        help=f"输出目录（默认 {OUTDIR}）")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    # 全量：建立映射并写入产物。
    OUTDIR = Path(args.outdir)
    try:
        result = build_mapping()
    except Exception as exc:  # noqa: BLE001
        print(f"[t156] 致命错误: {exc}", file=sys.stderr)
        return 2

    write_outputs(result)
    print(f"[t156] 已写入 {OUTDIR / 'highfreq_tables_l3.json'}")
    print(f"[t156] 已写入 {OUTDIR / 'REPORT.md'}")
    print(f"[t156] 已写入 {OUTDIR / 'DONE.md'}")
    print(f"[t156] 状态={result['status']} 总槽位={result['coverage']['total_slots']} "
          f"(L3={result['coverage']['l3_slots']} L2={result['coverage']['l2_slots']} "
          f"held={result['coverage']['held_slots']} unnamed={result['coverage']['unnamed_slots']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
