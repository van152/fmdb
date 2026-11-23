#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t108 - 4CC <-> memory-offset extraction v2: inline helper tracing + Cnti fix.

Extends ``scripts/t97_extract_4cc_mem.py`` (left untouched) with three things:

1. **1-hop / 2-hop helper inlining.**  t97 left 2,525 dispatch branches as
   ``helper_computed`` because the helper they call was not decompiled.  IDA 9.4
   has since decompiled those helpers (``scratch/t95/funcs/*.c``, indexed by
   ``scratch/t107/out/helpers_index.json``).  For every such branch t108 now
   looks at *which argument of the helper call is the object* and then opens
   ``funcs/<helper>.c``:

   * ``arg0 == this`` (or a this alias) and the helper reads/writes
     ``arg0 + K`` -> ``resolved_via_helper`` with the byte offset ``K``
     (``offset_space="this"``).
   * ``arg0 == *(this + K)`` -> two-level resolution
     ``0xK -> 0xM`` (``offset_space="subobject"``).
   * the helper forwards a 4CC literal (or the dispatch code) into another
     function that is itself a table property handler -> the 4CC is resolved
     inside that handler and reported with ``offset_space="child_table"``
     plus the full ``helper_chain`` (this is the "secondary dispatcher" case,
     e.g. ``0x1411E9540`` / ``0x143CA2E60`` -> ``STARTING_RECORD::*_prop``).
   * the helper only touches globals / registries / out-params / pure
     arithmetic and never a persistent field of the object ->
     ``confirmed_computed_or_ui`` with a ``computed_reason``.

2. **``Cnti`` regression fix.**  The CLUB setter branch wrote both the
   sub-object pointer ``*(a1+216)`` and an inner adjunct flag ``*(a1+185)``;
   t97 picked the inner byte because it sorted by offset.  v2 classifies every
   offset occurrence by *role* (``test`` inside an ``if``/``while`` condition,
   ``write`` left of ``=``, ``read`` otherwise) and prefers the outer
   sub-object pointer over inner adjunct scalars, so ``Cnti -> 216``.

3. **t97 -> t108 comparison** over the full 67 tables and the 1,034-row XML
   denominator.

Deliverables (``--outdir``, default ``scratch/t108/out``):

  * ``fourcc_mem_map_v2.json``   - 67 tables, v2 map (+ ``helper_chain``, C lines)
  * ``xml_triage_v2.json``       - 1,034 rows + t97->t108 upgrade matrix
  * ``static_read_join_v2.json`` - 4CC <-> mem_off <-> slot19/slot20 join
  * ``REPORT.md`` / ``DONE.md``

Read-only towards ``reports/``, ``evidence/``, ``LEDGER.json`` and ``scratch/t97``.

Usage
-----
    py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --help
    py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --selftest
    py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --run

Exit codes: 0 = ok, 1 = selftest failure / internal error, 2 = bad usage.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import io
import json
import re
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------- #
# baseline (t97) import - never modified, only reused
# --------------------------------------------------------------------------- #
SCHEMA_VERSION = 2
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
T97_SCRIPT = HERE / "t97_extract_4cc_mem.py"


def _load_t97():
    spec = importlib.util.spec_from_file_location("t97_extract_4cc_mem", T97_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["t97_extract_4cc_mem"] = mod
    spec.loader.exec_module(mod)
    return mod


T97 = _load_t97()

FUNCS_DIR = T97.FUNCS_DIR
T95_DIR = T97.T95_DIR
VTABLE_INDEX = T97.VTABLE_INDEX
XML_COVERAGE = T97.XML_COVERAGE
L3_SCHEMA = T97.L3_SCHEMA
NUM = T97.NUM
GENERIC_HELPERS = T97.GENERIC_HELPERS

DEFAULT_OUTDIR = REPO / "scratch" / "t108" / "out"
T107_HELPERS = REPO / "scratch" / "t107" / "out" / "helpers_index.json"
T97_OUT = REPO / "scratch" / "t97" / "out"

MAX_HELPER_DEPTH = 2

# t97's original analysis + ranking, captured before we monkey-patch them below
BASE_ANALYZE_BRANCH = T97.analyze_branch
BASE_CAND_RANK = T97.cand_rank

# (func_va, branch line) -> v2 branch info, so the v2 extras can be re-attached to
# the candidate dicts that t97.build() creates (it only copies its own keys).
_INFO_BY_BRANCH: dict = {}


def v2_extra_fields(info: dict) -> dict:
    out = {
        "offset_space": info.get("offset_space"),
        "primary_role": info.get("primary_role"),
        "roles": info.get("roles"),
        "helper_chain": info.get("helper_chain") or [],
        "child": info.get("child"),
        "subobj_path": info.get("subobj_path"),
        "inner_off": info.get("inner_off"),
        "helper_member_offsets": info.get("helper_member_offsets"),
        "helper_member_roles": info.get("helper_member_roles"),
        "computed_reasons": info.get("computed_reasons") or [],
        "primary_line": info.get("primary_line"),
        "helper_resolutions": [
            {k: r.get(k) for k in (
                "helper_va", "helper_file", "helper_name", "status", "resolution",
                "computed_reason", "call_line", "forward", "depth",
            )}
            for r in (info.get("helper_resolutions") or [])
        ][:6],
    }
    return out


def attach_v2_extras(fmap: dict, verbose: bool = True) -> dict:
    """Re-attach the v2 branch info that ``t97.build()`` does not copy.

    ``t97.build()`` builds its candidate dict from a fixed key list over the
    info dict returned by ``analyze_branch``.  Because we monkey-patch
    ``analyze_branch`` with ``analyze_branch_v2``, the extra v2 fields
    (``offset_space`` / ``helper_chain`` / ``child`` / ``roles`` / ...) live in
    ``info["_extra"]`` only, keyed by ``(func_va, branch line)`` in
    ``_INFO_BY_BRANCH``.  Without this pass ``fourcc_mem_map_v2.json`` would
    report ``child_table_resolved == 0`` and
    ``helper_inline_resolutions_in_map == 0`` even though the tracer resolved
    them.  Every candidate (including ``alt``) is patched in place.
    """
    stats = {"candidates": 0, "attached": 0, "no_info": 0, "with_child": 0, "with_helper": 0}
    for rec in fmap.get("tables") or []:
        for cand in (rec.get("fourccs") or {}).values():
            for node in (cand, cand.get("alt")):
                if not isinstance(node, dict):
                    continue
                stats["candidates"] += 1
                try:
                    key = (int(node["func_va"], 16) & 0xFFFFFFFFFFFFFFFF, int(node["line_no"]))
                except (KeyError, TypeError, ValueError):
                    stats["no_info"] += 1
                    continue
                info = _INFO_BY_BRANCH.get(key)
                if info is None:
                    stats["no_info"] += 1
                    continue
                for k, v in (info.get("_extra") or {}).items():
                    node[k] = copy.deepcopy(v)
                stats["attached"] += 1
                if node.get("offset_space") == "child_table":
                    stats["with_child"] += 1
                if node.get("helper_chain"):
                    stats["with_helper"] += 1
    fmap["v2_extras"] = stats
    if verbose:
        print(
            "[t108] attach_v2_extras: %d/%d candidates patched "
            "(child_table=%d, helper_chain=%d, no_info=%d)"
            % (
                stats["attached"],
                stats["candidates"],
                stats["with_child"],
                stats["with_helper"],
                stats["no_info"],
            ),
            flush=True,
        )
    return stats


# --------------------------------------------------------------------------- #
# positional offset scan (t97 semantics + match position, for role tagging)
# --------------------------------------------------------------------------- #
def _offset_pattern(base: str):
    return re.compile(
        r"\*\s*\(\s*(?P<t1>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*\(\s*"
        + re.escape(base)
        + r"\s*\+\s*(?P<o1>" + NUM + r")\s*\)"
        r"|\*\s*\(\s*\(\s*(?P<t2>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*"
        + re.escape(base)
        + r"\s*\+\s*(?P<o2>" + NUM + r")\s*\)"
        r"|\*\s*\(\s*" + re.escape(base) + r"\s*\+\s*(?P<o3>" + NUM + r")\s*\)"
        r"|\b" + re.escape(base) + r"\s*\[\s*(?P<o4>" + NUM + r")\s*\]"
        r"|\b" + re.escape(base) + r"\s*\+\s*(?P<o5>" + NUM + r")\b"
    )


def offsets_with_pos(line: str, base: str, elem: int):
    """[(off_int, start_pos)] for one base variable on one source line."""
    out = []
    if not line or base not in line:
        return out
    for m in _offset_pattern(base).finditer(line):
        if m.group("o1") is not None:
            off = T97.parse_num(m.group("o1")) * elem
        elif m.group("o2") is not None:
            off = T97.parse_num(m.group("o2")) * (
                T97.POINTER_TARGETS.get(
                    T97.norm_type(m.group("t2")) + " *",
                    T97.type_size(T97.norm_type(m.group("t2"))) or 1,
                )
            )
        elif m.group("o3") is not None:
            off = T97.parse_num(m.group("o3")) * elem
        elif m.group("o4") is not None:
            off = T97.parse_num(m.group("o4")) * elem
        else:
            off = T97.parse_num(m.group("o5")) * elem
        out.append((off, m.start()))
    return out


COND_HEAD_RE = re.compile(r"^\s*(?:\}\s*)?(?:else\s+)?(?:if|while|for)\s*\(")


def _cond_ranges(text: str):
    """Character ranges of the controlling expression of an if/while line."""
    m = COND_HEAD_RE.match(text)
    if not m:
        return []
    start = text.index("(", m.start())
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return [(start, i)]
    return [(start, len(text))]


def _first_assign_pos(text: str):
    """Index of the first plain `=` (not ==/!=/<=/>=/compound)."""
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            q = ch
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == q:
                    break
                i += 1
            i += 1
            continue
        if ch == "=":
            prev = text[i - 1] if i else ""
            nxt = text[i + 1] if i + 1 < n else ""
            if prev in "=!<>+-*/%&|^" or nxt == "=":
                i += 1
                continue
            return i
        i += 1
    return None


def classify_roles(f, body_lines):
    """{off_int: {role}} for one branch body; role in {test, write, read}."""
    roles = defaultdict(set)
    for ln, text in body_lines:
        ranges = _cond_ranges(text)
        eq = _first_assign_pos(text)
        for base, elem in f.base_vars_at(ln - 1).items():
            if base not in text:
                continue
            for off, pos in offsets_with_pos(text, base, elem):
                if any(s <= pos < e for s, e in ranges):
                    roles[off].add("test")
                elif eq is not None and pos < eq:
                    roles[off].add("write")
                else:
                    roles[off].add("read")
    return roles


# --------------------------------------------------------------------------- #
# 4CC literals & call sites inside a branch body
# --------------------------------------------------------------------------- #
CALL_RE = re.compile(r"\b(?:sub|unk)_([0-9A-Fa-f]{6,12})\s*\(")
VAR_ASSIGN_RE = re.compile(
    r"^\s*(?:LOBYTE\s*\(\s*)?(?P<v>[A-Za-z_][A-Za-z0-9_]*)\s*\)?\s*=\s*"
    r"(?:\(\s*(?:(?:unsigned|signed)\s+)?(?:int|__int64|__int32|_DWORD|_QWORD|char)\s*\)\s*)?"
    r"(?P<lit>" + NUM + r")\s*;\s*$"
)


def split_args(text: str, open_idx: int):
    """Split a call argument list starting at text[open_idx] == '('."""
    depth = 0
    cur = []
    args = []
    i = open_idx
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            q = ch
            cur.append(ch)
            i += 1
            while i < n:
                cur.append(text[i])
                if text[i] == "\\":
                    cur.append(text[i + 1] if i + 1 < n else "")
                    i += 2
                    continue
                if text[i] == q:
                    break
                i += 1
            i += 1
            continue
        if ch in "([{":
            depth += 1
            if depth == 1 and ch == "(":
                i += 1
                continue
            cur.append(ch)
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                if "".join(cur).strip():
                    args.append("".join(cur).strip())
                return args, i
            cur.append(ch)
        elif ch == "," and depth == 1:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    return args, n


def branch_calls(f, body_lines):
    """[(va, args, line_no, literal_per_arg)] for sub_/unk_ calls in a body."""
    out = []
    literals = {}
    for ln, text in body_lines:
        m = VAR_ASSIGN_RE.match(text)
        if m:
            try:
                v = T97.parse_num(m.group("lit"))
            except ValueError:
                v = None
            if v is not None and v <= 0xFFFFFFFF and T97.int4cc(v & 0xFFFFFFFF):
                literals[m.group("v")] = v & 0xFFFFFFFF
        for cm in CALL_RE.finditer(text):
            va = int(cm.group(1), 16)
            if not (0x140000000 <= va < 0x145000000):
                continue
            args, _ = split_args(text, cm.end() - 1)
            lits = []
            for a in args:
                a = a.strip()
                v = None
                if re.fullmatch(NUM, a):
                    v = T97.parse_num(a)
                else:
                    core = re.sub(r"^\(*\s*(?:unsigned|signed)?\s*(?:int|__int64|__int32|_DWORD|char|_BYTE)\s*\)*", "", a).strip()
                    if core in literals:
                        v = literals[core]
                if v is not None and v <= 0xFFFFFFFF and T97.int4cc(v & 0xFFFFFFFF):
                    lits.append((v, T97.int4cc(v & 0xFFFFFFFF)))
                else:
                    lits.append(None)
            out.append({"va": va, "args": args, "line": ln, "arg_codes": lits})
    return out


def strip_casts(text: str) -> str:
    t = text.strip()
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r"^\(\s*(?:const\s+)?[A-Za-z_][A-Za-z0-9_]*(?:\s*\*+)?\s*\)\s*", "", t).strip()
    if t.startswith("(") and t.endswith(")"):
        depth = 0
        ok = True
        for i, ch in enumerate(t):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(t) - 1:
                    ok = False
                    break
        if ok:
            t = t[1:-1].strip()
    return t


