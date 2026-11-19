# Pi session migration to C drive

Status: `partial_copy_verified_sources_retained`. Source session files are retained.

- Source: `D:\tmp2b\fm24-db\scratch\t02\pi-sessions`
- Pi default target: `C:\Users\oak\.pi\agent\sessions\--D--tmp2b-fm24-db--`
- Project sessions in source snapshot: 64

## Result Counts

- `copied_verified`: 58
- `skipped_active`: 6

## Safety

Files were copied, then SHA-256 verified against the source before being made visible at the target path.
Existing destination conflicts were not overwritten. Sessions identified as active were skipped.
No D-drive source file was deleted.
