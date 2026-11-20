#!/usr/bin/env python3
"""t16b: re-calibrate t16 naming bridge and emit a conservative per-tag ledger."""
from __future__ import annotations
import argparse, json, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t16b/out"
LIMIT = 45_000

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

def selftest() -> bool:
    assert norm_pair(4, 2) == (4, 2)
    assert split_codes(["aa", "bb"], 8, 10) == [("aa", 10, 4), ("bb", 14, 4)]
    assert split_codes(["aa"], 4, 3) == [("aa", 3, 4)]
    assert len(shard_rows([{"field": str(i)} for i in range(3)], 120)[0]) == 3
    print("t16b build selftest: PASS")
    return True

def norm_pair(offset: Any, width: Any) -> tuple[int, int] | None:
    try:
        return int(offset), int(width)
    except (TypeError, ValueError):
        return None

def split_codes(codes: list[str], width: Any, offset: Any) -> list[tuple[str, int, int]]:
    pair = norm_pair(offset, width)
    if pair is None:
        return []
    off, wid = pair
    if wid == 8 and len(codes) == 2:
        return [(codes[0], off, 4), (codes[1], off + 4, 4)]
    return [(c, off, wid) for c in codes]

def shard_rows(rows: list[dict[str, Any]], max_bytes: int = LIMIT) -> list[list[dict[str, Any]]]:
    parts: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for row in rows:
        trial = current + [row]
        size = len(json.dumps(trial, ensure_ascii=False, separators=(",", ":")).encode())
        if current and size > max_bytes:
            parts.append(current)
            current = [row]
        else:
            current = trial
    if current:
        parts.append(current)
    return parts