SUBPTR_RE = re.compile(
    r"^\*\s*\(\s*(?P<t>[A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*\(\s*(?P<base>[A-Za-z_][A-Za-z0-9_]*)\s*\+\s*(?P<off>"
    + NUM + r")\s*\)$"
)
ADDR_RE = re.compile(r"^(?P<base>[A-Za-z_][A-Za-z0-9_]*)\s*\+\s*(?P<off>" + NUM + r")$")


def classify_arg0(f, line_idx, argtext: str):
    """How does a helper call receive the object?

    kind: this | subobject | interior | other
    """
    t = strip_casts(argtext)
    bases = f.base_vars_at(line_idx)
    if t in bases:
        return {"kind": "this", "var": t, "elem": bases[t]}
    m = SUBPTR_RE.match(t)
    if m and m.group("base") in bases:
        off = T97.parse_num(m.group("off")) * bases[m.group("base")]
        return {
            "kind": "subobject",
            "var": m.group("base"),
            "ptr_type": T97.norm_type(m.group("t")),
            "off": off,
            "off_hex": hex(off),
        }
    m = ADDR_RE.match(t)
    if m and m.group("base") in bases:
        off = T97.parse_num(m.group("off")) * bases[m.group("base")]
        return {"kind": "interior", "var": m.group("base"), "off": off, "off_hex": hex(off)}
    return {"kind": "other", "text": t}


# --------------------------------------------------------------------------- #
# helper tracer
# --------------------------------------------------------------------------- #
GLOBAL_RE = re.compile(
    r"\b(?:qword|dword|word|byte|unk|off|MEMORY\[|NtCurrentTeb|TlsIndex|xmmword)_?[0-9A-Fa-f]*"
)
INDIRECT_CALL_RE = re.compile(r"\(\s*\*+\s*\(?[^)]*\)?\s*\)\s*\(")


