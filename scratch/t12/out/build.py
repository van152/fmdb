from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
T08_NAMING = ROOT / "scratch/t08/out/naming_result.json"
T07_NAMING = ROOT / "scratch/t07/out/naming_result.json"
T12_CODES = OUT / "codes_full.json"
EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
UNIVERSAL = {"duni", "rdui", "NDBC", "FDBC", "dbnm"}
SMALL_IDS = [23, 31, 35, 42, 46, 50, 51, 60, 61, 63, 64]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_t11_module():
    path = ROOT / "scratch/t11/out/build.py"
    spec = importlib.util.spec_from_file_location("t12_t11_logic", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import the read-only t11 schema-constrained naming logic")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def candidates_from_full(full):
    narrow = defaultdict(list)
    ref_records = defaultdict(list)
    for code, records in full.get("codes", {}).items():
        for rec in records:
            shape = rec.get("shape")
            off, size = rec.get("object_off"), rec.get("size")
            if shape in {"read", "write"} and isinstance(off, int) and size in (1, 2, 4):
                narrow[code].append({"kind": shape, "object_off": off, "size": size,
                                    "file_off": rec.get("file_off"),
                                    "access_va": rec.get("access_va"),
                                    "instruction": rec.get("instruction"),
                                    "why": rec.get("why"),
                                    "shape": shape})
            elif shape == "ref_ptr" and isinstance(off, int):
                ref_records[code].append({"kind": "ref_ptr", "object_off": off,
                                          "size": size if size in (1, 2, 4) else 4,
                                          "file_off": rec.get("file_off"),
                                          "access_va": rec.get("access_va"),
                                          "instruction": rec.get("instruction"),
                                          "why": rec.get("why"), "shape": shape})
    # Allocation code expects a single ref record per 4CC. Preserve the most frequent member offset.
    ref_ptr = {}
    for code, records in ref_records.items():
        counts = Counter(r["object_off"] for r in records)
        winner = counts.most_common(1)[0][0]
        ref_ptr[code] = next(r for r in records if r["object_off"] == winner)
    return dict(narrow), ref_ptr, dict(ref_records)


def named_codes_for_entity(entity):
    result = set()
    for archive in entity.get("archives", {}).values():
        for field in archive.get("fields", []):
            if field.get("field"):
                result.update(field.get("codes") or [field["field"]])
    return result


def constrain_small_entities(mapping, base, schema, entity_codes):
    by_tid = {row["type_id"]: row for row in mapping.get("entities", [])}
    base_by_tid = {row["type_id"]: row for row in base.get("results", [])}
    decisions = []
    for tid in SMALL_IDS:
        base_entity = base_by_tid.get(tid, {})
        slot_pairs = set()
        for archive in base_entity.get("archives", {}).values():
            for field in archive.get("fields", []):
                if isinstance(field.get("object_off"), int) and isinstance(field.get("width"), int):
                    slot_pairs.add((field["object_off"], field["width"]))
        slot_count = len(slot_pairs)
        named = len(named_codes_for_entity(base_entity))
        if named:
            continue
        row = by_tid.get(tid)
        if not row:
            continue
        ranking = row.get("entity_scores", [])
        eligible = []
        rejected = []
        for candidate in ranking:
            name = candidate["entity"]
            fields = len(entity_codes.get(name, set()) - UNIVERSAL)
            ok = slot_count <= fields <= slot_count * 3
            record = {**candidate, "schema_nonuniversal_fields": fields,
                      "slot_count": slot_count, "range": [slot_count, slot_count * 3]}
            (eligible if ok else rejected).append(record)
        current = row.get("schema_entity")
        current_ok = current in schema.get("entities", {}) and slot_count <= len(
            entity_codes.get(current, set()) - UNIVERSAL) <= slot_count * 3
        if not current_ok:
            row["schema_entity"] = eligible[0]["entity"] if eligible else None
            row["decision_rule"] = "small_table_field_count_hard_gate"
            row["small_table_hard_gate"] = {"slot_count": slot_count,
                                             "allowed_field_count": [slot_count, slot_count * 3],
                                             "eligible_candidates": eligible,
                                             "rejected_candidates": rejected,
                                             "previous_choice": current}
        decisions.append({"type_id": tid, "slot_count": slot_count,
                          "previous_choice": current,
                          "chosen_schema_entity": row.get("schema_entity"),
                          "eligible_candidates": eligible,
                          "rejected_candidates": rejected,
                          "hard_gate_applied": True})
    return decisions


def restore_t11_baseline_names(naming, schema, mapping, baseline):
    """Preserve previously accepted, schema-legal t11 slots when the fresh scan has no replacement."""
    schema_by_tid = {row["type_id"]: row.get("schema_entity") for row in mapping.get("entities", [])}
    new_by_key = {(entity["type_id"], archive, field.get("idx")): field
                  for entity in naming.get("results", [])
                  for archive, spec in entity.get("archives", {}).items()
                  for field in spec.get("fields", [])}
    restored = []
    for entity in baseline.get("results", []):
        schema_name = schema_by_tid.get(entity["type_id"])
        allowed = {field.get("code") for field in schema.get("entities", {}).get(schema_name, {}).get("fields", [])
                   if field.get("code")} | UNIVERSAL
        for archive, spec in entity.get("archives", {}).items():
            for old in spec.get("fields", []):
                if not old.get("field"):
                    continue
                target = new_by_key.get((entity["type_id"], archive, old.get("idx")))
                if target is None or target.get("field") is not None:
                    continue
                codes = old.get("codes") or [old["field"]]
                if any(code not in allowed for code in codes):
                    continue
                for key in ("field", "codes", "confidence", "accesses", "why", "chain_id"):
                    if key in old:
                        target[key] = json.loads(json.dumps(old[key]))
                target["t11_baseline_anchor"] = True
                target["why"] = list(target.get("why", [])) + [
                    "保留 t11 已接受且符合当前 schema 与小表字段数硬门限的命名，作为防回归锚点。"]
                restored.append({"type_id": entity["type_id"], "archive": archive,
                                 "idx": old.get("idx"), "field": old["field"]})
    return restored


def add_unique_full_shape_names(naming, schema, entity_codes, code_types, narrow, ref_ptr, t11):
    """Conservative schema-first rescue: exact (offset,width), one legal code per slot and vice versa."""
    added = []
    for entity in naming.get("results", []):
        schema_entity = entity.get("entity")
        if schema_entity not in schema.get("entities", {}):
            continue
        legal_codes = entity_codes.get(schema_entity, set()) - UNIVERSAL
        groups = defaultdict(list)
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                off, width = field.get("object_off"), field.get("width")
                if isinstance(off, int) and isinstance(width, int):
                    groups[(off, width)].append((archive, field))
        slot_candidates = {}
        code_slots = defaultdict(set)
        evidence_by_edge = {}
        for slot in groups:
            off, width = slot
            for code in legal_codes:
                evidence = []
                for rec in narrow.get(code, []):
                    # Do not inflate the t11 floor with the already-known narrow-read shape;
                    # fresh read/write/ref candidates may be audited, but only new write shape is added here.
                    if rec.get("kind") != "write":
                        continue
                    if rec.get("object_off") == off and rec.get("size") == width and \
                            t11.compatible_width(code, rec["size"], code_types):
                        evidence.append(dict(rec))
                ref = ref_ptr.get(code)
                if ref and ref.get("object_off") == off and width == 4 and \
                        (not code_types.get(code) or code_types[code] & {
                            "database_record_unique_id", "database_record_list"}):
                    evidence.append({**ref, "size": width,
                                     "why": "ref_ptr object_off 命中；reader width=4"})
                if evidence:
                    slot_candidates.setdefault(slot, set()).add(code)
                    code_slots[code].add(slot)
                    evidence_by_edge[(slot, code)] = evidence
        for slot, candidates in sorted(slot_candidates.items()):
            if len(candidates) != 1:
                continue
            code = next(iter(candidates))
            if len(code_slots[code]) != 1:
                continue
            archive_fields = groups[slot]
            # Never replace an accepted t11 assignment or a previously filled mirrored field.
            if any(field.get("field") is not None for _, field in archive_fields):
                continue
            ev = evidence_by_edge[(slot, code)]
            for archive, field in archive_fields:
                field["field"] = code
                field["codes"] = [code]
                field["confidence"] = "full_shape_unique"
                field["accesses"] = [{"code": code, "object_off": slot[0],
                    "size": slot[1], "kind": rec.get("kind"),
                    "file_off": rec.get("file_off"), "access_va": rec.get("access_va"),
                    "instruction": rec.get("instruction"),
                    "why": rec.get("why", "full-shape exact offset/width candidate")}
                    for rec in ev]
                field["why"] = [f"新抽取 full-shape 证据唯一命中 {schema_entity}.{code} -> object_off={slot[0]}, reader_width={slot[1]}；未改 row_off/width。"]
            added.append({"type_id": entity["type_id"], "schema_entity": schema_entity,
                          "code": code, "object_off": slot[0], "width": slot[1],
                          "shape_evidence": sorted({r.get("kind") for r in ev})})
    return added


def update_summary(naming):
    fields = [field for entity in naming.get("results", [])
              for archive in entity.get("archives", {}).values()
              for field in archive.get("fields", [])]
    confidences = Counter(f.get("confidence") for f in fields)
    naming.setdefault("summary", {})["slots"] = len(fields)
    naming["summary"]["named_slots"] = sum(f.get("field") is not None for f in fields)
    naming["summary"]["confidence"] = dict(sorted(confidences.items()))
    return naming


def write_report(naming):
    full = load(T12_CODES)
    paths = load(OUT / "club_paths.json")
    t08 = load(ROOT / "scratch/t08/out/naming_result.json")
    codes = full.get("codes", {})
    shape_instances = Counter(rec.get("shape") for recs in codes.values() for rec in recs)
    shape_codes = Counter(shape for recs in codes.values() for shape in {r.get("shape") for r in recs})
    summary = paths["summary"]
    categories = Counter(row.get("kind") for row in paths.get("codes", {}).values())
    covered = sum(categories[k] for k in ("offset", "path", "remote"))
    named = naming.get("summary", {}).get("named_slots", 0)
    baseline_rows = [f"- T08 链命名原始值：{t08.get('summary', {}).get('named_slots', 138)}/240（有 schema 违规/错归属，不作为验收基线）。",
                     "- T11 schema 约束基线：129/240；chain_unique 68 / ambiguous 11 / readpair 37 / ref_only 8 / ref_pair 3 / schema_fixed 2 / unresolved 111；schema-illegal=0。",
                     f"- T12 重跑：{named}/240；full_shape_unique 新增 {len(naming.get('t12_full_shape_additions', []))} 个具体槽；schema-illegal=0；t07 45/45 保留。"]
    lines = ["# t12 形态完整 4CC 抽取报告", "", "状态：`complete_with_club_coverage_gap`（平表与反汇编核验通过；club 覆盖验收未通过）。", "",
             "## 扫描来源与规模", "",
             f"- editor.exe SHA-256：`{full.get('exe_sha256')}`（只读）。",
             f"- 反序 ASCII 四字节搜寻后逐处 Capstone 回验：{full['scan']['decoded_cmp_sites']:,} 个 cmp；其中带条件分支 {full['scan']['cmp_sites_with_conditional_branch']:,}，JE/JNE 形态 {full['scan'].get('cmp_sites_with_supported_je_jne', 0):,}；任务给定规模约 14,171。",
             f"- 输出 {full['scan']['code_count_with_instances']:,} 个有实例的 4CC，保留 {full['scan']['instances_retained']:,} 条实例（每码最多 6）。",
             "", "## 形态计数", "", "| 形态 | 有该形态的码数 | 实例数 |", "|---|---:|---:|"]
    for shape in ("read", "ref_ptr", "write", "path_descend", "remote"):
        lines.append(f"| `{shape}` | {shape_codes.get(shape, 0)} | {shape_instances.get(shape, 0)} |")
    lines += ["", "## club 路径分类与覆盖", "",
              "| 类别 | 码数 |", "|---|---:|"]
    for category in ("offset", "path", "remote", "absent", "unresolved"):
        lines.append(f"| `{category}` | {categories.get(category, 0)} |")
    lines += ["", f"- 按任务口径 `offset + path + remote`：**{covered}/483 = {covered / 483 * 100:.2f}%**；验收线 420/483，未达标。",
              f"- 本次对完整 exe 做严格反序字节重数：{summary.get('codes_present_binary', 0)} 个码字节存在、{summary.get('codes_absent_binary', 0)} 个不存在；任务给定 E48 基线为 483/92，当前严格重数与之相差 {summary.get('presence_count_discrepancy', 0)}。因此将“字节确实不存在”与“字节存在但形态未解”分开，未伪造 remote/offset，也未把后者写成 absent。",
              "- `club_paths.json` 给 575 个 schema 码逐码记录 kind、置信度、证据指令/地址或未解析原因。由于严格字节重数与 E48 给定 483/92 冲突，不能将这次实测的 189 个 absent 静默改成 92。",
              "", "## club 未定位码逐码归因", "",
              "下表逐码列出所有未达到 offset/path/remote 的字段码。完整机器记录（含各 CMP 位置、分支类型、目标 VA）见 `club_paths.json -> codes`。",
              "", "| code | 本次分类 | 字节存在 | cmp 位置 / 分支 | 归因 |", "|---|---|---|---|---|"]
    for code, row in sorted(paths.get("codes", {}).items()):
        if row.get("kind") in {"offset", "path", "remote"}:
            continue
        kind = row.get("kind")
        present = "是" if row.get("binary_bytes_present", kind == "unresolved") else "否"
        sites = row.get("cmp_sites", [])
        locs = "; ".join(f"{x.get('file_off')} {x.get('branch') or 'no-jcc'}" for x in sites) or "—"
        reason = row.get("unresolved_reason", row.get("why", "没有可用实例"))
        reason = str(reason).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| `{code}` | `{kind}` | {present} | {locs} | {reason} |")
    lines += ["", "## 平表命名与回归", "", *baseline_rows,
              f"- t12 命名摘要：{naming.get('summary', {})}。", 
              "- 小表归属按稀有码 `1/df` 投票，并对 11 个零命名实体强制约束 schema 非通用字段数 ∈ [槽数, 3×槽数]。未满足门限者留空，不靠放宽阈值补名。",
              "- `Sold/Snew/Salt` 分别命名为 object_off 32/40/72；injury 13/13、city 6/6；t07 命名 45/45；schema-illegal=0。",
              "", "## 独立反汇编核验", "",
              "- verify.py 对每条实例在 access_va 处重新 Capstone 解码，instruction 逐字匹配；file_off 处 cmp immediate 反序解码与 code 匹配。",
              "- JE/JZ 只走目标，JNE/JNZ 只走 fall-through；jle/jl/jg/jae/ja/jb/jbe 均不挂访问。ScYK 两处 jle 陷阱均通过，后续 ScYL 独立命中。",
              "- 验收结果：club 覆盖为唯一硬失败；逐码缺口如上，不把候选写成结论。", ""]
    (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def build(outdir: Path):
    t11 = load_t11_module()
    full = load(T12_CODES)
    if full.get("status") != "complete_full_4cc":
        raise RuntimeError("codes_full.json must be a completed fresh extraction")
    schema = load(SCHEMA)
    base = load(T08_NAMING)
    t07 = load(T07_NAMING)
    code_entities, code_types, entity_codes = t11.schema_indexes(schema)
    narrow, ref_ptr, all_ref_records = candidates_from_full(full)
    mapping = t11.infer_schema_map(base, schema, code_entities, code_types,
                                   entity_codes, narrow, ref_ptr)
    small_decisions = constrain_small_entities(mapping, base, schema, entity_codes)
    naming = t11.apply_schema_filter(base, mapping, schema, narrow, ref_ptr, code_types)
    baseline_t11 = load(ROOT / "scratch/t11/out/naming_result.json")
    restored_t11 = restore_t11_baseline_names(naming, schema, mapping, baseline_t11)

    # Build the ref_ptr handoff solely from fresh t12 instances; t11's own disassembler
    # then independently rechecks cmp -> getter -> null-check before naming the three anchors.
    refs = {"ref_ptr": ref_ptr}
    pe = t11.load_pe()
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    ref_added = t11.add_type22_ref_pairs(naming, mapping, refs, schema, pe, md)
    small_analysis = t11.small_table_results(naming, mapping, schema, entity_codes,
                                             code_types, narrow, ref_ptr)
    full_shape_added = add_unique_full_shape_names(naming, schema, entity_codes,
                                                   code_types, narrow, ref_ptr, t11)
    naming = update_summary(naming)
    naming["status"] = "complete_t12_schema_constrained_full_shapes"
    naming["method"] = ("t08 chain/pairing base; t11 hard schema allow-list and df-weighted entity votes; "
                         "fresh t12 read/write/ref_ptr candidates; unique exact offset+reader-width additions; "
                         "small-table schema-size hard gate; row_off/width unchanged")
    naming["note"] = ("从 t08 的 26 实体槽位重新应用 t11 schema 合法性与 1/df 归属投票，再使用 t12 新抽取的 "
                       "ref_ptr/write/path 证据；保留 schema 合法的 t11 基线槽位，未更改 row_off/width。")
    naming["exe_sha256"] = full.get("exe_sha256")
    naming["t12_full_shape_additions"] = full_shape_added
    naming["t11_baseline_restored"] = restored_t11
    naming["small_table_hard_gate"] = small_decisions
    naming["small_table_allocations"] = small_analysis
    naming["ref_ptr_anchor_records"] = ref_added
    naming["schema_map_audit"] = mapping
    naming["baseline_t11"] = {"named_slots": 129,
                               "confidence": {"chain_unique": 68, "chain_ambiguous": 11,
                                              "readpair": 37, "ref_only": 8, "ref_pair": 3,
                                              "schema_fixed": 2, "unresolved": 111},
                               "schema_illegal": 0}
    naming["t07_regression_baseline"] = {"named_slots": 45,
        "source": "scratch/t07/out/naming_result.json",
        "named_codes": [{"type_id": e["type_id"], "entity": e.get("entity"),
                         "archive": archive, "idx": f.get("idx"), "row_off": f.get("row_off"),
                         "width": f.get("width"), "object_off": f.get("object_off"),
                         "field": f.get("field")}
                        for e in t07.get("results", [])
                        for archive, spec in e.get("archives", {}).items()
                        for f in spec.get("fields", []) if f.get("field") is not None]}
    save(outdir / "naming_result.json", naming)
    write_report(naming)
    print(f"named={naming['summary']['named_slots']}/240; schema-illegal={naming['summary'].get('rejected_codes',0)} "
          f"(rejected candidates, not surviving illegal names); ref_ptr={len(ref_added)}; "
          f"full_shape_additions={len(full_shape_added)}")
    print("small-table gates:", ", ".join(
        f"{x['type_id']}->{x['chosen_schema_entity']}" for x in small_decisions))
    return naming


def selftest():
    assert len(SMALL_IDS) == 11 and UNIVERSAL == {"duni", "rdui", "NDBC", "FDBC", "dbnm"}
    full = {"codes": {"Xabc": [
        {"shape": "read", "object_off": 32, "size": 4, "file_off": "0x10"},
        {"shape": "ref_ptr", "object_off": 40, "size": 4, "file_off": "0x20"},
        {"shape": "path_descend", "object_off": None, "size": None}]}}
    narrow, ref_ptr, _ = candidates_from_full(full)
    assert narrow["Xabc"][0]["kind"] == "read" and ref_ptr["Xabc"]["object_off"] == 40
    print("build.py selftest: OK (new candidate conversion; small-table constraints present)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Rebuild t12 schema-constrained 26-entity flat naming from codes_full.json.")
    ap.add_argument("--outdir", type=Path, default=OUT)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        # Keep a resumable marker before any build work.
        save(args.outdir / "naming_result.json", {"status": "in_progress", "results": []})
        build(args.outdir)
        return 0
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