class Build:
    def __init__(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        import t16_serializer_walk as t16
        self.w = t16.Walker()
        self.schema = self.w.schema
        self.stage2 = self.w.stage2
        self.entities = {v.get("code"): (k, v) for k, v in self.schema["entities"].items()}
        self.code_doc = load(ROOT / "scratch/t12/out/codes_full.json")
        self.exe_sha256 = self.code_doc.get("exe_sha256")
        self.codes = self.w.codes
        self.chains = self.w.code_chain
        self.baselines: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
        self.expected_rows: list[dict[str, Any]] = []
        self.docs: dict[str, dict[str, Any]] = {}
        self.class_stats: dict[str, dict[str, Any]] = {}
        self.g1: dict[str, Any] = {}
        self._load_baselines()

    def _add_ref(self, tag: str, field: str, offset: Any, width: Any, source: str,
                 table_type: int | None = None, note: str | None = None) -> None:
        ref = {"entity_tag": tag, "field": field, "offset": offset, "width": width,
               "source": source, "table_type": table_type, "note": note}
        self.expected_rows.append(ref)
        self.baselines[tag][field].append(ref)

    def _load_baselines(self) -> None:
        weather = load(ROOT / "scratch/t01/inbox/t01l/output.json")["row_offset_map"]
        for code, item in weather.items():
            if code == "wnam":
                self._add_ref("weat", code, None, None, "scratch/t01/inbox/t01l/output.json",
                              27, "variable UTF-8 name; no fixed numeric width")
            else:
                off = int(item.get("season", 0)) * 23 + int(item.get("nested_member_offset_in_season", 0))
                self._add_ref("weat", code, off, item.get("width"),
                              "scratch/t01/inbox/t01l/output.json", 27,
                              "normalized after variable name prefix: season*23 + member offset")
        comp = load(ROOT / "scratch/t01/inbox/t01f/output.json")["row_offset_map"]
        for code, item in comp.items():
            if item.get("counted_as_new_schema_business_field"):
                self._add_ref("comp", code, item.get("row_offset"), item.get("width"),
                              "scratch/t01/inbox/t01f/output.json", 25)
        names = load(ROOT / "reports/t12_field_names.json")
        usable = {"readpair", "ref_only", "chain_unique", "schema_fixed", "ref_pair", "full_shape_unique"}
        for slot in names.get("slots", []):
            tag = None
            try:
                _, entity = self.w.entity_schema(slot.get("schema_entity", ""))
                tag = entity.get("code")
            except Exception:
                continue
            if slot.get("confidence") not in usable:
                continue
            for code, off, wid in split_codes(slot.get("codes", []), slot.get("width"), slot.get("row_off")):
                self._add_ref(tag, code, off, wid, "reports/t12_field_names.json",
                              int(slot["type_id"]), f"E55 {slot.get('archive')} {slot.get('confidence')}")

    def resolved_tags(self) -> list[str]:
        tags = sorted({x["entity"] for x in self.stage2.get("tables", []) if x.get("status") == "resolved"})
        priority = ["club", "nati", "comp", "team"]
        return [x for x in priority if x in tags] + [x for x in tags if x not in priority]

    def _direct_matches(self, code: str, object_off: Any, width: int) -> list[dict[str, Any]]:
        if object_off is None:
            return []
        out = []
        for inst in self.codes.get(code, []):
            if inst.get("shape") == "read" and inst.get("object_off") == int(object_off) and inst.get("size") == width:
                out.append(inst)
        return out

    def _walk_candidates(self, tag: str, top_fields: list[dict[str, Any]], walk: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
        codes = Counter(f.get("code") for f in top_fields)
        field_by_code = {f.get("code"): f for f in top_fields if f.get("code")}
        allowed = self.schema.get("type_width_candidates", {})
        candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
        branches = 0
        functions = 0
        for trace in walk.get("classes", []):
            table_type = int(trace.get("table_type", -1))
            for fn in trace.get("serializer_functions", []):
                functions += 1
                branches += int(fn.get("branch_count", 0))
                cursor = 0
                for event in fn.get("events", []):
                    width = int(event.get("width", 0))
                    obj = event.get("object_off")
                    for code, field in field_by_code.items():
                        widths = set(allowed.get(field.get("type", ""), {}).get("candidates", []))
                        if widths and width not in widths:
                            continue
                        if codes[code] != 1:
                            continue
                        matches = self._direct_matches(code, obj, width)
                        for inst in matches:
                            candidates[code].append({"offset": cursor, "width": width,
                                "table_type": table_type, "class": trace.get("class"),
                                "object_off": obj, "4CC": code, "chain": self.chains.get(code),
                                "serializer_function": fn.get("function_off"),
                                "instruction_offset": event.get("inst_off"),
                                "call_offset": event.get("call_off"),
                                "code_instance_offset": inst.get("file_off"),
                                "code_read_file_offset": (hex(self.w.pe.va2f(int(inst["access_va"], 16)))
                                    if inst.get("access_va") and self.w.pe.va2f(int(inst["access_va"], 16)) is not None else None),
                                "code_access_va": inst.get("access_va"),
                                "code_instruction": inst.get("instruction"),
                                "binary": "editor.exe", "exe_sha256": self.exe_sha256,
                                "branch_depth": event.get("branch_depth"),
                                "branch_count": fn.get("branch_count", 0)})
                    cursor += width
        return candidates, {"classes_walked": len(walk.get("classes", [])),
                            "serializer_functions": functions, "conditional_jump_count": branches,
                            "class_branches": [{"table_type": x.get("table_type"), "class": x.get("class"),
                                "status": x.get("status"), "serializer_functions": len(x.get("serializer_functions", [])),
                                "conditional_jump_count": sum(int(y.get("branch_count", 0)) for y in x.get("serializer_functions", []))}
                                for x in walk.get("classes", [])]}

    def _build_entity(self, tag: str) -> dict[str, Any]:
        if tag not in self.entities:
            return {"entity_tag": tag, "entity": tag, "fields": [], "fields_total": 0,
                    "fields_named": 0, "fields_unnamed": 0, "status": "schema_missing"}
        name, entity = self.entities[tag]
        top = [f for f in entity.get("fields", []) if f.get("parent") is None]
        nested = [f for f in entity.get("fields", []) if f.get("parent") is not None]
        skip_play = tag == "play"
        if not skip_play:
            engine, _ = self.w.field_rows(name)
            candidates, stat = self._walk_candidates(tag, top, engine.get("walk", {}))
        else:
            engine, candidates = {}, defaultdict(list)
            stat = {"classes_walked": 0, "serializer_functions": 0, "conditional_jump_count": 0, "class_branches": []}
        rows = []
        conflicts = []
        for f in top:
            code, typ = f.get("code"), f.get("type", "unknown")
            cand = candidates.get(code, [])
            unique_pairs = {(x["offset"], x["width"]) for x in cand}
            field_refs = self.baselines[tag].get(code, [])
            ref_pairs = {(int(x["offset"]), int(x["width"])) for x in field_refs
                         if x.get("offset") is not None and x.get("width") is not None}
            chosen_ref = next((x for x in field_refs if x.get("offset") is not None), None)
            chosen_source = chosen_ref.get("source") if chosen_ref else None
            if len(unique_pairs) == 1:
                off, width = next(iter(unique_pairs))
                evidence = {"bridge": "walked object_off/width -> codes_full read instance -> exact schema field code",
                            "matches": cand, "table_types": sorted({x["table_type"] for x in cand})}
                if ref_pairs and (off, width) not in ref_pairs:
                    conflicts.append({"field": code, "kind": "walk_vs_inherited", "walk": [off, width],
                                      "inherited": sorted([list(x) for x in ref_pairs])})
                    if chosen_ref:
                        off, width = int(chosen_ref["offset"]), int(chosen_ref["width"])
                        grade, source = "L3_inherited", chosen_source
                        evidence["walk_conflict_preserved"] = True
                    else:
                        grade, source = "unnamed", "no unique inherited baseline"
                        off = width = None
                else:
                    grade, source = "L3_instruction", "scratch/t12/out/codes_full.json + t16 walked serializer + schema_inventory"
                    if chosen_ref:
                        evidence["inherited_confirmation"] = {"source": chosen_source, "offset": chosen_ref["offset"], "width": chosen_ref["width"]}
            elif len(unique_pairs) > 1:
                conflicts.append({"field": code, "kind": "mixed_walk_offsets", "walk": sorted([list(x) for x in unique_pairs])})
                if len(ref_pairs) == 1:
                    off, width = next(iter(ref_pairs)); grade, source = "L3_inherited", chosen_source
                    evidence = {"baseline": field_refs, "walk_candidates": cand, "conflict_preserved": True}
                else:
                    off = width = None; grade, source = "unnamed", "ambiguous walk branches"
                    evidence = {"walk_candidates": cand}
            elif len(ref_pairs) == 1:
                off, width = next(iter(ref_pairs)); grade, source = "L3_inherited", chosen_source
                evidence = {"inherited": field_refs, "walk_candidates": cand}
            elif len(ref_pairs) > 1:
                off = width = None; grade, source = "unnamed", "conflicting inherited references"
                evidence = {"inherited": field_refs}
                conflicts.append({"field": code, "kind": "baseline_conflict", "inherited": sorted([list(x) for x in ref_pairs])})
            else:
                off = width = None; grade, source = "unnamed", "no closed naming bridge"
                evidence = {"reason": "no unique direct object_off/width/4CC/schema bridge"}
            rows.append({"field": code, "offset": off, "width": width, "grade": grade,
                         "evidence": evidence, "source": source, "type": typ})
        for f in nested:
            rows.append({"field": f.get("code"), "parent": f.get("parent"), "offset": None, "width": None,
                         "grade": "unnamed", "evidence": {"reason": "nested/list member; no row-inline mapping asserted"},
                         "source": "scratch/t05/schema_inventory.json", "type": f.get("type", "unknown")})
        named = sum(x["grade"] in ("L3_instruction", "L3_inherited") for x in rows)
        doc = {"entity": name, "entity_tag": tag, "fields_total": len(rows), "top_level_fields": len(top),
               "nested_fields": len(nested), "fields_named": named, "fields_unnamed": len(rows)-named,
               "conflicts": conflicts, "walk_summary": stat, "scope_note": (
                   "Player tag not walked: its schema includes PDxx attribute blocks, excluded by AGENTS.md; all rows retained unnamed."
                   if skip_play else "") , "fields": rows}
        self.docs[tag] = doc
        self.class_stats[tag] = stat
        return doc

    def _attach_data_crosschecks(self) -> None:
        fk = load(ROOT / "scratch/t15/out/fk.json")
        table_to_tag = {int(x["table_type"]): x["entity"] for x in self.stage2["tables"] if x.get("status") == "resolved"}
        for t in fk.get("tables", []):
            typ = int(t.get("table_type", -1))
            if typ not in (30, 38, 49):
                continue
            tag = table_to_tag.get(typ)
            if tag not in self.docs:
                continue
            attached = 0
            semantic_targets = {30: ("play", "Pijl", "STARTING_INJURY supports an injury-list relation"),
                                38: ("play", "Pbnl", "STARTING_BAN supports a ban-list relation"),
                                49: ("pers", "Plhs", "STARTING_PERSON_HISTORY supports a person-history-list relation")}
            target_tag, target_field, relation = semantic_targets[typ]
            target = next((r for r in self.docs.get(target_tag, {}).get("fields", [])
                           if r.get("field") == target_field), None)
            if target is not None:
                target.setdefault("corroboration", []).append({"grade": "L2_data", "subgrade": "C_candidate",
                    "table_type": typ, "rtti_class": t.get("rtti_class"), "relation_candidate": relation,
                    "evidence": t.get("key_evidence"), "source": "scratch/t15/out/fk.json",
                    "caveat": "C-class data evidence supports a list-relation candidate only; it does not establish an inline field offset."})
                attached += 1
            t["_t16b_attached_rows"] = attached

    def _g1_compare(self) -> dict[str, Any]:
        observations: dict[tuple[str, str, int], list[tuple[int, int]]] = defaultdict(list)
        for tag, doc in self.docs.items():
            if not doc.get("walk_summary", {}).get("classes_walked"):
                continue
            # Reconstruct candidates identically from the persisted bridge evidence.
            for row in doc["fields"]:
                evidence = row.get("evidence", {})
                matches = evidence.get("matches", []) or evidence.get("walk_candidates", [])
                for m in matches:
                    observations[(tag, row["field"], int(m["table_type"]))].append((int(m["offset"]), int(m["width"])))
        checks, conflicts, missing = [], [], []
        for ref in self.expected_rows:
            tag, code, typ = ref["entity_tag"], ref["field"], ref.get("table_type")
            if tag not in self.docs:
                continue
            if ref.get("offset") is None or ref.get("width") is None:
                checks.append({"entity_tag": tag, "field": code, "source": ref["source"], "status": "not_comparable",
                               "reason": ref.get("note")})
                continue
            observed = sorted(set(observations.get((tag, code, int(typ)), []))) if typ is not None else []
            expected = (int(ref["offset"]), int(ref["width"]))
            if expected in observed:
                status = "match"
            elif observed:
                status = "conflict"
                conflicts.append({"entity_tag": tag, "field": code, "source": ref["source"], "table_type": typ,
                                  "expected": list(expected), "observed": [list(x) for x in observed]})
            else:
                status = "missing"
                missing.append({"entity_tag": tag, "field": code, "source": ref["source"], "table_type": typ,
                                "expected": list(expected)})
            checks.append({"entity_tag": tag, "field": code, "source": ref["source"], "table_type": typ,
                           "expected": list(expected), "observed": [list(x) for x in observed], "status": status})
        comparable = [x for x in checks if x["status"] != "not_comparable"]
        matches = sum(x["status"] == "match" for x in comparable)
        return {"status": "pass" if comparable and matches / len(comparable) >= .95 else "fail",
                "matches": matches, "compared": len(comparable), "not_comparable": len(checks)-len(comparable),
                "consistency": matches / len(comparable) if comparable else None, "threshold": .95,
                "checks": checks, "conflicts": conflicts, "missing": missing}

    def _write_entity(self, tag: str) -> None:
        doc = self.docs[tag]
        fields = doc["fields"]
        base = OUT / f"fields_{tag}"
        # Every shard is one compact JSON line, <=45 KB; this also keeps writes below 400 lines.
        parts = shard_rows(fields)
        total_size = len(json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode())
        for p in OUT.glob(f"fields_{tag}.part*.json"):
            p.unlink()
        if total_size <= LIMIT:
            dump(OUT / f"fields_{tag}.json", doc)
        else:
            names = []
            for i, rows in enumerate(parts, 1):
                name = f"fields_{tag}.part{i:03d}.json"
                dump(OUT / name, {"entity_tag": tag, "fields": rows})
                names.append(name)
            manifest = {k: v for k, v in doc.items() if k != "fields"}
            manifest.update({"storage": "sharded", "shards": names, "shard_limit_bytes": LIMIT})
            dump(OUT / f"fields_{tag}.json", manifest)

    def _ledger(self, status: str) -> dict[str, Any]:
        entries = []
        for tag in self.resolved_tags():
            if tag not in self.docs:
                continue
            d, s = self.docs[tag], self.class_stats[tag]
            entries.append({"entity_tag": tag, "entity": d.get("entity"), "fields_total": d["fields_total"],
                "top_level_fields": d["top_level_fields"], "nested_fields": d["nested_fields"],
                "fields_named": d["fields_named"], "fields_unnamed": d["fields_unnamed"],
                "coverage": round(d["fields_named"] / d["fields_total"], 6) if d["fields_total"] else 0,
                "conflicts": len(d["conflicts"]),
                "data_crosscheck_fields": sum(bool(x.get("corroboration")) for x in d["fields"]),
                "classes_walked": s.get("classes_walked", 0),
                "serializer_functions": s.get("serializer_functions", 0),
                "conditional_jump_count": s.get("conditional_jump_count", 0),
                "scope_note": d.get("scope_note", "")})
        return {"status": status, "source": "scratch/t14/out/stage2_map.json (resolved tag dedupe)",
                "resolved_entity_tags": len({x["entity"] for x in self.stage2["tables"] if x.get("status")=="resolved"}),
                "entities": entries, "g1": {k:v for k,v in self.g1.items() if k not in ("checks", "conflicts", "missing")},
                "g1_conflict_columns": self.g1.get("conflicts", []), "g1_missing_columns": self.g1.get("missing", []),
                "data_crosscheck_sources": ["scratch/t15/out/fk.json table_type 30/38/49; C-candidate only"]}

    def _write_report(self, status: str) -> None:
        lines = ["# t16b — naming bridge recalibration and entity ledger", "", f"Status: `{status}`", "",
            "## Method", "", "- Reused `scripts/t16_serializer_walk.py` without modification. For each resolved stage2 tag, walked its class readers; only a unique object_off+width direct-read 4CC instance and exact schema code is `L3_instruction`.",
            "- Known E27/E20/E55 rows are `L3_inherited` if a unique fresh bridge is absent. If fresh walk and baseline disagree, the baseline row is retained and the conflict is explicit; ambiguous rows remain unnamed.",
            "- Every schema top-level and nested field is represented. Nested/list members stay unnamed unless a row-inline bridge exists. Player tag is listed but not walked because its schema contains out-of-scope PDxx blocks.",
            "- Branch counts are conditional-jump instruction counts reported by t16, not a proof that each branch corresponds to an individual schema field.", "",
            "## G1 inheritance comparison", "", f"- Result: `{self.g1.get('status')}`; exact matches {self.g1.get('matches')}/{self.g1.get('compared')} = {self.g1.get('consistency')}; threshold 95%.",
            f"- Not numerically comparable (variable-width baseline): {self.g1.get('not_comparable')}.",
            f"- Conflicting columns: {len(self.g1.get('conflicts', []))}; missing walk mappings: {len(self.g1.get('missing', []))}. Missing numeric baseline mappings count as non-matches; only the variable-width E27 name is excluded from the numeric denominator.", "",
            "### Conflicts (walk value differs from inherited baseline)", "", "| tag | field | table | expected offset/width | walked offset/width | source |", "|---|---|---:|---|---|---|"]
        for x in self.g1.get("conflicts", []):
            lines.append(f"| {x['entity_tag']} | {x['field']} | {x.get('table_type')} | {x['expected']} | {x['observed']} | {x['source']} |")
        if not self.g1.get("conflicts"):
            lines.append("| — | none | — | — | — | — |")
        lines.extend(["", "### Baseline fields with no matching walked bridge", "", "| tag | field | table | expected | source |", "|---|---|---:|---|---|"])
        for x in self.g1.get("missing", []):
            lines.append(f"| {x['entity_tag']} | {x['field']} | {x.get('table_type')} | {x['expected']} | {x['source']} |")
        if not self.g1.get("missing"):
            lines.append("| — | none | — | — | — |")
        lines.extend(["", "## Per-entity coverage", "", "| tag | entity | all fields | top-level | nested | named | unnamed | coverage | classes | serializer funcs | conditional jumps | conflicts | L2_data rows |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"])
        for x in self._ledger(status)["entities"]:
            lines.append(f"| {x['entity_tag']} | {x['entity']} | {x['fields_total']} | {x['top_level_fields']} | {x['nested_fields']} | {x['fields_named']} | {x['fields_unnamed']} | {x['coverage']:.1%} | {x['classes_walked']} | {x['serializer_functions']} | {x['conditional_jump_count']} | {x['conflicts']} | {x.get('data_crosscheck_fields', 0)} |")
        lines.extend(["", "## Club mixed-entity branch audit", ""])
        club = self.class_stats.get("club", {})
        lines.append(f"- Factory/class branches walked: {club.get('classes_walked', 0)}; serializer candidate functions: {club.get('serializer_functions', 0)}; reported conditional-jump instructions: {club.get('conditional_jump_count', 0)}.")
        lines.append("- Per-table counts:")
        for b in club.get("class_branches", []):
            lines.append(f"  - table {b.get('table_type')} `{b.get('class')}`: {b.get('serializer_functions')} serializer candidate(s), {b.get('conditional_jump_count')} conditional jumps; {b.get('status')}.")
        lines.extend(["", "t04 had closed one field only. The walk reports structural candidates but does not prove branch-to-field closure; fields remain individually graded and unresolved rows are not guessed.", "",
            "## G3 data-side cross-checks", "", "C-class t15 evidence is attached as secondary `grade=L2_data`, `subgrade=C_candidate`; it supports relation candidates, not field identity or an inline offset.", "- table 30 `STARTING_INJURY` → `play.Pijl` injury-list candidate.", "- table 38 `STARTING_BAN` → `play.Pbnl` ban-list candidate.", "- table 49 `STARTING_PERSON_HISTORY` → `pers.Plhs` person-history-list candidate.", "- These links remain C-class hypotheses; none is promoted to an inline serialized offset.", "",
            "## Unclosed / limitations", "", "- `unnamed` is an allowed ledger state. E55/E20/E27 mismatches are never overwritten silently.",
            "- Conditional serializer paths can produce candidate offsets; branch counts are not field counts. Verify sample checks bridge evidence, not full control-flow closure.",
            "- Player (`play`) rows are present but unwalked to honor the PDxx exclusion. No game/editor/IDA was launched; external files were read-only.", ""])
        (OUT / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
        ledger_lines = ["# t16b ledger", "", f"Status: `{status}`", "",
            f"G1: `{self.g1.get('status')}` — {self.g1.get('matches')}/{self.g1.get('compared')} exact walk/baseline matches ({self.g1.get('consistency')}); threshold 95%.", "",
            "| tag | entity | fields | named | unnamed | coverage | conflicts | L2_data rows |", "|---|---|---:|---:|---:|---:|---:|---:|"]
        for x in self._ledger(status)["entities"]:
            ledger_lines.append(f"| {x['entity_tag']} | {x['entity']} | {x['fields_total']} | {x['fields_named']} | {x['fields_unnamed']} | {x['coverage']:.1%} | {x['conflicts']} | {x.get('data_crosscheck_fields', 0)} |")
        ledger_lines.extend(["", f"G1 mismatches: {len(self.g1.get('conflicts', []))}; baseline fields without a matching walk bridge: {len(self.g1.get('missing', []))}.",
            "See `REPORT.md` for full G1 conflict/missing columns, club branch counts, and limitations.", ""])
        (OUT / "ledger.md").write_text("\n".join(ledger_lines), encoding="utf-8")

    def run(self, limit: int | None = None) -> int:
        OUT.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "scripts/t16b_verify.py", OUT / "verify.py")
        tags = self.resolved_tags()
        selected = tags[:limit] if limit else tags
        for tag in selected:
            print(f"walk {tag} ...", flush=True)
            self._build_entity(tag)
            self._write_entity(tag)
            self.g1 = {"status": "pending", "matches": 0, "compared": 0, "consistency": None,
                       "not_comparable": 0, "conflicts": [], "missing": []}
            dump(OUT / "ledger.json", self._ledger("partial_ledger_build"))
        if len(selected) != len(tags):
            dump(OUT / "status.json", {"status": "partial_ledger_build", "completed_tags": selected, "remaining_tags": tags[len(selected):]})
            return 0
        self._attach_data_crosschecks()
        for tag in tags:
            self._write_entity(tag)
        self.g1 = self._g1_compare()
        qualifier = "g1_ge_95pct" if self.g1["status"] == "pass" else "g1_below_95pct"
        status = f"complete_ledger_partial_coverage_{qualifier}"
        for tag in tags:
            self.docs[tag]["status"] = status
            self._write_entity(tag)
        dump(OUT / "ledger.json", self._ledger(status))
        dump(OUT / "g1_checks.json", self.g1)
        self._write_report(status)
        dump(OUT / "status.json", {"status": status, "resolved_tags": tags, "g1_status": self.g1["status"],
                                    "g1_consistency": self.g1["consistency"], "entity_count": len(tags)})
        return 0

def main(argv: list[str] | None = None) -> int:
    global OUT
    ap = argparse.ArgumentParser(description="Recalibrate the t16 field naming bridge and emit t16b ledger.")
    ap.add_argument("--outdir", default=str(OUT), help="output directory (default scratch/t16b/out)")
    ap.add_argument("--limit", type=int, help="run only first N resolved tags for incremental testing")
    ap.add_argument("--selftest", action="store_true", help="run helper self-tests")
    args = ap.parse_args(argv)
    if args.selftest:
        return 0 if selftest() else 1
    OUT = Path(args.outdir)
    try:
        return Build().run(args.limit)
    except Exception as exc:
        print(f"fatal: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
