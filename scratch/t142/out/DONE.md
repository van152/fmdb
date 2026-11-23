DONE type=t142b
DONE type=t142 (alias line, same audit: fm24 relational fk graph & integrity)

tables_audited: 84 (numbered 79 + special 5)
rows_decoded: 4,387,917
columns_inventoried: 1,740
columns_scanned: 1,337
verified_fk_edges: 44 (code_corroborated 22 + statistical 22)
verified_pair_proofs: 6
newly_decoded_col_N_fks: 24
orphan_rows: 764 (column edges 764 + pair edges 0)
ambiguous_candidates: 32,851
uid_overlapping_class_pairs: 1146

artifacts: fk_graph_master.json, REPORT.md, DONE.md, stage1_columns.json, stage2_domains.json, stage3_edges.json, cache/
--selftest PASS
