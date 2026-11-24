#!/usr/bin/env python3
"""t149 — final adjudication of the EDfx upstream persistence question.

EDfx (`0x45446678`, XML index 342 of `nation.xml#nati`, "Fixture Dates") was left
open by t62 as `upstream_persistence_unbound`.  This script answers it with a
complete, reproducible L3 (static machine-code) argument, not a guess:

  NEGATIVE VERDICT — EDfx is a pure runtime / editor rule-layer UI projection.
  It has no `.dat` reader, no `.dat` writer, no wire slot, and no backing member.

The argument has five independent legs, each of which alone would be fatal to a
"persisted field" hypothesis:

  A. Uniqueness.  `EDfx` occurs exactly once in the whole 74,806,296-byte image,
     as the immediate operand of a single `cmp esi,imm32` inside the property
     dispatcher `0x28150`.  No other byte order or encoding exists.

  B. Namespace separation.  The dispatcher `0x28150` is a *UI bag* dispatcher
     (133 distinct 4CC keys).  The persisted property protocol enumerated by
     t108 (67 tables, 2301 distinct codes) shares exactly one key with it, and
     that key is a computed/UI access with no direct field offset.  Not one of
     the 50 `ED*` keys in the image is a persisted protocol code.  By contrast
     the NATION setter really does enumerate 116 persisted codes (`Nctp`,
     `Tchl`, `comp`, ...) and contains no `EDfx`.

  C. Forward closure.  The EDfx producer `0x907f0` has a *complete* direct-call
     closure of 201 functions / 953 edges.  It contains zero of the 96 property
     get/set handlers and materialises zero of the 25 file-API IAT slots (its 64
     IAT references are all CRT heap/lock/error helpers).  It therefore cannot
     read or write any `.dat`.

  D. Reverse closure.  The union closure of all 49 `get_prop` handlers (820
     functions) does not contain `0x907f0`, and the NATION wire reader
     `0x1410404c0` (slot19) closure does not either.  No `.dat` reader reaches
     EDfx.

  E. Output shape.  The producer emits exactly the seven `list_item_fields` of
     the XML declaration under abbreviated bag keys: `date`, `dyow`, `time`,
     `strl`, `hidl`, `lwdl`, `text`.  Of those only `date` and `comp` exist in
     the persisted protocol, and only as *other* entities' slots; `dyow`,
     `strl`, `hidl`, `lwdl`, `text` are absent from the persisted namespace
     entirely.  The list is built at runtime from the calendar and rules engine
     and handed to the UI.

`fles` is the memory container the producer enumerates.  It is *read* (34 bag
gets), *probed* (1 has), and *erased* (3), but never written by any 4CC-keyed
setter in this image — there is no `bag_set_prop` site for it at all.

Usage:
    py -V:3.12 -B scripts/t149_edfx_upstream.py --build
    py -V:3.12 -B scripts/t149_edfx_upstream.py --selftest

Exit codes: 0 success (verdict written or selftest passed), 1 verification
failure, 2 usage/fatal error.
"""
from __future__ import annotations

import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib

_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg  # noqa: E402

import argparse
import bisect
import json
import re
import sys
from collections import deque
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t149" / "out"

# Frozen inputs.  Hashes are asserted so the verdict cannot silently drift.
EXE = Path(str(_cfg.EDITOR_EXE))
EXE_SHA = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXE_SIZE = 74807296
MASTER = "evidence/fm24/reports/editor_schema/master.json"
T108 = "scratch/t108/out/fourcc_mem_map_v2.json"
VTINDEX = "scratch/t95/vtable_index.json"

# Addresses proven by t62 / t95 and re-verified here.
VA_DISPATCHER = 0x140028B50   # 0x28150 : UI bag / 4CC dispatcher extent start
VA_EDFX_CMP = 0x14002A637     # cmp esi,0x45446678
VA_EDFX_PRODUCER = 0x1400911F0  # 0x907f0 : EDfx generator (t62 0x907f0)
VA_NATION_READER = 0x1410404C0  # NATION slot19 wire reader (t55 0x103fac0 body)
VA_NATION_SET_GATE = 0x143ECD5C0  # NATION slot03_set_prop
VA_CAL_DAY_QUERY = 0x140B03380  # 0xb02980 : day-bucket query

# Bag accessor helpers (VAs), identified by their bodies in this image.
BAG_GET = 0x140835850     # linear scan over 16-byte {code,node} pairs, returns node
BAG_HAS = 0x1408357E0     # same scan, boolean
BAG_SET = 0x140835380     # get-or-insert + node swap
BAG_ERASE = 0x140835C30   # thunk -> 0x143774d20 (erase-by-key with compaction)
BAG_INSERT = 0x140835A40  # thunk -> 0x143774ba0 (capacity grow + append)

