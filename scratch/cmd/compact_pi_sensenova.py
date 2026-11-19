#!/usr/bin/env python3
"""Compact idle project Pi sessions through SenseNova2 only, at a fixed rate."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

ROOT = Path(r"D:\tmp2b\fm24-db")
SESSION_DIR = ROOT / "scratch" / "t02" / "pi-sessions"
EXTENSION = Path(r"Z:\aiproject\pi-extend\extensions\sensenova2\index.ts")
BASE_CONFIG = Path(r"Z:\aiproject\pi-extend\sensenova2.json")
PI = shutil.which("pi") or "pi"
INTERVAL_SECONDS = 30
REQUEST_TIMEOUT_SECONDS = 900
ACTIVE_SESSION_IDS = {
    "t24-club-cursor-openai-codex",
    "t25-nation-fields-hiyo-key2",
    "t26-hist-people-devseek",
}
SKIP_COMPACTED = True


def normpath(value: str) -> str:
    return os.path.normcase(os.path.normpath(value))


def load_session(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or rows[0].get("type") != "session":
        raise ValueError(f"invalid session header: {path.name}")
    return rows[0], rows


def discover_sessions() -> list[tuple[Path, dict[str, Any], list[dict[str, Any]]]]:
    found = []
    target_cwd = normpath(str(ROOT))
    for path in sorted(SESSION_DIR.glob("*.jsonl")):
        header, rows = load_session(path)
        if normpath(header.get("cwd", "")) == target_cwd:
            found.append((path, header, rows))
    return found


def make_sensenova_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    candidates = [item for item in config.get("candidates", []) if item.get("provider") == "sensenova"]
    if len(candidates) != 1:
        raise ValueError(f"expected exactly one SenseNova candidate, found {len(candidates)}")
    config["candidates"] = candidates
    config["retryRounds"] = 0
    config["cacheDir"] = False
    config["liveProgress"] = False
    return config


def read_rpc(pipe, events: list[dict[str, Any]], done: threading.Event) -> None:
    try:
        for line in iter(pipe.readline, ""):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            events.append(item)
            if item.get("type") == "response" and item.get("id") == "compact-request":
                done.set()
                return
    finally:
        done.set()


def run_compact(session_path: Path, config_path: Path) -> dict[str, Any]:
    env = os.environ.copy()
    if not env.get("SENSENOVA_API_KEY"):
        return {"success": False, "error": "SENSENOVA_API_KEY is absent in launcher environment"}
    env["PI_SENSENOVA2_CONFIG"] = str(config_path)
    argv = [
        PI, "--mode", "rpc", "--no-extensions", "--extension", str(EXTENSION),
        "--no-mcp", "--no-context-files", "--no-skills", "--approve",
        "--session", str(session_path),
    ]
    try:
        proc = subprocess.Popen(
            argv, cwd=ROOT, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1,
        )
    except OSError as exc:
        return {"success": False, "error": f"pi launch failed: {exc}"}
    assert proc.stdin is not None and proc.stdout is not None
    records: list[dict[str, Any]] = []
    done = threading.Event()
    reader = threading.Thread(target=read_rpc, args=(proc.stdout, records, done), daemon=True)
    reader.start()
    try:
        proc.stdin.write(json.dumps({"id": "compact-request", "type": "compact"}) + "\n")
        proc.stdin.flush()
        if not done.wait(REQUEST_TIMEOUT_SECONDS):
            proc.terminate()
            proc.wait(timeout=15)
            return {"success": False, "error": "SenseNova2 RPC compact timed out",
                    "events": [item.get("type") for item in records]}
    except (BrokenPipeError, OSError) as exc:
        try:
            proc.terminate()
        except OSError:
            pass
        proc.wait(timeout=15)
        return {"success": False, "error": f"RPC stdin failed: {exc}",
                "events": [item.get("type") for item in records]}
    finally:
        try:
            proc.stdin.close()
        except OSError:
            pass
    try:
        returncode = proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=15)
        return {"success": False, "error": "pi did not exit after RPC response",
                "events": [item.get("type") for item in records]}
    stderr = proc.stderr.read()[-2000:] if proc.stderr else ""
    response = next((item for item in records
                     if item.get("type") == "response" and item.get("id") == "compact-request"), None)
    header, rows = load_session(session_path)
    compactions = [item for item in rows if item.get("type") == "compaction"]
    entry = compactions[-1] if compactions else None
    new_entry = bool(entry and entry.get("fromHook") is True)
    response_error = None if response is None else response.get("error")
    no_op_small = bool(response and response.get("success") is False and returncode == 0 and
                        response_error == "Nothing to compact (session too small)" and not new_entry)
    success = bool(response and response.get("success") is True and returncode == 0 and new_entry)
    return {
        "success": success,
        "no_op_small": no_op_small,
        "response_success": None if response is None else response.get("success"),
        "error": response_error,
        "returncode": returncode,
        "compaction_count": len(compactions),
        "new_entry_from_sensenova2_hook": new_entry,
        "tokens_before": entry.get("tokensBefore") if entry else None,
        "summary_chars": len(entry.get("summary", "")) if entry else 0,
        "events": [item.get("type") for item in records
                   if item.get("type") in ("compaction_start", "compaction_end", "response")],
        "stderr": stderr,
    }


def test_copy() -> int:
    source = next(path for path, header, _ in discover_sessions()
                  if header.get("id") == "t20-subtable-cursor-openai-codex")
    with tempfile.TemporaryDirectory(prefix="pi-sensenova2-test-") as temp:
        temp_dir = Path(temp)
        copy = temp_dir / source.name
        shutil.copy2(source, copy)
        config = make_sensenova_config(BASE_CONFIG)
        config_path = temp_dir / "sensenova2-only.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        before_hash = hashlib.sha256(copy.read_bytes()).hexdigest()
        result = run_compact(copy, config_path)
        result.update({
            "test_session_copy": source.name,
            "original_unchanged_by_test": hashlib.sha256(source.read_bytes()).hexdigest() == before_hash,
            "provider_candidates": [item["provider"] for item in config["candidates"]],
            "retry_rounds": config["retryRounds"],
        })
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["success"] and result["original_unchanged_by_test"] else 1


def active_session_ids() -> set[str]:
    ps_script = (
        "$p=Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and "
        "$_.CommandLine -like '*pi-coding-agent*' }; "
        "$p | ForEach-Object { $_.CommandLine }"
    )
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script],
                         capture_output=True, text=True, check=False)
    command_lines = proc.stdout.splitlines()
    active = set(ACTIVE_SESSION_IDS)
    token_re = re.compile(r"--session-id(?:=|\s+)(\S+)")
    for line in command_lines:
        for match in token_re.finditer(line):
            active.add(match.group(1).strip('"'))
    return active


def append_log(log_path: Path, record: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def logged_statuses(log_path: Path) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    if not log_path.is_file():
        return latest
    for line_no, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid compaction checkpoint at line {line_no}: {exc}") from exc
        session_id = item.get("session")
        if session_id:
            latest[session_id] = item
    return latest


def run_batch(interval: int, limit: int | None, log_path: Path) -> int:
    config = make_sensenova_config(BASE_CONFIG)
    if len(config["candidates"]) != 1 or config["candidates"][0].get("provider") != "sensenova":
        raise ValueError("guard failed: compaction config must use SenseNova only")
    active = active_session_ids()
    checkpoint = logged_statuses(log_path)
    candidates = []
    skipped = []
    for path, header, rows in discover_sessions():
        session_id = header.get("id", "")
        if any(item.get("type") == "compaction" for item in rows):
            skipped.append({"session": session_id, "status": "skipped_already_compacted"})
        elif session_id in active:
            skipped.append({"session": session_id, "status": "skipped_active_pi_session"})
        elif session_id in checkpoint:
            previous = checkpoint[session_id]
            skipped.append({"session": session_id, "status": "skipped_checkpoint_" + str(previous.get("status", "unknown")),
                            "previous_error": previous.get("error")})
        else:
            candidates.append((path, session_id))
    if limit is not None:
        candidates = candidates[:limit]
    run_id = time.strftime("%Y%m%dT%H%M%S")
    print(json.dumps({"run_id": run_id, "eligible": len(candidates), "skipped": skipped,
                      "provider": "sensenova", "model": config["candidates"][0]["model"],
                      "interval_seconds": interval}, ensure_ascii=False), flush=True)
    with tempfile.TemporaryDirectory(prefix="pi-sensenova2-batch-") as temp:
        config_path = Path(temp) / "sensenova2-only.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        last_start: float | None = None
        results = []
        for path, session_id in candidates:
            if last_start is not None:
                remaining = interval - (time.monotonic() - last_start)
                if remaining > 0:
                    time.sleep(remaining)
            last_start = time.monotonic()
            append_log(log_path, {"run_id": run_id, "session": session_id, "status": "started",
                                  "provider": "sensenova", "model": config["candidates"][0]["model"],
                                  "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
            before_header, before_rows = load_session(path)
            before_ids = {item.get("id") for item in before_rows}
            result = run_compact(path, config_path)
            _, after_rows = load_session(path)
            appended = [item for item in after_rows if item.get("type") == "compaction"
                        and item.get("id") not in before_ids]
            if len(appended) != 1:
                result["success"] = False
                result["error"] = result.get("error") or f"expected one newly appended compaction entry; found {len(appended)}"
            if result.get("no_op_small"):
                status = "skipped_too_small"
            else:
                status = "compacted" if result.get("success") else "failed"
            result.update({"run_id": run_id, "session": session_id,
                           "status": status,
                           "new_compaction_entries": len(appended), "provider": "sensenova",
                           "model": config["candidates"][0]["model"]})
            results.append(result)
            append_log(log_path, result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
            if status == "failed":
                break
    summary = {"run_id": run_id, "attempted": len(results),
               "succeeded": sum(item.get("status") == "compacted" for item in results),
               "failed": sum(item.get("status") == "failed" for item in results),
               "pending_or_uncertain": sum(item.get("status") == "started" for item in checkpoint.values()),
               "skipped_too_small": sum(item.get("status") == "skipped_too_small" for item in results),
               "remaining_unattempted": max(0, len(candidates) - len(results)),
               "already_compacted_skipped": sum(item["status"] == "skipped_already_compacted" for item in skipped),
               "active_skipped": sum(item["status"] == "skipped_active_pi_session" for item in skipped),
               "log": str(log_path)}
    print(json.dumps({"summary": summary}, ensure_ascii=False), flush=True)
    return 0 if summary["failed"] == 0 and summary["remaining_unattempted"] == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--test", action="store_true", help="compact only an isolated session copy")
    modes.add_argument("--run", action="store_true", help="compact eligible project sessions")
    parser.add_argument("--interval-seconds", type=int, default=30,
                        help="minimum start-to-start interval; default is two sessions per minute")
    parser.add_argument("--limit", type=int, help="limit number of sessions for a trial batch")
    parser.add_argument("--log", type=Path,
                        default=ROOT / "scratch" / "cmd" / "sensenova2_compaction.jsonl",
                        help="append per-session results here")
    args = parser.parse_args()
    if args.interval_seconds < 30:
        parser.error("interval must be at least 30 seconds")
    if args.test:
        return test_copy()
    try:
        return run_batch(args.interval_seconds, args.limit, args.log)
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
