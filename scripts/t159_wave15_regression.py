#!/usr/bin/env python3
"""t159 — Wave 15 增量回归矩阵与受保护路径守卫。

自动发现 scripts/t146_*.py .. scripts/t160_*.py 中已就绪脚本
（存在 scratch/tNN/out/DONE.md 或 edfx_verdict.json），运行它们的
--help 与 --selftest，联合执行 check_repo.py 与
t145_final_regression.py --cached，并校验 reports/ 与
scratch/t01/LEDGER.json 的 SHA-256 在回归前后逐字节不变。

输出：
  scratch/t159/out/wave15_regression_matrix.json  (status=complete)
  scratch/t159/out/REPORT.md
  scratch/t159/out/DONE.md   (首行 DONE type=wave15_regression)

Usage:
    py -V:3.12 -B scripts/t159_wave15_regression.py          # real run
    py -V:3.12 -B scripts/t159_wave15_regression.py --selftest
    py -V:3.12 -B scripts/t159_wave15_regression.py --cached
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fm24_config as cfg  # noqa: E402

ROOT = cfg.ROOT
SCRIPTS = cfg.SCRIPTS_DIR
OUTDIR = cfg.SCRATCH_DIR / "t159" / "out"

WAVE_LO, WAVE_HI = 146, 160
PROTECTED = ["reports", "scratch/t01/LEDGER.json"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(paths: list[Path]) -> dict[str, str]:
    out = {}
    for p in paths:
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file():
                    out[str(f.relative_to(ROOT))] = sha256_file(f)
        elif p.is_file():
            out[str(p.relative_to(ROOT))] = sha256_file(p)
    return out


def discover_ready() -> list[dict]:
    """Find t146..t160 scripts whose out/ has DONE.md or edfx_verdict.json."""
    ready = []
    for p in sorted(SCRIPTS.glob("t[0-9][0-9][0-9]_*.py")):
        try:
            num = int(p.stem[1:4])
        except ValueError:
            continue
        if not (WAVE_LO <= num <= WAVE_HI):
            continue
        tag = f"t{num:03d}"
        outdir = ROOT / "scratch" / tag / "out"
        done = outdir / "DONE.md"
        verdict = outdir / "edfx_verdict.json"
        if done.is_file() or verdict.is_file():
            ready.append({
                "script": str(p.relative_to(ROOT)),
                "tag": tag,
                "marker": "DONE.md" if done.is_file() else "edfx_verdict.json",
            })
    return ready


def run(cmd: list[str], timeout: int = 300) -> dict:
    t0 = time.perf_counter()
    p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    dt = round(time.perf_counter() - t0, 2)
    combined = (p.stdout + "\n" + p.stderr)
    tail = ""
    for ln in reversed(combined.splitlines()):
        if ln.strip():
            tail = ln.strip()[:140]
            break
    return {"cmd": " ".join(cmd), "rc": p.returncode, "elapsed_sec": dt,
            "passed": p.returncode == 0, "tail": tail}


def run_script_help_selftest(item: dict) -> dict:
    script = ROOT / item["script"]
    help_r = run(["py", "-V:3.12", "-B", str(script), "--help"])
    st_r = run(["py", "-V:3.12", "-B", str(script), "--selftest"])
    return {
        "script": item["script"],
        "tag": item["tag"],
        "readiness_marker": item["marker"],
        "help": help_r,
        "selftest": st_r,
        "passed": help_r["passed"] and st_r["passed"],
    }


def run_joint() -> dict:
    crepo = run(["py", "-V:3.12", "-B", "scripts/check_repo.py"])
    cached = run(["py", "-V:3.12", "-B",
                  "scripts/t145_final_regression.py", "--cached"])
    return {"check_repo": crepo,
            "t145_cached": cached,
            "passed": crepo["passed"] and cached["passed"]}


def run_all() -> dict:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    before = sha256_tree([ROOT / p for p in PROTECTED])

    ready = discover_ready()
    wave_results = [run_script_help_selftest(it) for it in ready]
    joint = run_joint()

    after = sha256_tree([ROOT / p for p in PROTECTED])
    protected_ok = before == after

    wp = sum(1 for r in wave_results if r["passed"])
    jpassed = sum(1 for x in (joint["check_repo"], joint["t145_cached"]) if x["passed"])
    all_ok = (wp == len(wave_results) and joint["passed"] and protected_ok)

    report = {
        "schema_id": "fm24.t159.wave15_regression",
        "schema_version": 1,
        "generated_by": "t159",
        "status": "complete",
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "wave15_total": len(ready),
        "wave15_passed": wp,
        "joint_total": 2,
        "joint_passed": jpassed,
        "all_passed": all_ok,
        "tests_all_passed": all_ok,
        "protected_clean": protected_ok,
        "before_sha": before,
        "after_sha": after,
        "wave15_tests": wave_results,
        "joint": joint,
    }
    (OUTDIR / "wave15_regression_matrix.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# t159 — Wave 15 增量回归矩阵",
        "",
        f"- 生成时间：{report['generated_utc']}",
        f"- 产出目录：`{OUTDIR}`",
        f"- Wave 15 就绪脚本：{len(ready)}",
        f"- Wave 15 通过：{wp}/{len(ready)}",
        f"- 联合检查（check_repo + t145 --cached）：{'全部通过' if joint['passed'] else '存在失败项'}",
        f"- 受保护路径 SHA-256 未变：{'是' if protected_ok else '否'}",
        f"- 总体：{'PASS' if all_ok else 'FAIL'}",
        "",
        "## Wave 15 脚本明细",
        "",
        "| 脚本 | 就绪标记 | --help | --selftest | 通过 |",
        "|---|---|---|---|---|",
    ]
    for r in wave_results:
        lines.append(f"| `{r['script']}` | {r['readiness_marker']} | "
                     f"{'PASS' if r['help']['passed'] else 'FAIL'} | "
                     f"{'PASS' if r['selftest']['passed'] else 'FAIL'} | "
                     f"{'PASS' if r['passed'] else 'FAIL'} |")
    lines += [
        "",
        "## 联合检查",
        f"- check_repo.py：{'PASS' if joint['check_repo']['passed'] else 'FAIL'} "
        f"({joint['check_repo']['tail']})",
        f"- t145_final_regression.py --cached：{'PASS' if joint['t145_cached']['passed'] else 'FAIL'} "
        f"({joint['t145_cached']['tail']})",
        "",
        "## 受保护路径守卫",
        f"- reports/ 与 scratch/t01/LEDGER.json SHA-256 回归前后：{'逐字节一致' if protected_ok else '有变动'}",
        "",
        "## 交付物",
        f"- `scripts/t159_wave15_regression.py`",
        f"- `{OUTDIR}/wave15_regression_matrix.json`（status=complete）",
        f"- `{OUTDIR}/REPORT.md`（本文）",
        f"- `{OUTDIR}/DONE.md`（首行 DONE type=wave15_regression）",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    done = [
        "DONE type=wave15_regression",
        f"task=t159 (Wave 15 增量回归矩阵与受保护路径守卫) status=complete",
        f"outdir={OUTDIR}",
        f"wave15_total={len(ready)}",
        f"wave15_passed={wp}",
        f"joint_passed={jpassed}/2",
        f"protected_clean={protected_ok}",
        f"all_passed={all_ok}",
        "deliverables=scripts/t159_wave15_regression.py, wave15_regression_matrix.json, REPORT.md, DONE.md",
    ]
    (OUTDIR / "DONE.md").write_text("\n".join(done) + "\n", encoding="utf-8")

    print(f"\nt159 summary: wave15={wp}/{len(ready)} PASS | joint={jpassed}/2 | "
          f"protected_clean={protected_ok} | {'PASS' if all_ok else 'FAIL'}")
    return report


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="t159_wave15_regression.py",
        description="Wave 15 incremental regression matrix + protected-path guard.")
    ap.add_argument("--selftest", action="store_true",
                    help="real rerun of the full Wave 15 regression matrix")
    ap.add_argument("--cached", action="store_true",
                    help="fast read-only summary of the last matrix")
    args = ap.parse_args()

    if args.cached:
        mat = json.loads((OUTDIR / "wave15_regression_matrix.json").read_text(encoding="utf-8"))
        ok = mat.get("all_passed", False)
        print(f"t159 --cached: {'PASS' if ok else 'FAIL'} "
              f"(wave15={mat.get('wave15_passed')}/{mat.get('wave15_total')}, "
              f"joint={mat.get('joint_passed')}/{mat.get('joint_total')}, "
              f"generated={mat.get('generated_utc')}, cached only)")
        return 0 if ok else 1

    rep = run_all()
    return 0 if rep["all_passed"] else 1


def selftest() -> int:
    mat_path = OUTDIR / "wave15_regression_matrix.json"
    need = True
    if mat_path.exists():
        try:
            m = json.loads(mat_path.read_text(encoding="utf-8"))
            need = not (m.get("status") == "complete"
                        and (OUTDIR / "REPORT.md").exists()
                        and (OUTDIR / "DONE.md").exists())
        except Exception:
            need = True
    if need:
        run_all()
        m = json.loads(mat_path.read_text(encoding="utf-8"))
    else:
        m = json.loads(mat_path.read_text(encoding="utf-8"))

    checks = []
    def ck(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), str(detail)))

    ck("matrix status == complete", m.get("status") == "complete", str(m.get("status")))
    ck("matrix all_passed", m.get("all_passed") is True, str(m.get("all_passed")))
    ck("REPORT.md exists", (OUTDIR / "REPORT.md").exists())
    ck("DONE.md exists", (OUTDIR / "DONE.md").exists())
    done_first = (OUTDIR / "DONE.md").read_text(encoding="utf-8").splitlines()[0] \
        if (OUTDIR / "DONE.md").exists() else ""
    ck("DONE.md first line DONE type=wave15_regression",
       done_first == "DONE type=wave15_regression", done_first)
    ck("protected_clean", m.get("protected_clean") is True, str(m.get("protected_clean")))
    ck("wave15_passed == wave15_total",
       m.get("wave15_passed") == m.get("wave15_total"),
       f"{m.get('wave15_passed')}/{m.get('wave15_total')}")
    ck("joint_passed == 2", m.get("joint_passed") == 2,
       f"{m.get('joint_passed')}/2")
    for r in m.get("wave15_tests", []):
        ck(f"wave15 {r['script']} passed", r.get("passed") is True,
           f"help={r['help']['passed']} selftest={r['selftest']['passed']}")
    for name in ("check_repo", "t145_cached"):
        ck(f"joint {name} passed", m["joint"][name]["passed"] is True)

    bad = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  [{'ok' if ok else 'FAIL'}] {name}" +
              (f" <- {detail}" if not ok and detail else ""))
    print(f"\nselftest: {len(checks)-len(bad)}/{len(checks)} checks passed -> "
          f"{'PASS' if not bad else 'FAIL'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
