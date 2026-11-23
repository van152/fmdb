import json
p='scratch/t74/out/frames.json'
d=json.load(open(p,encoding='utf-8'))

t24 = {
 "entity":"team",
 "archives":{
  "server":{
   "payload_len":8819030,"header":14,"footer":8,"count":84507,"model":"variable",
   "row_rule":"[变长字段区][ordinal u32][UID u32][UID u32][selector 1B];行长 86..666,均值 104.358",
   "closure":"14 + Sigma(rowlen) + 8 == 8819030,84,507 行逐行铺满到 footer(唯一 DP 路径重建)",
   "identity":{"width":13,"anchor":"row_end-13","layout":"ord@-13 uid@-9 uid@-5 selector@-1",
     "selector_not_marker":"第 13 字节不是 0:selector 10 -> 84,256;11 -> 250;0 -> 1。故本表不能套 t0/t7/t8 的 marker==0 约束"},
   "ordinal_check":"ordinal == 行下标 0..84,506,84507/84507",
   "uid_check":"UID 对相等 84507/84507;UID 严格递增 84,506/84,506 相邻对",
   "sensitivity":"W13/f8=1 路;W12/f9=1 路;W14/f7=1 路;其余 (W12/f7/f8/f10/f12)、(W13/f7/f9/f10/f12)、(W14/f8/f9/f10/f12) 全 0 路。三路互不等价,取 W13/f8(与全仓其余表一致,且 13B 含 selector 语义位)",
   "ambiguity_resolution":"约束 = UID 对相等 + 相邻行 UID 严格递增。plain(W13/f8)得 4 路;加入 UID 严格递增后唯一;W12/f9 同 1 路",
   "rowlen_hist_distinct":269,
   "first_identity_at":133,
   "selector_crossref":"t39 REPORT 'Team selector {10,11}' 与 factory case 24 full-team arm(0xf49106, BL=11 -> NATIONAL_TEAM)方向一致;本任务只记录数据侧分布,不做 exe 断言",
   "payload_sha256":"72371cf99753cb4d54292584427dea8bfa503af013f7873f5327de6f48c95556",
   "verified":True},
  "client":{
   "status":"absent",
   "reason":"t66 已证 client 无 table_24 entry(双档目录 460 条中 client 侧缺失);本次 load_payload 亦取不到,按'无条目'处理,不伪造空行框"}}}

d['tables']['24']=t24
d['summary']={
 "tables_verified":["0","7","8","18","21","24","27","47","56"],
 "archives_verified":[[a,int(t)] for a,t in [("client",0),("server",0),("client",7),("server",7),
   ("client",8),("server",8),("client",18),("server",18),("client",21),("server",21),
   ("server",24),("client",27),("server",27),("client",47),("server",47),("client",56),("server",56)]],
 "escalations":[],
 "upstream_conflicts":[
   {"table":27,"upstream":"opaque middle 99B","ours":"95B middle + 13B identity = 108B","basis":"逐行闭合 334/334 且 footer 精确对齐"},
   {"table":47,"upstream":"25+2488*44+8","ours":"25 + sum(41+5k) + 8,rowlen 41..76","basis":"已有 OVERRIDE;本次双档独立复算 2488 行全部 (len-41)%5==0"},
   {"table":24,"upstream":"E37 82B 定长被否;均值 104.36B","ours":"变长 86..666,均值 104.358","basis":"84,507 行唯一铺法闭合"}],
 "double_archive_identical_payloads":["0","8","27","47","56"],
 "double_archive_different":[
   {"table":7,"client":36824,"server":38280,"delta_per_row":7,"rows":208},
   {"table":18,"client":139891,"server":149293,"delta_per_row":6,"rows":1567},
   {"table":21,"client":1839716,"server":8762775,"stride":[38,181]},
   {"table":24,"client":None,"server":8819030,"note":"client 无 entry"}]}

json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('tables:',sorted(d['tables'],key=int),'arcs:',len(d['summary']['archives_verified']))
