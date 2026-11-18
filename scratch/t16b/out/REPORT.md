# t16b — naming bridge recalibration and entity ledger

Status: `complete_ledger_partial_coverage_g1_below_95pct`

## Method

- Reused `scripts/t16_serializer_walk.py` without modification. For each resolved stage2 tag, walked its class readers; only a unique object_off+width direct-read 4CC instance and exact schema code is `L3_instruction`.
- Known E27/E20/E55 rows are `L3_inherited` if a unique fresh bridge is absent. If fresh walk and baseline disagree, the baseline row is retained and the conflict is explicit; ambiguous rows remain unnamed.
- Every schema top-level and nested field is represented. Nested/list members stay unnamed unless a row-inline bridge exists. Player tag is listed but not walked because its schema contains out-of-scope PDxx blocks.
- Branch counts are conditional-jump instruction counts reported by t16, not a proof that each branch corresponds to an individual schema field.

## G1 inheritance comparison

- Result: `fail`; exact matches 12/237 = 0.05063291139240506; threshold 95%.
- Not numerically comparable (variable-width baseline): 1.
- Conflicting columns: 18; missing walk mappings: 207. Missing numeric baseline mappings count as non-matches; only the variable-width E27 name is excluded from the numeric denominator.

### Conflicts (walk value differs from inherited baseline)

| tag | field | table | expected offset/width | walked offset/width | source |
|---|---|---:|---|---|---|
| comp | CTty | 25 | [18, 1] | [[6, 1]] | scratch/t01/inbox/t01f/output.json |
| stad | Spty | 21 | [2, 1] | [[33, 1]] | reports/t12_field_names.json |
| stad | Sste | 21 | [3, 1] | [[34, 1]] | reports/t12_field_names.json |
| stad | Senv | 21 | [4, 1] | [[35, 1]] | reports/t12_field_names.json |
| stad | Sdah | 21 | [5, 1] | [[36, 1]] | reports/t12_field_names.json |
| stad | Sitg | 21 | [5, 1] | [[36, 1]] | reports/t12_field_names.json |
| stad | Sext | 21 | [5, 1] | [[36, 1]] | reports/t12_field_names.json |
| stad | Sunt | 21 | [6, 1] | [[37, 1]] | reports/t12_field_names.json |
| stad | Su21 | 21 | [7, 1] | [[38, 1]] | reports/t12_field_names.json |
| stad | Su19 | 21 | [8, 1] | [[39, 1]] | reports/t12_field_names.json |
| stad | Soty | 21 | [9, 1] | [[40, 1]] | reports/t12_field_names.json |
| stad | Smnl | 21 | [11, 2] | [[42, 2]] | reports/t12_field_names.json |
| stad | Smnw | 21 | [13, 2] | [[44, 2]] | reports/t12_field_names.json |
| stad | Smxl | 21 | [15, 2] | [[46, 2]] | reports/t12_field_names.json |
| stad | Smxw | 21 | [17, 2] | [[48, 2]] | reports/t12_field_names.json |
| stad | Sdtr | 21 | [19, 1] | [[50, 1]] | reports/t12_field_names.json |
| stad | Sprr | 21 | [21, 1] | [[52, 1]] | reports/t12_field_names.json |
| lcrg | Lpop | 47 | [17, 4] | [[4, 4]] | reports/t12_field_names.json |

### Baseline fields with no matching walked bridge

