DONE type=t141

status: complete
generated_utc: 2026-11-22T19:40:20Z
elapsed_sec: 41.04

## RTTI counts (strict `.?AV…@@` descriptors, whole-file scan)
fm_exe_descriptors_unique: 7538
editor_exe_descriptors_unique: 1854
fm_exe_descriptors_occurrences: 7538
editor_exe_descriptors_occurrences: 1854

## DATABASE:: 3-way diff
database_common: 293
database_fm_only: 28
database_editor_only: 0

## Brief-regex (DATABASE|db)@@ union
regex_descriptors_fm: 321
regex_descriptors_editor: 293
regex_unique_classes_fm: 321
regex_unique_classes_editor: 293
regex_common: 293
regex_fm_only: 28
regex_editor_only: 0

## Literal-DATABASE-named classes 3-way diff
database_named_common: 9
database_named_fm_only: 16
database_named_editor_only: 11

## Entropy / packing finding
fm_max_section_entropy: 7.9442
editor_max_section_entropy: 7.9862
fm_largest_section: .arch (377772544 B, entropy 6.7811)
fm_high_entropy_sections_ge_7.2: 2
editor_high_entropy_sections_ge_7.2: 1
fm_wx_sections: ['.arch', '.xtext']
packing_verdict: NOT packed / NOT encrypted — plaintext RTTI, filenames and 4CC literals are directly readable in both binaries (no Denuvo/SteamStub-style encrypted code section).

## Deliverables
scratch/t141/out/fm_vs_editor_diff.json
scratch/t141/out/REPORT.md
scratch/t141/out/DONE.md
scripts/t141_fm_vs_editor_diff.py

--selftest PASS
