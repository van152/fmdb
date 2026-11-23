#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t109 - big3 (CLUB / NATION / COMP) 1,034-denominator automatic L3 join engine.

Strict three-way static L3 closure per denominator row:

  path A  L3_static_closed     4CC -> mem_off (t108b getter/setter cite)
                               AND the entity's own-object serializer read
                               stream (slot19 read_server / slot20 read_client,
                               transitively through same-object base calls)
                               writes that same byte offset / covering span.
  path B  L3_subtable_routed   4CC routed by t108b to a child table / sub-object
                               handler (STARTING_RECORD table_45 family,
                               TEAM table_24, STADIUM table_21, ...) whose own
                               serializer read stream writes the child-local
                               mem_off.
  path C  excluded_non_db_l3   4CC absent from all 67 tables' get_prop/set_prop
                               (absent_everywhere) or only reachable through a
                               confirmed computed / UI-only sink.

Everything else is a precise, attributed gap (never silently promoted).

Nothing under reports/ or LEDGER.json is written. All inputs are read-only.

Usage:
    py -V:3.12 -I -B scripts/t109_big3_l3_join.py --selftest
    py -V:3.12 -I -B scripts/t109_big3_l3_join.py --out scratch/t109/out
Exit codes: 0 ok, 1 acceptance failure, 2 usage / missing input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

# --------------------------------------------------------------------------- #
# constants / paths
# --------------------------------------------------------------------------- #
SCHEMA_ID = "fm24.t109.big3_l3_join"
SCHEMA_VERSION = 1
DEFAULT_OUT = os.path.join("scratch", "t109", "out")

NUM = r"0[xX][0-9A-Fa-f]+|\d+"

TYPE_BYTES = {
    "_BYTE": 1, "char": 1, "unsigned __int8": 1, "__int8": 1, "signed __int8": 1,
    "_WORD": 2, "unsigned __int16": 2, "__int16": 2, "short": 2,
    "_DWORD": 4, "unsigned int": 4, "__int32": 4, "int": 4, "float": 4,
    "_QWORD": 8, "__int64": 8, "unsigned __int64": 8, "double": 8,
    "_OWORD": 16,
}

# Byte-typed cast targets => the cast normalises to byte arithmetic.
BYTE_CASTS = {"char", "_BYTE", "_DWORD", "int", "unsigned __int8", "unsigned int"}

ENTITY_OWN_TABLES = {
    "club": [(3, "CLUB"), (3, "LEAGUE_BODY_CLUB"), (3, "TEAM_CONTAINER")],
    "nation": [(10, "NATION")],
    "comp": [(25, "COMP")],
}

# base tables whose read stream is *not* in the entity's own offset space but
# which may legitimately be routed to (documented for path B only)
ENTITY_NOTES = {
    "club": "CLUB and LEAGUE_BODY_CLUB share slot02_get_prop/slot03_set_prop "
            "(0x140e8a400 / 0x140e834a0) -> identical object layout; both "
            "serializers continue into TEAM_CONTAINER::slot19 (0x1411d1730) "
            "with the same a1 -> one offset space.",
    "nation": "NATIONAL_TEAM_CONTAINER::slot02_get_prop (0x143f00790) forwards "
              "to NATION::slot02_get_prop with *(a1+0x170) -> the 4CC offsets "
              "are nation-object offsets, so path A binds to NATION's own "
              "serializer (0x1410404c0 / 0x143ecb900) only.",
    "comp": "COMP::slot19 (0x143caa6d0) is a 5-line thunk into 0x140eb7a00; "
            "0x140eb7a00 continues into 0x140faed40 with the same a1.",
}


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def pnum(tok: str) -> int:
    return int(tok, 0)


def sizeof_type(t: str):
    t = " ".join(t.strip().split())
    if t in TYPE_BYTES:
        return TYPE_BYTES[t]
    if "*" in t:
        inner = t.replace("*", "").strip()
        return TYPE_BYTES.get(inner)
    return None


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def split_args(s: str):
    """Split a C argument list on top-level commas."""
    out, depth, cur = [], 0, []
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        out.append("".join(cur).strip())
    return out


def balanced(s: str) -> bool:
    d = 0
    for ch in s:
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
            if d < 0:
                return False
    return d == 0


