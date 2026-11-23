"""Probe: walk N people rows w/ t120 emulator, dump the 69-byte PLAYER_DATA block stats per PLAYER row."""
import sys, struct, json
from pathlib import Path

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
sys.path.insert(0, str(ROOT / "scripts"))

import zstandard
import t120_people_unicorn as t120

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 300

raw = (ROOT / "scratch/data/people_db.dat").read_bytes()
dctx = zstandard.ZstdDecompressor()
with dctx.stream_reader(raw[8:]) as rdr:
    buf = rdr.read(8 * 1024 * 1024)

m, ut, emu, _ = t120.setup_people_emulator()
pos = 6
rows = []
for idx in range(LIMIT):
    if pos + 5 >= len(buf):
        break
    ord_id = struct.unpack_from("<I", buf, pos)[0]
    pt = buf[pos + 4]
    obj, vt, s19, cerr = t120.call_people_factory(ut, emu, pt)
    if cerr or not s19:
        print("ctor fail", idx, cerr); break
    res = t120.run_person_row(ut, emu, obj, s19, buf[pos + 5:pos + 5 + 65536])
    if not res["ok"]:
        print("row fail", idx, res.get("error")); break
    blen = res["bytes_consumed"]
    body = buf[pos + 5:pos + 5 + blen]
    rec = {"i": idx, "off": pos, "pt": pt, "len": blen, "ord": ord_id}
    if pt == 2 and len(body) >= 98:
        blk = body[29:98]
        rec["nz"] = sum(1 for b in blk[15:] if b)
        rec["b0_14"] = list(blk[:15])
        rec["mx"] = max(blk[15:])
        rec["read29"] = any(r["wire_pos"] == 29 and r["n"] == 69 for r in res["reads"])
    rows.append(rec)
    pos += 5 + blen

pl = [r for r in rows if r["pt"] == 2]
print("rows", len(rows), "players", len(pl))
nz = sorted(pl, key=lambda r: -r["nz"])[:10]
for r in nz:
    print(r)
print("zero-attr players:", sum(1 for r in pl if r["nz"] == 0), "/", len(pl))
json.dump(rows, open(ROOT / "scratch/t126/out/_rows_probe.json", "w"))
