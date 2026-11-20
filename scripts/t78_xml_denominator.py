#!/usr/bin/env python3
"""t78 - bucket the 1,034 top-level club/nation/comp XML occurrences onto a
physical-coverage denominator, using ONLY already-frozen evidence.

Reads (read-only):
  reports/club_nation_subtable_schema.json          (schema v10: E97/E94/E99 + E106/E108/E107)
  scratch/t71/out/field_map_r3.json                 (24 club promotions: 22 cnst + Cebd + Cyfn)
  scratch/t72/out/inventory.json, fingerprints.json (slot census: kind=unnamed/held/l3_claimed/...)
  scratch/t57/out/field_map.json                    (club r1: 10 skipped_separate_member)
  scratch/t63/out/projections.json                  (club r2 4CC dispatch entries)
  scratch/t64/out/field_map_r2.json                 (comp r2 classification of the 196)
  scratch/t55/out/field_map.json                    (nation r1 census, 346 occurrences)
  scratch/t59/out/field_map.json                    (comp r1 census, 255 occurrences)
  scratch/t69/out/tail_ledger.json                  (18 tail items)
  evidence/fm24/reports/editor_schema/master.json   (field type / dependencies)

Writes only: scratch/t78/out/{buckets.json,coverage.md,DONE.md}

No .dat is touched, no disassembly is performed; every claim is a JSON pointer
into an existing frozen artifact.

Exit codes: 0 ok / 1 self-check failed / 2 usage or fatal.
"""
import argparse
import json
import os
import sys

BUCKETS = [
    "mapped_l3",
    "independent_member",
    "string_name_table",
    "ui_or_derived",
    "held",
    "unresolved_wire_slot",
    "no_wire_evidence",
]
ENTITIES = ["club", "nation", "comp"]
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS_DIR)
OUTDIR = os.path.join(ROOT, "scratch", "t78", "out")

P_SCHEMA = "reports/club_nation_subtable_schema.json"
P_T71 = "scratch/t71/out/field_map_r3.json"
P_T72INV = "scratch/t72/out/inventory.json"
P_T72FP = "scratch/t72/out/fingerprints.json"
P_T57 = "scratch/t57/out/field_map.json"
P_T63 = "scratch/t63/out/projections.json"
P_T64 = "scratch/t64/out/field_map_r2.json"
P_T55 = "scratch/t55/out/field_map.json"
P_T59 = "scratch/t59/out/field_map.json"
P_T69 = "scratch/t69/out/tail_ledger.json"
P_MASTER = "evidence/fm24/reports/editor_schema/master.json"


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def ptr(path, pointer):
    return "%s#%s" % (path, pointer)


def build_occurrences():
    """Occurrence spine in frozen XML order, one record per (entity, xml_index)."""
    occ = []
    t57 = load(P_T57)
    t55 = load(P_T55)
    t59 = load(P_T59)
    for f in t57["fields"]:
        occ.append({"entity": "club", "xml_index": f["xml_index"], "code": f["code"],
                    "root": "club", "r1_grade": f["grade"]})
    for f in t55["fields"]:
        occ.append({"entity": "nation", "xml_index": f["xml_index"], "code": f["code"],
                    "root": "nati", "r1_grade": f["grade"]})
    for f in t59["fields"]:
        occ.append({"entity": "comp", "xml_index": f["xml_index"], "code": f["code"],
                    "root": "comp", "r1_grade": f["status"]})
    for o in occ:
        o["id"] = "%s.xml#%s/%03d" % (o["entity"], o["root"], o["xml_index"])
    return occ


def master_fields():
    m = load(P_MASTER)
    out = {}
    for ent, key in (("club", "club.xml"), ("nation", "nation.xml"), ("comp", "comp.xml")):
        out[ent] = m["entities"][key][0]["fields"]
    return out


# ---------------------------------------------------------------- classify
DISPLAY_BUCKET = {"button": "ui_or_derived", "picture": "ui_or_derived"}

# t64 classification -> bucket. advanced_rules_or_debug is *absence of a literal
# 4CC case in the bounded roots*, so it is no_wire_evidence, not a derived value.
COMP64_RULE = {
    "derived_count": "ui_or_derived",
    "derived_list_or_shared_handler": "ui_or_derived",
    "derived_parent_or_global_state": "ui_or_derived",
    "rules_context_sibling": "ui_or_derived",
    "projection_candidate": "ui_or_derived",
    "bounded_getter_without_wire_closure": "unresolved_wire_slot",
    "no_bounded_comp_getter_case": "no_wire_evidence",
    "advanced_rules_or_debug": "no_wire_evidence",
}


