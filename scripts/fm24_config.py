#!/usr/bin/env python3
"""Central path and dependency configuration for fm24-db scripts.

All new code must import this module instead of hardcoding D:\\ / Z:\\ paths.
Every default can be overridden with an environment variable so the repository
can be cloned to another machine without editing source files.

Environment variables:
    FM24_ROOT         repository root
    FM24_LEGACY_DIR   old evidence/binary input directory
    FM24_GAME_DIR     game installation directory
    FM24_DATA_DIR     directory holding the raw .dat inputs (git-ignored)
    FM24_VENDOR_DIR   directory containing vendored Python packages (zstandard)
    FM24_IDA_LIB_DIR  IDA Python library directory
    FM24_PYTHON       Python launcher used by subprocesses (default: py -V:3.12)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("FM24_ROOT", Path(__file__).resolve().parent.parent)).resolve()
SCRIPTS_DIR = ROOT / "scripts"
REPORTS_DIR = ROOT / "reports"
EVIDENCE_DIR = ROOT / "evidence"
SCRATCH_DIR = ROOT / "scratch"

LEGACY_DIR = Path(os.environ.get("FM24_LEGACY_DIR", r"D:\tmp2b\fm24")).resolve()
GAME_DIR = Path(os.environ.get("FM24_GAME_DIR",
                               r"Z:\SteamLibrary\steamapps\common\Football Manager 2024"))
GAME_DB_DIR = GAME_DIR / "data" / "database" / "db" / "2430" / "2430_fm"
DATA_DIR = Path(os.environ.get("FM24_DATA_DIR", SCRATCH_DIR / "data"))
INPUT_DIR = LEGACY_DIR / "input"
IDA_DIR = LEGACY_DIR / "ida"
VENDOR_DIR = Path(os.environ.get("FM24_VENDOR_DIR", LEGACY_DIR / "tools" / "python"))
LEGACY_TOOLS_DIR = Path(os.environ.get("FM24_LEGACY_TOOLS_DIR", r"D:\tmp2b\tools\python"))
IDA_LIB_DIR = Path(os.environ.get("FM24_IDA_LIB_DIR",
                                  r"C:\Program Files\IDA Professional 9.4\idalib\python"))
MINGW_ZSTD_DLL = Path(r"C:\Program Files\Git\mingw64\bin\libzstd.dll")
EDITOR_SCHEMA_FIELDS_MD = LEGACY_DIR / "reports" / "EDITOR_SCHEMA_FIELDS.md"
MASTER_SCHEMA_JSON = EVIDENCE_DIR / "fm24" / "reports" / "editor_schema" / "master.json"

EDITOR_EXE = INPUT_DIR / "editor.exe"
FM_EXE = INPUT_DIR / "fm.exe"
IDA_DB = IDA_DIR / "editor_merge_v2.i64"
OLD_DBDAT_READER = LEGACY_DIR / "scripts" / "modding_read_dbdat.py"
LANG_DB_DAT = INPUT_DIR / "lang_db_2400.dat"

_PYTHON = os.environ.get("FM24_PYTHON", "py -V:3.12").split()


def python_cmd(*args: str) -> list[str]:
    """Command line for launching a sibling script with the pinned Python."""
    return [*_PYTHON, "-B", *args]


def ensure_vendor() -> None:
    """Put the vendored packages (notably zstandard) on sys.path."""
    candidate = str(VENDOR_DIR)
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


def missing_inputs() -> list[str]:
    """Paths that are expected to exist for full (non-selftest) runs."""
    candidates = [DATA_DIR, INPUT_DIR, VENDOR_DIR]
    return [str(p) for p in candidates if not p.exists()]


if __name__ == "__main__":
    for name in ("ROOT", "LEGACY_DIR", "GAME_DIR", "DATA_DIR", "INPUT_DIR",
                 "VENDOR_DIR", "EDITOR_EXE", "FM_EXE"):
        print(f"{name}={globals()[name]}")
    missing = missing_inputs()
    print("missing_inputs=" + (", ".join(missing) if missing else "none"))
