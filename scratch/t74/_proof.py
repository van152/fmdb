"""验证 W+footer=21 不变量:三个唯一解是否为同一物理铺法;并统计 marker 字节分布。"""
import sys, json
sys.path.insert(0, 'scripts')
from collections import Counter
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec, SPECS

c = codec()
rep = {}
for archive, tid, n, kind in SPECS:
    b = payload(c, archive, tid)
    if kind == "fixed":
        r = P.fixed_rows(b, P.FIXED[(archive, tid)])
    elif kind == "lang":
        r = P.seq_lang(b, n)
    elif kind == "weat":
        r = P.seq_weat(b, n)
    elif kind == "derby":
        r = P.seq_derby(b, n, 65 if archive == "client" else 71)
    else:
        r = P._dp_rows(b, n, 14, 8)
    rows = r["rows"]
    ends = [e for s, e in rows]
    mk = Counter(b[e - 1] for e in ends)
    # W+footer=21 等价:三种 (W,footer) 的行尾物理位置是否一致
    alt = {}
    for W, fo in ((12, 9), (13, 8), (14, 7)):
        hi = len(b) - fo
        cnt, starts, _ = P._dp(b, "eq", 14, hi, n, W)
        alt[f"{W}/{fo}"] = (cnt, list(starts) if starts else None)
    same = len({tuple(v[1]) for v in alt.values() if v[1]}) == 1 and all(v[1] for v in alt.values())
    rep[f"{tid}_{archive}"] = {
        "marker_bytes": dict(mk),
        "marker_all_zero": set(mk) == {0},
        "alt_tilings": {k: v[0] for k, v in alt.items()},
        "row_starts_same": same,
    }
    print(f"t{tid}/{archive:6s} marker={dict(mk)} allzero={set(mk)=={0}} "
          f"paths(12/9,13/8,14/7)={[v[0] for v in alt.values()]} same_phys={same}")
json.dump(rep, open('scratch/t74/out/identity_width_proof.json', 'w'), indent=1, ensure_ascii=False)
