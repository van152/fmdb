"""t112 exploration — extract linear wire-read program from slot19 C body.

Filters boilerplate (error checks, vector growth) and keeps structural flow:
READ/STRING/IDENTITY ops, if/else conditions, do-while loops, sub calls.
"""
import re
import sys
import pathlib

FUNCS = pathlib.Path(r"D:\tmp2b\fm24-db\scratch\t95\funcs")

BOILER = re.compile(
    r"^\s*(v\d+ = \*a2;|if \( \*\(_DWORD \*\)\(?v\d+ ?\+ 16\)? != 0 \)|return 0;|"
    r"while \( \+\+v\d+ < \(unsigned __int64\)|sub_1407E4490|sub_141758A00|sub_1407E4890|"
    r"v\d+ = a1\[\d+\]|LODWORD|_Interlocked|if \( v\d+ != 0 \)$|"
    r"v\d+ = \(_QWORD \*\)a1\[\d+\]|v26 = |v27 = |v28 = |v29 = |v30 = |v31 = |v59 = )"
)

def load(va: str) -> str:
    for cand in (FUNCS / f"{va}.c", FUNCS / f"{va.lower()}.c"):
        if cand.exists():
            return cand.read_text(encoding="utf-8", errors="replace")
    return f"// MISSING {va}.c"

def get_body(text: str) -> list[str]:
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("{")), 0)
    depth = 0
    body: list[str] = []
    for ln in lines[start:]:
        body.append(ln)
        depth += ln.count("{") - ln.count("}")
        if depth == 0 and len(body) > 1:
            break
    return body

def annotate(va: str, depth: int = 0) -> None:
    text = load(va)
    thunk = re.search(r"->0x([0-9A-Fa-f]{9})\)", text)
    if "thunk" in text and thunk:
        annotate(thunk.group(1).upper(), depth)
        return
    body = get_body(text)
    for ln in body:
        s = ln.strip()
        if not s or s in ("{", "}"):
            print("  " * depth + s)
            continue
        if "sub_140814B10" in s or "sub_14371BDF0" in s:
            print("  " * depth + s + "   <<< STR")
        elif "sub_140FAED40" in s or "sub_143DCB6F0" in s:
            print("  " * depth + s + "   <<< IDENTITY(12B)")
        elif "sub_140FEA0C0" in s:
            print("  " * depth + s + "   <<< U64(uid pair 8B)")
        elif "sub_140DB8980" in s:
            print("  " * depth + s + "   <<< DATE(4B)")
        elif "sub_140DB89D0" in s:
            print("  " * depth + s + "   <<< DATE-WRITE (ignore)")
        elif "+ 40LL))" in s:
            m = re.search(r"\+ 40LL\)\)\([^,]+, ([^,]+), (\d+)\)", s)
            size = m.group(2) if m else "?"
            dst = (m.group(1) if m else s[:40]).strip()
            print("  " * depth + f"READ {size} -> {dst}   | {s[:110]}")
        elif re.match(r"(if|else|do|while|for)\b", s):
            print("  " * depth + s)
        elif re.match(r"sub_[0-9A-F]{9}\(", s):
            m = re.search(r"sub_([0-9A-Fa-f]{9})\(", s)
            print("  " * depth + s + f"   <<< CALL {m.group(1).upper()}")
        elif BOILER.match(ln):
            continue
        else:
            print("  " * depth + ("| " + s[:120]))

def main() -> int:
    for va in sys.argv[1:]:
        print(f"\n########## slot19 {va.upper()} ##########")
        annotate(va.upper())
    return 0

if __name__ == "__main__":
    sys.exit(main())
