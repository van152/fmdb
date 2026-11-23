DONE type=t127b
task=t127 (Playing History 3-file system) status=complete supersedes=none
files=pl_hist_index.dat(3,081,975B)+pl_hist_id.dat(4,124,656B)+pl_hist_dt.dat(56,996,116B) header_prefix=03 01 74 61 64 (tags index=0x0df1 id=0x0001 dt=0x0003)
players_indexed=515,581
career_rows=4,515,803 (stride 44B, mean 8.759/player, max 57)
closure_diff=0 (dt 198,695,332 B == sum of 515,581 contiguous blocks)
linkage: offsets_in_bounds=True misaligned=0 contiguity_violations=0 rows_accounted_eq_dt=True
chain: links=4,000,222 terminators=515,581 malformed=0 closed=True
index: uid_strictly_increasing=True ordinal_col_is_position=True
row_layout: 44B verified fields = year_from/year_to, apps, goals, fee_gbp, club_id, comp_id, join(day,year), leave(day,year), next_row; duplicates club_id_dup/comp_id_dup identical 100%
dt_framing: 48,510 zstd chunk frames (4,096B each, last 2,468B) + 1 skippable chunk-table frame (0x184D2A5E, 12B records, compressed+decompressed sizes match 48510/48510)
stars_decoded=5 Harry Kane(18 rows), Lionel Messi(24 rows), Cristiano Ronaldo(26 rows), Kevin De Bruyne(22 rows), Kylian Mbappe(10 rows)
correction=id pair is INCLUSIVE [first,last] -> earlier dump undercounted by 1 per player (Kane 17->18, Messi 23->24, Ronaldo 25->26)
--selftest PASS
deliverables=scripts/t127_pl_hist.py, scratch/t127/out/pl_hist_schema.json, scratch/t127/out/REPORT.md, scratch/t127/out/DONE.md