def classify_club(occ, ctx):
    """Club: mapped_l3 > independent_member > ui_or_derived > held > residue."""
    i = occ["xml_index"]
    code = occ["code"]
    if code in ctx["t71_by_code"]:
        return ("mapped_l3", ptr(P_T71, "/fields/%d" % ctx["t71_by_code"][code]),
                "t71 promotion (prior %s/%s)" % (ctx["t71"][ctx["t71_by_code"][code]]["prior"]["ledger"],
                                                ctx["t71"][ctx["t71_by_code"][code]]["prior"]["grade"]))
    if i in ctx["r2_l3"]:
        return ("mapped_l3", ptr(P_SCHEMA, "/club_main_row_fields_r2/new_L3_records/%d" % ctx["r2_l3"][i]),
                "t63 r2 new L3 (projection_family=%s)" % ctx["r2"][i]["projection_family"])
    if occ["r1_grade"] == "L3":
        return ("mapped_l3", ptr(P_SCHEMA, "/club_main_row_fields/L3_fields/%d" % ctx["r1_l3"][i]),
                "E97 L3 (t57 r1, frozen)")
    if occ["r1_grade"] == "skipped_separate_member":
        return ("independent_member", ptr(P_T69, "/entries/%d" % ctx["tail"]["club.%s" % code]),
                "t69 tail item %s -> separate member" % ctx["tail"]["club.%s" % code])
    if i in ctx["r2_held"]:
        return ("held", ptr(P_SCHEMA, "/club_main_row_fields_r2/held_records/%d" % ctx["r2_held"][i]),
                ctx["r2"][i]["reason"][:80])
    if occ["r1_grade"] == "held":
        return ("held", ptr(P_T57, "/fields/%d/grade" % i),
                "E97 r1 held, no t71/t63 promotion")
    if ctx["master_type"][i] in DISPLAY_BUCKET:
        return ("ui_or_derived", ptr(P_MASTER, "/entities/club.xml/0/fields/%d/type" % i),
                "master type=%s: display resource, no packed row scalar" % ctx["master_type"][i])
    if i in ctx["dispatch"]:
        return ("unresolved_wire_slot", ptr(P_T63, "/occurrences/%d/dispatch" % ctx["dispatch"][i]),
                "4CC getter reachable, no named main-row slot (t72 unnamed %d)"
                % ctx["unnamed_slots"]["club"])
    return ("no_wire_evidence", ptr(P_SCHEMA, "/club_main_row_fields_r2/unmapped_records/%d" % ctx["r2um"][i]),
            ctx["r2"][i]["reason"][:80])


def classify_nation(occ, ctx):
    i = occ["xml_index"]
    code = occ["code"]
    g = occ["r1_grade"]
    if g == "L3":
        return ("mapped_l3", ptr(P_SCHEMA, "/nation_main_row_fields/L3_fields/%d" % ctx["n_l3"][i]),
                "E94 L3")
    if code == "TCrs":
        return ("independent_member", ptr(P_T55, "/fields/%d/reason" % i),
                "t53: persists in table_9.dat + table_extra_9.dat, not a table_10 slot")
    if g == "no_wire_slot" and code == "EDfx":
        return ("ui_or_derived", ptr(P_T55, "/fields/%d/reason" % i),
                "t53: generated UI output only")
    if i in ctx["n_r2_held"]:
        return ("held", ptr(P_SCHEMA, "/nation_main_row_fields_r2/held_records/%d" % ctx["n_r2_held"][i]),
                ctx["n_r2"][i]["status"])
    if g in ("held", "linked_parent_held", "prior_collection", "prior_identity"):
        return ("held", ptr(P_T55, "/fields/%d/grade" % i),
                "E94/E108 %s: byte located, promotion withheld" % g)
    return ("no_wire_evidence", ptr(P_SCHEMA, "/nation_main_row_fields_r2/unmapped_records/%d" % ctx["n_r2um"][i]),
            "E108: no_bounded_exact_getter_gate")


