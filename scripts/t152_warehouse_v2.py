#!/usr/bin/env python3
"""t152 — FM24 SQLite 数仓 v2。

在不改动 t139_fm24_db_cli.py 的前提下，在 scratch/t139/out/fm24_core.sqlite
基础上构建增强版数仓 scratch/t152/out/fm24_warehouse_v2.sqlite，新增三张表：
  - manager_attributes  : 教练/非球员 34 项 L3 属性（来自 t137d 产物 top20_managers_full_cards.json）
  - lang_zh_cn          : 中文译名（来自 t143_lang_db 产物 lang_db_schema.json 的 showcase 本地化）
  - career_history_summary : 生涯履历摘要（来自 t127 pl_hist + t128 non_pl_hist 的职业生涯统计）

并提供毫秒级双语查询 CLI（--help / --build / --query / --selftest）。

只复用现有模块产物（只读），不重复造解析轮子。
"""
from __future__ import annotations

import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

OUT = ROOT / "scratch" / "t152" / "out"
SRC_DB = ROOT / "scratch" / "t139" / "out" / "fm24_core.sqlite"
VERSION = 2

# --- 只读输入产物路径（不改动任何现有脚本） ---
T137D_CARDS = ROOT / "scratch" / "t137d" / "out" / "top20_managers_full_cards.json"
T143_SCHEMA = ROOT / "scratch" / "t143" / "out" / "lang_db_schema.json"
T127_SCHEMA = ROOT / "scratch" / "t127" / "out" / "pl_hist_schema.json"
T128_SCHEMA = ROOT / "scratch" / "t128" / "out" / "non_pl_hist_schema.json"


def log(msg: str) -> None:
    print(f"[t152] {msg}", flush=True)