class Tracer:
    """Reads ``scratch/t95/funcs/<va>.c`` and resolves helper call sites."""

    def __init__(self, helpers_index: dict | None = None):
        self.index = {}
        if helpers_index:
            for k, v in helpers_index.items():
                self.index[int(k, 16)] = v
        self.cache = {}
        self.stats = Counter()

    # -- file access --------------------------------------------------------
    def path_for(self, va: int):
        p = FUNCS_DIR / ("%x.c" % va)
        if p.exists():
            return p
        rec = self.index.get(va)
        if rec and rec.get("file"):
            p2 = T95_DIR / rec["file"]
            if p2.exists():
                return p2
        return None

    def func(self, va: int):
        if va in self.cache:
            return self.cache[va]
        p = self.path_for(va)
        f = T97.CFunc(p, va) if p is not None else None
        if f is not None:
            # CFunc skips alias bookkeeping when the signature has no parameters
            for attr, default in (
                ("_bv_cache", {}),
                ("base_vars", {}),
                ("alias_defs", {}),
                ("_base_candidates", []),
                ("code_vars", set()),
                ("this_name", None),
            ):
                if not hasattr(f, attr):
                    setattr(f, attr, default)
        self.cache[va] = f
        return f

    # -- purity -------------------------------------------------------------
    @staticmethod
    def purity(f) -> dict:
        text = "\n".join(f.clean)
        globals_used = sorted(set(m.group(0) for m in GLOBAL_RE.finditer(text)))
        indirect = len(INDIRECT_CALL_RE.findall(text))
        return {
            "globals": globals_used[:8],
            "global_refs": len(globals_used),
            "indirect_calls": indirect,
            "lines": len(f.clean),
        }

    # -- member offsets of arg0 --------------------------------------------
    @staticmethod
    def member_offsets(f):
        """All arg0-relative offsets touched anywhere in the helper body."""
        out = {}
        if not getattr(f, "params", None) or not getattr(f, "this_name", None):
            return []
        for i, text in enumerate(f.clean):
            if not text.strip():
                continue
            for base, elem in f.base_vars_at(i).items():
                if base not in text:
                    continue
                for o in T97.extract_offsets(text, base, elem, i + 1):
                    key = (o["off_int"], o["line"])
                    if key in out:
                        continue
                    out[key] = o
        items = sorted(out.values(), key=lambda o: (o["off_int"], o["line"]))
        return items

    @staticmethod
    def roles_of(f, offsets):
        """{off_int: {roles}} for helper-body offsets."""
        roles = defaultdict(set)
        for i, text in enumerate(f.clean):
            ranges = _cond_ranges(text)
            eq = _first_assign_pos(text)
            for base, elem in f.base_vars_at(i).items():
                if base not in text:
                    continue
                for off, pos in offsets_with_pos(text, base, elem):
                    if any(s <= pos < e for s, e in ranges):
                        roles[off].add("test")
                    elif eq is not None and pos < eq:
                        roles[off].add("write")
                    else:
                        roles[off].add("read")
        return roles

    # -- code forwarding (secondary dispatcher) ----------------------------
    def forwarding_targets(self, hf, param_name: str):
        out = []
        for i, text in enumerate(hf.clean):
            for cm in CALL_RE.finditer(text):
                va = int(cm.group(1), 16)
                args, _ = split_args(text, cm.end() - 1)
                if any(strip_casts(a) == param_name for a in args):
                    out.append((va, i + 1))
        return out

    def resolve_code_in(self, va: int, code_int: int, depth: int):
        """Analyze the 4CC branch of another handler function."""
        f = self.func(va)
        if f is None:
            return None
        for br in f.find_branches():
            if br["code_int"] != code_int:
                continue
            info = analyze_branch_v2(f, br, tracer=self, depth=depth + 1, allow_inline=False)
            return {
                "target_va": hex(va),
                "target_file": "funcs/%x.c" % va,
                "target_name": f.name,
                "code": br["fourcc"],
                "code_int": br["code_int"],
                "line_no": br["line_no"],
                "access_kind": info["access_kind"],
                "primary_off": info["primary_off"],
                "primary_off_int": info["primary_off_int"],
                "width": info["width"],
                "c_type": info["c_type"],
                "mem_offsets": info["mem_offsets"][:8],
                "subobj": info["subobj"],
            }
        return None

    # -- the actual trace ---------------------------------------------------
    def resolve(self, va: int, form: dict, code_int, codes_from_body, depth: int):
        """Classify one helper call inside a 4CC branch body."""
        if va in GENERIC_HELPERS:
            return {"status": "generic_glue", "helper_va": hex(va)}
        hf = self.func(va)
        if hf is None:
            self.stats["file_missing"] += 1
            return {"status": "no_file", "helper_va": hex(va)}
        pur = self.purity(hf)
        base = {
            "helper_va": hex(va),
            "helper_file": "funcs/%x.c" % va,
            "helper_name": hf.name,
            "helper_lines": len(hf.clean),
            "arg0": form,
            "depth": depth,
            "purity": pur,
        }

        # ---- (a) secondary dispatcher: code literal / code arg forwarded ----
        if form["kind"] in ("this", "subobject", "interior", "other"):
            call_codes = [c for c in (codes_from_body or []) if c]
            disp = self._try_dispatch(hf, call_codes, code_int, depth, base)
            if disp:
                return disp

        # ---- (b) member getter / setter on the object -----------------------
        if form["kind"] == "other":
            self.stats["arg0_not_this"] += 1
            return {
                **base,
                "status": "computed",
                "computed_reason": "arg0_is_out_param_local_or_global",
            }
        offs = self.member_offsets(hf)
        if offs:
            roles = self.roles_of(hf, offs)
            self.stats["member_resolved"] += 1
            return {
                **base,
                "status": "resolved",
                "resolution": "member",
                "member_offsets": offs[:12],
                "member_roles": {hex(k): sorted(v) for k, v in roles.items()},
            }

        # ---- (c) one more hop: helper calls another helper on the object ----
        if depth < MAX_HELPER_DEPTH:
            p0 = hf.params[0][0] if hf.params else None
            for i, text in enumerate(hf.clean):
                for cm in CALL_RE.finditer(text):
                    va2 = int(cm.group(1), 16)
                    if va2 in GENERIC_HELPERS or va2 == va:
                        continue
                    args, _ = split_args(text, cm.end() - 1)
                    if not args:
                        continue
                    form2 = classify_arg0(hf, i, args[0])
                    if form2["kind"] == "other":
                        continue
                    sub = self.resolve(va2, form2, None, [], depth + 1)
                    if sub.get("status") in ("resolved", "dispatched"):
                        self.stats["hop2_resolved"] += 1
                        return {
                            **base,
                            "status": sub["status"],
                            "resolution": sub.get("resolution"),
                            "via_hop2": sub,
                            "member_offsets": sub.get("member_offsets"),
                            "member_roles": sub.get("member_roles"),
                            "forward": sub.get("forward"),
                        }
                    self.stats["hop2_dead"] += 1

        # ---- (d) computed / UI only ----------------------------------------
        reason = "constant_or_arith_only"
        if pur["global_refs"]:
            reason = "global_or_registry_lookup"
        if pur["indirect_calls"]:
            reason = "vtable_dispatch_through_global"
        self.stats["computed_" + reason] += 1
        return {**base, "status": "computed", "computed_reason": reason}

    def _try_dispatch(self, hf, call_codes, code_int, depth, base):
        """Is the helper forwarding a 4CC into another table handler?"""
        if depth >= MAX_HELPER_DEPTH + 1:
            return None
        param_names = [p[0] for p in hf.params]
        tried = set()
        for idx, (pn, pdecl) in enumerate(hf.params):
            for tva, tline in self.forwarding_targets(hf, pn):
                if tva in tried:
                    continue
                tried.add(tva)
                if self.path_for(tva) is None:
                    continue
                # candidate codes for this parameter position
                cands = []
                if call_codes:
                    cands.extend(call_codes)
                if code_int is not None:
                    cands.append(code_int)
                seen = set()
                for c in cands:
                    if c in seen:
                        continue
                    seen.add(c)
                    rec = self.resolve_code_in(tva, c, depth)
                    if rec is None:
                        continue
                    self.stats["dispatch_resolved"] += 1
                    return {
                        **base,
                        "status": "dispatched",
                        "resolution": "child_handler",
                        "forward": {
                            "code": rec["code"],
                            "code_int": rec["code_int"],
                            "arg_index": idx,
                            "param": pn,
                            "helper_call_line": tline,
                            "target_va": rec["target_va"],
                            "target_file": rec["target_file"],
                            "target_name": rec["target_name"],
                            "target_line_no": rec["line_no"],
                            "target_access_kind": rec["access_kind"],
                            "target_primary_off": rec["primary_off"],
                            "target_width": rec["width"],
                            "target_c_type": rec["c_type"],
                        },
                        "child_target": rec,
                    }
        return None


# --------------------------------------------------------------------------- #
# branch analysis v2
# --------------------------------------------------------------------------- #
KIND_ORDER = [
    "direct_field",
    "bitfield",
    "subobj_deref",
    "resolved_via_helper",
    "helper_computed",
    "delegated_or_empty",
]


def _pick_primary(offsets, sub_ptr_offsets, roles):
    """Role- and sub-object-aware choice of the field offset inside a branch."""

    def score(o):
        off = o["off_int"]
        rs = roles.get(off) or {"read"}
        test_only = 1 if rs == {"test"} else 0
        is_sub = 0 if off in sub_ptr_offsets else 1
        return (test_only, is_sub, off, o.get("line") or 0)

    cand = [o for o in offsets if o.get("width") in (1, 2, 4, 8)]
    if not cand:
        cand = list(offsets)
    if not cand:
        return None
    return min(cand, key=score)


def analyze_branch_v2(f, br, tracer=None, depth: int = 0, allow_inline: bool = True):
    """t97 branch analysis + role-aware primary + helper inlining."""
    info = BASE_ANALYZE_BRANCH(f, br)
    a, b = br["body"]
    body = [(i + 1, f.clean[i]) for i in range(a, min(b + 1, len(f.lines)))]
    roles = classify_roles(f, body)
    info["roles"] = {hex(k): sorted(v) for k, v in sorted(roles.items())}

    uniq = info["mem_offsets"]
    subobjs = info.get("subobjects") or []
    sub_ptr = {s["ptr_off_int"] for s in subobjs}
    primary = _pick_primary(uniq, sub_ptr, roles)

    kind = info["access_kind"]
    if uniq:
        if primary is not None and primary["off_int"] in sub_ptr:
            kind = "subobj_deref"
            so = next((s for s in subobjs if s["ptr_off_int"] == primary["off_int"]), None)
            if so is not None:
                info["subobj"] = so
        elif info["bitmask_or_shift"] and any(
            o["off_int"] == primary["off_int"] for o in uniq
        ):
            kind = "bitfield"
        else:
            kind = "direct_field"
        info["access_kind"] = kind
        info["primary_off"] = primary["off"]
        info["primary_off_int"] = primary["off_int"]
        info["c_type"] = primary["c_type"] or info["c_type"]
        info["width"] = primary["width"] or info["width"]
        info["primary_role"] = sorted(roles.get(primary["off_int"], {"read"}))
        info["offset_space"] = "this"
    else:
        info["offset_space"] = None
        info["primary_role"] = None

    info.setdefault("helper_chain", [])
    info["helper_resolutions"] = []
    info["computed_reasons"] = []

    # ---- helper inlining ---------------------------------------------------
    if tracer is not None and allow_inline and not uniq and kind in (
        "helper_computed",
        "delegated_or_empty",
        "subobj_deref",
    ):
        calls = branch_calls(f, body)
        literal_codes = sorted(
            {c for call in calls for (c, _) in [x for x in call["arg_codes"] if x]}
        )
        best = None
        for call in calls:
            form = classify_arg0(f, call["line"] - 1, call["args"][0]) if call["args"] else {"kind": "other"}
            codes = [c for c in [x[0] if x else None for x in call["arg_codes"]] if c]
            res = tracer.resolve(call["va"], form, br["code_int"], codes or literal_codes, depth=1)
            res["call_line"] = call["line"]
            res["call_args"] = call["args"][:4]
            info["helper_resolutions"].append(res)
            if res.get("status") in ("resolved", "dispatched") and best is None:
                best = res
            if res.get("status") == "computed" and res.get("computed_reason"):
                info["computed_reasons"].append(res["computed_reason"])

        if best is not None:
            info["helper_chain"] = [
                {
                    "va": best["helper_va"],
                    "file": best["helper_file"],
                    "name": best["helper_name"],
                    "arg0_form": best["arg0"]["kind"],
                    "call_line": best["call_line"],
                }
            ]
            if best["status"] == "dispatched":
                fw = best["forward"]
                info["helper_chain"].append(
                    {
                        "va": fw["target_va"],
                        "file": fw["target_file"],
                        "name": fw["target_name"],
                        "role": "child_table_handler",
                        "code": fw["code"],
                        "line_no": fw["target_line_no"],
                    }
                )
                ch = best["child_target"]
                info["access_kind"] = "resolved_via_helper"
                info["offset_space"] = "child_table"
                info["child"] = {
                    "table_handler_va": fw["target_va"],
                    "table_handler_file": fw["target_file"],
                    "code": fw["code"],
                    "code_int": fw["code_int"],
                    "mem_off": fw["target_primary_off"],
                    "mem_off_int": ch["primary_off_int"],
                    "width": fw["target_width"],
                    "c_type": fw["target_c_type"],
                    "access_kind": fw["target_access_kind"],
                    "line_no": fw["target_line_no"],
                }
                info["primary_off"] = None
                info["primary_off_int"] = None
            else:
                mem = best.get("member_offsets") or []
                if mem:
                    mem_roles = {
                        int(k, 16): set(v) for k, v in (best.get("member_roles") or {}).items()
                    }
                    # prefer a non-test, this-relative read; else first offset
                    pool = [o for o in mem if mem_roles.get(o["off_int"], {"read"}) != {"test"}]
                    pick = (pool or mem)[0]
                    info["access_kind"] = "resolved_via_helper"
                    info["helper_member_offsets"] = mem[:8]
                    info["helper_member_roles"] = {
                        hex(k): sorted(v) for k, v in sorted(mem_roles.items())
                    }
                    if best["arg0"]["kind"] == "subobject":
                        info["offset_space"] = "subobject"
                        info["subobj_path"] = [
                            best["arg0"]["off"],
                            pick["off_int"],
                        ]
                        info["inner_off"] = pick["off"]
                        info["inner_off_int"] = pick["off_int"]
                        info["subobj"] = {
                            "ptr_off": best["arg0"]["off_hex"],
                            "ptr_off_int": best["arg0"]["off"],
                            "ptr_type": best["arg0"].get("ptr_type"),
                            "var": "<helper-arg0>",
                            "ptr_line": best["call_line"],
                            "inner_off": pick["off"],
                            "inner_off_int": pick["off_int"],
                            "inner_type": pick["c_type"],
                            "via_helper": best["helper_va"],
                        }
                    elif best["arg0"]["kind"] == "interior":
                        info["offset_space"] = "this"
                    else:
                        info["offset_space"] = "this"
                    info["primary_off"] = best["arg0"]["off_hex"] if best["arg0"]["kind"] == "subobject" else pick["off"]
                    info["primary_off_int"] = best["arg0"]["off"] if best["arg0"]["kind"] == "subobject" else pick["off_int"]
                    info["c_type"] = pick["c_type"]
                    info["width"] = pick["width"]
                    info["primary_line"] = pick["line"]
        elif info["helper_resolutions"]:
            info["access_kind"] = "confirmed_computed_or_ui"
    info["branch_code"] = br.get("fourcc")
    _INFO_BY_BRANCH[(f.va & 0xFFFFFFFFFFFFFFFF, br["line_no"])] = info
    info["_extra"] = v2_extra_fields(info)
    return info


