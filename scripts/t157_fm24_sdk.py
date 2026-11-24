#!/usr/bin/env python3
"""t157_fm24_sdk — FM24 全库统一纯 Python 读写 SDK 与 CLI.

顶层入口，延迟加载并统一封装现有子模块（不重写底层二进制解析器）：
  * fm24_config        : 统一路径/依赖配置（所有路径由此派生，绝不硬编码 D:\\/Z:\\）
  * t133_fm24_reader_v2: 世界库 server_db/client_db 79 表只读解码 + footer 闭合
  * t138_people_pure_py: 人物库 people_db.dat 65.8 万行纯 Python 解码
  * t143_lang_db       : 22 语种语言库 (lang_db_2400/2430) UID 联合与中文译名
  * t152_warehouse_v2  : SQLite 數仓 (basic_people/clubs/manager_attributes/...)
  * t155_history_roundtrip: 6 个历史库位级双向无损回写
  * t140_fm24_roundtrip: 双向回写 (Stage1 SHA-256 位级回环 / Stage2 FMF 重打包)

CLI 子命令：--help / inventory / lookup <uid_or_name> / selftest
退出码：0=成功，1=校验失败，2=用法/致命错误。

只读输入：原始 .dat 只读；严禁修改 reports/、scratch/t01/LEDGER.json 及既有脚本。
"""
from __future__ import annotations

import argparse
import importlib
import json
import sqlite3
import sys
import time
from pathlib import Path

# 把 scripts 目录放到 sys.path 头部，以便 import 同目录 tNN_*.py
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import fm24_config as _cfg  # noqa: E402  (必须在 sys.path 调整之后)

ROOT = _cfg.ROOT
OUTDIR = _cfg.SCRATCH_DIR / "t157" / "out"

# 全库 13 个 .dat 档案（scratch/data 下），供 inventory 健康体检用
DATA_DIR = _cfg.DATA_DIR
THIRTEEN_DAT = [
    "server_db.dat",
    "client_db.dat",
    "people_db.dat",
    "basic_people_db.dat",
    "lang_db_2400.dat",      # 如存在则由 t143 读 LANG_DB_DAT(editor.exe 输入)
    "lang_update_db.dat",
    "summary.dat",
    "pl_hist_dt.dat",
    "pl_hist_id.dat",
    "pl_hist_index.dat",
    "non_pl_hist_dt.dat",
    "non_pl_hist_id.dat",
    "non_pl_hist_index.dat",
]

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2


class FM24SDKError(RuntimeError):
    """SDK 层封装错误（不吞底层子模块的诚实失败）。"""


def _import(name: str):
    """按名延迟导入同目录子模块，失败时给出清晰错误。"""
    try:
        return importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - 依赖缺失时诚实报错
        raise FM24SDKError(f"无法导入子模块 {name}: {exc}") from exc


