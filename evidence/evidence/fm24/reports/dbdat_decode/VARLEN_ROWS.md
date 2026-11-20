# 变长表行边界与 `table_extra_*`：静态调查

> **b47 后续补充（2026-11-17）：**本文关于 table_3 84,250/84,259 的边界限制仍成立；b47 将差异交叉定位到 table_extra_3 在 named-candidate index 84249 后的 9 个终端辅助 ordinal，但其 Club 身份和主表切片仍未分配。Club 字段新增 6 个 L2 命名候选，并有 Csti 单样本候选与 Crep/坐标负探测；当前结论见 [`DB_TABLES_BIG.md`](DB_TABLES_BIG.md)。以下为原始 b17 记录，不应覆盖后续字段级结论。

## 结论摘要

- **强假设不成立（按“table_extra_N 是行偏移/长度索引表”解释）**。两库中的 extra 项头部 count 都与对应 table_N 的 count 相同，但内容尺寸远超 `count×4` / `count×8`，样本字节也不像偏移序列。更像与主表同 count 的辅助/扩展负载；`table_extra_24` 甚至精确满足 `12 + 82×84507`，像 82-byte/row 的固定宽度扩展区。**不能把这些文件当作通用 row-offset 索引。**
- **替代证据：table_3 的身份/名称锚点可以切出样例行，但还不是经全表验证的通用 serializer。**重复-u32 DUNI、紧随的长度前缀 UTF-8 名称和 table_24 同 DUNI 链共同找出 84,249 个单调锚点；另有 table_3 首行的特殊前缀，总共切出 84,250 个候选片段，对照 header 的 84,259 行尚差 9 行。因此全表边界仍未闭合。前 20 个连续片段及 Liverpool/Manchester City/Arsenal 等行通过边界、名称和 ID 交叉检查。
- `--fields` 输出 11 个 Club schema **字段候选**：2 个高置信、5 个中置信、4 个低置信。`Cyfn` 成立年、球衣颜色、`Club.Csti`、声誉和坐标尚未可靠解码；不能宣称字段全解。
- `people_db.dat` 前 20 条可按名称长度和尾部重复身份字段连续切分，确实呈现人物姓名；其类型/尾部语义和历史数组未解。

## 1. Extra 条目清单与假设检验

下表尺寸为解压后的 `.dat` payload 尺寸；count 读自 payload offset 8 的 u32。

| Archive | Extra 项 | Extra bytes / count | 对应 table_N bytes / count | 观察 |
|---|---|---:|---:|---|
| client | `table_extra_3.dat` | 13,053,908 / 84,259 | `table_3.dat` 6,932,082 / 84,259 | count 相同；extra 平均约 154.93 bytes/row，不是 count×4/8 |
| client | `table_extra_9.dat` | 83,927 / 251 | `table_9.dat` 31,956 / 251 | count 相同；extra offset 16 处有长度 11 的 UTF-8 字符串 `Les Fennecs` |
| server | `table_extra_3.dat` | 35,009,248 / 84,259 | `table_3.dat` 16,595,312 / 84,259 | count 相同；extra 平均约 415.50 bytes/row，不是 count×4/8 |
| server | `table_extra_9.dat` | 105,228 / 251 | `table_9.dat` 307,564 / 251 | count 相同；同样能读到 `Les Fennecs` 字符串 |
| server | `table_extra_24.dat` | 6,929,586 / 84,507 | `table_24.dat` 8,819,030 / 84,507 | count 相同；`size = 12 + 82×count` 精确成立，候选为 82-byte 扩展记录/row |
| client/server | `table_extra_21.dat` | **不存在** | table_21 是已验证固定步长表 | 没有固定步长表的 extra 对照项 |

尺寸检查覆盖了 2/4-byte 长度数组、8-byte `(offset,len)` 数组、count 与 count+1 项的 offset 数组，以及带 12/14-byte 头、0/8-byte 尾的简单形式，均不匹配。server `table_extra_3` offset 12 起的首批 u32 为 `0, 1795, 256, 256, 16777216, 17263616`；若当作 table_3 offset/len 对，`16777216` 已越过主表 16,595,312-byte payload 的边界，序列也不单调。server `table_extra_24` 同位置是 `0, 0xffffffff, 0, 10000, ...`，不构成有效偏移对。特别是 `table_extra_9` 开头可直接解出字符串、而 `table_extra_24` 的 body 有 82-byte/row 算术，这些都与“统一偏移/长度索引”不相容。

**范围限定：**这证伪的是 extra 文件作为简单、通用 row-offset/row-length 表的强假设；不能排除某个 extra 文件内部另有复杂索引或 per-row 辅助字段。`table_extra_3/9/24` 的完整内部 serializer 仍未恢复。

复现：

```powershell
python -I scripts\modding_varlen_rows.py --inspect-extras
```