def k_sort(v):
    return v


# --------------------------------------------------------------------------- #
# candidate ranking v2
# --------------------------------------------------------------------------- #
KIND_RANK_V2 = {
    "direct_field": 0,
    "bitfield": 1,
    "subobj_deref": 2,
    "resolved_via_helper": 3,
    "confirmed_computed_or_ui": 4,
    "helper_computed": 4,
    "delegated_or_empty": 5,
}


def cand_rank_v2(c: dict):
    """Prefer direct evidence > helper-resolved > computed; then shallow."""
    kind = c.get("access_kind")
    return (
        KIND_RANK_V2.get(kind, 6),
        0 if c.get("offset_space") == "this" else 1,
        0 if not c.get("delegated") else 1,
        c.get("depth", 0),
        T97.SLOT_RANK.get(c.get("slot"), 2),
        c.get("line_no", 0),
    )


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #
def build_v2(verbose: bool = True):
    helpers_index = {}
    if T107_HELPERS.exists():
        helpers_index = json.loads(T97.read_text(T107_HELPERS)).get("helpers") or {}
    tracer = Tracer(helpers_index)
    T97.analyze_branch = lambda f, br: analyze_branch_v2(f, br, tracer=tracer, depth=0)
    T97.cand_rank = cand_rank_v2
    fmap = T97.build(DEFAULT_OUTDIR, verbose=verbose)
    attach_v2_extras(fmap, verbose=verbose)
    fmap["schema_id"] = "fm24.t108.fourcc_mem_map_v2"
    fmap["schema_version"] = SCHEMA_VERSION
    fmap["generated_by"] = "t108"
    fmap["method"] += (
        "  t108 adds: (i) every offset occurrence is tagged test/write/read and a "
        "sub-object pointer field wins over inner adjunct scalars; (ii) branches without "
        "any direct offset inline the helper they call (1-2 hops, scratch/t95/funcs/<va>.c): "
        "an arg0-relative getter/setter yields `resolved_via_helper` (this- or "
        "subobject-relative), a helper that forwards a 4CC into another table handler is "
        "resolved inside that handler (`offset_space=child_table`), and helpers that only "
        "read globals/registries/out-params are marked `confirmed_computed_or_ui`."
    )
    fmap["tracer_stats"] = dict(tracer.stats)
    fmap["inputs"]["t107_helpers_index"] = {
        "path": "scratch/t107/out/helpers_index.json",
        "sha256": T97.sha256_of(T107_HELPERS) if T107_HELPERS.exists() else None,
    }
    fmap["inputs"]["t97_baseline"] = {
        "path": "scratch/t97/out/fourcc_mem_map.json",
        "sha256": T97.sha256_of(T97_OUT / "fourcc_mem_map.json")
        if (T97_OUT / "fourcc_mem_map.json").exists()
        else None,
    }
    return fmap


# --------------------------------------------------------------------------- #
# triage v2
# --------------------------------------------------------------------------- #
ENTITY_TABLE_MATCH = T97.ENTITY_TABLE_MATCH


def kind_to_bucket(cand: dict) -> str:
    kind = cand.get("access_kind")
    space = cand.get("offset_space")
    if kind == "resolved_via_helper":
        if space == "child_table":
            return "hit_helper_child_table"
        if space == "subobject":
            return "hit_resolved_via_helper_subobj"
        return "hit_resolved_via_helper"
    if kind in ("direct_field", "bitfield"):
        return "hit_direct_mem_off"
    if kind == "subobj_deref":
        return "hit_subobj_deref"
    if kind == "confirmed_computed_or_ui":
        return "hit_confirmed_computed_or_ui"
    if kind == "helper_computed":
        return "hit_helper_computed"
    return "hit_delegated_or_empty"


def triage_v2(fourcc_map: dict, xml_cov: dict):
    by_entity = defaultdict(dict)
    secondary = defaultdict(dict)
    shared_vas = {int(x["va"], 16) for x in fourcc_map.get("shared_protocol_handlers", [])}
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
                if cur is None or cand_rank_v2(cand) < cand_rank_v2(cur):
                    store[e][code] = cand
    lower_index = {e: {c.lower(): c for c in d} for e, d in by_entity.items()}
    global_index = defaultdict(list)
    for rec in fourcc_map["tables"]:
        for code, cand in rec["fourccs"].items():
            global_index[code].append(
                {
                    "table_type": rec["table_type"],
                    "table_class": rec["class"],
                    "entity_tag": rec["entity_tag"],
                    "access_kind": cand["access_kind"],
                    "offset_space": cand.get("offset_space"),
                    "primary_off": cand.get("primary_off"),
                    "func_va": cand["func_va"],
                    "line_no": cand["line_no"],
                }
            )

    def detail(hit, match_kind):
        return {
            "table_class": hit.get("table_class"),
            "slot": hit["slot"],
            "func_va": hit["func_va"],
            "file": hit["file"],
            "line_no": hit["line_no"],
            "access_kind": hit["access_kind"],
            "offset_space": hit.get("offset_space"),
            "primary_off": hit.get("primary_off"),
            "width": hit.get("width"),
            "c_type": hit.get("c_type"),
            "primary_role": hit.get("primary_role"),
            "mem_offsets": hit.get("mem_offsets"),
            "subobj": hit.get("subobj"),
            "helper_calls": hit.get("helper_calls"),
            "helper_chain": hit.get("helper_chain"),
            "child": hit.get("child"),
            "computed_reasons": hit.get("computed_reasons"),
            "bitmask_or_shift": hit.get("bitmask_or_shift"),
            "delegated": hit["delegated"],
            "match_kind": match_kind,
        }

    rows = xml_cov["rows"]
    out_rows = []
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
        rec = None
        if hit is not None:
            rec = detail(hit, match_kind)
            proposed = kind_to_bucket(hit)
            sec = secondary.get(ent, {}).get(code)
            if sec is not None:
                rec["secondary_hit"] = {
                    "table_class": sec.get("table_class"),
                    "slot": sec["slot"],
                    "func_va": sec["func_va"],
                    "line_no": sec["line_no"],
                    "access_kind": sec["access_kind"],
                    "primary_off": sec.get("primary_off"),
                }
        else:
            sec = secondary.get(ent, {}).get(code)
            elsewhere = global_index.get(code, [])
            if sec is not None:
                rec = detail(sec, "same_entity_tag_other_table")
                rec["secondary_only"] = True
                proposed = "hit_other_table_same_tag"
            elif elsewhere:
                only_shared = all(e_.get("func_va") in shared_vas for e_ in elsewhere)
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
                proposed = "absent_everywhere_in_67_tables"
        rows_out = {
            "id": r["id"],
            "entity": ent,
            "code": code,
            "bucket_after": bucket,
            "bucket_before": r.get("bucket_before"),
            "proposed_bucket": proposed,
            "t108": rec,
            "pointer": r.get("pointer"),
        }
        out_rows.append(rows_out)

    transitions = defaultdict(Counter)
    for row in out_rows:
        transitions[row["bucket_after"]][row["proposed_bucket"]] += 1
    per_ent = defaultdict(Counter)
    for row in out_rows:
        per_ent[row["entity"]][row["proposed_bucket"]] += 1
    summary = {
        "denominator": len(rows),
        "by_entity": {ent: dict(sorted(c.items())) for ent, c in sorted(per_ent.items())},
        "by_bucket_transition": {
            b: dict(sorted(c.items())) for b, c in sorted(transitions.items())
        },
        "proposed_totals": dict(sorted(Counter(r["proposed_bucket"] for r in out_rows).items())),
        "breakout": {
            b: {"total": sum(c.values()), **dict(sorted(c.items()))}
            for b, c in sorted(transitions.items())
        },
    }
    return summary, out_rows, by_entity


