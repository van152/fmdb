#!/usr/bin/env python3
"""t105 — big-3 table serializer line audit (CLUB / COMP / NATION / NATIONAL_TEAM_CONTAINER).

Parses the Hex-Rays C pseudo-code in ``scratch/t95/funcs/*.c`` (read-only) and
emits, for each of the eight serializers, an ordered list of wire-read steps:

    seq_idx, line_no, read_kind, dst_mem_off, wire_width, version_gate, helper_va

plus a ``needed_helpers`` census of every callee that has no decompiled body in
the t95 corpus (candidates for the next IDA round).

Read kinds
----------
stream_vcall_40 : ``(*(... **)(*(_QWORD *)S + 40LL))(S, dst, width)``
                  -> the raw stream reader, vtable slot 40 (0x28), width literal.
helper_call     : a curated read helper (``sub_140F7EC80`` & friends).  Width is
                  descriptor driven -> reported as ``varlen:<helper_va>``.
loop_vector     : any read nested inside a loop body (vector element read).
base_class_call : tail continuation into the base serializer
                  (TEAM_CONTAINER::read_server / read_client, ENTITY base).

Only the t95 corpus + vtable_index.json are read; nothing under ``reports/`` or
``reports/LEDGER.json`` is touched.

Usage
-----
  py -V:3.12 -I -B scripts/t105_big3_serializers.py
  py -V:3.12 -I -B scripts/t105_big3_serializers.py --selftest
  py -V:3.12 -I -B scripts/t105_big3_serializers.py --out scratch/t105/out

Exit codes: 0 ok, 1 acceptance/selftest failure, 2 usage or missing input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUNCS = ROOT / "scratch/t95/funcs"
VTABLE = ROOT / "scratch/t95/vtable_index.json"
DEFAULT_OUT = ROOT / "scratch/t105/out"

SCHEMA = "t105.big3_serializers.v1"

# ---------------------------------------------------------------- function map
# (class, lane, va, file, vtable slot)
TARGETS = [
    ("CLUB", "server", "0x140e5b1a0", "140e5b1a0.c", 19),
    ("CLUB", "client", "0x140e5cf50", "140e5cf50.c", 20),
    ("COMP", "server", "0x140eb7a00", "140eb7a00.c", 19),
    ("COMP", "client", "0x140eb9000", "140eb9000.c", 20),
    ("NATION", "server", "0x1410404c0", "1410404c0.c", 19),
    ("NATION", "client", "0x143ecb900", "143ecb900.c", 20),
    ("NATIONAL_TEAM_CONTAINER", "server", "0x14105d510", "14105d510.c", 19),
    ("NATIONAL_TEAM_CONTAINER", "client", "0x143ef3bf0", "143ef3bf0.c", 20),
]

# vtable slot 19/20 entry -> decompiled body (thunks are followed by t95)
VTABLE_BODY = {
    "0x141041b30": "0x143ecb900",  # NATION::read_client  (thunk -> body)
    "0x141060660": "0x143ef3bf0",  # NTC::read_client     (thunk -> body)
    "0x143caa6d0": "0x140eb7a00",  # COMP::read_server    (thunk -> body)
}

# ------------------------------------------------------------------- helpers
# read helper families, curated from static disassembly of the thunk targets.
# width is always descriptor driven (``varlen``); the ``slot`` is the reader
# context field that holds the per-field type descriptor.
REF_FIXUP = {
    # helper va -> descriptor slot inside the reader context
    "0x140f7ec80": "desc:arg3",     # -> sub_143D5E790
    "0x140f7f220": "desc:+0x20",    # -> sub_143D60090
    "0x140f7f730": "desc:+0x58",    # -> sub_143D61490
    "0x140f7fc40": "desc:+0x78",    # -> sub_143D61720
    "0x140f7fd40": "desc:+0x80",    # -> sub_143D624C0
    "0x140f7fe40": "desc:+0x90",    # -> sub_143D626C0
    "0x140f80150": "desc:+0xb8",    # -> sub_143D64710
    "0x140f80250": "desc:+0xc0",    # -> sub_143D64820
    "0x140f7ee40": "desc:ref",      # -> sub_143D5EA60
    "0x140f7f320": "desc:+0x30",    # -> sub_143D60660
    "0x140f7f930": "inline",        # fixed-stride ref fixup
    "0x140f7f220": "desc:+0x20",
    "0x140db8980": "desc:+0x18",    # (dest, stream) order
}

# helper va -> (dest_arg_index, stream_arg_index) for helper_call reads
READ_HELPERS = {
    "0x140f7ec80": (1, 0),
    "0x140f7f220": (1, 0),
    "0x140f7f320": (1, 0),
    "0x140f7f730": (1, 0),
    "0x140f7f930": (1, 0),
    "0x140f7fc40": (1, 0),
    "0x140f7fd40": (1, 0),
    "0x140f7fe40": (1, 0),
    "0x140f80150": (1, 0),
    "0x140f80250": (1, 0),
    "0x140f7ee40": (1, 0),
    "0x140db8980": (0, 1),
    "0x140814b10": (2, 0),   # (stream, status, dest)
    "0x140839480": (2, 0),
    "0x140839290": (2, 0),
    "0x14105fa40": (2, 1),   # (status, stream, dest)
    "0x141073d90": (2, 1),
    "0x141074100": (2, 1),
    "0x14104f0b0": (2, 1),
    "0x140eb8850": (2, 1),
    "0x1409fa4b0": (0, 1),   # (obj, stream)
    "0x1409f8630": (0, 1),
    "0x1415cfd70": (0, 1),
    "0x1415cfea0": (0, 1),
    "0x14141d4a0": (0, 1),
    "0x14141d570": (0, 1),
    "0x14144c6a0": (0, 1),
    "0x141571860": (0, 1),
    "0x14155be50": (0, 1),
    "0x14155d840": (0, 1),
    "0x14155e830": (0, 1),
    "0x141060130": (0, 1),
    "0x1410604a0": (0, 1),
    "0x1410605b0": (0, 1),
    "0x141060550": (0, 1),
    "0x140eb5f80": (0, 1),
    "0x141060080": (0, 1),
    "0x140eb89f0": (0, 1),
}

# base serializer continuations (tail calls)
BASE_CALLS = {
    "0x1411d1730": "TEAM_CONTAINER::read_server",
    "0x1411d2f80": "TEAM_CONTAINER::read_client",
    "0x140faed40": "ENTITY::read_core(tt=25/10 passthrough)",
    "0x141041a50": "NATION::post_read_fixup",
}

# coarse role for the needed_helpers census
ROLE_HINTS = [
    ("0x140f7", "stream_read_descriptor"),
    ("0x140814b", "stream_read_helper"),
    ("0x140839", "stream_read_helper"),
    ("0x140db89", "stream_read_ref"),
    ("0x140eb8", "subobject_reader"),
    ("0x140eb5f", "subobject_reader"),
    ("0x1409fa", "subobject_reader"),
    ("0x1409f8", "subobject_reader"),
    ("0x1415cf", "subobject_reader"),
    ("0x14141d", "subobject_reader"),
    ("0x14144c", "subobject_reader"),
    ("0x141571", "subobject_reader"),
    ("0x14155b", "subobject_reader"),
    ("0x14155d", "subobject_reader"),
    ("0x14155e", "subobject_reader"),
    ("0x1410601", "subobject_reader"),
    ("0x1410604", "subobject_reader"),
    ("0x1410605", "subobject_reader"),
    ("0x14105fa", "value_reader"),
    ("0x14105fb", "vector_payload"),
    ("0x14105fc", "vector_payload"),
    ("0x141073d", "stream_read_helper"),
    ("0x1410741", "stream_read_helper"),
    ("0x14104f0", "stream_read_helper"),
    ("0x1410416", "container_resize"),
    ("0x1410418", "container_resize"),
    ("0x1410419", "container_append"),
    ("0x141041a", "post_read_fixup"),
    ("0x141011f", "container_resize"),
    ("0x140cd95", "vector_append"),
    ("0x140893b", "vector_reserve"),
    ("0x14087f5", "vector_append"),
    ("0x1408c97", "vector_append"),
    ("0x140ba1b", "vector_append"),
    ("0x140b247", "free"),
    ("0x141758a", "memmove"),
    ("0x141750c", "alloc"),
    ("0x141750e", "tls_guard"),
    ("0x1417510", "tls_guard"),
    ("0x1412d33", "free"),
    ("0x1412e70", "stream_token"),
    ("0x1407e44", "alloc"),
    ("0x1407e48", "free"),
    ("0x1407e49", "allocator"),
    ("0x1407e53", "pool_create"),
    ("0x1407e58", "pool_alloc"),
    ("0x1407e3e", "pool_init"),
    ("0x1407e3a", "value_reader"),
    ("0x1400526", "assert"),
    ("0x1400568", "lookup"),
    ("0x140057", "lookup"),
    ("0x14007a9", "alloc"),
    ("0x14007ad", "free"),
    ("0x1400870", "flag_check"),
    ("0x14007c9", "ctor"),
    ("0x1400839", "stream_read_helper"),
    ("0x1400", "helper"),
    ("0x14150f6", "stream_read_helper"),
    ("0x14151dc", "stream_read_helper"),
    ("0x14151e1", "stream_read_helper"),
    ("0x1415cf", "subobject_reader"),
    ("0x14157", "subobject_reader"),
    ("0x1415", "subobject_reader"),
    ("0x1412", "runtime"),
    ("0x1413", "runtime"),
    ("0x1414", "runtime"),
    ("0x1417", "runtime"),
    ("0x1408", "runtime"),
    ("0x1409", "subobject_reader"),
    ("0x140e", "class_helper"),
    ("0x140f", "stream_read_helper"),
    ("0x1410", "class_helper"),
    ("0x1411", "class_helper"),
    ("0x143", "class_helper"),
    ("0x14003", "runtime"),
    ("0x1400", "helper"),
    ("0x14", "runtime"),
]

VER_RE = [
    (re.compile(r"\*\(\s*unsigned __int16\s*\*\s*\)\s*\(\s*a4\s*\+\s*1416\s*\)"), "dbver"),
    (re.compile(r"\*\(\s*_WORD\s*\*\s*\)\s*\(\s*a4\s*\+\s*1416\s*\)"), "dbver"),
    (re.compile(r"\(\s*unsigned __int16\s*\)\s*\*\s*\(\s*a4\s*\+\s*1416\s*\)"), "dbver"),
]

ASSIGN_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*([^;]+)$")
VCALL_RE = re.compile(r"\*\s*\(\s*\*[^;]*?\+\s*40(?:LL)?\s*\)")
SUB_RE = re.compile(r"\b(sub_[0-9A-F]{6,9})\s*\(")


def is_vcall40(text: str) -> bool:
    """vtable slot 40 (0x28) stream reader, both textual forms.

    Hex-Rays emits either
        (*(void (__fastcall **)(...))(*(_QWORD *)v122 + 40LL))(v122, dst, w)
        (*(void (__fastcall **)(...))(**a2 + 40))(*a2, dst, w)
    """
    if "40LL))" in text or "40))(" in text:
        return VCALL_RE.search(text) is not None
    return False


def base_ident(expr: str) -> str:
    e = _strip_casts(canon(expr))
    m = re.search(r"([A-Za-z_]\w*)\s*$", e)
    return m.group(1) if m else e


def const_eval(expr: str, env: dict, depth: int = 0):
    """best-effort integer evaluation of a Hex-Rays expression."""
    if depth > 4:
        return None
    e = _strip_casts(canon(expr))
    e = e.replace("LL)", ")").replace("LL", "")
    if re.fullmatch(r"(0x[0-9A-Fa-f]+|\d+)", e):
        return int(e, 0)
    m = re.fullmatch(r"([A-Za-z_]\w*)\s*([+-])\s*(0x[0-9A-Fa-f]+|\d+)", e)
    if m:
        base = const_eval(m.group(1), env, depth + 1)
        if base is None:
            return None
        d = int(m.group(3), 0)
        return base + d if m.group(2) == "+" else base - d
    if re.fullmatch(r"[A-Za-z_]\w*", e) and e in env:
        return const_eval(env[e], env, depth + 1)
    return None


# ----------------------------------------------------------------- utilities
def canon(text: str) -> str:
    """collapse whitespace and drop redundant casts for gate strings."""
    t = re.sub(r"\s+", " ", text).strip()
    return t


def split_args(argtext: str) -> list[str]:
    """split a C argument list at top level commas."""
    out, depth, cur = [], 0, []
    for ch in argtext:
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


def trailing_call_args(stmt: str) -> list[str] | None:
    """return the argument list of the outermost call of the statement.

    Handles both
        (*(...)(*(_QWORD *)v + 40LL))(v, dst, w)
        sub_140F7EC80(a, b, c)
    """
    text = stmt.strip()
    if text.endswith(";"):
        text = text[:-1]
    # find the last top-level '(' that opens the final argument list
    depth = 0
    open_at = None
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                open_at = i  # closing paren of first balanced group
                break
    if open_at is None:
        return None
    # The outermost call: if the statement starts with '(' the callee is a
    # parenthesised vtable expression, so args are in the *second* balanced group.
    if text.startswith("("):
        rest = text[open_at + 1 :]
        # rest == "(args)" possibly followed by nothing
        rest = rest.strip()
        if not rest.startswith("("):
            return None
        depth = 0
        for i, ch in enumerate(rest):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return split_args(rest[1:i])
        return None
    # plain name call
    m = re.match(r"^[A-Za-z_][\w:]*\s*\(", text)
    if not m:
        return None
    inner = text[m.end() - 1 :]
    depth = 0
    for i, ch in enumerate(inner):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return split_args(inner[1:i])
    return None


# ------------------------------------------------------------------- scanner
class Ctx:
    __slots__ = ("kind", "cond", "idx", "parent")

    def __init__(self, kind: str, cond: str, idx: int, parent):
        self.kind = kind
        self.cond = cond
        self.idx = idx
        self.parent = parent


def classify_header(header: str) -> tuple[str, str]:
    h = canon(header)
    if h.startswith("if"):
        m = re.match(r"if\s*\((.*)\)$", h, re.S)
        return "if", (m.group(1).strip() if m else "")
    if h.startswith("else"):
        return "else", ""
    if h.startswith("for"):
        m = re.match(r"for\s*\((.*)\)$", h, re.S)
        return "for", (m.group(1).strip() if m else "")
    if h.startswith("while"):
        m = re.match(r"while\s*\((.*)\)$", h, re.S)
        return "while", (m.group(1).strip() if m else "")
    if h.startswith("do"):
        return "do", ""
    if h.startswith("switch"):
        m = re.match(r"switch\s*\((.*)\)$", h, re.S)
        return "switch", (m.group(1).strip() if m else "")
    if not h:
        return "func", ""
    return "block", h


def parse_c(path: Path) -> dict:
    """returns {signature, params, stackvars, stmts:[{text,line,end_line,ctxs}]}"""
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # body begins at the first line that is exactly '{' after the signature
    body_start = None
    sig_lines = []
    for i, ln in enumerate(raw):
        s = ln.strip()
        if s == "{":
            body_start = i
            break
        if s.startswith("//"):
            continue
        sig_lines.append(ln)
    if body_start is None:
        raise SystemExit(f"t105: no body in {path}")

    sig = " ".join(sig_lines)
    sig = canon(sig)
    sig = re.sub(r"^//.*?attributes.*?", "", sig)

    params = parse_params(sig)
    stackvars, heapvars = parse_locals(raw[body_start:])

    stmts = []
    stack: list[Ctx] = [Ctx("func", "", 0, None)]
    ctx_idx = 1
    buf: list[str] = []
    buf_line = None
    paren = 0
    pending_header = ""
    last_closed_do: Ctx | None = None
    line = body_start + 1
    in_line_comment = False

    def flush_stmt(end_line: int):
        nonlocal buf, buf_line, pending_header, last_closed_do
        text = canon("".join(buf))
        buf = []
        buf_line = None
        if not text:
            return
        if text.startswith("while") and last_closed_do is not None:
            last_closed_do.cond = canon(text)
            last_closed_do = None
            return
        # skip pure declarations (they were parsed separately) - keep them, they
        # never match a read
        stmts.append(
            {
                "text": text,
                "line": buf_line if buf_line is not None else end_line,
                "end_line": end_line,
                "ctxs": list(stack),
            }
        )

    for ln_idx in range(body_start, len(raw)):
        ln = raw[ln_idx]
        ln_no = ln_idx + 1
        i = 0
        while i < len(ln):
            ch = ln[i]
            if in_line_comment:
                break
            if ch == "/" and i + 1 < len(ln) and ln[i + 1] == "/":
                break
            if ch == '"':
                # skip string literal
                j = i + 1
                while j < len(ln) and ln[j] != '"':
                    j += 2 if ln[j] == "\\" else 1
                buf.append(ln[i : j + 1])
                i = j + 1
                continue
            if ch == "{":
                header = canon("".join(buf))
                buf = []
                kind, cond = classify_header(header)
                if header:
                    pending_header = header
                ctx = Ctx(kind, cond, ctx_idx, stack[-1])
                ctx_idx += 1
                stack.append(ctx)
                buf_line = None
                i += 1
                continue
            if ch == "}":
                text = canon("".join(buf))
                buf = []
                if text and not text.startswith("while"):
                    flush_stmt(ln_no)
                popped = stack.pop() if len(stack) > 1 else None
                if popped is not None and popped.kind == "do":
                    last_closed_do = popped
                if len(stack) > 1 and stack[-1].kind in ("if", "else"):
                    pass
                # `} while (...);` tail
                m = re.match(r"\s*while\s*\(", ln[i:])
                if m:
                    # let the normal scan pick the while(...) statement up
                    pass
                i += 1
                continue
            if ch == "(":
                paren += 1
                buf.append(ch)
                i += 1
                continue
            if ch == ")":
                paren = max(0, paren - 1)
                buf.append(ch)
                i += 1
                continue
            if ch == ";":
                if paren == 0:
                    buf.append(ch)
                    if buf_line is None:
                        buf_line = ln_no
                    flush_stmt(ln_no)
                    i += 1
                    continue
                buf.append(ch)
                i += 1
                continue
            if buf_line is None and not ch.isspace():
                buf_line = ln_no
            buf.append(ch)
            i += 1
        # EOL: a header such as `if (...)` stays in buf and is consumed by '{'
    return {
        "signature": sig,
        "params": params,
        "stackvars": stackvars,
        "heapvars": heapvars,
        "stmts": stmts,
    }


def parse_params(sig: str) -> dict:
    """name -> element size in bytes (pointer element / scalar size)."""
    m = re.search(r"\((.*)\)\s*$", sig, re.S)
    if not m:
        return {}
    body = m.group(1)
    params = {}
    for part in split_args(body):
        p = canon(part)
        if not p or p == "void":
            continue
        mm = re.search(r"([A-Za-z_]\w*)\s*$", p)
        if not mm:
            continue
        name = mm.group(1)
        head = p[: mm.start()].strip()
        elem = 8
        check = head + " " + name
        if re.search(r"__int64\s*\*\s*" + name + r"\b", check) or re.search(
            r"_QWORD\s*\*\s*" + name + r"\b", check
        ):
            elem = 8
        elif re.search(r"char\s*\*\s*" + name + r"\b", check) or re.search(
            r"_BYTE\s*\*\s*" + name + r"\b", check
        ):
            elem = 1
        elif re.search(r"int\s*\*\s*" + name + r"\b", check) or re.search(
            r"_DWORD\s*\*\s*" + name + r"\b", check
        ):
            elem = 4
        elif re.search(r"__int16\s*\*\s*" + name + r"\b", check) or re.search(
            r"_WORD\s*\*\s*" + name + r"\b", check
        ):
            elem = 2
        params[name] = elem
    return params


LOCAL_RE = re.compile(r"^\s*([A-Za-z_][\w \t\*]*?)\b(v\d+)\s*;\s*//\s*\[([^\]]+)\]", re.M)


def parse_locals(lines: list[str]) -> tuple[dict, dict]:
    stackvars, heapvars = {}, {}
    text = "\n".join(lines)
    for m in LOCAL_RE.finditer(text):
        decl, name, slot = m.group(1), m.group(2), m.group(3)
        stackvars[name] = {"decl": canon(decl), "slot": canon(slot)}
    return stackvars, heapvars


# ------------------------------------------------------------ dest resolving
def _strip_casts(expr: str) -> str:
    e = expr.strip()
    while True:
        e2 = re.sub(r"^\(\s*(?:unsigned\s+)?(?:__int64|_QWORD|_DWORD|_WORD|_BYTE|int|char|int\*|void\s*\*|__int64\s*\*|_QWORD\s*\*|_DWORD\s*\*)\s*\)", "", e).strip()
        e2 = re.sub(r"^\(\s*(?:unsigned\s+)?(?:__int16|__int8|unsigned\s+int)\s*\)", "", e2).strip()
        if e2 == e:
            return e
        e = e2


def parse_member(expr: str, params: dict, env: dict, depth: int = 0) -> dict | None:
    """Resolve an expression that addresses an object member.

    returns {off, cls, expr} where cls in direct|nested|stack|heap|unknown
    """
    if depth > 6:
        return None
    e = _strip_casts(canon(expr))
    e = e.replace("LL)", ")").replace("LL", "")
    if not e:
        return None

    # stack temp by reference
    m = re.fullmatch(r"&\s*(v\d+)", e)
    if m:
        return {"off": f"stack:{m.group(1)}", "cls": "stack", "expr": m.group(1)}
    m = re.fullmatch(r"(v\d+)", e)
    if m:
        name = m.group(1)
        if name in params:
            pass
        elif name in env:
            return parse_member(env[name], params, env, depth + 1)
        else:
            return {"off": f"stack:{name}", "cls": "stack", "expr": name}

    # nested: *(T *)(*(T *)(base + N) + M)
    m = re.match(
        r"^\*\(\s*\w+\s*\*\s*\)\s*\(\s*(.+?)\s*\+\s*(0x[0-9A-Fa-f]+|\d+)\s*\)$", e
    )
    if m:
        inner = m.group(1).strip()
        delta = int(m.group(2), 0)
        sub = parse_member(inner, params, env, depth + 1)
        if sub and sub["cls"] in ("direct", "nested"):
            return {
                "off": f"{sub['off']}->0x{delta:x}",
                "cls": "nested",
                "expr": e,
            }
        if sub and sub["cls"] == "stack":
            return {"off": f"{sub['off']}->0x{delta:x}", "cls": "nested", "expr": e}
        return {"off": f"?->0x{delta:x}", "cls": "unknown", "expr": e}

    # base + N
    m = re.match(r"^([A-Za-z_]\w*)\s*\+\s*(0x[0-9A-Fa-f]+|\d+)$", e)
    if m:
        name, delta = m.group(1), int(m.group(2), 0)
        if name in env:
            return parse_member(env[name], params, env, depth + 1) if False else _apply_delta(env[name], delta, params, env, depth)
        elem = params.get(name, 1)
        return {"off": f"0x{delta * elem:x}", "cls": "direct", "expr": e}

    # plain identifier that is a heap object
    m = re.fullmatch(r"([A-Za-z_]\w*)", e)
    if m:
        name = m.group(1)
        if name in env:
            return parse_member(env[name], params, env, depth + 1)
        return {"off": "unknown", "cls": "unknown", "expr": e}
    return None


def _apply_delta(base_expr: str, delta: int, params: dict, env: dict, depth: int) -> dict | None:
    base = parse_member(base_expr, params, env, depth + 1)
    if not base:
        return None
    # base may already be an offset string
    off = base["off"]
    m = re.fullmatch(r"0x([0-9A-Fa-f]+)", off)
    if m:
        return {
            "off": f"0x{int(m.group(1), 16) + delta:x}",
            "cls": base["cls"],
            "expr": base_expr,
        }
    return {"off": f"{off}->0x{delta:x}", "cls": "nested", "expr": base_expr}


def canon_gate(cond: str, aliases: dict) -> str:
    t = canon(cond)
    for rx, rep in VER_RE:
        t = rx.sub(rep, t)
    # alias deref: *v13 -> dbver when v13 aliases a4+1416
    for var, target in aliases.items():
        if target == "dbver":
            t = re.sub(r"\*\s*" + re.escape(var) + r"\b", "dbver", t)
        else:
            t = re.sub(r"\b" + re.escape(var) + r"\b", f"({target})", t)
    t = t.replace("(int)", "").replace("(unsigned __int16)", "").replace("(_DWORD)", "")
    t = re.sub(r"\s*([<>=!]=?|&&|\|\|)\s*", r" \1 ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def gate_ver_constraints(gate: str | None) -> list[str]:
    if not gate:
        return []
    out = []
    for m in re.finditer(r"dbver\s*(>=|<=|>|<|==|!=)\s*(0x[0-9A-Fa-f]+|\d+)", gate):
        op, val = m.group(1), m.group(2)
        out.append(f"ver{op}{val.lower() if val.lower().startswith('0x') else val}")
    return out


# ---------------------------------------------------------------- extraction
def extract(fn: dict) -> dict:
    params = fn["params"]
    stackvars = fn["stackvars"]
    stmts = fn["stmts"]
    env: dict[str, str] = {}
    aliases: dict[str, str] = {}

    # ---- pass 0: env bookkeeping (whole-function, program order)
    for st in stmts:
        m = ASSIGN_RE.match(st["text"].rstrip(";"))
        if m:
            lhs, rhs = m.group(1), canon(m.group(2))
            env[lhs] = rhs
            if "1416" in rhs and ("a4" in rhs or "dbver" in rhs):
                aliases[lhs] = "dbver"

    # ---- pass 1: infer the stream variable
    stream_votes: Counter = Counter()
    for st in stmts:
        text = st["text"]
        if is_vcall40(text):
            args = trailing_call_args(text)
            if args:
                stream_votes[base_ident(args[0])] += 1
        else:
            mh = SUB_RE.search(text)
            if mh:
                hv = "0x" + mh.group(1)[4:].lower()
                if hv in READ_HELPERS:
                    di, si = READ_HELPERS[hv]
                    args = trailing_call_args(text)
                    if args and len(args) > si:
                        stream_votes[base_ident(args[si])] += 1
    stream_var = stream_votes.most_common(1)[0][0] if stream_votes else None

    steps = []
    for st in stmts:
        text = st["text"]

        # ---- gate chain from enclosing contexts
        conds = []
        in_loop = None
        for c in st["ctxs"]:
            if c.kind in ("if", "else") and c.cond:
                conds.append(canon_gate(c.cond, aliases))
            elif c.kind == "while" and c.cond and not c.cond.startswith("++"):
                if in_loop is None:
                    in_loop = canon(c.cond)
            elif c.kind == "for" and c.cond:
                if in_loop is None:
                    in_loop = canon(c.cond)
        gate = " && ".join([c for c in conds if c]) or None

        kind = None
        dst = None
        width = None
        width_ev = None
        helper = None
        coalesced = False
        args = None

        if is_vcall40(text):
            args = trailing_call_args(text)
            if args and len(args) >= 2:
                kind = "stream_vcall_40"
                dst = parse_member(args[1], params, env)
                if len(args) >= 3:
                    w = const_eval(args[2], env)
                    if w is not None:
                        width = w
                        width_ev = "literal_arg3" if re.fullmatch(
                            r"(0x[0-9A-Fa-f]+|\d+)", canon(_strip_casts(args[2]))
                        ) else "const_folded_arg3"
                    else:
                        width, coalesced, width_ev = resolve_span_width(env, args[2])
        else:
            mh = SUB_RE.search(text)
            if mh:
                hv = "0x" + mh.group(1)[4:].lower()
                args = trailing_call_args(text)
                if hv in BASE_CALLS:
                    kind = "base_class_call"
                    helper = hv
                    dst = {"off": "n/a", "cls": "none", "expr": ""}
                    width = f"varlen:{hv}"
                    width_ev = "base_serializer"
                elif args:
                    curated = READ_HELPERS.get(hv)
                    has_stream = stream_var is not None and any(
                        base_ident(a) == stream_var for a in args
                    )
                    if curated or (has_stream and hv in REF_FIXUP) or has_stream:
                        kind = "helper_call"
                        helper = hv
                        dst = pick_dest(args, params, env, stream_var)
                        width = f"varlen:{hv}"
                        width_ev = REF_FIXUP.get(hv, "stream_arg")

        if kind is None:
            continue
        if dst is None:
            dst = {"off": "unknown", "cls": "unknown", "expr": ""}
        if in_loop is not None and kind in ("stream_vcall_40", "helper_call"):
            kind = "loop_vector"

        step = {
            "seq_idx": len(steps),
            "line_no": st["line"],
            "end_line_no": st["end_line"],
            "read_kind": kind,
            "dst_mem_off": dst["off"],
            "dst_class": dst["cls"],
            "dst_expr": canon(dst.get("expr") or ""),
            "wire_width": width,
            "width_evidence": width_ev,
            "version_gate": gate,
            "ver_constraints": gate_ver_constraints(gate),
            "loop_guard": in_loop,
            "helper_va": helper,
            "coalesced_span": coalesced,
            "stack_var": None,
            "materialized_to": None,
        }
        if dst["cls"] == "stack":
            step["stack_var"] = dst["off"].split(":", 1)[1]
        steps.append(step)

    # ---- stack-temp materialisation pass
    for i, s in enumerate(steps):
        if not s["stack_var"]:
            continue
        var = s["stack_var"]
        rx_setter = re.compile(
            r"\b(sub_[0-9A-F]{6,9})\s*\(\s*([^,]+?)\s*,\s*\(?(?:unsigned __int8|unsigned int|int|char)?\)?\s*"
            + re.escape(var)
            + r"\s*\)"
        )
        rx_assign = re.compile(
            r"\*\(\s*\w+\s*\*\s*\)\s*\(\s*([^)]+?)\s*\)\s*=\s*" + re.escape(var) + r"\b"
        )
        # statement-level scan right after the read
        cand = None
        for st in stmts:
            if st["line"] < s["line_no"]:
                continue
            if st["line"] > s["end_line_no"] + 40:
                break
            t = st["text"]
            if var not in t:
                continue
            m1 = rx_setter.search(t)
            if m1:
                mem = parse_member(m1.group(2), params, env)
                if mem and mem["off"] not in ("unknown",):
                    cand = {
                        "off": mem["off"],
                        "line_no": st["line"],
                        "via": f"setter:{m1.group(1)}",
                    }
                    break
            m2 = rx_assign.search(t)
            if m2:
                mem = parse_member(m2.group(1), params, env)
                if mem and mem["off"] != "unknown":
                    cand = {"off": mem["off"], "line_no": st["line"], "via": "assign"}
                    break
        if cand:
            s["materialized_to"] = cand
        else:
            # vector count / loop guard?
            for st in stmts:
                if st["line"] < s["line_no"] or st["line"] > s["end_line_no"] + 40:
                    continue
                if re.search(r"(<|<=|>=|>)\s*\(?(?:unsigned __int8|int|char)?\)?\s*" + re.escape(var) + r"\b", st["text"]):
                    s["materialized_to"] = {
                        "off": None,
                        "line_no": st["line"],
                        "via": "vector_count",
                    }
                    break
    return {"steps": steps}


def resolve_span_width(env: dict, wexpr: str) -> tuple[object, bool, str]:
    """width of a deferred / coalesced span flush."""
    w = const_eval(wexpr, env)
    if w is not None:
        return w, True, f"pending_var:{canon(wexpr)}"
    return "varlen:deferred", True, f"pending_var:{canon(wexpr)}"


def pick_dest(args: list[str], params: dict, env: dict, stream_var: str | None):
    """choose the destination member among a helper's arguments."""
    best = None
    for a in args:
        if stream_var is not None and base_ident(a) == stream_var:
            continue
        got = parse_member(a, params, env)
        if not got:
            continue
        if got["cls"] in ("direct", "nested") and got["off"] != "unknown":
            return got
        if best is None and got["cls"] == "stack":
            best = got
    return best


