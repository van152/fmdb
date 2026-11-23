"""t72 row 0: full read trace with fixed harness."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
import t111_unicorn_last11 as T
from diff_t3 import load_specific

tabs = load_specific([("server", 72)])
p = tabs[("server", 72)]
footer = len(p) - 9
ut, emu, db_a3 = T.setup_emulator_v2()
T.set_version_globals(emu, 0x0DF1)
vt_fb = T.load_vtable_fallback()

pos = 13
flag = p[pos]; pos += 1
print(f"flag={flag:#x}")
obj, vt, s19 = T.construct_v2(ut, emu, 72, flag)
print(f"vt={vt:#x} s19={s19:#x}")
res = T.run_row_v2(ut, emu, obj, s19, p[pos:footer], 0x0DF1, 1)
print(f"ok={res['ok']} consumed={res['bytes_consumed']} err={res['error']} rip={res['end_rip']}")
for rd in res["reads"]:
    keys = ("wire_pos", "n", "dst_kind", "u_val", "hex", "caller")
    print("  ", {k: rd.get(k) for k in keys if rd.get(k) is not None or k in ("wire_pos","n","dst_kind")})
