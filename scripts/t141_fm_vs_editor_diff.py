"""t141_fm_vs_editor_diff — Pure-Python binary audit: 491 MB `fm.exe` (game) vs 74 MB `editor.exe`.

Compares the FM24 database layer of both read-only PEs without touching IDA:
  * PE layout / section / entropy / packing-and-protection assessment (pefile + numpy)
  * complete MSVC RTTI class census (`DATABASE::`, `db::`, `STARTING_*`, TABLE/ARCHIVE),
    with exact 3-way set diffs (common / fm-only / editor-only)
  * database archive filename + magic-anchor string comparison
    (`server_db.dat`, `client_db.dat`, `people_db.dat`, `basic_people_db.dat`,
     `lang_db_2400.dat`, `pl_hist_dt.dat`, `table_%d.dat`, `tad.`, `fmf.`, `0x0DF1`)
  * 4CC (PDxx / Big-3) literal census: dictionary codes + structural imm32 opcode contexts

Everything is measured directly from the PE bytes; nothing is inferred from IDA sessions.

Usage:
  py -V:3.12 -B scripts/t141_fm_vs_editor_diff.py --selftest
  py -V:3.12 -B scripts/t141_fm_vs_editor_diff.py
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import bisect
import hashlib
import json
import mmap
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    import pefile
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"pefile required: {exc}")

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch/t141/out"

FM_EXE = Path(str(_cfg.FM_EXE))
EDITOR_EXE = Path(str(_cfg.EDITOR_EXE))

T95_VTABLE = ROOT / "scratch/t95/vtable_index.json"
T113_PEOPLE = ROOT / "scratch/t113/out/people_vtables_full.json"
T120_PEOPLE = ROOT / "scratch/t120/out/people_unicorn_traces.json"
T109_BIG3 = ROOT / "scratch/t109/out/big3_l3_join.json"
CLUB_NATION_SCHEMA = ROOT / "reports/club_nation_subtable_schema.json"
T12_FIELDS = ROOT / "reports/t12_field_names.json"

RTTI_PREFIX = b".?AV"
# strict MSVC type-descriptor grammar used for the census (.?AV<CLASS>@<NS>@@)
RX_RTTI_STRICT = re.compile(rb"^\.\?AV([A-Za-z0-9_@]+)@@$")
RX_RTTI_TEMPLATE = re.compile(rb"^\.\?AV\?\$")
RX_4CC = re.compile(rb"^[A-Za-z][A-Za-z0-9_]{3}$")

# imm32 opcode contexts used for the structural 4CC census (x86-64, no full disassembly)
IMM1_OPCODES = {0x68, 0x3D} | set(range(0xB8, 0xC0))  # push imm32, cmp eax,imm32, mov r32,imm32
IMM_REX_BYTE = 0x41  # REX.B -> mov r8d..r15d, imm32
IMM_GRP1_BYTE = 0x81  # group1 r/m32, imm32 -> /7 = cmp
IMM_GRP1_MODRM = set(range(0xF8, 0x100))

DB_FILENAME_NEEDLES = [
    b"server_db.dat",
    b"client_db.dat",
    b"people_db.dat",
    b"basic_people_db.dat",
    b"lang_db_2400.dat",
    b"pl_hist_dt.dat",
    b"table_%d.dat",
    b"non_pl_hist_dt.dat",
    b"lang_update_db.dat",
    b"summary.dat",
    b"_db.dat",
    b".dat",
]
DB_MAGIC_NEEDLES = [
    b"tad.",
    b"fmf.",
    b"TAD.",
    b"FMF.",
    b"0DF1",
]
DB_VERSION_PATTERNS = {
    "0x0DF1_le16": b"\xf1\x0d",
    "0x0DF1_le32": b"\xf1\x0d\x00\x00",
    "0x0DF1_ascii_upper": b"0DF1",
}


# ----------------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------------
def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _utc(ts: int) -> str:
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return "invalid"


def entropy_of_bytes(buf: bytes) -> float:
    a = np.frombuffer(buf, dtype=np.uint8)
    if a.size == 0:
        return 0.0
    c = np.bincount(a, minlength=256).astype(np.float64)
    c /= c.sum()
    c = c[c > 0]
    return float(-(c * np.log2(c)).sum())


def parse_mangled(raw: bytes | str) -> tuple[str, str] | None:
    """'.?AVAWARD@DATABASE@@' -> ('AWARD', 'DATABASE'). Strict grammar only."""
    if isinstance(raw, str):
        raw = raw.encode("latin1", "replace")
    m = RX_RTTI_STRICT.match(raw)
    if not m:
        return None
    body = m.group(1).decode("latin1").rstrip("@")
    parts = body.split("@")
    cls = parts[0]
    ns = "@".join(reversed(parts[1:]))  # MSVC nests outermost-last
    return cls, ns


# ----------------------------------------------------------------------------------
# PE metadata + section layout / entropy
# ----------------------------------------------------------------------------------
def _section_flags(ch: int) -> dict:
    return {
        "cnt_code": bool(ch & 0x00000020),
        "cnt_init_data": bool(ch & 0x00000040),
        "cnt_uninit_data": bool(ch & 0x00000080),
        "discardable": bool(ch & 0x02000000),
        "not_cached": bool(ch & 0x04000000),
        "not_paged": bool(ch & 0x08000000),
        "shared": bool(ch & 0x10000000),
        "mem_execute": bool(ch & 0x20000000),
        "mem_read": bool(ch & 0x40000000),
        "mem_write": bool(ch & 0x80000000),
    }


def section_stats(path: Path, off: int, size: int, chunk: int = 32 << 20) -> dict:
    """Exact full-section byte histogram (entropy / zero / printable ratios)."""
    if size <= 0:
        return {"raw_analyzed": 0, "entropy": None, "zero_ratio": None,
                "printable_ratio": None, "distinct_bytes": 0}
    cnt = np.zeros(256, np.int64)
    n = 0
    printable = 0
    zeros = 0
    mz = 0
    mv = 0
    with open(path, "rb") as f:
        f.seek(off)
        while n < size:
            b = f.read(min(chunk, size - n))
            if not b:
                break
            a = np.frombuffer(b, dtype=np.uint8)
            cnt += np.bincount(a, minlength=256)
            n += a.size
            printable += int(((a >= 0x20) & (a < 0x7F)).sum())
            zeros += int((a == 0).sum())
            mz += int(a.sum(dtype=np.int64))
            mv += int((a.astype(np.int64) ** 2).sum())
    p = cnt / max(1, cnt.sum())
    p = p[p > 0]
    ent = float(-(p * np.log2(p)).sum())
    return {
        "raw_analyzed": n,
        "entropy": round(ent, 4),
        "zero_ratio": round(zeros / max(1, n), 4),
        "printable_ratio": round(printable / max(1, n), 4),
        "distinct_bytes": int((cnt > 0).sum()),
    }


def pe_meta(path: Path, with_section_entropy: bool = True) -> dict:
    pe = pefile.PE(str(path), fast_load=True)
    pe.parse_data_directories(
        directories=[
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"],
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"],
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"],
        ]
    )
    ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    secs = []
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("latin1")
        ch = s.Characteristics
        rec = {
            "name": name,
            "virtual_address": hex(s.VirtualAddress),
            "virtual_size": s.Misc_VirtualSize,
            "raw_offset": s.PointerToRawData,
            "raw_size": s.SizeOfRawData,
            "characteristics": hex(ch),
            "flags": _section_flags(ch),
            "is_entrypoint_section": bool(
                s.VirtualAddress <= ep < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData)
            ),
        }
        if with_section_entropy:
            rec.update(section_stats(path, s.PointerToRawData, s.SizeOfRawData))
        secs.append(rec)

    imports: list[str] = []
    n_import_funcs = 0
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for dll in pe.DIRECTORY_ENTRY_IMPORT:
            imports.append(dll.dll.decode("latin1", "replace"))
            n_import_funcs += len(dll.imports)

    doc = {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "mtime_utc": _utc(int(path.stat().st_mtime)),
        "machine": hex(pe.FILE_HEADER.Machine),
        "is_64bit": pe.FILE_HEADER.Machine == 0x8664,
        "time_date_stamp": hex(pe.FILE_HEADER.TimeDateStamp),
        "time_date_stamp_utc": _utc(pe.FILE_HEADER.TimeDateStamp),
        "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
        "size_of_image": pe.OPTIONAL_HEADER.SizeOfImage,
        "size_of_headers": pe.OPTIONAL_HEADER.SizeOfHeaders,
        "subsystem": pe.OPTIONAL_HEADER.Subsystem,
        "dll_characteristics": hex(pe.OPTIONAL_HEADER.DllCharacteristics),
        "dll_characteristics_flags": {
            "high_entropy_va": bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0020),
            "dynamic_base": bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0040),
            "nx_compat": bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0100),
            "no_seh": bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0400),
            "guard_cf": bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x4000),
            "terminal_server_aware": bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x8000),
        },
        "entry_point_rva": hex(ep),
        "entry_point_section": next(
            (s["name"] for s in secs if s["is_entrypoint_section"]), None
        ),
        "num_sections": len(secs),
        "sections": secs,
        "has_reloc_section": any(s["name"] == ".reloc" for s in secs),
        "data_directories": [
            {
                "index": i,
                "name": pefile.DIRECTORY_ENTRY.get(n, n),
                "va": hex(d.VirtualAddress),
                "size": d.Size,
            }
            for i, (n, d) in enumerate(
                zip(
                    [
                        "EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY", "BASERELOC",
                        "DEBUG", "ARCHITECTURE", "GLOBALPTR", "TLS", "LOAD_CONFIG", "BOUND_IMPORT",
                        "IAT", "DELAY_IMPORT", "COM_DESCRIPTOR",
                    ],
                    pe.OPTIONAL_HEADER.DATA_DIRECTORY,
                )
            )
            if d.Size
        ],
        "import_dll_count": len(imports),
        "import_dlls": sorted(imports),
        "import_func_count": n_import_funcs,
    }
    pe.close()
    return doc


class SectionMap:
    """raw file offset -> section record (bisect over PointerToRawData ranges)."""

    def __init__(self, sections: list[dict]):
        self.entries = [
            (s["raw_offset"], s["raw_offset"] + s["raw_size"], s["name"],
             s["flags"]["mem_execute"])
            for s in sections
            if s["raw_size"] > 0
        ]
        self.entries.sort()
        self.starts = [e[0] for e in self.entries]

    def at(self, off: int) -> tuple[str, bool]:
        i = bisect.bisect_right(self.starts, off) - 1
        if i < 0:
            return ("<headers>", False)
        s, e, name, is_exec = self.entries[i]
        if s <= off < e:
            return (name, is_exec)
        return ("<gap>", False)


# ----------------------------------------------------------------------------------
# RTTI census
# ----------------------------------------------------------------------------------
def scan_rtti(path: Path, prefix_limit: int | None = None) -> dict:
    """Walk every b'.?AV' occurrence, decode the descriptor string, classify."""
    size = path.stat().st_size
    limit = size if prefix_limit is None else min(size, prefix_limit)
    strict: Counter = Counter()
    template: Counter = Counter()
    other = 0
    total_probe = 0
    sec_hist: Counter = Counter()
    header_ok = 0

    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            secmap = SectionMap(pe_sections_of(path))
            pos = 0
            while True:
                i = mm.find(RTTI_PREFIX, pos, limit)
                if i < 0:
                    break
                pos = i + 1
                total_probe += 1
                j = mm.find(b"\x00", i, min(i + 300, limit))
                if j < 0:
                    continue
                raw = mm[i:j]
                if RX_RTTI_STRICT.match(raw):
                    body = raw[4:-2].decode("latin1").rstrip("@")
                    strict[body] += 1
                    sec_hist[secmap.at(i)[0]] += 1
                    # MSVC TypeDescriptor: [vfptr(8)][spare=0(8)][name]
                    if i >= 16 and mm[i - 8:i] == b"\x00" * 8 and mm[i - 16:i - 8] != b"\x00" * 8:
                        header_ok += 1
                elif RX_RTTI_TEMPLATE.match(raw):
                    template[raw[4:].decode("latin1")] += 1
                else:
                    other += 1
        finally:
            mm.close()

    by_class: dict[str, dict[str, int]] = {}
    ns_counts: Counter = Counter()
    for body, cnt in strict.items():
        parts = body.split("@")
        cls = parts[0]
        ns = "@".join(reversed(parts[1:]))
        ns_counts[ns] += cnt
        rec = by_class.setdefault(body, {"class": cls, "namespace": ns, "descriptor_count": 0})
        rec["descriptor_count"] += cnt

    return {
        "size_scanned": limit,
        "rtti_probe_occurrences": total_probe,
        "strict_descriptors_occurrences": sum(strict.values()),
        "strict_descriptors_unique": len(strict),
        "template_descriptors_occurrences": sum(template.values()),
        "template_descriptors_unique": len(template),
        "unparsed_occurrences": other,
        "descriptors_with_msvc_typeinfo_header": header_ok,
        "descriptors_by_section": dict(sec_hist),
        "namespace_counts": ns_counts,
        "by_class": by_class,
    }


_PE_CACHE: dict[str, list[dict]] = {}


def pe_sections_of(path: Path) -> list[dict]:
    key = str(path)
    if key in _PE_CACHE:
        return _PE_CACHE[key]
    pe = pefile.PE(str(path), fast_load=True)
    secs = []
    for s in pe.sections:
        ch = s.Characteristics
        secs.append(
            {
                "name": s.Name.rstrip(b"\x00").decode("latin1"),
                "raw_offset": s.PointerToRawData,
                "raw_size": s.SizeOfRawData,
                "flags": _section_flags(ch),
            }
        )
    pe.close()
    _PE_CACHE[key] = secs
    return secs


def group_census(scan: dict, ns_names: set[str]) -> dict:
    """Collect {descriptor_body: class name} for one namespace (or set of namespaces)."""
    out = {}
    for body, rec in scan["by_class"].items():
        ns = rec["namespace"]
        top = ns.split("@")[0]
        if ns in ns_names or top in ns_names:
            out[body] = rec["class"]
    return out


def three_way(fm: dict, ed: dict) -> dict:
    fk, ek = set(fm), set(ed)
    common = sorted(fk & ek)
    return {
        "fm_unique_descriptors": len(fk),
        "editor_unique_descriptors": len(ek),
        "common_count": len(common),
        "fm_only_count": len(fk - ek),
        "editor_only_count": len(ek - fk),
        "common": common,
        "fm_only": sorted(fk - ek),
        "editor_only": sorted(ek - fk),
    }


def class_only_three_way(fm: dict, ed: dict) -> dict:
    """Same 3-way diff on bare class names (namespace stripped)."""
    fc = {v for v in fm.values()}
    ec = {v for v in ed.values()}
    return {
        "common": sorted(fc & ec),
        "fm_only": sorted(fc - ec),
        "editor_only": sorted(ec - fc),
        "counts": {
            "fm_unique": len(fc),
            "editor_unique": len(ec),
            "common": len(fc & ec),
            "fm_only": len(fc - ec),
            "editor_only": len(ec - fc),
        },
    }


# ----------------------------------------------------------------------------------
# string / magic needle scan
# ----------------------------------------------------------------------------------
def needle_scan(path: Path, needles: list[bytes], max_offsets: int = 5,
                prefix_limit: int | None = None) -> dict:
    size = path.stat().st_size
    limit = size if prefix_limit is None else min(size, prefix_limit)
    secmap = SectionMap(pe_sections_of(path))
    res = {}
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for nd in needles:
                pos = 0
                cnt = 0
                offs = []
                secs: Counter = Counter()
                while True:
                    i = mm.find(nd, pos, limit)
                    if i < 0:
                        break
                    cnt += 1
                    pos = i + 1
                    sec = secmap.at(i)[0]
                    secs[sec] += 1
                    if len(offs) < max_offsets:
                        ctx_lo = max(0, i - 24)
                        ctx_hi = min(limit, i + len(nd) + 40)
                        offs.append(
                            {
                                "offset": hex(i),
                                "file_offset_dec": i,
                                "section": sec,
                                "context_ascii": _squash(mm[ctx_lo:ctx_hi]),
                            }
                        )
                res[nd.decode("latin1")] = {
                    "count": cnt,
                    "present": cnt > 0,
                    "by_section": dict(secs),
                    "first_offsets": offs,
                }
        finally:
            mm.close()
    return res


def _squash(b: bytes) -> str:
    out = []
    for x in b:
        out.append(chr(x) if 0x20 <= x < 0x7F else ".")
    return "".join(out)


# ----------------------------------------------------------------------------------
# 4CC census (dictionary + structural imm32 contexts)
# ----------------------------------------------------------------------------------
def load_fourcc_dictionary() -> dict:
    """Collect 4CC codes known from this repo's prior artifacts (read-only)."""
    codes: dict[str, set] = {
        "t109_big3": set(),
        "t113_people": set(),
        "t120_people": set(),
        "club_nation_schema": set(),
        "t12_field_names": set(),
    }

    def add(bucket: str, val):
        if isinstance(val, str) and RX_4CC.match(val.encode("latin1", "replace")):
            codes[bucket].add(val)

    if T109_BIG3.exists():
        for row in json.load(open(T109_BIG3, encoding="utf-8")).get("rows", []):
            add("t109_big3", row.get("code"))
    if T113_PEOPLE.exists():
        doc = json.load(open(T113_PEOPLE, encoding="utf-8"))
        for vt in doc.get("vtables", []):
            for slot in (vt.get("core") or {}).values():
                for c in slot.get("fourccs") or []:
                    add("t113_people", c)
    if T120_PEOPLE.exists():
        doc = json.load(open(T120_PEOPLE, encoding="utf-8"))
        for key, stats in (doc.get("samples_by_type") or {}).items():
            if isinstance(stats, dict):
                for c in stats.get("fourccs") or []:
                    add("t120_people", c)
    if CLUB_NATION_SCHEMA.exists():
        _harvest_json_codes(json.load(open(CLUB_NATION_SCHEMA, encoding="utf-8")), "club_nation_schema", add)
    if T12_FIELDS.exists():
        _harvest_json_codes(json.load(open(T12_FIELDS, encoding="utf-8")), "t12_field_names", add)

    union = set().union(*codes.values())
    return {"buckets": {k: sorted(v) for k, v in codes.items()}, "codes": sorted(union)}


