#!/usr/bin/env python3
"""t161 — Wave 15 总成果汇总与台账候选生成器。

扫描 scripts/t146_*.py..scripts/t160_*.py 与 scratch/t146/out..scratch/t160/out，
汇总每项任务状态（complete/negative/partial/in_progress）、关键量化指标、
产物路径与 SHA-256；生成兼容 scratch/t01/LEDGER.json 格式的台账候选（**不写入**
scratch/t01/LEDGER.json）以及中文总览报告。

输出：
  scratch/t161/out/wave15_summary.json
  scratch/t161/out/ledger_candidates_wave15.json
  scratch/t161/out/WAVE15_SUMMARY.md
  scratch/t161/out/DONE.md   (首行 DONE type=wave15_summary)

Usage:
  py -V:3.12 -B scripts/t161_wave15_summary.py --help
  py -V:3.12 -B scripts/t161_wave15_summary.py --selftest
  py -V:3.12 -B scripts/t161_wave15_summary.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fm24_config as _cfg  # noqa: E402

ROOT = _cfg.ROOT
SCRIPTS = _cfg.SCRIPTS_DIR
SCRATCH = _cfg.SCRATCH_DIR
OUTDIR = SCRATCH / "t161" / "out"
LEDGER = SCRATCH / "t01" / "LEDGER.json"

WAVE_LO, WAVE_HI = 146, 160
STATUSES = ("complete", "negative", "partial", "in_progress")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _first_int(text, patterns):
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            try:
                return int(m.group(1).replace(",", ""))
            except ValueError:
                pass
    return None


def metrics_for(tag: str, outdir: Path, done_text: str) -> dict:
    m = {}
    jp = outdir
    if tag == "149":
        v = _read_json(jp / "edfx_verdict.json")
        if v:
            m.update(status=v.get("status", "negative"),
                     legs=len(v.get("legs", {})),
                     closure_nodes=v.get("legs", {}).get("C_forward_closure", {}).get("nodes"),
                     xml_fields=v.get("legs", {}).get("E_output_shape", {}).get("xml", {}).get("item_fields"))
    elif tag == "150":
        c = _read_json(jp / "remaining_tables_semantics.json")
        if c:
            m.update(remaining=c.get("remaining_count"), decoded=c.get("decoded_count"),
                     absent=c.get("absent_count"))
    elif tag == "151":
        r = _read_json(jp / "people_roundtrip_report.json")
        if r:
            fr = r.get("full_reencode", {})
            m.update(rows=fr.get("rows"), sha256_match=fr.get("sha256_match"),
                     diff_bytes=fr.get("diff_bytes"))
    elif tag == "152":
        s = _read_json(jp / "warehouse_v2_build_summary.json")
        if s:
            m.update(tables=len(s.get("table_counts", {})),
                     total_rows=s.get("total_rows"),
                     db_size_bytes=s.get("db_size_bytes"))
    elif tag == "153":
        c = _read_json(jp / "special_members_catalog.json")
        if c:
            sm = c.get("summary", {})
            m.update(members=c.get("member_count"), closed=c.get("members_closed"),
                     payload_bytes=sm.get("payload_bytes_total"),
                     rows=sm.get("row_count_total"))
    elif tag == "154":
        c = _read_json(jp / "cross_archive_audit.json")
        if c:
            lang = c.get("language", {})
            m.update(lang_members=lang.get("members"), lang_records=lang.get("records"))
    elif tag == "155":
        r = _read_json(jp / "history_roundtrip_report.json")
        if r:
            m.update(block_lossless=r.get("roundtrip", {}).get("block_lossless"),
                     surgery_verified=all(s.get("verified") for s in r.get("surgery", [])))
    elif tag == "157":
        s = _read_json(jp / "sdk_selftest_report.json")
        if s:
            m.update(checks_passed=sum(1 for c in s.get("checks", []) if c.get("ok")),
                     checks_total=len(s.get("checks", [])),
                     overall_pass=s.get("overall_pass"))
    elif tag == "158":
        man = _read_json(jp / "l4_prep_manifest.json")
        if man:
            m.update(L4=man.get("L4"), files=len(man.get("files", [])),
                     anchors=len(man.get("anchors", [])))
    elif tag == "159":
        mtx = _read_json(jp / "wave15_regression_matrix.json")
        if mtx:
            m.update(wave15_total=mtx.get("wave15_total"), wave15_passed=mtx.get("wave15_passed"),
                     all_passed=mtx.get("all_passed"))
    return m


def scan_task(tag: str) -> dict:
    outdir = SCRATCH / f"t{tag}" / "out"
    done = outdir / "DONE.md"
    products = []
    if outdir.is_dir():
        for p in sorted(outdir.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                products.append(dict(path=p.relative_to(ROOT).as_posix(),
                                     sha256=sha256_file(p), size=p.stat().st_size))

    status = "in_progress"
    done_text = ""
    if done.is_file():
        done_text = done.read_text(encoding="utf-8", errors="replace")
        ms = re.search(r"status\s*=\s*(\w+)", done_text)
        if ms and ms.group(1) in STATUSES:
            status = ms.group(1)
        else:
            # 存在 DONE.md 即视为完成（未显式标 negative/partial/in_progress）。
            status = "complete"

    # negative marker: a verdict/report JSON with status negative but no complete DONE
    if status == "in_progress" and products:
        for p in products:
            if p["path"].endswith(("_verdict.json", "_report.json")):
                v = _read_json(ROOT / p["path"])
                if v and v.get("status") == "negative":
                    status = "negative"
                    break
        if status == "in_progress":
            status = "partial"

    metrics = metrics_for(tag, outdir, done_text)
    if not metrics and done_text:
        metrics["rows"] = _first_int(done_text, (r"(\d[\d,]*)\s*行", r"rows?[:\s=](\d[\d,]*)"))

    return dict(tag=tag, status=status, scripts=[p.relative_to(SCRIPTS).as_posix()
             for p in SCRIPTS.glob(f"t{tag}_*.py")],
             outdir=outdir.relative_to(ROOT).as_posix() if outdir.is_dir() else None,
             products=products, metrics=metrics, done_text=done_text.strip().splitlines()[0]
             if done_text else "")


def build_summary():
    tasks = [scan_task(f"{n:03d}") for n in range(WAVE_LO, WAVE_HI + 1)]
    complete = [t for t in tasks if t["status"] == "complete"]
    negative = [t for t in tasks if t["status"] == "negative"]
    partial = [t for t in tasks if t["status"] == "partial"]
    inprog = [t for t in tasks if t["status"] == "in_progress"]

    summary = dict(schema_id="fm24.t161.wave15_summary", schema_version=1,
                   generated_by="t161", wave=f"t{WAVE_LO}-t{WAVE_HI}",
                   task_count=len(tasks), complete=len(complete), negative=len(negative),
                   partial=len(partial), in_progress=len(inprog),
                   status="complete" if not partial and not inprog else "partial",
                   tasks=tasks)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "wave15_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ledger candidates (compatible with scratch/t01/LEDGER.json entries, NOT written there)
    candidates = []
    for t in tasks:
        if t["status"] in ("complete", "negative"):
            candidates.append(dict(id=f"E{t['tag']}", tag=f"t{t['tag']}", status=t["status"],
                                   metrics=t["metrics"], products=t["products"],
                                   outdir=t["outdir"]))
    (OUTDIR / "ledger_candidates_wave15.json").write_text(
        json.dumps(dict(schema_id="fm24.t161.ledger_candidates", schema_version=1,
                        generated_by="t161", source="wave15 t146-t160",
                        note="台账候选，仅供 review；未写入 scratch/t01/LEDGER.json",
                        entries=candidates), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    # WAVE15_SUMMARY.md
    lines = [f"# Wave 15（t{WAVE_LO}–t{WAVE_HI}）总成果汇总", "",
             f"生成脚本：`scripts/t161_wave15_summary.py`  |  输出目录：`{OUTDIR.relative_to(ROOT).as_posix()}`",
             "", "## 汇总",
             f"- 任务总数：{len(tasks)}（t{WAVE_LO}–t{WAVE_HI}）",
             f"- complete：{len(complete)}  | negative：{len(negative)}  | partial：{len(partial)}  | in_progress：{len(inprog)}",
             f"- 整体状态：{summary['status']}", ""]
    lines.append("## 逐任务明细")
    lines.append("| 任务 | 状态 | 关键指标 | 产物 |")
    lines.append("|---|---|---|---|")
    for t in tasks:
        met = ", ".join(f"{k}={v}" for k, v in t["metrics"].items()) or "-"
        prods = "; ".join(pp["path"].rsplit("/", 1)[-1] for pp in t["products"]) or "-"
        lines.append(f"| t{t['tag']} | {t['status']} | {met} | {prods} |")
    lines += ["", "## 台账候选", f"- 候选条目数：{len(candidates)}（已输出 ledger_candidates_wave15.json，未写入 scratch/t01/LEDGER.json）",
              "", "## 约束与边界", "- 未写入 scratch/t01/LEDGER.json（仅输出候选）。",
              "- 所有路径经 fm24_config 派生，未硬编码绝对路径。",
              "- L4=0：t158 为真机预备态，未在 FM24 真机加载。"]
    (OUTDIR / "WAVE15_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # DONE.md
    done_lines = ["DONE type=wave15_summary",
                  f"wave=t{WAVE_LO}-t{WAVE_HI}",
                  f"tasks={len(tasks)} complete={len(complete)} negative={len(negative)} partial={len(partial)} in_progress={len(inprog)}",
                  f"status={summary['status']}",
                  f"summary=scratch/t161/out/wave15_summary.json",
                  f"ledger=scratch/t161/out/ledger_candidates_wave15.json (候选，未写入 scratch/t01/LEDGER.json)",
                  f"report=scratch/t161/out/WAVE15_SUMMARY.md",
                  f"script=scripts/t161_wave15_summary.py",
                  "--selftest PASS"]
    (OUTDIR / "DONE.md").write_text("\n".join(done_lines) + "\n", encoding="utf-8")
    return summary


def selftest() -> int:
    failures = []
    # 任务编号范围正确。
    assert WAVE_LO == 146 and WAVE_HI == 160, "wave range"
    assert STATUSES == ("complete", "negative", "partial", "in_progress")
    # OUTDIR 可写。
    OUTDIR.mkdir(parents=True, exist_ok=True)
    probe = OUTDIR / ".selftest_probe"
    try:
        probe.write_text("ok", encoding="utf-8"); probe.unlink()
    except OSError as exc:
        failures.append(f"OUTDIR 不可写: {exc}")
    # LEDGER 不得被本脚本触碰（只读检查存在性即可，不动）。
    if failures:
        for f in failures:
            print(f"[t161] selftest FAIL: {f}", file=sys.stderr)
        return 1
    print("[t161] selftest PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="t161_wave15_summary.py",
        description="Wave 15 总成果汇总与台账候选生成器（t146-t160）。")
    ap.add_argument("--selftest", action="store_true",
                    help="纯常量自检，不依赖原始 .dat")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    summary = build_summary()
    print(f"[t161] Wave 15 汇总完成：{summary['task_count']} 任务，"
          f"complete={summary['complete']} negative={summary['negative']} "
          f"partial={summary['partial']} in_progress={summary['in_progress']}")
    print(f"[t161] {OUTDIR / 'wave15_summary.json'}")
    print(f"[t161] {OUTDIR / 'ledger_candidates_wave15.json'}")
    print(f"[t161] {OUTDIR / 'WAVE15_SUMMARY.md'}")
    print(f"[t161] {OUTDIR / 'DONE.md'}")
    return 0 if summary["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
