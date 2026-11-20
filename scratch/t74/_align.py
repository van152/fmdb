"""identity 宽度对齐自证:行框独立确定后(fixed stride / 顺序语法 / 唯一 DP),
统计行尾各对齐位置 (-11..-16) 能构成 (ordinal==i, UID对相等) 的行数。
只有唯一一个偏移能对所有行成立 -> 该偏移即 identity 起点,宽度 = 行尾-起点。
footer 用敏感性网格(仅 footer=8 非零)固定,不参与本判据。
"""
import sys, json
sys.path.insert(0, 'scripts')
from collections import Counter
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec, SPECS

c = codec()
MODEL = {}
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
    al = {}
    for off in range(11, 17):
        hit = 0
        for i, (s, e) in enumerate(rows):
            p = e - off
            if p < s:
                continue
            o, u1, u2 = P.struct_u32(b, p), P.struct_u32(b, p + 4), P.struct_u32(b, p + 8)
            hit += (o == i and u1 == u2 and u1 > 0)
        al[off] = hit
    good = [k for k, v in al.items() if v == n]
    rep[f"{tid}_{archive}"] = {"align_hits": al, "count": n, "only_offsets": good}
    print(f"t{tid}/{archive:6s} n={n:6d} align_hits={al} -> 唯一偏移={good}")
json.dump(rep, open('scratch/t74/out/identity_width_proof.json', 'w'), indent=1, ensure_ascii=False)