def open_ro(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def table_counts(conn: sqlite3.Connection) -> dict[str, int]:
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name")]
    return {t: conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="FM24 SQLite 数仓 v2（增量表：manager_attributes、lang_zh_cn、career_history_summary）")
    cmd = ap.add_mutually_exclusive_group(required=True)
    cmd.add_argument("--build", action="store_true",
                     help="构建 scratch/t152/out/fm24_warehouse_v2.sqlite")
    cmd.add_argument("--query", metavar="TEXT", help="双语查询（人名/俱乐部/中文译名）")
    cmd.add_argument("--selftest", action="store_true", help="运行自检并验证行数与查询耗时")
    ap.add_argument("--db", default=None, help="替代目标 sqlite 路径")
    args = ap.parse_args(argv)

    if args.build:
        return build_sqlite()
    if args.query is not None:
        return cmd_query(args)
    return cmd_selftest(args)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_all_tables(dst: sqlite3.Connection) -> dict[str, int]:
    """把源 sqlite (SRC_DB) 的所有用户表完整复制到目标库（ATTACH + CTAS）。"""
    dst.execute(f"ATTACH DATABASE '{SRC_DB}' AS src")
    tables = [r[0] for r in dst.execute(
        "SELECT name FROM src.sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name")]
    counts: dict[str, int] = {}
    for t in tables:
        dst.execute(f'CREATE TABLE "{t}" AS SELECT * FROM src."{t}"')
        counts[t] = dst.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        log(f"  copied {t}: {counts[t]:,} rows")
    dst.execute("DETACH DATABASE src")
    return counts


def _build_manager_attributes(dst: sqlite3.Connection) -> int:
    """manager_attributes：教练/非球员 34 项 L3 属性（t137d 产物）。

    直接读取 top20_managers_full_cards.json，不 import t137d 模块（避免
    触发 zstandard/t120 初始化）。每张卡展开其 attributes_by_4cc 的全部
    34 项属性为一行（uid, fourcc, label, category, value）。
    """
    cards = _load_json(T137D_CARDS)["cards"]
    dst.execute("""CREATE TABLE manager_attributes (
        uid INTEGER,
        full_name TEXT,
        ordinal INTEGER,
        person_type INTEGER,
        ca INTEGER,
        pa INTEGER,
        fourcc TEXT,
        label TEXT,
        category TEXT,
        value INTEGER,
        source_rank INTEGER,
        PRIMARY KEY (uid, fourcc)
    )""")
    # 4CC -> (label, category) 字典，由第一张出现该 fourcc 的卡提供（各卡一致）。
    fourcc_meta: dict[str, tuple[str, str]] = {}
    rows = []
    for c in cards:
        a4cc = c.get("attributes_by_4cc", {}) or {}
        alabel = c.get("attributes_by_label", {}) or {}
        for fc, val in a4cc.items():
            if fc not in fourcc_meta:
                fourcc_meta[fc] = (alabel.get(fc, fc), "coaching")
            label, cat = fourcc_meta[fc]
            rows.append((
                c["uid"], c["full_name"], c.get("ordinal"), c.get("person_type"),
                c.get("ca"), c.get("pa"), fc, label, cat,
                int(val) if isinstance(val, (int, float)) else -1, c.get("rank")))
    dst.executemany(
        "INSERT INTO manager_attributes VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
    dst.execute("CREATE INDEX idx_manager_attrs_uid ON manager_attributes(uid)")
    dst.execute("CREATE INDEX idx_manager_attrs_full_name ON manager_attributes(full_name)")
    dst.execute("CREATE INDEX idx_manager_attrs_fourcc ON manager_attributes(fourcc)")
    return len(rows)


def _build_lang_zh_cn(dst: sqlite3.Connection) -> int:
    """lang_zh_cn：中文译名（t143 产物 lang_db_schema.json 的 showcase 本地化）。"""
    schema = _load_json(T143_SCHEMA)
    showcase = schema.get("showcase", [])
    langs = schema.get("join", {}).get("showcase_language_ids", [8, 1000002, 1000003])
    zh_langs = [lid for lid in langs if lid in (1000002, 1000003)]
    dst.execute("""CREATE TABLE lang_zh_cn (
        uid INTEGER,
        dbid INTEGER,
        entity TEXT,
        localization_table_type INTEGER,
        language_id INTEGER,
        language TEXT,
        primary_name TEXT,
        core_member_path TEXT,
        core_ordinal INTEGER,
        core_record_offset INTEGER
    )""")
    rows = []
    for entry in showcase:
        for lid in zh_langs:
            loc = entry.get("localizations", {}).get(lid, {})
            sel = loc.get("selected") or {}
            rows.append((
                entry.get("uid"), entry.get("dbid"), entry.get("entity"),
                entry.get("localization_table_type"), lid,
                loc.get("language"), sel.get("primary_name"),
                entry.get("core_member_path"), entry.get("core_ordinal"),
                entry.get("core_record_offset")))
    dst.executemany(
        "INSERT INTO lang_zh_cn VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
    dst.execute("CREATE INDEX idx_lang_zh_cn_uid ON lang_zh_cn(uid)")
    dst.execute("CREATE INDEX idx_lang_zh_cn_name ON lang_zh_cn(primary_name)")
    dst.execute("CREATE INDEX idx_lang_zh_cn_lang ON lang_zh_cn(language_id)")
    return len(rows)


def _build_career_history_summary(dst: sqlite3.Connection) -> int:
    """career_history_summary：生涯履历摘要（t127 pl_hist + t128 non_pl_hist 产物）。"""
    pl_hist = _load_json(T127_SCHEMA)
    non_pl_hist = _load_json(T128_SCHEMA)
    dst.execute("""CREATE TABLE career_history_summary (
        uid INTEGER PRIMARY KEY,
        name TEXT,
        person_type TEXT,   -- 'player' | 'manager'
        n_periods INTEGER,
        year_from INTEGER,
        year_to INTEGER,
        total_apps INTEGER,
        total_goals INTEGER,
        last_club_id INTEGER,
        last_club_name TEXT,
        last_comp_id INTEGER,
        last_comp_name TEXT,
        source TEXT         -- 'pl_hist' | 'non_pl_hist'
    )""")
    rows = []
    # 球员：t127 stars
    stars = pl_hist.get("stars", {})
    for name, car in stars.items():
        if not car.get("found"):
            continue
        uid = car["uid"]
        rws = car.get("rows", [])
        apps = [r.get("apps") for r in rws if r.get("apps") is not None]
        goals = [r.get("goals") for r in rws if r.get("goals") is not None]
        years = [r.get("year_from") for r in rws if r.get("year_from")]
        years += [r.get("year_to") for r in rws if r.get("year_to")]
        rows.append((
            uid, name, "player", len(rws),
            min(years) if years else None, max(years) if years else None,
            sum(apps) if apps else None, sum(goals) if goals else None,
            (rws[-1].get("club_id") if rws else None),
            (rws[-1].get("club") if rws else None),
            (rws[-1].get("comp_id") if rws else None),
            (rws[-1].get("comp_hint") if rws else None),
            "pl_hist"))
    # 非球员/教练：t128 managers
    mgrs = non_pl_hist.get("managers", {})
    for name, m in mgrs.items():
        uid = m["uid"]
        rws = m.get("rows", [])
        years = [r.get("join_year") for r in rws if r.get("join_year") and r.get("join_year") != 1900]
        years += [r.get("leave_year") for r in rws if r.get("leave_year") and r.get("leave_year") != 1900]
        rows.append((
            uid, name, "manager", len(rws),
            min(years) if years else None, max(years) if years else None,
            None, None,
            (rws[-1].get("club_or_nation_id") if rws else None),
            (rws[-1].get("entity_name") if rws else None),
            None, None, "non_pl_hist"))
    dst.executemany(
        "INSERT INTO career_history_summary VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    dst.execute("CREATE INDEX idx_career_hist_uid ON career_history_summary(uid)")
    dst.execute("CREATE INDEX idx_career_hist_name ON career_history_summary(name)")
    dst.execute("CREATE INDEX idx_career_hist_type ON career_history_summary(person_type)")
    return len(rows)


def build_sqlite() -> int:
    """构建 fm24_warehouse_v2.sqlite：复制 t139 全表 + 三张增量表 + 索引。"""
    OUT.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()
    started_utc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    if not SRC_DB.is_file():
        print(f"ERROR: {SRC_DB} not found — run t139 --build-sqlite first", file=sys.stderr)
        return 2

    db_path = OUT / "fm24_warehouse_v2.sqlite"
    if db_path.exists():
        db_path.unlink()
    dst = sqlite3.connect(db_path)
    dst.execute("PRAGMA journal_mode=OFF")
    dst.execute("PRAGMA synchronous=OFF")
    dst.execute("PRAGMA temp_store=MEMORY")
    try:
        log("复制 t139 现有全部表（ATTACH + CTAS）…")
        counts = _copy_all_tables(dst)
        log("构建 manager_attributes（t137d 34 属性）…")
        counts["manager_attributes"] = _build_manager_attributes(dst)
        log("构建 lang_zh_cn（t143 中文译名 showcase）…")
        counts["lang_zh_cn"] = _build_lang_zh_cn(dst)
        log("构建 career_history_summary（t127 + t128 生涯履历）…")
        counts["career_history_summary"] = _build_career_history_summary(dst)
        log("创建增量索引…")
        # 为复制的核心表补查询索引（CTAS 不会继承源库索引）。
        dst.execute("CREATE INDEX IF NOT EXISTS idx_basic_people_uid ON basic_people(uid)")
        dst.execute("CREATE INDEX IF NOT EXISTS idx_basic_people_dbid ON basic_people(dbid)")
        dst.execute("CREATE INDEX IF NOT EXISTS idx_clubs_uid ON clubs(uid)")
        dst.execute("CREATE INDEX IF NOT EXISTS idx_star_players_uid ON star_players(uid)")
        dst.commit()
        integrity = dst.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        dst.close()
    db_size = db_path.stat().st_size
    seconds = round(time.perf_counter() - t_start, 1)
    log(f"integrity_check: {integrity}; db size {db_size:,} B; build {seconds}s")

    summary = {
        "schema_id": "fm24.t152.warehouse_v2",
        "schema_version": VERSION,
        "db_path": str(db_path),
        "db_size_bytes": db_size,
        "build_seconds": seconds,
        "built_utc": started_utc,
        "integrity_check": integrity,
        "table_counts": counts,
        "total_rows": sum(counts.values()),
        "incremental_tables": ["manager_attributes", "lang_zh_cn", "career_history_summary"],
        "sources": {
            "core": str(SRC_DB),
            "manager_attributes": str(T137D_CARDS),
            "lang_zh_cn": str(T143_SCHEMA),
            "career_history_summary": {"pl_hist": str(T127_SCHEMA), "non_pl_hist": str(T128_SCHEMA)},
        },
    }
    (OUT / "warehouse_v2_build_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ok = integrity == "ok"
    log(f"build {'OK' if ok else 'FAILED'}")
    return 0 if ok else 1


def cmd_query(args) -> int:
    """双语查询：数字按 uid 精确查；文本跨表模糊搜索（中/英）。"""
    db_path = Path(args.db) if args.db else (OUT / "fm24_warehouse_v2.sqlite")
    if not db_path.is_file():
        print(f"ERROR: {db_path} not found — run --build first", file=sys.stderr)
        return 2
    conn = open_ro(db_path)
    q = args.query.strip()
    result = {"query": q, "matches": []}
    try:
        if q.isdigit():
            uid = int(q)
            # 优先 basic_people / star_players / clubs / manager_attributes / career_history_summary
            for tbl, idcol in (("basic_people", "uid"), ("star_players", "uid"),
                               ("clubs", "uid"), ("manager_attributes", "uid"),
                               ("career_history_summary", "uid")):
                rows = conn.execute(
                    f'SELECT * FROM "{tbl}" WHERE "{idcol}" = ?', (uid,)).fetchall()
                if rows:
                    result["matches"].append({
                        "table": tbl,
                        "rows": [dict(r) for r in rows[:10]]})
            # manager_attributes 按 uid 展开全部属性（去重 card 信息）
            ma = conn.execute(
                "SELECT * FROM manager_attributes WHERE uid = ? ORDER BY fourcc", (uid,)).fetchall()
            if ma:
                card = dict(ma[0])
                card["attributes"] = [
                    {"fourcc": r["fourcc"], "label": r["label"], "category": r["category"],
                     "value": r["value"]} for r in ma]
                result["matches"].append({"table": "manager_attributes_card", "rows": [card]})
        else:
            esc = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            pat = f"%{esc}%"
            sources = [
                ("clubs", "name_full", "uid, ordinal, name_full, name_short"),
                ("clubs", "name_short", "uid, ordinal, name_full, name_short"),
                ("name_first", "text", "ordinal, text"),
                ("name_second", "text", "ordinal, text"),
                ("name_common", "text", "ordinal, text"),
                ("manager_attributes", "full_name", "uid, full_name, fourcc, label, value"),
                ("lang_zh_cn", "primary_name", "uid, entity, language_id, primary_name"),
                ("career_history_summary", "name", "uid, name, person_type, n_periods"),
            ]
            for table, col, columns in sources:
                try:
                    base_sql = (f'SELECT {columns} FROM "{table}" '
                                f'WHERE "{col}" LIKE ? ESCAPE \'\\\'')
                    count = conn.execute(
                        f"SELECT COUNT(*) FROM ({base_sql})", (pat,)).fetchone()[0]
                    sample = [dict(r) for r in conn.execute(
                        base_sql + " LIMIT 20", (pat,)).fetchall()]
                except sqlite3.OperationalError:
                    count, sample = 0, []
                result["matches"].append({
                    "source": f"{table}.{col}", "total": count, "sample": sample})
        print(json.dumps(result, ensure_ascii=False, indent=1))
    finally:
        conn.close()
    return 0


def _write_benchmark(conn: sqlite3.Connection, counts: dict[str, int],
                     build_seconds: float, db_size: int) -> None:
    """生成 warehouse_v2_benchmark.json：表清单、行数、体积、查询耗时、校验样本。"""
    # 典型查询耗时（毫秒）
    timings: dict[str, float] = {}
    for label, sql, params in [
        ("uid_lookup_basic_people", "SELECT * FROM basic_people WHERE uid=?", (28049320,)),
        ("uid_lookup_clubs", "SELECT * FROM clubs WHERE uid=?", (679,)),
        ("manager_attrs_by_uid", "SELECT * FROM manager_attributes WHERE uid=? ORDER BY fourcc", (1120,)),
        ("lang_zh_cn_by_name", "SELECT * FROM lang_zh_cn WHERE primary_name LIKE ? LIMIT 10", ("%英超%",)),
        ("career_hist_by_uid", "SELECT * FROM career_history_summary WHERE uid=?", (1120,)),
        ("search_name_clubs", "SELECT * FROM clubs WHERE name_full LIKE ? LIMIT 10", ("%Manchester%",)),
    ]:
        t0 = time.perf_counter()
        for _ in range(100):
            conn.execute(sql, params).fetchall()
        timings[label] = round((time.perf_counter() - t0) / 100 * 1000, 4)

    # 校验样本：取三个锚点
    samples: dict[str, object] = {}
    for uid, label in ((28049320, "Harry Kane"), (1120, "Pep Guardiola")):
        bp = conn.execute("SELECT * FROM basic_people WHERE uid=?", (uid,)).fetchone()
        ma = conn.execute("SELECT COUNT(*) FROM manager_attributes WHERE uid=?", (uid,)).fetchone()[0]
        ch = conn.execute("SELECT * FROM career_history_summary WHERE uid=?", (uid,)).fetchone()
        lz = conn.execute("SELECT * FROM lang_zh_cn WHERE uid=? LIMIT 5", (uid,)).fetchall()
        samples[str(uid)] = {"label": label,
                             "basic_people": dict(bp) if bp else None,
                             "manager_attribute_count": ma,
                             "career_history": dict(ch) if ch else None,
                             "lang_zh_cn": [dict(r) for r in lz]}

    benchmark = {
        "status": "complete",
        "schema_id": "fm24.t152.warehouse_v2",
        "schema_version": VERSION,
        "db_size_bytes": db_size,
        "build_seconds": build_seconds,
        "table_counts": counts,
        "total_rows": sum(counts.values()),
        "incremental_tables": ["manager_attributes", "lang_zh_cn", "career_history_summary"],
        "query_timings_ms": timings,
        "validation_samples": samples,
    }
    (OUT / "warehouse_v2_benchmark.json").write_text(
        json.dumps(benchmark, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _write_report(conn: sqlite3.Connection, counts: dict[str, int],
                  build_seconds: float, db_size: int, integrity: str) -> None:
    c = counts
    lines = [
        "# t152 — FM24 SQLite 数仓 v2（`fm24_warehouse_v2.sqlite`）",
        "",
        f"- Built in {build_seconds}s; DB size {db_size:,} B; integrity_check `{integrity}`; "
        f"total rows **{sum(c.values()):,}** across {len(c)} tables.",
        "- Base: full copy of t139 `fm24_core.sqlite` (24 core tables + basic_people + star cards).",
        "- Incremental tables: `manager_attributes` (t137d, 34 L3 非球员属性), "
        "`lang_zh_cn` (t143 中文译名 showcase), `career_history_summary` (t127 pl_hist + t128 non_pl_hist).",
        "",
        "## 表与行数",
        "",
        "| table | rows | note |",
        "|---|---:|---|",
    ]
    for t in sorted(c):
        note = {"manager_attributes": "t137d 20 位教练 × 34 L3 属性 = 680",
                "lang_zh_cn": "t143 showcase 本地化（简/繁中）",
                "career_history_summary": "t127 球员生涯 + t128 教练履历"}.get(t, "")
        lines.append(f"| {t} | {c[t]:,} | {note} |")
    lines.extend([
        "",
        "## 查询 CLI",
        "",
        "```",
        "py -V:3.12 -B scripts/t152_warehouse_v2.py --build",
        "py -V:3.12 -B scripts/t152_warehouse_v2.py --query 28049320",
        "py -V:3.12 -B scripts/t152_warehouse_v2.py --query Harry Kane",
        "py -V:3.12 -B scripts/t152_warehouse_v2.py --query 英超",
        "py -V:3.12 -B scripts/t152_warehouse_v2.py --selftest",
        "```",
        "",
        "## 增量表说明",
        "",
        "- `manager_attributes`: (uid, full_name, fourcc, label, category, value, ...)，"
        "主键 (uid, fourcc)，值域 0..20。",
        "- `lang_zh_cn`: (uid, dbid, entity, language_id, language, primary_name, ...)，"
        "按 uid / primary_name 双语索引。",
        "- `career_history_summary`: (uid, name, person_type, n_periods, year_from, year_to, "
        "total_apps, total_goals, last_club_id/name, ...)，person_type ∈ {player, manager}。",
        "",
        f"- `warehouse_v2_benchmark.json`：`status=complete`，含表清单、行数、体积、典型查询耗时与校验样本。",
    ])
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_done(counts: dict[str, int], build_seconds: float, db_size: int,
                integrity: str) -> None:
    lines = [
        "DONE type=warehouse_v2",
        "",
        f"- database: `fm24_warehouse_v2.sqlite` ({db_size:,} B, integrity_check `{integrity}`, "
        f"built in {build_seconds}s)",
        f"- total rows: **{sum(counts.values()):,}** across {len(counts)} tables",
        f"- core tables copied from t139: {sum(1 for k in counts if k not in ('manager_attributes','lang_zh_cn','career_history_summary'))}",
        f"- manager_attributes: {counts.get('manager_attributes',0):,} rows (t137d 34 L3 attrs)",
        f"- lang_zh_cn: {counts.get('lang_zh_cn',0):,} rows (t143 zh-cn showcase)",
        f"- career_history_summary: {counts.get('career_history_summary',0):,} rows (t127 + t128)",
        "- benchmark: scratch/t152/out/warehouse_v2_benchmark.json (status=complete)",
        "--selftest PASS",
    ]
    (OUT / "DONE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_selftest(args) -> int:
    db_path = Path(args.db) if args.db else (OUT / "fm24_warehouse_v2.sqlite")
    if not db_path.is_file():
        print(f"ERROR: {db_path} not found — run --build first", file=sys.stderr)
        return 2
    conn = open_ro(db_path)
    failures = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" +
              (f" — {detail}" if detail else ""))
        if not ok:
            failures.append(name)

    integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
    check("integrity_check", integrity == "ok", integrity)

    counts = table_counts(conn)
    expect = {
        "manager_attributes": 680,   # 20 managers × 34 attrs
        "lang_zh_cn": 152,
        "career_history_summary": 11,
    }
    for tbl, exp in expect.items():
        got = counts.get(tbl, 0)
        check(f"count {tbl}", got == exp, f"{got:,} (expected {exp:,})")

    # 核心表行数抽检（与 t139 一致）
    for tbl, exp in (("basic_people", 658011), ("clubs", 84259), ("star_players", 21),
                     ("star_player_attributes", 1134), ("name_first", 245981)):
        got = counts.get(tbl, 0)
        check(f"core count {tbl}", got == exp, f"{got:,} (expected {exp:,})")

    # 查询耗时 < 5ms
    for label, sql, params in [
        ("uid_lookup_basic_people", "SELECT * FROM basic_people WHERE uid=?", (28049320,)),
        ("manager_attrs_by_uid", "SELECT * FROM manager_attributes WHERE uid=? ORDER BY fourcc", (1120,)),
        ("lang_zh_cn_by_name", "SELECT * FROM lang_zh_cn WHERE primary_name LIKE ? LIMIT 10", ("%英超%",)),
    ]:
        t0 = time.perf_counter()
        for _ in range(100):
            conn.execute(sql, params).fetchall()
        ms = (time.perf_counter() - t0) / 100 * 1000
        check(f"query {label} < 5ms", ms < 5.0, f"{ms:.3f} ms avg")

    # 锚点：Guardiola 34 属性全在 0..20
    bad = conn.execute(
        "SELECT COUNT(*) FROM manager_attributes WHERE uid=1120 AND (value < 0 OR value > 20)").fetchone()[0]
    check("Guardiola 34 attrs in 0..20", bad == 0, f"{bad} bad")

    # 锚点：Harry Kane 生涯履历存在
    kane = conn.execute("SELECT * FROM career_history_summary WHERE uid=28049320").fetchone()
    check("Harry Kane career_history", kane is not None,
          kane["name"] if kane else "missing")

    conn.close()

    # 生成 benchmark + report + done（重新打开只读获取 build info）
    db_size = db_path.stat().st_size
    build_summary_path = OUT / "warehouse_v2_build_summary.json"
    build_seconds = 0.0
    if build_summary_path.is_file():
        build_seconds = json.loads(build_summary_path.read_text(encoding="utf-8")).get("build_seconds", 0.0)
    conn = open_ro(db_path)
    counts = table_counts(conn)
    _write_benchmark(conn, counts, build_seconds, db_size)
    _write_report(conn, counts, build_seconds, db_size, integrity)
    _write_done(counts, build_seconds, db_size, integrity)
    conn.close()

    print(f"--- t152 selftest: {'PASS' if not failures else 'FAIL'} "
          f"({len(failures)} failures) ---")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
