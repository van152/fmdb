import pathlib

p = pathlib.Path('scripts/t142_fk_graph_audit.py')
s = p.read_text(encoding='utf-8')

# 1) statistical rule: specificity is judged by support coverage, not by uid magnitude
old = '''    if (cand["target_key"] == "uid"
            and cand["uniform_chance"] <= UID_UNIFORM_MAX
            and cand["target_large_share"] >= UID_LARGE_SHARE_MIN
            and not low_spec
            and prof["distinct"] >= MIN_DISTINCT_STAT):'''
new = '''    if (cand["target_key"] == "uid"
            and cand["uniform_chance"] <= UID_UNIFORM_MAX
            and not low_spec
            and prof["distinct"] >= MIN_DISTINCT_STAT):'''
assert old in s
s = s.replace(old, new)

s = s.replace('UID_UNIFORM_MAX = 1e-4         # accidental hit chance of a random u32 draw',
              'UID_UNIFORM_MAX = 1e-3         # accidental hit chance of a random u32 draw')
s = s.replace('''UID_LARGE_SHARE_MIN = 0.5      # share of target uids >= 1e6 (non-sequential)
''', '')

# 2) compact the ambiguous records kept in stage 3
old_amb = '''                else:
                    rec["verified"] = False
                    ambiguous.append(rec)'''
new_amb = '''                else:
                    rec["verified"] = False
                    ambiguous.append(dict(
                        src_table=name, src_column=cname, src_col_id=cid,
                        src_offset=off, target=cand["target"],
                        target_key=cand["target_key"], tier=tier,
                        rows=prof["non_sentinel_rows"], distinct=prof["distinct"],
                        hit_rate=cand["hit_rate"],
                        support_coverage=cand["support_coverage"],
                        evidence=notes))'''
assert old_amb in s
s = s.replace(old_amb, new_amb)

old_sup = '''                    else:
                        rec["tier"] = "superseded"
                        rec["verified"] = False
                        rec["evidence"] = notes + ["superseded_by:" +
                                                   best["target"] + "." + best["target_key"]]
                        ambiguous.append(rec)'''
new_sup = '''                    else:
                        ambiguous.append(dict(
                            src_table=name, src_column=cname, src_col_id=cid,
                            src_offset=off, target=cand["target"],
                            target_key=cand["target_key"], tier="superseded",
                            rows=prof["non_sentinel_rows"], distinct=prof["distinct"],
                            hit_rate=cand["hit_rate"],
                            support_coverage=cand["support_coverage"],
                            evidence=notes + ["superseded_by:" +
                                              best["target"] + "." + best["target_key"]]))'''
assert old_sup in s
s = s.replace(old_sup, new_sup)

p.write_text(s, encoding='utf-8')
print('ok')