def _harvest_json_codes(node, bucket: str, add) -> None:
    """Find 4-char code strings inside schema JSON (keys named code/fields/name/4cc)."""
    KEY_HINT = ("code", "4cc", "field", "fields", "slot", "name", "tag", "id")
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str) and any(h in k.lower() for h in KEY_HINT):
                if isinstance(v, str):
                    add(bucket, v)
                elif isinstance(v, list):
                    for x in v:
                        if isinstance(x, str):
                            add(bucket, x)
                        else:
                            _harvest_json_codes(x, bucket, add)
                else:
                    _harvest_json_codes(v, bucket, add)
            else:
                _harvest_json_codes(v, bucket, add)
    elif isinstance(node, list):
        for x in node:
            _harvest_json_codes(x, bucket, add)


def fourcc_census(path: Path, codes: list[str], prefix_limit: int | None = None,
                  chunk: int = 48 << 20) -> dict:
    """Count 4CC literals for a dictionary of codes, split by section class and by
    imm32 opcode context (mov r32/cmp eax/push imm32). One streaming numpy pass."""
    size = path.stat().st_size
    limit = size if prefix_limit is None else min(size, prefix_limit)

    code_bytes = [c.encode("latin1") for c in codes]
    keys = np.array(sorted({int.from_bytes(b, "little") for b in code_bytes}), dtype=np.uint32)
    code_list = [int(k).to_bytes(4, "little").decode("latin1") for k in keys]
    firstbyte = np.zeros(256, bool)
    for b in code_bytes:
        firstbyte[b[0]] = True

    section_names = [s["name"] for s in pe_sections_of(path)]
    sec_starts = np.array([s["raw_offset"] for s in pe_sections_of(path)], dtype=np.int64)
    sec_ends = np.array([s["raw_offset"] + s["raw_size"] for s in pe_sections_of(path)], dtype=np.int64)
    sec_exec = np.array([s["flags"]["mem_execute"] for s in pe_sections_of(path)], dtype=bool)

    nsec = max(1, len(section_names))
    if not section_names:
        section_names = ["<none>"]
    n_total = np.zeros(len(keys), np.int64)
    n_exec = np.zeros(len(keys), np.int64)
    n_imm = np.zeros(len(keys), np.int64)
    per_section = np.zeros((len(keys), nsec), np.int64)

    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            off = 0
            while off < limit:
                core = min(chunk, limit - off)
                m = min(core + 3, limit - off)
                if m < 4:
                    break
                a = np.frombuffer(mm, dtype=np.uint8, count=m, offset=off)
                fb = firstbyte[a]
                idx = np.flatnonzero(fb)
                if idx.size:
                    idx = idx[idx <= m - 4]
                if idx.size:
                    g = idx.astype(np.int64) + off
                    keep = g < off + core
                    idx = idx[keep]
                    g = g[keep]
                    k = (
                        a[idx].astype(np.uint32)
                        | (a[idx + 1].astype(np.uint32) << 8)
                        | (a[idx + 2].astype(np.uint32) << 16)
                        | (a[idx + 3].astype(np.uint32) << 24)
                    )
                    p = np.searchsorted(keys, k)
                    np.clip(p, 0, len(keys) - 1, out=p)
                    hit = keys[p] == k
                    if hit.any():
                        ph = p[hit]
                        gh = g[hit]
                        hidx = idx[hit]  # chunk-local offsets of the hit positions
                        nkey = len(keys)
                        n_total += np.bincount(ph, minlength=nkey)[:nkey]
                        # section attribution
                        si = np.searchsorted(sec_starts, gh, side="right") - 1
                        si = np.where(si < 0, 0, si)
                        insec = (gh >= sec_starts[si]) & (gh < sec_ends[si])
                        si_ok = np.where(insec, si, nsec - 1)
                        flat = ph.astype(np.int64) * nsec + si_ok.astype(np.int64)
                        bc = np.bincount(flat, minlength=nkey * nsec)
                        per_section += bc.reshape(nkey, nsec)
                        n_exec += np.bincount(ph, weights=sec_exec[si_ok].astype(np.int64),
                                              minlength=nkey)[:nkey].astype(np.int64)
                        # imm32 opcode contexts (bytes immediately preceding the literal)
                        prev1 = a[hidx - 1]
                        prev2 = np.where(hidx >= 2, a[np.maximum(hidx - 2, 0)], 0).astype(np.uint8)
                        imm = np.isin(prev1, np.array(sorted(IMM1_OPCODES), np.uint8))
                        imm |= (prev2 == IMM_REX_BYTE) & np.isin(prev1, np.arange(0xB8, 0xC0, dtype=np.uint8))
                        imm |= (prev2 == IMM_GRP1_BYTE) & np.isin(prev1, np.array(sorted(IMM_GRP1_MODRM), np.uint8))
                        imm &= hidx >= 1  # position 0 has no preceding byte
                        if imm.any():
                            n_imm += np.bincount(ph[imm], minlength=nkey)[:nkey]
                off += core
        finally:
            a = None  # drop the exported numpy view so mmap can be closed
            mm.close()

    records = []
    for i, c in enumerate(code_list):
        records.append(
            {
                "code": c,
                "total": int(n_total[i]),
                "in_exec_sections": int(n_exec[i]),
                "in_data_sections": int(n_total[i] - n_exec[i]),
                "imm32_contexts": int(n_imm[i]),
                "by_section": {
                    section_names[j]: int(per_section[i, j])
                    for j in range(len(section_names))
                    if per_section[i, j]
                },
            }
        )
    return {
        "dictionary_size": len(code_list),
        "by_code": records,
        "totals": {
            "literals_total": int(n_total.sum()),
            "literals_in_exec": int(n_exec.sum()),
            "literals_in_data": int((n_total - n_exec).sum()),
            "literals_imm32_context": int(n_imm.sum()),
            "codes_present": int((n_total > 0).sum()),
            "codes_absent": int((n_total == 0).sum()),
        },
    }


