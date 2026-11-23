"""server/t3 CLUB: run rows 0-19 clean, then row 20 with full read trace."""
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
nrows = struct.unpack_from("<I", p, 8)[0]
print(f"rows={nrows} footer={footer}")
ut, emu, db_a3 = T.setup_emulator_v2()
T.set_version_globals(emu, 0x0DF1)
vt_fb = T.load_vtable_fallback()

pos = 13
for r in range(21):
    flag = p[pos]; pos += 1
    obj, vt, s19 = T.construct_v2(ut, emu, 3, flag)
    if s19 == 0:
        print(f"row{r} ctor fail")
        break
    res = T.run_row_v2(ut, emu, obj, s19, p[pos:footer], 0x0DF1, 1)
    ok = res["ok"] and (r < 20 or res.get("rax") == 1)
    print(f"row{r} flag={flag:#x} ok={res['ok']} rax={res.get('rax',0):#x} consumed={res['bytes_consumed']} err={str(res['error'])[:70]}", flush=True)
    if not res["ok"] or r == 20:
        if not res["ok"]:
            for rd in res["reads"][-25:]:
                print("   ", {k: rd.get(k) for k in ("wire_pos","n","dst_kind","u_val","hex","caller") if rd.get(k) is not None or k in ("wire_pos","n","dst_kind")})
        break
    pos += res["bytes_consumed"]
print("end_pos:", pos, "footer:", footer)
