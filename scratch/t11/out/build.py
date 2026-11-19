from __future__ import annotations

import argparse
import importlib.util
import json
import re
import runpy
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
LAYOUTS = ROOT / "scratch/t05/layouts.json"
T07_TABLE = ROOT / "scratch/t07/out/4cc_table.json"
T07_NAMING = ROOT / "scratch/t07/out/naming_result.json"
T08_NAMING = ROOT / "scratch/t08/out/naming_result.json"
REFS = ROOT / "scratch/cmd/ref_ptr_codes.json"
UNIVERSAL = {"duni", "rdui", "NDBC", "FDBC", "dbnm"}
SMALL_IDS = [23, 31, 35, 42, 46, 50, 51, 60, 61, 63, 64]
ALIAS = {"city": "city", "inju": "injury", "stad": "stadium",
         "lcrg": "local region", "stgn": "stage name", "regi": "region"}
KNOWN_TYPE_SCHEMA = {2: "city", 6: "injury", 21: "stadium", 23: "stage name", 47: "local region"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def schema_indexes(schema):
    code_entities = defaultdict(set)
    code_types = defaultdict(set)
    entity_codes = {}
    for name, entity in schema["entities"].items():
        codes = set()
        for field in entity.get("fields", []):
            code = field.get("code")
            if not code:
                continue
            codes.add(code)
            code_entities[code].add(name)
            if field.get("type"):
                code_types[code].add(field["type"])
        entity_codes[name] = codes
    return code_entities, code_types, entity_codes


def allowed_widths(types):
    widths = {
        "boolean": {1}, "real": {4}, "float": {4}, "cash": {4},
        "database_record_unique_id": {4}, "database_record_list": {4},
        "day_of_week": {1}, "date": {2, 4}, "integer": {1, 2, 4},
        "enum": {1, 2, 4}, "multiple_enum": {1, 2, 4},
        "short_distance": {1, 2}, "string": {4}, "text": {4},
        "picture": {4}, "unique_id": {8},
    }
    out = set()
    for kind in types:
        out |= widths.get(kind, set())
    return out


def compatible_width(code, width, code_types):
    types = code_types.get(code, set())
    if not types:
        return True
    allowed = allowed_widths(types)
    return not allowed or width in allowed


def extract_candidates(table, refs):
    narrow = defaultdict(list)
    for code, records in table.get("codes", {}).items():
        for rec in records:
            if rec.get("kind") not in ("read", "write", "ref_only"):
                continue
            if not isinstance(rec.get("object_off"), int) or rec.get("size") not in (1, 2, 4):
                continue
            narrow[code].append({"kind": rec["kind"], "object_off": rec["object_off"],
                                 "size": rec["size"], "file_off": rec.get("file_off"),
                                 "access_va": rec.get("access_va"),
                                 "instruction": rec.get("instruction"),
                                 "source": "scratch/t07/out/4cc_table.json"})
    ref_ptr = {}
    for code, rec in refs.get("ref_ptr", {}).items():
        if isinstance(rec.get("object_off"), int):
            ref_ptr[code] = {"kind": "ref_ptr", "object_off": rec["object_off"],
                             "file_off": rec.get("file_off"),
                             "source": "scratch/cmd/ref_ptr_codes.json"}
    return narrow, ref_ptr


def unique_slots(entity):
    """Represent mirrored archives once for schema allocation; retain all concrete slots."""
    concrete = []
    for archive, spec in entity.get("archives", {}).items():
        for f in spec.get("fields", []):
            off = f.get("object_off")
            if isinstance(off, int):
                concrete.append({"archive": archive, "idx": f.get("idx"),
                                 "row_off": f.get("row_off"), "width": f.get("width"),
                                 "object_off": off})
    grouped = defaultdict(list)
    for slot in concrete:
        grouped[(slot["object_off"], slot["width"])].append(slot)
    keys = sorted(grouped)
    return keys, {key: grouped[key] for key in keys}


def candidate_records(code, slot, narrow, ref_ptr, code_types):
    off, width = slot
    hits = []
    for rec in narrow.get(code, []):
        # The schema-first pass follows the task's object_off intersection rule;
        # retain observed access size as evidence, but do not substitute it for reader width.
        if rec["object_off"] == off:
            hits.append(dict(rec))
    ref = ref_ptr.get(code)
    if ref and ref["object_off"] == off and width == 4 and (
            not code_types.get(code) or code_types[code] & {"database_record_unique_id", "database_record_list"}):
        hits.append({**ref, "size": width,
                     "why": "ref_ptr object_off 命中；宽度取 reader slot width (4B), 不取 qword getter 宽度"})
    # Identical records from mirrored client/server archives are one allocation edge.
    uniq = {}
    for rec in hits:
        k = (rec.get("kind"), rec.get("object_off"), rec.get("size"), rec.get("file_off"))
        uniq[k] = rec
    return list(uniq.values())


def allocation_for_entity(entity_name, slots, schema, entity_codes, code_types,
                          narrow, ref_ptr):
    codes = sorted(entity_codes.get(entity_name, set()) - UNIVERSAL)
    edges = {}
    evidence = {}
    for code in codes:
        for i, slot in enumerate(slots):
            hits = candidate_records(code, slot, narrow, ref_ptr, code_types)
            if hits:
                edges.setdefault(code, set()).add(i)
                evidence[(code, i)] = hits
    nslots = len(slots)
    dp = {0: 1}
    for code in sorted(edges):
        nxt = dict(dp)
        for mask, count in dp.items():
            for i in edges[code]:
                bit = 1 << i
                if not mask & bit:
                    nxt[mask | bit] = nxt.get(mask | bit, 0) + count
        dp = nxt
    max_match = max((mask.bit_count() for mask in dp), default=0)
    n_solutions = sum(count for mask, count in dp.items() if mask.bit_count() == max_match)
    complete = nslots > 0 and max_match == nslots
    solution_count = n_solutions
    assignments = {}
    if complete and solution_count == 1:
        # Unique full assignment can be recovered by a bounded DFS; at most five slots.
        ordered_slots = sorted(range(nslots), key=lambda i: sum(i in v for v in edges.values()))
        found = []
        def visit(pos, used, chosen):
            if len(found) > 1:
                return
            if pos == len(ordered_slots):
                found.append(dict(chosen))
                return
            i = ordered_slots[pos]
            for code in sorted(c for c, inds in edges.items() if i in inds and c not in used):
                chosen[i] = code
                visit(pos + 1, used | {code}, chosen)
                chosen.pop(i, None)
        visit(0, set(), {})
        assignments = found[0] if len(found) == 1 else []
    slot_candidate_codes = {
        str(i): sorted(code for code, inds in edges.items() if i in inds)
        for i in range(nslots)
    }
    return {"schema_entity": entity_name, "slot_pairs": [list(x) for x in slots],
            "max_matched_slots": max_match, "slot_count": nslots,
            "complete_assignment_count": solution_count if complete else 0,
            "maximum_partial_assignment_count": solution_count,
            "complete_unique": bool(complete and solution_count == 1),
            "slot_candidates": slot_candidate_codes,
            "assignment": {str(i): code for i, code in assignments.items()},
            "evidence": {f"{code}@slot{i}": evidence[(code, i)]
                         for code, inds in edges.items() for i in inds}}


def vote_from_codes(codes, code_entities, df):
    scores = Counter()
    detail = []
    for code in sorted(set(codes) - UNIVERSAL):
        owners = sorted(code_entities.get(code, set()))
        if not owners:
            detail.append({"code": code, "df": 0, "weight": 0.0, "entities": []})
            continue
        weight = 1.0 / df[code]
        for owner in owners:
            scores[owner] += weight
        detail.append({"code": code, "df": df[code], "weight": weight,
                       "entities": owners})
    ranking = [{"entity": name, "score": round(score, 8)}
               for name, score in sorted(scores.items(), key=lambda x: (-x[1], x[0]))]
    return detail, ranking


def infer_schema_map(base, schema, code_entities, code_types, entity_codes,
                     narrow, ref_ptr):
    df = Counter({code: len(owners) for code, owners in code_entities.items()})
    mappings = []
    for ent in base.get("results", []):
        tid = ent["type_id"]
        codes = {code for arch in ent.get("archives", {}).values()
                 for f in arch.get("fields", []) for code in f.get("codes", [])}
        source = "t08_field_codes"
        if not codes:
            slots, _ = unique_slots(ent)
            code_candidates = set()
            for name in schema["entities"]:
                for code in entity_codes[name] - UNIVERSAL:
                    if any(candidate_records(code, slot, narrow, ref_ptr, code_types)
                           for slot in slots):
                        code_candidates.add(code)
            codes = code_candidates
            source = "offset_width_candidates_for_zero_named_table"
        detail, ranking = vote_from_codes(codes, code_entities, df)
        old_name = ent.get("entity")
        alias = ALIAS.get(old_name)
        chosen = ranking[0]["entity"] if ranking else None
        forced = KNOWN_TYPE_SCHEMA.get(tid)
        if forced:
            chosen = forced
        elif alias and alias in schema["entities"] and old_name != "regi":
            chosen = alias
        rule = "known_type_or_layout_schema_anchor" if forced or (alias and old_name != "regi") else "inverse_schema_df_vote"
        # type 47 has a reader-layout anchor at Lpop's exact unique schema code. The raw
        # code-list vote also includes the known cross-table injury-chain bleed; preserve
        # both the arithmetic and the independent layout/schema anchor in the audit.
        if tid == 47 and "local region" in schema["entities"]:
            chosen = "local region"
            rule = "Lpop_unique_schema_anchor_overrides_cross_chain_vote"
        if not chosen and alias and alias in schema["entities"]:
            chosen = alias
            rule = "known_layout_entity_alias"
        # Emit all ranked candidates, including losers and their scores.
        mappings.append({"type_id": tid, "schema_entity": chosen,
                         "source": source, "decision_rule": rule,
                         "original_layout_entity": old_name,
                         "code_votes": detail, "entity_scores": ranking,
                         "losing_entities": [x for x in ranking if x["entity"] != chosen]})
    return {"status": "complete_schema_df_voted", "method":
            "df(code)=number of schema entities containing code; each non-universal observed code gives 1/df to each owning entity; zero-named tables use offset+reader-width candidates",
            "universal_codes": sorted(UNIVERSAL), "entities": mappings}


def parse_codes(field):
    codes = field.get("codes") or []
    if not codes and field.get("field"):
        codes = re.split(r"[+|]", field["field"])
    return [c for c in codes if c]


def field_name(codes, old_field):
    if len(codes) == 1:
        return codes[0]
    if old_field and "+" in old_field and "|" not in old_field:
        return "+".join(codes)
    return "|".join(codes)


def apply_schema_filter(base, mapping, schema, narrow, ref_ptr, code_types):
    result = json.loads(json.dumps(base))
    by_tid = {x["type_id"]: x for x in mapping["entities"]}
    stats = Counter()
    for ent in result.get("results", []):
        tid = ent["type_id"]
        map_item = by_tid[tid]
        schema_entity = map_item.get("schema_entity")
        allowed = {f.get("code") for f in schema["entities"].get(schema_entity, {}).get("fields", [])
                   if f.get("code")}
        ent["entity"] = schema_entity or ent.get("entity")
        for archive, spec in ent.get("archives", {}).items():
            for f in spec.get("fields", []):
                original_codes = parse_codes(f)
                # Additional names may only be drawn from a legal code already evidenced
                # in the chain/access records; rejected labels remain auditable.
                legal = [c for c in original_codes if c in allowed or c in UNIVERSAL]
                invalid = [c for c in original_codes if c not in allowed and c not in UNIVERSAL]
                if invalid:
                    rejected = f.setdefault("rejected", [])
                    old_accesses = [a for a in f.get("accesses", []) if a.get("code") in invalid]
                    for code in invalid:
                        rejected.append({"code": code, "reason": f"not in {schema_entity} schema field set",
                                         "source_field": f.get("field"),
                                         "accesses": [a for a in old_accesses if a.get("code") == code]})
                    f["accesses"] = [a for a in f.get("accesses", []) if a.get("code") not in invalid]
                    stats["rejected_codes"] += len(invalid)
                if invalid and legal:
                    f["field"] = field_name(legal, f.get("field"))
                    f["codes"] = legal
                    f["confidence"] = "schema_fixed" if len(legal) == 1 else "chain_ambiguous"
                    f["why"] = list(f.get("why", [])) + [
                        f"schema 约束 {schema_entity}: 拒绝 {','.join(invalid)}，保留合法候选 {','.join(legal)}。"]
                    stats["rescued_slots"] += 1
                elif invalid and not legal:
                    f["field"] = None
                    f["codes"] = []
                    f["confidence"] = "unresolved"
                    f["why"] = list(f.get("why", [])) + [
                        f"schema 约束 {schema_entity}: 所有原候选均非法，降级 unresolved；原码见 rejected。"]
                    stats["emptied_slots"] += 1
                elif f.get("confidence") == "chain_ambiguous" and len(legal) == 1:
                    f["field"] = legal[0]
                    f["codes"] = legal
                    f["confidence"] = "schema_fixed"
                    stats["ambiguous_resolved"] += 1
                    f["why"] = list(f.get("why", [])) + [
                        f"同槽候选中仅 {legal[0]} 属于 {schema_entity} schema，按合规码唯一裁决。"]
                elif f.get("field") is not None and not legal and not original_codes:
                    # A name without code evidence is never schema-valid.
                    f["field"] = None
                    f["confidence"] = "unresolved"
                    stats["emptied_slots"] += 1
                # row_off and width are immutable by construction.
    result["status"] = "complete_schema_constrained_ref_ptr"
    result["note"] = ("t08 naming base plus hard schema allow-list, unique compliant-code ambiguity resolution, "
                      "and independently decoded ref_ptr getters; row_off/width unchanged.")
    named = sum(f.get("field") is not None for e in result.get("results", [])
                for a in e.get("archives", {}).values() for f in a.get("fields", []))
    confidences = Counter(f.get("confidence") for e in result.get("results", [])
                          for a in e.get("archives", {}).values() for f in a.get("fields", []))
    result["summary"] = {"slots": sum(confidences.values()), "named_slots": named,
                          "confidence": dict(sorted(confidences.items())), **dict(stats)}
    return result


def load_pe():
    spec = importlib.util.spec_from_file_location("t11_pe", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.default()


def decode_ref_getter(pe, md, code, file_off):
    off = int(file_off, 16) if isinstance(file_off, str) else file_off
    va = pe.f2va(off)
    if va is None:
        return None
    ins = list(md.disasm(pe.raw[off:off + 24], va))
    if len(ins) < 2 or ins[0].mnemonic != "cmp" or ins[1].mnemonic not in ("je", "jz"):
        return None
    try:
        target = int(ins[1].op_str.strip(), 0)
    except ValueError:
        return None
    target_off = pe.va2f(target)
    if target_off is None:
        return None
    seq = list(md.disasm(pe.raw[target_off:target_off + 32], target))
    for i, cur in enumerate(seq[:4]):
        if cur.mnemonic != "mov" or "qword ptr [" not in cur.op_str.lower():
            continue
        mem = re.search(r"\[\s*([a-z0-9]+)\s*\+\s*(0x[0-9a-f]+)\s*\]", cur.op_str.lower())
        if not mem or i + 2 >= len(seq):
            continue
        reg = cur.op_str.split(",", 1)[0].strip().lower()
        test = seq[i + 1]
        branch = seq[i + 2]
        if test.mnemonic != "test" or test.op_str.lower().replace(" ", "") != f"{reg},{reg}":
            continue
        if branch.mnemonic not in ("je", "jz", "jne", "jnz"):
            continue
        return {"code": code, "file_off": hex(off), "cmp_va": hex(va),
                "object_off": int(mem.group(2), 16), "access_va": hex(cur.address),
                "instruction": f"{cur.mnemonic} {cur.op_str}",
                "null_check": f"{test.mnemonic} {test.op_str}; {branch.mnemonic} {branch.op_str}",
                "kind": "ref_ptr", "branch": branch.mnemonic,
                "branch_target_va": hex(int(branch.op_str, 0))}
    return None


def add_type22_ref_pairs(result, mapping, refs, schema, pe, md):
    type22 = next((x for x in result["results"] if x["type_id"] == 22), None)
    if not type22:
        return []
    allowed = {f.get("code") for f in schema["entities"]["club"].get("fields", [])}
    specs = {"Sold": (32, 4, 4), "Snew": (40, 4, 8), "Salt": (72, 4, 17)}
    recorded = []
    for code, (off, width, row_off) in specs.items():
        ref = refs.get("ref_ptr", {}).get(code)
        decoded = decode_ref_getter(pe, md, code, ref.get("file_off") if ref else None)
        if not ref or ref.get("object_off") != off or not decoded or decoded["object_off"] != off:
            continue
        if code not in allowed:
            continue
        slot = next((f for f in type22["archives"]["server"]["fields"]
                     if f.get("object_off") == off and f.get("width") == width
                     and f.get("row_off") == row_off), None)
        if not slot:
            continue
        access = {"code": code, "object_off": off, "size": width, "kind": "ref_ptr",
                  "file_off": decoded["file_off"], "access_va": decoded["access_va"],
                  "cmp_va": decoded["cmp_va"], "instruction": decoded["instruction"],
                  "null_check": decoded["null_check"],
                  "why": "mov r64,qword ptr [reg+OFF] + test/null branch; object_off=OFF, width来自reader slot"}
        slot["field"] = code
        slot["codes"] = [code]
        slot["confidence"] = "ref_pair"
        slot["accesses"] = [access]
        slot["why"] = [f"{code} ref_ptr cmp 在 {decoded['file_off']}，对象偏移 +{off:#x}；reader row+{row_off}/w{width}。"]
        slot.pop("rejected", None)
        recorded.append({"type_id": 22, "row_off": row_off, "width": width,
                         "object_off": off, **access})
    result["summary"]["named_slots"] = sum(f.get("field") is not None for e in result["results"]
        for a in e.get("archives", {}).values() for f in a.get("fields", []))
    result["summary"]["confidence"] = dict(sorted(Counter(f.get("confidence") for e in result["results"]
        for a in e.get("archives", {}).values() for f in a.get("fields", [])).items()))
    result["summary"]["ref_ptr_added"] = len(recorded)
    return recorded


def small_table_results(result, mapping, schema, entity_codes, code_types,
                        narrow, ref_ptr):
    mapped = {x["type_id"]: x.get("schema_entity") for x in mapping["entities"]}
    out = []
    for tid in SMALL_IDS:
        entity = next(x for x in result["results"] if x["type_id"] == tid)
        name = mapped.get(tid)
        slots, concrete = unique_slots(entity)
        all_schema_unique = []
        for candidate_schema in schema["entities"]:
            candidate_allocation = allocation_for_entity(candidate_schema, slots, schema, entity_codes,
                                                         code_types, narrow, ref_ptr)
            if candidate_allocation["complete_unique"]:
                all_schema_unique.append({"schema_entity": candidate_schema,
                    "assignment": candidate_allocation["assignment"],
                    "solution_space_size": candidate_allocation["complete_assignment_count"]})
        if name not in schema["entities"]:
            allocation = {"schema_entity": name, "slot_pairs": [list(x) for x in slots],
                          "max_matched_slots": 0, "slot_count": len(slots),
                          "complete_assignment_count": 0, "maximum_partial_assignment_count": 0,
                          "complete_unique": False, "slot_candidates": {}, "assignment": {}, "evidence": {}}
            status = "no_instance"
        else:
            allocation = allocation_for_entity(name, slots, schema, entity_codes,
                                               code_types, narrow, ref_ptr)
            if allocation["max_matched_slots"] == 0:
                status = "no_instance"
            elif allocation["complete_unique"]:
                status = "unique_solution"
            else:
                status = "ambiguous"
        if name in schema["entities"]:
            table_candidate_offsets = sorted({rec["object_off"] for code in entity_codes.get(name, set()) - UNIVERSAL
                for rec in narrow.get(code, [])} | {ref_ptr[code]["object_off"]
                for code in entity_codes.get(name, set()) - UNIVERSAL if code in ref_ptr})
        else:
            table_candidate_offsets = sorted({rec["object_off"] for records in narrow.values() for rec in records} |
                                             {rec["object_off"] for rec in ref_ptr.values()})
        slot_offsets = sorted({x[0] for x in slots})
        intersection = sorted(set(slot_offsets) & set(table_candidate_offsets))
        no_instance_numeric = {"reader_slot_offsets": slot_offsets,
                               "schema_candidate_offsets": table_candidate_offsets,
                               "intersection": intersection,
                               "intersection_empty": not intersection}
        assignments = allocation.get("assignment", {}) if status == "unique_solution" else {}
        if status == "unique_solution":
            for slot_index, code in assignments.items():
                off, width = slots[int(slot_index)]
                ev = allocation["evidence"].get(f"{code}@slot{slot_index}", [])
                for archive_spec in entity.get("archives", {}).values():
                    for f in archive_spec.get("fields", []):
                        if f.get("object_off") != off or f.get("width") != width or f.get("field") is not None:
                            continue
                        evidence = []
                        for rec in ev:
                            evidence.append({"code": code, "object_off": off, "size": width,
                                "kind": rec["kind"], "file_off": rec.get("file_off"),
                                "access_va": rec.get("access_va"),
                                "instruction": rec.get("instruction"),
                                "why": rec.get("why", "schema-first offset/width candidate")})
                        f["field"] = code
                        f["codes"] = [code]
                        f["confidence"] = "schema_first"
                        f["accesses"] = evidence
                        f["why"] = [f"唯一完整单射分配: {name}.{code} -> object_off {off}, reader width {width}。"]
        out.append({"type_id": tid, "schema_entity": name,
                    "schema_fields_without_universal": len(entity_codes.get(name, set()) - UNIVERSAL)
                        if name in schema["entities"] else 0,
                    "reader_slots": [{"object_off": off, "width": width,
                        "concrete_slots": concrete[(off, width)],
                        "candidate_codes": allocation.get("slot_candidates", {}).get(str(i), [])}
                        for i, (off, width) in enumerate(slots)],
                    "solution_space_size": allocation.get("complete_assignment_count", 0),
                    "maximum_partial_solution_space_size": allocation.get("maximum_partial_assignment_count", 0),
                    "max_matched_slots": allocation.get("max_matched_slots", 0),
                    "status": status, "assignment": assignments,
                    "all_schema_unique_solutions": all_schema_unique,
                    "schema_search_count": len(schema["entities"]),
                    "no_instance_numeric": no_instance_numeric,
                    "candidate_evidence": allocation.get("evidence", {}),
                    "data_side_verification": {"status": "pending"}})
    return {"status": "complete_schema_first_analysis", "tables": out}


def data_side_checks(small, naming, schema):
    """Export selected rows through scripts/fm24_dump.py; never write to its inputs."""
    dump_mod = runpy.run_path(str(ROOT / "scripts/fm24_dump.py"))
    codec = dump_mod["_reader"]()
    naming_by_type = {e["type_id"]: e for e in naming["results"]}
    attempts = []
    unique_rows = [x for x in small["tables"] if x["status"] == "unique_solution"]
    for row in unique_rows:
        tid = row["type_id"]
        ent = naming_by_type[tid]
        archive = "server" if "server" in ent["archives"] else next(iter(ent["archives"]))
        dumped = dump_mod["dump"](archive, tid, 512, codec)
        slot_results = []
        supported = True
        for slot_index, code in row.get("assignment", {}).items():
            slot = row["reader_slots"][int(slot_index)]
            concrete = next((x for x in slot["concrete_slots"] if x["archive"] == archive),
                            slot["concrete_slots"][0])
            width, row_off = slot["width"], concrete["row_off"]
            values = []
            for rec in dumped["rows"]:
                raw = bytes.fromhex(rec["raw_hex"])
                values.append(int.from_bytes(raw[row_off:row_off + width], "little")
                              if row_off + width <= len(raw) else None)
            field_types = sorted({f.get("type") for f in schema["entities"][row["schema_entity"]]["fields"]
                                  if f.get("code") == code and f.get("type")})
            # Conservative, field-semantic checks; string IDs cannot be certified from a 1B slot.
            ok = True
            reason = "observed column retained for semantic review"
            if "string" in field_types or "text" in field_types:
                ok = width == 4
                reason = "string/reference field requires 4B row value; reader slot is " + str(width) + "B"
            elif "boolean" in field_types:
                ok = all(v in (0, 1) for v in values if v is not None)
                reason = "boolean domain must be {0,1}"
            elif code.lower() == "year":
                ok = all(1800 <= v <= 2200 for v in values if v is not None)
                reason = "year domain must be 1800..2200"
            slot_results.append({"code": code, "row_off": row_off, "width": width,
                                 "schema_types": field_types, "sample_count": len(values),
                                 "sample_values": values[:16],
                                 "distinct_sample_values": sorted(set(v for v in values if v is not None))[:32],
                                 "semantic_check": reason, "supported": ok})
            supported = supported and ok
        record = {"type_id": tid, "archive": archive, "export_rows": len(dumped["rows"]),
                  "status": "supported" if supported else "not_supported",
                  "slot_checks": slot_results,
                  "source": "scripts/fm24_dump.py read-only export"}
        row["data_side_verification"] = record
        attempts.append(record)
        if not supported:
            row["status_before_data_check"] = "unique_solution"
            row["status"] = "ambiguous"
            row["downgrade_reason"] = "data-side value domain does not support the schema-first name"
            for f_ent in ent["archives"].values():
                for f in f_ent["fields"]:
                    if f.get("confidence") == "schema_first":
                        f["confidence"] = "chain_ambiguous"
                        f["why"] = list(f.get("why", [])) + ["数据侧值域不支持唯一解，降级为 ambiguous；候选留存。"]
    # A second read-only diagnostic is retained even when no second unique table exists.
    if len(attempts) < 2:
        tid = next((t for t in (31, 35, 42, 46, 50, 51, 60, 64) if t in naming_by_type), None)
        if tid is not None:
            ent = naming_by_type[tid]
            archive = "server" if "server" in ent["archives"] else next(iter(ent["archives"]))
            dumped = dump_mod["dump"](archive, tid, 512, codec)
            row = next(x for x in small["tables"] if x["type_id"] == tid)
            diag = []
            for slot in row["reader_slots"]:
                concrete = next((x for x in slot["concrete_slots"] if x["archive"] == archive),
                                slot["concrete_slots"][0])
                off, width = concrete["row_off"], slot["width"]
                vals = [int.from_bytes(bytes.fromhex(r["raw_hex"])[off:off + width], "little")
                        for r in dumped["rows"] if off + width <= len(bytes.fromhex(r["raw_hex"]))]
                diag.append({"object_off": slot["object_off"], "row_off": off, "width": width,
                             "candidate_codes": slot["candidate_codes"], "sample_count": len(vals),
                             "sample_values": vals[:16],
                             "distinct_sample_values": sorted(set(vals))[:32]})
            attempts.append({"type_id": tid, "archive": archive,
                             "export_rows": len(dumped["rows"]),
                             "status": "diagnostic_only_not_unique",
                             "slots": diag, "source": "scripts/fm24_dump.py read-only export"})
    small["data_side_attempts"] = attempts
    return small


def selftest():
    assert allowed_widths({"database_record_unique_id"}) == {4}
    assert compatible_width("x", 4, {})
    assert not compatible_width("x", 8, {"x": {"boolean"}})
    assert vote_from_codes(["x"], {"x": {"a", "b"}}, Counter({"x": 2}))[1][0]["score"] == 0.5
    print("build.py selftest: OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build t11 schema-constrained naming and schema-first small-table allocations.")
    ap.add_argument("--outdir", default=str(OUT))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        for filename, value in (("schema_map.json", {"status": "in_progress", "entities": []}),
                                ("naming_result.json", {"status": "in_progress", "results": []}),
                                ("small_tables.json", {"status": "in_progress", "tables": []})):
            save(Path(args.outdir) / filename, value)
        schema = load(SCHEMA)
        layouts = load(LAYOUTS)
        table = load(T07_TABLE)
        refs = load(REFS)
        base = load(T08_NAMING)
        code_entities, code_types, entity_codes = schema_indexes(schema)
        df = Counter({code: len(names) for code, names in code_entities.items()})
        narrow, ref_ptr = extract_candidates(table, refs)
        mapping = infer_schema_map(base, schema, code_entities, code_types, entity_codes, narrow, ref_ptr)
        save(Path(args.outdir) / "schema_map.json", mapping)
        naming = apply_schema_filter(base, mapping, schema, narrow, ref_ptr, code_types)
        pe = load_pe()
        from capstone import CS_ARCH_X86, CS_MODE_64, Cs
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        ref_added = add_type22_ref_pairs(naming, mapping, refs, schema, pe, md)
        small = small_table_results(naming, mapping, schema, entity_codes, code_types, narrow, ref_ptr)
        small = data_side_checks(small, naming, schema)
        naming["summary"]["named_slots"] = sum(f.get("field") is not None for e in naming["results"]
            for a in e.get("archives", {}).values() for f in a.get("fields", []))
        naming["summary"]["confidence"] = dict(sorted(Counter(f.get("confidence") for e in naming["results"]
            for a in e.get("archives", {}).values() for f in a.get("fields", [])).items()))
        naming["summary"]["ref_ptr_added"] = len(ref_added)
        naming["exe_sha256"] = table.get("exe_sha256")
        small["status"] = "complete_schema_first_analysis"
        small["ref_ptr_anchor_records"] = ref_added
        save(Path(args.outdir) / "naming_result.json", naming)
        save(Path(args.outdir) / "small_tables.json", small)
        print(f"schema mappings={len(mapping['entities'])}; named={naming['summary']['named_slots']}/240; "
              f"ref_ptr={len(ref_added)}; rejected codes={naming['summary'].get('rejected_codes', 0)}")
        for row in small["tables"]:
            print(f"type {row['type_id']}: {row['schema_entity']} {row['status']} "
                  f"max={row['max_matched_slots']}/{len(row['reader_slots'])} "
                  f"solutions={row['solution_space_size']}")
        return 0
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