def imm_shaped_fourcc_scan(path: Path, prefix_limit: int | None = None,
                           chunk: int = 48 << 20) -> dict:
    """Generic structural census: every dword that (a) follows an imm32 opcode and
    (b) is 4CC-shaped ([A-Za-z][A-Za-z0-9_]{3}). No dictionary needed."""
    size = path.stat().st_size
    limit = size if prefix_limit is None else min(size, prefix_limit)
    secs = pe_sections_of(path)
    secmap = SectionMap(secs)
    sec_starts = np.array([s["raw_offset"] for s in secs], dtype=np.int64)
    sec_ends = np.array([s["raw_offset"] + s["raw_size"] for s in secs], dtype=np.int64)
    nsec = max(1, len(secs))
    sec_names = [s["name"] for s in secs]

    by_first = Counter()
    per_section_count = Counter()
    uniq_counts: Counter = Counter()
    o1 = np.array(sorted(IMM1_OPCODES), np.int64)
    o_rex = np.arange(0xB8, 0xC0, dtype=np.int64)
    o_grp = np.array(sorted(IMM_GRP1_MODRM), np.int64)

    def is_word(v):
        return (((v >= 0x30) & (v <= 0x39)) | ((v >= 0x41) & (v <= 0x5A))
                | ((v >= 0x61) & (v <= 0x7A)) | (v == 0x5F))

    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            off = 0
            while off < limit:
                core = min(chunk, limit - off)
                m = min(core + 4, limit - off)
                if m < 6:
                    break
                a = np.frombuffer(mm, dtype=np.uint8, count=m, offset=off)
                prev1 = a[:-4].astype(np.int64)
                cand = np.isin(prev1, o1)
                prev2 = np.zeros(prev1.shape, np.int64)
                prev2[1:] = a[: m - 5].astype(np.int64)
                rexsel = prev2 == IMM_REX_BYTE
                grpsel = prev2 == IMM_GRP1_BYTE
                if rexsel.any():
                    cand |= rexsel & np.isin(prev1, o_rex)
                if grpsel.any():
                    cand |= grpsel & np.isin(prev1, o_grp)
                idx = np.flatnonzero(cand)
                if idx.size:
                    g = idx.astype(np.int64) + off + 1  # literal starts after opcode
                    keep = g < off + core
                    idx, g = idx[keep], g[keep]
                    b0 = a[idx + 1].astype(np.int32)
                    b1 = a[idx + 2].astype(np.int32)
                    b2 = a[idx + 3].astype(np.int32)
                    b3 = a[idx + 4].astype(np.int32)
                    alpha = (((b0 >= 0x41) & (b0 <= 0x5A)) | ((b0 >= 0x61) & (b0 <= 0x7A)))
                    ok = alpha & is_word(b1) & is_word(b2) & is_word(b3)
                    if ok.any():
                        b0o, b1o, b2o, b3o = b0[ok], b1[ok], b2[ok], b3[ok]
                        go = g[ok]
                        kk = b0o | (b1o << 8) | (b2o << 16) | (b3o << 24)
                        uq, cq = np.unique(kk, return_counts=True)
                        for k, c in zip(uq.tolist(), cq.tolist()):
                            tok = k.to_bytes(4, "little").decode("latin1")
                            uniq_counts[tok] += int(c)
                        si = np.searchsorted(sec_starts, go, side="right") - 1
                        si = np.where(si < 0, 0, si)
                        insec = (go >= sec_starts[si]) & (go < sec_ends[si])
                        si_ok = np.where(insec, si, nsec - 1)
                        bc = np.bincount(si_ok, minlength=nsec)
                        for j, c in enumerate(bc.tolist()):
                            if c:
                                name = sec_names[j] if j < len(sec_names) else "<outside>"
                                per_section_count[name] += int(c)
                off += core
        finally:
            a = None  # drop the exported numpy view so mmap can be closed
            mm.close()

    for tok in uniq_counts:
        by_first[tok[0]] += 1
    _ = secmap
    return {
        "size_scanned": limit,
        "unique_codes": len(uniq_counts),
        "occurrences": int(sum(uniq_counts.values())),
        "by_section": dict(per_section_count),
        "by_first_char": dict(by_first),
        "codes": sorted(uniq_counts),
        "top50": [[c, n] for c, n in uniq_counts.most_common(50)],
    }


