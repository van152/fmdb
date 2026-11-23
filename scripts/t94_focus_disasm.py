"""PE unwind-table lookup for t94 (adapted from old-workspace focus_disasm.py).

Static-only: parses .pdata (DATA_DIRECTORY[3]) of the target PE to give exact
function bounds for a VA. Never launches anything.
"""
from __future__ import annotations

import bisect
import struct
from pathlib import Path

import pefile

DEFAULT_PE = Path(r'D:/tmp2b/fm24/input/editor.exe')


def _load_pe(pe_path: Path):
    pe = pefile.PE(str(pe_path), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    directory = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
    records = sorted(struct.iter_unpack('<III', pe.get_data(directory.VirtualAddress, directory.Size)))
    return image_base, records


IMAGE_BASE, RECORDS = _load_pe(DEFAULT_PE)
STARTS = [r[0] for r in RECORDS]


def set_pe(pe_path) -> None:
    """Point the unwind-table lookup at another input binary."""
    global IMAGE_BASE, RECORDS, STARTS
    IMAGE_BASE, RECORDS = _load_pe(Path(pe_path))
    STARTS = [r[0] for r in RECORDS]


def owner(va: int):
    """Return the PE RuntimeFunction triple (start_rva, end_rva, unwind_rva) covering a VA, or None."""
    rva = va - IMAGE_BASE
    index = bisect.bisect_right(STARTS, rva) - 1
    if index >= 0:
        record = RECORDS[index]
        if record[0] <= rva < record[1]:
            return record
    return None
