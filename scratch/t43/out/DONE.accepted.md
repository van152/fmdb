# t43 DONE (commander-accepted)

状态:`integrated_data_base_fix_closed`。E80 `data_base` 修复已最小化集成进 `scripts/fm24_dump.py` 的 `load_payload`(仅此一函数,签名不变,不 import t38)。

- `fm24_dump --selftest`:49/0/1SKIP → **50 PASS / 0 FAIL / 0 SKIP**(server34 SKIP→PASS)。
- 79 数字表:`fm24_dump.load_payload` == `t38.load_payload_mf` == 独立 size-select 解码,**逐字节全等 79/79**,全 `len==entry.size`。
- 119 受影响条目(server2 / lang_update117)修后全闭合;旧法坐标 119/119 错 −25B。
- 方法论负例保留:42 个 lang_update 条目旧法字节巧合相同 12B stub(len/SHA 自检假阳,仅成员边界判据可识);server34 legacy=12B 负例不删。
- 独立 `verify.py --selftest` **19 PASS / 0 FAIL**;commander `scratch/cmd/t43_spot.py` **13/13**;`t01_anchors` **7/7**;t39/t34/t36 spot 全 PASS。
- `data_base=34` 结构含义仍候选(未 L3 exe 静态确认),仅操作性偏移。**L4=0**。

## 接受说明
devseek 三次 attempt 均 rc=124 超时(17:07→17:37→18:07→attempt3),交付实质(REPORT.md 18:02 / verify.py 19/19 / integration_report.json / build.py / fm24_dump.py fix 17:15 稳定)完整且经 commander 独立全 census 验证,但 `DONE.md` 哨兵未及写入。commander 据完整已验交付接受,记 **E86**,自写本 `DONE.accepted.md`。

## 关联
- 工作树 `scripts/t38_multiframe.py` 被另一会话纯增 +145 行(check#10/#11 无界选帧对照),非 t43 改动,HEAD 24 / 工作树 32 均 0 FAIL,另案 reconcile。
- 未启动游戏/编辑器/IDA,未联网,未读写 Z:。