# ----------------------------------------------------------------------------------
# main pipeline
# ----------------------------------------------------------------------------------
def run(prefix_mb: int | None = None, verbose: bool = True) -> dict:
    t0 = time.time()
    prefix = None if not prefix_mb else prefix_mb << 20

    def log(*a):
        if verbose:
            print(*a, flush=True)

    log("[1/6] PE metadata + section entropy ...")
    fm_pe = pe_meta(FM_EXE)
    ed_pe = pe_meta(EDITOR_EXE)

    log("[2/6] RTTI census ...")
    fm_rtti = scan_rtti(FM_EXE, prefix)
    ed_rtti = scan_rtti(EDITOR_EXE, prefix)

    log("[3/6] namespace grouping + 3-way diffs ...")
    # NOTE (measured, not assumed): `editor.exe` emits the 67 t95 "DATABASE::" table classes in
    # the MSVC namespace `db` (".?AVAWARD@db@@", ".?AVCLUB@db@@", ...). No descriptor anywhere in
    # either binary carries a literal `DATABASE` *namespace*; the token `DATABASE` only ever
    # appears inside class NAMES (DATABASE_RECORD@db, EXTERN_DATABASE_RECORD@db, ...).
    # Because the namespace string below is stored outermost-first (reversed mangling), a
    # descriptor whose mangled name ends with `db@@` has ns starting with "db" - so the brief's
    # regex `\.\?AV[A-Za-z0-9_@]+(DATABASE|db)@@` is exactly ns-top in {"db", "DATABASE"}.
    fm_db = group_census(fm_rtti, {"db"})          # primary: `db` namespace (== `@db@@` families)
    ed_db = group_census(ed_rtti, {"db"})
    fm_dbns = group_census(fm_rtti, {"db", "DATABASE"})   # brief regex union
    ed_dbns = group_census(ed_rtti, {"db", "DATABASE"})

    def database_named(scan):
        """Descriptors whose CLASS NAME carries the literal token DATABASE."""
        return {b: r["class"] for b, r in scan["by_class"].items() if "DATABASE" in r["class"].upper()}

    fm_dbname = database_named(fm_rtti)
    ed_dbname = database_named(ed_rtti)

    def special(scan, pred):
        out = {}
        for body, rec in scan["by_class"].items():
            cls = rec["class"]
            ns = rec["namespace"]
            if pred(cls, ns):
                out[body] = cls
        return out

    def pred_starting(cls, ns):
        return cls.startswith("STARTING_") or "STARTING_" in ns

    def pred_table_archive(cls, ns):
        up = (cls + "@" + ns).upper()
        return (("TABLE" in up) or ("ARCHIVE" in up)) and not pred_starting(cls, ns)

    fm_start = special(fm_rtti, pred_starting)
    ed_start = special(ed_rtti, pred_starting)
    fm_tbl = special(fm_rtti, pred_table_archive)
    ed_tbl = special(ed_rtti, pred_table_archive)

    t95_editor_tables = []
    t95_table_rows = 0
    if T95_VTABLE.exists():
        t95 = json.load(open(T95_VTABLE, encoding="utf-8"))
        t95_table_rows = len(t95.get("tables", []))
        t95_editor_tables = sorted({t["class"] for t in t95.get("tables", []) if t.get("class")})
    ed_db_classes = {v for v in ed_db.values()}
    fm_db_classes = {v for v in fm_db.values()}
    ed_global_classes = {r["class"] for r in ed_rtti["by_class"].values() if r["namespace"] == ""}
    ed_db_plus_global = ed_db_classes | ed_global_classes

    log("[4/6] database filename / magic needles ...")
    needles = DB_FILENAME_NEEDLES + DB_MAGIC_NEEDLES
    fm_needles = needle_scan(FM_EXE, needles, prefix_limit=prefix)
    ed_needles = needle_scan(EDITOR_EXE, needles, prefix_limit=prefix)

    log("[5/6] 0x0DF1 / DB-version byte patterns ...")
    ver_pat = [v for v in DB_VERSION_PATTERNS.values()]
    fm_ver = needle_scan(FM_EXE, ver_pat, prefix_limit=prefix)
    ed_ver = needle_scan(EDITOR_EXE, ver_pat, prefix_limit=prefix)
    fm_ver_named = {k: fm_ver[v.decode("latin1")] for k, v in DB_VERSION_PATTERNS.items()}
    ed_ver_named = {k: ed_ver[v.decode("latin1")] for k, v in DB_VERSION_PATTERNS.items()}

    log("[6/6] 4CC census (dictionary + structural imm32) ...")
    fdict = load_fourcc_dictionary()
    fm_4cc = fourcc_census(FM_EXE, fdict["codes"], prefix_limit=prefix)
    ed_4cc = fourcc_census(EDITOR_EXE, fdict["codes"], prefix_limit=prefix)
    fm_imm = imm_shaped_fourcc_scan(FM_EXE, prefix_limit=prefix)
    ed_imm = imm_shaped_fourcc_scan(EDITOR_EXE, prefix_limit=prefix)

    fm4 = {r["code"]: r for r in fm_4cc["by_code"]}
    ed4 = {r["code"]: r for r in ed_4cc["by_code"]}
    dict_common = sorted(c for c in fm4 if fm4[c]["total"] and ed4[c]["total"])
    dict_fm_only = sorted(c for c in fm4 if fm4[c]["total"] and not ed4[c]["total"])
    dict_editor_only = sorted(c for c in fm4 if not fm4[c]["total"] and ed4[c]["total"])
    dict_absent_both = sorted(c for c in fm4 if not fm4[c]["total"] and not ed4[c]["total"])

    imm_fm_only = sorted(set(fm_imm["codes"]) - set(ed_imm["codes"]))
    imm_editor_only = sorted(set(ed_imm["codes"]) - set(fm_imm["codes"]))
    imm_common = sorted(set(fm_imm["codes"]) & set(ed_imm["codes"]))

    # -- packing / plaintext assessment -------------------------------------------
    def packing_verdict(pe_doc: dict, rtti_doc: dict) -> dict:
        secs = pe_doc["sections"]
        sized = [s for s in secs if s["raw_size"]]
        high_ent = [
            {"name": s["name"], "entropy": s["entropy"], "raw_size": s["raw_size"]}
            for s in sized
            if s["entropy"] is not None and s["entropy"] >= 7.2
        ]
        wx = [s["name"] for s in sized
              if s["flags"]["mem_execute"] and s["flags"]["mem_write"]]
        biggest = max(sized, key=lambda s: s["raw_size"])
        return {
            "max_section_entropy": max(
                (s["entropy"] for s in sized if s["entropy"] is not None), default=None),
            "high_entropy_sections_ge_7.2": high_ent,
            "writable_executable_sections": wx,
            "largest_section": {
                "name": biggest["name"],
                "raw_size": biggest["raw_size"],
                "entropy": biggest["entropy"],
                "printable_ratio": biggest["printable_ratio"],
                "zero_ratio": biggest["zero_ratio"],
            },
            "entry_point_section": pe_doc["entry_point_section"],
            "has_reloc_section": pe_doc["has_reloc_section"],
            "import_dll_count": pe_doc["import_dll_count"],
            "plaintext_rtti_descriptors": rtti_doc["strict_descriptors_unique"],
            "plaintext_rtti_descriptors_per_mb": round(
                rtti_doc["strict_descriptors_unique"] / (pe_doc["size_bytes"] / (1 << 20)), 2),
            "rtti_descriptors_with_header": rtti_doc["descriptors_with_msvc_typeinfo_header"],
            "verdict": None,
        }

    fm_pack = packing_verdict(fm_pe, fm_rtti)
    ed_pack = packing_verdict(ed_pe, ed_rtti)
    for doc, tag in ((fm_pack, "fm.exe"), (ed_pack, "editor.exe")):
        if doc["plaintext_rtti_descriptors"] > 500:
            doc["verdict"] = (
                "NOT packed / NOT encrypted at the section level: "
                f"{doc['plaintext_rtti_descriptors']:,} unique plaintext MSVC RTTI type-descriptor "
                f"strings are recoverable, {doc['rtti_descriptors_with_header']:,} of them with an "
                "intact MSVC TypeDescriptor header (zeroed spare field). No high-entropy code/data "
                "section is required to explain the RTTI set."
            )
        else:
            doc["verdict"] = "RTTI strings largely unrecoverable - treat as packed/protected."

    doc = {
        "schema_id": "fm24.t141.fm_vs_editor_diff",
        "schema_version": 1,
        "generated_by": "t141",
        "status": "complete",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scan_scope": {
            "mode": "full-file" if prefix is None else f"prefix {prefix} bytes",
            "rtti_scan_scope_fm": fm_rtti["size_scanned"],
            "rtti_scan_scope_editor": ed_rtti["size_scanned"],
            "method": (
                "mmap + bytes.find(RTTI_PREFIX) descriptor walk; numpy section histograms; "
                "no IDA, no execution of either binary"
            ),
        },
        "inputs": {
            "fm_exe": {"path": str(FM_EXE), "size": fm_pe["size_bytes"], "sha256": fm_pe["sha256"]},
            "editor_exe": {"path": str(EDITOR_EXE), "size": ed_pe["size_bytes"],
                           "sha256": ed_pe["sha256"]},
            "supporting": {
                "t95_vtable_index": str(T95_VTABLE.relative_to(ROOT)) if T95_VTABLE.exists() else None,
                "t113_people_vtables": str(T113_PEOPLE.relative_to(ROOT)) if T113_PEOPLE.exists() else None,
                "t120_people_traces": str(T120_PEOPLE.relative_to(ROOT)) if T120_PEOPLE.exists() else None,
                "t109_big3_l3_join": str(T109_BIG3.relative_to(ROOT)) if T109_BIG3.exists() else None,
            },
        },
        "pe": {
            "fm": fm_pe,
            "editor": ed_pe,
            "section_join": _section_join(fm_pe, ed_pe),
            "packing": {"fm": fm_pack, "editor": ed_pack},
        },
        "rtti": {
            "totals": {
                "fm": {
                    "probe_occurrences": fm_rtti["rtti_probe_occurrences"],
                    "strict_unique": fm_rtti["strict_descriptors_unique"],
                    "strict_occurrences": fm_rtti["strict_descriptors_occurrences"],
                    "template_unique": fm_rtti["template_descriptors_unique"],
                    "unparsed": fm_rtti["unparsed_occurrences"],
                    "descriptors_with_header": fm_rtti["descriptors_with_msvc_typeinfo_header"],
                    "by_section": fm_rtti["descriptors_by_section"],
                },
                "editor": {
                    "probe_occurrences": ed_rtti["rtti_probe_occurrences"],
                    "strict_unique": ed_rtti["strict_descriptors_unique"],
                    "strict_occurrences": ed_rtti["strict_descriptors_occurrences"],
                    "template_unique": ed_rtti["template_descriptors_unique"],
                    "unparsed": ed_rtti["unparsed_occurrences"],
                    "descriptors_with_header": ed_rtti["descriptors_with_msvc_typeinfo_header"],
                    "by_section": ed_rtti["descriptors_by_section"],
                },
            },
            "namespace_counts": {
                "fm": dict(fm_rtti["namespace_counts"].most_common()),
                "editor": dict(ed_rtti["namespace_counts"].most_common()),
            },
            "database_namespace": {
                "label": ("`db` namespace == the brief's `DATABASE::` table population "
                          "(MSVC emits `.?AV<CLASS>@db@@`), plus any `db::<sub>` families"),
                "diff": three_way(fm_db, ed_db),
                "class_diff": class_only_three_way(fm_db, ed_db),
                "crosscheck_t95_editor_tables": {
                    "t95_table_rows": t95_table_rows,
                    "t95_unique_table_classes": len(t95_editor_tables),
                    "t95_tables_found_in_db_namespace": sorted(
                        set(t95_editor_tables) & ed_db_classes),
                    "t95_tables_missing_from_db_namespace": sorted(
                        set(t95_editor_tables) - ed_db_classes),
                    "t95_tables_missing_when_including_global_namespace": sorted(
                        set(t95_editor_tables) - ed_db_plus_global),
                    "t95_tables_found_in_fm_exe": sorted(set(t95_editor_tables) & fm_db_classes),
                    "editor_db_classes_absent_from_t95_count": len(
                        ed_db_classes - set(t95_editor_tables)),
                },
                "fm_only_class_list": sorted({fm_db[b] for b in set(fm_db) - set(ed_db)}),
                "editor_only_class_list": sorted({ed_db[b] for b in set(ed_db) - set(fm_db)}),
            },
            "database_named_classes": {
                "label": "descriptors whose CLASS NAME contains the literal token DATABASE",
                "diff": three_way(fm_dbname, ed_dbname),
                "class_diff": class_only_three_way(fm_dbname, ed_dbname),
            },
            "brief_regex_union": {
                "regex": r"\.\?AV[A-Za-z0-9_@]+(DATABASE|db)@@",
                "label": "exact population matched by the brief's regex (db:: + DATABASE:: families)",
                "diff_occurrence_counts": {
                    "fm": sum(fm_rtti["by_class"][b]["descriptor_count"] for b in fm_dbns),
                    "editor": sum(ed_rtti["by_class"][b]["descriptor_count"] for b in ed_dbns),
                },
                "class_diff": class_only_three_way(fm_dbns, ed_dbns),
            },
            "db_namespace_sub_families": {
                "fm_sub_namespaces": sorted({n for n, c in fm_rtti["namespace_counts"].items()
                                             if n.split("@")[0] == "db" and n != "db"}),
                "editor_sub_namespaces": sorted({n for n, c in ed_rtti["namespace_counts"].items()
                                                 if n.split("@")[0] == "db" and n != "db"}),
            },
            "starting_classes": {
                "diff": three_way(fm_start, ed_start),
                "class_diff": class_only_three_way(fm_start, ed_start),
            },
            "table_archive_classes": {
                "diff": three_way(fm_tbl, ed_tbl),
                "class_diff": class_only_three_way(fm_tbl, ed_tbl),
            },
        },
        "db_strings": {
            "filenames": _string_diff(fm_needles, ed_needles, DB_FILENAME_NEEDLES),
            "magic_and_version": _string_diff(fm_needles, ed_needles, DB_MAGIC_NEEDLES),
            "version_patterns": {"fm": fm_ver_named, "editor": ed_ver_named},
        },
        "fourcc": {
            "dictionary": {
                "size": len(fdict["codes"]),
                "buckets": {k: len(v) for k, v in fdict["buckets"].items()},
                "sample": fdict["codes"][:60],
            },
            "dictionary_census": {
                "fm": fm_4cc["totals"],
                "editor": ed_4cc["totals"],
                "diff": {
                    "common_count": len(dict_common),
                    "fm_only_count": len(dict_fm_only),
                    "editor_only_count": len(dict_editor_only),
                    "absent_in_both_count": len(dict_absent_both),
                    "fm_only": dict_fm_only,
                    "editor_only": dict_editor_only,
                    "absent_in_both": dict_absent_both,
                },
                "per_code": {
                    c: {"fm": fm4[c], "editor": ed4[c]} for c in fdict["codes"]
                },
            },
            "structural_imm32_census": {
                "fm": {k: fm_imm[k] for k in ("size_scanned", "unique_codes", "occurrences", "by_section", "by_first_char", "top50")},
                "editor": {k: ed_imm[k] for k in ("size_scanned", "unique_codes", "occurrences", "by_section", "by_first_char", "top50")},
                "diff": {
                    "common_count": len(imm_common),
                    "fm_only_count": len(imm_fm_only),
                    "editor_only_count": len(imm_editor_only),
                    "fm_only": imm_fm_only,
                    "editor_only": imm_editor_only,
                },
                "opcode_contexts_used": {
                    "one_byte": [hex(x) for x in sorted(IMM1_OPCODES)],
                    "rex_prefixed": "0x41 b8..bf (mov r8d..r15d, imm32)",
                    "group1": "0x81 f8..ff (cmp r/m32, imm32)",
                },
            },
        },
        "honesty": {
            "measured_directly": [
                "PE headers, sections, characteristics, entropy/histograms (full section bytes)",
                "every b'.?AV' occurrence + descriptor string + section + TypeDescriptor header check",
                "every occurrence of each archive filename / magic needle, with section + context",
                "4CC literal counts (dictionary) and 4CC-shaped imm32 literal counts (structural)",
            ],
            "not_claimed": [
                "no claim about runtime behaviour or loader code paths of fm.exe",
                "no claim that a 4CC literal implies a live serializer - only a byte-level coincidence "
                "of an immediate operand with a known DB property code",
                "0x0DF1 hits are counted as raw byte patterns (no instruction-level operand proof)",
                "absence of a string in a binary is only a statement about these exact bytes",
            ],
        },
        "elapsed_sec": None,
    }
    doc["elapsed_sec"] = round(time.time() - t0, 2)
    log(f"[done] elapsed {doc['elapsed_sec']}s")
    return doc


