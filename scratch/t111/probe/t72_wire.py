"""Dump t72 wire bytes + hand-decode against s19 schema."""
import struct, sys
from pathlib import Path
ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.insert(0, str(ROOT / "scratch/t111/probe"))
from diff_t3 import load_specific

tabs = load_specific([("server", 72)])
p = tabs[("server", 72)]
ver = struct.unpack_from("<H", p, 6)[0]
nrows = struct.unpack_from("<I", p, 8)[0]
footer = len(p) - 9
print(f"size={len(p)} ver={ver:#x} nrows={nrows} footer={footer} data_bytes={footer-13} avg={(footer-13)/nrows:.1f}")
body = p[13:footer]
print("first 160 bytes:", body[:160].hex(" "))
print()
# locate the 15-byte motif
motif = bytes.fromhex("011e000000000364d62d0000ffe907")
idx = body.find(motif)
print("motif at body offset:", idx)
# count motif occurrences & spacing
import re
posns = [m.start() for m in re.finditer(re.escape(motif), body)]
print("motif count:", len(posns), "gaps:", [b - a for a, b in zip(posns, posns[1:])][:10])
# year pattern
print("bytes 13..", )
