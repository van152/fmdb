"""identity 宽度 + footer 的双重自证,写成 identity_width_proof.json。

判据 A(对齐自证):行框已独立确定(fixed stride / 顺序语法 / 唯一 DP)后,
  统计行尾 -11..-16 各偏移"构成 (ordinal==i, UID对相等)"的行数;
  唯一使全部行成立的偏移即 identity 起点 -> 宽度 13。
判据 B(footer 唯一性):固定 W=13,暴力 footer ∈ 7..12,只有 footer=8 能闭合。
"""
import sys, json
sys.path.insert(0, 'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec, SPECS


def rows_of(b, archive, tid, n, kind):
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
    return r["rows"] if r else None


def main():
    c = codec()
    rep = {}
    for archive, tid, n, kind in SPECS:
        b = payload(c, archive, tid)
        rows = rows_of(b, archive, tid, n, kind)
        assert rows, (archive, tid)
        align = {}
        for off in range(11, 17):
            hit = 0
            for i, (s, e) in enumerate(rows):
                p = e - off
                if p < s:
                    continue
                o, u1, u2 = P.struct_u32(b, p), P.struct_u32(b, p + 4), P.struct_u32(b, p + 8)
                hit += (o == i and u1 == u2 and u1 > 0)
            align[off] = hit
        foot = {}
        for fo in range(5, 13):
            cnt, _, _ = P._dp(b, "f", 14, len(b) - fo, n, 13)
            foot[fo] = cnt
        rep[f"{tid}_{archive}"] = {
            "count": n,
            "align_hits_by_row_end_offset": align,
            "unique_identity_offset": [k for k, v in align.items() if v == n],
            "identity_width": 13,
            "footer_paths_W13": foot,
            "unique_footer": [k for k, v in foot.items() if v == 1],
        }
        print(f"t{tid}/{archive:6s} align唯一={[k for k,v in align.items() if v==n]} "
              f"footer唯一={[k for k,v in foot.items() if v==1]}")
    json.dump(rep, open('scratch/t74/out/identity_width_proof.json', 'w'),
              indent=1, ensure_ascii=False)
    print("\nwritten: scratch/t74/out/identity_width_proof.json")


if __name__ == "__main__":
    main()
