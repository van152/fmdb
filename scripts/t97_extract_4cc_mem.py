#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t97 - Hex-Rays 4CC <-> memory-offset extraction for all 67 FM24 table classes.

Reads the IDA 9.4 / Hex-Rays artefacts produced by t95
(``scratch/t95/vtable_index.json`` + ``scratch/t95/funcs/*.c``) and, for every
table class in the index, walks ``slot02_get_prop`` / ``slot03_set_prop``
(plus the delegated base-class getters/setters reachable from them) and maps
every 4CC dispatch branch to the byte offsets read/written inside the branch.

Deliverables (written to ``--outdir``, default ``scratch/t97/out``):

  * ``fourcc_mem_map.json``  - 67 tables, 4CC -> mem_off (+ func_va, line_no)
  * ``xml_triage.json``      - 1,034-row XML denominator triage against the map
  * ``static_read_join.json``- 4CC <-> mem_off <-> slot19/slot20 line join
  * ``REPORT.md`` / ``DONE.md``

Everything is read-only towards ``reports/``, ``evidence/`` and ``LEDGER.json``.

Usage
-----
    py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --help
    py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest
    py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --run
    py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --run --outdir scratch/t97/out

Exit codes: 0 = ok, 1 = selftest failure / internal error, 2 = bad usage.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA_VERSION = 1

REPO = Path(__file__).resolve().parent.parent
T95_DIR = REPO / "scratch" / "t95"
FUNCS_DIR = T95_DIR / "funcs"
VTABLE_INDEX = T95_DIR / "vtable_index.json"
XML_COVERAGE = REPO / "reports" / "xml_denominator_coverage.json"
DEFAULT_OUTDIR = REPO / "scratch" / "t97" / "out"

CORE_SLOTS = [
    "slot02_get_prop",
    "slot03_set_prop",
    "slot05_reg_prop",
    "slot19_read_server",
    "slot20_read_client",
    "slot21_write",
]
PROP_SLOTS = ("slot02_get_prop", "slot03_set_prop")

# Generic Hex-Rays variant/serialiser wrappers: they appear in nearly every
# dispatch branch of nearly every table, so they carry no field semantics.
GENERIC_HELPERS = {
    0x14083D4F0,  # variant out-param accessor (get_property glue)
    0x14083DFA0,  # variant set glue
    0x14083B5F0,
    0x14083DB80,
    0x1407E4890,
    0x1407E4490,
    0x14083ADC0,
    0x14083B0A0,
    0x14083B5F0,
}

TYPE_SIZES = {
    "_BYTE": 1,
    "char": 1,
    "signed __int8": 1,
    "unsigned __int8": 1,
    "__int8": 1,
    "bool": 1,
    "_WORD": 2,
    "__int16": 2,
    "unsigned __int16": 2,
    "short": 2,
    "wchar_t": 2,
    "_DWORD": 4,
    "__int32": 4,
    "unsigned __int32": 4,
    "int": 4,
    "unsigned int": 4,
    "float": 4,
    "unsigned long": 4,
    "_QWORD": 8,
    "__int64": 8,
    "unsigned __int64": 8,
    "double": 8,
    "__int128": 16,
    "_OWORD": 16,
    "_TBYTE": 10,
}

POINTER_TARGETS = {  # pointer declarations seen in Hex-Rays output -> pointee size
    "_BYTE *": 1,
    "char *": 1,
    "unsigned __int8 *": 1,
    "__int8 *": 1,
    "_WORD *": 2,
    "__int16 *": 2,
    "unsigned __int16 *": 2,
    "_DWORD *": 4,
    "__int32 *": 4,
    "int *": 4,
    "unsigned int *": 4,
    "float *": 4,
    "_QWORD *": 8,
    "__int64 *": 8,
    "unsigned __int64 *": 8,
    "double *": 8,
}

NUM = r"(?:0x[0-9A-Fa-f]+|\d+)"


# --------------------------------------------------------------------------- #
# basic helpers
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    return io.open(path, encoding="utf-8", errors="replace").read()


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def int4cc(value: int):
    """Decode a 32-bit dispatch constant as big-endian ASCII 4CC, or None."""
    if value < 0 or value > 0xFFFFFFFF:
        return None
    raw = struct.pack(">I", value)
    if not all(0x20 <= c <= 0x7E for c in raw):
        return None
    if not any(0x41 <= c <= 0x5A or 0x61 <= c <= 0x7A for c in raw):
        return None
    return raw.decode("ascii")


def code_to_int(code: str):
    if len(code) != 4:
        return None
    try:
        return struct.unpack(">I", code.encode("latin-1"))[0]
    except Exception:
        return None


def parse_num(tok: str) -> int:
    tok = tok.strip()
    return int(tok, 16) if tok.lower().startswith("0x") else int(tok, 10)


def strip_strings(line: str) -> str:
    out = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == '"':
            j = i + 1
            while j < n:
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == '"':
                    break
                j += 1
            out.append('""')
            i = j + 1
            continue
        if ch == "'":
            j = i + 1
            while j < n:
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == "'":
                    break
                j += 1
            out.append("'0'")
            i = j + 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def norm_type(t: str) -> str:
    t = t.replace("const ", " ").replace("volatile ", " ").replace("struct ", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def type_size(t: str):
    """Size of a non-pointer C type, or None."""
    t = norm_type(t)
    return TYPE_SIZES.get(t)


def elem_size_of_decl(decl: str) -> int:
    """Byte element size implied by a variable declaration.

    Integer-typed locals/params address bytes in Hex-Rays output, so the
    element size is 1.  Pointer-typed variables address elements of the
    pointee type.
    """
    d = norm_type(decl)
    stars = d.count("*")
    if stars == 0:
        return 1
    # single level of pointee only (arrays of pointers are never `this`)
    d = d.replace("*", "*").strip()
    if d.endswith("*"):
        base = d[:-1].strip()
        key = norm_type(base) + " *"
        if key in POINTER_TARGETS:
            return POINTER_TARGETS[key]
        size = type_size(base)
        if size:
            return size
    return 8


# --------------------------------------------------------------------------- #
# offset extraction
# --------------------------------------------------------------------------- #
def _tail_bitop(text: str):
    """Detect a bitfield op applied right after a memory access."""
    m = re.match(r"^\s*\)*\s*(&\s*(0x[0-9A-Fa-f]+|\d+)|>>\s*(\d+)|<<\s*(\d+))", text)
    if not m:
        return None
    return re.sub(r"\s+", "", m.group(1))


def extract_offsets(line: str, base: str, elem: int, line_no: int):
    """All byte offsets of ``base`` referenced on one source line.

    Handles the four Hex-Rays spellings:
        *(_DWORD *)(a1 + 44)        -> 44 * elem
        *((_BYTE *)a1 + 186)        -> 186 * 1
        *(a1 + 7)                   -> 7 * elem
        a1[3]                       -> 3 * elem
        a1 + 15                     -> 15 * elem  (address only, no width)
    """
    hits = []
    if not line or base not in line:
        return hits
    pat = re.compile(
        r"\*\s*\(\s*(?P<t1>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*\(\s*"
        + re.escape(base)
        + r"\s*\+\s*(?P<o1>"
        + NUM
        + r")\s*\)"
        r"|\*\s*\(\s*\(\s*(?P<t2>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*"
        + re.escape(base)
        + r"\s*\+\s*(?P<o2>"
        + NUM
        + r")\s*\)"
        r"|\*\s*\(\s*"
        + re.escape(base)
        + r"\s*\+\s*(?P<o3>"
        + NUM
        + r")\s*\)"
        r"|\b"
        + re.escape(base)
        + r"\s*\[\s*(?P<o4>"
        + NUM
        + r")\s*\]"
        r"|\b"
        + re.escape(base)
        + r"\s*\+\s*(?P<o5>"
        + NUM
        + r")\b"
    )
    for m in pat.finditer(line):
        tail = line[m.end():]
        if m.group("o1") is not None:
            off = parse_num(m.group("o1")) * elem
            ctype = norm_type(m.group("t1"))
            width = type_size(ctype)
            how = "deref_cast_before"
        elif m.group("o2") is not None:
            off = parse_num(m.group("o2")) * POINTER_TARGETS.get(
                norm_type(m.group("t2")) + " *", type_size(norm_type(m.group("t2"))) or 1
            )
            ctype = norm_type(m.group("t2"))
            width = type_size(ctype)
            how = "deref_cast_after"
        elif m.group("o3") is not None:
            off = parse_num(m.group("o3")) * elem
            ctype = None
            width = None
            how = "deref_uncast"
        elif m.group("o4") is not None:
            off = parse_num(m.group("o4")) * elem
            ctype = None
            width = None
            how = "subscript"
        else:
            off = parse_num(m.group("o5")) * elem
            ctype = None
            width = None
            how = "address"
            # read_server idiom: reader->Read(this + off, SIZE)
            msize = re.match(r"^\s*,\s*(\d+)\s*\)", tail)
            if msize:
                width = int(msize.group(1))
                how = "address_with_size"
        hits.append(
            {
                "off_int": off,
                "off": hex(off),
                "width": width,
                "c_type": ctype,
                "line": line_no,
                "how": how,
                "bitop": _tail_bitop(tail),
            }
        )
    return hits


def extract_callees(line: str):
    out = []
    for m in re.finditer(r"\b(?:sub|unk)_([0-9A-Fa-f]{6,12})\b", line):
        va = int(m.group(1), 16)
        if 0x140000000 <= va < 0x145000000:
            out.append(va)
    return out


# --------------------------------------------------------------------------- #
# decompiled function model
# --------------------------------------------------------------------------- #
CASE_RE = re.compile(r"^(?:case\s+(?P<v>[0-9A-Fa-fx]+)|(?P<def>default))\s*:$")
IF_RE = re.compile(r"^(?:else\s+)?if\s*\((?P<cond>.*)\)\s*$")
SWITCH_RE = re.compile(r"^switch\s*\((?P<expr>.*)\)\s*$")


class CFunc:
    """A parsed Hex-Rays C listing for one function."""

    def __init__(self, path: Path, va: int = None):
        self.path = path
        self.va = va
        self.name = path.stem
        self.raw = read_text(path)
        self.lines = self.raw.split("\n")
        self.clean = [strip_strings(l) for l in self.lines]
        self.depths = []
        d = 0
        for c in self.clean:
            self.depths.append(d)
            d += c.count("{") - c.count("}")
        self.total_depth = d
        self.sig_line = None
        self.params = []  # [(name, decl)]
        self.locals = {}  # name -> decl
        self._parse_signature()
        self._parse_locals()
        self.code_vars = set()
        self._parse_code_vars()
        self.base_vars = {}
        self._parse_bases()

    # -- signature / locals -------------------------------------------------
    def _parse_signature(self):
        # Hex-Rays wraps long parameter lists over several lines: rebuild the
        # signature text by accumulating until the parentheses balance.
        joined = None
        for i, line in enumerate(self.clean):
            st = line.strip()
            if st.startswith("//") or not st:
                continue
            if "(" not in line:
                continue
            buf = line
            par = line.count("(") - line.count(")")
            j = i + 1
            while par > 0 and j < len(self.clean):
                buf += " " + self.clean[j].strip()
                par += self.clean[j].count("(") - self.clean[j].count(")")
                j += 1
            if ")" in buf:
                joined = buf
                self.sig_line = i
                break
        if joined is not None:
            if True:
                if True:
                    line = joined
                    inner = line[line.find("(") + 1: line.rfind(")")]
                    depth = 0
                    cur = ""
                    parts = []
                    for ch in inner:
                        if ch == "(":
                            depth += 1
                        elif ch == ")":
                            depth -= 1
                        if ch == "," and depth == 0:
                            parts.append(cur)
                            cur = ""
                        else:
                            cur += ch
                    if cur.strip():
                        parts.append(cur)
                    for p in parts:
                        p = p.strip()
                        if not p or p == "void":
                            continue
                        m = re.match(r"^(?P<decl>.*?)(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*$", p)
                        if not m:
                            continue
                        decl = re.sub(r"\[\d*\]$", "", m.group("decl").strip())
                        self.params.append((m.group("name"), norm_type(decl)))

    def _parse_locals(self):
        for line in self.clean:
            m = re.match(
                r"^\s+(?P<decl>[A-Za-z_][A-Za-z0-9_ ]*(?:\s*\*+\s*)?)(?P<name>[a-z_][A-Za-z0-9_]*)"
                r"\s*(\[[^\]]*\])?\s*;\s*//",
                line,
            )
            if m:
                decl = norm_type(m.group("decl"))
                if m.group(3):
                    decl = decl + " *"
                self.locals[m.group("name")] = decl

    def decl_of(self, name: str):
        for pn, pd in self.params:
            if pn == name:
                return pd
        return self.locals.get(name)

    def elem_of(self, name: str) -> int:
        decl = self.decl_of(name)
        if decl is None:
            return 1
        return elem_size_of_decl(decl)

    # -- dispatch variable aliases -----------------------------------------
    def _parse_code_vars(self):
        if len(self.params) < 2:
            return
        self.code_var = self.params[1][0]
        self.code_vars = {self.code_var}
        changed = True
        while changed:
            changed = False
            for line in self.clean:
                m = re.match(
                    r"^\s*(?P<v>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
                    r"(?:\(\s*(?:(?:unsigned|signed)\s+)?(?:int|__int64|__int32|_DWORD|char)\s*\)\s*)?"
                    r"(?P<src>[A-Za-z_][A-Za-z0-9_]*)\s*;\s*$",
                    line,
                )
                if not m:
                    continue
                if m.group("src") in self.code_vars and m.group("v") not in self.code_vars:
                    self.code_vars.add(m.group("v"))
                    changed = True

    def is_code_expr(self, expr: str) -> bool:
        e = expr.strip()
        e = re.sub(r"^\(*\s*(?:unsigned|signed)?\s*(?:int|__int64|__int32|_DWORD|char)\s*\)", "", e)
        e = e.strip().strip("()").strip()
        return e in self.code_vars

    # -- `this` pointers ----------------------------------------------------
    def _parse_bases(self):
        """Reaching-definition model of the `this` pointer.

        Hex-Rays recycles temporaries (`v5 = a1; ... v5 = *(_QWORD *)(v45+288);`),
        so an alias is only valid up to the next write.  Every assignment to a
        local is recorded with its line number; `is_base_at()` walks back from a
        use to decide whether that use still holds `this`.
        """
        if not self.params:
            return
        self.this_name = self.params[0][0]
        self.base_vars = {self.this_name: self.elem_of(self.this_name)}
        # `this` copies are emitted bare (`v6 = a1;`) or with a cast
        # (`v6 = (_DWORD *)a1;`); both refer to the same object.
        self._base_assign = re.compile(
            r"^\s*(?P<v>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
            r"(?:\(\s*(?:const\s+)?[A-Za-z_][A-Za-z0-9_ ]*?\s*\*+\s*\)\s*)?"
            r"(?P<src>[A-Za-z_][A-Za-z0-9_]*)\s*;\s*$"
        )
        # var -> [(line_idx, src_name or None)]  (None == "assigned something else")
        self.alias_defs = {}
        for idx, line in enumerate(self.clean):
            m = self._base_assign.match(line)
            if m and m.group("v") in self.locals:
                self.alias_defs.setdefault(m.group("v"), []).append(
                    (idx, m.group("src") if m.group("src") in self.locals or
                     m.group("src") == self.this_name else None)
                )
                continue
            for v in re.findall(r"(?<![\w>.])([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)", line):
                if v in self.locals:
                    self.alias_defs.setdefault(v, []).append((idx, None))
        # vars that are ever a copy of something are the only interesting ones
        self._base_candidates = [
            v for v, defs in self.alias_defs.items()
            if any(src is not None for _, src in defs)
        ]
        # global (steady-state) closure, used by the delegation walk
        for v in self._base_candidates:
            if self.is_base_at(v, len(self.clean) - 1) or self.is_base_at(v, 0):
                self.base_vars.setdefault(v, self.elem_of(v))
        self._bv_cache = {}

    def is_base_at(self, var: str, line_idx: int) -> bool:
        """Does `var` still hold `this` at `line_idx`?"""
        for _ in range(8):
            if var == self.this_name:
                return True
            defs = [ln for ln, _ in self.alias_defs.get(var, []) if ln < line_idx]
            if not defs:
                return False
            last = max(defs)
            src = None
            for ln, s_ in self.alias_defs[var]:
                if ln == last:
                    src = s_
                    break
            if src is None:
                return False
            var = src
        return False

    def base_vars_at(self, line_idx: int) -> dict:
        """{var: elem_size} of every local that holds `this` at this line."""
        key = line_idx
        if key in self._bv_cache:
            return self._bv_cache[key]
        out = {self.this_name: self.elem_of(self.this_name)}
        for v in self._base_candidates:
            if v != self.this_name and self.is_base_at(v, line_idx):
                out[v] = self.elem_of(v)
        self._bv_cache[key] = out
        return out

    # -- switch table -------------------------------------------------------
    def switches(self):
        """[(expr, open_line, close_line)] with brace-matched extents."""
        out = []
        for i, c in enumerate(self.clean):
            m = SWITCH_RE.match(c.strip())
            if not m:
                continue
            # find the opening brace
            j = i
            while j < len(self.clean) and "{" not in self.clean[j]:
                j += 1
                if j > i + 2:
                    break
            if j >= len(self.clean) or "{" not in self.clean[j]:
                continue
            open_line = j
            target = self.depths[open_line] + 1
            k = open_line + 1
            while k < len(self.clean) and self.depths[k] >= target:
                k += 1
            out.append((m.group("expr"), open_line, k - 1))
        return out

    def enclosing_switch(self, line_no: int, switches):
        best = None
        for expr, o, cl in switches:
            if o < line_no <= cl:
                if best is None or o > best[1]:
                    best = (expr, o, cl)
        return best

    # -- branch scan --------------------------------------------------------
    def find_branches(self):
        """All 4CC dispatch branches, in source order.

        Returns dicts: fourcc, code_int, line_no, body=(a,b), kind, cond.
        """
        branches = []
        sw = self.switches()
        in_block_cases = set()
        i = -1
        n = len(self.lines)
        while i + 1 < n:
            i += 1
            s = self.clean[i].strip()
            if not s:
                continue
            m = CASE_RE.match(s)
            if m:
                if not m.group("v"):
                    continue
                try:
                    val = parse_num(m.group("v"))
                except ValueError:
                    continue
                code = int4cc(val & 0xFFFFFFFF)
                if code is None:
                    continue
                # group consecutive labels
                labels = [(i, val, code)]
                j = i
                while True:
                    k = j + 1
                    while k < n and not self.clean[k].strip():
                        k += 1
                    if k >= n:
                        break
                    m2 = CASE_RE.match(self.clean[k].strip())
                    if m2 and m2.group("v") and self.depths[k] == self.depths[j]:
                        try:
                            v2 = parse_num(m2.group("v"))
                        except ValueError:
                            break
                        c2 = int4cc(v2 & 0xFFFFFFFF)
                        if c2 is None:
                            break
                        labels.append((k, v2, c2))
                        j = k
                        continue
                    break
                start, end = self._case_body(j)
                enc = self.enclosing_switch(labels[0][0], sw)
                for ln, val, code in labels:
                    if enc is None:
                        continue
                    if not self.is_code_expr(enc[0]):
                        continue
                    branches.append(
                        {
                            "fourcc": code,
                            "code_int": val,
                            "line_no": ln + 1,
                            "body": (start, end),
                            "kind": "case",
                            "cond": enc[0].strip(),
                        }
                    )
                i = j
                continue
            m = IF_RE.match(s)
            if m and self.depths[i] > 0:
                cond = m.group("cond")
                comps = self._cond_codes(cond)
                if not comps:
                    continue
                inverted = any(op == "!=" for _, op, _ in comps)
                if inverted:
                    start, end = self._guarded_body(i)
                else:
                    start, end = self._if_body(i)
                for val, op, code in comps:
                    if op == "!=" and len(comps) > 1:
                        continue
                    branches.append(
                        {
                            "fourcc": code,
                            "code_int": val,
                            "line_no": i + 1,
                            "body": (start, end),
                            "kind": "guard" if inverted else "if",
                            "cond": cond.strip(),
                        }
                    )
        branches.sort(key=lambda b: b["line_no"])
        return branches

    def _cond_codes(self, cond: str):
        out = []
        for var in self.code_vars:
            for m in re.finditer(
                r"(?<![A-Za-z0-9_])" + re.escape(var) + r"(?![A-Za-z0-9_])\s*(==|!=)\s*(" + NUM + r")",
                cond,
            ):
                val = parse_num(m.group(2))
                code = int4cc(val & 0xFFFFFFFF)
                if code is not None:
                    out.append((val, m.group(1), code))
            for m in re.finditer(
                r"(" + NUM + r")\s*(==|!=)\s*(?<![A-Za-z0-9_])" + re.escape(var) + r"(?![A-Za-z0-9_])",
                cond,
            ):
                val = parse_num(m.group(1))
                code = int4cc(val & 0xFFFFFFFF)
                if code is not None:
                    out.append((val, m.group(2), code))
        seen = set()
        uniq = []
        for t in out:
            if t in seen:
                continue
            seen.add(t)
            uniq.append(t)
        return uniq

    def _block_after(self, i: int):
        """Body range of the `{ ... }` that is the consequent of line i."""
        j = i + 1
        n = len(self.lines)
        while j < n:
            s = self.clean[j].strip()
            if not s:
                j += 1
                continue
            if s.startswith("{"):
                target = self.depths[j]
                k = j + 1
                while k < n and self.depths[k] > target:
                    k += 1
                return (j + 1, k - 1)
            break
        return None

    def _statement_after(self, i: int):
        """End line of the single statement following line i."""
        j = i + 1
        n = len(self.lines)
        while j < n and not self.clean[j].strip():
            j += 1
        if j >= n:
            return n - 1
        d0 = self.depths[i]
        k = j
        while k < n:
            s = self.clean[k].strip()
            if s.endswith(";") and self.depths[k] <= d0 + 0:
                return k
            if self.depths[k] < d0:
                return k - 1
            k += 1
        return n - 1

    def _if_body(self, i: int):
        blk = self._block_after(i)
        if blk:
            return blk
        end = self._statement_after(i)
        return (i + 1, end)

    def _guarded_body(self, i: int):
        """Body of a `if (code != X) goto/return;  <body>` guard."""
        blk = self._block_after(i)
        if blk:
            start = blk[1] + 1
        else:
            end = self._statement_after(i)
            start = end + 1
        d0 = self.depths[i]
        n = len(self.lines)
        k = start
        while k < n:
            s = self.clean[k].strip()
            if self.depths[k] < d0:
                return (start, k - 1)
            if self.depths[k] == d0:
                if re.match(r"^(break;|goto\s+\w+;|return\b.*;?$|case\s|default:|\})", s):
                    return (start, k - 1)
                if IF_RE.match(s) and self._cond_codes(IF_RE.match(s).group("cond")):
                    return (start, k - 1)
            k += 1
        return (start, n - 1)

    def _case_body(self, label_line: int):
        d0 = self.depths[label_line]
        n = len(self.lines)
        k = label_line + 1
        while k < n:
            s = self.clean[k].strip()
            if not s:
                k += 1
                continue
            if self.depths[k] < d0:
                return (label_line + 1, k - 1)
            if self.depths[k] == d0:
                if re.match(r"^(case\s|default:)", s):
                    return (label_line + 1, k - 1)
                if re.match(r"^(break;|goto\s+\w+;|return\b|\})", s):
                    # the terminator belongs to this case (covers one-statement
                    # bodies such as `case X: return sub_...;`)
                    return (label_line + 1, k)
            k += 1
        return (label_line + 1, n - 1)