def classify_comp(occ, ctx):
    i = occ["xml_index"]
    g = occ["r1_grade"]
    if g == "L3":
        return ("mapped_l3", ptr(P_SCHEMA, "/comp_main_row_fields/L3_fields/%d" % ctx["c_l3"][i]), "E99 L3")
    if g == "held":
        return ("held", ptr(P_SCHEMA, "/comp_main_row_fields/held_records/%d" % ctx["c_held"][i]),
                "E99 held, E107 preserved")
    cls = ctx["c64"][i]["classification"]
    if ctx["master_type"][i] == "button":
        return ("ui_or_derived", ptr(P_MASTER, "/entities/comp.xml/0/fields/%d/type" % i),
                "master type=button: UI action, no stored value (t64 %s)" % cls)
    bucket = COMP64_RULE[cls]
    return (bucket, ptr(P_T64, "/fields/%d/classification" % ctx["c64_idx"][i]), cls)


CLASSIFIERS = {"club": classify_club, "nation": classify_nation, "comp": classify_comp}
def _idx_from_id(rec_id):
    """'E97/club.xml#club/031' -> 31; nation r2 records carry 'xml_index' instead."""
    tail = rec_id.rsplit("/", 1)[-1]
    return int(tail)


def build_ctx():
    schema = load(P_SCHEMA)
    ctx = {}

    t71 = load(P_T71)["fields"]
    ctx["t71"] = t71
    ctx["t71_by_code"] = {f["code"]: k for k, f in enumerate(t71)}

    # ---- club
    cr1 = schema["club_main_row_fields"]
    cr2 = schema["club_main_row_fields_r2"]
    ctx["r1_l3"] = {r["xml_index"]: k for k, r in enumerate(cr1["L3_fields"])}
    ctx["r2_l3"] = {_idx_from_id(r["id"]): k for k, r in enumerate(cr2["new_L3_records"])}
    ctx["r2_held"] = {_idx_from_id(r["id"]): k for k, r in enumerate(cr2["held_records"])}
    ctx["r2um"] = {_idx_from_id(r["id"]): k for k, r in enumerate(cr2["unmapped_records"])}
    ctx["r2"] = {_idx_from_id(r["id"]): r
                 for r in cr2["new_L3_records"] + cr2["held_records"] + cr2["unmapped_records"]}

    tail = load(P_T69)["entries"]
    ctx["tail"] = {e["id"]: k for k, e in enumerate(tail)}

    # club 4CC dispatch reachability, keyed by zero-padded suffix
    proj = load(P_T63)["occurrences"]
    ctx["dispatch"] = {_idx_from_id(o["id"]): k for k, o in enumerate(proj) if o.get("dispatch")}
    ctx["t63_dispatch_total"] = sum(1 for o in proj if o.get("dispatch"))

    # ---- nation
    nr1 = schema["nation_main_row_fields"]
    nr2 = schema["nation_main_row_fields_r2"]
    ctx["n_l3"] = {r["xml_index"]: k for k, r in enumerate(nr1["L3_fields"])}
    ctx["n_r2_held"] = {r["xml_index"]: k for k, r in enumerate(nr2["held_records"])}
    ctx["n_r2um"] = {r["xml_index"]: k for k, r in enumerate(nr2["unmapped_records"])}
    ctx["n_r2"] = {r["xml_index"]: r for r in nr2["held_records"] + nr2["unmapped_records"]}

    # ---- comp
    cr = schema["comp_main_row_fields"]
    ctx["c_l3"] = {r["xml_index"]: k for k, r in enumerate(cr["L3_fields"])}
    ctx["c_held"] = {r["xml_index"]: k for k, r in enumerate(cr["held_records"])}
    c64 = load(P_T64)["fields"]
    ctx["c64"] = {r["xml_index"]: r for r in c64}
    ctx["c64_idx"] = {r["xml_index"]: k for k, r in enumerate(c64)}

    # ---- master types, positional (order verified identical to the census order)
    mf = master_fields()
    ctx["master_type"] = {e: {k: f.get("type") for k, f in enumerate(mf[e])} for e in ENTITIES}

    # ---- t72 slot census
    inv = load(P_T72INV)["tables"]
    ctx["inv"] = inv
    ctx["unnamed_slots"] = {e: sum(1 for s in inv[e]["slots"] if s["kind"] == "unnamed")
                            for e in ENTITIES}
    return ctx


