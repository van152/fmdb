#!/usr/bin/env python3
"""Repository hygiene check: no hardcoded absolute paths in scripts, pointers valid.

Usage:
    python scripts/check_repo.py
Exit codes: 0 clean / 1 issues found / 2 fatal.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"fm24_config.py", "check_repo.py"}
MARKERS = ("tmp2b", "SteamLibrary", "Program Files", "Users\\\\oak", "Users/oak")


def is_absolute_path(value: str) -> bool:
    if not isinstance(value, str) or len(value) < 4 or value[1:3] not in (":\\", ":/"):
        return False
    return value[0].isalpha()


def docstring_ids(tree: ast.AST) -> set[int]:
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr):
                value = body[0].value
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    ids.add(id(value))
    return ids


def scan_paths() -> list[str]:
    issues = []
    for path in sorted((ROOT / "scripts").glob("*.py")):
        if path.name in SKIP:
            continue
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
        docs = docstring_ids(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or id(node) in docs:
                continue
            value = node.value
            if isinstance(value, str) and is_absolute_path(value) and any(m in value for m in MARKERS):
                issues.append(f"{path.relative_to(ROOT)}:{node.lineno}: hardcoded path {value[:80]}")
    return issues


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_pointers() -> list[str]:
    issues = []
    schema = ROOT / "reports" / "club_nation_subtable_schema.json"
    if not schema.is_file():
        return [f"missing {schema.relative_to(ROOT)}"]
    doc = json.loads(schema.read_text(encoding="utf-8"))
    for key in ("other_tables_schema", "xml_denominator_coverage"):
        ptr = doc.get("pointer_artifacts", {}).get(key, {})
        target = ROOT / ptr.get("path", "")
        if not target.is_file():
            issues.append(f"pointer target missing: {ptr.get('path')}")
        elif sha256(target) != ptr.get("sha256"):
            issues.append(f"pointer SHA drift: {ptr.get('path')}")
    return issues


def main() -> int:
    issues = scan_paths() + scan_pointers()
    if issues:
        print("check_repo: FAIL")
        for line in issues[:50]:
            print("  " + line)
        print(f"  total: {len(issues)}")
        return 1
    print("check_repo: PASS (no hardcoded paths, schema pointers consistent)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