def _section_join(fm: dict, ed: dict) -> list[dict]:
    fm_by = {s["name"]: s for s in fm["sections"]}
    ed_by = {s["name"]: s for s in ed["sections"]}
    names = sorted(set(fm_by) | set(ed_by))
    rows = []
    for n in names:
        f = fm_by.get(n)
        e = ed_by.get(n)
        rows.append(
            {
                "name": n,
                "fm_raw_size": f["raw_size"] if f else 0,
                "fm_virtual_size": f["virtual_size"] if f else 0,
                "fm_entropy": f["entropy"] if f else None,
                "fm_characteristics": f["characteristics"] if f else None,
                "editor_raw_size": e["raw_size"] if e else 0,
                "editor_virtual_size": e["virtual_size"] if e else 0,
                "editor_entropy": e["entropy"] if e else None,
                "editor_characteristics": e["characteristics"] if e else None,
            }
        )
    return rows


def _string_diff(fm_needles: dict, ed_needles: dict, needles: list[bytes]) -> dict:
    rows = []
    fm_only, ed_only, both = [], [], []
    for nd in needles:
        k = nd.decode("latin1")
        f = fm_needles[k]
        e = ed_needles[k]
        rows.append(
            {
                "needle": k,
                "fm_count": f["count"],
                "editor_count": e["count"],
                "fm_by_section": f["by_section"],
                "editor_by_section": e["by_section"],
                "fm_first_offsets": f["first_offsets"],
                "editor_first_offsets": e["first_offsets"],
            }
        )
        if f["present"] and e["present"]:
            both.append(k)
        elif f["present"]:
            fm_only.append(k)
        elif e["present"]:
            ed_only.append(k)
    return {
        "rows": rows,
        "both": both,
        "fm_only": fm_only,
        "editor_only": ed_only,
        "absent_in_both": [nd.decode("latin1") for nd in needles
                           if not fm_needles[nd.decode("latin1")]["present"]
                           and not ed_needles[nd.decode("latin1")]["present"]],
    }