| tag | field | table | expected | source |
|---|---|---:|---|---|
| weat | w0sd | 27 | [0, 2] | scratch/t01/inbox/t01l/output.json |
| weat | w0p0 | 27 | [2, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0p1 | 27 | [3, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0p2 | 27 | [4, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0p3 | 27 | [5, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0p4 | 27 | [6, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0w0 | 27 | [7, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0w1 | 27 | [8, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0w2 | 27 | [9, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0w3 | 27 | [10, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0w4 | 27 | [11, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0te | 27 | [12, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0tv | 27 | [13, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t0 | 27 | [14, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t1 | 27 | [15, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t2 | 27 | [16, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t3 | 27 | [17, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t4 | 27 | [18, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t5 | 27 | [19, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t6 | 27 | [20, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0t7 | 27 | [21, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w0dn | 27 | [22, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1sd | 27 | [23, 2] | scratch/t01/inbox/t01l/output.json |
| weat | w1p0 | 27 | [25, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1p1 | 27 | [26, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1p2 | 27 | [27, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1p3 | 27 | [28, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1p4 | 27 | [29, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1w0 | 27 | [30, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1w1 | 27 | [31, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1w2 | 27 | [32, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1w3 | 27 | [33, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1w4 | 27 | [34, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1te | 27 | [35, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1tv | 27 | [36, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t0 | 27 | [37, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t1 | 27 | [38, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t2 | 27 | [39, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t3 | 27 | [40, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t4 | 27 | [41, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t5 | 27 | [42, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t6 | 27 | [43, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1t7 | 27 | [44, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w1dn | 27 | [45, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2sd | 27 | [46, 2] | scratch/t01/inbox/t01l/output.json |
| weat | w2p0 | 27 | [48, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2p1 | 27 | [49, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2p2 | 27 | [50, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2p3 | 27 | [51, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2p4 | 27 | [52, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2w0 | 27 | [53, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2w1 | 27 | [54, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2w2 | 27 | [55, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2w3 | 27 | [56, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2w4 | 27 | [57, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2te | 27 | [58, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2tv | 27 | [59, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t0 | 27 | [60, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t1 | 27 | [61, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t2 | 27 | [62, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t3 | 27 | [63, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t4 | 27 | [64, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t5 | 27 | [65, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t6 | 27 | [66, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2t7 | 27 | [67, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w2dn | 27 | [68, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3sd | 27 | [69, 2] | scratch/t01/inbox/t01l/output.json |
| weat | w3p0 | 27 | [71, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3p1 | 27 | [72, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3p2 | 27 | [73, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3p3 | 27 | [74, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3p4 | 27 | [75, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3w0 | 27 | [76, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3w1 | 27 | [77, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3w2 | 27 | [78, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3w3 | 27 | [79, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3w4 | 27 | [80, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3te | 27 | [81, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3tv | 27 | [82, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t0 | 27 | [83, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t1 | 27 | [84, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t2 | 27 | [85, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t3 | 27 | [86, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t4 | 27 | [87, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t5 | 27 | [88, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t6 | 27 | [89, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3t7 | 27 | [90, 1] | scratch/t01/inbox/t01l/output.json |
| weat | w3dn | 27 | [91, 1] | scratch/t01/inbox/t01l/output.json |
| comp | cfcl | 25 | [3, 2] | scratch/t01/inbox/t01f/output.json |
| comp | cbcl | 25 | [5, 2] | scratch/t01/inbox/t01f/output.json |
| comp | ctcl | 25 | [7, 2] | scratch/t01/inbox/t01f/output.json |
| comp | levl | 25 | [15, 1] | scratch/t01/inbox/t01f/output.json |
| comp | cmnl | 25 | [76, 2] | scratch/t01/inbox/t01f/output.json |
| comp | cmnw | 25 | [78, 2] | scratch/t01/inbox/t01f/output.json |
| comp | cmxl | 25 | [80, 2] | scratch/t01/inbox/t01f/output.json |
| comp | cmxw | 25 | [82, 2] | scratch/t01/inbox/t01f/output.json |
| comp | cnor | 25 | [84, 4] | scratch/t01/inbox/t01f/output.json |
| comp | csou | 25 | [88, 4] | scratch/t01/inbox/t01f/output.json |
| comp | cwes | 25 | [92, 4] | scratch/t01/inbox/t01f/output.json |
| comp | ceas | 25 | [96, 4] | scratch/t01/inbox/t01f/output.json |
| comp | wbcl | 25 | [101, 2] | scratch/t01/inbox/t01f/output.json |
| comp | wbst | 25 | [103, 4] | scratch/t01/inbox/t01f/output.json |
| comp | wben | 25 | [107, 4] | scratch/t01/inbox/t01f/output.json |
| comp | cuae | 25 | [111, 1] | scratch/t01/inbox/t01f/output.json |
| comp | csso | 25 | [112, 1] | scratch/t01/inbox/t01f/output.json |
| city | Clat | 2 | [1, 4] | reports/t12_field_names.json |
| city | Clon | 2 | [5, 4] | reports/t12_field_names.json |
| city | Cnti | 2 | [10, 4] | reports/t12_field_names.json |
| city | Cwea | 2 | [14, 4] | reports/t12_field_names.json |
| city | Clgi | 2 | [21, 4] | reports/t12_field_names.json |
| city | Clri | 2 | [25, 4] | reports/t12_field_names.json |
| city | Clat | 2 | [1, 4] | reports/t12_field_names.json |
| city | Clon | 2 | [5, 4] | reports/t12_field_names.json |
| city | Cnti | 2 | [10, 4] | reports/t12_field_names.json |
| city | Cwea | 2 | [14, 4] | reports/t12_field_names.json |
| city | Clgi | 2 | [21, 4] | reports/t12_field_names.json |
| city | Clri | 2 | [25, 4] | reports/t12_field_names.json |
| inju | Imnd | 6 | [3, 2] | reports/t12_field_names.json |
| inju | Iexd | 6 | [5, 2] | reports/t12_field_names.json |
| inju | Iiar | 6 | [7, 1] | reports/t12_field_names.json |
| inju | Irec | 6 | [8, 1] | reports/t12_field_names.json |
| inju | Iocr | 6 | [13, 4] | reports/t12_field_names.json |
| inju | Imip | 6 | [17, 1] | reports/t12_field_names.json |
| inju | Icau | 6 | [18, 2] | reports/t12_field_names.json |
| inju | Iagr | 6 | [20, 1] | reports/t12_field_names.json |
| inju | Icms | 6 | [21, 1] | reports/t12_field_names.json |
| inju | Icon | 6 | [22, 1] | reports/t12_field_names.json |
| inju | inSr | 6 | [23, 1] | reports/t12_field_names.json |
| inju | Igpr | 6 | [24, 1] | reports/t12_field_names.json |
| inju | Icdp | 6 | [25, 1] | reports/t12_field_names.json |
| inju | Ibin | 6 | [26, 1] | reports/t12_field_names.json |
| inju | Ibis | 6 | [26, 1] | reports/t12_field_names.json |
| inju | Ibph | 6 | [26, 1] | reports/t12_field_names.json |
| inju | Ibsp | 6 | [26, 1] | reports/t12_field_names.json |
| inju | Ibpg | 6 | [26, 1] | reports/t12_field_names.json |
| club | Slea | 19 | [8, 4] | reports/t12_field_names.json |
| club | Ssta | 19 | [12, 4] | reports/t12_field_names.json |
| club | Slmd | 19 | [16, 4] | reports/t12_field_names.json |
| club | Scap | 19 | [20, 4] | reports/t12_field_names.json |
| club | Sscp | 19 | [24, 4] | reports/t12_field_names.json |
| club | Sceb | 19 | [28, 4] | reports/t12_field_names.json |
| club | Slea | 19 | [8, 4] | reports/t12_field_names.json |
| club | Ssta | 19 | [12, 4] | reports/t12_field_names.json |
| club | Slmd | 19 | [16, 4] | reports/t12_field_names.json |
| club | Scap | 19 | [20, 4] | reports/t12_field_names.json |
| club | Sscp | 19 | [24, 4] | reports/t12_field_names.json |
| club | Sceb | 19 | [28, 4] | reports/t12_field_names.json |
| stad | Scov | 21 | [22, 2] | reports/t12_field_names.json |
| club | Sold | 22 | [4, 4] | reports/t12_field_names.json |
| club | Snew | 22 | [8, 4] | reports/t12_field_names.json |
| club | Scap | 22 | [12, 4] | reports/t12_field_names.json |
| club | Styp | 22 | [16, 1] | reports/t12_field_names.json |
| club | Salt | 22 | [17, 4] | reports/t12_field_names.json |
| club | Scpm | 22 | [21, 1] | reports/t12_field_names.json |
| club | Sscp | 22 | [22, 4] | reports/t12_field_names.json |
| club | Snxa | 22 | [26, 4] | reports/t12_field_names.json |
| club | Snmn | 22 | [30, 4] | reports/t12_field_names.json |
| club | Snmx | 22 | [34, 4] | reports/t12_field_names.json |
| club | Stks | 22 | [38, 4] | reports/t12_field_names.json |
| club | Slhm | 22 | [42, 1] | reports/t12_field_names.json |
| club | Scam | 22 | [43, 4] | reports/t12_field_names.json |
| club | Scns | 22 | [47, 1] | reports/t12_field_names.json |
| club | ScTL | 22 | [48, 1] | reports/t12_field_names.json |
| club | ScYL | 22 | [49, 1] | reports/t12_field_names.json |
| club | Sceb | 22 | [50, 4] | reports/t12_field_names.json |
| play | inju | 30 | [4, 4] | reports/t12_field_names.json |
| play | futu | 30 | [16, 1] | reports/t12_field_names.json |
| play | perm | 30 | [17, 1] | reports/t12_field_names.json |
| play | seve | 30 | [18, 1] | reports/t12_field_names.json |
| play | side | 30 | [19, 1] | reports/t12_field_names.json |
| play | pret | 30 | [20, 1] | reports/t12_field_names.json |
| club | edyr | 34 | [10, 2] | reports/t12_field_names.json |
| club | dbrt | 34 | [21, 1] | reports/t12_field_names.json |
| club | posi | 34 | [26, 1] | reports/t12_field_names.json |
| club | tcop | 34 | [27, 4] | reports/t12_field_names.json |
| club | year | 37 | [12, 2] | reports/t12_field_names.json |
| club | posi | 37 | [14, 1] | reports/t12_field_names.json |
| club | play | 37 | [15, 1] | reports/t12_field_names.json |
| club | wins | 37 | [16, 1] | reports/t12_field_names.json |
| club | draw | 37 | [17, 1] | reports/t12_field_names.json |
| club | lost | 37 | [18, 1] | reports/t12_field_names.json |
| club | gfor | 37 | [19, 2] | reports/t12_field_names.json |
| club | gaga | 37 | [21, 2] | reports/t12_field_names.json |
| club | poin | 37 | [23, 2] | reports/t12_field_names.json |
| club | orde | 37 | [25, 1] | reports/t12_field_names.json |
| club | mxtm | 37 | [26, 1] | reports/t12_field_names.json |
| club | mths | 43 | [24, 4] | reports/t12_field_names.json |
| club | pyiv | 43 | [32, 1] | reports/t12_field_names.json |
| lcrg | Lwea | 47 | [8, 4] | reports/t12_field_names.json |
| pers | divi | 49 | [5, 4] | reports/t12_field_names.json |
| pers | comp | 49 | [13, 4] | reports/t12_field_names.json |
| pers | otea | 49 | [17, 4] | reports/t12_field_names.json |
| pers | plac | 49 | [21, 1] | reports/t12_field_names.json |
| pers | ajob | 49 | [22, 1] | reports/t12_field_names.json |
| pers | divi | 58 | [0, 4] | reports/t12_field_names.json |
| pers | team | 58 | [8, 4] | reports/t12_field_names.json |
| pers | team | 58 | [12, 4] | reports/t12_field_names.json |
| pers | comp | 58 | [28, 4] | reports/t12_field_names.json |
| club | Ttyp | 62 | [0, 1] | reports/t12_field_names.json |
| club | comp | 70 | [8, 4] | reports/t12_field_names.json |
| club | wrcl | 70 | [16, 2] | reports/t12_field_names.json |
| club | styr | 70 | [18, 2] | reports/t12_field_names.json |
| club | enyr | 70 | [20, 2] | reports/t12_field_names.json |
| club | type | 70 | [22, 1] | reports/t12_field_names.json |
| club | mage | 70 | [24, 1] | reports/t12_field_names.json |
| club | mlen | 70 | [25, 1] | reports/t12_field_names.json |
| club | isog | 70 | [26, 1] | reports/t12_field_names.json |

## Per-entity coverage

| tag | entity | all fields | top-level | nested | named | unnamed | coverage | classes | serializer funcs | conditional jumps | conflicts | L2_data rows |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| club | club | 672 | 433 | 239 | 14 | 658 | 2.1% | 15 | 16 | 139 | 11 | 0 |
| nati | nation | 441 | 346 | 95 | 0 | 441 | 0.0% | 1 | 1 | 11 | 0 | 0 |
| comp | comp | 294 | 255 | 39 | 18 | 276 | 6.1% | 2 | 2 | 24 | 1 | 0 |
| team | team | 25 | 25 | 0 | 0 | 25 | 0.0% | 2 | 2 | 42 | 0 | 0 |
| agrm | agreement | 8 | 8 | 0 | 0 | 8 | 0.0% | 1 | 1 | 1 | 0 | 0 |
| awar | award | 65 | 38 | 27 | 4 | 61 | 6.2% | 2 | 5 | 47 | 0 | 0 |
| city | city | 15 | 15 | 0 | 7 | 8 | 46.7% | 1 | 1 | 1 | 0 | 0 |
| cont | continent | 16 | 16 | 0 | 1 | 15 | 6.2% | 1 | 1 | 13 | 0 | 0 |
| curr | currency | 7 | 7 | 0 | 1 | 6 | 14.3% | 1 | 2 | 11 | 0 | 0 |
| drbr | derby | 22 | 22 | 0 | 0 | 22 | 0.0% | 1 | 1 | 11 | 0 | 0 |
| inju | injury | 27 | 27 | 0 | 20 | 7 | 74.1% | 1 | 1 | 3 | 0 | 0 |
| lang | language | 12 | 12 | 0 | 5 | 7 | 41.7% | 1 | 1 | 8 | 0 | 0 |
| lcrg | local region | 13 | 11 | 2 | 2 | 11 | 15.4% | 1 | 1 | 16 | 1 | 0 |
| mdso | media source | 25 | 22 | 3 | 0 | 25 | 0.0% | 1 | 1 | 6 | 0 | 0 |
| pers | person | 405 | 271 | 134 | 14 | 391 | 3.5% | 16 | 21 | 136 | 0 | 1 |
| play | player | 241 | 179 | 62 | 0 | 241 | 0.0% | 0 | 0 | 0 | 0 | 2 |
| regi | region | 6 | 6 | 0 | 0 | 6 | 0.0% | 1 | 1 | 8 | 0 | 0 |
| stad | stadium | 76 | 60 | 16 | 27 | 49 | 35.5% | 2 | 2 | 66 | 17 | 0 |
| stgn | stage name | 8 | 8 | 0 | 0 | 8 | 0.0% | 1 | 1 | 1 | 0 | 0 |
| weat | weather | 94 | 94 | 0 | 88 | 6 | 93.6% | 1 | 1 | 4 | 0 | 0 |

## Club mixed-entity branch audit

- Factory/class branches walked: 15; serializer candidate functions: 16; reported conditional-jump instructions: 139.
- Per-table counts:
  - table 3 `LEAGUE_BODY_CLUB`: 2 serializer candidate(s), 11 conditional jumps; ok.
  - table 33 `STARTING_CLUB_DEBT`: 1 serializer candidate(s), 20 conditional jumps; ok.
  - table 34 `STARTING_TEAM_CUP_HISTORY`: 1 serializer candidate(s), 12 conditional jumps; ok.
  - table 37 `STARTING_TEAM_LEAGUE_HISTORY`: 1 serializer candidate(s), 15 conditional jumps; ok.
  - table 43 `STARTING_MONTHLY_INSTALLMENT`: 1 serializer candidate(s), 15 conditional jumps; ok.
  - table 50 `STARTING_MLS_TRADED_SLOT`: 1 serializer candidate(s), 6 conditional jumps; ok.
  - table 51 `STARTING_MLS_GENERAL_ALLOCATION_MONEY`: 1 serializer candidate(s), 3 conditional jumps; ok.
  - table 58 `STARTING_WEEKLY_WAGE_CONTRIBUTION`: 1 serializer candidate(s), 16 conditional jumps; ok.
  - table 60 `STARTING_MLS_TARGETED_ALLOCATION_MONEY`: 1 serializer candidate(s), 3 conditional jumps; ok.
  - table 61 `STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT`: 1 serializer candidate(s), 3 conditional jumps; ok.
  - table 62 `STARTING_RESERVE_TEAM`: 1 serializer candidate(s), 11 conditional jumps; ok.
  - table 63 `STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER`: 1 serializer candidate(s), 3 conditional jumps; ok.
  - table 64 `STARTING_CLUB_STAFF_JOB_STATUS`: 1 serializer candidate(s), 4 conditional jumps; ok.
  - table 66 `STARTING_CLUB_TRANSFER_PREFERENCE`: 1 serializer candidate(s), 5 conditional jumps; ok.
  - table 70 `STARTING_VISION_OBJECTIVE`: 1 serializer candidate(s), 12 conditional jumps; ok.

t04 had closed one field only. The walk reports structural candidates but does not prove branch-to-field closure; fields remain individually graded and unresolved rows are not guessed.

## G3 data-side cross-checks

C-class t15 evidence is attached as secondary `grade=L2_data`, `subgrade=C_candidate`; it supports relation candidates, not field identity or an inline offset.
- table 30 `STARTING_INJURY` → `play.Pijl` injury-list candidate.
- table 38 `STARTING_BAN` → `play.Pbnl` ban-list candidate.
- table 49 `STARTING_PERSON_HISTORY` → `pers.Plhs` person-history-list candidate.
- These links remain C-class hypotheses; none is promoted to an inline serialized offset.

## Unclosed / limitations

- `unnamed` is an allowed ledger state. E55/E20/E27 mismatches are never overwritten silently.
- Conditional serializer paths can produce candidate offsets; branch counts are not field counts. Verify sample checks bridge evidence, not full control-flow closure.
- Player (`play`) rows are present but unwalked to honor the PDxx exclusion. No game/editor/IDA was launched; external files were read-only.
