# t38 — 多帧感知 payload 加载器(devseek 基础设施,解 E66 阻塞)

先读 <WORKSPACE>\AGENTS.md。你是受指挥官委派的子代理。FM24 archive 成员常含**多 zstd 帧**:空 stub 首帧(count=0)+ 真实 payload 第二帧。现有 `scripts/fm24_dump.py:load_payload` 取**首帧**,导致 server table34 返回 12B 空 stub(真实 313082B 在第二帧)、client table3 有 28 帧需选 +34 真实帧。本任务建**独立多帧感知加载器**,为 sol 静态闭合(额度恢复后)与后续 dump 移除阻塞。**不修改 fm24_dump.py**(避影响既有调用者)。

## 关键判据(指挥官已核实)
目录条目(`codec["list_tables"]` + `codec["_resolve_table"](tid,ents,fn)`)含权威字段:
- **`size`** = 真实解压 payload 字节数(server34=**313082**,client3=**6932082**,server73=**45**)。**选帧判据:解压长度 == entry["size"] 的那个帧。**
- **`packed_size`** = 成员压缩区字节数,**界定成员边界**(帧枚举不得越过 offset+packed_size 进入后续成员)。
- `offset` = 成员起点;首 zstd MAGIC(28b52ffd)在 offset 起 64B 内(参 load_payload)。
- `sha256` / `record_count_header` / `payload_version` 可作辅助校验(先查 sha256 是否为 payload SHA)。

> **指挥官修正(E77,server34 实测)**:`packed_size` 是**真实帧**的压缩 size,**不是整个成员区**。多帧成员常有空 stub 首帧 precedes 真实帧(server34:hit-off=9,frame1 stub 12B,frame2 真实 313082B 压缩 size=89082=packed_size)。**用 `db[hit:off+packed_size]` 界定会截断真实第二帧**(实测 BOUNDED frame2=287410 eof=False,UNBOUNDED frame2=313082 a07b2bb7 eof=True)。正确做法:**无界 `db[hit:]` 逐帧解压,按 len==entry["size"] 且 SHA 匹配选帧**(后续成员帧不匹配无害),或按 **next member offset** 界定成员区。你的 --selftest 要求 server34→313082 会暴露此截断,务必用无界 size+SHA 匹配。

## 必读
- scripts/fm24_dump.py(load_payload/_reader/DB_DIR/MAGIC;**只读不改**)
- scratch/t29/out/subtable_inventory.json(t34 packed_offset/payload_size 313082/SHA a07b2bb7 先例,E66)
- scratch/t35/out/cafl_cvfl_discovery.json(client table3 28 帧选 +34 帧 6932082 SHA db8ea78c)
- scratch/t33/out/profiles/(7 表 payload_size/sha,多帧与单帧混合)
- scratch/cmd/t29b_spot.py + t33_spot.py + t35_spot.py(commander 多帧 pick_frame 参考实现;**注意其帧 walker 会越成员边界,你须用 packed_size 界定**)

## 任务
1. **scripts/t38_multiframe.py**:函数 `load_payload_mf(codec, archive, tid) -> bytes`:
   - 取 entry offset/packed_size/size;在 [offset, offset+packed_size) 内定位首 MAGIC;
   - 用 zstandard decompressobj 逐帧解压(unused_data 推进),**仅限 packed_size 边界内**;
   - 返回解压长度 == entry["size"] 的帧;若多帧同长则用 entry sha256(若是 payload SHA)或 record_count_header 消歧;无匹配则 raise(诚实失败,不返回首帧凑数)。
   - zstandard 在 <OLD_REPO>/tools/python(sys.path 插入);FM24_DB_DIR=<WORKSPACE>/scratch/data。
2. **--selftest**:验证 server34→313082(SHA a07b2bb7...)、client3→6932082(SHA db8ea78c...)、server73→45、server66→18094、server43→24632;**单帧表回归**:对 t33 七表 + t29 若干单帧表,load_payload_mf 结果与 load_payload 一致(单帧时首帧即真实帧)。
3. **--help**;退出码 0 成功/1 校验失败/2 用法或致命。单次打印 ≤400 行。
4. **REPORT.md**:多帧成员清单(哪些表多帧/首帧 stub 长度/真实帧相对偏移/size)、选帧判据验证、单帧回归结果、与 load_payload 差异表。
5. 独立 verify.py(不 import 加载器自身 selftest,从 archive 复算选帧;ROOT=parents[2] 若需仓根)。

## 纪律
- 只读 scratch/data/ + 仓内证据;**只写 scratch/t38/out/ 与 scripts/t38_*.py**;**不改 fm24_dump.py 及其他 scripts**(指挥官后续决定是否集成)。
- 负结果保留(无匹配帧如实 raise);不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 候选不写结论;帧消歧依据须落盘证据。

## 交付 scratch/t38/out/
- multiframe_report.json(多帧成员清单+选帧证据)、REPORT.md、verify.py、DONE.md
- scripts/t38_multiframe.py

Python `py -V:3.12 -I -B`;完成跑 --selftest(须 PASS)+ 自己的 verify + t01_anchors.py(7/7)。打印交付清单。