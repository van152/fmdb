"""修正 frames.json 的 t47 header 并重算全部 row_widths_*.csv(直方图摘要)。"""
import sys, json, csv, os
sys.path.insert(0, 'scripts')
from collections import Counter
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec, SPECS

OUT = 'scratch/t74/out'
fp = f'{OUT}/frames.json'
d = json.load(open(fp, encoding='utf-8'))
c = codec()

# --- t47 header 裁决:25 使首行 35B 违反 (len-41)%5==0;14 使 2488/2488 满足
for arc in ('client', 'server'):
    a = d['tables']['47']['archives'][arc]
    a['header'] = 14
    a['header_note'] = ("14 = 标准头(count u32@8);上游 OVERRIDE 记 25(14+11B 扩展)不成立:"
                        "H=25 时首行 35B,违反全表 (len-41)%5==0;H=14 时 2488/2488 行满足。"
                        "DP 在 H=14/H=25 下均唯一,但只有 H=14 满足行长规则")
d['summary']['upstream_conflicts'] = [
    x for x in d['summary']['upstream_conflicts'] if x['table'] != 47
] + [{"table": 47, "upstream": "25+2488*44+8",
      "ours": "14 + sum(41+5k) + 8",
      "basis": "H=25 首行 35B 破坏 (len-41)%5==0;H=14 全 2488 行成立"}]

# --- 重算所有 (archive,table) 的行长直方图 + 回填 payload_sha/closure
import hashlib
built = {}
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
    assert r and r['closure'] and r['bad_identity'] == 0, (archive, tid)
    lens = [e - s for s, e in r['rows']]
    built[(archive, tid)] = lens
    a = d['tables'][str(tid)]['archives'].setdefault(archive, {})
    a['payload_len'] = len(b)
    a['payload_sha256'] = hashlib.sha256(b).hexdigest()
    a['header'] = 14
    a['footer'] = 8
    a['count'] = n
    a['row_len_range'] = [min(lens), max(lens)]
    a['bad_identity'] = 0
    a['verified'] = True

json.dump(d, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('frames.json updated', os.path.getsize(fp), 'bytes')

# --- CSV 直方图
rows_out = []
for (archive, tid), lens in built.items():
    hist = Counter(lens)
    mean = round(sum(lens) / len(lens), 3)
    path = f'{OUT}/row_widths_{tid}_{archive}.csv'
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['table', 'archive', 'model', 'header', 'footer', 'count',
                    'rowlen_min', 'rowlen_max', 'rowlen_mean', 'rowlen_value', 'row_freq'])
        for v in sorted(hist):
            w.writerow([tid, archive, d['tables'][str(tid)]['archives'][archive]['model'],
                        14, 8, len(lens), min(lens), max(lens), mean, v, hist[v]])
    rows_out.append((tid, archive, len(lens), min(lens), max(lens), mean, len(hist)))
for r in sorted(rows_out):
    print('csv t%-3s %-6s rows=%-6d len=%d..%d mean=%s distinct=%d' % r)
