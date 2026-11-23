"""server/t3: try R6-style config variants on row 20."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t111_unicorn_last11 as T
from diff_t3 import load_specific

tabs = load_specific([("server", 3)])
p = tabs[("server", 3)]
footer = len(p) - 9

variants = [
    ("base", 0, {}),
    ("globals", 0, {0x141B60352: 1, 0x141B5FC2C: 1, 0x141B55C2C: 1}),
    ("streambit2", 2, {}),
    ("both", 2, {0x141B60352: 1, 0x141B5FC2C: 1, 0x141B55C2C: 1}),
]
for name, sf, eg in variants:
    ut, emu, _ = T.setup_emulator_v2()
    T.set_version_globals(emu, 0x0DF1)
    for g, v in eg.items():
        emu.mu.mem_write(g, struct.pack("<B", v))
    pos = 13
    err = None
    for r in range(21):
        flag = p[pos]; pos += 1
        obj, vt, s19 = T.construct_v2(ut, emu, 3, flag)
        res = T.run_row_v2(ut, emu, obj, s19, p[pos:footer], 0x0DF1, 1, stream_flags=sf)
        if not res["ok"]:
            err = f"row{r} cons={res['bytes_consumed']} err={str(res['error'])[:60]}"
            break
        pos += res["bytes_consumed"]
    print(f"{name:12s}: {'ALL 21 OK end=' + str(pos) if err is None else err}", flush=True)
