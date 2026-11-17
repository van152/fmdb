# 外部只读引用

本工作区不复制大资产;以下路径一律只读。

## 旧证据库 `D:\tmp2b\fm24`(冻结,2026-11-18 起不再写入)

已快照进 `evidence/fm24/`(见 `evidence/MANIFEST.json` SHA-256)的除外,其余按原始路径引用:

| 路径 | 用途 |
|---|---|
| `reports/dbdat_decode/people_evidence/`、`reports/dbdat_decode/ida/` | 人物证据与伪代码子目录(未快照) |
| `reports/reverse_engineering/`(86 份伪代码 + `ida_focus_results.json`) | L3 侦察起点 |
| `reports/editor_schema/`(其余)、`reports/editor_gen/*_evidence/` | schema 与生成器证据 |
| `scripts/`(`modding_read_dbdat.py`、`modding_db_names.py`、`b47_tables_big.py` 等) | 旧解码器,按需回链复用,不搬运 |
| `reports/qa/REGRESSION_BASELINE.json` | 旧回归基线(参考) |

## IDA / 二进制

| 路径 | 说明 |
|---|---|
| `D:\tmp2b\fm24\ida\editor_merge_v2.i64` | editor.exe IDA 库(501MB,不复制;IDA 会话产物只写 scratch) |
| `D:\tmp2b\fm24\input\editor.exe`、`D:\tmp2b\fm24\input\fm.exe` | 静态分析对象 |
| `D:\tmp2b\fm24\reports\qa\IDA_PROVENANCE.md`(已快照) | L3 来源登记规则,引用 exe 地址时必须遵守 |

## 游戏安装库(只读)

- `Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\`
  - `client_db.dat`、`server_db.dat`、`lang_update_db.dat`、`people_db.dat`、`basic_people_db.dat`、`summary.dat`、`pl_hist_*`、`non_pl_hist_*`

## 范围外

- `D:\tmp2b\fm27\`:FM27 研究,独立项目,不在本工作区操作范围。