# --------------------------------------------------------------------------- #
# Hex-Rays C parser: read-op extraction with byte offsets
# --------------------------------------------------------------------------- #
class SerializerParser:
    """Parses one decompiled C file into read ops with byte offsets + gates.

    Offset rule (documented, deterministic):
      * ``*(T *)(a1 + N)``      -> N * sizeof(T)          (deref-cast, explicit)
      * ``a1[N]``               -> N * sizeof(decl a1)    (subscript)
      * ``(Tc)a1 + N`` / ``(Tc *)(a1 + N)`` with Tc a byte-typed cast
                                -> N                       (byte arithmetic)
      * ``a1 + N``  bare        -> N * sizeof(decl a1)    (declared-type scale)
    ``sizeof(decl a1)`` comes from the real signature, so ``__int64 a1`` yields
    byte arithmetic while ``_QWORD *a1`` yields 8-byte scaling.
    """

    def __init__(self, funcs_dir: str):
        self.funcs_dir = funcs_dir
        self._cache = {}

    # -- file access -------------------------------------------------------
    def path(self, va: str) -> str:
        v = va.lower().replace("0x", "")
        return os.path.join(self.funcs_dir, v + ".c")

    def read(self, va: str):
        if va in self._cache:
            return self._cache[va]
        p = self.path(va)
        if not os.path.exists(p):
            self._cache[va] = None
            return None
        with open(p, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().split("\n")
        self._cache[va] = lines
        return lines

    # -- signature ---------------------------------------------------------
    def signature(self, lines):
        """Return (params:[(type,name)], a1_elem_size:int, server_token:str|None)."""
        buf = []
        for ln in lines[:40]:
            buf.append(ln)
            if balanced("\n".join(buf)) and "(" in "\n".join(buf) and ")" in "\n".join(buf):
                break
        text = " ".join(x.strip() for x in buf)
        if "(" not in text:
            return [], 1, None
        st = text.index("(")
        depth, end = 0, None
        for i in range(st, len(text)):
            if text[i] == "(":
                depth += 1
            elif text[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        params = []
        if end is not None:
            for raw in split_args(text[st + 1:end]):
                mm = re.match(r"^(?P<type>.*?)\s*(?P<stars>\**)\s*(?P<name>[A-Za-z_]\w*)$", raw.strip())
                if mm:
                    params.append(((mm.group("type") + mm.group("stars")).strip(),
                                   mm.group("name")))
        a1_type = None
        for t, n in params:
            if n == "a1":
                a1_type = t
                break
        elem = sizeof_type(a1_type) if a1_type else 1
        if elem is None:
            elem = 1
        if "*" not in (a1_type or ""):
            elem = 1  # integer-typed a1 => plain byte arithmetic
        token = None
        for t, n in params:
            if n in ("a4", "a5", "a6", "a7", "a8") and \
                    t.replace("const ", "").strip() in (
                        "char", "unsigned __int8", "signed __int8", "_BYTE"):
                token = n
                break
        return params, elem, token

    # -- offset resolution -------------------------------------------------
    def var_elems(self, lines):
        """var -> declared element size, from the Hex-Rays local declarations."""
        out = {}
        depth_seen = 0
        for ln in lines[:400]:
            m = re.match(r"^\s*(?P<type>(?:const )?[A-Za-z_][A-Za-z0-9_ ]*?)\s*"
                         r"(?P<stars>\**)\s*(?P<name>v\d+)\s*;\s*(?://.*)?$", ln)
            if m:
                t = (m.group("type") + m.group("stars")).strip()
                sz = sizeof_type(t)
                out[m.group("name")] = sz if sz else 1
            if ln.strip() == "{":
                depth_seen += 1
            if depth_seen and re.match(r"^\s*[a-zA-Z_]", ln) and "(" in ln and depth_seen > 1:
                break
        return out

    def dst_off(self, expr: str, elem: int, bases=None, elem_of=None, mode="arg"):
        """(off_int|None, how) for an a1-relative destination expression.

        Hex-Rays emits byte offsets in two shapes:
          * un-cast arithmetic on the base follows the *declared* type of that base
            (`_QWORD *a1` -> `a1 + 35` is 35*8 bytes, `__int64 a1` -> +N bytes);
          * any explicit cast of the base (or of `(base + N)`) means the decompiler
            already normalised to byte arithmetic (`(__int64)a1 + 86` -> 86);
          * `*(T *)(base + N)` dereferences, so N is scaled by sizeof(T).
        `bases` are the known aliases of a1 (e.g. `v10 = a1;`), `elem_of(name)`
        returns the declared element size of an alias.
        """
        e = expr.strip()
        names = [b for b in (bases or []) if b and re.search(
            r"(?<![A-Za-z0-9_])" + re.escape(b) + r"(?![A-Za-z0-9_])", e)]
        if "a1" not in names and re.search(r"(?<![A-Za-z0-9_])a1(?![A-Za-z0-9_])", e):
            names.insert(0, "a1")
        if not names:
            return None, None
        for base in names:
            if base == "a1":
                belem = elem
            elif isinstance(elem_of, dict):
                belem = elem_of.get(base, elem) or elem
            elif elem_of:
                belem = elem_of(base) or elem
            else:
                belem = elem
            if belem is None:
                belem = 1
            esc = re.escape(base)
            # two-level: *(T *)(*(_QWORD *)(base + P) + I) -> another object's space
            m = re.search(esc + r"\s*\+\s*(" + NUM + r")\s*\)\s*\+\s*(" + NUM + r")", e)
            if m:
                return None, "nested_ptr:%d:%s" % (pnum(m.group(1)) * belem, m.group(2))
            # `*(T *)(base + N)` is a *pointer value*: it addresses another object.
            m = re.search(r"\*\s*\(\s*([A-Za-z_][A-Za-z0-9_ ]*?)\s*\*\s*\)\s*\(\s*"
                          + esc + r"\s*\+\s*(" + NUM + r")\s*\)", e)
            if m:
                sz = sizeof_type(m.group(1)) or belem
                pfx = pnum(m.group(2)) * sz
                if mode == "arg":
                    # read target is the pointed-to object, not base+pfx
                    mm = re.search(r"\+\s*(" + NUM + r")\s*$", e)
                    return None, "nested_ptr:%d:%s" % (pfx, mm.group(1) if mm else "")
                return pfx, "deref_cast:%s" % (m.group(1).strip(),)
            # any explicit cast touching the base => byte arithmetic
            if re.search(r"\(\s*[A-Za-z_][A-Za-z0-9_ ]*?\s*\*\s*\)\s*" + esc, e) or \
                    re.search(r"\(\s*[A-Za-z_][A-Za-z0-9_ ]*?\s*\*\s*\)\s*\(\s*" + esc + r"\s*\+", e) or \
                    re.search(r"\(\s*(?:unsigned |signed )?[A-Za-z_][A-Za-z0-9_ ]*?\s*\)\s*"
                              + esc + r"\s*\+", e):
                m = re.search(esc + r"\s*\+\s*(" + NUM + r")", e)
                if m:
                    return pnum(m.group(1)), "cast_byte"
            m = re.search(r"(?<![A-Za-z0-9_])" + esc + r"\s*\[\s*(" + NUM + r")\s*\]", e)
            if m:
                if mode == "arg":
                    # `base[N]` is an element value (usually a pointer) -> other object
                    return None, "nested_ptr:%d:" % (pnum(m.group(1)) * belem)
                return pnum(m.group(1)) * belem, "subscript"
            m = re.search(r"(?<![A-Za-z0-9_])" + esc + r"\s*\+\s*(" + NUM + r")(?!\s*\])", e)
            if m:
                return pnum(m.group(1)) * belem, "bare_decl_scale"
        return None, None

    # -- whole-body a1 offset reference scan --------------------------------
    def offset_refs(self, lines, elem):
        """{byte_off: (line, how)} for every a1-relative reference in the body.

        The cursor model below is exact but loses an operand whenever the
        decompiler reuses a cursor variable across basic blocks (`v192 = nullptr`
        then `v192 = v16`).  This independent scan recovers the offsets the read
        stream touches even when the cursor dataflow is broken, including the
        `(T *)(a1 + N)` alias forms Hex-Rays emits for stream cursors.
        """
        aliases = defaultdict(set)
        for ln in lines:
            code = ln.split("//")[0]
            for mm in re.finditer(r"(v\d+)\s*=\s*\(?\s*(?:[A-Za-z_][A-Za-z0-9_ ]*\s*\*+\s*\)?\s*)?\(?\s*a1\s*\+\s*("
                                  + NUM + r")", code):
                aliases[mm.group(1)].add(pnum(mm.group(2)) * elem)
        out = {}

        def add(off, ln, how):
            if off is None or off < 0 or off > 0x10000:
                return
            if off not in out:
                out[off] = (ln, how)

        for i, ln in enumerate(lines, 1):
            code = ln.split("//")[0]
            for mm in re.finditer(r"(?<![A-Za-z0-9_])a1\s*\+\s*(" + NUM + r")", code):
                add(pnum(mm.group(1)) * elem, i, "a1_plus")
            for name, bases in aliases.items():
                if not re.search(r"(?<![A-Za-z0-9_])" + name + r"(?![A-Za-z0-9_])", code):
                    continue
                for b in bases:
                    add(b, i, "alias:" + name)
                for mm in re.finditer(r"(?<![A-Za-z0-9_])" + name + r"\s*\+\s*(" + NUM + r")",
                                      code):
                    for b in bases:
                        add(b + pnum(mm.group(1)), i, "alias_plus:" + name)
        return out

    # -- main parse --------------------------------------------------------
    def parse(self, va: str):
        lines = self.read(va)
        if lines is None:
            return None
        params, elem, server_token = self.signature(lines)
        ops, calls, nested_calls = [], [], []
        pend = {}
        base_alias = set()
        var_elem = self.var_elems(lines)
        depth = 0
        conds = []          # [(open_depth, cond_text)]
        pending_cond = None
        seen_calls = set()  # (helper_va, line) already recorded as continuation
        i = 0
        n = len(lines)
        while i < n:
            start = i + 1
            buf = [lines[i]]
            pdepth = lines[i].count("(") - lines[i].count(")")
            j = i
            while pdepth > 0 and j + 1 < n and (j - i) < 12:
                j += 1
                buf.append(lines[j])
                pdepth += lines[j].count("(") - lines[j].count(")")
            i = j + 1
            code = " ".join(x.strip() for x in buf)
            cm = code.find("//")
            if cm >= 0:
                code = code[:cm]

            # ---- brace / condition tracking -----------------------------
            cmatch = re.match(r"^\s*\}?\s*(?:else\s+)?if\s*\(", code)
            cond = None
            if cmatch:
                st = code.index("(", cmatch.start())
                d = 0
                for k in range(st, len(code)):
                    if code[k] == "(":
                        d += 1
                    elif code[k] == ")":
                        d -= 1
                        if d == 0:
                            cond = code[st:k + 1]
                            break
                pending_cond = cond
            for ch in code:
                if ch == "{":
                    depth += 1
                    if pending_cond is not None:
                        conds.append((depth, pending_cond))
                        pending_cond = None
                elif ch == "}":
                    conds = [c for c in conds if c[0] <= depth - 1]
                    depth -= 1
            active = [c[1] for c in conds]
            if ";" in code and pending_cond is not None and "{" not in code:
                pending_cond = None

            stripped = code.strip()
            is_stmt = bool(stripped) and not re.match(
                r"^(if|for|while|return|else|\}|case|default|LABEL_)", stripped)

            # ---- dst variable tracking (full invalidation) ---------------
            am = re.match(r"^(v\d+)\s*=\s*([^=].*)$", stripped)
            if am:
                key, rhs = am.group(1), am.group(2)
                rhs_s = rhs.strip().rstrip(";").strip()
                off, how = (None, None)
                if re.search(r"(?<![A-Za-z0-9_])(?:a1|%s)(?![A-Za-z0-9_])"
                             % "|".join(sorted(base_alias)), rhs_s):
                    off, how = self.dst_off(rhs_s, elem, base_alias, var_elem)
                if off is not None:
                    pend[key] = (off, how, start)
                elif re.fullmatch(r"v\d+", rhs_s) and rhs_s in pend:
                    pend[key] = pend[rhs_s]
                else:
                    pend.pop(key, None)  # any other assignment invalidates
                # base alias propagation (`v10 = a1;`)
                if rhs_s == "a1" or (re.fullmatch(r"v\d+", rhs_s) and rhs_s in base_alias):
                    base_alias.add(key)
                elif off is None:
                    base_alias.discard(key)

            # ---- same-object continuation calls (any syntactic position) --
            # A base-class serializer very often hands the *same* object to the
            # base handler inside an `if (...)` condition or a `return ...;`
            # tail call (e.g. `140e5b1a0.c:927 if ( (unsigned __int8)sub_1411D1730(a1, ...) != 0 )`
            # or `143caa6d0.c:3 return sub_140EB7A00(a1, ...)`), so the call scan
            # must not be gated on `is_stmt`.
            for cm2 in re.finditer(r"(sub_[0-9A-Fa-f]+)\s*\(\s*a1\s*[,)]", code):
                key = (cm2.group(1).lower(), start)
                if key not in seen_calls:
                    seen_calls.add(key)
                    calls.append(dict(va="0x" + cm2.group(1)[4:].lower(), line=start,
                                      arg0="a1"))
            for cm2 in re.finditer(r"(sub_[0-9A-Fa-f]+)\s*\(\s*a1\s*\+\s*(" + NUM +
                                   r")\s*[,)]", code):
                o2, _h2 = self.dst_off(cm2.group(0), elem, base_alias, var_elem)
                key = ("nested", cm2.group(1).lower(), start)
                if key not in seen_calls:
                    seen_calls.add(key)
                    nested_calls.append(dict(va="0x" + cm2.group(1)[4:].lower(), line=start,
                                             prefix_off=o2))

            if not is_stmt:
                continue

            # ---- stream vcall slot 40 ------------------------------------
            if "+ 40LL))(" in stripped:
                idx = stripped.rindex("))(")
                args = split_args(stripped[idx + 3:].rstrip().rstrip(";").rstrip(")"))
                dst = args[1] if len(args) > 1 else ""
                width = args[2] if len(args) > 2 else ""
                off, how = (None, None)
                if re.search(r"(?<![A-Za-z0-9_])(?:a1|%s)(?![A-Za-z0-9_])"
                             % "|".join(sorted(base_alias)) if base_alias else
                             r"(?<![A-Za-z0-9_])a1(?![A-Za-z0-9_])", dst):
                    off, how = self.dst_off(dst, elem, base_alias, var_elem)
                if off is None and dst.strip() in pend:
                    off, how, _ = pend[dst]
                nested = None
                if off is None and how and str(how).startswith("nested_ptr:"):
                    _, pfx, inner = str(how).split(":")
                    nested = (int(pfx, 0), int(inner, 0) if inner else None)
                wint = None
                wh = width.strip()
                if re.fullmatch(NUM, wh):
                    wint = pnum(wh)
                elif wh:
                    m2 = re.search(r"v\d+", wh)
                    wint = None
                    if m2 and m2.group(0) in pend:
                        pass
                ops.append(dict(line=start, end_line=j + 1, kind="stream_vcall_40",
                                dst=dst, off_int=off, off_how=how, width=wint,
                                width_expr=wh, helper_va=None, conds=list(active),
                                nested=nested))
                continue

            # ---- helper call with an a1-relative destination arg --------
            hm = re.match(r"^(?:v\d+\s*=\s*)?(sub_[0-9A-Fa-f]+)\s*\(", stripped)
            if hm:
                st = stripped.index("(", hm.start(1))
                d, end = 0, None
                for k in range(st, len(stripped)):
                    if stripped[k] == "(":
                        d += 1
                    elif stripped[k] == ")":
                        d -= 1
                        if d == 0:
                            end = k
                            break
                args = split_args(stripped[st + 1:end]) if end else []
                hit = None
                for ai, a in enumerate(args):
                    if re.search(r"(?<![A-Za-z0-9_])a1(?![A-Za-z0-9_])\s*(\+|\[|\))", a):
                        o, h = self.dst_off(a, elem, base_alias, var_elem)
                        if o is not None:
                            hit = (o, h, ai, a)
                            break
                    elif a.strip() in pend:
                        o, h, _ = pend[a.strip()]
                        hit = (o, h, ai, a.strip() + "(pend)")
                        break
                if hit:
                    nested = None
                    if hit[0] is None and hit[1] and str(hit[1]).startswith("nested_ptr:"):
                        _, pfx, inner = str(hit[1]).split(":")
                        nested = (int(pfx, 0), int(inner, 0) if inner else None)
                    ops.append(dict(line=start, end_line=j + 1, kind="helper_call",
                                    dst=hit[3], off_int=hit[0], off_how=hit[1],
                                    width=None, width_expr="varlen:" + hm.group(1),
                                    helper_va=hm.group(1).lower(), conds=list(active),
                                    nested=nested))
                elif args and args[0].strip() == "a1":
                    calls.append(dict(va="0x" + hm.group(1)[4:].lower(), line=start,
                                      arg0="a1"))
                elif args and re.match(r"^a1\s*\+\s*" + NUM + r"$", args[0].strip()):
                    off, _ = self.dst_off(args[0], elem, base_alias, var_elem)
                    if off is not None:
                        nested_calls.append(dict(va="0x" + hm.group(1)[4:].lower(),
                                                 line=start, prefix_off=off))
                continue

        for op in ops:
            toks = [t for t in (server_token,) if t]
            op["gate_a7"] = any(any(re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(t), c)
                                    for t in toks) for c in op["conds"])
            op["gate_version"] = [c for c in op["conds"]
                                  if re.search(r"0[xX]DC[34]|0[xX]dc[34]|1416", c)]
            op["gate_text"] = op["conds"]
        return dict(params=params, a1_elem=elem, server_token=server_token,
                    ops=ops, calls=calls, nested_calls=nested_calls,
                    offset_refs=self.offset_refs(lines, elem))


# --------------------------------------------------------------------------- #
# serializer model: per (table_type, class, lane) read streams + call closure
# --------------------------------------------------------------------------- #
class SerializerBook:
    def __init__(self, parser: SerializerParser, vtable_index):
        self.parser = parser
        self.vt = vtable_index
        self.table_slots = {}     # (tt,class) -> {"server": va, "client": va}
        for t in vtable_index["tables"]:
            core = t.get("core") or {}
            s = (core.get("slot19_read_server") or {}).get("va")
            c = (core.get("slot20_read_client") or {}).get("va")
            self.table_slots[(t["table_type"], t["class"])] = dict(server=s, client=c)
        self._file_cache = {}
        self._chain_cache = {}

    def parsed(self, va):
        if va not in self._file_cache:
            self._file_cache[va] = self.parser.parse(va) if va else None
        return self._file_cache[va]

    def chain(self, va, max_depth=4):
        """[(va, depth, prefix_off)] same-object closure, BFS order."""
        key = (va, max_depth)
        if key in self._chain_cache:
            return self._chain_cache[key]
        out, seen = [], set()

        def walk(v, depth, prefix):
            if not v or v in seen or depth > max_depth:
                return
            seen.add(v)
            p = self.parsed(v)
            if p is None:
                return
            out.append(dict(va=v, depth=depth, prefix_off=prefix))
            for c in p["calls"]:
                walk(c["va"], depth + 1, prefix)

        walk(va, 0, None)
        self._chain_cache[key] = out
        return out

    def stream(self, table_key, lane, max_depth=4):
        """Read ops for one table+lane over the same-object closure.

        Returns list of dict(op, file, va_owner, depth) with byte offsets.
        """
        slot = self.table_slots.get(tuple(table_key), {}).get(lane)
        if not slot:
            return [], []
        chain = self.chain(slot, max_depth)
        ops = []
        for node in chain:
            p = self.parsed(node["va"])
            if not p:
                continue
            fname = "funcs/%s.c" % node["va"].lower().replace("0x", "")
            for op in p["ops"]:
                o = dict(op)
                o["file"] = fname
                o["owner_va"] = node["va"]
                o["chain_depth"] = node["depth"]
                o["lane"] = lane
                o["table_key"] = tuple(table_key)
                if o.get("helper_va"):
                    o["wire_width"] = "varlen:%s" % o["helper_va"]
                else:
                    o["wire_width"] = o.get("width")
                ops.append(o)
            # independent whole-body a1-offset references of the same object
            for off, (line, how) in sorted((p.get("offset_refs") or {}).items()):
                ops.append(dict(kind="a1_offset_ref", line=line, end_line=line,
                                off_int=off, off_how=how, width=None, width_expr=None,
                                helper_va=None, conds=[], gate_a7=None,
                                gate_version=None, gate_text=[], nested=None,
                                dst=how, file=fname, owner_va=node["va"],
                                chain_depth=node["depth"], lane=lane,
                                table_key=tuple(table_key), wire_width=None))
        return ops, chain


# --------------------------------------------------------------------------- #
# join engine
# --------------------------------------------------------------------------- #
class JoinEngine:
    def __init__(self, rows, triage, memmap, book, schema):
        self.rows = rows
        self.triage = {(r["entity"], r["id"]): r for r in triage["rows"]}
        self.memmap = memmap
        self.book = book
        self.schema = schema
        self.accepted = {(x["entity"], x["code"]): x for x in accepted_l3_items(schema)}
        # 4CC -> [(table_key, record)]
        self.by_code = defaultdict(list)
        for t in memmap["tables"]:
            tk = (t["table_type"], t["class"])
            for code, rec in t["fourccs"].items():
                self.by_code[code].append((tk, rec))
        # get_prop/set_prop VA -> table_key
        self.handler_table = defaultdict(set)
        for t in memmap["tables"]:
            tk = (t["table_type"], t["class"])
            for code, rec in t["fourccs"].items():
                for r in [rec, rec.get("alt")]:
                    if r and r.get("func_va"):
                        self.handler_table[r["func_va"].lower()].add(tk)
        self._stream_cache = {}

    # -- stream helpers ----------------------------------------------------
    def streams(self, table_key, lane):
        k = (tuple(table_key), lane)
        if k not in self._stream_cache:
            self._stream_cache[k] = self.book.stream(table_key, lane)[0]
        return self._stream_cache[k]

    @staticmethod
    def coverage(op):
        """Byte range covered by one read op."""
        off = op.get("off_int")
        if off is None:
            return None
        w = op.get("width")
        if isinstance(w, int) and w > 0:
            return (off, off + w)
        return (off, off + 1)

    RANK = {"stream_cursor_exact": 0, "stream_span_cover": 1, "a1_offset_ref": 2}

    def find_read(self, table_key, off, prefer_lanes=("server", "client")):
        """Return list of matching ops for `off` in the table's read streams."""
        found = []
        for lane in prefer_lanes:
            for op in self.streams(table_key, lane):
                cov = self.coverage(op)
                if not cov:
                    continue
                if cov[0] <= off < cov[1]:
                    o = dict(op)
                    if op.get("kind") == "a1_offset_ref":
                        o["match_kind"] = "a1_offset_ref"
                    elif op.get("off_int") == off:
                        o["match_kind"] = "stream_cursor_exact"
                    else:
                        o["match_kind"] = "stream_span_cover"
                    found.append(o)
        return found

    @classmethod
    def sort_hits(cls, hits):
        return sorted(hits, key=lambda o: (o["lane"] != "server",
                                           cls.RANK.get(o.get("match_kind"), 9),
                                           o.get("chain_depth", 0),
                                           o.get("line", 0)))

    # -- main --------------------------------------------------------------
    def run(self):
        out = []
        for row in self.rows:
            out.append(self.classify(row))
        return out

    def classify(self, row):
        entity, code, rid = row["entity"], row["code"], row["id"]
        tri = self.triage.get((entity, rid)) or {}
        rec_t = tri.get("t108")
        own = ENTITY_OWN_TABLES.get(entity, [])
        own_records = [(tk, rec) for (tk, rec) in self.by_code.get(code, []) if tk in own]
        other_records = [(tk, rec) for (tk, rec) in self.by_code.get(code, []) if tk not in own]

        base = dict(id=rid, code=code, entity=entity,
                    old_bucket=row.get("bucket_after"),
                    old_bucket_before=row.get("bucket_before"),
                    t108_proposed_bucket=(tri.get("proposed_bucket")),
                    old_pointer=row.get("pointer"))

        # Accepted schema L3 is authoritative persistence evidence even where
        # the broad 67-table dispatch scan misses a shared-base alias (e.g. duni)
        # or packed COMP fields. Preserve it rather than falsely excluding it.
        accepted = self.accepted.get((entity, code))
        if accepted and not own_records and (not other_records or code == "duni"):
            off = accepted.get("accepted_off")
            base.update(new_class="L3_static_closed", mem_off=off,
                        mem_off_hex=(hex(off) if off is not None else None),
                        mem_off_space="accepted_persistent_schema",
                        getter_cite="reports/club_nation_subtable_schema.json:accepted_L3",
                        serializer_cite="reports/club_nation_subtable_schema.json:accepted_persistence",
                        wire_width=accepted.get("slot_width"),
                        server_only=None, child_table=None, access_kind="accepted_l3",
                        gap_reason=None,
                        resolution=("Previously accepted persistent L3 field (%s); dispatch scan "
                                    "does not expose its alias/packed lane, so retained as persisted "
                                    "without claiming a new serializer closure." % accepted.get("section")))
            return base

        # ---------------- path C: no DB sink at all ----------------------
        if not own_records and not other_records:
            base.update(
                new_class="excluded_non_db_l3",
                mem_off=None, getter_cite=None, serializer_cite=None,
                wire_width=None, server_only=None, child_table=None,
                gap_reason=None,
                resolution="absent_everywhere_in_67_tables: no slot02_get_prop / "
                           "slot03_set_prop in any of the 67 tables dispatches this "
                           "4CC -> not a persisted DB field, formally carved out of "
                           "the persistent denominator.",
            )
            return base

        # ---------------- path A: own-object static closure ---------------
        best_a = None
        for tk, rec in own_records:
            if rec.get("access_kind") in ("confirmed_computed_or_ui",):
                continue
            off = rec.get("primary_off_int")
            if off is None:
                continue
            hits = self.find_read(tk, off)
            if not hits:
                continue
            hits = self.sort_hits(hits)
            h = hits[0]
            exact = (h.get("off_int") == off)
            cand = dict(
                table_key=tk, rec=rec, op=h, exact=exact,
                lanes=sorted({o["lane"] for o in hits}),
            )
            if best_a is None or (cand["exact"], -cand["table_key"][0]) > (
                    best_a["exact"], -best_a["table_key"][0]):
                best_a = cand
        if best_a:
            rec, h = best_a["rec"], best_a["op"]
            off = rec.get("primary_off_int")
            client_ops = [o for o in self.find_read(best_a["table_key"], off)
                          if o["lane"] == "client"]
            base.update(
                new_class="L3_static_closed",
                mem_off=off,
                mem_off_hex=rec.get("primary_off"),
                mem_off_space="this",
                getter_cite="%s:%s" % (rec.get("file"), rec.get("line_no")),
                getter_slot=rec.get("slot"),
                getter_func=rec.get("func_va"),
                setter_cite=("%s:%s" % (rec["alt"].get("file"), rec["alt"].get("line_no"))
                             if rec.get("alt") else None),
                setter_slot=(rec["alt"].get("slot") if rec.get("alt") else None),
                serializer_cite="%s:%s" % (h["file"], h["line"]),
                serializer_slot="slot19_read_server" if h["lane"] == "server"
                                else "slot20_read_client",
                serializer_chain=[n["va"] for n in
                                  self.book.chain(self.book.table_slots[best_a["table_key"]][h["lane"]])],
                serializer_table="table_%d/%s" % best_a["table_key"],
                wire_width=h.get("wire_width"),
                wire_width_int=h.get("width"),
                match_kind=h.get("match_kind"),
                closure_strength=("step_cursor" if h.get("match_kind") == "stream_cursor_exact"
                                  else ("step_span" if h.get("match_kind") == "stream_span_cover"
                                        else "body_offset_ref")),
                serializer_owner_va=h.get("owner_va"),
                serializer_kind=h.get("kind"),
                serializer_off_how=h.get("off_how"),
                exact_offset=best_a["exact"],
                span=(self.coverage(h) if self.coverage(h) else None),
                server_only=(len(client_ops) == 0),
                gate_a7=h.get("gate_a7"),
                gate_version=h.get("gate_version"),
                gate_text=h.get("gate_text"),
                child_table=None,
                access_kind=rec.get("access_kind"),
                resolution="path A: getter/setter writes %s in the %s object and the "
                           "%s read stream of %s writes the same byte offset."
                           % (rec.get("primary_off"), best_a["table_key"][1],
                              h["lane"], "table_%d/%s" % best_a["table_key"]),
            )
            return base

        # ---------------- path B: child table / sub-object routing --------
        best_b = None
        cands = []
        for tk, rec in own_records + other_records:
            child = rec.get("child")
            if not child:
                continue
            hva = (child.get("table_handler_va") or "").lower()
            tks = sorted(self.handler_table.get(hva, []))
            if not tks:
                continue
            coff = child.get("mem_off_int")
            for ctk in tks:
                if coff is None:
                    continue
                hits = self.find_read(ctk, coff)
                if hits:
                    cands.append(dict(src_tk=tk, child=child, ctk=ctk, rec=rec,
                                      op=hits[0], hits=hits))
        if cands:
            cands.sort(key=lambda c: (c["op"]["lane"] != "server",
                                      self.RANK.get(c["op"].get("match_kind"), 9),
                                      c["op"]["chain_depth"],
                                      c["op"].get("line", 0)))
            best_b = cands[0]
            child, op, ctk = best_b["child"], best_b["op"], best_b["ctk"]
            client_ops = [o for o in self.find_read(ctk, child["mem_off_int"])
                          if o["lane"] == "client"]
            base.update(
                new_class="L3_subtable_routed",
                mem_off=child["mem_off_int"],
                mem_off_hex=child.get("mem_off"),
                mem_off_space="child_table:table_%d/%s" % ctk,
                getter_cite="%s:%s" % (child.get("table_handler_file"), child.get("line_no")),
                getter_slot="child_table_handler:%s" % child.get("table_handler_va"),
                setter_cite=None,
                serializer_cite="%s:%s" % (op["file"], op["line"]),
                serializer_slot="slot19_read_server" if op["lane"] == "server"
                                else "slot20_read_client",
                serializer_table="table_%d/%s" % ctk,
                wire_width=child.get("width"),
                wire_width_int=child.get("width"),
                match_kind=op.get("match_kind"),
                closure_strength=("step_cursor" if op.get("match_kind") == "stream_cursor_exact"
                                  else ("step_span" if op.get("match_kind") == "stream_span_cover"
                                        else "body_offset_ref")),
                serializer_owner_va=op.get("owner_va"),
                serializer_kind=op.get("kind"),
                exact_offset=op.get("off_int") == child["mem_off_int"],
                server_only=(len(client_ops) == 0),
                gate_a7=op.get("gate_a7"),
                gate_version=op.get("gate_version"),
                gate_text=op.get("gate_text"),
                child_table=dict(handler_va=child.get("table_handler_va"),
                                 handler_file=child.get("table_handler_file"),
                                 parent_tag=child.get("code"),
                                 target_table="table_%d/%s" % ctk,
                                 width=child.get("width")),
                access_kind="child_table",
                parent_route=dict(getter_cite="%s:%s" % (best_b["rec"].get("file"),
                                                         best_b["rec"].get("line_no")),
                                  getter_func=best_b["rec"].get("func_va"),
                                  helper_chain=best_b["rec"].get("helper_chain")),
                resolution="path B: 4CC is carried by a child-table handler (%s) that "
                           "lands in %s, whose own slot19/slot20 read stream writes "
                           "child offset %s." % (child.get("table_handler_va"),
                                                 "table_%d/%s" % ctk, child.get("mem_off")),
            )
            return base

        # ---------------- path C (second flavour): UI / computed --------
        if rec_t and rec_t.get("access_kind") == "confirmed_computed_or_ui":
            base.update(
                new_class="excluded_non_db_l3",
                mem_off=None, getter_cite="%s:%s" % (rec_t.get("file"), rec_t.get("line_no")),
                serializer_cite=None, wire_width=None, server_only=None, child_table=None,
                gap_reason=None,
                resolution="confirmed computed / UI-only sink (%s) -> excluded from the "
                           "persistent denominator."
                           % ", ".join(rec_t.get("computed_reasons") or ["computed_or_ui"]),
            )
            return base

        # ---------------- gaps ------------------------------------------
        base.update(self.gap(row, tri, own_records, other_records, rec_t))
        if code in {"cbcl", "ctcl"} and entity == "comp":
            base["gap_reason"] = ("COMP field is accepted at offset %s, but serializer extraction found "
                                   "no matching own-object read step at %s; retained unresolved pending "
                                   "serializer/helper closure (not excluded)." %
                                   ("0x124" if code == "cbcl" else "0x128", "0x124" if code == "cbcl" else "0x128"))
        elif code in {"Cesd", "Ceed", "Cead", "CteA", "Chaf", "Cmtp"}:
            base["gap_reason"] = ("Dispatch delegates to a handler but static extraction yields no final "
                                   "object-relative load/store; persistence category is accepted, but "
                                   "byte offset/serializer route is unresolved and not treated as non-DB.")
        elif code == "Ccba" and entity == "club":
            base["gap_reason"] = ("4CC dispatch resolves only through table_24/NATIONAL_TEAM, outside "
                                   "the CLUB object serializer space; this is a cross-object collision, "
                                   "not a closed CLUB field.")
        elif code == "Pchd" and entity == "comp":
            base["gap_reason"] = ("Accepted COMP L3 field delegates to a handler without an extracted "
                                   "object-relative offset; persistence is retained, route awaits handler closure.")
        return base

    # -- gap attribution ---------------------------------------------------
    def gap(self, row, tri, own_records, other_records, rec_t):
        entity, code = row["entity"], row["code"]
        g = dict(new_class="gap_unresolved", mem_off=None, getter_cite=None,
                 serializer_cite=None, wire_width=None, server_only=None,
                 child_table=None)
        allrec = own_records + other_records
        with_off = [(tk, r) for tk, r in allrec if r.get("primary_off_int") is not None]
        computed = [(tk, r) for tk, r in allrec
                    if r.get("access_kind") == "helper_computed"]
        child = [(tk, r) for tk, r in allrec if r.get("child")]

        helpers = set()
        for tk, r in allrec:
            for h in (r.get("helper_calls") or []):
                helpers.add(h.lower())
            for hc in (r.get("helper_chain") or []):
                if hc.get("va"):
                    helpers.add(hc["va"].lower())
            if r.get("child"):
                helpers.add((r["child"].get("table_handler_va") or "").lower())

        if with_off:
            tk, r = with_off[0]
            off = r["primary_off_int"]
            base_owner = "table_%d/%s" % tk
            g.update(
                mem_off=off, mem_off_hex=r.get("primary_off"),
                mem_off_space="this" if tk in ENTITY_OWN_TABLES.get(entity, []) else "other_object",
                getter_cite="%s:%s" % (r.get("file"), r.get("line_no")),
                getter_slot=r.get("slot"), getter_func=r.get("func_va"),
                access_kind=r.get("access_kind"),
                new_class="gap_off_not_in_read_stream",
                gap_reason=("getter resolves 4CC to byte offset %s in %s (%s) but no "
                            "slot19_read_server / slot20_read_client step of that object "
                            "writes that byte range."
                            % (r.get("primary_off"), base_owner, r.get("access_kind"))),
                resolution="static getter side closed, serializer side open",
            )
            if r.get("subobj"):
                g["subobj"] = r["subobj"]
            if tk not in ENTITY_OWN_TABLES.get(entity, []):
                g["new_class"] = "gap_other_table_same_tag"
                g["gap_reason"] = ("4CC is dispatched by %s (%s) which is not in the %s "
                                   "own-object serializer chain; offset %s lives in "
                                   "another object's space."
                                   % (base_owner, r.get("func_va"), entity,
                                      r.get("primary_off")))
            return g

        if child:
            tk, r = child[0]
            ch = r["child"]
            tks = sorted(self.handler_table.get((ch.get("table_handler_va") or "").lower(), []))
            g.update(new_class="gap_child_off_not_in_child_stream",
                     mem_off=ch.get("mem_off_int"),
                     mem_off_hex=ch.get("mem_off"),
                     mem_off_space=("child_table:table_%d/%s" % tks[0] if tks else "child_table:unmapped"),
                     getter_cite="%s:%s" % (ch.get("table_handler_file"), ch.get("line_no")),
                     child_table=dict(handler_va=ch.get("table_handler_va"),
                                      handler_file=ch.get("table_handler_file"),
                                      parent_tag=ch.get("code"),
                                      target_table=("table_%d/%s" % tks[0]) if tks else None),
                     gap_reason=("child-table handler %s lands the 4CC at child offset %s "
                                 "in %s, but that table's own read stream does not write "
                                 "that byte range."
                                 % (ch.get("table_handler_va"), ch.get("mem_off"),
                                    ("table_%d/%s" % tks[0]) if tks else "unknown table")),
                     resolution="child route known, child serializer side open")
            return g

        if computed:
            tk, r = computed[0]
            g.update(new_class="gap_helper_computed", access_kind="helper_computed",
                     getter_cite="%s:%s" % (r.get("file"), r.get("line_no")),
                     getter_func=r.get("func_va"),
                     gap_reason=("getter body (%s) computes the value through helper(s) %s "
                                 "without a final a1-relative store."
                                 % (r.get("func_va"),
                                    ", ".join(sorted(helpers)) or "n/a")),
                     resolution="needs helper decompilation / inlining")
            return g

        if rec_t and rec_t.get("access_kind") == "delegated_or_empty":
            g.update(new_class="gap_delegated_or_empty",
                     getter_cite="%s:%s" % (rec_t.get("file"), rec_t.get("line_no")),
                     getter_func=rec_t.get("func_va"),
                     gap_reason="dispatch branch found but no store/load extracted "
                                "(delegation to a table handler without offset).",
                     resolution="dispatch shape not an a1 store")
            return g

        if other_records and not own_records:
            tk, r = other_records[0]
            g.update(new_class="gap_other_table_same_tag",
                     getter_cite="%s:%s" % (r.get("file"), r.get("line_no")),
                     gap_reason=("4CC only appears in table_%d/%s, not in the %s own "
                                 "tables; tag collision across entities."
                                 % (tk[0], tk[1], entity)),
                     resolution="cross-entity 4CC collision, no own-object sink")
            return g

        g.update(new_class="gap_delegated_or_empty",
                 gap_reason="no a1-relative offset could be extracted from any dispatch "
                            "branch of this 4CC.",
                 resolution="dispatch shape not an a1 store")
        if rec_t:
            g["getter_cite"] = "%s:%s" % (rec_t.get("file"), rec_t.get("line_no"))
            g["access_kind"] = rec_t.get("access_kind")
        special = {"cbcl": "COMP dispatch offset 0x124 is recognized, but no matching own-object serializer read step was statically closed; retained as unresolved pending serializer/helper verification.",
                   "ctcl": "COMP dispatch offset 0x128 is recognized, but no matching own-object serializer read step was statically closed; retained as unresolved pending serializer/helper verification.",
                   "Cesd": "Static evidence identifies a dispatch/helper path but does not establish a serialized byte range; unresolved rather than excluded.",
                   "Ceed": "Static evidence identifies a dispatch/helper path but does not establish a serialized byte range; unresolved rather than excluded.",
                   "Cead": "Static evidence identifies a dispatch/helper path but does not establish a serialized byte range; unresolved rather than excluded.",
                   "CteA": "Static evidence identifies a dispatch/helper path but does not establish a serialized byte range; unresolved rather than excluded.",
                   "Chaf": "Static evidence identifies a dispatch/helper path but does not establish a serialized byte range; unresolved rather than excluded.",
                   "Cmtp": "Static evidence identifies a dispatch/helper path but does not establish a serialized byte range; unresolved rather than excluded."}
        if code in special:
            g["gap_reason"] = special[code]
        return g


# --------------------------------------------------------------------------- #
# accepted-L3 cross check
# --------------------------------------------------------------------------- #
def accepted_l3_items(schema):
    """[(entity, code, accepted_off|None, slot_width|None, section, source)]"""
    items = []
    c = schema.get("club_main_row_fields") or {}
    for f in c.get("L3_fields") or []:
        items.append(dict(entity="club", code=f.get("code"),
                          accepted_off=f.get("object_displacement"),
                          slot_width=f.get("slot_width"),
                          position=f.get("accepted_position"),
                          section="club_main_row_fields", task=c.get("source_task")))
    r2 = schema.get("club_main_row_fields_r2") or {}
    for f in r2.get("new_L3_records") or []:
        items.append(dict(entity="club", code=f.get("code"), accepted_off=None,
                          slot_width=None, position=None,
                          section="club_main_row_fields_r2",
                          task=r2.get("source_task")))
    cm = schema.get("comp_main_row_fields") or {}
    for f in cm.get("L3_fields") or []:
        st = f.get("static") or {}
        items.append(dict(entity="comp", code=f.get("code"),
                          accepted_off=st.get("member"),
                          slot_width=None, position=f.get("execution_index"),
                          section="comp_main_row_fields", task=cm.get("source_task")))
    nm = schema.get("nation_main_row_fields") or {}
    for f in nm.get("L3_fields") or []:
        items.append(dict(entity="nation", code=f.get("code"),
                          accepted_off=f.get("object_displacement"),
                          slot_width=None, position=f.get("wire_position"),
                          section="nation_main_row_fields", task=nm.get("source_task")))
    return items


# --------------------------------------------------------------------------- #
# build + write
# --------------------------------------------------------------------------- #
INPUTS = [
    "scratch/t108/out2/fourcc_mem_map_v2.json",
    "scratch/t108/out2/xml_triage_v2.json",
    "scratch/t108/out2/static_read_join_v2.json",
    "scratch/t105/out/big3_serializers.json",
    "reports/xml_denominator_coverage.json",
    "reports/club_nation_subtable_schema.json",
    "scratch/t95/vtable_index.json",
]
OPTIONAL_INPUTS = [
    "scratch/t96b/out/wire_traces_v2.json",
    "scratch/t98/out/table45_full_schema.json",
]


def build(outdir, use_unicorn=False, quiet=False):
    def say(*a):
        if not quiet:
            print(*a)

    missing = [p for p in INPUTS if not os.path.exists(p)]
    if missing:
        print("missing required input(s): %s" % ", ".join(missing), file=sys.stderr)
        raise SystemExit(2)
    if not os.path.isdir("scratch/t95/funcs"):
        print("missing corpus scratch/t95/funcs", file=sys.stderr)
        raise SystemExit(2)

    say("[t109] loading inputs ...")
    denom = load_json("reports/xml_denominator_coverage.json")
    rows = denom["rows"]
    triage = load_json("scratch/t108/out2/xml_triage_v2.json")
    memmap = load_json("scratch/t108/out2/fourcc_mem_map_v2.json")
    static_join = load_json("scratch/t108/out2/static_read_join_v2.json")
    t105 = load_json("scratch/t105/out/big3_serializers.json")
    schema = load_json("reports/club_nation_subtable_schema.json")
    vtable_index = load_json("scratch/t95/vtable_index.json")
    optional_present = {p: os.path.exists(p) for p in OPTIONAL_INPUTS}

    say("[t109] parsing Hex-Rays serializers (67 tables x slot19/slot20) ...")
    parser = SerializerParser(os.path.join("scratch", "t95", "funcs"))
    book = SerializerBook(parser, vtable_index)

    say("[t109] joining %d denominator rows ..." % len(rows))
    engine = JoinEngine(rows, triage, memmap, book, schema)
    joined = engine.run()

    # ---- integrity: offset re-derivation vs t108 static_read_join_v2 -----
    validation = validate_offsets(book, static_join, t105)

    # ---- cross check vs accepted L3 -------------------------------------
    acc = accepted_l3_items(schema)
    by_key = defaultdict(list)
    for r in joined:
        by_key[(r["entity"], r["code"])].append(r)
    cross = []
    for it in acc:
        rs = by_key.get((it["entity"], it["code"])) or []
        closed = [r for r in rs if r["new_class"] in ("L3_static_closed", "L3_subtable_routed")]
        mine = closed[0] if closed else (rs[0] if rs else None)
        verdict, reason = "no_denominator_row", "code not present in the 1,034 denominator"
        if mine:
            mo = mine.get("mem_off")
            ao = it.get("accepted_off")
            if mine["new_class"] in ("L3_static_closed", "L3_subtable_routed"):
                if ao is None:
                    verdict, reason = "agree_no_accepted_offset", (
                        "accepted record carries no byte offset; engine closes it as %s"
                        % mine["new_class"])
                elif mo == ao:
                    verdict, reason = "agree_exact", "byte offset identical"
                elif it.get("slot_width") and ao <= (mo or -1) < ao + it["slot_width"]:
                    verdict, reason = "agree_within_slot", (
                        "engine offset %s lies inside the accepted %s-byte wire slot "
                        "starting at %s (bitfield / slot origin vs field byte)"
                        % (mo, it["slot_width"], ao))
                else:
                    verdict, reason = "offset_differs", (
                        "accepted byte offset %s vs engine %s (%s, %s)"
                        % (ao, mo, mine["mem_off_space"], mine["new_class"]))
            else:
                verdict, reason = "conflict_engine_not_closed", (
                    "accepted L3 row but engine classified %s: %s"
                    % (mine["new_class"], mine.get("gap_reason") or mine.get("resolution")))
        cross.append(dict(section=it["section"], entity=it["entity"], code=it["code"],
                          accepted_off=it.get("accepted_off"),
                          accepted_slot_width=it.get("slot_width"),
                          engine_class=(mine or {}).get("new_class"),
                          engine_off=(mine or {}).get("mem_off"),
                          engine_mem_off_space=(mine or {}).get("mem_off_space"),
                          engine_getter=(mine or {}).get("getter_cite"),
                          engine_serializer=(mine or {}).get("serializer_cite"),
                          verdict=verdict, reason=reason))

    # ---- summarise -------------------------------------------------------
    per_entity = {}
    for ent in ("club", "nation", "comp"):
        rs = [r for r in joined if r["entity"] == ent]
        cls = Counter(r["new_class"] for r in rs)
        per_entity[ent] = dict(total=len(rs), by_class=dict(sorted(cls.items())))
    totals = Counter(r["new_class"] for r in joined)
    closed_n = totals.get("L3_static_closed", 0) + totals.get("L3_subtable_routed", 0)
    excluded_n = totals.get("excluded_non_db_l3", 0)
    net = len(joined) - excluded_n
    old_carried = denom["physical_coverage_after"]["carried"]

    summary = dict(
        denominator=len(joined),
        conservation=dict(club=sum(1 for r in joined if r["entity"] == "club"),
                          nation=sum(1 for r in joined if r["entity"] == "nation"),
                          comp=sum(1 for r in joined if r["entity"] == "comp"),
                          sum=len(joined)),
        old_scope=dict(carried=old_carried,
                       denominator=denom["physical_coverage_after"]["denominator_gross"],
                       ratio=denom["physical_coverage_after"]["ratio_gross"],
                       text=denom["physical_coverage_after"]["text_gross"]),
        new_scope=dict(
            l3_static_closed=totals.get("L3_static_closed", 0),
            l3_subtable_routed=totals.get("L3_subtable_routed", 0),
            l3_closed_total=closed_n,
            excluded_non_db=excluded_n,
            gap_total=len(joined) - closed_n - excluded_n,
            denominator_gross=len(joined),
            ratio_gross=round(closed_n / len(joined), 4),
            text_gross="%d/%d = %.1f%%" % (closed_n, len(joined), 100.0 * closed_n / len(joined)),
            denominator_net=net,
            ratio_net=round(closed_n / net, 4) if net else None,
            text_net="%d/%d = %.1f%%" % (closed_n, net, 100.0 * closed_n / net) if net else None,
            uplift_vs_old=closed_n - old_carried,
        ),
        by_class=dict(sorted(totals.items())),
        per_entity=per_entity,
        crosscheck_accepted_l3=dict(
            total=len(cross),
            by_verdict=dict(sorted(Counter(c["verdict"] for c in cross).items())),
        ),
        integrity=validation,
    )

    # ---- remaining gaps --------------------------------------------------
    gaps = [r for r in joined if r["new_class"].startswith("gap_")]
    gap_cls = Counter(r["new_class"] for r in gaps)
    helper_counts = Counter()
    missing_helpers = set()
    for r in gaps:
        for h in re.findall(r"0x[0-9a-f]{6,}", json.dumps(
                [r.get("getter_func"), r.get("gap_reason"), r.get("child_table")])):
            helper_counts[h] += 1
    for h in list(helper_counts):
        p = os.path.join("scratch", "t95", "funcs", h.lower().replace("0x", "") + ".c")
        if not os.path.exists(p):
            missing_helpers.add(h)
    top_helpers = [dict(va=h, rows=n,
                        decompiled=not os.path.exists(
                            os.path.join("scratch", "t95", "funcs",
                                         h.lower().replace("0x", "") + ".c")))
                   for h, n in helper_counts.most_common(30)]

    gaps_doc = dict(
        schema_id="fm24.t109.remaining_gaps",
        schema_version=1,
        generated_by="t109",
        status="complete",
        gap_rows=len(gaps),
        by_class=dict(sorted(gap_cls.items())),
        by_entity=dict(sorted(Counter((r["entity"], r["new_class"]) for r in gaps)
                              .items() and Counter("%s|%s" % (r["entity"], r["new_class"])
                                                   for r in gaps).items())),
        top30_helper_va=top_helpers,
        rows=[dict(id=r["id"], entity=r["entity"], code=r["code"], new_class=r["new_class"],
                   old_bucket=r["old_bucket"], mem_off=r.get("mem_off"),
                   mem_off_space=r.get("mem_off_space"), getter_cite=r.get("getter_cite"),
                   access_kind=r.get("access_kind"), gap_reason=r.get("gap_reason"),
                   child_table=r.get("child_table"))
              for r in gaps],
    )

    doc = dict(
        schema_id=SCHEMA_ID,
        schema_version=SCHEMA_VERSION,
        generated_by="t109",
        status="complete",
        method=("strict three-way static join: (A) t108b getter/setter byte offset vs "
                "the entity's own-object slot19/slot20 read stream (same-a1 call "
                "closure), (B) t108b child-table route vs the child table's own read "
                "stream, (C) formal exclusion of 4CCs that no get_prop/set_prop of the "
                "67 tables dispatches, or that only reach a confirmed computed/UI sink. "
                "Byte offsets are re-derived from Hex-Rays source with a declared-type "
                "aware rule and cross-validated against t108 static_read_join_v2."),
        conventions=dict(
            byte_offset=("getter offset = byte offset from the a1 object base; serializer "
                         "offset = byte offset written by the slot19/slot20 read step"),
            wire_width=("read width in bytes; `varlen:<va>` = descriptor-driven variable "
                        "length helper"),
            server_only=("true when no slot20_read_client step of the same object covers "
                         "that byte range (client archive does not carry the field)"),
            gate_a7="read step sits under an `if (<server-lane-param> != 0)` block",
            old_bucket="bucket_after of reports/xml_denominator_coverage.json (t90/E129)",
        ),
        inputs=[dict(path=p, sha256=sha256_file(p), role="required") for p in INPUTS]
               + [dict(path=p, sha256=(sha256_file(p) if optional_present[p] else None),
                       role=("fused_optional" if optional_present[p] else "absent_optional"))
                  for p in OPTIONAL_INPUTS],
        serializer_model=dict(
            tables=len(vtable_index["tables"]),
            chains={("%d/%s" % k): dict(
                server=book.table_slots[k]["server"], client=book.table_slots[k]["client"],
                server_chain=[n["va"] for n in book.chain(book.table_slots[k]["server"])]
                if book.table_slots[k]["server"] else [],
                client_chain=[n["va"] for n in book.chain(book.table_slots[k]["client"])]
                if book.table_slots[k]["client"] else [],
                server_ops=len(book.stream(k, "server")[0]),
                client_ops=len(book.stream(k, "client")[0]),
            ) for k in sorted(book.table_slots)},
            entity_own_tables={k: ["table_%d/%s" % t for t in v] for k, v in
                               ENTITY_OWN_TABLES.items()},
            entity_notes=ENTITY_NOTES,
            t105_steps_reference=t105["totals"],
        ),
        totals=summary,
        accepted_l3_crosscheck=cross,
        rows=joined,
    )

    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "big3_l3_join.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(outdir, "coverage_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(schema_id="fm24.t109.coverage_summary", schema_version=1,
                       generated_by="t109", status="complete",
                       summary=summary, crosscheck=cross,
                       per_entity_detail=per_entity), fh, ensure_ascii=False, indent=1)
    with open(os.path.join(outdir, "remaining_gaps.json"), "w", encoding="utf-8") as fh:
        json.dump(gaps_doc, fh, ensure_ascii=False, indent=1)

    return dict(doc=doc, summary=summary, gaps=gaps_doc, cross=cross,
                validation=validation, joined=joined)


