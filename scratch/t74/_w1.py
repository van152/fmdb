import json, io
p='scratch/t74/out/frames.json'
d=json.load(open(p,encoding='utf-8'))

d['tables']['8']={
 "entity":"language",
 "archives":{
  "client":{
   "payload_len":5248,"header":14,"footer":8,"count":126,"model":"variable",
   "row_rule":"[u32 name_len][UTF-8 name][17B suffix_prefix][ordinal u32][UID u32][UID u32][marker 0]",
   "closure":"14 + Σ(4+name_len+17+13) + 8 == 5248 (逐行复算 126/126)",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "ordinal_check":"ordinal == 行下标 0..125,126/126;UID 对相等;marker 全 0",
   "sensitivity":"DP(W13/f8)=1 路;W12/f9=1 路;f7/f10/f12=0 路",
   "payload_sha256":"0c8fbbb7875632f780b12b3e33520abe3cf3ae73fc6830649f51aa5b17b43eb2",
   "verified":True},
  "server":{
   "payload_len":5248,"header":14,"footer":8,"count":126,"model":"variable",
   "row_rule":"同 client(两档 payload 逐字节相同,sha 相同)",
   "closure":"同上 126/126",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "sensitivity":"同 client",
   "payload_sha256":"0c8fbbb7875632f780b12b3e33520abe3cf3ae73fc6830649f51aa5b17b43eb2",
   "verified":True}}}

d['tables']['18']={
 "entity":"derby",
 "archives":{
  "client":{
   "payload_len":139891,"header":14,"footer":8,"count":1567,"model":"variable",
   "row_rule":"[k × ([u32 len][UTF-8 name])][(65-4k)B 数值区][ordinal u32][UID u32][UID u32][marker 0]",
   "const_note":"常量 65 = (65-4k)+4k;等价表述:行长 == Σ name_len + 65,k∈{2,4}",
   "closure":"14 + Σrowlen + 8 == 139891;逐行复算 1567/1567 成立",
   "k_distribution":{"2":1446,"4":121},
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "ordinal_check":"ordinal == 行下标,1567/1567;UID 对相等;marker 全 0",
   "sensitivity":"DP(W13/f8)=1 路;W12/f9=1 路;f7/f10/f12=0 路",
   "payload_sha256":"9d73151026d706219a6c68eae485eef08a81b018c1b3170d922081334dc5c62d",
   "verified":True},
  "server":{
   "payload_len":149293,"header":14,"footer":8,"count":1567,"model":"variable",
   "row_rule":"同 client 但常量 71(而非 65);即 server 每行多 6B,位于数值区内、identity 之前",
   "closure":"14 + Σrowlen + 8 == 149293;逐行复算 1567/1567 成立(行长 == Σ name_len + 71)",
   "k_distribution":{"2":1446,"4":121},
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "ordinal_check":"ordinal == 行下标,1567/1567;marker 全 0",
   "server_diff":{"delta_bytes_per_row":6,"rows":"1567/1567 每行均 +6B",
     "data_side_evidence":"同一 ordinal 的 client/server 行,server 行在 identity trailer 前的 6B 处多出 6 字节;数值区常量 65→71。差异来源为 6B 插入,位置在 trailer 之前(数据侧观测,不判语义)",
     "sample_hex":"server 侧对应位置出现 43 00 4d 00 60 00 一类 6B 序列"},
   "sensitivity":"DP(W13/f8)=1 路;W12/f9=1 路;f7/f10/f12=0 路",
   "payload_sha256":"bc04b791930171eef8fabf5a680b636b6223336f07f9cf170fb48b124ebcd734",
   "verified":True}}}

d['tables']['47']={
 "entity":"local_region",
 "archives":{
  "client":{
   "payload_len":109505,"header":25,"footer":8,"count":2488,"model":"variable",
   "row_rule":"lcrg_tail:行长 = 41 + 5k(k>=0,行长 41/46/51/56/61/71/76)",
   "header_note":"25 = 标准 14 + 11B 扩展;count u32@8 仍为 2488",
   "closure":"25 + Σrowlen + 8 == 109505;2488 行全部 (len-41)%5==0",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "ordinal_check":"ordinal == 行下标,2488/2488;UID 对相等;marker 全 0",
   "sensitivity":"DP(W13/f8)=1 路;W12/f9=1 路;f7/f10/f12=0 路",
   "len_hist":{"41":1380,"46":878,"51":129,"56":79,"61":6,"71":14,"76":2},
   "payload_sha256":"a7f7d479d3a91a3ad08a1ad648555e11a59445b9e6dd9fda126889f6f4f10793",
   "verified":True},
  "server":{
   "payload_len":109505,"header":25,"footer":8,"count":2488,"model":"variable",
   "row_rule":"同 client(两档 payload 逐字节相同)",
   "closure":"同 client 2488 行闭合",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 marker@-1"},
   "sensitivity":"同 client",
   "payload_sha256":"a7f7d479d3a91a3ad08a1ad648555e11a59445b9e6dd9fda126889f6f4f10793",
   "verified":True}}}

json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('ok tables:',sorted(d['tables'],key=int))