## 2. table_3 候选边界与 20 个连续 Club 片段

### 候选边界规则

server `table_3.dat`：count 84,259，size 16,595,312 bytes，数据区为 header 后的变长串流；不满足固定 stride。当前候选扫描器：

1. 扫描长度前缀 UTF-8 名称；
2. 检查名称前 39/40 bytes 的 repeated-u32 候选是否也出现在 server table_24；
3. 以 identity 值的长单调序列筛出主要名称锚点，并对一字节重叠候选保留实际 DUNI 位置；
4. 特殊处理 payload 首行（offset 14 起，DUNI 在 row-relative +8）；其余样例 DUNI 位于行片段起点，主名称紧随其后。

例：首行片段 offset `14..203`；Apolonia offset `203..450`，DUNI `57`，名称 payload 在 row-relative `+39`；Manchester City offset `282309..283805`，DUNI `173568`，名称 payload 在 `+40`。这对样例支持“DUNI/name anchor 是行起点线索”，但不等价于完整通用行 serializer。

前 20 个连续候选切片（坐标是 `table_3.dat` payload offset）：

| # | Club DBID 候选 | 名称 | 短名候选 | start..end | bytes | Nation 候选 | City 候选 |
|---:|---:|---|---|---:|---:|---:|---:|
| 0 | 126 | Klubi i Futbollit Albpetrol Patos | KF Albpetrol | 14..203 | 189 | 首行特殊布局 | 7615 |
| 1 | 57 | Klubi i Futbollit Apolonia Fier | KF Apolonia | 203..450 | 247 | 126 | 7623 |
| 2 | 58 | Klubi Sportiv Besa Kavajë | KS Besa | 450..624 | 174 | 126 | 7620 |
| 3 | 59 | Klubi Sportiv Besëlidhja Lezhë | KS Besëlidhja | 624..811 | 187 | 126 | 7614 |
| 4 | 60 | Klubi i Futbollit Tirana | KF Tirana | 811..1105 | 294 | 126 | 7618 |
| 5 | 61 | Klubi i Futbollit Elbasani | KF Elbasani | 1105..1279 | 174 | 126 | 7630 |
| 6 | 62 | Flamurtari Football Club | Flamurtari | 1279..1522 | 243 | 126 | 7624 |
| 7 | 63 | Klubi i Futbollit Iliria Fushë-Krujë | KF Iliria | 1522..1706 | 184 | 126 | 7617 |
| 8 | 64 | Klubi i Futbollit Shkumbini | KF Shkumbini | 1706..1886 | 180 | 126 | 7621 |
| 9 | 65 | KS Shqiponja Gjirokastër | Shqiponja | 1886..2045 | 159 | 126 | null/未解 |
| 10 | 66 | Futboll Klub Tomori Berat | FK Tomori | 2045..2224 | 179 | 126 | 7627 |
| 11 | 67 | Klubi i Futbollit Laçi | KF Laçi | 2224..2448 | 224 | 126 | 7616 |
| 12 | 68 | Futboll Klub Partizani Tirana | FK Partizani | 2448..2830 | 382 | 126 | 7618 |
| 13 | 69 | Klubi Futbollit Olimpik Tirana | Olimpik Tirana | 2830..3011 | 181 | 126 | 7618 |
| 14 | 70 | Klubi Futbollit Teuta Durrës | KF Teuta | 3011..3257 | 246 | 126 | 7619 |
| 15 | 71 | Klubi i Futbollit Vllaznia Shkodër | KF Vllaznia | 3257..3564 | 307 | 126 | 7613 |
| 16 | 72 | Atlético Petróleos de Luanda | Petro Luanda | 3564..3851 | 287 | 1 | 1188 |
| 17 | 74 | Clube Desportivo Primeiro de Agosto | 1º Agosto | 3851..4237 | 386 | 1 | 1188 |
| 18 | 75 | Estrela Clube 1º de Maio de Benguela | 1º Maio Benguela | 4237..4468 | 231 | 1 | 21629 |
| 19 | 76 | Asociación Atlética Argentinos Juniors | Argentinos Jrs. | 4468..5484 | 1016 | 187 | 1110 |

这些是连续候选片段，并非对 84,259 行完整覆盖后的证明。当前总计输出 84,250 个候选片段，header count 尚差 9；未找到这些遗漏行的通用边界。其余边界不应被当作最终 row index 使用。

## 3. Club 字段试解与人工合理性核对

schema 来源 `reports/editor_schema/master.json` 的 `club.xml`。当前 `--fields` 输出 11 个字段候选，置信层次如下：

