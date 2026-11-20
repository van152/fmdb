# t48 REPORT — schema v4(Cafl/Cvfl 并 CLUB_LINK 共享 auxiliary)

**状态:accepted(E88)。v4 实质由 luna(gpt-6-luna/hiyo-key2)在指挥官收尾停止前完成;REPORT/DONE 由指挥官补写。**

## 交付
- `reports/club_nation_subtable_schema.json` + `.md`(v4,in-place 演进;md 340 行)
- `scratch/t48/out/consolidate_v4.py`(--help/--selftest;SELFTEST PASS)
- `scratch/t48/out/verify.py`(独立,不 import builder;VERIFY PASS rc0)
- `scratch/t48/out/club_nation_subtable_schema.v3.json` + `.v3.md`(v3 快照,JSON SHA 81efb123da581540)

## v4 内容
- **v3 八表 verbatim 保留**(Cstc22/Clhs37/CSrs62/Cmti43/CNtp66/Cdbt33/Tchl34/Csme59);v4 tables == v3 snapshot tables(逐字节)。negative_regressions 4 verbatim。
- **CLUB_LINK 共享 named auxiliary POD**(t44 E84):`server_db/club_links.dat`,table_type=null,无 RTTI/vptr/slot19/factory case。9261 行 × 47 B,payload 435279 B,closure `12 + 9261*47 + 0 = 435279`。payload SHA 8933328064b13a9d / row_block 17a167f0 / compressed 894f1efb / packed 63944(全吻合 E84)。
- **Cafl/Cvfl 两视图**:Cafl 29 occurrence(idx370-398),Cvfl 19(idx400-418)。grades:Cafl{L3:26, held_all_missing:1, held_domain_conflict:2},Cvfl{L3:16, held_domain_conflict:2, runtime_only_no_wire_slot:1}。
- **dual accounting**:
  - club_L3_fields = 52(v3 numeric-table scoped,verbatim 保留)
  - club_L3_occurrences = 94 = 52 + 26 Cafl + 16 Cvfl
  - club_L3_unique_wire_fields = 59 = 52 + 7 CLUB_LINK 物理 wire 单元(affl/ismc 共 endpoint lane 不加槽;20 bool 共一个 u32 wire word 计 1;Cvfl.clfr 无 wire slot 排除)
  - held_fields = 21 = 16 v3 + 3 Cafl + 2 Cvfl(unique CLUB_LINK held 坐标 3:type/yfee/msls)
  - L4 = 0
- **t46 nation 数据侧已并**:server table_10 251 行 SHA 19337841,row_block 4162770e,A_B_C_D internal grammar open,new_L3=0。nation_side t37 inventory partial,new_L3_claims=0。

## 验证
- consolidate_v4.py --selftest:PASS(v3 八表 verbatim;94 occurrences;59 unique-wire;CLUB_LINK closure/coordinate policies;held/runtime exclusions;t46 L3=0)。
- verify.py:VERIFY PASS rc0。
- **指挥官独立 spot `scratch/cmd/t48_spot.py`:43/43**(不 import builder;独立重解码 club_links.dat 验 payload/compressed/row_block SHA + count@8=9261 + closure;v3 tables verbatim 比对;dual accounting 算术;t44 grades;negatives;t46 status;anchors 7/7)。

## 边界 / 待办
- v4 scope 早于 t47:**Ntxr 7 L3(t47 E87)尚未并入 nation_side**;t49 t9 wire 验收未做。下一 **v5** 应并 t47 Ntxr + t49 t9 结果。
- 候选/held 不升级;negative 原样保留;L4=0;未跑游戏/编辑器/IDA。