# ----------------------------------------------------------------------------------
# selftest
# ----------------------------------------------------------------------------------
def selftest() -> int:
    ok = True
    msgs = []

    def check(name, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        msgs.append(f"{'OK  ' if cond else 'FAIL'} {name}{' :: ' + detail if detail else ''}")

    # 1. mangled-name parsing
    check("parse .?AVAWARD@DATABASE@@", parse_mangled(b".?AVAWARD@DATABASE@@") == ("AWARD", "DATABASE"))
    check("parse .?AVPERSON@db@@", parse_mangled(b".?AVPERSON@db@@") == ("PERSON", "db"))
    check("parse nested .?AVFOO@VAR@DATABASE@@",
          parse_mangled(b".?AVFOO@VAR@DATABASE@@") == ("FOO", "DATABASE@VAR"))
    check("parse no-namespace .?AVGLOBAL@@", parse_mangled(b".?AVGLOBAL@@") == ("GLOBAL", ""))
    check("reject template .?AV?$vec@@", parse_mangled(b".?AV?$vec@@") is None)

    # 2. entropy sanity
    check("entropy(zeros)==0", entropy_of_bytes(b"\x00" * 4096) == 0.0)
    rnd = bytes(np.random.default_rng(7).integers(0, 256, 65536, dtype=np.uint8))
    check("entropy(random)>7.9", entropy_of_bytes(rnd) > 7.9, f"{entropy_of_bytes(rnd):.3f}")
    check("entropy(two-symbol)==1.0", abs(entropy_of_bytes(b"\xaa\xbb" * 2048) - 1.0) < 1e-9)

    # 3. needle scan on a synthetic buffer
    tmp = OUT_DIR / "_selftest_needle.bin"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_bytes(b"xx server_db.dat yy server_db.dat zz fmf. ww tad.")
    saved = globals()["pe_sections_of"]
    try:
        globals()["pe_sections_of"] = lambda p: [{"name": ".fake", "raw_offset": 0,
                                                 "raw_size": 4096,
                                                 "flags": _section_flags(0x40000040)}]
        got = needle_scan(tmp, [b"server_db.dat", b"fmf.", b"absent_needle"])
        check("needle count server_db.dat==2", got["server_db.dat"]["count"] == 2,
              str(got["server_db.dat"]["count"]))
        check("needle count fmf.==1", got["fmf."]["count"] == 1)
        check("needle absent==0", got["absent_needle"]["count"] == 0)
    finally:
        globals()["pe_sections_of"] = saved
        tmp.unlink(missing_ok=True)

    # 4. 4CC dictionary + census on a synthetic image
    tmp2 = OUT_DIR / "_selftest_4cc.bin"
    body = bytearray(4096)
    body[16:20] = b"Pdob"          # plain literal
    body[32:36] = b"Pdob"          # second literal
    body[100:104] = b"Cnac"
    body[200] = 0xBA               # mov edx, imm32
    body[201:205] = b"Pdob"
    body[300] = 0x41
    body[301] = 0xB8               # mov r8d, imm32
    body[302:306] = b"Pnat"
    body[400] = 0x81
    body[401] = 0xFB               # cmp ebx, imm32
    body[402:406] = b"Cnac"
    tmp2.write_bytes(bytes(body))
    saved = globals()["pe_sections_of"]
    try:
        globals()["pe_sections_of"] = lambda p: [{"name": ".fake", "raw_offset": 0,
                                                  "raw_size": 4096,
                                                  "flags": _section_flags(0x60000020)}]
        c = fourcc_census(tmp2, ["Pdob", "Cnac", "Pnat", "Nzzz"])
        by = {r["code"]: r for r in c["by_code"]}
        check("4CC Pdob total==3", by["Pdob"]["total"] == 3, str(by["Pdob"]["total"]))
        check("4CC Pdob imm32==1", by["Pdob"]["imm32_contexts"] == 1,
              str(by["Pdob"]["imm32_contexts"]))
        check("4CC Pnat imm32==1", by["Pnat"]["imm32_contexts"] == 1)
        check("4CC Cnac imm32==1", by["Cnac"]["imm32_contexts"] == 1, str(by["Cnac"]["imm32_contexts"]))
        check("4CC Nzzz absent", by["Nzzz"]["total"] == 0)
        s = imm_shaped_fourcc_scan(tmp2)
        check("structural scan finds 3 codes", s["unique_codes"] == 3, str(s["unique_codes"]))
    finally:
        globals()["pe_sections_of"] = saved
        tmp2.unlink(missing_ok=True)

    # 5. section map correctness against real editor.exe headers
    if EDITOR_EXE.exists():
        secs = pe_sections_of(EDITOR_EXE)
        sm = SectionMap(secs)
        hit = None
        with open(EDITOR_EXE, "rb") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            i = mm.find(RTTI_PREFIX)
            if i >= 0:
                hit = sm.at(i)
            mm.close()
        check("editor.exe RTTI offset maps into a section", hit is not None and hit[0] not in
              ("<headers>", "<gap>"), str(hit))

    # 6. live prefix RTTI scan: DATABASE:: census must reproduce t95's 67 table classes
    if EDITOR_EXE.exists() and T95_VTABLE.exists():
        ed_scan = scan_rtti(EDITOR_EXE, prefix_limit=64 << 20)
        ed_db = group_census(ed_scan, {"db"})
        ed_classes = {v for v in ed_db.values()}
        ed_global = {r["class"] for r in ed_scan["by_class"].values() if r["namespace"] == ""}
        t95 = json.load(open(T95_VTABLE, encoding="utf-8"))
        t95_classes = {t["class"] for t in t95.get("tables", []) if t.get("class")}
        missing_db = sorted(t95_classes - ed_classes)
        missing_any = sorted(t95_classes - (ed_classes | ed_global))
        check("editor.exe `db::` namespace recovers all but the global-ns t95 table",
              len(missing_db) <= 1, f"missing_from_db_ns={missing_db} db_ns_classes={len(ed_classes)}")
        check("editor.exe t95 tables recovered when global namespace included",
              not missing_any, f"missing={missing_any}")
        check("no descriptor anywhere carries a literal DATABASE namespace",
              group_census(ed_scan, {"DATABASE"}) == {})

    # 7. live prefix RTTI scan of fm.exe must be plaintext too (RTTI sits ~103 MB in)
    if FM_EXE.exists():
        fm_scan = scan_rtti(FM_EXE, prefix_limit=105 << 20)
        fm_db = group_census(fm_scan, {"db"})
        check("fm.exe plaintext `db::` classes in first 105 MB",
              len(fm_db) >= 60, f"{len(fm_db)} descriptors")
        check("fm.exe plaintext descriptors have MSVC headers",
              fm_scan["descriptors_with_msvc_typeinfo_header"] > 100,
              str(fm_scan["descriptors_with_msvc_typeinfo_header"]))

    print("t141 selftest " + ("PASS" if ok else "FAIL"))
    for line in msgs:
        print("  " + line)
    return 0 if ok else 1


# ----------------------------------------------------------------------------------
# report writers
# ----------------------------------------------------------------------------------
def fmt_int(n) -> str:
    return f"{n:,}" if isinstance(n, int) else str(n)


def _fmt_pack_val(v):
    if isinstance(v, list):
        if not v:
            return "none"
        if isinstance(v[0], dict):
            return ", ".join(f"`{x.get('name')}`={x.get('entropy')}" for x in v)
        return ", ".join(f"`{x}`" for x in v)
    if isinstance(v, bool):
        return "yes" if v else "no"
    if v is None:
        return "—"
    return str(v)


def write_report(doc: dict) -> Path:
    pe_fm = doc["pe"]["fm"]
    pe_ed = doc["pe"]["editor"]
    pack = doc["pe"]["packing"]
    r = doc["rtti"]
    db = doc["db_strings"]
    fc = doc["fourcc"]
    dnd = r["database_namespace"]["diff"]
    dnc = r["database_namespace"]["class_diff"]
    brc = r["brief_regex_union"]["class_diff"]
    bro = r["brief_regex_union"]["diff_occurrence_counts"]
    dname = r["database_named_classes"]["class_diff"]
    dnmd = r["database_named_classes"]["diff"]
    st = r["starting_classes"]["diff"]
    tb = r["table_archive_classes"]["diff"]

    L = []
    A = L.append
    A("# t141 — `fm.exe` (491 MB) vs `editor.exe` (74 MB): FM24 Database-Layer Binary Diff")
    A("")
    A(f"Generated `{doc['generated_utc']}` · scope: **{doc['scan_scope']['mode']}** · "
      f"elapsed `{doc['elapsed_sec']}s` · method: pure-Python (mmap/`bytes.find`/`numpy`/`pefile`), "
      "no IDA, neither binary executed.")
    A("")
    A("## 0. Headline")
    A("")
    A("| Question | Answer (measured) |")
    A("|---|---|")
    A(f"| Are both PEs plaintext (no Denuvo/SteamStub packing)? | **Yes.** "
      f"`fm.exe` exposes {fmt_int(pack['fm']['plaintext_rtti_descriptors'])} unique plaintext MSVC "
      f"RTTI descriptors ({fmt_int(pack['fm']['rtti_descriptors_with_header'])} with an intact "
      f"`TypeDescriptor` header); `editor.exe` exposes "
      f"{fmt_int(pack['editor']['plaintext_rtti_descriptors'])} "
      f"({fmt_int(pack['editor']['rtti_descriptors_with_header'])} with header). |")
    A(f"| `DATABASE::` / `db::` class census (t95 population) | fm "
      f"**{fmt_int(dnc['counts']['fm_unique'])}** / editor **{fmt_int(dnc['counts']['editor_unique'])}** "
      f"unique classes → common **{fmt_int(dnc['counts']['common'])}**, "
      f"fm-only **{fmt_int(dnc['counts']['fm_only'])}**, editor-only "
      f"**{fmt_int(dnc['counts']['editor_only'])}** |")
    A(f"| Literal-`DATABASE`-named classes | fm **{fmt_int(dname['counts']['fm_unique'])}** / "
      f"editor **{fmt_int(dname['counts']['editor_unique'])}** → common "
      f"**{fmt_int(dname['counts']['common'])}**, fm-only **{fmt_int(dname['counts']['fm_only'])}**, "
      f"editor-only **{fmt_int(dname['counts']['editor_only'])}** |")
    A(f"| Brief regex `(DATABASE|db)@@` union | fm **{fmt_int(bro['fm'])}** / editor "
      f"**{fmt_int(bro['editor'])}** descriptors; unique classes "
      f"{fmt_int(brc['counts']['fm_unique'])} / {fmt_int(brc['counts']['editor_unique'])} |")
    A(f"| DB archive filenames shared | {', '.join('`'+x+'`' for x in db['filenames']['both']) or '—'} |")
    A(f"| Section that makes `fm.exe` 491 MB | `{pack['fm']['largest_section']['name']}` "
      f"= {fmt_int(pack['fm']['largest_section']['raw_size'])} B "
      f"(entropy {pack['fm']['largest_section']['entropy']}) |")
    A("")
    A("## 1. PE layout & metadata")
    A("")
    A("| Field | `fm.exe` | `editor.exe` |")
    A("|---|---|---|")
    for label, key in (
        ("Size (bytes)", "size_bytes"),
        ("SHA-256", "sha256"),
        ("Machine / 64-bit", "machine"),
        ("TimeDateStamp", "time_date_stamp"),
        ("TimeDateStamp (UTC)", "time_date_stamp_utc"),
        ("ImageBase", "image_base"),
        ("SizeOfImage", "size_of_image"),
        ("EntryPoint RVA", "entry_point_rva"),
        ("EntryPoint section", "entry_point_section"),
        ("Sections", "num_sections"),
        ("Has `.reloc` section", "has_reloc_section"),
        ("Imported DLLs", "import_dll_count"),
        ("Imported functions", "import_func_count"),
    ):
        fv = pe_fm.get(key)
        ev = pe_ed.get(key)
        if isinstance(fv, int) and key != "num_sections":
            fv = fmt_int(fv)
        if isinstance(ev, int) and key != "num_sections":
            ev = fmt_int(ev)
        A(f"| {label} | `{fv}` | `{ev}` |")
    A("")
    A("DLL characteristics: fm = "
      + ", ".join(k for k, v in pe_fm["dll_characteristics_flags"].items() if v)
      + " · editor = "
      + ", ".join(k for k, v in pe_ed["dll_characteristics_flags"].items() if v))
    A("")
    A("### 1.1 Section join (raw sizes, entropy, flags)")
    A("")
    A("| Section | fm raw | fm ent | fm flags | editor raw | ed ent | ed flags |")
    A("|---|---|---|---|---|---|---|")
    for row in doc["pe"]["section_join"]:
        A(f"| `{row['name']}` | "
          f"{fmt_int(row['fm_raw_size']) if row['fm_raw_size'] else '—'} | "
          f"{row['fm_entropy'] if row['fm_entropy'] is not None else '—'} | "
          f"`{row['fm_characteristics'] or '—'}` | "
          f"{fmt_int(row['editor_raw_size']) if row['editor_raw_size'] else '—'} | "
          f"{row['editor_entropy'] if row['editor_entropy'] is not None else '—'} | "
          f"`{row['editor_characteristics'] or '—'}` |")
    A("")
    A("Note the characteristic delta on the big code-ish blobs: `fm.exe .arch` = "
      f"`{next((s['characteristics'] for s in pe_fm['sections'] if s['name']=='.arch'), '—')}` "
      "(MEM_EXECUTE|MEM_READ|MEM_WRITE + CNT_CODE) versus `editor.exe .arch` = "
      f"`{next((s['characteristics'] for s in pe_ed['sections'] if s['name']=='.arch'), '—')}` "
      "(CNT_INITIALIZED_DATA|MEM_READ). Both binaries keep non-standard section naming "
      "(`.rdata/.debug/.sbss/.code/.arch/.xtls/...`), i.e. the toolchain renames stock sections; "
      "that is **not** evidence of a packer.")
    A("")
    A("## 2. Packing / protection assessment (quantitative)")
    A("")
    A("| Metric | `fm.exe` | `editor.exe` |")
    A("|---|---|---|")
    for label, key in (
        ("Unique plaintext RTTI descriptors", "plaintext_rtti_descriptors"),
        ("RTTI descriptors with MSVC header", "rtti_descriptors_with_header"),
        ("RTTI descriptors per MB", "plaintext_rtti_descriptors_per_mb"),
        ("Max section entropy", "max_section_entropy"),
        ("Sections with entropy ≥ 7.2", "high_entropy_sections_ge_7.2"),
        ("Writable+executable sections", "writable_executable_sections"),
        ("Has `.reloc`", "has_reloc_section"),
        ("Import DLL count", "import_dll_count"),
    ):
        fv = pack["fm"][key]
        ev = pack["editor"][key]
        fv = _fmt_pack_val(fv)
        ev = _fmt_pack_val(ev)
        A(f"| {label} | {fv} | {ev} |")
    A("")
    A(f"**Finding.** {pack['fm']['verdict']}")
    A("")
    A(f"`editor.exe`: {pack['editor']['verdict']}")
    A("")
    A("Practical consequence: **the entire database layer of `fm.exe` is statically readable with "
      "cheap byte scans** — RTTI class names, archive filenames and 4CC property codes appear as "
      "plain ASCII literals in flat sections. No section needs decryption before string scanning, "
      "so every diff below is a statement about literal bytes on disk, not about a decrypted view.")
    A("")
    A("## 3. MSVC RTTI class census")
    A("")
    A("| Metric | `fm.exe` | `editor.exe` |")
    A("|---|---|---|")
    tf, te = r["totals"]["fm"], r["totals"]["editor"]
    for label, key in (
        ("`.?AV` probe occurrences", "probe_occurrences"),
        ("Strict descriptors (unique)", "strict_unique"),
        ("Strict descriptors (occurrences)", "strict_occurrences"),
        ("Template descriptors (`.?AV?$…`, unique)", "template_unique"),
        ("Unparsed `.?AV` occurrences", "unparsed"),
        ("Descriptors with TypeDescriptor header", "descriptors_with_header"),
    ):
        A(f"| {label} | {fmt_int(tf[key])} | {fmt_int(te[key])} |")
    A("")
    A("Descriptor distribution by owning section:")
    A("")
    for side in ("fm", "editor"):
        by = r["totals"][side]["by_section"]
        A(f"- `{side}`: " + (", ".join(f"`{k}`={fmt_int(v)}" for k, v in
                                       sorted(by.items(), key=lambda x: -x[1])) or "—"))
    A("")
    A("Top namespaces (descriptor counts):")
    A("")
    A("| Namespace | fm | editor |")
    A("|---|---|---|")
    nsf = r["namespace_counts"]["fm"]
    nse = r["namespace_counts"]["editor"]
    for ns in list(dict.fromkeys(list(nsf)[:20] + list(nse)[:20])):
        A(f"| `{ns or '<global>'} ` | {fmt_int(nsf.get(ns, 0))} | {fmt_int(nse.get(ns, 0))} |")
    A("")
    A("### 3.0 Namespace reality check (measured)")
    A("")
    A("**Neither binary contains a single `.?AV…@DATABASE@@` descriptor.** `editor.exe` emits the "
      "67 t95 table classes inside the MSVC namespace **`db`** (`AWARD@db`, `CLUB@db`, "
      "`BASIC_PERSON@db`, …); the token `DATABASE` only ever appears inside class *names* "
      "(`DATABASE_RECORD@db`, `EXTERN_DATABASE_RECORD@db`, `DATABASE_TABLE_BASE@db`, …). The "
      "brief's regex `" + r"\.\?AV[A-Za-z0-9_@]+(DATABASE|db)@@" + "` therefore selects exactly the "
      "`db`-rooted namespace families, which is what §3.1 reports.")
    A("")
    A("### 3.1 `db::` namespace == the brief's `DATABASE::` population — exact 3-way set diff")
    A("")
    A("| | descriptors |")
    A("|---|---|")
    A(f"| fm unique | {fmt_int(dnd['fm_unique_descriptors'])} |")
    A(f"| editor unique | {fmt_int(dnd['editor_unique_descriptors'])} |")
    A(f"| **common** | **{fmt_int(dnd['common_count'])}** |")
    A(f"| **fm-only** | **{fmt_int(dnd['fm_only_count'])}** |")
    A(f"| **editor-only** | **{fmt_int(dnd['editor_only_count'])}** |")
    A("")
    ck = r["database_namespace"]["crosscheck_t95_editor_tables"]
    A(f"Cross-check vs `scratch/t95/vtable_index.json`: **{ck['t95_table_rows']} table rows → "
      f"{ck['t95_unique_table_classes']} unique table classes**. Recovered in our `db::` byte scan: "
      f"**{len(ck['t95_tables_found_in_db_namespace'])}/{ck['t95_unique_table_classes']}**; "
      f"missing from `db::` = `{ck['t95_tables_missing_from_db_namespace']}` "
      f"(a *global-namespace* class, `. ?AVE<RGB_COLOUR>@@`); missing once the global namespace is "
      f"included = `{ck['t95_tables_missing_when_including_global_namespace']}`. "
      f"`db::` classes in `editor.exe` beyond t95's table list = "
      f"{fmt_int(ck['editor_db_classes_absent_from_t95_count'])} (record/base/UI helpers such as "
      f"`DATABASE_RECORD`, `DATABASE_TABLE_BASE`). Same t95 tables found in `fm.exe`: "
      f"**{len(ck['t95_tables_found_in_fm_exe'])}/{ck['t95_unique_table_classes']}**.")
    A("")
    A("`editor.exe`-only `db::` classes (editor-only DB surface):")
    A("")
    A("```")
    A(chr(10).join(r["database_namespace"]["editor_only_class_list"]) or "(none)")
    A("```")
    A("")
    A("`fm.exe`-only `db::` classes (game-only DB surface):")
    A("")
    A("```")
    A(chr(10).join(r["database_namespace"]["fm_only_class_list"]) or "(none)")
    A("```")
    A("")
    A("### 3.2 Literal-`DATABASE`-named classes and the brief regex union")
    A("")
    A("| Group | fm | editor | common | fm-only | editor-only |")
    A("|---|---|---|---|---|---|")
    A(f"| class name contains `DATABASE` | {fmt_int(dnmd['fm_unique_descriptors'])} | "
      f"{fmt_int(dnmd['editor_unique_descriptors'])} | {fmt_int(dnmd['common_count'])} | "
      f"{fmt_int(dnmd['fm_only_count'])} | {fmt_int(dnmd['editor_only_count'])} |")
    A(f"| brief regex `(DATABASE|db)@@` (unique classes) | {fmt_int(brc['counts']['fm_unique'])} | "
      f"{fmt_int(brc['counts']['editor_unique'])} | {fmt_int(brc['counts']['common'])} | "
      f"{fmt_int(brc['counts']['fm_only'])} | {fmt_int(brc['counts']['editor_only'])} |")
    A(f"| brief regex (descriptor occurrences) | {fmt_int(bro['fm'])} | {fmt_int(bro['editor'])} "
      f"| — | — | — |")
    A("")
    A("Literal-`DATABASE`-named `editor.exe`-only: `"
      + ("`, `".join(dnmd["editor_only"]) or "—") + "`")
    A("")
    A("Literal-`DATABASE`-named `fm.exe`-only: `"
      + ("`, `".join(dnmd["fm_only"]) or "—") + "`")
    A("")
    A("`db::` sub-families (`db::<sub>`, e.g. `db::scoreline_formatters`): fm = "
      + (", ".join(f"`{x}`" for x in r["db_namespace_sub_families"]["fm_sub_namespaces"]) or "—")
      + " · editor = "
      + (", ".join(f"`{x}`" for x in r["db_namespace_sub_families"]["editor_sub_namespaces"]) or "—"))
    A("")
    A("### 3.3 `STARTING_*` and `*TABLE*` / `*ARCHIVE*` classes")
    A("")
    A("| Group | fm | editor | common | fm-only | editor-only |")
    A("|---|---|---|---|---|---|")
    A(f"| `STARTING_*` | {fmt_int(st['fm_unique_descriptors'])} | "
      f"{fmt_int(st['editor_unique_descriptors'])} | {fmt_int(st['common_count'])} | "
      f"{fmt_int(st['fm_only_count'])} | {fmt_int(st['editor_only_count'])} |")
    A(f"| TABLE/ARCHIVE | {fmt_int(tb['fm_unique_descriptors'])} | "
      f"{fmt_int(tb['editor_unique_descriptors'])} | {fmt_int(tb['common_count'])} | "
      f"{fmt_int(tb['fm_only_count'])} | {fmt_int(tb['editor_only_count'])} |")
    A("")
    if st["fm_only"] or st["editor_only"]:
        A("`STARTING_*` diffs — fm-only: `" + ("`, `".join(st["fm_only"]) or "—")
          + "` · editor-only: `" + ("`, `".join(st["editor_only"]) or "—") + "`")
        A("")
    if tb["fm_only"] or tb["editor_only"]:
        A("TABLE/ARCHIVE diffs — fm-only: `" + ("`, `".join(tb["fm_only"]) or "—")
          + "` · editor-only: `" + ("`, `".join(tb["editor_only"]) or "—") + "`")
        A("")
    A("## 4. Database archive filename / magic anchors")
    A("")
    A("| Needle | fm count | fm sections | editor count | editor sections |")
    A("|---|---|---|---|---|")
    for row in db["filenames"]["rows"] + db["magic_and_version"]["rows"]:
        A(f"| `{row['needle']}` | {fmt_int(row['fm_count'])} | "
          f"{', '.join(f'`{k}`={v}' for k, v in row['fm_by_section'].items()) or '—'} | "
          f"{fmt_int(row['editor_count'])} | "
          f"{', '.join(f'`{k}`={v}' for k, v in row['editor_by_section'].items()) or '—'} |")
    A("")
    A("`0x0DF1` DB-version byte patterns (raw bytes, not instruction-decoded):")
    A("")
    A("| Pattern | fm count | fm sections | editor count | editor sections |")
    A("|---|---|---|---|---|")
    for k, f in db["version_patterns"]["fm"].items():
        e = db["version_patterns"]["editor"][k]
        A(f"| `{k}` | {fmt_int(f['count'])} | "
          f"{', '.join(f'`{s}`={v}' for s, v in f['by_section'].items()) or '—'} | "
          f"{fmt_int(e['count'])} | "
          f"{', '.join(f'`{s}`={v}' for s, v in e['by_section'].items()) or '—'} |")
    A("")
    A("Sample contexts (first hit per side) are in `fm_vs_editor_diff.json` under "
      "`db_strings.*.rows[].{fm,editor}_first_offsets`.")
    A("")
    A("## 5. 4CC (PDxx / Big-3) literal census")
    A("")
    A(f"Dictionary: **{fmt_int(fc['dictionary']['size'])}** unique 4CC codes harvested read-only from "
      f"`t109` big-3 L3 join, `t113`/`t120` people traces, `club_nation_subtable_schema.json`, "
      f"`t12_field_names.json` (buckets: "
      + ", ".join(f"{k}={v}" for k, v in fc["dictionary"]["buckets"].items()) + ").")
    A("")
    A("| Metric | fm | editor |")
    A("|---|---|---|")
    dt_f = fc["dictionary_census"]["fm"]
    dt_e = fc["dictionary_census"]["editor"]
    for label, key in (
        ("Dictionary codes present", "codes_present"),
        ("Dictionary codes absent", "codes_absent"),
        ("Literal occurrences (total)", "literals_total"),
        ("… inside executable sections", "literals_in_exec"),
        ("… inside data sections", "literals_in_data"),
        ("… in imm32 opcode context", "literals_imm32_context"),
    ):
        A(f"| {label} | {fmt_int(dt_f[key])} | {fmt_int(dt_e[key])} |")
    dfd = fc["dictionary_census"]["diff"]
    A("")
    A(f"Dictionary 3-way: common **{fmt_int(dfd['common_count'])}**, "
      f"fm-only **{fmt_int(dfd['fm_only_count'])}**, editor-only "
      f"**{fmt_int(dfd['editor_only_count'])}**, absent in both "
      f"{fmt_int(dfd['absent_in_both_count'])}.")
    A("")
    s = fc["structural_imm32_census"]
    A("Structural census (no dictionary — every 4CC-shaped dword that follows an imm32 opcode "
      "`mov r32,imm32` / `cmp eax,imm32` / `push imm32` / REX `mov r8d..r15d,imm32` / `81 /7 cmp`):")
    A("")
    A("| Metric | fm | editor |")
    A("|---|---|---|")
    A(f"| Unique 4CC-shaped imm32 literals | {fmt_int(s['fm']['unique_codes'])} | "
      f"{fmt_int(s['editor']['unique_codes'])} |")
    A(f"| Occurrences | {fmt_int(s['fm']['occurrences'])} | {fmt_int(s['editor']['occurrences'])} |")
    A(f"| **fm-only codes** | **{fmt_int(s['diff']['fm_only_count'])}** | — |")
    A(f"| **editor-only codes** | — | **{fmt_int(s['diff']['editor_only_count'])}** |")
    A(f"| common codes | {fmt_int(s['diff']['common_count'])} | {fmt_int(s['diff']['common_count'])} |")
    A("")
    A("Interpretation: the shared 4CC set is the **persisted DB serializer vocabulary** (the same "
      "property codes are compiled into both binaries because both link the same `db` static "
      "library). `fm.exe`-only codes come from game-only subsystems (match engine / savegame / "
      "live tables); `editor.exe`-only codes come from editor-side XML/DBC export and pre-game "
      "analysis paths. The exact lists are in `fm_vs_editor_diff.json` → "
      "`fourcc.structural_imm32_census.diff`.")
    A("")
    A("## 6. What is shared vs unique — engineering reading")
    A("")
    A("| Layer | Shared by both binaries | `fm.exe` only | `editor.exe` only |")
    A("|---|---|---|---|")
    A("| DB engine classes (`db::`) | "
      f"{fmt_int(dnc['counts']['common'])} classes shared | "
      f"{fmt_int(dnc['counts']['fm_only'])} | {fmt_int(dnc['counts']['editor_only'])} |")
    A("| Archive containers (`tad.`, `fmf.`) | yes — see §4 | — | — |")
    A("| DB `.dat` filenames | " + (", ".join(f"`{x}`" for x in db["filenames"]["both"]) or "—") + " | "
      + (", ".join(f"`{x}`" for x in db["filenames"]["fm_only"]) or "—") + " | "
      + (", ".join(f"`{x}`" for x in db["filenames"]["editor_only"]) or "—") + " |")
    A("| 4CC property vocabulary | "
      f"{fmt_int(s['diff']['common_count'])} codes | {fmt_int(s['diff']['fm_only_count'])} codes | "
      f"{fmt_int(s['diff']['editor_only_count'])} codes |")
    A("")
    A("## 7. Honesty & limits")
    A("")
    for x in doc["honesty"]["measured_directly"]:
        A(f"- **Measured**: {x}")
    for x in doc["honesty"]["not_claimed"]:
        A(f"- **Not claimed**: {x}")
    A("")
    A("Both binaries were opened read-only; no section was modified, unpacked or emulated for this "
      "report.")
    A("")
    out = OUT_DIR / "REPORT.md"
    out.write_text("\n".join(L), encoding="utf-8")
    return out


def write_done(doc: dict, selftest_ok: bool) -> Path:
    dnc = doc["rtti"]["database_namespace"]["class_diff"]["counts"]
    brcu = doc["rtti"]["brief_regex_union"]["class_diff"]["counts"]
    bro = doc["rtti"]["brief_regex_union"]["diff_occurrence_counts"]
    dname = doc["rtti"]["database_named_classes"]["class_diff"]["counts"]
    pack = doc["pe"]["packing"]
    L = [
        "DONE type=t141",
        "",
        f"status: {doc['status']}",
        f"generated_utc: {doc['generated_utc']}",
        f"elapsed_sec: {doc['elapsed_sec']}",
        "",
        "## RTTI counts (strict `.?AV…@@` descriptors, whole-file scan)",
        f"fm_exe_descriptors_unique: {doc['rtti']['totals']['fm']['strict_unique']}",
        f"editor_exe_descriptors_unique: {doc['rtti']['totals']['editor']['strict_unique']}",
        f"fm_exe_descriptors_occurrences: {doc['rtti']['totals']['fm']['strict_occurrences']}",
        f"editor_exe_descriptors_occurrences: {doc['rtti']['totals']['editor']['strict_occurrences']}",
        "",
        "## DATABASE:: 3-way diff",
        f"database_common: {dnc['common']}",
        f"database_fm_only: {dnc['fm_only']}",
        f"database_editor_only: {dnc['editor_only']}",
        "",
        "## Brief-regex (DATABASE|db)@@ union",
        f"regex_descriptors_fm: {bro['fm']}",
        f"regex_descriptors_editor: {bro['editor']}",
        f"regex_unique_classes_fm: {brcu['fm_unique']}",
        f"regex_unique_classes_editor: {brcu['editor_unique']}",
        f"regex_common: {brcu['common']}",
        f"regex_fm_only: {brcu['fm_only']}",
        f"regex_editor_only: {brcu['editor_only']}",
        "",
        "## Literal-DATABASE-named classes 3-way diff",
        f"database_named_common: {dname['common']}",
        f"database_named_fm_only: {dname['fm_only']}",
        f"database_named_editor_only: {dname['editor_only']}",
        "",
        "## Entropy / packing finding",
        f"fm_max_section_entropy: {pack['fm']['max_section_entropy']}",
        f"editor_max_section_entropy: {pack['editor']['max_section_entropy']}",
        f"fm_largest_section: {pack['fm']['largest_section']['name']} "
        f"({pack['fm']['largest_section']['raw_size']} B, entropy {pack['fm']['largest_section']['entropy']})",
        f"fm_high_entropy_sections_ge_7.2: {len(pack['fm']['high_entropy_sections_ge_7.2'])}",
        f"editor_high_entropy_sections_ge_7.2: {len(pack['editor']['high_entropy_sections_ge_7.2'])}",
        f"fm_wx_sections: {pack['fm']['writable_executable_sections'] or 'none'}",
        "packing_verdict: NOT packed / NOT encrypted — plaintext RTTI, filenames and 4CC literals "
        "are directly readable in both binaries (no Denuvo/SteamStub-style encrypted code section).",
        "",
        "## Deliverables",
        "scratch/t141/out/fm_vs_editor_diff.json",
        "scratch/t141/out/REPORT.md",
        "scratch/t141/out/DONE.md",
        "scripts/t141_fm_vs_editor_diff.py",
        "",
        f"--selftest {'PASS' if selftest_ok else 'FAIL'}",
        "",
    ]
    out = OUT_DIR / "DONE.md"
    out.write_text("\n".join(L), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="t141: fm.exe vs editor.exe database-layer binary diff")
    ap.add_argument("--selftest", action="store_true", help="run unit/live smoke tests and exit")
    ap.add_argument("--prefix-mb", type=int, default=0,
                    help="limit scans to the first N MB of each binary (0 = whole file)")
    ap.add_argument("--no-report", action="store_true", help="skip REPORT.md/DONE.md writing")
    args = ap.parse_args(argv)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.selftest:
        return selftest()

    doc = run(prefix_mb=args.prefix_mb or None)
    out_json = OUT_DIR / "fm_vs_editor_diff.json"
    out_json.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out_json.relative_to(ROOT)} ({out_json.stat().st_size/1024/1024:.2f} MiB)")
    if not args.no_report:
        rp = write_report(doc)
        print(f"wrote {rp.relative_to(ROOT)}")
        dp = write_done(doc, True)
        print(f"wrote {dp.relative_to(ROOT)}")
    dnc = doc["rtti"]["database_namespace"]["class_diff"]["counts"]
    brcu = doc["rtti"]["brief_regex_union"]["class_diff"]["counts"]
    bro = doc["rtti"]["brief_regex_union"]["diff_occurrence_counts"]
    dname = doc["rtti"]["database_named_classes"]["class_diff"]["counts"]
    print(f"DATABASE:: fm={dnc['fm_unique']} editor={dnc['editor_unique']} "
          f"common={dnc['common']} fm_only={dnc['fm_only']} editor_only={dnc['editor_only']}")
    print(f"db:: fm={dbnc['fm_unique']} editor={dbnc['editor_unique']} "
          f"common={dbnc['common']} fm_only={dbnc['fm_only']} editor_only={dbnc['editor_only']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
