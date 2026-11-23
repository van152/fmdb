# t01-e: 实体定义类虚表枚举(H3 验证)—— 12/32 实体 slot6→注册函数确认

产物: `scratch/t01/t01e_vtables.json`(vtables=确认表 / forward_scan / reverse_refs / unmatched_clusters / slot6_unmatched / spot_checks)
脚本: `scripts/t01e_vtable_enum.py`(py -V:3.12 -I 可复跑;纯 stdlib+capstone)

## 方法与判定修正
- 判定修正:字面"44 项全在 [0x140001000,0x150000000)"会**漏掉锚点本身**(0x187d2b0 slot43=0x0,字节见 JSON);主判据改为 **43 个在域指针 + null 终止**。4B 对齐控制扫描 = 0 run(8B 对齐充分)。
- 正向:debug 区 0x1758600..0x1a7d000 共 595 个 ≥40 指针 run;63 个 43+null 主候选。
- 反向(主力):全文件指针索引,对 t01a 245 个注册块/簇 VA 在 block-0x80..+8 查引用;引用目标须字节验证为函数起始(3 种 prologue 变体,见下)——过滤掉 11 个指到函数中段/填充的伪引用(pers/nnpl/ktfl 因此未确认)。

## (a) 虚表↔实体映射 —— 14 行 / 12 实体(32 实体中)
全部 slot6 指向字节验证的注册函数起始,cont 0.75..1.0:
- 43 ptr+null 锚点形 5 张:awar 0x187ae20、**comp 0x187d2b0(锚,slot6=0x140ebfa40 复现)**、drbr 0x1886870、inju 0x1881d30、weat 0x18823e0(嵌于 89-run 的 slot 46..88,slot0=0x141882f40)
- 非 null 终止形:stad 0x188d1d0、mdso 0x18bd300(43 指针,后随 float/字符串数据);club 0x187c300+0x18bf1f0、nati 0x1888ed0+0x188db40(68 槽,slot2=0x1407eb2d0 与锚点同值,同族确认)
- 大槽位形:agen 0x18b56a0、offc 0x18bfc50、jour 0x18c5360(243 槽 run,slot6=注册函数)——**H3"同构 44 项"不成立:槽位数随实体变化,不变量是 slot0=debug 区 col 指针、slot6=注册函数**
- 3 种 prologue 变体(块起始-fn起始):V1 -0x20 `55 56 57 48 83 ec 40`(9 实体)、V2 -0x24 `55 56 57 53 48 83 ec 38`(club)、V3 -0x29 `55 41 56 56 57 53 48 83 ec 40`(agen/offc/jour)

## 抽验(capstone,4 张含 3 种变体)
awar 0xe49090→AWna/AWsn/AWci ✓;club 0xe87d50→Cnam/Csnm/Csxn(`c7 45 f8` 形)✓;agen 0x1435760→Abnt/Ascp/Apat ✓;comp 0xebf040→PLgn/cnam/csnm ✓——均为 55 56 57[53|41 56]前奏 + c7 45 <d8> <imm32> 块 + `48 83 c0 38`。

## (b) 未被 slot6 指到的簇:161/175(.rdata 104/.reloc 57)
high/medium 19 个:pers 三段(0xde7a42/0xdfc1f0/0x1199290)、ktfl 三段(0xeab22a/0x11fa3e7/0x132576e)、nnpl 0x13f44c0、nati 0x153128b、cont 0xedae95、club 弱簇 0xe850f8/0x11f6fa2 等——注册函数分段化,段函数无 slot6 引用(调用者疑在壳区/.arch,负结果如实记)。

## (c) 有虚表但 slot6 不匹配的:59 张主候选
- 46 张 slot6→桩(xor eax,eax;ret / mov al,1;ret @0x1400015a0/15b0/15e0/1000)→ 抽象/接口基类族,非实体表
- 13 张 slot6→其它代码(如 ~296 张同族表共享 0x1401f4ef0,有函数无注册签名)→ 其它类族,负结果
- .reloc 交叉核对(VA=off+0x16B600):**0 命中** ——这 59 张与 .reloc 注册子系统无关联

## 移交阶段二的锚点
1. nnpl 注册函数 0xdc6780(block-0x24,V2 形)有引用但不落在 fn 起始(slot15=fn 起始的表在 0x18765b0 run,slot6 另有所指)→ nnpl 表结构 unknown
2. pers/ktfl 全文件无 fn 起始引用 → 表可能未在明文区(壳/.arch)
3. 243-run(agen/offc/jour)与 762-run(pers 区 0x1943440,内含 0x1944520 pers 引用@slot540)的内部边界未解——疑多表拼接,值得阶段二切分
4. 4 张 slot6 非 fn 起始引用(nati fn-0x10 ×4 表共享)→ 该槽或为数据指针/哨兵,unknown
