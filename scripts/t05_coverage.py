#!/usr/bin/env python3
"""t05 覆盖矩阵 — 合并三处知识源,输出全库解析进度(只读输入,只写本工作区)。

知识源:
  1. 本仓 census  scratch/t01/inbox/t01h/output.json   (74 factory type / mode / reader entry)
  2. 上游普查    D:/tmp2b/fm24/reports/dbdat_decode/*   (行边界 / 身份 / entity 分级, 全只读)
  3. 本仓产物    scratch/t01|t02 下的 field map         (已命名偏移)

输出:
  scratch/t05/COVERAGE.json   机读
  scratch/t05/COVERAGE.md     人读报表

用法:
  py -V:3.12 -I -B scripts/t05_coverage.py
  py -V:3.12 -I -B scripts/t05_coverage.py --json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
UPSTREAM = pathlib.Path(r"D:\tmp2b\fm24")
SCHEMA_MD = UPSTREAM / "reports" / "EDITOR_SCHEMA_FIELDS.md"

CLIENT_IDS = [0, 2, 3, 5, 6, 7, 8, 9, 10, 18, 19, 21, 22, 23, 25, 27, 35, 41, 47, 56]

# 32 个数据库实体(其余是 advanced/* 规则树与 enums,不落在 .dat 表里)
DB_ENTITIES = {
    "agent", "agreement", "alternative names", "award", "city", "club b team",
    "club c team", "club d team", "club", "comp", "continent", "contract",
    "currency", "derby", "description", "injury", "journalist", "language",
    "local region", "media source", "nation", "non player", "official",
    "person name", "person", "player", "region", "stadium", "stage name",
    "team kit", "team", "weather",
}

# 本仓(fm24-db)已独立闭合边界的表 —— (archive, tid) -> 等式
FMDB_CLOSED = {
    ("client", 0): "14+3545*77+8=272987",
    ("client", 2): "14+56293*43+8=2420621",
    ("client", 3): "84,259 行全封口(5B block + 3 特例行)",
    ("client", 5): "14+7*34+8=260",
    ("client", 6): "14+115*16+8=1862",
    ("client", 7): "208 行变长全封口",
    ("client", 8): "126 行语言名全封口",
    ("client", 9): "251 行 sentinel+duni 尾锚全封口",
    ("client", 10): "14+24710+8=24732 (4 段计数循环)",
    ("client", 18): "1567 行双字符串全封口",
    ("client", 19): "14+28*45+8=1282",
    ("client", 21): "14+48413*38+8=1839716",
    ("client", 22): "14+449*13+8=5859",
    ("client", 23): "14+278*14+8=3914",
    ("client", 25): "comp 行边界",
    ("client", 27): "334 行变长全封口",
    ("client", 35): "14+890*15+8=13372",
    ("client", 41): "173 行变长全封口",
    ("client", 47): "14+Σ(41+5k)+8=109505 (2488行, rdui/duni 双验)",
    ("client", 56): "14+6*13+8=100",
    ("server", 3): "84,259 行全封口",
    ("server", 19): "14+28*46+8=1310",
}

# schema 实体名 -> (code, 声明字段数) 由正则从 EDITOR_SCHEMA_FIELDS.md 现取,这里只留别名映射
ENTITY_ALIAS = {
    "award": "award", "injury": "injury", "language": "language", "nation": "nation",
    "currency": "currency", "city": "city", "stadium": "stadium", "club": "club",
    "competition": "comp", "comp": "comp", "team": "team", "weather": "weather",
    "continent": "continent", "region": "region", "local region": "local region",
    "media source": "media source", "derby": "derby", "stage name": "stage name",
    "agreement": "agreement", "person": "person", "player": "player",
    "non player": "non player", "official": "official", "agent": "agent",
}


def parse_schema() -> dict[str, dict]:
    """从 EDITOR_SCHEMA_FIELDS.md 解析每个实体的字段序列与规模。"""
    text = SCHEMA_MD.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    pat = re.compile(r"### (.+?)（记录标识 `([A-Za-z0-9]+)`，(\d+) 个字段）(.*?)(?=\n### )", re.S)
    for m in pat.finditer(text):
        name, code, declared, body = m.group(1).strip(), m.group(2), int(m.group(3)), m.group(4)
        fields: list[dict] = []
        for line in body.splitlines():
            if not line.startswith("|") or line.startswith("| 字段代码") or line.startswith("|---"):
                continue
            sub = ("\u3000" in line[:8]) or ("↳" in line)
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 3:
                continue
            fc = cells[0].strip("`").strip()
            if not fc or fc.startswith("↳"):
                continue
            fields.append({"field": fc, "type": cells[2], "sub": sub})
        top = [f for f in fields if not f["sub"]]
        top_lists = [f for f in top if "list" in f["type"]]
        out[name] = {
            "code": code,
            "declared_fields": declared,
            "top_level": len(top),
            "top_lists": len(top_lists),
            "scalars": len(top) - len(top_lists),
            "fields": top,
        }
    return out


def load_json(p: pathlib.Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def norm_boundary(obj) -> tuple[str, str]:
    """归一行边界描述 -> (closed|candidate|open|empty|unknown, 等式/模型)。"""
    if not isinstance(obj, dict):
        return ("unknown", "")
    st = str(obj.get("status") or obj.get("model") or "")
    eq = str(obj.get("equation") or obj.get("formula") or obj.get("closure") or st)
    if "empty" in st:
        return ("empty", eq)
    if "unresolved" in st or "unknown" in st or "nonstandard" in st or "variable" in st:
        return ("open", eq)
    if "arithmetic_candidate" in st or "candidate" in st:
        return ("candidate", eq)          # 算术成立但身份未验,不等于已闭合
    if "exact" in st or "fixed_stride" in st or "closed" in st or "fully_consumed" in st:
        return ("closed", eq)
    return ("other", eq)


def boundary_from_model(model: str | None, ident) -> tuple[str, str]:
    m = str(model or "")
    if "fixed" in m:
        s = ""
        if isinstance(ident, dict):
            s = str(ident.get("equation") or ident.get("closure") or "")
        return ("closed", s or m)
    if "variable" in m:
        return ("open", m)
    return ("unknown", m)


def _iter_entries(v):
    """把 row_offset_map / field_offsets / named / fields 统一拆成条目列表。"""
    if isinstance(v, dict):
        for kk, vv in v.items():
            if isinstance(vv, dict):
                yield kk, vv
            else:
                yield kk, {"value": vv}
    elif isinstance(v, list):
        for e in v:
            if isinstance(e, dict):
                yield None, e


def collect_named_fields():
    """扫描本仓产物 -> (schema 字段名集合, 已描述偏移集合, 来源)。"""
    patterns = [
        "scratch/t02/*_reference.json",
        "scratch/t02/*_partial.json",
        "scratch/t01/inbox/*/output.json",
        "scratch/t02/inbox/*/output.json",
        "scratch/t02/inbox/*/framework.json",
        "scratch/t02/inbox/*/OUTBOX/framework.json",
        "scratch/t02/inbox/*/fw*.json",
        "scratch/t05/*/output.json",
        "scratch/t05/*/club_fields.json",
        "scratch/t05/*/attrs.json",
        "scratch/t05/*/team.json",
        "scratch/t05/*/comp.json",
        "scratch/t05/*/boundaries.json",
    ]
    named: dict[int, set[str]] = {}
    offsets: dict[int, set[str]] = {}
    sources: dict[int, list[str]] = {}
    seen_paths = set()
    for pat in patterns:
        for p in sorted(ROOT.glob(pat)):
            if p in seen_paths:
                continue
            seen_paths.add(p)
            d = load_json(p)
            if not isinstance(d, dict):
                continue
            tid = d.get("type_id", d.get("table_id"))
            if not isinstance(tid, int):
                continue
            got_n: set[str] = set()
            got_o: set[str] = set()

            def feed(container, nesting=0):
                for key, ent in _iter_entries(container):
                    f = ent.get("field") or ent.get("code") or (key if key and re.fullmatch(r"[A-Za-z0-9]{4}", str(key)) else None)
                    if f:
                        got_n.add(str(f))
                    ro = ent.get("row_off", ent.get("row_offset", ent.get("offset")))
                    if ro is None:
                        ro = ent.get("idx")
                    if ro is not None:
                        got_o.add(str(ro))
                    if nesting == 0:
                        # class_fields: {class: [entries]}
                        for sub in ("fields", "named"):
                            sv = ent.get(sub)
                            if isinstance(sv, list):
                                feed(sv, 1)

            for key in ("row_offset_map", "field_offsets", "named", "fields", "slots", "named_anchors"):
                v = d.get(key)
                if v is not None:
                    feed(v)
            cf = d.get("class_fields")
            if isinstance(cf, dict):
                for arr in cf.values():
                    if isinstance(arr, list):
                        feed(arr)
            if got_n or got_o:
                if got_n:
                    named.setdefault(tid, set()).update(got_n)
                if got_o:
                    offsets.setdefault(tid, set()).update(got_o)
                sources.setdefault(tid, []).append(str(p.relative_to(ROOT)))
    return named, offsets, sources


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    schema = parse_schema()
    schema_all = len(schema)
    schema = {k: v for k, v in schema.items() if k in DB_ENTITIES}
    census = load_json(ROOT / "scratch/t01/inbox/t01h/output.json") or {}
    three_way = load_json(ROOT / "scratch/t01/stage2_three_way.json") or {}
    field_count = {r.get("table_type"): r.get("field_count", 0) for r in three_way.get("rows", [])}

    # census: type_id -> info
    cinfo: dict[int, dict] = {}
    for it in census.get("census", []):
        tid = it.get("type_id")
        if not isinstance(tid, int):
            continue
        ent = it.get("entity", {}) or {}
        cands = ent.get("matched") or ent.get("candidates") or []
        rd = it.get("reader", {}) or {}
        s19 = (rd.get("slot19_readers") or [{}])[0] if rd.get("slot19_readers") else {}
        cinfo[tid] = {
            "census_entity": (cands[0] if cands else None),
            "mode": rd.get("mode"),
            "reader_entry": s19.get("entry_file_offset") if isinstance(s19, dict) else None,
            "schema_field_count": field_count.get(tid, 0),
        }

    # 上游 client 小表 / 大表
    up_small = (load_json(UPSTREAM / "reports/dbdat_decode/db_tables_small.json") or {}).get("tables") or {}
    up_big = (load_json(UPSTREAM / "reports/dbdat_decode/db_tables_big.json") or {}).get("tables") or {}
    up_server = (load_json(UPSTREAM / "reports/dbdat_decode/server_tables_census.json") or {}).get("entries") or []

    upstream: dict[tuple[str, int], dict] = {}
    for k, it in (up_small.items() if isinstance(up_small, dict) else []):
        tid = it.get("table_id", k)
        if not isinstance(tid, int):
            continue
        st, eq = norm_boundary(it.get("row_boundary"))
        em = it.get("entity_mapping") or {}
        upstream[("client", tid)] = {
            "count": it.get("record_count"),
            "payload": it.get("payload_size"),
            "boundary": st, "equation": eq,
            "entity": em.get("entity") if isinstance(em, dict) else None,
            "entity_tier": em.get("status") if isinstance(em, dict) else None,
        }
    for k, it in (up_big.items() if isinstance(up_big, dict) else []):
        tid = it.get("table_id", k)
        if not isinstance(tid, int):
            continue
        st, eq = boundary_from_model(it.get("model"), it.get("identity_validation"))
        upstream[("client", tid)] = {
            "count": (it.get("identity_validation") or {}).get("count") if isinstance(it.get("identity_validation"), dict) else None,
            "payload": it.get("payload_size"),
            "boundary": st, "equation": eq,
            "entity": it.get("entity"),
            "entity_tier": it.get("evidence_level"),
        }
    for it in up_server:
        if it.get("entry_type") != "table":
            continue
        tid = it.get("table_id")
        if not isinstance(tid, int):
            continue
        st, eq = norm_boundary(it.get("row_boundary"))
        em = it.get("entity_mapping") or {}
        upstream[("server", tid)] = {
            "count": it.get("record_count_header"),
            "payload": it.get("payload_size"),
            "boundary": st, "equation": eq,
            "entity": em.get("entity") if isinstance(em, dict) else None,
            "entity_tier": em.get("tier") if isinstance(em, dict) else None,
            "model": it.get("row_model"),
        }

    named, offsets, named_src = collect_named_fields()

    rows = []
    # client 20
    for tid in CLIENT_IDS:
        ci = cinfo.get(tid, {})
        up = upstream.get(("client", tid), {})
        rows.append({
            "archive": "client", "table_id": tid,
            "entity": up.get("entity") or ci.get("census_entity"),
            "entity_tier": up.get("entity_tier"),
            "mode": ci.get("mode"),
            "count": up.get("count"),
            "payload": up.get("payload"),
            "boundary": up.get("boundary", "unknown"),
            "equation": up.get("equation", ""),
            "named": len(named.get(tid, ())),
            "offsets": len(offsets.get(tid, ())),
        })
    # server 59
    for tid in sorted(k[1] for k in upstream if k[0] == "server"):
        up = upstream[("server", tid)]
        ci = cinfo.get(tid, {})
        rows.append({
            "archive": "server", "table_id": tid,
            "entity": up.get("entity"),
            "entity_tier": up.get("entity_tier"),
            "mode": ci.get("mode") or up.get("model"),
            "count": up.get("count"),
            "payload": up.get("payload"),
            "boundary": up.get("boundary", "unknown"),
            "equation": up.get("equation", ""),
            "named": len(named.get(tid, ())),
            "offsets": len(offsets.get(tid, ())),
        })

    def scalar_budget(entity_name: str | None) -> int | None:
        if not entity_name:
            return None
        key = ENTITY_ALIAS.get(str(entity_name).strip().lower())
        if key and key in schema:
            return schema[key]["scalars"]
        return None

    # 合并本仓独立闭合结论: 任一来源闭合即视为闭合
    for r in rows:
        key = (r["archive"], r["table_id"])
        r["upstream_boundary"] = r["boundary"]
        r["fmdb_closed"] = key in FMDB_CLOSED
        r["fmdb_equation"] = FMDB_CLOSED.get(key, "")
        if r["boundary"] == "closed" or key in FMDB_CLOSED:
            r["effective"] = "closed"
        else:
            r["effective"] = r["boundary"]

    for r in rows:
        r["scalar_budget"] = scalar_budget(r["entity"])

    client_rows = [r for r in rows if r["archive"] == "client"]
    server_rows = [r for r in rows if r["archive"] == "server"]
    client_closed = sum(1 for r in client_rows if r["effective"] == "closed")
    server_closed = sum(1 for r in server_rows if r["effective"] == "closed")
    server_cand = sum(1 for r in server_rows if r["effective"] == "candidate")
    server_open = sum(1 for r in server_rows if r["effective"] in ("open", "unknown", "other"))
    client_named = sum(r["named"] for r in client_rows)
    server_named = sum(r["named"] for r in server_rows)
    client_offs = sum(r["offsets"] for r in client_rows)
    server_offs = sum(r["offsets"] for r in server_rows)
    # 字段映射是"按实体"的(tid 在 client/server 都有同名表),合计时按实体去重
    entity_named = sum(len(v) for v in named.values())
    entity_offs = sum(len(v) for v in offsets.values())
    budget_total = sum(r["scalar_budget"] or 0 for r in rows)

    summary = {
        "client_tables": len(client_rows),
        "client_boundary_closed": client_closed,
        "server_tables": len(server_rows),
        "server_boundary_closed": server_closed,
        "server_boundary_candidate": server_cand,
        "server_boundary_open": server_open,
        "schema_named_fields_client": client_named,
        "schema_named_fields_server": server_named,
        "schema_named_fields_total": client_named + server_named,
        "schema_named_fields_entity_dedup": entity_named,
        "described_offsets_client": client_offs,
        "described_offsets_server": server_offs,
        "described_offsets_total": client_offs + server_offs,
        "described_offsets_entity_dedup": entity_offs,
        "scalar_budget_known_entities": budget_total,
        "schema_entities_all": schema_all,
        "schema_entities_db": len(schema),
        "schema_declared_fields_total": sum(v["declared_fields"] for v in schema.values()),
        "schema_scalars_total": sum(v["scalars"] for v in schema.values()),
        "schema_top_lists_total": sum(v["top_lists"] for v in schema.values()),
    }

    out = {"summary": summary, "tables": rows,
           "schema": {k: {kk: vv for kk, vv in v.items() if kk != "fields"} for k, v in schema.items()},
           "named_sources": {str(k): v for k, v in named_src.items()}}

    (ROOT / "scratch/t05").mkdir(parents=True, exist_ok=True)
    (ROOT / "scratch/t05/COVERAGE.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = ["# 全库解析覆盖矩阵", "",
             f"生成:{__import__('datetime').datetime.now():%Y-%m-%d %H:%M}", "",
             "## 总览", "",
             "| 指标 | 数值 |", "|---|---|",
             f"| client 表边界闭合 | **{client_closed}/{len(client_rows)}** |",
             f"| server 表边界闭合 | **{server_closed}/{len(server_rows)}**(另有 {server_cand} 张算术候选、{server_open} 张未解) |",
             f"| 已描述行内偏移(按实体去重) | **{entity_offs}** |",
             f"| 其中有 schema 字段码 | {entity_named} |",
             f"| 数据库实体数 | {summary['schema_entities_db']}(全文档 {schema_all}) |",
             f"| 实体声明字段总数 | {summary['schema_declared_fields_total']} |",
             f"| 实体顶层列表字段 | {summary['schema_top_lists_total']} |",
             f"| **实体顶层标量(真正可落偏移)** | **{summary['schema_scalars_total']}** |",
             f"| 已映射实体标量预算合计 | {budget_total} |",
             f"| 字段映射进度(粗) | {entity_offs}/{summary['schema_scalars_total']} = {entity_offs*100.0/max(1,summary['schema_scalars_total']):.1f}% |",
             "",
             "> 注:字段映射按实体(tid)计,client/server 同名表的行内布局可能不同;",
             "> 表中 client/server 两栏的偏移数是同一实体结论的复用,不是两套独立成果。",
             "",
             "## client 20 表", "",
             "| tid | entity | mode | count | 边界 | 上游 | 偏移 | 命名字段 | 标量预算 | 等式 |",
             "|---:|---|---|---:|---|---|---:|---:|---:|---|"]
    for r in client_rows:
        lines.append("| %d | %s | %s | %s | %s | %s | %d | %d | %s | %s |" % (
            r["table_id"], r["entity"] or "?", r["mode"] or "?", r["count"] or "?",
            r["effective"], r["upstream_boundary"], r["offsets"], r["named"], r["scalar_budget"] or "-",
            (r["fmdb_equation"] or r["equation"] or "")[:38]))
    lines += ["", "## server 59 表", "",
              "| tid | entity | model | count | 边界 | 上游 | 偏移 | 命名字段 | 标量预算 |",
              "|---:|---|---|---:|---|---|---:|---:|---:|"]
    for r in server_rows:
        lines.append("| %d | %s | %s | %s | %s | %s | %d | %d | %s |" % (
            r["table_id"], r["entity"] or "?", (r["mode"] or "?")[:22], r["count"] or "?",
            r["effective"], r["upstream_boundary"], r["offsets"], r["named"], r["scalar_budget"] or "-"))
    lines += ["", "## 未闭合清单", ""]
    for r in rows:
        if r["effective"] != "closed":
            lines.append("- %s table_%d: **%s**(上游 %s) %s" % (
                r["archive"], r["table_id"], r["effective"], r["upstream_boundary"],
                (r["equation"] or "")[:60]))
    (ROOT / "scratch/t05/COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        print("\nwrote scratch/t05/COVERAGE.{json,md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
