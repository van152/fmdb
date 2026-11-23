"""server/t3 row 20 isolated (fresh emulator starts directly at row 20)."""
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

# replay rows 0-19 in a THROWAWAY emulator just to find row 20's offset
ut, emu, _ = T.setup_emulator_v2()
T.set_version_globals(emu, 0x0DF1)
pos = 13
for r in range(20):
    flag = p[pos]; pos += 1
    obj, vt, s19 = T.construct_v2(ut, emu, 3, flag)
    res = T.run_row_v2(ut, emu, obj, s19, p[pos:footer], 0x0DF1, 1)
    if not res["ok"]:
        print("replay failed early at row", r); sys.exit(1)
    pos += res["bytes_consumed"]
print("row20 starts at", pos, "flag byte:", hex(p[pos]))
row20_pos = pos

# fresh emulator, row 20 only
ut2, emu2, _ = T.setup_emulator_v2()
T.set_version_globals(emu2, 0x0DF1)
flag = p[row20_pos]
obj, vt, s19 = T.construct_v2(ut2, emu2, 3, flag)
res = T.run_row_v2(ut2, emu2, obj, s19, p[row20_pos+1:footer], 0x0DF1, 1)
print(f"iso row20 flag={flag:#x} ok={res['ok']} rax={res.get('rax',0):#x} consumed={res['bytes_consumed']} err={str(res['error'])[:80]}")
if not res["ok"]:
    for rd in res["reads"][-6:]:
        print("   ", {k: rd.get(k) for k in ("wire_pos","n","u_val","hex","caller")})