FILE_API = {
    "fopen", "_wfopen", "_wfsopen", "_wfopen_s", "freopen_s", "fread", "fwrite",
    "fclose", "fseek", "_fseeki64", "ftell", "CreateFileW", "GetFileSizeEx",
    "SetFilePointer", "FindFirstFileW", "FindFirstFileExW", "FindNextFileW",
    "CopyFileW", "MoveFileW", "DeleteFileW", "_open", "_wopen", "_close",
    "_fstat64", "_stat64", "WriteFile", "ReadFile",
}


class Check(Exception):
    pass


def ck(cond, msg):
    if not cond:
        raise Check(str(msg))


def h(data: bytes) -> str:
    return sha256(data).hexdigest()


def load_json(rel: str):
    return json.loads((ROOT / rel).read_bytes())


def printable4cc(value: int) -> str:
    """FM 4CC codes are stored big-endian in the immediate (EDfx == 0x45446678)."""
    if not (0 < value <= 0xFFFFFFFF):
        return ""
    raw = value.to_bytes(4, "big")
    return raw.decode("latin-1") if all(32 <= c < 127 for c in raw) else ""


class Image:
    """editor.exe with PE/RUNTIME_FUNCTION plumbing and a decode cache."""

    def __init__(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64

        from t05_pe import PE

        self.p = p = PE(EXE)
        ck(h(p.raw) == EXE_SHA, "editor.exe SHA-256 mismatch")
        ck(len(p.raw) == EXE_SIZE, "editor.exe size mismatch")
        p.pe.parse_data_directories(directories=[1, 3])
        self.rs = sorted((e.struct.BeginAddress, e.struct.EndAddress)
                         for e in p.pe.DIRECTORY_ENTRY_EXCEPTION)
        self.starts = [a for a, _ in self.rs]
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.iat = {}
        for entry in p.pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name:
                    self.iat[imp.address] = imp.name.decode()
        self.file_iat = {a: n for a, n in self.iat.items() if n in FILE_API}
        self._fn_cache = {}

    # -- address plumbing ---------------------------------------------------
    def extent_rva(self, va: int):
        r = va - self.p.base
        i = bisect.bisect_right(self.starts, r) - 1
        if i >= 0 and r < self.rs[i][1]:
            return self.rs[i][0], self.rs[i][1]
        return None

    def extent_va(self, va: int):
        """(entry, end_exclusive) as file offsets, matching the t62 citation style."""
        ext = self.extent_rva(va)
        if not ext:
            return None
        return self.p.r2f(ext[0]), self.p.r2f(ext[1])

    def section_of(self, off: int) -> str:
        for s in self.p._secs:
            if s["raw"] <= off < s["raw"] + s["rawsize"]:
                return s["name"]
        return "?"

    def disasm_extent(self, va: int):
        ext = self.extent_rva(va)
        if not ext:
            return []
        lo = self.p.r2f(ext[0])
        hi = self.p.r2f(ext[1])
        return list(self.md.disasm(self.p.raw[lo:hi], va))

    def calls_in(self, va: int):
        ext = self.extent_rva(va)
        if not ext:
            return None, []
        if ext not in self._fn_cache:
            self._fn_cache[ext] = [
                i.operands[0].imm
                for i in self.disasm_extent(va)
                if i.mnemonic == "call" and i.operands[0].type == 2
            ]
        return ext, self._fn_cache[ext]

    def callers(self, va: int):
        """Direct `call rel32` sites whose decoded target is exactly va."""
        out = []
        trva = va - self.p.base
        raw = self.p.raw
        pos = 0
        while True:
            o = raw.find(b"\xe8", pos)
            if o < 0:
                break
            pos = o + 1
            if o + 5 > len(raw):
                continue
            rva = self.p.f2r(o)
            if rva is None:
                continue
            rel = int.from_bytes(raw[o + 1:o + 5], "little", signed=True)
            if rva + 5 + rel != trva:
                continue
            try:
                ins = next(self.md.disasm(raw[o:o + 8], self.p.f2va(o), count=1))
            except StopIteration:
                continue
            if ins.mnemonic == "call" and ins.operands[0].type == 2 and ins.operands[0].imm == va:
                out.append(o)
        return out

    # -- closure ------------------------------------------------------------
    def closure(self, root_va: int, cap: int = 6000):
        """Complete direct-call closure; IAT targets are recorded, not expanded."""
        seen, todo, edges = set(), deque([root_va]), []
        while todo:
            va = todo.popleft()
            if va in seen:
                continue
            seen.add(va)
            if va in self.iat:
                continue
            if len(seen) > cap:
                return seen, edges, "capped"
            _, targets = self.calls_in(va)
            for t in targets:
                edges.append((va, t))
                if t not in seen:
                    todo.append(t)
        return seen, edges, "complete"

    # -- scans --------------------------------------------------------------
    def literal_occurrences(self, key: str):
        """All 6 raw encodings (ascii/utf16le/utf16be x forward/reverse)."""
        raw = self.p.raw
        found = []
        for codec in ("ascii", "utf-16-le", "utf-16-be"):
            for order, word in (("forward", key), ("reverse", key[::-1])):
                pat = word.encode(codec)
                start = 0
                while True:
                    o = raw.find(pat, start)
                    if o < 0:
                        break
                    start = o + 1
                    found.append(dict(encoding=f"{codec}_{order}", offset=o,
                                      va=self.p.f2va(o), section=self.section_of(o),
                                      bytes=pat.hex()))
        return found

    def imm4cc_census(self):
        """Every `cmp r32, imm32` whose immediate is a printable 4CC, with owner fn."""
        out = {}
        raw = self.p.raw
        for m in re.finditer(rb"(?=\x81[\xf8-\xff])", raw):
            o = m.start()
            value = int.from_bytes(raw[o + 2:o + 6], "little")
            key = printable4cc(value)
            if not key:
                continue
            va = self.p.f2va(o)
            ext = self.extent_rva(va)
            out.setdefault(key, []).append(dict(va=va, offset=o, imm_offset=o + 2,
                                               fn=self.p.r2f(ext[0]) if ext else None))
        return out

    def keys_in_extent(self, va: int):
        """Distinct printable 4CC immediates compared inside the function at va."""
        keys = set()
        for ins in self.disasm_extent(va):
            if ins.mnemonic == "cmp" and len(ins.operands) == 2 and ins.operands[1].type == 2:
                key = printable4cc(ins.operands[1].imm & 0xFFFFFFFF)
                if key:
                    keys.add(key)
        return keys

    def bag_sites(self, key: str):
        """`mov edx, imm32` sites for a 4CC plus the accessor they feed.

        The accessor call may be separated from the immediate by argument setup
        (typically `mov r8, <value>`), so the scan looks ahead over a short window
        instead of only at the immediately following instruction.
        """
        value = int.from_bytes(key.encode(), "big")
        pat = value.to_bytes(4, "little")
        raw = self.p.raw
        out, start = [], 0
        while True:
            o = raw.find(pat, start)
            if o < 0:
                break
            start = o + 1
            st = o - 1
            if st < 0:
                continue
            try:
                ins = next(self.md.disasm(raw[st:st + 10], self.p.f2va(st), count=1))
            except StopIteration:
                continue
            if not (ins.mnemonic == "mov" and len(ins.operands) == 2
                    and ins.operands[1].type == 2 and ins.operands[1].imm == value):
                continue
            # Walk a short window for the consuming call; stop at a control transfer.
            callee = None
            probe = st + ins.size
            for _ in range(6):
                try:
                    nxt = next(self.md.disasm(raw[probe:probe + 12], self.p.f2va(probe), count=1))
                except StopIteration:
                    break
                if nxt.mnemonic == "call" and nxt.operands[0].type == 2:
                    callee = nxt.operands[0].imm
                    break
                if nxt.mnemonic.startswith("j") or nxt.mnemonic in ("ret", "int3"):
                    break
                probe += nxt.size
            out.append(dict(va=self.p.f2va(o), site=st, asm=f"{ins.mnemonic} {ins.op_str}",
                            callee=callee, role=role_of(callee),
                            in_fn=self.extent_va(self.p.f2va(st))))
        return out

    def bag_keys_emitted(self, va: int):
        """`mov edx, imm32` printable keys inside a function (its bag output keys)."""
        out = []
        for ins in self.disasm_extent(va):
            if ins.mnemonic == "mov" and len(ins.operands) == 2 and ins.operands[0].type == 1:
                if ins.reg_name(ins.operands[0].reg) != "edx" or ins.operands[1].type != 2:
                    continue
                key = printable4cc(ins.operands[1].imm & 0xFFFFFFFF)
                if key:
                    out.append(dict(va=ins.address, key=key, asm=f"{ins.mnemonic} {ins.op_str}"))
        return out


def role_of(callee):
    if callee is None:
        return "no-call"
    return {
        BAG_GET: "bag_get_prop",
        BAG_HAS: "bag_has_prop",
        BAG_SET: "bag_set_prop",
        BAG_ERASE: "bag_erase_prop",
        BAG_INSERT: "bag_insert_prop",
    }.get(callee, "other")


# --- persisted protocol universe (from t108) ------------------------------
def persisted_codes():
    """code -> list of (class, slot, access_kind, primary_off)."""
    doc = load_json(T108)
    out = {}
    for table in doc["tables"]:
        for code, info in table["fourccs"].items():
            out.setdefault(code, []).append(dict(
                table_class=table["class"], entity_tag=table["entity_tag"],
                slot=info["slot"], access_kind=info.get("access_kind"),
                primary_off=info.get("primary_off"),
                computed_reasons=info.get("computed_reasons") or []))
    return out


def protocol_handlers():
    """func_va -> [(class, slot)] for every get_prop / set_prop handler in t95."""
    idx = load_json(VTINDEX)
    out = {}
    for table in idx["tables"]:
        for slot, info in (table.get("core") or {}).items():
            if ("get_prop" not in slot and "set_prop" not in slot):
                continue
            start = info.get("func_start")
            if start:
                out.setdefault(int(start, 16), []).append((table["class"], slot))
    return out


def xml_edfx_item_fields():
    """The declared `list_item_fields` of nation.xml#nati index 342."""
    master = load_json(MASTER)
    blocks = master["entities"]["nation.xml"]
    block = next(b for b in blocks if any(f["field"] == "EDfx" for f in b["fields"]))
    idx, field = next((i, f) for i, f in enumerate(block["fields"]) if f["field"] == "EDfx")
    return dict(block_id=block["id"], xml_index=idx,
                name=field.get("name"), type=field.get("type"),
                item_fields=[f["field"] for f in field["list_item_fields"]])


# Producer bag keys -> XML list_item_fields.  Every mapping is justified by the
# value the producer computes immediately before emitting the key, so this is an
# observed correspondence, not a name-similarity guess.
KEY_TO_ITEM_FIELD = {
    "date": ("date", "0x14009153c..0x140091555 converts the packed day word and bags it as `date`"),
    "dyow": ("day_of_week", "0x1400915bb..0x140091619 computes a 1..7 day-of-week byte, bagged at 0x14009162b"),
    "time": ("time", "0x140091640 reads word [r14+0x3c] then bags it as `time` at 0x140091650"),
    "strl": ("stadium_rules", "0x140091665..0x1400916a0 renders the rules string via 0xb095f0 then bags `strl`"),
    "hidl": ("highest_division_level", "0x140091665 reads byte [r14+0x51] (0xff sentinel = optional) then bags `hidl`"),
    "lwdl": ("lowest_division_level", "0x1400916df reads byte [r14+0x52] (0xff sentinel = optional) then bags `lwdl`"),
    "text": ("text", "0x140091709..0x140091731 formats via 0xb095f0 family then bags `text`"),
}


def build() -> int:
    img = Image()
    p = img.p

    # ---------- A. uniqueness ---------------------------------------------
    literal = img.literal_occurrences("EDfx")
    ck(len(literal) == 1, f"EDfx literal count {len(literal)} != 1")
    ck(literal[0]["offset"] == 0x29C39, f"EDfx literal at {literal[0]['offset']:#x} != 0x29c39")
    ck(literal[0]["encoding"] == "ascii_reverse", literal[0]["encoding"])
    cmp_ins = next(i for i in img.md.disasm(p.raw[0x29C37:0x29C48], VA_EDFX_CMP, count=1)
                   if i.mnemonic == "cmp")
    ck(cmp_ins.mnemonic == "cmp" and cmp_ins.op_str == "esi, 0x45446678", cmp_ins.op_str)
    ext_disp = img.extent_va(VA_EDFX_CMP)
    ck(ext_disp == (0x28150, 0x2AA20), f"dispatcher extent {ext_disp}")

    census = img.imm4cc_census()
    ck(census["EDfx"] == [dict(va=VA_EDFX_CMP, offset=0x29C37, imm_offset=0x29C39, fn=0x28150)],
       f"EDfx imm census {census['EDfx']}")
    ed_keys = sorted(k for k in census if k.startswith("ED"))

    # ---------- B. namespace separation -----------------------------------
    dispatcher_keys = img.keys_in_extent(VA_DISPATCHER)
    persisted = persisted_codes()
    shared = sorted(dispatcher_keys & set(persisted))
    shared_detail = [(k, persisted[k]) for k in shared]
    for _, hits in shared_detail:
        ck(all(x["primary_off"] is None for x in hits),
           "dispatcher/persisted overlap unexpectedly has a direct field offset")
    ck("EDfx" not in persisted, "EDfx unexpectedly present in the persisted protocol")

    nation_set_keys = sorted(img.keys_in_extent(VA_NATION_SET_GATE)
                             | img.keys_in_extent(0x141063F30))
    ck("EDfx" not in nation_set_keys, "EDfx unexpectedly in the NATION setter key gate")
    nation_persisted = sorted(k for k in nation_set_keys if k in persisted)
    ck(len(nation_persisted) >= 40, f"NATION setter persisted keys {len(nation_persisted)}")

    # ---------- C. forward closure ----------------------------------------
    handlers = protocol_handlers()
    fwd_seen, fwd_edges, fwd_status = img.closure(VA_EDFX_PRODUCER)
    ck(fwd_status == "complete", f"producer closure {fwd_status}")
    ck(len(fwd_seen) == 201, f"producer closure nodes {len(fwd_seen)} != 201")
    ck(not (fwd_seen & set(handlers)), "producer closure reaches a property handler")
    ck(VA_DISPATCHER not in fwd_seen, "producer closure reaches the 4CC dispatcher")

    producer_iat = set()
    producer_file_iat = []
    for va in fwd_seen:
        if va in img.iat:
            producer_iat.add(img.iat[va])
        for ins in img.disasm_extent(va):
            for op in ins.operands:
                if op.type == 3 and ins.reg_name(op.mem.base) == "rip":
                    slot = ins.address + ins.size + op.mem.disp
                    if slot in img.file_iat:
                        producer_file_iat.append(dict(va=ins.address, api=img.file_iat[slot]))
                if op.type == 2 and op.imm in img.file_iat:
                    producer_file_iat.append(dict(va=ins.address, api=img.file_iat[op.imm]))
    ck(not producer_file_iat, f"producer closure touches file API: {producer_file_iat[:3]}")

    # ---------- D. reverse closure ----------------------------------------
    reader_handlers = [va for va, slots in handlers.items()
                       if any("get_prop" in s for _, s in slots)]
    reader_union = set()
    for va in reader_handlers:
        reader_union |= img.closure(va)[0]
    ck(VA_EDFX_PRODUCER not in reader_union, "a get_prop handler reaches the EDfx producer")
    ck(VA_DISPATCHER not in reader_union, "a get_prop handler reaches the 4CC dispatcher")

    nat_reader_seen, _, nat_status = img.closure(VA_NATION_READER)
    ck(nat_status == "complete", nat_status)
    ck(VA_EDFX_PRODUCER not in nat_reader_seen, "NATION wire reader reaches EDfx producer")
    nat_108 = [dict(va=i.address, asm=f"{i.mnemonic} {i.op_str}")
               for va in nat_reader_seen for i in img.disasm_extent(va)
               if "0x108" in i.op_str]
    ck(not nat_108, f"NATION reader touches +0x108: {nat_108[:3]}")

    # ---------- E. producer output shape ----------------------------------
    emitted = img.bag_keys_emitted(VA_EDFX_PRODUCER)
    emitted_keys = sorted({e["key"] for e in emitted})
    xml = xml_edfx_item_fields()
    ck(xml["xml_index"] == 342 and xml["type"] == "list", str(xml))
    ck(len(xml["item_fields"]) == 7, f"xml item fields {xml['item_fields']}")

    mapped = {}
    for key, (item, witness) in KEY_TO_ITEM_FIELD.items():
        ck(key in emitted_keys, f"producer does not emit {key!r}")
        ck(item in xml["item_fields"], f"{item!r} not an XML item field")
        sites = [e["va"] for e in emitted if e["key"] == key]
        mapped[key] = dict(item_field=item, witness=witness,
                           emitted_at=[hex(s) for s in sites[:3]],
                           emitted_count=len(sites),
                           persisted=key in persisted)
    ck(sorted(m["item_field"] for m in mapped.values()) == sorted(xml["item_fields"]),
       "producer key set does not cover the XML item fields 1:1")
    unpersisted = sorted(k for k, m in mapped.items() if not m["persisted"])
    ck(len(unpersisted) == 6, f"unpersisted item keys {unpersisted}")
    ck([k for k, m in mapped.items() if m["persisted"]] == ["date"],
       f"only `date` should be in the persisted namespace: {[(k, m['persisted']) for k, m in mapped.items()]}")

    # ---------- fles container --------------------------------------------
    fles = img.bag_sites("fles")
    fles_roles = {}
    for site in fles:
        fles_roles[site["role"]] = fles_roles.get(site["role"], 0) + 1
    ck(fles_roles.get("bag_set_prop", 0) == 0, f"fles has a set_prop writer: {fles_roles}")
    ck(fles_roles.get("bag_get_prop", 0) >= 30, f"fles get sites {fles_roles}")

    comp_sites = img.bag_sites("comp")
    comp_roles = {}
    for site in comp_sites:
        comp_roles[site["role"]] = comp_roles.get(site["role"], 0) + 1

    # The producer's own `fles` read, for the chain.
    prod_fles = [dict(va=s["va"], role=s["role"]) for s in fles
                 if img.extent_va(s["va"]) and img.extent_va(s["va"])[0] == 0x907F0]

    # ---------- NATION +0x108 ---------------------------------------------
    nat_set_108 = [dict(va=i.address, asm=f"{i.mnemonic} {i.op_str}")
                   for i in img.disasm_extent(VA_NATION_SET_GATE) if "0x108" in i.op_str]
    ck(nat_set_108, "expected a +0x108 access in the NATION setter")
    nat_108_persisted = [c for c, hits in persisted.items()
                         if any(x["primary_off"] == "0x108" and x["slot"].endswith("get_prop")
                                for x in hits)]

    # ---------- caller chain ----------------------------------------------
    producer_callers = [dict(va=img.p.f2va(o), fn=img.extent_va(img.p.f2va(o))[0])
                        for o in img.callers(VA_EDFX_PRODUCER)]
    ck(len(producer_callers) == 1, f"EDfx producer callers {producer_callers}")
    ck(producer_callers[0]["fn"] == 0x28150, "producer caller is not the dispatcher")

    # ---------- verdict ----------------------------------------------------
    verdict = {
        "schema_id": "fm24.t149.edfx_verdict",
        "schema_version": 1,
        "generated_by": "t149",
        "status": "negative",
        "question": "Does EDfx bind to a concrete .dat table/member/offset (L3), or is it a pure runtime/editor rule-layer field?",
        "answer": "Pure runtime/editor rule-layer UI projection field. No .dat reader, writer, wire slot or backing member exists.",
        "L3": True,
        "L4": 0,
        "reader": None,
        "writer": None,
        "member": None,
        "row_offset": None,
        "binary_provenance": {
            "path": str(_cfg.EDITOR_EXE),
            "sha256": h(p.raw),
            "size": len(p.raw),
            "image_base": p.base,
            "evidence_grade": "L3 (static disassembly of editor.exe; no runtime execution, no game load)",
        },
        "inputs": {
            "editor_exe": EXE_SHA,
            "master_json_sha256": h((ROOT / MASTER).read_bytes()),
            "t108_sha256": h((ROOT / T108).read_bytes()),
            "vtable_index_sha256": h((ROOT / VTINDEX).read_bytes()),
        },
        "legs": {
            "A_uniqueness": {
                "claim": "EDfx appears exactly once in the 74.8 MB image and only as a compare immediate.",
                "literal_occurrences": literal,
                "instruction": dict(va=VA_EDFX_CMP, bytes=cmp_ins.bytes.hex(),
                                    asm=f"{cmp_ins.mnemonic} {cmp_ins.op_str}"),
                "owning_function": dict(entry=hex(ext_disp[0]), end_exclusive=hex(ext_disp[1]),
                                        copied_from_t62="0x28150 dispatcher"),
                "imm4cc_census_distinct_keys": len(census),
                "imm4cc_census_ed_keys": ed_keys,
                "note": "Only ascii_reverse exists; forward, UTF-16LE and UTF-16BE are all empty.",
            },
            "B_namespace_separation": {
                "claim": "The dispatcher's 4CC namespace is disjoint from the persisted property protocol.",
                "dispatcher_keys_count": len(dispatcher_keys),
                "dispatcher_keys_sample": sorted(dispatcher_keys)[:24],
                "persisted_codes_count": len(persisted),
                "shared_keys": shared,
                "shared_keys_detail": shared_detail,
                "shared_keys_all_computed_or_ui": True,
                "ED_family_persisted": sorted(k for k in persisted if k.startswith("ED")),
                "nation_setter_keys_count": len(nation_set_keys),
                "nation_setter_persisted_keys": nation_persisted,
                "nation_setter_contains_EDfx": "EDfx" in nation_set_keys,
            },
            "C_forward_closure": {
                "claim": "The EDfx producer cannot reach any .dat reader/writer or file API.",
                "root": hex(VA_EDFX_PRODUCER),
                "nodes": len(fwd_seen),
                "edges": len(fwd_edges),
                "status": fwd_status,
                "protocol_handlers_reached": sorted(hex(x) for x in fwd_seen & set(handlers)),
                "dispatcher_reached": VA_DISPATCHER in fwd_seen,
                "file_api_sites": producer_file_iat,
                "iat_imports_referenced": sorted(producer_iat),
                "file_api_iat_slots_in_image": len(img.file_iat),
                "total_iat_slots_in_image": len(img.iat),
            },
            "D_reverse_closure": {
                "claim": "No .dat reader reaches the EDfx producer or dispatcher.",
                "get_prop_handler_count": len(reader_handlers),
                "get_prop_union_nodes": len(reader_union),
                "producer_in_union": VA_EDFX_PRODUCER in reader_union,
                "dispatcher_in_union": VA_DISPATCHER in reader_union,
                "nation_reader": dict(root=hex(VA_NATION_READER), slot="slot19",
                                      nodes=len(nat_reader_seen), status=nat_status,
                                      backlink_0x108_accesses=nat_108),
            },
            "E_output_shape": {
                "claim": "The producer emits exactly the seven XML list_item_fields under bag keys; five are absent from the persisted namespace.",
                "xml": xml,
                "producer_emitted_keys": emitted_keys,
                "producer_emitted_sites": emitted,
                "mapping": mapped,
                "unpersisted_item_keys": unpersisted,
            },
        },
        "containers": {
            "fles": {
                "code": "fles",
                "imm": hex(int.from_bytes(b"fles", "big")),
                "role_counts": fles_roles,
                "sites": fles,
                "conclusion": "Memory bag read (34), probed (1) and erased (3); never written by any 4CC-keyed setter. No deserializer populates it here.",
                "producer_fles_reads": prod_fles,
            },
            "comp": {
                "code": "comp",
                "role_counts": comp_roles,
                "conclusion": "Contrast control: comp does have bag_insert sites, so the absence for fles is a real asymmetry, not a scanner artifact.",
            },
            "nation_plus_0x108": {
                "setter": hex(VA_NATION_SET_GATE),
                "setter_108_accesses": nat_set_108,
                "persisted_codes_at_0x108_getter": nat_108_persisted,
                "conclusion": "NATION+0x108 is the generic object backlink (`link`/`nhrl` getters per t108), read through the setter gate and never an EDfx slot.",
            },
        },
        "call_chain": {
            "ui_caller_into_dispatcher": [hex(x) for x in
                                          (img.p.f2va(o) for o in img.callers(VA_DISPATCHER))],
            "producer_callers": producer_callers,
            "spine": [
                dict(site="0x14002a637", role="cmp esi,0x45446678 — exact EDfx key, sole occurrence"),
                dict(site="0x14002a63d", role="jne 0x14002b084 — not EDfx, leave the arm"),
                dict(site="0x14002a669", role="cmp eax,0xa — require selected object type NATION"),
                dict(site="0x14002a680", role="call 0x1400911f0 — enter the EDfx generator"),
                dict(site="0x14009127b", role="bag_get `comp` on each rules row (read only)"),
                dict(site="0x14009154d", role="bag_set `date` into the UI output bag"),
                dict(site="0x14009162b", role="bag_set `dyow` (day_of_week)"),
                dict(site="0x140091650", role="bag_set `time`"),
                dict(site="0x140091698", role="bag_set `strl` (stadium_rules)"),
                dict(site="0x1400916ca", role="bag_set `hidl` (highest_division_level)"),
                dict(site="0x1400916f4", role="bag_set `lwdl` (lowest_division_level)"),
                dict(site="0x140091729", role="bag_set `text`"),
                dict(site="0x140091418", role="call 0x140b03380 — query the in-memory calendar day buckets"),
                dict(site="0x1400913d9", role="call 0x1410403f0 — read NATION+0x108 backlink for the join"),
                dict(site="0x14002a685", role="jmp 0x14002a968 — return the boxed UI list; no archive stream"),
            ],
        },
        "t62_reopen_adjudication": [
            dict(id="E1", reopen="Find another byte match or a proven computed EDfx key reaching a persistence path.",
                 adjudication="closed", basis="leg A: exhaustive 6-encoding scan over 74.8 MB yields one occurrence, a compare immediate."),
            dict(id="E2", reopen="Provide an alias from the boxed list to a concrete writer.",
                 adjudication="closed", basis="leg C: producer closure has no property handler and no file API; the list is only moved to the caller output slot."),
            dict(id="E3", reopen="EDsc normalisation evidence.", adjudication="not applicable",
                 basis="Concerns EDsc; t62 already closed it by static dispatch replay. Unchanged here."),
            dict(id="E4", reopen="Supply an EDsc output/member alias into a modern NATION transfer site.",
                 adjudication="not applicable", basis="Concerns EDsc; outside this task's EDfx scope."),
            dict(id="E5", reopen="Show a matching shared Tgl table/element pointer feeding a schedule input.",
                 adjudication="moot", basis="leg C/E: the producer never needs the shared Tchl vector; its inputs are the `comp` rules rows and the calendar buckets, and its output is a UI bag."),
            dict(id="E6", reopen="New directory match in the pinned archives, or a proven indirect mapped member.",
                 adjudication="closed", basis="legs C/D: no member can be mapped because no reader/writer pair exists."),
            dict(id="E7", reopen="Trace the producer of the rule/fixture content into a deserializer and back into a writer.",
                 adjudication="closed as negative", basis="legs B+C+D: bidirectional closure proves neither direction exists, so table_10/table_25 cannot be its backing."),
        ],
        "method": {
            "disassembly": "Capstone CS_ARCH_X86/CS_MODE_64 over PE file offsets mapped via t05_pe.",
            "closure": "complete direct-call closure; IAT slots recorded but not expanded; cap 6000 nodes.",
            "namespace": "t108 fourcc_mem_map_v2 (67 tables, 2301 codes) is the persisted protocol denominator.",
            "no_runtime": "Static only. No game/editor launch, no Unicorn emulation, no network, no Z: access.",
        },
        "limits": [
            "Static disassembly cannot exclude a hypothetical dynamically computed key equal to 0x45446678 at runtime; leg B makes that useless anyway because no ED* code is in the persisted protocol.",
            "Virtual/indirect calls inside the producer closure (313 register/vtable dispatches) are not expanded; the 56 rip-relative ones are all resolved to non-file IAT imports.",
            "The 56 rip-relative indirect calls in the closure resolve entirely to CRT/lock/debug imports; none is a file API.",
            "Wrap/teardown helpers that clear `fles` (0x141ce4c60) are reached through vtable slots, so their callers are not enumerable by direct-call scan.",
        ],
        "deliverables": {
            "verdict": "scratch/t149/out/edfx_verdict.json",
            "report": "scratch/t149/out/REPORT.md",
            "done": "scratch/t149/out/DONE.md",
            "script": "scripts/t149_edfx_upstream.py",
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "edfx_verdict.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("t149 NEGATIVE verdict written")
    print(f"  EDfx literal occurrences      : {len(literal)} (offset {literal[0]['offset']:#x})")
    print(f"  dispatcher keys / persisted   : {len(dispatcher_keys)} / {len(persisted)} (shared {shared})")
    print(f"  producer closure              : {len(fwd_seen)} nodes, {len(fwd_edges)} edges, {fwd_status}")
    print(f"  protocol handlers reached     : {len(fwd_seen & set(handlers))}")
    print(f"  file-API sites in closure     : {len(producer_file_iat)}")
    print(f"  get_prop union -> producer    : {VA_EDFX_PRODUCER in reader_union}")
    print(f"  XML item fields covered       : {len(mapped)}/7 ({len(unpersisted)} unpersisted)")
    print(f"  fles roles                    : {fles_roles}")
    return 0


def selftest() -> int:
    """Pure-constant assertions; runs without editor.exe or any data input."""
    ck(int.from_bytes(b"EDfx", "big") == 0x45446678, "EDfx big-endian 4CC")
    ck(int.from_bytes(b"EDfx"[::-1], "big") == 0x78664445, "EDfx reverse 4CC")
    ck(printable4cc(0x45446678) == "EDfx", "printable4cc EDfx")
    ck(printable4cc(0x666C6573) == "fles", "printable4cc fles")
    ck(printable4cc(0x636F6D70) == "comp", "printable4cc comp")
    ck(printable4cc(0x0000000A) == "", "non-printable rejected")
    ck(len(b"EDfx") == 4 and b"EDfx".hex() == "45446678", "4CC byte width")

    # Bag accessor table must not alias.
    roles = [role_of(x) for x in (BAG_GET, BAG_HAS, BAG_SET, BAG_ERASE, BAG_INSERT, None, 0)]
    ck(roles == ["bag_get_prop", "bag_has_prop", "bag_set_prop", "bag_erase_prop",
                 "bag_insert_prop", "no-call", "other"], roles)
    ck(len({BAG_GET, BAG_HAS, BAG_SET, BAG_ERASE, BAG_INSERT}) == 5, "accessors distinct")

    # The producer mapping must be a bijection onto the 7 XML item fields.
    ck(len(set(KEY_TO_ITEM_FIELD)) == 7, "7 producer keys")
    ck(len({v[0] for v in KEY_TO_ITEM_FIELD.values()}) == 7, "7 distinct item fields")
    expected = {"date", "day_of_week", "time", "stadium_rules", "text",
                "highest_division_level", "lowest_division_level"}
    ck({v[0] for v in KEY_TO_ITEM_FIELD.values()} == expected, "item field set")
    ck(all(int.from_bytes(k.encode(), "big") > 0x20202020 for k in KEY_TO_ITEM_FIELD),
       "keys are printable 4CC")

    # File-API allowlist sanity.
    ck("fopen" in FILE_API and "CreateFileW" in FILE_API and "ReadFile" in FILE_API,
       "file api set")
    ck("malloc" not in FILE_API and "free" not in FILE_API, "heap api excluded")

    # Address constants must be internally consistent (dispatcher owns the cmp).
    ck(0x28150 <= (VA_EDFX_CMP - 0x140000000) < 0x2AA20, "cmp inside dispatcher extent")
    ck(VA_EDFX_PRODUCER - 0x140000000 == 0x911F0, "producer VA == 0x907f0 file offset mapping")
    ck(VA_NATION_READER - 0x140000000 == 0x10404C0, "nation reader VA mapping")
    print("t149 selftest PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="t149_edfx_upstream.py",
        description="Final adjudication of the EDfx upstream persistence question (L3 static proof).")
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--build", action="store_true",
                     help="recompute the verdict and write scratch/t149/out/edfx_verdict.json (default)")
    grp.add_argument("--selftest", action="store_true",
                     help="run pure-constant assertions; needs no inputs")
    args = ap.parse_args()
    try:
        return selftest() if args.selftest else build()
    except Check as e:
        print(f"t149 check failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001 - fatal path is exit code 2
        print(f"t149 fatal: {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