def run_build():
    ctx = build_ctx()
    rows = []
    for o in build_occurrences():
        sub = dict(ctx)
        sub["master_type"] = ctx["master_type"][o["entity"]]
        bucket, ref, note = CLASSIFIERS[o["entity"]](o, sub)
        rows.append({"id": o["id"], "code": o["code"], "entity": o["entity"],
                     "bucket": bucket, "evidence_ref": ref, "note": note})
    return rows


def counts(rows):
    tab = {e: {b: 0 for b in BUCKETS} for e in ENTITIES}
    for r in rows:
        tab[r["entity"]][r["bucket"]] += 1
    return tab


def unnamed_slot_keys():
    inv = load(P_T72INV)["tables"]
    return {e: [(s["position"], s["key"], s["kind"]) for s in inv[e]["slots"] if s["kind"] == "unnamed"]
            for e in ENTITIES}


def write_buckets(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write('{\n "generated_by": "scripts/t78_xml_denominator.py",\n')
        fh.write(' "schema_basis": ["%s", "%s", "%s"],\n' % (P_SCHEMA, P_T71, P_T72INV))
        fh.write(' "count": %d,\n' % len(rows))
        fh.write(' "buckets": %s,\n' % json.dumps(BUCKETS))
        fh.write(' "occurrences": [\n')
        for k, r in enumerate(rows):
            fh.write("  " + json.dumps(r, ensure_ascii=False, sort_keys=True))
            fh.write(",\n" if k < len(rows) - 1 else "\n")
        fh.write(" ]\n}\n")


def write_coverage(rows, path):
    tab = counts(rows)
    total = len(rows)
    lines = []
    lines.append("# t78 — club/nation/comp 1,034 XML occurrence 真实物理覆盖率")
    lines.append("")
    lines.append("分母 = 三主表 XML 顶层 occurrence 共 **%d**(club 433 / nation 346 / comp 255)。" % total)
    lines.append("证据全部来自冻结工件(schema v10 + t71 r3 + t72 inventory + t57/t69 尾账),无新解码、无反汇编。")
    lines.append("")
    lines.append("| entity | " + " | ".join(BUCKETS) + " | Σ |")
    lines.append("|---|" + "---|" * (len(BUCKETS) + 1))
    for e in ENTITIES:
        cells = [str(tab[e][b]) for b in BUCKETS]
        lines.append("| %s | %s | **%d** |" % (e, " | ".join(cells), sum(tab[e].values())))
    cells = [str(sum(tab[e][b] for e in ENTITIES)) for b in BUCKETS]
    lines.append("| Σ | %s | **%d** |" % (" | ".join(cells), total))
    lines.append("")
    phys = sum(tab[e][b] for e in ENTITIES for b in ("mapped_l3", "independent_member", "string_name_table"))
    lines.append("**已落到物理承载(mapped_l3 + independent_member + string_name_table)= %d / %d = %.1f%%**;"
                 % (phys, total, 100.0 * phys / total))
    lines.append("held %d;unresolved_wire_slot %d(有 wire 槽但未命名,t72 已给指纹);no_wire_evidence %d。"
                 % (sum(tab[e]["held"] for e in ENTITIES),
                    sum(tab[e]["unresolved_wire_slot"] for e in ENTITIES),
                    sum(tab[e]["no_wire_evidence"] for e in ENTITIES)))
    lines.append("")
    lines.append("## unresolved_wire_slot 明细(给 t02 定向对照与后续波次排序)")
    lines.append("")
    keys = unnamed_slot_keys()
    for e in ENTITIES:
        n = tab[e]["unresolved_wire_slot"]
        if not n:
            continue
        lines.append("- **%s**:%d 个 occurrence 挂在 %d 个未命名物理槽上:`%s`"
                     % (e, n, len(keys[e]), ", ".join("pos%d/%s" % (p, k) for p, k, _ in keys[e]) or "t72 unnamed 集合"))
    lines.append("")
    lines.append("## 抽样交叉(每桶前 3 条)")
    lines.append("")
    for b in BUCKETS:
        for r in [r for r in rows if r["bucket"] == b][:3]:
            lines.append("- `%s` %s(%s)→ %s" % (r["entity"], r["code"], b, r["evidence_ref"]))
    lines.append("")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


def write_done(rows, path):
    tab = counts(rows)
    phys = sum(tab[e][b] for e in ENTITIES for b in ("mapped_l3", "independent_member", "string_name_table"))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("DONE type=t78 status=complete\n\n")
        fh.write("分母 %d = club 433 + nation 346 + comp 255;已落物理承载 %d(%.1f%%)。"
                 % (len(rows), phys, 100.0 * phys / len(rows)))
        fh.write("deepseek devseek 三轮撞墙,按 E112 先例由指挥官本地修通 write_coverage/write_done 后 build。E116。\n")


def selftest():
    """Recompute the ledger anchors that t77 will inherit as its denominator."""
    rows = run_build()
    fails = []
    tab = counts(rows)
    if len(rows) != 1034:
        fails.append("total %d != 1034" % len(rows))
    for e, want in (("club", 433), ("nation", 346), ("comp", 255)):
        got = sum(tab[e].values())
        if got != want:
            fails.append("%s %d != %d" % (e, got, want))
    anchors = [
        ("club mapped_l3 = 13 r1 + 8 r2 + 24 t71", tab["club"]["mapped_l3"], 45),
        ("club independent_member = t57 skipped 10", tab["club"]["independent_member"], 10),
        ("club held = 18 r2 + 10 r1 remaining", tab["club"]["held"], 28),
        ("club no_wire_evidence = 106 no-dispatch", tab["club"]["no_wire_evidence"], 106),
        ("nation mapped_l3 = E94 5", tab["nation"]["mapped_l3"], 5),
        ("nation no_wire_evidence = E108 318", tab["nation"]["no_wire_evidence"], 318),
        ("comp mapped_l3 = E99 49", tab["comp"]["mapped_l3"], 49),
        ("comp held = E99 10", tab["comp"]["held"], 10),
        ("comp unresolved = t64 bounded_getter 38", tab["comp"]["unresolved_wire_slot"], 38),
        ("comp no_wire = 196-38-13-5", tab["comp"]["no_wire_evidence"], 140),
        ("no bucket is empty-by-accident: mapped_l3 sum",
         sum(tab[e]["mapped_l3"] for e in ENTITIES), 99),
    ]
    for label, got, want in anchors:
        status = "ok" if got == want else "FAIL"
        print("%-52s got=%-5s want=%-5s %s" % (label, got, want, status))
        if got != want:
            fails.append(label)
    # t71 id/code pairs must all exist on the club spine
    ctx = build_ctx()
    spine = {o["xml_index"]: o for o in build_occurrences() if o["entity"] == "club"}
    for f in ctx["t71"]:
        idx = _idx_from_id(f["id"])
        if spine.get(idx, {}).get("code") != f["code"]:
            fails.append("t71 %s does not match club spine %d" % (f["code"], idx))
    # one bucket per occurrence, no duplicates
    if len({r["id"] for r in rows}) != len(rows):
        fails.append("duplicate occurrence id")
    if any(r["bucket"] not in BUCKETS for r in rows):
        fails.append("unknown bucket")
    print("SELFTEST %s (%d checks)" % ("PASS" if not fails else "FAIL", 11 + 1 + 2))
    for f in fails:
        print("  - " + f)
    return 0 if not fails else 1


def main(argv):
    ap = argparse.ArgumentParser(
        prog="t78_xml_denominator.py",
        description="Bucket the 1,034 club/nation/comp XML occurrences onto a physical-coverage "
                    "denominator using frozen artifacts only (no .dat, no disassembly).")
    ap.add_argument("--outdir", default=OUTDIR, help="output directory (default scratch/t78/out)")
    ap.add_argument("--build", action="store_true", help="write buckets.json + coverage.md + DONE.md")
    ap.add_argument("--selftest", action="store_true", help="recompute the ledger anchors and compare")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.build:
        ap.print_help()
        return 2
    rows = run_build()
    write_buckets(rows, os.path.join(args.outdir, "buckets.json"))
    write_coverage(rows, os.path.join(args.outdir, "coverage.md"))
    write_done(rows, os.path.join(args.outdir, "DONE.md"))
    print("wrote %s (3 files, %d occurrences)" % (args.outdir, len(rows)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (KeyError, FileNotFoundError, ValueError) as exc:
        print("FATAL: %r" % (exc,), file=sys.stderr)
        sys.exit(2)