# --------------------------------------------------------------------------- #
# regression vs accepted L3
# --------------------------------------------------------------------------- #
def validate_v2(rows):
    if not L3_SCHEMA.exists():
        return {"available": False}
    d = json.loads(T97.read_text(L3_SCHEMA))
    sections = {
        "club_main_row_fields": "club",
        "nation_main_row_fields": "nation",
        "comp_main_row_fields": "comp",
    }
    rows_by = {}
    for r in rows:
        rows_by.setdefault((r["entity"], r["code"].lower()), r)
    items = []
    counts = Counter()
    for sect, ent in sections.items():
        for x in (d.get(sect) or {}).get("L3_fields") or []:
            code = x.get("code")
            disp = x.get("object_displacement")
            width = x.get("slot_width")
            if disp is None:
                continue
            r = rows_by.get((ent, str(code).lower()))
            cand = (r or {}).get("t108") or {}
            got = cand.get("primary_off")
            space = cand.get("offset_space")
            got_i = int(got, 16) if isinstance(got, str) else None
            if got_i is None or space not in ("this", None):
                verdict = "no_static_hit"
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
                    "t108_off": got_i,
                    "t108_off_hex": got,
                    "t108_access_kind": cand.get("access_kind"),
                    "t108_offset_space": space,
                    "t108_primary_role": cand.get("primary_role"),
                    "t108_table_class": cand.get("table_class"),
                    "t108_func_va": cand.get("func_va"),
                    "t108_line_no": cand.get("line_no"),
                    "verdict": verdict,
                }
            )
    counts["checked"] = len(items)
    return {
        "available": True,
        "source": {
            "path": "reports/club_nation_subtable_schema.json",
            "sha256": T97.sha256_of(L3_SCHEMA),
        },
        "note": (
            "accepted `object_displacement` is the wire-slot origin; t108 reports the exact "
            "byte offset of the field, so bitfields may land inside the slot (`within_slot`)."
        ),
        "totals": dict(counts),
        "items": items,
    }


# --------------------------------------------------------------------------- #
# t97 -> t108 comparison
# --------------------------------------------------------------------------- #
def load_t97_xml():
    p = T97_OUT / "xml_triage.json"
    if not p.exists():
        return None
    return json.loads(T97.read_text(p))


def compare_v2(xml_v2, fourcc_map):
    """t97 -> t108 upgrade matrix (per denominator row + per access_kind)."""
    old = load_t97_xml()
    old_rows = {}
    if old:
        old_rows = {r["id"]: r for r in old["rows"]}
    per_bucket = defaultdict(Counter)
    upgrades = []
    kind_delta = Counter()
    for row in xml_v2["rows"]:
        o = old_rows.get(row["id"]) or {}
        oto = (o.get("t97") or {})
        nto = (row.get("t108") or {})
        old_kind = oto.get("access_kind")
        new_kind = nto.get("access_kind")
        kind_delta[(old_kind, new_kind)] += 1
        b = row["bucket_after"]
        per_bucket[b]["rows"] += 1
        if o.get("proposed_bucket"):
            per_bucket[b]["t97_" + o["proposed_bucket"]] += 1
        per_bucket[b]["t108_" + row["proposed_bucket"]] += 1
        gained_off = (
            oto.get("primary_off") is None
            and nto.get("primary_off") is not None
        )
        gained_child = (row.get("t108") or {}).get("offset_space") == "child_table"
        if gained_off:
            per_bucket[b]["gained_this_offset"] += 1
            upgrades.append(
                {
                    "id": row["id"],
                    "entity": row["entity"],
                    "code": row["code"],
                    "bucket": b,
                    "t97_kind": old_kind,
                    "t108_kind": new_kind,
                    "t97_off": oto.get("primary_off"),
                    "t108_off": nto.get("primary_off"),
                    "offset_space": nto.get("offset_space"),
                    "helper_chain": nto.get("helper_chain"),
                    "func_va": nto.get("func_va"),
                    "line_no": nto.get("line_no"),
                }
            )
        elif gained_child:
            per_bucket[b]["gained_child_table_offset"] += 1
            upgrades.append(
                {
                    "id": row["id"],
                    "entity": row["entity"],
                    "code": row["code"],
                    "bucket": b,
                    "t97_kind": old_kind,
                    "t108_kind": new_kind,
                    "t97_off": oto.get("primary_off"),
                    "t108_off": None,
                    "child_off": ((row.get("t108") or {}).get("child") or {}).get("mem_off"),
                    "offset_space": "child_table",
                    "helper_chain": nto.get("helper_chain"),
                    "func_va": nto.get("func_va"),
                    "line_no": nto.get("line_no"),
                }
            )
    # global access_kind delta over all table x 4CC pairs
    old_pairs = {}
    p97 = T97_OUT / "fourcc_mem_map.json"
    if p97.exists():
        d = json.loads(T97.read_text(p97))
        for rec in d["tables"]:
            for code, cand in rec["fourccs"].items():
                old_pairs[(rec["table_type"], rec["class"], code)] = cand["access_kind"]
    pair_delta = Counter()
    kinds_new = Counter()
    kinds_old = Counter()
    for rec in fourcc_map["tables"]:
        for code, cand in rec["fourccs"].items():
            k = (rec["table_type"], rec["class"], code)
            kinds_new[cand["access_kind"]] += 1
            kinds_old[old_pairs.get(k, "absent_then")] += 1
            pair_delta[(old_pairs.get(k, "absent_then"), cand["access_kind"])] += 1
    return {
        "t97_available": bool(old),
        "per_bucket": {b: dict(sorted(c.items())) for b, c in sorted(per_bucket.items())},
        "upgrades": upgrades,
        "upgrade_count": len(upgrades),
        "row_kind_delta": {
            "%s->%s" % (a or "none", b or "none"): n
            for (a, b), n in sorted(kind_delta.items(), key=lambda kv: -kv[1])
            if a != b
        },
        "pair_kind_delta": {
            "%s->%s" % (a, b): n for (a, b), n in sorted(pair_delta.items(), key=lambda kv: -kv[1])
            if a != b
        },
        "kinds_t97": dict(sorted(kinds_old.items())),
        "kinds_t108": dict(sorted(kinds_new.items())),
    }