# --------------------------------------------------------------------- stats
def summarize(name: str, steps: list[dict]) -> dict:
    kinds = Counter(s["read_kind"] for s in steps)
    widths = Counter(str(s["wire_width"]) for s in steps)
    fixed = sum(1 for s in steps if isinstance(s["wire_width"], int))
    varlen = len(steps) - fixed
    gates = Counter()
    for s in steps:
        for v in s["ver_constraints"]:
            gates[v] += 1
    offs = OrderedDict()
    for s in steps:
        if s["dst_class"] in ("direct", "nested"):
            offs.setdefault(s["dst_mem_off"], 0)
            offs[s["dst_mem_off"]] += 1
    return {
        "steps": len(steps),
        "by_kind": dict(kinds),
        "fixed_width": fixed,
        "varlen_width": varlen,
        "width_histogram": dict(widths.most_common()),
        "ver_gates": dict(gates.most_common()),
        "distinct_dst_offsets": len(offs),
        "dst_offsets": list(offs)[:400],
        "gated_steps": sum(1 for s in steps if s["version_gate"]),
        "stack_temp_steps": sum(1 for s in steps if s["stack_var"]),
        "coalesced_steps": sum(1 for s in steps if s["coalesced_span"]),
    }


def helper_role(va: str) -> str:
    for pre, role in ROLE_HINTS:
        if va.startswith(pre):
            return role
    return "unknown"


