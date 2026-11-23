"""Probe: walk N people rows w/ t120 emulator; save per-PLAYER-row reads + body slice for analysis."""
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
    buf = rdr.read(32 * 1024 * 1024)

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
    rec = {"i": idx, "off": pos, "pt": pt, "len": blen, "ord": ord_id}
    if pt == 2:
        rec["reads"] = [[r["wire_pos"], r["obj_off_dec"], r["n"], r["hex"]]
                        for r in res["reads"] if r["n"] and r["obj_off_dec"] is not None]
    rows.append(rec)
    pos += 5 + blen

json.dump({"rows": rows, "end": pos, "buf_len": len(buf)},
          open(ROOT / "scratch/t126/out/_walk.json", "w"))
pl = [r for r in rows if r["pt"] == 2]
print("rows", len(rows), "players", len(pl), "end", pos)
from collections import Counter
print("types", Counter(r["pt"] for r in rows))
print("player reads median", sorted(len(r["reads"]) for r in pl)[len(pl)//2] if pl else 0)
