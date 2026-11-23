"""t112 exploration — annotate slot19 C decompilations into wire-read programs.

Prints recursive annotated C for a slot19 function so per-table row programs can
be derived and hand-checked against t96c row0_reads.
"""
import re
import sys
import pathlib

FUNCS = pathlib.Path(r"D:\tmp2b\fm24-db\scratch\t95\funcs")
seen: set[str] = set()
out: list[str] = []

VT_CALL = re.compile(r"\(\*\(_QWORD \*\)([A-Za-z0-9_ *()]+?) \+ 40LL\)\)\(([^,]+), ([^,]+), (\w+)\)")

def annotate(text: str) -> str:
    lines = text.splitlines()
    res = []
    for ln in lines:
        tag = ""
        if "sub_140814B10" in ln or "sub_14371BDF0" in ln:
            tag = "  <<< STRING READ (u32 len + bytes)"
        elif "sub_143DCB6F0" in ln or "sub_140FAED40" in ln:
            tag = "  <<< IDENTITY 12B (ordinal,uid,dbid)"
        else:
            m = VT_CALL.search(ln)
            if m:
                tag = f"  <<< READ {m.group(4)} bytes -> {m.group(3).strip()}"
            else:
                m2 = re.search(r"\+ 40LL\)\)", ln)
                if m2 and "40LL" in ln:
                    tag = "  <<< vtable+40 call (size?)"
        res.append(ln + tag)
    return "\n".join(res)

def load(va: str) -> str:
    p = FUNCS / f"{va}.c"
    if not p.exists():
        p = FUNCS / f"{va.lower()}.c"
    if not p.exists():
        return f"// MISSING {va}.c"
    return p.read_text(encoding="utf-8", errors="replace")

def walk(va: str, depth: int = 0, label: str = "") -> None:
    key = va.lower()
    if key in seen or depth > 6:
        out.append(f"{'  '*depth}[skip {va} {label}]")
        return
    seen.add(key)
    text = load(va)
    out.append(f"\n{'='*20} {va} {label} (depth {depth}) {'='*20}")
    out.append(annotate(text))
    # follow sub_ calls
    subs = re.findall(r"sub_([0-9A-Fa-f]{9})\(", text)
    thunk_subs = re.findall(r"jmp:0x[0-9a-f]+->0x([0-9a-f]{9})", text)
    for s in dict.fromkeys(subs + thunk_subs):
        if s.lower() in ("14371bdf0", "143dcb6f0"):
            continue
        walk(s, depth + 1, f"called by {va}")

def main() -> int:
    for va in sys.argv[1:]:
        seen.clear()
        out.clear()
        walk(va.upper(), 0, "slot19")
        print("\n".join(out))
    return 0

if __name__ == "__main__":
    sys.exit(main())
