# t22 · FM24 2430 国家表：`Ncpi`（Capital City）

**新增 1 个 L3 字段。** `client_db/table_10.dat` 的 `row+9`（十进制，4 字节小端）是 `Ncpi`，指向同版 `client_db/table_2.dat` 的 **零基城市行号**；`0xFFFFFFFF` 表示未设。不是城市永久 ID，也不是城市名字符串。编辑器资源把它称为 **Capital City**；这是游戏的字段名，不是要求城市的归属一定与原国家条目相同。

## 静态证据

来源：安装版 `Football Manager 2024 Editor/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`，与已按 `evidence/MANIFEST.json` 校验的 [静态来源登记](../evidence/fm24/reports/qa/IDA_PROVENANCE.md) 一致；对该 PE 原始字节用 Capstone 静态反汇编，未使用 IDA 或运行编辑器。以下地址均为该二进制的 VA；file offset 和原指令字节见[机读结果](t22_nation_capital.json)。

| 环节 | 证据 |
|---|---|
| 普通 client 行读取 | 在 `0x141040fb4`、`0x141040fd8`、`0x141040ffc` 连续读 `1+4+4` 字节。其后 `0x141041020` 取 `NATION+0xe8`，`0x14104102a` 传宽度 4，`0x141041033` 调流读取；因此本字段在 `row+9`。行原点沿用 t02-g2 的 251 行边界校验。 |
| `Ncpi` | `0x141042b44` 比较 4CC；通过条件后 `0x141042b74` 取 `NATION+0xe8`，`0x141042b80` 调 `0x140fe76a0`。后者从引用对象的 `+0xc`/`+0x10` 取两枚 u32（`+0x10` 为 0 时复用 `+0xc`），在 `0x140fe76d0` 显式传 `0x63697479`（`city`）给引用包装路径。没有把运行时包装后的 ID 当作磁盘编码。 |
| `Ncac`、`NcpR` | `0x141042ac5` 和 `0x141043264` 都取 `NATION+0xe8`。`Ncac` 经 `0x143e34390`，`NcpR` 在本分支内联：两者的打包输入及位操作相同，之后都调用 `0x140fead00` 包装。但空值/排除判断路径不完全相同，不能将所有返回行为视为等价；也不应计成三个磁盘字段。 |

字段名不靠 4CC 缩写猜测。直接从安装版 `Football Manager 2024/data/comp editor.fmf` 解出 `comp editor/format/database/nation.xml`，第 157–168 行的记录明写 `Ncpi` / `Capital City` / `database_record_unique_id` / `city` / `is_client_field=true` / `is_optional=true` / `duni not_equals=775`。这条定义在 **XML 注释**里（活动定义 0 条）；它证明字段名和目标类型，不证明当前界面提供编辑入口。完整资源成员的 SHA-256 和归档位置见 JSON。

### `775` 是谁，门控解释了什么

- `Ncpi` 在 `0x141042b5a` 起先有未知虚调用布尔门控，随后 `0x141042b65` 比较 `NATION+0xc` 是否等于 `0x307`（775），满足任一短路条件便到 `0x141043bc4`。`Ncac` 在 `0x141042ad6` 比较同一 ID，也判空；`NcpR` 的该分支只判空，没有这项 ID 比较。
- `duni=775` 在 2430 是 **Israel（国家行 149）**，原始 `row+9` 为 `ff ff ff ff`。这一门控作用于 getter；不能据此推断该条为何写成空、也不能把其余 19 个空值归因于这一检查。`775` 不在下列五个非空记录中。未知布尔门控和备用返回值不赋业务义。

## 语言表与数据交叉验证

- 只读解压 2430 `client_db.dat` 两个成员。`table_10` 的 251 行逐行闭合（`14+24,710+8=24,732`）；`table_2` 的 56,293 行逐行校验 ordinal、重复 ID 和边界字节。20 行未设；231/231 非空值按城市行号命中。把同一个整数当城市永久 ID 则只匹配 25/231，不能替代正确的连接。
- 城市名、国家名从英文语言成员 `8_2`、`8_9` 直接按持久 ID 对照：2400 基础层加 2430 更新层，有有效更新名时优先用更新。语言表编号 9 是国家名称表，不是对象表 `table_10`。六个未参与最早定位的对照（阿根廷、澳大利亚、巴西、德国、日本、美国）全部读到预期首都。
- 比较目标 `city row+10` 的国家行号，226/231 指回原行；其余 **5 条保留**，不能用城市归属关系过滤掉这些条目：

| 国家行 / duni | 数据库条目 | 目标城市行 / duni | 城市归属条目 |
|---|---|---|---|
| 69 / 124 | Macau (China PR) | 1291 / 103194 · Beijing | China PR |
| 83 / 138 | Chinese Taipei (China PR) | 1291 / 103194 · Beijing | China PR |
| 124 / 583 | Soviet Union | 7953 / 1301073 · Moscow | Russia |
| 248 / 62003815 | Yugoslavia | 8072 / 1301357 · Belgrade | Serbia |
| 250 / 82082540 | Netherlands Antilles | 1268 / 103135 · Willemstad | Curaçao |

后三条与历史首都相符；前两条只能确定数据库将其指向 Beijing，不从这些记录推断配置原因。五条都不改变字段定义，也不适合强制改为同国归属。

## 复验与限制

```powershell
py -V:3.12 -I -B scripts/t22_nation_capital.py --selftest
py -V:3.12 -I -B scripts/t22_nation_capital.py --dump-rows
```

本轮亲自复核安装包、程序指令及全表连接；DevSeek `deepseek-v4.1-flash-free` 做了 3 次窄范围审查，峰值并行 2。来自子代理的「返回城市名」及「775 返回显示文本」推断未采纳；它们不符合目前所见静态证据。首轮探针的原始负结果仍在 `scratch/t22-nation-entry/`。仅确认 2430 客户端这一字段；不晋升服务器布局、写回能力或 L4。
