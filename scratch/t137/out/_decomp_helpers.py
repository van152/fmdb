"""One-shot idalib decompile of NON_PLAYER attribute-block helpers into scratch/t137/out/ida/."""
import sys, time
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
IDA_LIB = r"C:\Program Files\IDA Professional 9.4\idalib\python"
WORK = ROOT / "scratch/t95/editor_work.i64"
OUT = ROOT / "scratch/t137/out/ida"
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [0x140DC4DB0, 0x140DCA530, 0x140DC4E30, 0x140DC4C90, 0x140DC1D30, 0x140DC40F0]


def main():
    sys.path.insert(0, IDA_LIB)
    import idapro, ida_hexrays, ida_funcs, ida_name, ida_bytes
    rc = idapro.open_database(str(WORK), False)
    if rc:
        print("open_database rc", rc); return 1
    if not ida_hexrays.init_hexrays_plugin():
        print("no hexrays"); return 1
    ok = 0
    for va in TARGETS:
        fs = ida_funcs.get_func(va)
        if not fs:
            print(hex(va), "no func"); continue
        f = va
        try:
            cf = ida_hexrays.decompile(f)
        except Exception as exc:
            print(hex(va), "err", exc); continue
        if cf is None:
            print(hex(va), "None"); continue
        txt = str(cf)
        p = OUT / f"{va - 0x140000000 + 0x140000000:x}.c"
        p = OUT / f"{f:x}.c"
        p.write_text(txt, encoding="utf-8")
        print(hex(va), "->", p.name, txt.count("\n") + 1, "lines")
        ok += 1
    print("ok", ok, f"{time.time()-t0:.1f}s" if (t0 := globals().get("t0", time.time())) else "")
    idapro.close_database(False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
