"""Resolve entity vtable slots and reader entry from editor.exe."""
from __future__ import annotations
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *

VTYPES = (19, 41, 23, 8, 2, 18, 24, 6)


def census():
    return {x["type_id"]: x for x in json.loads(T01H.read_text(encoding="utf-8"))["census"]}


def vtable(pe, vptr_off, n=24):
    out = []
    for i in range(n):
        va = pe.qword(vptr_off + i * 8)
        out.append({"slot": i, "va": hex(va), "target_file_offset":
                    None if pe.off(va) is None else hex(pe.off(va))})
    return out


def entity_info(pe, tid):
    c = census()[tid]
    cc = c["constructor_classes"][0]
    vptr = int(cc["rtti"]["vptr_file_offset"], 16)
    vt = vtable(pe, vptr)
    entry = vt[19]["target_file_offset"]
    entry_off = int(entry, 16) if entry else None
    unwrapped = pe.resolve_jmp(entry_off) if entry_off is not None else None
    return {
        "type_id": tid,
        "entity": (cc["entity"]["matched"] or [None])[0],
        "rtti": cc["rtti"]["name"],
        "vptr_file_offset": hex(vptr),
        "getter_entry": vt[2]["target_file_offset"],
        "getter_unwrapped": hex(pe.resolve_jmp(int(vt[2]["target_file_offset"], 16)))
        if vt[2]["target_file_offset"] else None,
        "reader_entry": entry,
        "reader_unwrapped": hex(unwrapped) if unwrapped else None,
        "allocation_bytes": [a["size"] for a in c["allocation"]],
    }