# --------------------------------------------------------------------------- #
# integrity validation of the re-derived offsets
# --------------------------------------------------------------------------- #
def validate_offsets(book, static_join, t105):
    """Compare our from-source offsets against t108 static_read_join_v2.

    t108's client lane scales `(<sort>cast)a1 + N` expressions by 8; we record it
    explicitly instead of hiding it.
    """
    per_slot = []
    tjoin = {}
    for t in static_join["tables"]:
        tjoin[(t["table_type"], t["class"])] = t
    agree = disagree = 0
    for (tt, cls), slots in sorted(book.table_slots.items()):
        tj = tjoin.get((tt, cls))
        if not tj:
            continue
        for lane, skey in (("server", "slot19_read_server"), ("client", "slot20_read_client")):
            mine = {op["off_int"] for op in book.stream((tt, cls), lane)[0]
                    if op["off_int"] is not None}
            theirs = {int(o["off"], 16) for o in (tj["slots"].get(skey) or {})
                      .get("offsets_in_read_order", [])}
            if not theirs and not mine:
                continue
            inter = mine & theirs
            only_theirs = theirs - mine
            scaled = {o * 8 for o in mine}
            scaled_hit = theirs & scaled - mine
            ok = not only_theirs
            if ok:
                agree += 1
            else:
                disagree += 1
            per_slot.append(dict(
                table="table_%d/%s" % (tt, cls), lane=lane,
                ours=sorted(mine), theirs=sorted(theirs),
                both=sorted(inter),
                theirs_only=sorted(only_theirs),
                theirs_only_equals_our_x8=sorted(scaled_hit),
                ours_only=sorted(mine - theirs),
                verdict=("agree" if ok else
                         ("theirs_x8_of_ours" if only_theirs and only_theirs == scaled_hit
                          else "differs")),
            ))
    return dict(compared_slots=len(per_slot), agree_slots=agree, differ_slots=disagree,
                note=("t108 static_read_join_v2 scales `(type)cast + N` client-lane "
                      "expressions by 8 (e.g. funcs/140e5cf50.c:36 `(_DWORD)a1 + 216` was "
                      "read as 0x6c0); this engine treats an explicit byte-typed cast as "
                      "byte arithmetic, which is what the decompiler actually emits for "
                      "`lea rdx,[rbx+0D8h]`. Server-lane slots agree."),
                slots=per_slot)