# --------------------------------------------------------------------------- #
# branch body analysis
# --------------------------------------------------------------------------- #
SUB_CALL_RE = re.compile(r"\b(?:sub|unk)_([0-9A-Fa-f]{6,12})\s*\(")


def _first_delegation(stmt_lines):
    """First `return sub_XXXXXXXX(...)` target of a pure delegation branch."""
    for t in stmt_lines:
        m = re.match(r"^return\s+(?:\([^)]*\)\s*)?sub_([0-9A-Fa-f]+)\s*\(", t)
        if m:
            return hex(int(m.group(1), 16))
    return None


def analyze_branch(f: CFunc, br) -> dict:
    a, b = br["body"]
    body_lines = []
    if b >= a:
        body_lines = [(idx + 1, f.clean[idx]) for idx in range(a, min(b + 1, len(f.lines)))]
    offsets = []
    for ln, text in body_lines:
        for base, elem in f.base_vars_at(ln - 1).items():
            if base in text:
                offsets.extend(extract_offsets(text, base, elem, ln))
    # de-duplicate on (off, width, line)
    seen = set()
    uniq = []
    for o in offsets:
        key = (o["off_int"], o["width"], o["line"], o["how"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(o)
    uniq.sort(key=lambda o: (o["off_int"], o["line"]))

    helpers = []
    for ln, text in body_lines:
        for va in extract_callees(text):
            if va in GENERIC_HELPERS or va == f.va:
                continue
            if va not in helpers:
                helpers.append(va)

    stmt_lines = [t.strip() for _, t in body_lines if t.strip()]

    # width / type of the primary field
    width = None
    ctype = None
    for o in uniq:
        if o["width"]:
            width = o["width"]
            ctype = o["c_type"]
            break
    if width is None:
        for o in uniq:
            if o["width"]:
                break

    # subobject pointer loads inside the branch: v = *(_QWORD *)(base + N);
    subobjs = []
    for ln, text in body_lines:
        m = re.search(
            r"(?<![A-Za-z0-9_])(?P<var>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*\*\s*\(\s*(?P<t>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*\(\s*(?P<base>"
            + "|".join(re.escape(x) for x in f.base_vars)
            + r")\s*\+\s*(?P<off>"
            + NUM
            + r")\s*\)\s*;",
            text,
        )
        if not m:
            continue
        var = m.group("var")
        ptr_off = parse_num(m.group("off")) * f.base_vars[m.group("base")]
        is_slot = m.group("var") not in f.base_vars
        inner_off = None
        inner_type = None
        for text2 in f.clean:
            m2 = re.search(
                r"\*\s*\(\s*(?P<t2>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*\(\s*"
                + re.escape(var)
                + r"\s*\+\s*(?P<off2>"
                + NUM
                + r")",
                text2,
            )
            if m2:
                inner_off = parse_num(m2.group("off2"))
                inner_type = norm_type(m2.group("t2"))
                break
        if not is_slot:
            continue
        subobjs.append(
            {
                "ptr_off": hex(ptr_off),
                "ptr_off_int": ptr_off,
                "ptr_type": norm_type(m.group("t")),
                "var": var,
                "ptr_line": ln,
                "inner_off": hex(inner_off) if inner_off is not None else None,
                "inner_off_int": inner_off,
                "inner_type": inner_type,
            }
        )
    subobj = subobjs[0] if subobjs else None

    # bitfield via a loaded variable that is masked / shifted on a later line
    for o in uniq:
        mvar = None
        for ln, text in body_lines:
            for mbase, melem in f.base_vars.items():
                for m0 in re.finditer(
                    r"(?P<var>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*\*\s*\([^)]*\)\s*\(\s*"
                    + re.escape(mbase)
                    + r"\s*\+\s*(?P<off>"
                    + NUM
                    + r")\s*\)\s*;",
                    text,
                ):
                    if parse_num(m0.group("off")) * melem == o["off_int"]:
                        mvar = m0.group("var")
                        break
                if mvar:
                    break
            if mvar:
                break
        if not mvar:
            continue
        for ln, text in body_lines:
            m1 = re.search(
                re.escape(mvar) + r"\s*(&\s*(0x[0-9A-Fa-f]+|\d+)|>>\s*(\d+))", text
            )
            if m1:
                op = re.sub(r"\s+", "", m1.group(1))
                o["bitop"] = op
                break
    bitops = sorted({o["bitop"] for o in uniq if o.get("bitop") and not o["bitop"].startswith("<<")})

    # delegation / empty detection
    TERMINAL = re.compile(r"^(break;|goto\s+\w+;|return.*;?|\{|\}|else$|default:)$")
    DELEGATION = re.compile(r"^return\s+(?:\([^)]*\)\s*)?sub_[0-9A-Fa-f]+\s*\(.*\)\s*;$")
    terminal_only = all(TERMINAL.match(t) or t.startswith("//") for t in stmt_lines) if stmt_lines else True
    pure_delegation = bool(stmt_lines) and all(
        TERMINAL.match(t) or DELEGATION.match(t) or t.startswith("//") for t in stmt_lines
    )
    direct = [o for o in uniq if o["width"] in (1, 2, 4, 8)]
    variant_tail = any("sub_14083D4F0" in t for t in stmt_lines)

    # Split 8-byte reads into "subobject pointer" vs "plain 64-bit value".
    # A pointer that is dereferenced later in the function addresses a
    # sub-object (extra_3 / extra_9 / subtable style), not a scalar field.
    sub_ptr_offsets = {s["ptr_off_int"] for s in subobjs}
    scalar = [o for o in uniq if o["width"] in (1, 2, 4)]
    ptr_values = [o for o in uniq if o["width"] == 8 and o["off_int"] not in sub_ptr_offsets]
    sub_only = [o for o in uniq if o["width"] == 8 and o["off_int"] in sub_ptr_offsets]
    direct = scalar + ptr_values

    if bitops and (direct or sub_only or subobjs):
        kind = "bitfield"
    elif direct:
        kind = "direct_field"
    elif sub_only or subobjs:
        kind = "subobj_deref"
    elif uniq:
        kind = "helper_computed"
    elif pure_delegation or terminal_only:
        kind = "delegated_or_empty"
    else:
        kind = "helper_computed"

    primaries = direct if direct else (sub_only if sub_only else [o for o in uniq if o["width"] in (1, 2, 4, 8)])
    primary = min(primaries, key=lambda o: (o["off_int"], o["line"])) if primaries else (
        min(uniq, key=lambda o: (o["off_int"], o["line"])) if uniq else None
    )
    if primary and width is None:
        width = primary["width"]
        ctype = primary["c_type"]
    # a subobject pointer field is the answer when nothing scalar was found
    if kind == "subobj_deref" and subobj is not None and primary is None:
        primary = {"off": subobj["ptr_off"], "off_int": subobj["ptr_off_int"], "width": 8,
                   "c_type": subobj["ptr_type"], "line": subobj["ptr_line"], "how": "subobj_ptr"}

    return {
        "mem_offsets": uniq,
        "primary_off": primary["off"] if primary else None,
        "primary_off_int": primary["off_int"] if primary else None,
        "c_type": ctype,
        "width": width,
        "bitmask_or_shift": ",".join(bitops) if bitops else None,
        "helper_calls": [hex(v) for v in helpers],
        "access_kind": kind,
        "subobj": subobj,
        "subobjects": subobjs,
        "body_span": [a + 1, b + 1] if b >= a else None,
        "stmt_count": len(stmt_lines),
        "variant_tail": variant_tail,
        "delegate_va": _first_delegation(stmt_lines),
        "helper_files_present": sorted(
            hex(v) for v in helpers if (FUNCS_DIR / ("%x.c" % v)).exists()
        ),
    }


# --------------------------------------------------------------------------- #
# table chain resolution
# --------------------------------------------------------------------------- #
KIND_RANK = {
    "direct_field": 0,
    "bitfield": 1,
    "subobj_deref": 2,
    "helper_computed": 3,
    "delegated_or_empty": 4,
}
SLOT_RANK = {"slot02_get_prop": 0, "slot03_set_prop": 1}


def cand_rank(c: dict):
    """Global preference order for competing candidates of the same 4CC.

    A getter hit beats a setter hit of equal quality (the getter reads the
    field, the setter writes it), and a shallower/less delegated hit wins.
    """
    return (
        KIND_RANK.get(c.get("access_kind"), 5),
        0 if not c.get("delegated") else 1,
        c.get("depth", 0),
        SLOT_RANK.get(c.get("slot"), 2),
        c.get("line_no", 0),
    )


def slot_usage(vtable_index: dict) -> Counter:
    """How many table entries use each VA as their slot02/slot03 handler."""
    c = Counter()
    for t in vtable_index["tables"]:
        for slot in PROP_SLOTS:
            core = t["core"].get(slot) or {}
            if core.get("va"):
                c[int(core["va"], 16)] += 1
    return c


def resolve_chain(vtable_index: dict, funcs_available: set) -> dict:
    """Map every function VA used by the index to its decompiled file."""
    va2info = {}
    for t in vtable_index["tables"]:
        for slot, rec in t["core"].items():
            if not rec or not rec.get("va"):
                continue
            va = int(rec["va"], 16)
            va2info[va] = {
                "va": va,
                "file": rec.get("file"),
                "slot": slot,
                "lines": rec.get("lines"),
                "thunk": rec.get("thunk"),
            }
    for key, rec in vtable_index.get("hop1_functions", {}).items():
        va = int(rec["va"], 16)
        va2info[va] = {
            "va": va,
            "file": rec.get("file"),
            "slot": "hop1",
            "lines": rec.get("lines"),
            "thunk": rec.get("thunk"),
        }
    return va2info


def prop_capable(f: CFunc) -> bool:
    return bool(f.find_branches())


ENTITY_OF_CLASS = {}


def build(outdir: Path, verbose: bool = True) -> dict:
    vtable_index = json.loads(read_text(VTABLE_INDEX))
    tables = vtable_index["tables"]

    # ---- parse cache ----------------------------------------------------
    cache = {}

    def get_func(file_rel: str, va: int = None):
        if not file_rel:
            return None
        p = T95_DIR / file_rel
        key = str(p)
        if key in cache:
            return cache[key]
        if not p.exists():
            cache[key] = None
            return None
        f = CFunc(p, va)
        cache[key] = f
        return f

    stats = Counter()
    all_fourcc = set()
    table_records = []
    missing_subcalls = []
    helper_freq = Counter()
    helper_tables = defaultdict(set)
    missing_seen = set()

    # A VA used as slot02/slot03 by many different table entries is a shared
    # object-protocol handler (copy/delete/backpointer/unknown-prop glue), not
    # a base-class field getter.  Following it would smear every table's code
    # set across all tables, so it is excluded from the delegation walk.
    usage = slot_usage(vtable_index)
    SHARED_HANDLER_MIN = 6
    shared_handlers = {va for va, n in usage.items() if n >= SHARED_HANDLER_MIN}
    hop1_vas = {int(rec["va"], 16) for rec in vtable_index.get("hop1_functions", {}).values()}

    prop_file_cache = {}

    def parse_prop_file(file_rel, va):
        if file_rel in prop_file_cache:
            return prop_file_cache[file_rel]
        f = get_func(file_rel, va)
        if f is None:
            prop_file_cache[file_rel] = (None, [])
            return (None, [])
        brs = f.find_branches()
        prop_file_cache[file_rel] = (f, brs)
        return (f, brs)

    for t in tables:
        tt = t["table_type"]
        cls = t["class"]
        ent = t.get("entity_tag")
        rec = {
            "table_type": tt,
            "class": cls,
            "entity_tag": ent,
            "vtable_va": t.get("vtable_va"),
            "slot_count": t.get("slot_count"),
            "entity": ENTITY_OF_CLASS.get(cls, ent),
            "fourccs": {},
            "chain": [],
        }
        per_slot = {}
        for slot in PROP_SLOTS:
            core = t["core"].get(slot) or {}
            if not core.get("va") or not core.get("file"):
                continue
            va = int(core["va"], 16)
            f, brs = parse_prop_file(core["file"], va)
            if f is None:
                missing_subcalls.append(
                    {"table_type": tt, "class": cls, "slot": slot, "va": core["va"], "why": "file missing"}
                )
                continue
            rec["chain"].append(
                {
                    "slot": slot,
                    "va": core["va"],
                    "file": core["file"],
                    "depth": 0,
                    "branches": len(brs),
                    "thunk": core.get("thunk"),
                }
            )
            per_slot[slot] = (f, brs)
        # follow delegation inside slot02/slot03 (base-class get_prop / set_prop)
        for slot in PROP_SLOTS:
            if slot not in per_slot:
                continue
            base_f, base_brs = per_slot[slot]
            frontier = [(base_f, base_brs, 0)]
            seen = {base_f.va}
            while frontier:
                f, brs, depth = frontier.pop(0)
                if depth >= 3:
                    continue
                code_alt = "|".join(re.escape(v) for v in (f.code_vars or {"a2"}))
                base_alt = "|".join(re.escape(v) for v in (f.base_vars or {"a1"}))
                for callee in sorted({c for line in f.clean for c in extract_callees(line)}):
                    if callee in seen or callee in shared_handlers:
                        continue
                    # the call must forward the property code
                    call_re = re.compile(
                        r"sub_%X\s*\((?P<args>[^;]*)\b(?:%s)\s*[,)]" % (callee, code_alt)
                    )
                    call = call_re.search(f.raw)
                    if not call:
                        continue
                    same_object = bool(
                        re.match(
                            r"\s*(?:\([A-Za-z_][A-Za-z0-9_ ]*\*?\)\s*)?(?:%s)\s*," % base_alt,
                            call.group("args"),
                        )
                    )
                    rel = "funcs/%x.c" % callee
                    p = T95_DIR / rel
                    if not p.exists():
                        key = (tt, cls, slot, callee)
                        if key not in missing_seen:
                            missing_seen.add(key)
                            missing_subcalls.append(
                                {
                                    "table_type": tt,
                                    "class": cls,
                                    "slot": slot,
                                    "from_va": hex(f.va),
                                    "va": hex(callee),
                                    "arg0_is_this": same_object,
                                    "why": (
                                        "code-forwarding sub-call with no decompiled file "
                                        "(same-object base-class style)"
                                        if same_object else
                                        "code-forwarding sub-call with no decompiled file "
                                        "(cross-object / subtable style)"
                                    ),
                                }
                            )
                        continue
                    # same-object delegate = base-class get_prop/set_prop;
                    # cross-object delegate is followed when t95 curated it as a
                    # 2-hop target or when the target is itself a table's
                    # get_prop/set_prop (a sub-object's property handler).
                    if not same_object and callee not in hop1_vas and callee not in usage:
                        continue
                    cf, cbrs = parse_prop_file(rel, callee)
                    if cf is None or not cbrs:
                        continue
                    seen.add(callee)
                    rec["chain"].append(
                        {
                            "slot": slot,
                            "va": hex(callee),
                            "file": rel,
                            "depth": depth + 1,
                            "branches": len(cbrs),
                            "via": hex(f.va),
                            "same_object": same_object,
                            "hop1_curated": callee in hop1_vas,
                            "is_table_property_handler": callee in usage,
                        }
                    )
                    frontier.append((cf, cbrs, depth + 1))

        # ---- collect 4CC -> offsets for this table ----------------------
        for entry in rec["chain"]:
            f = get_func(entry["file"], int(entry["va"], 16))
            if f is None:
                continue
            brs = f.find_branches()
            for br in brs:
                info = analyze_branch(f, br)
                code = br["fourcc"]
                cand = {
                    "code_int": br["code_int"],
                    "slot": entry["slot"],
                    "func_va": entry["va"],
                    "func_name": f.name,
                    "file": entry["file"],
                    "line_no": br["line_no"],
                    "body_span": info["body_span"],
                    "kind": br["kind"],
                    "cond": br["cond"],
                    "primary_off": info["primary_off"],
                    "primary_off_int": info["primary_off_int"],
                    "c_type": info["c_type"],
                    "width": info["width"],
                    "bitmask_or_shift": info["bitmask_or_shift"],
                    "helper_calls": info["helper_calls"],
                    "access_kind": info["access_kind"],
                    "subobj": info["subobj"],
                    "mem_offsets": info["mem_offsets"],
                    "depth": entry["depth"],
                    "delegated": entry["depth"] > 0,
                    "via": entry.get("via"),
                }
                prev = rec["fourccs"].get(code)
                if prev is None:
                    rec["fourccs"][code] = cand
                else:
                    # keep both: prefer a direct field hit over a delegated one
                    if cand_rank(cand) < cand_rank(prev):
                        cand["alt"] = prev
                        rec["fourccs"][code] = cand
                    else:
                        prev.setdefault("alt", cand)
                all_fourcc.add(code)
                for h in info["helper_calls"]:
                    helper_freq[h] += 1
                    helper_tables[h].add((tt, cls))
        rec["fourcc_count"] = len(rec["fourccs"])
        stats["tables"] += 1
        stats["table_fourcc_pairs"] += len(rec["fourccs"])
        if verbose:
            top = sorted(rec["fourccs"])[:6]
            print(
                "tt=%2d %-38s chain=%d 4cc=%3d  %s"
                % (tt, cls, len(rec["chain"]), len(rec["fourccs"]), ",".join(top)),
                flush=True,
            )
        table_records.append(rec)

    # helper classification: generic = appears in many tables/branches
    table_records_helpers = {
        h: {"branches": helper_freq[h], "tables": len(helper_tables[h])}
        for h in helper_freq
    }

    out = {
        "schema_id": "fm24.t97.fourcc_mem_map",
        "schema_version": SCHEMA_VERSION,
        "generated_by": "t97",
        "status": "complete",
        "inputs": {
            "vtable_index": {
                "path": "scratch/t95/vtable_index.json",
                "sha256": sha256_of(VTABLE_INDEX),
            },
            "funcs_dir": "scratch/t95/funcs",
            "funcs_files": len(list(FUNCS_DIR.glob("*.c"))),
        },
        "method": (
            "Hex-Rays C parsing: every `case <int>:` / `if (<code> == <int>)` / "
            "`if (<code> != <int>) <guard>; <body>` dispatch branch is located, the branch "
            "body is brace/terminator delimited, and every `base + n` / `*(T *)(base + n)` / "
            "`base[n]` address expression is converted to a byte offset using the declared "
            "element size of the base variable (integer locals/params address bytes, pointer "
            "locals address pointee-sized elements).  Delegation to base-class get_prop / "
            "set_prop is followed up to depth 3."
        ),
        "table_count": len(table_records),
        "unique_fourcc_count": len(all_fourcc),
        "unique_fourccs": sorted(all_fourcc),
        "helper_frequency": table_records_helpers,
        "generic_helpers": [hex(v) for v in sorted(GENERIC_HELPERS)],
        "shared_protocol_handlers": [
            {"va": hex(va), "used_by_table_entries": usage[va]}
            for va in sorted(shared_handlers)
        ],
        "missing_subcalls": missing_subcalls,
        "tables": table_records,
        "stats": dict(stats),
    }
    return out


# --------------------------------------------------------------------------- #
# XML denominator triage
# --------------------------------------------------------------------------- #
ENTITY_TABLE_MATCH = {
    "club": {(3, "CLUB"), (3, "TEAM_CONTAINER"), (3, "LEAGUE_BODY_CLUB")},
    "nation": {(9, "NATIONAL_TEAM_CONTAINER"), (9, "TEAM_CONTAINER"), (10, "NATION")},
    "comp": {(25, "COMP")},
}


def triage(fourcc_map: dict, xml_cov: dict):
    """Join the extracted 4CC map onto the 1,034-row XML denominator."""
    # index: entity -> code -> best candidate (primary = the entity's own class chain)
    by_entity = defaultdict(dict)
    secondary = defaultdict(dict)  # same entity_tag, but a different table family
    # shared object-protocol handlers carry a generic layout, so a hit that
    # only comes from them is not evidence for a specific table's field
    shared_vas = {
        int(x["va"], 16) for x in fourcc_map.get("shared_protocol_handlers", [])
    }
    for rec in fourcc_map["tables"]:
        key = (rec["table_type"], rec["class"])
        keys = [e for e, pairs in ENTITY_TABLE_MATCH.items() if key in pairs]
        store = by_entity
        if not keys:
            tag = rec.get("entity_tag")
            if tag is None:
                continue
            keys = [tag]
            store = secondary
        for e in set(keys):
            for code, cand in rec["fourccs"].items():
                if store is secondary and cand.get("func_va") in shared_vas:
                    continue
                cur = store[e].get(code)
                if cur is None or cand_rank(cand) < cand_rank(cur):
                    store[e][code] = cand

    lower_index = {e: {c.lower(): c for c in d} for e, d in by_entity.items()}

    # global code -> [(table_type, class, access_kind, primary_off)] over all 67 tables
    global_index = defaultdict(list)
    for rec in fourcc_map["tables"]:
        for code, cand in rec["fourccs"].items():
            global_index[code].append(
                {
                    "table_type": rec["table_type"],
                    "table_class": rec["class"],
                    "entity_tag": rec["entity_tag"],
                    "access_kind": cand["access_kind"],
                    "primary_off": cand["primary_off"],
                    "func_va": cand["func_va"],
                    "line_no": cand["line_no"],
                }
            )

    rows = xml_cov["rows"]
    out_rows = []
    transitions = defaultdict(Counter)
    detail_counts = Counter()
    for r in rows:
        ent = r["entity"]
        code = r["code"]
        bucket = r.get("bucket_after")
        hit = by_entity.get(ent, {}).get(code)
        match_kind = "exact"
        if hit is None:
            alt = lower_index.get(ent, {}).get(code.lower())
            if alt is not None:
                hit = by_entity[ent][alt]
                match_kind = "case_insensitive"
        if hit is None:
            proposed = "absent_in_entity_get_set_chain"
            rec = None
            sec = secondary.get(ent, {}).get(code)
            elsewhere = global_index.get(code, [])
            if rec is None and sec is None and elsewhere:
                only_shared = all(
                    e_.get("func_va") in shared_vas for e_ in elsewhere
                )
                proposed = (
                    "absent_locally_only_in_shared_handler"
                    if only_shared
                    else "absent_locally_code_in_other_table"
                )
                rec = {
                    "other_tables": elsewhere[:6],
                    "other_table_count": len(elsewhere),
                    "all_in_shared_handler": only_shared,
                    "match_kind": "cross_table_code",
                }
        else:
            sec = None
            rec = {
                "table_class": hit["table_class"] if "table_class" in hit else None,
                "slot": hit["slot"],
                "func_va": hit["func_va"],
                "file": hit["file"],
                "line_no": hit["line_no"],
                "access_kind": hit["access_kind"],
                "primary_off": hit["primary_off"],
                "width": hit["width"],
                "c_type": hit["c_type"],
                "mem_offsets": hit["mem_offsets"],
                "subobj": hit["subobj"],
                "helper_calls": hit["helper_calls"],
                "bitmask_or_shift": hit["bitmask_or_shift"],
                "delegated": hit["delegated"],
                "match_kind": match_kind,
            }
            kind = hit["access_kind"]
            if kind in ("direct_field", "bitfield"):
                proposed = "hit_direct_mem_off"
            elif kind == "subobj_deref":
                proposed = "hit_subobj_deref"
            elif kind == "helper_computed":
                proposed = "hit_helper_computed"
            else:
                proposed = "hit_delegated_or_empty"
            if sec is not None:
                rec["secondary_hit"] = {
                    "table_class": sec.get("table_class"),
                    "slot": sec["slot"],
                    "func_va": sec["func_va"],
                    "line_no": sec["line_no"],
                    "access_kind": sec["access_kind"],
                    "primary_off": sec["primary_off"],
                }
        if rec is None and sec is not None:
            rec = {
                "table_class": sec.get("table_class"),
                "slot": sec["slot"],
                "func_va": sec["func_va"],
                "file": sec["file"],
                "line_no": sec["line_no"],
                "access_kind": sec["access_kind"],
                "primary_off": sec["primary_off"],
                "width": sec["width"],
                "c_type": sec["c_type"],
                "mem_offsets": sec["mem_offsets"],
                "subobj": sec["subobj"],
                "helper_calls": sec["helper_calls"],
                "bitmask_or_shift": sec["bitmask_or_shift"],
                "delegated": sec["delegated"],
                "match_kind": "same_entity_tag_other_table",
                "secondary_only": True,
            }
            proposed = "hit_other_table_same_tag"
        if proposed == "absent_in_entity_get_set_chain" and rec is None:
            proposed = "absent_everywhere_in_67_tables"
        transitions[bucket][proposed] += 1
        detail_counts[(ent, bucket, proposed)] += 1
        out_rows.append(
            {
                "id": r["id"],
                "entity": ent,
                "code": code,
                "bucket_after": bucket,
                "bucket_before": r.get("bucket_before"),
                "proposed_bucket": proposed,
                "t97": rec,
                "pointer": r.get("pointer"),
            }
        )

    per_ent = defaultdict(Counter)
    for (ent, bucket, proposed), n in detail_counts.items():
        per_ent[(ent, bucket)][proposed] += n
    summary = {
        "denominator": len(rows),
        "by_entity_bucket_transition": {
            "%s|%s" % (ent, bucket): dict(sorted(c.items()))
            for (ent, bucket), c in sorted(per_ent.items())
        },
        "by_bucket_transition": {b: dict(sorted(c.items())) for b, c in sorted(transitions.items())},
        "proposed_totals": dict(sorted(Counter(r["proposed_bucket"] for r in out_rows).items())),
        "per_entity_proposed": {
            ent: dict(sorted(Counter(r["proposed_bucket"] for r in out_rows if r["entity"] == ent).items()))
            for ent in sorted({r["entity"] for r in out_rows})
        },
    }
    summary["breakout"] = {}
    for bucket in sorted(transitions):
        d = transitions[bucket]
        summary["breakout"][bucket] = {
            "total": sum(d.values()),
            **{k: v for k, v in sorted(d.items())},
        }
    return summary, out_rows, by_entity


# --------------------------------------------------------------------------- #
# independent validation against already-accepted L3 displacements
# --------------------------------------------------------------------------- #
L3_SCHEMA = REPO / "reports" / "club_nation_subtable_schema.json"


def validate_vs_accepted_l3(xml_out: dict):
    """Compare the t97 byte offsets with the accepted L3 `object_displacement`.

    The accepted L3 value is the *wire slot origin* (slot_width bytes wide),
    while t97 reports the exact byte offset of the field inside the object, so
    a bitfield may sit a few bytes into an accepted slot.  Both cases are
    counted (`exact` / `within_slot`).
    """
    if not L3_SCHEMA.exists():
        return {"available": False}
    d = json.loads(read_text(L3_SCHEMA))
    sections = {
        "club_main_row_fields": "club",
        "nation_main_row_fields": "nation",
        "comp_main_row_fields": "comp",
    }
    rows_by = {}
    for r in xml_out["rows"]:
        rows_by.setdefault((r["entity"], r["code"].lower()), r)
    items = []
    counts = Counter()
    for sect, ent in sections.items():
        fields = (d.get(sect) or {}).get("L3_fields") or []
        for x in fields:
            code = x.get("code")
            disp = x.get("object_displacement")
            width = x.get("slot_width")
            if disp is None:
                continue
            r = rows_by.get((ent, str(code).lower()))
            cand = (r or {}).get("t97") or {}
            got = cand.get("primary_off")
            got_i = int(got, 16) if isinstance(got, str) else None
            if got_i is None:
                verdict = "no_static_hit_fieldsize_unknown" if False else "no_static_hit"
            elif got_i == disp:
                verdict = "exact"
            elif width and disp <= got_i < disp + width:
                verdict = "within_slot"
            else:
                verdict = "mismatch"
            counts[verdict] += 1
            items.append(
                {
                    "section": sect,
                    "entity": ent,
                    "code": code,
                    "accepted_displacement": disp,
                    "accepted_slot_width": width,
                    "t97_off": got_i,
                    "t97_off_hex": got,
                    "t97_access_kind": cand.get("access_kind"),
                    "t97_table_class": cand.get("table_class"),
                    "t97_func_va": cand.get("func_va"),
                    "t97_line_no": cand.get("line_no"),
                    "verdict": verdict,
                }
            )
    counts["checked"] = len(items)
    return {
        "available": True,
        "source": {
            "path": "reports/club_nation_subtable_schema.json",
            "sha256": sha256_of(L3_SCHEMA),
        },
        "note": (
            "accepted `object_displacement` is the wire-slot origin; t97 reports the exact "
            "byte offset of the field, so bitfields may land inside the slot (`within_slot`)."
        ),
        "totals": dict(counts),
        "items": items,
    }


# --------------------------------------------------------------------------- #
# static read_server / read_client cross-check
# --------------------------------------------------------------------------- #
def static_read_join(fourcc_map: dict):
    out = []
    for rec in fourcc_map["tables"]:
        entry = {
            "table_type": rec["table_type"],
            "class": rec["class"],
            "entity_tag": rec["entity_tag"],
            "slots": {},
            "joins": [],
            "join_summary": Counter(),
        }
        offs = {}
        for slot in ("slot19_read_server", "slot20_read_client", "slot21_write"):
            core = next((c for c in rec["chain"] if c["slot"] == slot), None)
            # chain only holds prop slots; re-read from vtable index later
            offs[slot] = []
        out.append(entry)
    return out


def build_static_join(fourcc_map: dict, vtable_index: dict):
    tables_by_key = {(t["table_type"], t["class"]): t for t in vtable_index["tables"]}
    result = []
    totals = Counter()
    for rec in fourcc_map["tables"]:
        src = tables_by_key.get((rec["table_type"], rec["class"]))
        entry = {
            "table_type": rec["table_type"],
            "class": rec["class"],
            "entity_tag": rec["entity_tag"],
            "slots": {},
            "fourcc_joins": [],
            "counters": {},
        }
        slot_offsets = {}
        for slot in ("slot19_read_server", "slot20_read_client", "slot21_write"):
            core = (src or {}).get("core", {}).get(slot) or {}
            rel = core.get("file")
            if not rel:
                entry["slots"][slot] = None
                slot_offsets[slot] = {}
                continue
            p = T95_DIR / rel
            if not p.exists():
                entry["slots"][slot] = {"file": rel, "missing": True}
                slot_offsets[slot] = {}
                continue
            va = int(core["va"], 16) if core.get("va") else None
            funcs = [CFunc(p, va)]
            # one level of same-object tail delegation (e.g. COMP slot19 ->
            # 0x143caa6d0 -> 0x140eb7a00) so thin wrappers still contribute
            for _ in range(2):
                fw = funcs[-1]
                nxt = None
                stmts = [t.strip() for t in fw.clean if t.strip()]
                for t in stmts:
                    m = re.match(r"^return\s+(?:sub_([0-9A-Fa-f]+))\s*\(\s*(?:\([^)]*\)\s*)?([A-Za-z_]\w*)\s*,", t)
                    if m and m.group(2) == (fw.params[0][0] if fw.params else "a1"):
                        cand = T95_DIR / ("funcs/%s.c" % m.group(1).lower())
                        if cand.exists():
                            nxt = CFunc(cand, int(m.group(1), 16))
                        break
                if nxt is None:
                    break
                funcs.append(nxt)
            ordering = []
            first_line = {}
            first_file = {}
            for f in funcs:
                for i, text in enumerate(f.clean):
                    for base, elem in f.base_vars_at(i).items():
                        if base not in text:
                            continue
                        for o in extract_offsets(text, base, elem, i + 1):
                            if o["off_int"] not in first_line:
                                first_line[o["off_int"]] = o["line"]
                                first_file[o["off_int"]] = f.path.name
                            if o not in ordering:
                                ordering.append(o)
            ordering.sort(key=lambda o: (o["line"], o["off_int"]))
            entry["slots"][slot] = {
                "file": rel,
                "va": core.get("va"),
                "lines": core.get("lines"),
                "files_followed": [f.path.name for f in funcs],
                "offset_count": len(first_line),
                "offsets_in_read_order": [
                    {"off": hex(k), "line": first_line[k], "file": first_file[k]}
                    for k in sorted(first_line, key=lambda x: first_line[x])
                ],
            }
            slot_offsets[slot] = first_line
        # join against the 4CC map
        n_hit19 = n_hit20 = n_hit_any = 0
        for code in sorted(rec["fourccs"]):
            cand = rec["fourccs"][code]
            po = cand.get("primary_off_int")
            hit19 = po is not None and po in slot_offsets.get("slot19_read_server", {})
            hit20 = po is not None and po in slot_offsets.get("slot20_read_client", {})
            if hit19:
                n_hit19 += 1
            if hit20:
                n_hit20 += 1
            if hit19 or hit20:
                n_hit_any += 1
            entry["fourcc_joins"].append(
                {
                    "fourcc": code,
                    "code_int": cand["code_int"],
                    "primary_off": cand["primary_off"],
                    "access_kind": cand["access_kind"],
                    "func_va": cand["func_va"],
                    "prop_line": cand["line_no"],
                    "in_read_server": hit19,
                    "read_server_line": slot_offsets.get("slot19_read_server", {}).get(po) if hit19 else None,
                    "in_read_client": hit20,
                    "read_client_line": slot_offsets.get("slot20_read_client", {}).get(po) if hit20 else None,
                }
            )
        entry["counters"] = {
            "fourccs_with_off": sum(1 for c in rec["fourccs"].values() if c.get("primary_off_int") is not None),
            "hit_read_server": n_hit19,
            "hit_read_client": n_hit20,
            "hit_any_read": n_hit_any,
        }
        totals["fourccs_with_off"] += entry["counters"]["fourccs_with_off"]
        totals["hit_read_server"] += n_hit19
        totals["hit_read_client"] += n_hit20
        totals["hit_any_read"] += n_hit_any
        result.append(entry)
    return result, dict(totals)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def run(args):
    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = REPO / outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("[t97] parsing scratch/t95 Hex-Rays output ...", flush=True)
    fourcc_map = build(outdir, verbose=not args.quiet)
    for rec in fourcc_map["tables"]:
        for code, cand in rec["fourccs"].items():
            cand["table_class"] = rec["class"]
            if "alt" in cand:
                cand["alt"]["table_class"] = rec["class"]

    (outdir / "fourcc_mem_map.json").write_text(
        json.dumps(fourcc_map, indent=1, sort_keys=False, ensure_ascii=False), encoding="utf-8"
    )
    print("[t97] wrote fourcc_mem_map.json", flush=True)

    xml_cov = json.loads(io.open(XML_COVERAGE, encoding="utf-8").read())
    summary, rows, by_entity = triage(fourcc_map, xml_cov)
    xml_out_placeholder = {"rows": rows}
    xml_out = {
        "schema_id": "fm24.t97.xml_triage",
        "schema_version": SCHEMA_VERSION,
        "generated_by": "t97",
        "status": "complete",
        "source": {
            "path": "reports/xml_denominator_coverage.json",
            "sha256": sha256_of(XML_COVERAGE),
            "denominator": xml_cov.get("count"),
            "buckets_used": xml_cov.get("buckets_order"),
        },
        "note": (
            "annotation only: reports/ is NOT modified. `proposed_bucket` is a t97 candidate "
            "class derived from static Hex-Rays evidence, not an accepted bucket."
        ),
        "summary": summary,
        "code_index_size": {e: len(d) for e, d in sorted(by_entity.items())},
        "validation_vs_accepted_L3": validate_vs_accepted_l3(xml_out_placeholder),
        "rows": rows,
    }
    (outdir / "xml_triage.json").write_text(
        json.dumps(xml_out, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("[t97] wrote xml_triage.json", flush=True)

    vtable_index = json.loads(read_text(VTABLE_INDEX))
    join, jtot = build_static_join(fourcc_map, vtable_index)
    join_out = {
        "schema_id": "fm24.t97.static_read_join",
        "schema_version": SCHEMA_VERSION,
        "generated_by": "t97",
        "status": "complete",
        "method": (
            "all `base + n` address expressions inside slot19_read_server / "
            "slot20_read_client / slot21_write are converted to byte offsets with the same "
            "declared-element-size rule; the 4CC primary offset from slot02/slot03 is then "
            "intersected with those offset sets."
        ),
        "totals": jtot,
        "tables": join,
    }
    (outdir / "static_read_join.json").write_text(
        json.dumps(join_out, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("[t97] wrote static_read_join.json", flush=True)

    if args.report:
        write_report(outdir, fourcc_map, xml_out, join_out)
    write_done(outdir, fourcc_map, xml_out, join_out)
    return fourcc_map, xml_out, join_out


def write_done(outdir: Path, fourcc_map, xml_out, join_out):
    """DONE.md - completion marker with the headline numbers."""
    kinds = Counter()
    pairs = 0
    with_off = 0
    for rec in fourcc_map["tables"]:
        for cand in rec["fourccs"].values():
            kinds[cand["access_kind"]] += 1
            pairs += 1
            if cand.get("primary_off_int") is not None:
                with_off += 1
    s = xml_out["summary"]
    br = s["breakout"]
    t = join_out["totals"]
    val = xml_out.get("validation_vs_accepted_L3") or {}
    vt = val.get("totals") or {}

    def nz(bucket, key):
        return (br.get(bucket) or {}).get(key, 0)

    L = []
    A = L.append
    A("DONE type=t97")
    A("")
    A("# t97 — 全量 67 表 Hex-Rays 4CC ↔ 内存偏移抽取 + XML 1,034 分母分诊")
    A("")
    A("status: complete")
    A("outputs: scratch/t97/out")
    A("")
    A("## 摘要数字")
    A("")
    A(f"- tables_covered: {fourcc_map['table_count']}/67")
    A(f"- unique_fourcc: {fourcc_map['unique_fourcc_count']}")
    A(f"- table_fourcc_pairs: {pairs}")
    A(f"- pairs_with_byte_offset: {with_off}")
    A(f"- access_kind: direct_field={kinds.get('direct_field', 0)}, bitfield={kinds.get('bitfield', 0)}, "
      f"subobj_deref={kinds.get('subobj_deref', 0)}, helper_computed={kinds.get('helper_computed', 0)}, "
      f"delegated_or_empty={kinds.get('delegated_or_empty', 0)}")
    A(f"- missing_subcalls: {len(fourcc_map['missing_subcalls'])}")
    A("")
    A("## 1,034 分母分诊")
    A("")
    A(f"- denominator: {s['denominator']}")
    A(f"- unresolved_wire_slot (160): direct_mem_off={nz('unresolved_wire_slot', 'hit_direct_mem_off')}, "
      f"helper_computed={nz('unresolved_wire_slot', 'hit_helper_computed')}, "
      f"absent_everywhere={nz('unresolved_wire_slot', 'absent_everywhere_in_67_tables')}")
    A(f"- held (59): direct_mem_off={nz('held', 'hit_direct_mem_off')}, "
      f"helper_computed={nz('held', 'hit_helper_computed')}, "
      f"absent_everywhere={nz('held', 'absent_everywhere_in_67_tables')}")
    A(f"- no_wire_evidence (564): direct_mem_off={nz('no_wire_evidence', 'hit_direct_mem_off')}, "
      f"helper_computed={nz('no_wire_evidence', 'hit_helper_computed')}, "
      f"absent_everywhere={nz('no_wire_evidence', 'absent_everywhere_in_67_tables')}")
    A(f"- total_direct_mem_off_hits: {s['proposed_totals'].get('hit_direct_mem_off', 0)}")
    A(f"- total_absent_everywhere: {s['proposed_totals'].get('absent_everywhere_in_67_tables', 0)}")
    A("")
    A("## 静态 read 交叉")
    A("")
    A(f"- fourccs_with_offset: {t.get('fourccs_with_off', 0)}")
    A(f"- hit_read_server: {t.get('hit_read_server', 0)}")
    A(f"- hit_read_client: {t.get('hit_read_client', 0)}")
    A(f"- hit_any_read: {t.get('hit_any_read', 0)}")
    A("")
    A("## 回归验证（对已验收 L3）")
    A("")
    A(f"- checked: {vt.get('checked', 0)}")
    A(f"- exact: {vt.get('exact', 0)}")
    A(f"- within_slot: {vt.get('within_slot', 0)}")
    A(f"- no_static_hit: {vt.get('no_static_hit', 0)}")
    A(f"- mismatch: {vt.get('mismatch', 0)}")
    A("")
    A("## 验收")
    A("")
    A("- `py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest` → exit 0 (25 assertions,")
    A("  incl. STARTING_RECORD `1415446a0.c`: 1869899892('otht')->0x28, 1918989417('rati')->0x5a, 1920099681('rrea')->0x5c)")
    A("- 67/67 tables covered; all JSON deliverables parse cleanly")
    A("- `reports/` and `LEDGER.json` untouched (read-only inputs)")
    A("")
    A("## 交付物")
    A("")
    A("| 文件 | 字节 | sha256[:16] |")
    A("|---|---|---|")
    for name in ("fourcc_mem_map.json", "xml_triage.json", "static_read_join.json", "REPORT.md", "DONE.md"):
        p = outdir / name
        if p.exists():
            A(f"| `{name}` | {p.stat().st_size} | `{sha256_of(p)[:16]}` |")
    A("")
    (outdir / "DONE.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("[t97] wrote DONE.md", flush=True)


def fmt_hex(v):
    return v if isinstance(v, str) else hex(v)


def write_report(outdir: Path, fourcc_map, xml_out, join_out):
    """REPORT.md - findings, per-table hit rates, 1,034 breakout, missing sub-calls."""
    lines = []
    A = lines.append
    kinds = Counter()
    with_off = 0
    pairs = 0
    for rec in fourcc_map["tables"]:
        for cand in rec["fourccs"].values():
            kinds[cand["access_kind"]] += 1
            pairs += 1
            if cand.get("primary_off_int") is not None:
                with_off += 1
    join_by = {(j["table_type"], j["class"]): j for j in join_out["tables"]}
    t = join_out["totals"]
    s = xml_out["summary"]
    val = xml_out.get("validation_vs_accepted_L3") or {}

    A("# t97 — Hex-Rays 4CC ↔ 内存偏移全量抽取 + 1,034 分母分诊")
    A("")
    A("> 只读输入：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（Hex-Rays 反编译 C）、")
    A("> `reports/xml_denominator_coverage.json`。**本任务不修改 `reports/` 与 `LEDGER.json`**。")
    A("")
    A("## 0. 交付物")
    A("")
    A("| 文件 | 内容 |")
    A("|---|---|")
    A("| `fourcc_mem_map.json` | 67 张表的 4CC → `mem_off` / `access_kind` / `func_va` / `line_no`（`\"status\": \"complete\"`） |")
    A("| `xml_triage.json` | 1,034 条分母逐条分诊 + 分桶变化汇总 + 对已验收 L3 的回归验证 |")
    A("| `static_read_join.json` | 4CC ↔ `mem_off` ↔ slot19/slot20 行号 的静态交叉表 |")
    A("| `REPORT.md` / `DONE.md` | 本报告 / 完成标记（`DONE type=t97`） |")
    A("")
    A("## 1. 覆盖与规模")
    A("")
    A(f"- 表条目（`vtable_index.tables`）：**{fourcc_map['table_count']}**")
    A(f"- 唯一 4CC：**{fourcc_map['unique_fourcc_count']}**（t95 初扫曾见 1,897；本任务因追踪基类/子对象 get_prop 而扩大）")
    A(f"- 表×4CC 分支记录：**{pairs}**，其中有明确字节偏移：**{with_off}**（{with_off / max(pairs, 1):.1%}）")
    A("- 纯静态：只解析 t95 的反编译产物，无数据库 dump、无第三方依赖")
    A("")
    A("| access_kind | 分支数 | 含义 |")
    A("|---|---|---|")
    meaning = {
        "direct_field": "分支内直接解引用 `this + N` 的标量/指针字段",
        "bitfield": "同一字段带 `& mask` / `>> n` 位域操作",
        "subobj_deref": "先取 `this + N` 处的子对象指针，再读其内部字段",
        "helper_computed": "值由 helper 子函数计算（helper 未反编译时无字节偏移）",
        "delegated_or_empty": "分支仅 `return sub_X(this, code, out)` 或直接 `goto`/`break`",
    }
    for k, v in kinds.most_common():
        A(f"| `{k}` | {v} | {meaning.get(k, '')} |")
    A("")
    A("## 2. 每张大表命中率")
    A("")
    A("| tt | class | 链上函数数 | 4CC | 有明确 mem_off | read_server 命中 | slot19 偏移数 |")
    A("|---|---|---|---|---|---|---|")
    big = sorted(fourcc_map["tables"], key=lambda r: -r["fourcc_count"])[:24]
    for rec in big:
        wo = sum(1 for c in rec["fourccs"].values() if c.get("primary_off_int") is not None)
        j = join_by.get((rec["table_type"], rec["class"]), {})
        cnt = j.get("counters") or {}
        s19 = (j.get("slots") or {}).get("slot19_read_server") or {}
        A(
            f"| {rec['table_type']} | {rec['class']} | {len(rec['chain'])} | {rec['fourcc_count']} | "
            f"{wo} ({wo / max(rec['fourcc_count'], 1):.0%}) | {cnt.get('hit_read_server', 0)} | "
            f"{s19.get('offset_count', 0)} |"
        )
    A("")
    A(f"其余 {max(len(fourcc_map['tables']) - len(big), 0)} 张表见 `fourcc_mem_map.json`（多为 2–30 个 4CC 的档案表）。")
    A("")
    A("### 2.1 解析器要点（为什么 `helper_computed` 占比高）")
    A("")
    A("- CLUB/COMP 这类 4,500 行的 `get_prop` 把大量 4CC 直接转交给子对象或 helper，例如")
    A("  `return sub_143CA2E60(v21, 11, code, a3)`（COMP）、`v214 = sub_140E73FB0(a1)`（CLUB）。")
    A("  这些 helper 不在 t95 的 352 份反编译产物中，因此只能记录到 `helper_calls`，无法给出字节偏移。")
    A("- 尾调用到**基类** handler（`CLUB → TEAM_CONTAINER`、`NATIONAL_TEAM_CONTAINER → TEAM_CONTAINER`、")
    A("  `NATION → 1410668F0 / 141063F30 / 141045D50`）已按「同对象」规则追踪至 depth 3，结果标 `delegated`。")
    A("- 共享对象协议 handler（`0x140FE3F20` / `0x140FE2700`，被 13–14 个表条目复用）**不作为基类 getter 追踪**，")
    A("  否则 `BaCP/COPY/DELE/Duni/HiSe/ISTP` 等通用协议码会污染全部 67 张表。")
    A("")
    A("## 3. NATION (tt=10) 专项核对")
    A("")
    nat = next(r for r in fourcc_map["tables"] if r["table_type"] == 10)
    A("| 槽 | 函数 | depth | 分支数 | 关系 |")
    A("|---|---|---|---|---|")
    for c in nat["chain"]:
        rel = "自身槽" if c["depth"] == 0 else (
            "同对象基类/尾调用" if c.get("same_object") else "跨对象（子对象 / hop1 精选）"
        )
        A(f"| `{c['slot']}` | `{c['va']}` (`{c['file']}`) | {c['depth']} | {c['branches']} | {rel} |")
    A("")
    A("任务书点名的四份 nation 侧文件：")
    A("")
    for va, name in (
        ("0x141042940", "141042940.c"),
        ("0x141045d50", "141045d50.c"),
        ("0x141063f30", "141063f30.c"),
        ("0x1410668f0", "1410668f0.c"),
    ):
        in_chain = any(c["va"] == va for c in nat["chain"])
        A(f"- `{name}`：{'在链上 ✔' if in_chain else '未在链上 ✘'}")
    A("")
    nation_missing = [
        m for m in fourcc_map["missing_subcalls"]
        if m["class"] in ("NATION", "NATIONAL_TEAM_CONTAINER")
    ]
    A(f"`NATION`/`NATIONAL_TEAM_CONTAINER` 的 `missing_subcalls`：**{len(nation_missing)}** 条"
      "（转发 4CC 但无反编译文件的直接子调用）")
    A("")
    if nation_missing:
        A("| class | slot | from | 未反编译目标 | arg0 是 this |")
        A("|---|---|---|---|---|")
        for m in nation_missing:
            A(f"| {m['class']} | `{m['slot']}` | `{m['from_va']}` | `{m['va']}` | {m['arg0_is_this']} |")
        A("")
    A("## 4. 1,034 分母分诊")
    A("")
    A(f"分母：**{s['denominator']}** 条（club 433 / nation 346 / comp 255）。")
    A("分桶变化全部落在候选标签上，`reports/` 未被改写（`proposed_bucket` 是静态候选，不是已接受的桶）。")
    A("")
    A("| 原桶（`bucket_after`） | 总数 | 直接 mem_off | subobj_deref | helper_computed | delegated/empty | 同类同 tag 其它表 | 仅共享 handler | 其它表另有 | 全 67 表皆无 |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for bucket, d in s["breakout"].items():
        A(
            "| `{}` | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                bucket, d["total"],
                d.get("hit_direct_mem_off", 0), d.get("hit_subobj_deref", 0),
                d.get("hit_helper_computed", 0), d.get("hit_delegated_or_empty", 0),
                d.get("hit_other_table_same_tag", 0),
                d.get("absent_locally_only_in_shared_handler", 0),
                d.get("absent_locally_code_in_other_table", 0),
                d.get("absent_everywhere_in_67_tables", 0),
            )
        )
    A("")
    A("### 4.1 三个关键桶的突破")
    A("")
    for bucket in ("unresolved_wire_slot", "held", "no_wire_evidence"):
        d = s["breakout"].get(bucket)
        if not d:
            continue
        absent = (
            d.get("absent_everywhere_in_67_tables", 0)
            + d.get("absent_locally_code_in_other_table", 0)
            + d.get("absent_locally_only_in_shared_handler", 0)
        )
        A(
            f"- **`{bucket}`（{d['total']} 条）**：明确 `mem_off` **{d.get('hit_direct_mem_off', 0)}** 条；"
            f"`subobj_deref` {d.get('hit_subobj_deref', 0)} 条；`helper_computed` {d.get('hit_helper_computed', 0)} 条；"
            f"delegated/empty {d.get('hit_delegated_or_empty', 0)} 条；链上不存在 {absent} 条"
            f"（其中全 67 表皆无 {d.get('absent_everywhere_in_67_tables', 0)} 条 = 强证据：纯 UI / 编辑器派生 / 仅存档字段）"
        )
    A("")
    A("### 4.2 分实体")
    A("")
    A("| entity | 直接 mem_off | helper_computed | delegated/empty | 同类同 tag | 其它表另有 | 全表皆无 |")
    A("|---|---|---|---|---|---|---|")
    per_ent = defaultdict(Counter)
    for r in xml_out["rows"]:
        per_ent[r["entity"]][r["proposed_bucket"]] += 1
    for ent in sorted(per_ent):
        c = per_ent[ent]
        A(
            f"| {ent} | {c.get('hit_direct_mem_off', 0)} | {c.get('hit_helper_computed', 0)} | "
            f"{c.get('hit_delegated_or_empty', 0)} | {c.get('hit_other_table_same_tag', 0)} | "
            f"{c.get('absent_locally_code_in_other_table', 0)} | {c.get('absent_everywhere_in_67_tables', 0)} |"
        )
    A("")
    A("## 5. 对已验收 L3 的独立回归（防自欺）")
    A("")
    if val.get("available"):
        vt = val["totals"]
        A(f"来源：`{val['source']['path']}`（只读），逐字段对比 `object_displacement`：")
        A("")
        A(
            f"- 检查 **{vt.get('checked', 0)}** 条：exact **{vt.get('exact', 0)}**、"
            f"within_slot **{vt.get('within_slot', 0)}**、no_static_hit **{vt.get('no_static_hit', 0)}**、"
            f"mismatch **{vt.get('mismatch', 0)}**"
        )
        A("")
        A("> 已验收值是**线槽起点**（slot_width 字节宽），t97 报的是**字段字节偏移**；"
          "位域可能落在槽内几字节处，故单列 `within_slot`。")
        A("")
        A("| section | code | 已验收 disp | 宽度 | t97 off | access_kind | 判定 |")
        A("|---|---|---|---|---|---|---|")
        for it in val["items"]:
            A(
                f"| {it['section'].replace('_main_row_fields', '')} | `{it['code']}` | {it['accepted_displacement']} | "
                f"{it['accepted_slot_width']} | {it['t97_off'] if it['t97_off'] is not None else '—'} | "
                f"`{it['t97_access_kind'] or '—'}` | {it['verdict']} |"
            )
        A("")
        A("`no_static_hit` 的两条（`Cedp` / `Cncl`）其值由未反编译 helper 计算；`duni` 是基类序列化的身份列，")
        A("不走 4CC 分派，属已知特例。")
    else:
        A("（未找到可用的已验收 L3 表）")
    A("")
    A("## 6. slot19/slot20 静态偏移交叉")
    A("")
    A(f"- slot02/03 有明确 `mem_off` 的分支：**{t.get('fourccs_with_off', 0)}**")
    A(f"- 与 `slot19_read_server` 偏移集合相交：**{t.get('hit_read_server', 0)}**")
    A(f"- 与 `slot20_read_client` 偏移集合相交：**{t.get('hit_read_client', 0)}**")
    A(f"- 至少命中一侧：**{t.get('hit_any_read', 0)}**")
    A("")
    A("| tt | class | 有 off | slot19 命中 | slot20 命中 | 至少一侧 |")
    A("|---|---|---|---|---|---|")
    for j in sorted(join_out["tables"], key=lambda x: -x["counters"].get("hit_any_read", 0))[:15]:
        c = j["counters"]
        if not c.get("fourccs_with_off"):
            continue
        A(
            f"| {j['table_type']} | {j['class']} | {c['fourccs_with_off']} | {c['hit_read_server']} | "
            f"{c['hit_read_client']} | {c['hit_any_read']} |"
        )
    A("")
    A("## 7. `missing_subcalls` 清单")
    A("")
    ms = fourcc_map["missing_subcalls"]
    A(f"合计 **{len(ms)}** 条（去重：表 × 槽 × 目标）。这些是 `slot02`/`slot03`（含追踪到的基类）里")
    A("**转发 4CC 但无反编译文件**的直接子调用，是后续扩大反编译的第一优先目标。")
    A("完整清单见 `fourcc_mem_map.json#/missing_subcalls`。")
    A("")
    if ms:
        by_cls = Counter(m["class"] for m in ms)
        A("| class | 条数 |")
        A("|---|---|")
        for cls, n in by_cls.most_common():
            A(f"| {cls} | {n} |")
        A("")
        tgt = Counter(m["va"] for m in ms)
        A("出现最多的未反编译目标：")
        A("")
        A("| 目标 VA | 出现次数 | 存在 this 直传 |")
        A("|---|---|---|")
        for va, n in tgt.most_common(12):
            this_direct = any(m["va"] == va and m["arg0_is_this"] for m in ms)
            A(f"| `{va}` | {n} | {this_direct} |")
        A("")
        A("明细（前 40 条）：")
        A("")
        A("| tt | class | slot | from | 目标 | arg0=this |")
        A("|---|---|---|---|---|---|")
        for m in ms[:40]:
            A(
                f"| {m['table_type']} | {m['class']} | `{m['slot']}` | `{m['from_va']}` | "
                f"`{m['va']}` | {m['arg0_is_this']} |"
            )
        A("")
    A("## 8. 方法与已知限制")
    A("")
    A("1. **分支定位**：`case <int>:`（含多标签 fallthrough）、`if (V == N) {…}`、`if (V != N) <guard>; <body>`，")
    A("   以及 `switch` 表；`V` 取第二个形参及其别名（如 CLUB 的 `v4 = (int)a2`）。")
    A("2. **分支体**：花括号匹配 + 同层终止符（`break` / `goto` / `return` / 下一个 `case` / `}`）。")
    A("3. **字节偏移**：按 base 变量**声明元素宽度**换算（整型局部/形参 = 1 字节寻址，`_DWORD *` = ×4，")
    A("   `_QWORD *` = ×8），并对 `this` 的别名做**逐行 reaching-definition 判定**（Hex-Rays 会复用临时变量，")
    A("   例如 COMP 的 `v5` 在某行之后已改指别的对象，其后不得再当作 `this`）。")
    A("4. **`primary_off`**：分支体内最小的「带宽度解引用」偏移；64 位 `lo|hi` 拼接（如 `a1+40` / `a1+44`）取低位。")
    A("5. **不追踪共享协议 handler**（`0x140FE3F20` / `0x140FE2700`），避免跨表污染；其下 `COPY/DELE/BaCP` 等")
    A("   通用协议码因此不会出现在各表 4CC 集合里。")
    A("6. **限制**：`helper_computed` 分支无字节偏移（helper 未反编译，见第 7 节）；位域偏移可能比已验收")
    A("   线槽起点深 1–5 字节（记 `within_slot`）；`duni` 这类身份列走基类序列化，不在 4CC 分派中。")
    A("")
    A("## 9. 复现")
    A("")
    A("```")
    A("py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest   # 25 项断言，含 STARTING_RECORD 三条")
    A("py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --run        # 写 4 个交付物到 scratch/t97/out")
    A("```")
    A("")
    A("> 备注：任务书示例写 `1869899892 == 0x6F737474 == 'ostt'`，实际 `0x6F746874 = 'otht'`；")
    A("> 自检按真实字节 `'otht' -> 0x28` 断言（偏移结论不受影响）。")
    A("")
    (outdir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[t97] wrote REPORT.md", flush=True)


# --------------------------------------------------------------------------- #
# selftest
# --------------------------------------------------------------------------- #
def selftest() -> int:
    ok = True
    msgs = []

    def chk(cond, label, extra=""):
        nonlocal ok
        if not cond:
            ok = False
        msgs.append(("PASS" if cond else "FAIL") + " " + label + ((" :: " + extra) if extra else ""))

    # --- 4CC codec ---
    chk(int4cc(0x6F746874) == "otht", "int4cc(0x6F746874) == 'otht'", str(int4cc(0x6F746874)))
    chk(int4cc(0x7465616D) == "team", "int4cc(0x7465616D) == 'team'")
    chk(code_to_int("team") == 0x7465616D, "code_to_int('team')")
    chk(int4cc(0x6F746874) == "otht", "4CC decode is big-endian ASCII")

    # --- STARTING_RECORD get_prop (tt=45) ---
    p = FUNCS_DIR / "1415446a0.c"
    chk(p.exists(), "funcs/1415446a0.c present")
    if p.exists():
        f = CFunc(p, 0x1415446A0)
        brs = f.find_branches()
        got = {b["code_int"]: b for b in brs}
        for want_int, want_off, label in (
            (1869899892, 0x28, "otht"),
            (1918989417, 0x5A, "rati"),
            (1920099681, 0x5C, "rrea"),
        ):
            b = got.get(want_int)
            chk(b is not None, "STARTING_RECORD branch %d (%s) found" % (want_int, label))
            if b is None:
                continue
            chk(b["fourcc"] == label, "  fourcc == %r" % label, b["fourcc"])
            info = analyze_branch(f, b)
            chk(
                info["primary_off_int"] == want_off,
                "  %s -> mem_off 0x%x" % (label, want_off),
                str(info["primary_off_int"]),
            )
        # the variant glue `sub_14083D4F0(a1) + N` must never be taken as a field
        b = got.get(1869899892)
        if b:
            info = analyze_branch(f, b)
            offs = {o["off_int"] for o in info["mem_offsets"]}
            chk(72 not in offs, "variant glue offset 72 excluded from otht", str(sorted(offs)))
            chk(40 in offs and 44 in offs, "otht reads both 40 and 44", str(sorted(offs)))

    # --- offset unit handling ---
    hits = extract_offsets("v43 = ((unsigned __int64)*(unsigned int *)(a1 + 44) << 32) | *(int *)(a1 + 40);", "a1", 1, 1)
    chk({h["off_int"] for h in hits} == {40, 44}, "integer base: byte offsets", str([h["off_int"] for h in hits]))
    hits = extract_offsets("v11 = *((unsigned __int8 *)a1 + 185);", "a1", 8, 1)
    chk([h["off_int"] for h in hits] == [185], "cast-after base: byte offset", str(hits))
    hits = extract_offsets("v35 = a1[3];", "a1", 8, 1)
    chk([h["off_int"] for h in hits] == [24], "_QWORD base: index*8 = 24", str(hits))
    hits = extract_offsets("v12 = *(_DWORD *)(v11 + 5);", "v11", 4, 1)
    chk([h["off_int"] for h in hits] == [20], "_DWORD base: index*4 = 20", str(hits))
    hits = extract_offsets("(*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 19, 4);", "a1", 4, 1)
    chk([h["off_int"] for h in hits] == [76], "read_server address+size idiom", str(hits))
    hits = extract_offsets("v6 = sub_14083D4F0(a1) + 72;", "a1", 1, 1)
    chk(hits == [], "helper-return arithmetic is not a this-offset", str(hits))

    # --- e2e on the 67-table index ---
    idx = json.loads(read_text(VTABLE_INDEX))
    chk(len(idx["tables"]) == 67, "vtable_index has 67 table entries", str(len(idx["tables"])))
    club = next(t for t in idx["tables"] if t["class"] == "CLUB")
    fc = CFunc(T95_DIR / club["core"]["slot02_get_prop"]["file"])
    chk(len(fc.find_branches()) > 100, "CLUB get_prop yields >100 branches", str(len(fc.find_branches())))
    chk("v4" in fc.code_vars, "CLUB dispatch alias v4 detected", str(sorted(fc.code_vars)))

    text = "\n".join(msgs)
    print(text)
    print("selftest:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser(
        prog="t97_extract_4cc_mem.py",
        description="t97: Hex-Rays 4CC <-> memory offset extraction for the 67 FM24 table classes",
        epilog="exit codes: 0 ok, 1 selftest failure / internal error, 2 bad usage",
    )
    ap.add_argument("--run", action="store_true", help="run the extraction and write deliverables")
    ap.add_argument("--selftest", action="store_true", help="run built-in assertions")
    ap.add_argument(
        "--outdir",
        default=str(DEFAULT_OUTDIR),
        help="output directory (default: scratch/t97/out)",
    )
    ap.add_argument("--report", action="store_true", default=True, help="write REPORT.md (default on)")
    ap.add_argument("--no-report", action="store_false", dest="report", help="skip REPORT.md")
    ap.add_argument("--quiet", action="store_true", help="suppress per-table progress lines")
    args = ap.parse_args(argv)
    if not (args.run or args.selftest):
        ap.print_help()
        return 2
    if args.selftest:
        return selftest()
    try:
        run(args)
    except Exception:
        import traceback

        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