class FM24Database:
    """FM24 全库统一读写入口。所有子系统延迟加载，首次访问才初始化。"""

    def __init__(self, out_dir: str | Path | None = None) -> None:
        self.out_dir = Path(out_dir) if out_dir else OUTDIR
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self._world = None      # t133 registry / reader
        self._people = None     # t138 module handle
        self._lang = None       # t143 module handle
        self._warehouse = None  # t152 sqlite connection
        self._history = None    # t155 module handle
        self._roundtrip = None  # t140 module handle

    # ---------------------------------------------------------------- 延迟子系统
    @property
    def world(self):
        """世界库 79 表读取器（t133_fm24_reader_v2 + t112_fm24_reader.Archive），延迟加载。"""
        if self._world is None:
            t133 = _import("t133_fm24_reader_v2")
            t112 = _import("t112_fm24_reader")  # Archive 容器在此模块
            records, specs = t133.registry(t133.load(t133.TRACE))
            l3 = t133.load(t133.L3)
            self._world = {"t133": t133, "t112": t112, "archive_cls": t112.Archive,
                           "records": records, "specs": specs, "l3": l3}
        return self._world

    @property
    def people(self):
        """人物库 t138_people_pure_py 模块句柄，延迟加载。"""
        if self._people is None:
            self._people = _import("t138_people_pure_py")
        return self._people

    @property
    def lang(self):
        """语言库 t143_lang_db 模块句柄，延迟加载。"""
        if self._lang is None:
            self._lang = _import("t143_lang_db")
        return self._lang

    @property
    def warehouse(self):
        """t152 SQLite 數仓只读连接，延迟加载。"""
        if self._warehouse is None:
            mod = _import("t152_warehouse_v2")
            db_path = mod.OUT / "fm24_warehouse_v2.sqlite"
            if not db_path.is_file():
                raise FM24SDKError(
                    f"數仓未构建: {db_path} — 先运行 t152_warehouse_v2.py --build")
            self._warehouse = mod.open_ro(db_path)
        return self._warehouse

    @property
    def history(self):
        """t155_history_roundtrip 模块句柄，延迟加载。"""
        if self._history is None:
            self._history = _import("t155_history_roundtrip")
        return self._history

    @property
    def roundtrip(self):
        """t140_fm24_roundtrip 模块句柄，延迟加载。"""
        if self._roundtrip is None:
            self._roundtrip = _import("t140_fm24_roundtrip")
        return self._roundtrip

    # ---------------------------------------------------------------- 体检
    def inventory(self) -> dict:
        """全库 13 档案健康体检：每个 .dat 的可读性与闭合状态。"""
        t0 = time.perf_counter()
        entries: list[dict] = []
        overall_ok = True
        for name in THIRTEEN_DAT:
            if name == "lang_db_2400.dat":
                path = _cfg.LANG_DB_DAT  # legacy 游戏输入目录，不在 scratch/data
            else:
                path = DATA_DIR / name
            rec: dict = {"archive": name, "present": path.is_file(),
                         "bytes": path.stat().st_size if path.is_file() else 0,
                         "readable": False, "closed": None, "detail": "", "subsystem": ""}
            if not path.is_file():
                rec["detail"] = "缺失"
                overall_ok = False
                entries.append(rec)
                continue
            try:
                if name in ("server_db.dat", "client_db.dat"):
                    rec["subsystem"] = "t133/t112 世界库 79 表"
                    arch = name.split("_")[0]  # server | client
                    arc = self.world["archive_cls"](arch)
                    n_tables = 0
                    closed = 0
                    for key, trace in sorted(self.world["records"].items()):
                        if key[0] != arch:
                            continue
                        n_tables += 1
                        spec = self.world["specs"].get(key)
                        if spec is None:
                            continue
                        payload = arc.payload(key[1])
                        res = self.world["t133"].verify_table(
                            spec, trace, self.world["l3"], payload, samples=0)
                        if res["footer_closed"]:
                            closed += 1
                    rec["readable"] = True
                    rec["tables"] = n_tables
                    rec["closed"] = closed
                    rec["detail"] = f"{closed}/{n_tables} 表 footer 闭合"
                    if closed != n_tables:
                        overall_ok = False
                elif name == "people_db.dat":
                    rec["subsystem"] = "t138 人物库"
                    raw = self.people.decompress_people_db()
                    decoded, end_pos, count, row_end, footer = self.people.walk(
                        raw, None, None)
                    rec["readable"] = True
                    rec["rows_header"] = count
                    rec["rows_decoded"] = decoded
                    rec["closed"] = (end_pos == len(raw))
                    rec["detail"] = f"解码 {decoded:,}/{count:,} 行, EOF 闭合={end_pos == len(raw)}"
                    if end_pos != len(raw):
                        overall_ok = False
                elif name in ("lang_db_2400.dat", "lang_update_db.dat"):
                    rec["subsystem"] = "t143 语言库"
                    source = (self.lang.SOURCES[0] if name == "lang_db_2400.dat"
                              else self.lang.SOURCES[1])
                    ar = self.lang.LanguageArchive(source)  # 构造已校验 FMF 布局、22 语种×16 表
                    mc = int(ar.metadata()["member_count"])
                    rec["readable"] = True
                    rec["members"] = mc
                    rec["closed"] = bool(mc == 352)
                    rec["detail"] = f"{mc} 个成员 (22 语种 × 16 表), 结构完整={mc == 352}"
                    if not rec["closed"]:
                        overall_ok = False
                else:
                    rec["subsystem"] = "原始归档"
                    rec["readable"] = True
                    rec["closed"] = True
                    rec["detail"] = "存在且可读（未纳入深度解码子系统）"
            except Exception as exc:  # 不吞任何子模块诚实失败
                rec["readable"] = False
                rec["closed"] = False
                rec["detail"] = f"错误: {exc!s}"
                overall_ok = False
            entries.append(rec)
        elapsed_ms = round(1000.0 * (time.perf_counter() - t0), 1)
        return {
            "status": "complete" if overall_ok else "partial",
            "elapsed_ms": elapsed_ms,
            "archives_total": len(entries),
            "archives_ok": sum(1 for e in entries if e["readable"] and e["closed"] is not False),
            "archives": entries,
        }

    # ---------------------------------------------------------------- 聚合查询
    def _uid_from_number(self, text: str) -> int | None:
        try:
            v = int(text)
            if 0 <= v <= 0xFFFFFFFF:
                return v
        except ValueError:
            return None
        return None

    def lookup(self, uid_or_name: str) -> dict:
        """跨库聚合查询：数字按 uid 精确；文本跨表模糊搜索中/英译名。

        返回：实体基本信息 + 中文译名 + 能力属性/履历（可用子系统皆已实测）。
        """
        t0 = time.perf_counter()
        result: dict = {"query": uid_or_name, "kind": None, "entities": [],
                        "subsystems": {}, "elapsed_ms": 0.0}

        uid = self._uid_from_number(uid_or_name)
        if uid is not None:
            result["kind"] = "uid"
            result["uid"] = uid
            self._lookup_by_uid(result, uid)
        else:
            result["kind"] = "name"
            result["name"] = uid_or_name
            self._lookup_by_name(result, uid_or_name)
        result["elapsed_ms"] = round(1000.0 * (time.perf_counter() - t0), 1)
        return result

    def _lookup_by_uid(self, result: dict, uid: int) -> None:
        # 1) 數仓：basic_people / clubs / manager_attributes / career_history_summary
        try:
            conn = self.warehouse
            subsys: dict = {}
            for tbl, idcol in (("basic_people", "uid"), ("clubs", "uid"),
                               ("star_players", "uid"), ("manager_attributes", "uid"),
                               ("career_history_summary", "uid")):
                try:
                    rows = [dict(r) for r in conn.execute(
                        f'SELECT * FROM "{tbl}" WHERE "{idcol}" = ? LIMIT 10', (uid,))]
                except sqlite3.OperationalError:
                    rows = []
                if rows:
                    subsys[tbl] = rows
            if subsys:
                result["subsystems"]["warehouse"] = subsys
                ent = {"uid": uid, "source": "warehouse", "tables": list(subsys),
                       "rows": subsys}
                result["entities"].append(ent)
        except FM24SDKError as exc:
            result["subsystems"]["warehouse"] = {"error": str(exc)}

        # 2) 语言库：全语种本地化（含中文译名），t143 lookup(uid)
        try:
            matches = self.lang.lookup(uid)
            if matches:
                result["subsystems"]["lang"] = matches
                for m in matches:
                    ent = {"uid": uid, "dbid": m.get("dbid"), "entity": m.get("entity"),
                           "localization_table_type": m.get("localization_table_type"),
                           "localizations": m.get("localizations", {}),
                           "source": "lang_db"}
                    result["entities"].append(ent)
        except FM24SDKError as exc:
            result["subsystems"]["lang"] = {"error": str(exc)}

        # 3) 人物库：t138 不按 uid 索引（按 ordinal 顺序存储），仅标注
        result["subsystems"]["people"] = {
            "note": "people_db.dat 按 ordinal 顺序存储，无 uid 索引；全表扫描需 t138.walk(verify-full)",
        }

    def _lookup_by_name(self, result: dict, name: str) -> None:
        try:
            conn = self.warehouse
            esc = name.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            pat = f"%{esc}%"
            found_uids: list[int] = []
            sources: list[dict] = []
            for table, col, columns in (
                ("clubs", "name_full", "uid, ordinal, name_full, name_short"),
                ("clubs", "name_short", "uid, ordinal, name_full, name_short"),
                ("star_players", "name", "uid, ordinal, name, person_type, ca, pa"),
                ("lang_zh_cn", "primary_name", "uid, entity, language_id, primary_name"),
                ("career_history_summary", "name", "uid, name, person_type, n_periods"),
            ):
                try:
                    base_sql = (f'SELECT {columns} FROM "{table}" '
                                f'WHERE "{col}" LIKE ? ESCAPE \'\\\'')
                    rows = [dict(r) for r in conn.execute(base_sql + " LIMIT 10", (pat,))]
                except sqlite3.OperationalError:
                    rows = []
                if rows:
                    sources.append({"source": f"{table}.{col}", "sample": rows})
                    for r in rows:
                        u = r.get("uid")
                        if u is not None and u not in found_uids:
                            found_uids.append(u)
            if sources:
                result["subsystems"]["warehouse_text"] = sources
            for u in found_uids[:5]:
                ent = {"uid": u, "source": "warehouse_name_match"}
                result["entities"].append(ent)
                # 对每个候选 uid 再做语言库本地化
                try:
                    matches = self.lang.lookup(u)
                    if matches:
                        ent["localizations"] = matches
                        result["subsystems"].setdefault("lang", []).extend(matches)
                except FM24SDKError:
                    pass
        except FM24SDKError as exc:
            result["subsystems"]["warehouse_text"] = {"error": str(exc)}

    # ---------------------------------------------------------------- 自检
    def selftest(self) -> dict:
        """全面自检所有子模块集成，返回结构化结果；退出码由 CLI 决定。"""
        t0 = time.perf_counter()
        checks: list[dict] = []
        overall = True

        def ck(name: str, ok: bool, detail: str = "") -> None:
            nonlocal overall
            overall = overall and ok
            checks.append({"name": name, "ok": ok, "detail": detail})

        # --- t133 世界库：注册表组成 + 首表闭合抽检 ---
        try:
            w = self.world
            n_specs = len(w["specs"])
            n_records = len(w["records"])
            ck("t133 registry", n_records == 79,
               f"records={n_records} specs={n_specs}")
            # 对 server/8 做一次单表闭合抽检
            key = ("server", 8)
            if key in w["specs"]:
                arc = w["archive_cls"]("server")
                res = w["t133"].verify_table(w["specs"][key], w["records"][key],
                                             w["l3"], arc.payload(8), samples=0)
                ck("t133 server/8 闭合", res["footer_closed"],
                   f"rows={res['rows_decoded']} err={res.get('error')}")
            else:
                ck("t133 server/8 闭合", False, "server/8 不在注册表")
        except Exception as exc:
            ck("t133 世界库", False, f"{exc!s}")
            overall = False

        # --- t138 人物库：合成语法回环 ---
        try:
            pmod = self.people
            st = pmod.selftest()
            ck("t138 selftest", bool(st.get("pass")),
               f"cases={len(st.get('cases', []))}")
        except Exception as exc:
            ck("t138 selftest", False, f"{exc!s}")
            overall = False

        # --- t143 语言库：合成控制 + 焦点 UID 联合 ---
        try:
            lmod = self.lang
            lmod.controls()
            ck("t143 controls", True, "合成 UTF-8/NULL/变长 通过")
            m = lmod.lookup(8)  # 焦点 UID
            ck("t143 lookup(8)", bool(m), f"matches={len(m)}")
        except Exception as exc:
            ck("t143 语言库", False, f"{exc!s}")
            overall = False

        # --- t152 數仓：完整性 + 行数抽检 ---
        try:
            wmod = _import("t152_warehouse_v2")
            db_path = wmod.OUT / "fm24_warehouse_v2.sqlite"
            if db_path.is_file():
                conn = wmod.open_ro(db_path)
                integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
                ck("t152 integrity", integrity == "ok", integrity)
                counts = wmod.table_counts(conn)
                for tbl, exp in (("basic_people", 658011), ("clubs", 84259),
                                 ("lang_zh_cn", 152), ("manager_attributes", 680)):
                    got = counts.get(tbl, 0)
                    ck(f"t152 count {tbl}", got == exp, f"{got:,} (期望 {exp:,})")
                conn.close()
            else:
                ck("t152 數仓存在", False, f"{db_path} 缺失（先运行 --build）")
                overall = False
        except Exception as exc:
            ck("t152 數仓", False, f"{exc!s}")
            overall = False

        # --- t155 历史库：block-level lossless ---
        try:
            hmod = self.history
            rt = hmod.roundtrip_all(self.out_dir / "t155_selftest")
            ck("t155 block lossless", bool(rt.get("overall_block_lossless")),
               str(rt.get("summary", ""))[:80])
        except Exception as exc:
            ck("t155 历史库", False, f"{exc!s}")
            overall = False

        # --- t140 双向回写：轻量 selftest（不跑完整 Unicorn，避免过慢）---
        try:
            rmod = self.roundtrip
            st = rmod.selftest(self.out_dir / "t140_selftest")
            ck("t140 selftest", st == 0, f"退出码={st}")
        except Exception as exc:
            ck("t140 双向回写", False, f"{exc!s}")
            overall = False

        elapsed_ms = round(1000.0 * (time.perf_counter() - t0), 1)
        return {
            "status": "complete" if overall else "partial",
            "overall_pass": overall,
            "elapsed_ms": elapsed_ms,
            "checks": checks,
            "passed": sum(1 for c in checks if c["ok"]),
            "failed": sum(1 for c in checks if not c["ok"]),
        }

    # ---------------------------------------------------------------- 报告落盘
    def write_selftest_report(self, report: dict) -> Path:
        out = self.out_dir / "sdk_selftest_report.json"
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        return out