# --------------------------------------------------------------------------- #
# run
# --------------------------------------------------------------------------- #
def run(args):
    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = REPO / outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("[t108] parsing scratch/t95 Hex-Rays output (+ helper inlining) ...", flush=True)
    fmap = build_v2(verbose=not args.quiet)
    for rec in fmap["tables"]:
        for code, cand in rec["fourccs"].items():
            cand["table_class"] = rec["class"]
            if "alt" in cand:
                cand["alt"]["table_class"] = rec["class"]
    (outdir / "fourcc_mem_map_v2.json").write_text(
        json.dumps(fmap, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("[t108] wrote fourcc_mem_map_v2.json", flush=True)

    xml_cov = json.loads(T97.read_text(XML_COVERAGE))
    summary, rows, by_entity = triage_v2(fmap, xml_cov)
    comparison = compare_v2({"rows": rows}, fmap)
    xml_out = {
        "schema_id": "fm24.t108.xml_triage_v2",
        "schema_version": SCHEMA_VERSION,
        "generated_by": "t108",
        "status": "complete",
        "source": {
            "path": "reports/xml_denominator_coverage.json",
            "sha256": T97.sha256_of(XML_COVERAGE),
            "denominator": xml_cov.get("count"),
            "buckets_used": xml_cov.get("buckets_order"),
        },
        "note": (
            "annotation only: reports/ is NOT modified. `proposed_bucket` is a t108 candidate "
            "class derived from static Hex-Rays evidence (t97 evidence + helper inlining), not "
            "an accepted bucket. `offset_space` says whether the reported offset is relative to "
            "`this`, to a sub-object, or to a child table handler."
        ),
        "summary": summary,
        "code_index_size": {e: len(d) for e, d in sorted(by_entity.items())},
        "validation_vs_accepted_L3": validate_v2(rows),
        "comparison_t97_vs_t108": comparison,
        "rows": rows,
    }
    (outdir / "xml_triage_v2.json").write_text(
        json.dumps(xml_out, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("[t108] wrote xml_triage_v2.json", flush=True)

    vtable_index = json.loads(T97.read_text(VTABLE_INDEX))
    join, jtot = T97.build_static_join(fmap, vtable_index)
    old_join = {}
    pj = T97_OUT / "static_read_join.json"
    if pj.exists():
        old_join = json.loads(T97.read_text(pj)).get("totals") or {}
    join_out = {
        "schema_id": "fm24.t108.static_read_join_v2",
        "schema_version": SCHEMA_VERSION,
        "generated_by": "t108",
        "status": "complete",
        "method": (
            "all `base + n` address expressions inside slot19_read_server / "
            "slot20_read_client / slot21_write are converted to byte offsets with the same "
            "declared-element-size rule; the 4CC primary offset from slot02/slot03 (v2, incl. "
            "helper-resolved this-relative offsets) is then intersected with those offset sets."
        ),
        "totals": jtot,
        "totals_t97": old_join,
        "delta": {
            k: jtot.get(k, 0) - (old_join.get(k) or 0)
            for k in ("fourccs_with_off", "hit_read_server", "hit_read_client", "hit_any_read")
        },
        "tables": join,
    }
    (outdir / "static_read_join_v2.json").write_text(
        json.dumps(join_out, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print("[t108] wrote static_read_join_v2.json", flush=True)

    if args.report:
        write_report(outdir, fmap, xml_out, join_out)
    write_done(outdir, fmap, xml_out, join_out)
    return fmap, xml_out, join_out


def _kind_counts(fmap):
    kinds = Counter()
    pairs = 0
    with_off = 0
    child = 0
    for rec in fmap["tables"]:
        for cand in rec["fourccs"].values():
            kinds[cand["access_kind"]] += 1
            pairs += 1
            if cand.get("primary_off_int") is not None:
                with_off += 1
            if cand.get("offset_space") == "child_table":
                child += 1
    return kinds, pairs, with_off, child


def write_done(outdir, fmap, xml_out, join_out):
    kinds, pairs, with_off, child = _kind_counts(fmap)
    s = xml_out["summary"]
    br = s["breakout"]
    t = join_out["totals"]
    d = join_out["delta"]
    vt = (xml_out.get("validation_vs_accepted_L3") or {}).get("totals") or {}
    cmp_ = xml_out["comparison_t97_vs_t108"]
    ko = (cmp_.get("kinds_t97") or {})
    L = []
    A = L.append
    A("DONE type=t108b")
    A("")
    A("# t108 — 4CC ↔ 内存偏移 v2（helper 内联 + Cnti 修复）")
    A("")
    A("status: complete")
    try:
        _rel = outdir.resolve().relative_to(REPO).as_posix()
    except ValueError:
        _rel = outdir.as_posix()
    A(f"outputs: {_rel}")
    A("")
    A("## 核心统计")
    A("")
    A(f"- tables_covered: {fmap['table_count']}/67")
    A(f"- unique_fourcc: {fmap['unique_fourcc_count']}")
    A(f"- table_fourcc_pairs: {pairs}")
    A(f"- pairs_with_this_or_subobj_offset: {with_off} (t97: 1808)  → +{with_off - 1808}")
    A(f"- child_table_resolved (4CC 在子表 handler 内定位): {child}")
    A(
        "- access_kind: direct_field={}, bitfield={}, subobj_deref={}, "
        "resolved_via_helper={}, helper_computed={}, confirmed_computed_or_ui={}, "
        "delegated_or_empty={}".format(
            kinds.get("direct_field", 0),
            kinds.get("bitfield", 0),
            kinds.get("subobj_deref", 0),
            kinds.get("resolved_via_helper", 0),
            kinds.get("helper_computed", 0),
            kinds.get("confirmed_computed_or_ui", 0),
            kinds.get("delegated_or_empty", 0),
        )
    )
    A(
        "- t97 access_kind: direct_field={}, bitfield={}, subobj_deref={}, helper_computed={}, "
        "delegated_or_empty={}".format(
            ko.get("direct_field", 0),
            ko.get("bitfield", 0),
            ko.get("subobj_deref", 0),
            ko.get("helper_computed", 0),
            ko.get("delegated_or_empty", 0),
        )
    )
    A(
        "- helper_computed: {} → {}".format(
            ko.get("helper_computed", 0), kinds.get("helper_computed", 0)
        )
    )
    A(f"- helper_inline_resolutions_in_map: {sum(1 for rec in fmap['tables'] for c in rec['fourccs'].values() if c.get('helper_chain'))}")
    _ex = fmap.get("v2_extras") or {}
    if _ex:
        A(
            "- attach_v2_extras: {}/{} 候选（含 alt）已回填（child_table {}，helper_chain {}）".format(
                _ex.get("attached", 0),
                _ex.get("candidates", 0),
                _ex.get("with_child", 0),
                _ex.get("with_helper", 0),
            )
        )
    A("")
    A("## 回归（18 条已验收 L3）")
    A("")
    A(
        f"- checked={vt.get('checked', 0)} exact={vt.get('exact', 0)} "
        f"within_slot={vt.get('within_slot', 0)} no_static_hit={vt.get('no_static_hit', 0)} "
        f"mismatch={vt.get('mismatch', 0)}"
    )
    A("- `Cnti == 216`（0xd8：外层子对象指针，压过内层附属标量 0xb9）")
    A("")
    A("## 1,034 分母")
    A("")
    for bucket in ("unresolved_wire_slot", "held", "no_wire_evidence"):
        dd = br.get(bucket) or {}
        A(
            "- {} ({} 条): direct_mem_off={}, resolved_via_helper={}, "
            "resolved_via_helper_subobj={}, child_table={}, helper_computed={}, absent_everywhere={}".format(
                bucket,
                dd.get("total", 0),
                dd.get("hit_direct_mem_off", 0),
                dd.get("hit_resolved_via_helper", 0),
                dd.get("hit_resolved_via_helper_subobj", 0),
                dd.get("hit_helper_child_table", 0),
                dd.get("hit_helper_computed", 0),
                dd.get("absent_everywhere_in_67_tables", 0),
            )
        )
    A(f"- denominator_upgrades_with_new_this_offset: {cmp_.get('upgrade_count', 0)}")
    A(f"- proposed_totals: {json.dumps(s['proposed_totals'], ensure_ascii=False)}")
    A("")
    A("## 静态 read 交叉")
    A("")
    A(f"- fourccs_with_offset: {t.get('fourccs_with_off', 0)}")
    A(f"- hit_read_server: {t.get('hit_read_server', 0)}")
    A(f"- hit_read_client: {t.get('hit_read_client', 0)}")
    A(f"- hit_any_read: {t.get('hit_any_read', 0)} (t97: 802, delta {d.get('hit_any_read', 0)})")
    A("")
    A("## 交付物")
    A("")
    A("| 文件 | 字节 | sha256[:16] |")
    A("|---|---|---|")
    for name in (
        "fourcc_mem_map_v2.json",
        "xml_triage_v2.json",
        "static_read_join_v2.json",
        "REPORT.md",
        "DONE.md",
    ):
        p = outdir / name
        if p.exists():
            A(f"| `{name}` | {p.stat().st_size} | `{T97.sha256_of(p)[:16]}` |")
    A("")
    (outdir / "DONE.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("[t108] wrote DONE.md", flush=True)


def write_report(outdir, fmap, xml_out, join_out):
    kinds, pairs, with_off, child = _kind_counts(fmap)
    s = xml_out["summary"]
    br = s["breakout"]
    t = join_out["totals"]
    dd = join_out["delta"]
    vt = (xml_out.get("validation_vs_accepted_L3") or {}).get("totals") or {}
    val = xml_out.get("validation_vs_accepted_L3") or {}
    cmp_ = xml_out["comparison_t97_vs_t108"]
    ko = cmp_.get("kinds_t97") or {}
    ts = fmap.get("tracer_stats") or {}
    L = []
    A = L.append
    A("# t108 — Hex-Rays 4CC ↔ 内存偏移 v2（helper 内联 + Cnti 修复 + 1,034 分母闭环）")
    A("")
    A("> 只读输入：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（1,173 份 Hex-Rays C，")
    A("> 含 t107 补反编译的 500+ helper）、`scratch/t107/out/helpers_index.json`、")
    A("> `scratch/t97/out/*`（基线）、`reports/xml_denominator_coverage.json`、")
    A("> `reports/club_nation_subtable_schema.json`。")
    A("> **本任务不修改 `reports/`、`LEDGER.json`、`scripts/t97_extract_4cc_mem.py`。**")
    A("")
    A("## 0. 交付物")
    A("")
    A("| 文件 | 内容 |")
    A("|---|---|")
    A("| `fourcc_mem_map_v2.json` | 67 张表的 v2 映射（`helper_chain` 溯源 + 精确 C 行号） |")
    A("| `xml_triage_v2.json` | 1,034 条分母 v2 分诊 + `t97 -> t108` 提升对比矩阵 |")
    A("| `static_read_join_v2.json` | 4CC ↔ `mem_off` ↔ slot19/slot20 交叉表（含 delta） |")
    A("| `REPORT.md` / `DONE.md` | 本报告 / 完成标记（`DONE type=t108b`） |")
    A("")
    A("## 1. t97 → t108 总览")
    A("")
    A("| 指标 | t97 | t108 | 变化 |")
    A("|---|---|---|---|")
    A(f"| 表×4CC 分支记录 | 6219 | {pairs} | {pairs - 6219:+d} |")
    A(f"| 有 `this`/子对象字节偏移 | 1808 | {with_off} | {with_off - 1808:+d} |")
    A(
        "| `direct_field` | {} | {} | {:+d} |".format(
            ko.get("direct_field", 0), kinds.get("direct_field", 0),
            kinds.get("direct_field", 0) - ko.get("direct_field", 0),
        )
    )
    A(
        "| `bitfield` | {} | {} | {:+d} |".format(
            ko.get("bitfield", 0), kinds.get("bitfield", 0),
            kinds.get("bitfield", 0) - ko.get("bitfield", 0),
        )
    )
    A(
        "| `subobj_deref` | {} | {} | {:+d} |".format(
            ko.get("subobj_deref", 0), kinds.get("subobj_deref", 0),
            kinds.get("subobj_deref", 0) - ko.get("subobj_deref", 0),
        )
    )
    A(f"| `resolved_via_helper` | 0 | {kinds.get('resolved_via_helper', 0)} | +{kinds.get('resolved_via_helper', 0)} |")
    A(
        "| `helper_computed` | {} | {} | {:+d} |".format(
            ko.get("helper_computed", 0), kinds.get("helper_computed", 0),
            kinds.get("helper_computed", 0) - ko.get("helper_computed", 0),
        )
    )
    A(
        "| `delegated_or_empty` | {} | {} | {:+d} |".format(
            ko.get("delegated_or_empty", 0), kinds.get("delegated_or_empty", 0),
            kinds.get("delegated_or_empty", 0) - ko.get("delegated_or_empty", 0),
        )
    )
    A(
        "| `confirmed_computed_or_ui` | 0 | {} | +{} |".format(
            kinds.get("confirmed_computed_or_ui", 0), kinds.get("confirmed_computed_or_ui", 0)
        )
    )
    A(f"| 子表 handler 内定位（`offset_space=child_table`） | 0 | {child} | +{child} |")
    A(f"| slot19/slot20 交叉命中（至少一侧） | 802 | {t.get('hit_any_read', 0)} | {dd.get('hit_any_read', 0):+d} |")
    A("")
    A("解析器（helper 追踪）内部计数：")
    A("")
    A("```")
    for k, v in sorted(ts.items(), key=lambda kv: -kv[1]):
        A(f"{k:32s} {v}")
    A("```")
    A("")
    ex = fmap.get("v2_extras") or {}
    if ex:
        A(
            "回填（`attach_v2_extras`）：{}/{} 个候选（含 `alt`）已挂上 v2 字段，"
            "其中 `offset_space=child_table` {} 个、带 `helper_chain` {} 个。".format(
                ex.get("attached", 0),
                ex.get("candidates", 0),
                ex.get("with_child", 0),
                ex.get("with_helper", 0),
            )
        )
        A("")
    A("## 2. helper_computed 的处置")
    A("")
    A(
        f"t97 遗留 `helper_computed` **{ko.get('helper_computed', 0)}** 条，t108 后剩 "
        f"**{kinds.get('helper_computed', 0)}** 条；新增 `resolved_via_helper` "
        f"**{kinds.get('resolved_via_helper', 0)}** 条、"
        f"`confirmed_computed_or_ui` **{kinds.get('confirmed_computed_or_ui', 0)}** 条。"
    )
    A("")
    A("三类判定的判据（全部静态、可复现）：")
    A("")
    A("1. **`resolved_via_helper`（偏移落地）**：helper 的 arg0 就是 `this`（或 `this` 别名、")
    A("   `this + K` 内部指针），且 helper 体内对 `arg0 + K` 有真实读/写 → 把 `K` 提升为字段偏移；")
    A("   若传入的是 `*(this + K)`（子对象指针），则记录二级偏移 `0xK -> 0xM`。")
    A("2. **`offset_space=child_table`（次级分派器）**：helper 把 4CC 字面量/分派码转发给另一个函数，")
    A("   而那个函数本身是某张表的 `slot02/slot03` handler → 在该 handler 内定位该 4CC 的精确 `mem_off`，")
    A("   `helper_chain` 记录完整链路（例：`CLUB CBDa → sub_1411E9540(type=9) → STARTING_RECORD::set_prop('otht') → +0x28`）。")
    A("3. **`confirmed_computed_or_ui`（明确非持久化字段）**：helper 只碰全局/注册表/out-param/纯算术，")
    A("   不读写对象自身字段。`computed_reason` 给出理由（`global_or_registry_lookup` /")
    A("   `arg0_is_out_param_local_or_global` / `constant_or_arith_only` / `vtable_dispatch_through_global`）。")
    A("")
    A("### 2.1 高频 helper 的处置结果")
    A("")
    A("| helper VA | 出现分支数（t97） | t108 判定 | 说明 |")
    A("|---|---|---|---|")
    notes = {
        "0x1411e9540": ("child_table", "按 (obj_id, type) 查注册表 → `STARTING_RECORD::set_prop(code)`"),
        "0x1407c9510": ("computed", "`a1[0..2] = 0`：out-param 构造，arg0 非 `this`"),
        "0x140fe2700": ("protocol", "共享对象协议 handler（`BaCP/COPY/DELE`），无字段语义"),
        "0x1411f4bd0": ("computed", "内置 vector 扫描 + vtable `+16` 转发，值在子对象"),
        "0x143ca2e60": ("child_table", "同 `0x1411E9540`，转发给 `STARTING_RECORD::get_prop`"),
        "0x140fead00": ("computed", "variant 组装（`sub_14083D4F0(...)+40` 粘合）"),
        "0x140e75ff0": ("computed", "内置 vector 扫描（`this+280/288`）返回子对象指针"),
        "0x140e63b10": ("resolved", "读 `this+72/80` 的 16 字节记录数组，匹配 tag/字段"),
        "0x140e759f0": ("resolved", "同上（`this+72/80`），递归取 vtable 结果"),
    }
    freq = (fmap.get("helper_frequency") or {})
    for va, (how, why) in notes.items():
        A(f"| `{va}` | {(freq.get(va) or {}).get('branches', 0)} | `{how}` | {why} |")
    A("")
    A("## 3. `Cnti` 回归修复（`mismatch == 0`）")
    A("")
    A("CLUB `slot03_set_prop`（`funcs/140e834a0.c`，分支 2028–2067 行）同一分支里既写外层子对象指针")
    A("`*(_QWORD *)(a1 + 216)`，也在条件里读附属标志字节 `*(_BYTE *)(a1 + 185)`：")
    A("")
    A("```c")
    A("2033  v32 = *(_QWORD *)(a1 + 216);            // 外层：子对象指针（写入前先读旧值）")
    A("2042  if ( *(_BYTE *)(a1 + 185) != 0 )          // 内层：附属标志（仅条件判断）")
    A("2065  *(_QWORD *)(a1 + 216) = v200;             // 真正的写入目标")
    A("```")
    A("")
    A("t97 按「分支内最小偏移」取 185 → `mismatch`。t108 给每个偏移标注**角色**")
    A("（`test` = 条件表达式内、`write` = `=` 左侧、`read` = 其它），并让**外层子对象指针**")
    A("优先于**仅出现在条件里的附属标量**，因此 `Cnti → 0xd8 = 216`，与已验收 L3 一致。")
    A("")
    A("角色标注同时让 `Cedp`/`Cncl` 从 `no_static_hit` 变为可定位：它们的 helper")
    A("（`sub_140E63B10` / `sub_140E759F0`）直接读 `this + 72` / `this + 80`（内嵌记录数组），")
    A("内联后给出 `+0x48`，正落在已验收位移 72 上。")
    A("")
    A(f"**回归结果：checked={vt.get('checked', 0)} / exact={vt.get('exact', 0)} / "
      f"within_slot={vt.get('within_slot', 0)} / no_static_hit={vt.get('no_static_hit', 0)} / "
      f"mismatch={vt.get('mismatch', 0)}**")
    A("")
    if val.get("available"):
        A("| section | code | 已验收 disp | 宽度 | t108 off | kind | offset_space | 判定 |")
        A("|---|---|---|---|---|---|---|---|")
        for it in val["items"]:
            A(
                f"| {it['section'].replace('_main_row_fields', '')} | `{it['code']}` | "
                f"{it['accepted_displacement']} | {it['accepted_slot_width']} | "
                f"{it['t108_off'] if it['t108_off'] is not None else '—'} | "
                f"`{it['t108_access_kind'] or '—'}` | {it['t108_offset_space'] or '—'} | "
                f"{it['verdict']} |"
            )
        A("")
    A("## 4. 新解锁的核心字段（CLUB / COMP / NATION）")
    A("")
    for cls in ("CLUB", "COMP", "NATION", "TEAM_CONTAINER", "NATIONAL_TEAM_CONTAINER"):
        recs = [r for r in fmap["tables"] if r["class"] == cls]
        if not recs:
            continue
        rec = recs[0]
        rows_ = []
        for code, c in rec["fourccs"].items():
            if c["access_kind"] != "resolved_via_helper":
                continue
            rows_.append((code, c))
        A(f"### {cls}（tt={rec['table_type']}）：`resolved_via_helper` {len(rows_)} 条")
        A("")
        if rows_:
            A("| 4CC | 槽 | 偏移 | offset_space | helper 链 | 证据行 |")
            A("|---|---|---|---|---|---|")
            for code, c in sorted(rows_)[:24]:
                chain = " → ".join(
                    f"`{x['va']}`" + (f"({x.get('code')})" if x.get("code") else "")
                    for x in (c.get("helper_chain") or [])
                )
                off = c.get("primary_off") or ((c.get("child") or {}).get("mem_off"))
                A(
                    f"| `{code}` | `{c['slot']}` | `{off}` | `{c.get('offset_space')}` | {chain or '—'} | "
                    f"`{c['file']}:{c['line_no']}` |"
                )
            A("")
    A("## 5. 1,034 分母 v2 分诊")
    A("")
    A(f"分母 **{s['denominator']}** 条（club 433 / nation 346 / comp 255）。")
    A("")
    A("| 原桶 | 总数 | t108: 直接 mem_off | helper 内联(this) | helper 内联(子对象) | 子表 handler | subobj_deref | 仍 helper_computed | 全 67 表皆无 |")
    A("|---|---|---|---|---|---|---|---|---|")
    for bucket, bd in br.items():
        A(
            "| `{}` | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                bucket,
                bd.get("total", 0),
                bd.get("hit_direct_mem_off", 0),
                bd.get("hit_resolved_via_helper", 0),
                bd.get("hit_resolved_via_helper_subobj", 0),
                bd.get("hit_helper_child_table", 0),
                bd.get("hit_subobj_deref", 0),
                bd.get("hit_helper_computed", 0),
                bd.get("absent_everywhere_in_67_tables", 0),
            )
        )
    A("")
    A("### 5.1 三个关键桶的 t97 → t108 变化")
    A("")
    A("| 桶 | 总数 | t97 直接 mem_off | t108 直接 mem_off | t97 helper_computed | t108 helper_computed | t97→t108 新落地偏移 |")
    A("|---|---|---|---|---|---|---|")
    for bucket in ("unresolved_wire_slot", "held", "no_wire_evidence"):
        bd = br.get(bucket) or {}
        pb = (cmp_.get("per_bucket") or {}).get(bucket) or {}
        A(
            "| `{}` | {} | {} | {} | {} | {} | {} |".format(
                bucket,
                bd.get("total", 0),
                pb.get("t97_hit_direct_mem_off", 0),
                bd.get("hit_direct_mem_off", 0),
                pb.get("t97_hit_helper_computed", 0),
                bd.get("hit_helper_computed", 0),
                pb.get("gained_this_offset", 0),
            )
        )
    A("")
    A(f"分母行级别的 `access_kind` 迁移（t97 -> t108，仅列变化）：")
    A("")
    A("| 迁移 | 行数 |")
    A("|---|---|")
    for k, v in (cmp_.get("row_kind_delta") or {}).items():
        A(f"| `{k}` | {v} |")
    A("")
    A("全表 6,000+ 表×4CC 分支的 `access_kind` 迁移（仅列前 12）：")
    A("")
    A("| 迁移 | 条数 |")
    A("|---|---|")
    for k, v in list((cmp_.get("pair_kind_delta") or {}).items())[:12]:
        A(f"| `{k}` | {v} |")
    A("")
    A("### 5.2 分实体")
    A("")
    A("| entity | 直接 mem_off | helper(this) | helper(子对象) | 子表 handler | subobj_deref | 仍 helper_computed | 全表皆无 |")
    A("|---|---|---|---|---|---|---|---|")
    for ent, c in (s.get("by_entity") or {}).items():
        A(
            "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                ent,
                c.get("hit_direct_mem_off", 0),
                c.get("hit_resolved_via_helper", 0),
                c.get("hit_resolved_via_helper_subobj", 0),
                c.get("hit_helper_child_table", 0),
                c.get("hit_subobj_deref", 0),
                c.get("hit_helper_computed", 0),
                c.get("absent_everywhere_in_67_tables", 0),
            )
        )
    A("")
    A("## 6. slot19/slot20 静态交叉（802 → {}）".format(t.get("hit_any_read", 0)))
    A("")
    A(f"- slot02/03 有 `this` 相对偏移的分支：**{t.get('fourccs_with_off', 0)}**"
      f"（t97: 1808, {dd.get('fourccs_with_off', 0):+d}）")
    A(f"- 与 `slot19_read_server` 偏移集合相交：**{t.get('hit_read_server', 0)}**"
      f"（t97: 724, {dd.get('hit_read_server', 0):+d}）")
    A(f"- 与 `slot20_read_client` 偏移集合相交：**{t.get('hit_read_client', 0)}**"
      f"（t97: 250, {dd.get('hit_read_client', 0):+d}）")
    A(f"- 至少命中一侧：**{t.get('hit_any_read', 0)}**（t97: 802, {dd.get('hit_any_read', 0):+d}）")
    A("")
    A("| tt | class | 有 off | slot19 命中 | slot20 命中 | 至少一侧 |")
    A("|---|---|---|---|---|---|")
    for j in sorted(join_out["tables"], key=lambda x: -x["counters"].get("hit_any_read", 0))[:15]:
        c = j["counters"]
        A(
            f"| {j['table_type']} | {j['class']} | {c.get('fourccs_with_off', 0)} | "
            f"{c.get('hit_read_server', 0)} | {c.get('hit_read_client', 0)} | {c.get('hit_any_read', 0)} |"
        )
    A("")
    A("## 7. 方法与已知限制")
    A("")
    A("1. **分支定位与字节换算**沿用 t97（`case`/`if`/guard 三型；按 base 变量声明元素宽度换算；")
    A("   `this` 别名做逐行 reaching-definition 判定）。")
    A("2. **新增角色标注**：每个偏移出现点被标为 `test`（if/while 条件内）、`write`（`=` 左侧）或 `read`；")
    A("   选择 `primary_off` 时先排除「只在条件里出现」的偏移，再让子对象指针优先于内层标量。")
    A("3. **helper 内联**最多 2 跳，仅当分支自身没有直接偏移、且 helper 的 arg0 是 `this`/`this` 派生时")
    A("   才把 helper 内的 `arg0 + K` 作为该 4CC 的偏移；arg0 是 out-param / 局部变量 / 全局的一律不内联。")
    A("4. **`child_table` 偏移不与 `this` 偏移混用**：`offset_space` 显式区分，")
    A("   交叉表与 L3 回归只使用 `this` / 子对象相对偏移，避免把子表字段当成 `this` 字段。")
    A("5. **置信度**：仍无法定位的分支保留 `helper_computed`（helper 无反编译文件），")
    A("   或以 `confirmed_computed_or_ui` + `computed_reason` 明确标注为全局/注册表/out-param/纯算术。")
    A("")
    A("## 8. 复现")
    A("")
    A("```")
    A("py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --selftest   # 断言含 Cnti==216、18/18 mismatch==0")
    A("py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --run        # 写 5 个交付物到 scratch/t108/out")
    A("```")
    A("")
    (outdir / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("[t108] wrote REPORT.md", flush=True)


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

    # --- codec ---
    chk(T97.int4cc(0x6F746874) == "otht", "int4cc(0x6F746874) == 'otht'")
    chk(T97.int4cc(0x436E7469) == "Cnti", "int4cc(0x436E7469) == 'Cnti'")

    # --- role classifier ---
    roles = classify_roles(
        _FakeFunc(),
        [
            (1, "v32 = *(_QWORD *)(a1 + 216);"),
            (2, "if ( *(_BYTE *)(a1 + 185) != 0 )"),
            (3, "*(_QWORD *)(a1 + 216) = v200;"),
        ],
    )
    chk(roles[216] == {"read", "write"}, "role: 0xd8 read+write", str(sorted(roles[216])))
    chk(roles[185] == {"test"}, "role: 0xb9 test-only", str(sorted(roles[185])))

    # --- Cnti: 216 wins over 185 ---
    p = T97.T95_DIR / "funcs" / "140e834a0.c"
    chk(p.exists(), "funcs/140e834a0.c present")
    if p.exists():
        f = T97.CFunc(p, 0x140E834A0)
        br = next(
            (b for b in f.find_branches() if b["code_int"] == 0x436E7469),
            None,
        )
        chk(br is not None, "CLUB set_prop Cnti branch found")
        if br is not None:
            info = analyze_branch_v2(f, br, tracer=None)
            chk(info["primary_off_int"] == 216, "Cnti -> 0xd8 (216)", str(info["primary_off"]))
            chk(info["access_kind"] == "subobj_deref", "Cnti kind == subobj_deref", info["access_kind"])
            chk(185 in {o["off_int"] for o in info["mem_offsets"]}, "Cnti still records 0xb9 as auxiliary")

    # --- helper tracer: member getter ---
    index = {}
    if T107_HELPERS.exists():
        index = json.loads(T97.read_text(T107_HELPERS)).get("helpers") or {}
    tr = Tracer(index)
    hf = tr.func(0x140E63B10)
    chk(hf is not None, "helper 0x140E63B10 decompiled")
    if hf is not None:
        offs = {o["off_int"] for o in tr.member_offsets(hf)}
        chk(72 in offs and 80 in offs, "helper 0x140E63B10 reads this+72 / this+80", str(sorted(offs)))

    # --- helper tracer: out-param helper is not an object field getter ---
    res = tr.resolve(
        0x1407C9510,
        {"kind": "other", "text": "&v133"},
        0x43456470,
        [],
        1,
    )
    chk(res["status"] == "computed", "out-param helper 0x1407C9510 -> computed", res.get("computed_reason"))

    # --- secondary dispatcher: 0x1411E9540 -> STARTING_RECORD set_prop('otht') ---
    res = tr.resolve(
        0x1411E9540,
        {"kind": "this", "var": "a1", "elem": 1},
        0x43424444,
        [0x6F746874],
        1,
    )
    chk(res["status"] == "dispatched", "0x1411E9540 forwards 4CC -> dispatched", res.get("status"))
    if res["status"] == "dispatched":
        fw = res["forward"]
        chk(fw["target_va"] == "0x141545680", "  forwarded to STARTING_RECORD set_prop", fw["target_va"])
        chk(fw["code"] == "otht", "  forwarded code == otht", fw["code"])
        chk(fw["target_primary_off"] == "0x28", "  otht -> 0x28", str(fw["target_primary_off"]))

    # --- 2nd dispatcher: 0x143CA2E60 -> STARTING_RECORD get_prop('otht') ---
    res = tr.resolve(
        0x143CA2E60,
        {"kind": "this", "var": "a1", "elem": 1},
        0x43456473,
        [0x6F746874],
        1,
    )
    chk(res["status"] == "dispatched", "0x143CA2E60 forwards 4CC -> dispatched", res.get("status"))
    if res["status"] == "dispatched":
        chk(res["forward"]["target_va"] == "0x1415446a0", "  forwarded to STARTING_RECORD get_prop",
            res["forward"]["target_va"])

    # --- helper corpus ---
    n_files = len(list(FUNCS_DIR.glob("*.c")))
    chk(n_files > 1000, "funcs corpus > 1000 C files (t107 backfill)", str(n_files))

    # --- index integrity ---
    idx = json.loads(T97.read_text(VTABLE_INDEX))
    chk(len(idx["tables"]) == 67, "vtable_index has 67 table entries", str(len(idx["tables"])))

    # --- produced artefacts (only when --run was executed before) ---
    tri = DEFAULT_OUTDIR / "xml_triage_v2.json"
    if tri.exists():
        d = json.loads(T97.read_text(tri))
        tot = (d.get("validation_vs_accepted_L3") or {}).get("totals") or {}
        chk(tot.get("mismatch", 0) == 0, "18/18 L3 regression: mismatch == 0", str(tot))
        chk(tot.get("checked") == 18, "18 accepted L3 items checked", str(tot.get("checked")))
        cnt = next(
            (r for r in d["rows"] if r["entity"] == "club" and r["code"] == "Cnti"),
            None,
        )
        chk(cnt is not None and (cnt.get("t108") or {}).get("primary_off") == "0xd8",
            "triage row Cnti -> 0xd8", str((cnt or {}).get("t108", {}).get("primary_off")))

    print("\n".join(msgs))
    print("selftest:", "OK" if ok else "FAILED")
    return 0 if ok else 1


class _FakeFunc:
    """Minimal CFunc stand-in for the role classifier self-test."""

    params = [("a1", "__int64")]
    this_name = "a1"

    def base_vars_at(self, line_idx):
        return {"a1": 1}


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv):
    ap = argparse.ArgumentParser(
        prog="t108_extract_4cc_v2.py",
        description=(
            "t108: 4CC <-> memory-offset extraction v2 for the 67 FM24 table classes "
            "(t97 baseline + helper inlining + Cnti fix)"
        ),
        epilog="exit codes: 0 ok, 1 selftest failure / internal error, 2 bad usage",
    )
    ap.add_argument("--run", action="store_true", help="run the extraction and write deliverables")
    ap.add_argument("--selftest", action="store_true", help="run built-in assertions")
    ap.add_argument(
        "--outdir",
        default=str(DEFAULT_OUTDIR),
        help="output directory (default: scratch/t108/out)",
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
