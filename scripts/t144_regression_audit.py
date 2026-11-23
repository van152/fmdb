"""t144 Wave 13+14 regression audit + deliverable SHA-256 matrix.

Pure mechanical verification. Read-only: never touches reports/, scratch/t01/LEDGER.json
or any scripts/tNN_*.py. Writes only to scripts/t144_regression_audit.py and
scratch/t144/out/.

Usage:
    py -V:3.12 -B scripts/t144_regression_audit.py          # full regression -> scratch/t144/out/
    py -V:3.12 -B scripts/t144_regression_audit.py --selftest  # full regression + self assertions

Deliverables (scratch/t144/out/):
  regression_matrix.json  per-script exit code, runtime, pass/fail,
                          DONE.md catalog, SHA-256 manifest, protected-path clean check
  REPORT.md               markdown table of all regression checks + completed task catalog
  DONE.md                 first line `DONE type=t144`, pass count (?/18),
                          protected-path clean=True, --selftest PASS
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "scratch" / "t144" / "out"
TIMEOUT_S = 120
BIG_SKIP_BYTES = 50 * 1024 * 1024  # skip .bin/.pkl/.sqlite larger than this
PROTECTED = ["reports/", "scratch/t01/LEDGER.json"]

# (script, extra_args). t01_anchors has no --selftest support -> runs bare.
SCRIPTS = [
    ("scripts/t01_anchors.py", []),
    ("scripts/t97_extract_4cc_mem.py", ["--selftest"]),
    ("scripts/t98_table45_closure.py", ["--selftest"]),
    ("scripts/t106_special_members.py", ["--selftest"]),
    ("scripts/t108_extract_4cc_v2.py", ["--selftest"]),
    ("scripts/t109_big3_l3_join.py", ["--selftest"]),
    ("scripts/t110_master_l3_schema.py", ["--selftest"]),
    ("scripts/t112_fm24_reader.py", ["--selftest"]),
    ("scripts/t115_basic_people_full.py", ["--selftest"]),
    ("scripts/t119_unicorn_last5.py", ["--selftest"]),
    ("scripts/t120_people_unicorn.py", ["--selftest"]),
    ("scripts/t121_master_79of79.py", ["--selftest"]),
    ("scripts/t122_people_l3_schema.py", ["--selftest"]),
    ("scripts/t123_basic_people_l3.py", ["--selftest"]),
    ("scripts/t125_big3_gap_closure.py", ["--selftest"]),
    ("scripts/t126_player_attributes_l3.py", ["--selftest"]),
    ("scripts/t133_fm24_reader_v2.py", ["--selftest"]),
    ("scripts/t135_star_player_cards.py", ["--selftest"]),
]


def last_lines(text: str, n: int = 3) -> list[str]:
    lines = text.splitlines()
    return lines[-n:] if lines else []


def run_one(script: str, args: list[str]) -> dict:
    cmd = ["py", "-V:3.12", "-B", str(script), *args]
    start = time.perf_counter()
    result: dict = {
        "script": script,
        "args": args,
        "cmd": " ".join(cmd),
        "exit_code": None,
        "elapsed_s": None,
        "pass": False,
        "timeout": False,
        "stdout_last3": [],
        "stderr_last3": [],
        "error": None,
    }
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_S,
        )
        result["exit_code"] = proc.returncode
        result["pass"] = proc.returncode == 0
        result["stdout_last3"] = last_lines(proc.stdout, 3)
        result["stderr_last3"] = last_lines(proc.stderr, 3)
    except subprocess.TimeoutExpired as exc:
        result["timeout"] = True
        result["exit_code"] = -1
        result["pass"] = False
        result["stdout_last3"] = last_lines(exc.stdout.decode("utf-8", "replace") if exc.stdout else "", 3)
        result["stderr_last3"] = last_lines(exc.stderr.decode("utf-8", "replace") if exc.stderr else "", 3)
        result["error"] = f"timeout after {TIMEOUT_S}s"
    except Exception as exc:  # noqa: BLE001
        result["exit_code"] = -2
        result["pass"] = False
        result["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        result["elapsed_s"] = round(time.perf_counter() - start, 4)
    return result


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_done_catalog() -> dict:
    """Scan scratch/t95..t143/out/DONE.md and deliverable manifests."""
    catalog: dict[str, dict] = {}
    for n in range(95, 144):
        task = f"t{n}"
        tdir = ROOT / "scratch" / task
        entry: dict = {"task": task, "dir_exists": tdir.is_dir()}
        if not tdir.is_dir():
            catalog[task] = entry
            continue
        outdir = tdir / "out"
        done_path = outdir / "DONE.md"
        entry["out_exists"] = outdir.is_dir()
        entry["has_done"] = done_path.is_file()
        entry["done_first10"] = []
        if entry["has_done"]:
            text = done_path.read_text(encoding="utf-8", errors="replace")
            entry["done_first10"] = text.splitlines()[:10]
        # Deliverable manifest: every .json/.md under out/ (skip oversized binaries).
        deliverables: dict[str, dict] = {}
        skipped: list[str] = []
        if outdir.is_dir():
            for p in sorted(outdir.rglob("*")):
                if not p.is_file():
                    continue
                suf = p.suffix.lower()
                if suf in (".bin", ".pkl", ".sqlite"):
                    try:
                        if p.stat().st_size > BIG_SKIP_BYTES:
                            skipped.append(str(p.relative_to(outdir)))
                    except OSError:
                        skipped.append(str(p.relative_to(outdir)))
                    continue
                if suf not in (".json", ".md"):
                    continue
                try:
                    st = p.stat()
                    deliverables[str(p.relative_to(outdir))] = {
                        "bytes": st.st_size,
                        "sha256": sha256_of(p),
                    }
                except OSError as exc:  # noqa: BLE001
                    deliverables[str(p.relative_to(outdir))] = {"error": str(exc)}
        entry["deliverables"] = deliverables
        entry["deliverable_count"] = len(deliverables)
        entry["skipped_oversized"] = skipped
        catalog[task] = entry
    return catalog


def protected_paths_clean() -> dict:
    try:
        proc = subprocess.run(
            ["git", "status", "--short", *PROTECTED],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output = proc.stdout + proc.stderr
        clean = proc.returncode == 0 and not proc.stdout.strip()
        return {"clean": clean, "exit_code": proc.returncode, "output": output.strip()}
    except Exception as exc:  # noqa: BLE001
        return {"clean": False, "error": f"{type(exc).__name__}: {exc}", "output": ""}


def build_report(matrix: dict) -> str:
    lines: list[str] = []
    lines.append("# t144 Wave 13+14 Regression Audit")
    lines.append("")
    lines.append(f"Python: 3.12  |  timeout: {TIMEOUT_S}s per script  |  cwd: `{ROOT}`")
    lines.append("")
    lines.append("## 1. Regression checks (Wave 13+14 scripts)")
    lines.append("")
    lines.append("| # | script | args | exit_code | elapsed_s | pass | timeout | stdout last 3 lines |")
    lines.append("|---|--------|------|-----------|-----------|------|---------|---------------------|")
    for i, s in enumerate(matrix["scripts"], 1):
        out = " / ".join(s["stdout_last3"]).replace("|", "\\|")[:80]
        lines.append(
            f"| {i} | {s['script']} | {', '.join(s['args']) or '-'} | "
            f"{s['exit_code']} | {s['elapsed_s']} | {'YES' if s['pass'] else 'NO'} | "
            f"{'YES' if s['timeout'] else 'no'} | {out} |"
        )
    lines.append("")
    lines.append(f"- scripts run: {matrix['script_total']}")
    lines.append(f"- passed: {matrix['script_pass']}")
    lines.append(f"- failed: {matrix['script_fail']}")
    lines.append("")
    lines.append("## 2. Protected-path clean check")
    lines.append("")
    pp = matrix["protected_paths"]
    lines.append(f"- paths: {', '.join(PROTECTED)}")
    lines.append(f"- clean: {'YES' if pp['clean'] else 'NO'}")
    if pp.get("output"):
        lines.append(f"- git output: `{pp['output']}`")
    lines.append("")
    lines.append("## 3. Completed task catalog (scratch/t95..t143/out/DONE.md)")
    lines.append("")
    lines.append("| task | has DONE.md | first line | deliverables |")
    lines.append("|------|-------------|------------|--------------|")
    cat = matrix["done_catalog"]
    for task in sorted(cat, key=lambda k: int(k[1:])):
        e = cat[task]
        if not e["dir_exists"]:
            lines.append(f"| {task} | dir missing | - | - |")
            continue
        first = (e["done_first10"][:1] or ["-"])[0].replace("|", "\\|")[:70]
        lines.append(
            f"| {task} | {'YES' if e['has_done'] else 'no'} | {first} | {e['deliverable_count']} |"
        )
    lines.append("")
    lines.append(f"- tasks with DONE.md: {matrix['done_count']} / {matrix['done_total']}")
    lines.append("")
    lines.append("## 4. SHA-256 deliverable manifest")
    lines.append("")
    lines.append("See `regression_matrix.json` for per-file SHA-256 + byte size of every "
                 "`.json`/`.md` under each `scratch/t*/out/` (t95..t143). Oversized "
                 "`.bin`/`.pkl`/`.sqlite` (> 50 MB) are skipped.")
    return "\n".join(lines) + "\n"


def build_done_md(matrix: dict, selftest_ok: bool) -> str:
    lines = []
    lines.append("DONE type=t144")
    lines.append("")
    lines.append(f"Pass count: {matrix['script_pass']}/{matrix['script_total']}")
    lines.append(f"protected-path clean: {'True' if matrix['protected_paths']['clean'] else 'False'}")
    lines.append(f"--selftest: {'PASS' if selftest_ok else 'FAIL'}")
    lines.append("")
    lines.append(f"Scripts passed: {matrix['script_pass']} of {matrix['script_total']}")
    lines.append(f"Failed scripts: {[s['script'] for s in matrix['scripts'] if not s['pass']]}")
    lines.append(f"Tasks with DONE.md (t95-t143): {matrix['done_count']} / {matrix['done_total']}")
    lines.append("")
    lines.append("Deliverables: scratch/t144/out/regression_matrix.json, REPORT.md, DONE.md")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Wave 13+14 regression audit (t144).")
    ap.add_argument("--selftest", action="store_true", help="run full regression plus internal assertions")
    a = ap.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)

    # 1. Run every Wave 13+14 script.
    script_results = [run_one(script, args) for script, args in SCRIPTS]
    script_pass = sum(1 for s in script_results if s["pass"])
    script_fail = len(script_results) - script_pass

    # 2. DONE.md catalog + SHA-256 manifest.
    catalog = scan_done_catalog()
    done_count = sum(1 for e in catalog.values() if e.get("has_done"))
    done_total = len(catalog)

    # 3. Protected-path check.
    protected = protected_paths_clean()

    matrix = {
        "task": "t144",
        "python": "3.12",
        "timeout_s": TIMEOUT_S,
        "scripts": script_results,
        "script_total": len(script_results),
        "script_pass": script_pass,
        "script_fail": script_fail,
        "done_catalog": catalog,
        "done_count": done_count,
        "done_total": done_total,
        "protected_paths": protected,
        "protected_clean": bool(protected.get("clean")),
    }

    matrix_path = OUTDIR / "regression_matrix.json"
    matrix_path.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")

    report_path = OUTDIR / "REPORT.md"
    report_path.write_text(build_report(matrix), encoding="utf-8")

    # 4. Self-test assertions.
    selftest_ok = True
    assertions = []
    try:
        assert matrix_path.is_file(), "regression_matrix.json missing"
        loaded = json.loads(matrix_path.read_text(encoding="utf-8"))
        assert loaded["script_total"] == 18
        assert loaded["script_pass"] == script_pass
        assert report_path.is_file(), "REPORT.md missing"
        done_path = OUTDIR / "DONE.md"
        done_text = build_done_md(matrix, selftest_ok)
        done_path.write_text(done_text, encoding="utf-8")
        first_line = done_text.splitlines()[0]
        assert first_line == "DONE type=t144", f"bad DONE.md first line: {first_line!r}"
        assert f"{script_pass}/18" in done_text
        assertions.append("DONE.md first line == DONE type=t144")
        assertions.append(f"pass count {script_pass}/18 present in DONE.md")
        if not protected.get("clean"):
            selftest_ok = False
            assertions.append("FAIL: protected paths not clean")
        if script_fail:
            assertions.append(f"FAIL: {script_fail} script(s) did not pass")
        else:
            assertions.append("all 18 scripts passed")
    except Exception as exc:  # noqa: BLE001
        selftest_ok = False
        assertions.append(f"SELFTEST ASSERTION ERROR: {type(exc).__name__}: {exc}")

    # Rewrite DONE.md with final selftest status if it changed.
    done_path = OUTDIR / "DONE.md"
    done_text = build_done_md(matrix, selftest_ok)
    done_path.write_text(done_text, encoding="utf-8")

    # Console summary.
    print(json.dumps({
        "task": "t144",
        "scripts_pass": f"{script_pass}/{len(script_results)}",
        "failed": [s["script"] for s in script_results if not s["pass"]],
        "done_tasks": f"{done_count}/{done_total}",
        "protected_clean": bool(protected.get("clean")),
        "selftest": "PASS" if selftest_ok else "FAIL",
        "outdir": str(OUTDIR),
    }, indent=2, ensure_ascii=False))
    return 0 if selftest_ok else 1


if __name__ == "__main__":
    sys.exit(main())
