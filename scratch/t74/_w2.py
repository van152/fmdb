import json
p='scratch/t74/out/frames.json'
d=json.load(open(p,encoding='utf-8'))

d['tables']['27']={
 "entity":"weather",
 "archives":{
  "client":{
   "payload_len":43345,"header":14,"footer":8,"count":334,"model":"variable",
   "row_rule":"[u32 name_len][UTF-8 profile name][95B numeric middle][ordinal u32][UID u32][UID u32][marker 0]",
   "closure":"14 + Σ(4+name_len+95+13) + 8 == 43345;顺序游标逐行前进 334 行恰好停在 footer(43337==F),无需 DP",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "ordinal_check":"ordinal == 行下标 0..333,334/334;UID 对相等;marker 全 0",
   "sensitivity":"DP(W13/f8)=3 路(固定 95B 中段使歧义);但顺序文法(行长可由 name_len 唯一复算)只有 1 条,且逐行闭合到 footer。W12/f9 同样 1 条。f7/f10/f12 无法闭合。",
   "ambiguity_note":"纯 DP 在 13B 下得 3 路(见 _x43 探针:row0 若把边界放在 139/141 会误读 identity);决定性约束是'行长 == 4+name_len+95+13'逐行成立 334/334,加 footer 精确对齐,故取此唯一文法。上游 sms 表称 opaque middle 99B,本仓实测 95B+13B 合计 108B 才闭合。",
   "row_len_range":[117,156],
   "payload_sha256":"aaf5f170938babd755f9e020226d3dfcb437c3cd5bdb01796f30acee18e48770",
   "verified":True},
  "server":{
   "payload_len":43345,"header":14,"footer":8,"count":334,"model":"variable",
   "row_rule":"同 client(两档 payload 逐字节相同,sha 相同)",
   "closure":"同 client 334 行闭合",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "sensitivity":"同 client",
   "payload_sha256":"aaf5f170938babd755f9e020226d3dfcb437c3cd5bdb01796f30acee18e48770",
   "verified":True}}}

d['tables']['7']={
 "entity":"media",
 "archives":{
  "client":{
   "payload_len":36824,"header":14,"footer":8,"count":208,"model":"variable",
   "row_rule":"[u32 name_len][UTF-8 name][6B scalar prefix(10 种取值)][u32 url_len][UTF-8 url][variable middle][ordinal u32][UID u32][UID u32][marker 0]",
   "closure":"14 + Σrowlen + 8 == 36824;身份 trailer 由 DP 唯一铺满(1 路),行首 name 长度前缀逐行可读,url 长度前缀对 204/208 行成立(4 行 url_len==0)",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "identity_prefix_5B":"trailer 前 5B 有 16 种取值,最常见 0000000001(161/208)、0000000000(31/208);不参与行框",
   "six_byte_prefix":{"distinct":10,"top":{"000100000006":75,"000100000001":72,"000200000005":25,"000100000004":16}},
   "rows_with_url":204,
   "row_len_range":[80,715],
   "sensitivity":"DP(W13/f8)=1 路;W12/f9=1 路;f7/f10/f12=0 路",
   "unresolved":"middle 段是嵌套 count/list 区,未能定出唯一字节文法(见 REPORT 负结果);行框与行长复算仍然精确",
   "payload_sha256":"71860a6f2e4de62ff5d1861b6e64e9fbd4544b9d2539de37ec5e811a4a198db1",
   "verified":True},
  "server":{
   "payload_len":38280,"header":14,"footer":8,"count":208,"model":"variable",
   "row_rule":"同 client,但每行多 7B:插入位置在 identity trailer 之前(middle 段内)",
   "closure":"14 + Σrowlen + 8 == 38280;DP 唯一 1 路",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "server_diff":{"delta_bytes_per_row":7,"rows":"208/208 每行均 +7B(与 client 逐行配对长度差全为 7)",
     "data_side_evidence":"server 行在 identity trailer 之前出现 7B 插入,形如 01 04 01 00 6c 07 00;client 对应位置无该 7B。client 首行 [14,204) 长 190,server 首行 [14,211) 长 197。",
     "position_evidence":"row0 client: ...d8 02 00 00 | 00 00 00 00 01 ;server: ...d8 02 00 00 | 01 04 01 00 6c 07 00 00 00 00 00 01 —— 7B 紧接在 marker 前的 5B 前缀区之前/之中,不动 ordinal/UID",
     "identity_unchanged":"两档同一 ordinal 的 UID 对相同,trailer 位置仅随行尾平移"},
   "row_len_range":[87,722],
   "sensitivity":"DP(W13/f8)=1 路;W12/f9=1 路;f7/f10/f12=0 路",
   "payload_sha256":"b7ccbe1e9112c4887a7169306e61b7b25be74249f8fb4950982277872d6dfeab",
   "verified":True}}}

json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('tables now:',sorted(d['tables'],key=int))
