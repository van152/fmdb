"""server/t24 A/B: original 5 dbctx globals vs expanded 20."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t111_unicorn_last11 as T
from diff_t3 import load_specific

tabs = load_specific([("server", 24)])
p = tabs[("server", 24)]
footer = len(p) - 9
nrows = struct.unpack_from("<I", p, 8)[0]
print(f"t24 rows={nrows} footer={footer}")

OLD = [0x141B5FDC8, 0x141B5FDD0, 0x141B5FE00, 0x141B5FE10, 0x141BF7E10]

for name, globs in (("old5", OLD), ("new20", T.DBCTX_GLOBALS)):
    ut, emu, db_a3 = T.setup_emulator_v2()
    for g in T.DBCTX_GLOBALS:  # setup writes all 20; overwrite per variant
        pass
    for g in OLD + [x for x in T.DBCTX_GLOBALS if x not in globs]:
        val = db_a3 if g in globs else 0
        emu.mu.mem_write(g, struct.pack("<Q", val))
    T.set_version_globals(emu, 0x0DF1)
    pos = 13
    err = None
    n = 0
    for r in range(8):
        flag = p[pos]; pos += 1
        obj, vt, s19 = T.construct_v2(ut, emu, 24, flag)
        res = T.run_row_v2(ut, emu, obj, s19, p[pos:footer], 0x0DF1, 1)
        if not res["ok"]:
            err = f"row{r} flag={flag:#x} cons={res['bytes_consumed']} rip={res['end_rip']} err={str(res['error'])[:60]}"
            break
        pos += res["bytes_consumed"]
        n += 1
    print(f"{name:6s}: rows_ok={n} :: {err}", flush=True)