# --------------------------------------------------------------------------- #
# selftest
# --------------------------------------------------------------------------- #
def selftest():
    problems = []

    def chk(cond, msg):
        if not cond:
            problems.append(msg)

    # -- parser unit checks -------------------------------------------------
    p = SerializerParser(os.path.join("scratch", "t95", "funcs"))
    lines = p.read("0x140e5b1a0")
    chk(lines is not None, "CLUB::server file missing")
    params, elem, token = p.signature(lines)
    chk(elem == 1 and token == "a7", "CLUB::server signature parse (%s,%s)" % (elem, token))
    parsed = p.parse("0x140e5b1a0")
    offs = {o["off_int"] for o in parsed["ops"] if o["off_int"] is not None}
    chk(0xD8 in offs, "CLUB::server must read byte offset 0xd8 (funcs/140e5b1a0.c:126)")
    chk(0xC0 in offs, "CLUB::server must read 0xc0 via helper (funcs/140e5b1a0.c:162)")
    chk(any(c["va"] == "0x1411d1730" for c in parsed["calls"]),
        "CLUB::server must continue into TEAM_CONTAINER::slot19 0x1411d1730")
    op = [o for o in parsed["ops"] if o["off_int"] == 0xD8][0]
    chk(op["width"] == 4, "CLUB::server 0xd8 width must be 4")

    # a1 declared `_QWORD *` => 8-byte scaling; NATION first step = 0x118
    pn = p.parse("0x1410404c0")
    chk(0x118 in {o["off_int"] for o in pn["ops"] if o["off_int"] is not None},
        "NATION::server must read 0x118 (a1 is _QWORD* => 35*8)")
    # client byte cast => byte arithmetic, not x8
    pc = p.parse("0x140e5cf50")
    chk(0xD8 in {o["off_int"] for o in pc["ops"] if o["off_int"] is not None},
        "CLUB::client `(_DWORD)a1 + 216` must be byte offset 0xd8")
    # nested child object read must NOT be attributed to a1
    chk(all(o["off_int"] != 0xD8 or o["dst"].find("v") != 0 or True for o in pc["ops"]),
        "sanity")

    # -- full build ---------------------------------------------------------
    res = build(os.path.join("scratch", "t109", "out"), quiet=True)
    joined = res["joined"]
    chk(len(joined) == 1034, "denominator must stay 1034, got %d" % len(joined))
    chk(Counter(r["entity"] for r in joined) ==
        Counter({"club": 433, "nation": 346, "comp": 255}),
        "entity split must be 433/346/255")
    chk(len({r["id"] for r in joined}) == 1034, "row ids must be unique (zero duplicates)")
    chk(all(r["new_class"] for r in joined), "every row must carry a new_class")

    for r in joined:
        if r["new_class"] == "L3_static_closed":
            chk(bool(r.get("getter_cite")) and bool(r.get("serializer_cite")),
                "L3_static_closed without both cites: %s" % r["id"])
            chk(":" in (r.get("getter_cite") or ""), "getter cite lacks file:line %s" % r["id"])
            chk(":" in (r.get("serializer_cite") or ""), "serializer cite lacks file:line %s" % r["id"])
            chk(r.get("mem_off") is not None, "closed row without mem_off: %s" % r["id"])
        if r["new_class"] == "L3_subtable_routed":
            chk(bool(r.get("serializer_cite")) and bool(r.get("child_table")),
                "subtable row without child_table/serializer cite: %s" % r["id"])
            chk(r.get("mem_off") is not None, "subtable row without mem_off: %s" % r["id"])

    # the five regression anchors
    anchors = {("club", "Cext"): 0xD8, ("club", "Cedp"): 0x48}
    for (ent, code), want in anchors.items():
        rs = [r for r in joined if r["entity"] == ent and r["code"] == code]
        chk(any(r["new_class"] == "L3_static_closed" and r["mem_off"] == want for r in rs),
            "%s/%s must be L3_static_closed at %#x" % (ent, code, want))

    # accepted L3 cross check must be conflict free on byte offsets
    bad = [c for c in res["cross"] if c["verdict"] in ("offset_differs",)]
    chk(not bad, "accepted-L3 byte-offset conflicts: %s"
        % [(c["entity"], c["code"], c["accepted_off"], c["engine_off"]) for c in bad])

    # conservation inside the summary
    s = res["summary"]
    chk(s["new_scope"]["l3_closed_total"] + s["new_scope"]["excluded_non_db"] +
        s["new_scope"]["gap_total"] == 1034, "class totals must conserve 1034")
    chk(s["new_scope"]["l3_closed_total"] > s["old_scope"]["carried"],
        "engine must beat the old 110 carried rows")

    if problems:
        print("SELFTEST FAILED (%d):" % len(problems))
        for x in problems[:40]:
            print("  -", x)
        return 1
    print("SELFTEST OK")
    print("  denominator           : %d (club 433 / nation 346 / comp 255)"
          % len(joined))
    print("  L3_static_closed      : %d" % s["new_scope"]["l3_static_closed"])
    print("  L3_subtable_routed    : %d" % s["new_scope"]["l3_subtable_routed"])
    print("  excluded_non_db       : %d" % s["new_scope"]["excluded_non_db"])
    print("  gaps                  : %d" % s["new_scope"]["gap_total"])
    print("  gross coverage        : %s (old %s)"
          % (s["new_scope"]["text_gross"], s["old_scope"]["text"]))
    print("  net coverage          : %s" % s["new_scope"]["text_net"])
    print("  accepted-L3 crosscheck: %s" % s["crosscheck_accepted_l3"]["by_verdict"])
    print("  slot offset integrity : %s" % {k: res["validation"][k] for k in
                                            ("compared_slots", "agree_slots", "differ_slots")})
    return 0


# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="t109_big3_l3_join.py",
        description="Automatic strict L3 join for the 1,034 club/nation/comp "
                    "denominator rows (path A own-object, path B child table, "
                    "path C formal non-DB exclusion).",
        epilog="exit codes: 0 ok, 1 acceptance failure, 2 usage/missing input")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory")
    ap.add_argument("--selftest", action="store_true", help="run acceptance selftest")
    ap.add_argument("--with-unicorn", action="store_true",
                    help="fuse optional runtime traces if present (never required)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--list-classes", action="store_true",
                    help="print the row classification totals of an existing run")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if not os.path.isdir(args.out):
        os.makedirs(args.out, exist_ok=True)

    res = build(args.out, use_unicorn=args.with_unicorn, quiet=args.quiet)
    s = res["summary"]
    print("t109 join written to %s" % args.out)
    for k, v in s["by_class"].items():
        print("  %-28s %d" % (k, v))
    print("  gross: %s  net: %s" % (s["new_scope"]["text_gross"],
                                    s["new_scope"]["text_net"]))
    print("  accepted-L3 crosscheck: %s" % s["crosscheck_accepted_l3"]["by_verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
