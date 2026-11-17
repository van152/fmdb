# t01-j 任务书:basic_people_db.dat 侦察 —— person 家族的行仓库

> 交给 pi gpt-6-luna max。t01i 证明 factory type-id ≠ archive 表 ID 的天真假设:client/server 主 archive 都无 table_1,而 BASIC_PERSON(factory type 1)reader 存在。指挥官补充的独立事实:**server_db.dat 59 表 ID(0..73 缺 {1,4,11,13,14,15,16,17,20,28,40,53,54,55} 中的 11 个 null-return + {1,4,14,44})与工厂 74 项跳表几乎互补吻合** → BASIC_PERSON 行极可能在独立文件 `basic_people_db.dat`。
> 规则不变:只读输入、不启动游戏/编辑器/IDA、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 已知锚点

- `Z:/.../2430/2430_fm/basic_people_db.dat`:12,934,775 B,头 `03 01 74 61 64 2e f1 0d 28 b5 2f fd`(tad. 容器 + 紧随 Zstd 成员)—— 与主 archive 同构
- 容器解析:旧库 `scripts/modding_read_dbdat.py` 的 `_entries/_archive_layout/_decompress_entry`(t01i 已用其解析 client 目录成功);若该文件目录结构有差异,以字节证据为准并给差异
- BASIC_PERSON 静态锚(t01h/t01i 已核):跳表项 `0xf49d3c: da ef ff ff` → handler 0xf48d12 → alloc 0x70(wrapper `mov edx,0x70`)→ RTTI `.?AVBASIC_PERSON@db@@`(0x1aac700,vptr 0x187b328);slot19 reader `0x187b3c0: 70 fd e4 40 01 00 00 00` → `0xe4f370`,straight-line,首宽 `0xe4f393: 41 b8 01`
- 主 archive 参考:client 20 表/31 项,server 59 表/77 项(t01i output.json 有全 ID 列表)

## 任务(按序,一条线走穿)

1. **目录枚举**:basic_people_db.dat 的 FMF 目录帧定位(`02 01 66 6d 66 2e 08 00 00 28 b5 2f fd` 模式,参照 t01i 报告的 client 帧位置 0xc81799)、解压目录、列出全部条目与数值表 ID;与主 archive 目录结构逐字段对比(同构性)
2. **行框架**:选 ID 最接近 person 的表(或唯一表),用 t01f/t01g 的方法恢复:count、行起公式、stride(若变长,给模式);payload 总量封口校验
3. **BASIC_PERSON 呼应**:把 reader 0xe4f370 的 27 条宽度指令序列与行字节逐段对照——若行内字段宽度序列与 reader 一致,BASIC_PERSON 行仓库假设成立(L3);不一致则如实记录差异
4. **身份块**:找 duni/rdui/行序号模式(comp/nation 先例);抽 5 行验证

## 验收判据

- 目录全枚举(条目数、数值表 ID 列表)+ 至少一张表的行框架(行起/stride/count 封口)→ 即使 BASIC_PERSON 假设不成立也算达标;
- 加分:宽度序列与 reader 对齐 + 5 行抽验 → person 行仓库实锤;
- 或负结果:文件结构与 tad. 容器不同构,给出真实结构描述。

## 交付

`scratch/t01/inbox/t01j/`:`output.json`(目录+框架+对照)、`REPORT.md` ≤100 行、`verify.py --selftest`(只读,含正负对照)。

## 纪律

深度优先;45 分钟无进展记录现状换线;勿重做 t01f/g/h/i 已证部分;候选不写成结论。
