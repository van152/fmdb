# t72 — 三主表未命名槽位清单 + 值域指纹(数据侧)— 验收报告(指挥官补写)

**status: partial(可验收)。** 两条核心交付(`inventory.json` + `fingerprints.json`)完整、自洽、与冻结事实交叉吻合;`verify.py`/`REPORT.md`/`DONE.md` 因 devseek 连续撞 40 分钟超时墙未及写出,由指挥官按 t53/t68 先例补写并记账 E112。第 2 波 t75 的输入不受影响。

## 交付内容

- `inventory.json`:三表全部物理槽位分类——club 34(unnamed 20 / l3_claimed 9 / held 5),comp 84(unnamed 36 / l3_claimed 32 / held 4 / collection_closed 12),nation 40(unnamed 24 / l3_claimed 5 / held 10 / identity_envelope 1)。10 项 `escalations` 全部是 nation 段内变长文法(A/B/C/D、Nftb 等),按上交纪律跳过,未硬猜。3 条 negative_notes 原样保留。
- `fingerprints.json`:unnamed+held 逐槽双档指纹——宽度直方图、首/末行 (row,absolute,raw)、distinct、zero/all-ones 计数与占比、u8/i8/u16/i16/u32/i32 解释域、值直方图、外键探针(1B 槽明确标"无判别力"不硬配)、xref_hint(只描述形态,不命名语义)。
- 行重放以 t57/t59/t55 冻结轨迹为基准:club/client 84,259 行、payload 6,932,082、header 13/footer 9、`coordinate_digests_matched=16`;comp/nation 同法。输入 11 个文件的 SHA-256 记录在 `inputs_sha256`。

## 指挥官 spot 检查(2026-11-21)

1. club selector 槽值直方图 `{0: 84,256, 12: 3}` —— 与 t57 REPORT 冻结事实"两档均有 84,256 条 selector 0、3 条 selector 12"精确一致。
2. `scripts/t72_slot_fingerprint.py --help` / `--selftest` PASS(独立复算路径存在)。
3. `grading_ceiling=L2/candidate`、`L4=0`、`inputs_sha256` 11 项——分级与溯源守约。
4. comp `collection_closed=12` 与 t66 已闭 7 文法+4 lane 的槽位口径一致,未重复下场。

## 局限(原样保留)

- 无独立 verify.py(builder 自带 selftest 代替);t75 反查时对将转正的槽位须按 t75 brief 自行全档复核。
- nation 段内 item 指纹缺位(10 escalations)——已由 t75(sol)接手范围覆盖。

## 复跑

```bash
export FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data
py -V:3.12 -I -B scripts/t72_slot_fingerprint.py --selftest
```
