DONE type=t106

- 成员：13（server_db 12 + 独立 summary.dat 1）
- 字节精确闭合：13/13
- 解码载荷合计：28,432,613 B
- 记录/行合计：1,858,739
- name_table_0/1/2 行数：245,981 / 542,060 / 85,668
- name_table_extra_0/1/2 字符串数：245,981 / 542,060 / 85,668
- common_name_links 行数：12,056（sentinel 279）
- club_links 行数：9,261（常量字节位 23/47）
- simple_vars：34 B 前导 + 28,552 条 (u8 key,u8 len) 记录，169 个键码
- summary.dat：54,087 个 body + 11,004 B 尾块（63 个 (u32,f32) 对）
- table_for_old_save_23：278×14 B + 7 B 尾；table_for_old_save_25：7,047 变长行（唯一 DP 路径）+ 9 B footer
- fantasy_draft_future_regens：40 行 + 31 B 尾块

产出：`special_members_schema.json`、`REPORT.md`、`DONE.md`