| 字段 | 候选证据 | 置信度 |
|---|---|---|
| `duni` | row anchor repeated-u32，低/高 u32 相等；Manchester City `0x0002a6000002a600` | 高 |
| `dbnm` | anchor 后首个长度前缀名称；与查询名一致 | 高 |
| `Csnm` | 第二个长度前缀名称；20 行样例中是常见短名形式 | 中，字段归属仍需 serializer 证据 |
| `Cnti` | row 前缀内重复的小型 ID；例：England 139、Albania 126、Angola 1、Argentina 187 | 中/候选 |
| `Cbni` | 同一前缀窗口有 `0xffffffff` sentinel，候选为 optional null | 候选 |
| `Cccn` | 重复国家 ID 与 schema 的 Continental Cup Nation 字段相符 | 候选，具体槽位未证 |
| `Ccty` | 名称前 14 bytes 的 u32 候选；Albania 城市候选 7613–7630，England 1040/1061/1075，Angola 1188，Argentina 1110 | 中/候选，城市表本体未在本轮验证 |
| `Clri` | `Ccty` 后的 u16 候选 | 低 |
| `Cext` | 附近 byte 的低位 boolean 候选 | 低；不能据此断言生灭状态 |
| `PLgn` | 附近 u16 enum 候选 | 低；未与 enum 表对齐 |
| `Cedp` | 附近 byte 候选 | 低；未用 MLS 对照验证 |

其中 Cnti/Cbni/Cccn/Ccty 的槽位和值都标为候选；尤其 `Ccty` 的城市合理性核对并不等同于读取了 table_2 城市行。`Cext/PLgn/Cedp` 只是 raw 邻接槽位假设，不应拿去写数据库。

### Manchester City / Liverpool / Arsenal 静态核对

| Club | Club DBID / row slice | Cnti 候选 | Ccty 候选 | 已验证 Team.Tsti → Stadium | known fact核对 |
|---|---|---:|---:|---|---|
| Liverpool | 172800 / `278532..281035` | 139 | 1061 | rdui 67 → DBID 676 | Anfield 坐标/容量在上一份 `CLUB_STADIUM.md` 核对；Ccty 名称合理 |
| Manchester City | 173568 / `282309..283805` | 139 | 1075 | rdui 7716 → DBID 5114325 | Etihad 坐标/容量核对；Ccty 名称合理 |
| Arsenal | 153856 / `210032..211427` | 139 | 1040 | rdui 7718 → DBID 5114336 | Emirates 坐标/容量核对；Ccty 名称合理 |

成立年份（Liverpool 1892、Manchester City 1880、Arsenal 1886）、颜色字段、Club.Csti、声誉与经纬度**尚未从 table_3/table_extra_3 中定位**。stadium 映射仍来自已验证的 Team.Tsti 路径，不是 Club.Csti 二进制字段解码。本轮没有声称这些属性已完成。

复现：

```powershell
python -I scripts\modding_club_stadium.py --club "Manchester City" --fields
python -I scripts\modding_club_stadium.py --club Liverpool --fields
python -I scripts\modding_club_stadium.py --club Arsenal --fields
```

## 4. people_db.dat 能力试验

`people_db.dat` 安装文件 67,502,767 bytes，外层头 `03017461642ef10d`，offset 8 处直接 Zstandard frame；frame 未提供解压总尺寸。本轮没有全量解压，只流式读取解压前缀 1 MiB。前 6 bytes `00005b0a0a00` 暂作为未解 preamble；之后 20 条连续片段满足同一结构候选：

```text
u32 identity-key
u32 type-candidate (=5 in these 20)
u8 unknown
u32 name-length
UTF-8 name
8 zero bytes
u32 repeated identity-key
u64 repeated-u32 tail-candidate
```

例如首条 `Zarko Serafimovski`：payload offset `6..57`（51 bytes），identity key 候选 657483，name length 18；尾部再次出现 657483，随后 `0x7754bb3d7754bb3d`。第 2 条 `Ronny Pattinasarani` 位于 `57..109`，长度 52。20 条边界都连续，名字呈人物姓名形态，身份重复检查通过。

**能力边界：**目前只验证了 people_db 前缀中的身份/名称片段；type 与 tail 的语义未证，未找到/解析历史数组，也没有声称这就是每个人的完整业务记录。不能据此批量解析整个 people_db。

复现：

```powershell
python -I scripts\modding_varlen_rows.py --people-sample
```

## 5. 未解项与安全范围

1. table_3 候选切片目前 84,250/84,259；全表精确边界仍差 9 行。`table_24` 通用边界也未恢复。
2. `table_extra_3/9/24` 的字段 serializer 和 per-row 对应关系未解；不能把 count 相同当作偏移索引。
3. Club schema 虽输出 11 个字段候选，但成立年、颜色、`Club.Csti`、声誉、坐标没有可靠值；低置信候选不应用于写库。
4. people_db 历史数组及完整 row 语义未解。
5. 只读游戏安装库及工作区文件；没有修改 `modding_read_dbdat.py`，没有写游戏目录或用户 Documents，没有启动 FM24/Pre-Game Editor。所有结论都是静态证据，未做实际加载验证。