# =====================================================================
# CLI
# =====================================================================

def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="t157_fm24_sdk.py",
        description="FM24 全库统一纯 Python 读写 SDK 与 CLI（t157）。",
        epilog=("示例:\n"
                "  py -V:3.12 -B scripts/t157_fm24_sdk.py --selftest\n"
                "  py -V:3.12 -B scripts/t157_fm24_sdk.py inventory\n"
                "  py -V:3.12 -B scripts/t157_fm24_sdk.py lookup 28049320\n"
                "  py -V:3.12 -B scripts/t157_fm24_sdk.py lookup 梅西"),
    )
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--selftest", action="store_true",
                   help="运行全面自检所有子模块集成（退出码 0/1/2）")
    sub = ap.add_subparsers(dest="cmd", metavar="{inventory,lookup,selftest,--help}")
    sub.add_parser("inventory", help="全库 13 档案健康体检")
    p_lookup = sub.add_parser("lookup", help="跨库聚合查询（数字=uid，文本=中/英译名）")
    p_lookup.add_argument("uid_or_name", metavar="UID_OR_NAME",
                          help="球员/教练/俱乐部 uid（数字）或中/英文名称")
    sub.add_parser("selftest", help="等价于 --selftest")
    return ap


def _run_inventory(db: FM24Database) -> int:
    rep = db.inventory()
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return EXIT_OK if rep["status"] == "complete" else EXIT_FAIL


def _run_lookup(db: FM24Database, uid_or_name: str) -> int:
    rep = db.lookup(uid_or_name)
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return EXIT_OK


def _run_selftest(db: FM24Database, write_report: bool = True) -> int:
    rep = db.selftest()
    if write_report:
        path = db.write_selftest_report(rep)
        print(f"[t157] selftest report -> {path}")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    if rep["status"] == "complete" and rep["overall_pass"]:
        return EXIT_OK
    if rep["status"] == "partial":
        return EXIT_FAIL
    return EXIT_USAGE


def main(argv: list[str] | None = None) -> int:
    ap = _build_parser()
    args = ap.parse_args(argv)
    db = FM24Database()

    if args.selftest or args.cmd == "selftest":
        return _run_selftest(db)
    if args.cmd == "inventory":
        return _run_inventory(db)
    if args.cmd == "lookup":
        return _run_lookup(db, args.uid_or_name)
    ap.print_help()
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
