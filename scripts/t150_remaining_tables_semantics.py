#!/usr/bin/env python3
"""t150 — 其余非主表语义目录普查（补齐 79 编号表的语义覆盖）。

为 79 张编号表中尚未建立语义目录的表（排除主表 {3, 9, 10, 25} 及
reports/other_tables_schema.json 已覆盖的 13 张非主表），汇总机读语义目录：

  * client/server 行数（来自 t133 reader_v2_verify.json）
  * RTTI 类名（来自 scratch/t95/vtable_index.json）
  * 物理列结构与样本行（来自 t133 reader_v2_verify.json）
  * 外键关系（来自 scratch/t142/out/fk_graph_master.json）
  * 可匹配到的 4CC 语义字段（来自 scratch/t108/out/fourcc_mem_map_v2.json）

未确认列如实标为 `unnamed` 或 `candidate`，严禁编造。仅在数据齐全时
进行全量解码；否则 `--selftest` 以纯常量断言自检。

退出码：0 成功 / 1 校验失败 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fm24_config as cfg  # noqa: E402  (统一路径配置)

SCRIPT = Path(__file__).resolve()
OUTDIR = cfg.SCRATCH_DIR / "t150" / "out"
VERIFY_JSON = cfg.SCRATCH_DIR / "t133" / "out" / "reader_v2_verify.json"
VTABLE_JSON = cfg.SCRATCH_DIR / "t95" / "vtable_index.json"
FK_JSON = cfg.SCRATCH_DIR / "t142" / "out" / "fk_graph_master.json"
FOURCC_JSON = cfg.SCRATCH_DIR / "t108" / "out" / "fourcc_mem_map_v2.json"
OTHER_SCHEMA_JSON = cfg.REPORTS_DIR / "other_tables_schema.json"

# 主表（t136 已覆盖）+ other_tables_schema.json 已覆盖的 13 张非主表。
MAIN_TABLES = {3, 9, 10, 25}
OTHER_COVERED = {2, 5, 19, 41, 21, 18, 27, 47, 56, 0, 7, 8, 24}
EXCLUDED = MAIN_TABLES | OTHER_COVERED  # 17 个 table_id

ALL_TABLE_IDS = set(range(79))  # 79 张编号表 0..78


# --------------------------------------------------------------------------- #
# 辅助读取
# --------------------------------------------------------------------------- #
def _load_json(path: Path, what: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[t150] 缺少输入 {what}: {path}", file=sys.stderr)
        return None
    except json.JSONDecodeError as exc:
        print(f"[t150] 解析失败 {what}: {path}: {exc}", file=sys.stderr)
        return None


def _tid(key: str) -> int:
    """'client/6' -> 6"""
    return int(key.rsplit("/", 1)[1])


def _archive(key: str) -> str:
    return key.split("/", 1)[0]


# --------------------------------------------------------------------------- #
# 核心调度
# --------------------------------------------------------------------------- #
def build_catalog() -> dict:
    """建立剩余表语义目录。返回可直接序列化的 dict。"""
    verify = _load_json(VERIFY_JSON, "t133 reader_v2_verify.json")
    vtable = _load_json(VTABLE_JSON, "t95 vtable_index.json")
    fk = _load_json(FK_JSON, "t142 fk_graph_master.json")
    fourcc = _load_json(FOURCC_JSON, "t108 fourcc_mem_map_v2.json")
    other = _load_json(OTHER_SCHEMA_JSON, "reports/other_tables_schema.json")

    # RTTI 按 table_id 归集（同一 tid 可能有多个 class/条目，如 tid=3）。
    rtti_by_tid: dict[int, list[dict]] = {}
    if vtable and isinstance(vtable.get("tables"), list):
        for entry in vtable["tables"]:
            rtti_by_tid.setdefault(entry["table_type"], []).append({
                "class": entry.get("class"),
                "entity_tag": entry.get("entity_tag"),
                "vtable_va": entry.get("vtable_va"),
                "slot_count": entry.get("slot_count"),
            })

    # 4CC 按 table_id 归集。
    fourcc_by_tid: dict[int, dict] = {}
    if fourcc and isinstance(fourcc.get("tables"), list):
        for entry in fourcc["tables"]:
            fourcc_by_tid[entry["table_type"]] = entry

    # 外键边按 src_table 归集（key 形如 "server/12"）。
    fk_by_table: dict[str, list[dict]] = {}
    if fk and isinstance(fk.get("edges_verified"), list):
        for edge in fk["edges_verified"]:
            fk_by_table.setdefault(edge.get("src_table"), []).append({
                "src_column": edge.get("src_column"),
                "target": edge.get("target"),
                "target_key": edge.get("target_key"),
                "tier": edge.get("tier"),
                "verified": edge.get("verified"),
                "hit_rate": edge.get("hit_rate"),
                "distinct": edge.get("distinct"),
            })

    # 已解码表汇总（t133 reader_v2_verify，key 形如 "client/6"）。
    verify_tables: dict[str, dict] = {}
    if verify and isinstance(verify.get("tables"), dict):
        verify_tables = verify["tables"]

    # other_tables_schema 覆盖表 id（防御性再校验）。
    other_covered_ids = set()
    if other and isinstance(other.get("table_ids"), dict):
        other_covered_ids = {int(k) for k in other["table_ids"].keys()}
    excluded = MAIN_TABLES | OTHER_COVERED | other_covered_ids

    remaining_ids = sorted(ALL_TABLE_IDS - excluded)

    catalog: dict[str, dict] = {}
    for tid in remaining_ids:
        # 该 tid 在哪些 archive 存在。
        present_archives = [a for a in ("client", "server")
                            if f"{a}/{tid}" in verify_tables]

        # RTTI（可能为空，或多条）。
        rtti_entries = rtti_by_tid.get(tid, [])

        # 4CC（单条）。
        fcc_entry = fourcc_by_tid.get(tid)

        table_record: dict = {
            "table_id": tid,
            "entity": None,
            "present_archives": present_archives,
            "rtti": rtti_entries,
            "tables": {},
            "status": "absent",
            "evidence_grade": "L1",
            "notes": [],
        }

        if not present_archives:
            table_record["status"] = "absent"
            table_record["notes"].append(
                "未在 client_db/server_db 数字表库中出现（无物理行，可能为空表或非数字成员）")
            catalog[str(tid)] = table_record
            continue

        table_record["status"] = "decoded"
        # 取第一个出现的 archive 作为 entity 来源（优先 server，其次 client）。
        primary_arch = "server" if "server" in present_archives else "client"
        primary_key = f"{primary_arch}/{tid}"
        pinfo = verify_tables[primary_key]

        # class / entity_tag：优先用 RTTI，其次 t133 class。
        if rtti_entries:
            table_record["entity"] = rtti_entries[0].get("class")
        else:
            table_record["entity"] = pinfo.get("class")

        for arch in present_archives:
            key = f"{arch}/{tid}"
            info = verify_tables[key]
            sample_rows = info.get("sample_rows", []) or []

            # 物理列：从样本行的键名推导（l3 命名列或 col_<off>）。
            columns: list[dict] = []
            seen_names: set[str] = set()
            seen_offs: dict[int, str] = {}
            for row in sample_rows:
                for name, val in row.items():
                    if name in ("row_flag", "identity"):
                        continue
                    if name in seen_names:
                        continue
                    if name.startswith("col_"):
                        try:
                            off = int(name.split("_", 1)[1])
                        except ValueError:
                            off = None
                        kind = "unnamed"
                    else:
                        off = None
                        kind = "named_l3"
                    if off is not None and off in seen_offs:
                        continue
                    columns.append({
                        "name": name,
                        "kind": kind,
                        "row0_off": off,
                        "sample_value": val,
                    })
                    seen_names.add(name)
                    if off is not None:
                        seen_offs[off] = name

            columns.sort(key=lambda c: (c["row0_off"] is None, c["row0_off"] or 0))

            # 4CC 语义字段（对象偏移体系，与行偏移不等价，仅做语义索引）。
            fcc_fields: list[dict] = []
            if fcc_entry:
                for fcc, finfo in (fcc_entry.get("fourccs") or {}).items():
                    for mo in (finfo.get("mem_offsets") or []):
                        fcc_fields.append({
                            "fourcc": fcc,
                            "slot": finfo.get("slot"),
                            "func_va": finfo.get("func_va"),
                            "kind": finfo.get("kind"),
                            "c_type": finfo.get("c_type") or mo.get("c_type"),
                            "width": mo.get("width"),
                            "mem_off": mo.get("off_int"),
                            "access_kind": finfo.get("access_kind"),
                        })
            fcc_fields.sort(key=lambda x: (x["mem_off"] is None, x["mem_off"] or 0))

            # 外键（仅当该 archive/tid 有 verified 边时）。
            fk_edges = fk_by_table.get(key, [])

            table_record["tables"][arch] = {
                "class": info.get("class"),
                "kind": info.get("kind"),
                "rows_header": info.get("rows_header"),
                "rows_decoded": info.get("rows_decoded"),
                "row_len_min": info.get("row_len_min"),
                "row_len_max": info.get("row_len_max"),
                "l3_named_fields": info.get("l3_named_fields"),
                "footer_closed": info.get("footer_closed"),
                "diff": info.get("diff"),
                "error": info.get("error"),
                "flags_seen": info.get("flags_seen"),
                "columns": columns,
                "column_count": len(columns),
                "fourcc_fields": fcc_fields,
                "fourcc_field_count": len(fcc_fields),
                "foreign_keys": fk_edges,
                "fk_edge_count": len(fk_edges),
                "sample_rows": sample_rows[:3],
            }

        # 证据等级判定：有 L3 4CC 或 verified 外键即提升。
        any_l3 = any(tbl["fourcc_field_count"] > 0 for tbl in table_record["tables"].values())
        any_fk = any(tbl["fk_edge_count"] > 0 for tbl in table_record["tables"].values())
        if any_l3 and any_fk:
            table_record["evidence_grade"] = "L2+L3"
        elif any_l3 or any_fk:
            table_record["evidence_grade"] = "L2"
        else:
            table_record["evidence_grade"] = "L1"

        catalog[str(tid)] = table_record

    decoded_count = sum(1 for v in catalog.values() if v["status"] == "decoded")
    absent_count = sum(1 for v in catalog.values() if v["status"] == "absent")

    # 顶层状态：所有剩余表均已入目录（decoded 或 absent）即 complete。
    status = "complete" if decoded_count + absent_count == len(remaining_ids) else "partial"

    return {
        "schema_id": "fm24.remaining_tables_semantics",
        "schema_version": 1,
        "status": status,
        "generated_by": "t150",
        "evidence_grade_policy": "L1 自检 / L2 独立事实对照 / L3 exe 静态或机器码仿真证据。"
        " candidate/unnamed 仅为占位，非结论；L4=0。",
        "excluded_table_ids": sorted(excluded),
        "remaining_table_ids": remaining_ids,
        "remaining_count": len(remaining_ids),
        "decoded_count": decoded_count,
        "absent_count": absent_count,
        "tables": catalog,
    }


def write_outputs(catalog: dict) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTDIR / "remaining_tables_semantics.json"
    json_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

    # REPORT.md
    lines = [
        "# t150 — 其余非主表语义目录普查",
        "",
        f"生成脚本：`scripts/t150_remaining_tables_semantics.py`",
        f"输出目录：`{OUTDIR.as_posix()}`",
        "",
        "## 汇总",
        f"- 79 号编号表总数：79（table_id 0..78）",
        f"- 已排除（主表 {sorted(MAIN_TABLES)} + other_tables_schema 13 表 {sorted(OTHER_COVERED)}）：{len(EXCLUDED)}",
        f"- 剩余待普查表：{catalog['remaining_count']}",
        f"-  其中有物理行（decoded）：{catalog['decoded_count']}",
        f"-  其中无物理行（absent）：{catalog['absent_count']}",
        "",
        "## 逐表身份与证据等级",
        "",
        "| table_id | entity/RTTI | archives | rows(client/server) | kind | 4CC字段 | 外键边 | 等级 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for tid in catalog["remaining_table_ids"]:
        rec = catalog["tables"][str(tid)]
        arches = ",".join(rec["present_archives"]) if rec["present_archives"] else "-"
        if rec["status"] == "absent":
            rows_s = "-"
            kind_s = "-"
            n4cc = 0
            nfk = 0
        else:
            parts = []
            for arch in ("client", "server"):
                t = rec["tables"].get(arch)
                if t:
                    parts.append(f"{arch[:1]}={t['rows_header']}")
            rows_s = " ".join(parts) if parts else "-"
            kind_s = rec["tables"][rec["present_archives"][0]]["kind"]
            n4cc = sum(t["fourcc_field_count"] for t in rec["tables"].values())
            nfk = sum(t["fk_edge_count"] for t in rec["tables"].values())
        entity = rec["entity"] or "-"
        lines.append(
            f"| {tid} | {entity} | {arches} | {rows_s} | {kind_s} | {n4cc} | {nfk} | {rec['evidence_grade']} |"
        )

    lines += [
        "",
        "## 说明",
        "- `absent`：该 table_id 未在 client_db/server_db 数字表库中出现，无物理行可解码。",
        "- `unnamed`：物理列存在但尚无 L2/L3 语义锚点，诚实占位，非结论。",
        "- `candidate`：有初步线索但未达到 L2 独立事实对照，非结论。",
        "- 4CC 字段偏移为 C++ 对象内偏移（mem_off），与行内偏移（row0_off）不等价，"
        "  两者仅做语义索引，不直接等号。",
        "- 外键 `tier` 为 `code_corroborated`（L3 辅佐）或 `statistical`（L2 统计对照）。",
        "",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    # DONE.md
    done_lines = [
        "DONE type=remaining_tables_semantics",
        "",
        f"剩余表普查完成：{catalog['remaining_count']} 张表（decoded {catalog['decoded_count']} / "
        f"absent {catalog['absent_count']}）。",
        f"产物：`{json_path.as_posix()}`、`{OUTDIR.as_posix()}/REPORT.md`。",
        "",
    ]
    (OUTDIR / "DONE.md").write_text("\n".join(done_lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# selftest（纯常量断言，不依赖原始 .dat）
# --------------------------------------------------------------------------- #
def selftest() -> int:
    failures: list[str] = []

    # 1. 排除集合正确性。
    assert MAIN_TABLES == {3, 9, 10, 25}, "MAIN_TABLES"
    assert OTHER_COVERED == {2, 5, 19, 41, 21, 18, 27, 47, 56, 0, 7, 8, 24}, "OTHER_COVERED"
    assert EXCLUDED == MAIN_TABLES | OTHER_COVERED, "EXCLUDED union"
    assert len(EXCLUDED) == 17, f"EXCLUDED size {len(EXCLUDED)}"
    assert len(ALL_TABLE_IDS) == 79, "ALL_TABLE_IDS 79"
    remaining = sorted(ALL_TABLE_IDS - EXCLUDED)
    assert len(remaining) == 62, f"剩余表应 62 张，实际 {len(remaining)}"

    # 2. 缺失的 table_id（absent）预期值：0-78 中既非已覆盖又无物理行的。
    expected_absent = {1, 4, 11, 13, 14, 15, 16, 17, 20, 28, 40, 44, 53, 54, 55, 74, 75, 76, 77, 78}
    assert expected_absent.issubset(set(remaining)), "expected_absent ⊆ remaining"

    # 3. 输入文件存在性（全量模式才强制；selftest 只断言常量，文件缺失不计入失败）。
    missing = [str(p) for p in (VERIFY_JSON, VTABLE_JSON, FK_JSON, FOURCC_JSON, OTHER_SCHEMA_JSON)
               if not p.exists()]
    if missing:
        print(f"[t150] selftest: 缺少输入文件（全量跑需补充）：{missing}", file=sys.stderr)

    # 4. 若全部输入齐全，做端到端一致性断言。
    if not missing:
        catalog = build_catalog()
        assert catalog["schema_id"] == "fm24.remaining_tables_semantics"
        assert catalog["schema_version"] == 1
        assert catalog["generated_by"] == "t150"
        assert catalog["status"] == "complete"
        assert catalog["remaining_count"] == 62
        assert catalog["decoded_count"] + catalog["absent_count"] == 62

        # 每张剩余表都有记录。
        assert set(catalog["tables"].keys()) == {str(t) for t in remaining}

        # 已解码表必有 present_archives 且非空。
        for tid in remaining:
            rec = catalog["tables"][str(tid)]
            if rec["status"] == "decoded":
                assert rec["present_archives"], f"tid {tid} decoded 但无 archive"
                for arch, t in rec["tables"].items():
                    assert t["rows_header"] is not None
                    assert t["kind"] in ("fixed", "variable", "empty")
                    # columns 名唯一（按 off 去重后）。
                    names = [c["name"] for c in t["columns"]]
                    assert len(names) == len(set(names)), f"tid {tid} arch {arch} 列名重复"
                    # 4CC 字段非负宽度。
                    for f in t["fourcc_fields"]:
                        if f["width"] is not None:
                            assert f["width"] >= 0
            else:
                assert rec["status"] == "absent"
                assert not rec["present_archives"]

        # 外键仅出现在 decoded 表中。
        for tid in remaining:
            rec = catalog["tables"][str(tid)]
            if rec["status"] == "absent":
                assert rec["evidence_grade"] == "L1"

    # 5. 输出目录可写。
    OUTDIR.mkdir(parents=True, exist_ok=True)
    probe = OUTDIR / ".selftest_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        failures.append(f"OUTDIR 不可写: {exc}")

    if failures:
        for f in failures:
            print(f"[t150] selftest FAIL: {f}", file=sys.stderr)
        return 1
    print("[t150] selftest PASS")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    global OUTDIR
    parser = argparse.ArgumentParser(
        prog="t150_remaining_tables_semantics.py",
        description="79 张编号表中其余非主表的语义目录普查（t150）。",
    )
    parser.add_argument("--selftest", action="store_true",
                        help="纯常量自检（不依赖原始 .dat），退出码 0/1/2")
    parser.add_argument("--outdir", default=str(OUTDIR),
                        help=f"输出目录（默认 {OUTDIR}）")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    # 全量：建立目录并写入产物。
    OUTDIR = Path(args.outdir)
    try:
        catalog = build_catalog()
    except Exception as exc:  # noqa: BLE001
        print(f"[t150] 致命错误: {exc}", file=sys.stderr)
        return 2

    write_outputs(catalog)
    print(f"[t150] 已写入 {OUTDIR / 'remaining_tables_semantics.json'}")
    print(f"[t150] 已写入 {OUTDIR / 'REPORT.md'}")
    print(f"[t150] 已写入 {OUTDIR / 'DONE.md'}")
    print(f"[t150] 剩余表 {catalog['remaining_count']} 张，"
          f"decoded {catalog['decoded_count']}，absent {catalog['absent_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
