"""敏感性网格:每表独立重算 (W, footer) 下的路径数,证明 identity 宽度自证。"""
import sys, os, json
sys.path.insert(0, 'scripts')
import t74_frames_part2 as P
import t74_frames_part3 as S
from t74_row_frames9 import payload, codec, SPECS

c = codec()
out = {}
for archive, tid, n, kind in SPECS:
    b = payload(c, archive, tid)
    g = S.sens_grid(b, n, 14, Ws=(12, 13, 14), foots=(7, 8, 9, 10, 12))
    uniq = [f"{W}/{f}" for (W, f), v in g.items() if v == 1]
    out[f"{tid}_{archive}"] = {f"{W}/{f}": v for (W, f), v in g.items()}
    print(f"t{tid}/{archive:6s} n={n:6d} unique={(uniq)}")
    print("   ", {f"{W}/{f}": v for (W, f), v in g.items()})
json.dump(out, open('scratch/t74/out/sensitivity.json', 'w'), indent=1)