def collect_helpers(all_steps: dict[str, list[dict]]) -> list[dict]:
    cnt = Counter()
    where: dict[str, set] = {}
    for fname, steps in all_steps.items():
        for s in steps:
            hv = s["helper_va"]
            if not hv:
                continue
            cnt[hv] += 1
            where.setdefault(hv, set()).add(fname)
    present = {p.stem for p in FUNCS.glob("*.c")}
    out = []
    for hv, n in cnt.most_common():
        stem = hv[2:]
        out.append(
            {
                "helper_va": hv,
                "calls": n,
                "used_by": sorted(where[hv]),
                "decompiled": stem in present,
                "role": helper_role(hv),
                "file_if_present": f"funcs/{stem}.c" if stem in present else None,
            }
        )
    return out


# --------------------------------------------------------------------- build
def build(outdir: Path) -> dict:
    if not FUNCS.is_dir():
        raise SystemExit(f"t105: missing corpus {FUNCS}")
    functions = {}
    all_steps = {}
    for cls, lane, va, fname, slot in TARGETS:
        path = FUNCS / fname
        if not path.is_file():
            raise SystemExit(f"t105: missing {path}")
        parsed = parse_c(path)
        got = extract(parsed)
        key = f"{cls}::{lane}"
        steps = got["steps"]
        functions[key] = {
            "class": cls,
            "lane": lane,
            "va": va,
            "file": f"funcs/{fname}",
            "vtable_slot": slot,
            "c_lines": len(path.read_text(encoding="utf-8", errors="replace").splitlines()),
            "signature": parsed["signature"],
            "params": parsed["params"],
            "summary": summarize(key, steps),
            "steps": steps,
        }
        all_steps[key] = steps

    needed = collect_helpers(all_steps)
    doc = {
        "schema": SCHEMA,
        "status": "complete",
        "inputs": {
            "vtable_index": "scratch/t95/vtable_index.json",
            "corpus": "scratch/t95/funcs/*.c",
            "functions": len(functions),
        },
        "conventions": {
            "read_kind": {
                "stream_vcall_40": "raw stream reader, vtable slot 40 (0x28)", 
                "helper_call": "descriptor driven helper (width=varlen:<va>)",
                "loop_vector": "read inside a loop body (vector element)",
                "base_class_call": "tail continuation into the base serializer",
            },
            "dst_mem_off": "byte offset from the a1 object base; `0xNN->0xMM` = nested"
            " (member pointer at +0xNN, then +0xMM inside it); `stack:vNN` = stack temp",
            "a4_1416": "db version u16 (0xDC3 = 3523, 0xDC4 = 3524)",
            "a5": "stream flags byte (1/4/8/0x10/0x20)",
            "a6": "client-build flag", 
            "a7": "server-lane flag (a7!=0 -> server-only block)",
        },
        "functions": functions,
        "needed_helpers": needed,
        "totals": {
            "functions": len(functions),
            "steps": sum(len(v) for v in all_steps.values()),
            "fixed_width": sum(
                1 for v in all_steps.values() for s in v if isinstance(s["wire_width"], int)
            ),
            "varlen_width": sum(
                1 for v in all_steps.values() for s in v if not isinstance(s["wire_width"], int)
            ),
            "gated": sum(1 for v in all_steps.values() for s in v if s["version_gate"]),
            "unique_helpers": len(needed),
            "missing_helpers": sum(1 for h in needed if not h["decompiled"]),
        },
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "big3_serializers.json").write_text(
        json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    write_report(outdir, doc)
    return doc


def write_report(outdir: Path, doc: dict) -> None:
    f = doc["functions"]
    t = doc["totals"]
    L = []
    A = L.append
    A("# t105 — 三大主表序列化器逐行审计(`CLUB` / `COMP` / `NATION` / `NATIONAL_TEAM_CONTAINER`)")
    A("")
    A(f"机读产物:`big3_serializers.json`(`status={doc['status']}`,schema `{SCHEMA}`)。")
    A("输入:只读 `scratch/t95/funcs/*.c` + `scratch/t95/vtable_index.json`;未触碰 `reports/` 与 `LEDGER.json`。")
    A("")
    A("## 1. 总览")
    A("")
    A("| 序列化器 | VA | C 行数 | 读取步骤 | 定长 | 变长 | 门控步骤 | 栈临时 | 内联 span | 唯一目标偏移 |")
    A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k, v in f.items():
        s = v["summary"]
        A(
            f"| `{k}` | `{v['va']}` | {v['c_lines']} | {s['steps']} | {s['fixed_width']} | "
            f"{s['varlen_width']} | {s['gated_steps']} | {s['stack_temp_steps']} | "
            f"{s['coalesced_steps']} | {s['distinct_dst_offsets']} |"
        )
    A(
        f"| **合计** | 8 函数 | — | **{t['steps']}** | {t['fixed_width']} | {t['varlen_width']} | "
        f"{t['gated']} | — | — | — |"
    )
    A("")
    A("## 2. 每个序列化器的读取构成")
    A("")
    for k, v in f.items():
        s = v["summary"]
        A(f"### `{k}` — `{v['file']}`(slot {v['vtable_slot']},{v['c_lines']} 行)")
        A("")
        A("```c")
        A(v["signature"][:400])
        A("```")
        A("")
        A("| read_kind | 次数 |")
        A("|---|---:|")
        for kk, n in sorted(s["by_kind"].items(), key=lambda x: -x[1]):
            A(f"| `{kk}` | {n} |")
        A("")
        A("宽度直方图:" + ", ".join(f"`{w}`×{n}" for w, n in s["width_histogram"].items()))
        A("")
        if s["ver_gates"]:
            A("版本门控:" + ", ".join(f"`{g}`×{n}" for g, n in s["ver_gates"].items()))
            A("")
    A("## 3. 版本门控总结")
    A("")
    gates = Counter()
    for v in f.values():
        for g, n in v["summary"]["ver_gates"].items():
            gates[g] += n
    A("版本阈值的唯一来源是 `*(unsigned __int16 *)(a4 + 1416)`(下文记为 `dbver`):")
    A("")
    A("| 门控 | 出现次数(步骤) | 语义 |")
    A("|---|---:|---|")
    semantics = {
        "ver>=0xdc4": "3569+ 新版本专属字段(旧档不读)",
        "ver<=0xdc3": "旧版本(≤3523)专属字段/回填",
        "ver<0xdc4": "旧版本专属",
        "ver>=0xdc3": "边界包含",
        "ver<=0xdec": "COMP 特例:5624449 标记回填",
    }
    for g, n in gates.most_common():
        A(f"| `{g}` | {n} | {semantics.get(g, '版本分支')} |")
    A("")
    A("## 4. `needed_helpers` — 下一轮 IDA 补反编译清单(Top 30)")
    A("")
    nh = doc["needed_helpers"]
    A(f"本轮共记录 {len(nh)} 个被调用的 helper;其中 **{t['missing_helpers']} 个在 `scratch/t95/funcs/` 中没有反编译体**。")
    A("")
    A("| # | helper VA | 调用次数 | 角色推断 | 有反编译 | 调用方 |")
    A("|---:|---|---:|---|---|---|")
    for i, h in enumerate(nh[:30], 1):
        A(
            f"| {i} | `{h['helper_va']}` | {h['calls']} | {h['role']} | "
            f"{'yes' if h['decompiled'] else '**no**'} | {', '.join(h['used_by'])} |"
        )
    A("")
    A("### 已确认的读取 helper 家族(`varlen` 宽度来源)")
    A("")
    A("| helper | 反编译体 | 语义 |")
    A("|---|---|---|")
    fam = [
        ("0x140f7ec80", "sub_143d5e790", "引用字段读取+按 descriptor(第 3 参)解引用"),
        ("0x140f7f220", "sub_143d60090", "引用字段读取,descriptor @ stream+0x20"),
        ("0x140f7f320", "sub_143d60660", "引用字段读取,descriptor @ stream+0x30"),
        ("0x140f7f730", "sub_143d61490", "引用字段读取,descriptor @ stream+0x58"),
        ("0x140f7fc40", "sub_143d61720", "引用字段读取,descriptor @ stream+0x78"),
        ("0x140f7fd40", "sub_143d624c0", "引用字段读取(可选),descriptor @ stream+0x80"),
        ("0x140f7fe40", "sub_143d626c0", "引用字段读取,descriptor @ stream+0x90"),
        ("0x140f80150", "sub_143d64710", "引用字段读取,descriptor @ stream+0xb8"),
        ("0x140f80250", "sub_143d64820", "可空引用字段读取,descriptor @ stream+0xc0"),
        ("0x140f7ee40", "sub_143d5ea60", "引用字段读取(带 type==17 判定)"),
    ]
    for hv, body, note in fam:
        A(f"| `{hv}` | `{body}` | {note} |")
    A("")
    A("## 5. 方法学与口径")
    A("")
    A("- `wire_width` 定长值只来自 vtable slot 40 调用的第 3 个实参(`literal_arg3`);")
    A("  走 descriptor 的 helper 一律记 `varlen:<helper_va>`,不用猜测值填充。")
    A("- 引擎在 `CLUB::read_server` 里把相邻小字段**合并成一次 span 读**(`v123/v124/v125` 三元组 +")
    A("  `(stream, dest)` 双参 flush 调用);这类步骤标 `coalesced_span=true`,宽度取 pending 变量。")
    A("- 栈临时变量(`stack:vNN`)额外做一次具化追踪:`materialized_to` 给出随后写入的成员偏移")
    A("  (`assign` / `setter:<va>` / `vector_count`),用来把计数读与真正的容器成员对齐。")
    A("- `loop_vector` = 该读取步骤位于循环体内(向量元素读);`loop_guard` 给出循环条件。")
    A("- 偏移换算:`a1` 为 `_QWORD *` 时 `a1 + N` 记 `N*8`;带 `(_DWORD)` 强转的按字节;")
    A("  `*(_QWORD *)(a1 + N) + M` 记 `0xN->0xM`(二级间接)。")
    A("")
    (outdir / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_done(outdir: Path, doc: dict) -> None:
    t = doc["totals"]
    f = doc["functions"]
    top = doc["needed_helpers"][:10]
    L = []
    A = L.append
    A("DONE type=t105")
    A("")
    A("三大主表 + NTC 共 8 个序列化器逐行读取步骤已抽取完毕。")
    A("")
    A(f"- 函数: {t['functions']}(`CLUB`/`COMP`/`NATION`/`NATIONAL_TEAM_CONTAINER` × server/client)")
    A(f"- 读取步骤: {t['steps']}(定长 {t['fixed_width']} / 变长 {t['varlen_width']})")
    A(f"- 带版本门控的步骤: {t['gated']}")
    A(f"- 记录 helper: {t['unique_helpers']},其中缺反编译 {t['missing_helpers']}")
    A("")
    A("| 序列化器 | 步骤 | 定长 | 变长 | 门控 |")
    A("|---|---:|---:|---:|---:|")
    for k, v in f.items():
        s = v["summary"]
        A(f"| `{k}` | {s['steps']} | {s['fixed_width']} | {s['varlen_width']} | {s['gated_steps']} |")
    A("")
    A("needed_helpers Top 10:" + ", ".join(f"`{h['helper_va']}`×{h['calls']}" for h in top))
    A("")
    A("交付: `big3_serializers.json`, `REPORT.md`, `DONE.md`(本文件)。")
    (outdir / "DONE.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    fails = []

    def chk(cond, msg):
        if not cond:
            fails.append(msg)

    # --- unit: statement scanner + arg splitter
    chk(split_args("a, b + 1, (c, d)") == ["a", "b + 1", "(c, d)"], "split_args")
    chk(
        trailing_call_args('(*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v122 + 40LL))(v122, a1 + 216, 4)')
        == ["v122", "a1 + 216", "4"],
        "vcall args",
    )
    chk(trailing_call_args("sub_140F7EC80(a3, (_DWORD)a1 + 216, *(_QWORD *)(a3 + 40), a5, 1, 0)")[1]
        == "(_DWORD)a1 + 216", "helper args")

    if not FUNCS.is_dir():
        print("t105 selftest: corpus missing", file=sys.stderr)
        return 2
    out = DEFAULT_OUT / "_selftest"
    doc = build(out)
    F = doc["functions"]

    def steps(key):
        return F[key]["steps"]

    # CLUB client: 5 consecutive u32 lanes at 0xd8..0xf8
    s = steps("CLUB::client")
    chk(len(s) >= 6, "CLUB::client step count")
    head = [x["dst_mem_off"] for x in s[:5]]
    chk(head == ["0xd8", "0xe0", "0xe8", "0xf0", "0xf8"], f"CLUB::client first5 {head}")
    chk(all(x["wire_width"] == 4 for x in s[:5]), "CLUB::client widths")
    chk(all(x["read_kind"] == "stream_vcall_40" for x in s[:5]), "CLUB::client kinds")
    chk(any(x["read_kind"] == "loop_vector" for x in s), "CLUB::client loop_vector present")
    chk(any(x["read_kind"] == "base_class_call" for x in s), "CLUB::client base_class_call present")

    # CLUB server: server-only block gated by a7 != 0, first lane 0xd8
    s = steps("CLUB::server")
    chk(s[0]["dst_mem_off"] == "0xd8", "CLUB::server first dst")
    chk("a7" in (s[0]["version_gate"] or ""), f"CLUB::server first gate {s[0]['version_gate']}")
    chk(any("ver>=0xdc4" in (x["version_gate"] or "") for x in s), "CLUB::server ver gate")
    chk(any(x["stack_var"] for x in s), "CLUB::server stack temps")
    chk(any(x["coalesced_span"] for x in s), "CLUB::server coalesced span")

    # COMP server: 1-byte lanes at 0x15c/0x15d
    s = steps("COMP::server")
    chk(s[0]["dst_mem_off"] == "0x15c" and s[0]["wire_width"] == 1, "COMP::server first")
    chk(s[1]["dst_mem_off"] == "0x15d", "COMP::server second")
    chk(any("ver>=0xdc4" in (x["version_gate"] or "") for x in s), "COMP::server ver gate")

    # COMP client: 8-byte lanes and vector loops
    s = steps("COMP::client")
    chk(s[0]["dst_mem_off"] == "0x58", f"COMP::client first {s[0]['dst_mem_off']}")
    chk(any(x["wire_width"] == 8 for x in s), "COMP::client u64 lanes")

    # NATION server: a1 is _QWORD* -> a1+35 = 0x118, gated by a7
    s = steps("NATION::server")
    chk(s[0]["dst_mem_off"] == "0x118", f"NATION::server first {s[0]['dst_mem_off']}")
    chk(any(x["dst_mem_off"] == "0x188" for x in s), "NATION::server a1+49 -> 0x188")
    chk(any(x["read_kind"] == "base_class_call" for x in s), "NATION::server base call")

    # NTC server: first lane 2 bytes at 0x19c
    s = steps("NTC::server")
    chk(s[0]["dst_mem_off"] == "0x19c" and s[0]["wire_width"] == 2, "NTC::server first")
    chk(sum(1 for x in s if x["read_kind"] == "stream_vcall_40") > 50, "NTC::server vcall volume")
    chk(any(x["dst_mem_off"].startswith("0x170->") for x in s), "NTC::server nested dst")

    # NTC client: vector loops with per-item helper reads
    s = steps("NTC::client")
    chk(len(s) >= 8, "NTC::client steps")
    chk(any(x["read_kind"] == "loop_vector" for x in s), "NTC::client loop_vector")

    # every step well formed
    for k, v in F.items():
        for x in v["steps"]:
            chk(x["read_kind"] in ("stream_vcall_40", "helper_call", "loop_vector", "base_class_call"),
                f"{k} kind {x['read_kind']}")
            chk(x["wire_width"] is not None, f"{k} width None")
            chk(isinstance(x["line_no"], int) and x["line_no"] > 0, f"{k} line")

    # needed helpers
    nh = doc["needed_helpers"]
    chk(len(nh) >= 40, f"needed_helpers too small: {len(nh)}")
    chk(any(h["helper_va"] == "0x140f7ec80" for h in nh), "0x140f7ec80 missing from census")
    chk(all(h["calls"] >= 1 for h in nh), "helper calls")
    chk(doc["status"] == "complete", "status")

    if fails:
        print("t105 selftest FAILED:")
        for x in fails:
            print("  -", x)
        return 1
    print(f"t105 selftest PASS  (functions={doc['totals']['functions']} "
          f"steps={doc['totals']['steps']} helpers={doc['totals']['unique_helpers']})")
    return 0


# ---------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="t105_big3_serializers.py",
        description="Extract ordered wire-read steps from the big-3 table serializers.",
    )
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    ap.add_argument("--selftest", action="store_true", help="run built-in checks and exit")
    ap.add_argument("--json", action="store_true", help="print the JSON document to stdout")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not FUNCS.is_dir():
        print(f"t105: missing corpus {FUNCS}", file=sys.stderr)
        return 2
    out = Path(args.out)
    try:
        doc = build(out)
    except SystemExit as exc:  # missing input
        print(str(exc), file=sys.stderr)
        return 2
    write_done(out, doc)
    t = doc["totals"]
    print(f"t105: {t['functions']} serializers, {t['steps']} read steps "
          f"(fixed {t['fixed_width']} / varlen {t['varlen_width']}), "
          f"{t['gated']} gated, {t['unique_helpers']} helpers "
          f"({t['missing_helpers']} without body)")
    print(f"wrote {out/'big3_serializers.json'}, {out/'REPORT.md'}, {out/'DONE.md'}")
    if args.json:
        print(json.dumps(doc, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
